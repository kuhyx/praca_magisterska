# Part 1: Project Setup

[← Back to Index](README.md) | [Next: Part 2 - Create the Player →](part-2-create-player.md)

---

## Step 1.1: Create New Project

1. Open Epic Games Launcher
2. Click "Unreal Engine" tab on the left sidebar
3. Click yellow "Launch" button next to your UE5 version
4. Wait for Unreal Engine to open (this may take 1-2 minutes)

5. In the "Unreal Project Browser" window that appears:
   - At the top, select "Games" category (should be selected by default)
   - Click "Blank" template (empty square icon)
   
6. On the right side panel, configure:
   - **Project Defaults:** Blueprint (not C++)
   - **Target Platform:** Desktop
   - **Quality Preset:** Maximum
   - **Starter Content:** UNCHECKED (we don't need it)
   - **Raytracing:** UNCHECKED

7. At the bottom:
   - Choose folder location where you want to save
   - Name the project: `BulletHellGame`
   
8. Click "Create" button (bottom right, yellow)

### Expected Result

Unreal Editor opens with an empty level. You should see:
- Main 3D viewport in the center
- Outliner panel on the right (showing "Untitled" level)
- Details panel on the right side

> **NOTE:** The Content Drawer is NOT open by default. To open it:
> - Click "Content Drawer" button at the bottom of the screen, OR
> - Press `Ctrl+Space`, OR
> - Go to Window → Content Drawer

---

## Step 1.2: Set Up 2D Game View

Since bullet-hell games are typically 2D, we'll set up a top-down orthographic view.

1. In the main viewport, look at the top-left corner
2. Click the dropdown that says "Perspective"
3. Select "Top" from the dropdown menu (`Alt + J`)

4. To set up proper camera for the game:
   - Go to menu bar (the top bar): **Edit** (Second from left, next to "File" and "Window") → **Project Settings**
   - In the left sidebar, search for "Maps & Modes" (Project → 4th from the top, next to GameplayTags and Movies)
   - Click on "Maps & Modes"
   
5. Under "Default Modes":
   - Find "Default GameMode" dropdown
   - We'll create our own later, leave it for now

6. Close Project Settings window (X in top right)

---

## Step 1.3: Create Folder Structure

1. Look at the Content Browser at the bottom of the screen
2. You should see "Content" folder on the left panel

3. Right-click on "Content" folder → **New Folder**
   - Name it: `Blueprints`

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
├── Blueprints/
├── Materials/
├── Sprites/
└── UI/
```

---

[← Back to Index](README.md) | [Next: Part 2 - Create the Player →](part-2-create-player.md)
