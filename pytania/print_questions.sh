#!/usr/bin/env bash
#
# print_questions.sh — Convert and print exam questions from OBRONA_MAGISTERSKA_ODPOWIEDZI.md
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
SOURCE_MD="${SCRIPT_DIR}/OBRONA_MAGISTERSKA_ODPOWIEDZI.md"
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

# ── Verify source file ───────────────────────────────────────────────────────
if [[ ! -f "$SOURCE_MD" ]]; then
    echo "Error: Source file not found: $SOURCE_MD" >&2
    exit 1
fi

# ── List questions ────────────────────────────────────────────────────────────
list_questions() {
    echo "Available questions in $(basename "$SOURCE_MD"):"
    echo ""
    grep "^## PYTANIE" "$SOURCE_MD" | while IFS= read -r line; do
        # Extract question number and title
        num=$(echo "$line" | sed 's/^## PYTANIE \([0-9/]*\):.*/\1/')
        title=$(echo "$line" | sed 's/^## PYTANIE [0-9/]*: //')
        printf "  %6s  %s\n" "$num" "$title"
    done
    echo ""
    echo "Total: $(grep -c "^## PYTANIE" "$SOURCE_MD") questions"
}

if $LIST_ONLY; then
    list_questions
    exit 0
fi

# ── Extract questions ─────────────────────────────────────────────────────────
extract_questions() {
    local md_file="$1"
    shift
    local selected=("$@")

    if [[ ${#selected[@]} -eq 0 ]]; then
        # All questions — output entire file
        cat "$md_file"
        return
    fi

    local tmpfile
    tmpfile=$(mktemp)
    local in_question=false
    local current_num=""
    local line_num=0

    # Build a grep pattern to find question headers with their line numbers
    # Then extract the relevant sections
    local question_starts=()
    local question_labels=()

    while IFS= read -r line; do
        ((line_num++)) || true
        if [[ "$line" =~ ^##\ PYTANIE\ ([0-9]+(/[0-9]+)?): ]]; then
            question_starts+=("$line_num")
            question_labels+=("${BASH_REMATCH[1]}")
        fi
    done < "$md_file"

    # Total lines in file
    local total_lines
    total_lines=$(wc -l < "$md_file")

    # For each selected question, find its start and end lines
    local first=true
    for sel in "${selected[@]}"; do
        for i in "${!question_labels[@]}"; do
            local label="${question_labels[$i]}"
            # Match: exact number, or either side of a slash (e.g., "13" matches "13/27")
            local match=false
            if [[ "$label" == "$sel" ]]; then
                match=true
            elif [[ "$label" == */* ]]; then
                local left="${label%%/*}"
                local right="${label##*/}"
                if [[ "$sel" == "$left" || "$sel" == "$right" ]]; then
                    match=true
                fi
            fi

            if $match; then
                local start="${question_starts[$i]}"
                local end="$total_lines"

                # End = next question start - 1, or EOF
                local next=$((i + 1))
                if [[ $next -lt ${#question_starts[@]} ]]; then
                    end=$(( ${question_starts[$next]} - 1 ))
                fi

                # Strip trailing blank lines and \newpage
                if ! $first; then
                    echo ""
                    echo "\\newpage"
                    echo ""
                fi
                first=false

                sed -n "${start},${end}p" "$md_file" | sed '/^\\newpage$/d' | sed -e :a -e '/^\s*$/{ $d; N; ba; }'
                break
            fi
        done
    done

    rm -f "$tmpfile"
}

# ── Generate output filename ─────────────────────────────────────────────────
if [[ -z "$OUTPUT_PDF" ]]; then
    if [[ ${#QUESTIONS[@]} -eq 0 ]]; then
        OUTPUT_PDF="/tmp/obrona_all_questions.pdf"
    elif [[ ${#QUESTIONS[@]} -eq 1 ]]; then
        OUTPUT_PDF="/tmp/obrona_q${QUESTIONS[0]}.pdf"
    else
        joined=$(IFS=_; echo "${QUESTIONS[*]}")
        OUTPUT_PDF="/tmp/obrona_q${joined}.pdf"
    fi
fi

# ── Create temporary markdown ────────────────────────────────────────────────
TMP_DIR=$(mktemp -d)
TMP_MD="${TMP_DIR}/questions.md"

extract_questions "$SOURCE_MD" "${QUESTIONS[@]}" > "$TMP_MD"

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
