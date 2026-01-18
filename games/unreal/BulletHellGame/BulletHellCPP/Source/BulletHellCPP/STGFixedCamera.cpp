#include "STGFixedCamera.h"
#include "STGGameDirector.h"
#include "Camera/CameraComponent.h"
#include "Kismet/GameplayStatics.h"

ASTGFixedCamera::ASTGFixedCamera()
{
    PrimaryActorTick.bCanEverTick = false;

    // Root scene component
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

    // Camera component
    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    Camera->SetupAttachment(RootComponent);
    
    // Default rotation: looking down (-Z direction = top-down view)
    Camera->SetRelativeRotation(FRotator(-90.f, 0.f, 0.f));
    
    // Set default field of view
    Camera->FieldOfView = FieldOfView;
}

float ASTGFixedCamera::CalculateCameraHeightForPlayArea(const FVector2D& PlayAreaSize, float FOV) const
{
    // For a top-down camera, we need to calculate height so the play area fits in view
    // Using the larger dimension (width or height) to ensure everything fits
    // FOV is horizontal, so we use the X (width) dimension primarily
    
    const float HalfWidth = PlayAreaSize.X / 2.0f;
    const float HalfHeight = PlayAreaSize.Y / 2.0f;
    
    // Calculate height needed for width (using horizontal FOV)
    const float HalfFOVRad = FMath::DegreesToRadians(FOV / 2.0f);
    const float HeightForWidth = HalfWidth / FMath::Tan(HalfFOVRad);
    
    // Calculate height needed for height (approximate vertical FOV assuming 16:9)
    // Vertical FOV = 2 * atan(tan(HorizontalFOV/2) / AspectRatio)
    const float AspectRatio = 16.0f / 9.0f;
    const float VerticalHalfFOVRad = FMath::Atan(FMath::Tan(HalfFOVRad) / AspectRatio);
    const float HeightForHeight = HalfHeight / FMath::Tan(VerticalHalfFOVRad);
    
    // Use the larger height to ensure both dimensions fit
    return FMath::Max(HeightForWidth, HeightForHeight);
}

void ASTGFixedCamera::BeginPlay()
{
    Super::BeginPlay();

    // Apply FOV setting
    Camera->FieldOfView = FieldOfView;
    
    if (bUseOrthographic)
    {
        Camera->ProjectionMode = ECameraProjectionMode::Orthographic;
        Camera->OrthoWidth = OrthoWidth;
    }
    else
    {
        Camera->ProjectionMode = ECameraProjectionMode::Perspective;
    }

    // Calculate camera position
    FVector CameraPosition = FVector::ZeroVector;
    
    if (bAutoFitPlayArea)
    {
        // Find the Game Director to get play area bounds
        TArray<AActor*> FoundDirectors;
        UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGGameDirector::StaticClass(), FoundDirectors);
        
        if (FoundDirectors.Num() > 0)
        {
            ASTGGameDirector* Director = Cast<ASTGGameDirector>(FoundDirectors[0]);
            if (Director)
            {
                // Calculate play area center and size
                FVector2D PlayAreaCenter = (Director->PlayAreaMin + Director->PlayAreaMax) / 2.0f;
                FVector2D PlayAreaSize = Director->GetPlayAreaSize();
                
                // Add margin by using a narrower effective FOV
                // This makes the camera pull back to show more area around the edges
                float EffectiveFOV = FieldOfView * (1.0f - PlayAreaMargin);
                
                // Calculate required height with the effective (narrower) FOV
                float RequiredHeight = CalculateCameraHeightForPlayArea(PlayAreaSize, EffectiveFOV);
                
                // Set camera position at center of play area, at calculated height
                CameraPosition = FVector(PlayAreaCenter.X, PlayAreaCenter.Y, RequiredHeight);
                
                if (GEngine)
                {
                    GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Cyan, 
                        FString::Printf(TEXT("Camera auto-fit: Height=%.0f, FOV=%.0f (effective=%.0f) for area %.0fx%.0f"), 
                            RequiredHeight, FieldOfView, EffectiveFOV, PlayAreaSize.X, PlayAreaSize.Y));
                }
            }
        }
        else
        {
            // No Game Director found, fall back to manual settings
            UE_LOG(LogTemp, Warning, TEXT("STGFixedCamera: No STGGameDirector found, using manual CameraHeight"));
            CameraPosition = FVector(0.f, 0.f, CameraHeight);
        }
    }
    else
    {
        // Manual mode - use specified height
        CameraPosition = FVector(0.f, 0.f, CameraHeight);
    }
    
    SetActorLocation(CameraPosition);

    // Activate this camera for player 0
    APlayerController* PC = UGameplayStatics::GetPlayerController(GetWorld(), 0);
    if (PC)
    {
        PC->SetViewTargetWithBlend(this, 0.0f);
    }
}
