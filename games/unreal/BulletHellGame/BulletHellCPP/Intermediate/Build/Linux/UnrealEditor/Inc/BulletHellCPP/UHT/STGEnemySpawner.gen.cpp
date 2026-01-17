// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BulletHellCPP/STGEnemySpawner.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGEnemySpawner() {}

// Begin Cross Module References
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGEnemySpawner();
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGEnemySpawner_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_AActor();
UPackage* Z_Construct_UPackage__Script_BulletHellCPP();
// End Cross Module References

// Begin Class ASTGEnemySpawner
void ASTGEnemySpawner::StaticRegisterNativesASTGEnemySpawner()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(ASTGEnemySpawner);
UClass* Z_Construct_UClass_ASTGEnemySpawner_NoRegister()
{
	return ASTGEnemySpawner::StaticClass();
}
struct Z_Construct_UClass_ASTGEnemySpawner_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "IncludePath", "STGEnemySpawner.h" },
		{ "ModuleRelativePath", "STGEnemySpawner.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_SpawnAreaHalfWidth_MetaData[] = {
		{ "Category", "Spawning" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== SPAWNING VARIABLES =====\n// Half-width for Y spawn range (should be less than play area to allow wave movement)\n" },
#endif
		{ "ModuleRelativePath", "STGEnemySpawner.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== SPAWNING VARIABLES =====\nHalf-width for Y spawn range (should be less than play area to allow wave movement)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_GameDuration_MetaData[] = {
		{ "Category", "Spawning" },
		{ "ModuleRelativePath", "STGEnemySpawner.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MaxSimultaneousEnemies_MetaData[] = {
		{ "Category", "Spawning" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// 5 minutes\n" },
#endif
		{ "ModuleRelativePath", "STGEnemySpawner.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "5 minutes" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BaseSpawnInterval_MetaData[] = {
		{ "Category", "Spawning" },
		{ "ModuleRelativePath", "STGEnemySpawner.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ElapsedTime_MetaData[] = {
		{ "Category", "Spawning" },
		{ "ModuleRelativePath", "STGEnemySpawner.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bSpawningActive_MetaData[] = {
		{ "Category", "Spawning" },
		{ "ModuleRelativePath", "STGEnemySpawner.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FFloatPropertyParams NewProp_SpawnAreaHalfWidth;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_GameDuration;
	static const UECodeGen_Private::FIntPropertyParams NewProp_MaxSimultaneousEnemies;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_BaseSpawnInterval;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_ElapsedTime;
	static void NewProp_bSpawningActive_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bSpawningActive;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGEnemySpawner>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_SpawnAreaHalfWidth = { "SpawnAreaHalfWidth", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemySpawner, SpawnAreaHalfWidth), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_SpawnAreaHalfWidth_MetaData), NewProp_SpawnAreaHalfWidth_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_GameDuration = { "GameDuration", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemySpawner, GameDuration), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_GameDuration_MetaData), NewProp_GameDuration_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_MaxSimultaneousEnemies = { "MaxSimultaneousEnemies", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemySpawner, MaxSimultaneousEnemies), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MaxSimultaneousEnemies_MetaData), NewProp_MaxSimultaneousEnemies_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_BaseSpawnInterval = { "BaseSpawnInterval", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemySpawner, BaseSpawnInterval), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BaseSpawnInterval_MetaData), NewProp_BaseSpawnInterval_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_ElapsedTime = { "ElapsedTime", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemySpawner, ElapsedTime), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ElapsedTime_MetaData), NewProp_ElapsedTime_MetaData) };
void Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_bSpawningActive_SetBit(void* Obj)
{
	((ASTGEnemySpawner*)Obj)->bSpawningActive = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_bSpawningActive = { "bSpawningActive", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGEnemySpawner), &Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_bSpawningActive_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bSpawningActive_MetaData), NewProp_bSpawningActive_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGEnemySpawner_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_SpawnAreaHalfWidth,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_GameDuration,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_MaxSimultaneousEnemies,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_BaseSpawnInterval,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_ElapsedTime,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemySpawner_Statics::NewProp_bSpawningActive,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemySpawner_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGEnemySpawner_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AActor,
	(UObject* (*)())Z_Construct_UPackage__Script_BulletHellCPP,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemySpawner_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGEnemySpawner_Statics::ClassParams = {
	&ASTGEnemySpawner::StaticClass,
	"Engine",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_ASTGEnemySpawner_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemySpawner_Statics::PropPointers),
	0,
	0x009000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemySpawner_Statics::Class_MetaDataParams), Z_Construct_UClass_ASTGEnemySpawner_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_ASTGEnemySpawner()
{
	if (!Z_Registration_Info_UClass_ASTGEnemySpawner.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_ASTGEnemySpawner.OuterSingleton, Z_Construct_UClass_ASTGEnemySpawner_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_ASTGEnemySpawner.OuterSingleton;
}
template<> BULLETHELLCPP_API UClass* StaticClass<ASTGEnemySpawner>()
{
	return ASTGEnemySpawner::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGEnemySpawner);
ASTGEnemySpawner::~ASTGEnemySpawner() {}
// End Class ASTGEnemySpawner

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemySpawner_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGEnemySpawner, ASTGEnemySpawner::StaticClass, TEXT("ASTGEnemySpawner"), &Z_Registration_Info_UClass_ASTGEnemySpawner, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGEnemySpawner), 1062965579U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemySpawner_h_514711947(TEXT("/Script/BulletHellCPP"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemySpawner_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemySpawner_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
