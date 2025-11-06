#include "ShootEmUpEnemy.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "DrawDebugHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"
#include "ShootEmUpProjectile.h"
#include "ShootEmUpPlayerPawn.h"
#include "ShootEmUpGameMode.h"
#include "UObject/ConstructorHelpers.h"

AShootEmUpEnemy::AShootEmUpEnemy()
{
    PrimaryActorTick.bCanEverTick = true;

    CollisionComponent = CreateDefaultSubobject<USphereComponent>(TEXT("Collision"));
    SetRootComponent(CollisionComponent);
    CollisionComponent->InitSphereRadius(40.0f);
    CollisionComponent->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    CollisionComponent->SetCollisionResponseToAllChannels(ECR_Overlap);
    CollisionComponent->OnComponentBeginOverlap.AddDynamic(this, &AShootEmUpEnemy::OnEnemyOverlap);

    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    MeshComponent->SetupAttachment(RootComponent);
    MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);

    static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshA(TEXT("/Engine/BasicShapes/Cone.Cone"));
    static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshB(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
    static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshC(TEXT("/Engine/BasicShapes/Sphere.Sphere"));
    static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshD(TEXT("/Engine/BasicShapes/Cube.Cube"));
    static ConstructorHelpers::FObjectFinder<UMaterialInterface> Material(TEXT("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"));
    MeshTypeA = MeshA.Succeeded() ? MeshA.Object : nullptr;
    MeshTypeB = MeshB.Succeeded() ? MeshB.Object : nullptr;
    MeshTypeC = MeshC.Succeeded() ? MeshC.Object : nullptr;
    MeshTypeD = MeshD.Succeeded() ? MeshD.Object : nullptr;
    BaseMaterial = Material.Succeeded() ? Material.Object : nullptr;
    if (MeshTypeA)
    {
        MeshComponent->SetStaticMesh(MeshTypeA);
    }
    if (BaseMaterial)
    {
        MeshComponent->SetMaterial(0, BaseMaterial);
    }

    MoveSpeed = 250.0f;
    MaxHealth = 5;
    ShootInterval = 1.5f;
    ScoreValue = 100;
    BulletDamage = 1.0f;
    BulletSpeed = 800.0f;
    Lifetime = 120.0f;

    TimeSinceLastShot = 0.0f;
    CurrentHealth = MaxHealth;
    Archetype = EEnemyArchetype::TypeA;
    TimeAlive = 0.0f;
    HorizontalPhase = FMath::FRandRange(0.f, 360.f);
}

void AShootEmUpEnemy::BeginPlay()
{
    Super::BeginPlay();

    CurrentHealth = MaxHealth;
    CachedGameMode = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this));
    ConfigureAppearance();

    if (Lifetime > 0.f)
    {
        SetLifeSpan(Lifetime);
    }
}

void AShootEmUpEnemy::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    TimeSinceLastShot += DeltaSeconds;
    TimeAlive += DeltaSeconds;

    const FVector DesiredVelocity = ComputeDesiredVelocity(DeltaSeconds);
    if (!DesiredVelocity.IsNearlyZero())
    {
        const FVector NewLocation = GetActorLocation() + DesiredVelocity * DeltaSeconds;
        FVector ClampedLocation = NewLocation;
        ClampedLocation.Z = 0.f;
        SetActorLocation(ClampedLocation);
    }

    HandleShooting(DeltaSeconds);
}

void AShootEmUpEnemy::SetArchetype(EEnemyArchetype InType)
{
    Archetype = InType;
    ConfigureAppearance();
}

void AShootEmUpEnemy::HandleProjectileImpact(float IncomingDamage, AShootEmUpProjectile* FromProjectile)
{
    CurrentHealth -= FMath::RoundToInt(IncomingDamage);
    if (CurrentHealth <= 0)
    {
        if (CachedGameMode.IsValid())
        {
            CachedGameMode->NotifyEnemyKilled(this);
        }
        DrawDebugSphere(GetWorld(), GetActorLocation(), 120.f, 24, FColor::Orange, false, 0.6f, 0, 2.f);
        RequestDestroy();
    }
}

void AShootEmUpEnemy::SetPlayerReference(APawn* InPlayer)
{
    PlayerPawn = InPlayer;
}

FVector AShootEmUpEnemy::ComputeDesiredVelocity(float DeltaSeconds)
{
    const FVector CurrentLocation = GetActorLocation();
    FVector DesiredVelocity = FVector::ZeroVector;

    const FVector CenterLocation(0.f, 0.f, CurrentLocation.Z);
    FVector ToCenter = CenterLocation - CurrentLocation;
    ToCenter.Z = 0.f;
    const FVector Bias = ToCenter * 0.4f;

    switch (Archetype)
    {
    case EEnemyArchetype::TypeA:
    {
        const FVector Down = FVector(0.f, -1.f, 0.f) * MoveSpeed;
        DesiredVelocity = Down + Bias;
        break;
    }
    case EEnemyArchetype::TypeB:
    {
        const float Phase = FMath::DegreesToRadians(HorizontalPhase + TimeAlive * 160.f);
        const FVector Wave(FMath::Sin(Phase) * MoveSpeed * 0.7f, -MoveSpeed * 0.8f + FMath::Cos(Phase) * MoveSpeed * 0.5f, 0.f);
        DesiredVelocity = Wave + Bias;
        break;
    }
    case EEnemyArchetype::TypeC:
    {
        const float Phase = FMath::DegreesToRadians(TimeAlive * 220.f);
        const FVector Spiral(FMath::Cos(Phase) * MoveSpeed, -MoveSpeed * 0.4f + FMath::Sin(Phase) * MoveSpeed * 0.6f, 0.f);
        DesiredVelocity = Spiral + Bias * 0.5f;
        break;
    }
    case EEnemyArchetype::TypeD:
    {
        const float InwardFactor = FMath::Clamp(TimeAlive / 6.f, 0.f, 1.f);
        const FVector DownFast = FVector(0.f, -MoveSpeed * (1.f + InwardFactor), 0.f);
        const float Phase = FMath::DegreesToRadians(HorizontalPhase + TimeAlive * 240.f);
        const FVector Swirl(FMath::Sin(Phase) * MoveSpeed * 1.3f, FMath::Cos(Phase) * MoveSpeed * 1.3f, 0.f);
        DesiredVelocity = DownFast + Swirl + Bias * 0.6f;
        break;
    }
    default:
        DesiredVelocity = FVector(0.f, -MoveSpeed, 0.f) + Bias;
        break;
    }

    DesiredVelocity.Z = 0.f;
    return DesiredVelocity;
}

void AShootEmUpEnemy::ConfigureAppearance()
{
    UMaterialInstanceDynamic* DynMat = MeshComponent->CreateAndSetMaterialInstanceDynamic(0);
    if (!DynMat)
    {
        return;
    }

    switch (Archetype)
    {
    case EEnemyArchetype::TypeA:
        if (MeshTypeA)
        {
            MeshComponent->SetStaticMesh(MeshTypeA);
        }
        DynMat->SetVectorParameterValue(TEXT("Color"), FLinearColor::Red);
        MeshComponent->SetRelativeScale3D(FVector(0.7f, 0.7f, 1.2f));
        MoveSpeed = 220.f;
        ShootInterval = 1.4f;
        BulletSpeed = 900.f;
        BulletDamage = 1.0f;
        ScoreValue = 120;
        break;
    case EEnemyArchetype::TypeB:
        if (MeshTypeB)
        {
            MeshComponent->SetStaticMesh(MeshTypeB);
        }
        DynMat->SetVectorParameterValue(TEXT("Color"), FLinearColor::Green);
        MeshComponent->SetRelativeScale3D(FVector(0.9f, 0.6f, 1.5f));
        MoveSpeed = 260.f;
        ShootInterval = 1.0f;
        BulletSpeed = 1100.f;
        BulletDamage = 1.2f;
        ScoreValue = 160;
        break;
    case EEnemyArchetype::TypeC:
        if (MeshTypeC)
        {
            MeshComponent->SetStaticMesh(MeshTypeC);
        }
        DynMat->SetVectorParameterValue(TEXT("Color"), FLinearColor::Blue);
        MeshComponent->SetRelativeScale3D(FVector(1.3f, 1.3f, 0.8f));
        MoveSpeed = 320.f;
        ShootInterval = 2.2f;
        BulletSpeed = 700.f;
        BulletDamage = 1.5f;
        ScoreValue = 200;
        break;
    case EEnemyArchetype::TypeD:
        if (MeshTypeD)
        {
            MeshComponent->SetStaticMesh(MeshTypeD);
        }
        DynMat->SetVectorParameterValue(TEXT("Color"), FLinearColor::Yellow);
        MeshComponent->SetRelativeScale3D(FVector(1.0f, 1.0f, 1.0f));
        MoveSpeed = 420.f;
        ShootInterval = 0.6f;
        BulletSpeed = 1400.f;
        BulletDamage = 1.5f;
        ScoreValue = 260;
        break;
    }
}

void AShootEmUpEnemy::HandleShooting(float DeltaSeconds)
{
    if (ShootInterval <= 0.f || !PlayerPawn.IsValid())
    {
        return;
    }

    if (TimeSinceLastShot < ShootInterval)
    {
        return;
    }

    const FVector EnemyLocation = GetActorLocation();
    FVector ToPlayer = FVector::ForwardVector;
    if (APawn* Player = PlayerPawn.Get())
    {
        ToPlayer = (Player->GetActorLocation() - EnemyLocation).GetSafeNormal();
    }

    switch (Archetype)
    {
    case EEnemyArchetype::TypeA:
        ShootDirectedAtPlayer(4, 6.f, BulletSpeed, BulletDamage, FLinearColor::Red);
        break;
    case EEnemyArchetype::TypeB:
        ShootRadialPattern(12, 180.f, BulletSpeed * 0.9f, BulletDamage, FLinearColor::Green);
        break;
    case EEnemyArchetype::TypeC:
        ShootDirectedAtPlayer(1, 2.f, BulletSpeed * 1.4f, BulletDamage * 1.5f, FLinearColor::Blue);
        break;
    case EEnemyArchetype::TypeD:
        ShootRadialPattern(24, 360.f, BulletSpeed * 1.2f, BulletDamage, FLinearColor::Yellow);
        ShootDirectedAtPlayer(8, 25.f, BulletSpeed, BulletDamage, FLinearColor::Yellow);
        break;
    }

    TimeSinceLastShot = 0.f;
}

void AShootEmUpEnemy::ShootRadialPattern(int32 BulletCount, float SpreadAngleDeg, float BulletSpeedLocal, float DamageScalar, const FLinearColor& ColorTint)
{
    if (!CachedGameMode.IsValid())
    {
        CachedGameMode = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this));
    }

    if (!CachedGameMode.IsValid())
    {
        return;
    }

    const FVector Origin = GetActorLocation();
    const float StepAngle = SpreadAngleDeg / FMath::Max(1, BulletCount);
    const float StartAngle = -SpreadAngleDeg * 0.5f;

    for (int32 Index = 0; Index < BulletCount; ++Index)
    {
        const float AngleDeg = StartAngle + StepAngle * Index;
        const float AngleRad = FMath::DegreesToRadians(AngleDeg);
        const FVector Direction(FMath::Sin(AngleRad), FMath::Cos(AngleRad), 0.0f);
        CachedGameMode->SpawnEnemyProjectile(Origin, Direction, BulletSpeedLocal, DamageScalar, ColorTint);
    }
}

void AShootEmUpEnemy::ShootDirectedAtPlayer(int32 BulletCount, float AngleVarianceDeg, float BulletSpeedLocal, float DamageScalar, const FLinearColor& ColorTint)
{
    if (!CachedGameMode.IsValid())
    {
        CachedGameMode = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this));
    }

    if (!CachedGameMode.IsValid() || !PlayerPawn.IsValid())
    {
        return;
    }

    const FVector Origin = GetActorLocation();
    const FVector ToPlayer = (PlayerPawn->GetActorLocation() - Origin).GetSafeNormal();

    for (int32 Index = 0; Index < BulletCount; ++Index)
    {
        const float RandomAngle = FMath::FRandRange(-AngleVarianceDeg, AngleVarianceDeg);
        const FRotator Rotator(0.f, RandomAngle, 0.f);
        const FVector Direction = Rotator.RotateVector(ToPlayer);
        CachedGameMode->SpawnEnemyProjectile(Origin, Direction, BulletSpeedLocal, DamageScalar, ColorTint);
    }
}

void AShootEmUpEnemy::RequestDestroy()
{
    if (CachedGameMode.IsValid())
    {
        CachedGameMode->RegisterEnemyDestroyed(this);
    }

    Destroy();
}

void AShootEmUpEnemy::OnEnemyOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    if (AShootEmUpPlayerPawn* Player = Cast<AShootEmUpPlayerPawn>(OtherActor))
    {
        Player->HandleProjectileImpact(BulletDamage, nullptr);
        HandleProjectileImpact(CurrentHealth, nullptr);
    }
}
