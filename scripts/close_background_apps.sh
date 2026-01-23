#!/bin/bash
# close_background_apps.sh
# Script to close unnecessary background applications before performance testing
# Author: Krzysztof Rudnicki
# Date: January 19, 2026

echo "=== Closing Background Applications for Performance Testing ==="
echo ""

# List of common background applications to close
# Add or remove applications as needed for your system
APPS_TO_CLOSE=(
    "firefox"
    "chromium"
    "chrome"
    "brave"
    # "code"         # VS Code - KEEP RUNNING (needed for development)
    "slack"
    "discord"
    "spotify"
    "telegram"
    "teams"
    "zoom"
    "dropbox"
    "syncthing"
    "steam"
    "lutris"
)

# Function to gracefully close an application
close_app() {
    local app_name="$1"
    if pgrep -x "$app_name" > /dev/null 2>&1; then
        echo "Closing $app_name..."
        pkill -TERM "$app_name" 2>/dev/null
        sleep 1
        # Force kill if still running
        if pgrep -x "$app_name" > /dev/null 2>&1; then
            pkill -KILL "$app_name" 2>/dev/null
        fi
    fi
}

# Close each application in the list
for app in "${APPS_TO_CLOSE[@]}"; do
    close_app "$app"
done

echo ""
echo "=== Background applications closed ==="
echo ""

# Show remaining resource-intensive processes
echo "Top 10 CPU-consuming processes:"
echo "--------------------------------"
ps aux --sort=-%cpu | head -11 | tail -10

echo ""
echo "Top 10 Memory-consuming processes:"
echo "----------------------------------"
ps aux --sort=-%mem | head -11 | tail -10

echo ""
echo "=== System ready for performance testing ==="
echo "Note: Verify no unwanted processes are still running before starting tests."
