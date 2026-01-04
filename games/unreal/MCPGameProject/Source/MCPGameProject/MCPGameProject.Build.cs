// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class MCPGameProject : ModuleRules
{
	public MCPGameProject(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { 
			"Core", 
			"CoreUObject", 
			"Engine", 
			"InputCore", 
			"EnhancedInput",
			"UMG",
			"Slate",
			"SlateCore",
			"Niagara"
		});

		PrivateDependencyModuleNames.AddRange(new string[] {  });
	}
}
