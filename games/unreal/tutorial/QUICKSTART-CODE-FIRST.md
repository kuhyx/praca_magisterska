# Quick Start: Code-First Unreal Tutorial

**Problem Solved:** The Blueprint tutorial requires extensive manual UI work (60+ clicks to define 12 variables). The code-first approach lets you **copy-paste entire code blocks** instead.

---

## ⚡ 3-Minute Quick Start

### 1. Choose Your Path

- **New to Unreal?** → Start with [Code-First Tutorial](code-first-approach.md) (recommended)
- **Want comparison?** → Read [Blueprint vs Code Comparison](blueprint-vs-code-comparison.md)
- **Need copy-paste code?** → Go to [Appendix D: C++ Reference](appendix-d-cpp-reference.md)

### 2. Create C++ Project

```
Unreal Engine → New Project → Games → Blank
✅ Project Type: C++ (NOT Blueprint!)
Name: BulletHellGame
```

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

A: You can migrate! See [Migration Guide in Appendix D](appendix-d-cpp-reference.md#migration-guide)

**Q: Do I need to know Unreal's C++ API?**

A: No! The tutorial provides **complete, working code** you can copy-paste. You'll learn the API as you read the code.

---

## 🚀 Get Started Now

**[→ Start the Code-First Tutorial](code-first-approach.md)**

Build the complete bullet-hell game in 2-3 hours with copy-paste ready code!

---

[Back to Main Index](README.md)
