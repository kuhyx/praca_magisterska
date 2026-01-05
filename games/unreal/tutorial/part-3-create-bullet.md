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

| Variable Name       | Type    | Default Value |
| ------------------- | ------- | ------------- |
| `TravelDirection`   | Vector  | (0, 1, 0)     |
| `TravelSpeed`       | Float   | 1200.0        |
| `RemainingLifetime` | Float   | 4.0           |
| `IsEnemyProjectile` | Boolean | false         |
| `Damage`            | Integer | 1             |

### Expected Result after Compile

- Compile button shows GREEN checkmark
- Components panel shows: DefaultSceneRoot → BulletSprite, BulletCollision, TempVisual
- Variables panel shows all 5 variables with correct types

### Expected Result in Viewport (Blueprint Editor)

- Small cube visible (the TempVisual placeholder)
- Sphere collision visible (radius 8)

---

## Step 3.2: Bullet Movement Logic

1. In Event Graph, from **Event Tick:**

### a) Calculate movement

1. Right-click → `Get TravelDirection`
2. Right-click → `Get TravelSpeed`
3. Right-click → search `Multiply (Vector * Float)` → add it
   - Connect TravelDirection to the Vector input
   - Connect TravelSpeed to the Float input
   - Result: a vector representing full speed in travel direction

4. Right-click → `Get World Delta Seconds`
5. Right-click → search `Multiply (Vector * Float)` → add another one
   - Connect the RESULT from step 3 to the Vector input
   - Connect World Delta Seconds to the Float input
   - Result: movement delta for this frame (frame-rate independent)

6. Right-click → `Get Actor Location`
7. Right-click → search `Add (Vector + Vector)` → add it
   - Connect Actor Location to first input
   - Connect the movement delta (from step 5) to second input

8. Right-click → `Set Actor Location`
   - Connect the Add result to "New Location"
   - Connect execution wire from Event Tick to Set Actor Location

#### b) Check lifetime and destroy when expired

9. Right-click → `Get RemainingLifetime`

10. Right-click → `Get World Delta Seconds`

11. Right-click → search `Subtract (Float)` → add it
    - Connect RemainingLifetime to the TOP input (A)
    - Connect World Delta Seconds to the BOTTOM input (B)
    - Result: RemainingLifetime minus DeltaSeconds

12. Right-click → `Set RemainingLifetime`
    - Connect the Subtract result to it
    - This ALWAYS stores the new decreased lifetime value

13. Connect execution wire:
    - From `Set Actor Location` (from step 8) → `Set RemainingLifetime`

14. Right-click → search `<= (Float)` (less than or equal) → add it
    - Connect RemainingLifetime (from Set node output, or Get again) to TOP input
    - Type `0` in BOTTOM input
    - Result: true if lifetime has expired

15. From `Set RemainingLifetime`, drag execution → `Branch`
    - Connect the `<=` result to Branch's "Condition" input

16. **On TRUE (lifetime expired):**
    - From Branch's "True" pin, drag → `Destroy Actor`
    - Target: leave as "Self" (destroys this bullet)

17. **On FALSE (still alive):**
    - Leave unconnected (bullet continues to exist, will check again next frame)

**Visual:**

```
Event Tick ──► Set Actor Location ──► Set RemainingLifetime ──► Branch
               (movement)              = Remaining - Delta      (Remaining <= 0?)
                                                                     │
                                                          TRUE ──────┴────── FALSE
                                                            │                  │
                                                            ▼                  ▼
                                                      Destroy Actor        (nothing)
```

### 2. CREATE "Initialize" FUNCTION

#### a) Create the function

1. In "My Blueprint" panel (left side), find "Functions" section
2. Click the **"+"** button next to Functions
3. Name the new function `Initialize`
4. Double-click to open the function graph

#### b) Add input parameters

1. In the function graph, you should see a purple "Initialize" entry node
2. With the entry node selected, look at the Details panel (right side)
3. Find "Inputs" section and click "+" to add parameters:

| Parameter     | Type    | Default |
| ------------- | ------- | ------- |
| `Direction`   | Vector  | -       |
| `Speed`       | Float   | -       |
| `bIsEnemy`    | Boolean | -       |
| `Lifetime`    | Float   | -       |
| `DamageValue` | Integer | 1       |

The entry node should now show 5 input pins.

#### c) Build the function logic

1. **Normalize and set direction:**
   - Drag from **Direction** parameter (yellow pin) → search `Normalize` → add it
   - Right-click → `Set TravelDirection`
   - Connect Normalize's "Return Value" → Set TravelDirection input

2. **Set travel speed:**
   - Right-click → `Set TravelSpeed`
   - Drag from **Speed** parameter → Set TravelSpeed input

3. **Set enemy projectile flag:**
   - Right-click → `Set IsEnemyProjectile`
   - Drag from **bIsEnemy** parameter → Set IsEnemyProjectile input

4. **Set remaining lifetime:**
   - Right-click → `Set RemainingLifetime`
   - Drag from **Lifetime** parameter → Set RemainingLifetime input

5. **Set damage:**
   - Right-click → `Set Damage`
   - Drag from **DamageValue** parameter → Set Damage input

#### d) CRITICAL - Connect execution wires

> **IMPORTANT:** Without execution wires, the SET nodes will NEVER run! You must chain them together.

6. From **Initialize** entry node (white triangle on right), drag execution → **Set TravelDirection**
7. From Set TravelDirection (white triangle), drag execution → **Set TravelSpeed**
8. From Set TravelSpeed, drag execution → **Set IsEnemyProjectile**
9. From Set IsEnemyProjectile, drag execution → **Set RemainingLifetime**
10. From Set RemainingLifetime, drag execution → **Set Damage**

**Visual:**

```
┌─────────────────────────┐
│ Initialize              │
│ Direction ○─────────────┼──► Normalize ──► Set TravelDirection
│ Speed ○─────────────────┼──────────────────► Set TravelSpeed
│ bIsEnemy ○──────────────┼──────────────────► Set IsEnemyProjectile
│ Lifetime ○──────────────┼──────────────────► Set RemainingLifetime
│ DamageValue ○───────────┼──────────────────► Set Damage
└──────────┬──────────────┘
           │ (white execution wire)
           ▼
    Set TravelDirection ──► Set TravelSpeed ──► Set IsEnemyProjectile
                                                         │
                                                         ▼
                              Set Damage ◄── Set RemainingLifetime
```

### 3. Compile and Save

### Expected Result after Compile

- Compile button shows GREEN checkmark
- "Initialize" function appears under Functions with 5 input parameters

> **NOTE:** Bullet testing is possible after completing [Step 3.4](#step-34-complete-player-firing-logic-bp_player).

---

## Step 3.3: Bullet Collision Logic

### 1. ADD THE OVERLAP EVENT

1. In the Components panel (top-left), click on **"BulletCollision"** to select it

2. In the Details panel (right side), scroll down to find the **"Events"** section
   - Look for "On Component Begin Overlap"
   - Click the green **"+"** button next to it
   - This creates an event node in the Event Graph

3. The Event Graph now shows a red node: **"On Component Begin Overlap (BulletCollision)"**
   - This fires whenever another actor overlaps with the bullet's collision sphere

### 2. CHECK IF THIS IS AN ENEMY PROJECTILE

4. Right-click → `Get IsEnemyProjectile`
   - This gets your boolean variable

5. From "On Component Begin Overlap", drag execution → `Branch`
   - Connect IsEnemyProjectile to Branch's "Condition" input
   - TRUE = this is an enemy bullet (should damage player)
   - FALSE = this is a player bullet (should damage enemies)

### 3. TRUE BRANCH - Enemy Bullet Hits Player

6. From the **"On Component Begin Overlap"** node, look for the **"Other Actor"** output pin
   - This is the actor that overlapped with the bullet
   - Drag from "Other Actor" → search `Cast to BP_Player`

7. Connect execution wire:
   - From Branch **TRUE** pin → `Cast to BP_Player`

8. The cast has two execution outputs:
   - **"Cast Succeeded"** (top) - the other actor IS a player
   - **"Cast Failed"** (bottom) - the other actor is NOT a player

9. From "Cast Succeeded", we need to damage the player:
   - From the cast's **"As BP Player"** output pin, drag → search `TakeHit`
   - This calls the TakeHit function you created in [Part 2](part-2-create-player.md)
   - **IMPORTANT:** The "Target" pin on TakeHit should now be connected to "As BP Player" (this happened automatically when you dragged from that pin)
   - If Target shows "self", you must manually connect "As BP Player" to the "Target" pin - TakeHit must be called ON the player, not on the bullet!

10. Connect the Damage parameter:
    - Right-click → `Get Damage` (your bullet's damage variable)
    - Connect to TakeHit's "DamageAmount" input

11. After damaging the player, destroy the bullet:
    - From TakeHit, drag execution → `Destroy Actor`
    - Leave "Target" as "Self" (destroys this bullet)

12. Connect execution wire:
    - Cast to BP_Player → TakeHit → Destroy Actor

### 4. FALSE BRANCH - Player Bullet Hits Enemy (PLACEHOLDER)

> **NOTE:** BP_Enemy doesn't exist yet, so we'll add a placeholder. You'll complete this logic in [Part 4, Step 4.7](part-4-create-enemy.md#step-47-complete-bullet-collision-logic-bp_bullet).

13. From Branch **FALSE** pin, drag execution → `Print String`
    - In the "In String" field, type: `TODO: Damage enemy`
    - This is temporary - we'll replace it with real enemy damage logic in Part 4

**Visual:**

```
┌──────────────────────────────────────┐
│ On Component Begin Overlap           │
│ (BulletCollision)                    │
│                          Other Actor ○─────────────────────┐
└──────────────┬───────────────────────┘                     │
               │                                             │
               ▼                                             ▼
        ┌─────────────────┐                       ┌──────────────────┐
        │ Branch          │                       │ Cast to BP_Player│
        │ IsEnemyProjectile                       └────────┬─────────┘
        └───────┬───┬─────┘                                │
                │   │                             Cast Succeeded
          TRUE ─┘   └─ FALSE                               │
                │         │                                ▼
                ▼         │                       ┌──────────────────┐
     Cast to BP_Player    │                       │ TakeHit          │
     (see above)          │                       │ Damage: Damage   │
                          │                       └────────┬─────────┘
                          ▼                                │
               ┌──────────────────┐                        ▼
               │ Print String     │               ┌──────────────────┐
               │ "TODO: Damage    │               │ Destroy Actor    │
               │  enemy"          │               │ (Self)           │
               └──────────────────┘               └──────────────────┘
```

### 4. Compile and Save

### Expected Result after Compile

- Compile button shows GREEN checkmark
- Event Graph shows "On Component Begin Overlap" event connected to Branch

> **NOTE:** Collision testing requires player firing (Step 3.4) and enemies (Part 4). Full collision behavior is testable after completing [Part 4](part-4-create-enemy.md).

---

## Step 3.4: Complete Player Firing Logic (BP_Player)

Now that BP_Bullet exists, we can complete the player's firing functions.

### 1. Open BP_Player Blueprint

- In Content Drawer, navigate to Content → Blueprints
- Double-click "BP_Player" to open the Blueprint Editor

### 2. SET THE BULLET CLASS VARIABLE

1. In My Blueprint panel, find the `BulletClass` variable
2. Click on it to select it
3. In Details panel, find "Default Value"
4. Click the dropdown and select `BP_Bullet`
5. Compile to save the change

### 3. CREATE SPAWN BULLET FUNCTION

#### a) In "My Blueprint" panel, under "Functions", click "+"

#### b) Name the function `SpawnBullet`

#### c) Double-click to open function graph

#### d) Add input parameters to the function

- In the function graph, look at the purple "SpawnBullet" entry node
- In Details panel (right side), find "Inputs" section
- Click "+" to add a new input parameter

| Parameter       | Type   |
| --------------- | ------ |
| `SpawnLocation` | Vector |
| `Direction`     | Vector |

The entry node should now show two input pins: SpawnLocation and Direction

#### e) Build the spawning logic

1. Right-click → search `Spawn Actor from Class` → add it

2. For the "Class" input:
   - Right-click → `Get BulletClass` (your variable)
   - Connect BulletClass output (blue pin) to SpawnActor's "Class" input (purple pin)

3. For the "Spawn Transform Location" input:
   - On the SpawnActor node, look for "Spawn Transform Location" (orange pin)
   - If you only see "Spawn Transform", right-click on it → "Split Struct Pin" to expand it
   - Drag a wire from the **SpawnLocation** parameter (on the SpawnBullet entry node) to **"Spawn Transform Location"**
   - Leave Rotation and Scale at defaults (0,0,0 and 1,1,1)

4. Connect execution wire:
   - Drag from SpawnBullet entry node (white triangle) → SpawnActor (white triangle)

#### f) Initialize the spawned bullet

5. Add the Cast node:
   - From SpawnActor's **"Return Value"** output (blue pin on right side), drag → search `Cast to BP_Bullet`
   - Connect "Return Value" to the Cast's "Object" input

6. Connect execution wire:
   - From SpawnActor (white triangle output) → Cast to BP_Bullet (white triangle input)

7. Add the Initialize call:
   - From the Cast's **"As BP Bullet"** output (blue pin), drag → search `Initialize`
   - This calls the Initialize function you created in Step 3.2
   - **IMPORTANT:** The "Target" pin should automatically connect to "As BP Bullet"

8. Connect Initialize parameters:
   - **Direction**: Drag from the **Direction** parameter (on SpawnBullet entry node, yellow pin) → Initialize's "Direction" input
   - **Speed**: Right-click → `Get BulletSpeed` → connect to Initialize's "Speed" input
   - **bIsEnemy**: Leave unchecked (false) - player bullets aren't enemy projectiles
   - **Lifetime**: Type `4.0` in the input field (or leave default)
   - **DamageValue**: Leave at default `1`

9. Connect execution wire:
   - From Cast to BP_Bullet → Initialize

**Visual:**

```
┌───────────────────────┐      ┌─────────────────────────────────┐
│ SpawnBullet           │─────►│ Spawn Actor from Class          │
│ SpawnLocation ○───────┼─────►│   Class: BulletClass            │
│ Direction ○           │      │   Spawn Transform Location ○◄───┘
└───────────────────────┘      │   Return Value ○────────────────┐
                               └─────────────────────────────────┘
                                                                 │
                                           ┌─────────────────────┘
                                           ▼
                               ┌─────────────────────────┐
                               │ Cast to BP_Bullet       │
                               │   Object ○◄─────────────┘
                               │   As BP Bullet ○────────┐
                               └─────────────────────────┘
                                                         │
                                           ┌─────────────┘
                                           ▼
                               ┌─────────────────────────┐
                               │ Initialize              │
                               │   Target ○◄─────────────┘
                               │   Direction ○◄──────────── (from entry node)
                               │   Speed ○◄────────────── BulletSpeed
                               │   bIsEnemy: false       │
                               │   Lifetime: 4.0         │
                               └─────────────────────────┘
```

#### g) Compile (should have no errors now)

### 4. CREATE FIRE VOLLEY FUNCTION

#### a) In "My Blueprint" panel, under "Functions", click "+"

#### b) Name the function `FireVolley`

#### c) Double-click to open function graph

#### d) Inside FireVolley function graph, build this logic step by step

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
      - Result: VolleySpread _(VolleySize - 1) = 12_ 2 = 24
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
      - Result: Index \* VolleySpread (0, 12, 24 for indices 0, 1, 2)
    - Right-click → `Add (float)`
      - Connect StartAngle (the -12 from step 10) to first input
      - Connect (Index \* VolleySpread) to second input
      - Result: StartAngle + (Index \* VolleySpread) = -12, 0, +12 degrees

    This is the angle in DEGREES. Store or continue with this value.

13. **Convert angle from degrees to a direction vector:**

    In Unreal's top-down view (looking down Z axis):
    - X axis = up/down on screen (vertical)
    - Y axis = left/right on screen (horizontal)
    - Angle 0° = straight up = direction (1, 0, 0)
    - Angle 90° = right = direction (0, 1, 0)

    ```
    Direction.X = Cos(angle)   // Cos for vertical (forward/up)
    Direction.Y = Sin(angle)   // Sin for horizontal offset
    Direction.Z = 0
    ```

    BUT Unreal's Sin/Cos use RADIANS, not degrees!

    **a) Convert degrees to radians:**
    - Right-click → search `Degrees To Radians` → add it
    - Connect your angle (from step 12) to the input
    - Output is angle in radians

    **b) Calculate X component (Cos - forward/up direction):**
    - Right-click → `Cos (Radians)` → add it
    - Connect the Degrees To Radians output to Cos input

    **c) Calculate Y component (Sin - horizontal offset):**
    - Right-click → `Sin (Radians)` → add it
    - To connect the SAME radians value to Sin (without losing the Cos connection):
      - **Option 1:** Ctrl+drag from "Degrees To Radians" output to Sin input (creates second wire)
      - **Option 2:** Drag directly from "Degrees To Radians" output again - UE5 allows multiple wires from one output pin
    - Both Cos and Sin should now be connected to the same radians value

    **d) Make the direction vector:**
    - Right-click → `Make Vector`
    - Connect Cos result to X (forward/up direction)
    - Connect Sin result to Y (horizontal spread)
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

- StartAngle = -(12 \* 2) / 2 = -12°
- Bullet 0: -12 + (0 \* 12) = -12° → slightly left
- Bullet 1: -12 + (1 \* 12) = 0° → straight up
- Bullet 2: -12 + (2 \* 12) = +12° → slightly right

### 5. CONNECT FIREVOLLEY TO THE FIRE RATE LIMITER

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

### Expected Result after Compile

- Compile button shows GREEN checkmark
- "FireVolley" and "SpawnBullet" functions appear under Functions in My Blueprint panel

### Expected Result in Play mode

- Pressing Z or Left Mouse Button spawns 3 bullets in a spread pattern
- Bullets travel upward from player position
- Rapid fire when holding the button (every 0.08 seconds)
- Bullets disappear after 4 seconds (RemainingLifetime)

---

[← Previous: Part 2 - Create the Player](part-2-create-player.md) | [Back to Index](README.md) | [Next: Part 4 - Create the Enemy →](part-4-create-enemy.md)
