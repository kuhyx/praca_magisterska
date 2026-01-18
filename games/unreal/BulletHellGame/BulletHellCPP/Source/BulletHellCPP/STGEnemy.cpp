#include "STGEnemy.h"
#include "STGGameSettings.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Kismet/GameplayStatics.h"
#include "NiagaraFunctionLibrary.h"
#include "NiagaraComponent.h"
#include "STGProjectile.h"
#include "STGPawn.h"

ASTGEnemy::ASTGEnemy()
{
    PrimaryActorTick.bCanEverTick = true;

    // Root component
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

    // Collision component (create FIRST so it can receive overlaps)
    CollisionComp = CreateDefaultSubobject<UBoxComponent>(TEXT("CollisionComp"));
    CollisionComp->SetupAttachment(RootComponent);
    CollisionComp->SetBoxExtent(FVector(30.f, 30.f, 10.f));
    CollisionComp->SetCollisionProfileName("OverlapAllDynamic");
    CollisionComp->SetGenerateOverlapEvents(true);
    CollisionComp->OnComponentBeginOverlap.AddDynamic(this, &ASTGEnemy::OnOverlapBegin);

    // Mesh component - default to cube, will be changed per enemy type
    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
    MeshComp->SetupAttachment(RootComponent);
    MeshComp->SetCollisionProfileName("NoCollision");
    
    // Load default cube mesh (will be overridden in InitializeFromType)
    static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMesh(TEXT("/Engine/BasicShapes/Cube"));
    if (CubeMesh.Succeeded())
    {
        MeshComp->SetStaticMesh(CubeMesh.Object);
        MeshComp->SetRelativeScale3D(FVector(0.6f, 0.6f, 0.1f));
    }
}

void ASTGEnemy::BeginPlay()
{
    Super::BeginPlay();
    
    CurrentHealth = MaxHealth;
    StartY = GetActorLocation().Y;  // Store starting Y for wave pattern
    WaveSeed = FMath::FRand() * 1000.0f;
    ElapsedTime = 0.0f;

    // Start firing timer
    // Only start firing if this enemy type shoots bullets
    if (BulletsPerBurst > 0 && FireInterval > 0.0f)
    {
        GetWorldTimerManager().SetTimer(TimerHandle_Fire, this, &ASTGEnemy::Fire, 
                                        FireInterval, true, 0.5f);  // Start firing after 0.5s delay
    }
}

void ASTGEnemy::InitializeFromType(EEnemyType Type)
{
    EnemyType = Type;
    
    // Load cube mesh (all enemies use cube, but with different scales for distinct top-down shapes)
    UStaticMesh* CubeMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube"));
    
    // Create emissive material for bright, visible colors
    UMaterial* BaseMaterial = LoadObject<UMaterial>(nullptr, TEXT("/Engine/BasicShapes/BasicShapeMaterial"));
    UMaterialInstanceDynamic* DynMaterial = nullptr;
    if (BaseMaterial)
    {
        DynMaterial = UMaterialInstanceDynamic::Create(BaseMaterial, this);
        MeshComp->SetMaterial(0, DynMaterial);
    }
    
    switch (Type)
    {
    case EEnemyType::Fodder:
        // EASIEST - Very slow, NO bullets, 1 HP
        // Shape: Small circle (equal X/Y scale) - GREEN
        MaxHealth = STG::Enemy::Fodder::Health;
        ScoreValue = STG::Enemy::Fodder::ScoreValue;
        VerticalSpeed = STG::Enemy::Fodder::VerticalSpeed;
        HorizontalAmplitude = STG::Enemy::Fodder::HorizontalAmplitude;
        HorizontalFrequency = STG::Enemy::Fodder::HorizontalFrequency;
        FireInterval = STG::Enemy::Fodder::FireInterval;
        BulletsPerBurst = STG::Enemy::Fodder::BulletsPerBurst;
        BurstSpread = STG::Enemy::Fodder::BurstSpread;
        EnemyBulletSpeed = STG::Enemy::Fodder::BulletSpeed;
        if (CubeMesh) MeshComp->SetStaticMesh(CubeMesh);
        MeshComp->SetRelativeScale3D(FVector(0.25f, 0.25f, 0.05f));  // Tiny square
        if (DynMaterial) DynMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor(0.0f, 1.0f, 0.2f)); // Bright green
        break;
        
    case EEnemyType::Runner:
        // Fast but harmless - Quick, NO bullets, low HP
        // Shape: Diamond (rotated 45°) - CYAN
        MaxHealth = STG::Enemy::Runner::Health;
        ScoreValue = STG::Enemy::Runner::ScoreValue;
        VerticalSpeed = STG::Enemy::Runner::VerticalSpeed;
        HorizontalAmplitude = STG::Enemy::Runner::HorizontalAmplitude;
        HorizontalFrequency = STG::Enemy::Runner::HorizontalFrequency;
        FireInterval = STG::Enemy::Runner::FireInterval;
        BulletsPerBurst = STG::Enemy::Runner::BulletsPerBurst;
        BurstSpread = STG::Enemy::Runner::BurstSpread;
        EnemyBulletSpeed = STG::Enemy::Runner::BulletSpeed;
        if (CubeMesh) MeshComp->SetStaticMesh(CubeMesh);
        MeshComp->SetRelativeScale3D(FVector(0.35f, 0.35f, 0.05f));  // Small square
        MeshComp->SetRelativeRotation(FRotator(0.f, 45.f, 0.f));     // Rotated = diamond shape
        if (DynMaterial) DynMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor(0.0f, 0.9f, 1.0f)); // Cyan
        break;
        
    case EEnemyType::Turret:
        // Slow shooter - Slow, shoots lots, medium tanky
        // Shape: Square (axis-aligned) - ORANGE
        MaxHealth = STG::Enemy::Turret::Health;
        ScoreValue = STG::Enemy::Turret::ScoreValue;
        VerticalSpeed = STG::Enemy::Turret::VerticalSpeed;
        HorizontalAmplitude = STG::Enemy::Turret::HorizontalAmplitude;
        HorizontalFrequency = STG::Enemy::Turret::HorizontalFrequency;
        FireInterval = STG::Enemy::Turret::FireInterval;
        BulletsPerBurst = STG::Enemy::Turret::BulletsPerBurst;
        BurstSpread = STG::Enemy::Turret::BurstSpread;
        EnemyBulletSpeed = STG::Enemy::Turret::BulletSpeed;
        if (CubeMesh) MeshComp->SetStaticMesh(CubeMesh);
        MeshComp->SetRelativeScale3D(FVector(0.5f, 0.5f, 0.08f));   // Medium square
        if (DynMaterial) DynMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor(1.0f, 0.5f, 0.0f)); // Orange
        break;
        
    case EEnemyType::Tank:
        // HARDEST - Slow, bullet hell, very tanky
        // Shape: Large rectangle (wider than tall) - RED
        MaxHealth = STG::Enemy::Tank::Health;
        ScoreValue = STG::Enemy::Tank::ScoreValue;
        VerticalSpeed = STG::Enemy::Tank::VerticalSpeed;
        HorizontalAmplitude = STG::Enemy::Tank::HorizontalAmplitude;
        HorizontalFrequency = STG::Enemy::Tank::HorizontalFrequency;
        FireInterval = STG::Enemy::Tank::FireInterval;
        BulletsPerBurst = STG::Enemy::Tank::BulletsPerBurst;
        BurstSpread = STG::Enemy::Tank::BurstSpread;
        EnemyBulletSpeed = STG::Enemy::Tank::BulletSpeed;
        if (CubeMesh) MeshComp->SetStaticMesh(CubeMesh);
        MeshComp->SetRelativeScale3D(FVector(0.4f, 0.8f, 0.1f));    // Wide rectangle
        if (DynMaterial) DynMaterial->SetVectorParameterValue(TEXT("Color"), FLinearColor(1.0f, 0.1f, 0.1f)); // Red
        break;
    }
    
    CurrentHealth = MaxHealth;
    
    // Restart fire timer with new interval (if this enemy shoots)
    GetWorldTimerManager().ClearTimer(TimerHandle_Fire);
    if (BulletsPerBurst > 0 && FireInterval > 0.0f)
    {
        GetWorldTimerManager().SetTimer(TimerHandle_Fire, this, &ASTGEnemy::Fire, 
                                        FireInterval, true, 0.5f);
    }
}

void ASTGEnemy::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    ElapsedTime += DeltaTime;

    // Sinusoidal movement (wave pattern)
    FVector NewLocation = GetActorLocation();
    
    // Move downward (-X direction in top-down view)
    NewLocation.X -= VerticalSpeed * DeltaTime;
    
    // Horizontal sine wave (Y axis = left/right)
    float HorizontalOffset = HorizontalAmplitude * FMath::Sin(
        HorizontalFrequency * (ElapsedTime + WaveSeed)
    );
    NewLocation.Y = StartY + HorizontalOffset;
    
    // Clamp to horizontal boundaries
    NewLocation.Y = FMath::Clamp(NewLocation.Y, BoundsMinY, BoundsMaxY);
    
    SetActorLocation(NewLocation);

    // Check if enemy should despawn (moved off screen)
    if (NewLocation.X < DespawnY)
    {
        Destroy();
    }
}

void ASTGEnemy::Fire()
{
    // Fire radial burst of bullets
    for (int32 i = 0; i < BulletsPerBurst; i++)
    {
        // Calculate angle for this bullet in the burst (evenly distributed in 360 degrees)
        float AngleDeg = (BurstSpread / BulletsPerBurst) * i;
        float AngleRad = FMath::DegreesToRadians(AngleDeg);
        
        // Calculate direction vector (in X-Y plane for top-down)
        FVector Direction = FVector(
            FMath::Cos(AngleRad),
            FMath::Sin(AngleRad),
            0.0f
        );
        
        // Spawn location at enemy position (same Z level)
        FVector SpawnLocation = GetActorLocation();
        
        // Create rotation from direction
        FRotator SpawnRotation = Direction.Rotation();
        
        // Spawn bullet
        ASTGProjectile* Bullet = GetWorld()->SpawnActor<ASTGProjectile>(
            ASTGProjectile::StaticClass(),
            SpawnLocation,
            SpawnRotation
        );
        
        if (Bullet)
        {
            Bullet->bIsPlayerBullet = false;
            Bullet->BulletScale = STG::Enemy::BulletVisualScale;     // BIG visual - easy to see!
            Bullet->CollisionRadius = STG::Enemy::BulletCollisionRadius; // TINY hitbox - allows "grazing"
            Bullet->EmissiveIntensity = STG::Enemy::BulletEmissive;  // Bright glow
            Bullet->SetSpeed(EnemyBulletSpeed);
            Bullet->SetBulletColor(FLinearColor(1.0f, 0.3f, 0.1f)); // Orange-red
        }
    }
}

void ASTGEnemy::HandleDamage(float DamageAmount)
{
    CurrentHealth -= DamageAmount;
    
    // Spawn hit effect
    SpawnHitEffect();
    
    if (CurrentHealth <= 0)
    {
        // Award score to player
        ASTGPawn* Player = Cast<ASTGPawn>(UGameplayStatics::GetPlayerPawn(GetWorld(), 0));
        if (Player)
        {
            Player->AddScore(ScoreValue);
        }
        
        // Spawn death explosion
        SpawnDeathEffect();
        
        // Destroy enemy
        Destroy();
    }
}

void ASTGEnemy::SpawnHitEffect()
{
    if (HitEffect)
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(
            GetWorld(),
            HitEffect,
            GetActorLocation(),
            FRotator::ZeroRotator,
            FVector(1.0f),
            true,
            true,
            ENCPoolMethod::None,
            true
        );
    }
}

void ASTGEnemy::SpawnDeathEffect()
{
    if (DeathEffect)
    {
        UNiagaraComponent* NiagaraComp = UNiagaraFunctionLibrary::SpawnSystemAtLocation(
            GetWorld(),
            DeathEffect,
            GetActorLocation(),
            FRotator::ZeroRotator,
            FVector(1.0f),
            true,
            true,
            ENCPoolMethod::None,
            true
        );
        
        // Override particle count if component supports it
        if (NiagaraComp)
        {
            NiagaraComp->SetIntParameter(TEXT("SpawnCount"), DeathParticleCount);
        }
    }
}

void ASTGEnemy::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                                UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                                bool bFromSweep, const FHitResult& SweepResult)
{
    // Enemy collides with player
    if (OtherActor && OtherActor != this)
    {
        ASTGPawn* Player = Cast<ASTGPawn>(OtherActor);
        if (Player)
        {
            Player->TakeHit(1);
            Destroy(); // Enemy dies on collision with player
        }
    }
}
