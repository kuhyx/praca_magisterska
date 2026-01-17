// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BulletHellCPP/STGEnemy.h"
#include "Runtime/Engine/Classes/Engine/HitResult.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGEnemy() {}

// Begin Cross Module References
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGEnemy();
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGEnemy_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_AActor();
ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UBoxComponent_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UPrimitiveComponent_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UStaticMeshComponent_NoRegister();
ENGINE_API UScriptStruct* Z_Construct_UScriptStruct_FHitResult();
UPackage* Z_Construct_UPackage__Script_BulletHellCPP();
// End Cross Module References

// Begin Class ASTGEnemy Function OnOverlapBegin
struct Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics
{
	struct STGEnemy_eventOnOverlapBegin_Parms
	{
		UPrimitiveComponent* OverlappedComp;
		AActor* OtherActor;
		UPrimitiveComponent* OtherComp;
		int32 OtherBodyIndex;
		bool bFromSweep;
		FHitResult SweepResult;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_OverlappedComp_MetaData[] = {
		{ "EditInline", "true" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_OtherComp_MetaData[] = {
		{ "EditInline", "true" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_SweepResult_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_OverlappedComp;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_OtherActor;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_OtherComp;
	static const UECodeGen_Private::FIntPropertyParams NewProp_OtherBodyIndex;
	static void NewProp_bFromSweep_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bFromSweep;
	static const UECodeGen_Private::FStructPropertyParams NewProp_SweepResult;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OverlappedComp = { "OverlappedComp", nullptr, (EPropertyFlags)0x0010000000080080, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGEnemy_eventOnOverlapBegin_Parms, OverlappedComp), Z_Construct_UClass_UPrimitiveComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_OverlappedComp_MetaData), NewProp_OverlappedComp_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OtherActor = { "OtherActor", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGEnemy_eventOnOverlapBegin_Parms, OtherActor), Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OtherComp = { "OtherComp", nullptr, (EPropertyFlags)0x0010000000080080, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGEnemy_eventOnOverlapBegin_Parms, OtherComp), Z_Construct_UClass_UPrimitiveComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_OtherComp_MetaData), NewProp_OtherComp_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OtherBodyIndex = { "OtherBodyIndex", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGEnemy_eventOnOverlapBegin_Parms, OtherBodyIndex), METADATA_PARAMS(0, nullptr) };
void Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_bFromSweep_SetBit(void* Obj)
{
	((STGEnemy_eventOnOverlapBegin_Parms*)Obj)->bFromSweep = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_bFromSweep = { "bFromSweep", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(STGEnemy_eventOnOverlapBegin_Parms), &Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_bFromSweep_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_SweepResult = { "SweepResult", nullptr, (EPropertyFlags)0x0010008008000182, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(STGEnemy_eventOnOverlapBegin_Parms, SweepResult), Z_Construct_UScriptStruct_FHitResult, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_SweepResult_MetaData), NewProp_SweepResult_MetaData) }; // 4100991306
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OverlappedComp,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OtherActor,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OtherComp,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_OtherBodyIndex,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_bFromSweep,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::NewProp_SweepResult,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_ASTGEnemy, nullptr, "OnOverlapBegin", nullptr, nullptr, Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::PropPointers), sizeof(Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::STGEnemy_eventOnOverlapBegin_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x00420401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::Function_MetaDataParams), Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::STGEnemy_eventOnOverlapBegin_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(ASTGEnemy::execOnOverlapBegin)
{
	P_GET_OBJECT(UPrimitiveComponent,Z_Param_OverlappedComp);
	P_GET_OBJECT(AActor,Z_Param_OtherActor);
	P_GET_OBJECT(UPrimitiveComponent,Z_Param_OtherComp);
	P_GET_PROPERTY(FIntProperty,Z_Param_OtherBodyIndex);
	P_GET_UBOOL(Z_Param_bFromSweep);
	P_GET_STRUCT_REF(FHitResult,Z_Param_Out_SweepResult);
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->OnOverlapBegin(Z_Param_OverlappedComp,Z_Param_OtherActor,Z_Param_OtherComp,Z_Param_OtherBodyIndex,Z_Param_bFromSweep,Z_Param_Out_SweepResult);
	P_NATIVE_END;
}
// End Class ASTGEnemy Function OnOverlapBegin

// Begin Class ASTGEnemy
void ASTGEnemy::StaticRegisterNativesASTGEnemy()
{
	UClass* Class = ASTGEnemy::StaticClass();
	static const FNameNativePtrPair Funcs[] = {
		{ "OnOverlapBegin", &ASTGEnemy::execOnOverlapBegin },
	};
	FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(ASTGEnemy);
UClass* Z_Construct_UClass_ASTGEnemy_NoRegister()
{
	return ASTGEnemy::StaticClass();
}
struct Z_Construct_UClass_ASTGEnemy_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "IncludePath", "STGEnemy.h" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MeshComp_MetaData[] = {
		{ "Category", "Components" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== COMPONENTS =====\n" },
#endif
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGEnemy.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== COMPONENTS =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CollisionComp_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MaxHealth_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== HEALTH & SCORE (copy-paste all 15 variables!) =====\n" },
#endif
		{ "ModuleRelativePath", "STGEnemy.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== HEALTH & SCORE (copy-paste all 15 variables!) =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CurrentHealth_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ScoreValue_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_VerticalSpeed_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== MOVEMENT =====\n" },
#endif
		{ "ModuleRelativePath", "STGEnemy.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== MOVEMENT =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_HorizontalAmplitude_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_HorizontalFrequency_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_DespawnY_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_FireInterval_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== FIRING =====\n" },
#endif
		{ "ModuleRelativePath", "STGEnemy.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== FIRING =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BulletsPerBurst_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BurstSpread_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_EnemyBulletSpeed_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_EnemyBulletLifetime_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_MeshComp;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_CollisionComp;
	static const UECodeGen_Private::FIntPropertyParams NewProp_MaxHealth;
	static const UECodeGen_Private::FIntPropertyParams NewProp_CurrentHealth;
	static const UECodeGen_Private::FIntPropertyParams NewProp_ScoreValue;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_VerticalSpeed;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_HorizontalAmplitude;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_HorizontalFrequency;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_DespawnY;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_FireInterval;
	static const UECodeGen_Private::FIntPropertyParams NewProp_BulletsPerBurst;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_BurstSpread;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_EnemyBulletSpeed;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_EnemyBulletLifetime;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_ASTGEnemy_OnOverlapBegin, "OnOverlapBegin" }, // 3335619389
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGEnemy>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MeshComp = { "MeshComp", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, MeshComp), Z_Construct_UClass_UStaticMeshComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MeshComp_MetaData), NewProp_MeshComp_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_CollisionComp = { "CollisionComp", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, CollisionComp), Z_Construct_UClass_UBoxComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CollisionComp_MetaData), NewProp_CollisionComp_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MaxHealth = { "MaxHealth", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, MaxHealth), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MaxHealth_MetaData), NewProp_MaxHealth_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_CurrentHealth = { "CurrentHealth", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, CurrentHealth), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CurrentHealth_MetaData), NewProp_CurrentHealth_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_ScoreValue = { "ScoreValue", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, ScoreValue), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ScoreValue_MetaData), NewProp_ScoreValue_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_VerticalSpeed = { "VerticalSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, VerticalSpeed), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_VerticalSpeed_MetaData), NewProp_VerticalSpeed_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_HorizontalAmplitude = { "HorizontalAmplitude", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, HorizontalAmplitude), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_HorizontalAmplitude_MetaData), NewProp_HorizontalAmplitude_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_HorizontalFrequency = { "HorizontalFrequency", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, HorizontalFrequency), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_HorizontalFrequency_MetaData), NewProp_HorizontalFrequency_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_DespawnY = { "DespawnY", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, DespawnY), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_DespawnY_MetaData), NewProp_DespawnY_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_FireInterval = { "FireInterval", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, FireInterval), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_FireInterval_MetaData), NewProp_FireInterval_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_BulletsPerBurst = { "BulletsPerBurst", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, BulletsPerBurst), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BulletsPerBurst_MetaData), NewProp_BulletsPerBurst_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_BurstSpread = { "BurstSpread", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, BurstSpread), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BurstSpread_MetaData), NewProp_BurstSpread_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyBulletSpeed = { "EnemyBulletSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, EnemyBulletSpeed), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_EnemyBulletSpeed_MetaData), NewProp_EnemyBulletSpeed_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyBulletLifetime = { "EnemyBulletLifetime", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, EnemyBulletLifetime), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_EnemyBulletLifetime_MetaData), NewProp_EnemyBulletLifetime_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGEnemy_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MeshComp,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_CollisionComp,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MaxHealth,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_CurrentHealth,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_ScoreValue,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_VerticalSpeed,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_HorizontalAmplitude,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_HorizontalFrequency,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_DespawnY,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_FireInterval,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_BulletsPerBurst,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_BurstSpread,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyBulletSpeed,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyBulletLifetime,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemy_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGEnemy_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AActor,
	(UObject* (*)())Z_Construct_UPackage__Script_BulletHellCPP,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemy_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGEnemy_Statics::ClassParams = {
	&ASTGEnemy::StaticClass,
	"Engine",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	FuncInfo,
	Z_Construct_UClass_ASTGEnemy_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	UE_ARRAY_COUNT(FuncInfo),
	UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemy_Statics::PropPointers),
	0,
	0x009000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemy_Statics::Class_MetaDataParams), Z_Construct_UClass_ASTGEnemy_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_ASTGEnemy()
{
	if (!Z_Registration_Info_UClass_ASTGEnemy.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_ASTGEnemy.OuterSingleton, Z_Construct_UClass_ASTGEnemy_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_ASTGEnemy.OuterSingleton;
}
template<> BULLETHELLCPP_API UClass* StaticClass<ASTGEnemy>()
{
	return ASTGEnemy::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGEnemy);
ASTGEnemy::~ASTGEnemy() {}
// End Class ASTGEnemy

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGEnemy, ASTGEnemy::StaticClass, TEXT("ASTGEnemy"), &Z_Registration_Info_UClass_ASTGEnemy, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGEnemy), 495625582U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_1358030057(TEXT("/Script/BulletHellCPP"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
