// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "MCPGameProject/STGEnemy.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeSTGEnemy() {}

// Begin Cross Module References
ENGINE_API UClass* Z_Construct_UClass_AActor();
ENGINE_API UClass* Z_Construct_UClass_UBoxComponent_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UStaticMeshComponent_NoRegister();
MCPGAMEPROJECT_API UClass* Z_Construct_UClass_ASTGEnemy();
MCPGAMEPROJECT_API UClass* Z_Construct_UClass_ASTGEnemy_NoRegister();
MCPGAMEPROJECT_API UEnum* Z_Construct_UEnum_MCPGameProject_EEnemyType();
UPackage* Z_Construct_UPackage__Script_MCPGameProject();
// End Cross Module References

// Begin Enum EEnemyType
static FEnumRegistrationInfo Z_Registration_Info_UEnum_EEnemyType;
static UEnum* EEnemyType_StaticEnum()
{
	if (!Z_Registration_Info_UEnum_EEnemyType.OuterSingleton)
	{
		Z_Registration_Info_UEnum_EEnemyType.OuterSingleton = GetStaticEnum(Z_Construct_UEnum_MCPGameProject_EEnemyType, (UObject*)Z_Construct_UPackage__Script_MCPGameProject(), TEXT("EEnemyType"));
	}
	return Z_Registration_Info_UEnum_EEnemyType.OuterSingleton;
}
template<> MCPGAMEPROJECT_API UEnum* StaticEnum<EEnemyType>()
{
	return EEnemyType_StaticEnum();
}
struct Z_Construct_UEnum_MCPGameProject_EEnemyType_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "STGEnemy.h" },
		{ "TypeA.DisplayName", "Type A" },
		{ "TypeA.Name", "EEnemyType::TypeA" },
		{ "TypeB.DisplayName", "Type B" },
		{ "TypeB.Name", "EEnemyType::TypeB" },
		{ "TypeC.DisplayName", "Type C" },
		{ "TypeC.Name", "EEnemyType::TypeC" },
		{ "TypeD.DisplayName", "Type D" },
		{ "TypeD.Name", "EEnemyType::TypeD" },
	};
#endif // WITH_METADATA
	static constexpr UECodeGen_Private::FEnumeratorParam Enumerators[] = {
		{ "EEnemyType::TypeA", (int64)EEnemyType::TypeA },
		{ "EEnemyType::TypeB", (int64)EEnemyType::TypeB },
		{ "EEnemyType::TypeC", (int64)EEnemyType::TypeC },
		{ "EEnemyType::TypeD", (int64)EEnemyType::TypeD },
	};
	static const UECodeGen_Private::FEnumParams EnumParams;
};
const UECodeGen_Private::FEnumParams Z_Construct_UEnum_MCPGameProject_EEnemyType_Statics::EnumParams = {
	(UObject*(*)())Z_Construct_UPackage__Script_MCPGameProject,
	nullptr,
	"EEnemyType",
	"EEnemyType",
	Z_Construct_UEnum_MCPGameProject_EEnemyType_Statics::Enumerators,
	RF_Public|RF_Transient|RF_MarkAsNative,
	UE_ARRAY_COUNT(Z_Construct_UEnum_MCPGameProject_EEnemyType_Statics::Enumerators),
	EEnumFlags::None,
	(uint8)UEnum::ECppForm::EnumClass,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UEnum_MCPGameProject_EEnemyType_Statics::Enum_MetaDataParams), Z_Construct_UEnum_MCPGameProject_EEnemyType_Statics::Enum_MetaDataParams)
};
UEnum* Z_Construct_UEnum_MCPGameProject_EEnemyType()
{
	if (!Z_Registration_Info_UEnum_EEnemyType.InnerSingleton)
	{
		UECodeGen_Private::ConstructUEnum(Z_Registration_Info_UEnum_EEnemyType.InnerSingleton, Z_Construct_UEnum_MCPGameProject_EEnemyType_Statics::EnumParams);
	}
	return Z_Registration_Info_UEnum_EEnemyType.InnerSingleton;
}
// End Enum EEnemyType

// Begin Class ASTGEnemy
void ASTGEnemy::StaticRegisterNativesASTGEnemy()
{
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
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CollisionComp_MetaData[] = {
		{ "Category", "Components" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_EnemyType_MetaData[] = {
		{ "Category", "Enemy Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Health_MetaData[] = {
		{ "Category", "Enemy Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MoveSpeed_MetaData[] = {
		{ "Category", "Enemy Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_FireRate_MetaData[] = {
		{ "Category", "Enemy Stats" },
		{ "ModuleRelativePath", "STGEnemy.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_MeshComp;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_CollisionComp;
	static const UECodeGen_Private::FBytePropertyParams NewProp_EnemyType_Underlying;
	static const UECodeGen_Private::FEnumPropertyParams NewProp_EnemyType;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_Health;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_MoveSpeed;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_FireRate;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ASTGEnemy>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MeshComp = { "MeshComp", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, MeshComp), Z_Construct_UClass_UStaticMeshComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MeshComp_MetaData), NewProp_MeshComp_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_CollisionComp = { "CollisionComp", nullptr, (EPropertyFlags)0x00100000000a001d, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, CollisionComp), Z_Construct_UClass_UBoxComponent_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CollisionComp_MetaData), NewProp_CollisionComp_MetaData) };
const UECodeGen_Private::FBytePropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyType_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, nullptr, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FEnumPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyType = { "EnemyType", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, EnemyType), Z_Construct_UEnum_MCPGameProject_EEnemyType, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_EnemyType_MetaData), NewProp_EnemyType_MetaData) }; // 952559657
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_Health = { "Health", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, Health), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Health_MetaData), NewProp_Health_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MoveSpeed = { "MoveSpeed", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, MoveSpeed), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MoveSpeed_MetaData), NewProp_MoveSpeed_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_ASTGEnemy_Statics::NewProp_FireRate = { "FireRate", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(ASTGEnemy, FireRate), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_FireRate_MetaData), NewProp_FireRate_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_ASTGEnemy_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MeshComp,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_CollisionComp,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyType_Underlying,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_EnemyType,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_Health,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_MoveSpeed,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_ASTGEnemy_Statics::NewProp_FireRate,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemy_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_ASTGEnemy_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_AActor,
	(UObject* (*)())Z_Construct_UPackage__Script_MCPGameProject,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_ASTGEnemy_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_ASTGEnemy_Statics::ClassParams = {
	&ASTGEnemy::StaticClass,
	"Engine",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_ASTGEnemy_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
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
template<> MCPGAMEPROJECT_API UClass* StaticClass<ASTGEnemy>()
{
	return ASTGEnemy::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(ASTGEnemy);
ASTGEnemy::~ASTGEnemy() {}
// End Class ASTGEnemy

// Begin Registration
struct Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_Statics
{
	static constexpr FEnumRegisterCompiledInInfo EnumInfo[] = {
		{ EEnemyType_StaticEnum, TEXT("EEnemyType"), &Z_Registration_Info_UEnum_EEnemyType, CONSTRUCT_RELOAD_VERSION_INFO(FEnumReloadVersionInfo, 952559657U) },
	};
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_ASTGEnemy, ASTGEnemy::StaticClass, TEXT("ASTGEnemy"), &Z_Registration_Info_UClass_ASTGEnemy, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(ASTGEnemy), 1052407015U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_3444486008(TEXT("/Script/MCPGameProject"),
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_Statics::ClassInfo),
	nullptr, 0,
	Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_Statics::EnumInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_Statics::EnumInfo));
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
