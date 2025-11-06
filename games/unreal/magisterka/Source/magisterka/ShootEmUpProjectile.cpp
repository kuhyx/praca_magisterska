#include "ShootEmUpProjectile.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "ShootEmUpEnemy.h"
#include "ShootEmUpPlayerPawn.h"
#include "UObject/ConstructorHelpers.h"
#include "Engine/CollisionProfile.h"

AShootEmUpProjectile::AShootEmUpProjectile()
{
    PrimaryActorTick.bCanEverTick = true;

    CollisionComponent = CreateDefaultSubobject<USphereComponent>(TEXT("Collision"));
    SetRootComponent(CollisionComponent);
    CollisionComponent->InitSphereRadius(6.0f);
    CollisionComponent->SetCollisionProfileName(UCollisionProfile::Projectile_ProfileName);
    CollisionComponent->SetGenerateOverlapEvents(true);
    CollisionComponent->OnComponentBeginOverlap.AddDynamic(this, &AShootEmUpProjectile::OnProjectileOverlap);
    CollisionComponent->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    CollisionComponent->SetCollisionResponseToAllChannels(ECR_Overlap);

    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Visual"));
    MeshComponent->SetupAttachment(RootComponent);
    MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    MeshComponent->SetRelativeScale3D(FVector(0.2f));

    static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere.Sphere"));
    if (SphereMesh.Succeeded())
    {
        MeshComponent->SetStaticMesh(SphereMesh.Object);
    }

    MovementComponent = CreateDefaultSubobject<UProjectileMovementComponent>(TEXT("Movement"));
    MovementComponent->InitialSpeed = 2000.0f;
    MovementComponent->MaxSpeed = 4000.0f;
    MovementComponent->ProjectileGravityScale = 0.0f;
    MovementComponent->bRotationFollowsVelocity = true;

    DefaultSpeed = 1500.0f;
    DefaultLifeSpan = 5.0f;
    DefaultDamage = 1.0f;

    bFromPlayer = false;
    Damage = DefaultDamage;

    PrimaryActorTick.bCanEverTick = false;
}

void AShootEmUpProjectile::BeginPlay()
{
    Super::BeginPlay();

    if (!IsPendingKill())
    {
        SetLifeSpan(DefaultLifeSpan);
    }
}

void AShootEmUpProjectile::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
}

void AShootEmUpProjectile::InitProjectile(const FVector& Direction, float Speed, float LifeSeconds, bool bPlayerBullet, float InDamage, const FLinearColor& TintColor)
{
    bFromPlayer = bPlayerBullet;
    Damage = InDamage > 0.f ? InDamage : DefaultDamage;

    const FVector NormalizedDirection = Direction.GetSafeNormal(FVector::ForwardVector);
    MovementComponent->Velocity = NormalizedDirection * (Speed > 0.f ? Speed : DefaultSpeed);

    if (LifeSeconds > 0.f)
    {
        SetLifeSpan(LifeSeconds);
    }

    UMaterialInstanceDynamic* DynMat = MeshComponent->CreateAndSetMaterialInstanceDynamic(0);
    if (DynMat)
    {
        DynMat->SetVectorParameterValue(TEXT("Color"), TintColor);
    }
    else
    {
        MeshComponent->SetVectorParameterValueOnMaterials(TEXT("Color"), TintColor);
    }

    CollisionComponent->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
}

void AShootEmUpProjectile::OnProjectileOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    if (!OtherActor || OtherActor == this)
    {
        return;
    }

    if (AShootEmUpProjectile* OtherProjectile = Cast<AShootEmUpProjectile>(OtherActor))
    {
        Destroy();
        if (IsValid(OtherProjectile))
        {
            OtherProjectile->Destroy();
        }
        return;
    }

    if (bFromPlayer)
    {
        if (AShootEmUpEnemy* HitEnemy = Cast<AShootEmUpEnemy>(OtherActor))
        {
            HitEnemy->HandleProjectileImpact(Damage, this);
            Destroy();
        }
    }
    else
    {
        if (AShootEmUpPlayerPawn* Player = Cast<AShootEmUpPlayerPawn>(OtherActor))
        {
            Player->HandleProjectileImpact(Damage, this);
            Destroy();
        }
    }
}
