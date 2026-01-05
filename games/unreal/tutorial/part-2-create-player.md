# Part 2: Create the Player

[← Previous: Part 1 - Project Setup](part-1-project-setup.md) | [Back to Index](README.md) | [Next: Part 3 - Create the Bullet →](part-3-create-bullet.md)

---

## Step 2.1: Create Player Blueprint

1. In Content Browser, double-click "Blueprints" folder to open it

2. Right-click in empty space → **Blueprint Class**

3. In the popup window "Pick Parent Class":
   - Click "Pawn" (NOT Character - we want simple 2D control)
   - Click "Select"

4. Name the new Blueprint: `BP_Player`

5. Double-click "BP_Player" to open the Blueprint Editor

### Expected Result

A new tab opens showing the Blueprint Editor with:
- Components panel on the left
- Viewport in the center
- Details panel on the right
- Tab bar above the Viewport with: Viewport | Construction Script | Event Graph (third from left)

---

## Step 2.2: Add Player Visual Components

1. In the Components panel (left side), you'll see "DefaultSceneRoot"
   - Click on "DefaultSceneRoot" to select it (this ensures new components are added as children)

2. With DefaultSceneRoot selected, click **"Add"** button (green, top of Components panel)
   - Search for "Paper Sprite"
   - Click "Paper Sprite" to add it (it will be added as a child of DefaultSceneRoot)
   - Rename it to `PlayerSprite` (click on it, then press F2)

   > **NOTE:** If Paper Sprite is not available:
   > - Go to Edit → Plugins (from main menu bar)
   > - Search for "Paper2D"
   > - Make sure "Paper2D" plugin is ENABLED
   > - Restart the editor if prompted

3. With "PlayerSprite" selected, look at Details panel (right side):
   - Find "Source Sprite" property
   - For now, leave it empty (we'll create sprites later)
   - Under "Transform", set Scale to `(1.0, 1.0, 1.0)`

4. With DefaultSceneRoot still selected, click **"Add"** button again:
   - Search for "Box Collision"
   - Click "Box Collision" to add it (it will be added as a child of DefaultSceneRoot)
   - Rename it to `PlayerCollision`

5. With "PlayerCollision" selected, in Details panel:
   - Under "Shape", set Box Extent to: `X=25, Y=25, Z=10`
   - Under "Collision", click "Collision Presets" dropdown
   - Select "Custom..."
   - Set "Collision Enabled" to "Query Only (No Physics Collision)"
   - Enable "Generate Overlap Events" box

6. With DefaultSceneRoot still selected, click **"Add"** button:
   - Search for "Arrow"
   - Click "Arrow" to add it (it will be added as a child of DefaultSceneRoot)
   - This shows which direction is "forward" (useful for debugging)

7. With DefaultSceneRoot still selected, click **"Add"** button:
   - Search for "Cube" → add "Cube" (Static Mesh)
   - Rename it to `TempVisual`
   - In Details panel, set Scale to `(0.5, 0.5, 0.1)` so it's small and flat
   - This provides a visible placeholder until we add proper sprites in [Part 9](part-9-final-setup.md)

8. With DefaultSceneRoot still selected, click **"Add"** button:
   - Search for "Camera" → add "Camera"
   - Rename it to `PlayerCamera`
   - In Details panel, set Location to: `X=0, Y=0, Z=1000` (1000 units above player)
   - Set Rotation to: `X=0, Y=-90, Z=0` (looking straight down)
   - In Details panel, find "Activation" category → "Auto Activate" checkbox
     - This should already be ENABLED by default
     - If not, check/enable it - this tells Unreal to use THIS camera when playing
   - This camera will follow the player, making testing easy
   
   > **NOTE:** This temporary camera ensures you can see the player during testing.
   > In [Part 8](part-8-game-mode-level.md), we'll set up a proper fixed camera for the final game.

### Expected Result

Components panel shows:

```
DefaultSceneRoot
├── PlayerSprite (Paper Sprite)
├── PlayerCollision (Box Collision)
├── Arrow
├── TempVisual (Cube)
└── PlayerCamera (Camera)
```

9. **IMPORTANT - Enable Auto Possession for testing:**
   - Click on "BP_Player (Self)" at the top of the Components panel (the root)
   - In Details panel, find "Pawn" category
   - Find "Auto Possess Player" dropdown (currently set to "Disabled")
   - Change it to **"Player 0"**
   - This makes the engine automatically possess this pawn when playing, which activates the PlayerCamera
   
   > **NOTE:** This setting will be overridden later when we set up the GameMode
   > in [Part 8](part-8-game-mode-level.md), which handles possession automatically.

---

## Step 2.3: Create Player Variables

*(Continue in the same BP_Player Blueprint Editor tab that was opened in Step 2.1)*

1. In the Blueprint Editor, look at the left panel (below the Components panel)
2. Find "My Blueprint" section
3. Under "Variables", click the **"+"** button

4. Create these variables one by one (click +, then set properties in Details):

   > **NOTE:** Variables are NOT added to the Components hierarchy. They appear in a 
   > separate "Variables" list within the "My Blueprint" panel. Variables store 
   > data values, while Components are physical/visual parts of the actor.

| # | Variable Name | Type | Default Value |
|---|---------------|------|---------------|
| 1 | `MoveSpeed` | Float | 750.0 |
| 2 | `BoundsMin` | Vector 2D | X=-850, Y=-450 |
| 3 | `BoundsMax` | Vector 2D | X=850, Y=450 |
| 4 | `FireInterval` | Float | 0.08 |
| 5 | `FireTimer` | Float | 0.0 |
| 6 | `BulletSpeed` | Float | 2200.0 |
| 7 | `MaxLives` | Integer | 3 |
| 8 | `CurrentLives` | Integer | 3 |
| 9 | `VolleySize` | Integer | 3 |
| 10 | `VolleySpread` | Float | 12.0 |
| 11 | `SpecialUsed` | Boolean | false (unchecked) |
| 12 | `BulletClass` | Class Reference* | (set later) |

> *For BulletClass: In the type dropdown, go to "Object Types" category → "Actor" → select "Class Reference" (the subcategory under Actor). This will hold reference to bullet blueprint class for spawning.

> **TIP:** For Variable 1 (MoveSpeed), click the "eye" icon to make it public/editable. Compile the blueprint (Click on "Compile" third option from left or simply `Ctrl + Alt`) before setting the default value.

5. Click **"Compile"** button (top left, blue checkmark icon)
6. Click **"Save"** button (floppy disk icon next to Compile)

### Expected Result

My Blueprint panel shows:
- All 12 variables you created listed under "Variables"
- A "Components" category with 4 component references (DefaultSceneRoot, PlayerSprite, PlayerCollision, Arrow) - these are automatically created from the components you added in Step 2.2

---

## Step 2.4: Set Up Enhanced Input System

UE5 uses the Enhanced Input System. Before creating movement logic in our Blueprint, we first need to create Input Actions and an Input Mapping Context.

### 0. ENABLE ENHANCED INPUT IN PROJECT SETTINGS (CRITICAL)

Before creating any input assets, you **MUST** configure the project to use Enhanced Input as the default input system:

1. Go to **Edit → Project Settings**
2. In the left sidebar, scroll down to "Engine" section
3. Click on "Input"
4. Find "Default Classes" section (near the top)
5. Set "Default Player Input Class" to: `EnhancedPlayerInput`
6. Set "Default Input Component Class" to: `EnhancedInputComponent`
7. Close Project Settings

> ⚠️ **WARNING:** If you skip this step, WASD controls will NOT work even if everything else is set up correctly!

### 1. SET UP INPUT ASSETS (in Content Drawer)

#### A) CREATE INPUT ACTIONS

1. Open Content Drawer (`Ctrl+Space` or click "Content Drawer" at bottom)
2. In Content folder, right-click → **New Folder** → name it `Input`

3. Inside Input folder, right-click → **Input → Input Action**
   - Name it `IA_Move`
   - Double-click to open
   - Set "Value Type" to `Axis2D (Vector2D)`
   - Save and close

4. Create another Input Action: `IA_Fire`
   - Set "Value Type" to `Digital (bool)` (default)

5. Create another Input Action: `IA_Special`
   - Set "Value Type" to `Digital (bool)`

#### B) CREATE INPUT MAPPING CONTEXT

1. In Input folder, right-click → **Input → Input Mapping Context**
   - Name it `IMC_Default`
   - Double-click to open

2. Click **"+"** next to "Mappings" to add IA_Move:
   - Select "IA_Move" from dropdown
   - Click "+" under IA_Move to add key bindings:
   
   > **NOTE:** In Unreal's top-down view, X axis = up/down, Y axis = left/right

   **For W key (move UP on screen):**
   - Click "+", select "W"
   - No modifiers needed (outputs X positive = up)
   - TOTAL MODIFIERS FOR W: **0**
     
   **For S key (move DOWN on screen):**
   - Click "+", select "S"
   - Click "+" next to "Modifiers" → Add "Negate"
   - TOTAL MODIFIERS FOR S: **1** (Negate only)
     
   **For A key (move LEFT on screen):**
   - Click "+", select "A"
   - Click "+" next to "Modifiers" → Add "Swizzle Input Axis Values" → Order: "YXZ"
   - Click "+" next to "Modifiers" AGAIN → Add "Negate"
   - TOTAL MODIFIERS FOR A: **2** (Swizzle AND Negate)
     
   **For D key (move RIGHT on screen):**
   - Click "+", select "D"
   - Click "+" next to "Modifiers" → Add "Swizzle Input Axis Values" → Order: "YXZ"
   - TOTAL MODIFIERS FOR D: **1** (Swizzle only)

   **Summary Table - verify your IMC_Default matches this:**
   
   | Key | Modifiers | Output Vector |
   |-----|-----------|---------------|
   | W | (none) | (1, 0) = UP |
   | S | Negate | (-1, 0) = DOWN |
   | A | Swizzle Input Axis Values (YXZ) + Negate | (0, -1) = LEFT |
   | D | Swizzle Input Axis Values (YXZ) | (0, 1) = RIGHT |

   After adding all keys, press `Ctrl+S` to SAVE IMC_Default!

3. Click "+" to add **IA_Fire**:
   - Select "IA_Fire"
   - Add key: `Z`
   - Add key: `Left Mouse Button`

4. Click "+" to add **IA_Special**:
   - Select "IA_Special"
   - Add key: `X`
   - Add key: `Right Mouse Button`

5. Save the Input Mapping Context

### 2. NOW OPEN BP_PLAYER BLUEPRINT

1. In Content Drawer, navigate to Content → Blueprints
2. Double-click "BP_Player" to open the Blueprint Editor
3. Click on **"Event Graph"** tab (above the main view, third tab from left, next to Construction Script)

You should see three default events (red nodes):
- Event BeginPlay
- Event ActorBeginOverlap  
- Event Tick

### 3. ADD MAPPING CONTEXT IN BEGINPLAY

From "Event BeginPlay" node:

1. Right-click in empty space → search `Get Player Controller` → add it
   - Use the one under "Game" → "Player" category
   - It has a "Player Index" input (default 0) and "Return Value" output
2. From the blue "Return Value" output, drag and search `Get Enhanced Input Local Player Subsystem`
3. From that blue output, drag and search `Add Mapping Context`
4. For "Mapping Context" input: 
   - Click dropdown and select `IMC_Default`
   - Or drag IMC_Default from Content Drawer
5. Set "Priority" to `0`

6. **CRITICAL - Connect the EXECUTION wire (white wire):**
   - The WHITE TRIANGLE pins are different from the BLUE CIRCLE pins!
   - Blue circles = DATA (what values to use)
   - White triangles = EXECUTION (when to run)
   
   - On "Event BeginPlay", find the WHITE TRIANGLE on the RIGHT side
   - On "Add Mapping Context", find the WHITE TRIANGLE on the LEFT side
   - Click and DRAG from BeginPlay's white triangle to Add Mapping Context's white triangle
   
   **WITHOUT THIS WHITE WIRE, THE CODE NEVER RUNS!**

Your graph should look like this:

```
┌──────────────────┐         ┌─────────────────────────────────────┐
│ Event BeginPlay  │         │      Add Mapping Context            │
│                  ├────────►│►                                    │
│                  │ WHITE   │  Target ○────────────────┐          │
└──────────────────┘ WIRE    │  Mapping Context: IMC_Default       │
                             │  Priority: 0                        │
                             └─────────────────────────────────────┘
                                      ▲
┌──────────────────┐                  │
│Get Player        │    ┌─────────────────────────┐
│Controller        ├───►│ Enhanced Input Local    │
│ Player Index [0] │    │ Player Subsystem        ├───┘
└──────────────────┘    └─────────────────────────┘
                           (blue data wires)
```

**VERIFY:** You must have BOTH:
- Blue data wires connecting the nodes (passes the subsystem reference)
- White execution wire from Event BeginPlay to Add Mapping Context (makes it run)

### 4. INPUT DEBUG TEST (verify input works - separate from movement logic)

Before creating movement, let's verify input is working with a separate debug setup. This debug logic is COMPLETELY INDEPENDENT from movement - you can delete it later without affecting anything.

#### a) Create debug variables (these are ONLY for debugging):
- In My Blueprint panel → Variables → click "+"
- Name: `DEBUG_LastMoveInput`
- Type: Vector 2D
- Default Value: (0, 0)
- Compile to save

#### b) Create a SEPARATE debug event using a Custom Event:
- Right-click in empty space → search `Custom Event` → add it
- Name it `DEBUG_PrintInput`
- This keeps debug logic completely isolated

#### c) Build the debug logic from DEBUG_PrintInput:

1. **Get the current input value:**
   - Right-click → "Get Player Controller"
   - Drag → "Get Enhanced Input Local Player Subsystem"
   - Drag → search "IA_Move" (under Input → Enhanced Action Values)

2. **Compare to last value (only print on change):**
   - Right-click → "Not Equal (Vector2D)"
   - Connect IA_Move to TOP input
   - "Get DEBUG_LastMoveInput" → connect to BOTTOM input

3. **Branch on change:**
   - From DEBUG_PrintInput WHITE pin → "Branch"
   - Connect != result to Condition

4. **On TRUE (changed):**
   - "Set DEBUG_LastMoveInput" = IA_Move value
   - Then → "Print String" with IA_Move value

#### d) Call the debug event from Event Tick:
- From "Event Tick" WHITE pin → search `DEBUG_PrintInput`
- This adds a node that calls your custom event

**Visual (two separate areas in your graph):**

```
AREA 1 - Event Tick (will later have movement):
┌─────────────┐      ┌─────────────────────┐
│ Event Tick  │─────►│ DEBUG_PrintInput    │
└─────────────┘      │ (call custom event) │
                     └─────────────────────┘

AREA 2 - Debug logic (completely separate):
┌─────────────────────┐
│ DEBUG_PrintInput    │
│ (Custom Event)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ Branch                      │
│ Condition: IA_Move != Last  │
└──────┬──────────────────────┘
       │ TRUE
       ▼
┌──────────────────┐     ┌──────────────┐
│Set DEBUG_LastMove│────►│ Print String │
└──────────────────┘     └──────────────┘
```

#### e) Compile and Save
#### f) Drag BP_Player into level, Press Play (`Alt+P`)
#### g) IMPORTANT: Click inside the game viewport to give it keyboard focus!
#### h) Press WASD keys and look at top-left of screen

**Expected:** Message appears ONLY when you press or release a key:
- Press W: prints "X=1.0 Y=0.0"
- Release W: prints "X=0.0 Y=0.0"
- Log is NOT spammed every frame

**TO DISABLE DEBUG LATER:** Simply delete the "DEBUG_PrintInput" call node from Event Tick. The Custom Event and its logic can stay (unused) or be deleted entirely - movement will be unaffected either way.

#### Debugging Steps (if you see "X=0.0 Y=0.0" always):

<details>
<summary><b>DEBUGGING STEP 1</b> - Verify the pawn is possessed</summary>

- When playing, look at the Outliner (right panel)
- Find BP_Player in the list
- If it shows a small controller icon next to it, it's possessed
- If NOT possessed: Check that "Auto Possess Player" = "Player 0" in BP_Player
</details>

<details>
<summary><b>DEBUGGING STEP 2</b> - Verify the game window has keyboard focus</summary>

- After pressing Play, CLICK INSIDE THE GAME VIEWPORT
- The viewport must have focus to receive keyboard input
- Try pressing `Shift+F1` to release mouse, then click viewport again
- Then press WASD again
</details>

<details>
<summary><b>DEBUGGING STEP 3</b> - Test with a simpler Print String</summary>

- Delete the current Print String setup
- From Event Tick, drag → Print String
- Type "Tick is running" in the In String field (just plain text)
- Play the game - you should see "Tick is running" spam in top-left
- If you DON'T see this: The blueprint isn't running at all
</details>

<details>
<summary><b>DEBUGGING STEP 4</b> - Test BeginPlay is running</summary>

- From Event BeginPlay, AFTER the Add Mapping Context node
- Add another Print String with text "BeginPlay executed"
- Connect the white wire: BeginPlay → Add Mapping Context → Print String
- Play the game - you should see "BeginPlay executed" once at start
- If you DON'T see this: BeginPlay isn't running (pawn not spawned?)
</details>

<details>
<summary><b>DEBUGGING STEP 5</b> - Check if there are MULTIPLE BP_Player in level</summary>

- Look in Outliner for multiple BP_Player instances
- Delete ALL of them
- Drag in exactly ONE fresh BP_Player from Content Drawer
- Try again
</details>

<details>
<summary><b>DEBUGGING STEP 6</b> - Nuclear option (create fresh test)</summary>

- Create a NEW blueprint: "BP_InputTest" (Pawn class)
- Add ONLY: Auto Possess Player = Player 0
- In Event Graph: Event BeginPlay → Add Mapping Context (IMC_Default)
- In Event Graph: Event Tick → Print String (connected to Get IA_Move)
- Drag this minimal test blueprint into level
- If THIS works, something is wrong with your BP_Player
</details>

**IF THIS TEST WORKS:** Continue to step 5. You can optionally delete the DEBUG_PrintInput call from Event Tick to stop the debug prints.
**IF THIS TEST FAILS:** Work through debugging steps above.

### 5. MOVEMENT LOGIC - Create this node network

> **NOTE:** If you added debug from step 4, Event Tick already has a wire to DEBUG_PrintInput. To have BOTH debug AND movement run from Event Tick, you need a Sequence node (one output pin = one wire only).

#### a) INSERT A SEQUENCE NODE between Event Tick and debug:
- Delete the wire from Event Tick to DEBUG_PrintInput
- Right-click → search `Sequence` → add it
- Connect Event Tick → Sequence (input)
- Connect Sequence "Then 0" → DEBUG_PrintInput
- Sequence "Then 1" will be used for movement

```
RESULT:
Event Tick → Sequence ─┬─ Then 0 → DEBUG_PrintInput
                       │
                       └─ Then 1 → (movement, next steps)
```

If you skipped debug, just connect Event Tick directly to movement.

#### b) Starting point for movement:
- If using Sequence: drag from "Then 1" output
- If no debug: drag from Event Tick directly

#### c) Right-click → search `Get Player Controller` and add it
(This is a NEW Get Player Controller - separate from the one in debug)

#### d) From Player Controller output, drag → `Get Enhanced Input Local Player Subsystem`

#### e) From subsystem output, drag and right-click → search `IA_Move`
- Look under "Input" → "Enhanced Action Values" → select "IA_Move"
- This node returns the current value of the IA_Move input action

#### f) The output is an Input Action Value (Vector2D since we set IA_Move to Axis2D).
Right-click the output pin → "Split Struct Pin" to get X and Y components,
OR drag from output and search "To Vector 2D" to convert it

#### g) Right-click → `Make Vector`
- Connect the X from movement input to X
- Connect the Y from movement input to Y  
- Set Z to 0

#### h) Right-click → `Normalize`
- Connect the vector output to Normalize input

#### i) Right-click → `Get World Delta Seconds`

#### j) Right-click → `Get MoveSpeed` (your variable)

#### k) Right-click → Multiply (float * float)
- Connect Delta Seconds output to first input
- Connect MoveSpeed output to second input

#### l) Right-click → Multiply (vector * float)
- Connect Normalized vector (from step h) to vector input
- Connect (DeltaSeconds * MoveSpeed) result (from step k) to float input
- This output is the "movement delta" - how far to move this frame

#### m) Right-click → `Get Actor Location`

#### n) Right-click → Add (vector + vector)
- Connect current location (from step m) to first input
- Connect movement delta (from step l) to second input

#### o) CLAMP X COORDINATE:

First, break apart the new position vector from step n:
- Right-click on the output pin of the Add node (from step n) → "Split Struct Pin"
- This splits the vector into three separate pins: X, Y, Z

Now clamp the X value:
- Right-click in empty space → search `Clamp (float)` → add it
- Connect the "X" output (from the split Add node) to "Value" input of Clamp

Get the min bound:
- Right-click → search `Get BoundsMin` (your variable) → add it
- Right-click on BoundsMin output pin → "Split Struct Pin" (splits into X, Y)
- Connect BoundsMin's "X" to Clamp's "Min" input

Get the max bound:
- Right-click → search `Get BoundsMax` (your variable) → add it
- Right-click on BoundsMax output pin → "Split Struct Pin"
- Connect BoundsMax's "X" to Clamp's "Max" input

The Clamp node now outputs the X position clamped within bounds.

#### p) CLAMP Y COORDINATE:
- Right-click → add another `Clamp (float)` node
- Connect the "Y" output (from the split Add node in step o) to "Value"
- Connect BoundsMin's "Y" (already split) to "Min"
- Connect BoundsMax's "Y" (already split) to "Max"

#### q) Right-click → `Make Vector`
- Connect clamped X
- Connect clamped Y
- Set Z to 0

#### r) Right-click → `Set Actor Location`
- Connect the clamped vector to "New Location"

#### s) CRITICAL - Connect the execution wire (white wire):
- If using Sequence (from step a): drag from "Then 1" to Set Actor Location
- If no debug: drag from Event Tick to Set Actor Location
- Without this execution wire, the movement code NEVER runs!

**Final Structure (with debug - using Sequence node):**
```
Event Tick → Sequence ─┬─ Then 0 → DEBUG_PrintInput
                       │
                       └─ Then 1 → [movement] → Set Actor Location
```

**Final Structure (without debug):**
```
Event Tick → [movement logic] → Set Actor Location
```

**TO REMOVE DEBUG:** Delete the wire from "Then 0" to DEBUG_PrintInput. Movement on "Then 1" is completely unaffected.

### 6. Click Compile and Save

### Expected Result after Compile:
- Compile button shows GREEN checkmark (no errors)
- No warnings about unconnected pins

### How to Test at This Stage:
1. Open any level (or the default "Untitled" level)
2. From Content Drawer, drag BP_Player into the viewport
3. Press Play (`Alt+P`)
4. Click inside the game viewport to give it keyboard focus
5. You should see the cube (TempVisual added in Step 2.2) and control it with WASD

### Expected Result when tested:
- Player pawn moves smoothly when pressing WASD keys
- Movement is frame-rate independent (consistent speed)
- Player cannot move outside the screen bounds (stops at edges)
- Releasing keys immediately stops movement (no drift)

> **NOTE:** Full game testing will be possible after completing [Part 8 (Level Setup)](part-8-game-mode-level.md).

### Visual Diagram of Movement Nodes:

```
┌─────────────┐     ┌──────────┐
│ Event Tick  │────►│ Sequence │─┬─ Then 0 ──► DEBUG_PrintInput (optional)
└─────────────┘     └──────────┘ │
                                 └─ Then 1 ──► Movement logic ──► Set Actor Location

(If no debug, skip Sequence and connect Event Tick directly to movement)
                 
┌──────────────────────────────────┐                 ┌────────────────────┐
│ Get Enhanced Input Subsystem     │                 │ Set Actor Location │
│ → Get Action Value (IA_Move)     │                 └────────────────────┘
│ → Get as Vector2D                │                          ▲
└────────────────┬─────────────────┘                          │
                 │                                    ┌───────────────┐
                 ▼                                    │ Clamped Vector│
    ┌────────────────────────────┐                    └───────────────┘
    │      Make Vector           │───►Normalize───►          ▲
    │  X=Input.X, Y=Input.Y, Z=0 │   (direction)             │
    └────────────────────────────┘        │           ┌─────────────┐
                                          ▼           │ + Location  │
                                    ┌──────────────┐  └─────────────┘
                                    │ * MoveSpeed  │─────────┘
                                    │ * DeltaTime  │
                                    └──────────────┘
```

---

## Step 2.5: Create Player Firing Logic

1. Continue in Event Graph, we'll add firing after movement

2. After the movement logic, add firing check using Enhanced Input:

#### a) Right-click → search `IA_Fire`
- Look under "Input" → "Enhanced Action Events" category (diamond ◇ icons)
- Select "IA_Fire" (the one with diamond icon, NOT the square icon)
- This creates an EVENT node (red, like Event Tick) that fires when the button is pressed

> **NOTE:** 
> - "Enhanced Action Events" (diamond ◇) = triggers when button pressed
> - "Enhanced Action Values" (square □) = reads current value continuously
> 
> For firing, we want the EVENT.

#### b) From the "Triggered" execution pin, build the fire rate limiter:

1. **Get current timer value:**
   - Right-click → `Get FireTimer` (your variable)

2. **Subtract frame time from it:**
   - Right-click → `Get World Delta Seconds` (time since last frame, ~0.016 at 60fps)
   - Right-click → search "float - float" or "Subtract" → add Subtract node
   - Connect FireTimer to the TOP input (A)
   - Connect Delta Seconds to the BOTTOM input (B)
   - Result = FireTimer minus DeltaSeconds

3. **Store the new timer value:**
   - Right-click → `Set FireTimer`
   - Connect the Subtract result to it
   - Connect execution wire: Triggered → Set FireTimer

4. **Check if we can fire:**
   - From Set FireTimer, drag execution → `Branch`
   - Right-click → `<= (float)` (less than or equal)
   - Connect FireTimer (use the output from Set, or Get it again) to top input
   - Type `0` in bottom input
   - Connect result to Branch's Condition

5. **On TRUE branch (timer expired, can fire):**
   - Right-click → `Set FireTimer`
   - Right-click → `Get FireInterval` (your variable)
   - Connect FireInterval to Set FireTimer (resets the cooldown)
   - For now, add a Print String with text "FIRE!" to verify it works
   - Leave the execution wire after this Set FireTimer OPEN (we'll connect FireVolley function here in [Step 3.4](part-3-create-bullet.md#step-34-complete-player-firing-logic-bp_player))

**Visual:**

```
┌──────────────────┐
│ IA_Fire Triggered│
└────────┬─────────┘
         │ (white wire)
         ▼
┌─────────────────────────────────────┐
│ Set FireTimer                        │
│   = FireTimer - GetWorldDeltaSeconds │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐    TRUE    ┌─────────────────────┐
│ Branch          │───────────►│ Set FireTimer       │──► Print "FIRE!"
│ FireTimer <= 0  │            │   = FireInterval    │    (placeholder)
└────────┬────────┘            └─────────────────────┘
         │ FALSE
         ▼
      (do nothing)
```

**TEST NOW:** Press Play, hold Z key. You should see "FIRE!" spam in top-left at rapid intervals (every 0.08 seconds = FireInterval).

> **NOTE:** Since IA_Fire was set up with Z key and Left Mouse Button in the Input Mapping Context, both inputs will trigger this action automatically.

### 3. PLACEHOLDER FOR BULLET SPAWNING

The Print String "FIRE!" is a placeholder. We will replace it with actual bullet spawning in [STEP 3.4](part-3-create-bullet.md#step-34-complete-player-firing-logic-bp_player), AFTER creating BP_Bullet in Part 3.

Leave the execution wire open after the "Set FireTimer = FireInterval" node. We'll connect FireVolley function there in STEP 3.4.

### 4. Compile and Save

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Fire rate limiter logic works (Print String spams when holding Z)
- Actual bullets will be added in [STEP 3.4](part-3-create-bullet.md#step-34-complete-player-firing-logic-bp_player) after BP_Bullet is created

---

## Step 2.6: Create Player Damage and Special Ability

> **IMPORTANT - Dependency Note:**
> The `HandleDeath` function needs to call `BP_GameDirector`, which we create in [Part 6](part-6-game-director.md).
> In this step, we will create **placeholder functions** that compile but aren't fully functional.
> We will complete `HandleDeath` in [Part 6](part-6-game-director.md#step-63-game-director-update-logic) after GameDirector exists.

---

### 1. CREATE "HandleDeath" FUNCTION (Placeholder):

We create this FIRST because `TakeHit` will call it. For now, it's a placeholder.

#### a) Create the function:
1. In My Blueprint panel (left side), find "Functions" section
2. Click the **"+"** button next to "Functions"
3. Name it `HandleDeath`
4. Double-click to open the function graph

#### b) Add placeholder logic (will be completed in Part 6):

1. The function graph opens with a purple "HandleDeath" entry node

2. **Hide the player:**
   - From the entry node's WHITE execution pin, drag and search `Set Actor Hidden in Game`
   - Check the "New Hidden" checkbox (set to TRUE)
   - This makes the player invisible when they die

3. **Add a placeholder comment:**
   - Right-click in empty space → search `Add Comment` (or press C)
   - Type: "TODO: Call GameDirector.HandlePlayerDeath (Part 6)"
   - Position it near the end of the function

4. **Connect execution:**
   ```
   HandleDeath (entry) ──► Set Actor Hidden in Game
                                    │
                                    ▼
                          [TODO comment - no connection needed]
   ```

5. Click "Compile" - should show GREEN checkmark

> **NOTE:** This function is incomplete! We'll add the GameDirector call in [Part 6, Step 6.3](part-6-game-director.md#step-63-game-director-update-logic).

---

### 2. CREATE "TakeHit" FUNCTION:

Now we can create TakeHit, which calls HandleDeath.

#### a) Create the function:
1. In My Blueprint panel → Functions → click **"+"**
2. Name it `TakeHit`
3. Double-click to open the function graph

#### b) Add input parameter:
1. With the function graph open, look at the Details panel (right side)
2. Find "Inputs" section
3. Click **"+"** to add a new input
4. Name: `Damage`
5. Type: `Integer`
6. The purple entry node now shows a "Damage" output pin

#### c) Build the function logic:

**Step 1 - Get current lives:**
- Right-click in empty space → search `Get CurrentLives` → add it
- This reads the CurrentLives variable value

**Step 2 - Subtract damage from lives:**
- Right-click → search `integer - integer` or `Subtract (int)` → add it
- Connect `CurrentLives` (from Step 1) to the TOP input (A)
- Connect `Damage` (from the purple entry node) to the BOTTOM input (B)
- Result = CurrentLives minus Damage

**Step 3 - Clamp the result (prevent negative lives):**
- Right-click → search `Clamp (int)` → add the "Clamp (integer)" node
- Connect the Subtract result (from Step 2) to the "Value" input
- Set "Min" to `0` (type directly in the field)
- Set "Max" to `99` (or any high number - we just want to prevent negatives)
- The output is the clamped value (0 or higher)

**Step 4 - Store the new lives value:**
- Right-click → search `Set CurrentLives` → add it
- Connect the Clamp output (from Step 3) to the input
- **IMPORTANT:** Connect execution wire from entry node → Set CurrentLives

**Step 5 - Check if player should die:**
- From `Set CurrentLives`, drag execution → search `Branch` → add it
- Right-click → search `<= (integer)` (less than or equal) → add it
- Connect `CurrentLives` (drag from Set node's output, or add new Get) to TOP input
- Type `0` in BOTTOM input
- Connect the `<=` result (boolean) to Branch's "Condition" input

**Step 6 - On TRUE (player is dead):**
- From Branch's "True" execution pin, drag → search `HandleDeath` → add it
- This calls the function we created in step 1

**Step 7 - On FALSE (player still alive):**
- Leave the "False" pin unconnected (do nothing, player survives)

#### d) Visual diagram of TakeHit function:

```
┌────────────────────────┐
│ TakeHit (entry)        │
│         Damage ○───────┼──────────────────────┐
└───────────┬────────────┘                      │
            │ (white execution wire)            │
            ▼                                   ▼
┌───────────────────────────────────────────────────────┐
│ Set CurrentLives                                      │
│   = Clamp( CurrentLives - Damage, Min=0, Max=99 )    │
└───────────┬───────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────┐
│ Branch                      │
│ Condition: CurrentLives <= 0│
└───────┬─────────────┬───────┘
        │ TRUE        │ FALSE
        ▼             ▼
┌───────────────┐   (nothing)
│ HandleDeath   │
└───────────────┘
```

#### e) Click Compile and Save

---

### 3. SPECIAL ABILITY (Screen Clear) - Input Setup Only:

> **IMPORTANT - Dependency Note:**
> The special ability needs to destroy BP_Enemy and BP_Bullet actors, which don't exist yet.
> In this step, we create ONLY the input handling and mark-as-used logic.
> We will complete the destruction logic in [Part 4, Step 4.6](part-4-create-enemy.md#step-46-complete-special-ability-in-bp_player) after BP_Enemy exists.

Using Enhanced Input (IA_Special was already set up with X and Right Mouse in Step 2.4):

#### a) Create the event node:
1. Go back to the **Event Graph** tab (not inside a function)
2. Right-click in empty space → search `EnhancedInputAction IA_Special`
   - Look under "Input" → "Enhanced Action Events" category
   - Select "IA_Special" (the EVENT with diamond ◇ icon)
3. This creates a red event node that fires when X or Right Mouse is pressed

#### b) Check if special was already used:
1. From the "Triggered" execution pin, drag → search `Branch` → add it
2. Right-click → search `Get SpecialUsed` → add it
3. Right-click → search `NOT Boolean` → add it
4. Connect SpecialUsed → NOT → Branch Condition
   - We branch on "NOT SpecialUsed" (true = hasn't been used yet)

#### c) On TRUE (special available) - placeholder:
1. From Branch's "True" pin, drag → search `Set SpecialUsed` → add it
2. Check the box to set it to TRUE (marks ability as used)

3. **Add placeholder Print String:**
   - From Set SpecialUsed, drag → search `Print String` → add it
   - Type: "SPECIAL ABILITY ACTIVATED!" in the In String field
   - This verifies the input works; we'll replace it with actual destruction in Part 4

4. **Add a placeholder comment:**
   - Right-click in empty space → search `Add Comment` (or press C)
   - Type: "TODO: Add enemy/bullet destruction (Part 4)"
   - Position it after the Print String

#### d) On FALSE (special already used):
- Leave unconnected (nothing happens on second press)

#### e) Visual diagram (placeholder version):

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
┌────────────────────────────────────┐
│ Print String                       │
│ "SPECIAL ABILITY ACTIVATED!"       │
└────────────────────────────────────┘
        │
        ▼
  [TODO comment - destruction logic added in Part 4]
```

#### f) Compile and Save

#### g) Test the placeholder:
1. Press Play
2. Press X key (or Right Mouse Button)
3. You should see "SPECIAL ABILITY ACTIVATED!" appear once
4. Pressing X again should do nothing (SpecialUsed = true)

> **REMINDER:** Complete the special ability with actual enemy/bullet destruction in [Part 4, Step 4.6](part-4-create-enemy.md#step-46-complete-special-ability-in-bp_player) after creating BP_Enemy.

---

### 4. Compile and Save

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- "TakeHit" and "HandleDeath" functions appear under Functions in My Blueprint panel
- Event Graph shows IA_Special event with branching logic

### Expected Result in Play mode (at this stage):
- Press X key: "SPECIAL ABILITY ACTIVATED!" appears once in top-left
- Press X again: Nothing happens (SpecialUsed is now true)
- TakeHit and HandleDeath functions exist but cannot be tested yet (nothing calls them)

> **NOTE:** Full testing of damage/death systems requires:
> - BP_Bullet collision (Part 3) to call TakeHit
> - BP_GameDirector (Part 6) for HandleDeath to notify
> - BP_Enemy (Part 4) for special ability to destroy

> **REMINDER:** Complete the `HandleDeath` function in [Part 6, Step 6.3](part-6-game-director.md#step-63-game-director-update-logic) after creating BP_GameDirector.

---

[← Previous: Part 1 - Project Setup](part-1-project-setup.md) | [Back to Index](README.md) | [Next: Part 3 - Create the Bullet →](part-3-create-bullet.md)
