#!/bin/bash
# Markdown Linter and Formatter Script
# Usage: ./lint-markdown.sh [--fix]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIX_MODE=false

# Parse arguments
if [[ "$1" == "--fix" ]]; then
    FIX_MODE=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "Markdown Linter and Formatter"
echo "========================================="

# Check for required tools
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${YELLOW}Warning: $1 not found. Installing...${NC}"
        return 1
    fi
    return 0
}

# Install markdownlint-cli if not present
if ! check_tool "markdownlint"; then
    echo "Installing markdownlint-cli..."
    npm install -g markdownlint-cli
fi

# Install prettier if not present
if ! check_tool "prettier"; then
    echo "Installing prettier..."
    npm install -g prettier
fi

# Create markdownlint config if it doesn't exist
CONFIG_FILE="$SCRIPT_DIR/.markdownlint.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Creating markdownlint configuration..."
    cat > "$CONFIG_FILE" << 'EOF'
{
  "default": true,
  "MD013": {
    "line_length": 300,
    "code_blocks": false,
    "tables": false
  },
  "MD024": {
    "siblings_only": true
  },
  "MD033": {
    "allowed_elements": ["br", "details", "summary", "kbd"]
  },
  "MD041": false,
  "MD036": false,
  "MD040": false,
  "MD046": false
}
EOF
fi

# Create prettier config if it doesn't exist
PRETTIER_CONFIG="$SCRIPT_DIR/.prettierrc"
if [[ ! -f "$PRETTIER_CONFIG" ]]; then
    echo "Creating prettier configuration..."
    cat > "$PRETTIER_CONFIG" << 'EOF'
{
  "proseWrap": "preserve",
  "tabWidth": 2,
  "useTabs": false,
  "printWidth": 300
}
EOF
fi

echo ""
echo "========================================="
echo "Running Linters on Markdown Files"
echo "========================================="

# Find all markdown files
MD_FILES=$(find "$SCRIPT_DIR" -maxdepth 1 -name "*.md" -type f | sort)

TOTAL_ISSUES=0

if [[ "$FIX_MODE" == true ]]; then
    echo -e "${GREEN}Running in FIX mode - will auto-fix issues${NC}"
    echo ""
    
    # Run prettier to format
    echo "Step 1: Running Prettier (formatting)..."
    for file in $MD_FILES; do
        echo "  Formatting: $(basename "$file")"
        prettier --write "$file" 2>/dev/null || true
    done
    
    echo ""
    echo "Step 2: Running markdownlint with --fix..."
    for file in $MD_FILES; do
        echo "  Linting: $(basename "$file")"
        markdownlint --fix --config "$CONFIG_FILE" "$file" 2>&1 || true
    done
    
    echo ""
    echo "Step 3: Final check for remaining issues..."
    for file in $MD_FILES; do
        OUTPUT=$(markdownlint --config "$CONFIG_FILE" "$file" 2>&1 || true)
        if [[ -n "$OUTPUT" ]]; then
            echo -e "${YELLOW}$(basename "$file"):${NC}"
            echo "$OUTPUT"
            TOTAL_ISSUES=$((TOTAL_ISSUES + $(echo "$OUTPUT" | wc -l)))
        fi
    done
else
    echo -e "${YELLOW}Running in CHECK mode - use --fix to auto-fix${NC}"
    echo ""
    
    for file in $MD_FILES; do
        echo "Checking: $(basename "$file")"
        OUTPUT=$(markdownlint --config "$CONFIG_FILE" "$file" 2>&1 || true)
        if [[ -n "$OUTPUT" ]]; then
            echo -e "${RED}Issues found:${NC}"
            echo "$OUTPUT"
            TOTAL_ISSUES=$((TOTAL_ISSUES + $(echo "$OUTPUT" | wc -l)))
        else
            echo -e "${GREEN}  ✓ No issues${NC}"
        fi
        echo ""
    done
fi

echo ""
echo "========================================="
echo "Summary"
echo "========================================="

if [[ $TOTAL_ISSUES -eq 0 ]]; then
    echo -e "${GREEN}✓ All markdown files are clean!${NC}"
else
    echo -e "${YELLOW}Found $TOTAL_ISSUES remaining issue(s)${NC}"
    echo "Some issues may require manual fixing."
fi

echo ""
echo "Done!"
