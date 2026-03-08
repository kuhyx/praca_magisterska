#!/bin/bash
# Build and run the C++ shortest-path visualizer (requires raylib)
set -e
cd "$(dirname "$0")"

if ! command -v pkg-config &>/dev/null || ! pkg-config --exists raylib; then
    echo "raylib not found. Install with: sudo pacman -S raylib"
    exit 1
fi

echo "Compiling..."
g++ -std=c++17 -O2 -o visualizer algorithms.cpp visualizer.cpp \
    $(pkg-config --cflags --libs raylib) -lm
echo "Running..."
./visualizer
