#!/usr/bin/env python3
"""
Anki Generator - Modular approach with 3 combinable strategies.

Usage:
    python anki_generator.py [options]

Options:
    --filter      Apply strict filtering (answers > 100 chars)
    --extract     Use improved extraction algorithm
    --main-only   Only generate main exam questions (45 comprehensive cards)

Combinations:
    python anki_generator.py                           # Basic extraction, no filter
    python anki_generator.py --filter                  # Approach 1: Strict filter only
    python anki_generator.py --extract                 # Approach 2: Better extraction only  
    python anki_generator.py --main-only               # Approach 3: Main questions only
    python anki_generator.py --filter --extract        # Approach 4: Filter + Better extraction
    python anki_generator.py --filter --main-only      # Approach 5: Filter + Main only
    python anki_generator.py --extract --main-only     # Approach 6: Better extraction + Main only
    python anki_generator.py --filter --extract --main-only  # Approach 7: All three
"""

import os
import re
import argparse
from pathlib import Path

# =============================================================================
# SHARED UTILITIES
# =============================================================================

def clean_text(text):
    """Clean and format text for Anki."""
    if not text:
        return ""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    text = text.replace('\t', ' ')
    text = text.replace('"', '&quot;')
    text = re.sub(r' +', ' ', text)
    return text.strip()

def get_file_metadata(filepath):
    """Extract question number and subject from filename."""
    filename = os.path.basename(filepath)
    match = re.match(r'(\d+)-(.+)\.md', filename)
    num = match.group(1) if match else "00"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    subj_match = re.search(r'Przedmiot:\s*(\w+)', content)
    subject = subj_match.group(1) if subj_match else "Ogólne"
    
    return num, subject, content

def get_main_question(content):
    """Extract the main exam question."""
    q_match = re.search(r'## Pytanie\s*\n\s*\*\*["\']?(.+?)["\']?\*\*', content, re.DOTALL)
    if q_match:
        return re.sub(r'\s+', ' ', q_match.group(1).strip())
    return None

# =============================================================================
# APPROACH 1: STRICT FILTERING
# =============================================================================

def apply_strict_filter(cards, min_length=100):
    """Filter cards to only include those with answers > min_length characters."""
    return [c for c in cards if len(c['back']) > min_length]

# =============================================================================
# APPROACH 2: BETTER EXTRACTION
# =============================================================================

def extract_structured_content(body):
    """Improved extraction - multiple content types with better formatting."""
    parts = []
    
    # 1. Definitions
    def_match = re.search(r'#### Definicja[^\n]*\n([^\n#]+)', body)
    if def_match:
        parts.append(f"<b>Definicja:</b> {def_match.group(1).strip()}")
    
    # 2. Bullet points with bold terms
    bullets = re.findall(r'[-•]\s*\*\*([^*]+)\*\*[:\s-]*([^\n]*)', body)
    for term, desc in bullets[:5]:
        if desc.strip():
            parts.append(f"• <b>{term}</b>: {desc.strip()}")
        else:
            parts.append(f"• <b>{term}</b>")
    
    # 3. Key-value patterns
    if len(parts) < 2:
        kvs = re.findall(r'\*\*([^*\n]+)\*\*\s*[-–:]\s*([^\n*]{10,150})', body)
        for k, v in kvs[:4]:
            entry = f"<b>{k.strip()}</b>: {v.strip()}"
            if entry not in parts:
                parts.append(entry)
    
    # 4. Paragraphs as fallback
    if not parts:
        paras = [p.strip() for p in body.split('\n\n') 
                if p.strip() and not p.startswith('```') and not p.startswith('|') and len(p.strip()) > 30]
        for p in paras[:2]:
            parts.append(p[:300])
    
    return '<br>'.join([clean_text(p) for p in parts]) if parts else None

def extract_cards_better(filepath):
    """Extract cards with improved algorithm."""
    num, subject, content = get_file_metadata(filepath)
    base_tags = f"egzamin pyt{num} {subject}"
    cards = []
    
    # Main question
    main_q = get_main_question(content)
    if main_q:
        answer_match = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## [^�]|\Z)', content, re.DOTALL)
        if answer_match:
            answer = extract_structured_content(answer_match.group(1))
            if answer:
                cards.append({'front': clean_text(main_q), 'back': answer, 'tags': f"{base_tags} main"})
    
    # Detail sections
    sections = re.findall(r'^### (?:\d+\.\s*)?([^\n]+)\n((?:(?!^### ).)*)', content, re.MULTILINE | re.DOTALL)
    for header, body in sections:
        header = header.strip()
        if 'Przykład' in header or '"' in header or 'Mnemonic' in header or len(body) < 50:
            continue
        
        answer = extract_structured_content(body)
        if answer:
            cards.append({'front': f"Wyjaśnij: {clean_text(header)}", 'back': answer, 'tags': f"{base_tags} detail"})
    
    return cards

def extract_cards_basic(filepath):
    """Basic extraction - simpler algorithm."""
    num, subject, content = get_file_metadata(filepath)
    base_tags = f"egzamin pyt{num} {subject}"
    cards = []
    
    # Main question - just headers
    main_q = get_main_question(content)
    if main_q:
        answer_match = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
        if answer_match:
            headers = re.findall(r'^### (?:\d+\.\s*)?(.+)$', answer_match.group(1), re.MULTILINE)
            if headers:
                answer = '<ul>' + ''.join([f'<li>{clean_text(h)}</li>' for h in headers[:6]]) + '</ul>'
                cards.append({'front': clean_text(main_q), 'back': answer, 'tags': f"{base_tags} main"})
    
    # Detail sections - first paragraph only
    sections = re.findall(r'^### (?:\d+\.\s*)?([^\n]+)\n((?:(?!^### ).)*)', content, re.MULTILINE | re.DOTALL)
    for header, body in sections:
        header = header.strip()
        body = body.strip()
        if len(body) < 50 or 'Przykład' in header:
            continue
        
        paras = [p.strip() for p in body.split('\n\n') if p.strip() and not p.startswith('```')]
        if paras:
            answer = clean_text(paras[0][:400])
            cards.append({'front': f"Wyjaśnij: {clean_text(header)}", 'back': answer, 'tags': f"{base_tags} detail"})
    
    return cards

# =============================================================================
# APPROACH 3: MAIN QUESTIONS ONLY
# =============================================================================

def extract_main_only(filepath):
    """Extract only the main exam question with comprehensive answer."""
    num, subject, content = get_file_metadata(filepath)
    base_tags = f"egzamin pyt{num} {subject} main"
    
    main_q = get_main_question(content)
    if not main_q:
        return []
    
    # Build comprehensive answer from multiple sections
    answer_parts = []
    
    # Get main answer section
    answer_match = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## [^�]|\Z)', content, re.DOTALL)
    if answer_match:
        section = answer_match.group(1)
        
        # Get all ### headers with their first substantive content
        headers = re.findall(r'^### (?:\d+\.\s*)?([^\n]+)\n((?:(?!^### ).)*)', section, re.MULTILINE | re.DOTALL)
        
        for header, body in headers[:5]:
            header = header.strip()
            if 'Przykład' in header or 'Mnemonic' in header or '"' in header:
                continue
            
            # Get key point from this section
            key_point = None
            
            # Try to get a definition or first bullet
            def_match = re.search(r'Rozpoznawana klasa języków\s*\n\s*\*\*([^*]+)\*\*', body)
            if def_match:
                key_point = def_match.group(1).strip()
            
            if not key_point:
                bullets = re.findall(r'[-•]\s*\*\*([^*]+)\*\*[:\s-]*([^\n]*)', body)
                if bullets:
                    term, desc = bullets[0]
                    key_point = f"{term}: {desc.strip()}" if desc.strip() else term
            
            if not key_point:
                para_match = re.search(r'\n\n([^#\n\-•|`][^\n]{20,150})', body)
                if para_match:
                    key_point = para_match.group(1).strip()
            
            if key_point:
                answer_parts.append(f"<b>{header}</b>: {key_point}")
    
    if answer_parts:
        answer = '<br><br>'.join([clean_text(p) for p in answer_parts])
        return [{'front': clean_text(main_q), 'back': answer, 'tags': base_tags}]
    
    return []

# =============================================================================
# MAIN GENERATOR
# =============================================================================

def generate_anki(use_filter=False, use_better_extract=False, main_only=False):
    """Generate Anki deck with specified approaches."""
    odpowiedzi_dir = Path("/home/kuchy/praca_magisterska/pytania/odpowiedzi")
    
    # Determine output filename based on options
    suffix_parts = []
    if use_filter:
        suffix_parts.append("filter")
    if use_better_extract:
        suffix_parts.append("extract")
    if main_only:
        suffix_parts.append("main")
    suffix = "_".join(suffix_parts) if suffix_parts else "basic"
    
    output_file = Path(f"/home/kuchy/praca_magisterska/pytania/anki_{suffix}.txt")
    deck_name = f"Egzamin_{suffix.replace('_', '+')}"
    
    all_cards = []
    
    for md_file in sorted(odpowiedzi_dir.glob("*.md")):
        if main_only:
            # Approach 3: Only main questions
            cards = extract_main_only(md_file)
        elif use_better_extract:
            # Approach 2: Better extraction
            cards = extract_cards_better(md_file)
        else:
            # Basic extraction
            cards = extract_cards_basic(md_file)
        
        all_cards.extend(cards)
    
    # Approach 1: Apply filtering if requested
    if use_filter:
        all_cards = apply_strict_filter(all_cards, min_length=100)
    
    # Remove duplicates
    seen = set()
    unique = []
    for c in all_cards:
        key = c['front'][:80]
        if key not in seen:
            seen.add(key)
            unique.append(c)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"#separator:Tab\n#html:true\n#notetype:Basic\n#deck:{deck_name}\n\n")
        for c in unique:
            f.write(f"{c['front']}\t{c['back']}\t{c['tags']}\n")
    
    # Statistics
    lengths = [len(c['back']) for c in unique]
    short = sum(1 for l in lengths if l < 50)
    medium = sum(1 for l in lengths if 50 <= l < 150)
    good = sum(1 for l in lengths if l >= 150)
    
    print(f"✅ Generated: {output_file.name}")
    print(f"   Cards: {len(unique)}")
    print(f"   Quality: {short} short / {medium} medium / {good} good")
    print()
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Generate Anki flashcards with modular approaches")
    parser.add_argument('--filter', action='store_true', help='Approach 1: Strict filtering (>100 chars)')
    parser.add_argument('--extract', action='store_true', help='Approach 2: Better extraction algorithm')
    parser.add_argument('--main-only', action='store_true', help='Approach 3: Main exam questions only')
    parser.add_argument('--all-combinations', action='store_true', help='Generate all 7 combinations')
    
    args = parser.parse_args()
    
    if args.all_combinations:
        # Generate all 7 combinations
        print("=" * 60)
        print("Generating all 7 combinations...")
        print("=" * 60 + "\n")
        
        combinations = [
            (True, False, False),   # 1: Filter only
            (False, True, False),   # 2: Extract only
            (False, False, True),   # 3: Main only
            (True, True, False),    # 4: Filter + Extract
            (True, False, True),    # 5: Filter + Main
            (False, True, True),    # 6: Extract + Main
            (True, True, True),     # 7: All three
        ]
        
        for i, (f, e, m) in enumerate(combinations, 1):
            print(f"--- Combination {i} (filter={f}, extract={e}, main={m}) ---")
            generate_anki(use_filter=f, use_better_extract=e, main_only=m)
    else:
        generate_anki(
            use_filter=args.filter,
            use_better_extract=args.extract,
            main_only=args.main_only
        )

if __name__ == "__main__":
    main()
