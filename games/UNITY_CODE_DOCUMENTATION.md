# Unity Bullet Hell — Complete Code Documentation

**Project**: `magisterka_2/` (Unity 2D, C#)
**Namespace**: `Magisterka.BulletHell`
**Purpose**: Performance benchmark bullet-hell shooter for comparing Unity vs Unreal Engine.
**Duration**: 90-second survival round with escalating difficulty.

---

## Architecture Overview

The project follows a **scene-free bootstrap pattern**: the game builds itself entirely at runtime from C# code, with no dependency on a pre-configured Unity scene. This is done via:

1. **`GameBootstrap`** — Static class with `[RuntimeInitializeOnLoadMethod]` that ensures `GameInitializer` exists.
2. **`GameInitializer`** — MonoBehaviour that constructs the entire game hierarchy: camera, player, pools, HUD, spawner, director.

This architecture means the game can run from a completely empty scene — ideal for reproducible benchmarking across machines.

### Dependency Graph

```
GameBootstrap → GameInitializer
                  ├── Camera (orthographic, 2D)
                  ├── BackgroundScroller (parallax starfield)
                  ├── EffectManager (VFX pooling)
                  ├── ScoreManager (HUD + score)
                  ├── BulletPool × 2 (player & enemy)
                  ├── PlayerController
                  ├── EnemySpawner
                  └── GameDirector (timer, victory, game-over)
```

### Key Design Patterns

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Singleton** | `GameDirector`, `EnemySpawner`, `ScoreManager`, `EffectManager`, `PlayerController` | Provides global access to managers via `.Instance` |
| **Object Pooling** | `BulletPool`, `EffectManager` | Eliminates per-frame allocation; critical for performance at 1000+ active bullets |
| **Bootstrap/Factory** | `GameBootstrap` + `GameInitializer` | Scene-independent initialization for benchmark reproducibility |
| **Component Composition** | `[RequireComponent(typeof(Health))]` on `EnemyController` and `PlayerController` | Ensures Health component always present; decouples damage logic from entity logic |
| **Event-driven Communication** | `Health.Died`, `Health.Damaged`, `ScoreManager.ScoreChanged` | Loose coupling between systems via C# events/delegates |
| **Blueprint/Data-driven Configuration** | `EnemyBlueprint` class | Runtime data objects define enemy archetypes without requiring ScriptableObjects |

---

## File-by-File Documentation

### 1. `Faction.cs` — Combat Side Identifier

**What it does**: Defines a simple enum with two values: `Player` and `Enemy`.

**Why it works this way**: Used throughout the collision and damage system to prevent friendly fire. When a bullet hits a `Health` component, factions are compared — bullets only damage entities of the opposite faction. This is the simplest possible friend-or-foe identification, avoiding complex layer setups.

**Key detail**: Stored as `int` (Player=0, Enemy=1), making comparison extremely cheap.

---

### 2. `GameBootstrap.cs` — Runtime Scene Initializer

**What it does**: A static class with `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]` that runs automatically after any scene loads. It checks if a `GameInitializer` already exists; if not, it creates one and marks it `DontDestroyOnLoad`.

**Why it works this way**: This guarantees the game bootstraps correctly regardless of which scene is loaded or how the build is configured. No manual scene setup needed. The `AfterSceneLoad` timing ensures the scene hierarchy is ready before initialization begins.

**Performance relevance**: Zero runtime cost — runs exactly once at startup.

---

### 3. `GameInitializer.cs` — Full Scene Builder

**What it does**: A MonoBehaviour that constructs the **entire game** programmatically in `Awake()`:
- Creates an orthographic 2D camera (size 6.5, black background, positioned at z=-10)
- Sets `Application.targetFrameRate = 240` (uncapped for benchmarking)
- Hides cursor
- Creates `BackgroundScroller`, `EffectManager`, `ScoreManager`
- Creates two `BulletPool` instances (player: 400 warm, cyan; enemy: 900 warm, orange-red)
- Creates `PlayerController` with calculated movement bounds from camera aspect
- Builds the entire HUD (canvas, score label, life icons, timer, game-over text, damage overlay)
- Creates `EnemySpawner` and `GameDirector`, wiring them together

**Why it works this way**: Building everything in code means:
1. **No scene dependency** — benchmarks are perfectly reproducible
2. **Single source of truth** — all wiring is visible in one file
3. **No serialization bugs** — no missing references from scene changes

**HUD construction detail**: The `CreateHud()` method builds the entire UI canvas from scratch including:
- Score text (upper-left, 24pt)
- Life icons (programmatically generated circular sprites via `BuildLifeSprite()`)
- Timer text (upper-right, 24pt)
- Game over/victory text (center, 48pt, initially hidden)
- Damage overlay (full-screen red flash, initially transparent)

**`BuildLifeSprite()`**: Generates a 32×32 pixel circular texture at runtime using distance-from-center calculation. No external assets needed.

---

### 4. `GameDirector.cs` — Game Flow Controller

**What it does**: Singleton MonoBehaviour that manages the overall game timer and end conditions:
- Counts down from `totalDuration` (90s) to 0
- When timer hits 0: stops the spawner, enters "cleanup phase"
- During cleanup: waits until `_spawner.HasActiveEnemies` is false, then triggers victory
- On player death (game over): stops the timer
- Updates the timer UI label every frame in `MM:SS` format

**Why it works this way**: The two-phase end condition (timer expired → wait for enemies cleared) prevents an abrupt ending while enemies are still on screen. The player must survive AND clear all remaining enemies after time runs out.

**State machine**:
```
RUNNING → _timeRemaining <= 0 → EXPIRED (spawning stops)
EXPIRED → no active enemies  → VICTORY
RUNNING → player dies         → GAME OVER
```

---

### 5. `Health.cs` — Hit Point System

**What it does**: Tracks HP for any entity (player or enemy). Exposes:
- `Configure(faction, maxHP)` — sets faction and max health
- `ApplyDamage(amount, hitPoint)` — reduces HP, spawns hit effect, fires `Damaged` event, triggers death at 0
- `RestoreFull()` — resets to max HP (used on player respawn)
- `Kill()` — instant death (used by bomb screen-clear)
- Events: `Died` (Action<Health>), `Damaged` (Action<float, Vector2>)

**Why it works this way**: Decoupled from entity logic. `PlayerController` and `EnemyController` both `[RequireComponent(typeof(Health))]` and subscribe to events. This means the damage system works identically regardless of who takes damage — the same `ApplyDamage` path is used for player health, enemy health, and bullet-vs-bullet collision.

**Hit effect integration**: Every `ApplyDamage` call automatically triggers `EffectManager.SpawnHitEffect()`, so visual feedback is always consistent.

---

### 6. `BulletPool.cs` — Object Pool for Bullets

**What it does**: Manages a pool of `Bullet` objects using a `Queue<Bullet>` (for O(1) get/return) and a `HashSet<Bullet>` for tracking live bullets:
- `Create(parent, name, color, faction, warmCount)` — static factory that creates and pre-warms the pool
- `Spawn(position, direction, speed, damage)` — activates a pooled bullet or creates a new one if pool is empty
- `Return(bullet)` — deactivates and re-queues the bullet
- `ClearLiveBullets()` — returns all active bullets to pool (used by bomb and screen clear)

**Why it works this way**: In a bullet-hell game, thousands of bullets are spawned and destroyed per second. Without pooling, `Instantiate`/`Destroy` would generate massive GC pressure. The `Queue` provides FIFO reuse, and the `HashSet` enables O(1) membership checking for `ClearLiveBullets()`.

**Warm capacity**: Pre-allocates 400 player bullets and 900 enemy bullets at startup to avoid first-frame allocation spikes. These numbers were tuned empirically to the game's peak bullet counts.

**Pool hierarchy**: Inactive bullets are parented to a hidden `_poolRoot` transform. When spawned, bullets are unparented (`SetParent(null)`) to avoid transform hierarchy overhead.

---

### 7. `Bullet.cs` — Individual Bullet Behavior

**What it does**: Each bullet moves in a straight line at constant speed, checks bounds, and handles collisions:
- Movement: `transform.position += direction * speed * deltaTime` (no physics engine)
- Bounds check: despawns if beyond ±14 units from origin
- Collision via `OnTriggerEnter2D`:
  - Bullet vs bullet (opposite faction): both despawn
  - Bullet vs Health (opposite faction): applies damage, despawns
  - Respects player invulnerability
- **Sprite caching**: `static Dictionary<Color, Sprite> SpriteCache` — generates colored 16×16 pixel textures once and reuses them

**Why it works this way**: Using `transform.position` directly instead of `Rigidbody2D.velocity` gives deterministic control over movement. The `Rigidbody2D` is set to `Kinematic` with `Interpolation` — it exists only so Unity's physics system can generate trigger events, not for actual physics simulation.

**Sprite generation**: Bullets generate their own 16×16 solid-color sprites via a static cache. This avoids needing any sprite assets and ensures bullets of the same color share the same `Sprite` object.

---

### 8. `EnemyBlueprint.cs` — Enemy Archetype Configuration

**What it does**: A sealed immutable data class that defines all parameters for an enemy type:
- Name, color, scale, sprite
- Movement style (`EnemyMovementStyle` enum: ZigZag, Straight, Sine, Orbit)
- Fire style (`EnemyFireStyle` enum: None, Radial, Stream, Burst)
- Numerical stats: move speed, horizontal amplitude/frequency, fire interval, bullets per volley, bullet speed/damage, contact damage, health, score value, orbit radius, centering bias

**Why it works this way**: Using a plain C# class instead of `ScriptableObject` keeps everything in code (no Unity asset files). The 19-parameter constructor is intentionally explicit — it makes the 4 enemy definitions in `EnemySpawner.BuildBlueprints()` fully self-documenting.

**Four archetypes**:
| Name | Movement | Fire | Behavior |
|------|---------|------|----------|
| **Blazer** | ZigZag | Radial | Orange, zig-zags down, fires radial bursts (12+ bullets) |
| **Striker** | Straight | Stream | Purple, drops straight down, fires aimed stream + homing shots |
| **Cascade** | Sine | Burst | Green, sine-waves, fires tight burst salvos |
| **Interceptor** | Orbit | None | Yellow, fast orbital movement, no shooting, relies on collision |

---

### 9. `EnemyController.cs` — Enemy AI and Behavior

**What it does**: Controls individual enemy behavior every frame:
- **Movement**: Four movement patterns based on `EnemyBlueprint.Movement`:
  - `ZigZag`: Moves down + sinusoidal horizontal offset
  - `Straight`: Pure downward movement
  - `Sine`: Downward + absolute sine positioning (position-based, not velocity-based)
  - `Orbit`: Circular/elliptical path with slower vertical descent
- **Firing**: Three firing patterns based on `EnemyBlueprint.Fire`:
  - `Radial`: N bullets evenly around 360° with a rotating offset
  - `Stream`: Downward spread + one homing shot aimed at the player
  - `Burst`: Triple salvos of 3 bullets each at increasing spread
- **Difficulty scaling**: All stats scale with `_difficulty` parameter: health increases (+12 per difficulty unit), movement speeds up, fire rate decreases, radial bullet count increases
- **Death**: Awards score, spawns explosion effect, notifies spawner, destroys self
- **Contact damage**: If the enemy's collider touches the player, deals `ContactDamage` and the enemy self-destructs
- **Despawn**: If the enemy falls below the camera view by `despawnPadding`, it's cleaned up

**Why it works this way**: The pattern-based movement system allows each enemy type to feel distinct while sharing the same update loop. Difficulty scaling is multiplicative — the same `AdvanceMovement()` code handles early weak enemies and late-game tough ones.

**Centering bias**: Some enemies (Blazer with 1.2 bias) tend to drift toward center X, making them cluster dangerously. This creates organic difficulty without specific AI pathfinding.

---

### 10. `EnemySpawner.cs` — Wave Generation System

**What it does**: Singleton that continuously spawns enemy waves with escalating difficulty:
- **Spawn routine**: Coroutine that loops for `totalDuration` (90s), spawning waves at decreasing intervals
- **Spawn delay curve**: Linearly interpolates from `spawnDelayStart` (1.6s) to `spawnDelayEnd` (0.45s) based on elapsed time
- **Introduction phase**: First 4 enemies are spawned one at a time (one of each type) so the player sees all archetypes
- **Wave composition**: After introduction, spawns 2–10 enemies per wave, scaling with elapsed time (`1 + elapsed * 0.05`)
- **Difficulty value**: Linearly interpolates from 1.2 to 6.0 based on game progress
- **Spatial distribution**: Enemies spawn at the top of the camera view, horizontally distributed with slight randomness and centering bias
- **Screen clear**: `ClearScreen()` kills all active enemies and clears all enemy bullets (used by player bomb)
- **Procedural sprites**: `GenerateSprite()` creates 64×64 pixel textures for four shapes: Disc, Triangle, Diamond, Arrow
- **Blueprint definitions**: `BuildBlueprints()` creates all four enemy archetypes with hardcoded stats

**Why it works this way**: The coroutine-based spawn loop allows natural timing control without complex state machines. The escalating difficulty curve ensures the game gets progressively harder over 90 seconds — from manageable waves of 2–3 enemies to frantic swarms of 10.

**Enemy tracking**: A `List<EnemyController> _liveEnemies` tracks all active enemies. This is critical for:
- `HasActiveEnemies` (checked by GameDirector for victory condition)
- `ClearScreen()` (iterating all enemies to kill them)

---

### 11. `PlayerController.cs` — Player Input and Progression

**What it does**: Comprehensive player logic:

**Movement** (WASD/arrows):
- Base speed 12 units/s, focus mode (LeftShift) at 0.6× speed
- Clamped to camera bounds with 0.5 unit padding

**Shooting** (Z key or left mouse):
- Auto-fire at 0.12s intervals (8.3 shots/sec)
- Fires a volley of bullets in a fan pattern, size based on level
- Base volley: 5 bullets with angular spread increasing by level
- Extra directional shots unlock at levels 2, 4, 6, 8 (side, diagonal, back shots)

**Bomb** (X key or space or right mouse):
- One-use screen clear: destroys all enemies, clears all bullets
- Visual: player flashes white, dashes upward then returns
- Grants temporary invulnerability during animation

**Progression system**:
- Level calculated from score using exponential thresholds: `baseLevelThreshold` (1500), doubling each level
- Max level: 12
- Each level-up: visual flash, explosion effect, camera shake
- Stats affected: volley width (more bullets), extra directional shots

**Health/Lives**:
- Starts with `maxLives` (default 1)
- On death: explosion VFX, renderer disabled, wait `respawnDelay` (0.7s), clear screen, reposition to bottom, flash invulnerability for 2s
- If lives < 0: game over sequence

**Test modes** (command-line or runtime toggles):
- `--invincible` / I key: permanent invulnerability (yellow color indicator)
- `--stationary` / P key: disables all movement and shooting (for passive performance testing)

**Why it works this way**: The progression mechanic (score → level → more bullets) creates a natural performance escalation: as the player gets stronger, more player bullets are on screen, increasing GPU/CPU load. This is deliberate for benchmarking — the workload scales organically over the 90-second run.

**Test modes rationale**: `--invincible` prevents game-over during unattended benchmark runs. `--stationary` isolates enemy/spawner performance by removing player bullet generation.

---

### 12. `ScoreManager.cs` — Score and HUD Controller

**What it does**: Singleton that manages:
- Score accumulation and display (`Score: N`)
- Life icon visibility (enabling/disabling `Image` components)
- Status messages ("GAME OVER" in red, "YOU WIN" in green)
- Damage flash overlay (full-screen red pulse with sine-curve fade)
- `ScoreChanged` event (consumed by `PlayerController` for level-up detection)

**Why it works this way**: The queued initialization pattern (`_queuedLives`, `_queuedStatus`) handles race conditions where `SetLives()` or status messages are called before the HUD is fully constructed. This is essential because `PlayerController.Initialize()` and `ScoreManager.Initialize()` may run in unpredictable order.

**Damage flash**: The `DamageFlashRoutine` uses a sine curve (`sin(normalized * PI)`) to create a smooth peak-and-fade effect. Strength parameter controls peak alpha (0.35–0.75).

---

### 13. `EffectManager.cs` — Visual Effects Hub

**What it does**: Singleton managing all visual feedback using pooled `EffectPulse` sprites:
- `SpawnHitEffect(position, faction, intensity)` — 1–3 expanding circles (color by faction)
- `SpawnExplosion(position, faction, size)` — 4 concentric expanding circles
- `SpawnScreenClear(position, radius)` — 6 large expanding circles + camera shake
- `ShakeCamera(duration, strength)` — delegates to `CameraShaker`
- Internal pool of `EffectPulse` objects (warmed to 64, recycled via callbacks)

**Why it works this way**: Like `BulletPool`, effect objects are pooled to avoid GC spikes. The multi-pulse explosion technique (multiple expanding circles at different speeds) creates convincing explosion effects using only simple scaling sprites — no particle systems, no shaders.

---

### 14. `EffectPulse.cs` — Animated Sprite Effect

**What it does**: A single expanding, fading sprite:
- `Play(position, color, startSize, endSize, duration, callback)` — configure and start
- Each frame: interpolates scale from start to end, fades alpha from 1 to 0
- On completion: deactivates self, invokes recycle callback

**Sprite generation**: `BuildPulseSprite()` creates a 32×32 radial gradient texture (alpha = (1 - distance)²) giving a soft, circular glow effect.

**Why it works this way**: The radial gradient sprite combined with scale animation creates the appearance of an expanding shockwave or explosion ring. The quadratic alpha falloff (`alpha * alpha`) ensures edges are smooth.

---

### 15. `CameraShaker.cs` — Screen Shake

**What it does**: Attached to the main camera, provides juicy screen shake:
- `Shake(duration, strength)` — sets shake parameters (max of current and new)
- Each frame during shake: random offset within `_shakeStrength` circle, strength decaying over time
- After shake: smoothly lerps back to original position

**Why it works this way**: The "max of current and new" approach allows overlapping shakes without resetting, creating more organic screen feedback during intense combat.

---

### 16. `BackgroundScroller.cs` — Parallax Starfield

**What it does**: Creates two large starfield tiles and scrolls them downward at different speeds:
- Tile A: scrolls at `scrollSpeed` (full speed)
- Tile B: scrolls at `scrollSpeed * parallaxFactor` (0.6× speed, creating depth illusion)
- When a tile scrolls off the bottom, it teleports back above the top (infinite loop)
- `GenerateStarSprite()`: Creates a procedural starfield texture — dark background with random white pixels (star density: ~1 per 45 pixels)

**Why it works this way**: The parallax effect gives depth to a 2D game with zero external assets. Two tiles ensure seamless continuous scrolling. The procedural generation means no texture files are needed in the build.

---

## Performance-Critical Design Decisions

| Decision | Rationale |
|----------|-----------|
| Object pooling for bullets and effects | Avoids GC allocation spikes from `Instantiate`/`Destroy` |
| `transform.position` movement (no physics forces) | Deterministic movement, no physics solver overhead |
| Kinematic Rigidbody2D on bullets | Enables trigger detection without full physics simulation |
| Procedural sprite/texture generation | Zero asset loading, reproducible across machines |
| `targetFrameRate = 240` | Uncapped rendering for benchmarking |
| Scene-free bootstrap | Eliminates scene deserialization variability |
| HashSet for live bullet tracking | O(1) membership test during screen clears |
| Static sprite caching (Bullet.SpriteCache) | Single shared texture per color |
