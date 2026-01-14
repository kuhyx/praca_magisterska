#!/bin/bash
# Helper script to guide through Unity game testing with Nsight

echo "======================================"
echo "Unity Game + Nsight Testing Guide"
echo "======================================"
echo ""

# Check if Nsight is installed
if ! command -v nv-nsight-gfx &> /dev/null; then
    echo "⚠️  NVIDIA Nsight Graphics not found in PATH"
    echo ""
    echo "To install:"
    echo "1. Download from: https://developer.nvidia.com/nsight-graphics"
    echo "2. Run the installer"
    echo "3. Add to PATH or note installation directory"
    echo ""
    exit 1
fi

echo "✓ NVIDIA Nsight Graphics found"
echo ""

# Get scenario from user
echo "Select test scenario:"
echo "1) Low difficulty (50-100 bullets)"
echo "2) Medium difficulty (200-300 bullets)"
echo "3) High difficulty (500+ bullets)"
read -p "Enter scenario number (1-3): " SCENARIO_NUM

case $SCENARIO_NUM in
    1)
        SCENARIO="low"
        SCENARIO_NAME="Low Difficulty"
        ;;
    2)
        SCENARIO="medium"
        SCENARIO_NAME="Medium Difficulty"
        ;;
    3)
        SCENARIO="high"
        SCENARIO_NAME="High Difficulty"
        ;;
    *)
        echo "Invalid scenario number"
        exit 1
        ;;
esac

echo ""
echo "Testing scenario: $SCENARIO_NAME"
echo ""

# Pre-test checklist
echo "Pre-test checklist:"
echo "- [ ] Close all background applications"
echo "- [ ] Disable system updates"
echo "- [ ] Set power mode to High Performance"
echo "- [ ] Wait 5 minutes for system stabilization"
echo ""
read -p "Press Enter when ready to continue..."

echo ""
echo "Step 1: Launch Unity Game"
echo "------------------------"
echo "Navigate to the Unity bullet-hell game and launch it."
echo "Select the '$SCENARIO_NAME' mode from the menu."
echo ""
read -p "Press Enter when Unity game is running..."

echo ""
echo "Step 2: Launch NVIDIA Nsight Graphics"
echo "------------------------------------"
echo "1. Open NVIDIA Nsight Graphics application"
echo "2. Click 'Connect' or 'Attach to Process'"
echo "3. Find the Unity process (usually 'Unity.exe' or similar)"
echo "4. Click 'Attach'"
echo ""
read -p "Press Enter when Nsight is attached..."

echo ""
echo "Step 3: Start gameplay and capture frames"
echo "----------------------------------------"
echo "You will capture 5 frames at these time points:"
echo "  - 5 seconds into gameplay"
echo "  - 10 seconds into gameplay"
echo "  - 15 seconds into gameplay"
echo "  - 20 seconds into gameplay"
echo "  - 25 seconds into gameplay"
echo ""
echo "For each capture:"
echo "1. In Nsight, press F11 (or click 'Capture Frame')"
echo "2. Save the capture with naming: unity_${SCENARIO}_capture_1.nsight"
echo "   (increment number for each capture)"
echo ""
read -p "Press Enter to start timer..."

# Timer for captures
for i in {1..5}; do
    TIME=$((i * 5))
    echo ""
    echo "Waiting for ${TIME} seconds..."
    sleep 5
    echo ">>> CAPTURE #${i} NOW! (Time: ${TIME}s) <<<"
    echo "Press F11 in Nsight to capture"
    echo "Save as: unity_${SCENARIO}_capture_${i}.nsight"
    read -p "Press Enter when capture is saved..."
done

echo ""
echo "Step 4: Export metrics"
echo "---------------------"
echo "In Nsight, for each capture:"
echo "1. Open the capture file"
echo "2. Go to GPU Trace or Performance view"
echo "3. Export metrics to CSV"
echo "4. Save as: unity_${SCENARIO}_capture_${i}_metrics.csv"
echo ""
read -p "Press Enter when exports are complete..."

echo ""
echo "Step 5: Take screenshots"
echo "-----------------------"
echo "Capture screenshots of:"
echo "- GPU Timeline view"
echo "- Memory analysis view"
echo "- Any interesting performance bottlenecks"
echo ""
echo "Save screenshots to: screenshots/unity/${SCENARIO}/"
echo ""
read -p "Press Enter when screenshots are saved..."

echo ""
echo "✓ Testing complete for Unity - $SCENARIO_NAME"
echo ""
echo "Captured files:"
echo "  - unity_${SCENARIO}_capture_1.nsight through unity_${SCENARIO}_capture_5.nsight"
echo "  - unity_${SCENARIO}_capture_*_metrics.csv"
echo "  - screenshots/unity/${SCENARIO}/*.png"
echo ""
echo "Next steps:"
echo "1. Close Unity game"
echo "2. Wait 2 minutes for system cooldown"
echo "3. Run this script again or run: ./run_unreal_test.sh"
echo "   to test the same scenario in Unreal Engine"
echo ""
