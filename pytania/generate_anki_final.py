#!/usr/bin/env python3
"""
Generate comprehensive Anki flashcards from exam questions.
Creates tab-separated file for Anki import with proper HTML formatting.
"""

import os
import re
from pathlib import Path

def clean_text(text):
    """Clean and format text for Anki."""
    if not text:
        return ""
    
    # Convert markdown formatting to HTML
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    
    # Handle special characters
    text = text.replace('\t', ' ')
    text = text.replace('"', '&quot;')
    
    # Clean up whitespace but preserve intentional line breaks
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    
    return text

def format_list(items, numbered=False):
    """Format a list of items as HTML."""
    if not items:
        return ""
    
    tag = "ol" if numbered else "ul"
    html = f"<{tag}>"
    for item in items:
        cleaned = clean_text(item)
        if cleaned:
            html += f"<li>{cleaned}</li>"
    html += f"</{tag}>"
    return html

def extract_from_file(filepath):
    """Extract flashcard data from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = []
    
    # Get file metadata
    filename = os.path.basename(filepath)
    match = re.match(r'(\d+)-(.+)\.md', filename)
    num = match.group(1) if match else "00"
    topic_slug = match.group(2).replace('-', '_') if match else "unknown"
    
    # Extract subject
    subj_match = re.search(r'Przedmiot:\s*(\w+)', content)
    subject = subj_match.group(1) if subj_match else "Ogólne"
    
    # Base tags
    base_tags = f"egzamin_magisterski pyt{num} {subject}"
    
    # =====================================================
    # CARD TYPE 1: Main Exam Question
    # =====================================================
    q_match = re.search(r'## Pytanie\s*\n\s*\*\*["\']?(.+?)["\']?\*\*', content, re.DOTALL)
    if q_match:
        main_q = re.sub(r'\s+', ' ', q_match.group(1).strip())
        
        # Extract key topics from main answer
        answer_match = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## [�🎯]|\n---\s*\n## |\Z)', content, re.DOTALL)
        if answer_match:
            answer_section = answer_match.group(1)
            # Get main headers
            headers = re.findall(r'^### (?:\d+\.\s*)?(.+)$', answer_section, re.MULTILINE)
            headers = [h.strip() for h in headers if len(h.strip()) > 3][:6]
            
            if headers:
                answer_html = "<b>Kluczowe zagadnienia:</b>" + format_list(headers)
                cards.append({
                    'front': clean_text(main_q),
                    'back': answer_html,
                    'tags': f"{base_tags} pytanie_glowne"
                })
    
    # =====================================================
    # CARD TYPE 2: Subsection Cards (detailed concepts)
    # =====================================================
    # Find all ### sections
    sections = re.findall(
        r'^### (?:\d+\.\s*)?(.+?)\n((?:(?!^###).)+)', 
        content, 
        re.MULTILINE | re.DOTALL
    )
    
    for header, body in sections:
        header = header.strip()
        body = body.strip()
        
        # Skip very short sections or example sections
        if len(body) < 50 or header.lower().startswith('przykład'):
            continue
        
        # Extract key information from body
        answer_parts = []
        
        # Look for #### sub-headers
        subheaders = re.findall(r'^#### (.+)$', body, re.MULTILINE)
        if subheaders:
            answer_parts.extend(subheaders[:4])
        
        # Look for bullet points with bold terms
        bullets = re.findall(r'[-•]\s*\*\*([^*]+)\*\*[:\s-]*([^\n]+)?', body)
        for term, desc in bullets[:5]:
            if desc:
                answer_parts.append(f"<b>{term}</b>: {desc.strip()}")
            else:
                answer_parts.append(f"<b>{term}</b>")
        
        # If no structured content, get first paragraph
        if not answer_parts:
            paras = [p.strip() for p in body.split('\n\n') 
                    if p.strip() and not p.strip().startswith('```') 
                    and not p.strip().startswith('|')]
            if paras:
                first = paras[0]
                # Limit length
                if len(first) > 300:
                    first = first[:300] + "..."
                answer_parts.append(first)
        
        if answer_parts:
            # Determine card type
            if "Definicja" in header or "Co to" in header:
                q = f"Co to jest: {header.replace('Definicja', '').strip()}?"
            elif "Charakterystyka" in header:
                q = f"Scharakteryzuj: {header.replace('Charakterystyka', '').strip()}"
            elif header.endswith('?'):
                q = header
            else:
                q = f"Omów: {header}"
            
            # Format answer
            if len(answer_parts) > 1:
                answer_html = format_list(answer_parts)
            else:
                answer_html = clean_text(answer_parts[0])
            
            cards.append({
                'front': clean_text(q),
                'back': answer_html,
                'tags': f"{base_tags} szczegoly"
            })
    
    # =====================================================
    # CARD TYPE 3: Algorithms/Formulas
    # =====================================================
    algo_patterns = [
        r'#### Złożoność(?:\s+czasowa)?\s*\n(.+?)(?=\n####|\n###|\Z)',
        r'Złożoność:\s*\*\*([^*]+)\*\*',
    ]
    
    for pattern in algo_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches[:2]:
            if len(match) > 10:
                # Find context - which algorithm?
                algo_context = re.search(r'### (\d+\.\s*)?(.+?)(?=\n)', content[:content.find(match)])
                if algo_context:
                    algo_name = algo_context.group(2).strip()
                    cards.append({
                        'front': f"Jaka jest złożoność algorytmu/metody: {algo_name}?",
                        'back': clean_text(match.strip()[:200]),
                        'tags': f"{base_tags} zlozonosc"
                    })
                    break
    
    # =====================================================
    # CARD TYPE 4: Comparisons (when file contains comparisons)
    # =====================================================
    compare_match = re.search(r'## .*(Porównanie|Zestawienie|vs).*\n(.+?)(?=\n## |\Z)', content, re.DOTALL | re.IGNORECASE)
    if compare_match:
        compare_section = compare_match.group(2)
        # Extract comparison items
        items = re.findall(r'\|\s*\*\*([^|*]+)\*\*\s*\|([^|]+)\|', compare_section)
        if items:
            comparison_html = "<table><tr><th>Aspekt</th><th>Wartość</th></tr>"
            for aspect, value in items[:6]:
                comparison_html += f"<tr><td>{clean_text(aspect)}</td><td>{clean_text(value)}</td></tr>"
            comparison_html += "</table>"
            
            # Get comparison title
            title_match = re.search(r'## .*(Porównanie|Zestawienie).*?(\w+.*?(?:vs|i|oraz).*?\w+)', compare_match.group(0), re.IGNORECASE)
            if title_match:
                cards.append({
                    'front': f"Porównaj kluczowe różnice w temacie: pytanie {num}",
                    'back': comparison_html,
                    'tags': f"{base_tags} porownanie"
                })
    
    # =====================================================
    # CARD TYPE 5: Q&A from practice questions section
    # =====================================================
    qa_section = re.search(r'## 🎓 Pytania.*?\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
    if qa_section:
        qa_content = qa_section.group(1)
        # Find Q&A pairs
        qas = re.findall(r'### Q\d+:?\s*["\']?(.+?)["\']?\s*\n.*?Odpowiedź:\s*\n?(.+?)(?=\n### |\Z)', qa_content, re.DOTALL)
        for q, a in qas[:3]:
            q = re.sub(r'\s+', ' ', q.strip())
            a = a.strip()
            if len(a) > 30:
                # Limit answer length
                a_lines = a.split('\n')
                a_short = '\n'.join(a_lines[:5])
                if len(a_short) > 400:
                    a_short = a_short[:400] + "..."
                
                cards.append({
                    'front': clean_text(q),
                    'back': clean_text(a_short).replace('\n', '<br>'),
                    'tags': f"{base_tags} egzamin_praktyka"
                })
    
    return cards

def main():
    odpowiedzi_dir = Path("/home/kuchy/praca_magisterska/pytania/odpowiedzi")
    output_file = Path("/home/kuchy/praca_magisterska/pytania/anki_egzamin_magisterski.txt")
    
    all_cards = []
    
    for md_file in sorted(odpowiedzi_dir.glob("*.md")):
        print(f"Processing: {md_file.name}", end=" ")
        try:
            cards = extract_from_file(md_file)
            all_cards.extend(cards)
            print(f"→ {len(cards)} cards")
        except Exception as e:
            print(f"→ ERROR: {e}")
    
    # Remove potential duplicates (same front)
    seen = set()
    unique_cards = []
    for card in all_cards:
        if card['front'] not in seen:
            seen.add(card['front'])
            unique_cards.append(card)
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Anki headers
        f.write("#separator:tab\n")
        f.write("#html:true\n") 
        f.write("#tags column:3\n")
        f.write("#deck:Egzamin Magisterski ISY\n")
        f.write("#notetype:Basic\n")
        f.write("\n")
        
        for card in unique_cards:
            # Ensure no tabs in content (would break parsing)
            front = card['front'].replace('\t', ' ')
            back = card['back'].replace('\t', ' ')
            tags = card['tags']
            
            f.write(f"{front}\t{back}\t{tags}\n")
    
    print(f"\n{'='*50}")
    print(f"✅ Generated {len(unique_cards)} unique flashcards")
    print(f"📁 Saved to: {output_file}")
    print(f"{'='*50}")
    print("\n📋 IMPORT INSTRUCTIONS:")
    print("─" * 40)
    print("Anki Desktop:")
    print("  1. File → Import")
    print("  2. Select: anki_egzamin_magisterski.txt")
    print("  3. Verify: Fields separated by Tab")
    print("  4. Check: Allow HTML in fields")
    print("  5. Click Import")
    print()
    print("AnkiWeb / AnkiDroid:")
    print("  1. First import on Anki Desktop")
    print("  2. Click Sync to upload to AnkiWeb")
    print("  3. Sync on mobile to download")

if __name__ == "__main__":
    main()
