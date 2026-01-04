#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGEnemy.generated.h"

UENUM(BlueprintType)
enum class EEnemyType : uint8
{
	TypeA UMETA(DisplayName = "Type A - Basic Grunt"),      // Red cube, straight movement, single shots
	TypeB UMETA(DisplayName = "Type B - Wave Rider"),       // Blue sphere, sine wave, spread shots
	TypeC UMETA(DisplayName = "Type C - Tracker"),          // Yellow cone, seeks player, burst fire
	TypeD UMETA(DisplayName = "Type D - Tank"),             // Purple cylinder, slow, no shooting but tanky
};

UCLASS()
class MCPGAMEPROJECT_API ASTGEnemy : public AActor
{
	GENERATED_BODY()
	
public:	
	ASTGEnemy();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	class UStaticMeshComponent* MeshComp;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	class UBoxComponent* CollisionComp;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	EEnemyType EnemyType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	float Health;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	float MaxHealth;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	float MoveSpeed;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	float FireRate;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	int32 BulletsPerShot;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	int32 ScoreValue;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Enemy Stats")
	FLinearColor EnemyColor;

	FTimerHandle TimerHandle_Fire;
	FTimerHandle TimerHandle_BurstFire;
	int32 BurstShotsRemaining;

	void Fire();
	void HandleDamage(float DamageAmount);

	// Movement logic
	FVector TargetLocation;
	void UpdateMovement(float DeltaTime);

	// Configure based on type
	void ConfigureForType();

	// Overlap detection for player collision
	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

private:
	float SpawnTime;
	UMaterialInstanceDynamic* DynamicMaterial;
	bool bHasEnteredPlayArea;
	FVector InitialSpawnLocation;
	
	// For different movement patterns
	float SineOffset;
	float OrbitAngle;
};

