#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
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
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float SpawnAreaHalfWidth = 900.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float GameDuration = 300.0f; // 5 minutes

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    int32 MaxSimultaneousEnemies = 120;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float BaseSpawnInterval = 2.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Spawning")
    float ElapsedTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Spawning")
    bool bSpawningActive = true;

private:
    float SpawnTimer = 0.0f;
    float CurrentSpawnInterval = 2.0f;
    
    void SpawnEnemy();
    float CalculateSpawnInterval();
    FVector GetRandomSpawnLocation();
};