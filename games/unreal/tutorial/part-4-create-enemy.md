# Part 4: Create the Enemy

[← Previous: Part 3 - Create the Bullet](part-3-create-bullet.md) | [Back to Index](README.md) | [Next: Part 5 - Create Enemy Spawner →](part-5-create-spawner.md)

---

## Step 4.1: Create Enemy Blueprint

1. Content Browser → Blueprints
2. Right-click → **Blueprint Class** → **Actor**
3. Name: `BP_Enemy`
4. Double-click to open

5. **Add Components:**
   - Paper Sprite → `EnemySprite`
   - Box Collision → `EnemyCollision`
     - Box Extent: `X=30, Y=30, Z=10`
     - Generate Overlap Events: **CHECKED**
   - Cube (Static Mesh) → name `TempVisual`
     - Scale: `(0.6, 0.6, 0.1)` - larger than player cube
     - This provides visibility until proper visuals in [Part 9](part-9-final-setup.md)

6. **Create Variables:**

| Variable Name | Type | Default Value |
|---------------|------|---------------|
| `MaxHealth` | Integer | 12 |
| `CurrentHealth` | Integer | 12 |
| `ScoreValue` | Integer | 50 |
| `VerticalSpeed` | Float | 220.0 |
| `HorizontalAmplitude` | Float | 250.0 |
| `HorizontalFrequency` | Float | 1.8 |
| `DespawnY` | Float | -750.0 |
| `FireInterval` | Float | 0.35 |
| `BulletsPerBurst` | Integer | 20 |
| `BurstSpread` | Float | 360.0 |
| `EnemyBulletSpeed` | Float | 1000.0 |
| `EnemyBulletLifetime` | Float | 6.0 |
| `BaseX` | Float | 0.0 |
| `WaveSeed` | Float | 0.0 |
| `FireTimer` | Float | 0.0 |
| `BulletClass` | Class Reference to Actor | (set later) |

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Components panel shows: DefaultSceneRoot → EnemySprite, EnemyCollision, TempVisual
- Variables panel shows all 16 variables with correct types and defaults

### Expected Result in Viewport (Blueprint Editor):
- Cube visible (the TempVisual placeholder, larger than player)
- Box collision visible (30x30x10)

---

## Step 4.2: Enemy Initialization

1. In Event Graph, from **"Event BeginPlay":**

#### a) Set CurrentHealth = MaxHealth

#### b) Get Actor Location → Break Vector → Set BaseX = X value

#### c) Random Float in Range (0, 6.28) → Set WaveSeed
(6.28 ≈ 2π for wave randomization)

#### d) Random Float in Range (0, FireInterval) → Set FireTimer

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- BeginPlay event connected to variable setters

### Expected Result in Play mode:
- Each enemy spawns with randomized WaveSeed (0 to 6.28)
- Each enemy starts with different FireTimer offset
- This creates varied, non-synchronized enemy behavior

---

## Step 4.3: Enemy Movement Logic

1. In Event Graph, from **"Event Tick":**

#### a) VERTICAL MOVEMENT:
- Get Actor Location → Break into X, Y, Z
- Subtract (VerticalSpeed * DeltaSeconds) from Y

#### b) HORIZONTAL SINE WAVE:
- Get Game Time in Seconds
- Add WaveSeed
- Multiply by HorizontalFrequency
- Calculate Sine of result
- Multiply by HorizontalAmplitude
- Add to BaseX
- This becomes new X position

#### c) Set Actor Location with new X, Y (Z stays 0)

#### d) DESPAWN CHECK:
- If Y < DespawnY: Destroy Actor
- If Abs(X) > 1400: Destroy Actor

**Visual Diagram:**

```
┌─────────────┐
│ Event Tick  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Get Location                                │
│  NewY = Y - (VerticalSpeed * DeltaSeconds)   │
│  NewX = BaseX + Sin(Time * Freq) * Amplitude │
│  Set Location (NewX, NewY, 0)                │
└──────────────────────────────────────────────┘
```

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Event Tick connected to movement and despawn logic

### Expected Result in Play mode:
- Enemies drift downward at VerticalSpeed (220 units/sec)
- Enemies oscillate horizontally in sine wave pattern
- Each enemy has different horizontal phase (due to WaveSeed)
- Enemies disappear when Y < -750 or |X| > 1400

---

## Step 4.4: Enemy Firing Logic

### 1. Continue in Event Tick (after movement):

#### a) Decrease FireTimer by DeltaSeconds

#### b) Branch: if FireTimer <= 0:
- Reset FireTimer to FireInterval
- Call "FireBurst" function

### 2. CREATE "FireBurst" FUNCTION:

#### a) Add function "FireBurst"

#### b) Inside:
- Get BulletsPerBurst
- Calculate angle step: `360 / BulletsPerBurst` (for full circle)
  - OR: `BurstSpread / (BulletsPerBurst - 1)` (for partial arc)

#### c) For Loop from 0 to BulletsPerBurst - 1:
- Calculate angle: `i * AngleStep`
- Convert to direction vector:
  - X = Sin(angle in radians)
  - Y = -Cos(angle in radians)  ← negative because enemies fire DOWN
- Spawn bullet:
  - Spawn Actor from Class (BP_Bullet)
  - Get spawned bullet, call Initialize:
    - Direction = calculated direction
    - Speed = EnemyBulletSpeed
    - bIsEnemy = **true**
    - Lifetime = EnemyBulletLifetime

**Visual: Radial bullet pattern (20 bullets in 360°)**

```
                ↑
             ↗  |  ↖
          ↗    |    ↖
       →───────●───────←
          ↘    |    ↙
             ↘  |  ↙
                ↓
```

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- "FireBurst" function appears under Functions

### Expected Result in Play mode:
- Every 0.35 seconds (FireInterval), enemy fires bullet burst
- 20 bullets spawn in a full 360° circle pattern
- Bullets travel outward from enemy position
- Different enemies fire at different times (randomized FireTimer)

---

## Step 4.5: Enemy Damage and Death

### 1. CREATE "ApplyDamage" FUNCTION:

#### a) Add input: `DamageAmount` (Integer)

#### b) Inside:
- Subtract DamageAmount from CurrentHealth
- If CurrentHealth <= 0:
  - Call HandleDeath

### 2. CREATE "HandleDeath" FUNCTION:

#### a) Inside:
- Get reference to ScoreManager (we'll create in [Part 7](part-7-score-manager-ui.md))
- Call AddScore, passing ScoreValue
- Spawn death effect (optional)
- Destroy Actor

### 3. COLLISION WITH PLAYER:

#### a) On the EnemyCollision component overlap event:
- Cast Other Actor to BP_Player
- If successful:
  - Call TakeHit(1) on player
  - Call HandleDeath() on self

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- "ApplyDamage" and "HandleDeath" functions appear under Functions
- EnemyCollision has overlap event in Event Graph

### Expected Result in Play mode:
- Player bullets hitting enemy: Enemy health decreases
- After 12 hits (MaxHealth): Enemy disappears, score increases by 50
- Player colliding with enemy: Player takes 1 damage, enemy dies

---

## Step 4.6: Complete Special Ability in BP_Player

Now that BP_Enemy exists (and BP_Bullet from Part 3), we can complete the special ability that was set up as a placeholder in [Part 2, Step 2.6](part-2-create-player.md#step-26-create-player-damage-and-special-ability).

### 1. Open BP_Player Blueprint:
1. Content Browser → Blueprints → double-click `BP_Player`
2. Go to **Event Graph** tab
3. Find the `EnhancedInputAction IA_Special` event node (created in Step 2.6)
4. Locate the `Print String "SPECIAL ABILITY ACTIVATED!"` node

### 2. Replace Print String with destruction logic:

#### a) Delete the placeholder:
- Select the `Print String` node
- Press Delete
- (Keep the TODO comment if you want, or delete it too)

#### b) Destroy all enemies:
1. From `Set SpecialUsed` output execution pin, drag → search `Get All Actors of Class` → add it
2. Click the "Actor Class" dropdown → search and select `BP_Enemy`
3. The output "Out Actors" is an array of all enemies currently in the level

#### c) Loop through enemies and destroy them:
1. From `Get All Actors of Class`, drag execution → search `For Each Loop` → add it
2. Connect the "Out Actors" array (blue pin) to the loop's "Array" input (blue pin)
3. From "Loop Body" execution pin, drag → search `Destroy Actor` → add it
4. Connect "Array Element" (blue pin - the current enemy in the loop) to Destroy Actor's "Target" input

#### d) Now destroy enemy bullets (after enemies are done):
1. From `For Each Loop`'s **"Completed"** execution pin (NOT "Loop Body"), drag → search `Get All Actors of Class` → add it
2. Click "Actor Class" dropdown → select `BP_Bullet`
3. From this Get All Actors, drag execution → search `For Each Loop` → add another loop

#### e) Filter to only destroy ENEMY bullets (keep player bullets):
1. From the second loop's "Loop Body" pin, drag → search `Branch` → add it
2. From "Array Element" (the current bullet), drag → search `Get IsEnemyProjectile` → add it
   - This reads the IsEnemyProjectile variable from BP_Bullet
3. Connect `IsEnemyProjectile` output (boolean) to Branch's "Condition" input

#### f) Destroy only if it's an enemy bullet:
1. From Branch's **"True"** pin, drag → search `Destroy Actor` → add it
2. Connect "Array Element" (the bullet) to Destroy Actor's "Target"
3. Leave Branch's "False" pin unconnected (player bullets are preserved)

### 3. Visual diagram of completed special ability:

```
┌─────────────────────────────┐
│ EnhancedInputAction         │
│ IA_Special - Triggered      │
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│ Branch                      │
│ Condition: NOT SpecialUsed  │
└───────┬─────────────┬───────┘
        │ TRUE        │ FALSE
        ▼             ▼
┌───────────────┐   (nothing - ability already used)
│Set SpecialUsed│
│   = true      │
└───────┬───────┘
        │
        ▼
┌────────────────────────────┐
│ Get All Actors of Class    │
│ Actor Class: BP_Enemy      │
│ Out Actors ○───────────────┼──────────┐
└───────────┬────────────────┘          │
            │                           │
            ▼                           ▼
┌────────────────────────────┐   ┌─────────────┐
│ For Each Loop              │──►│Destroy Actor│
│   Array ○──────────────────┼───│Target: Enemy│
│                            │   └─────────────┘
│   Loop Body ───────────────┼───────────┘
│   Completed ───────────────┼───┐
└────────────────────────────┘   │
                                 │
            ┌────────────────────┘
            ▼
┌────────────────────────────┐
│ Get All Actors of Class    │
│ Actor Class: BP_Bullet     │
│ Out Actors ○───────────────┼──────────┐
└───────────┬────────────────┘          │
            │                           │
            ▼                           ▼
┌────────────────────────────┐   ┌─────────────────────────────────┐
│ For Each Loop              │──►│ Get IsEnemyProjectile           │
│   Array ○──────────────────┼───│   (from Array Element)          │
│                            │   └───────────────┬─────────────────┘
│   Loop Body ───────────────┼───────────────────┘
└────────────────────────────┘          │
                                        ▼
                              ┌─────────────────────────────┐
                              │ Branch                      │
                              │ Condition: IsEnemyProjectile│
                              └───────┬─────────────┬───────┘
                                      │ TRUE        │ FALSE
                                      ▼             ▼
                              ┌───────────────┐   (skip - player bullet)
                              │ Destroy Actor │
                              │ Target: Bullet│
                              └───────────────┘
```

### 4. Compile and Save

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- No warnings about missing classes (BP_Enemy and BP_Bullet now exist)

### Expected Result in Play mode:
- Press X (or Right Mouse Button) once:
  - ALL enemies on screen instantly disappear
  - ALL enemy bullets (red) instantly disappear
  - Player bullets (yellow) remain unaffected
  - "SPECIAL ABILITY ACTIVATED!" no longer prints (we deleted it)
- Press X again: Nothing happens (SpecialUsed = true, one use only)

---

[← Previous: Part 3 - Create the Bullet](part-3-create-bullet.md) | [Back to Index](README.md) | [Next: Part 5 - Create Enemy Spawner →](part-5-create-spawner.md)
