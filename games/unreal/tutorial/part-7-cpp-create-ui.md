# Part 7 (C++): Create UI

[← Previous: Part 6 (C++) - Create Game Director](part-6-cpp-create-game-director.md) | [Back to Index](README.md) | [Next: Part 8 (C++) - Create Game Mode →](part-8-cpp-create-game-mode.md)

---

## Overview

For UI, we use **Widget Blueprints** for visual layout (drag-and-drop is better for UI design), but bind to C++ properties for data.

**Time:** ~15 minutes

---

## Step 7.1: Create Widget Blueprint

1. Content Browser → UI folder
2. Right-click → **User Interface → Widget Blueprint**
3. Name: `WBP_HUD`
4. Double-click to open Widget Designer

---

## Step 7.2: Design HUD Layout

In Widget Designer:

1. **Add Text blocks** (from Palette → Common):
   - `txt_Score` - Display score
   - `txt_Lives` - Display lives
   - `txt_Timer` - Display time remaining

2. **Position them** (top-left corner):
   - Score: Top-left (0, 0)
   - Lives: Below score (0, 30)
   - Timer: Below lives (0, 60)

3. **Style text:**
   - Font Size: 24
   - Color: White
   - Set default text: "Score: 0", "Lives: 3", "Time: 300"

4. **Compile and Save**

---

## Step 7.3: Create HUD Manager C++ Class

We'll create a simple C++ class to update the UI.

### Create STGHUDManager.h:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGHUDManager.generated.h"

UCLASS()
class BULLETHELLGAME_API ASTGHUDManager : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGHUDManager();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UI")
    TSubclassOf<class UUserWidget> HUDWidgetClass;

    UFUNCTION(BlueprintCallable, Category = "UI")
    void UpdateScore(int32 NewScore);

    UFUNCTION(BlueprintCallable, Category = "UI")
    void UpdateLives(int32 NewLives);

    UFUNCTION(BlueprintCallable, Category = "UI")
    void UpdateTimer(float TimeRemaining);

private:
    class UUserWidget* HUDWidget;
};
```

### STGHUDManager.cpp:

```cpp
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
```

---

## Step 7.4: Integrate HUD with Game

1. Place `STGHUDManager` in level
2. Select it, in Details panel:
   - Set **HUD Widget Class** → `WBP_HUD`

3. Update `STGGameDirector` to update timer:

```cpp
void ASTGGameDirector::Tick(float DeltaTime)
{
    // ... existing code ...
    
    // Update HUD
    TArray<AActor*> FoundManagers;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGHUDManager::StaticClass(), FoundManagers);
    if (FoundManagers.Num() > 0)
    {
        ASTGHUDManager* HUDMgr = Cast<ASTGHUDManager>(FoundManagers[0]);
        if (HUDMgr)
        {
            HUDMgr->UpdateTimer(GameDuration - ElapsedTime);
        }
    }
}
```

4. Update `STGPawn` to update score/lives when they change

---

## Step 7.5: Test UI

Press Play

### Expected Result:

**In Play Mode:**
- ✅ UI appears in top-left corner
- ✅ "Score: 0", "Lives: 3", "Time: 300" displayed
- ✅ Timer counts down from 300
- ✅ Score increases when enemies are destroyed
- ✅ Lives decrease when player is hit
- ✅ Text is readable (white on dark background)

---

[← Previous: Part 6 (C++) - Create Game Director](part-6-cpp-create-game-director.md) | [Back to Index](README.md) | [Next: Part 8 (C++) - Create Game Mode →](part-8-cpp-create-game-mode.md)
