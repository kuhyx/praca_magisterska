#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "ShootEmUpEnemy.generated.h"

class USphereComponent;
class UStaticMeshComponent;
class AShootEmUpProjectile;
class AShootEmUpGameMode;
class UMaterialInterface;

UENUM(BlueprintType)
enum class EEnemyArchetype : uint8
{
    TypeA,
    TypeB,
    TypeC,
    TypeD
};

UCLASS(Abstract)
class MAGISTERKA_API AShootEmUpEnemy : public APawn
{
    GENERATED_BODY()

public:
    AShootEmUpEnemy();

    virtual void Tick(float DeltaSeconds) override;
    virtual void BeginPlay() override;

    void SetArchetype(EEnemyArchetype InType);
    EEnemyArchetype GetArchetype() const { return Archetype; }

    void HandleProjectileImpact(float IncomingDamage, AShootEmUpProjectile* FromProjectile);

    int32 GetScoreValue() const { return ScoreValue; }

    void SetPlayerReference(APawn* InPlayer);

protected:
    virtual FVector ComputeDesiredVelocity(float DeltaSeconds);
    virtual void ConfigureAppearance();
    virtual void HandleShooting(float DeltaSeconds);

    void ShootRadialPattern(int32 BulletCount, float SpreadAngleDeg, float BulletSpeed, float DamageScalar, const FLinearColor& ColorTint);
    void ShootDirectedAtPlayer(int32 BulletCount, float AngleVarianceDeg, float BulletSpeed, float DamageScalar, const FLinearColor& ColorTint);

    void RequestDestroy();

    UPROPERTY(VisibleAnywhere, Category = "Components")
    USphereComponent* CollisionComponent;

    UPROPERTY(VisibleAnywhere, Category = "Components")
    UStaticMeshComponent* MeshComponent;

    UPROPERTY(EditDefaultsOnly, Category = "Enemy")
    float MoveSpeed;

    UPROPERTY(EditDefaultsOnly, Category = "Enemy")
    int32 MaxHealth;

    UPROPERTY(EditDefaultsOnly, Category = "Enemy")
    float ShootInterval;

    UPROPERTY(EditDefaultsOnly, Category = "Enemy")
    int32 ScoreValue;

    UPROPERTY(EditDefaultsOnly, Category = "Enemy")
    float BulletDamage;

    UPROPERTY(EditDefaultsOnly, Category = "Enemy")
    float BulletSpeed;

    UPROPERTY(EditDefaultsOnly, Category = "Enemy")
    float Lifetime;

    float TimeSinceLastShot;
    int32 CurrentHealth;
    float TimeAlive;
    float HorizontalPhase;

    TWeakObjectPtr<APawn> PlayerPawn;
    TWeakObjectPtr<AShootEmUpGameMode> CachedGameMode;

private:
    EEnemyArchetype Archetype;

    UStaticMesh* MeshTypeA;
    UStaticMesh* MeshTypeB;
    UStaticMesh* MeshTypeC;
    UStaticMesh* MeshTypeD;
    UMaterialInterface* BaseMaterial;

    UFUNCTION()
    void OnEnemyOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
