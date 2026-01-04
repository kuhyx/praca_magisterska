#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "STGPawn.generated.h"

class UCameraComponent;
class USpringArmComponent;
class UStaticMeshComponent;
class UBoxComponent;

UCLASS()
class MCPGAMEPROJECT_API ASTGPawn : public APawn
{
	GENERATED_BODY()

public:
	ASTGPawn();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	// Components
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ShipMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USpringArmComponent* SpringArm;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UCameraComponent* Camera;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UBoxComponent* Hitbox; // The 1-pixel hitbox

	// Visual indicator for hitbox
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* HitboxIndicator;

	// Gameplay Variables
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
	float MoveSpeed;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 Lives;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 Score;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 Level;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	int32 BulletCount;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
	bool bCanSpecial;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
	float FireRate;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
	bool bIsInvulnerable;

	// Input functions
	void MoveForward(float Value);
	void MoveRight(float Value);
	void StartFire();
	void StopFire();
	void UseSpecial();

	// Logic
	void FireShot();
	FTimerHandle TimerHandle_Fire;
	FTimerHandle TimerHandle_Invulnerability;
	bool bIsFiring;

	void HandleDamage(float DamageAmount);
	void AddScore(int32 Points);
	void LevelUp();
	void Die();
	void Respawn();
	void ClearScreen();
	void EndInvulnerability();

	FVector MovementInput;

	// Boundaries
	UPROPERTY(EditAnywhere, Category = "Boundaries")
	float MinX;
	
	UPROPERTY(EditAnywhere, Category = "Boundaries")
	float MaxX;
	
	UPROPERTY(EditAnywhere, Category = "Boundaries")
	float MinY;
	
	UPROPERTY(EditAnywhere, Category = "Boundaries")
	float MaxY;

private:
	UMaterialInstanceDynamic* ShipMaterial;
	float InvulnerabilityFlashTimer;
};

