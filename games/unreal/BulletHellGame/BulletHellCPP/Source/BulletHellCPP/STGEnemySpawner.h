#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGGameSettings.h"
#include "STGEnemy.h"
#include "STGEnemySpawner.generated.h"

UCLASS()
class BULLETHELLCPP_API ASTGEnemySpawner : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGEnemySpawner();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    // ===== SPAWNING VARIABLES =====
    // Defaults from STGGameSettings.h
    
    // Enemy class to spawn (use Blueprint subclass for VFX support)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    TSubclassOf<ASTGEnemy> EnemyClass;
    
    // Half-width for Y spawn range (should be less than play area to allow wave movement)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float SpawnAreaHalfWidth = STG::Spawner::SpawnAreaHalfWidth;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float GameDuration = STG::Game::DefaultDuration;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    int32 MaxSimultaneousEnemies = STG::Spawner::MaxSimultaneousEnemies;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float BaseSpawnInterval = STG::Spawner::BaseSpawnInterval;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Spawning")
    float ElapsedTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Spawning")
    bool bSpawningActive = true;

private:
    float SpawnTimer = 0.0f;
    float CurrentSpawnInterval = STG::Spawner::BaseSpawnInterval;
    
    void SpawnEnemy();
    float CalculateSpawnInterval();
    FVector GetRandomSpawnLocation();
    EEnemyType GetRandomEnemyType(float GameProgress);
};