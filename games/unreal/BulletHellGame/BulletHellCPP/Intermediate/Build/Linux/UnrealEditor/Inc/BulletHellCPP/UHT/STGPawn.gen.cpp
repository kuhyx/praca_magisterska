// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BulletHellCPP/STGPawn.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGPawn() {}

// Begin Cross Module References
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGPawn();
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGPawn_NoRegister();
COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FVector2D();
ENGINE_API UClass* Z_Construct_UClass_APawn();
ENGINE_API UClass* Z_Construct_UClass_UBoxComponent_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UStaticMeshComponent_NoRegister();
ENHANCEDINPUT_API UClass* Z_Construct_UClass_UInputAction_NoRegister();
ENHANCEDINPUT_API UClass* Z_Construct_UClass_UInputMappingContext_NoRegister();
NIAGARA_API UClass* Z_Construct_UClass_UNiagaraSystem_NoRegister();
UPackage* Z_Construct_UPackage__Script_BulletHellCPP();
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
		{ "Comment", "// ===== COMPONENTS =====\n" },
#endif
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== COMPONENTS =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Hitbox_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_HitboxIndicator_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_DefaultMappingContext_MetaData[] = {
		{ "Category", "Input" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== ENHANCED INPUT =====\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== ENHANCED INPUT =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MoveAction_MetaData[] = {
		{ "Category", "Input" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_FireAction_MetaData[] = {
		{ "Category", "Input" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_SpecialAction_MetaData[] = {
		{ "Category", "Input" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CheatInvincibleAction_MetaData[] = {
		{ "Category", "Input" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MoveSpeed_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== MOVEMENT & BOUNDARIES =====\n// Defaults from STGGameSettings.h - can be overridden in Blueprint\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== MOVEMENT & BOUNDARIES =====\nDefaults from STGGameSettings.h - can be overridden in Blueprint" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BoundsMin_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BoundsMax_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bShowDebugBounds_MetaData[] = {
		{ "Category", "Debug" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== DEBUG / TESTING =====\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== DEBUG / TESTING =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bDebugInvincible_MetaData[] = {
		{ "Category", "Debug" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Invincibility mode (ignores all damage)\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Invincibility mode (ignores all damage)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bStationary_MetaData[] = {
		{ "Category", "Debug" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Stationary mode (disables player movement for performance testing)\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Stationary mode (disables player movement for performance testing)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_HitEffect_MetaData[] = {
		{ "Category", "VFX" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== VFX =====\n// Niagara effect when player gets hit\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== VFX =====\nNiagara effect when player gets hit" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_FireInterval_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== FIRING =====\n// Defaults from STGGameSettings.h (starts weak, upgrades with score)\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== FIRING =====\nDefaults from STGGameSettings.h (starts weak, upgrades with score)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BulletSpeed_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_VolleySize_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_VolleySpread_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_UpgradeLevel_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Current upgrade level (0-4)\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Current upgrade level (0-4)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MaxLives_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== LIVES & SCORE =====\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== LIVES & SCORE =====" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CurrentLives_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Score_MetaData[] = {
		{ "Category", "Stats" },
		{ "ModuleRelativePath", "STGPawn.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bSpecialUsed_MetaData[] = {
		{ "Category", "Stats" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== SPECIAL ABILITY =====\n" },
#endif
		{ "ModuleRelativePath", "STGPawn.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== SPECIAL ABILITY =====" },
#endif
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_ShipMesh;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Hitbox;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_HitboxIndicator;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_DefaultMappingContext;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_MoveAction;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_FireAction;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_SpecialAction;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_CheatInvincibleAction;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_MoveSpeed;
	static const UECodeGen_Private::FStructPropertyParams NewProp_BoundsMin;
	static const UECodeGen_Private::FStructPropertyParams NewProp_BoundsMax;
	static void NewProp_bShowDebugBounds_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bShowDebugBounds;
	static void NewProp_bDebugInvincible_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bDebugInvincible;
	static void NewProp_bStationary_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bStationary;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_HitEffect;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_FireInterval;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_BulletSpeed;
	static const UECodeGen_Private::FIntPropertyParams NewProp_VolleySize;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_VolleySpread;
	static const UECodeGen_Private::FIntPropertyParams NewProp_UpgradeLevel;
	static const UECodeGen_Private::FIntPropertyParams NewProp_MaxLives;
	static const UECodeGen_Private::FIntPropertyParams NewProp_CurrentLives;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Score;
	static void NewProp_bSpecialUsed_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bSpecialUsed;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGPawn>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_ShipMesh = { "ShipMesh", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, ShipMesh), Z_Construct_UClass_UStaticMeshComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ShipMesh_MetaData), NewProp_ShipMesh_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_Hitbox = { "Hitbox", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, Hitbox), Z_Construct_UClass_UBoxComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Hitbox_MetaData), NewProp_Hitbox_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_HitboxIndicator = { "HitboxIndicator", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, HitboxIndicator), Z_Construct_UClass_UStaticMeshComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_HitboxIndicator_MetaData), NewProp_HitboxIndicator_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_DefaultMappingContext = { "DefaultMappingContext", nullptr, (EPropertyFlags)0x0010000000000015, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, DefaultMappingContext), Z_Construct_UClass_UInputMappingContext_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_DefaultMappingContext_MetaData), NewProp_DefaultMappingContext_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_MoveAction = { "MoveAction", nullptr, (EPropertyFlags)0x0010000000000015, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, MoveAction), Z_Construct_UClass_UInputAction_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MoveAction_MetaData), NewProp_MoveAction_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_FireAction = { "FireAction", nullptr, (EPropertyFlags)0x0010000000000015, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, FireAction), Z_Construct_UClass_UInputAction_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_FireAction_MetaData), NewProp_FireAction_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_SpecialAction = { "SpecialAction", nullptr, (EPropertyFlags)0x0010000000000015, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, SpecialAction), Z_Construct_UClass_UInputAction_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_SpecialAction_MetaData), NewProp_SpecialAction_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_CheatInvincibleAction = { "CheatInvincibleAction", nullptr, (EPropertyFlags)0x0010000000000015, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, CheatInvincibleAction), Z_Construct_UClass_UInputAction_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CheatInvincibleAction_MetaData), NewProp_CheatInvincibleAction_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_MoveSpeed = { "MoveSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, MoveSpeed), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MoveSpeed_MetaData), NewProp_MoveSpeed_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_BoundsMin = { "BoundsMin", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, BoundsMin), Z_Construct_UScriptStruct_FVector2D, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BoundsMin_MetaData), NewProp_BoundsMin_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_BoundsMax = { "BoundsMax", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, BoundsMax), Z_Construct_UScriptStruct_FVector2D, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BoundsMax_MetaData), NewProp_BoundsMax_MetaData) };
void Z_Construct_UClass_ASTGPawn_Statics::NewProp_bShowDebugBounds_SetBit(void* Obj)
{
	((ASTGPawn*)Obj)->bShowDebugBounds = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_bShowDebugBounds = { "bShowDebugBounds", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGPawn), &Z_Construct_UClass_ASTGPawn_Statics::NewProp_bShowDebugBounds_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bShowDebugBounds_MetaData), NewProp_bShowDebugBounds_MetaData) };
void Z_Construct_UClass_ASTGPawn_Statics::NewProp_bDebugInvincible_SetBit(void* Obj)
{
	((ASTGPawn*)Obj)->bDebugInvincible = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_bDebugInvincible = { "bDebugInvincible", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGPawn), &Z_Construct_UClass_ASTGPawn_Statics::NewProp_bDebugInvincible_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bDebugInvincible_MetaData), NewProp_bDebugInvincible_MetaData) };
void Z_Construct_UClass_ASTGPawn_Statics::NewProp_bStationary_SetBit(void* Obj)
{
	((ASTGPawn*)Obj)->bStationary = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_bStationary = { "bStationary", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGPawn), &Z_Construct_UClass_ASTGPawn_Statics::NewProp_bStationary_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bStationary_MetaData), NewProp_bStationary_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_HitEffect = { "HitEffect", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, HitEffect), Z_Construct_UClass_UNiagaraSystem_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_HitEffect_MetaData), NewProp_HitEffect_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_FireInterval = { "FireInterval", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, FireInterval), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_FireInterval_MetaData), NewProp_FireInterval_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_BulletSpeed = { "BulletSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, BulletSpeed), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BulletSpeed_MetaData), NewProp_BulletSpeed_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_VolleySize = { "VolleySize", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, VolleySize), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_VolleySize_MetaData), NewProp_VolleySize_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_VolleySpread = { "VolleySpread", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, VolleySpread), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_VolleySpread_MetaData), NewProp_VolleySpread_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_UpgradeLevel = { "UpgradeLevel", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, UpgradeLevel), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_UpgradeLevel_MetaData), NewProp_UpgradeLevel_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_MaxLives = { "MaxLives", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, MaxLives), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MaxLives_MetaData), NewProp_MaxLives_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_CurrentLives = { "CurrentLives", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, CurrentLives), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CurrentLives_MetaData), NewProp_CurrentLives_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_Score = { "Score", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGPawn, Score), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Score_MetaData), NewProp_Score_MetaData) };
void Z_Construct_UClass_ASTGPawn_Statics::NewProp_bSpecialUsed_SetBit(void* Obj)
{
	((ASTGPawn*)Obj)->bSpecialUsed = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGPawn_Statics::NewProp_bSpecialUsed = { "bSpecialUsed", nullptr, (EPropertyFlags)0x0010000000020015, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGPawn), &Z_Construct_UClass_ASTGPawn_Statics::NewProp_bSpecialUsed_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bSpecialUsed_MetaData), NewProp_bSpecialUsed_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGPawn_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_ShipMesh,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_Hitbox,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_HitboxIndicator,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_DefaultMappingContext,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_MoveAction,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_FireAction,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_SpecialAction,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_CheatInvincibleAction,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_MoveSpeed,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_BoundsMin,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_BoundsMax,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_bShowDebugBounds,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_bDebugInvincible,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_bStationary,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_HitEffect,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_FireInterval,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_BulletSpeed,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_VolleySize,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_VolleySpread,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_UpgradeLevel,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_MaxLives,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_CurrentLives,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_Score,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGPawn_Statics::NewProp_bSpecialUsed,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGPawn_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGPawn_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_APawn,
	(UObject* (*)())Z_Construct_UPackage__Script_BulletHellCPP,
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
template<> BULLETHELLCPP_API UClass* StaticClass<ASTGPawn>()
{
	return ASTGPawn::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGPawn);
ASTGPawn::~ASTGPawn() {}
// End Class ASTGPawn

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGPawn_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGPawn, ASTGPawn::StaticClass, TEXT("ASTGPawn"), &Z_Registration_Info_UClass_ASTGPawn, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGPawn), 3512990002U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGPawn_h_1360490560(TEXT("/Script/BulletHellCPP"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGPawn_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGPawn_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
