#!/usr/bin/env python3
"""
Generate Anki flashcards from exam questions in odpowiedzi/ folder.
Creates a tab-separated file compatible with Anki import.
"""

import os
import re
from pathlib import Path

def extract_main_question(content, filename):
    """Extract the main exam question from the file."""
    # Extract the main question from ## Pytanie section
    question_match = re.search(r'## Pytanie\s*\n\s*\*\*["\']?(.+?)["\']?\*\*', content, re.DOTALL)
    if question_match:
        main_question = question_match.group(1).strip()
        main_question = re.sub(r'\s+', ' ', main_question)
        return main_question
    
    # Fallback to title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return title_match.group(1) if title_match else filename

def extract_subject(content):
    """Extract the subject code."""
    subject_match = re.search(r'Przedmiot:\s*(\w+)', content)
    return subject_match.group(1) if subject_match else "Ogólne"

def extract_key_points(content):
    """Extract key points from the main answer section."""
    points = []
    
    # Look for main answer section
    main_answer = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## [^�]|\n---\s*\n## |\Z)', content, re.DOTALL)
    if not main_answer:
        return points
    
    answer_text = main_answer.group(1)
    
    # Extract ### headers as key points
    headers = re.findall(r'^### (.+)$', answer_text, re.MULTILINE)
    for h in headers[:6]:
        # Clean header
        h = re.sub(r'\d+\.\s*', '', h).strip()
        if h and len(h) > 3:
            points.append(h)
    
    return points

def extract_definitions(content):
    """Extract key definitions from the content."""
    definitions = []
    
    # Pattern for **Term** - definition or **Term**: definition
    pattern = r'\*\*([^*\n]+)\*\*\s*[-–:]\s*([^*\n]{20,150})'
    matches = re.findall(pattern, content)
    
    for term, definition in matches:
        term = term.strip()
        definition = definition.strip()
        # Filter out non-definition patterns
        if term and definition and not term.startswith('Przykład') and not term.startswith('Uwaga'):
            definitions.append((term, definition))
    
    return definitions[:5]

def clean_html(text):
    """Convert markdown to HTML and clean for Anki."""
    if not text:
        return ""
    
    # Replace markdown bold/italic with HTML
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    
    # Clean up special characters
    text = text.replace('\t', ' ')
    text = text.replace('"', '&quot;')
    
    # Handle newlines - convert to <br>
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def process_file(filepath):
    """Process a single file and return flashcards."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = []
    
    # Extract metadata
    filename = os.path.basename(filepath)
    match = re.match(r'(\d+)-(.+)\.md', filename)
    if match:
        num = match.group(1)
        topic = match.group(2).replace('-', '_')
    else:
        num = "00"
        topic = "unknown"
    
    subject = extract_subject(content)
    main_question = extract_main_question(content, filename)
    
    # Base tags for this question
    base_tags = f"egzamin_magisterski pytanie_{num} {subject}"
    
    # Card 1: Main question with key points
    key_points = extract_key_points(content)
    if key_points:
        answer = "<ul>" + "".join([f"<li>{clean_html(p)}</li>" for p in key_points]) + "</ul>"
        cards.append({
            'front': clean_html(main_question),
            'back': answer,
            'tags': base_tags
        })
    
    # Card 2+: Key definitions as individual cards
    definitions = extract_definitions(content)
    for term, definition in definitions:
        q = f"Definicja: {term}"
        a = clean_html(definition)
        cards.append({
            'front': q,
            'back': a,
            'tags': f"{base_tags} definicje"
        })
    
    return cards

def main():
    odpowiedzi_dir = Path("/home/kuchy/praca_magisterska/pytania/odpowiedzi")
    output_file = Path("/home/kuchy/praca_magisterska/pytania/anki_egzamin_magisterski.txt")
    
    all_cards = []
    
    # Process each file
    for md_file in sorted(odpowiedzi_dir.glob("*.md")):
        print(f"Processing: {md_file.name}")
        try:
            cards = process_file(md_file)
            all_cards.extend(cards)
            print(f"  -> {len(cards)} cards")
        except Exception as e:
            print(f"  -> Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Write Anki-compatible file
    with open(output_file, 'w', encoding='utf-8') as f:
        # File headers for Anki
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write("#tags column:3\n")
        f.write("#deck:Egzamin Magisterski ISY\n")
        f.write("#notetype:Basic\n")
        f.write("\n")
        
        for card in all_cards:
            front = card['front']
            back = card['back']
            tags = card['tags']
            
            # Ensure no tabs in content
            front = front.replace('\t', ' ')
            back = back.replace('\t', ' ')
            
            f.write(f"{front}\t{back}\t{tags}\n")
    
    print(f"\n✅ Created {len(all_cards)} flashcards")
    print(f"📁 Output: {output_file}")
    print("\n=== Import Instructions ===")
    print("1. Open Anki desktop → File → Import")
    print("2. Select: anki_egzamin_magisterski.txt")
    print("3. Set 'Fields separated by: Tab'")
    print("4. Check 'Allow HTML in fields'") 
    print("5. Map: Field 1 → Front, Field 2 → Back, Field 3 → Tags")
    print("6. Click Import")
    print("\nFor AnkiWeb/AnkiDroid: Sync after importing on desktop")

if __name__ == "__main__":
    main()
