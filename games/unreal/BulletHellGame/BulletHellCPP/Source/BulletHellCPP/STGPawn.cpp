#include "STGPawn.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "DrawDebugHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "NiagaraFunctionLibrary.h"
#include "NiagaraComponent.h"
#include "STGProjectile.h"
#include "STGEnemy.h" 
#include "STGGameDirector.h"
#include "STGHUDManager.h"

ASTGPawn::ASTGPawn()
{
    PrimaryActorTick.bCanEverTick = true;

    // Root component
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

    // Ship mesh - flat 2D circle (cylinder with no height)
    ShipMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ShipMesh"));
    ShipMesh->SetupAttachment(RootComponent);
    ShipMesh->SetCollisionProfileName("NoCollision");

    // Load cylinder mesh and flatten it to make a 2D circle
    static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMesh(TEXT("/Engine/BasicShapes/Cylinder"));
    if (CylinderMesh.Succeeded())
    {
        ShipMesh->SetStaticMesh(CylinderMesh.Object);
        ShipMesh->SetRelativeScale3D(FVector(0.08f, 0.08f, 0.001f));  // Flat 2D circle, very small
    }

    // Hitbox - matches the visual circle size exactly
    // What you see is what you get!
    Hitbox = CreateDefaultSubobject<UBoxComponent>(TEXT("Hitbox"));
    Hitbox->SetupAttachment(RootComponent);
    Hitbox->SetBoxExtent(FVector(4.0f, 4.0f, 4.0f));  // Matches 0.08 scale cylinder (50 * 0.08 = 4)
    Hitbox->SetCollisionProfileName("OverlapAllDynamic");
    Hitbox->SetGenerateOverlapEvents(true);

    // No separate hitbox indicator needed - the sphere IS the hitbox
    HitboxIndicator = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("HitboxIndicator"));
    HitboxIndicator->SetupAttachment(RootComponent);
    HitboxIndicator->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    HitboxIndicator->SetVisibility(false);  // Not needed anymore
    
    // NOTE: Camera removed - use a fixed CameraActor in the level instead
    // This allows the camera to show the entire play area without following the player
}

void ASTGPawn::BeginPlay()
{
    Super::BeginPlay();
    CurrentLives = MaxLives;

    // Parse command-line arguments for testing modes
    FString CmdLine = FCommandLine::Get();
    
    // Check for --invincible flag
    if (CmdLine.Contains(TEXT("--invincible")) || CmdLine.Contains(TEXT("-invincible")))
    {
        bDebugInvincible = true;
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Cyan, TEXT("[CMD] INVINCIBILITY MODE ENABLED"));
        }
        UE_LOG(LogTemp, Warning, TEXT("Command-line: Invincibility enabled"));
    }
    
    // Check for --stationary flag
    if (CmdLine.Contains(TEXT("--stationary")) || CmdLine.Contains(TEXT("-stationary")))
    {
        bStationary = true;
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Cyan, TEXT("[CMD] STATIONARY MODE ENABLED"));
        }
        UE_LOG(LogTemp, Warning, TEXT("Command-line: Stationary mode enabled"));
    }

    // Try to add Input Mapping Context (works when placed in level with Auto Possess)
    SetupInputMappingContext();
    
    // Force flat 2D circle at runtime (in case Blueprint overrides it)
    // Use LoadObject instead of ConstructorHelpers (which only works in constructors)
    UStaticMesh* CylinderMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder"));
    if (CylinderMesh && ShipMesh)
    {
        ShipMesh->SetStaticMesh(CylinderMesh);
        ShipMesh->SetRelativeScale3D(FVector(0.08f, 0.08f, 0.001f));  // Flat 2D circle
        ShipMesh->SetRelativeRotation(FRotator::ZeroRotator);
    }
    
    // Initialize HUD with starting values (delayed to ensure HUD is ready)
    FTimerHandle TimerHandle;
    GetWorldTimerManager().SetTimer(TimerHandle, this, &ASTGPawn::UpdateHUD, 0.1f, false);
}

void ASTGPawn::PossessedBy(AController* NewController)
{
    Super::PossessedBy(NewController);
    
    // Add Input Mapping Context when possessed (works when spawned by GameMode)
    SetupInputMappingContext();
}

void ASTGPawn::SetupInputMappingContext()
{
    if (APlayerController* PlayerController = Cast<APlayerController>(Controller))
    {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
        {
            // Only add if not already added
            if (!Subsystem->HasMappingContext(DefaultMappingContext))
            {
                Subsystem->AddMappingContext(DefaultMappingContext, 0);
            }
        }
    }
}

void ASTGPawn::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    // Draw debug bounds (play area border)
    if (bShowDebugBounds)
    {
        float Z = GetActorLocation().Z;
        FVector TopLeft(BoundsMax.X, BoundsMin.Y, Z);
        FVector TopRight(BoundsMax.X, BoundsMax.Y, Z);
        FVector BottomLeft(BoundsMin.X, BoundsMin.Y, Z);
        FVector BottomRight(BoundsMin.X, BoundsMax.Y, Z);
        
        FColor BoundsColor = FColor::Green;
        float Thickness = 3.0f;
        
        DrawDebugLine(GetWorld(), TopLeft, TopRight, BoundsColor, false, -1.f, 0, Thickness);
        DrawDebugLine(GetWorld(), TopRight, BottomRight, BoundsColor, false, -1.f, 0, Thickness);
        DrawDebugLine(GetWorld(), BottomRight, BottomLeft, BoundsColor, false, -1.f, 0, Thickness);
        DrawDebugLine(GetWorld(), BottomLeft, TopLeft, BoundsColor, false, -1.f, 0, Thickness);
    }

    // Movement with bounds clamping (skip if dead or stationary mode)
    if (!bIsDead && !bStationary && !MovementInput.IsZero())
    {
        FVector NewLocation = GetActorLocation();
        NewLocation.X += MovementInput.Y * MoveSpeed * DeltaTime; // Forward/Back
        NewLocation.Y += MovementInput.X * MoveSpeed * DeltaTime; // Left/Right

        // Clamp to bounds
        NewLocation.X = FMath::Clamp(NewLocation.X, BoundsMin.X, BoundsMax.X);
        NewLocation.Y = FMath::Clamp(NewLocation.Y, BoundsMin.Y, BoundsMax.Y);

        SetActorLocation(NewLocation);
    }

    // Auto-fire when holding fire button
    if (bIsFiring)
    {
        FireTimer -= DeltaTime;
        if (FireTimer <= 0.0f)
        {
            FireShot();
            FireTimer = FireInterval;
        }
    }
}

void ASTGPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    // Set up Enhanced Input bindings
    if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        // Movement
        EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ASTGPawn::Move);
        EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Completed, this, &ASTGPawn::Move);

        // Fire
        EnhancedInputComponent->BindAction(FireAction, ETriggerEvent::Started, this, &ASTGPawn::StartFire);
        EnhancedInputComponent->BindAction(FireAction, ETriggerEvent::Completed, this, &ASTGPawn::StopFire);

        // Special
        EnhancedInputComponent->BindAction(SpecialAction, ETriggerEvent::Started, this, &ASTGPawn::UseSpecial);

        // Cheat: Toggle Invincibility (I key)
        EnhancedInputComponent->BindAction(CheatInvincibleAction, ETriggerEvent::Started, this, &ASTGPawn::ToggleInvincibility);
    }
}

void ASTGPawn::Move(const FInputActionValue& Value)
{
    MovementInput = Value.Get<FVector2D>();
}

void ASTGPawn::StartFire(const FInputActionValue& Value)
{
    bIsFiring = true;
    FireTimer = 0.0f; // Fire immediately
}

void ASTGPawn::StopFire(const FInputActionValue& Value)
{
    bIsFiring = false;
}

void ASTGPawn::FireShot()
{
    // Spawn volley of bullets shooting FORWARD (+X direction = toward top of screen)
    for (int32 i = 0; i < VolleySize; i++)
    {
        // Spawn slightly in front of player (+X)
        FVector SpawnLocation = GetActorLocation() + FVector(50.f, 0.f, 0.f);
        
        // Base rotation: FRotator(0,0,0) points in +X direction (forward in top-down view)
        FRotator SpawnRotation = FRotator::ZeroRotator;

        // Spread calculation: fan out on Yaw (left/right)
        float Angle = VolleySpread * (i - (VolleySize - 1) / 2.0f);
        SpawnRotation.Yaw += Angle;

        // Spawn bullet
        UWorld* World = GetWorld();
        if (World)
        {
            ASTGProjectile* Bullet = World->SpawnActor<ASTGProjectile>(
                ASTGProjectile::StaticClass(), 
                SpawnLocation, 
                SpawnRotation
            );
            
            if (Bullet)
            {
                Bullet->bIsPlayerBullet = true;
                Bullet->BulletScale = 0.06f;        // Small bullets
                Bullet->EmissiveIntensity = 2.0f;   // Dim glow
                Bullet->SetSpeed(BulletSpeed);
                Bullet->SetBulletColor(FLinearColor(0.2f, 0.8f, 0.3f)); // Soft green
            }
        }
    }
}

void ASTGPawn::UseSpecial(const FInputActionValue& Value)
{
    if (!bSpecialUsed)
    {
        bSpecialUsed = true;
        
        // Destroy all enemies on screen
        TArray<AActor*> FoundEnemies;
        UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGEnemy::StaticClass(), FoundEnemies);
        for (AActor* Enemy : FoundEnemies)
        {
            Enemy->Destroy();
        }

        // Destroy all enemy bullets (not player bullets)
        TArray<AActor*> FoundBullets;
        UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGProjectile::StaticClass(), FoundBullets);
        for (AActor* Bullet : FoundBullets)
        {
            ASTGProjectile* Projectile = Cast<ASTGProjectile>(Bullet);
            if (Projectile && !Projectile->bIsPlayerBullet)
            {
                Projectile->Destroy();
            }
        }
        
        UE_LOG(LogTemp, Warning, TEXT("SPECIAL ABILITY - Screen Cleared!"));
    }
}

void ASTGPawn::ToggleInvincibility(const FInputActionValue& Value)
{
    bDebugInvincible = !bDebugInvincible;
    
    if (GEngine)
    {
        FString Msg = bDebugInvincible ? TEXT("[CHEAT] INVINCIBILITY ON") : TEXT("[CHEAT] INVINCIBILITY OFF");
        FColor Color = bDebugInvincible ? FColor::Cyan : FColor::Yellow;
        GEngine->AddOnScreenDebugMessage(-1, 2.0f, Color, Msg);
    }
}

void ASTGPawn::TakeHit(int32 Damage)
{
    // Debug invincibility check
    if (bDebugInvincible)
    {
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(-1, 0.3f, FColor::Cyan, TEXT("[INVINCIBLE] Hit ignored!"));
        }
        return;
    }
    
    CurrentLives = FMath::Clamp(CurrentLives - Damage, 0, MaxLives);
    UpdateHUD();

    // Spawn hit VFX
    if (HitEffect)
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(
            GetWorld(),
            HitEffect,
            GetActorLocation(),
            FRotator::ZeroRotator,
            FVector(1.0f),
            true,
            true,
            ENCPoolMethod::None,
            true
        );
    }

    if (GEngine)
    {
        FString Msg = FString::Printf(TEXT("Player hit! Lives remaining: %d"), CurrentLives);
        GEngine->AddOnScreenDebugMessage(-1, 1.0f, FColor::Red, Msg);
    }

    if (CurrentLives <= 0)
    {
        HandleDeath();
    }
}

void ASTGPawn::HandleDeath()
{
    SetActorHiddenInGame(true);
    
    // Find and notify Game Director
    TArray<AActor*> FoundDirectors;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGGameDirector::StaticClass(), FoundDirectors);
    if (FoundDirectors.Num() > 0)
    {
        ASTGGameDirector* Director = Cast<ASTGGameDirector>(FoundDirectors[0]);
        if (Director)
        {
            Director->OnPlayerDied();
        }
    }
}

void ASTGPawn::AddScore(int32 Points)
{
    Score += Points;
    CheckUpgrades();  // Check if we leveled up!
    UpdateHUD();
}

void ASTGPawn::CheckUpgrades()
{
    int32 NewLevel = 0;
    
    // Determine upgrade level based on score thresholds
    if (Score >= STG::Player::UpgradeScore4)
    {
        NewLevel = 4;  // Max power!
    }
    else if (Score >= STG::Player::UpgradeScore3)
    {
        NewLevel = 3;
    }
    else if (Score >= STG::Player::UpgradeScore2)
    {
        NewLevel = 2;
    }
    else if (Score >= STG::Player::UpgradeScore1)
    {
        NewLevel = 1;
    }
    
    // Apply upgrade if level changed
    if (NewLevel > UpgradeLevel)
    {
        UpgradeLevel = NewLevel;
        
        // Set stats based on upgrade level
        switch (UpgradeLevel)
        {
            case 1:  // First upgrade: 2 bullets, faster fire
                VolleySize = 2;
                VolleySpread = 8.0f;
                FireInterval = 0.35f;
                break;
            case 2:  // Second upgrade: 3 bullets, even faster
                VolleySize = 3;
                VolleySpread = 12.0f;
                FireInterval = 0.20f;
                break;
            case 3:  // Third upgrade: 4 bullets, rapid fire
                VolleySize = 4;
                VolleySpread = 16.0f;
                FireInterval = 0.12f;
                break;
            case 4:  // Max upgrade: 5 bullets, maximum fire rate
                VolleySize = STG::Player::MaxVolleySize;
                VolleySpread = STG::Player::MaxVolleySpread;
                FireInterval = STG::Player::MaxFireInterval;
                break;
        }
        
        // Show upgrade message
        if (GEngine)
        {
            FString Msg = FString::Printf(TEXT("POWER UP! Level %d - %d bullets, %.2fs fire rate"), 
                UpgradeLevel, VolleySize, FireInterval);
            GEngine->AddOnScreenDebugMessage(-1, 3.0f, FColor::Yellow, Msg);
        }
    }
}

void ASTGPawn::UpdateHUD()
{
    TArray<AActor*> FoundManagers;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ASTGHUDManager::StaticClass(), FoundManagers);
    if (FoundManagers.Num() > 0)
    {
        ASTGHUDManager* HUDMgr = Cast<ASTGHUDManager>(FoundManagers[0]);
        if (HUDMgr)
        {
            HUDMgr->UpdateScore(Score);
            HUDMgr->UpdateLives(CurrentLives);
        }
    }
}
