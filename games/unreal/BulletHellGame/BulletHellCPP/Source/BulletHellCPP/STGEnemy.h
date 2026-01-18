#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGGameSettings.h"
#include "STGEnemy.generated.h"

class UStaticMeshComponent;
class UBoxComponent;

// Enemy types - ordered by difficulty (easiest to hardest)
UENUM(BlueprintType)
enum class EEnemyType : uint8
{
    Fodder,     // Easiest: Very slow, no bullets, 1 HP
    Runner,     // Fast but harmless: Quick, no bullets, low HP
    Turret,     // Slow shooter: Slow, shoots lots, medium tanky
    Tank        // Hardest: Slow, bullet hell, very tanky
};

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

    // ===== ENEMY TYPE =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    EEnemyType EnemyType = EEnemyType::Fodder;

    // Initialize stats based on enemy type (call after spawning)
    void InitializeFromType(EEnemyType Type);

    // ===== HEALTH & SCORE =====
    // Defaults from STGGameSettings.h (Fodder enemy type - easiest)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxHealth = STG::Enemy::Fodder::Health;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 CurrentHealth = STG::Enemy::Fodder::Health;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 ScoreValue = STG::Enemy::Fodder::ScoreValue;

    // ===== MOVEMENT =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float VerticalSpeed = STG::Enemy::Fodder::VerticalSpeed;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalAmplitude = STG::Enemy::Fodder::HorizontalAmplitude;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float HorizontalFrequency = STG::Enemy::Fodder::HorizontalFrequency;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float DespawnY = STG::Enemy::DespawnY;

    // ===== BOUNDARIES =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BoundsMinY = STG::PlayArea::MinY;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BoundsMaxY = STG::PlayArea::MaxY;

    // ===== FIRING =====
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float FireInterval = STG::Enemy::Fodder::FireInterval;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 BulletsPerBurst = STG::Enemy::Fodder::BulletsPerBurst;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float BurstSpread = STG::Enemy::Fodder::BurstSpread;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletSpeed = STG::Enemy::Fodder::BulletSpeed;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float EnemyBulletLifetime = STG::Enemy::BulletLifetime;

    // ===== VFX =====
    // Niagara effect for when enemy takes damage
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VFX")
    class UNiagaraSystem* HitEffect;

    // Niagara effect for when enemy dies (GPU-heavy explosion)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VFX")
    class UNiagaraSystem* DeathEffect;

    // Number of particles for death explosion (higher = more GPU load)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VFX")
    int32 DeathParticleCount = STG::VFX::DeathParticleCount;

    // ===== FUNCTIONS =====
    void Fire();
    void HandleDamage(float DamageAmount);
    void SpawnHitEffect();
    void SpawnDeathEffect();

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