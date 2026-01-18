# Part 9 (C++): Polish & Debug Features

[← Previous: Part 8 (C++) - Create Game Mode](part-8-cpp-create-game-mode.md) | [Back to Index](README.md) | [Next: Part 10 (C++) - Final Setup →](part-10-cpp-final-setup.md)

---

## Overview

Add debug cheats, visual polish, enemy variety, and optimization for a complete game experience.

**Time:** ~30 minutes

---

## Step 9.1: Add Debug Cheat (Invincibility Toggle)

### Create Input Action

1. **Content Browser** → Right-click → **Input → Input Action**
2. Name: `IA_CheatInvincible`
3. Save

### Add to Input Mapping Context

1. Open `IMC_Player`
2. Click **+** to add new mapping
3. Select `IA_CheatInvincible`
4. **Key:** Click dropdown → Select **I** key
5. Save

### Configure BP_Player

1. Open **BP_Player**
2. In **Class Defaults** → **Input** section:
   - **Cheat Invincible Action** → Select `IA_CheatInvincible`
3. **Compile** and **Save**

### Test

Press **I** during gameplay → Should see "[CHEAT] INVINCIBILITY ON/OFF" message.

---

## Step 9.2: Fixed Camera Setup

The player-attached camera moves with the player. For a bullet-hell game, we want a **fixed camera** showing the entire play area.

### New STGFixedCamera Class

The camera has been removed from STGPawn. A new `STGFixedCamera` actor handles the view.

**Key Feature:** The camera **automatically calculates** the correct height to show exactly the play area defined in `STGGameDirector`. No manual tweaking needed!

**Key Properties:**
- `bAutoFitPlayArea` - When true (default), camera auto-sizes to fit the play area
- `PlayAreaMargin` - Extra margin around play area (default: 5%)
- `FieldOfView` - Camera FOV (default: 60°)
- `bUseOrthographic` - Enable for 2D-style flat projection

### Play Area Bounds (STGGameDirector)

The play area is now centrally defined in `STGGameDirector`:
- `PlayAreaMin` - Bottom-left corner (default: -850, -450)
- `PlayAreaMax` - Top-right corner (default: 850, 450)

**Changing the play area in Game Director automatically updates the camera view!**

### Level Setup

1. Open your game level in the editor
2. Open the **Place Actors** panel:
   - **Menu:** Window → Place Actors
3. In the Place Actors panel, click the **Search** field
4. Type `STGFixedCamera`
5. **Drag** the `STGFixedCamera` class from the panel into your level viewport
6. The camera will automatically position itself to show the play area on BeginPlay

**Optional adjustments** (in Details panel):
- **Play Area Margin** - Increase for more space around edges
- **Field of View** - Higher values = wider angle, lower camera height
- **bAutoFitPlayArea** - Disable to use manual `CameraHeight` instead

The camera automatically activates on BeginPlay and displays a debug message showing the calculated height.

---

## Step 9.3: Enemy Variety

Four enemy types with incremental difficulty - enemies start completely harmless and gradually become more threatening:

| Type | Shape | Color | HP | Speed | Bullets | Difficulty |
|------|-------|-------|----|----|---------|------------|
| **Fodder** | Tiny square | Green | 1 | Very slow | None | ⭐ Easiest |
| **Runner** | Diamond ◇ | Cyan | 3 | Medium | None | ⭐⭐ Easy |
| **Turret** | Square ■ | Orange | 15 | Slow | 4 (360°) | ⭐⭐⭐ Medium |
| **Tank** | Rectangle ▬ | Red | 50 | Crawling | 20 (360°) | ⭐⭐⭐⭐ Hard |

### Incremental Design Philosophy

- **Fodder**: Training targets - dies in 1 hit, no threat, SPAM these!
- **Runner**: Adds speed challenge - still no bullets, but harder to hit
- **Turret**: Introduces bullets GENTLY - slow, few bullets (first shooter)
- **Tank**: Full challenge - tanky HP + bullet hell (rapid fire)

### Visual Distinction (Top-Down)

All shapes are flat cubes with different scales/rotations:

- **Fodder** - Tiny green square (easy to spot, easy to kill)
- **Runner** - Cyan diamond (rotated 45°, quick movement)
- **Turret** - Orange square (medium size, first to shoot)
- **Tank** - Red wide rectangle (large, intimidating)

### Difficulty Progression (Fodder Spam!)

- **0-25%**: All Fodder - endless targets!
- **25-50%**: Fodder (85%) + Runner (15%) - almost all fodder
- **50-75%**: Fodder (70%) + Runner (20%) + Turret (10%) - mostly fodder
- **75-100%**: Fodder (55%) + Runner (20%) + Turret (15%) + Tank (10%)

---

## Step 9.4: Player Upgrade System

Player starts WEAK and gets stronger with score! Classic arcade progression.

### Starting Stats (Level 0)

- **Volley**: 1 bullet (single shot)
- **Fire Rate**: 0.5 seconds (slow)
- **Spread**: 0° (straight ahead)

### Upgrade Thresholds

| Level | Score | Bullets | Fire Rate | Spread |
|-------|-------|---------|-----------|--------|
| 0 | 0 | 1 | 0.50s | 0° |
| 1 | 100 | 2 | 0.35s | 8° |
| 2 | 300 | 3 | 0.20s | 12° |
| 3 | 600 | 4 | 0.12s | 16° |
| 4 | 1000 | 5 | 0.08s | 20° |

### How It Works

```cpp
void ASTGPawn::CheckUpgrades()
{
    // Called every time score changes
    // Compares score against STG::Player::UpgradeScore1-4 thresholds
    // Increases VolleySize, VolleySpread, decreases FireInterval
    // Shows "POWER UP!" message on screen
}
```

---

## Step 9.4: Distinct Bullet Visuals

Bullets now have different sizes, brightness, and **grazing** support:

**Player Bullets:**

- Scale: 0.06 (small)
- Emissive Intensity: 2.0 (dim)
- Color: Soft green (0.2, 0.8, 0.3)

**Enemy Bullets (with Grazing!):**

- Visual Scale: 0.25 (LARGE - easy to see)
- Collision Radius: 3.0 (TINY hitbox)
- Emissive Intensity: 8.0 (bright glow)
- Color: Orange-red (1.0, 0.3, 0.1)

> **Grazing Mechanic**: Enemy bullets appear large but have tiny hitboxes.
> Players can "touch" bullets visually without dying - a classic bullet-hell feature!

---

## Step 9.5: Centralized Game Settings

All game constants are now defined in **`STGGameSettings.h`** - one file to rule them all!

### What's Centralized

| Category | Examples |
|----------|----------|
| **Play Area** | MinX/MaxX, MinY/MaxY, Width/Height |
| **Game Timing** | DefaultDuration (60s), DebugQuickDuration (10s) |
| **Player** | MoveSpeed, FireInterval, BulletSpeed, MaxLives |
| **Enemy Types** | Health, ScoreValue, Speed, BurstSpread for each type |
| **Spawner** | BaseSpawnInterval, MaxSimultaneousEnemies |
| **Camera** | DefaultFOV, DefaultHeight, DefaultMargin |
| **VFX** | DeathParticleCount |

### Usage in Code

```cpp
#include "STGGameSettings.h"

// Access via namespaces
float speed = STG::Player::MoveSpeed;
float width = STG::PlayArea::Width;
int32 health = STG::Enemy::Tank::Health;
```

### Changing Values

1. Open `Source/BulletHellCPP/STGGameSettings.h`
2. Find the value you want to change
3. Modify it once - all systems update automatically!

**Example:** To change play area size:
```cpp
namespace PlayArea
{
    constexpr float MinX = -1000.0f;  // Was -850
    constexpr float MaxX = 1000.0f;   // Was 850
    // ... camera, player bounds, spawner all update automatically
}
```

---

## Step 9.6: 60-Second Game Duration

Game duration is now set in `STGGameSettings.h`:

- `STG::Game::DefaultDuration` = 60.0f (1 minute)
- `STG::Spawner::BaseSpawnInterval` = 1.0f
- `STG::Spawner::MinSpawnInterval` = 0.5f (end-game intensity)

---

## Step 9.7: Hit/Death Visual Effects (Niagara)

VFX properties added to enemies and player for GPU-intensive particle effects.

### Create Niagara Systems

1. **Content Browser** → Right-click → **FX → Niagara System**
2. Select **"New system from selected emitter(s)"**
3. Search and add **"Fountain"** emitter as base
4. Create two systems:
   - `NS_HitEffect` - Small burst (50-100 particles)
   - `NS_DeathExplosion` - Large explosion (500+ particles)

### Configure Hit Effect

1. **Open** `NS_HitEffect` (double-click in Content Browser)
2. You'll see the **System Overview** panel in the center with the emitter graph
3. Click on the **Fountain** emitter (right panel) to select it

**Emitter Update Section:**

4. Find **Emitter State** → Click on it
5. Change **Life Cycle Mode** from `Self` to **System**
6. **IMPORTANT:** Set **Loop Behavior** to **Once** (not Infinite!)
   - This makes the emitter play once and then mark itself as complete
   - Without this, the particles stay forever!

**Configure Spawn Rate for Burst:**

7. Keep the existing **Spawn Rate** module in **Emitter Update** (don't delete it)
8. Click on **Spawn Rate** to select it
9. If you see a warning **"The module has unmet dependencies"**:
   - Click **"Fix issue"** to move SpawnRate after EmitterState (required order)
10. In the **Selection** panel (right side), set:
    - **Spawn Rate** = `500` (high value to spawn many particles quickly)
11. The particles will burst once because **Life Cycle Mode = System** (set in step 5) makes the emitter fire only when the system is triggered, not continuously

**Particle Spawn Section:**

10. Click **Initialize Particle** module
11. Find **Lifetime** → Set **Lifetime Min** = `0.3`, **Lifetime Max** = `0.5`
12. Find **Sprite Size** → Set **Sprite Size Min** = `3`, **Sprite Size Max** = `8`

13. Click **Add Velocity** (or **Add Velocity in Cone**) module
14. Set **Velocity Strength Min** = `200`, **Velocity Strength Max** = `400`

**Particle Update Section:**

15. Click **Scale Color** module (in Particle Update)
16. The module scales color/alpha over the particle's lifetime using curves:
    - **Scale Mode** = `RGB and Alpha Separately` (default is fine)
    - **Scale Alpha** → Check the box, set to **Float from Curve**
    - In the **FloatCurve** graph below, the curve should go from **1.0** (left/start) to **0.0** (right/end)
    - This makes particles fade out over their lifetime
17. To edit the curve: click on the curve line, drag points, or use the **Templates** buttons (the curve icons) to pick a preset fade shape

**Render Section:**

18. Ensure **Sprite Renderer** is enabled (checked)

19. Click **Compile** (top toolbar) → Then **Save**

### Configure Death Explosion

1. **Open** `NS_DeathExplosion`
2. Click the **Fountain** emitter to select it

**Emitter Update:**

3. Click on **Spawn Rate** module
4. If you see a dependency warning, click **"Fix issue"**
5. Set **Spawn Rate** = `1000` (high value for big explosion)
6. Click **Emitter State**:
   - Change **Life Cycle Mode** to `System`
   - **IMPORTANT:** Set **Loop Behavior** to **Once** (prevents particles staying forever)

**Particle Spawn:**

7. In **Initialize Particle**:
   - **Lifetime Min** = `0.5`, **Lifetime Max** = `1.0`
   - **Sprite Size Min** = `5`, **Sprite Size Max** = `15`

8. In **Shape Location** → Set **Shape Primitive** = `Sphere`
9. In **Add Velocity** → Set **Velocity Strength Min** = `500`, **Max** = `800`

**Particle Update:**

10. Click **+** next to **Particle Update** → Search and add `Drag`
11. Set **Drag** = `2.0` (particles slow down naturally)

12. In **Scale Color**:
    - Start: **Red** (1.0, 0.2, 0.0) with alpha 1.0
    - End: **Yellow** (1.0, 0.8, 0.0) with alpha 0.0

13. **Compile** and **Save**

### Assign in Blueprints

**Create BP_Enemy:**

1. **Content Browser** → Right-click → **Blueprint Class**
2. In the popup, expand **All Classes** and search for `STGEnemy`
3. Select **STGEnemy** as the parent class → Click **Select**
4. Name it `BP_Enemy`
5. Open `BP_Enemy` (double-click)
6. Click **Class Defaults** (top toolbar)
7. In the **Details** panel, search for `vfx`
8. Under **VFX** section:
   - **Hit Effect** → Select `NS_HitEffect` from dropdown
   - **Death Effect** → Select `NS_DeathExplosion` from dropdown
   - **Death Particle Count** → `500`
9. **Compile** and **Save**

**Configure Spawner to use BP_Enemy:**

1. **Rebuild the project** (the C++ code was updated to add Enemy Class property)
2. Find `STGEnemySpawner` in your level (World Outliner)
3. Select it → Look at **Details** panel
4. Under **Spawning** section, find **Enemy Class**
5. Click the dropdown → Select `BP_Enemy`
6. Save level

> **Note:** If you don't see "Enemy Class", rebuild the C++ project. The property was just added to STGEnemySpawner.

**For Player:**
1. Open `BP_Player`
2. In **Class Defaults → VFX**:
   - **Hit Effect** → `NS_HitEffect`

---

## Step 9.8: Fix HUD Visibility

The HUD won't display unless `WBP_HUD` is assigned to the HUD Manager.

### Configure STGHUDManager in Level

1. Select `STGHUDManager` in your level
2. In **Details** panel → **UI** section:
   - **HUD Widget Class** → Select `WBP_HUD`
3. Save level

### Update WBP_HUD for Victory/Game Over

Add a result text block:

1. Open `WBP_HUD`
2. Add **Text** widget
3. Name: `txt_Result`
4. Position: Center of screen
5. Font Size: 72+
6. Set **Visibility** to **Hidden** (initially)
7. Save

The code will show/hide this text and set appropriate color for Victory (green) or Game Over (red).

---

## Step 9.9: Test All Features

1. Press **Play**
2. Verify:
   - ✅ Camera is fixed, shows entire play area
   - ✅ Different enemy types spawn as game progresses
   - ✅ Player bullets small/dim, enemy bullets large/bright
   - ✅ Hit effects appear when enemies are damaged
   - ✅ Death explosions are visually impressive
   - ✅ HUD shows Score, Lives, Timer
   - ✅ Press **I** to toggle invincibility
   - ✅ Victory/Game Over text appears at end

---

## Summary

Added:

- ✅ Invincibility cheat (I key)
- ✅ Fixed camera showing entire play area (auto-fits to play bounds)
- ✅ **Centralized game settings** (`STGGameSettings.h`)
- ✅ 4 enemy types with different behaviors
- ✅ Distinct bullet visuals (size/brightness)
- ✅ 60-second game duration
- ✅ Niagara particle effects (GPU-intensive)
- ✅ HUD configuration instructions
- ✅ Victory/Game Over display in HUD

---

[← Previous: Part 8 (C++) - Create Game Mode](part-8-cpp-create-game-mode.md) | [Back to Index](README.md) | [Next: Part 10 (C++) - Final Setup →](part-10-cpp-final-setup.md)
