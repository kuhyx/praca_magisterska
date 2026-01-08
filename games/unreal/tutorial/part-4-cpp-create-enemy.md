# Part 4 (C++): Create the Enemy

[← Previous: Part 3 (C++) - Create the Bullet](part-3-cpp-create-bullet.md) | [Back to Index](README.md) | [Next: Part 5 (C++) - Create Enemy Spawner →](part-5-cpp-create-spawner.md)

---

## Overview

Create enemy ships in C++. Again, we'll copy-paste all 15 enemy variables instead of clicking UI 75+ times.

**Time comparison:**
- Blueprint approach (Part 4): ~90 minutes (16 variables + complex Blueprint nodes)
- C++ approach (this part): ~25 minutes (copy-paste code)

---

## Step 4.1: Create STGEnemy C++ Class

### In Unreal Editor:

1. Go to **Tools → New C++ Class** (top menu bar)
2. In the "Choose Parent Class" window:
   - Click **"Actor"** (enemies are independent game objects)
   - Click **"Next"**

3. In the "Name Your New Actor" window:
   - **Name:** `STGEnemy`
   - **Path:** Should be `Source/BulletHellGame/` (default)
   - Click **"Create Class"**

### What Happens Next:

1. Unreal generates `STGEnemy.h` and `STGEnemy.cpp`
2. VS Code opens with the new files
3. Project compiles automatically (~30-60 seconds)
4. Unreal Editor refreshes

---

## Step 4.2: Define Enemy Variables in STGEnemy.h

**This is where the magic happens!** Instead of clicking UI 75+ times (16 variables × ~5 clicks each), we'll **copy-paste** all variables at once.

### Open STGEnemy.h in VS Code

Replace the entire file content with:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGEnemy.generated.h"

class UStaticMeshComponent;
class UBoxComponent;

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

    // ===== COMPONENTS =====
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UBoxComponent* CollisionComp;

    // ===== HEALTH & SCORE (copy-paste all 15 variables!) =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxHealth = 12;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentHealth = 12;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 ScoreValue = 50;

    // ===== MOVEMENT =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VerticalSpeed = 220.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalAmplitude = 250.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalFrequency = 1.8f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float DespawnY = -750.0f;

    // ===== FIRING =====
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

    // ===== FUNCTIONS =====
    void Fire();
    void HandleDamage(float DamageAmount);

    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                        bool bFromSweep, const FHitResult& SweepResult);

private:
    FTimerHandle TimerHandle_Fire;
    float BaseX = 0.0f;
    float WaveSeed = 0.0f;
    float ElapsedTime = 0.0f;
};
```

### What Just Happened?

You just defined **15 gameplay variables + 2 components** with default values in ~30 seconds!

In the Blueprint tutorial, this would require:
- 16 variables × 5 clicks each = **80 clicks**
- **~20 minutes** of manual work
- High chance of typos or wrong types

**Time saved: 19.5 minutes** ⚡

---

## Step 4.3: Implement STGEnemy Logic

### Open STGEnemy.cpp in VS Code

Replace the file content with:

```cpp
#include "STGEnemy.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Kismet/GameplayStatics.h"
#include "STGProjectile.h"
#include "STGPawn.h"

ASTGEnemy::ASTGEnemy()
{
    PrimaryActorTick.bCanEverTick = true;

    // Root component
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

    // Mesh component
    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
    MeshComp->SetupAttachment(RootComponent);
    MeshComp->SetCollisionProfileName("NoCollision");
    
    // Load cube mesh
    static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMesh(TEXT("/Engine/BasicShapes/Cube"));
    if (CubeMesh.Succeeded())
    {
        MeshComp->SetStaticMesh(CubeMesh.Object);
        MeshComp->SetRelativeScale3D(FVector(0.6f, 0.6f, 0.1f));
    }

    // Collision component
    CollisionComp = CreateDefaultSubobject<UBoxComponent>(TEXT("CollisionComp"));
    CollisionComp->SetupAttachment(RootComponent);
    CollisionComp->SetBoxExtent(FVector(30.f, 30.f, 10.f));
    CollisionComp->SetCollisionProfileName("OverlapAllDynamic");
    CollisionComp->SetGenerateOverlapEvents(true);
    CollisionComp->OnComponentBeginOverlap.AddDynamic(this, &ASTGEnemy::OnOverlapBegin);
}

void ASTGEnemy::BeginPlay()
{
    Super::BeginPlay();
    
    CurrentHealth = MaxHealth;
    BaseX = GetActorLocation().X;
    WaveSeed = FMath::FRand() * 1000.0f;
    ElapsedTime = 0.0f;

    // Start firing timer
    GetWorldTimerManager().SetTimer(TimerHandle_Fire, this, &ASTGEnemy::Fire, 
                                    FireInterval, true, FireInterval);
}

void ASTGEnemy::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    ElapsedTime += DeltaTime;

    // Sinusoidal movement (wave pattern)
    FVector NewLocation = GetActorLocation();
    
    // Move downward
    NewLocation.X -= VerticalSpeed * DeltaTime;
    
    // Horizontal sine wave
    float HorizontalOffset = HorizontalAmplitude * FMath::Sin(
        HorizontalFrequency * (ElapsedTime + WaveSeed)
    );
    NewLocation.Y = BaseX + HorizontalOffset;
    
    SetActorLocation(NewLocation);

    // Check if enemy should despawn (moved off screen)
    if (NewLocation.X < DespawnY)
    {
        Destroy();
    }
}

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
        
        // Spawn location slightly below enemy
        FVector SpawnLocation = GetActorLocation() + FVector(0.f, 0.f, -30.f);
        
        // Spawn bullet
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
            Bullet->Lifetime = EnemyBulletLifetime;
        }
    }
}

void ASTGEnemy::HandleDamage(float DamageAmount)
{
    CurrentHealth -= DamageAmount;
    
    if (CurrentHealth <= 0)
    {
        // Award score to player
        ASTGPawn* Player = Cast<ASTGPawn>(UGameplayStatics::GetPlayerPawn(GetWorld(), 0));
        if (Player)
        {
            Player->AddScore(ScoreValue);
        }
        
        // Destroy enemy
        Destroy();
    }
}

void ASTGEnemy::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                                UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                                bool bFromSweep, const FHitResult& SweepResult)
{
    // Enemy collides with player - damage player
    if (OtherActor && OtherActor != this)
    {
        ASTGPawn* Player = Cast<ASTGPawn>(OtherActor);
        if (Player)
        {
            Player->TakeHit(1);
            Destroy(); // Enemy dies on collision with player
        }
    }
}
```

---

## Step 4.4: Update Bullet Collision Logic

Now that enemies exist, we can complete the bullet collision logic.

### Open STGProjectile.cpp

Find the `OnOverlapBegin` function and update the player bullet section:

```cpp
void ASTGProjectile::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                                     UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                                     bool bFromSweep, const FHitResult& SweepResult)
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
```

### Add include at top of STGProjectile.cpp:

```cpp
#include "STGEnemy.h"  // Add this line
```

---

## Step 4.5: Compile the Code

### In Unreal Editor:

1. Click **"Compile"** button (bottom right)
2. Wait for compilation (~30-60 seconds)
3. Check for errors in Output Log

OR

### In VS Code:

1. Open terminal in VS Code (`Ctrl+` `)
2. Run build command (project-specific)
3. Wait for build to finish

### Expected Result:

- ✅ Compilation succeeds
- ✅ "C++ Classes" folder in Content Browser shows `STGEnemy`
- ✅ No errors in Output Log

---

## Step 4.6: Create Blueprint Child

Create a **minimal Blueprint** that inherits from STGEnemy. This Blueprint is ONLY for visual assets!

1. In Content Browser, navigate to `Content → Blueprints`
2. Right-click → **Blueprint Class**
3. In "Pick Parent Class" window:
   - Click "All Classes" dropdown
   - Search for `STGEnemy`
   - Select it
   - Click "Select"
4. Name it: `BP_Enemy`
5. Double-click to open

### In the Blueprint Editor:

**Components (Left Panel):**
- You'll see `MeshComp` and `CollisionComp` from C++
- NO NEED to add them manually!

**Variables (My Blueprint Panel):**
- You'll see all 15 variables from C++ (MaxHealth, VerticalSpeed, etc.)
- NO NEED to create them!
- All default values are already set from C++!

**What to do:**
- NOTHING for now! All logic is in C++
- Compile and Save

---

## Step 4.7: Test Enemy Spawning

1. Drag `BP_Enemy` from Content Browser into the level
2. Position it above the player (Y = 0, X = 500 or so)
3. Press **Play** (`Alt+P`)

### Expected Result

**In Play Mode Window:**

**Enemy behavior:**
- ✅ Enemy appears above player
- ✅ Enemy moves downward smoothly
- ✅ Enemy moves in sine wave pattern (left-right oscillation)
- ✅ Enemy fires red bullet bursts in circular pattern
- ✅ Bullets spread out in all directions (360-degree burst)

**Player vs Enemy:**
- ✅ Player bullets (green) destroy enemy when they hit
- ✅ Enemy bullets (red) damage player when they hit
- ✅ Player takes damage and loses life when hit
- ✅ Touching enemy directly damages player and destroys enemy

**Visual confirmation:**
- Enemy is a cube/box shape (red-ish by default)
- Enemy fires 20 red bullets in a circular burst every 0.35 seconds
- Player can shoot enemy with green bullets
- Score increases when enemy is destroyed (check Output Log or will see in UI later)

**To test collision:**
- Fly player into enemy - both should take damage
- Let enemy bullets hit player - player should take damage
- Shoot enemy with player bullets - enemy health should decrease

**Despawning:**
- After ~10 seconds, enemy moves off bottom of screen and disappears (auto-destroy)

---

## Step 4.8: Update Player Special Ability

Now that enemies exist, we can complete the special ability to destroy all enemies on screen.

### Open STGPawn.cpp

Find the `UseSpecial()` function and replace it with:

```cpp
void ASTGPawn::UseSpecial()
{
    if (!bSpecialUsed)
    {
        bSpecialUsed = true;
        
        // Destroy all enemies on screen
        TArray<AActor*> FoundEnemies;
        UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGEnemy::StaticClass(), FoundEnemies);
        for (AActor* Enemy : FoundEnemies)
        {
            Enemy->Destroy();
        }

        // Destroy all enemy bullets (not player bullets)
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
        
        UE_LOG(LogTemp, Warning, TEXT("SPECIAL ABILITY - Screen Cleared!"));
    }
}
```

### Add include at top of STGPawn.cpp:

```cpp
#include "STGEnemy.h"  // Add this line
```

### Compile again!

---

## Step 4.9: Test Special Ability

1. Place several `BP_Enemy` instances in the level (or duplicate the existing one)
2. Press **Play**
3. Let enemies spawn and fire bullets
4. Press **X** to activate special ability

### Expected Result in Play Mode:

- ✅ All enemies disappear instantly when X is pressed
- ✅ All red enemy bullets disappear instantly
- ✅ Player's green bullets remain (not destroyed)
- ✅ Message "SPECIAL ABILITY - Screen Cleared!" appears in Output Log
- ✅ Pressing X again does nothing (ability can only be used once per game)

---

## Comparison Summary

### Blueprint Approach (Part 4):

1. Create BP_Enemy Blueprint ✅
2. Add 2 components manually
3. Add 16 variables one-by-one = **~20 minutes of clicking**
4. Create Blueprint nodes for movement (~40 nodes with sine wave math)
5. Create Blueprint nodes for firing (~30 nodes for radial burst)
6. Create Blueprint nodes for collision detection
7. Create Blueprint nodes for health/damage system
8. Update BP_Player special ability nodes
9. **Total: ~90 minutes**

### C++ Approach (This Part):

1. Create STGEnemy C++ class ✅
2. Copy-paste header file with 15 variables **30 seconds**
3. Copy-paste implementation file with all logic
4. Update bullet collision (5 lines)
5. Update player special ability (10 lines)
6. Compile
7. Create BP_Enemy (inherits everything from C++)
8. **Total: ~25 minutes**

**Time saved: 65 minutes** ⚡⚡⚡

---

## What's Next?

In Part 5, we'll create the enemy spawner in C++. You'll see how easy it is to manage spawn rates and difficulty curves with code!

---

[← Previous: Part 3 (C++) - Create the Bullet](part-3-cpp-create-bullet.md) | [Back to Index](README.md) | [Next: Part 5 (C++) - Create Enemy Spawner →](part-5-cpp-create-spawner.md)
