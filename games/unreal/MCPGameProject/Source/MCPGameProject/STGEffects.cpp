#include "STGEffects.h"
#include "Components/StaticMeshComponent.h"

// ========== EXPLOSION EFFECT ==========

ASTGExplosionEffect::ASTGExplosionEffect()
{
	PrimaryActorTick.bCanEverTick = true;

	ExplosionMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ExplosionMesh"));
	ExplosionMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	RootComponent = ExplosionMesh;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
	if (SphereMesh.Succeeded())
	{
		ExplosionMesh->SetStaticMesh(SphereMesh.Object);
	}

	Duration = 0.4f;
	MaxScale = 2.0f;
	ExplosionColor = FLinearColor(1.0f, 0.5f, 0.0f); // Orange
	CurrentTime = 0.0f;
	DynamicMaterial = nullptr;

	InitialLifeSpan = Duration + 0.1f;
}

void ASTGExplosionEffect::BeginPlay()
{
	Super::BeginPlay();

	// Start small
	SetActorScale3D(FVector(0.1f));

	// Create glowing material
	DynamicMaterial = ExplosionMesh->CreateAndSetMaterialInstanceDynamic(0);
	if (DynamicMaterial)
	{
		DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), ExplosionColor);
		DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), ExplosionColor * 10.0f);
	}
}

void ASTGExplosionEffect::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	CurrentTime += DeltaTime;
	float Progress = CurrentTime / Duration;

	if (Progress <= 1.0f)
	{
		// Expand quickly, then slow down
		float ScaleProgress = FMath::Pow(Progress, 0.5f); // Ease out
		float CurrentScale = FMath::Lerp(0.1f, MaxScale, ScaleProgress);
		SetActorScale3D(FVector(CurrentScale));

		// Fade out
		if (DynamicMaterial)
		{
			float Alpha = 1.0f - Progress;
			DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), ExplosionColor * 10.0f * Alpha);
		}
	}
}

// ========== HIT EFFECT ==========

ASTGHitEffect::ASTGHitEffect()
{
	PrimaryActorTick.bCanEverTick = true;

	SparkMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SparkMesh"));
	SparkMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	RootComponent = SparkMesh;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere"));
	if (SphereMesh.Succeeded())
	{
		SparkMesh->SetStaticMesh(SphereMesh.Object);
	}

	SparkColor = FLinearColor::White;
	Duration = 0.15f;
	CurrentTime = 0.0f;
	DynamicMaterial = nullptr;

	InitialLifeSpan = Duration + 0.1f;
}

void ASTGHitEffect::BeginPlay()
{
	Super::BeginPlay();

	SetActorScale3D(FVector(0.2f));

	DynamicMaterial = SparkMesh->CreateAndSetMaterialInstanceDynamic(0);
	if (DynamicMaterial)
	{
		DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), SparkColor);
		DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), SparkColor * 20.0f);
	}
}

void ASTGHitEffect::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	CurrentTime += DeltaTime;
	float Progress = CurrentTime / Duration;

	if (Progress <= 1.0f)
	{
		// Quick flash
		float Scale = 0.2f * (1.0f + (1.0f - Progress) * 2.0f);
		SetActorScale3D(FVector(Scale));

		if (DynamicMaterial)
		{
			float Alpha = 1.0f - Progress;
			DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), SparkColor * 20.0f * Alpha);
		}
	}
}

// ========== SCREEN CLEAR EFFECT ==========

ASTGScreenClearEffect::ASTGScreenClearEffect()
{
	PrimaryActorTick.bCanEverTick = true;

	RingMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RingMesh"));
	RingMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	RootComponent = RingMesh;

	// Use a torus or cylinder for ring effect
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMesh(TEXT("/Engine/BasicShapes/Cylinder"));
	if (CylinderMesh.Succeeded())
	{
		RingMesh->SetStaticMesh(CylinderMesh.Object);
	}

	Duration = 0.5f;
	CurrentTime = 0.0f;
	DynamicMaterial = nullptr;

	InitialLifeSpan = Duration + 0.1f;
}

void ASTGScreenClearEffect::BeginPlay()
{
	Super::BeginPlay();

	SetActorScale3D(FVector(0.1f, 0.1f, 0.05f));
	SetActorRotation(FRotator(90.f, 0.f, 0.f)); // Flat ring

	DynamicMaterial = RingMesh->CreateAndSetMaterialInstanceDynamic(0);
	if (DynamicMaterial)
	{
		DynamicMaterial->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor::White);
		DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::White * 15.0f);
	}
}

void ASTGScreenClearEffect::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	CurrentTime += DeltaTime;
	float Progress = CurrentTime / Duration;

	if (Progress <= 1.0f)
	{
		// Expand rapidly
		float Scale = FMath::Lerp(0.1f, 50.0f, Progress);
		SetActorScale3D(FVector(Scale, Scale, 0.05f));

		if (DynamicMaterial)
		{
			float Alpha = 1.0f - FMath::Pow(Progress, 2.0f);
			DynamicMaterial->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor::White * 15.0f * Alpha);
		}
	}
}
