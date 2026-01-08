# Part 9 (C++): Final Setup

[← Previous: Part 8 (C++) - Create Game Mode](part-8-cpp-create-game-mode.md) | [Back to Index](README.md)

---

## Overview

Polish the game with visual assets, materials, and final tweaks.

**Time:** ~15 minutes

---

## Step 9.1: Assign Better Visuals to Blueprints

Now we use Blueprints for what they're good at: assigning visual assets!

### BP_Player:

1. Open `BP_Player`
2. Select `ShipMesh` component
3. In Details:
   - **Static Mesh** → Keep Cone or choose a spaceship model
   - **Material** → Create or assign a green emissive material
4. Compile and Save

### BP_Enemy:

1. Open `BP_Enemy`
2. Select `MeshComp` component
3. In Details:
   - **Static Mesh** → Keep Cube or choose enemy model
   - **Material** → Create or assign a red emissive material
4. Compile and Save

### BP_Bullet (if you created one):

1. Same process - assign materials for player (green) vs enemy (red) bullets

---

## Step 9.2: Create Background

1. In level, add **Plane** (from Place Actors → Basic → Plane)
2. Scale it large (Scale: 50, 50, 1)
3. Position below player (Z: -100)
4. Assign dark material (black or dark blue)
5. This provides contrast for bullets and enemies

---

## Step 9.3: Adjust Camera

If camera needs adjustment:

1. Select BP_Player in level
2. Find `SpringArm` component
3. Adjust:
   - **Target Arm Length** - Higher = further away camera
   - **Socket Offset** - Adjust view position

---

## Step 9.4: Final Testing

Press Play and verify:

**Gameplay:**
- ✅ Player moves smoothly with WASD
- ✅ Player fires green bullets in spread pattern
- ✅ Enemies spawn from top
- ✅ Enemies move in sine wave pattern
- ✅ Enemies fire red bullet bursts
- ✅ Collision detection works (bullets hit enemies, enemies hit player)
- ✅ Score increases when enemies destroyed
- ✅ Lives decrease when hit
- ✅ Special ability clears screen (X key)
- ✅ Timer counts down
- ✅ Victory after 300 seconds
- ✅ Game over if lives reach 0

**Visual Polish:**
- ✅ Player and enemies have distinct colors
- ✅ Bullets are visible and distinguishable
- ✅ UI is readable
- ✅ Background provides good contrast

**Performance:**
- ✅ 60 FPS with 100+ bullets on screen
- ✅ No lag or stuttering

---

## Step 9.5: Build Standalone Game (Optional)

To build a playable executable:

1. **File → Package Project → Windows** (or Linux)
2. Choose output folder
3. Wait for build (5-10 minutes)
4. Run the `.exe` file from output folder

---

## Completion Summary

### Total Time Comparison

| Part | Blueprint | C++ | Time Saved |
|------|-----------|-----|------------|
| 1. Project Setup | 5 min | 10 min | -5 min |
| 2. Player | 60 min | 15 min | 45 min ⚡ |
| 3. Bullet | 30 min | 10 min | 20 min ⚡ |
| 4. Enemy | 90 min | 25 min | 65 min ⚡ |
| 5. Spawner | 40 min | 10 min | 30 min ⚡ |
| 6. Game Director | 45 min | 10 min | 35 min ⚡ |
| 7. UI | 30 min | 15 min | 15 min ⚡ |
| 8. Game Mode | 20 min | 5 min | 15 min ⚡ |
| 9. Final Setup | 40 min | 15 min | 25 min ⚡ |
| **TOTAL** | **6-8 hours** | **2-3 hours** | **4-5 hours saved!** ⚡⚡⚡ |

### Key Benefits Achieved

✅ **90% faster variable definition** - copy-paste vs clicking  
✅ **Version control friendly** - readable C++ diffs instead of binary Blueprints  
✅ **Type-safe** - compiler catches errors before runtime  
✅ **IDE support** - autocomplete, refactoring, debugging  
✅ **Easier to maintain** - code is documentation  
✅ **Reusable** - copy C++ files to new projects instantly  

### Hybrid Approach Used

- **C++ for logic** - All game mechanics, variables, algorithms
- **Blueprints for visuals** - Meshes, materials, colors
- **Best of both worlds** - Fast development + visual asset management

---

## What's Next?

**Extend the game:**
- Add power-ups
- Multiple enemy types
- Boss battles
- Sound effects and music
- Particle effects
- Leaderboard system

**All easily done in C++** with the same copy-paste efficiency!

---

## Congratulations! 🎉

You've built a complete bullet-hell game in Unreal Engine using C++ in 2-3 hours instead of 6-8 hours with Blueprints!

---

[← Previous: Part 8 (C++) - Create Game Mode](part-8-cpp-create-game-mode.md) | [Back to Index](README.md)
