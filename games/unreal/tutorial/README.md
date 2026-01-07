# Unreal Engine Bullet Hell Game - Complete Tutorial

This tutorial recreates the Unity "magisterka_1" bullet-hell shooter in Unreal Engine 5.

## Game Features

- Player ship with movement and shooting
- Enemies that move downward with sinusoidal horizontal motion
- Enemy spawning that increases over time
- Radial bullet patterns from enemies
- Score, lives, and timer UI
- Special "bomb" ability to clear screen
- 5-minute game duration with victory/defeat conditions

---

## 🆕 Two Approaches Available

This tutorial offers **two ways** to implement the game:

### 1. **Code-First Approach (RECOMMENDED)** ⚡

**→ [🚀 QUICK START: 3-Minute Code-First Guide](QUICKSTART-CODE-FIRST.md)** ⭐

**→ Start the C++ Tutorial:**
- [Part 1 (C++): Project Setup](part-1-cpp-project-setup.md)
- [Part 2 (C++): Create Player](part-2-cpp-create-player.md)
- [Part 3 (C++): Create Bullet](part-3-cpp-create-bullet.md)
- [Parts 4-9 (C++) Summary](part-4-9-cpp-summary.md)

- ✅ **90% faster** - copy-paste variable blocks instead of clicking UI
- ✅ **Version control friendly** - readable Git diffs, not binary files
- ✅ **Easier to replicate** - copy entire class files between projects
- ✅ **Better for teams** - code review, refactoring tools, find/replace
- ✅ **Type-safe** - compiler catches errors at compile time

**Best for:** Anyone comfortable with C++ or wanting to learn modern game development workflows.

### 2. **Blueprint-Heavy Approach** 🎨

**→ [Start the Blueprint Tutorial](#table-of-contents)** (see below)

- ✅ **Visual node editing** - see logic flow graphically
- ✅ **Instant iteration** - no compile time for Blueprint changes
- ✅ **Designer-friendly** - non-programmers can modify behavior

**Best for:** Complete Unreal beginners, visual learners, or rapid prototyping.

### Comparison

| Task | Code-First (C++) | Blueprint |
|------|-----------------|-----------|
| Define 12+ variables | 2 minutes (copy-paste) | 15 minutes (clicking) |
| Version control | ✅ Readable diffs | ❌ Binary files |
| Refactoring | ✅ IDE tools | ❌ Manual |
| Full game time | ~2-3 hours | ~6-8 hours |

**💡 Pro Tip:** You can combine both! Use C++ for logic/variables, Blueprints for visual assets.

**📖 Migrating from Blueprint?** See [Migration Guide in Quickstart](QUICKSTART-CODE-FIRST.md#migrating-from-blueprint-to-c)

---

## Table of Contents

### Part 1: Project Setup

- [Step 1.1: Create New Project](part-1-project-setup.md#step-11-create-new-project)
- [Step 1.2: Set Up 2D Game View](part-1-project-setup.md#step-12-set-up-2d-game-view)
- [Step 1.3: Create Folder Structure](part-1-project-setup.md#step-13-create-folder-structure)

### Part 2: Create the Player

- [Step 2.1: Create Player Blueprint](part-2-create-player.md#step-21-create-player-blueprint)
- [Step 2.2: Add Player Visual Components](part-2-create-player.md#step-22-add-player-visual-components)
- [Step 2.3: Create Player Variables](part-2-create-player.md#step-23-create-player-variables)
- [Step 2.4: Set Up Enhanced Input System](part-2-create-player.md#step-24-set-up-enhanced-input-system)
- [Step 2.5: Create Player Firing Logic](part-2-create-player.md#step-25-create-player-firing-logic)
- [Step 2.6: Create Player Damage and Special Ability](part-2-create-player.md#step-26-create-player-damage-and-special-ability)

### Part 3: Create the Bullet

- [Step 3.1: Create Bullet Blueprint](part-3-create-bullet.md#step-31-create-bullet-blueprint)
- [Step 3.2: Bullet Movement Logic](part-3-create-bullet.md#step-32-bullet-movement-logic)
- [Step 3.3: Bullet Collision Logic](part-3-create-bullet.md#step-33-bullet-collision-logic)
- [Step 3.4: Complete Player Firing Logic](part-3-create-bullet.md#step-34-complete-player-firing-logic-bp_player)

### Part 4: Create the Enemy

- [Step 4.1: Create Enemy Blueprint](part-4-create-enemy.md#step-41-create-enemy-blueprint)
- [Step 4.2: Enemy Initialization](part-4-create-enemy.md#step-42-enemy-initialization)
- [Step 4.3: Enemy Movement Logic](part-4-create-enemy.md#step-43-enemy-movement-logic)
- [Step 4.4: Enemy Firing Logic](part-4-create-enemy.md#step-44-enemy-firing-logic)
- [Step 4.5: Enemy Damage and Death](part-4-create-enemy.md#step-45-enemy-damage-and-death)
- [Step 4.6: Complete Special Ability in BP_Player](part-4-create-enemy.md#step-46-complete-special-ability-in-bp_player)
- [Step 4.7: Complete Bullet Collision Logic](part-4-create-enemy.md#step-47-complete-bullet-collision-logic-bp_bullet)

### Part 5: Create Enemy Spawner

- [Step 5.1: Create Spawner Blueprint](part-5-create-spawner.md#step-51-create-spawner-blueprint)
- [Step 5.2: Spawn Rate Curve](part-5-create-spawner.md#step-52-spawn-rate-curve)
- [Step 5.3: Spawning Logic](part-5-create-spawner.md#step-53-spawning-logic)

### Part 6: Create Game Director

- [Step 6.1: Create Game Director Blueprint](part-6-game-director.md#step-61-create-game-director-blueprint)
- [Step 6.2: Game Director Initialization](part-6-game-director.md#step-62-game-director-initialization)
- [Step 6.3: Game Director Update Logic](part-6-game-director.md#step-63-game-director-update-logic)

### Part 7: Create Score Manager / UI

- [Step 7.1: Create UI Widget Blueprint](part-7-score-manager-ui.md#step-71-create-ui-widget-blueprint)
- [Step 7.2: Design HUD Layout](part-7-score-manager-ui.md#step-72-design-hud-layout)
- [Step 7.3: Create Score Manager Blueprint](part-7-score-manager-ui.md#step-73-create-score-manager-blueprint)
- [Step 7.4: Score Manager Initialization](part-7-score-manager-ui.md#step-74-score-manager-initialization)
- [Step 7.5: Score Manager Functions](part-7-score-manager-ui.md#step-75-score-manager-functions)

### Part 8: Create Game Mode and Level

- [Step 8.1: Create Custom Game Mode](part-8-game-mode-level.md#step-81-create-custom-game-mode)
- [Step 8.2: Configure Project to Use Game Mode](part-8-game-mode-level.md#step-82-configure-project-to-use-game-mode)
- [Step 8.3: Create Game Level](part-8-game-mode-level.md#step-83-create-game-level)
- [Step 8.4: Set Up Level Components](part-8-game-mode-level.md#step-84-set-up-level-components)
- [Step 8.5: Set Default Level](part-8-game-mode-level.md#step-85-set-default-level)

### Part 9: Final Setup and Testing

- [Step 9.1: Assign Blueprint References](part-9-final-setup.md#step-91-assign-blueprint-references)
- [Step 9.2: Create Final Visuals](part-9-final-setup.md#step-92-create-final-visuals-replace-placeholder)
- [Step 9.3: Add Background](part-9-final-setup.md#step-93-add-background-optional)
- [Step 9.4: Test the Game](part-9-final-setup.md#step-94-test-the-game)
- [Step 9.5: Build Standalone Game](part-9-final-setup.md#step-95-build-standalone-game)

### Appendices

- [Appendix A: Complete Variable Reference](appendix-a-variables.md) (Blueprint)
- [Appendix B: Troubleshooting](appendix-b-troubleshooting.md)
- [Appendix C: Unity to Unreal Conversion Notes](appendix-c-unity-conversion.md)

---

## Quick Start

### For Code-First Approach (Recommended)

1. Read [3-Minute Quickstart](QUICKSTART-CODE-FIRST.md)
2. Start with [Part 1 (C++): Project Setup](part-1-cpp-project-setup.md)
3. Follow parts 2-3, then [Parts 4-9 Summary](part-4-9-cpp-summary.md)
4. **Complete the game in 2-3 hours** instead of 6-8 hours!
5. **Already have Blueprint project?** See [Migration Guide](QUICKSTART-CODE-FIRST.md#migrating-from-blueprint-to-c)

### For Blueprint Approach

1. Start with [Part 1: Project Setup](part-1-project-setup.md)
2. Follow each part in order
3. Test frequently using the "EXPECTED RESULT" sections
4. Use the [Troubleshooting](appendix-b-troubleshooting.md) appendix if you encounter issues

---

## Navigation

Each page includes:

- **← Previous** and **Next →** links at the top and bottom
- Links back to this index
- Cross-references to related sections

---

_This tutorial is part of a master's thesis comparing Unity and Unreal Engine._
