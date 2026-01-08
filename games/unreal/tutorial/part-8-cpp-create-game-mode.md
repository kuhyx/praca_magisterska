# Part 8 (C++): Create Game Mode

[← Previous: Part 7 (C++) - Create UI](part-7-cpp-create-ui.md) | [Back to Index](README.md) | [Next: Part 9 (C++) - Final Setup →](part-9-cpp-final-setup.md)

---

## Overview

Create a custom Game Mode to set the default pawn class and manage game rules.

**Time:** ~5 minutes

---

## Step 8.1: Create STGGameMode C++ Class

1. **Tools → New C++ Class**
2. Choose **"Game Mode Base"** as parent
3. Name: `STGGameMode`
4. Create Class

---

## Step 8.2: Define Game Mode

### STGGameMode.h:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "STGGameMode.generated.h"

UCLASS()
class BULLETHELLGAME_API ASTGGameMode : public AGameModeBase
{
    GENERATED_BODY()
    
public:
    ASTGGameMode();
};
```

### STGGameMode.cpp:

```cpp
#include "STGGameMode.h"
#include "STGPawn.h"

ASTGGameMode::ASTGGameMode()
{
    // Set default pawn class to our player
    DefaultPawnClass = ASTGPawn::StaticClass();
    
    // Disable auto-possess (we'll handle spawning ourselves)
    bStartPlayersAsSpectators = false;
}
```

---

## Step 8.3: Set Game Mode in Project Settings

1. **Edit → Project Settings**
2. **Project → Maps & Modes**
3. Under "Default Modes":
   - **Default GameMode** → Select `STGGameMode`
4. Close Project Settings

---

## Step 8.4: Test

Create a new level or use existing one:

1. **File → New Level** → Empty Level
2. Save as `BulletHellLevel`
3. Add:
   - Player Start (from Place Actors panel)
   - STGEnemySpawner
   - STGGameDirector
   - STGHUDManager
   - Directional Light (for visibility)

4. Press Play

### Expected Result:

- ✅ Player automatically spawns at Player Start location
- ✅ No need to manually drag BP_Player into level
- ✅ All game systems work together

---

[← Previous: Part 7 (C++) - Create UI](part-7-cpp-create-ui.md) | [Back to Index](README.md) | [Next: Part 9 (C++) - Final Setup →](part-9-cpp-final-setup.md)
