#include "STGProjectile.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "STGPawn.h"
#include "STGEnemy.h"

ASTGProjectile::ASTGProjectile()
{
    PrimaryActorTick.bCanEverTick = true;

    // Collision sphere
    CollisionComp = CreateDefaultSubobject<USphereComponent>(TEXT("SphereComp"));
    CollisionComp->InitSphereRadius(5.0f);
    CollisionComp->SetCollisionProfileName("OverlapAllDynamic");
    CollisionComp->OnComponentBeginOverlap.AddDynamic(this, &ASTGProjectile::OnOverlapBegin);
    RootComponent = CollisionComp;

    // Visual mesh
    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
    MeshComp->SetupAttachment(CollisionComp);
    MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    
    static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
    if (SphereMesh.Succeeded())
    {
        MeshComp->SetStaticMesh(SphereMesh.Object);
        MeshComp->SetRelativeScale3D(FVector(0.1f, 0.1f, 0.1f));
    }

    // Projectile movement
    ProjectileMovement = CreateDefaultSubobject<UProjectileMovementComponent>(TEXT("ProjectileComp"));
    ProjectileMovement->UpdatedComponent = CollisionComp;
    ProjectileMovement->InitialSpeed = 1200.f;
    ProjectileMovement->MaxSpeed = 1200.f;
    ProjectileMovement->bRotationFollowsVelocity = true;
    ProjectileMovement->bShouldBounce = false;
    ProjectileMovement->ProjectileGravityScale = 0.0f;  // No gravity for top-down shooter!
}

void ASTGProjectile::BeginPlay()
{
    Super::BeginPlay();

    // Set lifetime here so Blueprint overrides of Lifetime variable work
    SetLifeSpan(Lifetime);

    // Create dynamic material for bullet color
    if (MeshComp)
    {
        DynamicMaterial = MeshComp->CreateAndSetMaterialInstanceDynamic(0);
        if (DynamicMaterial)
        {
            DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), BulletColor);
            DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), BulletColor * 3.0f);
        }
    }
}

void ASTGProjectile::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void ASTGProjectile::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                                     UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                                     bool bFromSweep, const FHitResult& SweepResult)
{
    if (OtherActor && OtherActor != this)
    {
        if (bIsPlayerBullet)
        {
            // Player bullet hits enemy
            ASTGEnemy* Enemy = Cast<ASTGEnemy>(OtherActor);
            if (Enemy)
            {
                Enemy->HandleDamage(Damage);
                Destroy();
            }
        }
        else
        {
            // Enemy bullet hits player
            ASTGPawn* Player = Cast<ASTGPawn>(OtherActor);
            if (Player)
            {
                Player->TakeHit(1);
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
        DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), BulletColor);
        DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), BulletColor * 3.0f);
    }
}

void ASTGProjectile::SetSpeed(float InSpeed)
{
    if (ProjectileMovement)
    {
        ProjectileMovement->InitialSpeed = InSpeed;
        ProjectileMovement->MaxSpeed = InSpeed;
    }
}
