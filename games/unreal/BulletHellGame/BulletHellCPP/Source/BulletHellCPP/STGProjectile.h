#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGProjectile.generated.h"

class USphereComponent;
class UProjectileMovementComponent;
class UStaticMeshComponent;

UCLASS()
class BULLETHELLCPP_API ASTGProjectile : public AActor
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