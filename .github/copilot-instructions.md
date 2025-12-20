# Copilot Instructions for Game Engine Comparison Thesis

## Project Overview

This is a **master's thesis** (praca magisterska) at Warsaw University of Technology (Politechnika Warszawska), Faculty of Electronics and Information Technology (EiTI). The thesis compares performance and capabilities of modern game engines, primarily **Unity vs Unreal Engine**.

### Repository Structure

- **`latex/`** - LaTeX thesis document using WUT-Thesis template
- **`magisterka_2/`** - Unity bullet-hell demo game (performance testing, newer version)
- **`games/unity/magisterka_1/`** - Unity bullet-hell demo (earlier iteration)
- **`My project/`** - Unity 3D Tic-Tac-Toe demo (URP pipeline)
- **`transcripts/`** - Interview transcripts with game developers (Polish)
- **`raw_observations/`** - Research observations and images

## Performance Testing

### Tools
- **NVIDIA Nsight** - Primary profiling tool for comparing GPU/CPU performance between Unity and Unreal implementations

### Methodology
Performance comparisons are made using equivalent bullet-hell game implementations in both engines. Metrics captured include frame time, draw calls, GPU utilization, and memory allocation patterns.

## LaTeX Thesis

### Build Commands
```bash
cd latex
scons quick          # Fast build using SCons
scons                # Full build with all checks
```

### Document Configuration (main.tex)
- **Faculty**: `\facultyeiti` (Electronics and IT)
- **Thesis type**: `\MasterThesis`
- **Language**: `\langpol` (Polish)
- **Bibliography**: BibLaTeX with `bibliografia.bib`

### Chapter Structure
Chapters are in `latex/tex/` following pattern `N-name.tex`:
1. `1-wstep.tex` - Introduction and methodology
2. `2-przeglad-literatury.tex` - Literature review
3. `3-silniki-gier.tex` - Game engine characteristics (Unity, Unreal, Godot)
4. `4-metodologia.tex` - Research methodology
5. `5-testy-wydajnosci.tex` - Performance tests
6. `6-analiza-mozliwosci.tex` - Capabilities analysis
7. `7-porownanie-wynikow.tex` - Results comparison
8. `8-podsumowanie.tex` - Conclusions

### LaTeX Conventions
- Images go in `latex/tex/img/`
- Use `\input{tex/N-filename}` for chapters
- Tables: caption above, `\label{tab:name}`, centered
- Figures: caption below, `\label{fig:name}`

## Unity Projects

### magisterka_2 (Bullet Hell Game)
**Namespace**: `Magisterka.BulletHell`

Key architecture patterns:
- **Bootstrap pattern**: `GameBootstrap.cs` ensures `GameInitializer` exists via `RuntimeInitializeOnLoadMethod`
- **Singleton managers**: `GameDirector.Instance` for global game state
- **Object pooling**: `BulletPool.cs` for performance-critical bullet spawning
- **Component composition**: Enemies use `[RequireComponent(typeof(Health))]`

Core scripts:
- `GameDirector.cs` - Timer, victory detection, difficulty pacing
- `EnemySpawner.cs` + `EnemyController.cs` - Enemy lifecycle
- `BulletPool.cs` - Object pooling with warm capacity
- `PlayerController.cs` - Player input and movement

### My project (Tic-Tac-Toe 3D)
**Namespace**: `TicTacToe3D`

Uses Unity's Universal Render Pipeline (URP). Simpler architecture for 3D showcase:
- `TicTacToeGameManager.cs` - Game logic, board generation, win detection
- `Tile.cs` - Individual tile interaction

## Research Data

### Interview Transcripts (`transcripts/`)
Polish-language interviews with Unity/Unreal developers.

**Participant Criteria**: Minimum 1 year of amateur or professional experience in at least one engine.

**Question Template**:
1. Years of professional/amateur experience per engine
2. Number of projects completed in each engine
3. Architecture comparison (C++ vs C#)
4. Collaboration workflows (working with teams, non-technical members)
5. Official documentation quality
6. Unofficial guides (YouTube tutorials, community resources)
7. AI/LLM usage in development workflow
8. Anticipated future features
9. External tool support (Git, Blender, etc.)
10. Free section (open-ended observations)

When working with transcripts, preserve original Polish text and speaker attributions.

## Code Style Guidelines

### C# (Unity)
- XML doc comments (`/// <summary>`) on public classes/methods
- `[SerializeField]` for inspector-exposed private fields
- Prefix private fields with underscore: `_spawner`, `_bulletPool`
- Use namespaces matching project: `Magisterka.BulletHell`, `TicTacToe3D`

### LaTeX
- Polish language for main content
- English abstracts via `\secondabstract`
- Follow WUT editorial requirements (margins, fonts per `wut-thesis.cls`)
