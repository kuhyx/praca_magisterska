#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGProjectile.generated.h"

class USphereComponent;
class UProjectileMovementComponent;
class UStaticMeshComponent;

UCLASS()
class MCPGAMEPROJECT_API ASTGProjectile : public AActor
{
	GENERATED_BODY()
	
public:	
	ASTGProjectile();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	// Sphere collision component
	UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
	USphereComponent* CollisionComp;

	// Visual mesh component
	UPROPERTY(VisibleDefaultsOnly, Category=Projectile)
	UStaticMeshComponent* MeshComp;

	// Projectile movement component
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Movement, meta = (AllowPrivateAccess = "true"))
	UProjectileMovementComponent* ProjectileMovement;

	// Function that is called when the projectile hits something
	UFUNCTION()
	void OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit);

	// Function that is called when the projectile overlaps something
	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
	bool bIsPlayerBullet;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
	float Damage;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Gameplay")
	FLinearColor BulletColor;

	// Set bullet color
	void SetBulletColor(FLinearColor InColor);
	
	// Set speed
	void SetSpeed(float InSpeed);

private:
	UMaterialInstanceDynamic* DynamicMaterial;
};

