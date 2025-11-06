#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "BackgroundScroller.generated.h"

class UStaticMeshComponent;

UCLASS()
class MAGISTERKA_API ABackgroundScroller : public AActor
{
    GENERATED_BODY()

public:
    ABackgroundScroller();

    virtual void Tick(float DeltaSeconds) override;

protected:
    virtual void BeginPlay() override;
    void ResetSegment(UStaticMeshComponent* Segment, float OffsetMultiplier);

    UPROPERTY(VisibleAnywhere, Category = "Components")
    USceneComponent* Root;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    TArray<UStaticMeshComponent*> Segments;

    UPROPERTY(EditDefaultsOnly, Category = "Scroll")
    float ScrollSpeed;

    UPROPERTY(EditDefaultsOnly, Category = "Scroll")
    float SegmentLength;
};
