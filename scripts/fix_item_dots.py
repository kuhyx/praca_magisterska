#!/usr/bin/env python3
"""Add missing periods at the end of \\item entries in LaTeX files."""
import re
import os


def process_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    modified = False
    in_lstlisting = False

    for i in range(len(lines)):
        line = lines[i]

        # Track lstlisting/verbatim environments
        if re.search(r'\\begin\{(lstlisting|verbatim)\}', line):
            in_lstlisting = True
        if re.search(r'\\end\{(lstlisting|verbatim)\}', line):
            in_lstlisting = False
            continue
        if in_lstlisting:
            continue

        # Check if this line is a boundary (start of next item or end of list)
        is_boundary = (
            bool(re.match(r'\s*\\item\b', line)) or
            bool(re.match(r'\s*\\end\{(itemize|enumerate|description)\}', line.strip()))
        )

        if not is_boundary:
            continue

        # Find the previous non-empty line
        j = i - 1
        while j >= 0 and lines[j].strip() == '':
            j -= 1

        if j < 0:
            continue

        prev_stripped = lines[j].strip()

        if not prev_stripped:
            continue

        # Skip structural/non-content lines
        skip_patterns = [
            r'^\\begin\{',
            r'^\\end\{',
            r'^\\hline',
            r'^\\label',
            r'^%',
            r'^\\centering',
            r'^\\caption',
            r'^\\\\$',       # bare line break
            r'^\\clearpage',
            r'^\\newpage',
            r'^\\raggedbottom',
            r'^\\small$',
            r'^\\footnotesize$',
            r'^\\endgroup',
            r'^\\begingroup',
        ]
        if any(re.match(p, prev_stripped) for p in skip_patterns):
            continue

        last_char = prev_stripped[-1]

        if last_char not in '.?!':
            lines[j] = lines[j].rstrip() + '.\n'
            modified = True
            display = prev_stripped[-70:] if len(prev_stripped) > 70 else prev_stripped
            print(f"  L{j+1}: {display} -> +dot")

    if modified:
        with open(filepath, 'w') as f:
            f.writelines(lines)
        return True
    return False


tex_dir = '/home/kuhy/praca_magisterska/latex/tex'
files = [
    '1-wstep.tex',
    '2-przeglad-literatury.tex',
    '3-silniki-gier.tex',
    '4-metodologia.tex',
    '5-testy-wydajnosci.tex',
    '6-analiza-mozliwosci.tex',
    '7-porownanie-wynikow.tex',
    '8-podsumowanie.tex',
    'narzedzia-profilowania.tex',
    'implementacja-gry.tex',
    'wywiady-analiza.tex',
]

changes = 0
for f in files:
    path = os.path.join(tex_dir, f)
    print(f"\n=== {f} ===")
    if process_file(path):
        changes += 1
    else:
        print("  No changes needed")

print(f"\n\nModified {changes} files")
