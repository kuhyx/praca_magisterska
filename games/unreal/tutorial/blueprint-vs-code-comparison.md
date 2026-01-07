# Blueprint vs Code: A Practical Comparison

[Back to Index](README.md) | [Code-First Tutorial](code-first-approach.md)

---

## The Problem: Editor-Heavy Blueprints Are Tedious

When implementing the bullet-hell game using Blueprints, you face these specific pain points:

### Pain Point 1: Defining Multiple Variables

**Blueprint Approach (Part 2: Create Player):**

For **each of the 12 player variables**, you must:

1. Click "+" button in Variables panel
2. Type variable name manually
3. Click in Details panel
4. Scroll to find "Variable Type" dropdown
5. Select type from long list (Float, Integer, Vector 2D, etc.)
6. Click "Compile" button
7. Wait for compile
8. Click on variable again
9. Find "Default Value" in Details panel
10. Type the value manually

**Result:** ~60 seconds per variable × 12 variables = **~12 minutes just for player variables**

If you make a typo, you have to:
- Delete the variable
- Start over from step 1

**Code Approach:**

```cpp
// Copy-paste this entire block (10 seconds):
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float MoveSpeed = 750.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMin = FVector2D(-850.0f, -450.0f);

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FVector2D BoundsMax = FVector2D(850.0f, 450.0f);

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float FireInterval = 0.08f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float BulletSpeed = 2200.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 VolleySize = 3;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float VolleySpread = 12.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 MaxLives = 3;

UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
int32 CurrentLives = 3;

UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
int32 Score = 0;

UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
bool bSpecialUsed = false;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float FireRate = 0.08f;
```

**Result:** 10 seconds to copy-paste entire block

**Time saved:** ~11 minutes per class × 4 classes (Player, Bullet, Enemy, GameMode) = **~44 minutes saved**

---

### Pain Point 2: Copying Parameters Between Classes

**Scenario:** You want Enemy bullets to have similar but slightly different parameters than Player bullets.

**Blueprint Approach:**

1. Open BP_Bullet
2. For each variable you want to copy:
   - Memorize or write down: name, type, default value
   - Open BP_Enemy
   - Click "+" to add variable
   - Type name manually (risk of typo)
   - Select type from dropdown
   - Compile
   - Set default value
   - Repeat 5-10 times

**Result:** ~5 minutes to copy 5-10 related variables, error-prone

**Code Approach:**

```cpp
// In STGProjectile.h - player bullets
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
float Speed = 2200.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
float Lifetime = 4.0f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
FLinearColor BulletColor = FLinearColor::Green;

// In STGEnemy.h - copy the block, change the values
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float EnemyBulletSpeed = 1000.0f;  // Changed value

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
float EnemyBulletLifetime = 6.0f;  // Changed value

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
FLinearColor EnemyBulletColor = FLinearColor::Red;  // Changed value
```

**Result:** 30 seconds to copy-paste and modify

**Benefit:**
- ✅ No typos in variable names (copy-paste exact)
- ✅ No wrong type selection (copy-paste exact)
- ✅ Easy to see differences (use IDE diff/compare)
- ✅ Can use find/replace to batch rename

---

### Pain Point 3: Blueprint Node Logic vs Code Logic

**Example:** Enemy firing a radial burst of bullets

**Blueprint Approach:**

You need to create this node network:

1. Event Tick node
2. Branch node (check if should fire)
3. Get FireTimer variable node
4. Float - Float (subtract) node
5. Get World Delta Seconds node
6. Set FireTimer node
7. Float <= Float (comparison) node
8. Constant 0.0 node
9. Branch node
10. For Loop node with Break node
11. Get BulletsPerBurst variable node
12. Float / Float (divide) node for angle calculation
13. Get BurstSpread variable node
14. Float * Float (multiply) node
15. Integer - Integer (subtract) for centering
16. Spawn Actor from Class node
17. Make Rotator node
18. Get Actor Location node
19. Get BulletClass variable node
20. Cast to BP_Bullet node
21. Set bIsPlayerBullet node
22. Set BulletColor node
23. ... (30+ nodes total)

**Issues:**
- Hard to see the big picture (nodes scattered across screen)
- Easy to forget connections (white execution wires vs blue data wires)
- Difficult to debug (print each node's output)
- Can't easily comment blocks of logic
- No IDE autocomplete or type checking

**Code Approach:**

```cpp
void ASTGEnemy::Fire()
{
    // Fire radial burst of bullets
    for (int32 i = 0; i < BulletsPerBurst; i++)
    {
        // Calculate angle for this bullet in the burst
        float AngleDeg = (BurstSpread / BulletsPerBurst) * i;
        float AngleRad = FMath::DegreesToRadians(AngleDeg);
        
        // Calculate direction vector
        FVector Direction = FVector(
            FMath::Cos(AngleRad),
            FMath::Sin(AngleRad),
            0.0f
        );
        
        // Spawn location slightly in front of enemy
        FVector SpawnLocation = GetActorLocation() + FVector(0.f, 0.f, -30.f);
        
        // Spawn the bullet
        ASTGProjectile* Bullet = GetWorld()->SpawnActor<ASTGProjectile>(
            ASTGProjectile::StaticClass(),
            SpawnLocation,
            Direction.Rotation()
        );
        
        if (Bullet)
        {
            Bullet->bIsPlayerBullet = false;
            Bullet->SetSpeed(EnemyBulletSpeed);
            Bullet->SetBulletColor(FLinearColor::Red);
        }
    }
}
```

**Benefits:**
- ✅ All logic in one place, easy to read top-to-bottom
- ✅ IDE autocomplete helps prevent typos
- ✅ Inline comments explain the logic
- ✅ Easy to debug (set breakpoints, inspect variables)
- ✅ Can copy-paste entire function to reuse pattern
- ✅ Compiler catches type errors immediately

---

### Pain Point 4: Making Changes to Multiple Parameters

**Scenario:** After playtesting, you decide all enemy health values should be doubled.

**Blueprint Approach:**

1. Open BP_Enemy
2. Find "MaxHealth" variable in My Blueprint panel
3. Click on it
4. Find Default Value in Details panel
5. Change 12 → 24
6. Click Compile
7. Click Save
8. Repeat for any enemy variants (BP_EnemyA, BP_EnemyB, etc.)

If you have 4 enemy types with different health values:
- Open each Blueprint
- Find the variable
- Change the value
- Compile and save
- **Result:** ~2 minutes

**Code Approach:**

```cpp
// Before (in STGEnemy.h):
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 MaxHealth = 12;

// After - just change one line:
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
int32 MaxHealth = 24;

// Compile once, all enemies updated
```

Or use find/replace to change multiple values at once:
- Find: `MaxHealth = 12;`
- Replace: `MaxHealth = 24;`
- Done in 5 seconds

**Benefit:** **24x faster** (2 minutes vs 5 seconds)

---

### Pain Point 5: Version Control and Collaboration

**Blueprint Approach:**

Blueprint files are **binary**, which means:

❌ **Cannot see changes in Git diff**
```
diff --git a/Content/Blueprints/BP_Player.uasset b/Content/Blueprints/BP_Player.uasset
index a1b2c3d..e4f5g6h 100644
Binary files a/Content/Blueprints/BP_Player.uasset and b/Content/Blueprints/BP_Player.uasset differ
```

You cannot tell:
- What changed?
- Who changed it?
- Why was it changed?
- Is it safe to merge?

❌ **Merge conflicts are nightmares**
- Two people modify same Blueprint
- Git shows "Binary conflict"
- You must manually recreate changes by:
  - Opening both versions in Unreal
  - Comparing node-by-node
  - Manually rebuilding the merged version

**Code Approach:**

C++ files are **plain text**, which means:

✅ **Readable Git diffs**
```cpp
diff --git a/Source/BulletHellGame/STGPawn.h b/Source/BulletHellGame/STGPawn.h
index a1b2c3d..e4f5g6h 100644
--- a/Source/BulletHellGame/STGPawn.h
+++ b/Source/BulletHellGame/STGPawn.h
@@ -15,7 +15,7 @@
 public:
     UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
-    float MoveSpeed = 750.0f;
+    float MoveSpeed = 850.0f;  // Increased for better feel
```

You can see:
- ✅ Exactly what changed (MoveSpeed increased)
- ✅ Who changed it (Git blame)
- ✅ Why (commit message + comment)
- ✅ Easy to review (GitHub PR with inline comments)

✅ **Merge conflicts are manageable**
- Git shows exactly which lines conflict
- Use standard merge tools (GitKraken, VSCode, etc.)
- Resolve conflicts like any code file

---

## Real-World Example: Adding a New Enemy Type

### Blueprint Approach

**Steps:**

1. Duplicate BP_Enemy → BP_EnemyVariant
2. Open BP_EnemyVariant
3. Find MaxHealth variable → change default value
4. Find ScoreValue variable → change default value
5. Find VerticalSpeed variable → change default value
6. Find HorizontalAmplitude variable → change default value
7. Find FireInterval variable → change default value
8. Find BulletsPerBurst variable → change default value
9. Compile
10. Find MeshComp in Components panel
11. Assign different mesh in Details panel
12. Find material slot → assign different material
13. Save

**Time:** ~8-10 minutes per variant

If you need 4 enemy types: **~35 minutes**

### Code Approach

**Steps:**

1. Create child Blueprint from STGEnemy: BP_EnemyVariant
2. Open BP_EnemyVariant
3. In Class Defaults panel, change visible C++ properties:
   - MaxHealth: 24 (was 12)
   - ScoreValue: 100 (was 50)
   - VerticalSpeed: 300 (was 220)
   - FireInterval: 0.2 (was 0.35)
4. Assign different mesh
5. Assign different material
6. Done

**Time:** ~2 minutes per variant

If you need 4 enemy types: **~8 minutes**

**OR** define variants in C++ enum and configure in constructor:

```cpp
// In STGEnemy.h:
UENUM(BlueprintType)
enum class EEnemyType : uint8
{
    Basic,
    Fast,
    Tank,
    Boss
};

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy")
EEnemyType Type = EEnemyType::Basic;

// In STGEnemy.cpp constructor:
void ASTGEnemy::ConfigureStats()
{
    switch (Type)
    {
        case EEnemyType::Basic:
            MaxHealth = 12;
            ScoreValue = 50;
            VerticalSpeed = 220.0f;
            FireInterval = 0.35f;
            break;
        case EEnemyType::Fast:
            MaxHealth = 6;
            ScoreValue = 75;
            VerticalSpeed = 400.0f;
            FireInterval = 0.2f;
            break;
        case EEnemyType::Tank:
            MaxHealth = 30;
            ScoreValue = 150;
            VerticalSpeed = 120.0f;
            FireInterval = 0.5f;
            break;
        case EEnemyType::Boss:
            MaxHealth = 100;
            ScoreValue = 500;
            VerticalSpeed = 80.0f;
            FireInterval = 0.15f;
            break;
    }
}
```

Now you can:
- Create ONE Blueprint that inherits from STGEnemy
- Change the "Type" dropdown in editor
- All stats automatically configured!

**Time:** ~30 seconds to change dropdown per variant

---

## Summary: Time Investment

### Full Bullet Hell Game Implementation

| Task | Blueprint | Code-First | Time Saved |
|------|-----------|------------|------------|
| Player (12 variables) | 15 min | 2 min | 13 min |
| Player logic (movement, fire) | 60 min | 15 min | 45 min |
| Bullet (5 variables) | 8 min | 1 min | 7 min |
| Bullet logic | 30 min | 10 min | 20 min |
| Enemy (15 variables) | 20 min | 2 min | 18 min |
| Enemy logic | 90 min | 25 min | 65 min |
| Enemy variants (×4) | 35 min | 8 min | 27 min |
| Game Mode (8 variables) | 12 min | 2 min | 10 min |
| Game Mode logic | 45 min | 15 min | 30 min |
| Spawning system | 40 min | 12 min | 28 min |
| **TOTAL** | **~6-8 hours** | **~2-3 hours** | **~4-5 hours saved!** |

### One-Time Learning Investment

- **Blueprint tutorial:** ~2 hours to learn the editor UI
- **C++ tutorial:** ~4 hours to learn C++ basics

**BUT:** After the initial learning, C++ is **3x faster** for every project going forward!

---

## Recommended Workflow

### 🎯 Best Practice: Hybrid Approach

1. **Define all logic and variables in C++**
   - All game mechanics
   - All stats, speeds, health values
   - All algorithms (movement, firing, spawning)

2. **Use Blueprints only for visual assets**
   - Assign meshes/sprites
   - Set material colors
   - Configure particle effects
   - Place sound effects

**Example:**

```cpp
// STGEnemy.h - all logic in C++
class ASTGEnemy : public AActor
{
    UPROPERTY(EditAnywhere, Category = "Stats")
    int32 MaxHealth = 12;
    
    UPROPERTY(EditAnywhere, Category = "Stats")
    float VerticalSpeed = 220.0f;
    
    void Fire(); // Implemented in C++
    void UpdateMovement(float DeltaTime); // Implemented in C++
};
```

Then in Blueprint `BP_Enemy` (child of ASTGEnemy):
- Inherits all C++ variables and logic
- Only sets: Mesh, Material, Color
- Can still override C++ functions in Blueprint if needed

**Best of both worlds:**
- ✅ Fast development (C++ for logic)
- ✅ Easy asset management (Blueprint for visuals)
- ✅ Version control friendly (most changes are in C++)
- ✅ Designer-friendly (non-programmers can tweak visuals)

---

## Migration Path

### If You've Already Started with Blueprints

Don't worry! You can migrate gradually:

#### Option 1: Reparent Existing Blueprints

1. Create C++ class (e.g., `STGPawn`)
2. Compile
3. Open existing Blueprint (e.g., `BP_Player`)
4. **File → Reparent Blueprint**
5. Select your C++ class
6. Blueprint now inherits from C++!
7. Delete duplicate variables (they're now in C++)
8. Keep only visual asset assignments

#### Option 2: Hybrid Migration

1. Keep Blueprints for now
2. For new features, use C++
3. Gradually move logic to C++ over time
4. Eventually Blueprints become thin wrappers

#### Option 3: Fresh Start with Code-First

1. Follow [Code-First Tutorial](code-first-approach.md)
2. Reference your existing Blueprint logic
3. Reimplement in C++ (faster than original creation!)
4. Create new minimal Blueprints that inherit from C++

---

## Conclusion

### When Blueprint-Heavy Makes Sense

- ✅ Learning Unreal for the first time (visual learning)
- ✅ Solo project, no version control needed
- ✅ Rapid prototyping (test idea in 30 minutes)
- ✅ Heavy use of animation state machines
- ✅ Level design and visual scripting

### When Code-First Makes Sense

- ✅ **Multiple variables to configure** (the pain you described!)
- ✅ **Team project** (version control is critical)
- ✅ **Medium to large game** (6+ hours of development)
- ✅ **Complex game logic** (algorithms, math, loops)
- ✅ **Want to reuse code** across projects
- ✅ **Want IDE tools** (refactoring, autocomplete, debugging)

### For This Bullet Hell Game Specifically

**Code-First is strongly recommended** because:

1. ✅ **Tons of variables** (50+ across all classes)
2. ✅ **Mathematical logic** (radial bursts, sine waves, interpolation)
3. ✅ **Repeated patterns** (firing, movement, spawning)
4. ✅ **Multiple similar classes** (enemy variants)
5. ✅ **Likely to iterate** (balancing, tweaking values)

---

## Get Started

Ready to try the code-first approach?

**→ [Start the Code-First C++ Tutorial](code-first-approach.md)**

Or continue with the Blueprint tutorial:

**→ [Blueprint Tutorial - Part 1](part-1-project-setup.md)**

---

[Back to Index](README.md) | [Code-First Tutorial](code-first-approach.md)
