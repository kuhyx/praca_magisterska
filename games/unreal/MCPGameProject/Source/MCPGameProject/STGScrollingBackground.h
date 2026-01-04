#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGScrollingBackground.generated.h"

UCLASS()
class MCPGAMEPROJECT_API ASTGScrollingBackground : public AActor
{
	GENERATED_BODY()
	
public:	
	ASTGScrollingBackground();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	class UStaticMeshComponent* BackgroundMesh1;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	class UStaticMeshComponent* BackgroundMesh2;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scrolling")
	float ScrollSpeed;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scrolling")
	float TileLength;

private:
	float ResetPosition;
};
