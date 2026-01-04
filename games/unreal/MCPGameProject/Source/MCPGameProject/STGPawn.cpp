#include "STGPawn.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Kismet/GameplayStatics.h"
#include "STGProjectile.h"
#include "STGEnemy.h"
#include "STGGameMode.h"
#include "STGEffects.h"

ASTGPawn::ASTGPawn()
{
	PrimaryActorTick.bCanEverTick = true;

	// Root component
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

	// Mesh - triangle/cone shape for the ship
	ShipMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ShipMesh"));
	ShipMesh->SetupAttachment(RootComponent);
	ShipMesh->SetCollisionProfileName("NoCollision"); // Visual only
	
	// Load cone mesh for ship
	static ConstructorHelpers::FObjectFinder<UStaticMesh> ConeMesh(TEXT("/Engine/BasicShapes/Cone"));
	if (ConeMesh.Succeeded())
	{
		ShipMesh->SetStaticMesh(ConeMesh.Object);
		ShipMesh->SetRelativeScale3D(FVector(0.5f, 0.5f, 0.7f));
		ShipMesh->SetRelativeRotation(FRotator(90.f, 0.f, 0.f)); // Point forward
	}

	// Hitbox (1 pixel - extremely tiny for bullet hell!)
	Hitbox = CreateDefaultSubobject<UBoxComponent>(TEXT("Hitbox"));
	Hitbox->SetupAttachment(RootComponent);
	Hitbox->SetBoxExtent(FVector(1.f, 1.f, 1.f)); // 1 pixel-ish hitbox
	Hitbox->SetCollisionProfileName("OverlapAllDynamic");
	Hitbox->SetGenerateOverlapEvents(true);

	// Visual hitbox indicator (small glowing sphere at center)
	HitboxIndicator = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("HitboxIndicator"));
	HitboxIndicator->SetupAttachment(RootComponent);
	HitboxIndicator->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	
	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
	if (SphereMesh.Succeeded())
	{
		HitboxIndicator->SetStaticMesh(SphereMesh.Object);
		HitboxIndicator->SetRelativeScale3D(FVector(0.05f, 0.05f, 0.05f)); // Very small
	}

	// Camera
	SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
	SpringArm->SetupAttachment(RootComponent);
	SpringArm->SetRelativeRotation(FRotator(-90.f, 0.f, 0.f)); // Top down
	SpringArm->TargetArmLength = 1200.f;
	SpringArm->bDoCollisionTest = false;
	SpringArm->bInheritPitch = false;
	SpringArm->bInheritRoll = false;
	SpringArm->bInheritYaw = false;

	Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
	Camera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);

	// Stats - 2 lives total (can die once, second death is game over)
	MoveSpeed = 600.f;
	Lives = 2;
	Score = 0;
	Level = 1;
	BulletCount = 1;
	bCanSpecial = true;
	FireRate = 0.08f;
	bIsInvulnerable = false;
	bIsFiring = false;

	// Boundaries
	MinX = -600.f;
	MaxX = 600.f;
	MinY = -800.f;
	MaxY = 800.f;

	ShipMaterial = nullptr;
	InvulnerabilityFlashTimer = 0.0f;
}

void ASTGPawn::BeginPlay()
{
	Super::BeginPlay();

	// Create dynamic material for ship
	if (ShipMesh && ShipMesh->GetStaticMesh())
	{
		ShipMaterial = ShipMesh->CreateAndSetMaterialInstanceDynamic(0);
		if (ShipMaterial)
		{
			ShipMaterial->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor::Green);
			ShipMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::Green * 3.0f);
		}
	}

	// Create hitbox indicator material
	if (HitboxIndicator && HitboxIndicator->GetStaticMesh())
	{
		UMaterialInstanceDynamic* HitboxMat = HitboxIndicator->CreateAndSetMaterialInstanceDynamic(0);
		if (HitboxMat)
		{
			HitboxMat->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor::White);
			HitboxMat->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::White * 10.0f);
		}
	}
}

void ASTGPawn::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Apply movement with boundaries
	if (!MovementInput.IsZero())
	{
		FVector NewLocation = GetActorLocation() + (MovementInput.GetSafeNormal() * MoveSpeed * DeltaTime);
		
		// Clamp to boundaries
		NewLocation.X = FMath::Clamp(NewLocation.X, MinX, MaxX);
		NewLocation.Y = FMath::Clamp(NewLocation.Y, MinY, MaxY);
		
		SetActorLocation(NewLocation, true);
	}

	// Invulnerability flashing effect
	if (bIsInvulnerable)
	{
		InvulnerabilityFlashTimer += DeltaTime;
		float Alpha = FMath::Abs(FMath::Sin(InvulnerabilityFlashTimer * 15.0f));
		if (ShipMesh)
		{
			ShipMesh->SetVisibility(Alpha > 0.5f);
		}
	}
}

void ASTGPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	PlayerInputComponent->BindAxis("MoveForward", this, &ASTGPawn::MoveForward);
	PlayerInputComponent->BindAxis("MoveRight", this, &ASTGPawn::MoveRight);

	PlayerInputComponent->BindAction("Fire", IE_Pressed, this, &ASTGPawn::StartFire);
	PlayerInputComponent->BindAction("Fire", IE_Released, this, &ASTGPawn::StopFire);
	PlayerInputComponent->BindAction("Special", IE_Pressed, this, &ASTGPawn::UseSpecial);
}

void ASTGPawn::MoveForward(float Value)
{
	MovementInput.X = Value;
}

void ASTGPawn::MoveRight(float Value)
{
	MovementInput.Y = Value;
}

void ASTGPawn::StartFire()
{
	bIsFiring = true;
	GetWorldTimerManager().SetTimer(TimerHandle_Fire, this, &ASTGPawn::FireShot, FireRate, true, 0.0f);
}

void ASTGPawn::StopFire()
{
	bIsFiring = false;
	GetWorldTimerManager().ClearTimer(TimerHandle_Fire);
}

void ASTGPawn::FireShot()
{
	UWorld* World = GetWorld();
	if (!World) return;

	FVector SpawnLocation = GetActorLocation() + FVector(50.f, 0.f, 0.f);

	// Base forward shooting
	// Number of bullets increases with level
	int32 NumBullets = BulletCount;
	float SpreadAngle = 8.0f;

	// Forward shots with spread
	for (int32 i = 0; i < NumBullets; i++)
	{
		float Offset = (i - (NumBullets - 1) / 2.0f);
		FRotator SpreadRot = FRotator(0.f, Offset * SpreadAngle, 0.f);
		
		ASTGProjectile* Projectile = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), SpawnLocation, SpreadRot);
		if (Projectile)
		{
			Projectile->bIsPlayerBullet = true;
			Projectile->SetSpeed(2500.0f);
		}
	}

	// Level 2+: Add side shots
	if (Level >= 2)
	{
		// Left side shot
		FVector LeftSpawn = GetActorLocation() + FVector(0.f, -30.f, 0.f);
		ASTGProjectile* LeftProj = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), LeftSpawn, FRotator(0.f, -45.f, 0.f));
		if (LeftProj)
		{
			LeftProj->bIsPlayerBullet = true;
			LeftProj->SetSpeed(2000.0f);
		}

		// Right side shot
		FVector RightSpawn = GetActorLocation() + FVector(0.f, 30.f, 0.f);
		ASTGProjectile* RightProj = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), RightSpawn, FRotator(0.f, 45.f, 0.f));
		if (RightProj)
		{
			RightProj->bIsPlayerBullet = true;
			RightProj->SetSpeed(2000.0f);
		}
	}

	// Level 3+: Add diagonal back shots
	if (Level >= 3)
	{
		FVector BackSpawn = GetActorLocation() + FVector(-30.f, 0.f, 0.f);
		
		ASTGProjectile* BackLeft = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), BackSpawn, FRotator(0.f, -135.f, 0.f));
		if (BackLeft)
		{
			BackLeft->bIsPlayerBullet = true;
			BackLeft->SetSpeed(1800.0f);
		}

		ASTGProjectile* BackRight = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), BackSpawn, FRotator(0.f, 135.f, 0.f));
		if (BackRight)
		{
			BackRight->bIsPlayerBullet = true;
			BackRight->SetSpeed(1800.0f);
		}
	}

	// Level 4+: Full rear shot
	if (Level >= 4)
	{
		FVector BackSpawn = GetActorLocation() + FVector(-50.f, 0.f, 0.f);
		ASTGProjectile* BackProj = World->SpawnActor<ASTGProjectile>(ASTGProjectile::StaticClass(), BackSpawn, FRotator(0.f, 180.f, 0.f));
		if (BackProj)
		{
			BackProj->bIsPlayerBullet = true;
			BackProj->SetSpeed(2000.0f);
		}
	}
}

void ASTGPawn::UseSpecial()
{
	if (bCanSpecial)
	{
		bCanSpecial = false;
		ClearScreen();
	}
}

void ASTGPawn::ClearScreen()
{
	UWorld* World = GetWorld();
	if (!World) return;

	// Spawn screen clear effect
	World->SpawnActor<ASTGScreenClearEffect>(ASTGScreenClearEffect::StaticClass(), GetActorLocation(), FRotator::ZeroRotator);

	// Destroy all enemies
	TArray<AActor*> FoundEnemies;
	UGameplayStatics::GetAllActorsOfClass(World, ASTGEnemy::StaticClass(), FoundEnemies);
	for (AActor* Actor : FoundEnemies)
	{
		// Give score for cleared enemies
		ASTGEnemy* Enemy = Cast<ASTGEnemy>(Actor);
		if (Enemy)
		{
			AddScore(Enemy->ScoreValue / 2); // Half score for special clear
			
			// Spawn explosion for each enemy
			ASTGExplosionEffect* Explosion = World->SpawnActor<ASTGExplosionEffect>(ASTGExplosionEffect::StaticClass(), Enemy->GetActorLocation(), FRotator::ZeroRotator);
			if (Explosion)
			{
				Explosion->ExplosionColor = Enemy->EnemyColor;
			}
		}
		Actor->Destroy();
	}

	// Destroy all enemy bullets
	TArray<AActor*> FoundBullets;
	UGameplayStatics::GetAllActorsOfClass(World, ASTGProjectile::StaticClass(), FoundBullets);
	for (AActor* Actor : FoundBullets)
	{
		ASTGProjectile* Bullet = Cast<ASTGProjectile>(Actor);
		if (Bullet && !Bullet->bIsPlayerBullet)
		{
			Actor->Destroy();
		}
	}
}

void ASTGPawn::HandleDamage(float DamageAmount)
{
	if (bIsInvulnerable) return;

	Lives--;
	
	if (Lives <= 0)
	{
		Die();
	}
	else
	{
		Respawn();
	}
}

void ASTGPawn::AddScore(int32 Points)
{
	int32 OldScore = Score;
	Score += Points;

	// Level up every 500 points
	int32 OldLevel = OldScore / 500;
	int32 NewLevel = Score / 500;
	
	if (NewLevel > OldLevel)
	{
		LevelUp();
	}
}

void ASTGPawn::LevelUp()
{
	Level++;
	BulletCount = FMath::Min(Level + 1, 5); // Cap at 5 forward bullets
	
	// Visual feedback - flash ship
	if (ShipMaterial)
	{
		ShipMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::Yellow * 20.0f);
		
		// Reset after short delay
		FTimerHandle TimerHandle_LevelUpFlash;
		GetWorldTimerManager().SetTimer(TimerHandle_LevelUpFlash, [this]()
		{
			if (ShipMaterial)
			{
				ShipMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::Green * 3.0f);
			}
		}, 0.5f, false);
	}
}

void ASTGPawn::Die()
{
	// Notify game mode
	ASTGGameMode* GameMode = Cast<ASTGGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
	if (GameMode)
	{
		GameMode->OnPlayerDied();
	}
}

void ASTGPawn::Respawn()
{
	// Clear screen before respawn
	ClearScreen();
	
	// Reset position to bottom center
	SetActorLocation(FVector(-400.f, 0.f, 0.f));
	
	// Grant invulnerability
	bIsInvulnerable = true;
	InvulnerabilityFlashTimer = 0.0f;
	
	GetWorldTimerManager().SetTimer(TimerHandle_Invulnerability, this, &ASTGPawn::EndInvulnerability, 3.0f, false);
}

void ASTGPawn::EndInvulnerability()
{
	bIsInvulnerable = false;
	if (ShipMesh)
	{
		ShipMesh->SetVisibility(true);
	}
}

