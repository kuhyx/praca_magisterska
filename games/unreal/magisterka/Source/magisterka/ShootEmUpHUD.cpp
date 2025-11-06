#include "ShootEmUpHUD.h"
#include "ShootEmUpGameMode.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"

AShootEmUpHUD::AShootEmUpHUD()
{
    ScoreColor = FLinearColor::White;
    TimerColor = FLinearColor::Yellow;
    LifeColor = FLinearColor::Green;
    AlertColor = FLinearColor::Red;
    LevelUpMessageTimer = 0.f;
}

void AShootEmUpHUD::DrawHUD()
{
    Super::DrawHUD();

    if (!Canvas)
    {
        return;
    }

    const float Margin = 32.f;

    DrawScore(Margin, Margin);
    DrawLives(Margin, Margin + 48.f);
    DrawTimer(Canvas->SizeX - 300.f, Margin);
    DrawLevelUp(Canvas->SizeX * 0.5f - 150.f, Margin * 0.5f);
    DrawGameOver(Canvas->SizeX * 0.5f - 200.f, Canvas->SizeY * 0.5f - 50.f);
}

void AShootEmUpHUD::SetLevelUpMessage(const FString& Message, float Duration)
{
    LevelUpMessage = Message;
    LevelUpMessageTimer = Duration;
}

void AShootEmUpHUD::DrawScore(float X, float Y)
{
    if (AShootEmUpGameMode* GM = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this)))
    {
        const FString ScoreText = FString::Printf(TEXT("Score: %d"), GM->GetScore());
        FCanvasTextItem TextItem(FVector2D(X, Y), FText::FromString(ScoreText), GEngine->GetLargeFont(), ScoreColor);
        TextItem.EnableShadow(FLinearColor::Black);
        Canvas->DrawItem(TextItem);
    }
}

void AShootEmUpHUD::DrawLives(float X, float Y)
{
    if (AShootEmUpGameMode* GM = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this)))
    {
        const int32 Lives = GM->GetLives();
        FString LifeText = TEXT("Lives: ");
        for (int32 Index = 0; Index < Lives; ++Index)
        {
            LifeText.Append(TEXT("[+] "));
        }
        if (Lives <= 0)
        {
            LifeText = TEXT("Lives: [x]");
        }

        FCanvasTextItem TextItem(FVector2D(X, Y), FText::FromString(LifeText), GEngine->GetLargeFont(), LifeColor);
        TextItem.EnableShadow(FLinearColor::Black);
        Canvas->DrawItem(TextItem);
    }
}

void AShootEmUpHUD::DrawTimer(float X, float Y)
{
    if (AShootEmUpGameMode* GM = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this)))
    {
        const float Remaining = GM->GetRemainingTime();
        const int32 Minutes = FMath::FloorToInt(Remaining / 60.f);
        const int32 Seconds = FMath::FloorToInt(FMath::Fmod(Remaining, 60.f));
        const FString TimerText = FString::Printf(TEXT("Time: %02d:%02d"), Minutes, Seconds);

        FCanvasTextItem TextItem(FVector2D(X, Y), FText::FromString(TimerText), GEngine->GetLargeFont(), TimerColor);
        TextItem.EnableShadow(FLinearColor::Black);
        Canvas->DrawItem(TextItem);
    }
}

void AShootEmUpHUD::DrawLevelUp(float X, float Y)
{
    if (LevelUpMessageTimer <= 0.f)
    {
        return;
    }

    LevelUpMessageTimer -= GetWorld()->GetDeltaSeconds();
    const FString Text = LevelUpMessage.IsEmpty() ? TEXT("Level Up!") : LevelUpMessage;

    FCanvasTextItem TextItem(FVector2D(X, Y), FText::FromString(Text), GEngine->GetLargeFont(), AlertColor);
    TextItem.EnableShadow(FLinearColor::Black);
    Canvas->DrawItem(TextItem);
}

void AShootEmUpHUD::DrawGameOver(float X, float Y)
{
    if (AShootEmUpGameMode* GM = Cast<AShootEmUpGameMode>(UGameplayStatics::GetGameMode(this)))
    {
        if (!GM->IsGameOver())
        {
            return;
        }

        const FString ResultText = GM->IsVictory() ? TEXT("Mission Complete!") : TEXT("Game Over");
        FCanvasTextItem TextItem(FVector2D(X, Y), FText::FromString(ResultText), GEngine->GetLargeFont(), AlertColor);
        TextItem.EnableShadow(FLinearColor::Black);
        Canvas->DrawItem(TextItem);
    }
}
