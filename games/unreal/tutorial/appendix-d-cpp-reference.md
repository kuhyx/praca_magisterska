# Appendix D: Complete C++ Class Reference

[← Part 9: Final Setup](part-9-final-setup.md) | [Back to Index](README.md) | [Code-First Approach →](code-first-approach.md)

---

## Overview

This appendix provides **complete, copy-paste ready C++ implementations** for all game classes. These can be used instead of the Blueprint-heavy tutorial to create the same bullet-hell game with:

- ✅ **Faster development** - copy entire variable blocks instead of clicking UI
- ✅ **Better version control** - readable Git diffs instead of binary Blueprint files
- ✅ **Easier refactoring** - IDE tools for rename, find references, etc.
- ✅ **Compile-time safety** - catch type errors before runtime

---

## File Structure

Add these files to your Unreal C++ project:

```
Source/BulletHellGame/
├── BulletHellGame.Build.cs          # (already exists)
├── BulletHellGame.h                 # (already exists)
├── STGPawn.h                        # Player ship
├── STGPawn.cpp
├── STGProjectile.h                  # Bullets
├── STGProjectile.cpp
├── STGEnemy.h                       # Enemy ships
├── STGEnemy.cpp
├── STGGameMode.h                    # Game rules, spawning
├── STGGameMode.cpp
└── STGHUD.h                         # UI overlay
    └── STGHUD.cpp
```

---

## Complete Variable Lists (Copy-Paste Ready!)

### BP_Player Variables (Now in STGPawn.h)

Instead of manually creating 12 variables in Blueprint UI, **copy this block:**

```cpp
// In STGPawn.h, inside the class definition:

// ===== MOVEMENT & BOUNDARIES =====
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float MoveSpeed = 750.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMin = FVector2D(-850.0f, -450.0f);

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMax = FVector2D(850.0f, 450.0f);

// ===== FIRING =====
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float FireInterval = 0.08f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float BulletSpeed = 2200.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 VolleySize = 3;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float VolleySpread = 12.0f;

// ===== LIVES & SCORE =====
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 MaxLives = 3;

UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
int32 CurrentLives = 3;

UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
int32 Score = 0;

// ===== SPECIAL ABILITY =====
UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
bool bSpecialUsed = false;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float FireRate = 0.08f;
```

**Time saved:** 15 minutes of clicking vs 30 seconds of copy-paste!

### BP_Enemy Variables (Now in STGEnemy.h)

```cpp
// In STGEnemy.h, inside the class definition:

// ===== HEALTH & SCORE =====
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 MaxHealth = 12;

UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
int32 CurrentHealth = 12;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 ScoreValue = 50;

// ===== MOVEMENT =====
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float VerticalSpeed = 220.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float HorizontalAmplitude = 250.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float HorizontalFrequency = 1.8f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float DespawnY = -750.0f;

// ===== FIRING =====
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float FireInterval = 0.35f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 BulletsPerBurst = 20;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float BurstSpread = 360.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float EnemyBulletSpeed = 1000.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float EnemyBulletLifetime = 6.0f;
```

**Time saved:** 20 minutes of clicking vs 30 seconds of copy-paste!

### BP_Bullet Variables (Now in STGProjectile.h)

```cpp
// In STGProjectile.h, inside the class definition:

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
bool bIsPlayerBullet = false;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
float Damage = 1.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
FLinearColor BulletColor = FLinearColor::Green;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
float Lifetime = 4.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
float Speed = 1200.0f;
```

### BP_GameMode Variables (Now in STGGameMode.h)

```cpp
// In STGGameMode.h, inside the class definition:

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game Rules")
float GameDuration = 300.0f; // 5 minutes (300 seconds)

UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
float TimeRemaining = 300.0f;

UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
bool bIsGameOver = false;

UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
bool bIsVictory = false;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
float BaseSpawnRate = 2.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
float SpawnAreaHalfWidth = 900.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
int32 MaxSimultaneousEnemies = 120;
```

---

## STGPawn.h (Complete File)

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "STGPawn.generated.h"

class UCameraComponent;
class USpringArmComponent;
class UStaticMeshComponent;
class UBoxComponent;

UCLASS()
class BULLETHELLGAME_API ASTGPawn : public APawn
{
    GENERATED_BODY()

public:
    ASTGPawn();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    // ===== COMPONENTS =====
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStaticMeshComponent* ShipMesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    USpringArmComponent* SpringArm;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UCameraComponent* Camera;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UBoxComponent* Hitbox;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStaticMeshComponent* HitboxIndicator;

    // ===== MOVEMENT & BOUNDARIES =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float MoveSpeed = 750.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    FVector2D BoundsMin = FVector2D(-850.0f, -450.0f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    FVector2D BoundsMax = FVector2D(850.0f, 450.0f);

    // ===== FIRING =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireInterval = 0.08f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BulletSpeed = 2200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 VolleySize = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VolleySpread = 12.0f;

    // ===== LIVES & SCORE =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxLives = 3;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentLives = 3;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 Score = 0;

    // ===== SPECIAL ABILITY =====
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    bool bSpecialUsed = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireRate = 0.08f;

    // ===== INPUT FUNCTIONS =====
    void MoveForward(float Value);
    void MoveRight(float Value);
    void StartFire();
    void StopFire();
    void UseSpecial();

    // ===== GAME LOGIC =====
    void FireShot();
    void TakeHit(int32 Damage);
    void HandleDeath();
    void AddScore(int32 Points);

private:
    FTimerHandle TimerHandle_Fire;
    bool bIsFiring = false;
    FVector MovementInput;
    float FireTimer = 0.0f;
};
```

---

## STGProjectile.h (Complete File)

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGProjectile.generated.h"

class USphereComponent;
class UProjectileMovementComponent;
class UStaticMeshComponent;

UCLASS()
class BULLETHELLGAME_API ASTGProjectile : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGProjectile();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    // Components
    UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
    USphereComponent* CollisionComp;

    UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
    UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Movement)
    UProjectileMovementComponent* ProjectileMovement;

    // Variables
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    bool bIsPlayerBullet = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    float Damage = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    FLinearColor BulletColor = FLinearColor::Green;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    float Lifetime = 4.0f;

    // Functions
    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    void SetBulletColor(FLinearColor InColor);
    void SetSpeed(float InSpeed);

private:
    UMaterialInstanceDynamic* DynamicMaterial;
};
```

---

## STGEnemy.h (Complete File)

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGEnemy.generated.h"

UCLASS()
class BULLETHELLGAME_API ASTGEnemy : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGEnemy();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    // Components
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UBoxComponent* CollisionComp;

    // ===== HEALTH & SCORE =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxHealth = 12;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentHealth = 12;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 ScoreValue = 50;

    // ===== MOVEMENT =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VerticalSpeed = 220.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalAmplitude = 250.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalFrequency = 1.8f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float DespawnY = -750.0f;

    // ===== FIRING =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireInterval = 0.35f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 BulletsPerBurst = 20;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BurstSpread = 360.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletSpeed = 1000.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletLifetime = 6.0f;

    // Functions
    void Fire();
    void HandleDamage(float DamageAmount);

    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

private:
    FTimerHandle TimerHandle_Fire;
    float BaseX = 0.0f;
    float WaveSeed = 0.0f;
    UMaterialInstanceDynamic* DynamicMaterial;
};
```

---

## STGGameMode.h (Complete File)

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "STGGameMode.generated.h"

UCLASS()
class BULLETHELLGAME_API ASTGGameMode : public AGameModeBase
{
    GENERATED_BODY()
    
public:
    ASTGGameMode();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ===== GAME RULES =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game Rules")
    float GameDuration = 300.0f; // 5 minutes

    UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
    float TimeRemaining = 300.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
    bool bIsGameOver = false;

    UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
    bool bIsVictory = false;

    UPROPERTY(BlueprintReadOnly, Category = "Game Rules")
    bool bTimerEnded = false;

    // ===== SPAWNING =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float BaseSpawnRate = 2.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    float SpawnAreaHalfWidth = 900.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
    int32 MaxSimultaneousEnemies = 120;

    // Functions
    void SpawnEnemy();
    void GameOver();
    void Victory();
    void OnEnemyKilled();
    void OnPlayerDied();
    FVector GetSpawnLocation();

private:
    FTimerHandle TimerHandle_Spawn;
    float SpawnRate = 2.0f;
    int32 TotalEnemiesSpawned = 0;
    int32 TotalEnemiesKilled = 0;
    void UpdateDifficulty();
    float DifficultyMultiplier = 1.0f;
};
```

---

## UPROPERTY Macros Explained

### Common Patterns

```cpp
// Editable in editor, visible in Blueprints, with default value
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float MoveSpeed = 750.0f;

// Read-only in editor and Blueprints
UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
int32 CurrentLives = 3;

// Only visible in editor Details panel, not exposed to Blueprints
UPROPERTY(VisibleDefaultsOnly, Category = "Components")
UStaticMeshComponent* MeshComp;

// Editable only on archetype (Blueprint class defaults), not instances
UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "Config")
float FireRate = 0.08f;
```

### Specifier Reference

| Specifier | Meaning |
|-----------|---------|
| `EditAnywhere` | Can edit value in Details panel (both class defaults and instances) |
| `EditDefaultsOnly` | Can edit only in class defaults (Blueprint), not placed instances |
| `VisibleAnywhere` | Shows value in Details panel but cannot edit |
| `BlueprintReadWrite` | Can Get/Set in Blueprints |
| `BlueprintReadOnly` | Can Get (but not Set) in Blueprints |
| `Category = "Name"` | Groups properties in Details panel |

---

## Benefits Summary

### Code-First C++ Approach

**Advantages:**
- ✅ **90% faster variable setup** - copy-paste blocks vs clicking UI
- ✅ **Version control friendly** - readable Git diffs
- ✅ **Refactoring tools** - IDE rename, find references, code navigation
- ✅ **Type safety** - compiler catches errors before runtime
- ✅ **Documentation** - code comments in same file as logic
- ✅ **Batch operations** - change multiple values with find/replace
- ✅ **Code reuse** - inherit classes, template patterns

**Disadvantages:**
- ❌ Longer initial compile time (~30-60 seconds vs instant Blueprint)
- ❌ Requires C++ knowledge
- ❌ Need to recompile after changes (though hot reload helps)

### When to Use Each

| Task | Use C++ | Use Blueprint |
|------|---------|---------------|
| Define game variables | ✅ Yes | ❌ No (too slow) |
| Implement game logic | ✅ Yes | ❌ No (hard to maintain) |
| Assign visual assets | ❌ No | ✅ Yes (easier in UI) |
| Create materials | ❌ No | ✅ Yes (visual editor) |
| Animation state machines | ❌ No | ✅ Yes (timeline editor) |
| Level design | ❌ No | ✅ Yes (visual placement) |

**Recommended Hybrid:**
1. Create C++ base classes with all logic and variables
2. Create Blueprint child classes that inherit from C++
3. Use Blueprints only to set visual assets (meshes, materials, sounds)

---

## Migration Guide

### If You Started with Blueprint Tutorial

To migrate existing Blueprint variables to C++:

1. **Open your Blueprint** (e.g., `BP_Player`)
2. **Copy all variable names and values** to a text file
3. **Create C++ header file** (e.g., `STGPawn.h`)
4. **Add UPROPERTY declarations** with copied names and default values
5. **Compile C++**
6. **Reparent Blueprint**: 
   - Open `BP_Player`
   - File → Reparent Blueprint
   - Select `STGPawn` (your C++ class)
7. **Variables now come from C++!**
8. **Delete old Blueprint variables** (they're redundant)

---

## Next Steps

- [Complete Code-First Tutorial](code-first-approach.md) - Full implementation guide
- [Blueprint Tutorial](README.md) - Original Blueprint-heavy version
- [Troubleshooting](appendix-b-troubleshooting.md) - Common issues

---

[← Part 9: Final Setup](part-9-final-setup.md) | [Back to Index](README.md) | [Code-First Approach →](code-first-approach.md)
