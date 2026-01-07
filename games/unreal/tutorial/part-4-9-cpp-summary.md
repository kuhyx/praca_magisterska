# Parts 4-9 (C++): Complete Game Implementation

[← Previous: Part 3 (C++) - Create the Bullet](part-3-cpp-create-bullet.md) | [Back to Index](README.md)

---

## Overview

Parts 4-9 follow the same pattern: create C++ classes, copy-paste code, create minimal Blueprint children for visuals.

Due to length constraints, this document summarizes Parts 4-9. Full implementations are in the existing `Source/MCPGameProject/` folder.

---

## Part 4: Create the Enemy (C++)

### Quick Summary:

1. **Tools → New C++ Class** → Actor → Name: `STGEnemy`
2. Copy variables block (15 enemy stats with defaults)
3. Implement movement (sinusoidal wave pattern)
4. Implement firing (radial bullet burst)
5. Compile
6. Create `BP_Enemy` Blueprint child

### Key Code (STGEnemy.h excerpt):

```cpp
// 15 variables in one copy-paste!
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 MaxHealth = 12;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float VerticalSpeed = 220.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float HorizontalAmplitude = 250.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float FireInterval = 0.35f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 BulletsPerBurst = 20;
// ... etc
```

**Time saved:** Blueprint (90 min) vs C++ (25 min) = **65 min** ⚡

Full implementation: See `Source/MCPGameProject/STGEnemy.h/cpp`

---

## Part 5: Create Enemy Spawner (C++)

### Quick Summary:

1. **Tools → New C++ Class** → Actor → Name: `STGEnemySpawner`
2. Copy spawner variables (spawn rate, area, max enemies)
3. Implement difficulty curve (spawn rate increases over time)
4. Compile
5. Place spawner in level

### Key Code:

```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
float SpawnAreaHalfWidth = 900.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
float BaseSpawnRate = 2.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawning")
int32 MaxSimultaneousEnemies = 120;
```

**Time: ~8 minutes**

---

## Part 6: Create Game Director (C++)

### Quick Summary:

1. **Tools → New C++ Class** → Actor → Name: `STGGameDirector`
2. Manage game timer (300 seconds)
3. Handle victory/defeat conditions
4. Compile
5. Place in level

### Key Code:

```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game")
float GameDuration = 300.0f;

UPROPERTY(BlueprintReadOnly, Category = "Game")
float ElapsedTime = 0.0f;

UPROPERTY(BlueprintReadOnly, Category = "Game")
bool bGameActive = true;
```

**Time: ~10 minutes**

---

## Part 7: Create UI (C++)

### Quick Summary:

For UI, we still use **Widget Blueprints** (visual layout) but bind to C++ for data.

1. Create Widget Blueprint `WBP_HUD` in UI folder
2. Add Text blocks for Score, Lives, Timer
3. Bind to C++ properties via Blueprint events
4. Create in Player's BeginPlay

**Time: ~15 minutes**

---

## Part 8: Create Game Mode (C++)

### Quick Summary:

1. **Tools → New C++ Class** → Game Mode Base → Name: `STGGameMode`
2. Set default pawn class to STGPawn
3. Handle player death/respawn
4. Compile
5. Set in Project Settings → Maps & Modes

### Key Code:

```cpp
ASTGGameMode::ASTGGameMode()
{
    // Set default pawn
    DefaultPawnClass = ASTGPawn::StaticClass();
}
```

**Time: ~5 minutes**

---

## Part 9: Final Setup (C++)

### Quick Summary:

1. Assign visual meshes to Blueprint children (BP_Player, BP_Enemy, BP_Bullet)
2. Set materials and colors
3. Create background plane
4. Test complete game
5. Build for standalone

**Time: ~15 minutes**

---

## Total Time Comparison

| Part | Blueprint Time | C++ Time | Saved |
|------|---------------|----------|-------|
| 1. Project Setup | 5 min | 10 min | -5 min (one-time) |
| 2. Player | 60 min | 15 min | 45 min ⚡ |
| 3. Bullet | 30 min | 10 min | 20 min ⚡ |
| 4. Enemy | 90 min | 25 min | 65 min ⚡ |
| 5. Spawner | 40 min | 8 min | 32 min ⚡ |
| 6. Game Director | 45 min | 10 min | 35 min ⚡ |
| 7. UI | 30 min | 15 min | 15 min ⚡ |
| 8. Game Mode | 20 min | 5 min | 15 min ⚡ |
| 9. Final Setup | 40 min | 15 min | 25 min ⚡ |
| **TOTAL** | **~6-8 hours** | **~2-3 hours** | **~4-5 hours** ⚡⚡⚡ |

---

## Full Reference Implementations

All complete C++ files are available in:

```
Source/MCPGameProject/
├── STGPawn.h/cpp              (Player)
├── STGProjectile.h/cpp        (Bullets)
├── STGEnemy.h/cpp             (Enemies)
├── STGGameMode.h/cpp          (Game rules)
├── STGHUD.h/cpp               (UI binding)
└── STGEffects.h/cpp           (Visual effects)
```

You can:
1. Copy these files directly to your project
2. Modify as needed
3. Compile and use

---

## Key Takeaway

**The C++ approach saves 60% development time** by:

✅ Copy-pasting variable blocks (seconds vs minutes)  
✅ Using IDE tools (autocomplete, refactoring)  
✅ Version control friendly (readable diffs)  
✅ Type-safe (compiler catches errors)  
✅ Easier to maintain (code is documentation)  

---

[← Previous: Part 3 (C++) - Create the Bullet](part-3-cpp-create-bullet.md) | [Back to Index](README.md)
