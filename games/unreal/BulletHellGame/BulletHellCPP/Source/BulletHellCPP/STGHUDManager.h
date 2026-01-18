#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGHUDManager.generated.h"

UCLASS()
class BULLETHELLCPP_API ASTGHUDManager : public AActor
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

    UFUNCTION(BlueprintCallable, Category = "UI")
    void ShowVictory();

    UFUNCTION(BlueprintCallable, Category = "UI")
    void ShowGameOver();

private:
    class UUserWidget* HUDWidget;
};