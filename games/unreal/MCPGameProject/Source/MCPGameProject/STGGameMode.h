#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "STGEnemy.h"
#include "STGGameMode.generated.h"

UCLASS()
class MCPGAMEPROJECT_API ASTGGameMode : public AGameModeBase
{
	GENERATED_BODY()
	
public:
	ASTGGameMode();

protected:
	virtual void BeginPlay() override;

public:
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game Rules")
	float GameDuration; // 90 seconds

	UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
	float TimeRemaining;

	UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
	bool bIsGameOver;

	UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
	bool bIsVictory;

	UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
	bool bTimerEnded;

	// Spawning
	FTimerHandle TimerHandle_Spawn;
	void SpawnEnemy();
	float SpawnRate;
	float BaseSpawnRate;
	
	// Track current wave phase
	int32 CurrentPhase; // 0-3 for introducing enemy types A-D
	float PhaseTimer;
	float PhaseDuration;

	// Track total enemies and kills
	int32 TotalEnemiesSpawned;
	int32 TotalEnemiesKilled;

	void GameOver();
	void Victory();
	void OnEnemyKilled();
	void OnPlayerDied();

	// Get a spawn location with bias toward center
	FVector GetSpawnLocation();
	EEnemyType GetEnemyTypeForCurrentPhase();

private:
	void UpdateDifficulty();
	float DifficultyMultiplier;
};

