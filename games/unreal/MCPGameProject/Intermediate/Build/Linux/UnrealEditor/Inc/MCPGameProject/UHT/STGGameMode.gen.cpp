// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "MCPGameProject/STGGameMode.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGGameMode() {}

// Begin Cross Module References
ENGINE_API UClass* Z_Construct_UClass_AGameModeBase();
MCPGAMEPROJECT_API UClass* Z_Construct_UClass_ASTGGameMode();
MCPGAMEPROJECT_API UClass* Z_Construct_UClass_ASTGGameMode_NoRegister();
UPackage* Z_Construct_UPackage__Script_MCPGameProject();
// End Cross Module References

// Begin Class ASTGGameMode
void ASTGGameMode::StaticRegisterNativesASTGGameMode()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(ASTGGameMode);
UClass* Z_Construct_UClass_ASTGGameMode_NoRegister()
{
	return ASTGGameMode::StaticClass();
}
struct Z_Construct_UClass_ASTGGameMode_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "HideCategories", "Info Rendering MovementReplication Replication Actor Input Movement Collision Rendering HLOD WorldPartition DataLayers Transformation" },
		{ "IncludePath", "STGGameMode.h" },
		{ "ModuleRelativePath", "STGGameMode.h" },
		{ "ShowCategories", "Input|MouseInput Input|TouchInput" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_GameDuration_MetaData[] = {
		{ "Category", "Game Rules" },
		{ "ModuleRelativePath", "STGGameMode.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_TimeRemaining_MetaData[] = {
		{ "Category", "Game Rules" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// 90 seconds\n" },
#endif
		{ "ModuleRelativePath", "STGGameMode.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "90 seconds" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bIsGameOver_MetaData[] = {
		{ "Category", "Game Rules" },
		{ "ModuleRelativePath", "STGGameMode.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FFloatPropertyParams NewProp_GameDuration;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_TimeRemaining;
	static void NewProp_bIsGameOver_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bIsGameOver;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGGameMode>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGGameMode_Statics::NewProp_GameDuration = { "GameDuration", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGGameMode, GameDuration), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_GameDuration_MetaData), NewProp_GameDuration_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGGameMode_Statics::NewProp_TimeRemaining = { "TimeRemaining", nullptr, (EPropertyFlags)0x0010000000000014, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGGameMode, TimeRemaining), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_TimeRemaining_MetaData), NewProp_TimeRemaining_MetaData) };
void Z_Construct_UClass_ASTGGameMode_Statics::NewProp_bIsGameOver_SetBit(void* Obj)
{
	((ASTGGameMode*)Obj)->bIsGameOver = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGGameMode_Statics::NewProp_bIsGameOver = { "bIsGameOver", nullptr, (EPropertyFlags)0x0010000000000014, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGGameMode), &Z_Construct_UClass_ASTGGameMode_Statics::NewProp_bIsGameOver_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bIsGameOver_MetaData), NewProp_bIsGameOver_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGGameMode_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGGameMode_Statics::NewProp_GameDuration,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGGameMode_Statics::NewProp_TimeRemaining,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGGameMode_Statics::NewProp_bIsGameOver,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameMode_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGGameMode_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AGameModeBase,
	(UObject* (*)())Z_Construct_UPackage__Script_MCPGameProject,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameMode_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGGameMode_Statics::ClassParams = {
	&ASTGGameMode::StaticClass,
	"Game",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_ASTGGameMode_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameMode_Statics::PropPointers),
	0,
	0x009002ACu,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameMode_Statics::Class_MetaDataParams), Z_Construct_UClass_ASTGGameMode_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_ASTGGameMode()
{
	if (!Z_Registration_Info_UClass_ASTGGameMode.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_ASTGGameMode.OuterSingleton, Z_Construct_UClass_ASTGGameMode_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_ASTGGameMode.OuterSingleton;
}
template<> MCPGAMEPROJECT_API UClass* StaticClass<ASTGGameMode>()
{
	return ASTGGameMode::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGGameMode);
ASTGGameMode::~ASTGGameMode() {}
// End Class ASTGGameMode

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGGameMode_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGGameMode, ASTGGameMode::StaticClass, TEXT("ASTGGameMode"), &Z_Registration_Info_UClass_ASTGGameMode, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGGameMode), 2798597277U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGGameMode_h_3872457600(TEXT("/Script/MCPGameProject"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGGameMode_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGGameMode_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
