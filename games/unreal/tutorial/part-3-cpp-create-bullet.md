# Part 3 (C++): Create the Bullet

[← Previous: Part 2 (C++) - Create the Player](part-2-cpp-create-player.md) | [Back to Index](README.md) | [Next: Part 4 (C++) - Create the Enemy →](part-4-cpp-create-enemy.md)

---

## Overview

Create the bullet/projectile class in C++. Again, we'll copy-paste all variables instead of clicking UI.

**Time comparison:**
- Blueprint: ~30 minutes (5 variables + Blueprint nodes)
- C++ (this part): ~10 minutes (copy-paste code)

---

## Step 3.1: Create STGProjectile C++ Class

1. **Tools → New C++ Class**
2. Choose **"Actor"** as parent class → Next
3. Name: `STGProjectile` → Create Class
4. Wait for compilation

---

## Step 3.2: Copy-Paste STGProjectile.h

Replace the entire header file with:

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

    // ===== COMPONENTS =====
    UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
    USphereComponent* CollisionComp;

    UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
    UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Movement)
    UProjectileMovementComponent* ProjectileMovement;

    // ===== VARIABLES (all with defaults!) =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    bool bIsPlayerBullet = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    float Damage = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    FLinearColor BulletColor = FLinearColor::Green;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
    float Lifetime = 4.0f;

    // ===== FUNCTIONS =====
    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                        bool bFromSweep, const FHitResult& SweepResult);

    void SetBulletColor(FLinearColor InColor);
    void SetSpeed(float InSpeed);

private:
    UMaterialInstanceDynamic* DynamicMaterial;
};
```

**What just happened:** 5 bullet variables defined with defaults in 10 seconds!

---

## Step 3.3: Copy-Paste STGProjectile.cpp

Replace the implementation file with:

```cpp
#include "STGProjectile.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "STGEnemy.h"  // Will create in Part 4
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

    // Create dynamic material for bullet color
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

void ASTGProjectile::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                                     UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                                     bool bFromSweep, const FHitResult& SweepResult)
{
    if (OtherActor && OtherActor != this)
    {
        if (bIsPlayerBullet)
        {
            // Player bullet hits enemy (will implement in Part 4)
            // ASTGEnemy* Enemy = Cast<ASTGEnemy>(OtherActor);
            // if (Enemy) { Enemy->HandleDamage(Damage); Destroy(); }
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

## Step 3.4: Compile

1. Click **Compile** in Unreal Editor
2. Wait for compilation
3. Check for errors

---

## Step 3.5: Update Player Firing Logic

Now that we have bullets, let's make the player actually spawn them!

### Open STGPawn.cpp

Find the `FireShot()` function and replace it with:

```cpp
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

        // Spawn bullet
        UWorld* World = GetWorld();
        if (World)
        {
            ASTGProjectile* Bullet = World->SpawnActor<ASTGProjectile>(
                ASTGProjectile::StaticClass(), 
                SpawnLocation, 
                SpawnRotation
            );
            
            if (Bullet)
            {
                Bullet->bIsPlayerBullet = true;
                Bullet->SetSpeed(BulletSpeed);
                Bullet->SetBulletColor(FLinearColor::Green);
            }
        }
    }
}
```

### Add include at top of STGPawn.cpp:

```cpp
#include "STGProjectile.h"  // Add this line
```

### Compile again!

---

## Step 3.6: Test Bullet Firing

1. Press **Play** (`Alt+P`)
2. Move with WASD
3. Press Z or Space to fire
4. You should see green spheres shooting upward!

### Expected Result:

- ✅ Player fires 3 bullets in a spread pattern
- ✅ Bullets are green
- ✅ Bullets auto-destroy after 4 seconds
- ✅ Can hold Z to auto-fire

---

## Comparison Summary

### Blueprint Approach:

- Create BP_Bullet Blueprint
- Add 5 variables manually (×5 clicks each = 25 clicks)
- Create Blueprint nodes for movement (~15 nodes)
- Create Blueprint nodes for collision (~10 nodes)
- Update BP_Player firing logic (~15 more nodes)
- **Total: ~30 minutes**

### C++ Approach:

- Create STGProjectile class
- Copy-paste header (5 variables with defaults)
- Copy-paste implementation
- Update one function in STGPawn
- Compile twice
- **Total: ~10 minutes**

**Time saved: 20 minutes** ⚡

---

## What's Next?

In Part 4, we'll create enemies with C++. You'll see how easy it is to copy enemy patterns!

---

[← Previous: Part 2 (C++) - Create the Player](part-2-cpp-create-player.md) | [Back to Index](README.md) | [Next: Part 4 (C++) - Create the Enemy →](part-4-cpp-create-enemy.md)
