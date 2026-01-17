#include "STGEnemy.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Kismet/GameplayStatics.h"
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

    // Mesh component
    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
    MeshComp->SetupAttachment(RootComponent);
    MeshComp->SetCollisionProfileName("NoCollision");
    
    // Load cube mesh
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
    GetWorldTimerManager().SetTimer(TimerHandle_Fire, this, &ASTGEnemy::Fire, 
                                    FireInterval, true, 0.5f);  // Start firing after 0.5s delay
    
    if (GEngine)
    {
        GEngine->AddOnScreenDebugMessage(-1, 2.0f, FColor::Orange, TEXT("Enemy spawned!"));
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
    
    SetActorLocation(NewLocation);

    // Check if enemy should despawn (moved off screen)
    if (NewLocation.X < DespawnY)
    {
        Destroy();
    }
}

void ASTGEnemy::Fire()
{
    if (GEngine)
    {
        GEngine->AddOnScreenDebugMessage(-1, 0.3f, FColor::Red, TEXT("Enemy FIRING!"));
    }
    
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
            Bullet->SetSpeed(EnemyBulletSpeed);
            Bullet->SetBulletColor(FLinearColor::Red);
        }
    }
}

void ASTGEnemy::HandleDamage(float DamageAmount)
{
    CurrentHealth -= DamageAmount;
    
    if (GEngine)
    {
        FString Msg = FString::Printf(TEXT("Enemy hit! Health: %d"), CurrentHealth);
        GEngine->AddOnScreenDebugMessage(-1, 0.5f, FColor::Yellow, Msg);
    }
    
    if (CurrentHealth <= 0)
    {
        // Award score to player
        ASTGPawn* Player = Cast<ASTGPawn>(UGameplayStatics::GetPlayerPawn(GetWorld(), 0));
        if (Player)
        {
            Player->AddScore(ScoreValue);
            if (GEngine)
            {
                FString Msg = FString::Printf(TEXT("Enemy destroyed! Score: %d"), Player->Score);
                GEngine->AddOnScreenDebugMessage(-1, 2.0f, FColor::Green, Msg);
            }
        }
        
        // Destroy enemy
        Destroy();
    }
}

void ASTGEnemy::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                                UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                                bool bFromSweep, const FHitResult& SweepResult)
{
    // Enemy collides with player - damage player
    if (OtherActor && OtherActor != this)
    {
        ASTGPawn* Player = Cast<ASTGPawn>(OtherActor);
        if (Player)
        {
            if (GEngine)
            {
                GEngine->AddOnScreenDebugMessage(-1, 1.0f, FColor::Red, TEXT("Player hit enemy! Both take damage!"));
            }
            Player->TakeHit(1);
            Destroy(); // Enemy dies on collision with player
        }
    }
}
