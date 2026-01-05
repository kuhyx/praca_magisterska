# Part 6: Create Game Director

[← Previous: Part 5 - Create Enemy Spawner](part-5-create-spawner.md) | [Back to Index](README.md) | [Next: Part 7 - Score Manager / UI →](part-7-score-manager-ui.md)

---

## Step 6.1: Create Game Director Blueprint

1. Content Browser → Blueprints
2. Right-click → **Blueprint Class** → **Actor**
3. Name: `BP_GameDirector`
4. Double-click to open

5. **Create Variables:**

| Variable Name | Type | Default Value |
|---------------|------|---------------|
| `PlayerReference` | Object Reference to BP_Player | - |
| `SpawnerReference` | Object Reference to BP_EnemySpawner | - |
| `GameDuration` | Float | 300.0 |
| `ElapsedTime` | Float | 0.0 |
| `GameActive` | Boolean | true |

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Variables panel shows all 5 variables with correct types
- No components needed (director is invisible logic actor)

---

## Step 6.2: Game Director Initialization

### 1. From Event BeginPlay:

#### a) Find player in scene:
- Get All Actors of Class → BP_Player
- Get first element (index 0)
- Set PlayerReference

#### b) Find spawner in scene:
- Get All Actors of Class → BP_EnemySpawner
- Get first element
- Set SpawnerReference

#### c) Initialize ScoreManager:
- Get ScoreManager reference
- Call RegisterGameStart with initial lives and duration

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- BeginPlay event connected to "Get All Actors of Class" nodes

### Expected Result in Play mode:
- Game Director automatically finds Player, Spawner, and ScoreManager
- UI initializes with correct starting values (Lives: 3, Time: 05:00)

---

## Step 6.3: Game Director Update Logic

### 1. From Event Tick:

#### a) Check if GameActive
- If false, skip everything

#### b) Update elapsed time:
- Add DeltaSeconds to ElapsedTime

#### c) Calculate remaining time:
- Subtract ElapsedTime from GameDuration
- Max with 0 (don't go negative)

#### d) Update UI timer:
- Get ScoreManager
- Call UpdateTimer with remaining time

#### e) Check for victory:
- If ElapsedTime >= GameDuration:
  - Set GameActive = false
  - Get SpawnerReference → Call StopSpawning
  - Get ScoreManager → Call HandleGameClear

### 2. CREATE "HandlePlayerDeath" FUNCTION:

#### a) Inside:
- Set GameActive = false
- Get SpawnerReference → Call StopSpawning
- Get ScoreManager → Call HandleGameOver

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- "HandlePlayerDeath" function appears under Functions
- Event Tick connected to timer update and victory check

### Expected Result in Play mode:
- Timer counts down from 05:00 to 00:00
- At 00:00: "Mission Complete" appears, enemies stop spawning
- When player dies: "Game Over" appears, enemies stop spawning

---

[← Previous: Part 5 - Create Enemy Spawner](part-5-create-spawner.md) | [Back to Index](README.md) | [Next: Part 7 - Score Manager / UI →](part-7-score-manager-ui.md)
