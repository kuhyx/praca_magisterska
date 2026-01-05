# Part 9: Final Setup and Testing

[← Previous: Part 8 - Game Mode and Level](part-8-game-mode-level.md) | [Back to Index](README.md) | [Appendix A: Variables →](appendix-a-variables.md)

---

## Step 9.1: Assign Blueprint References

### 1. Open BP_Player

- In Details panel (with blueprint open)
- Set BulletClass: `BP_Bullet`

### 2. Open BP_EnemySpawner

- Set EnemyClass: `BP_Enemy`

### 3. Open BP_Enemy

- Set BulletClass: `BP_Bullet`

### 4. Compile and Save all blueprints

### Expected Result after Compile (all blueprints)

- All blueprints compile with GREEN checkmark
- No "None" or missing references in variable defaults
- BP_Player.BulletClass → BP_Bullet
- BP_Enemy.BulletClass → BP_Bullet
- BP_EnemySpawner.EnemyClass → BP_Enemy

### Expected Result in Play mode

- Player can shoot bullets (BP_Bullet spawns)
- Enemies spawn and shoot bullets
- All collision/damage systems functional

---

## Step 9.2: Create Final Visuals (Replace Placeholder)

Now replace the temporary cube visuals with proper colored materials:

### 1. REMOVE TEMPORARY COMPONENTS

1. Open BP_Player blueprint
2. In Components panel, select "TempVisual" (the cube added in [Step 2.2](part-2-create-player.md#step-22-add-player-visual-components))
3. Press Delete to remove it
4. Select "PlayerCamera" and delete it (the level camera from [Step 8.4](part-8-game-mode-level.md#step-84-set-up-level-components) will be used)
5. Repeat for BP_Bullet and BP_Enemy (delete their TempVisual cubes)

### 2. Content Browser → Materials folder

### 3. PLAYER MATERIAL

1. Right-click → Material
2. Name: `M_Player`
3. Double-click to open Material Editor
4. Create Vector3 node (hold 3, click)
5. Set to blue color `(0, 0.5, 1)`
6. Connect to Base Color
7. Save and Close

### 4. BULLET MATERIALS

- Create `M_PlayerBullet` - Yellow `(1, 1, 0)`
- Create `M_EnemyBullet` - Red `(1, 0, 0)`

### 5. ENEMY MATERIAL

- Create `M_Enemy` - Magenta `(1, 0, 1)`

### 6. Apply materials to sprite components in each Blueprint

(Or use Sprite assets if you have 2D images)

### Expected Result in Play mode

- Player visible as blue shape
- Player bullets visible as yellow shapes
- Enemy bullets visible as red shapes
- Enemies visible as magenta shapes
- All game elements distinguishable by color

---

## Step 9.3: Add Background (Optional)

### 1. In level, add a Plane mesh

- Place Actors → Basic → Plane
- Scale: `X=20, Y=30, Z=1`
- Position: `X=0, Y=0, Z=-100` (behind everything)

### 2. Create dark space material

- `M_Background` - Dark blue/black

### Expected Result in Play mode

- Dark background visible behind all game elements
- Game elements (player, enemies, bullets) clearly visible against background
- Background doesn't interfere with gameplay (Z=-100, behind everything)

---

## Step 9.4: Test the Game

### 1. Click "Play" button (green arrow in main toolbar)

OR press `Alt+P`

### 2. TEST CHECKLIST

| #   | Test                                          | Pass? |
| --- | --------------------------------------------- | ----- |
| 1   | Player moves with WASD or Arrow keys          | ☐     |
| 2   | Player stays within screen bounds             | ☐     |
| 3   | Player shoots with Z key or Left Mouse        | ☐     |
| 4   | Bullets travel upward                         | ☐     |
| 5   | Enemies spawn at top of screen                | ☐     |
| 6   | Enemies move down with wavy motion            | ☐     |
| 7   | Enemies shoot radial bullet patterns          | ☐     |
| 8   | Player bullets damage enemies                 | ☐     |
| 9   | Enemy bullets damage player                   | ☐     |
| 10  | Score increases when enemies die              | ☐     |
| 11  | Lives decrease when player is hit             | ☐     |
| 12  | Timer counts down from 5:00                   | ☐     |
| 13  | Game shows "Game Over" when lives = 0         | ☐     |
| 14  | Game shows "Mission Complete" after 5 minutes | ☐     |
| 15  | Special ability (X key) clears screen         | ☐     |

### 3. To stop playing: Press `ESC` or click "Stop" button

### Expected Result - Complete Game Test

- All checklist items above should pass
- Frame rate stable (60+ FPS recommended)
- No crashes or Blueprint errors in Output Log
- Game is playable from start to victory/defeat

---

## Step 9.5: Build Standalone Game

1. **File → Package Project → Windows** (or your platform)
2. Select output folder
3. Wait for build to complete
4. Navigate to output folder → WindowsNoEditor → [ProjectName].exe
5. Run the executable to play standalone

### Expected Result

- Build completes without errors (check Output Log)
- Executable file created in output folder
- Running .exe launches the game in fullscreen
- Game plays identically to editor Play mode
- Can close with `Alt+F4` or in-game quit (if implemented)

---

## 🎉 Congratulations

You have completed the Unreal Engine Bullet Hell tutorial!

Your game includes:

- ✅ Player with 3 lives, WASD movement, Z/mouse shooting
- ✅ Volley shooting (3 bullets in spread pattern)
- ✅ Screen-clear special ability (X key, one use)
- ✅ Enemies with sine-wave movement
- ✅ Radial bullet patterns (20 bullets per burst)
- ✅ Progressive difficulty (spawn rate increases over 5 minutes)
- ✅ Score, lives, and timer UI
- ✅ Victory after 5 minutes survival
- ✅ Game over when lives reach 0

---

### Additional Resources

- [Appendix A: Complete Variable Reference](appendix-a-variables.md)
- [Appendix B: Troubleshooting](appendix-b-troubleshooting.md)
- [Appendix C: Unity to Unreal Conversion Notes](appendix-c-unity-conversion.md)

---

[← Previous: Part 8 - Game Mode and Level](part-8-game-mode-level.md) | [Back to Index](README.md) | [Appendix A: Variables →](appendix-a-variables.md)
