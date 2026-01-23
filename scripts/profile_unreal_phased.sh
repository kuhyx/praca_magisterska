#!/bin/bash
# =============================================================================
# Unreal Engine Phased Nsight Profiling Script
# =============================================================================
# Profiles the Unreal Engine game in 3 phases to avoid Nsight agent crashes
#
# Usage:
#   ./profile_unreal_phased.sh [phase]
#
# Arguments:
#   phase: 1, 2, 3, or "all" (default: all)
#     Phase 1: 0-30 seconds (--start-time=0)
#     Phase 2: 30-60 seconds (--start-time=30)
#     Phase 3: 60-90 seconds (--start-time=60)
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UNREAL_DIR="$PROJECT_DIR/games/unreal/BulletHellGame/BulletHellCPP/Linux"
UNREAL_EXE="$UNREAL_DIR/BulletHellCPP/Binaries/Linux/BulletHellCPP-Linux-DebugGame"
DATA_DIR="$PROJECT_DIR/data/nsight/unreal/debug"

PHASE="${1:-all}"
PHASE_DURATION=35  # 30s game + 5s buffer

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

mkdir -p "$DATA_DIR"

run_phase() {
    local phase_num=$1
    local start_time=$2
    local output_name="unreal_phase${phase_num}_${start_time}s"
    
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  PHASE ${phase_num}: Starting at ${start_time}s${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    
    # Clean up any previous nsys processes
    pkill -9 nsys 2>/dev/null || true
    pkill -9 -f BulletHellCPP 2>/dev/null || true
    sleep 2
    
    # Clean nsight temp files
    /bin/rm -rf /tmp/nvidia/nsight_systems/* 2>/dev/null || true
    
    echo -e "${YELLOW}Running Nsight profiler for ${PHASE_DURATION}s...${NC}"
    
    cd "$UNREAL_DIR"
    nsys profile \
        --trace=osrt,vulkan \
        --gpu-metrics-devices=0 \
        --sample=none \
        --cpuctxsw=none \
        --output="$DATA_DIR/$output_name" \
        --duration=$PHASE_DURATION \
        --force-overwrite=true \
        "$UNREAL_EXE" BulletHellCPP --invincible --stationary --start-time=$start_time || true
    
    echo -e "${GREEN}✓ Phase ${phase_num} complete${NC}"
    
    # Export data if capture succeeded
    if [ -f "$DATA_DIR/${output_name}.nsys-rep" ]; then
        echo -e "${YELLOW}Exporting stats...${NC}"
        nsys export --type sqlite -o "$DATA_DIR/${output_name}.sqlite" "$DATA_DIR/${output_name}.nsys-rep" 2>/dev/null || true
        nsys stats -r osrt_sum --format csv -o "$DATA_DIR/$output_name" "$DATA_DIR/${output_name}.nsys-rep" 2>/dev/null || true
        nsys stats -r vulkan_api_sum --format csv -o "$DATA_DIR/$output_name" "$DATA_DIR/${output_name}.nsys-rep" 2>/dev/null || true
        
        # Export GPU metrics if available
        if [ -f "$DATA_DIR/${output_name}.sqlite" ]; then
            sqlite3 -header -csv "$DATA_DIR/${output_name}.sqlite" "
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
            " > "$DATA_DIR/${output_name}_gpu_metrics.csv" 2>/dev/null || true
        fi
        
        local file_size=$(ls -lh "$DATA_DIR/${output_name}.nsys-rep" | awk '{print $5}')
        echo -e "${GREEN}✓ Exported: ${output_name}.nsys-rep (${file_size})${NC}"
    else
        echo -e "${RED}✗ Phase ${phase_num} capture failed${NC}"
    fi
    
    echo ""
    sleep 3  # Cool-down between phases
}

case "$PHASE" in
    1)
        run_phase 1 0
        ;;
    2)
        run_phase 2 30
        ;;
    3)
        run_phase 3 60
        ;;
    all)
        echo -e "${CYAN}${BOLD}"
        echo "╔═══════════════════════════════════════════════════════════╗"
        echo "║     UNREAL ENGINE PHASED PROFILING (3 x 30 seconds)      ║"
        echo "╚═══════════════════════════════════════════════════════════╝"
        echo -e "${NC}"
        
        run_phase 1 0
        run_phase 2 30
        run_phase 3 60
        
        echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  ALL PHASES COMPLETE${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
        
        # List captured files
        echo ""
        echo "Captured files:"
        ls -la "$DATA_DIR"/unreal_phase*.nsys-rep 2>/dev/null || echo "No captures found"
        ;;
    *)
        echo "Usage: $0 [1|2|3|all]"
        exit 1
        ;;
esac
