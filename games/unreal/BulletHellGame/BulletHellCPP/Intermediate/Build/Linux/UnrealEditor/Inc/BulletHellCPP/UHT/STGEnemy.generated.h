// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "STGEnemy.h"
#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class AActor;
class UPrimitiveComponent;
struct FHitResult;
#ifdef BULLETHELLCPP_STGEnemy_generated_h
#error "STGEnemy.generated.h already included, missing '#pragma once' in STGEnemy.h"
#endif
#define BULLETHELLCPP_STGEnemy_generated_h

#define FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_13_RPC_WRAPPERS_NO_PURE_DECLS \
	DECLARE_FUNCTION(execOnOverlapBegin);


#define FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_13_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesASTGEnemy(); \
	friend struct Z_Construct_UClass_ASTGEnemy_Statics; \
public: \
	DECLARE_CLASS(ASTGEnemy, AActor, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/BulletHellCPP"), NO_API) \
	DECLARE_SERIALIZER(ASTGEnemy)


#define FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_13_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	ASTGEnemy(ASTGEnemy&&); \
	ASTGEnemy(const ASTGEnemy&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, ASTGEnemy); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(ASTGEnemy); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(ASTGEnemy) \
	NO_API virtual ~ASTGEnemy();


#define FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_10_PROLOG
#define FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_13_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_13_RPC_WRAPPERS_NO_PURE_DECLS \
	FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_13_INCLASS_NO_PURE_DECLS \
	FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h_13_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> BULLETHELLCPP_API UClass* StaticClass<class ASTGEnemy>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_praca_magisterska_games_unreal_BulletHellGame_BulletHellCPP_Source_BulletHellCPP_STGEnemy_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
