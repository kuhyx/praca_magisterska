#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "ShootEmUpPlayerPawn.generated.h"

class USphereComponent;
class UStaticMeshComponent;
class UFloatingPawnMovement;
class USpringArmComponent;
class UCameraComponent;
class AShootEmUpProjectile;
class AShootEmUpGameMode;
class UMaterialInstanceDynamic;

UCLASS()
class MAGISTERKA_API AShootEmUpPlayerPawn : public APawn
{
    GENERATED_BODY()

public:
    AShootEmUpPlayerPawn();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

    void HandleProjectileImpact(float DamageAmount, AShootEmUpProjectile* FromProjectile);
    void NotifyEnemyDestroyed(int32 ScoreReward);

    int32 GetScore() const { return Score; }
    int32 GetLivesRemaining() const { return LivesRemaining; }
    int32 GetPlayerLevel() const { return PlayerLevel; }
    bool HasUsedSpecial() const { return bSpecialUsed; }

    void OnRespawn(const FVector& SpawnPoint);
    void ClearScreenSpecial();

protected:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void StartFiring();
    void StopFiring();
    void FireOnce();
    void PerformSpecial();

    TArray<FVector> BuildFireDirections() const;

    void LevelUp();

    void UpdateVisuals(float DeltaSeconds);

    UPROPERTY(VisibleAnywhere, Category = "Components")
    USphereComponent* CollisionComponent;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    UStaticMeshComponent* MeshComponent;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    UFloatingPawnMovement* MovementComponent;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    USpringArmComponent* SpringArmComponent;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    UCameraComponent* CameraComponent;

    UPROPERTY(EditDefaultsOnly, Category = "Combat")
    TSubclassOf<AShootEmUpProjectile> PlayerProjectileClass;

    UPROPERTY(EditDefaultsOnly, Category = "Combat")
    float FireInterval;

    UPROPERTY(EditDefaultsOnly, Category = "Combat")
    float ProjectileSpeed;

    UPROPERTY(EditDefaultsOnly, Category = "Combat")
    float ProjectileDamage;

    UPROPERTY(EditDefaultsOnly, Category = "Player")
    int32 MaxLives;

    UPROPERTY(EditDefaultsOnly, Category = "Player")
    float HitInvulnerabilityDuration;

    UPROPERTY(EditDefaultsOnly, Category = "Player")
    float ArenaHalfWidth;

    UPROPERTY(EditDefaultsOnly, Category = "Player")
    float ArenaHalfHeight;

    bool bIsFiring;
    bool bSpecialUsed;

    int32 Score;
    int32 PlayerLevel;
    int32 LivesRemaining;
    float InvulnerabilityTimer;
    float LevelUpFlashTimer;

    FVector MoveInput;

    FTimerHandle FireTimerHandle;

    TWeakObjectPtr<AShootEmUpGameMode> CachedGameMode;

    UPROPERTY()
    UMaterialInstanceDynamic* PlayerMaterial;
};
