// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BulletHellCPP/STGGameDirector.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGGameDirector() {}

// Begin Cross Module References
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGGameDirector();
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGGameDirector_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_AActor();
UPackage* Z_Construct_UPackage__Script_BulletHellCPP();
// End Cross Module References

// Begin Class ASTGGameDirector
void ASTGGameDirector::StaticRegisterNativesASTGGameDirector()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(ASTGGameDirector);
UClass* Z_Construct_UClass_ASTGGameDirector_NoRegister()
{
	return ASTGGameDirector::StaticClass();
}
struct Z_Construct_UClass_ASTGGameDirector_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "IncludePath", "STGGameDirector.h" },
		{ "ModuleRelativePath", "STGGameDirector.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_GameDuration_MetaData[] = {
		{ "Category", "Game" },
		{ "ModuleRelativePath", "STGGameDirector.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bDebugQuickGame_MetaData[] = {
		{ "Category", "Debug" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Debug: Set to true for 10-second game (quick victory testing)\n" },
#endif
		{ "ModuleRelativePath", "STGGameDirector.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Debug: Set to true for 10-second game (quick victory testing)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ElapsedTime_MetaData[] = {
		{ "Category", "Game" },
		{ "ModuleRelativePath", "STGGameDirector.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bGameActive_MetaData[] = {
		{ "Category", "Game" },
		{ "ModuleRelativePath", "STGGameDirector.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FFloatPropertyParams NewProp_GameDuration;
	static void NewProp_bDebugQuickGame_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bDebugQuickGame;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_ElapsedTime;
	static void NewProp_bGameActive_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bGameActive;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGGameDirector>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_GameDuration = { "GameDuration", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGGameDirector, GameDuration), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_GameDuration_MetaData), NewProp_GameDuration_MetaData) };
void Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bDebugQuickGame_SetBit(void* Obj)
{
	((ASTGGameDirector*)Obj)->bDebugQuickGame = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bDebugQuickGame = { "bDebugQuickGame", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGGameDirector), &Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bDebugQuickGame_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bDebugQuickGame_MetaData), NewProp_bDebugQuickGame_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_ElapsedTime = { "ElapsedTime", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGGameDirector, ElapsedTime), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ElapsedTime_MetaData), NewProp_ElapsedTime_MetaData) };
void Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bGameActive_SetBit(void* Obj)
{
	((ASTGGameDirector*)Obj)->bGameActive = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bGameActive = { "bGameActive", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGGameDirector), &Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bGameActive_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bGameActive_MetaData), NewProp_bGameActive_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGGameDirector_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_GameDuration,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bDebugQuickGame,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_ElapsedTime,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGGameDirector_Statics::NewProp_bGameActive,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameDirector_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGGameDirector_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AActor,
	(UObject* (*)())Z_Construct_UPackage__Script_BulletHellCPP,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameDirector_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGGameDirector_Statics::ClassParams = {
	&ASTGGameDirector::StaticClass,
	"Engine",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_ASTGGameDirector_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameDirector_Statics::PropPointers),
	0,
	0x009000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGGameDirector_Statics::Class_MetaDataParams), Z_Construct_UClass_ASTGGameDirector_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_ASTGGameDirector()
{
	if (!Z_Registration_Info_UClass_ASTGGameDirector.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_ASTGGameDirector.OuterSingleton, Z_Construct_UClass_ASTGGameDirector_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_ASTGGameDirector.OuterSingleton;
}
template<> BULLETHELLCPP_API UClass* StaticClass<ASTGGameDirector>()
{
	return ASTGGameDirector::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGGameDirector);
ASTGGameDirector::~ASTGGameDirector() {}
// End Class ASTGGameDirector

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameDirector_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGGameDirector, ASTGGameDirector::StaticClass, TEXT("ASTGGameDirector"), &Z_Registration_Info_UClass_ASTGGameDirector, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGGameDirector), 2554782372U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameDirector_h_3196909243(TEXT("/Script/BulletHellCPP"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameDirector_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGGameDirector_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
