#!/usr/bin/env python3
"""
Generate Anki flashcards from exam questions in odpowiedzi/ folder.
Creates a tab-separated file compatible with Anki import.
"""

import os
import re
from pathlib import Path

def extract_question_and_answer(filepath):
    """Extract main question and key answer points from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = []
    
    # Extract file number for tagging
    filename = os.path.basename(filepath)
    match = re.match(r'(\d+)-(.+)\.md', filename)
    if match:
        num = match.group(1)
        topic = match.group(2).replace('-', '_')
    else:
        num = "00"
        topic = "unknown"
    
    # Extract main title (usually contains the question)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Unknown"
    
    # Extract the main question from ## Pytanie section
    question_match = re.search(r'## Pytanie\s*\n\s*\*\*["\']?(.+?)["\']?\*\*', content, re.DOTALL)
    if question_match:
        main_question = question_match.group(1).strip()
        main_question = re.sub(r'\s+', ' ', main_question)
    else:
        main_question = title
    
    # Extract subject/przedmiot
    subject_match = re.search(r'Przedmiot:\s*(\w+)', content)
    subject = subject_match.group(1) if subject_match else "Ogólne"
    
    # Create main question card - extract key sections for answer
    answer_parts = []
    
    # Look for main answer section
    main_answer = re.search(r'## 📚 Odpowiedź główna\s*\n(.+?)(?=\n## |\n---\s*\n## |\Z)', content, re.DOTALL)
    if main_answer:
        answer_text = main_answer.group(1)
        # Extract key points, definitions, headers
        headers = re.findall(r'### (.+)', answer_text)
        for h in headers[:5]:  # Limit to first 5 headers
            answer_parts.append(f"• {h}")
    
    # Also extract key definitions if present
    definitions = re.findall(r'\*\*([^*]+)\*\*\s*[-–:]\s*([^*\n]+)', content)
    for term, definition in definitions[:3]:
        if len(definition) > 20 and len(definition) < 200:
            answer_parts.append(f"• {term}: {definition.strip()}")
    
    # If we found answer parts, create main card
    if answer_parts:
        answer_html = "<br>".join(answer_parts[:8])  # Limit answer length
        cards.append({
            'question': main_question,
            'answer': answer_html,
            'tags': f"egzamin_magisterski pytanie_{num} {subject} {topic}"
        })
    
    # Extract sub-questions and key concepts as additional cards
    # Look for ### headers with explanations
    subsections = re.findall(r'### (\d+\.\s+)?(.+?)\n\n(.+?)(?=\n### |\n## |\n---|\Z)', content, re.DOTALL)
    
    for _, header, body in subsections:
        if len(header) < 5 or header.startswith('Przykład'):
            continue
        
        # Extract first substantive paragraph or key points
        body_clean = body.strip()
        
        # Skip very short or code-only sections
        if len(body_clean) < 50:
            continue
        
        # Extract bullet points or first paragraph
        bullets = re.findall(r'[-•]\s*\*\*(.+?)\*\*[:\s]*([^\n]+)?', body_clean)
        if bullets:
            answer_text = "<br>".join([f"• {b[0]}: {b[1].strip()}" if b[1] else f"• {b[0]}" for b in bullets[:5]])
        else:
            # Get first meaningful paragraph
            paragraphs = [p.strip() for p in body_clean.split('\n\n') if p.strip() and not p.startswith('```') and not p.startswith('|')]
            if paragraphs:
                first_para = paragraphs[0]
                # Clean markdown
                first_para = re.sub(r'\*\*(.+?)\*\*', r'\1', first_para)
                first_para = re.sub(r'\*(.+?)\*', r'\1', first_para)
                answer_text = first_para[:400]
            else:
                continue
        
        # Create sub-concept card
        sub_question = f"Co to jest {header}?" if not header.endswith('?') else header
        if "Charakterystyka" in header or "Definicja" in header or "Właściwości" in header:
            # These are answer-type headers, reframe
            parent_topic = title.replace("Pytanie", "").strip(": 0123456789")
            sub_question = f"{header} - {parent_topic}"
        
        cards.append({
            'question': sub_question,
            'answer': answer_text,
            'tags': f"egzamin_magisterski pytanie_{num} {subject} {topic} szczegoly"
        })
    
    # Extract key formulas/definitions as separate cards
    formulas = re.findall(r'\*\*([A-Za-z\s]+(?:formuła|wzór|twierdzenie|definicja|lemat))\*\*[:\s]*\n?(.+?)(?=\n\n|\n\*\*|\Z)', content, re.IGNORECASE | re.DOTALL)
    for formula_name, formula_content in formulas:
        if len(formula_content) > 20:
            cards.append({
                'question': f"Podaj {formula_name.strip()}",
                'answer': formula_content.strip()[:300],
                'tags': f"egzamin_magisterski pytanie_{num} {subject} formuly"
            })
    
    return cards

def clean_for_anki(text):
    """Clean text for Anki import - escape special characters."""
    # Replace tabs with spaces
    text = text.replace('\t', '    ')
    # Convert markdown formatting to HTML
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Handle newlines - convert to <br> for Anki
    text = text.replace('\n', '<br>')
    # Remove multiple <br>
    text = re.sub(r'(<br>)+', '<br>', text)
    # Remove leading/trailing <br>
    text = re.sub(r'^<br>|<br>$', '', text)
    # Escape quotes in a way that works with tab-separated
    text = text.replace('"', '&quot;')
    return text.strip()

def main():
    odpowiedzi_dir = Path("/home/kuchy/praca_magisterska/pytania/odpowiedzi")
    output_file = Path("/home/kuchy/praca_magisterska/pytania/anki_egzamin_magisterski.txt")
    
    all_cards = []
    
    # Process each file
    for md_file in sorted(odpowiedzi_dir.glob("*.md")):
        print(f"Processing: {md_file.name}")
        try:
            cards = extract_question_and_answer(md_file)
            all_cards.extend(cards)
            print(f"  -> Extracted {len(cards)} cards")
        except Exception as e:
            print(f"  -> Error: {e}")
    
    # Write Anki file with headers
    with open(output_file, 'w', encoding='utf-8') as f:
        # Anki file headers
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write("#columns:Front\tBack\tTags\n")
        f.write("#deck:Egzamin Magisterski ISY\n")
        f.write("#notetype:Basic\n")
        f.write("\n")
        
        for card in all_cards:
            front = clean_for_anki(card['question'])
            back = clean_for_anki(card['answer'])
            tags = card['tags']
            f.write(f"{front}\t{back}\t{tags}\n")
    
    print(f"\n✅ Created {len(all_cards)} flashcards")
    print(f"📁 Output: {output_file}")
    print("\nTo import into Anki:")
    print("1. Open Anki → File → Import")
    print("2. Select the .txt file")
    print("3. Verify 'Allow HTML' is checked")
    print("4. Click Import")

if __name__ == "__main__":
    main()
