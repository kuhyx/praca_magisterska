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

1. **Add a Canvas Panel** (if not already present):
   - Drag **Canvas Panel** from Palette → Panel onto the root
   - This is your container for all UI elements

2. **Add Text blocks** (drag each from Palette → Common onto the Canvas Panel):
   - Drag a **Text** widget → rename to `txt_Score` (click on it in Hierarchy, press F2)
   - Drag another **Text** widget → rename to `txt_Lives`
   - Drag another **Text** widget → rename to `txt_Timer`

3. **Position them** (select each and set in Details panel → Slot):
   - `txt_Score`: Position X=20, Y=20
   - `txt_Lives`: Position X=20, Y=50
   - `txt_Timer`: Position X=20, Y=80

4. **Style each text** (select in Hierarchy, edit in Details panel):
   - Font → Size: 24
   - Color and Opacity: White
   - Set default Text content:
     - txt_Score: `Score: 0`
     - txt_Lives: `Lives: 3`
     - txt_Timer: `Time: 300`

5. **Important: Set "Is Variable" for each text block**:
   - Select `txt_Score` in Hierarchy
   - In Details panel, check **Is Variable** ✓
   - Repeat for `txt_Lives` and `txt_Timer`
   - (This allows C++ to find them by name)

6. **Compile and Save**

---

## Step 7.3: Create HUD Manager C++ Class

We'll create a simple C++ class to update the UI.

1. **Tools → New C++ Class** → **Actor** → Name: `STGHUDManager`
2. Wait for compilation

### STGHUDManager.h

Replace content with:

> **⚠️ IMPORTANT:** Replace `YOURPROJECTNAME_API` with your actual project's API macro (e.g., `BULLETHELLCPP_API`).

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGHUDManager.generated.h"

UCLASS()
class YOURPROJECTNAME_API ASTGHUDManager : public AActor
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

4. Update `STGPawn` to update score/lives when they change:

First, add the include at the top of `STGPawn.cpp`:
```cpp
#include "STGHUDManager.h"
```

Then create a helper function to find and update the HUD. Add this private method to `STGPawn.h`:
```cpp
private:
    void UpdateHUD();
```

Add the implementation in `STGPawn.cpp`:
```cpp
void ASTGPawn::UpdateHUD()
{
    TArray<AActor*> FoundManagers;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGHUDManager::StaticClass(), FoundManagers);
    if (FoundManagers.Num() > 0)
    {
        ASTGHUDManager* HUDMgr = Cast<ASTGHUDManager>(FoundManagers[0]);
        if (HUDMgr)
        {
            HUDMgr->UpdateScore(Score);
            HUDMgr->UpdateLives(CurrentLives);
        }
    }
}
```

Call `UpdateHUD()` in these places:

In `AddScore()`:
```cpp
void ASTGPawn::AddScore(int32 Points)
{
    Score += Points;
    UpdateHUD();
}
```

In `TakeHit()` (after updating CurrentLives):
```cpp
void ASTGPawn::TakeHit(int32 Damage)
{
    // ... existing damage code ...
    CurrentLives = FMath::Clamp(CurrentLives - Damage, 0, MaxLives);
    UpdateHUD();  // Add this line
    // ... rest of function ...
}
```

In `BeginPlay()` (to initialize HUD with starting values):
```cpp
void ASTGPawn::BeginPlay()
{
    Super::BeginPlay();
    CurrentLives = MaxLives;
    
    // ... existing input setup code ...
    
    // Initialize HUD
    UpdateHUD();
}
```

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
