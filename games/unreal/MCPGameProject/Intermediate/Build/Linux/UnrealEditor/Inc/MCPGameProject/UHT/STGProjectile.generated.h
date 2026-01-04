// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "STGProjectile.h"
#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class AActor;
class UPrimitiveComponent;
struct FHitResult;
#ifdef MCPGAMEPROJECT_STGProjectile_generated_h
#error "STGProjectile.generated.h already included, missing '#pragma once' in STGProjectile.h"
#endif
#define MCPGAMEPROJECT_STGProjectile_generated_h

#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_13_RPC_WRAPPERS_NO_PURE_DECLS \
	DECLARE_FUNCTION(execOnOverlapBegin); \
	DECLARE_FUNCTION(execOnHit);


#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_13_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesASTGProjectile(); \
	friend struct Z_Construct_UClass_ASTGProjectile_Statics; \
public: \
	DECLARE_CLASS(ASTGProjectile, AActor, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/MCPGameProject"), NO_API) \
	DECLARE_SERIALIZER(ASTGProjectile)


#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_13_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	ASTGProjectile(ASTGProjectile&&); \
	ASTGProjectile(const ASTGProjectile&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, ASTGProjectile); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(ASTGProjectile); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(ASTGProjectile) \
	NO_API virtual ~ASTGProjectile();


#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_10_PROLOG
#define FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_13_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_13_RPC_WRAPPERS_NO_PURE_DECLS \
	FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_13_INCLASS_NO_PURE_DECLS \
	FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h_13_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> MCPGAMEPROJECT_API UClass* StaticClass<class ASTGProjectile>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_praca_magisterska_games_unreal_MCPGameProject_Source_MCPGameProject_STGProjectile_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
