#include "STGHUD.h"
#include "Engine/Canvas.h"
#include "Engine/Font.h"
#include "Kismet/GameplayStatics.h"
#include "STGPawn.h"
#include "STGGameMode.h"

ASTGHUD::ASTGHUD()
{
	// Load default engine font
	static ConstructorHelpers::FObjectFinder<UFont> FontFinder(TEXT("/Engine/EngineFonts/Roboto"));
	if (FontFinder.Succeeded())
	{
		HUDFont = FontFinder.Object;
	}

	CurrentScore = 0;
	CurrentLives = 2;
	TimeRemaining = 90.0f;
	bIsGameOver = false;
	bIsVictory = false;
	CurrentLevel = 1;
	LevelUpDisplayTime = 0.0f;
}

void ASTGHUD::BeginPlay()
{
	Super::BeginPlay();
}

void ASTGHUD::DrawHUD()
{
	Super::DrawHUD();

	if (!Canvas) return;

	// Get player data
	ASTGPawn* PlayerPawn = Cast<ASTGPawn>(UGameplayStatics::GetPlayerPawn(GetWorld(), 0));
	if (PlayerPawn)
	{
		CurrentScore = PlayerPawn->Score;
		CurrentLives = PlayerPawn->Lives;
		
		// Check for level up
		if (PlayerPawn->Level > CurrentLevel)
		{
			CurrentLevel = PlayerPawn->Level;
			LevelUpDisplayTime = 2.0f; // Show for 2 seconds
		}
	}

	// Get game mode data
	ASTGGameMode* GameMode = Cast<ASTGGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
	if (GameMode)
	{
		TimeRemaining = GameMode->TimeRemaining;
		bIsGameOver = GameMode->bIsGameOver;
		bIsVictory = GameMode->bIsVictory;
	}

	// Draw HUD elements
	DrawScore();
	DrawLives();
	DrawTimer();
	
	// Update level up timer
	if (LevelUpDisplayTime > 0.0f)
	{
		LevelUpDisplayTime -= GetWorld()->GetDeltaSeconds();
		DrawLevelUp();
	}

	if (bIsGameOver)
	{
		if (bIsVictory)
		{
			DrawVictory();
		}
		else
		{
			DrawGameOver();
		}
	}
}

void ASTGHUD::DrawScore()
{
	// Score in upper left
	FString ScoreText = FString::Printf(TEXT("SCORE: %d"), CurrentScore);
	
	// Draw shadow
	DrawText(ScoreText, FLinearColor::Black, 22.0f, 22.0f, HUDFont, 1.5f, false);
	// Draw text
	DrawText(ScoreText, FLinearColor::White, 20.0f, 20.0f, HUDFont, 1.5f, false);
	
	// Draw level
	FString LevelText = FString::Printf(TEXT("LEVEL: %d"), CurrentLevel);
	DrawText(LevelText, FLinearColor::Black, 22.0f, 52.0f, HUDFont, 1.2f, false);
	DrawText(LevelText, FLinearColor::Yellow, 20.0f, 50.0f, HUDFont, 1.2f, false);
}

void ASTGHUD::DrawLives()
{
	// Lives display below score
	FString LivesText = TEXT("LIVES: ");
	for (int32 i = 0; i < CurrentLives; i++)
	{
		LivesText += TEXT("♥ ");
	}
	
	DrawText(LivesText, FLinearColor::Black, 22.0f, 82.0f, HUDFont, 1.2f, false);
	DrawText(LivesText, FLinearColor::Red, 20.0f, 80.0f, HUDFont, 1.2f, false);
}

void ASTGHUD::DrawTimer()
{
	// Timer in upper right
	int32 Minutes = FMath::FloorToInt(TimeRemaining / 60.0f);
	int32 Seconds = FMath::FloorToInt(FMath::Fmod(TimeRemaining, 60.0f));
	
	FString TimerText = FString::Printf(TEXT("TIME: %d:%02d"), Minutes, Seconds);
	
	// Get text size for right alignment
	float TextWidth = 0.0f;
	float TextHeight = 0.0f;
	GetTextSize(TimerText, TextWidth, TextHeight, HUDFont, 1.5f);
	
	float XPos = Canvas->SizeX - TextWidth - 20.0f;
	
	// Change color based on time remaining
	FLinearColor TimerColor = FLinearColor::White;
	if (TimeRemaining <= 10.0f)
	{
		TimerColor = FLinearColor::Red;
	}
	else if (TimeRemaining <= 30.0f)
	{
		TimerColor = FLinearColor::Yellow;
	}
	
	DrawText(TimerText, FLinearColor::Black, XPos + 2.0f, 22.0f, HUDFont, 1.5f, false);
	DrawText(TimerText, TimerColor, XPos, 20.0f, HUDFont, 1.5f, false);
}

void ASTGHUD::DrawGameOver()
{
	// Game Over in center
	FString GameOverText = TEXT("GAME OVER");
	
	float TextWidth = 0.0f;
	float TextHeight = 0.0f;
	GetTextSize(GameOverText, TextWidth, TextHeight, HUDFont, 3.0f);
	
	float XPos = (Canvas->SizeX - TextWidth) / 2.0f;
	float YPos = (Canvas->SizeY - TextHeight) / 2.0f;
	
	// Draw background box
	DrawRect(FLinearColor(0.0f, 0.0f, 0.0f, 0.7f), XPos - 20.0f, YPos - 10.0f, TextWidth + 40.0f, TextHeight + 20.0f);
	
	DrawText(GameOverText, FLinearColor::Black, XPos + 4.0f, YPos + 4.0f, HUDFont, 3.0f, false);
	DrawText(GameOverText, FLinearColor::Red, XPos, YPos, HUDFont, 3.0f, false);
	
	// Final score
	FString FinalScoreText = FString::Printf(TEXT("Final Score: %d"), CurrentScore);
	GetTextSize(FinalScoreText, TextWidth, TextHeight, HUDFont, 2.0f);
	XPos = (Canvas->SizeX - TextWidth) / 2.0f;
	DrawText(FinalScoreText, FLinearColor::White, XPos, YPos + 60.0f, HUDFont, 2.0f, false);
}

void ASTGHUD::DrawVictory()
{
	// Victory in center
	FString VictoryText = TEXT("VICTORY!");
	
	float TextWidth = 0.0f;
	float TextHeight = 0.0f;
	GetTextSize(VictoryText, TextWidth, TextHeight, HUDFont, 3.0f);
	
	float XPos = (Canvas->SizeX - TextWidth) / 2.0f;
	float YPos = (Canvas->SizeY - TextHeight) / 2.0f;
	
	// Draw background box
	DrawRect(FLinearColor(0.0f, 0.2f, 0.0f, 0.7f), XPos - 20.0f, YPos - 10.0f, TextWidth + 40.0f, TextHeight + 20.0f);
	
	DrawText(VictoryText, FLinearColor::Black, XPos + 4.0f, YPos + 4.0f, HUDFont, 3.0f, false);
	DrawText(VictoryText, FLinearColor::Green, XPos, YPos, HUDFont, 3.0f, false);
	
	// Final score
	FString FinalScoreText = FString::Printf(TEXT("Final Score: %d"), CurrentScore);
	GetTextSize(FinalScoreText, TextWidth, TextHeight, HUDFont, 2.0f);
	XPos = (Canvas->SizeX - TextWidth) / 2.0f;
	DrawText(FinalScoreText, FLinearColor::White, XPos, YPos + 60.0f, HUDFont, 2.0f, false);
}

void ASTGHUD::DrawLevelUp()
{
	// Level up flash in center
	FString LevelUpText = FString::Printf(TEXT("LEVEL UP! Level %d"), CurrentLevel);
	
	float TextWidth = 0.0f;
	float TextHeight = 0.0f;
	GetTextSize(LevelUpText, TextWidth, TextHeight, HUDFont, 2.5f);
	
	float XPos = (Canvas->SizeX - TextWidth) / 2.0f;
	float YPos = Canvas->SizeY * 0.3f;
	
	// Flash effect based on time
	float Alpha = FMath::Sin(LevelUpDisplayTime * 10.0f) * 0.3f + 0.7f;
	FLinearColor FlashColor = FLinearColor(1.0f, 1.0f, 0.0f, Alpha);
	
	DrawText(LevelUpText, FLinearColor::Black, XPos + 3.0f, YPos + 3.0f, HUDFont, 2.5f, false);
	DrawText(LevelUpText, FlashColor, XPos, YPos, HUDFont, 2.5f, false);
}
