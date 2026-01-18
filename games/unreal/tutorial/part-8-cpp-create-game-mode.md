# Part 8 (C++): Create Game Mode

[← Previous: Part 7 (C++) - Create UI](part-7-cpp-create-ui.md) | [Back to Index](README.md) | [Next: Part 9 (C++) - Polish & Debug Features →](part-9-cpp-polish.md)

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

> **⚠️ IMPORTANT:** Replace `YOURPROJECTNAME_API` with your actual project's API macro (e.g., `BULLETHELLCPP_API`).

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "STGGameMode.generated.h"

UCLASS()
class YOURPROJECTNAME_API ASTGGameMode : public AGameModeBase
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
    // Default to C++ pawn class
    // We'll override this in a Blueprint child to use BP_Player
    DefaultPawnClass = ASTGPawn::StaticClass();
    
    bStartPlayersAsSpectators = false;
}
```

> **Note:** We use the C++ STGPawn as default. In the next step, we'll create a Blueprint child of this GameMode to set BP_Player as the default pawn. This approach is more flexible than hardcoding Blueprint paths, which can break if files are moved.

---

## Step 8.3: Create BP_STGGameMode Blueprint

We create a Blueprint child of STGGameMode to configure BP_Player as the default pawn:

1. **Content Browser** → Right-click in empty space
2. Select **Blueprint Class**
3. In the popup, expand **All Classes** and search for `STGGameMode`
4. Select **STGGameMode** as parent → Click **Select**
5. Name: `BP_STGGameMode`
6. **Double-click** to open the Blueprint
7. In **Class Defaults** panel (right side):
   - Find **Default Pawn Class**
   - Click dropdown → Select `BP_Player`
8. **Compile** (top toolbar) → **Save**

> **Why use a Blueprint GameMode?**
> - Avoids hardcoded paths that break when files move
> - Allows designers to change settings without recompiling
> - Standard Unreal Engine practice for configuration

---

## Step 8.4: Set Game Mode in Project Settings

1. **Edit → Project Settings**
2. **Project → Maps & Modes**
3. Under "Default Modes":
   - **Default GameMode** → Select `BP_STGGameMode` (the Blueprint, not the C++ class)
4. Close Project Settings

> **⚠️ Important:** Make sure to select `BP_STGGameMode`, not `STGGameMode`. The Blueprint version has BP_Player configured as the default pawn.

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

[← Previous: Part 7 (C++) - Create UI](part-7-cpp-create-ui.md) | [Back to Index](README.md) | [Next: Part 9 (C++) - Polish & Debug Features →](part-9-cpp-polish.md)
