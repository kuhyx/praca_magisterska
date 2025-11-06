#include "ShootEmUpPlayerPawn.h"
#include "ShootEmUpProjectile.h"
#include "ShootEmUpGameMode.h"
#include "DrawDebugHelpers.h"
#include "Materials/MaterialInterface.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/FloatingPawnMovement.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "UObject/ConstructorHelpers.h"

AShootEmUpPlayerPawn::AShootEmUpPlayerPawn()
{
    PrimaryActorTick.bCanEverTick = true;

    CollisionComponent = CreateDefaultSubobject<USphereComponent>(TEXT("Collision"));
    SetRootComponent(CollisionComponent);
    CollisionComponent->InitSphereRadius(1.0f);
    CollisionComponent->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    CollisionComponent->SetCollisionProfileName(TEXT("Pawn"));
    CollisionComponent->SetGenerateOverlapEvents(true);

    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    MeshComponent->SetupAttachment(RootComponent);
    MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    MeshComponent->SetRelativeScale3D(FVector(0.5f, 1.2f, 0.4f));

    static ConstructorHelpers::FObjectFinder<UStaticMesh> ConeMesh(TEXT("/Engine/BasicShapes/Cone.Cone"));
    static ConstructorHelpers::FObjectFinder<UMaterialInterface> BaseMaterial(TEXT("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"));
    if (ConeMesh.Succeeded())
    {
        MeshComponent->SetStaticMesh(ConeMesh.Object);
        MeshComponent->SetRelativeRotation(FRotator(90.f, 0.f, 0.f));
    }
    if (BaseMaterial.Succeeded())
    {
        MeshComponent->SetMaterial(0, BaseMaterial.Object);
    }

    MovementComponent = CreateDefaultSubobject<UFloatingPawnMovement>(TEXT("Movement"));
    MovementComponent->MaxSpeed = 1200.0f;

    SpringArmComponent = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArmComponent->SetupAttachment(RootComponent);
    SpringArmComponent->TargetOffset = FVector(0.f, 0.f, 500.f);
    SpringArmComponent->SetRelativeRotation(FRotator(-90.f, 0.f, 0.f));
    SpringArmComponent->bDoCollisionTest = false;

    CameraComponent = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    CameraComponent->SetupAttachment(SpringArmComponent, USpringArmComponent::SocketName);
    CameraComponent->ProjectionMode = ECameraProjectionMode::Orthographic;
    CameraComponent->OrthoWidth = 2200.f;

    FireInterval = 0.15f;
    ProjectileSpeed = 2200.f;
    ProjectileDamage = 1.0f;
    MaxLives = 2;
    HitInvulnerabilityDuration = 1.5f;
    ArenaHalfWidth = 1200.f;
    ArenaHalfHeight = 1800.f;

    bIsFiring = false;
    bSpecialUsed = false;

    Score = 0;
    PlayerLevel = 1;
    LivesRemaining = MaxLives;
    InvulnerabilityTimer = 0.f;
    LevelUpFlashTimer = 0.f;

    AutoPossessPlayer = EAutoReceiveInput::Player0;
    PlayerMaterial = nullptr;
}

void AShootEmUpPlayerPawn::BeginPlay()
{
    Super::BeginPlay();

    CachedGameMode = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this));
    if (UStaticMeshComponent* Mesh = MeshComponent)
    {
        PlayerMaterial = Mesh->CreateAndSetMaterialInstanceDynamic(0);
        if (PlayerMaterial)
        {
            PlayerMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor::White);
        }
    }

    if (!PlayerProjectileClass)
    {
        PlayerProjectileClass = AShootEmUpProjectile::StaticClass();
    }
}

void AShootEmUpPlayerPawn::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    if (!MoveInput.IsNearlyZero())
    {
        MovementComponent->AddInputVector(MoveInput);
    }

    FVector Location = GetActorLocation();
    Location.X = FMath::Clamp(Location.X, -ArenaHalfWidth, ArenaHalfWidth);
    Location.Y = FMath::Clamp(Location.Y, -ArenaHalfHeight, ArenaHalfHeight);
    Location.Z = FMath::Clamp(Location.Z, -50.f, 50.f);
    SetActorLocation(Location);

    if (InvulnerabilityTimer > 0.f)
    {
        InvulnerabilityTimer -= DeltaSeconds;
    }

    if (LevelUpFlashTimer > 0.f)
    {
        LevelUpFlashTimer -= DeltaSeconds;
        if (LevelUpFlashTimer <= 0.f)
        {
                if (PlayerMaterial)
                {
                    PlayerMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor::White);
                }
        }
    }

    UpdateVisuals(DeltaSeconds);
}

void AShootEmUpPlayerPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &AShootEmUpPlayerPawn::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &AShootEmUpPlayerPawn::MoveRight);
    PlayerInputComponent->BindAction(TEXT("Fire"), IE_Pressed, this, &AShootEmUpPlayerPawn::StartFiring);
    PlayerInputComponent->BindAction(TEXT("Fire"), IE_Released, this, &AShootEmUpPlayerPawn::StopFiring);
    PlayerInputComponent->BindAction(TEXT("Special"), IE_Pressed, this, &AShootEmUpPlayerPawn::PerformSpecial);
}

void AShootEmUpPlayerPawn::HandleProjectileImpact(float DamageAmount, AShootEmUpProjectile* FromProjectile)
{
    if (InvulnerabilityTimer > 0.f)
    {
        return;
    }

    LivesRemaining = FMath::Max(0, LivesRemaining - 1);
    InvulnerabilityTimer = HitInvulnerabilityDuration;

    DrawDebugSphere(GetWorld(), GetActorLocation(), 100.f, 20, FColor::Red, false, 0.5f, 0, 2.f);

    if (CachedGameMode.IsValid())
    {
        CachedGameMode->HandlePlayerDamaged(LivesRemaining);
    }

    if (LivesRemaining <= 0)
    {
        if (CachedGameMode.IsValid())
        {
            CachedGameMode->HandlePlayerDeath();
        }
    }
    else
    {
        if (CachedGameMode.IsValid())
        {
            CachedGameMode->HandlePlayerRespawnRequest();
        }
    }
}

void AShootEmUpPlayerPawn::NotifyEnemyDestroyed(int32 ScoreReward)
{
    Score += ScoreReward;
    if (CachedGameMode.IsValid())
    {
        CachedGameMode->HandleScoreUpdated(Score);
    }

    const int32 ExpectedLevel = FMath::Clamp(Score / 500 + 1, 1, 10);
    if (ExpectedLevel > PlayerLevel)
    {
        PlayerLevel = ExpectedLevel;
        LevelUp();
    }
}

void AShootEmUpPlayerPawn::ClearScreenSpecial()
{
    if (CachedGameMode.IsValid())
    {
        CachedGameMode->HandleScreenClearRequested();
    }
}

void AShootEmUpPlayerPawn::OnRespawn(const FVector& SpawnPoint)
{
    SetActorLocation(SpawnPoint);
    InvulnerabilityTimer = HitInvulnerabilityDuration;
    MoveInput = FVector::ZeroVector;
    if (MovementComponent)
    {
        MovementComponent->StopMovementImmediately();
    }
    if (PlayerMaterial)
    {
        PlayerMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor::White);
    }
}

void AShootEmUpPlayerPawn::MoveForward(float Value)
{
    MoveInput.Y = FMath::Clamp(Value, -1.f, 1.f);
}

void AShootEmUpPlayerPawn::MoveRight(float Value)
{
    MoveInput.X = FMath::Clamp(Value, -1.f, 1.f);
}

void AShootEmUpPlayerPawn::StartFiring()
{
    bIsFiring = true;
    FireOnce();
    GetWorldTimerManager().SetTimer(FireTimerHandle, this, &AShootEmUpPlayerPawn::FireOnce, FireInterval, true, FireInterval);
}

void AShootEmUpPlayerPawn::StopFiring()
{
    bIsFiring = false;
    GetWorldTimerManager().ClearTimer(FireTimerHandle);
}

void AShootEmUpPlayerPawn::FireOnce()
{
    if (!PlayerProjectileClass || !CachedGameMode.IsValid())
    {
        return;
    }

    const FVector SpawnLocation = GetActorLocation() + FVector(0.f, 50.f, 0.f);
    const TArray<FVector> Directions = BuildFireDirections();

    for (const FVector& Direction : Directions)
    {
        FActorSpawnParameters Params;
        Params.Owner = this;
        Params.Instigator = this;
        AShootEmUpProjectile* Projectile = GetWorld()->SpawnActor<AShootEmUpProjectile>(PlayerProjectileClass, SpawnLocation, Direction.Rotation(), Params);
        if (Projectile)
        {
            Projectile->InitProjectile(Direction, ProjectileSpeed, 4.0f, true, ProjectileDamage, FLinearColor::White);
        }
    }
}

void AShootEmUpPlayerPawn::PerformSpecial()
{
    if (bSpecialUsed)
    {
        return;
    }

    bSpecialUsed = true;
    ClearScreenSpecial();
    LevelUpFlashTimer = 1.0f;
    if (PlayerMaterial)
    {
        PlayerMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor::Purple);
    }

    DrawDebugSphere(GetWorld(), GetActorLocation(), 320.f, 24, FColor::Purple, false, 1.0f, 0, 4.f);
}

TArray<FVector> AShootEmUpPlayerPawn::BuildFireDirections() const
{
    TArray<FVector> Directions;
    const FVector ForwardDir(0.f, 1.f, 0.f);
    const FVector RightDir(1.f, 0.f, 0.f);

    switch (PlayerLevel)
    {
    case 1:
        Directions.Add(ForwardDir);
        break;
    case 2:
        Directions.Add(ForwardDir);
        Directions.Add((ForwardDir + RightDir * 0.25f).GetSafeNormal());
        Directions.Add((ForwardDir - RightDir * 0.25f).GetSafeNormal());
        break;
    case 3:
        Directions.Add(ForwardDir);
        Directions.Add((ForwardDir + RightDir * 0.35f).GetSafeNormal());
        Directions.Add((ForwardDir - RightDir * 0.35f).GetSafeNormal());
        Directions.Add(RightDir);
        Directions.Add(-RightDir);
        break;
    default:
        Directions.Add(ForwardDir);
        Directions.Add((ForwardDir + RightDir * 0.35f).GetSafeNormal());
        Directions.Add((ForwardDir - RightDir * 0.35f).GetSafeNormal());
        Directions.Add(RightDir);
        Directions.Add(-RightDir);
        Directions.Add(-ForwardDir);
        break;
    }

    return Directions;
}

void AShootEmUpPlayerPawn::LevelUp()
{
    LevelUpFlashTimer = 1.0f;
    if (PlayerMaterial)
    {
        PlayerMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor::MakeRandomColor());
    }

    DrawDebugSphere(GetWorld(), GetActorLocation(), 160.f, 16, FColor::Purple, false, 1.0f, 0, 3.f);

    if (CachedGameMode.IsValid())
    {
        CachedGameMode->HandlePlayerLevelUp(PlayerLevel);
    }
}

void AShootEmUpPlayerPawn::UpdateVisuals(float DeltaSeconds)
{
    // Reserved for future VFX hooks; keep function to host level-up flashes or damage flicker.
}
