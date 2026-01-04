#include "STGGameMode.h"
#include "STGEnemy.h"
#include "STGPawn.h"
#include "STGHUD.h"
#include "STGScrollingBackground.h"
#include "Kismet/GameplayStatics.h"

ASTGGameMode::ASTGGameMode()
{
	PrimaryActorTick.bCanEverTick = true;
	
	// Set default pawn and HUD
	DefaultPawnClass = ASTGPawn::StaticClass();
	HUDClass = ASTGHUD::StaticClass();
	
	GameDuration = 90.0f; // 1:30
	BaseSpawnRate = 2.5f;
	SpawnRate = BaseSpawnRate;
	CurrentPhase = 0;
	PhaseDuration = 22.5f; // 90/4 = 22.5 seconds per phase
	PhaseTimer = 0.0f;
	TotalEnemiesSpawned = 0;
	TotalEnemiesKilled = 0;
	bIsGameOver = false;
	bIsVictory = false;
	bTimerEnded = false;
	DifficultyMultiplier = 1.0f;
}

void ASTGGameMode::BeginPlay()
{
	Super::BeginPlay();
	TimeRemaining = GameDuration;
	
	// Spawn scrolling background
	UWorld* World = GetWorld();
	if (World)
	{
		World->SpawnActor<ASTGScrollingBackground>(ASTGScrollingBackground::StaticClass(), FVector(0.f, 0.f, -100.f), FRotator::ZeroRotator);
	}
	
	// Start spawning enemies after a short delay
	GetWorldTimerManager().SetTimer(TimerHandle_Spawn, this, &ASTGGameMode::SpawnEnemy, SpawnRate, true, 1.0f);
}

void ASTGGameMode::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsGameOver) return;

	// Update timer
	if (!bTimerEnded)
	{
		TimeRemaining -= DeltaTime;
		PhaseTimer += DeltaTime;

		// Update phase (introduce new enemy types over time)
		if (PhaseTimer >= PhaseDuration && CurrentPhase < 3)
		{
			CurrentPhase++;
			PhaseTimer = 0.0f;
		}

		// Update difficulty
		UpdateDifficulty();

		// Check if time's up
		if (TimeRemaining <= 0.f)
		{
			TimeRemaining = 0.f;
			bTimerEnded = true;
			
			// Stop spawning
			GetWorldTimerManager().ClearTimer(TimerHandle_Spawn);
		}
	}
	else
	{
		// Timer ended - check if all enemies are dead
		TArray<AActor*> Enemies;
		UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGEnemy::StaticClass(), Enemies);
		
		if (Enemies.Num() == 0)
		{
			Victory();
		}
	}
}

void ASTGGameMode::UpdateDifficulty()
{
	// Calculate progress (0 to 1)
	float Progress = 1.0f - (TimeRemaining / GameDuration);
	
	// Increase spawn rate over time (more enemies as game progresses)
	// Start at 2.5s between spawns, end at 0.3s
	float NewSpawnRate = FMath::Lerp(BaseSpawnRate, 0.3f, Progress);
	
	// Also increase difficulty multiplier for enemy stats
	DifficultyMultiplier = 1.0f + (Progress * 0.5f);
	
	// Only update timer if rate changed significantly
	if (FMath::Abs(NewSpawnRate - SpawnRate) > 0.1f)
	{
		SpawnRate = NewSpawnRate;
		GetWorldTimerManager().SetTimer(TimerHandle_Spawn, this, &ASTGGameMode::SpawnEnemy, SpawnRate, true);
	}
}

void ASTGGameMode::SpawnEnemy()
{
	if (bIsGameOver || bTimerEnded) return;

	UWorld* World = GetWorld();
	if (!World) return;

	FVector SpawnLocation = GetSpawnLocation();
	FRotator SpawnRotation(0.f, 180.f, 0.f); // Face player (negative X)

	// Determine enemy type based on phase
	EEnemyType TypeToSpawn = GetEnemyTypeForCurrentPhase();

	// Spawn the enemy
	ASTGEnemy* Enemy = World->SpawnActor<ASTGEnemy>(ASTGEnemy::StaticClass(), SpawnLocation, SpawnRotation);
	if (Enemy)
	{
		Enemy->EnemyType = TypeToSpawn;
		Enemy->ConfigureForType();
		
		// Apply difficulty multiplier
		Enemy->Health *= DifficultyMultiplier;
		Enemy->MaxHealth *= DifficultyMultiplier;
		
		TotalEnemiesSpawned++;
	}

	// Sometimes spawn additional enemies in later phases
	float Progress = 1.0f - (TimeRemaining / GameDuration);
	if (Progress > 0.5f && FMath::FRand() < 0.3f)
	{
		// Spawn a second enemy
		FVector SecondLocation = GetSpawnLocation();
		ASTGEnemy* SecondEnemy = World->SpawnActor<ASTGEnemy>(ASTGEnemy::StaticClass(), SecondLocation, SpawnRotation);
		if (SecondEnemy)
		{
			SecondEnemy->EnemyType = GetEnemyTypeForCurrentPhase();
			SecondEnemy->ConfigureForType();
			SecondEnemy->Health *= DifficultyMultiplier;
			SecondEnemy->MaxHealth *= DifficultyMultiplier;
			TotalEnemiesSpawned++;
		}
	}

	// In final stretch, sometimes spawn a third
	if (Progress > 0.8f && FMath::FRand() < 0.2f)
	{
		FVector ThirdLocation = GetSpawnLocation();
		ASTGEnemy* ThirdEnemy = World->SpawnActor<ASTGEnemy>(ASTGEnemy::StaticClass(), ThirdLocation, SpawnRotation);
		if (ThirdEnemy)
		{
			ThirdEnemy->EnemyType = GetEnemyTypeForCurrentPhase();
			ThirdEnemy->ConfigureForType();
			ThirdEnemy->Health *= DifficultyMultiplier;
			ThirdEnemy->MaxHealth *= DifficultyMultiplier;
			TotalEnemiesSpawned++;
		}
	}
}

FVector ASTGGameMode::GetSpawnLocation()
{
	// Spawn at top of screen (positive X) with bias toward center
	float SpawnX = 1200.f; // Off screen to the right/top
	
	// Y position: use gaussian-like distribution centered at 0
	float RandomY = FMath::RandRange(-1.0f, 1.0f);
	// Square it to bias toward center
	float BiasedY = FMath::Sign(RandomY) * FMath::Pow(FMath::Abs(RandomY), 0.7f);
	float SpawnY = BiasedY * 700.f;
	
	// Make sure enemy is at least partially visible (1 pixel) when spawning
	// by clamping spawn position
	SpawnY = FMath::Clamp(SpawnY, -750.f, 750.f);
	
	return FVector(SpawnX, SpawnY, 0.f);
}

EEnemyType ASTGGameMode::GetEnemyTypeForCurrentPhase()
{
	// Progressive introduction:
	// Phase 0: Only Type A
	// Phase 1: Type A and B
	// Phase 2: Type A, B, and C
	// Phase 3: All types
	
	float Rand = FMath::FRand();
	
	switch (CurrentPhase)
	{
	case 0:
		return EEnemyType::TypeA;
		
	case 1:
		return (Rand < 0.6f) ? EEnemyType::TypeA : EEnemyType::TypeB;
		
	case 2:
		if (Rand < 0.4f) return EEnemyType::TypeA;
		if (Rand < 0.7f) return EEnemyType::TypeB;
		return EEnemyType::TypeC;
		
	case 3:
	default:
		if (Rand < 0.3f) return EEnemyType::TypeA;
		if (Rand < 0.55f) return EEnemyType::TypeB;
		if (Rand < 0.8f) return EEnemyType::TypeC;
		return EEnemyType::TypeD;
	}
}

void ASTGGameMode::OnEnemyKilled()
{
	TotalEnemiesKilled++;
}

void ASTGGameMode::OnPlayerDied()
{
	GameOver();
}

void ASTGGameMode::GameOver()
{
	if (bIsGameOver) return;
	
	bIsGameOver = true;
	bIsVictory = false;
	
	// Stop spawning
	GetWorldTimerManager().ClearTimer(TimerHandle_Spawn);
	
	// Clear all enemies and bullets
	TArray<AActor*> Enemies;
	UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGEnemy::StaticClass(), Enemies);
	for (AActor* Actor : Enemies)
	{
		Actor->Destroy();
	}
}

void ASTGGameMode::Victory()
{
	if (bIsGameOver) return;
	
	bIsGameOver = true;
	bIsVictory = true;
}

