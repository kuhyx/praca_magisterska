#!/usr/bin/env python3
"""
Generate Anki flashcards with ACTUAL substantive answers, not just headers.
"""

import os
import re
from pathlib import Path

def clean_text(text):
    """Clean text for Anki."""
    if not text:
        return ""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    text = text.replace('\t', ' ')
    text = text.replace('"', '&quot;')
    text = re.sub(r' +', ' ', text)
    return text.strip()

def extract_real_answer(content, section_name):
    """Extract actual content from a section, not just headers."""
    # Find the section
    pattern = rf'### (?:\d+\.\s*)?{re.escape(section_name)}\s*\n((?:(?!^### ).)+)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        return None
    
    body = match.group(1).strip()
    
    # Extract meaningful content
    lines = []
    
    # Get subheaders with their first line of content
    subheader_pattern = r'#### ([^\n]+)\n([^\n#]+)'
    for sub_header, first_line in re.findall(subheader_pattern, body):
        lines.append(f"<b>{sub_header.strip()}</b>: {first_line.strip()}")
    
    # Get bullet points
    bullet_pattern = r'[-•]\s*\*\*([^*]+)\*\*[:\s-]*([^\n]*)'
    for term, desc in re.findall(bullet_pattern, body):
        if desc.strip():
            lines.append(f"• <b>{term.strip()}</b>: {desc.strip()}")
        else:
            lines.append(f"• <b>{term.strip()}</b>")
    
    # If no structured content, get paragraphs
    if not lines:
        paras = [p.strip() for p in body.split('\n\n') 
                if p.strip() and not p.startswith('```') and not p.startswith('|')]
        for p in paras[:2]:
            if len(p) > 20 and len(p) < 400:
                lines.append(p)
    
    return '<br>'.join(lines[:6]) if lines else None

def extract_cards(filepath):
    """Extract flashcards from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = []
    filename = os.path.basename(filepath)
    match = re.match(r'(\d+)-(.+)\.md', filename)
    num = match.group(1) if match else "00"
    
    subj_match = re.search(r'Przedmiot:\s*(\w+)', content)
    subject = subj_match.group(1) if subj_match else "Ogólne"
    base_tags = f"egzamin_magisterski pyt{num} {subject}"
    
    # Get main question
    q_match = re.search(r'## Pytanie\s*\n\s*\*\*["\']?(.+?)["\']?\*\*', content, re.DOTALL)
    main_question = re.sub(r'\s+', ' ', q_match.group(1).strip()) if q_match else None
    
    # ===============================================
    # MAIN CARD: Question with REAL answer summary
    # ===============================================
    if main_question:
        # Build a real answer from the main sections
        answer_parts = []
        
        # For automata question - extract key facts about each automaton
        if "automat" in main_question.lower() or "maszyn" in main_question.lower():
            # FA
            fa_match = re.search(r'Automat Skończony.*?Rozpoznawana klasa języków\s*\n\s*\*\*([^*]+)\*\*', content, re.DOTALL)
            if fa_match:
                answer_parts.append(f"<b>Automat Skończony (FA)</b>: {fa_match.group(1).strip()}")
            
            # PDA
            pda_match = re.search(r'Automat ze Stosem.*?Rozpoznawana klasa języków\s*\n\s*\*\*([^*]+)\*\*', content, re.DOTALL)
            if pda_match:
                answer_parts.append(f"<b>Automat ze Stosem (PDA)</b>: {pda_match.group(1).strip()}")
            
            # TM
            tm_match = re.search(r'Maszyna Turinga.*?Rozpoznawana klasa języków\s*\n\s*\*\*([^*]+)\*\*', content, re.DOTALL)
            if tm_match:
                answer_parts.append(f"<b>Maszyna Turinga (TM)</b>: {tm_match.group(1).strip()}")
        
        # Generic extraction if specific didn't work
        if not answer_parts:
            # Look for key definitions/summaries
            key_patterns = [
                r'#### Definicja\s*\n([^\n#]+)',
                r'#### Charakterystyka\s*\n([^\n#]+)',
                r'\*\*Definicja[:\s]*\*\*\s*([^\n]+)',
            ]
            for pattern in key_patterns:
                for match in re.findall(pattern, content)[:3]:
                    if len(match) > 20:
                        answer_parts.append(match.strip())
        
        # Still nothing? Get first substantive paragraph from main answer
        if not answer_parts:
            main_answer = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
            if main_answer:
                # Skip headers, get actual content
                text = main_answer.group(1)
                paras = re.findall(r'\n\n([^#\n][^\n]{50,300})', text)
                answer_parts = paras[:3]
        
        if answer_parts:
            answer = '<br><br>'.join([clean_text(p) for p in answer_parts])
            cards.append({
                'front': clean_text(main_question),
                'back': answer,
                'tags': f"{base_tags} pytanie_glowne"
            })
    
    # ===============================================
    # CONCEPT CARDS: Specific topics with real content
    # ===============================================
    # Find all ### sections and extract their actual content
    sections = re.findall(
        r'^### (?:\d+\.\s*)?([^\n]+)\n((?:(?!^### ).)*)', 
        content, 
        re.MULTILINE | re.DOTALL
    )
    
    for header, body in sections:
        header = header.strip()
        body = body.strip()
        
        # Skip short sections, mnemonics, examples
        if len(body) < 80 or 'Przykład' in header or 'Mnemonic' in header or '"' in header:
            continue
        
        # Extract real content
        answer_lines = []
        
        # Get definition if present
        def_match = re.search(r'#### Definicja[^\n]*\n([^\n#]+(?:\n[^\n#]+)?)', body)
        if def_match:
            answer_lines.append(def_match.group(1).strip())
        
        # Get characterization
        char_match = re.search(r'#### Charakterystyka\s*\n((?:[-•][^\n]+\n?)+)', body)
        if char_match:
            bullets = re.findall(r'[-•]\s*\*\*([^*]+)\*\*[:\s]*([^\n]*)', char_match.group(1))
            for term, desc in bullets[:4]:
                answer_lines.append(f"• <b>{term}</b>: {desc.strip()}" if desc else f"• <b>{term}</b>")
        
        # Get bullet points if no structured content yet
        if not answer_lines:
            bullets = re.findall(r'[-•]\s*\*\*([^*]+)\*\*[:\s]*([^\n]*)', body)
            for term, desc in bullets[:5]:
                answer_lines.append(f"• <b>{term}</b>: {desc.strip()}" if desc else f"• <b>{term}</b>")
        
        # Get first paragraph if still nothing
        if not answer_lines:
            first_para = re.search(r'^([^#\n\-•|`][^\n]{30,250})', body, re.MULTILINE)
            if first_para:
                answer_lines.append(first_para.group(1))
        
        if answer_lines:
            question = f"Wyjaśnij: {header}" if not header.endswith('?') else header
            answer = '<br>'.join([clean_text(l) for l in answer_lines])
            
            cards.append({
                'front': clean_text(question),
                'back': answer,
                'tags': f"{base_tags} szczegoly"
            })
    
    # ===============================================
    # Q&A CARDS: From practice questions section
    # ===============================================
    qa_matches = re.findall(
        r'### Q\d+:\s*["\']?([^"\'?\n]+)\?*["\']?\s*\n.*?Odpowiedź:\s*\n(.+?)(?=\n### |\n## |\Z)',
        content, re.DOTALL
    )
    
    for question, answer in qa_matches[:5]:
        question = question.strip()
        answer = answer.strip()
        
        # Clean up answer - get first meaningful part
        answer_lines = answer.split('\n')
        clean_answer = []
        for line in answer_lines[:6]:
            line = line.strip()
            if line and not line.startswith('```') and not line.startswith('|'):
                clean_answer.append(line)
        
        if clean_answer:
            cards.append({
                'front': clean_text(question + '?'),
                'back': '<br>'.join([clean_text(l) for l in clean_answer]),
                'tags': f"{base_tags} qa"
            })
    
    return cards

def main():
    odpowiedzi_dir = Path("/home/kuchy/praca_magisterska/pytania/odpowiedzi")
    output_file = Path("/home/kuchy/praca_magisterska/pytania/anki_egzamin_magisterski.txt")
    
    all_cards = []
    
    for md_file in sorted(odpowiedzi_dir.glob("*.md")):
        print(f"Processing: {md_file.name}", end=" ")
        try:
            cards = extract_cards(md_file)
            all_cards.extend(cards)
            print(f"→ {len(cards)} cards")
        except Exception as e:
            print(f"→ ERROR: {e}")
    
    # Remove duplicates
    seen = set()
    unique_cards = []
    for card in all_cards:
        key = card['front'][:100]
        if key not in seen:
            seen.add(key)
            unique_cards.append(card)
    
    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#separator:Tab\n")
        f.write("#html:true\n")
        f.write("#notetype:Basic\n")
        f.write("#deck:Egzamin Magisterski ISY\n")
        f.write("#columns:Front\tBack\tTags\n")
        f.write("#tags column:3\n")
        f.write("\n")
        
        for card in unique_cards:
            front = card['front'].replace('\t', ' ')
            back = card['back'].replace('\t', ' ')
            tags = card['tags']
            f.write(f"{front}\t{back}\t{tags}\n")
    
    print(f"\n✅ Generated {len(unique_cards)} flashcards")
    print(f"📁 Output: {output_file}")

if __name__ == "__main__":
    main()
