#!/usr/bin/env python3
"""
Split OBRONA_MAGISTERSKA_ODPOWIEDZI.md into per-question files.
Each file: pytanie_NN.md (or pytanie_NN_MM.md for dual-numbered like 13/27).
Placed in pytania/questions/ folder.
"""
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(SCRIPT_DIR, 'OBRONA_MAGISTERSKA_ODPOWIEDZI.md')
OUT_DIR = os.path.join(SCRIPT_DIR, 'questions')
os.makedirs(OUT_DIR, exist_ok=True)

with open(SOURCE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all question boundaries
question_starts = []
for i, line in enumerate(lines):
    m = re.match(r'^## PYTANIE (\d+(/\d+)?):(.*)$', line)
    if m:
        raw_num = m.group(1)  # e.g. "13/27" or "1"
        title = m.group(3).strip()
        question_starts.append((i, raw_num, title))

print(f"Found {len(question_starts)} questions")

for idx, (start_line, raw_num, title) in enumerate(question_starts):
    # End = next question start or EOF
    if idx + 1 < len(question_starts):
        end_line = question_starts[idx + 1][0]
    else:
        end_line = len(lines)

    # Extract content, strip trailing \newpage and blank lines
    content_lines = lines[start_line:end_line]
    # Remove trailing \newpage and blank lines
    while content_lines and content_lines[-1].strip() in ('', '\\newpage'):
        content_lines.pop()
    # Add final newline
    content_lines.append('\n')

    # Build filename: pytanie_01.md, pytanie_13_27.md
    safe_num = raw_num.replace('/', '_')
    # Zero-pad single numbers for sorting
    parts = safe_num.split('_')
    padded = '_'.join(p.zfill(2) for p in parts)
    filename = f'pytanie_{padded}.md'

    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(content_lines)

    line_count = len(content_lines)
    print(f"  {filename:30s}  ({line_count:4d} lines)  PYTANIE {raw_num}: {title}")

print(f"\nAll files written to: {OUT_DIR}")
