#!/bin/bash
# =============================================================================
# Unified Nsight Profiling Script for Unity and Unreal Engine
# =============================================================================
# Profiles games using NVIDIA Nsight Systems with identical metrics for both engines.
# Uses phased profiling (3 x 30 seconds) to avoid data overload crashes.
#
# Usage:
#   ./profile.sh <engine> [phase]
#
# Arguments:
#   engine: "unity" or "unreal"
#   phase:  1, 2, 3, or "all" (default: all)
#
# Examples:
#   ./profile.sh unity          # Profile Unity, all phases
#   ./profile.sh unreal         # Profile Unreal, all phases
#   ./profile.sh unreal 1       # Profile Unreal, phase 1 only
#   ./profile.sh unity all      # Profile Unity, all phases
# =============================================================================

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Game executables
UNITY_EXE="$PROJECT_DIR/magisterka_2/Final.x86_64"
UNREAL_DIR="$PROJECT_DIR/games/unreal/BulletHellGame/BulletHellCPP/Linux"
UNREAL_EXE="$UNREAL_DIR/BulletHellCPP/Binaries/Linux/BulletHellCPP-Linux-DebugGame"

# Arguments
ENGINE="${1:-}"
PHASE="${2:-all}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

# Validate engine argument
if [[ -z "$ENGINE" ]]; then
    echo -e "${RED}Error: Engine argument required${NC}"
    echo ""
    echo "Usage: $0 <engine> [phase]"
    echo "  engine: 'unity' or 'unreal'"
    echo "  phase:  1, 2, 3, or 'all' (default: all)"
    exit 1
fi

if [[ "$ENGINE" != "unity" && "$ENGINE" != "unreal" ]]; then
    echo -e "${RED}Error: Engine must be 'unity' or 'unreal', got: $ENGINE${NC}"
    exit 1
fi

# Set engine-specific configuration
if [[ "$ENGINE" == "unity" ]]; then
    GAME_EXE="$UNITY_EXE"
    GAME_ARGS="-force-vulkan --invincible --stationary"
    DATA_DIR="$PROJECT_DIR/data/nsight/unity"
    OUTPUT_PREFIX="unity"
    WORK_DIR="$PROJECT_DIR"
else
    GAME_EXE="$UNREAL_EXE"
    GAME_ARGS="BulletHellCPP --invincible --stationary"
    DATA_DIR="$PROJECT_DIR/data/nsight/unreal"
    OUTPUT_PREFIX="unreal"
    WORK_DIR="$UNREAL_DIR"
fi

# Phase configuration
PHASE_DURATION=35  # 30s game + 5s buffer

# Check if game exists
if [ ! -f "$GAME_EXE" ]; then
    echo -e "${RED}Error: Game executable not found at $GAME_EXE${NC}"
    exit 1
fi

# Create output directory
mkdir -p "$DATA_DIR"

# Function to run a single phase
run_phase() {
    local phase_num=$1
    local start_time=$2
    local output_name="${OUTPUT_PREFIX}_phase${phase_num}_${start_time}s"
    local output_path="$DATA_DIR/$output_name"

    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  PHASE ${phase_num}: Starting at ${start_time}s${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"

    # Clean up any previous processes
    pkill -9 nsys 2>/dev/null || true
    pkill -9 -f "$(basename "$GAME_EXE")" 2>/dev/null || true
    sleep 2

    # Clean nsight temp files
    /bin/rm -rf /tmp/nvidia/nsight_systems/* 2>/dev/null || true

    echo -e "${YELLOW}Running Nsight profiler for ${PHASE_DURATION}s...${NC}"
    echo -e "${YELLOW}Tracing: vulkan + osrt + GPU metrics${NC}"

    # Build game arguments with start time
    local full_args="$GAME_ARGS"
    if [[ "$ENGINE" == "unreal" ]]; then
        full_args="$GAME_ARGS --start-time=$start_time"
    fi

    # Run profiler
    cd "$WORK_DIR"
    nsys profile \
        --trace=vulkan,osrt \
        --gpu-metrics-devices=0 \
        --sample=none \
        --cpuctxsw=none \
        --output="$output_path" \
        --duration=$PHASE_DURATION \
        --force-overwrite=true \
        -- "$GAME_EXE" $full_args || true

    echo -e "${GREEN}✓ Phase ${phase_num} profiling complete${NC}"

    # Export data if capture succeeded
    if [ -f "${output_path}.nsys-rep" ]; then
        echo -e "${YELLOW}Exporting stats...${NC}"

        # Export to SQLite
        nsys export --type sqlite -o "${output_path}.sqlite" "${output_path}.nsys-rep" 2>/dev/null || true

        # Export Vulkan API summary
        nsys stats -r vulkan_api_sum --format csv -o "${output_path}_vulkan_api" "${output_path}.nsys-rep" 2>/dev/null || true

        # Export OS runtime summary
        nsys stats -r osrt_sum --format csv -o "${output_path}_osrt" "${output_path}.nsys-rep" 2>/dev/null || true

        # Export GPU metrics if available
        if [ -f "${output_path}.sqlite" ]; then
            sqlite3 -header -csv "${output_path}.sqlite" "
            SELECT
                t.metricName,
                COUNT(*) as samples,
                ROUND(AVG(m.value), 2) as avg_value,
                MIN(m.value) as min_value,
                MAX(m.value) as max_value
            FROM GPU_METRICS m
            JOIN TARGET_INFO_GPU_METRICS t ON m.metricId = t.metricId
            GROUP BY t.metricName
            ORDER BY samples DESC;
            " > "${output_path}_gpu_metrics.csv" 2>/dev/null || true

            # Get frame count from Vulkan data
            FRAMES=$(sqlite3 "${output_path}.sqlite" "SELECT COUNT(*) FROM VULKAN_API WHERE nameId IN (SELECT id FROM StringIds WHERE value='vkQueuePresentKHR');" 2>/dev/null || echo "0")
            FPS=$(echo "scale=2; $FRAMES / 30" | bc 2>/dev/null || echo "N/A")

            echo -e "${GREEN}  Frames: ${FRAMES}, FPS: ${FPS}${NC}"
        fi

        local file_size=$(ls -lh "${output_path}.nsys-rep" | awk '{print $5}')
        echo -e "${GREEN}✓ Exported: ${output_name}.nsys-rep (${file_size})${NC}"
    else
        echo -e "${RED}✗ Phase ${phase_num} capture failed${NC}"
    fi

    echo ""
    sleep 3  # Cool-down between phases
}

# Function to display summary
display_summary() {
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}${BOLD}                    PROFILING SUMMARY                       ${NC}"
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -e "${YELLOW}Engine: ${ENGINE^^}${NC}"
    echo -e "${YELLOW}Output directory: ${DATA_DIR}${NC}"
    echo ""

    echo -e "${YELLOW}Generated files:${NC}"
    ls -la "$DATA_DIR"/${OUTPUT_PREFIX}_phase*.nsys-rep 2>/dev/null || echo "  No report files found"
    echo ""

    # Calculate total frames and FPS from all phases
    local total_frames=0
    local phases_count=0

    for phase in 1 2 3; do
        local sqlite_file="$DATA_DIR/${OUTPUT_PREFIX}_phase${phase}_*s.sqlite"
        sqlite_file=$(ls $sqlite_file 2>/dev/null | head -1)
        if [ -f "$sqlite_file" ]; then
            local frames=$(sqlite3 "$sqlite_file" "SELECT COUNT(*) FROM VULKAN_API WHERE nameId IN (SELECT id FROM StringIds WHERE value='vkQueuePresentKHR');" 2>/dev/null || echo "0")
            echo -e "  Phase $phase: ${frames} frames"
            total_frames=$((total_frames + frames))
            phases_count=$((phases_count + 1))
        fi
    done

    if [ $phases_count -gt 0 ]; then
        local total_duration=$((phases_count * 30))
        local avg_fps=$(echo "scale=2; $total_frames / $total_duration" | bc)
        echo ""
        echo -e "${GREEN}Total frames: ${total_frames}${NC}"
        echo -e "${GREEN}Average FPS: ${avg_fps}${NC}"
    fi

    echo ""
    echo -e "${GREEN}${BOLD}Done!${NC}"
}

# Main execution
echo -e "${CYAN}${BOLD}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     UNIFIED NSIGHT PROFILING (${ENGINE^^})                   "
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Engine:        ${ENGINE^^}"
echo "  Game:          ${GAME_EXE}"
echo "  Output dir:    ${DATA_DIR}"
echo "  Phase:         ${PHASE}"
echo "  Tracing:       vulkan + osrt + GPU metrics"
echo ""

case "$PHASE" in
    1)
        run_phase 1 0
        display_summary
        ;;
    2)
        run_phase 2 30
        display_summary
        ;;
    3)
        run_phase 3 60
        display_summary
        ;;
    all)
        echo -e "${CYAN}Running all 3 phases (3 x 30 seconds = 90 seconds total)${NC}"
        echo ""

        run_phase 1 0
        run_phase 2 30
        run_phase 3 60

        display_summary
        ;;
    *)
        echo -e "${RED}Error: Phase must be 1, 2, 3, or 'all', got: $PHASE${NC}"
        exit 1
        ;;
esac
