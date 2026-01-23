#!/bin/bash
# =============================================================================
# Unity Nsight Profiling Script
# =============================================================================
# Profiles the Unity bullet-hell game with NVIDIA Nsight Systems
#
# Usage:
#   ./profile_unity.sh [duration_seconds] [output_name]
#
# Examples:
#   ./profile_unity.sh              # 95s profile, default name
#   ./profile_unity.sh 60           # 60s profile
#   ./profile_unity.sh 95 my_test   # 95s profile, custom name
# =============================================================================

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_DIR/data/nsight"
UNITY_GAME="$PROJECT_DIR/magisterka_2/Final.x86_64"

# Arguments
DURATION="${1:-95}"
OUTPUT_NAME="${2:-unity_$(date +%Y%m%d_%H%M%S)}"
OUTPUT_PATH="$DATA_DIR/$OUTPUT_NAME"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}${BOLD}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           UNITY NSIGHT PROFILING                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Duration:    ${DURATION}s"
echo "  Output:      ${OUTPUT_PATH}.nsys-rep"
echo "  Game:        ${UNITY_GAME}"
echo ""

# Create output directory
mkdir -p "$DATA_DIR"

# Step 1: Run profiler
echo -e "${CYAN}[1/4] Running Nsight profiler (${DURATION}s)...${NC}"
nsys profile \
    --output="$OUTPUT_PATH" \
    --trace=vulkan,osrt \
    --duration="$DURATION" \
    --force-overwrite=true \
    -- "$UNITY_GAME" -force-vulkan --invincible --stationary

echo -e "${GREEN}✓ Profiling complete${NC}"
echo ""

# Step 2: Export Vulkan API summary
echo -e "${CYAN}[2/4] Exporting Vulkan API summary...${NC}"
nsys stats -r vulkan_api_sum --format csv \
    -o "${OUTPUT_PATH}_vulkan_api_sum" \
    "${OUTPUT_PATH}.nsys-rep" 2>&1 | grep -E "PROCESSED|SKIPPED" || true
echo -e "${GREEN}✓ Vulkan summary exported${NC}"

# Step 3: Export OS runtime summary
echo -e "${CYAN}[3/4] Exporting OS runtime summary...${NC}"
nsys stats -r osrt_sum --format csv \
    -o "${OUTPUT_PATH}_osrt_sum" \
    "${OUTPUT_PATH}.nsys-rep" 2>&1 | grep -E "PROCESSED|SKIPPED" || true
echo -e "${GREEN}✓ OS runtime summary exported${NC}"
echo ""

# Step 4: Calculate and display results
echo -e "${CYAN}[4/4] Analyzing results...${NC}"
echo ""

# Get frame count from SQLite
SQLITE_FILE="${OUTPUT_PATH}.sqlite"
if [ -f "$SQLITE_FILE" ]; then
    FRAMES=$(sqlite3 "$SQLITE_FILE" "SELECT COUNT(*) FROM VULKAN_API WHERE nameId IN (SELECT id FROM StringIds WHERE value='vkQueuePresentKHR');" 2>/dev/null || echo "0")
    FPS=$(echo "scale=2; $FRAMES / $DURATION" | bc)
else
    FRAMES="N/A"
    FPS="N/A"
fi

# Get report size
REPORT_SIZE=$(ls -lh "${OUTPUT_PATH}.nsys-rep" | awk '{print $5}')

# Display summary
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}${BOLD}                    PROFILING RESULTS                       ${NC}"
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Performance Metrics:${NC}"
echo "  Duration:      ${DURATION} seconds"
echo "  Total Frames:  ${FRAMES}"
echo "  Average FPS:   ${FPS}"
echo ""

echo -e "${YELLOW}Generated Files:${NC}"
echo "  Report:        ${OUTPUT_PATH}.nsys-rep (${REPORT_SIZE})"
echo "  SQLite:        ${OUTPUT_PATH}.sqlite"
ls "${OUTPUT_PATH}"*.csv 2>/dev/null | while read f; do
    echo "  CSV:           $(basename "$f")"
done
echo ""

# Display Vulkan API top 10
echo -e "${YELLOW}Vulkan API Summary (Top 10 by time):${NC}"
nsys stats -r vulkan_api_sum "${OUTPUT_PATH}.nsys-rep" 2>&1 | grep -A 15 "Time (%)" | head -13
echo ""

echo -e "${GREEN}${BOLD}Done!${NC}"
echo ""
echo "To view full report in Nsight UI:"
echo "  nsys-ui ${OUTPUT_PATH}.nsys-rep"
