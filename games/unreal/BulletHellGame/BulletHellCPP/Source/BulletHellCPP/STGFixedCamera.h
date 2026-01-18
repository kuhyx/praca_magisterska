#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGGameSettings.h"
#include "STGFixedCamera.generated.h"

class UCameraComponent;
class ASTGGameDirector;

/**
 * Fixed camera that shows the entire play area for the bullet-hell game.
 * Place this in the level and it will automatically become the active camera.
 * 
 * If bAutoFitPlayArea is true, the camera automatically calculates the correct
 * height and FOV to show exactly the play area defined in STGGameDirector.
 */
UCLASS()
class BULLETHELLCPP_API ASTGFixedCamera : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGFixedCamera();

protected:
    virtual void BeginPlay() override;

    // Calculate camera height needed to show the play area with given FOV
    float CalculateCameraHeightForPlayArea(const FVector2D& PlayAreaSize, float FOV) const;

public:    
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UCameraComponent* Camera;

    // ===== AUTO-FIT MODE =====
    // When true, camera automatically sizes to fit the play area from Game Director
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Camera|Auto Fit")
    bool bAutoFitPlayArea = true;

    // Extra margin around play area (percentage, 0.1 = 10% extra)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Camera|Auto Fit", meta = (EditCondition = "bAutoFitPlayArea", ClampMin = "0.0", ClampMax = "0.5"))
    float PlayAreaMargin = STG::Camera::DefaultMargin;

    // ===== MANUAL MODE =====
    // Height above play area (Z position) - only used if bAutoFitPlayArea is false
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Camera|Manual", meta = (EditCondition = "!bAutoFitPlayArea"))
    float CameraHeight = STG::Camera::DefaultHeight;

    // Field of view (degrees) - used in both modes
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Camera")
    float FieldOfView = STG::Camera::DefaultFOV;

    // Whether to use orthographic projection (better for 2D-style gameplay)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Camera")
    bool bUseOrthographic = false;

    // Orthographic width (only used if bUseOrthographic is true)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Camera", meta = (EditCondition = "bUseOrthographic"))
    float OrthoWidth = STG::Camera::OrthoWidth;
};
