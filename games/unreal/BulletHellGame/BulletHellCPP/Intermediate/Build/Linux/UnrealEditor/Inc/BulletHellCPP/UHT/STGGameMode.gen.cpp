// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BulletHellCPP/STGGameMode.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGGameMode() {}

// Begin Cross Module References
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGGameMode();
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGGameMode_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_AGameModeBase();
UPackage* Z_Construct_UPackage__Script_BulletHellCPP();
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
#endif // WITH_METADATA
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGGameMode>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
UObject* (*const Z_Construct_UClass_ASTGGameMode_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AGameModeBase,
	(UObject* (*)())Z_Construct_UPackage__Script_BulletHellCPP,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameMode_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGGameMode_Statics::ClassParams = {
	&ASTGGameMode::StaticClass,
	"Game",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	nullptr,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	0,
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
template<> BULLETHELLCPP_API UClass* StaticClass<ASTGGameMode>()
{
	return ASTGGameMode::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGGameMode);
ASTGGameMode::~ASTGGameMode() {}
// End Class ASTGGameMode

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameMode_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGGameMode, ASTGGameMode::StaticClass, TEXT("ASTGGameMode"), &Z_Registration_Info_UClass_ASTGGameMode, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGGameMode), 3083596696U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameMode_h_1207468865(TEXT("/Script/BulletHellCPP"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameMode_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameMode_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
