#!/bin/bash
# =============================================================================
# Unreal Engine Nsight Profiling Script
# =============================================================================
# Profiles the Unreal Engine bullet-hell game with NVIDIA Nsight Systems
# 
# Supports two build configurations:
#   - Shipping: osrt + GPU metrics only (Vulkan tracing crashes)
#   - Development: Full Vulkan + osrt + GPU metrics
#
# Usage:
#   ./profile_unreal.sh [config] [duration] [output_name]
#
# Arguments:
#   config:     "shipping" or "development" (default: shipping)
#   duration:   Test duration in seconds (default: 95)
#   output_name: Custom output name (default: auto-generated)
#
# Examples:
#   ./profile_unreal.sh                           # Shipping, 95s
#   ./profile_unreal.sh development               # Development with Vulkan, 95s
#   ./profile_unreal.sh shipping 60               # Shipping, 60s
#   ./profile_unreal.sh development 95 my_test    # Development, 95s, custom name
# =============================================================================

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UNREAL_BASE="$PROJECT_DIR/games/unreal/BulletHellGame/BulletHellCPP"

# Parse arguments
CONFIG="${1:-shipping}"
DURATION="${2:-95}"
OUTPUT_NAME_ARG="${3:-}"

# Validate config
if [[ "$CONFIG" != "shipping" && "$CONFIG" != "development" ]]; then
    echo "Error: config must be 'shipping' or 'development', got: $CONFIG"
    exit 1
fi

# Set paths based on configuration
if [[ "$CONFIG" == "shipping" ]]; then
    UNREAL_GAME="$UNREAL_BASE/Saved/StagedBuilds/Linux/BulletHellCPP.sh"
    DATA_DIR="$PROJECT_DIR/data/nsight/unreal/shipping"
    DEFAULT_PREFIX="unreal_shipping"
    TRACE_OPTS="osrt"
    TRACE_DESC="osrt + GPU metrics (Vulkan crashes Shipping builds)"
else
    UNREAL_GAME="$UNREAL_BASE/Saved/StagedBuilds/LinuxDevelopment/BulletHellCPP.sh"
    DATA_DIR="$PROJECT_DIR/data/nsight/unreal/development"
    DEFAULT_PREFIX="unreal_dev"
    TRACE_OPTS="vulkan,osrt"
    TRACE_DESC="Vulkan + osrt + GPU metrics"
fi

# Set output name
if [[ -n "$OUTPUT_NAME_ARG" ]]; then
    OUTPUT_NAME="$OUTPUT_NAME_ARG"
else
    OUTPUT_NAME="${DEFAULT_PREFIX}_$(date +%Y%m%d_%H%M%S)"
fi
OUTPUT_PATH="$DATA_DIR/$OUTPUT_NAME"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}${BOLD}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         UNREAL ENGINE NSIGHT PROFILING                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Build:       ${CONFIG^^}"
echo "  Duration:    ${DURATION}s"
echo "  Tracing:     ${TRACE_DESC}"
echo "  Output:      ${OUTPUT_PATH}.nsys-rep"
echo "  Game:        ${UNREAL_GAME}"
echo ""

# Check if game exists
if [ ! -f "$UNREAL_GAME" ]; then
    echo -e "${RED}Error: Unreal game not found at $UNREAL_GAME${NC}"
    echo ""
    if [[ "$CONFIG" == "shipping" ]]; then
        echo "Please package the game first via Unreal Editor:"
        echo "  1. File → Package Project → Build Configuration → Shipping"
        echo "  2. File → Package Project → Linux"
    else
        echo "Please package a Development build via Unreal Editor:"
        echo "  1. File → Package Project → Build Configuration → Development"
        echo "  2. File → Package Project → Linux"
        echo ""
        echo "The Development build should be saved to:"
        echo "  $UNREAL_BASE/Saved/StagedBuilds/LinuxDevelopment/"
    fi
    exit 1
fi

# Create output directory
mkdir -p "$DATA_DIR"

# Step 1: Run profiler
echo -e "${CYAN}[1/4] Running Nsight profiler (${DURATION}s)...${NC}"
echo -e "${YELLOW}Tracing: ${TRACE_DESC}${NC}"
nsys profile \
    --output="$OUTPUT_PATH" \
    --trace="$TRACE_OPTS" \
    --gpu-metrics-devices=0 \
    --duration="$DURATION" \
    --force-overwrite=true \
    --wait=all \
    -- "$UNREAL_GAME" --invincible --stationary

echo -e "${GREEN}✓ Profiling complete${NC}"
echo ""

# Step 2: Export OS runtime summary
echo -e "${CYAN}[2/4] Exporting OS runtime summary...${NC}"
nsys stats -r osrt_sum --format csv \
    -o "${OUTPUT_PATH}" \
    "${OUTPUT_PATH}.nsys-rep" 2>&1 | grep -E "PROCESSED|SKIPPED" || true
echo -e "${GREEN}✓ OS runtime summary exported${NC}"
echo ""

# Step 3: Export Vulkan summary (only for Development builds)
if [[ "$CONFIG" == "development" ]]; then
    echo -e "${CYAN}[3/4] Exporting Vulkan API summary...${NC}"
    nsys stats -r vulkan_api_sum --format csv \
        -o "${OUTPUT_PATH}" \
        "${OUTPUT_PATH}.nsys-rep" 2>&1 | grep -E "PROCESSED|SKIPPED" || true
    echo -e "${GREEN}✓ Vulkan API summary exported${NC}"
else
    echo -e "${CYAN}[3/4] Skipping Vulkan export (not available in Shipping)${NC}"
fi
echo ""

# Step 4: Export GPU metrics summary
echo -e "${CYAN}[4/4] Exporting GPU metrics summary...${NC}"
SQLITE_FILE="${OUTPUT_PATH}.sqlite"
if [ -f "$SQLITE_FILE" ]; then
    sqlite3 -header -csv "$SQLITE_FILE" "
    SELECT 
        t.metricName,
        COUNT(*) as samples,
        ROUND(AVG(m.value), 2) as avg_value,
        MIN(m.value) as min_value,
        MAX(m.value) as max_value
    FROM GPU_METRICS m 
    JOIN TARGET_INFO_GPU_METRICS t ON m.metricId = t.metricId
    GROUP BY t.metricName
    " > "${OUTPUT_PATH}_gpu_metrics.csv"
    echo -e "${GREEN}✓ GPU metrics exported${NC}"
fi
echo ""

# Get report size
REPORT_SIZE=$(ls -lh "${OUTPUT_PATH}.nsys-rep" | awk '{print $5}')

# Get GPU utilization metrics
GPU_ACTIVE="N/A"
GR_ACTIVE="N/A"
SM_ACTIVE="N/A"
if [ -f "$SQLITE_FILE" ]; then
    GPU_ACTIVE=$(sqlite3 "$SQLITE_FILE" "SELECT ROUND(AVG(m.value), 1) FROM GPU_METRICS m JOIN TARGET_INFO_GPU_METRICS t ON m.metricId = t.metricId WHERE t.metricName = 'GPU Active [Throughput %]';" 2>/dev/null || echo "N/A")
    GR_ACTIVE=$(sqlite3 "$SQLITE_FILE" "SELECT ROUND(AVG(m.value), 1) FROM GPU_METRICS m JOIN TARGET_INFO_GPU_METRICS t ON m.metricId = t.metricId WHERE t.metricName = 'GR Active [Throughput %]';" 2>/dev/null || echo "N/A")
    SM_ACTIVE=$(sqlite3 "$SQLITE_FILE" "SELECT ROUND(AVG(m.value), 1) FROM GPU_METRICS m JOIN TARGET_INFO_GPU_METRICS t ON m.metricId = t.metricId WHERE t.metricName = 'SMs Active [Throughput %]';" 2>/dev/null || echo "N/A")
fi

# Get frame count for Development builds (Vulkan data available)
FRAME_COUNT="N/A"
FPS="N/A"
if [[ "$CONFIG" == "development" ]] && [ -f "$SQLITE_FILE" ]; then
    FRAME_COUNT=$(sqlite3 "$SQLITE_FILE" "SELECT COUNT(*) FROM VULKAN_API WHERE nameId IN (SELECT id FROM StringIds WHERE value='vkQueuePresentKHR');" 2>/dev/null || echo "N/A")
    if [[ "$FRAME_COUNT" != "N/A" && "$FRAME_COUNT" -gt 0 ]]; then
        FPS=$(echo "scale=2; $FRAME_COUNT / $DURATION" | bc)
    fi
fi

# Display summary
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}${BOLD}                    PROFILING RESULTS                       ${NC}"
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Test Configuration:${NC}"
echo "  Build:         ${CONFIG^^}"
echo "  Duration:      ${DURATION} seconds"
echo "  Mode:          Stationary + Invincible"
echo ""

if [[ "$CONFIG" == "development" ]]; then
    echo -e "${YELLOW}Frame Performance:${NC}"
    echo "  Frame Count:   ${FRAME_COUNT}"
    echo "  Average FPS:   ${FPS}"
    echo ""
fi

echo -e "${YELLOW}GPU Utilization Metrics:${NC}"
echo "  GPU Active:    ${GPU_ACTIVE}%"
echo "  GR Active:     ${GR_ACTIVE}%"
echo "  SMs Active:    ${SM_ACTIVE}%"
echo ""

echo -e "${YELLOW}Generated Files:${NC}"
echo "  Report:        ${OUTPUT_PATH}.nsys-rep (${REPORT_SIZE})"
echo "  SQLite:        ${OUTPUT_PATH}.sqlite"
for f in "${OUTPUT_PATH}"*.csv; do
    if [ -f "$f" ]; then
        echo "  CSV:           $(basename "$f")"
    fi
done
echo ""

# Display OSRT API top 10
echo -e "${YELLOW}OS Runtime API Summary (Top 10 by time):${NC}"
nsys stats -r osrt_sum "${OUTPUT_PATH}.nsys-rep" 2>&1 | grep -A 13 "Time (%)" | head -13
echo ""

echo -e "${GREEN}${BOLD}Done!${NC}"
echo ""
echo "To view full report in Nsight UI:"
echo "  nsys-ui ${OUTPUT_PATH}.nsys-rep"
