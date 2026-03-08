# Thesis Defense — Exemplary Code Questions & Answers

Questions that may arise during the defense (obrona) about the game implementations,
along with answers that can be demonstrated directly from the source code.

---

## Category 1: Architecture & Design Patterns

### Q1: Why does the Unity version build the entire game from code instead of using a pre-configured scene?

**Answer (reference: `GameBootstrap.cs`, `GameInitializer.cs`)**:
The Unity version uses a **scene-free bootstrap pattern** where `GameBootstrap` (a static class with `[RuntimeInitializeOnLoadMethod]`) creates a `GameInitializer` MonoBehaviour that constructs everything in `Awake()`. This design ensures:
1. **Benchmark reproducibility** — no scene serialization variability between test runs
2. **No missing references** — all wiring is explicit in code, not serialized in scene files
3. **Single source of truth** — the entire game configuration is readable in `GameInitializer.BuildGame()`

The Unreal version, in contrast, uses level-placed actors — this is more idiomatic for Unreal but introduces scene-dependency.

---

### Q2: What design patterns are used in the Unity project, and why?

**Answer (reference: multiple files)**:
- **Singleton** (`GameDirector.Instance`, `ScoreManager.Instance`, etc.) — provides global access to managers; common in Unity game architecture
- **Object Pooling** (`BulletPool.cs`, `EffectManager.cs`) — eliminates GC pressure from Instantiate/Destroy in a bullet-hell scenario
- **Component Composition** (`[RequireComponent(typeof(Health))]`) — decouples health/damage from entity behavior
- **Event-driven Communication** (`Health.Died`, `ScoreManager.ScoreChanged`) — loose coupling via C# delegates
- **Factory Method** (`BulletPool.Create()`, `PlayerController.CreatePlayer()`) — encapsulates construction
- **Data-driven Configuration** (`EnemyBlueprint`) — enemy archetypes defined as runtime data objects

---

### Q3: How does the Unreal version discover and communicate between actors?

**Answer (reference: `STGGameDirector.cpp`, `STGPawn.cpp`)**:
The Unreal version uses `UGameplayStatics::GetAllActorsOfClass()` to find other actors at runtime. For example, the GameDirector finds the HUDManager each tick:
```cpp
TArray<AActor*> FoundManagers;
UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGHUDManager::StaticClass(), FoundManagers);
```
This is the standard UE5 approach but has O(N) complexity per call. The Unity version uses singletons (O(1) access) but sacrifices flexibility (only one instance allowed).

---

### Q4: Why does the Unreal version use a centralized settings header instead of UPROPERTY defaults?

**Answer (reference: `STGGameSettings.h`)**:
The `STGGameSettings.h` uses `constexpr` namespaces (`STG::Player::MoveSpeed`, `STG::Enemy::Tank::Health`, etc.) to define all game constants in one file. Benefits:
1. **Zero runtime cost** — values are compile-time constants
2. **Single source of truth** — change a value in one place, it propagates to all classes
3. **No editor dependency** — no need to set values in Blueprint/Inspector
4. **Self-documenting** — the namespace hierarchy (`STG::Enemy::Tank::Health = 50`) reads as game design documentation

UPROPERTY defaults are still used as initializers (`float MoveSpeed = STG::Player::MoveSpeed`) so values appear in the editor for debugging.

---

## Category 2: Performance & Optimization

### Q5: How does the Unity bullet pool work, and why is it needed?

**Answer (reference: `BulletPool.cs`, `Bullet.cs`)**:
`BulletPool` uses a `Queue<Bullet>` for O(1) get/return and a `HashSet<Bullet>` for tracking live bullets:
- **Spawn**: Dequeue from pool (or create new if empty), activate, configure
- **Return**: Deactivate, re-parent to hidden root, enqueue
- **ClearLiveBullets**: Iterate HashSet, return all to pool (used by bomb)

Pre-allocated capacities: 400 player bullets, 900 enemy bullets. Without pooling, `Instantiate`/`Destroy` calls would trigger garbage collection pauses, causing frame hitches — catastrophic in a game running at 240 FPS target with 1000+ active bullets.

---

### Q6: Why doesn't the Unreal version use object pooling for bullets?

**Answer (reference: `STGProjectile.cpp`, `STGPawn.cpp` FireShot)**:
The Unreal version uses `World->SpawnActor<ASTGProjectile>()` and `Destroy()` for each bullet — the standard UE5 approach. UE5's actor lifecycle is managed by the engine with its own memory management (no GC like C#), so the penalty for spawn/destroy is lower. However, each `SpawnActor` still creates a new UObject with components, registers overlaps, etc. — this IS measurable overhead.

**This is a deliberate comparison point**: the thesis measures whether UE5's native actor management can match Unity's explicit pooling. Any performance difference here reflects each engine's memory management strategy.

---

### Q7: How do the two engines handle bullet movement differently?

**Answer (reference: Unity `Bullet.cs` vs Unreal `STGProjectile.cpp`)**:

**Unity**: Manual position update every frame:
```csharp
transform.position += (Vector3)(_direction * (_speed * Time.deltaTime));
```
The `Rigidbody2D` is set to `Kinematic` — it exists only for trigger detection, not physics simulation. This gives full control over movement with zero physics solver overhead.

**Unreal**: Uses `UProjectileMovementComponent`:
```cpp
ProjectileMovement->InitialSpeed = InSpeed;
ProjectileMovement->ProjectileGravityScale = 0.0f;
```
This is UE5's built-in optimized component that handles velocity, acceleration, and bouncing. Since gravity is zero, the result is identical straight-line motion, but it leverages UE5's native tick pipeline.

---

### Q8: What is the "grazing mechanic" in the Unreal version?

**Answer (reference: `STGGameSettings.h`, `STGProjectile.cpp` BeginPlay)**:
Enemy bullets have a large visual mesh (`BulletVisualScale = 0.25`) but a tiny collision sphere (`BulletCollisionRadius = 3.0`):
```cpp
CollisionComp->SetSphereRadius(CollisionRadius);  // 3.0 units
MeshComp->SetRelativeScale3D(FVector(BulletScale)); // 0.25 scale
```
This means players can visually "graze" through bullets that appear to overlap them, adding skill expression. The Unity version doesn't have this distinction — visual and collision sizes are coupled.

---

### Q9: How does frame rate targeting differ between the two implementations?

**Answer (reference: Unity `GameInitializer.cs`, Unreal project settings)**:
Unity explicitly sets `Application.targetFrameRate = 240` in code to uncap rendering. Unreal relies on project settings (default uncapped) or console commands. Both aim for maximum frame throughput to stress-test the render pipeline.

---

## Category 3: Gameplay Systems

### Q10: How does the difficulty progression work in each engine?

**Answer (reference: Unity `EnemySpawner.cs`, Unreal `STGEnemySpawner.cpp`)**:

**Unity**:
- Spawn delay: linearly interpolates from 1.6s → 0.45s over 90 seconds
- Wave size: 2–10 enemies per wave, scaling with elapsed time
- Difficulty value: 1.2 → 6.0, scaling enemy HP (+12 per unit), speed, and fire rate
- Introduction: first 4 spawns introduce each enemy type once

**Unreal**:
- Spawn interval: 0.25s → 0.08s (linear), with 0.03s "chaos" in final 5 seconds
- One enemy per spawn tick (constant stream vs Unity's wave pulses)
- Type distribution: Fodder-only at start, gradually adding Runner, Turret, Tank
- Maximum 200 simultaneous enemies

**Key difference**: Unity spawns in **waves** (2–10 at once with delays), Unreal spawns a **constant stream** (one per interval). The Unreal "final rush" at 0.03s intervals creates more extreme end-game stress.

---

### Q11: How does the player upgrade/progression system compare?

**Answer (reference: Unity `PlayerController.cs` HandleScoreChanged, Unreal `STGPawn.cpp` CheckUpgrades)**:

**Unity**: Exponential thresholds with doubling increments:
- Base threshold: 1500, then doubles (1500 → 3000 → 6000 → ...)
- Max level 12 with unlockable directional shots (side, diagonal, rear)
- Smooth escalation over very high score ranges

**Unreal**: Fixed score thresholds with explicit upgrade tiers:
- Level 1 at 100, Level 2 at 300, Level 3 at 600, Level 4 (max) at 1000
- Each level explicitly sets volley size, spread, fire rate
- Faster progression — max power reached at 1000 score

**Why different**: The Unity version has longer duration before max power, creating more gradual performance escalation. Unreal reaches max power quickly, then maintains constant load — better for steady-state benchmarking.

---

### Q12: How does the screen-clear special ability work in each engine?

**Answer (reference: Unity `PlayerController.cs` PerformBomb, Unreal `STGPawn.cpp` UseSpecial)**:

**Unity**: Coroutine-based dramatic sequence:
1. Disable controls, enable invulnerability
2. Flash white, spawn screen-clear effects
3. Kill all enemies via `EnemySpawner.ClearScreen()` (which also clears enemy bullets)
4. Dash upward, then return to starting position
5. Re-enable controls

**Unreal**: Immediate, no animation:
1. Find all `ASTGEnemy` actors → `Destroy()` each
2. Find all `ASTGProjectile` where `!bIsPlayerBullet` → `Destroy()` each
3. Done in a single frame

**Unity's approach** is more cinematic; **Unreal's approach** is simpler but functional.

---

### Q13: How are enemy types defined differently in the two implementations?

**Answer (reference: Unity `EnemyBlueprint.cs`, Unreal `STGEnemy.h`)**:

**Unity** uses `EnemyBlueprint` — a sealed immutable C# class with 19 constructor parameters defining every aspect of an enemy archetype. Blueprints are created in `EnemySpawner.BuildBlueprints()` as an array of 4 instances.

**Unreal** uses `EEnemyType` enum + `InitializeFromType()` switch statement. Each case reads values from the `STGGameSettings.h` constexpr namespaces and sets `UPROPERTY` fields accordingly.

Both achieve the same goal — data-driven enemy configuration — but:
- Unity's approach is more **object-oriented** (data class encapsulation)
- Unreal's approach is more **configuration-driven** (header constants + switch)

---

## Category 4: Technical Implementation Details

### Q14: How is collision detection handled in each engine?

**Answer (reference: Unity `Bullet.cs` OnTriggerEnter2D, Unreal `STGProjectile.cpp` OnOverlapBegin)**:

**Unity**: Uses 2D physics with `CircleCollider2D` (trigger mode) + `Rigidbody2D` (Kinematic):
- `OnTriggerEnter2D` checks for bullet-vs-bullet (same faction → ignore), bullet-vs-Health (opposite faction → damage + despawn)
- Respects player invulnerability via `PlayerController.IsInvulnerable()`

**Unreal**: Uses 3D physics with `USphereComponent` + `UBoxComponent` (overlap events):
- `OnOverlapBegin` uses `Cast<>` to identify hit actors: `ASTGEnemy` or `ASTGPawn`
- Player bullets damage enemies, enemy bullets damage player

**Key technical difference**: Unity uses 2D physics (Box2D engine internally). Unreal uses 3D physics (Chaos/PhysX) even though the game is effectively 2D. The 3D physics overhead for a 2D game is a potential benchmark comparison point.

---

### Q15: How does each engine generate sprites/meshes at runtime without external assets?

**Answer (reference: Unity `Bullet.cs` GetOrCreateSprite, `EnemySpawner.cs` GenerateSprite, Unreal `STGEnemy.cpp` constructor)**:

**Unity**: Procedurally generates `Texture2D` objects and creates `Sprite` from them:
- Bullets: 16×16 solid-color squares, cached per color in `static Dictionary<Color, Sprite>`
- Enemies: 64×64 textures with shape-specific pixel tests (disc, triangle, diamond, arrow)
- Life icons: 32×32 circles via distance-from-center
- Effects: 32×32 radial gradients (alpha = (1-dist)²)
- Stars: Full-resolution textures with random white pixels

**Unreal**: Uses built-in engine meshes:
- Player: `/Engine/BasicShapes/Cylinder` flattened (0.08×0.08×0.001)
- Enemies: `/Engine/BasicShapes/Cube` at various scales (0.25–0.8)
- Bullets: `/Engine/BasicShapes/Sphere` with dynamic material for color/emissive
- Colors via `UMaterialInstanceDynamic` set at runtime

**Implication**: Unity creates zero external dependencies — entirely procedural. Unreal reuses engine-built-in meshes — cleaner but requires the engine's asset system.

---

### Q16: How is the HUD implemented differently in each engine?

**Answer (reference: Unity `GameInitializer.cs` CreateHud, Unreal `STGHUDManager.cpp`)**:

**Unity**: Entire canvas and all UI elements built from C# code:
- `Canvas`, `CanvasScaler`, `GraphicRaycaster` components created
- `Text` components for score, timer, status
- `Image` components for life icons and damage overlay
- All positioning via `RectTransform` anchors and offsets

**Unreal**: C++ creates/manages a widget, but layout is in a UMG Blueprint:
- `CreateWidget<UUserWidget>(GetWorld(), HUDWidgetClass)` instantiates the widget
- Updates find named elements: `GetWidgetFromName("txt_Score")`
- Widget layout, fonts, and positioning defined in the editor

**Tradeoff**: Unity's approach is fully self-contained but verbose (~100 lines of UI code). Unreal's approach is concise in C++ but requires a separate UMG asset.

---

### Q17: How does the camera system differ between engines?

**Answer (reference: Unity `GameInitializer.cs` BuildCamera, Unreal `STGFixedCamera.cpp`)**:

**Unity**: Simple orthographic camera:
```csharp
cam.orthographic = true;
cam.orthographicSize = 6.5f;
cam.transform.position = new Vector3(0f, 0f, -10f);
```
6.5 units = half the visible height. The camera is 2D by design.

**Unreal**: Perspective camera with trigonometric auto-fit:
```cpp
float HeightForWidth = HalfWidth / FMath::Tan(HalfFOVRad);
float HeightForHeight = HalfHeight / FMath::Tan(VerticalHalfFOVRad);
return FMath::Max(HeightForWidth, HeightForHeight);
```
Calculates required Z-height to fit the 1700×900 play area within 60° FOV, assuming 16:9 aspect ratio.

**Why different**: Unity's 2D pipeline natively supports orthographic. Unreal's 3D pipeline typically uses perspective — even for top-down games, this requires explicit camera distance calculation.

---

## Category 5: Testing & Benchmarking

### Q18: How are the games configured for automated performance testing?

**Answer (reference: Unity `PlayerController.cs` CheckCommandLineArgs, Unreal `STGPawn.cpp` BeginPlay + `STGGameDirector.cpp`)**:

Both support command-line flags:

| Flag | Unity | Unreal |
|------|-------|--------|
| Invincibility | `--invincible` | `--invincible` |
| No player movement | `--stationary` | `--stationary` |
| Auto-quit on end | N/A | `--autoquit` |
| Custom duration | N/A | `--duration=N` |
| Start at time offset | N/A | `--start-time=N` |

Usage: `./Final.x86_64 --invincible --stationary` (Unity) or passing flags via UE5 launch arguments.

These modes enable:
- **`--invincible`**: Prevents game-over during unattended profiling runs
- **`--stationary`**: Isolates enemy/spawner performance by removing player bullet generation
- **`--autoquit`**: Clean exit for batch profiling (Nsight capture scripts)
- **`--start-time=N`**: Jump to specific difficulty phase for targeted profiling

---

### Q19: What makes these implementations suitable for a fair engine comparison?

**Answer**: The games are designed with parity in mind:
1. **Same game concept** — top-down bullet hell with survival timer
2. **Same duration** — 90 seconds
3. **Same complexity arc** — escalating enemies and bullet counts
4. **Same test modes** — invincibility and stationary mode
5. **Equivalent enemy variety** — 4 types each, with similar gameplay roles
6. **Equivalent mechanics** — player shooting, screen-clear special, score-based upgrades

**Intentional differences** highlight engine characteristics:
- Unity uses object pooling → shows GC management approach
- Unreal uses spawn/destroy → shows native memory management
- Unity uses 2D physics → lightweight collision
- Unreal uses 3D physics → full physics engine for a 2D game
- Unity builds UI in code → no external assets
- Unreal uses UMG widgets → engine's standard UI system

---

### Q20: What specific metrics can be compared using these implementations?

**Answer**: Both games generate comparable workloads measurable via NVIDIA Nsight:
1. **Draw calls** — sprite rendering (Unity 2D) vs mesh rendering (Unreal 3D)
2. **GPU frame time** — shader complexity, overdraw, particle effects
3. **CPU frame time** — game logic, physics, spawning overhead
4. **Memory allocation patterns** — pooled (Unity) vs dynamic (Unreal)
5. **Physics overhead** — Box2D 2D triggers (Unity) vs Chaos/PhysX 3D overlaps (Unreal)
6. **Actor/object count scaling** — how each engine handles 100→1000+ active entities
7. **VFX cost** — sprite scaling (Unity) vs Niagara particles (Unreal)
8. **Input latency** — Legacy Input (Unity) vs Enhanced Input (Unreal)
