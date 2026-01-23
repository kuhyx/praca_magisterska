# Test Scenarios Document
**Project**: Master's Thesis - Game Engine Performance Comparison  
**Date**: January 19, 2026  
**Author**: Krzysztof Rudnicki  

---

## Overview

This document defines the test scenarios for comparing Unity and Unreal Engine performance using bullet-hell games and NVIDIA Nsight profiling.

---

## Test Hardware

- **CPU**: AMD Ryzen 9 7900X3D 12-Core Processor (24 cores, 48 threads)
- **GPU**: NVIDIA GeForce RTX 3090 (24 GB GDDR6X)
- **RAM**: 32 GB
- **OS**: Arch Linux (kernel 6.18.5-arch1-1)
- **NVIDIA Drivers**: 590.48.01

---

## Test Methodology

### Game: Bullet-Hell (Unity & Unreal implementations)

Both games implement identical gameplay mechanics:
- Player-controlled ship
- Enemy spawning system with escalating load
- Bullet pattern generation
- Collision detection
- 90-second survival mode with progressive load increase

> **Note**: The game runs continuously for 90 seconds with three load phases:
> - **0-30 seconds**: Low load phase
> - **30-60 seconds**: Medium load phase  
> - **60-90 seconds**: High load phase

### Performance Metrics to Capture

1. **Frame Time** (ms) - Time to render one frame
2. **FPS** (frames per second) - Derived from frame time
3. **GPU Utilization** (%) - Percentage of GPU capacity used
4. **Memory Usage** (MB) - VRAM and system RAM consumption
5. **Draw Calls** - Number of draw calls per frame
6. **Vertex Count** - Total vertices rendered per frame

---

## Load Phases

### Phase 1: Low Load (0-30 seconds)
**Objective**: Establish baseline performance with minimal load

**Parameters**:
- **Bullet count on screen**: 50-100 bullets
- **Active enemies**: 2-3 enemies
- **Time window**: 0-30 seconds of gameplay

**Expected Outcomes**:
- Stable frame rate (60 FPS target)
- Low GPU utilization (<50%)
- Minimal memory usage

**Nsight Capture Points**:
- 10 seconds (early low load)
- 20 seconds (stable low load)
- 25 seconds (end of low load phase)

---

### Phase 2: Medium Load (30-60 seconds)
**Objective**: Test performance under moderate load

**Parameters**:
- **Bullet count on screen**: 200-300 bullets
- **Active enemies**: 5-7 enemies
- **Time window**: 30-60 seconds of gameplay

**Expected Outcomes**:
- Moderate GPU utilization (50-70%)
- Frame rate may drop slightly
- Increased memory usage

**Nsight Capture Points**:
- 35 seconds (transition to medium load)
- 45 seconds (stable medium load)
- 55 seconds (end of medium load phase)

---

### Phase 3: High Load (60-90 seconds)
**Objective**: Test performance under maximum load (stress test)

**Parameters**:
- **Bullet count on screen**: 500+ bullets
- **Active enemies**: 10+ enemies
- **Time window**: 60-90 seconds of gameplay

**Expected Outcomes**:
- High GPU utilization (>70%)
- Potential frame drops
- Maximum memory usage observed

**Nsight Capture Points**:
- 65 seconds (transition to high load)
- 75 seconds (peak sustained load)
- 85 seconds (end of high load phase)

---

## Data Collection Procedure

### For Each Test Run:

1. **Pre-test Setup**:
   - Run `./scripts/close_background_apps.sh` to close unnecessary applications
   - Verify system is idle

2. **Unity Testing**:
   - Start NVIDIA Nsight Systems (`nsys-ui`)
   - Configure Nsight to profile the Unity game executable
   - Launch Unity bullet-hell game through Nsight
   - Let the game run for full 90 seconds (all three load phases)
   - Nsight captures performance data throughout the entire run
   - Save capture data with naming: `unity_run_[N].nsight-rep`
   - Export metrics to CSV: `unity_metrics_[N].csv`

3. **Unreal Testing**:
   - Close Unity completely
   - Start NVIDIA Nsight Systems (`nsys-ui`)
   - Configure Nsight to profile the Unreal game executable
   - Launch Unreal bullet-hell game through Nsight
   - Let the game run for full 90 seconds (all three load phases)
   - Nsight captures performance data throughout the entire run
   - Save capture data with naming: `unreal_run_[N].nsight-rep`
   - Export metrics to CSV: `unreal_metrics_[N].csv`

4. **Post-test Data Organization**:
   - Organize captures in folders: `data/nsight/unity/` and `data/nsight/unreal/`
   - Compile metrics into master spreadsheet: `performance_comparison.xlsx`
   - Take screenshots of key Nsight analysis views
   - Document any anomalies or issues observed

---

## Expected Data Outputs

### Per Test Run (3 runs per engine, 6 total):
- Nsight capture file (.nsight-rep)
- Metrics CSV with frame time, FPS, GPU %, memory, draw calls, vertices
- Screenshot of Nsight GPU trace for each load phase
- Screenshot of Nsight memory analysis

### Aggregate Data:
- Comparison table: Unity vs Unreal per load phase
- Performance graphs showing all metrics over 90-second timeline
- Statistical analysis (mean, std dev, min, max) per load phase

---

## Quality Assurance

### Validation Checks:
- [ ] All three runs completed for Unity
- [ ] All three runs completed for Unreal
- [ ] All CSV metrics exported
- [ ] Screenshots saved for all load phases
- [ ] Data organized in proper folder structure
- [ ] No system crashes or anomalies during testing
- [ ] Comparable conditions between Unity and Unreal runs

### Data Integrity:
- [ ] Frame times make sense (>0ms, <100ms typically)
- [ ] GPU utilization in valid range (0-100%)
- [ ] Memory values reasonable for game scope
- [ ] No obvious outliers without explanation

---

## Timeline

- **Day 1 (Sunday, Jan 19)**: Setup Nsight, run first test on Unity engine
- **Day 2 (Monday, Jan 20)**: Complete Unity tests (3 runs), run first test on Unreal engine
- **Day 3 (Tuesday, Jan 21)**: Complete Unreal tests (3 runs), verify data integrity
- **Day 4 (Wednesday, Jan 22)**: Analyze results, create comparison graphs, organize data

---

## Notes

- If a capture fails, note the reason and retry
- Document any differences in how load phases manifest in Unity vs Unreal
- Pay attention to engine-specific optimizations that may affect results
- Consider recording video of test runs for reference

---

**Status**: Ready for execution  
**Next Action**: Run `./scripts/close_background_apps.sh` and start Nsight profiling
