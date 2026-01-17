#include "STGEnemySpawner.h"
#include "STGEnemy.h"
#include "Kismet/GameplayStatics.h"

ASTGEnemySpawner::ASTGEnemySpawner()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ASTGEnemySpawner::BeginPlay()
{
    Super::BeginPlay();
    
    ElapsedTime = 0.0f;
    SpawnTimer = 0.0f;
    CurrentSpawnInterval = BaseSpawnInterval;
}

void ASTGEnemySpawner::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    if (!bSpawningActive)
        return;

    ElapsedTime += DeltaTime;

    // Stop spawning after game duration
    if (ElapsedTime >= GameDuration)
    {
        bSpawningActive = false;
        return;
    }

    // Update spawn interval based on difficulty curve
    CurrentSpawnInterval = CalculateSpawnInterval();

    // Spawn timer
    SpawnTimer -= DeltaTime;
    if (SpawnTimer <= 0.0f)
    {
        // Check enemy count
        TArray<AActor*> FoundEnemies;
        UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGEnemy::StaticClass(), FoundEnemies);
        
        if (FoundEnemies.Num() < MaxSimultaneousEnemies)
        {
            SpawnEnemy();
        }
        
        SpawnTimer = CurrentSpawnInterval;
    }
}

void ASTGEnemySpawner::SpawnEnemy()
{
    FVector SpawnLocation = GetRandomSpawnLocation();
    FRotator SpawnRotation = FRotator::ZeroRotator;

    ASTGEnemy* NewEnemy = GetWorld()->SpawnActor<ASTGEnemy>(
        ASTGEnemy::StaticClass(),
        SpawnLocation,
        SpawnRotation
    );
}

float ASTGEnemySpawner::CalculateSpawnInterval()
{
    // Difficulty curve: spawn faster as time progresses
    float GameProgress = ElapsedTime / GameDuration; // 0.0 to 1.0
    
    // Start at BaseSpawnInterval, reduce to 0.5 seconds at end
    float MinInterval = 0.5f;
    float Interval = FMath::Lerp(BaseSpawnInterval, MinInterval, GameProgress);
    
    return FMath::Max(Interval, MinInterval);
}

FVector ASTGEnemySpawner::GetRandomSpawnLocation()
{
    // Spawn at top of screen, random X position
    FVector SpawnLoc = GetActorLocation();
    SpawnLoc.Y = FMath::FRandRange(-SpawnAreaHalfWidth, SpawnAreaHalfWidth);
    SpawnLoc.X = 800.0f; // Top of play area
    SpawnLoc.Z = 0.0f;
    
    return SpawnLoc;
}