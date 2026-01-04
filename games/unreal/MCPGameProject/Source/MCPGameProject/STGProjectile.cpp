#include "STGProjectile.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "STGPawn.h"
#include "STGEnemy.h"
#include "STGEffects.h"
#include "Kismet/GameplayStatics.h"

ASTGProjectile::ASTGProjectile()
{
	// Use a sphere as a simple collision representation
	CollisionComp = CreateDefaultSubobject<USphereComponent>(TEXT("SphereComp"));
	CollisionComp->InitSphereRadius(8.0f);
	CollisionComp->SetCollisionProfileName("OverlapAllDynamic");
	CollisionComp->SetGenerateOverlapEvents(true);
	CollisionComp->OnComponentBeginOverlap.AddDynamic(this, &ASTGProjectile::OnOverlapBegin);

	// Players can't walk on it
	CollisionComp->SetWalkableSlopeOverride(FWalkableSlopeOverride(WalkableSlope_Unwalkable, 0.f));
	CollisionComp->CanCharacterStepUpOn = ECB_No;

	// Set as root component
	RootComponent = CollisionComp;

	// Visual mesh - use a sphere
	MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
	MeshComp->SetupAttachment(RootComponent);
	MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	
	// Load sphere mesh
	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
	if (SphereMesh.Succeeded())
	{
		MeshComp->SetStaticMesh(SphereMesh.Object);
		MeshComp->SetRelativeScale3D(FVector(0.15f, 0.15f, 0.15f)); // Small bullet
	}

	// Use a ProjectileMovementComponent to govern this projectile's movement
	ProjectileMovement = CreateDefaultSubobject<UProjectileMovementComponent>(TEXT("ProjectileComp"));
	ProjectileMovement->UpdatedComponent = CollisionComp;
	ProjectileMovement->InitialSpeed = 2000.f;
	ProjectileMovement->MaxSpeed = 2000.f;
	ProjectileMovement->bRotationFollowsVelocity = true;
	ProjectileMovement->bShouldBounce = false;
	ProjectileMovement->ProjectileGravityScale = 0.f; // No gravity

	// Die after 5 seconds by default
	InitialLifeSpan = 5.0f;
	
	bIsPlayerBullet = true;
	Damage = 1.0f;
	BulletColor = FLinearColor::Green;
	DynamicMaterial = nullptr;
}

void ASTGProjectile::BeginPlay()
{
	Super::BeginPlay();

	// Create dynamic material for color changing
	if (MeshComp && MeshComp->GetStaticMesh())
	{
		DynamicMaterial = MeshComp->CreateAndSetMaterialInstanceDynamic(0);
		if (DynamicMaterial)
		{
			// Set emissive color based on bullet type
			if (bIsPlayerBullet)
			{
				DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor::Green);
				DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::Green * 5.0f);
			}
			else
			{
				DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor::Red);
				DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::Red * 5.0f);
			}
		}
	}
}

void ASTGProjectile::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}

void ASTGProjectile::OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit)
{
	// Only add impulse and destroy projectile if we hit a physics
	if ((OtherActor != nullptr) && (OtherActor != this) && (OtherComp != nullptr) && OtherComp->IsSimulatingPhysics())
	{
		OtherComp->AddImpulseAtLocation(GetVelocity() * 100.0f, GetActorLocation());
		Destroy();
	}
}

void ASTGProjectile::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if ((OtherActor != nullptr) && (OtherActor != this) && (OtherActor != GetOwner()))
	{
		// Bullet vs Bullet
		ASTGProjectile* OtherProjectile = Cast<ASTGProjectile>(OtherActor);
		if (OtherProjectile)
		{
			// If opposite teams, destroy both
			if (bIsPlayerBullet != OtherProjectile->bIsPlayerBullet)
			{
				// Spawn hit effect at collision point
				FVector HitLocation = (GetActorLocation() + OtherProjectile->GetActorLocation()) / 2.0f;
				
				UWorld* World = GetWorld();
				if (World)
				{
					ASTGHitEffect* HitEffect = World->SpawnActor<ASTGHitEffect>(ASTGHitEffect::StaticClass(), HitLocation, FRotator::ZeroRotator);
					if (HitEffect)
					{
						HitEffect->SparkColor = FLinearColor::White;
					}
				}
				
				OtherProjectile->Destroy();
				Destroy();
			}
			return;
		}

		// Player Bullet vs Enemy
		if (bIsPlayerBullet)
		{
			ASTGEnemy* Enemy = Cast<ASTGEnemy>(OtherActor);
			if (Enemy)
			{
				// Spawn hit effect
				UWorld* World = GetWorld();
				if (World)
				{
					ASTGHitEffect* HitEffect = World->SpawnActor<ASTGHitEffect>(ASTGHitEffect::StaticClass(), GetActorLocation(), FRotator::ZeroRotator);
					if (HitEffect)
					{
						HitEffect->SparkColor = FLinearColor::Yellow;
					}
				}
				
				Enemy->HandleDamage(Damage);
				Destroy();
			}
		}
		// Enemy Bullet vs Player
		else
		{
			ASTGPawn* Player = Cast<ASTGPawn>(OtherActor);
			if (Player)
			{
				Player->HandleDamage(Damage);
				Destroy();
			}
		}
	}
}

void ASTGProjectile::SetBulletColor(FLinearColor InColor)
{
	BulletColor = InColor;
	if (DynamicMaterial)
	{
		DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), InColor);
		DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), InColor * 5.0f);
	}
}

void ASTGProjectile::SetSpeed(float InSpeed)
{
	if (ProjectileMovement)
	{
		ProjectileMovement->InitialSpeed = InSpeed;
		ProjectileMovement->MaxSpeed = InSpeed;
		ProjectileMovement->Velocity = GetActorForwardVector() * InSpeed;
	}
}

