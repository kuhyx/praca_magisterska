#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "ShootEmUpEnemy.h"
#include "ShootEmUpGameMode.generated.h"

class AShootEmUpPlayerPawn;
class AShootEmUpProjectile;
class AShootEmUpEnemy;
class AShootEmUpHUD;
class ABackgroundScroller;

USTRUCT()
struct FEnemySpawnStep
{
    GENERATED_BODY()

    UPROPERTY()
    float StartTime;

    UPROPERTY()
    float SpawnInterval;

    UPROPERTY()
    EEnemyArchetype Archetype;

    FEnemySpawnStep()
        : StartTime(0.f)
        , SpawnInterval(3.f)
        , Archetype(EEnemyArchetype::TypeA)
    {
    }

    FEnemySpawnStep(float InTime, float InInterval, EEnemyArchetype InType)
        : StartTime(InTime)
        , SpawnInterval(InInterval)
        , Archetype(InType)
    {
    }
};

UCLASS()
class MAGISTERKA_API AShootEmUpGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    AShootEmUpGameMode();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

    void NotifyEnemyKilled(AShootEmUpEnemy* Enemy);
    void RegisterEnemyDestroyed(AShootEmUpEnemy* Enemy);
    void SpawnEnemyProjectile(const FVector& Origin, const FVector& Direction, float Speed, float Damage, const FLinearColor& Tint);

    void HandlePlayerDamaged(int32 LivesRemaining);
    void HandlePlayerDeath();
    void HandlePlayerRespawnRequest();
    void HandleScoreUpdated(int32 NewScore);
    void HandlePlayerLevelUp(int32 NewLevel);
    void HandleScreenClearRequested();

    float GetRemainingTime() const { return FMath::Max(0.f, GameDuration - ElapsedTime); }
    int32 GetScore() const { return Score; }
    int32 GetLives() const { return LivesRemaining; }
    int32 GetPlayerLevel() const { return PlayerLevel; }
    bool IsGameOver() const { return bGameOver; }
    bool IsVictory() const { return bVictory; }

protected:
    void InitializePlayer();
    void InitializeBackground();
    void ScheduleNextSpawn(float Delay);
    void SpawnEnemyByArchetype(EEnemyArchetype Archetype);
    FVector GenerateSpawnLocation() const;
    EEnemyArchetype SelectCurrentArchetype() const;
    void UpdateDifficulty(float DeltaSeconds);
    void CleanupDestroyedActors();
    void TriggerGameOver(bool bPlayerWon);

    UPROPERTY(EditDefaultsOnly, Category = "Config")
    float GameDuration;

    UPROPERTY(EditDefaultsOnly, Category = "Config")
    float InitialSpawnInterval;

    UPROPERTY(EditDefaultsOnly, Category = "Config")
    float MinimumSpawnInterval;

    UPROPERTY(EditDefaultsOnly, Category = "Config")
    TSubclassOf<AShootEmUpProjectile> EnemyProjectileClass;

    UPROPERTY(EditDefaultsOnly, Category = "Config")
    TSubclassOf<ABackgroundScroller> BackgroundClass;

    UPROPERTY(EditDefaultsOnly, Category = "Config")
    FVector PlayerSpawnLocation;

private:
    void OnSpawnTimerElapsed();
    void UpdateTimer(float DeltaSeconds);

    FTimerHandle SpawnTimerHandle;

    TWeakObjectPtr<AShootEmUpPlayerPawn> PlayerPawn;
    TArray<TWeakObjectPtr<AShootEmUpEnemy>> ActiveEnemies;
    TArray<TWeakObjectPtr<AShootEmUpProjectile>> ActiveEnemyProjectiles;

    TArray<FEnemySpawnStep> SpawnSteps;

    float ElapsedTime;
    float CurrentSpawnInterval;
    int32 Score;
    int32 LivesRemaining;
    int32 PlayerLevel;

    bool bGameOver;
    bool bVictory;
};
