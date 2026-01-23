#include "STGEnemySpawner.h"
#include "STGGameSettings.h"
#include "STGEnemy.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/CommandLine.h"

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
    
    // Check for --start-time=N flag for phased profiling
    FString CmdLine = FCommandLine::Get();
    FString StartTimeValue;
    if (FParse::Value(*CmdLine, TEXT("--start-time="), StartTimeValue) || 
        FParse::Value(*CmdLine, TEXT("-start-time="), StartTimeValue))
    {
        float StartTime = FCString::Atof(*StartTimeValue);
        if (StartTime > 0 && StartTime < GameDuration)
        {
            ElapsedTime = StartTime;
            // Update spawn interval to match the difficulty at this time
            CurrentSpawnInterval = CalculateSpawnInterval();
            UE_LOG(LogTemp, Warning, TEXT("EnemySpawner: Fast-forwarding to %.0f seconds"), StartTime);
        }
    }
    
    // Default to base C++ class if no Blueprint assigned
    if (!EnemyClass)
    {
        EnemyClass = ASTGEnemy::StaticClass();
    }
    
    // Spawn initial wave well INSIDE the visible play area
    for (int32 i = 0; i < 5; i++)
    {
        FVector SpawnLoc;
        SpawnLoc.X = STG::PlayArea::MaxX * 0.5f;  // Upper half of play area
        SpawnLoc.Y = FMath::FRandRange(STG::PlayArea::MinY * 0.8f, STG::PlayArea::MaxY * 0.8f);
        SpawnLoc.Z = 0.0f;
        
        ASTGEnemy* NewEnemy = GetWorld()->SpawnActor<ASTGEnemy>(
            EnemyClass,
            SpawnLoc,
            FRotator::ZeroRotator
        );
        
        if (NewEnemy)
        {
            NewEnemy->InitializeFromType(EEnemyType::Fodder);
        }
    }
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
        EnemyClass,
        SpawnLocation,
        SpawnRotation
    );
    
    if (NewEnemy)
    {
        // Randomly select enemy type based on game progress
        float GameProgress = ElapsedTime / GameDuration;
        EEnemyType Type = GetRandomEnemyType(GameProgress);
        NewEnemy->InitializeFromType(Type);
    }
}

float ASTGEnemySpawner::CalculateSpawnInterval()
{
    float GameProgress = ElapsedTime / GameDuration; // 0.0 to 1.0
    float TimeRemaining = GameDuration - ElapsedTime;
    
    // FINAL RUSH: Last 5 seconds = absolute chaos!
    if (TimeRemaining <= STG::Spawner::FinalRushDuration)
    {
        return STG::Spawner::FinalRushInterval;
    }
    
    // LINEAR PROGRESSION: Steady acceleration throughout the game
    // At 0%: BaseSpawnInterval (0.25s - already fast!)
    // At 100%: MinSpawnInterval (0.08s)
    float Interval = FMath::Lerp(BaseSpawnInterval, STG::Spawner::MinSpawnInterval, GameProgress);
    
    return FMath::Max(Interval, STG::Spawner::MinSpawnInterval);
}

FVector ASTGEnemySpawner::GetRandomSpawnLocation()
{
    // Spawn at top of screen, random Y position
    FVector SpawnLoc = GetActorLocation();
    SpawnLoc.Y = FMath::FRandRange(-SpawnAreaHalfWidth, SpawnAreaHalfWidth);
    SpawnLoc.X = STG::Spawner::SpawnX; // Top of play area (from settings)
    SpawnLoc.Z = 0.0f;
    
    return SpawnLoc;
}

EEnemyType ASTGEnemySpawner::GetRandomEnemyType(float GameProgress)
{
    // Difficulty progression: Easiest to Hardest
    // Fodder (1HP, no bullets) → Runner (fast, no bullets) → Turret (slow, shoots) → Tank (tanky, bullet hell)
    
    float Roll = FMath::FRand();
    
    if (GameProgress < 0.25f)
    {
        // First 25%: ALL Fodder - spam them everywhere!
        return EEnemyType::Fodder;
    }
    else if (GameProgress < 0.5f)
    {
        // 25-50%: Fodder (85%), Runner (15%) - still almost all fodder
        if (Roll < 0.85f) return EEnemyType::Fodder;
        return EEnemyType::Runner;
    }
    else if (GameProgress < 0.75f)
    {
        // 50-75%: Fodder (70%), Runner (20%), Turret (10%) - mostly fodder
        if (Roll < 0.7f) return EEnemyType::Fodder;
        if (Roll < 0.9f) return EEnemyType::Runner;
        return EEnemyType::Turret;
    }
    else
    {
        // 75-100%: Fodder (55%), Runner (20%), Turret (15%), Tank (10%)
        if (Roll < 0.55f) return EEnemyType::Fodder;
        if (Roll < 0.75f) return EEnemyType::Runner;
        if (Roll < 0.9f) return EEnemyType::Turret;
        return EEnemyType::Tank;
    }
}