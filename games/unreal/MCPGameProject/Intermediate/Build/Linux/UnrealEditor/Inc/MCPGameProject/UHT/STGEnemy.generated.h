// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "STGEnemy.h"
#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
#ifdef MCPGAMEPROJECT_STGEnemy_generated_h
#error "STGEnemy.generated.h already included, missing '#pragma once' in STGEnemy.h"
#endif
#define MCPGAMEPROJECT_STGEnemy_generated_h

#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_19_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesASTGEnemy(); \
	friend struct Z_Construct_UClass_ASTGEnemy_Statics; \
public: \
	DECLARE_CLASS(ASTGEnemy, AActor, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/MCPGameProject"), NO_API) \
	DECLARE_SERIALIZER(ASTGEnemy)


#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_19_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	ASTGEnemy(ASTGEnemy&&); \
	ASTGEnemy(const ASTGEnemy&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, ASTGEnemy); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(ASTGEnemy); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(ASTGEnemy) \
	NO_API virtual ~ASTGEnemy();


#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_16_PROLOG
#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_19_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_19_INCLASS_NO_PURE_DECLS \
	FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h_19_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> MCPGAMEPROJECT_API UClass* StaticClass<class ASTGEnemy>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGEnemy_h


#define FOREACH_ENUM_EENEMYTYPE(op) \
	op(EEnemyType::TypeA) \
	op(EEnemyType::TypeB) \
	op(EEnemyType::TypeC) \
	op(EEnemyType::TypeD) 

enum class EEnemyType : uint8;
template<> struct TIsUEnumClass<EEnemyType> { enum { Value = true }; };
template<> MCPGAMEPROJECT_API UEnum* StaticEnum<EEnemyType>();

PRAGMA_ENABLE_DEPRECATION_WARNINGS
