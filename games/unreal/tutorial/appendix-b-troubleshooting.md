# Appendix B: Troubleshooting

[← Appendix A: Variables](appendix-a-variables.md) | [Back to Index](README.md) | [Appendix C: Unity Conversion →](appendix-c-unity-conversion.md)

---

## Player doesn't move

<details>
<summary><b>Click to expand solutions</b></summary>

1. Verify IMC_Default Input Mapping Context is added in BeginPlay
2. Check that IA_Move Input Action exists and has correct key bindings
3. Ensure "Possess" is called on player pawn (automatic with GameMode)
4. Verify MoveSpeed > 0
5. Check if blueprint has errors (Compile button should be green checkmark)
6. Make sure Enhanced Input plugin is enabled (Edit → Plugins → Enhanced Input)
7. **CRITICAL:** Verify Project Settings → Input → Default Classes are set to Enhanced Input

</details>

---

## Bullets don't spawn

<details>
<summary><b>Click to expand solutions</b></summary>

1. Check BulletClass variable is set to BP_Bullet
2. Verify SpawnActor node has valid class
3. Check that fire logic is connected to execution flow
4. Ensure the FireVolley function is connected to the fire rate limiter
5. Verify BP_Bullet blueprint compiles without errors

</details>

---

## No collisions detected

<details>
<summary><b>Click to expand solutions</b></summary>

1. Verify collision components have "Generate Overlap Events" checked
2. Check collision channels are set correctly
3. Ensure "Collision Enabled" is set to "Query Only" or "Query and Physics"
4. Verify both actors have collision components (not just one)
5. Check that the Cast To nodes succeed (add print statements to debug)

</details>

---

## UI doesn't appear

<details>
<summary><b>Click to expand solutions</b></summary>

1. Check HUD widget is created and added to viewport
2. Verify ScoreManager is in the level
3. Check widget blueprint compiles without errors
4. Ensure "Add to Viewport" node is connected in execution flow
5. Verify text color is visible against background (try white text)

</details>

---

## Enemies don't spawn

<details>
<summary><b>Click to expand solutions</b></summary>

1. Check EnemyClass is set in Spawner
2. Verify SpawningActive is true
3. Check spawn position is within camera view
4. Ensure BP_EnemySpawner is placed in the level
5. Verify the SpawnCurve asset is assigned

</details>

---

## Game runs too fast/slow

<details>
<summary><b>Click to expand solutions</b></summary>

1. All movement should multiply by DeltaSeconds
2. Check speed values (may need adjustment for Unreal scale)
3. Unreal uses centimeters; multiply Unity values by ~100
4. Verify no duplicate Event Tick processing
5. Check frame rate (use `stat fps` console command)

</details>

---

## Input works in editor but not in packaged build

<details>
<summary><b>Click to expand solutions</b></summary>

1. Ensure all Input Actions and IMC_Default are saved
2. Check that assets are not in a "Developer" folder (excluded from builds)
3. Verify Project Settings input classes are set correctly
4. Try clearing Saved and Intermediate folders, then rebuild

</details>

---

## Blueprint won't compile

<details>
<summary><b>Click to expand solutions</b></summary>

1. Look at the Compiler Results panel for specific errors
2. Check for circular references between blueprints
3. Ensure all required inputs are connected
4. Verify variable types match (no type mismatches)
5. Look for "Access None" errors (null references)

</details>

---

## Camera doesn't show the game correctly

<details>
<summary><b>Click to expand solutions</b></summary>

1. Verify camera position: `X=0, Y=0, Z=1000`
2. Verify camera rotation: `X=-90, Y=0, Z=0` (looking down)
3. Check "Auto Activate for Player" is enabled
4. For orthographic: Set Projection Mode and Ortho Width
5. Ensure no other cameras are taking priority

</details>

---

## General Debugging Tips

### Enable Print Statements
```
Right-click → Print String → Type message
```
Add these throughout your blueprints to track execution flow.

### Check Output Log
- **Window → Developer Tools → Output Log**
- Shows blueprint errors, warnings, and print statements

### Use Breakpoints
- Right-click any blueprint node → **Add Breakpoint**
- Execution pauses at that point during Play mode
- Step through with F10/F11

### Visualize Collisions
- In viewport: **Show → Collision**
- Shows collision shapes in play mode

### Console Commands
- Press `~` (tilde) to open console
- `stat fps` - Show frame rate
- `show collision` - Toggle collision visualization

---

[← Appendix A: Variables](appendix-a-variables.md) | [Back to Index](README.md) | [Appendix C: Unity Conversion →](appendix-c-unity-conversion.md)
