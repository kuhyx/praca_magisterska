# Part 5 (C++): Create Enemy Spawner

[← Previous: Part 4 (C++) - Create the Enemy](part-4-cpp-create-enemy.md) | [Back to Index](README.md) | [Next: Part 6 (C++) - Create Game Director →](part-6-cpp-create-game-director.md)

---

## Overview

Create an enemy spawner that gradually increases difficulty over time. Copy-paste variables instead of manual UI configuration.

**Time comparison:**
- Blueprint: ~40 minutes (variables + curve setup + Blueprint nodes)
- C++ (this part): ~10 minutes (copy-paste code)

---

## Step 5.1: Create STGEnemySpawner C++ Class

1. **Tools → New C++ Class** → Actor → Name: `STGEnemySpawner`
2. Wait for compilation

---

## Step 5.2: Define Spawner Variables

### Open STGEnemySpawner.h in VS Code

Replace content with:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGEnemySpawner.generated.h"

UCLASS()
class BULLETHELLGAME_API ASTGEnemySpawner : public AActor
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
```

---

## Step 5.3: Implement Spawner Logic

### Open STGEnemySpawner.cpp

Replace with:

```cpp
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
```

---

## Step 5.4: Compile

1. Click **Compile** in Unreal Editor
2. Wait for compilation
3. Check for errors

---

## Step 5.5: Place Spawner in Level

1. From Content Browser "C++ Classes" folder, find `STGEnemySpawner`
2. Can either:
   - **Option A**: Drag directly into level (no Blueprint needed!)
   - **Option B**: Create `BP_EnemySpawner` Blueprint child for tweaking values in editor

3. Position spawner at origin (0, 0, 0) or anywhere - location doesn't matter for spawning

---

## Step 5.6: Test Spawning

1. Remove any manually-placed enemies from level
2. Make sure spawner is placed
3. Press **Play**

### Expected Result in Play Mode:

**Spawning behavior:**
- ✅ Enemies spawn at top of screen every ~2 seconds initially
- ✅ Spawn rate gradually increases (gets faster over time)
- ✅ Enemies spawn at random horizontal positions
- ✅ Maximum of 120 enemies on screen at once
- ✅ After 5 minutes (300 seconds), spawning stops

**Visual confirmation:**
- Enemies appear from top edge of screen
- Each spawns at a different Y position (left-right spread)
- As time passes, enemies spawn more frequently
- Game becomes progressively harder

**Performance:**
- Even with many enemies, game maintains 60 FPS
- No lag or stuttering when many enemies/bullets on screen

---

## Comparison Summary

### Blueprint: ~40 minutes
- Create spawner Blueprint
- Add 6 variables manually
- Create spawn rate curve asset
- Complex Blueprint nodes for curve sampling
- Random position calculation nodes
- Enemy counting logic

### C++: ~10 minutes
- Create C++ class
- Copy-paste variables and logic
- Compile
- Place in level

**Time saved: 30 minutes** ⚡

---

[← Previous: Part 4 (C++) - Create the Enemy](part-4-cpp-create-enemy.md) | [Back to Index](README.md) | [Next: Part 6 (C++) - Create Game Director →](part-6-cpp-create-game-director.md)
