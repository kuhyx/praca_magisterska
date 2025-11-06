#include "ShootEmUpGameMode.h"
#include "ShootEmUpPlayerPawn.h"
#include "ShootEmUpProjectile.h"
#include "ShootEmUpHUD.h"
#include "BackgroundScroller.h"
#include "DrawDebugHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"

AShootEmUpGameMode::AShootEmUpGameMode()
{
    PrimaryActorTick.bCanEverTick = true;

    DefaultPawnClass = AShootEmUpPlayerPawn::StaticClass();
    HUDClass = AShootEmUpHUD::StaticClass();

    GameDuration = 90.f;
    InitialSpawnInterval = 2.2f;
    MinimumSpawnInterval = 0.3f;
    PlayerSpawnLocation = FVector(0.f, -800.f, 0.f);

    ElapsedTime = 0.f;
    CurrentSpawnInterval = InitialSpawnInterval;
    Score = 0;
    LivesRemaining = 2;
    PlayerLevel = 1;
    bGameOver = false;
    bVictory = false;

    SpawnSteps.Add(FEnemySpawnStep(0.f, 2.2f, EEnemyArchetype::TypeA));
    SpawnSteps.Add(FEnemySpawnStep(20.f, 1.6f, EEnemyArchetype::TypeB));
    SpawnSteps.Add(FEnemySpawnStep(40.f, 1.2f, EEnemyArchetype::TypeC));
    SpawnSteps.Add(FEnemySpawnStep(60.f, 0.8f, EEnemyArchetype::TypeD));
}

void AShootEmUpGameMode::BeginPlay()
{
    Super::BeginPlay();

    InitializePlayer();
    InitializeBackground();

    ScheduleNextSpawn(InitialSpawnInterval);
}

void AShootEmUpGameMode::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    if (bGameOver)
    {
        return;
    }

    UpdateTimer(DeltaSeconds);
    UpdateDifficulty(DeltaSeconds);
    CleanupDestroyedActors();

    if (ElapsedTime >= GameDuration)
    {
        if (ActiveEnemies.Num() == 0)
        {
            TriggerGameOver(true);
        }
    }
}

void AShootEmUpGameMode::NotifyEnemyKilled(AShootEmUpEnemy* Enemy)
{
    if (!Enemy)
    {
        return;
    }
    if (PlayerPawn.IsValid())
    {
        PlayerPawn->NotifyEnemyDestroyed(Enemy->GetScoreValue());
        Score = PlayerPawn->GetScore();
        PlayerLevel = PlayerPawn->GetPlayerLevel();
    }
}

void AShootEmUpGameMode::RegisterEnemyDestroyed(AShootEmUpEnemy* Enemy)
{
    ActiveEnemies.RemoveAll([Enemy](const TWeakObjectPtr<AShootEmUpEnemy>& Ptr)
    {
        return !Ptr.IsValid() || Ptr.Get() == Enemy;
    });
}

void AShootEmUpGameMode::SpawnEnemyProjectile(const FVector& Origin, const FVector& Direction, float Speed, float Damage, const FLinearColor& Tint)
{
    if (!EnemyProjectileClass)
    {
        EnemyProjectileClass = AShootEmUpProjectile::StaticClass();
    }

    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    FActorSpawnParameters Params;
    Params.Owner = this;
    AShootEmUpProjectile* Projectile = World->SpawnActor<AShootEmUpProjectile>(EnemyProjectileClass, Origin, Direction.Rotation(), Params);
    if (Projectile)
    {
        Projectile->InitProjectile(Direction, Speed, 6.f, false, Damage, Tint);
        ActiveEnemyProjectiles.Add(Projectile);
    }
}

void AShootEmUpGameMode::HandlePlayerDamaged(int32 InLivesRemaining)
{
    LivesRemaining = InLivesRemaining;
}

void AShootEmUpGameMode::HandlePlayerDeath()
{
    if (bGameOver)
    {
        return;
    }

    TriggerGameOver(false);
}

void AShootEmUpGameMode::HandlePlayerRespawnRequest()
{
    if (!PlayerPawn.IsValid())
    {
        return;
    }

    HandleScreenClearRequested();
    PlayerPawn->OnRespawn(PlayerSpawnLocation);
}

void AShootEmUpGameMode::HandleScoreUpdated(int32 NewScore)
{
    Score = NewScore;
}

void AShootEmUpGameMode::HandlePlayerLevelUp(int32 NewLevel)
{
    PlayerLevel = NewLevel;

    if (APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0))
    {
        if (AShootEmUpHUD* HUD = PC ? Cast<AShootEmUpHUD>(PC->GetHUD()) : nullptr)
        {
            const FString Message = FString::Printf(TEXT("Level %d"), NewLevel);
            HUD->SetLevelUpMessage(Message, 2.0f);
        }
    }
}

void AShootEmUpGameMode::HandleScreenClearRequested()
{
    TArray<TWeakObjectPtr<AShootEmUpProjectile>> ProjectilesCopy = ActiveEnemyProjectiles;
    for (auto& ProjectilePtr : ProjectilesCopy)
    {
        if (ProjectilePtr.IsValid())
        {
            ProjectilePtr->Destroy();
        }
    }
    ActiveEnemyProjectiles.Empty();

    TArray<AShootEmUpEnemy*> EnemiesCopy;
    for (const auto& EnemyPtr : ActiveEnemies)
    {
        if (AShootEmUpEnemy* Enemy = EnemyPtr.Get())
        {
            EnemiesCopy.Add(Enemy);
        }
    }

    for (AShootEmUpEnemy* Enemy : EnemiesCopy)
    {
        if (Enemy)
        {
            Enemy->HandleProjectileImpact(999.f, nullptr);
        }
    }

    if (UWorld* World = GetWorld())
    {
        DrawDebugSphere(World, PlayerSpawnLocation, 900.f, 32, FColor::Purple, false, 1.0f, 0, 6.f);
    }
}

void AShootEmUpGameMode::InitializePlayer()
{
    if (APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0))
    {
        if (APawn* ExistingPawn = PC->GetPawn())
        {
            PlayerPawn = Cast<AShootEmUpPlayerPawn>(ExistingPawn);
        }
        else
        {
            APawn* SpawnedPawn = PC->GetWorld()->SpawnActor<APawn>(DefaultPawnClass, PlayerSpawnLocation, FRotator::ZeroRotator);
            if (SpawnedPawn)
            {
                PC->Possess(SpawnedPawn);
                PlayerPawn = Cast<AShootEmUpPlayerPawn>(SpawnedPawn);
            }
        }
    }

    if (PlayerPawn.IsValid())
    {
        LivesRemaining = PlayerPawn->GetLivesRemaining();
        Score = PlayerPawn->GetScore();
        PlayerLevel = PlayerPawn->GetPlayerLevel();
    }
}

void AShootEmUpGameMode::InitializeBackground()
{
    if (!BackgroundClass)
    {
        BackgroundClass = ABackgroundScroller::StaticClass();
    }

    if (UWorld* World = GetWorld())
    {
        World->SpawnActor<ABackgroundScroller>(BackgroundClass, FVector::ZeroVector, FRotator::ZeroRotator);
    }
}

void AShootEmUpGameMode::ScheduleNextSpawn(float Delay)
{
    if (bGameOver)
    {
        return;
    }

    GetWorldTimerManager().SetTimer(SpawnTimerHandle, this, &AShootEmUpGameMode::OnSpawnTimerElapsed, Delay, false);
}

void AShootEmUpGameMode::SpawnEnemyByArchetype(EEnemyArchetype Archetype)
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    FVector SpawnLocation = GenerateSpawnLocation();
    FActorSpawnParameters Params;
    Params.Owner = this;
    AShootEmUpEnemy* Enemy = World->SpawnActor<AShootEmUpEnemy>(AShootEmUpEnemy::StaticClass(), SpawnLocation, FRotator::ZeroRotator, Params);
    if (Enemy)
    {
        Enemy->SetArchetype(Archetype);
        Enemy->SetPlayerReference(PlayerPawn.Get());
        ActiveEnemies.Add(Enemy);
    }
}

FVector AShootEmUpGameMode::GenerateSpawnLocation() const
{
    const float Bias = FMath::Pow(FMath::FRandRange(-1.f, 1.f), 3); // bias towards center
    const float YBias = FMath::Pow(FMath::FRandRange(-1.f, 1.f), 3);
    const float X = Bias * 900.f;
    const float Y = 1200.f + FMath::Abs(YBias) * 400.f;
    const float Z = 0.f;
    return FVector(X, Y, Z);
}

EEnemyArchetype AShootEmUpGameMode::SelectCurrentArchetype() const
{
    TArray<EEnemyArchetype> AvailableTypes;
    for (const FEnemySpawnStep& Step : SpawnSteps)
    {
        if (ElapsedTime >= Step.StartTime)
        {
            AvailableTypes.AddUnique(Step.Archetype);
        }
    }

    if (AvailableTypes.Num() == 0)
    {
        AvailableTypes.Add(EEnemyArchetype::TypeA);
    }

    const int32 RandomIndex = FMath::RandRange(0, AvailableTypes.Num() - 1);
    return AvailableTypes[RandomIndex];
}

void AShootEmUpGameMode::UpdateDifficulty(float DeltaSeconds)
{
    float StageInterval = InitialSpawnInterval;
    for (const FEnemySpawnStep& Step : SpawnSteps)
    {
        if (ElapsedTime >= Step.StartTime)
        {
            StageInterval = FMath::Min(StageInterval, Step.SpawnInterval);
        }
    }

    const float RampTarget = InitialSpawnInterval - (ElapsedTime / GameDuration) * (InitialSpawnInterval - MinimumSpawnInterval);
    const float TargetInterval = FMath::Clamp(FMath::Min(StageInterval, RampTarget), MinimumSpawnInterval, InitialSpawnInterval);
    CurrentSpawnInterval = FMath::FInterpTo(CurrentSpawnInterval, TargetInterval, DeltaSeconds, 0.7f);
}

void AShootEmUpGameMode::CleanupDestroyedActors()
{
    ActiveEnemyProjectiles.RemoveAll([](const TWeakObjectPtr<AShootEmUpProjectile>& Ptr)
    {
        return !Ptr.IsValid();
    });

    ActiveEnemies.RemoveAll([](const TWeakObjectPtr<AShootEmUpEnemy>& Ptr)
    {
        return !Ptr.IsValid();
    });
}

void AShootEmUpGameMode::TriggerGameOver(bool bPlayerWon)
{
    bGameOver = true;
    bVictory = bPlayerWon;
    GetWorldTimerManager().ClearTimer(SpawnTimerHandle);
}

void AShootEmUpGameMode::OnSpawnTimerElapsed()
{
    if (bGameOver)
    {
        return;
    }

    if (ElapsedTime >= GameDuration)
    {
        return;
    }

    const EEnemyArchetype Archetype = SelectCurrentArchetype();
    SpawnEnemyByArchetype(Archetype);

    ScheduleNextSpawn(CurrentSpawnInterval);
}

void AShootEmUpGameMode::UpdateTimer(float DeltaSeconds)
{
    ElapsedTime += DeltaSeconds;
}
