#!/bin/bash
# Auto-compile LaTeX thesis script
# Watches for changes and recompiles automatically

THESIS_DIR="/home/runner/work/praca_magisterska/praca_magisterska/latex"
MAIN_FILE="main.tex"
BUILD_DIR="build"

echo "========================================"
echo "LaTeX Thesis Auto-Compiler"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "$THESIS_DIR/$MAIN_FILE" ]; then
    echo "✗ Error: Cannot find $MAIN_FILE in $THESIS_DIR"
    echo "  Make sure you're running this from the repository root"
    exit 1
fi

cd "$THESIS_DIR" || exit 1

# Function to compile thesis
compile_thesis() {
    echo "[$(date +%H:%M:%S)] Compiling thesis..."
    
    # Create build directory if it doesn't exist
    mkdir -p "$BUILD_DIR"
    
    # Compile with pdflatex
    # First pass
    pdflatex -output-directory="$BUILD_DIR" -interaction=nonstopmode "$MAIN_FILE" > /dev/null 2>&1
    
    # Run biber for bibliography
    cd "$BUILD_DIR" && biber main > /dev/null 2>&1 && cd ..
    
    # Second pass (for references)
    pdflatex -output-directory="$BUILD_DIR" -interaction=nonstopmode "$MAIN_FILE" > /dev/null 2>&1
    
    # Third pass (to be sure)
    pdflatex -output-directory="$BUILD_DIR" -interaction=nonstopmode "$MAIN_FILE" > "$BUILD_DIR/last_compile.log" 2>&1
    
    # Check if compilation succeeded
    if [ -f "$BUILD_DIR/main.pdf" ]; then
        echo "✓ Compilation successful! PDF: $BUILD_DIR/main.pdf"
        
        # Show warnings and errors
        grep -i "warning" "$BUILD_DIR/last_compile.log" | head -5
        grep -i "error" "$BUILD_DIR/last_compile.log" | head -5
    else
        echo "✗ Compilation failed. Check $BUILD_DIR/last_compile.log for errors"
        tail -20 "$BUILD_DIR/last_compile.log"
    fi
    echo ""
}

# Check if inotify-tools is installed (for watch mode)
if command -v inotifywait >/dev/null 2>&1; then
    echo "Watch mode available. Options:"
    echo "1) Compile once and exit"
    echo "2) Compile and watch for changes (auto-recompile)"
    echo ""
    read -p "Select option (1 or 2): " OPTION
    
    if [ "$OPTION" = "2" ]; then
        echo "Starting watch mode..."
        echo "Monitoring .tex files in $THESIS_DIR for changes"
        echo "Press Ctrl+C to stop"
        echo ""
        
        # Initial compilation
        compile_thesis
        
        # Watch for changes
        while true; do
            inotifywait -q -e modify -r --include '.*\.tex$' .
            echo "[$(date +%H:%M:%S)] Change detected, recompiling..."
            compile_thesis
        done
    else
        compile_thesis
    fi
else
    echo "Note: Install inotify-tools for automatic recompilation on file changes"
    echo "  sudo apt-get install inotify-tools"
    echo ""
    compile_thesis
fi

echo "Done!"
