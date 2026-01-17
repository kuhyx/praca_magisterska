#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
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

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Game")
    float GameDuration = 300.0f;

    // Debug: Set to true for 10-second game (quick victory testing)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Debug")
    bool bDebugQuickGame = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    float ElapsedTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game")
    bool bGameActive = true;

    void OnPlayerDied();
    void OnVictory();
    void OnGameOver();
};