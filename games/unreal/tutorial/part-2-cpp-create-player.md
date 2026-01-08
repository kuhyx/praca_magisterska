# Part 2 (C++): Create the Player

[← Previous: Part 1 (C++) - Project Setup](part-1-cpp-project-setup.md) | [Back to Index](README.md) | [Next: Part 3 (C++) - Create the Bullet →](part-3-cpp-create-bullet.md)

---

## Overview

In this part, we'll create the player ship as a **C++ class** called `ASTGPawn`. 

**Time comparison:**
- Blueprint approach (Part 2): ~60 minutes (12 variables via UI + Blueprint nodes)
- C++ approach (this part): ~15 minutes (copy-paste code)

---

## Step 2.1: Create STGPawn C++ Class

### In Unreal Editor:

1. Go to **Tools → New C++ Class** (top menu bar)
2. In the "Choose Parent Class" window:
   - Click **"Pawn"** (NOT Character - we want simple 2D control)
   - Click **"Next"**

3. In the "Name Your New Actor" window:
   - **Name:** `STGPawn`
   - **Path:** Should be `Source/BulletHellGame/` (default)
   - Click **"Create Class"**

### What Happens Next:

1. Unreal generates `STGPawn.h` and `STGPawn.cpp`
2. Your IDE opens with the new files
3. Project compiles automatically (~30-60 seconds)
4. Unreal Editor refreshes

> **💡 TIP:** If compilation fails, check the Output Log in Unreal Editor

---

## Step 2.2: Define Player Variables in STGPawn.h

Now comes the magic! Instead of clicking UI 60+ times, we'll **copy-paste** all variables at once.

### Open STGPawn.h in your IDE

Find the class definition (should look like this):

```cpp
UCLASS()
class BULLETHELLGAME_API ASTGPawn : public APawn
{
    GENERATED_BODY()

public:
    ASTGPawn();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
};
```

### Replace the entire class with this:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "STGPawn.generated.h"

// Forward declarations
class UCameraComponent;
class USpringArmComponent;
class UStaticMeshComponent;
class UBoxComponent;

UCLASS()
class BULLETHELLGAME_API ASTGPawn : public APawn
{
    GENERATED_BODY()

public:
    ASTGPawn();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    // ===== COMPONENTS =====
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStaticMeshComponent* ShipMesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    USpringArmComponent* SpringArm;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UCameraComponent* Camera;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UBoxComponent* Hitbox;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStaticMeshComponent* HitboxIndicator;

    // ===== MOVEMENT & BOUNDARIES =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float MoveSpeed = 750.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    FVector2D BoundsMin = FVector2D(-850.0f, -450.0f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    FVector2D BoundsMax = FVector2D(850.0f, 450.0f);

    // ===== FIRING =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireInterval = 0.08f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BulletSpeed = 2200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 VolleySize = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VolleySpread = 12.0f;

    // ===== LIVES & SCORE =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxLives = 3;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentLives = 3;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 Score = 0;

    // ===== SPECIAL ABILITY =====
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    bool bSpecialUsed = false;

    // ===== INPUT FUNCTIONS =====
    void MoveForward(float Value);
    void MoveRight(float Value);
    void StartFire();
    void StopFire();
    void UseSpecial();

    // ===== GAME LOGIC =====
    void FireShot();
    void TakeHit(int32 Damage);
    void HandleDeath();
    void AddScore(int32 Points);

private:
    FTimerHandle TimerHandle_Fire;
    bool bIsFiring = false;
    FVector MovementInput;
    float FireTimer = 0.0f;
};
```

### What Just Happened?

You just defined **12 gameplay variables + 5 components** with default values in ~30 seconds (copy-paste time)!

In the Blueprint tutorial, this would require:
- 12 variables × 5 clicks each = 60 clicks
- ~15 minutes of manual work
- High chance of typos

**Time saved: 14.5 minutes** ⚡

---

## Step 2.3: Implement STGPawn Constructor

### Open STGPawn.cpp in your IDE

Replace the file content with:

```cpp
#include "STGPawn.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"

ASTGPawn::ASTGPawn()
{
    PrimaryActorTick.bCanEverTick = true;

    // Root component
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

    // Ship mesh - cone shape pointing upward
    ShipMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ShipMesh"));
    ShipMesh->SetupAttachment(RootComponent);
    ShipMesh->SetCollisionProfileName("NoCollision");
    
    // Load cone mesh from engine
    static ConstructorHelpers::FObjectFinder<UStaticMesh> ConeMesh(TEXT("/Engine/BasicShapes/Cone"));
    if (ConeMesh.Succeeded())
    {
        ShipMesh->SetStaticMesh(ConeMesh.Object);
        ShipMesh->SetRelativeScale3D(FVector(0.5f, 0.5f, 0.7f));
        ShipMesh->SetRelativeRotation(FRotator(90.f, 0.f, 0.f)); // Point forward
    }

    // Hitbox - small for bullet-hell precision
    Hitbox = CreateDefaultSubobject<UBoxComponent>(TEXT("Hitbox"));
    Hitbox->SetupAttachment(RootComponent);
    Hitbox->SetBoxExtent(FVector(25.f, 25.f, 10.f));
    Hitbox->SetCollisionProfileName("OverlapAllDynamic");
    Hitbox->SetGenerateOverlapEvents(true);

    // Visual hitbox indicator (small sphere)
    HitboxIndicator = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("HitboxIndicator"));
    HitboxIndicator->SetupAttachment(RootComponent);
    HitboxIndicator->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    
    static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
    if (SphereMesh.Succeeded())
    {
        HitboxIndicator->SetStaticMesh(SphereMesh.Object);
        HitboxIndicator->SetRelativeScale3D(FVector(0.05f, 0.05f, 0.05f));
    }

    // Camera setup for top-down view
    SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->SetRelativeRotation(FRotator(-90.f, 0.f, 0.f)); // Top-down
    SpringArm->TargetArmLength = 1200.f;
    SpringArm->bDoCollisionTest = false;
    SpringArm->bInheritPitch = false;
    SpringArm->bInheritRoll = false;
    SpringArm->bInheritYaw = false;

    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    Camera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);
}

void ASTGPawn::BeginPlay()
{
    Super::BeginPlay();
    CurrentLives = MaxLives;
}

void ASTGPawn::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    // Movement with bounds clamping
    if (!MovementInput.IsZero())
    {
        FVector NewLocation = GetActorLocation();
        FVector Normalized = MovementInput.GetSafeNormal();
        NewLocation += Normalized * MoveSpeed * DeltaTime;

        // Clamp to bounds
        NewLocation.X = FMath::Clamp(NewLocation.X, BoundsMin.X, BoundsMax.X);
        NewLocation.Y = FMath::Clamp(NewLocation.Y, BoundsMin.Y, BoundsMax.Y);

        SetActorLocation(NewLocation);
    }

    // Auto-fire when holding fire button
    if (bIsFiring)
    {
        FireTimer -= DeltaTime;
        if (FireTimer <= 0.0f)
        {
            FireShot();
            FireTimer = FireInterval;
        }
    }
}

void ASTGPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    // Bind movement axes
    PlayerInputComponent->BindAxis("MoveForward", this, &ASTGPawn::MoveForward);
    PlayerInputComponent->BindAxis("MoveRight", this, &ASTGPawn::MoveRight);

    // Bind actions
    PlayerInputComponent->BindAction("Fire", IE_Pressed, this, &ASTGPawn::StartFire);
    PlayerInputComponent->BindAction("Fire", IE_Released, this, &ASTGPawn::StopFire);
    PlayerInputComponent->BindAction("Special", IE_Pressed, this, &ASTGPawn::UseSpecial);
}

void ASTGPawn::MoveForward(float Value)
{
    MovementInput.X = Value;
}

void ASTGPawn::MoveRight(float Value)
{
    MovementInput.Y = Value;
}

void ASTGPawn::StartFire()
{
    bIsFiring = true;
    FireTimer = 0.0f; // Fire immediately
}

void ASTGPawn::StopFire()
{
    bIsFiring = false;
}

void ASTGPawn::FireShot()
{
    // Will implement in Part 3 when we create bullets
    UE_LOG(LogTemp, Warning, TEXT("FIRE!"));
}

void ASTGPawn::UseSpecial()
{
    if (!bSpecialUsed)
    {
        bSpecialUsed = true;
        UE_LOG(LogTemp, Warning, TEXT("SPECIAL ABILITY ACTIVATED!"));
        // Will implement enemy/bullet destruction in Part 4
    }
}

void ASTGPawn::TakeHit(int32 Damage)
{
    CurrentLives = FMath::Clamp(CurrentLives - Damage, 0, MaxLives);
    
    if (CurrentLives <= 0)
    {
        HandleDeath();
    }
}

void ASTGPawn::HandleDeath()
{
    SetActorHiddenInGame(true);
    // Will notify GameMode in Part 6
}

void ASTGPawn::AddScore(int32 Points)
{
    Score += Points;
}
```

---

## Step 2.4: Compile the Code

### In Unreal Editor:

1. Click **"Compile"** button (bottom right, or `Ctrl+Alt+F11`)
2. Wait for compilation (~30-60 seconds)
3. Check for errors in Output Log

OR

### In your IDE:

1. Build the project (`Ctrl+Shift+B` in Visual Studio, or `Ctrl+F9` in Rider)
2. Wait for build to finish
3. Unreal Editor will hot-reload automatically

### Expected Result:

- ✅ Compilation succeeds
- ✅ "C++ Classes" folder in Content Browser now shows `STGPawn`
- ✅ You can right-click STGPawn → "Create Blueprint Class based on STGPawn"

---

## Step 2.5: Configure Input Mappings

This step is the same as Blueprint tutorial - we need to configure keyboard inputs in Project Settings.

1. **Edit → Project Settings**
2. **Engine → Input**
3. **Axis Mappings** → Click "+" to add:
   - `MoveForward`: W = 1.0, S = -1.0
   - `MoveRight`: D = 1.0, A = -1.0
4. **Action Mappings** → Click "+" to add:
   - `Fire`: Space Bar, Left Mouse Button
   - `Special`: X, Right Mouse Button
5. Close Project Settings

---

## Step 2.6: Create Blueprint Child (for Visual Assets)

Now we create a **minimal Blueprint** that inherits from our C++ class. This Blueprint is ONLY for visual assets!

1. In Content Browser, navigate to `Content → Blueprints`
2. Right-click → **Blueprint Class**
3. In "Pick Parent Class" window:
   - Click "All Classes" dropdown at top
   - Search for `STGPawn`
   - Select it
   - Click "Select"
4. Name it: `BP_Player`
5. Double-click to open

### In the Blueprint Editor:

**Components (Left Panel):**
- You'll see all components we created in C++ (ShipMesh, Hitbox, Camera, etc.)
- NO NEED to add them manually - they're already there from C++!

**Variables (My Blueprint Panel):**
- You'll see all 12 variables we defined in C++ (MoveSpeed, BoundsMin, etc.)
- NO NEED to create them - they're already there from C++!
- You can see their default values (750.0, etc.) - all from C++!

**What to do in Blueprint:**
- NOTHING for now! All logic is in C++
- In Part 9, we'll assign visual meshes/materials here

### Compile and Save BP_Player

---

## Step 2.7: Test the Player

1. Drag `BP_Player` from Content Browser into the level viewport
2. Position it near the center (coordinates around X=0, Y=0, Z=0)
3. Press **Play** (`Alt+P`)

### Expected Result

**In Play Mode Window:**
- You see the cone/cube player ship from above (top-down view)
- Ship is positioned at center of screen
- Background is the default gray/blue Unreal grid
- Camera follows the player from above

**When pressing WASD keys:**
- **W** - Ship moves upward on screen (toward top)
- **S** - Ship moves downward on screen (toward bottom)
- **A** - Ship moves left
- **D** - Ship moves right
- Movement stops immediately when you release keys (no sliding)
- Ship stops at screen edges (cannot move outside bounds)

**When pressing Z or Space:**
- You see "FIRE!" message appear in top-left corner of screen (yellow text)
- Message appears repeatedly while holding the button
- No bullets yet (we'll add those after creating bullet class)

**When pressing X:**
- "SPECIAL ABILITY ACTIVATED!" appears once in top-left corner
- Pressing X again does nothing (ability used up)

**Visual Check:**
- Ship model is visible (cone or cube shape)
- Ship rotates/faces the direction of movement
- No errors in Output Log
- Frame rate counter shows stable FPS (if enabled)

**To exit Play mode:** Press `Esc` or click the "Stop" button in the toolbar

---

## Comparison: What We Just Did

### Blueprint Approach (Part 2):

1. Create BP_Player Blueprint ✅
2. Add 5 components manually (clicking, dragging)
3. Add 12 variables one-by-one (click +, type name, select type, compile, set value) × 12 = **15 minutes**
4. Create Blueprint nodes for movement logic (~30 nodes, connecting wires)
5. Create Blueprint nodes for firing logic (~20 nodes)
6. Configure input in Project Settings
7. **Total: ~60 minutes**

### C++ Approach (This Part):

1. Create STGPawn C++ class ✅
2. Copy-paste header file with all variables **30 seconds**
3. Copy-paste implementation file
4. Compile
5. Create BP_Player (inherits everything from C++)
6. Configure input in Project Settings
7. **Total: ~15 minutes**

**Time saved: 45 minutes** ⚡⚡⚡

---

## What's Next?

In Part 3, we'll create the bullet class in C++. You'll see how defining bullet behavior in code is much cleaner than Blueprint nodes.

---

[← Previous: Part 1 (C++) - Project Setup](part-1-cpp-project-setup.md) | [Back to Index](README.md) | [Next: Part 3 (C++) - Create the Bullet →](part-3-cpp-create-bullet.md)
