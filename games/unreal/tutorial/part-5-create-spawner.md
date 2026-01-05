# Part 5: Create Enemy Spawner

[← Previous: Part 4 - Create the Enemy](part-4-create-enemy.md) | [Back to Index](README.md) | [Next: Part 6 - Game Director →](part-6-game-director.md)

---

## Step 5.1: Create Spawner Blueprint

1. Content Browser → Blueprints
2. Right-click → **Blueprint Class** → **Actor**
3. Name: `BP_EnemySpawner`
4. Double-click to open

5. **Create Variables:**

| Variable Name | Type | Default Value |
|---------------|------|---------------|
| `EnemyClass` | Class Reference | (will reference BP_Enemy) |
| `SpawnAreaHalfWidth` | Float | 900.0 |
| `GameDuration` | Float | 300.0 (5 minutes) |
| `MaxSimultaneousEnemies` | Integer | 120 |
| `ElapsedTime` | Float | 0.0 |
| `SpawnTimer` | Float | 0.0 |
| `SpawningActive` | Boolean | true |

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Variables panel shows all 7 variables with correct types
- No components needed (spawner is invisible logic actor)

---

## Step 5.2: Spawn Rate Curve

### 1. Create Variable:
- `SpawnCurve` (Curve Float)

### 2. To create the curve asset:

1. In Content Browser, right-click → **Miscellaneous → Curve**
2. Select "CurveFloat"
3. Name it `SpawnRateCurve`
4. Double-click to open Curve Editor

### 3. In Curve Editor:

- Right-click on the curve → Add Key
- Create these keyframes:

| Time | Value | Description |
|------|-------|-------------|
| 0.0 | 0.4 | slow spawn at start |
| 0.5 | 2.0 | medium spawn halfway |
| 1.0 | 4.5 | fast spawn at end |

- The X axis is normalized time (0-1)
- The Y axis is spawns per second

### 4. In BP_EnemySpawner, set SpawnCurve default to this curve asset

### Expected Result in Curve Editor:
- Curve line visible starting at (0, 0.4), rising through (0.5, 2.0), ending at (1.0, 4.5)
- Smooth interpolation between keyframes

### Expected Result in Play mode:
- Game start: ~0.4 enemies spawn per second (slow)
- At 2.5 minutes: ~2 enemies spawn per second (medium)
- At 5 minutes: ~4.5 enemies spawn per second (intense)

---

## Step 5.3: Spawning Logic

### 1. In Event Graph, from Event Tick:

#### a) Check if SpawningActive is true
- If false, do nothing

#### b) Update ElapsedTime:
- Add DeltaSeconds to ElapsedTime

#### c) Calculate normalized time:
- Divide ElapsedTime by GameDuration
- Clamp between 0 and 1

#### d) Get spawn rate from curve:
- Get SpawnCurve
- Call `Get Float Value` with normalized time
- This returns spawns per second

#### e) Update SpawnTimer:
- Subtract DeltaSeconds from SpawnTimer
- If SpawnTimer <= 0:
  - Reset SpawnTimer to `(1.0 / SpawnsPerSecond)`
  - Call SpawnWave function

### 2. CREATE "SpawnWave" FUNCTION:

#### a) Inside:
- Calculate burst size based on time:
  ```
  BaseCount = 1 + (NormalizedTime * 6)
  BurstSize = BaseCount + Random(0, 2)
  Clamp between 1 and 12
  ```

#### b) For Loop from 0 to BurstSize - 1:
- Call SpawnEnemy function

### 3. CREATE "SpawnEnemy" FUNCTION:

#### a) Inside:
- Check: Get All Actors of Class (BP_Enemy)
  - Get array length
  - If >= MaxSimultaneousEnemies: Return (don't spawn)

#### b) Calculate spawn position:
- X = Random Float in Range (-SpawnAreaHalfWidth, SpawnAreaHalfWidth)
- Y = Get this actor's Y position (top of screen)
- Z = 0

#### c) Spawn Actor from Class:
- Class: EnemyClass
- Location: calculated position
- Rotation: (0, 0, 0)

### 4. CREATE "StopSpawning" FUNCTION:
- Set SpawningActive = false

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- "SpawnWave", "SpawnEnemy", "StopSpawning" functions appear under Functions

### Expected Result in Play mode:
- Enemies spawn at top of screen (Y=500) at random X positions
- Spawn rate increases over time following the curve
- Maximum 120 enemies on screen at once
- When StopSpawning called: No new enemies appear

---

[← Previous: Part 4 - Create the Enemy](part-4-create-enemy.md) | [Back to Index](README.md) | [Next: Part 6 - Game Director →](part-6-game-director.md)
