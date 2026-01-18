#include "STGHUDManager.h"
#include "Blueprint/UserWidget.h"
#include "Components/TextBlock.h"

ASTGHUDManager::ASTGHUDManager()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ASTGHUDManager::BeginPlay()
{
    Super::BeginPlay();
    
    if (HUDWidgetClass)
    {
        HUDWidget = CreateWidget<UUserWidget>(GetWorld(), HUDWidgetClass);
        if (HUDWidget)
        {
            HUDWidget->AddToViewport();
        }
    }
}

void ASTGHUDManager::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void ASTGHUDManager::UpdateScore(int32 NewScore)
{
    if (HUDWidget)
    {
        UTextBlock* ScoreText = Cast<UTextBlock>(HUDWidget->GetWidgetFromName(TEXT("txt_Score")));
        if (ScoreText)
        {
            ScoreText->SetText(FText::Format(FText::FromString("Score: {0}"), NewScore));
        }
    }
}

void ASTGHUDManager::UpdateLives(int32 NewLives)
{
    if (HUDWidget)
    {
        UTextBlock* LivesText = Cast<UTextBlock>(HUDWidget->GetWidgetFromName(TEXT("txt_Lives")));
        if (LivesText)
        {
            LivesText->SetText(FText::Format(FText::FromString("Lives: {0}"), NewLives));
        }
    }
}

void ASTGHUDManager::UpdateTimer(float TimeRemaining)
{
    if (HUDWidget)
    {
        UTextBlock* TimerText = Cast<UTextBlock>(HUDWidget->GetWidgetFromName(TEXT("txt_Timer")));
        if (TimerText)
        {
            int32 Seconds = FMath::CeilToInt(TimeRemaining);
            TimerText->SetText(FText::Format(FText::FromString("Time: {0}s"), Seconds));
        }
    }
}

void ASTGHUDManager::ShowVictory()
{
    if (HUDWidget)
    {
        // Try to find and show victory text
        UTextBlock* ResultText = Cast<UTextBlock>(HUDWidget->GetWidgetFromName(TEXT("txt_Result")));
        if (ResultText)
        {
            ResultText->SetText(FText::FromString("VICTORY!"));
            ResultText->SetColorAndOpacity(FSlateColor(FLinearColor::Green));
            ResultText->SetVisibility(ESlateVisibility::Visible);
        }
    }
}

void ASTGHUDManager::ShowGameOver()
{
    if (HUDWidget)
    {
        // Try to find and show game over text
        UTextBlock* ResultText = Cast<UTextBlock>(HUDWidget->GetWidgetFromName(TEXT("txt_Result")));
        if (ResultText)
        {
            ResultText->SetText(FText::FromString("GAME OVER"));
            ResultText->SetColorAndOpacity(FSlateColor(FLinearColor::Red));
            ResultText->SetVisibility(ESlateVisibility::Visible);
        }
    }
}