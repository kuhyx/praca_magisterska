#include "STGPawn.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "DrawDebugHelpers.h"

ASTGPawn::ASTGPawn()
{
    PrimaryActorTick.bCanEverTick = true;

    // Root component
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

    // Ship mesh - cone shape pointing upward
    ShipMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ShipMesh"));
    ShipMesh->SetupAttachment(RootComponent);
    ShipMesh->SetCollisionProfileName("NoCollision");

    // Load cone mesh from engine
    static ConstructorHelpers::FObjectFinder<UStaticMesh> ConeMesh(TEXT("/Engine/BasicShapes/Cone"));
    if (ConeMesh.Succeeded())
    {
        ShipMesh->SetStaticMesh(ConeMesh.Object);
        ShipMesh->SetRelativeScale3D(FVector(0.5f, 0.5f, 0.7f));
        ShipMesh->SetRelativeRotation(FRotator(90.f, 0.f, 0.f)); // Point forward
    }

    // Hitbox - small for bullet-hell precision
    Hitbox = CreateDefaultSubobject<UBoxComponent>(TEXT("Hitbox"));
    Hitbox->SetupAttachment(RootComponent);
    Hitbox->SetBoxExtent(FVector(25.f, 25.f, 10.f));
    Hitbox->SetCollisionProfileName("OverlapAllDynamic");
    Hitbox->SetGenerateOverlapEvents(true);

    // Visual hitbox indicator (small sphere)
    HitboxIndicator = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("HitboxIndicator"));
    HitboxIndicator->SetupAttachment(RootComponent);
    HitboxIndicator->SetCollisionEnabled(ECollisionEnabled::NoCollision);

    static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
    if (SphereMesh.Succeeded())
    {
        HitboxIndicator->SetStaticMesh(SphereMesh.Object);
        HitboxIndicator->SetRelativeScale3D(FVector(0.05f, 0.05f, 0.05f));
    }

    // Camera setup for top-down view
    SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->SetRelativeRotation(FRotator(-90.f, 0.f, 0.f)); // Top-down
    SpringArm->TargetArmLength = 1200.f;
    SpringArm->bDoCollisionTest = false;
    SpringArm->bInheritPitch = false;
    SpringArm->bInheritRoll = false;
    SpringArm->bInheritYaw = false;

    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    Camera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);
}

void ASTGPawn::BeginPlay()
{
    Super::BeginPlay();
    CurrentLives = MaxLives;

    // Add Input Mapping Context
    if (APlayerController* PlayerController = Cast<APlayerController>(Controller))
    {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
        {
            Subsystem->AddMappingContext(DefaultMappingContext, 0);
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

    // Movement with bounds clamping
    if (!MovementInput.IsZero())
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
    // Will implement in Part 3 when we create bullets
    // Display on-screen debug message (visible in game viewport)
    if (GEngine)
    {
        GEngine->AddOnScreenDebugMessage(-1, 0.1f, FColor::Yellow, TEXT("FIRE!"));
    }
}

void ASTGPawn::UseSpecial(const FInputActionValue& Value)
{
    if (!bSpecialUsed)
    {
        bSpecialUsed = true;
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(-1, 2.0f, FColor::Cyan, TEXT("SPECIAL ABILITY ACTIVATED!"));
        }
        // Will implement enemy/bullet destruction in Part 4
    }
}

void ASTGPawn::TakeHit(int32 Damage)
{
    CurrentLives = FMath::Clamp(CurrentLives - Damage, 0, MaxLives);

    if (CurrentLives <= 0)
    {
        HandleDeath();
    }
}

void ASTGPawn::HandleDeath()
{
    SetActorHiddenInGame(true);
    // Will notify GameMode in Part 6
}

void ASTGPawn::AddScore(int32 Points)
{
    Score += Points;
}
