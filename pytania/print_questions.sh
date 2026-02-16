#!/usr/bin/env bash
#
# print_questions.sh — Convert and print exam questions from questions/ folder
#
# Usage:
#   ./print_questions.sh [OPTIONS] [QUESTION_NUMBERS...]
#
# Examples:
#   ./print_questions.sh                  # Generate PDF of ALL questions
#   ./print_questions.sh 1                # Generate PDF of question 1
#   ./print_questions.sh 1 3 7            # Generate PDF of questions 1, 3, 7
#   ./print_questions.sh 1-5              # Generate PDF of questions 1 through 5
#   ./print_questions.sh 1 3-5 8          # Mix of individual and ranges
#   ./print_questions.sh --print 1 3      # Generate PDF AND print questions 1, 3
#   ./print_questions.sh --print          # Generate PDF AND print ALL questions
#   ./print_questions.sh --list           # List available questions
#
# Options:
#   --print, -p          Send to printer after generating PDF
#   --printer NAME       Printer name (default: Brother_HL-1110_series)
#   --list, -l           List available questions and exit
#   --output, -o FILE    Output PDF path (default: auto-generated in /tmp)
#   --keep, -k           Keep intermediate files (for debugging)
#   --help, -h           Show this help
#

set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUESTIONS_DIR="${SCRIPT_DIR}/questions"
PRINTER="Brother_HL-1110_series"
DO_PRINT=false
LIST_ONLY=false
KEEP_TMP=false
OUTPUT_PDF=""
QUESTIONS=()

# ── Parse arguments ───────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --print|-p)
            DO_PRINT=true
            shift
            ;;
        --printer)
            PRINTER="$2"
            shift 2
            ;;
        --list|-l)
            LIST_ONLY=true
            shift
            ;;
        --output|-o)
            OUTPUT_PDF="$2"
            shift 2
            ;;
        --keep|-k)
            KEEP_TMP=true
            shift
            ;;
        --help|-h)
            head -28 "$0" | tail -26
            exit 0
            ;;
        *)
            # Parse question numbers and ranges (e.g., "1", "3-5", "13/27")
            if [[ "$1" =~ ^[0-9]+(\/[0-9]+)?(-[0-9]+(\/[0-9]+)?)?$ ]]; then
                if [[ "$1" == *-* ]]; then
                    # Range: extract start-end
                    range_start="${1%%-*}"
                    range_end="${1##*-}"
                    for ((i=range_start; i<=range_end; i++)); do
                        QUESTIONS+=("$i")
                    done
                else
                    QUESTIONS+=("$1")
                fi
            else
                echo "Error: Unknown argument '$1'. Use --help for usage." >&2
                exit 1
            fi
            shift
            ;;
    esac
done

# ── Verify questions directory ────────────────────────────────────────────────
if [[ ! -d "$QUESTIONS_DIR" ]]; then
    echo "Error: Questions directory not found: $QUESTIONS_DIR" >&2
    echo "Run split_questions.py first to generate per-question files." >&2
    exit 1
fi

# ── Helper: find question file by number ──────────────────────────────────────
# Matches question number against filenames like pytanie_01.md, pytanie_13_27.md
find_question_file() {
    local num="$1"
    local padded
    padded=$(printf "%02d" "$num")

    # Try exact match: pytanie_NN.md
    local exact="${QUESTIONS_DIR}/pytanie_${padded}.md"
    if [[ -f "$exact" ]]; then
        echo "$exact"
        return 0
    fi

    # Try dual-numbered: pytanie_NN_MM.md (match either side)
    for f in "${QUESTIONS_DIR}"/pytanie_*_*.md; do
        [[ -f "$f" ]] || continue
        local base
        base=$(basename "$f" .md)
        # Extract numbers from pytanie_NN_MM
        local nums="${base#pytanie_}"
        local left="${nums%%_*}"
        local right="${nums##*_}"
        if [[ "$padded" == "$left" || "$padded" == "$right" ]]; then
            echo "$f"
            return 0
        fi
    done

    return 1
}

# ── List questions ────────────────────────────────────────────────────────────
list_questions() {
    echo "Available questions in ${QUESTIONS_DIR}/"
    echo ""
    for f in "${QUESTIONS_DIR}"/pytanie_*.md; do
        [[ -f "$f" ]] || continue
        # Read first line to get the header
        local header
        header=$(head -1 "$f")
        local num title
        num=$(echo "$header" | sed 's/^## PYTANIE \([0-9/]*\):.*/\1/')
        title=$(echo "$header" | sed 's/^## PYTANIE [0-9/]*: //')
        printf "  %6s  %s\n" "$num" "$title"
    done
    echo ""
    echo "Total: $(ls -1 "${QUESTIONS_DIR}"/pytanie_*.md 2>/dev/null | wc -l) questions"
}

if $LIST_ONLY; then
    list_questions
    exit 0
fi

# ── Assemble selected questions ───────────────────────────────────────────────
assemble_questions() {
    local selected=("$@")

    if [[ ${#selected[@]} -eq 0 ]]; then
        # All questions — concatenate all files in order
        local first=true
        for f in "${QUESTIONS_DIR}"/pytanie_*.md; do
            [[ -f "$f" ]] || continue
            if ! $first; then
                echo ""
                echo "\\newpage"
                echo ""
            fi
            first=false
            cat "$f"
        done
        return
    fi

    # Selected questions
    local first=true
    local found_any=false
    for sel in "${selected[@]}"; do
        local qfile
        if qfile=$(find_question_file "$sel"); then
            found_any=true
            if ! $first; then
                echo ""
                echo "\\newpage"
                echo ""
            fi
            first=false
            cat "$qfile"
        else
            echo "Warning: Question $sel not found, skipping." >&2
        fi
    done

    if ! $found_any; then
        return 1
    fi
}

# ── Generate output filename ─────────────────────────────────────────────────
if [[ -z "$OUTPUT_PDF" ]]; then
    if [[ ${#QUESTIONS[@]} -eq 0 ]]; then
        OUTPUT_PDF="/tmp/obrona_all_questions.pdf"
    elif [[ ${#QUESTIONS[@]} -eq 1 ]]; then
        OUTPUT_PDF="/tmp/obrona_q${QUESTIONS[0]}.pdf"
    else
        joined=$(IFS=_; echo "${QUESTIONS[*]}")
        joined="${joined//\//-}"  # Replace / with - for safe filenames
        OUTPUT_PDF="/tmp/obrona_q${joined}.pdf"
    fi
fi

# ── Create temporary markdown ────────────────────────────────────────────────
TMP_DIR=$(mktemp -d)
TMP_MD="${TMP_DIR}/questions.md"

if ! assemble_questions "${QUESTIONS[@]}" > "$TMP_MD"; then
    echo "Error: No matching questions found for: ${QUESTIONS[*]}" >&2
    echo "Use --list to see available questions." >&2
    rm -rf "$TMP_DIR"
    exit 1
fi

# Count extracted questions
extracted=$(grep -c "^## PYTANIE" "$TMP_MD" || echo "0")
if [[ "$extracted" -eq 0 ]]; then
    echo "Error: No matching questions found for: ${QUESTIONS[*]}" >&2
    echo "Use --list to see available questions." >&2
    rm -rf "$TMP_DIR"
    exit 1
fi

# ── Convert to PDF via pandoc + xelatex ───────────────────────────────────────
echo "Converting $extracted question(s) to PDF..."

pandoc "$TMP_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=xelatex \
    --resource-path="${SCRIPT_DIR}" \
    -V geometry:a4paper \
    -V geometry:margin=1.8cm \
    -V fontsize=12pt \
    -V mainfont="DejaVu Sans" \
    -V sansfont="DejaVu Sans" \
    -V monofont="DejaVu Sans Mono" \
    -V linestretch=1.15 \
    -V colorlinks=false \
    --highlight-style=monochrome \
    -V header-includes='\usepackage{fancyhdr}\pagestyle{fancy}\fancyhead[L]{\small Obrona magisterska}\fancyhead[R]{\small\thepage}\fancyfoot{}' \
    -V header-includes='\usepackage{enumitem}\setlist{nosep,leftmargin=*}' \
    -V header-includes='\renewcommand{\arraystretch}{1.3}' \
    -V header-includes='\usepackage{booktabs}' \
    2>/dev/null

echo "PDF generated: $OUTPUT_PDF"
echo "  Pages: $(pdfinfo "$OUTPUT_PDF" 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")"

# ── Print ─────────────────────────────────────────────────────────────────────
if $DO_PRINT; then
    if ! lpstat -p "$PRINTER" &>/dev/null; then
        echo "Error: Printer '$PRINTER' not found." >&2
        echo "Available printers:" >&2
        lpstat -p 2>/dev/null | awk '{print "  " $2}' >&2
        rm -rf "$TMP_DIR"
        exit 1
    fi

    echo "Printing to $PRINTER..."
    lp -d "$PRINTER" \
       -o media=A4 \
       -o sides=one-sided \
       -o fit-to-page \
       "$OUTPUT_PDF"
    echo "Print job submitted."
fi

# ── Cleanup ───────────────────────────────────────────────────────────────────
if $KEEP_TMP; then
    echo "Temporary files kept in: $TMP_DIR"
else
    rm -rf "$TMP_DIR"
fi
