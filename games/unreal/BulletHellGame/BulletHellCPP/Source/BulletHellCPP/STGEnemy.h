#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGEnemy.generated.h"

class UStaticMeshComponent;
class UBoxComponent;

UCLASS()
class BULLETHELLCPP_API ASTGEnemy : public AActor
{
    GENERATED_BODY()
    
public:    
    ASTGEnemy();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

    // ===== COMPONENTS =====
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UBoxComponent* CollisionComp;

    // ===== HEALTH & SCORE (copy-paste all 15 variables!) =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxHealth = 12;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentHealth = 12;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 ScoreValue = 50;

    // ===== MOVEMENT =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VerticalSpeed = 220.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalAmplitude = 250.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalFrequency = 1.8f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float DespawnY = -750.0f;

    // ===== FIRING =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireInterval = 0.35f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 BulletsPerBurst = 20;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BurstSpread = 360.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletSpeed = 1000.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletLifetime = 6.0f;

    // ===== FUNCTIONS =====
    void Fire();
    void HandleDamage(float DamageAmount);

    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, 
                        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, 
                        bool bFromSweep, const FHitResult& SweepResult);

private:
    FTimerHandle TimerHandle_Fire;
    float StartY = 0.0f;  // Starting Y position for wave pattern
    float WaveSeed = 0.0f;
    float ElapsedTime = 0.0f;
};