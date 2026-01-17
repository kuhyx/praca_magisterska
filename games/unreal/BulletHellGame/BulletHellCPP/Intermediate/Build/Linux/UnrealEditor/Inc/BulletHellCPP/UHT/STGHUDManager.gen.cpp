// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BulletHellCPP/STGHUDManager.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGHUDManager() {}

// Begin Cross Module References
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGHUDManager();
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGHUDManager_NoRegister();
COREUOBJECT_API UClass* Z_Construct_UClass_UClass();
ENGINE_API UClass* Z_Construct_UClass_AActor();
UMG_API UClass* Z_Construct_UClass_UUserWidget_NoRegister();
UPackage* Z_Construct_UPackage__Script_BulletHellCPP();
// End Cross Module References

// Begin Class ASTGHUDManager Function UpdateLives
struct Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics
{
	struct STGHUDManager_eventUpdateLives_Parms
	{
		int32 NewLives;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI" },
		{ "ModuleRelativePath", "STGHUDManager.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FIntPropertyParams NewProp_NewLives;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::NewProp_NewLives = { "NewLives", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGHUDManager_eventUpdateLives_Parms, NewLives), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::NewProp_NewLives,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_ASTGHUDManager, nullptr, "UpdateLives", nullptr, nullptr, Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::PropPointers), sizeof(Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::STGHUDManager_eventUpdateLives_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::Function_MetaDataParams), Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::STGHUDManager_eventUpdateLives_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_ASTGHUDManager_UpdateLives()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_ASTGHUDManager_UpdateLives_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(ASTGHUDManager::execUpdateLives)
{
	P_GET_PROPERTY(FIntProperty,Z_Param_NewLives);
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->UpdateLives(Z_Param_NewLives);
	P_NATIVE_END;
}
// End Class ASTGHUDManager Function UpdateLives

// Begin Class ASTGHUDManager Function UpdateScore
struct Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics
{
	struct STGHUDManager_eventUpdateScore_Parms
	{
		int32 NewScore;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI" },
		{ "ModuleRelativePath", "STGHUDManager.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FIntPropertyParams NewProp_NewScore;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::NewProp_NewScore = { "NewScore", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGHUDManager_eventUpdateScore_Parms, NewScore), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::NewProp_NewScore,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_ASTGHUDManager, nullptr, "UpdateScore", nullptr, nullptr, Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::PropPointers), sizeof(Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::STGHUDManager_eventUpdateScore_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::Function_MetaDataParams), Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::STGHUDManager_eventUpdateScore_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_ASTGHUDManager_UpdateScore()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_ASTGHUDManager_UpdateScore_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(ASTGHUDManager::execUpdateScore)
{
	P_GET_PROPERTY(FIntProperty,Z_Param_NewScore);
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->UpdateScore(Z_Param_NewScore);
	P_NATIVE_END;
}
// End Class ASTGHUDManager Function UpdateScore

// Begin Class ASTGHUDManager Function UpdateTimer
struct Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics
{
	struct STGHUDManager_eventUpdateTimer_Parms
	{
		float TimeRemaining;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI" },
		{ "ModuleRelativePath", "STGHUDManager.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FFloatPropertyParams NewProp_TimeRemaining;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::NewProp_TimeRemaining = { "TimeRemaining", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGHUDManager_eventUpdateTimer_Parms, TimeRemaining), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::NewProp_TimeRemaining,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_ASTGHUDManager, nullptr, "UpdateTimer", nullptr, nullptr, Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::PropPointers), sizeof(Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::STGHUDManager_eventUpdateTimer_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::Function_MetaDataParams), Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::STGHUDManager_eventUpdateTimer_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_ASTGHUDManager_UpdateTimer()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_ASTGHUDManager_UpdateTimer_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(ASTGHUDManager::execUpdateTimer)
{
	P_GET_PROPERTY(FFloatProperty,Z_Param_TimeRemaining);
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->UpdateTimer(Z_Param_TimeRemaining);
	P_NATIVE_END;
}
// End Class ASTGHUDManager Function UpdateTimer

// Begin Class ASTGHUDManager
void ASTGHUDManager::StaticRegisterNativesASTGHUDManager()
{
	UClass* Class = ASTGHUDManager::StaticClass();
	static const FNameNativePtrPair Funcs[] = {
		{ "UpdateLives", &ASTGHUDManager::execUpdateLives },
		{ "UpdateScore", &ASTGHUDManager::execUpdateScore },
		{ "UpdateTimer", &ASTGHUDManager::execUpdateTimer },
	};
	FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(ASTGHUDManager);
UClass* Z_Construct_UClass_ASTGHUDManager_NoRegister()
{
	return ASTGHUDManager::StaticClass();
}
struct Z_Construct_UClass_ASTGHUDManager_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "IncludePath", "STGHUDManager.h" },
		{ "ModuleRelativePath", "STGHUDManager.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_HUDWidgetClass_MetaData[] = {
		{ "Category", "UI" },
		{ "ModuleRelativePath", "STGHUDManager.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FClassPropertyParams NewProp_HUDWidgetClass;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_ASTGHUDManager_UpdateLives, "UpdateLives" }, // 4101215941
		{ &Z_Construct_UFunction_ASTGHUDManager_UpdateScore, "UpdateScore" }, // 1330109670
		{ &Z_Construct_UFunction_ASTGHUDManager_UpdateTimer, "UpdateTimer" }, // 3811812644
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGHUDManager>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FClassPropertyParams Z_Construct_UClass_ASTGHUDManager_Statics::NewProp_HUDWidgetClass = { "HUDWidgetClass", nullptr, (EPropertyFlags)0x0014000000000005, UECodeGen_Private::EPropertyGenFlags::Class, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGHUDManager, HUDWidgetClass), Z_Construct_UClass_UClass, Z_Construct_UClass_UUserWidget_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_HUDWidgetClass_MetaData), NewProp_HUDWidgetClass_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGHUDManager_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGHUDManager_Statics::NewProp_HUDWidgetClass,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGHUDManager_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGHUDManager_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AActor,
	(UObject* (*)())Z_Construct_UPackage__Script_BulletHellCPP,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGHUDManager_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGHUDManager_Statics::ClassParams = {
	&ASTGHUDManager::StaticClass,
	"Engine",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	FuncInfo,
	Z_Construct_UClass_ASTGHUDManager_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	UE_ARRAY_COUNT(FuncInfo),
	UE_ARRAY_COUNT(Z_Construct_UClass_ASTGHUDManager_Statics::PropPointers),
	0,
	0x009000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGHUDManager_Statics::Class_MetaDataParams), Z_Construct_UClass_ASTGHUDManager_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_ASTGHUDManager()
{
	if (!Z_Registration_Info_UClass_ASTGHUDManager.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_ASTGHUDManager.OuterSingleton, Z_Construct_UClass_ASTGHUDManager_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_ASTGHUDManager.OuterSingleton;
}
template<> BULLETHELLCPP_API UClass* StaticClass<ASTGHUDManager>()
{
	return ASTGHUDManager::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGHUDManager);
ASTGHUDManager::~ASTGHUDManager() {}
// End Class ASTGHUDManager

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGHUDManager_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGHUDManager, ASTGHUDManager::StaticClass, TEXT("ASTGHUDManager"), &Z_Registration_Info_UClass_ASTGHUDManager, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGHUDManager), 1598084018U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGHUDManager_h_3087175026(TEXT("/Script/BulletHellCPP"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGHUDManager_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGHUDManager_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
