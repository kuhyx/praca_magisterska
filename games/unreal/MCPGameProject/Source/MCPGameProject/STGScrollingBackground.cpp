#include "STGScrollingBackground.h"
#include "Components/StaticMeshComponent.h"

ASTGScrollingBackground::ASTGScrollingBackground()
{
	PrimaryActorTick.bCanEverTick = true;

	// Create root
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));

	// First background tile
	BackgroundMesh1 = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BackgroundMesh1"));
	BackgroundMesh1->SetupAttachment(RootComponent);
	BackgroundMesh1->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	
	// Second background tile (seamless scrolling)
	BackgroundMesh2 = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BackgroundMesh2"));
	BackgroundMesh2->SetupAttachment(RootComponent);
	BackgroundMesh2->SetCollisionEnabled(ECollisionEnabled::NoCollision);

	// Load plane mesh
	static ConstructorHelpers::FObjectFinder<UStaticMesh> PlaneMesh(TEXT("/Engine/BasicShapes/Plane"));
	if (PlaneMesh.Succeeded())
	{
		BackgroundMesh1->SetStaticMesh(PlaneMesh.Object);
		BackgroundMesh2->SetStaticMesh(PlaneMesh.Object);
		
		// Scale to fill screen area
		BackgroundMesh1->SetRelativeScale3D(FVector(40.0f, 25.0f, 1.0f));
		BackgroundMesh2->SetRelativeScale3D(FVector(40.0f, 25.0f, 1.0f));
	}

	ScrollSpeed = 200.0f;
	TileLength = 4000.0f; // Match scaled plane length
	ResetPosition = TileLength * 2.0f;
}

void ASTGScrollingBackground::BeginPlay()
{
	Super::BeginPlay();

	// Position backgrounds - one behind the other
	BackgroundMesh1->SetRelativeLocation(FVector(0.f, 0.f, -100.f)); // Slightly below play area
	BackgroundMesh2->SetRelativeLocation(FVector(TileLength, 0.f, -100.f));

	// Create dark space material
	UMaterialInstanceDynamic* BgMaterial1 = BackgroundMesh1->CreateAndSetMaterialInstanceDynamic(0);
	UMaterialInstanceDynamic* BgMaterial2 = BackgroundMesh2->CreateAndSetMaterialInstanceDynamic(0);
	
	if (BgMaterial1)
	{
		BgMaterial1->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor(0.02f, 0.02f, 0.05f)); // Dark blue-black
		BgMaterial1->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor(0.0f, 0.0f, 0.02f));
	}
	
	if (BgMaterial2)
	{
		BgMaterial2->SetVectorParameterValue(TEXT("BaseColor"), FLinearColor(0.02f, 0.02f, 0.05f));
		BgMaterial2->SetVectorParameterValue(TEXT("EmissiveColor"), FLinearColor(0.0f, 0.0f, 0.02f));
	}
}

void ASTGScrollingBackground::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Scroll both backgrounds
	FVector Offset = FVector(-ScrollSpeed * DeltaTime, 0.f, 0.f);
	
	BackgroundMesh1->AddRelativeLocation(Offset);
	BackgroundMesh2->AddRelativeLocation(Offset);

	// Wrap around when off screen
	if (BackgroundMesh1->GetRelativeLocation().X <= -TileLength)
	{
		FVector NewLoc = BackgroundMesh1->GetRelativeLocation();
		NewLoc.X += TileLength * 2.0f;
		BackgroundMesh1->SetRelativeLocation(NewLoc);
	}

	if (BackgroundMesh2->GetRelativeLocation().X <= -TileLength)
	{
		FVector NewLoc = BackgroundMesh2->GetRelativeLocation();
		NewLoc.X += TileLength * 2.0f;
		BackgroundMesh2->SetRelativeLocation(NewLoc);
	}
}
