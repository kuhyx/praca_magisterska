#include "STGGameMode.h"
#include "STGPawn.h"

ASTGGameMode::ASTGGameMode()
{
    // Default to C++ pawn class
    // Override this in Project Settings or create a Blueprint child of STGGameMode
    // and set DefaultPawnClass to BP_Player there
    DefaultPawnClass = ASTGPawn::StaticClass();
    
    bStartPlayersAsSpectators = false;
}