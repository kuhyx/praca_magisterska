// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BulletHellCPP/STGFixedCamera.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGFixedCamera() {}

// Begin Cross Module References
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGFixedCamera();
BULLETHELLCPP_API UClass* Z_Construct_UClass_ASTGFixedCamera_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_AActor();
ENGINE_API UClass* Z_Construct_UClass_UCameraComponent_NoRegister();
UPackage* Z_Construct_UPackage__Script_BulletHellCPP();
// End Cross Module References

// Begin Class ASTGFixedCamera
void ASTGFixedCamera::StaticRegisterNativesASTGFixedCamera()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(ASTGFixedCamera);
UClass* Z_Construct_UClass_ASTGFixedCamera_NoRegister()
{
	return ASTGFixedCamera::StaticClass();
}
struct Z_Construct_UClass_ASTGFixedCamera_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Fixed camera that shows the entire play area for the bullet-hell game.\n * Place this in the level and it will automatically become the active camera.\n * \n * If bAutoFitPlayArea is true, the camera automatically calculates the correct\n * height and FOV to show exactly the play area defined in STGGameDirector.\n */" },
#endif
		{ "IncludePath", "STGFixedCamera.h" },
		{ "ModuleRelativePath", "STGFixedCamera.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Fixed camera that shows the entire play area for the bullet-hell game.\nPlace this in the level and it will automatically become the active camera.\n\nIf bAutoFitPlayArea is true, the camera automatically calculates the correct\nheight and FOV to show exactly the play area defined in STGGameDirector." },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Camera_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGFixedCamera.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bAutoFitPlayArea_MetaData[] = {
		{ "Category", "Camera|Auto Fit" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== AUTO-FIT MODE =====\n// When true, camera automatically sizes to fit the play area from Game Director\n" },
#endif
		{ "ModuleRelativePath", "STGFixedCamera.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== AUTO-FIT MODE =====\nWhen true, camera automatically sizes to fit the play area from Game Director" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_PlayAreaMargin_MetaData[] = {
		{ "Category", "Camera|Auto Fit" },
		{ "ClampMax", "0.5" },
		{ "ClampMin", "0.0" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Extra margin around play area (percentage, 0.1 = 10% extra)\n" },
#endif
		{ "EditCondition", "bAutoFitPlayArea" },
		{ "ModuleRelativePath", "STGFixedCamera.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Extra margin around play area (percentage, 0.1 = 10% extra)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CameraHeight_MetaData[] = {
		{ "Category", "Camera|Manual" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// ===== MANUAL MODE =====\n// Height above play area (Z position) - only used if bAutoFitPlayArea is false\n" },
#endif
		{ "EditCondition", "!bAutoFitPlayArea" },
		{ "ModuleRelativePath", "STGFixedCamera.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "===== MANUAL MODE =====\nHeight above play area (Z position) - only used if bAutoFitPlayArea is false" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_FieldOfView_MetaData[] = {
		{ "Category", "Camera" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Field of view (degrees) - used in both modes\n" },
#endif
		{ "ModuleRelativePath", "STGFixedCamera.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Field of view (degrees) - used in both modes" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bUseOrthographic_MetaData[] = {
		{ "Category", "Camera" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Whether to use orthographic projection (better for 2D-style gameplay)\n" },
#endif
		{ "ModuleRelativePath", "STGFixedCamera.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Whether to use orthographic projection (better for 2D-style gameplay)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_OrthoWidth_MetaData[] = {
		{ "Category", "Camera" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Orthographic width (only used if bUseOrthographic is true)\n" },
#endif
		{ "EditCondition", "bUseOrthographic" },
		{ "ModuleRelativePath", "STGFixedCamera.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Orthographic width (only used if bUseOrthographic is true)" },
#endif
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Camera;
	static void NewProp_bAutoFitPlayArea_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bAutoFitPlayArea;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_PlayAreaMargin;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_CameraHeight;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_FieldOfView;
	static void NewProp_bUseOrthographic_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bUseOrthographic;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_OrthoWidth;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGFixedCamera>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_Camera = { "Camera", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGFixedCamera, Camera), Z_Construct_UClass_UCameraComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Camera_MetaData), NewProp_Camera_MetaData) };
void Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bAutoFitPlayArea_SetBit(void* Obj)
{
	((ASTGFixedCamera*)Obj)->bAutoFitPlayArea = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bAutoFitPlayArea = { "bAutoFitPlayArea", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGFixedCamera), &Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bAutoFitPlayArea_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bAutoFitPlayArea_MetaData), NewProp_bAutoFitPlayArea_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_PlayAreaMargin = { "PlayAreaMargin", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGFixedCamera, PlayAreaMargin), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_PlayAreaMargin_MetaData), NewProp_PlayAreaMargin_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_CameraHeight = { "CameraHeight", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGFixedCamera, CameraHeight), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CameraHeight_MetaData), NewProp_CameraHeight_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_FieldOfView = { "FieldOfView", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGFixedCamera, FieldOfView), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_FieldOfView_MetaData), NewProp_FieldOfView_MetaData) };
void Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bUseOrthographic_SetBit(void* Obj)
{
	((ASTGFixedCamera*)Obj)->bUseOrthographic = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bUseOrthographic = { "bUseOrthographic", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(ASTGFixedCamera), &Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bUseOrthographic_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bUseOrthographic_MetaData), NewProp_bUseOrthographic_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_OrthoWidth = { "OrthoWidth", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGFixedCamera, OrthoWidth), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_OrthoWidth_MetaData), NewProp_OrthoWidth_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGFixedCamera_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_Camera,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bAutoFitPlayArea,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_PlayAreaMargin,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_CameraHeight,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_FieldOfView,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_bUseOrthographic,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGFixedCamera_Statics::NewProp_OrthoWidth,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGFixedCamera_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGFixedCamera_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AActor,
	(UObject* (*)())Z_Construct_UPackage__Script_BulletHellCPP,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGFixedCamera_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGFixedCamera_Statics::ClassParams = {
	&ASTGFixedCamera::StaticClass,
	"Engine",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_ASTGFixedCamera_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_ASTGFixedCamera_Statics::PropPointers),
	0,
	0x009000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGFixedCamera_Statics::Class_MetaDataParams), Z_Construct_UClass_ASTGFixedCamera_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_ASTGFixedCamera()
{
	if (!Z_Registration_Info_UClass_ASTGFixedCamera.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_ASTGFixedCamera.OuterSingleton, Z_Construct_UClass_ASTGFixedCamera_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_ASTGFixedCamera.OuterSingleton;
}
template<> BULLETHELLCPP_API UClass* StaticClass<ASTGFixedCamera>()
{
	return ASTGFixedCamera::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGFixedCamera);
ASTGFixedCamera::~ASTGFixedCamera() {}
// End Class ASTGFixedCamera

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGFixedCamera_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGFixedCamera, ASTGFixedCamera::StaticClass, TEXT("ASTGFixedCamera"), &Z_Registration_Info_UClass_ASTGFixedCamera, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGFixedCamera), 4102960611U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGFixedCamera_h_1917616082(TEXT("/Script/BulletHellCPP"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGFixedCamera_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGFixedCamera_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
