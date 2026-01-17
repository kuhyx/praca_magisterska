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

### In Unreal Editor

1. Go to **Tools → New C++ Class** (top menu bar)
2. In the "Choose Parent Class" window:
   - Click **"Pawn"** (NOT Character - we want simple 2D control)
   - Click **"Next"**

3. In the "Name Your New Actor" window:
   - **Name:** `STGPawn`
   - **Path:** Should be `Source/BulletHellGame/` (default)
   - Click **"Create Class"**

### What Happens Next

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
class YOURPROJECTNAME_API ASTGPawn : public APawn
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

### Replace the entire file with this

> **⚠️ IMPORTANT:** Replace `YOURPROJECTNAME_API` with your actual project's API macro (e.g., `BULLETHELLCPP_API` if your project is named "BulletHellCPP"). The macro name is your project name in UPPERCASE followed by `_API`.

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "InputActionValue.h"
#include "STGPawn.generated.h"

// Forward declarations
class UCameraComponent;
class USpringArmComponent;
class UStaticMeshComponent;
class UBoxComponent;
class UInputMappingContext;
class UInputAction;

UCLASS()
class YOURPROJECTNAME_API ASTGPawn : public APawn
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

    // ===== ENHANCED INPUT =====
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    UInputMappingContext* DefaultMappingContext;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    UInputAction* MoveAction;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    UInputAction* FireAction;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    UInputAction* SpecialAction;

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

    // ===== INPUT FUNCTIONS (Enhanced Input) =====
    void Move(const FInputActionValue& Value);
    void StartFire(const FInputActionValue& Value);
    void StopFire(const FInputActionValue& Value);
    void UseSpecial(const FInputActionValue& Value);

    // ===== GAME LOGIC =====
    void FireShot();
    void TakeHit(int32 Damage);
    void HandleDeath();
    void AddScore(int32 Points);

private:
    FTimerHandle TimerHandle_Fire;
    bool bIsFiring = false;
    FVector2D MovementInput;
    float FireTimer = 0.0f;
};
```

### What Just Happened?

You just defined **12 gameplay variables + 5 components + 4 input actions** with default values in ~30 seconds (copy-paste time)!

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
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"

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

    // Add Input Mapping Context
    if (APlayerController* PlayerController = Cast<APlayerController>(Controller))
    {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
        {
            Subsystem->AddMappingContext(DefaultMappingContext, 0);
        }
    }
}

void ASTGPawn::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    // Movement with bounds clamping
    if (!MovementInput.IsZero())
    {
        FVector NewLocation = GetActorLocation();
        NewLocation.X += MovementInput.Y * MoveSpeed * DeltaTime; // Forward/Back
        NewLocation.Y += MovementInput.X * MoveSpeed * DeltaTime; // Left/Right

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

    // Set up Enhanced Input bindings
    if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        // Movement
        EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ASTGPawn::Move);
        EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Completed, this, &ASTGPawn::Move);

        // Fire
        EnhancedInputComponent->BindAction(FireAction, ETriggerEvent::Started, this, &ASTGPawn::StartFire);
        EnhancedInputComponent->BindAction(FireAction, ETriggerEvent::Completed, this, &ASTGPawn::StopFire);

        // Special
        EnhancedInputComponent->BindAction(SpecialAction, ETriggerEvent::Started, this, &ASTGPawn::UseSpecial);
    }
}

void ASTGPawn::Move(const FInputActionValue& Value)
{
    MovementInput = Value.Get<FVector2D>();
}

void ASTGPawn::StartFire(const FInputActionValue& Value)
{
    bIsFiring = true;
    FireTimer = 0.0f; // Fire immediately
}

void ASTGPawn::StopFire(const FInputActionValue& Value)
{
    bIsFiring = false;
}

void ASTGPawn::FireShot()
{
    // Will implement in Part 3 when we create bullets
    UE_LOG(LogTemp, Warning, TEXT("FIRE!"));
}

void ASTGPawn::UseSpecial(const FInputActionValue& Value)
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

### In Unreal Editor

1. Click **"Compile"** button (bottom right of the viewport)
2. Wait for compilation (~30-60 seconds)
3. Check for errors in Output Log

OR

### In your IDE

1. Build the project (`Ctrl+Shift+B` in Visual Studio, or `Ctrl+F9` in Rider)
2. Wait for build to finish
3. Unreal Editor will hot-reload automatically

### Expected Result

- ✅ Compilation succeeds
- ✅ "C++ Classes" folder in Content Browser now shows `STGPawn`
- ✅ You can right-click STGPawn → "Create Blueprint Class based on STGPawn"

---

## Step 2.5: Create Enhanced Input Assets

Unlike the deprecated Axis/Action Mappings, Enhanced Input uses **data assets** that you create in the Content Browser.

### Create Input Actions

1. In Content Browser, right-click → **Input → Input Action**
2. Name it: `IA_Move`
3. Double-click to open, set **Value Type** to `Axis2D (Vector2D)`
4. Save and close

Repeat for:

- `IA_Fire` (Value Type: `Digital (bool)`)
- `IA_Special` (Value Type: `Digital (bool)`)

### Create Input Mapping Context

1. In Content Browser, right-click → **Input → Input Mapping Context**
2. Name it: `IMC_Player`
3. Double-click to open
4. Click "+" to add mappings:

**For IA_Move:**

- Add `IA_Move`
- Click "+" next to it to add keys:
  - **W** → Modifiers: Add "Swizzle Input Axis Values" (YXZ)
  - **S** → Modifiers: Add "Swizzle Input Axis Values" (YXZ), then "Negate"
  - **A** → Modifiers: Add "Negate"
  - **D** → (no modifiers needed)

**For IA_Fire:**

- Add `IA_Fire`
- Add keys: **Space Bar**, **Left Mouse Button**

**For IA_Special:**

- Add `IA_Special`
- Add keys: **X**, **Right Mouse Button**

5. Save the Input Mapping Context

---

## Step 2.6: Create Blueprint Child (for Visual Assets)

Now we create a **minimal Blueprint** that inherits from our C++ class. This Blueprint is ONLY for visual assets and input asset references!

1. In Content Browser, navigate to `Content → Blueprints`
2. Right-click → **Blueprint Class**
3. In "Pick Parent Class" window:
   - Click "All Classes" dropdown at top
   - Search for `STGPawn`
   - Select it
   - Click "Select"
4. Name it: `BP_Player`
5. Double-click to open

### In the Blueprint Editor

**Components (Left Panel):**

- You'll see all components we created in C++ (ShipMesh, Hitbox, Camera, etc.)
- NO NEED to add them manually - they're already there from C++!

**Assigning Input Assets (Class Defaults):**

1. Click the **"Class Defaults"** button in the toolbar at the top of the Blueprint Editor (or press `Alt+Enter`)
2. In the Details panel on the right, scroll down or search for **"Input"**
3. You should see our custom Input properties (NOT the built-in Actor input settings):
   - **Default Mapping Context** → Assign `IMC_Player`
   - **Move Action** → Assign `IA_Move`
   - **Fire Action** → Assign `IA_Fire`
   - **Special Action** → Assign `IA_Special`

> **⚠️ NOTE:** If you only see "Block Input", "Auto Receive Input", and "Input Priority" - those are built-in Actor settings. Make sure you clicked **"Class Defaults"** button in the toolbar, and look for our custom properties labeled "Default Mapping Context", "Move Action", etc. They should be in a category called "Input" that we defined in C++.

**Variables (My Blueprint Panel):**

- You'll see all 12 variables we defined in C++ (MoveSpeed, BoundsMin, etc.)
- NO NEED to create them - they're already there from C++!
- You can see their default values (750.0, etc.) - all from C++!

**What to do in Blueprint:**

- Assign the input assets (as shown above)
- In Part 9, we'll assign visual meshes/materials here

### Compile and Save BP_Player

---

## Step 2.7: Test the Player

1. Drag `BP_Player` from Content Browser into the level viewport
2. Position it near the center (coordinates around X=0, Y=0, Z=0)
3. **Set Auto Possess Player:**
   - With `BP_Player` selected in the viewport, look at the **Details** panel on the right
   - Scroll down to the **Pawn** section (or search for "Auto Possess")
   - Find **Auto Possess Player** and set it to **"Player 0"**
4. Press **Play** (`Alt+P`)

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
- Ship stops at the green debug border (the play area bounds)
- You can toggle this border off in BP_Player → Details → Debug → "Show Debug Bounds"

**When pressing Space:**

- You see "FIRE!" message appear in top-left corner of screen (yellow text)
- Message appears repeatedly while holding the button
- No bullets yet (we'll add those after creating bullet class)

**When pressing X:**

- "SPECIAL ABILITY ACTIVATED!" appears in top-left corner (cyan text)
- Pressing X again does nothing (ability used up)

**Visual Check:**

- Ship model is visible (cone or cube shape)
- No errors in Output Log
- Frame rate counter shows stable FPS (if enabled)

**To exit Play mode:** Press `Esc` or click the "Stop" button in the toolbar

---

## Comparison: What We Just Did

### Blueprint Approach (Part 2)

1. Create BP_Player Blueprint ✅
2. Add 5 components manually (clicking, dragging)
3. Add 12 variables one-by-one (click +, type name, select type, compile, set value) × 12 = **15 minutes**
4. Create Blueprint nodes for movement logic (~30 nodes, connecting wires)
5. Create Blueprint nodes for firing logic (~20 nodes)
6. Create Enhanced Input assets
7. **Total: ~60 minutes**

### C++ Approach (This Part)

1. Create STGPawn C++ class ✅
2. Copy-paste header file with all variables **30 seconds**
3. Copy-paste implementation file
4. Compile
5. Create Enhanced Input assets (same in both approaches)
6. Create BP_Player (inherits everything from C++)
7. **Total: ~15 minutes**

**Time saved: 45 minutes** ⚡⚡⚡

---

## What's Next?

In Part 3, we'll create the bullet class in C++. You'll see how defining bullet behavior in code is much cleaner than Blueprint nodes.

---

[← Previous: Part 1 (C++) - Project Setup](part-1-cpp-project-setup.md) | [Back to Index](README.md) | [Next: Part 3 (C++) - Create the Bullet →](part-3-cpp-create-bullet.md)
