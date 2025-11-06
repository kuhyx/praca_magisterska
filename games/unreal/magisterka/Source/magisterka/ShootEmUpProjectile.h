#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ShootEmUpProjectile.generated.h"

class USphereComponent;
class UStaticMeshComponent;
class UProjectileMovementComponent;

UCLASS()
class MAGISTERKA_API AShootEmUpProjectile : public AActor
{
    GENERATED_BODY()

public:
    AShootEmUpProjectile();

    virtual void Tick(float DeltaSeconds) override;

    void InitProjectile(const FVector& Direction, float Speed, float LifeSeconds, bool bPlayerBullet, float InDamage, const FLinearColor& TintColor);

    bool IsPlayerProjectile() const { return bFromPlayer; }
    float GetDamage() const { return Damage; }

protected:
    virtual void BeginPlay() override;

private:
    UPROPERTY(VisibleAnywhere, Category = "Components")
    USphereComponent* CollisionComponent;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    UStaticMeshComponent* MeshComponent;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    UProjectileMovementComponent* MovementComponent;

    UPROPERTY(EditDefaultsOnly, Category = "Projectile")
    float DefaultSpeed;

    UPROPERTY(EditDefaultsOnly, Category = "Projectile")
    float DefaultLifeSpan;

    UPROPERTY(EditDefaultsOnly, Category = "Projectile")
    float DefaultDamage;

    bool bFromPlayer;
    float Damage;

    UFUNCTION()
    void OnProjectileOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
