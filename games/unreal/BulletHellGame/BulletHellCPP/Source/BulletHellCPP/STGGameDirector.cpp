#include "STGGameDirector.h"
#include "Kismet/GameplayStatics.h"
#include "STGHUDManager.h"
#include "STGEnemy.h"
#include "Misc/CommandLine.h"

ASTGGameDirector::ASTGGameDirector()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ASTGGameDirector::BeginPlay()
{
    Super::BeginPlay();
    ElapsedTime = 0.0f;
    bGameActive = true;
    
    // Parse command-line for benchmark mode
    FString CmdLine = FCommandLine::Get();
    
    // Check for --autoquit flag
    if (CmdLine.Contains(TEXT("--autoquit")) || CmdLine.Contains(TEXT("-autoquit")))
    {
        bAutoQuit = true;
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Cyan, TEXT("[CMD] AUTO-QUIT MODE ENABLED"));
        }
        UE_LOG(LogTemp, Warning, TEXT("Command-line: Auto-quit enabled"));
    }
    
    // Check for --duration=N flag (e.g., --duration=95)
    FString DurationValue;
    if (FParse::Value(*CmdLine, TEXT("--duration="), DurationValue) || 
        FParse::Value(*CmdLine, TEXT("-duration="), DurationValue))
    {
        float CustomDuration = FCString::Atof(*DurationValue);
        if (CustomDuration > 0)
        {
            GameDuration = CustomDuration;
            if (GEngine)
            {
                FString Msg = FString::Printf(TEXT("[CMD] GAME DURATION: %.0f seconds"), GameDuration);
                GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Cyan, Msg);
            }
            UE_LOG(LogTemp, Warning, TEXT("Command-line: Game duration set to %.0f seconds"), GameDuration);
        }
    }
    
    // Check for --start-time=N flag (e.g., --start-time=30) for phased profiling
    FString StartTimeValue;
    if (FParse::Value(*CmdLine, TEXT("--start-time="), StartTimeValue) || 
        FParse::Value(*CmdLine, TEXT("-start-time="), StartTimeValue))
    {
        float StartTime = FCString::Atof(*StartTimeValue);
        if (StartTime > 0 && StartTime < GameDuration)
        {
            ElapsedTime = StartTime;
            if (GEngine)
            {
                FString Msg = FString::Printf(TEXT("[CMD] START TIME: %.0f seconds (fast-forward)"), StartTime);
                GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Cyan, Msg);
            }
            UE_LOG(LogTemp, Warning, TEXT("Command-line: Starting at %.0f seconds"), StartTime);
        }
    }
    
    // Debug: Override game duration for quick testing
    if (bDebugQuickGame)
    {
        GameDuration = 10.0f;
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(-1, 3.0f, FColor::Yellow, TEXT("[DEBUG] Quick game mode: 10 seconds!"));
        }
    }
}

void ASTGGameDirector::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    if (!bGameActive)
        return;

    ElapsedTime += DeltaTime;

    // Display timer on screen (key 0 = persistent slot for timer)
    if (GEngine)
    {
        int32 Minutes = FMath::FloorToInt(ElapsedTime / 60.0f);
        int32 Seconds = FMath::FloorToInt(FMath::Fmod(ElapsedTime, 60.0f));
        FString TimeStr = FString::Printf(TEXT("Time: %02d:%02d"), Minutes, Seconds);
        GEngine->AddOnScreenDebugMessage(0, 0.0f, FColor::White, TimeStr);
    }

    // Check for victory (survived full duration)
    if (ElapsedTime >= GameDuration && !bInCleanupPhase)
    {
        // Enter cleanup phase - spawning stops, clear remaining enemies
        bInCleanupPhase = true;
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(-1, 3.0f, FColor::Yellow, TEXT("CLEANUP PHASE - Destroy all remaining enemies!"));
        }
    }
    
    // In cleanup phase, check if all enemies are gone
    if (bInCleanupPhase)
    {
        CheckCleanupVictory();
    }

	TArray<AActor*> FoundManagers;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGHUDManager::StaticClass(), FoundManagers);
    if (FoundManagers.Num() > 0)
    {
        ASTGHUDManager* HUDMgr = Cast<ASTGHUDManager>(FoundManagers[0]);
        if (HUDMgr)
        {
            HUDMgr->UpdateTimer(GameDuration - ElapsedTime);
        }
    }
}

void ASTGGameDirector::OnPlayerDied()
{
    OnGameOver();
}

void ASTGGameDirector::OnVictory()
{
    bGameActive = false;
    
    if (GEngine)
    {
        int32 Minutes = FMath::FloorToInt(ElapsedTime / 60.0f);
        int32 Seconds = FMath::FloorToInt(FMath::Fmod(ElapsedTime, 60.0f));
        FString Msg = FString::Printf(TEXT("VICTORY! You survived %02d:%02d!"), Minutes, Seconds);
        GEngine->AddOnScreenDebugMessage(-1, 999.0f, FColor::Green, Msg);
    }
    
    // Show victory in HUD
    TArray<AActor*> FoundManagers;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGHUDManager::StaticClass(), FoundManagers);
    if (FoundManagers.Num() > 0)
    {
        ASTGHUDManager* HUDMgr = Cast<ASTGHUDManager>(FoundManagers[0]);
        if (HUDMgr)
        {
            HUDMgr->ShowVictory();
        }
    }
    
    // Pause game or auto-quit for benchmarking
    if (bAutoQuit)
    {
        UE_LOG(LogTemp, Warning, TEXT("Auto-quit: Victory - requesting exit"));
        FPlatformMisc::RequestExit(false);
    }
    else
    {
        UGameplayStatics::SetGamePaused(GetWorld(), true);
    }
}

void ASTGGameDirector::OnGameOver()
{
    bGameActive = false;
    
    if (GEngine)
    {
        int32 Minutes = FMath::FloorToInt(ElapsedTime / 60.0f);
        int32 Seconds = FMath::FloorToInt(FMath::Fmod(ElapsedTime, 60.0f));
        FString Msg = FString::Printf(TEXT("GAME OVER! Survived %02d:%02d"), Minutes, Seconds);
        GEngine->AddOnScreenDebugMessage(-1, 999.0f, FColor::Red, Msg);
    }
    
    // Show game over in HUD
    TArray<AActor*> FoundManagers;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGHUDManager::StaticClass(), FoundManagers);
    if (FoundManagers.Num() > 0)
    {
        ASTGHUDManager* HUDMgr = Cast<ASTGHUDManager>(FoundManagers[0]);
        if (HUDMgr)
        {
            HUDMgr->ShowGameOver();
        }
    }
    
    // Pause game or auto-quit for benchmarking
    if (bAutoQuit)
    {
        UE_LOG(LogTemp, Warning, TEXT("Auto-quit: Game Over - requesting exit"));
        FPlatformMisc::RequestExit(false);
    }
    else
    {
        UGameplayStatics::SetGamePaused(GetWorld(), true);
    }
}

void ASTGGameDirector::CheckCleanupVictory()
{
    // Count remaining enemies
    TArray<AActor*> FoundEnemies;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGEnemy::StaticClass(), FoundEnemies);
    
    int32 EnemyCount = FoundEnemies.Num();
    
    // Show remaining enemy count
    if (GEngine)
    {
        FString Msg = FString::Printf(TEXT("Enemies remaining: %d"), EnemyCount);
        GEngine->AddOnScreenDebugMessage(1, 0.0f, FColor::Yellow, Msg);
    }
    
    // Victory when all enemies cleared!
    if (EnemyCount == 0)
    {
        OnVictory();
    }
}