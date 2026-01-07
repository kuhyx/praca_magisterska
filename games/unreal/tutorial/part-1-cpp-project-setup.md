# Part 1 (C++): Project Setup

[← Back to Index](README.md) | [Next: Part 2 (C++) - Create the Player →](part-2-cpp-create-player.md)

---

## Overview

This is the **C++ version** of Part 1. Unlike the Blueprint tutorial which creates a Blueprint-only project, we'll create a **C++ project** from the start. This enables:

- ✅ Copy-paste variable definitions instead of clicking UI
- ✅ Version control friendly (readable diffs)
- ✅ Faster development (define 12 variables in 30 seconds vs 15 minutes)

---

## Step 1.1: Create New C++ Project

1. Open Epic Games Launcher
2. Click "Unreal Engine" tab on the left sidebar
3. Click yellow "Launch" button next to your UE5 version
4. Wait for Unreal Engine to open (this may take 1-2 minutes)

5. In the "Unreal Project Browser" window that appears:
   - At the top, select "Games" category (should be selected by default)
   - Click "Blank" template (empty square icon)

6. On the right side panel, configure:
   - **Project Defaults:** **C++** ⚠️ (NOT Blueprint!)
   - **Target Platform:** Desktop
   - **Quality Preset:** Maximum (or Scalable for faster iteration)
   - **Starter Content:** UNCHECKED (we don't need it)
   - **Raytracing:** UNCHECKED

7. At the bottom:
   - Choose folder location where you want to save
   - Name the project: `BulletHellGame`

8. Click "Create" button (bottom right, yellow)

### What Happens Next

Unreal will:
1. Generate C++ project files (~30 seconds)
2. **Open your IDE** (Visual Studio, Rider, or VS Code)
3. **Compile the initial project** (2-5 minutes, first time only)
4. Open Unreal Editor

> **⚠️ IMPORTANT:** Do NOT close the IDE or compilation window! Wait for compilation to finish.

### Expected Result

After compilation completes:

- **Unreal Editor opens** with an empty level
- **Your IDE is open** with the project (Visual Studio/Rider/VS Code)
- Main 3D viewport in the center
- Outliner panel on the right (showing "Untitled" level)

### Troubleshooting

<details>
<summary><b>IDE didn't open?</b></summary>

- Check if Visual Studio or Rider is installed
- Go to `Edit → Editor Preferences → Source Code`
- Set "Source Code Editor" to your preferred IDE
- Right-click the `.uproject` file → "Generate Visual Studio project files"
- Open the `.sln` file in your IDE

</details>

<details>
<summary><b>Compilation failed?</b></summary>

- Check the Output Log (Window → Developer Tools → Output Log)
- Common issue: Missing Visual Studio C++ tools
  - Install "Desktop Development with C++" workload in Visual Studio Installer
- Try: `File → Refresh Visual Studio Project`

</details>

---

## Step 1.2: Verify C++ Project Structure

Before continuing, verify the C++ files were created:

1. In your file explorer, navigate to your project folder
2. You should see:

```
BulletHellGame/
├── BulletHellGame.uproject          # Project file
├── Source/                           # ⭐ C++ source code (this is new!)
│   └── BulletHellGame/
│       ├── BulletHellGame.h
│       ├── BulletHellGame.cpp
│       ├── BulletHellGame.Build.cs  # Build configuration
│       └── BulletHellGameGameMode.h/cpp  # Auto-generated
├── Content/                          # Assets and Blueprints
├── Config/                           # Project settings
├── Binaries/                         # Compiled code (gitignore this)
├── Intermediate/                     # Build artifacts (gitignore this)
└── BulletHellGame.sln               # Visual Studio solution (if using VS)
```

The `Source/` folder is what makes this a C++ project! This is where we'll add our game classes.

---

## Step 1.3: Set Up 2D Game View

Same as Blueprint tutorial:

1. In the main viewport, look at the top-left corner
2. Click the dropdown that says "Perspective"
3. Select "Top" from the dropdown menu (`Alt + J`)

---

## Step 1.4: Create Folder Structure

1. Open Content Browser (or Content Drawer with `Ctrl+Space`)
2. You should see "Content" folder on the left panel

3. Right-click on "Content" folder → **New Folder**
   - Name it: `Blueprints` (we'll use these for visual-only children)

4. Right-click on "Content" folder → **New Folder**
   - Name it: `Materials`

5. Right-click on "Content" folder → **New Folder**
   - Name it: `Sprites` (for 2D textures)

6. Right-click on "Content" folder → **New Folder**
   - Name it: `UI`

### Expected Result

Content Browser shows 4 folders:

```
Content/
├── Blueprints/    (For Blueprint children that inherit from C++)
├── Materials/
├── Sprites/
└── UI/
```

**AND** you should also see:

```
C++ Classes/
└── BulletHellGame/
    └── BulletHellGameGameMode  (Auto-generated C++ class)
```

This "C++ Classes" folder shows all C++ classes in the project.

---

## Step 1.5: Configure .gitignore (Recommended)

If using version control, create `.gitignore` in your project root:

```gitignore
# Unreal Engine
Binaries/
DerivedDataCache/
Intermediate/
Saved/

# IDE
*.sln
*.suo
*.opensdf
*.sdf
*.VC.db
*.VC.opendb
.vs/
.vscode/
.idea/

# Build artifacts
Build/
Releases/
```

This prevents committing large binary files and build artifacts.

---

## Comparison: C++ vs Blueprint Project

| Aspect | Blueprint Project | C++ Project |
|--------|------------------|-------------|
| Project creation time | ~30 seconds | ~5 minutes (first time) |
| Source/ folder | ❌ No | ✅ Yes |
| IDE integration | ❌ No | ✅ Yes |
| Can add C++ classes | ❌ Requires migration | ✅ Ready to go |
| Compile time | None (Blueprints) | 30-60 sec per change |
| Hot reload | Instant | Limited support |

**Key Difference:** C++ project has the `Source/` folder from the start. Blueprint projects require manual migration to add C++ support later.

---

## What's Next?

In Part 2, we'll create the player ship as a **C++ class** instead of a Blueprint. You'll see how defining 12 variables takes 30 seconds with copy-paste instead of 15 minutes with UI clicks.

---

[← Back to Index](README.md) | [Next: Part 2 (C++) - Create the Player →](part-2-cpp-create-player.md)
