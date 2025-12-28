#!/usr/bin/env python3
"""
Approach 1: STRICT FILTERING ONLY
- Only include cards with answers > 100 characters
- No changes to extraction logic
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
    
    # Main question
    q_match = re.search(r'## Pytanie\s*\n\s*\*\*["\']?(.+?)["\']?\*\*', content, re.DOTALL)
    if q_match:
        main_q = re.sub(r'\s+', ' ', q_match.group(1).strip())
        
        # Simple extraction - headers as answer
        answer_match = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
        if answer_match:
            headers = re.findall(r'^### (?:\d+\.\s*)?(.+)$', answer_match.group(1), re.MULTILINE)
            if headers:
                answer = '<ul>' + ''.join([f'<li>{clean_text(h)}</li>' for h in headers[:6]]) + '</ul>'
                cards.append({'front': clean_text(main_q), 'back': answer, 'tags': base_tags})
    
    # Detail cards - simple extraction
    sections = re.findall(r'^### (?:\d+\.\s*)?([^\n]+)\n((?:(?!^### ).)*)', content, re.MULTILINE | re.DOTALL)
    for header, body in sections:
        header = header.strip()
        body = body.strip()
        if len(body) < 50:
            continue
        
        # Get first paragraph
        paras = [p.strip() for p in body.split('\n\n') if p.strip() and not p.startswith('```')]
        if paras:
            answer = clean_text(paras[0][:400])
            cards.append({'front': f"Wyjaśnij: {clean_text(header)}", 'back': answer, 'tags': base_tags})
    
    return cards

def main():
    odpowiedzi_dir = Path("/home/kuchy/praca_magisterska/pytania/odpowiedzi")
    output_file = Path("/home/kuchy/praca_magisterska/pytania/anki_1_strict_filter.txt")
    
    all_cards = []
    for md_file in sorted(odpowiedzi_dir.glob("*.md")):
        all_cards.extend(extract_cards(md_file))
    
    # APPROACH 1: Strict filtering - only cards with answer > 100 chars
    filtered_cards = [c for c in all_cards if len(c['back']) > 100]
    
    # Remove duplicates
    seen = set()
    unique = []
    for c in filtered_cards:
        if c['front'][:80] not in seen:
            seen.add(c['front'][:80])
            unique.append(c)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#separator:Tab\n#html:true\n#notetype:Basic\n#deck:Egzamin_1_StrictFilter\n\n")
        for c in unique:
            f.write(f"{c['front']}\t{c['back']}\t{c['tags']}\n")
    
    print(f"✅ Approach 1 (Strict Filter): {len(unique)} cards -> {output_file.name}")

if __name__ == "__main__":
    main()
