#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "STGHUD.generated.h"

UCLASS()
class MCPGAMEPROJECT_API ASTGHUD : public AHUD
{
	GENERATED_BODY()
	
public:
	ASTGHUD();

	virtual void DrawHUD() override;

protected:
	virtual void BeginPlay() override;

private:
	// Fonts
	UFont* HUDFont;
	
	void DrawScore();
	void DrawLives();
	void DrawTimer();
	void DrawGameOver();
	void DrawVictory();
	void DrawLevelUp();
	
	// Cached values
	int32 CurrentScore;
	int32 CurrentLives;
	float TimeRemaining;
	bool bIsGameOver;
	bool bIsVictory;
	int32 CurrentLevel;
	float LevelUpDisplayTime;
};
