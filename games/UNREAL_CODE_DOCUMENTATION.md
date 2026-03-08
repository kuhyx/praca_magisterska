# Unreal Engine Bullet Hell — Complete Code Documentation

**Project**: `games/unreal/BulletHellGame/BulletHellCPP/`
**Language**: C++ (Unreal Engine 5.5)
**Module**: `BulletHellCPP`
**Purpose**: Performance benchmark bullet-hell shooter — Unreal counterpart to the Unity version for engine comparison.
**Duration**: 90-second survival round with escalating difficulty.

---

## Architecture Overview

The Unreal version follows a **standard UE5 actor-based architecture**: the game uses Actors placed in a level, with C++ classes providing all game logic. Unlike the Unity version (which bootstraps from an empty scene), this project relies on a pre-configured level with key actors placed:

1. **`ASTGGameMode`** — Sets default pawn class to `ASTGPawn`
2. **`ASTGGameDirector`** — Level-placed actor managing timer and game flow
3. **`ASTGEnemySpawner`** — Level-placed actor continuously spawning enemies
4. **`ASTGFixedCamera`** — Level-placed camera auto-fitting the play area
5. **`ASTGHUDManager`** — Level-placed actor managing UMG widget

### Dependency Graph

```
ASTGGameMode
  └── Spawns ASTGPawn (Default Pawn)

Level contains:
  ├── ASTGGameDirector (timer, victory/game-over)
  ├── ASTGEnemySpawner (wave spawning)
  ├── ASTGFixedCamera (top-down camera, auto-fit)
  └── ASTGHUDManager (UMG widget wrapper)

Runtime spawned:
  ├── ASTGEnemy (4 types: Fodder, Runner, Turret, Tank)
  └── ASTGProjectile (player & enemy bullets)
```

### Key Design Differences from Unity Version

| Aspect | Unity | Unreal |
|--------|-------|--------|
| **Initialization** | Scene-free bootstrap (code creates everything) | Level-placed actors (scene-dependent) |
| **Bullet management** | Object pooling (`BulletPool`) | Dynamic spawn/destroy (no pooling) |
| **Configuration** | Runtime `EnemyBlueprint` C# class | `STGGameSettings.h` constexpr namespace |
| **HUD** | Built entirely in C# code | UMG widget (Blueprint-defined layout) |
| **Movement** | Manual `transform.position` manipulation | UE5 `ProjectileMovementComponent` for bullets |
| **Input** | Legacy `Input.GetKey()` polling | Enhanced Input System (actions + contexts) |
| **VFX** | Pooled sprite scaling (`EffectPulse`) | Niagara particle system |
| **Enemy types** | Blazer, Striker, Cascade, Interceptor | Fodder, Runner, Turret, Tank |
| **Actor discovery** | Singleton pattern (`.Instance`) | `GetAllActorsOfClass()` runtime queries |
| **Camera** | Orthographic 2D | Perspective 3D (top-down at calculated height) |

---

## File-by-File Documentation

### 1. `STGGameSettings.h` — Centralized Game Constants

**What it does**: A header-only configuration file using nested `constexpr` namespaces to define ALL game constants in a single location:

- **`STG::PlayArea`** — World-space bounds: 1700×900 units centered at origin (±850×±450)
- **`STG::Game`** — Default duration (90s), debug quick mode (10s)
- **`STG::Player`** — Move speed (750), bullet speed (2200), max lives (3), upgrade thresholds (100/300/600/1000 score), starting vs max fire stats
- **`STG::Enemy::Fodder/Runner/Turret/Tank`** — Per-type stats: health, score, speeds, firing parameters
- **`STG::Enemy`** — Shared enemy settings: bullet lifetime (10s), visual scale vs collision radius (grazing mechanic)
- **`STG::Spawner`** — Spawn intervals (0.25s→0.08s→0.03s chaos), max 200 simultaneous enemies
- **`STG::Camera`** — FOV (60°), default height, ortho width
- **`STG::VFX`** — Death particle count (500)

**Why it works this way**: The `constexpr` approach gives:
1. **Zero runtime cost** — all values are compile-time constants
2. **Single source of truth** — change a value once, everything updates
3. **No serialization** — unlike UPROPERTY defaults which require editor interaction
4. **Clear hierarchy** — the namespace structure documents the game design

**Grazing mechanic**: `BulletVisualScale = 0.25` but `BulletCollisionRadius = 3.0` means enemy bullets appear large (easy to see) but have a tiny hitbox, so players can "graze" through near-misses. This is a classic bullet-hell design.

---

### 2. `STGGameMode.h/.cpp` — Game Mode Configuration

**What it does**: Minimal `AGameModeBase` subclass that sets `DefaultPawnClass = ASTGPawn::StaticClass()` and disables spectator start.

**Why it works this way**: UE5 requires a GameMode to define the default pawn class. This is the simplest possible setup — the GameMode does nothing else. The pawn spawning is handled by the engine's built-in `RestartPlayer()` flow.

---

### 3. `STGGameDirector.h/.cpp` — Game Flow Controller

**What it does**: Level-placed `AActor` that manages the game timer and end conditions:

**Tick behavior**:
1. Increments `ElapsedTime`
2. Displays timer via `GEngine->AddOnScreenDebugMessage`
3. When `ElapsedTime >= GameDuration`: enters cleanup phase (spawning stops)
4. During cleanup: counts active enemies via `GetAllActorsOfClass(ASTGEnemy)`, triggers victory when count reaches 0
5. Updates HUD timer via `ASTGHUDManager`

**End states**:
- **Victory**: All enemies cleared after time expires → shows "VICTORY!", pauses game (or auto-quits)
- **Game Over**: Player dies → shows "GAME OVER", pauses game (or auto-quits)

**Command-line arguments** (for automated benchmarking):
- `--autoquit` — Calls `FPlatformMisc::RequestExit(false)` when game ends
- `--duration=N` — Overrides game duration (e.g., `--duration=95`)
- `--start-time=N` — Fast-forwards elapsed time for phased profiling (e.g., `--start-time=30` starts at 30s difficulty)

**Why it works this way**: Using `GetAllActorsOfClass()` every tick during cleanup is not ideal for performance, but the cleanup phase is brief and occurs only once. The command-line argument system enables fully automated benchmarking — run the game, capture N seconds, auto-exit — perfect for Nsight profiling integration.

**Actor discovery pattern**: The Director finds the HUDManager via `GetAllActorsOfClass()` each tick. This is different from Unity's singleton pattern — UE5's approach is more flexible (supports multiple instances) but has higher per-query cost.

---

### 4. `STGFixedCamera.h/.cpp` — Camera System

**What it does**: A fixed top-down camera with automatic play-area fitting:

**Auto-fit mode** (default):
1. Finds `ASTGGameDirector` via `GetAllActorsOfClass()`
2. Reads play area bounds (`PlayAreaMin`, `PlayAreaMax`)
3. Calculates required camera height using `CalculateCameraHeightForPlayArea()`:
   - Computes height needed for horizontal extent using horizontal FOV
   - Computes height needed for vertical extent using derived vertical FOV (assuming 16:9)
   - Takes the maximum to ensure both dimensions fit
4. Applies optional margin (percentage of FOV narrowing)

**Manual mode**: Uses fixed `CameraHeight` and `FieldOfView`.

**Orthographic mode**: Optional, using `OrthoWidth` for 2D-style projection.

**Why it works this way**: The auto-fit calculation ensures the camera shows exactly the play area regardless of resolution or aspect ratio. The trigonometric approach (`height = halfWidth / tan(halfFOV)`) is the standard way to calculate camera distance for a given field of view.

**Key difference from Unity**: Unity uses a simple orthographic camera (set `orthographicSize`). Unreal's perspective camera requires explicit height calculation — this is more complex but gives the 3D depth effect that Unreal's renderer expects.

---

### 5. `STGPawn.h/.cpp` — Player Character

**What it does**: The player pawn with movement, shooting, screen-clear special, and upgrade progression:

**Construction** (ASTGPawn constructor):
- Creates a `UStaticMeshComponent` using `/Engine/BasicShapes/Cylinder` flattened to scale (0.08, 0.08, 0.001) — a flat 2D circle
- Creates a `UBoxComponent` hitbox (4×4×4 units) matching the visual size
- Creates a hidden `HitboxIndicator` (unused)

**Movement** (Enhanced Input):
- Uses `UInputMappingContext` and `UInputAction` bindings (UE5 Enhanced Input System)
- `Move()` reads 2D axis input, `Tick()` applies to position with bounds clamping
- Movement is in X (forward/back) and Y (left/right) — UE5's coordinate system for top-down

**Shooting**:
- Hold fire → auto-fire at `FireInterval`
- `VolleySize` bullets with `VolleySpread` angular distribution
- Bullets spawned as `ASTGProjectile` actors with `bIsPlayerBullet = true`
- Bullets colored soft green (0.2, 0.8, 0.3) with low emissive

**Upgrade system** (score-based):
| Level | Score | Volley | Spread | Fire Rate |
|-------|-------|--------|--------|-----------|
| 0 | 0 | 1 bullet | 0° | 0.50s |
| 1 | 100 | 2 bullets | 8° | 0.35s |
| 2 | 300 | 3 bullets | 12° | 0.20s |
| 3 | 600 | 4 bullets | 16° | 0.12s |
| 4 | 1000 | 5 bullets | 20° | 0.08s |

**Special ability** (one-use screen clear):
- Destroys all `ASTGEnemy` actors via `GetAllActorsOfClass()`
- Destroys all non-player `ASTGProjectile` actors

**Damage/death**:
- `TakeHit(damage)` — reduces lives, spawns Niagara hit VFX, triggers game over at 0
- Debug invincibility ignores all damage
- On death: hides actor, notifies `ASTGGameDirector::OnPlayerDied()`

**Command-line flags**:
- `--invincible` — Ignores all damage
- `--stationary` — Disables movement (for passive benchmarking)

**Why it works this way**: The Enhanced Input System is UE5's recommended input approach (Legacy Input is deprecated). The upgrade system creates a natural difficulty escalation — more bullets means more `ASTGProjectile` actors spawned, increasing rendering and physics overlap costs.

**Key architectural difference from Unity**: No object pooling for bullets. Each `FireShot()` calls `World->SpawnActor<ASTGProjectile>()`, and bullets are destroyed on hit or lifetime expiry. This is the standard UE5 approach but means higher actor creation/destruction overhead per frame.

---

### 6. `STGEnemy.h/.cpp` — Enemy Actors

**What it does**: Base enemy actor with 4 types defined by `EEnemyType` enum:

**Type initialization** (`InitializeFromType()`):
Each type loads the cube mesh at different scales/rotations with dynamic material colors:

| Type | HP | Score | Speed | Fires | Shape | Color |
|------|-----|-------|-------|-------|-------|-------|
| **Fodder** | 1 | 10 | 80 | No | Small square (0.25) | Green |
| **Runner** | 3 | 25 | 90 | No | Diamond (0.35, rotated 45°) | Cyan |
| **Turret** | 15 | 75 | 60 | Yes (4 bullets, 360° burst, 1.2s) | Medium square (0.5) | Orange |
| **Tank** | 50 | 200 | 40 | Yes (20 bullets, 360° rapid, 0.3s) | Wide rectangle (0.4×0.8) | Red |

**Movement** (Tick):
- Moves in -X direction (downward in top-down view) at `VerticalSpeed`
- Horizontal sinusoidal wave: `Y = StartY + Amplitude * sin(Frequency * (time + seed))`
- Y-clamped to play area bounds
- Despawns when X < `DespawnY`

**Firing** (timer-based):
- Uses `FTimerHandle` to call `Fire()` at `FireInterval`
- Spawns `BulletsPerBurst` projectiles in a 360° radial burst pattern
- Each bullet gets orange-red color, large visual scale with tiny collision (grazing)

**Damage/death**:
- `HandleDamage(amount)`: reduces HP, spawns Niagara hit effect, awards score on death
- `OnOverlapBegin()`: if overlapping player, damages player and self-destructs

**Why it works this way**: The `InitializeFromType()` pattern is similar to Unity's `EnemyBlueprint` but uses an enum + switch instead of a data class. All enemies use the same `ASTGEnemy` class with different configs — this avoids needing multiple Blueprint subclasses.

**Material system**: Each enemy creates a `UMaterialInstanceDynamic` from the basic shape material to set color. This allows runtime color changes without needing separate material assets — analogous to Unity's `SpriteRenderer.color`.

---

### 7. `STGEnemySpawner.h/.cpp` — Wave Spawning System

**What it does**: Level-placed actor that continuously spawns enemies with escalating difficulty:

**Initial wave**: 5 Fodder enemies spawned in `BeginPlay()` at upper half of play area.

**Tick spawning**:
1. Updates `ElapsedTime` and `CurrentSpawnInterval`
2. When `SpawnTimer` expires: checks enemy count (max 200), spawns one enemy
3. Stops spawning when `ElapsedTime >= GameDuration`

**Difficulty progression** (`GetRandomEnemyType()`):
| Game Progress | Enemy Distribution |
|--------------|-------------------|
| 0–25% | 100% Fodder (spam) |
| 25–50% | 85% Fodder, 15% Runner |
| 50–75% | 70% Fodder, 20% Runner, 10% Turret |
| 75–100% | 55% Fodder, 20% Runner, 15% Turret, 10% Tank |

**Spawn interval** (`CalculateSpawnInterval()`):
- Linear interpolation from `BaseSpawnInterval` (0.25s) to `MinSpawnInterval` (0.08s)
- Final 5 seconds: `FinalRushInterval` (0.03s) — absolute chaos mode

**Spawn location**: Top of play area (`STG::Spawner::SpawnX`), random Y within `SpawnAreaHalfWidth`.

**Command-line support**: `--start-time=N` fast-forwards the spawner's elapsed time and difficulty to match.

**Why it works this way**: The progressive difficulty ensures the game starts manageable (only harmless Fodder) and escalates to overwhelming (Tanks + rapid spawning). The "final rush" mechanic at 0.03s intervals creates a dramatic climax before the timer expires.

**Key difference from Unity**: The Unity spawner uses a coroutine-based loop and spawns multiple enemies per wave (2–10). The Unreal spawner uses tick-based timing and spawns one enemy per interval. The net effect is similar but the Unreal version creates a more constant stream while Unity has distinct wave pulses.

---

### 8. `STGProjectile.h/.cpp` — Bullet Actor

**What it does**: Individual bullet actor using UE5's built-in `UProjectileMovementComponent`:

**Construction**:
- `USphereComponent` for collision (radius configurable)
- `UStaticMeshComponent` using `/Engine/BasicShapes/Sphere` for visual
- `UProjectileMovementComponent` for movement: no gravity, no bouncing, rotation follows velocity

**BeginPlay configuration**:
- Sets `LifeSpan` for automatic destruction
- Applies `CollisionRadius` to sphere component
- Applies `BulletScale` to mesh component
- Creates `UMaterialInstanceDynamic` for color/emissive control

**Collision** (`OnOverlapBegin`):
- Player bullets → hit `ASTGEnemy` → call `HandleDamage()`, destroy self
- Enemy bullets → hit `ASTGPawn` → call `TakeHit()`, destroy self

**Grazing mechanic**: `BulletScale` controls visual size while `CollisionRadius` controls the actual hitbox. Enemy bullets have large visuals (0.25) but tiny collision (3.0 radius), allowing players to weave between bullets that appear to overlap.

**Why it works this way**: `UProjectileMovementComponent` provides efficient built-in projectile physics including speed, gravity, and bouncing. Since gravity is disabled, bullets travel in straight lines — functionally identical to Unity's manual `transform.position` movement but leveraging UE5's optimized component.

**No pooling**: Unlike Unity's `BulletPool`, each bullet is a new `AActor` spawned via `SpawnActor()` and destroyed via `Destroy()` or `LifeSpan`. This is the standard UE5 pattern. The performance impact of actor creation/destruction vs pooling is a key comparison point for the thesis.

---

### 9. `STGHUDManager.h/.cpp` — HUD Widget Manager

**What it does**: Actor-based wrapper for a UMG (Unreal Motion Graphics) widget:
- `BeginPlay()`: Creates and displays the widget from `HUDWidgetClass` (a Blueprint-defined UMG widget)
- `UpdateScore(score)`: Finds `txt_Score` text block, sets text
- `UpdateLives(lives)`: Finds `txt_Lives` text block, sets text
- `UpdateTimer(timeRemaining)`: Finds `txt_Timer` text block, sets formatted seconds
- `ShowVictory()`: Finds `txt_Result`, sets "VICTORY!" in green
- `ShowGameOver()`: Finds `txt_Result`, sets "GAME OVER" in red

**Why it works this way**: UE5's HUD is typically built in UMG (visual editor), not in C++. The C++ code only drives data updates, while the widget layout is defined in a Blueprint asset. This is the standard UE5 pattern — C++ logic + UMG layout.

**Widget name binding**: Finding widgets by name (`GetWidgetFromName("txt_Score")`) is a common UE5 pattern for C++ ↔ UMG communication. It's less type-safe than Blueprint bindings but allows the C++ code to work with any widget layout that follows the naming convention.

**Difference from Unity**: Unity's HUD is built entirely in C# code (`GameInitializer.CreateHud()`). Unreal delegates layout to UMG, which is more visual but requires a separate Blueprint asset.

---

### 10. `BulletHellCPP.Build.cs` — Build Configuration

**What it does**: Module build file declaring dependencies:
- `Core`, `CoreUObject`, `Engine` — standard UE5 modules
- `InputCore`, `EnhancedInput` — for the Enhanced Input System
- `UMG` — for HUD widget system
- `Niagara` — for particle VFX

**Why these dependencies**: Each module provides specific functionality:
- `EnhancedInput` replaces legacy input for UE5 projects
- `UMG` is needed for `CreateWidget<>()` and `UUserWidget`
- `Niagara` enables GPU particle effects for enemy death explosions

---

### 11. `STGFixedCamera.h/.cpp` — Top-Down Camera (continued)

The camera rotation is set to `FRotator(-90, 0, 0)` — looking straight down along -Z. The `CalculateCameraHeightForPlayArea()` method uses the horizontal FOV and an assumed 16:9 aspect ratio to compute the exact Z-height needed so the play area fills the viewport.

---

## Performance-Critical Design Decisions

| Decision | Rationale |
|----------|-----------|
| No bullet pooling (`SpawnActor`/`Destroy` per bullet) | Standard UE5 approach; creates a natural comparison point with Unity's pooled design |
| `UProjectileMovementComponent` for bullet movement | Leverages UE5's optimized built-in component vs manual tick movement |
| `constexpr` configuration namespace | Zero-cost abstractions; compile-time constants |
| Niagara for death VFX (500 particles) | GPU particle system; specifically tests GPU workload |
| `GetAllActorsOfClass()` for actor discovery | Standard UE5 pattern; O(N) scan but simple |
| Dynamic materials per enemy | One material instance per actor allows per-enemy colors |
| Enhanced Input System | UE5 recommended; maps cleanly to gamepad + keyboard |
| Large visual / small collision for enemy bullets | Grazing mechanic makes gameplay fair despite high bullet density |
| Command-line flags for benchmarking | Enables fully automated profiling runs |

---

## Coordinate System Note

Unreal uses a **left-handed Z-up** coordinate system:
- **X** = forward (toward top of screen in top-down view)
- **Y** = right (horizontal on screen)
- **Z** = up (camera height, perpendicular to play plane)

This means:
- Enemies move in **-X** direction (downward on screen)
- Player shoots in **+X** direction (upward on screen)
- Camera is at high **Z** looking down with rotation `(-90, 0, 0)`
- Play area bounds are on X/Y plane, Z ≈ 0
