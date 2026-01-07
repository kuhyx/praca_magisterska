# Quick Start: Code-First Unreal Tutorial

**Problem Solved:** The Blueprint tutorial requires extensive manual UI work (60+ clicks to define 12 variables). The code-first approach lets you **copy-paste entire code blocks** instead.

---

## ⚡ 3-Minute Quick Start

### 1. Choose Your Path

- **New Project?** → Start with [Part 1 (C++): Project Setup](part-1-cpp-project-setup.md)
- **Already have Blueprint project?** → See [Migration Guide](#migrating-from-blueprint-to-c) below
- **Just need code?** → See existing implementations in `Source/MCPGameProject/`

### 2. Create C++ Project (New Projects Only)

If starting fresh:

```
Unreal Engine → New Project → Games → Blank
✅ Project Type: C++ (NOT Blueprint!)
Name: BulletHellGame
```

If you already have a Blueprint project, skip to [Migration Guide](#migrating-from-blueprint-to-c) below.

### 3. Copy-Paste the Classes

Instead of clicking through UI 60+ times, just copy these ready-to-use files:

**STGPawn.h** (Player) - [Get from Appendix D](appendix-d-cpp-reference.md#stgpawnh-complete-file)
```cpp
// All 12 player variables in one copy-paste:
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float MoveSpeed = 750.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMin = FVector2D(-850.0f, -450.0f);

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMax = FVector2D(850.0f, 450.0f);

// ... (9 more variables, all with defaults)
```

**STGProjectile.h** (Bullets) - [Get from Appendix D](appendix-d-cpp-reference.md#stgprojectileh-complete-file)

**STGEnemy.h** (Enemies) - [Get from Appendix D](appendix-d-cpp-reference.md#stgenemyh-complete-file)

**STGGameMode.h** (Game Rules) - [Get from Appendix D](appendix-d-cpp-reference.md#stggamemodeh-complete-file)

### 4. Compile

- Click **Compile** in Unreal Editor (or build in IDE)
- Wait 30-60 seconds
- Done! All variables are now available in editor

### 5. Create Minimal Blueprints

Create Blueprint children **only** for visual assets:

1. `BP_Player` inherits from `STGPawn` → Assign ship mesh/material
2. `BP_Bullet` inherits from `STGProjectile` → Assign sphere mesh/color
3. `BP_Enemy` inherits from `STGEnemy` → Assign enemy mesh/material

**No need to define variables!** They all come from C++.

---

## 📊 Time Savings

| Task | Blueprint Approach | Code-First | Time Saved |
|------|-------------------|------------|------------|
| Define player variables (×12) | 15 minutes | 2 minutes | ⚡ 13 min |
| Define enemy variables (×15) | 20 minutes | 2 minutes | ⚡ 18 min |
| Create enemy variants (×4) | 35 minutes | 8 minutes | ⚡ 27 min |
| Implement firing logic | 30 minutes | 10 minutes | ⚡ 20 min |
| **Complete game** | **6-8 hours** | **2-3 hours** | **⚡ 4-5 hours** |

---

## 🎯 Key Benefits

### ✅ Copy-Paste Variables

**Blueprint:**
```
Click + → Type "MoveSpeed" → Select type "Float" → Compile → Set value "750.0"
Click + → Type "BoundsMin" → Select type "Vector2D" → Compile → Set value...
... (repeat 10 more times, ~15 minutes total)
```

**Code:**
```cpp
// Copy this entire block in 10 seconds:
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float MoveSpeed = 750.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMin = FVector2D(-850.0f, -450.0f);

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMax = FVector2D(850.0f, 450.0f);
```

### ✅ Version Control

**Blueprint:** Binary files, impossible to review changes

```diff
Binary files differ
```

**Code:** Readable diffs, easy code review

```diff
+ float MoveSpeed = 850.0f;  // Increased for better feel
- float MoveSpeed = 750.0f;
```

### ✅ Batch Modifications

**Blueprint:** Open each file, find variable, change value, save (2 min per file)

**Code:** Find/replace across all files (5 seconds)

```
Find: MaxHealth = 12;
Replace: MaxHealth = 24;
Replace All → Done!
```

---

## 🔗 Full Documentation Links

1. **[Code-First Tutorial](code-first-approach.md)** - Complete step-by-step guide
2. **[Appendix D: C++ Reference](appendix-d-cpp-reference.md)** - Copy-paste ready code
3. **[Blueprint vs Code Comparison](blueprint-vs-code-comparison.md)** - Detailed time analysis
4. **[Main Tutorial Index](README.md)** - Access both approaches

---

## 💡 Recommended Workflow

### For This Bullet Hell Game:

1. ✅ **Use C++ for ALL game logic and variables**
   - Player stats, movement, firing
   - Enemy behavior, health, spawning
   - Game rules, timers, scoring

2. ✅ **Use Blueprints ONLY for visual assets**
   - Assign meshes and materials
   - Set particle effects
   - Configure sound effects

### Result:

- 🚀 **3x faster development** (2-3 hours vs 6-8 hours)
- 📝 **Maintainable code** (version control, refactoring)
- 🎨 **Easy visual tweaks** (designers can change colors/meshes)

---

## 🔄 Migrating from Blueprint to C++

**Already started with the Blueprint tutorial?** Here's how to move to C++ without losing your work.

### Option 1: Add C++ to Existing Blueprint Project (Recommended)

This approach keeps your existing Blueprints and adds C++ support.

#### Step 1: Add C++ Support to Project

1. In Unreal Editor: **Tools → New C++ Class**
2. Choose any parent (e.g., "Actor") → Next
3. Name it anything (e.g., `Dummy`) → Create Class
4. **This triggers C++ project generation!**
   - Visual Studio/Rider opens
   - `Source/` folder is created
   - Project compiles (~2-5 minutes first time)

5. After compilation, you'll have:
   ```
   YourProject/
   ├── Source/              ← NEW! C++ folder created
   ├── Content/             ← Your existing Blueprints (unchanged)
   └── YourProject.uproject
   ```

#### Step 2: Create C++ Classes

Now follow the C++ tutorial parts to create classes:

1. **Tools → New C++ Class** → Pawn → `STGPawn`
2. Copy-paste code from [Part 2 (C++)](part-2-cpp-create-player.md)
3. Compile
4. Repeat for bullets, enemies, etc.

#### Step 3: Reparent Existing Blueprints

Instead of creating new BP_Player, **reparent your existing one**:

1. Open your existing `BP_Player` Blueprint
2. **File → Reparent Blueprint** (top menu)
3. In the dialog, click "All Classes" dropdown
4. Search for `STGPawn` (your C++ class)
5. Select it → Reparent

**What happens:**
- ✅ BP_Player now inherits from STGPawn (C++)
- ✅ All C++ variables appear in Blueprint
- ✅ Your existing visual assets (meshes, materials) are preserved
- ✅ Old Blueprint variables become redundant (you can delete them)

#### Step 4: Clean Up Duplicate Variables

1. In BP_Player, look at "Variables" panel
2. You'll see duplicates:
   - `MoveSpeed` (from Blueprint - old)
   - `MoveSpeed` (from STGPawn - new, with C++ icon)
3. **Delete the old Blueprint variables** - keep only C++ ones
4. Compile and Save

#### Step 5: Migrate Logic (If Needed)

If you had Blueprint nodes for logic:

**Option A:** Keep Blueprint nodes for now (hybrid approach)
- Blueprints can call C++ functions
- Gradually move logic to C++ over time

**Option B:** Move everything to C++ immediately
- Copy Blueprint logic to C++ functions
- Delete Blueprint nodes
- Use Blueprints only for visual assets

### Option 2: Fresh Start (Faster but Loses Visual Setup)

If you haven't done much visual work:

1. Create new C++ project
2. Follow C++ tutorial from [Part 1](part-1-cpp-project-setup.md)
3. Manually recreate any visual assets from old project

**When to use:** If you're still early in the Blueprint tutorial (Parts 1-3).

---

### Migration Example: BP_Player → STGPawn

**Before (Blueprint only):**
```
BP_Player (Blueprint)
├── Components (added manually in editor)
│   ├── ShipMesh
│   ├── Camera
│   └── Hitbox
├── Variables (defined one-by-one in UI)
│   ├── MoveSpeed = 750.0
│   ├── BoundsMin = (-850, -450)
│   └── ... (10 more)
└── Event Graph (Blueprint nodes for logic)
```

**After (Reparented to C++):**
```
BP_Player (Blueprint, inherits from STGPawn C++)
├── Parent Class: STGPawn ← NEW!
├── Components (inherited from C++)
│   ├── ShipMesh (from STGPawn)
│   ├── Camera (from STGPawn)
│   └── Hitbox (from STGPawn)
├── Variables (inherited from C++)
│   ├── MoveSpeed = 750.0 (from STGPawn)
│   ├── BoundsMin = (-850, -450) (from STGPawn)
│   └── ... (all from C++)
└── Visual Assets Only (meshes, materials)
    └── ShipMesh → Assign cone mesh
```

**Benefits:**
- ✅ Variables now in version control (C++ files)
- ✅ Can modify via IDE (autocomplete, refactoring)
- ✅ Type-safe (compiler checks)
- ✅ Blueprint kept for visual assets only

---

### Common Migration Pitfalls

**Problem:** "I reparented but variables duplicated!"
- **Solution:** Delete the old Blueprint variables manually. Keep only C++ ones (they have a C++ icon next to them).

**Problem:** "Compilation errors after adding C++ support"
- **Solution:** Make sure Visual Studio has "Desktop Development with C++" workload installed. Check Output Log for specific errors.

**Problem:** "My Blueprint logic stopped working after reparenting"
- **Solution:** Check that function names match. C++ functions must be marked `UFUNCTION(BlueprintCallable)` to be called from Blueprints.

**Problem:** "Hot reload isn't working"
- **Solution:** Close Unreal Editor before compiling C++ changes. Reopen after compilation. Hot reload is unreliable.

---

## ❓ FAQ

**Q: I'm new to C++, should I use Blueprint instead?**

A: The code-first tutorial is actually **easier for beginners** because:
- You copy-paste working code (less chance for errors)
- No complex node wiring (easier to understand flow)
- Clear error messages from compiler
- Better for learning (code is more transferable to other engines)

**Q: Can I mix C++ and Blueprints?**

A: Yes! That's the recommended approach:
- C++ base classes with all logic
- Blueprint children that inherit from C++
- Use Blueprints only for visual asset assignments

**Q: What if I already started with Blueprints?**

A: See the [Migration Guide](#migrating-from-blueprint-to-c) above! You can reparent existing Blueprints to C++ classes.

**Q: Do I need to know Unreal's C++ API?**

A: No! The tutorial provides **complete, working code** you can copy-paste. You'll learn the API as you read the code.

---

## 🚀 Get Started Now

**New Project:** [→ Start with Part 1 (C++)](part-1-cpp-project-setup.md)

**Existing Blueprint Project:** [→ See Migration Guide](#migrating-from-blueprint-to-c)

Build the complete bullet-hell game in 2-3 hours with copy-paste ready code!

---

[Back to Main Index](README.md)
