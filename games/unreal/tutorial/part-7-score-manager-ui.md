# Part 7: Create Score Manager / UI

[← Previous: Part 6 - Game Director](part-6-game-director.md) | [Back to Index](README.md) | [Next: Part 8 - Game Mode and Level →](part-8-game-mode-level.md)

---

## Step 7.1: Create UI Widget Blueprint

1. Content Browser → **UI** folder
2. Right-click → **User Interface → Widget Blueprint**
3. Name: `WBP_HUD`
4. Double-click to open Widget Designer

### Expected Result

Widget Designer opens with:

- Hierarchy panel on left
- Canvas preview in center
- Details panel on right

---

## Step 7.2: Design HUD Layout

### 1. In the Palette panel (left side), search for "Canvas Panel"

- Drag Canvas Panel to the Hierarchy (if not already there)

### 2. Add Score Text

1. In Palette, search for "Text"
2. Drag "Text" widget onto Canvas Panel in hierarchy
3. Rename it `ScoreText` (right-click → Rename)
4. In Details panel:
   - Under "Slot (Canvas Panel Slot)":
     - Anchors: Top-Left (click dropdown, select corner)
     - Position X: `20`
     - Position Y: `20`
     - Size X: `300`
     - Size Y: `40`
   - Under "Appearance":
     - Text: `Score: 0`
     - Font Size: `24`
     - Color: White

### 3. Add Lives Text

1. Drag another "Text" widget
2. Rename to `LivesText`
3. Position X: `20`, Y: `60`
4. Text: `Lives: 3`
5. Same font settings as Score

### 4. Add Timer Text

1. Drag another "Text" widget
2. Rename to `TimerText`
3. Position X: `20`, Y: `100`
4. Text: `Time: 05:00`
5. Same font settings

### 5. Click "Compile" and "Save" (top buttons)

### Expected Result

Preview shows:

```
┌────────────────────────────────────┐
│ Score: 0                           │
│ Lives: 3                           │
│ Time: 05:00                        │
│                                    │
│                                    │
└────────────────────────────────────┘
```

---

## Step 7.3: Create Score Manager Blueprint

1. Content Browser → Blueprints
2. Right-click → **Blueprint Class** → **Actor**
3. Name: `BP_ScoreManager`
4. Double-click to open

5. **Create Variables:**

| Variable Name    | Type                        | Default Value    |
| ---------------- | --------------------------- | ---------------- |
| `Score`          | Integer                     | 0                |
| `CurrentLives`   | Integer                     | 3                |
| `HUDWidget`      | Object Reference to WBP_HUD | -                |
| `HUDWidgetClass` | Class Reference             | (set to WBP_HUD) |

### Expected Result after Compile

- Compile button shows GREEN checkmark
- Variables panel shows all 4 variables with correct types

---

## Step 7.4: Score Manager Initialization

### 1. From Event BeginPlay

#### a) Create HUD Widget

- Right-click → `Create Widget`
- Class: Select WBP_HUD (or use HUDWidgetClass variable)
- Owning Player: Get Player Controller (index 0)

#### b) Store widget reference

- Set HUDWidget to the created widget

#### c) Add to viewport

- Right-click → `Add to Viewport`
- Connect widget reference as target

### Expected Result after Compile

- Compile button shows GREEN checkmark
- BeginPlay event connected to Create Widget → Add to Viewport

### Expected Result in Play mode

- HUD appears immediately when game starts
- HUD displays in top-left corner of screen
- Text is visible and readable (white on game background)

---

## Step 7.5: Score Manager Functions

### 1. CREATE "RegisterGameStart" FUNCTION

**Inputs:**

- `InitialLives` (Integer)
- `Duration` (Float)

**Inside:**

- Set Score = 0
- Set CurrentLives = InitialLives
- Update all UI labels

### 2. CREATE "AddScore" FUNCTION

**Input:** `Amount` (Integer)

**Inside:**

- Add Amount to Score
- Update Score label in HUD:
  - Get HUDWidget
  - Cast to WBP_HUD
  - Get "ScoreText" widget
  - Set Text to "Score: " + Score

### 3. CREATE "SetLives" FUNCTION

**Input:** `Lives` (Integer)

**Inside:**

- Set CurrentLives = Lives
- Update Lives label in HUD

### 4. CREATE "UpdateTimer" FUNCTION

**Input:** `TimeRemaining` (Float)

**Inside:**

- Convert to minutes:seconds format:

  ```
  Minutes = Floor(TimeRemaining / 60)
  Seconds = Floor(TimeRemaining mod 60)
  ```

- Format string: "Time: MM:SS"
- Update Timer label

### 5. CREATE "HandleGameOver" FUNCTION

**Inside:**

- Set Timer text to "Game Over"

### 6. CREATE "HandleGameClear" FUNCTION

**Inside:**

- Set Timer text to "Mission Complete"

### Expected Result after Compile

- Compile button shows GREEN checkmark
- All 6 functions appear under Functions panel

### Expected Result in Play mode

- Score updates instantly when enemies are killed (+50 each)
- Lives display updates when player is hit
- Timer counts down in MM:SS format
- "Game Over" or "Mission Complete" replaces timer at game end

---

[← Previous: Part 6 - Game Director](part-6-game-director.md) | [Back to Index](README.md) | [Next: Part 8 - Game Mode and Level →](part-8-game-mode-level.md)
