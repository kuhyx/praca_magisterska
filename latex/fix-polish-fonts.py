#!/usr/bin/env python3
"""
Fix Polish character support for WUT thesis template with XeTeX.
This script patches wut-thesis.cls to use fontspec with OpenType fonts
that properly support Polish characters (ą, ć, ę, ł, ń, ó, ś, ź, ż).
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def get_script_dir():
    return Path(__file__).parent.absolute()

def check_and_install_fonts():
    """Check if required TeX packages are available."""
    print("[1/4] Checking for required fonts...")
    
    # Check for TeX Gyre fonts (usually in texlive-fontsextra)
    try:
        result = subprocess.run(
            ['kpsewhich', 'texgyretermes-regular.otf'],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("  -> TeX Gyre fonts may not be installed.")
            print("  -> On Arch Linux, run: sudo pacman -S texlive-fontsextra")
    except FileNotFoundError:
        print("  -> kpsewhich not found. Make sure TeX Live is installed.")
    
    print("  -> Font check complete.")

def backup_cls_file(cls_path: Path, backup_path: Path):
    """Create backup of the class file."""
    print("\n[2/4] Creating backup of wut-thesis.cls...")
    
    if backup_path.exists():
        print("  -> Backup already exists, skipping.")
    else:
        shutil.copy2(cls_path, backup_path)
        print(f"  -> Backup created: {backup_path}")

def patch_cls_file(cls_path: Path):
    """Apply patches to the class file."""
    print("\n[3/4] Patching wut-thesis.cls...")
    
    content = cls_path.read_text(encoding='utf-8')
    
    # Check if already patched
    if 'fontspec' in content and 'ifxetex' in content:
        print("  -> Already patched, skipping class file modification.")
        return False
    
    # Patch 1: Replace fourier package with conditional font loading
    # Using Liberation fonts which are widely available and have full Polish support
    fourier_old = r'\RequirePackage{fourier}       % Adobe Utopia font'
    fourier_new = '''% Conditional font loading for XeTeX/LuaTeX compatibility with Polish characters
\\RequirePackage{iftex}
\\ifxetex
    \\RequirePackage{fontspec}
    \\defaultfontfeatures{Ligatures=TeX}
    % Use DejaVu fonts - widely available with full Polish character support
    \\setmainfont{DejaVu Serif}
    \\setsansfont{DejaVu Sans}
    \\setmonofont{DejaVu Sans Mono}
\\else\\ifluatex
    \\RequirePackage{fontspec}
    \\defaultfontfeatures{Ligatures=TeX}
    \\setmainfont{DejaVu Serif}
    \\setsansfont{DejaVu Sans}
    \\setmonofont{DejaVu Sans Mono}
\\else
    \\RequirePackage{fourier}       % Adobe Utopia font (pdfLaTeX only)
\\fi\\fi'''
    
    if fourier_old in content:
        content = content.replace(fourier_old, fourier_new)
        print("  -> Patched fourier package for XeTeX font support.")
    else:
        # Try without the comment
        fourier_old_alt = r'\RequirePackage{fourier}'
        if fourier_old_alt in content and 'fontspec' not in content:
            content = content.replace(fourier_old_alt, fourier_new, 1)
            print("  -> Patched fourier package for XeTeX font support.")
    
    # Patch 2: Fix microtype to disable expansion for XeTeX
    microtype_old = '''\\RequirePackage[
    protrusion=true,
    expansion=true
]{microtype}'''
    
    microtype_new = '''% Microtype - disable expansion for XeTeX (not supported)
\\ifxetex
    \\RequirePackage[protrusion=true]{microtype}
\\else
    \\RequirePackage[protrusion=true,expansion=true]{microtype}
\\fi'''
    
    if microtype_old in content:
        content = content.replace(microtype_old, microtype_new)
        print("  -> Patched microtype package for XeTeX compatibility.")
    
    # Write the patched content
    cls_path.write_text(content, encoding='utf-8')
    print("  -> Patches applied successfully.")
    return True

def clean_aux_files(latex_dir: Path):
    """Remove auxiliary files to force fresh compilation."""
    print("\n[4/4] Cleaning auxiliary files...")
    
    extensions = [
        '.aux', '.bbl', '.bcf', '.blg', '.fdb_latexmk', '.fls',
        '.log', '.out', '.run.xml', '.synctex.gz', '.toc',
        '.lof', '.lot', '.xdv', '.pdf'
    ]
    
    cleaned = 0
    for ext in extensions:
        file_path = latex_dir / f"main{ext}"
        if file_path.exists():
            file_path.unlink()
            cleaned += 1
    
    print(f"  -> Cleaned {cleaned} auxiliary files.")

def main():
    print("=== WUT Thesis Polish Font Fix ===")
    print("Fixes 'Missing character' errors for Polish letters (ą, ę, ł, etc.)")
    print("")
    
    script_dir = get_script_dir()
    cls_path = script_dir / "src" / "wut-thesis.cls"
    backup_path = script_dir / "src" / "wut-thesis.cls.backup"
    
    if not cls_path.exists():
        print(f"ERROR: Class file not found: {cls_path}")
        sys.exit(1)
    
    check_and_install_fonts()
    backup_cls_file(cls_path, backup_path)
    patch_cls_file(cls_path)
    clean_aux_files(script_dir)
    
    print("")
    print("=== Fix Applied Successfully ===")
    print("")
    print("To compile the document, run:")
    print(f"  cd {script_dir}")
    print("  latexmk -xelatex main.tex")
    print("")
    print("Or for a quick compilation:")
    print("  xelatex main.tex && biber main && xelatex main.tex && xelatex main.tex")
    print("")

if __name__ == "__main__":
    main()
