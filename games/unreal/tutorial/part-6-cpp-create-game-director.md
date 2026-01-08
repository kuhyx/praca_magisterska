# Part 6 (C++): Create Game Director

[← Previous: Part 5 (C++) - Create Enemy Spawner](part-5-cpp-create-spawner.md) | [Back to Index](README.md) | [Next: Part 7 (C++) - Create UI →](part-7-cpp-create-ui.md)

---

## Overview

Create a Game Director to manage the game timer, victory/defeat conditions, and overall game state.

**Time:** ~10 minutes

---

## Step 6.1: Create STGGameDirector C++ Class

1. **Tools → New C++ Class** → Actor → Name: `STGGameDirector`
2. Wait for compilation

---

## Step 6.2: Define Game Director Variables

### STGGameDirector.h:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGGameDirector.generated.h"

UCLASS()
class BULLETHELLGAME_API ASTGGameDirector : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGGameDirector();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game")
    float GameDuration = 300.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    float ElapsedTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    bool bGameActive = true;

    void OnPlayerDied();
    void OnVictory();
    void OnGameOver();
};
```

---

## Step 6.3: Implement Game Director

### STGGameDirector.cpp:

```cpp
#include "STGGameDirector.h"
#include "Kismet/GameplayStatics.h"

ASTGGameDirector::ASTGGameDirector()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ASTGGameDirector::BeginPlay()
{
    Super::BeginPlay();
    ElapsedTime = 0.0f;
    bGameActive = true;
}

void ASTGGameDirector::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    if (!bGameActive)
        return;

    ElapsedTime += DeltaTime;

    // Check for victory (survived full duration)
    if (ElapsedTime >= GameDuration)
    {
        OnVictory();
    }
}

void ASTGGameDirector::OnPlayerDied()
{
    OnGameOver();
}

void ASTGGameDirector::OnVictory()
{
    bGameActive = false;
    UE_LOG(LogTemp, Warning, TEXT("VICTORY! You survived %f seconds!"), ElapsedTime);
    
    // Pause game
    UGameplayStatics::SetGamePaused(GetWorld(), true);
}

void ASTGGameDirector::OnGameOver()
{
    bGameActive = false;
    UE_LOG(LogTemp, Warning, TEXT("GAME OVER! Survived %f seconds"), ElapsedTime);
    
    // Pause game
    UGameplayStatics::SetGamePaused(GetWorld(), true);
}
```

---

## Step 6.4: Update Player Death to Notify Director

### In STGPawn.cpp, update HandleDeath():

```cpp
void ASTGPawn::HandleDeath()
{
    SetActorHiddenInGame(true);
    
    // Find and notify Game Director
    TArray<AActor*> FoundDirectors;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGGameDirector::StaticClass(), FoundDirectors);
    if (FoundDirectors.Num() > 0)
    {
        ASTGGameDirector* Director = Cast<ASTGGameDirector>(FoundDirectors[0]);
        if (Director)
        {
            Director->OnPlayerDied();
        }
    }
}
```

Add include: `#include "STGGameDirector.h"`

---

## Step 6.5: Place Director in Level and Test

1. Drag `STGGameDirector` from C++ Classes into level
2. Press Play
3. Wait 5 minutes OR let player die

### Expected Result:

- ✅ Timer counts up from 0
- ✅ After 300 seconds: "VICTORY!" message, game pauses
- ✅ If player dies: "GAME OVER!" message, game pauses

---

[← Previous: Part 5 (C++) - Create Enemy Spawner](part-5-cpp-create-spawner.md) | [Back to Index](README.md) | [Next: Part 7 (C++) - Create UI →](part-7-cpp-create-ui.md)
