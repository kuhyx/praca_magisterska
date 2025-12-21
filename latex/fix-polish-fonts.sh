#!/bin/bash
# Fix Polish character support for WUT thesis template with XeTeX
# This script wraps the Python fix script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running Polish font fix..."
python3 "$SCRIPT_DIR/fix-polish-fonts.py"

echo ""
echo "Running full compilation..."
cd "$SCRIPT_DIR"
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex

echo ""
echo "=== Compilation Complete ==="
echo "Output: $SCRIPT_DIR/main.pdf"
