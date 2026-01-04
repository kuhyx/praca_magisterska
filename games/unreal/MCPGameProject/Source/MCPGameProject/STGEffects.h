#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGEffects.generated.h"

// Simple explosion effect actor
UCLASS()
class MCPGAMEPROJECT_API ASTGExplosionEffect : public AActor
{
	GENERATED_BODY()
	
public:	
	ASTGExplosionEffect();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	class UStaticMeshComponent* ExplosionMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
	float Duration;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
	float MaxScale;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
	FLinearColor ExplosionColor;

private:
	float CurrentTime;
	UMaterialInstanceDynamic* DynamicMaterial;
};

// Hit spark effect
UCLASS()
class MCPGAMEPROJECT_API ASTGHitEffect : public AActor
{
	GENERATED_BODY()
	
public:	
	ASTGHitEffect();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	class UStaticMeshComponent* SparkMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
	FLinearColor SparkColor;

private:
	float CurrentTime;
	float Duration;
	UMaterialInstanceDynamic* DynamicMaterial;
};

// Screen clear effect (expanding ring)
UCLASS()
class MCPGAMEPROJECT_API ASTGScreenClearEffect : public AActor
{
	GENERATED_BODY()
	
public:	
	ASTGScreenClearEffect();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	class UStaticMeshComponent* RingMesh;

private:
	float CurrentTime;
	float Duration;
	UMaterialInstanceDynamic* DynamicMaterial;
};
