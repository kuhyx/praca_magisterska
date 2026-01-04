#include "STGEnemy.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Kismet/GameplayStatics.h"
#include "STGProjectile.h"
#include "STGPawn.h"
#include "STGGameMode.h"
#include "STGEffects.h"

ASTGEnemy::ASTGEnemy()
{
	PrimaryActorTick.bCanEverTick = true;

	CollisionComp = CreateDefaultSubobject<UBoxComponent>(TEXT("CollisionComp"));
	CollisionComp->SetBoxExtent(FVector(40.f, 40.f, 40.f));
	CollisionComp->SetCollisionProfileName("OverlapAllDynamic");
	CollisionComp->SetGenerateOverlapEvents(true);
	CollisionComp->OnComponentBeginOverlap.AddDynamic(this, &ASTGEnemy::OnOverlapBegin);
	RootComponent = CollisionComp;

	MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
	MeshComp->SetupAttachment(RootComponent);
	MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);

	// Default stats
	EnemyType = EEnemyType::TypeA;
	Health = 3.0f;
	MaxHealth = 3.0f;
	MoveSpeed = 200.0f;
	FireRate = 1.5f;
	BulletsPerShot = 1;
	ScoreValue = 100;
	EnemyColor = FLinearColor::Red;
	
	SpawnTime = 0.0f;
	DynamicMaterial = nullptr;
	bHasEnteredPlayArea = false;
	SineOffset = 0.0f;
	OrbitAngle = 0.0f;
	BurstShotsRemaining = 0;
}

void ASTGEnemy::BeginPlay()
{
	Super::BeginPlay();

	SpawnTime = GetWorld()->GetTimeSeconds();
	InitialSpawnLocation = GetActorLocation();
	SineOffset = FMath::RandRange(0.0f, PI * 2.0f);
	OrbitAngle = FMath::RandRange(0.0f, PI * 2.0f);

	// Configure based on enemy type
	ConfigureForType();

	// Set initial target to center with some randomness
	TargetLocation = FVector(0.f, FMath::RandRange(-300.f, 300.f), GetActorLocation().Z);

	// Start firing if this enemy shoots
	if (FireRate > 0.0f && EnemyType != EEnemyType::TypeD)
	{
		float InitialDelay = FMath::RandRange(0.5f, 1.5f);
		GetWorldTimerManager().SetTimer(TimerHandle_Fire, this, &ASTGEnemy::Fire, FireRate, true, InitialDelay);
	}
}

void ASTGEnemy::ConfigureForType()
{
	UStaticMesh* MeshToUse = nullptr;
	FVector MeshScale = FVector(1.0f);

	switch (EnemyType)
	{
	case EEnemyType::TypeA: // Basic Grunt - Red Cube
		{
			static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMesh(TEXT("/Engine/BasicShapes/Cube"));
			if (CubeMesh.Succeeded()) MeshToUse = CubeMesh.Object;
			MeshScale = FVector(0.6f, 0.6f, 0.6f);
			EnemyColor = FLinearColor::Red;
			Health = MaxHealth = 2.0f;
			MoveSpeed = 250.0f;
			FireRate = 2.0f;
			BulletsPerShot = 1;
			ScoreValue = 100;
			CollisionComp->SetBoxExtent(FVector(30.f, 30.f, 30.f));
		}
		break;

	case EEnemyType::TypeB: // Wave Rider - Blue Sphere
		{
			static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
			if (SphereMesh.Succeeded()) MeshToUse = SphereMesh.Object;
			MeshScale = FVector(0.7f, 0.7f, 0.7f);
			EnemyColor = FLinearColor::Blue;
			Health = MaxHealth = 3.0f;
			MoveSpeed = 180.0f;
			FireRate = 1.2f;
			BulletsPerShot = 3;
			ScoreValue = 150;
			CollisionComp->SetBoxExtent(FVector(35.f, 35.f, 35.f));
		}
		break;

	case EEnemyType::TypeC: // Tracker - Yellow Cone
		{
			static ConstructorHelpers::FObjectFinder<UStaticMesh> ConeMesh(TEXT("/Engine/BasicShapes/Cone"));
			if (ConeMesh.Succeeded()) MeshToUse = ConeMesh.Object;
			MeshScale = FVector(0.5f, 0.5f, 0.8f);
			EnemyColor = FLinearColor::Yellow;
			Health = MaxHealth = 4.0f;
			MoveSpeed = 300.0f;
			FireRate = 0.8f;
			BulletsPerShot = 5; // Burst fire
			ScoreValue = 200;
			CollisionComp->SetBoxExtent(FVector(25.f, 25.f, 40.f));
		}
		break;

	case EEnemyType::TypeD: // Tank - Purple Cylinder (no shooting, tanky)
		{
			static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMesh(TEXT("/Engine/BasicShapes/Cylinder"));
			if (CylinderMesh.Succeeded()) MeshToUse = CylinderMesh.Object;
			MeshScale = FVector(1.0f, 1.0f, 0.8f);
			EnemyColor = FLinearColor(0.5f, 0.0f, 0.8f); // Purple
			Health = MaxHealth = 10.0f;
			MoveSpeed = 100.0f;
			FireRate = 0.0f; // No shooting
			BulletsPerShot = 0;
			ScoreValue = 300;
			CollisionComp->SetBoxExtent(FVector(50.f, 50.f, 40.f));
		}
		break;
	}

	if (MeshToUse && MeshComp)
	{
		MeshComp->SetStaticMesh(MeshToUse);
		MeshComp->SetRelativeScale3D(MeshScale);
		
		// Create dynamic material
		DynamicMaterial = MeshComp->CreateAndSetMaterialInstanceDynamic(0);
		if (DynamicMaterial)
		{
			DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), EnemyColor);
			DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), EnemyColor * 2.0f);
		}
	}
}

void ASTGEnemy::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	UpdateMovement(DeltaTime);
}

void ASTGEnemy::UpdateMovement(float DeltaTime)
{
	FVector CurrentLocation = GetActorLocation();
	FVector Direction = FVector::ZeroVector;
	float TimeSinceSpawn = GetWorld()->GetTimeSeconds() - SpawnTime;
	
	// Bias towards center
	FVector ToCenter = (FVector(0.f, 0.f, CurrentLocation.Z) - CurrentLocation);
	float DistanceToCenter = ToCenter.Size2D();
	FVector CenterBias = ToCenter.GetSafeNormal2D() * FMath::Clamp(DistanceToCenter / 500.0f, 0.0f, 1.0f) * 0.3f;

	switch (EnemyType)
	{
	case EEnemyType::TypeA: // Straight down with slight horizontal movement
		{
			Direction = FVector(-1.f, 0.f, 0.f); // Move down (negative X)
			Direction += CenterBias;
		}
		break;

	case EEnemyType::TypeB: // Sine wave pattern
		{
			float SineValue = FMath::Sin((TimeSinceSpawn + SineOffset) * 3.0f);
			Direction = FVector(-0.7f, SineValue * 0.7f, 0.f);
			Direction += CenterBias * 0.5f;
		}
		break;

	case EEnemyType::TypeC: // Seek player
		{
			APawn* PlayerPawn = UGameplayStatics::GetPlayerPawn(this, 0);
			if (PlayerPawn)
			{
				FVector ToPlayer = (PlayerPawn->GetActorLocation() - CurrentLocation);
				Direction = ToPlayer.GetSafeNormal2D();
			}
			else
			{
				Direction = FVector(-1.f, 0.f, 0.f);
			}
			Direction += CenterBias * 0.2f;
		}
		break;

	case EEnemyType::TypeD: // Slow descent, slight orbit
		{
			OrbitAngle += DeltaTime * 0.5f;
			Direction = FVector(-0.5f, FMath::Sin(OrbitAngle) * 0.3f, 0.f);
			Direction += CenterBias;
		}
		break;
	}

	Direction = Direction.GetSafeNormal();
	AddActorWorldOffset(Direction * MoveSpeed * DeltaTime);

	// Mark as entered play area after moving a bit
	if (!bHasEnteredPlayArea && CurrentLocation.X < 800.0f)
	{
		bHasEnteredPlayArea = true;
	}

	// Destroy if too far off screen (below play area)
	if (GetActorLocation().X < -1500.0f)
	{
		Destroy();
	}
}

void ASTGEnemy::Fire()
{
	if (EnemyType == EEnemyType::TypeD) return; // Type D doesn't shoot

	UWorld* World = GetWorld();
	if (!World) return;

	FVector SpawnLocation = GetActorLocation();
	
	// Get player location for aiming
	APawn* PlayerPawn = UGameplayStatics::GetPlayerPawn(this, 0);
	FVector PlayerLocation = PlayerPawn ? PlayerPawn->GetActorLocation() : FVector(-500.f, 0.f, 0.f);
	FVector ToPlayer = (PlayerLocation - SpawnLocation).GetSafeNormal();
	FRotator BaseRotation = ToPlayer.Rotation();

	switch (EnemyType)
	{
	case EEnemyType::TypeA: // Single aimed shot
		{
			FActorSpawnParameters SpawnParams;
			SpawnParams.Owner = this;
			ASTGProjectile* Projectile = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), SpawnLocation, BaseRotation, SpawnParams);
			if (Projectile)
			{
				Projectile->bIsPlayerBullet = false;
				Projectile->SetSpeed(800.0f);
			}
		}
		break;

	case EEnemyType::TypeB: // 3-way spread
		{
			for (int32 i = -1; i <= 1; i++)
			{
				FRotator SpreadRot = BaseRotation + FRotator(0.f, i * 15.0f, 0.f);
				FActorSpawnParameters SpawnParams;
				SpawnParams.Owner = this;
				ASTGProjectile* Projectile = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), SpawnLocation, SpreadRot, SpawnParams);
				if (Projectile)
				{
					Projectile->bIsPlayerBullet = false;
					Projectile->SetSpeed(600.0f);
				}
			}
		}
		break;

	case EEnemyType::TypeC: // Burst fire (5 rapid shots)
		{
			BurstShotsRemaining = 5;
			GetWorldTimerManager().SetTimer(TimerHandle_BurstFire, [this, World, SpawnLocation, BaseRotation]()
			{
				if (BurstShotsRemaining > 0 && !IsPendingKillPending())
				{
					FActorSpawnParameters SpawnParams;
					SpawnParams.Owner = this;
					
					// Slight random spread on each burst shot
					FRotator SpreadRot = BaseRotation + FRotator(0.f, FMath::RandRange(-5.f, 5.f), 0.f);
					ASTGProjectile* Projectile = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), SpawnLocation, SpreadRot, SpawnParams);
					if (Projectile)
					{
						Projectile->bIsPlayerBullet = false;
						Projectile->SetSpeed(1000.0f);
					}
					BurstShotsRemaining--;
				}
			}, 0.08f, true, 0.0f);
		}
		break;

	case EEnemyType::TypeD:
		// No shooting
		break;
	}
}

void ASTGEnemy::HandleDamage(float DamageAmount)
{
	Health -= DamageAmount;
	
	// Flash effect when hit
	if (DynamicMaterial)
	{
		DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::White * 10.0f);
		
		// Reset color after short delay
		FTimerHandle TimerHandle_Flash;
		GetWorldTimerManager().SetTimer(TimerHandle_Flash, [this]()
		{
			if (DynamicMaterial && !IsPendingKillPending())
			{
				DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), EnemyColor * 2.0f);
			}
		}, 0.05f, false);
	}
	
	if (Health <= 0.f)
	{
		// Add score to player
		ASTGPawn* PlayerPawn = Cast<ASTGPawn>(UGameplayStatics::GetPlayerPawn(this, 0));
		if (PlayerPawn)
		{
			PlayerPawn->AddScore(ScoreValue);
		}

		// Notify game mode
		ASTGGameMode* GameMode = Cast<ASTGGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
		if (GameMode)
		{
			GameMode->OnEnemyKilled();
		}

		// Spawn explosion effect
		UWorld* World = GetWorld();
		if (World)
		{
			FActorSpawnParameters SpawnParams;
			ASTGExplosionEffect* Explosion = World->SpawnActor<ASTGExplosionEffect>(ASTGExplosionEffect::StaticClass(), GetActorLocation(), FRotator::ZeroRotator, SpawnParams);
			if (Explosion)
			{
				Explosion->ExplosionColor = EnemyColor;
				Explosion->MaxScale = (EnemyType == EEnemyType::TypeD) ? 3.0f : 1.5f; // Bigger explosion for tanks
			}
		}

		// Destroy this enemy
		Destroy();
	}
}

void ASTGEnemy::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (OtherActor != nullptr && OtherActor != this)
	{
		// Check if we hit the player
		ASTGPawn* Player = Cast<ASTGPawn>(OtherActor);
		if (Player)
		{
			// Damage player on collision
			Player->HandleDamage(1.0f);
		}
	}
}

