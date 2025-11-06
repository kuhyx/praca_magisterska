#include "BackgroundScroller.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"

ABackgroundScroller::ABackgroundScroller()
{
    PrimaryActorTick.bCanEverTick = true;

    Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    SetRootComponent(Root);

    static ConstructorHelpers::FObjectFinder<UStaticMesh> PlaneMesh(TEXT("/Engine/BasicShapes/Plane.Plane"));

    const int32 SegmentCount = 3;
    Segments.Reserve(SegmentCount);
    for (int32 Index = 0; Index < SegmentCount; ++Index)
    {
        UStaticMeshComponent* Segment = CreateDefaultSubobject<UStaticMeshComponent>(*FString::Printf(TEXT("Segment_%d"), Index));
        Segment->SetupAttachment(Root);
        Segment->SetCollisionEnabled(ECollisionEnabled::NoCollision);
        Segment->SetRelativeRotation(FRotator(0.f, 0.f, 0.f));
        Segment->SetRelativeScale3D(FVector(20.f, 20.f, 1.f));
        if (PlaneMesh.Succeeded())
        {
            Segment->SetStaticMesh(PlaneMesh.Object);
        }
        Segments.Add(Segment);
    }

    ScrollSpeed = 300.f;
    SegmentLength = 2000.f;
}

void ABackgroundScroller::BeginPlay()
{
    Super::BeginPlay();

    for (int32 Index = 0; Index < Segments.Num(); ++Index)
    {
        if (Segments[Index])
        {
            Segments[Index]->SetRelativeLocation(FVector(0.f, Index * SegmentLength, -200.f));
        }
    }
}

void ABackgroundScroller::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    for (int32 Index = 0; Index < Segments.Num(); ++Index)
    {
        if (UStaticMeshComponent* Segment = Segments[Index])
        {
            FVector Location = Segment->GetComponentLocation();
            Location.Y -= ScrollSpeed * DeltaSeconds;
            if (Location.Y <= -SegmentLength)
            {
                Location.Y += SegmentLength * Segments.Num();
            }
            Segment->SetWorldLocation(Location);
        }
    }
}

void ABackgroundScroller::ResetSegment(UStaticMeshComponent* Segment, float OffsetMultiplier)
{
    if (!Segment)
    {
        return;
    }

    const FVector BaseLocation(0.f, OffsetMultiplier * SegmentLength, -200.f);
    Segment->SetRelativeLocation(BaseLocation);
}
