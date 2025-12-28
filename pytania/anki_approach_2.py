#!/usr/bin/env python3
"""
Approach 2: BETTER EXTRACTION ONLY
- Improved algorithm to get more complete content
- No minimum length filtering
"""

import os
import re
from pathlib import Path

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    text = text.replace('\t', ' ')
    text = text.replace('"', '&quot;')
    text = re.sub(r' +', ' ', text)
    return text.strip()

def extract_structured_content(body):
    """Better extraction - look for multiple content types."""
    parts = []
    
    # 1. Look for definitions
    def_match = re.search(r'#### Definicja[^\n]*\n([^\n#]+)', body)
    if def_match:
        parts.append(f"<b>Definicja:</b> {def_match.group(1).strip()}")
    
    # 2. Look for bullet points with bold terms
    bullets = re.findall(r'[-•]\s*\*\*([^*]+)\*\*[:\s-]*([^\n]*)', body)
    for term, desc in bullets[:5]:
        if desc.strip():
            parts.append(f"• <b>{term}</b>: {desc.strip()}")
        else:
            parts.append(f"• <b>{term}</b>")
    
    # 3. Look for key-value patterns
    if not parts:
        kvs = re.findall(r'\*\*([^*]+)\*\*\s*[-:]\s*([^\n*]+)', body)
        for k, v in kvs[:4]:
            parts.append(f"<b>{k}</b>: {v.strip()}")
    
    # 4. Get paragraphs as fallback
    if not parts:
        paras = [p.strip() for p in body.split('\n\n') 
                if p.strip() and not p.startswith('```') and not p.startswith('|') and len(p.strip()) > 30]
        for p in paras[:2]:
            parts.append(p[:300])
    
    return '<br>'.join([clean_text(p) for p in parts]) if parts else None

def extract_cards(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = []
    filename = os.path.basename(filepath)
    match = re.match(r'(\d+)-(.+)\.md', filename)
    num = match.group(1) if match else "00"
    
    subj_match = re.search(r'Przedmiot:\s*(\w+)', content)
    subject = subj_match.group(1) if subj_match else "Ogólne"
    base_tags = f"egzamin pyt{num} {subject}"
    
    # Main question with better extraction
    q_match = re.search(r'## Pytanie\s*\n\s*\*\*["\']?(.+?)["\']?\*\*', content, re.DOTALL)
    if q_match:
        main_q = re.sub(r'\s+', ' ', q_match.group(1).strip())
        
        answer_match = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
        if answer_match:
            answer = extract_structured_content(answer_match.group(1))
            if answer:
                cards.append({'front': clean_text(main_q), 'back': answer, 'tags': base_tags})
    
    # Detail cards with better extraction
    sections = re.findall(r'^### (?:\d+\.\s*)?([^\n]+)\n((?:(?!^### ).)*)', content, re.MULTILINE | re.DOTALL)
    for header, body in sections:
        header = header.strip()
        if 'Przykład' in header or '"' in header or len(body) < 50:
            continue
        
        answer = extract_structured_content(body)
        if answer:
            cards.append({'front': f"Wyjaśnij: {clean_text(header)}", 'back': answer, 'tags': base_tags})
    
    return cards

def main():
    odpowiedzi_dir = Path("/home/kuchy/praca_magisterska/pytania/odpowiedzi")
    output_file = Path("/home/kuchy/praca_magisterska/pytania/anki_2_better_extract.txt")
    
    all_cards = []
    for md_file in sorted(odpowiedzi_dir.glob("*.md")):
        all_cards.extend(extract_cards(md_file))
    
    # No filtering - just dedupe
    seen = set()
    unique = []
    for c in all_cards:
        if c['front'][:80] not in seen:
            seen.add(c['front'][:80])
            unique.append(c)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#separator:Tab\n#html:true\n#notetype:Basic\n#deck:Egzamin_2_BetterExtract\n\n")
        for c in unique:
            f.write(f"{c['front']}\t{c['back']}\t{c['tags']}\n")
    
    print(f"✅ Approach 2 (Better Extraction): {len(unique)} cards -> {output_file.name}")

if __name__ == "__main__":
    main()
