# Unreal Engine Shoot 'em Up Setup Instructions

Since I cannot directly access the running Unreal Editor, I have generated the C++ source code for the core game logic. Follow these steps to set up the game in your Unreal Engine project.

## 1. Project Setup
1.  Ensure you have an Unreal Engine 5 C++ project named `MCPGameProject`.
2.  If your project is named differently, you will need to rename the `MCPGAMEPROJECT_API` macro and the includes in the provided C++ files.

## 2. Source Code
I have placed the C++ source files in `games/unreal/Source/MCPGameProject/`.
Copy these files (`STGPawn.h/cpp`, `STGEnemy.h/cpp`, `STGProjectile.h/cpp`, `STGGameMode.h/cpp`) into your project's `Source/MCPGameProject/` directory.

## 3. Compilation
I have already compiled the project for you.
However, if you do not see the classes in the Editor:
1.  **Restart the Unreal Editor**. This is often required when adding new C++ classes.
2.  If you still don't see them, try clicking the **Compile** button (or Live Coding icon) in the bottom right corner of the Editor.

## 4. Blueprint Setup
Once compiled, open the Editor and create the following Blueprints:

### BP_Player (Inherits from ASTGPawn)
1.  Create a Blueprint class based on `ASTGPawn`.
2.  **Components**:
    *   Select the `ShipMesh` component and assign a Static Mesh (e.g., a spaceship or triangle).
    *   Adjust the `SpringArm` length and rotation to get a good top-down view.
3.  **Input**:
    *   Go to Project Settings -> Input.
    *   Add Axis Mappings: `MoveForward` (W=1, S=-1), `MoveRight` (D=1, A=-1).
    *   Add Action Mappings: `Fire` (Space/Mouse Left), `Special` (Q/Right Mouse).

### BP_Bullet (Inherits from ASTGProjectile)
1.  Create a Blueprint based on `ASTGProjectile`.
2.  **Visuals**: Add a Sphere Static Mesh or Particle System to the `RootComponent` or as a child.
3.  **Collision**: Ensure the Collision Component settings allow overlap with Pawns and Enemies.

### BP_Enemy (Inherits from ASTGEnemy)
1.  Create a Blueprint based on `ASTGEnemy`.
2.  **Visuals**: Assign a mesh to `MeshComp`.
3.  **Variants**: You can create child Blueprints for Enemy A, B, C, D and set the `EnemyType` variable in the Details panel for each.
    *   *Tip*: Use the Construction Script to change the Mesh or Material based on `EnemyType`.

### BP_GameMode (Inherits from ASTGGameMode)
1.  Create a Blueprint based on `ASTGGameMode`.
2.  **Settings**: Set `Default Pawn Class` to `BP_Player`.
3.  **Spawning**: The C++ code handles spawning, but you might need to adjust the `SpawnLocation` logic in `STGGameMode.cpp` if your map coordinates differ.

## 5. UI (HUD)
1.  Create a Widget Blueprint `WBP_HUD`.
2.  Add Text blocks for **Score**, **Lives**, and **Timer**.
3.  Bind these text blocks to functions that cast to `BP_Player` (for Score/Lives) and `BP_GameMode` (for Timer) to get the values.
4.  In `BP_Player`'s `BeginPlay` event, create the `WBP_HUD` widget and add it to the viewport.

## 6. Level Setup
1.  Place a `BP_GameMode` in the level or set it in World Settings.
2.  Add a background (e.g., a large plane with a scrolling material).
3.  Place a `PlayerStart` actor.

## 7. Testing
Press Play. The game should:
*   Spawn enemies progressively.
*   Allow you to move and shoot.
*   Track score and lives.
*   End after 90 seconds.
