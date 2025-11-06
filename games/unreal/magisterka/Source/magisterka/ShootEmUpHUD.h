#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "ShootEmUpHUD.generated.h"

class AShootEmUpGameMode;
class AShootEmUpPlayerPawn;

UCLASS()
class MAGISTERKA_API AShootEmUpHUD : public AHUD
{
    GENERATED_BODY()

public:
    AShootEmUpHUD();

    virtual void DrawHUD() override;

    void SetLevelUpMessage(const FString& Message, float Duration);

protected:
    void DrawScore(float X, float Y);
    void DrawLives(float X, float Y);
    void DrawTimer(float X, float Y);
    void DrawLevelUp(float X, float Y);
    void DrawGameOver(float X, float Y);

    FLinearColor ScoreColor;
    FLinearColor TimerColor;
    FLinearColor LifeColor;
    FLinearColor AlertColor;

    float LevelUpMessageTimer;
    FString LevelUpMessage;
};
