// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "MCPGameProject/STGPawn.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGPawn() {}

// Begin Cross Module References
ENGINE_API UClass* Z_Construct_UClass_APawn();
ENGINE_API UClass* Z_Construct_UClass_UBoxComponent_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UCameraComponent_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_USpringArmComponent_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UStaticMeshComponent_NoRegister();
MCPGAMEPROJECT_API UClass* Z_Construct_UClass_ASTGPawn();
MCPGAMEPROJECT_API UClass* Z_Construct_UClass_ASTGPawn_NoRegister();
UPackage* Z_Construct_UPackage__Script_MCPGameProject();
// End Cross Module References

// Begin Class ASTGPawn
void ASTGPawn::StaticRegisterNativesASTGPawn()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(ASTGPawn);
UClass* Z_Construct_UClass_ASTGPawn_NoRegister()
{
	return ASTGPawn::StaticClass();
}
struct Z_Construct_UClass_ASTGPawn_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "HideCategories", "Navigation" },
		{ "IncludePath", "STGPawn.h" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ShipMesh_MetaData[] = {
		{ "Category", "Components" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Components\n" },
#endif
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Components" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_SpringArm_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Camera_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Hitbox_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MoveSpeed_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Gameplay Variables\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Gameplay Variables" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Lives_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Score_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Level_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BulletCount_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bCanSpecial_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_ShipMesh;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_SpringArm;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Camera;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Hitbox;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_MoveSpeed;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Lives;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Score;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Level;
	static const UECodeGen_Private::FIntPropertyParams NewProp_BulletCount;
	static void NewProp_bCanSpecial_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bCanSpecial;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGPawn>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_ShipMesh = { "ShipMesh", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, ShipMesh), Z_Construct_UClass_UStaticMeshComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ShipMesh_MetaData), NewProp_ShipMesh_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_SpringArm = { "SpringArm", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, SpringArm), Z_Construct_UClass_USpringArmComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_SpringArm_MetaData), NewProp_SpringArm_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_Camera = { "Camera", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, Camera), Z_Construct_UClass_UCameraComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Camera_MetaData), NewProp_Camera_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_Hitbox = { "Hitbox", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, Hitbox), Z_Construct_UClass_UBoxComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Hitbox_MetaData), NewProp_Hitbox_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_MoveSpeed = { "MoveSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, MoveSpeed), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MoveSpeed_MetaData), NewProp_MoveSpeed_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_Lives = { "Lives", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, Lives), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Lives_MetaData), NewProp_Lives_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_Score = { "Score", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, Score), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Score_MetaData), NewProp_Score_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_Level = { "Level", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, Level), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Level_MetaData), NewProp_Level_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_BulletCount = { "BulletCount", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, BulletCount), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BulletCount_MetaData), NewProp_BulletCount_MetaData) };
void Z_Construct_UClass_ASTGPawn_Statics::NewProp_bCanSpecial_SetBit(void* Obj)
{
	((ASTGPawn*)Obj)->bCanSpecial = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_bCanSpecial = { "bCanSpecial", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGPawn), &Z_Construct_UClass_ASTGPawn_Statics::NewProp_bCanSpecial_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bCanSpecial_MetaData), NewProp_bCanSpecial_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGPawn_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_ShipMesh,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_SpringArm,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_Camera,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_Hitbox,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_MoveSpeed,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_Lives,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_Score,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_Level,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_BulletCount,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_bCanSpecial,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGPawn_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGPawn_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_APawn,
	(UObject* (*)())Z_Construct_UPackage__Script_MCPGameProject,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGPawn_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGPawn_Statics::ClassParams = {
	&ASTGPawn::StaticClass,
	"Game",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_ASTGPawn_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_ASTGPawn_Statics::PropPointers),
	0,
	0x009000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGPawn_Statics::Class_MetaDataParams), Z_Construct_UClass_ASTGPawn_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_ASTGPawn()
{
	if (!Z_Registration_Info_UClass_ASTGPawn.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_ASTGPawn.OuterSingleton, Z_Construct_UClass_ASTGPawn_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_ASTGPawn.OuterSingleton;
}
template<> MCPGAMEPROJECT_API UClass* StaticClass<ASTGPawn>()
{
	return ASTGPawn::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGPawn);
ASTGPawn::~ASTGPawn() {}
// End Class ASTGPawn

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGPawn_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGPawn, ASTGPawn::StaticClass, TEXT("ASTGPawn"), &Z_Registration_Info_UClass_ASTGPawn, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGPawn), 3325776374U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGPawn_h_689296646(TEXT("/Script/MCPGameProject"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGPawn_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGPawn_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
