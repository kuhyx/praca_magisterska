# Code-First Approach: Building the Bullet Hell Game in C++

[Back to Index](README.md)

---

## Why Use the Code-First Approach?

The Blueprint-heavy tutorial requires **extensive manual UI work** - clicking through dozens of variable properties, typing values one by one, and repeating the process for every component. This is:

- **Time-consuming**: Each variable requires 5-10 clicks to configure
- **Error-prone**: Easy to mistype values or select wrong types
- **Hard to replicate**: Difficult to copy settings between projects
- **Poor for version control**: Blueprint files are binary and hard to diff/merge

**The code-first approach solves these problems** by defining all game logic, variables, and configurations in C++ header and source files. You can:

✅ **Copy-paste entire variable blocks** instead of typing one-by-one  
✅ **Version control with readable diffs** using standard Git tools  
✅ **Refactor with IDE tools** (rename, find references, etc.)  
✅ **Compile-time type checking** prevents common mistakes  
✅ **Create Blueprints that inherit from C++** classes for visual-only assets

---

## Overview: Implementation Strategy

We will create **C++ base classes** for all game logic:

1. **ASTGPawn** - Player ship with movement, firing, lives
2. **ASTGProjectile** - Bullets (player and enemy)
3. **ASTGEnemy** - Enemy ships with AI and firing patterns
4. **ASTGGameMode** - Game rules, spawning, timer
5. **ASTGHUD** - UI display for score, lives, timer

Then create **minimal Blueprint classes** that inherit from these C++ classes, used only for:
- Assigning visual meshes/sprites
- Setting material colors
- Configuring asset references (sound effects, particle effects)

---

## Part 1: Project Setup

### Step 1.1: Create C++ Project in Unreal

1. Open Unreal Engine 5
2. Create **New Project**
3. Select **Games → Blank** template
4. **Project Defaults**:
   - Project Type: **C++** (NOT Blueprint!)
   - Target Platform: **Desktop**
   - Quality Preset: **Scalable**
   - Starter Content: **No Starter Content**
5. Name: `BulletHellGame`
6. Click **Create**

Unreal will:
- Generate C++ project structure
- Open Visual Studio / VS Code / Rider
- Compile initial project code (~2-5 minutes)

### Step 1.2: Verify Project Structure

Your project folder should contain:

```
BulletHellGame/
├── BulletHellGame.uproject       # Project file
├── Source/                       # C++ source code
│   └── BulletHellGame/
│       ├── BulletHellGame.h
│       ├── BulletHellGame.cpp
│       ├── BulletHellGame.Build.cs
│       └── BulletHellGameGameMode.h/cpp  # Auto-generated
├── Content/                      # Assets (minimal Blueprints here)
├── Config/                       # Project settings
└── Intermediate/                 # Build artifacts (gitignore this)
```

### Step 1.3: Configure .gitignore

Add to `.gitignore`:

```gitignore
# Unreal Engine
Binaries/
DerivedDataCache/
Intermediate/
Saved/
*.sln
*.suo
*.opensdf
*.sdf
*.VC.db
*.VC.opendb
```

---

## Part 2: Create the Player (C++ Implementation)

### Step 2.1: Create STGPawn Header

Create `Source/BulletHellGame/STGPawn.h`:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "STGPawn.generated.h"

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

    // ===== GAMEPLAY VARIABLES (All in one place - easy copy/paste!) =====
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
    int32 MaxLives = 3;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentLives = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 VolleySize = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VolleySpread = 12.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    bool bSpecialUsed = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 Score = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireRate = 0.08f;

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

**Key advantages of this approach:**

1. **All 12 player variables defined in ~12 lines** (vs 60+ clicks in Blueprint UI)
2. **Default values inline** (`= 750.0f`) - no need to set after compile
3. **Copy-paste friendly** - duplicate variables easily
4. **Version control friendly** - see exact changes in Git diff
5. **Type-safe** - compiler catches type mismatches

### Step 2.2: Create STGPawn Implementation

Create `Source/BulletHellGame/STGPawn.cpp`:

```cpp
#include "STGPawn.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Kismet/GameplayStatics.h"
#include "STGProjectile.h"

ASTGPawn::ASTGPawn()
{
    PrimaryActorTick.bCanEverTick = true;

    // Root component
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

    // Ship mesh - cone shape pointing upward
    ShipMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ShipMesh"));
    ShipMesh->SetupAttachment(RootComponent);
    ShipMesh->SetCollisionProfileName("NoCollision");
    
    // Load cone mesh
    static ConstructorHelpers::FObjectFinder<UStaticMesh> ConeMesh(TEXT("/Engine/BasicShapes/Cone"));
    if (ConeMesh.Succeeded())
    {
        ShipMesh->SetStaticMesh(ConeMesh.Object);
        ShipMesh->SetRelativeScale3D(FVector(0.5f, 0.5f, 0.7f));
        ShipMesh->SetRelativeRotation(FRotator(90.f, 0.f, 0.f));
    }

    // Hitbox - tiny for bullet-hell precision
    Hitbox = CreateDefaultSubobject<UBoxComponent>(TEXT("Hitbox"));
    Hitbox->SetupAttachment(RootComponent);
    Hitbox->SetBoxExtent(FVector(25.f, 25.f, 10.f));
    Hitbox->SetCollisionProfileName("OverlapAllDynamic");
    Hitbox->SetGenerateOverlapEvents(true);

    // Visual hitbox indicator
    HitboxIndicator = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("HitboxIndicator"));
    HitboxIndicator->SetupAttachment(RootComponent);
    HitboxIndicator->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    
    static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
    if (SphereMesh.Succeeded())
    {
        HitboxIndicator->SetStaticMesh(SphereMesh.Object);
        HitboxIndicator->SetRelativeScale3D(FVector(0.05f, 0.05f, 0.05f));
    }

    // Camera setup
    SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->SetRelativeRotation(FRotator(-90.f, 0.f, 0.f)); // Top-down view
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

    // Movement
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

    // Auto-fire
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
    // Spawn volley of bullets
    for (int32 i = 0; i < VolleySize; i++)
    {
        FVector SpawnLocation = GetActorLocation() + FVector(0.f, 0.f, 50.f);
        FRotator SpawnRotation = FRotator(90.f, 0.f, 0.f);

        // Spread calculation
        float Angle = VolleySpread * (i - (VolleySize - 1) / 2.0f);
        SpawnRotation.Yaw += Angle;

        // Spawn bullet (will create this class next)
        UWorld* World = GetWorld();
        if (World)
        {
            ASTGProjectile* Bullet = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), SpawnLocation, SpawnRotation);
            if (Bullet)
            {
                Bullet->bIsPlayerBullet = true;
                Bullet->SetSpeed(BulletSpeed);
                Bullet->SetBulletColor(FLinearColor::Green);
            }
        }
    }
}

void ASTGPawn::UseSpecial()
{
    if (!bSpecialUsed)
    {
        bSpecialUsed = true;
        
        // Destroy all enemies and bullets on screen
        TArray<AActor*> FoundEnemies;
        UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGEnemy::StaticClass(), FoundEnemies);
        for (AActor* Enemy : FoundEnemies)
        {
            Enemy->Destroy();
        }

        TArray<AActor*> FoundBullets;
        UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGProjectile::StaticClass(), FoundBullets);
        for (AActor* Bullet : FoundBullets)
        {
            ASTGProjectile* Projectile = Cast<ASTGProjectile>(Bullet);
            if (Projectile && !Projectile->bIsPlayerBullet)
            {
                Projectile->Destroy();
            }
        }
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
    
    // Notify GameMode
    ASTGGameMode* GameMode = Cast<ASTGGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
    if (GameMode)
    {
        GameMode->OnPlayerDied();
    }
}

void ASTGPawn::AddScore(int32 Points)
{
    Score += Points;
}
```

**Notice how much easier this is:**

- **Movement logic in ~10 lines** vs 30+ Blueprint nodes
- **Fire logic with volley calculation** - would be complex in Blueprints
- **Easy to copy patterns** between functions
- **IDE autocomplete** helps prevent typos

### Step 2.3: Configure Input Mappings

You still need to configure input in Project Settings (this can't be done in code):

1. **Edit → Project Settings**
2. **Engine → Input**
3. **Axis Mappings**:
   - `MoveForward`: W = 1.0, S = -1.0
   - `MoveRight`: D = 1.0, A = -1.0
4. **Action Mappings**:
   - `Fire`: Space, Left Mouse Button
   - `Special`: X, Right Mouse Button

**This is a one-time setup** - all other configuration is in code.

### Step 2.4: Compile and Test

1. **In Unreal Editor**: Click **Compile** button (or close editor)
2. **Build in IDE**: Build Solution / Compile Project
3. **Expected compile time**: ~30-60 seconds (vs instant in Blueprint, but you save hours on UI work)
4. **Open Unreal Editor** (if you closed it)
5. **Content Browser → C++ Classes → BulletHellGame** - you should see `STGPawn`

---

## Part 3: Create the Projectile (C++ Implementation)

### Step 3.1: Create STGProjectile Header

Create `Source/BulletHellGame/STGProjectile.h`:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGProjectile.generated.h"

class USphereComponent;
class UProjectileMovementComponent;
class UStaticMeshComponent;

UCLASS()
class BULLETHELLGAME_API ASTGProjectile : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGProjectile();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    // Components
    UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
    USphereComponent* CollisionComp;

    UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
    UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Movement)
    UProjectileMovementComponent* ProjectileMovement;

    // Variables (again, all in one place!)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    bool bIsPlayerBullet = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    float Damage = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    FLinearColor BulletColor = FLinearColor::Green;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    float Lifetime = 4.0f;

    // Functions
    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    void SetBulletColor(FLinearColor InColor);
    void SetSpeed(float InSpeed);

private:
    UMaterialInstanceDynamic* DynamicMaterial;
};
```

### Step 3.2: Create STGProjectile Implementation

Create `Source/BulletHellGame/STGProjectile.cpp`:

```cpp
#include "STGProjectile.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "STGEnemy.h"
#include "STGPawn.h"

ASTGProjectile::ASTGProjectile()
{
    PrimaryActorTick.bCanEverTick = true;

    // Collision sphere
    CollisionComp = CreateDefaultSubobject<USphereComponent>(TEXT("SphereComp"));
    CollisionComp->InitSphereRadius(5.0f);
    CollisionComp->SetCollisionProfileName("OverlapAllDynamic");
    CollisionComp->OnComponentBeginOverlap.AddDynamic(this, &ASTGProjectile::OnOverlapBegin);
    RootComponent = CollisionComp;

    // Visual mesh
    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
    MeshComp->SetupAttachment(CollisionComp);
    MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    
    static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
    if (SphereMesh.Succeeded())
    {
        MeshComp->SetStaticMesh(SphereMesh.Object);
        MeshComp->SetRelativeScale3D(FVector(0.1f, 0.1f, 0.1f));
    }

    // Projectile movement
    ProjectileMovement = CreateDefaultSubobject<UProjectileMovementComponent>(TEXT("ProjectileComp"));
    ProjectileMovement->UpdatedComponent = CollisionComp;
    ProjectileMovement->InitialSpeed = 1200.f;
    ProjectileMovement->MaxSpeed = 1200.f;
    ProjectileMovement->bRotationFollowsVelocity = true;
    ProjectileMovement->bShouldBounce = false;

    // Auto-destroy after lifetime
    InitialLifeSpan = Lifetime;
}

void ASTGProjectile::BeginPlay()
{
    Super::BeginPlay();

    // Create dynamic material
    if (MeshComp)
    {
        DynamicMaterial = MeshComp->CreateAndSetMaterialInstanceDynamic(0);
        if (DynamicMaterial)
        {
            DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), BulletColor);
            DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), BulletColor * 3.0f);
        }
    }
}

void ASTGProjectile::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void ASTGProjectile::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    if (OtherActor && OtherActor != this)
    {
        if (bIsPlayerBullet)
        {
            // Player bullet hits enemy
            ASTGEnemy* Enemy = Cast<ASTGEnemy>(OtherActor);
            if (Enemy)
            {
                Enemy->HandleDamage(Damage);
                Destroy();
            }
        }
        else
        {
            // Enemy bullet hits player
            ASTGPawn* Player = Cast<ASTGPawn>(OtherActor);
            if (Player)
            {
                Player->TakeHit(1);
                Destroy();
            }
        }
    }
}

void ASTGProjectile::SetBulletColor(FLinearColor InColor)
{
    BulletColor = InColor;
    if (DynamicMaterial)
    {
        DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), BulletColor);
        DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), BulletColor * 3.0f);
    }
}

void ASTGProjectile::SetSpeed(float InSpeed)
{
    if (ProjectileMovement)
    {
        ProjectileMovement->InitialSpeed = InSpeed;
        ProjectileMovement->MaxSpeed = InSpeed;
    }
}
```

---

## Part 4: Create the Enemy (C++ Implementation)

I'll provide the complete implementation - notice how **defining 15+ enemy variables takes ~15 lines of code** instead of 75+ clicks:

### Step 4.1: Create STGEnemy Header

Create `Source/BulletHellGame/STGEnemy.h`:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGEnemy.generated.h"

UCLASS()
class BULLETHELLGAME_API ASTGEnemy : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGEnemy();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    // Components
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UBoxComponent* CollisionComp;

    // Variables - all configurable in one place!
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxHealth = 12;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentHealth = 12;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 ScoreValue = 50;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VerticalSpeed = 220.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalAmplitude = 250.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalFrequency = 1.8f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float DespawnY = -750.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireInterval = 0.35f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 BulletsPerBurst = 20;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BurstSpread = 360.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletSpeed = 1000.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletLifetime = 6.0f;

    // Functions
    void Fire();
    void HandleDamage(float DamageAmount);

    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

private:
    FTimerHandle TimerHandle_Fire;
    float BaseX;
    float WaveSeed;
    UMaterialInstanceDynamic* DynamicMaterial;
};
```

**See the difference?** All 15 enemy stat variables defined in ~15 lines with default values. In the Blueprint approach, this would require:
- 15 × (Click +, type name, select type, click compile, set value) = **75+ clicks**
- Easy to make mistakes
- Hard to duplicate for enemy variants

---

## Comparison: Time Investment

### Blueprint-Heavy Approach (Original Tutorial)

**Part 2: Create Player**
- Step 2.3: Create 12 variables manually = **~15 minutes**
  - For each variable: Click +, name it, select type from dropdown, compile, set default value
  - Easy to mistype or select wrong type
- Step 2.4: Set up Enhanced Input = **~20 minutes**
  - Create 3 Input Action assets manually
  - Create Input Mapping Context
  - Add 8 key bindings with modifiers
- Step 2.5: Create firing logic with Blueprint nodes = **~25 minutes**
  - Drag ~20 nodes, connect white/blue wires
  - Easy to miss connections
- **Total for Player: ~60 minutes**

**Full Game Blueprint Tutorial: ~6-8 hours**

### Code-First Approach

**Part 2: Create Player**
- Step 2.1: Copy-paste header file = **~2 minutes**
  - All 12 variables defined inline with defaults
- Step 2.2: Copy-paste implementation = **~3 minutes**
  - Movement, firing, all logic in readable code
- Step 2.3: Configure input mappings (one-time) = **~5 minutes**
- Step 2.4: Compile = **~1 minute**
- **Total for Player: ~11 minutes** (5.5x faster!)

**Full Game C++ Implementation: ~2-3 hours** (3x faster!)

---

## When to Use Each Approach

### Use Code-First (C++) When:

✅ You have **many variables** to configure  
✅ You want **version control** with readable diffs  
✅ You need **complex logic** (math, loops, algorithms)  
✅ You're working in a **team** (better for code review)  
✅ You want **refactoring tools** (rename, find references)  
✅ You need **compile-time safety** (type checking)

### Use Blueprints When:

✅ Setting **visual assets** (meshes, materials, sprites)  
✅ **Rapid prototyping** of simple mechanics  
✅ **Non-programmers** need to modify behavior  
✅ Creating **animation blueprints** (visual timeline editing)  
✅ **Level design** and placement

### Hybrid Approach (Recommended):

🎯 **C++ base classes** → Define all logic and variables  
🎯 **Blueprint child classes** → Inherit from C++, set only visual assets  
🎯 **Best of both worlds** → Code maintainability + visual asset management

---

## Next Steps

Continue with the complete C++ implementations:

- [Part 5: Enemy Spawning System (C++)](code-first-part5-spawning.md)
- [Part 6: Game Mode and Rules (C++)](code-first-part6-gamemode.md)
- [Part 7: HUD and UI (C++)](code-first-part7-hud.md)
- [Complete C++ Reference](appendix-d-cpp-reference.md)

---

[Back to Index](README.md)
