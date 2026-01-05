# Part 8: Create Game Mode and Level

[← Previous: Part 7 - Score Manager / UI](part-7-score-manager-ui.md) | [Back to Index](README.md) | [Next: Part 9 - Final Setup and Testing →](part-9-final-setup.md)

---

## Step 8.1: Create Custom Game Mode

1. Content Browser → Blueprints
2. Right-click → **Blueprint Class**
3. In popup, expand "All Classes"
4. Search for "Game Mode Base"
5. Select "Game Mode Base" and click Select
6. Name: `BP_BulletHellGameMode`
7. Double-click to open

8. In the Details panel (with BP_BulletHellGameMode open):
   - Find "Classes" section
   - Default Pawn Class: Select `BP_Player`
   - Player Controller Class: Keep default

### Expected Result after Compile:
- Compile button shows GREEN checkmark
- Details panel shows "Default Pawn Class" set to BP_Player

---

## Step 8.2: Configure Project to Use Game Mode

1. Go to **Edit → Project Settings**
2. In left sidebar, click "Maps & Modes"
3. Under "Default Modes":
   - Default GameMode: Select `BP_BulletHellGameMode`
4. Close Project Settings

### Expected Result:
- Project Settings shows BP_BulletHellGameMode as Default GameMode
- This means the game will automatically spawn BP_Player when Play is pressed

---

## Step 8.3: Create Game Level

1. **File → New Level**
2. Select "Empty Level"
3. **File → Save Current Level As**
4. Navigate to Content folder
5. Name: `BulletHellLevel`
6. Click Save

### Expected Result:
- New level file "BulletHellLevel" appears in Content folder
- Level is completely empty (black viewport)
- Outliner shows only default actors (if any)

---

## Step 8.4: Set Up Level Components

In the level (main viewport), we need to add game actors:

### 1. ADD CAMERA:

1. In Place Actors panel (left side, or Window → Place Actors)
2. Search for "Camera Actor"
3. Drag into viewport
4. Position camera:
   - In Details panel, under Transform:
   - Location: `X=0, Y=0, Z=1000`
   - Rotation: `X=-90, Y=0, Z=0` (looking down)
5. Set as default camera:
   - In Details panel, find "Auto Activate for Player"
   - Check the box, set Player Index to `0`

**For Orthographic View:**
- Click on Camera component
- In Details, set "Projection Mode" to `Orthographic`
- Set "Ortho Width" to `1920` (or your screen width)

### 2. ADD PLAYER:

1. From Content Browser, drag `BP_Player` into level
2. Position: `X=0, Y=-300, Z=0` (bottom center)

### 3. ADD ENEMY SPAWNER:

1. Drag `BP_EnemySpawner` into level
2. Position: `X=0, Y=500, Z=0` (top of screen)
3. In Details panel, set EnemyClass to `BP_Enemy`

### 4. ADD GAME DIRECTOR:

1. Drag `BP_GameDirector` into level
2. Position doesn't matter (it's invisible)

### 5. ADD SCORE MANAGER:

1. Drag `BP_ScoreManager` into level
2. Position doesn't matter

### 6. Save the level (`Ctrl+S`)

### Expected Result in Level Viewport:
- Camera actor visible at top of scene (Z=1000)
- BP_Player visible at bottom center (Y=-300)
- BP_EnemySpawner visible at top (Y=500)
- BP_GameDirector and BP_ScoreManager in Outliner (invisible actors)

### Expected Result in Outliner:
```
- CameraActor
- BP_Player
- BP_EnemySpawner  
- BP_GameDirector
- BP_ScoreManager
```

---

## Step 8.5: Set Default Level

1. **Edit → Project Settings**
2. Maps & Modes
3. Under "Default Maps":
   - Editor Startup Map: Select `BulletHellLevel`
   - Game Default Map: Select `BulletHellLevel`

### Expected Result:
- Project Settings shows BulletHellLevel as both startup and default map
- Launching the game (standalone or in editor) loads this level automatically

---

[← Previous: Part 7 - Score Manager / UI](part-7-score-manager-ui.md) | [Back to Index](README.md) | [Next: Part 9 - Final Setup and Testing →](part-9-final-setup.md)
