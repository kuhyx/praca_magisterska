#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "InputActionValue.h"
#include "STGGameSettings.h"
#include "STGPawn.generated.h"

// Forward declarations
class UStaticMeshComponent;
class UBoxComponent;
class UInputMappingContext;
class UInputAction;

UCLASS()
class BULLETHELLCPP_API ASTGPawn : public APawn
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

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    UInputAction* CheatInvincibleAction;

    // ===== MOVEMENT & BOUNDARIES =====
    // Defaults from STGGameSettings.h - can be overridden in Blueprint
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float MoveSpeed = STG::Player::MoveSpeed;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    FVector2D BoundsMin = FVector2D(STG::PlayArea::MinX, STG::PlayArea::MinY);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    FVector2D BoundsMax = FVector2D(STG::PlayArea::MaxX, STG::PlayArea::MaxY);

    // ===== DEBUG =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Debug")
    bool bShowDebugBounds = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Debug")
    bool bDebugInvincible = false;

    // ===== VFX =====
    // Niagara effect when player gets hit
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VFX")
    class UNiagaraSystem* HitEffect;

    // ===== FIRING =====
    // Defaults from STGGameSettings.h (starts weak, upgrades with score)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireInterval = STG::Player::StartFireInterval;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BulletSpeed = STG::Player::BulletSpeed;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 VolleySize = STG::Player::StartVolleySize;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VolleySpread = STG::Player::StartVolleySpread;

    // Current upgrade level (0-4)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 UpgradeLevel = 0;

    // ===== LIVES & SCORE =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxLives = STG::Player::MaxLives;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentLives = STG::Player::MaxLives;

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
    void ToggleInvincibility(const FInputActionValue& Value);

    // ===== GAME LOGIC =====
    void FireShot();
    void TakeHit(int32 Damage);
    void HandleDeath();
    void AddScore(int32 Points);
    void CheckUpgrades();  // Check if score unlocks new upgrade level

protected:
    virtual void PossessedBy(AController* NewController) override;

private:
    FTimerHandle TimerHandle_Fire;
    bool bIsFiring = false;
    bool bIsDead = false;
    FVector2D MovementInput;
    float FireTimer = 0.0f;
    
    void UpdateHUD();
    void SetupInputMappingContext();
};
