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

    // ===== DEBUG =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Debug")
    bool bShowDebugBounds = true;

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
    bool bIsDead = false;
    FVector2D MovementInput;
    float FireTimer = 0.0f;
};
