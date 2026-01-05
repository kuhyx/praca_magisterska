# Part 3: Create the Bullet

[← Previous: Part 2 - Create the Player](part-2-create-player.md) | [Back to Index](README.md) | [Next: Part 4 - Create the Enemy →](part-4-create-enemy.md)

---

## Step 3.1: Create Bullet Blueprint

1. In Content Browser → Blueprints folder
2. Right-click → **Blueprint Class** → **Actor**
3. Name it: `BP_Bullet`
4. Double-click to open

5. **Add Components:**
   - Paper Sprite → name `BulletSprite`
   - Sphere Collision → name `BulletCollision`
     - Radius: `8`
     - Generate Overlap Events: **CHECKED**
     - Collision Preset: Custom → Query Only
   - Cube (Static Mesh) → name `TempVisual`
     - Scale: `(0.1, 0.1, 0.05)` - small bullet-sized cube
     - This provides visibility until proper visuals in [Part 9](part-9-final-setup.md)

6. **Create Variables:**

| Variable Name | Type | Default Value |
|---------------|------|---------------|
| `TravelDirection` | Vector | (0, 1, 0) |
| `TravelSpeed` | Float | 1200.0 |
| `RemainingLifetime` | Float | 4.0 |
| `IsEnemyProjectile` | Boolean | false |
| `Damage` | Integer | 1 |

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Components panel shows: DefaultSceneRoot → BulletSprite, BulletCollision, TempVisual
- Variables panel shows all 5 variables with correct types

### Expected Result in Viewport (Blueprint Editor):
- Small cube visible (the TempVisual placeholder)
- Sphere collision visible (radius 8)

---

## Step 3.2: Bullet Movement Logic

1. In Event Graph, from **Event Tick:**

#### a) Calculate movement:
- Get TravelDirection
- Multiply by TravelSpeed
- Multiply by Delta Seconds
- Add to current location
- Set Actor Location

#### b) Check lifetime:
- Subtract Delta Seconds from RemainingLifetime
- If <= 0: Destroy Actor

### 2. CREATE "Initialize" FUNCTION:

#### a) Add input parameters:
| Parameter | Type | Default |
|-----------|------|---------|
| `Direction` | Vector | - |
| `Speed` | Float | - |
| `bIsEnemy` | Boolean | - |
| `Lifetime` | Float | - |
| `DamageValue` | Integer | 1 |

#### b) Inside:
- Normalize Direction → Set TravelDirection
- Set TravelSpeed = Speed
- Set IsEnemyProjectile = bIsEnemy
- Set RemainingLifetime = Lifetime
- Set Damage = DamageValue

### 3. Compile and Save

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- "Initialize" function appears under Functions with 5 input parameters

### Expected Result in Play mode (when spawned by player):
- Bullets move in their assigned direction at TravelSpeed
- Bullets automatically destroy after RemainingLifetime seconds (default 4s)
- Movement is smooth and frame-rate independent

---

## Step 3.3: Bullet Collision Logic

1. Click on "BulletCollision" component in Components panel

2. In Details panel, scroll to "Events" section
   - Click "+" next to **"On Component Begin Overlap"**
   - This creates event node in Event Graph

3. In the Event Graph, from "On Component Begin Overlap":

#### a) First, check if this is enemy projectile:
- Get IsEnemyProjectile
- Branch

#### b) IF IS ENEMY PROJECTILE (True branch):
- Get Other Actor from the overlap event
- Cast to BP_Player
- If cast succeeds:
  - Call TakeHit on player, passing Damage
  - Destroy this bullet (Destroy Actor)
  
#### c) IF IS PLAYER BULLET (False branch):
- Get Other Actor
- Cast to BP_Enemy
- If cast succeeds:
  - Call ApplyDamage on enemy, passing Damage
  - Destroy this bullet

### 4. Compile and Save

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Event Graph shows "On Component Begin Overlap" event connected to Branch

### Expected Result in Play mode:
- Player bullets (IsEnemyProjectile=false) hitting enemies:
  - Enemy takes damage, bullet disappears
- Enemy bullets (IsEnemyProjectile=true) hitting player:
  - Player takes hit, bullet disappears
- Bullets passing through other objects: No effect (bullets ignore non-targets)

---

## Step 3.4: Complete Player Firing Logic (BP_Player)

Now that BP_Bullet exists, we can complete the player's firing functions.

### 1. Open BP_Player Blueprint:
- In Content Drawer, navigate to Content → Blueprints
- Double-click "BP_Player" to open the Blueprint Editor

### 2. SET THE BULLET CLASS VARIABLE:

1. In My Blueprint panel, find the `BulletClass` variable
2. Click on it to select it
3. In Details panel, find "Default Value"
4. Click the dropdown and select `BP_Bullet`
5. Compile to save the change

### 3. CREATE SPAWN BULLET FUNCTION:

#### a) In "My Blueprint" panel, under "Functions", click "+"
#### b) Name the function `SpawnBullet`
#### c) Double-click to open function graph

#### d) Add input parameters to the function:
- In the function graph, look at the purple "SpawnBullet" entry node
- In Details panel (right side), find "Inputs" section
- Click "+" to add a new input parameter

| Parameter | Type |
|-----------|------|
| `SpawnLocation` | Vector |
| `Direction` | Vector |

The entry node should now show two input pins: SpawnLocation and Direction

#### e) Build the spawning logic:

1. Right-click → search `Spawn Actor from Class` → add it

2. For the "Class" input:
   - Right-click → `Get BulletClass` (your variable)
   - Connect to "Class" pin

3. For the "Spawn Transform" input:
   - Right-click on the "Spawn Transform" pin → "Split Struct Pin"
   - This splits it into Location, Rotation, Scale
   - Connect "SpawnLocation" (from entry node) to "Spawn Transform Location"
   - Leave Rotation and Scale at defaults

4. Connect execution wire:
   - Drag from SpawnBullet entry node → Spawn Actor from Class

#### f) Initialize the spawned bullet:

5. The "Spawn Actor from Class" has a "Return Value" output (the spawned actor)
   - Drag from Return Value → search `Cast to BP_Bullet`
   - This works now because BP_Bullet exists!

6. From the cast's "As BP Bullet" output, drag → search `Initialize`
   - This calls the Initialize function on the bullet (created in Step 3.2)
   - Connect "Direction" (from entry node) to Initialize's Direction input
   - Right-click → `Get BulletSpeed` → connect to Speed input
   - For "bIsEnemy" input: leave unchecked (false) - player bullets aren't enemy
   - For "Lifetime": type `4.0` (or leave default)

7. Connect execution wires:
   - Spawn Actor → Cast to BP_Bullet → Initialize

**Visual:**

```
┌───────────────────────┐      ┌─────────────────────────┐
│ SpawnBullet           │─────►│ Spawn Actor from Class  │
│ SpawnLocation ○       │      │ Class: BulletClass      │
│ Direction ○           │      │ Location: SpawnLocation │
└───────────────────────┘      └───────────┬─────────────┘
                                           │
                                           ▼
                               ┌─────────────────────────┐
                               │ Cast to BP_Bullet       │
                               └───────────┬─────────────┘
                                           │
                                           ▼
                               ┌─────────────────────────┐
                               │ Initialize              │
                               │ Direction: Direction    │
                               │ Speed: BulletSpeed      │
                               │ bIsEnemy: false         │
                               └─────────────────────────┘
```

#### g) Compile (should have no errors now)

### 4. CREATE FIRE VOLLEY FUNCTION:

#### a) In "My Blueprint" panel, under "Functions", click "+"
#### b) Name the function `FireVolley`
#### c) Double-click to open function graph

#### d) Inside FireVolley function graph, build this logic step by step:

---

**STEP 1 - Get the volley size and check for single bullet case:**

1. You should see a purple "FireVolley" entry node on the left
   - This is where execution starts when the function is called

2. Right-click → search `Get VolleySize` → add it
   - This gets your variable value (default 3)

3. Right-click → search `Equal (Integer)` or `==` → add it
   - Connect VolleySize output to the TOP input (A)
   - Type `1` in the BOTTOM input (B)
   - This checks: is VolleySize exactly 1?

4. From FireVolley entry node, drag execution → `Branch`
   - Connect the == result to Branch's "Condition" input
   - TRUE = single bullet, FALSE = multiple bullets in spread

---

**STEP 2 - TRUE branch: Fire single bullet straight up:**

5. From Branch TRUE pin, drag execution → right-click → search `SpawnBullet` (the function you created in step 3 above)

6. For SpawnBullet's "Spawn Location" input:
   - Right-click → `Get Actor Location`
   - Connect the output to Spawn Location

7. For SpawnBullet's "Direction" input (fire straight UP):
   - Right-click → `Make Vector`
   - Set X = 1 (up in top-down view)
   - Set Y = 0
   - Set Z = 0
   - Connect to Direction input

8. After SpawnBullet, drag execution → `Return Node`
   - This exits the function early (don't continue to the loop)

**Visual so far:**

```
┌─────────────┐      ┌────────────────────┐
│ FireVolley  │─────►│ Branch             │
│ (entry)     │      │ VolleySize == 1    │
└─────────────┘      └─────────┬──────────┘
                               │ TRUE
                               ▼
                     ┌─────────────────────┐
                     │ SpawnBullet         │
                     │ Location: ActorLoc  │───► Return
                     │ Direction: (1,0,0)  │
                     └─────────────────────┘
```

---

**STEP 3 - FALSE branch: Fire multiple bullets in a spread pattern:**

9. From Branch FALSE pin, we need to loop through each bullet.
   First, calculate the starting angle:
   
   The spread is CENTERED on "straight up". For 3 bullets with 12° spread:
   - Bullet 0: -12° (left of center)
   - Bullet 1: 0° (center, straight up)  
   - Bullet 2: +12° (right of center)
   
   **Formula:** `StartAngle = -(VolleySpread * (VolleySize - 1)) / 2`

10. **Calculate StartAngle:**
    - Right-click → `Get VolleySize`
    - Right-click → `Subtract (Integer)` → connect VolleySize, type `1`
      - Result: (VolleySize - 1) = 2 for default
    
    - Right-click → `Get VolleySpread`
    - Right-click → `Multiply (float)` → connect VolleySpread and (VolleySize-1)
      - NOTE: The integer will auto-convert to float
      - Result: VolleySpread * (VolleySize - 1) = 12 * 2 = 24
    
    - Right-click → `Divide (float)` → connect the multiply result, type `2`
      - Result: 24 / 2 = 12
    
    - Right-click → `Negate (float)` or "Multiply by -1"
      - Result: -12 (this is StartAngle)
    
    - Right-click → `Set` → create a LOCAL variable "StartAngle" (Float)
      - OR just keep the wire connected (we'll use it in the loop)

11. **Set up the FOR loop:**
    - From Branch FALSE pin, drag → right-click → search `For Loop`
    - "First Index": type `0`
    - "Last Index": connect (VolleySize - 1) 
      - You already calculated this in step 10, reuse it or calculate again:
      - Get VolleySize → Subtract 1 → connect to Last Index
    
    The loop will run with Index = 0, 1, 2 for VolleySize=3

12. **Inside the loop (from "Loop Body" execution pin):**
    
    Calculate angle for THIS bullet:
    - Right-click → `Multiply (float)`
      - Connect loop "Index" to first input (auto-converts int to float)
      - Connect VolleySpread to second input
      - Result: Index * VolleySpread (0, 12, 24 for indices 0, 1, 2)
    
    - Right-click → `Add (float)`
      - Connect StartAngle (the -12 from step 10) to first input
      - Connect (Index * VolleySpread) to second input
      - Result: StartAngle + (Index * VolleySpread) = -12, 0, +12 degrees
    
    This is the angle in DEGREES. Store or continue with this value.

13. **Convert angle from degrees to a direction vector:**
    
    In Unreal's top-down view (looking down Z axis):
    - X axis = forward/back (up/down on screen)
    - Y axis = left/right
    - Angle 0° = straight up = direction (1, 0, 0)
    - Angle 90° = right = direction (0, 1, 0)
    
    ```
    Direction.X = Cos(angle)
    Direction.Y = Sin(angle)
    Direction.Z = 0
    ```
    
    BUT Unreal's Sin/Cos use RADIANS, not degrees!
    
    **a) Convert degrees to radians:**
    - Right-click → search `Radians` or `Degrees to Radians`
    - Connect your angle (from step 12) to input
    - Output is angle in radians
    
    **b) Calculate X component (Cos):**
    - Right-click → `Cos (Radians)`
    - Connect radians output
    - This is the X direction component
    
    **c) Calculate Y component (Sin):**
    - Right-click → `Sin (Radians)`
    - Connect radians output (same value as Cos input)
    - This is the Y direction component
    
    **d) Make the direction vector:**
    - Right-click → `Make Vector`
    - Connect Cos result to X
    - Connect Sin result to Y
    - Set Z = 0

14. **Spawn the bullet:**
    - From the loop body execution, drag → `SpawnBullet` (from step 3)
    - Spawn Location: `Get Actor Location`
    - Direction: Connect the Make Vector from step 13

15. **Connect loop completion:**
    - The For Loop has a "Completed" execution pin
    - This fires AFTER all iterations are done
    - Drag from "Completed" → `Return Node` (or leave unconnected)

**Complete Visual:**

```
┌─────────────┐      ┌────────────────────┐
│ FireVolley  │─────►│ Branch             │
│ (entry)     │      │ VolleySize == 1    │
└─────────────┘      └──────┬───────┬─────┘
                            │TRUE   │FALSE
                            ▼       ▼
                     ┌──────────┐  ┌─────────────────────────────┐
                     │SpawnBullet│  │ Calculate StartAngle        │
                     │Dir:(1,0,0)│  │ = -(Spread*(Size-1))/2      │
                     └─────┬────┘  └──────────────┬──────────────┘
                           │                      ▼
                           ▼              ┌─────────────────┐
                        Return            │ For Loop        │
                                          │ 0 to Size-1     │
                                          └───────┬─────────┘
                                                  │ Loop Body
                                                  ▼
                                   ┌──────────────────────────────┐
                                   │ Angle = Start + (i * Spread) │
                                   │ Radians = DegreesToRadians   │
                                   │ Dir.X = Cos(Radians)         │
                                   │ Dir.Y = Sin(Radians)         │
                                   │ SpawnBullet(Location, Dir)   │
                                   └──────────────────────────────┘
```

**Test Values (VolleySize=3, VolleySpread=12):**
- StartAngle = -(12 * 2) / 2 = -12°
- Bullet 0: -12 + (0 * 12) = -12° → slightly left
- Bullet 1: -12 + (1 * 12) = 0° → straight up
- Bullet 2: -12 + (2 * 12) = +12° → slightly right

### 5. CONNECT FIREVOLLEY TO THE FIRE RATE LIMITER:

1. Go back to the Event Graph tab
2. Find your IA_Fire logic from [Step 2.5](part-2-create-player.md#step-25-create-player-firing-logic)
3. Delete the Print String "FIRE!" placeholder
4. From the "Set FireTimer = FireInterval" node, drag execution → `FireVolley`

**Updated Visual:**

```
┌─────────────────┐    TRUE    ┌─────────────────────┐
│ Branch          │───────────►│ Set FireTimer       │──► FireVolley
│ FireTimer <= 0  │            │   = FireInterval    │
└─────────────────┘            └─────────────────────┘
```

### 6. Compile and Save

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- "FireVolley" and "SpawnBullet" functions appear under Functions in My Blueprint panel

### Expected Result in Play mode:
- Pressing Z or Left Mouse Button spawns 3 bullets in a spread pattern
- Bullets travel upward from player position
- Rapid fire when holding the button (every 0.08 seconds)
- Bullets disappear after 4 seconds (RemainingLifetime)

---

[← Previous: Part 2 - Create the Player](part-2-create-player.md) | [Back to Index](README.md) | [Next: Part 4 - Create the Enemy →](part-4-create-enemy.md)
