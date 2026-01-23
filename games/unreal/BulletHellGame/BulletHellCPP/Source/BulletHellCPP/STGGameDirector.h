#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGGameSettings.h"
#include "STGGameDirector.generated.h"

UCLASS()
class BULLETHELLCPP_API ASTGGameDirector : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGGameDirector();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    // ===== PLAY AREA BOUNDS =====
    // Central definition of play area - other systems read from here
    // Defaults come from STGGameSettings.h
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Play Area")
    FVector2D PlayAreaMin = FVector2D(STG::PlayArea::MinX, STG::PlayArea::MinY);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Play Area")
    FVector2D PlayAreaMax = FVector2D(STG::PlayArea::MaxX, STG::PlayArea::MaxY);

    // Get the play area dimensions
    UFUNCTION(BlueprintCallable, Category = "Play Area")
    FVector2D GetPlayAreaSize() const { return PlayAreaMax - PlayAreaMin; }

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game")
    float GameDuration = STG::Game::DefaultDuration;

    // Debug: Set to true for 10-second game (quick victory testing)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Debug")
    bool bDebugQuickGame = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    float ElapsedTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    bool bGameActive = true;

    // Cleanup phase: spawning done, waiting for all enemies to clear
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    bool bInCleanupPhase = false;

    // Auto-quit after game ends (for benchmarking)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Benchmark")
    bool bAutoQuit = false;

    void OnPlayerDied();
    void OnVictory();
    void OnGameOver();
    void CheckCleanupVictory();  // Check if all enemies cleared
};