#!/bin/bash
# Run the Python shortest-path visualizer (requires pygame)
set -e
cd "$(dirname "$0")"
python3 visualizer.py
