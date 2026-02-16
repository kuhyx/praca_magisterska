#!/usr/bin/env python3
"""
Generate B&W normalization step diagrams for PYTANIE 3.
Each diagram shows database tables at a specific normalization stage.
Designed for A4 laser printer output (300 DPI, black & white).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common settings
DPI = 300
FONT_SIZE = 8
HEADER_COLOR = '#D0D0D0'
CELL_COLOR = '#FFFFFF'
HIGHLIGHT_COLOR = '#F0D0D0'  # light red-ish gray for violations
FIXED_COLOR = '#D0F0D0'      # light green-ish gray for fixed
FD_ARROW_COLOR = '#444444'


def draw_table(ax, x, y, title, headers, rows, col_widths=None,
               highlight_cols=None, highlight_rows=None, highlight_cells=None,
               strikethrough_cells=None, title_fontsize=9):
    """Draw a single table on the axes at position (x, y).
    
    Args:
        ax: matplotlib axes
        x, y: top-left position
        title: table title string
        headers: list of column header strings
        rows: list of lists (row data)
        col_widths: list of column widths (in inches-ish units)
        highlight_cols: set of column indices to highlight
        highlight_rows: set of row indices to highlight
        highlight_cells: set of (row, col) to highlight
        strikethrough_cells: set of (row, col) to draw strikethrough
        title_fontsize: font size for table title
    
    Returns:
        (width, height) of the drawn table
    """
    n_cols = len(headers)
    n_rows = len(rows)
    
    if col_widths is None:
        # Auto-calculate based on content
        col_widths = []
        for c in range(n_cols):
            max_len = len(headers[c])
            for r in rows:
                if c < len(r):
                    max_len = max(max_len, len(str(r[c])))
            col_widths.append(max(max_len * 0.08 + 0.1, 0.5))
    
    row_height = 0.22
    total_width = sum(col_widths)
    total_height = (n_rows + 1) * row_height  # +1 for header
    
    # Title
    ax.text(x + total_width / 2, y + 0.18, title,
            fontsize=title_fontsize, fontweight='bold',
            ha='center', va='bottom', family='monospace')
    
    y_start = y
    
    # Draw header row
    cx = x
    for c, (hdr, w) in enumerate(zip(headers, col_widths)):
        color = HEADER_COLOR
        rect = mpatches.FancyBboxPatch(
            (cx, y_start), w, -row_height,
            boxstyle="square,pad=0", facecolor=color,
            edgecolor='black', linewidth=0.5)
        ax.add_patch(rect)
        ax.text(cx + w / 2, y_start - row_height / 2, hdr,
                fontsize=FONT_SIZE, fontweight='bold',
                ha='center', va='center', family='monospace')
        cx += w
    
    # Draw data rows
    for r_idx, row in enumerate(rows):
        cy = y_start - (r_idx + 1) * row_height
        cx = x
        for c_idx, (val, w) in enumerate(zip(row, col_widths)):
            color = CELL_COLOR
            if highlight_cols and c_idx in highlight_cols:
                color = HIGHLIGHT_COLOR
            if highlight_rows and r_idx in highlight_rows:
                color = HIGHLIGHT_COLOR
            if highlight_cells and (r_idx, c_idx) in highlight_cells:
                color = HIGHLIGHT_COLOR
            
            rect = mpatches.FancyBboxPatch(
                (cx, cy), w, -row_height,
                boxstyle="square,pad=0", facecolor=color,
                edgecolor='black', linewidth=0.5)
            ax.add_patch(rect)
            
            text_color = 'black'
            ax.text(cx + w / 2, cy - row_height / 2, str(val),
                    fontsize=FONT_SIZE, ha='center', va='center',
                    family='monospace', color=text_color)
            
            if strikethrough_cells and (r_idx, c_idx) in strikethrough_cells:
                ax.plot([cx + 0.03, cx + w - 0.03],
                        [cy - row_height / 2, cy - row_height / 2],
                        color='black', linewidth=1.0)
            
            cx += w
    
    return total_width, total_height + 0.25  # extra for title


def create_figure(width_inches=11.69, height_inches=8.27):
    """Create A4 landscape figure."""
    fig, ax = plt.subplots(1, 1, figsize=(width_inches, height_inches), dpi=DPI)
    ax.set_xlim(0, width_inches)
    ax.set_ylim(0, height_inches)
    ax.axis('off')
    ax.set_aspect('equal')
    return fig, ax


def add_arrow(ax, x1, y1, x2, y2, label='', color='black'):
    """Draw an arrow with optional label."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.12, label, fontsize=7, ha='center', va='bottom',
                family='monospace', color=color)


def add_label(ax, x, y, text, fontsize=8, color='black', ha='left', style='normal'):
    """Add a text label."""
    ax.text(x, y, text, fontsize=fontsize, ha=ha, va='center',
            family='monospace', color=color, style=style)


# ============================================================
# DIAGRAM 1: 0NF Table
# ============================================================
def draw_0nf():
    fig, ax = create_figure(11.69, 5.5)
    
    headers = ['StID', 'Imie', 'Telefony', 'KursID', 'NazwaKursu',
               'Prowadzacy', 'WydzialID', 'NazwaWydzialu']
    rows = [
        ['1', 'Anna', '111-222, 333-444', 'K10', 'Bazy danych', 'Kowalski', 'W4', 'EiTI'],
        ['1', 'Anna', '111-222, 333-444', 'K20', 'Algorytmy', 'Nowak', 'W4', 'EiTI'],
        ['2', 'Jan', '555-666', 'K10', 'Bazy danych', 'Kowalski', 'W4', 'EiTI'],
        ['3', 'Ewa', '777-888', 'K30', 'Optyka', 'Wisniewski', 'W2', 'Fizyka'],
    ]
    col_widths = [0.5, 0.55, 1.55, 0.65, 1.1, 1.05, 0.85, 1.2]
    
    # Highlight the non-atomic column
    draw_table(ax, 0.8, 4.5, '0NF: Rejestr (forma nienormalna)',
               headers, rows, col_widths,
               highlight_cols={2},  # Telefony column
               title_fontsize=11)
    
    # Annotations
    add_label(ax, 0.8, 1.9,
              'PROBLEM: Kolumna "Telefony" zawiera LISTY wartosci (nieatomowe).',
              fontsize=9, color='black')
    add_label(ax, 0.8, 1.55,
              'Redundancja: "Anna", "W4", "EiTI", "Bazy danych" powtorzone wielokrotnie.',
              fontsize=9, color='black')
    add_label(ax, 0.8, 1.2,
              'Zaleznosci funkcyjne:  StID -> Imie, WydzialID    |    WydzialID -> NazwaWydzialu',
              fontsize=8, color='#333333')
    add_label(ax, 0.8, 0.9,
              '  KursID -> NazwaKursu    |    (StID,KursID) -> Prowadzacy    |    Prowadzacy -> KursID',
              fontsize=8, color='#333333')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_0nf_table.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_0nf_table.png")


# ============================================================
# DIAGRAM 2: 1NF — atomic values
# ============================================================
def draw_1nf():
    fig, ax = create_figure(11.69, 6.0)
    
    # Main table after removing Telefony
    headers1 = ['StID*', 'Imie', 'KursID*', 'NazwaKursu',
                'Prowadzacy', 'WydzialID', 'NazwaWydzialu']
    rows1 = [
        ['1', 'Anna', 'K10', 'Bazy danych', 'Kowalski', 'W4', 'EiTI'],
        ['1', 'Anna', 'K20', 'Algorytmy', 'Nowak', 'W4', 'EiTI'],
        ['2', 'Jan', 'K10', 'Bazy danych', 'Kowalski', 'W4', 'EiTI'],
        ['3', 'Ewa', 'K30', 'Optyka', 'Wisniewski', 'W2', 'Fizyka'],
    ]
    cw1 = [0.55, 0.55, 0.7, 1.1, 1.05, 0.85, 1.2]
    
    draw_table(ax, 0.5, 5.2, '1NF: Rejestr  (klucz: StID, KursID)',
               headers1, rows1, cw1, title_fontsize=10)
    
    # Telefony table
    headers2 = ['StID*', 'Telefon*']
    rows2 = [
        ['1', '111-222'],
        ['1', '333-444'],
        ['2', '555-666'],
        ['3', '777-888'],
    ]
    cw2 = [0.55, 0.85]
    
    draw_table(ax, 7.5, 5.2, 'Telefony  (klucz: StID, Telefon)',
               headers2, rows2, cw2, title_fontsize=10)
    
    # Arrow
    add_arrow(ax, 6.6, 4.3, 7.4, 4.3, 'wydzielono', '#333333')
    
    # Annotations
    add_label(ax, 0.5, 2.6,
              'KROK: Nieatomowa kolumna "Telefony" wydzielona do osobnej tabeli.',
              fontsize=9)
    add_label(ax, 0.5, 2.25,
              'Kazda komorka zawiera JEDNA wartosc. Klucz glowny wyznaczony.',
              fontsize=9)
    add_label(ax, 0.5, 1.85,
              'PROBLEM 2NF: NazwaKursu zalezy TYLKO od KursID (czesc klucza).',
              fontsize=9, color='black')
    add_label(ax, 0.5, 1.5,
              '             Imie, WydzialID, NazwaWydzialu zaleza TYLKO od StID (czesc klucza).',
              fontsize=9, color='black')
    add_label(ax, 0.5, 1.15,
              '  --> Czesciowe zaleznosci od klucza zlozonego = NARUSZENIE 2NF.',
              fontsize=9, color='black')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_1nf_tables.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_1nf_tables.png")


# ============================================================
# DIAGRAM 3: 2NF — no partial dependencies
# ============================================================
def draw_2nf():
    fig, ax = create_figure(11.69, 6.5)
    
    # Studenci
    h1 = ['StID*', 'Imie', 'WydzialID', 'NazwaWydzialu']
    r1 = [['1', 'Anna', 'W4', 'EiTI'],
          ['2', 'Jan', 'W4', 'EiTI'],
          ['3', 'Ewa', 'W2', 'Fizyka']]
    cw1 = [0.55, 0.55, 0.85, 1.2]
    draw_table(ax, 0.3, 5.8, 'Studenci (kl: StID)',
               h1, r1, cw1, highlight_cols={2, 3}, title_fontsize=9)
    
    # Kursy
    h2 = ['KursID*', 'NazwaKursu']
    r2 = [['K10', 'Bazy danych'], ['K20', 'Algorytmy'], ['K30', 'Optyka']]
    cw2 = [0.7, 1.1]
    draw_table(ax, 4.0, 5.8, 'Kursy (kl: KursID)',
               h2, r2, cw2, title_fontsize=9)
    
    # Zapisy
    h3 = ['StID*', 'KursID*', 'Prowadzacy']
    r3 = [['1', 'K10', 'Kowalski'], ['1', 'K20', 'Nowak'],
          ['2', 'K10', 'Kowalski'], ['3', 'K30', 'Wisniewski']]
    cw3 = [0.55, 0.7, 1.05]
    draw_table(ax, 6.8, 5.8, 'Zapisy (kl: StID, KursID)',
               h3, r3, cw3, title_fontsize=9)
    
    # Telefony
    h4 = ['StID*', 'Telefon*']
    r4 = [['1', '111-222'], ['1', '333-444'], ['2', '555-666'], ['3', '777-888']]
    cw4 = [0.55, 0.85]
    draw_table(ax, 9.5, 5.8, 'Telefony',
               h4, r4, cw4, title_fontsize=9)
    
    # Annotations
    add_label(ax, 0.3, 3.3,
              'KROK: Rozbito czesc. zaleznosci — atrybuty zalezne od czesci klucza wydzielone.',
              fontsize=9)
    add_label(ax, 0.3, 2.95,
              '  StID -> Imie, WydzialID, NazwaWydzialu  ==>  tabela Studenci',
              fontsize=8, color='#333333')
    add_label(ax, 0.3, 2.65,
              '  KursID -> NazwaKursu                    ==>  tabela Kursy',
              fontsize=8, color='#333333')
    add_label(ax, 0.3, 2.3,
              'PROBLEM 3NF w "Studenci": StID -> WydzialID -> NazwaWydzialu',
              fontsize=9, color='black')
    add_label(ax, 0.3, 1.95,
              '  NazwaWydzialu zalezy od WydzialID (nie-klucz), nie bezposrednio od StID.',
              fontsize=9, color='black')
    add_label(ax, 0.3, 1.6,
              '  --> Zaleznosc PRZECHODNIA = NARUSZENIE 3NF.',
              fontsize=9, color='black')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_2nf_tables.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_2nf_tables.png")


# ============================================================
# DIAGRAM 4: 3NF — no transitive dependencies
# ============================================================
def draw_3nf():
    fig, ax = create_figure(11.69, 6.5)
    
    # Studenci (fixed)
    h1 = ['StID*', 'Imie', 'WydzialID']
    r1 = [['1', 'Anna', 'W4'], ['2', 'Jan', 'W4'], ['3', 'Ewa', 'W2']]
    cw1 = [0.55, 0.55, 0.85]
    draw_table(ax, 0.3, 5.8, 'Studenci (kl: StID)',
               h1, r1, cw1, title_fontsize=9)
    
    # Wydzialy (new!)
    h2 = ['WydzialID*', 'NazwaWydzialu']
    r2 = [['W4', 'EiTI'], ['W2', 'Fizyka']]
    cw2 = [0.85, 1.2]
    draw_table(ax, 2.6, 5.8, 'Wydzialy (kl: WydzialID)',
               h2, r2, cw2, title_fontsize=9)
    
    # Kursy
    h3 = ['KursID*', 'NazwaKursu']
    r3 = [['K10', 'Bazy danych'], ['K20', 'Algorytmy'], ['K30', 'Optyka']]
    cw3 = [0.7, 1.1]
    draw_table(ax, 5.2, 5.8, 'Kursy (kl: KursID)',
               h3, r3, cw3, title_fontsize=9)
    
    # Zapisy (highlight BCNF violation)
    h4 = ['StID*', 'KursID*', 'Prowadzacy']
    r4 = [['1', 'K10', 'Kowalski'], ['1', 'K20', 'Nowak'],
          ['2', 'K10', 'Kowalski'], ['3', 'K30', 'Wisniewski']]
    cw4 = [0.55, 0.7, 1.05]
    draw_table(ax, 7.8, 5.8, 'Zapisy (kl: StID, KursID)',
               h4, r4, cw4, highlight_cols={1, 2}, title_fontsize=9)
    
    # Annotations
    add_label(ax, 0.3, 3.3,
              'KROK: Rozdzielono Studenci -> Studenci + Wydzialy (usun. zal. przechodnia).',
              fontsize=9)
    add_label(ax, 0.3, 2.95,
              '  StID -> WydzialID -> NazwaWydzialu  rozbito: NazwaWydzialu w osobnej tabeli.',
              fontsize=8, color='#333333')
    add_label(ax, 0.3, 2.55,
              'PROBLEM BCNF w "Zapisy":  FD: Prowadzacy -> KursID (1 prowadzacy = 1 kurs)',
              fontsize=9, color='black')
    add_label(ax, 0.3, 2.2,
              '  Prowadzacy NIE jest nadkluczem tabeli Zapisy -> NARUSZENIE BCNF.',
              fontsize=9, color='black')
    add_label(ax, 0.3, 1.85,
              '  3NF OK, bo KursID jest atrybutem pierwszym (prime) -> wyjatek 3NF.',
              fontsize=9, color='#333333')
    add_label(ax, 0.3, 1.5,
              '  BCNF nie ma takiego wyjatku -> kazda nietrywialna FD wymaga nadklucza po lewej.',
              fontsize=9, color='#333333')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_3nf_tables.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_3nf_tables.png")


# ============================================================
# DIAGRAM 5: BCNF — every determinant is a superkey
# ============================================================
def draw_bcnf():
    fig, ax = create_figure(11.69, 7.5)
    
    # Studenci
    h1 = ['StID*', 'Imie', 'WydzialID']
    r1 = [['1', 'Anna', 'W4'], ['2', 'Jan', 'W4'], ['3', 'Ewa', 'W2']]
    cw1 = [0.55, 0.55, 0.85]
    draw_table(ax, 0.3, 6.8, 'Studenci', h1, r1, cw1, title_fontsize=9)
    
    # Wydzialy
    h2 = ['WydzialID*', 'NazwaWydz.']
    r2 = [['W4', 'EiTI'], ['W2', 'Fizyka']]
    cw2 = [0.85, 1.0]
    draw_table(ax, 2.5, 6.8, 'Wydzialy', h2, r2, cw2, title_fontsize=9)
    
    # Kursy
    h3 = ['KursID*', 'NazwaKursu']
    r3 = [['K10', 'Bazy danych'], ['K20', 'Algorytmy'], ['K30', 'Optyka']]
    cw3 = [0.7, 1.1]
    draw_table(ax, 4.8, 6.8, 'Kursy', h3, r3, cw3, title_fontsize=9)
    
    # ProwadzacyKurs (NEW - from BCNF decomposition)
    h4 = ['Prowadzacy*', 'KursID']
    r4 = [['Kowalski', 'K10'], ['Nowak', 'K20'], ['Wisniewski', 'K30']]
    cw4 = [1.05, 0.7]
    draw_table(ax, 7.2, 6.8, 'ProwadzacyKurs (kl: Prow.)',
               h4, r4, cw4, title_fontsize=9)
    
    # StudentProwadzacy (NEW)
    h5 = ['StID*', 'Prowadzacy*']
    r5 = [['1', 'Kowalski'], ['1', 'Nowak'], ['2', 'Kowalski'], ['3', 'Wisniewski']]
    cw5 = [0.55, 1.05]
    draw_table(ax, 9.5, 6.8, 'StudentProw. (kl: oba)',
               h5, r5, cw5, title_fontsize=9)
    
    # Telefony
    h6 = ['StID*', 'Telefon*']
    r6 = [['1', '111-222'], ['1', '333-444'], ['2', '555-666'], ['3', '777-888']]
    cw6 = [0.55, 0.85]
    draw_table(ax, 0.3, 4.6, 'Telefony', h6, r6, cw6, title_fontsize=9)
    
    # Annotations
    add_label(ax, 0.3, 2.9,
              'KROK: Zapisy(StID, KursID, Prowadzacy) rozbite na:',
              fontsize=9)
    add_label(ax, 0.3, 2.55,
              '  ProwadzacyKurs(Prowadzacy, KursID)  — FD: Prowadzacy -> KursID, klucz: Prowadzacy',
              fontsize=8, color='#333333')
    add_label(ax, 0.3, 2.25,
              '  StudentProwadzacy(StID, Prowadzacy)  — ktory student u ktorego prowadzacego',
              fontsize=8, color='#333333')
    add_label(ax, 0.3, 1.85,
              'Teraz KAZDA nietrywialna FD ma nadklucz po lewej stronie -> BCNF spelnione.',
              fontsize=9)
    add_label(ax, 0.3, 1.45,
              'Rekonstrukcja: StudentProw. JOIN ProwadzacyKurs ON Prowadzacy -> odtworzenie Zapisy.',
              fontsize=8, color='#333333')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_bcnf_tables.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_bcnf_tables.png")


# ============================================================
# DIAGRAM 6: 4NF example — multi-valued dependencies
# ============================================================
def draw_4nf():
    fig, ax = create_figure(11.69, 7.5)
    
    # Before: table with MVD violation
    h_before = ['StID*', 'Hobby*', 'Umiejetnosc*']
    r_before = [
        ['1', 'Szachy', 'Python'],
        ['1', 'Szachy', 'SQL'],
        ['1', 'Bieganie', 'Python'],
        ['1', 'Bieganie', 'SQL'],
        ['2', 'Plywanie', 'Java'],
    ]
    cw_before = [0.55, 0.9, 1.0]
    draw_table(ax, 0.5, 6.8,
               'PRZED: StudentAktywnosci (klucz: StID, Hobby, Umiejetnosc)',
               h_before, r_before, cw_before,
               highlight_cols={1, 2}, title_fontsize=10)
    
    # Arrows
    add_label(ax, 3.5, 6.3, 'StID  ->>  Hobby', fontsize=9, color='black')
    add_label(ax, 3.5, 6.0, 'StID  ->>  Umiejetnosc', fontsize=9, color='black')
    add_label(ax, 3.5, 5.6, 'NIEZALEZNE MVD w jednej tabeli', fontsize=9, color='black')
    add_label(ax, 3.5, 5.2, '= iloczyn kartezjanski = NARUSZENIE 4NF', fontsize=9, color='black')
    
    # After: two tables
    add_arrow(ax, 3.0, 4.2, 3.0, 3.7, '', '#333333')
    add_label(ax, 3.2, 3.95, 'dekompozycja', fontsize=8, color='#333333')
    
    h_hobby = ['StID*', 'Hobby*']
    r_hobby = [['1', 'Szachy'], ['1', 'Bieganie'], ['2', 'Plywanie']]
    cw_hobby = [0.55, 0.9]
    draw_table(ax, 0.5, 3.5,
               'PO: StudentHobby',
               h_hobby, r_hobby, cw_hobby, title_fontsize=10)
    
    h_skill = ['StID*', 'Umiejetnosc*']
    r_skill = [['1', 'Python'], ['1', 'SQL'], ['2', 'Java']]
    cw_skill = [0.55, 1.0]
    draw_table(ax, 3.5, 3.5,
               'PO: StudentUmiejetnosc',
               h_skill, r_skill, cw_skill, title_fontsize=10)
    
    # Summary on the right side
    add_label(ax, 6.5, 6.5, '4NF: BCNF + brak nietrywialnych MVD', fontsize=10)
    add_label(ax, 6.5, 6.1,
              'MVD X ->> Y: jeden X = ZBIOR Y-ow,', fontsize=8, color='#333333')
    add_label(ax, 6.5, 5.8,
              'niezaleznie od reszty kolumn.', fontsize=8, color='#333333')
    add_label(ax, 6.5, 5.35,
              'Naruszenie: Student 1 ma 2 hobby i 2 umiejetnosci', fontsize=8)
    add_label(ax, 6.5, 5.05,
              '  -> 2 x 2 = 4 wiersze (iloczyn kartezjanski!)', fontsize=8)
    add_label(ax, 6.5, 4.65,
              'Naprawa: rozdziel niezalezne MVD do osobnych tabel.', fontsize=8)
    add_label(ax, 6.5, 4.25,
              'Po dekompozycji: 3 + 3 = 6 wierszy zamiast 5 z ilocz.', fontsize=8,
              color='#333333')
    add_label(ax, 6.5, 3.85,
              '  (ale BEZ sztucznych kombinacji!)', fontsize=8, color='#333333')
    
    # Key insight box
    rect = mpatches.FancyBboxPatch(
        (6.3, 2.5), 5.0, 1.0,
        boxstyle="round,pad=0.1", facecolor='#F0F0F0',
        edgecolor='black', linewidth=1.0)
    ax.add_patch(rect)
    add_label(ax, 6.5, 3.2,
              'ROZNICA 4NF vs BCNF:', fontsize=9)
    add_label(ax, 6.5, 2.85,
              'BCNF dotyczy FD (X -> Y, jedna wartosc)', fontsize=8, color='#333333')
    add_label(ax, 6.5, 2.55,
              '4NF dotyczy MVD (X ->> Y, zbior wartosci)', fontsize=8, color='#333333')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_4nf_example.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_4nf_example.png")


# ============================================================
# DIAGRAM 7: 5NF example — join dependencies
# ============================================================
def draw_5nf():
    fig, ax = create_figure(11.69, 8.5)
    
    # Before: ternary table
    h_before = ['Dostawca*', 'Czesc*', 'Projekt*']
    r_before = [
        ['Alfa', 'Sruba', 'Most'],
        ['Alfa', 'Sruba', 'Wiezowiec'],
        ['Alfa', 'Nakretka', 'Most'],
        ['Beta', 'Sruba', 'Wiezowiec'],
        ['Beta', 'Nakretka', 'Wiezowiec'],
    ]
    cw_before = [0.9, 0.9, 1.0]
    draw_table(ax, 0.5, 7.8,
               'PRZED: Dostawy (klucz: Dostawca, Czesc, Projekt)',
               h_before, r_before, cw_before, title_fontsize=10)
    
    add_label(ax, 3.8, 7.3, 'Tabela w 4NF (brak nietrywialnych MVD),', fontsize=8)
    add_label(ax, 3.8, 7.0, 'ale NIE w 5NF jesli zachodzi regula cykliczna:', fontsize=8)
    add_label(ax, 3.8, 6.55,
              'Jesli Dostawca dostarcza Czesc', fontsize=8, color='#333333')
    add_label(ax, 3.8, 6.25,
              '  I Dostawca dostarcza do Projektu', fontsize=8, color='#333333')
    add_label(ax, 3.8, 5.95,
              '  I Czesc jest uzywana w Projekcie', fontsize=8, color='#333333')
    add_label(ax, 3.8, 5.65,
              '  ==> Dostawca dostarcza te Czesc do tego Projektu.', fontsize=8,
              color='black')
    
    # Arrow down
    add_arrow(ax, 1.8, 5.1, 1.8, 4.6, 'dekompozycja 5NF', '#333333')
    
    # After: three binary tables
    h1 = ['Dostawca*', 'Czesc*']
    r1 = [['Alfa', 'Sruba'], ['Alfa', 'Nakretka'], ['Beta', 'Sruba'], ['Beta', 'Nakretka']]
    cw1 = [0.9, 0.9]
    draw_table(ax, 0.3, 4.3, 'DostawcaCzesc',
               h1, r1, cw1, title_fontsize=9)
    
    h2 = ['Dostawca*', 'Projekt*']
    r2 = [['Alfa', 'Most'], ['Alfa', 'Wiezowiec'], ['Beta', 'Wiezowiec']]
    cw2 = [0.9, 1.0]
    draw_table(ax, 3.0, 4.3, 'DostawcaProjekt',
               h2, r2, cw2, title_fontsize=9)
    
    h3 = ['Czesc*', 'Projekt*']
    r3 = [['Sruba', 'Most'], ['Sruba', 'Wiezowiec'],
          ['Nakretka', 'Most'], ['Nakretka', 'Wiezowiec']]
    cw3 = [0.9, 1.0]
    draw_table(ax, 5.7, 4.3, 'CzescProjekt',
               h3, r3, cw3, title_fontsize=9)
    
    # Join reconstruction note
    rect = mpatches.FancyBboxPatch(
        (8.3, 3.5), 3.0, 4.0,
        boxstyle="round,pad=0.1", facecolor='#F0F0F0',
        edgecolor='black', linewidth=1.0)
    ax.add_patch(rect)
    
    add_label(ax, 8.5, 7.2, '5NF (PJNF):', fontsize=10)
    add_label(ax, 8.5, 6.8, 'Project-Join NF', fontsize=8, color='#333333')
    add_label(ax, 8.5, 6.35, 'Kazda zaleznosc', fontsize=8)
    add_label(ax, 8.5, 6.05, 'zlaczenia (JD)', fontsize=8)
    add_label(ax, 8.5, 5.75, 'implikowana przez', fontsize=8)
    add_label(ax, 8.5, 5.45, 'klucze kandydujace.', fontsize=8)
    add_label(ax, 8.5, 4.9, 'Rekonstrukcja:', fontsize=9)
    add_label(ax, 8.5, 4.55, 'DC JOIN DP JOIN CP', fontsize=8, color='#333333')
    add_label(ax, 8.5, 4.2, '= oryginalna tabela', fontsize=8, color='#333333')
    add_label(ax, 8.5, 3.75, '(bezstratnie!)', fontsize=8, color='#333333')
    
    # Verification example at the bottom
    add_label(ax, 0.3, 2.0,
              'Weryfikacja: Alfa dostarcza Nakretke? Alfa -> Wiezowiec? Nakretka -> Wiezowiec?',
              fontsize=8)
    add_label(ax, 0.3, 1.65,
              '  TAK, TAK, TAK --> wg reguly cyklicznej: Alfa dostarcza Nakretke do Wiezowca.',
              fontsize=8, color='#333333')
    add_label(ax, 0.3, 1.25,
              'Ale: Alfa dostarcza Nakretke? TAK. Alfa -> Most? TAK. Nakretka -> Most? TAK.',
              fontsize=8)
    add_label(ax, 0.3, 0.9,
              '  --> Alfa dostarcza Nakretke do Mostu. (Tego wiersza NIE MA w oryginale -- BLAD!)',
              fontsize=8, color='black')
    add_label(ax, 0.3, 0.5,
              '  Dekompozycja 5NF jest poprawna TYLKO jesli regula cykliczna rzeczywiscie zachodzi!',
              fontsize=8, color='black')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_5nf_example.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_5nf_example.png")


# ============================================================
# DIAGRAM 8: Full normalization summary flowchart
# ============================================================
def draw_summary_flow():
    fig, ax = create_figure(11.69, 6.0)
    
    # Boxes for each NF
    box_y = 4.5
    box_h = 1.8
    box_w = 1.4
    gap = 0.25
    
    nf_data = [
        ('0NF', 'Nienormalna', 'Listy w\nkomorkach,\nbrak klucza'),
        ('1NF', 'Atomowosc', 'Kazda komorka\n= 1 wartosc,\njest klucz'),
        ('2NF', 'Pelny klucz', 'Brak czesciowej\nzaleznosci od\nklucza zlozonego'),
        ('3NF', 'Tylko klucz', 'Brak zaleznosci\nprzechodniej\nA->B->C'),
        ('BCNF', 'Nadklucz', 'Lewa strona\nkazdej FD\n= nadklucz'),
        ('4NF', 'Brak MVD', 'Brak nietryw.\nwielowart.\nzaleznosci'),
        ('5NF', 'Brak JD', 'Kazda zal.\nzlaczenia\nimpl. kluczem'),
    ]
    
    for i, (name, subtitle, desc) in enumerate(nf_data):
        x = 0.3 + i * (box_w + gap)
        
        # Main box
        rect = mpatches.FancyBboxPatch(
            (x, box_y - box_h), box_w, box_h,
            boxstyle="round,pad=0.05",
            facecolor='#F5F5F5' if i == 0 else '#FFFFFF',
            edgecolor='black', linewidth=1.2)
        ax.add_patch(rect)
        
        # NF name
        ax.text(x + box_w / 2, box_y - 0.15, name,
                fontsize=12, fontweight='bold', ha='center', va='top',
                family='monospace')
        
        # Subtitle
        ax.text(x + box_w / 2, box_y - 0.45, subtitle,
                fontsize=7, ha='center', va='top',
                family='monospace', color='#333333')
        
        # Description
        ax.text(x + box_w / 2, box_y - 0.75, desc,
                fontsize=6.5, ha='center', va='top',
                family='monospace', color='#555555',
                linespacing=1.3)
        
        # Arrow to next
        if i < len(nf_data) - 1:
            ax.annotate('', xy=(x + box_w + 0.02, box_y - box_h / 2),
                        xytext=(x + box_w + gap - 0.02, box_y - box_h / 2),
                        arrowprops=dict(arrowstyle='<-', color='black', lw=1.5))
    
    # Bottom: mnemonic
    ax.text(5.85, 2.2,
            '\"Klucz, caly klucz i tylko klucz -- tak mi dopomoz Codd\"',
            fontsize=11, ha='center', va='center', family='monospace',
            style='italic')
    ax.text(5.85, 1.8,
            '1NF: klucz istnieje  |  2NF: caly klucz  |  3NF: tylko klucz',
            fontsize=9, ha='center', va='center', family='monospace',
            color='#333333')
    ax.text(5.85, 1.4,
            'BCNF: kazdy determinant = nadklucz  |  4NF: +brak MVD  |  5NF: +brak JD',
            fontsize=9, ha='center', va='center', family='monospace',
            color='#333333')
    
    # Hierarchy
    ax.text(5.85, 0.8,
            '5NF  (zawiera sie w)  4NF  (zaw.)  BCNF  (zaw.)  3NF  (zaw.)  2NF  (zaw.)  1NF',
            fontsize=8, ha='center', va='center', family='monospace',
            color='#555555')
    
    fig.savefig(os.path.join(OUTPUT_DIR, 'nf_summary_flow.png'),
                bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print("Generated: nf_summary_flow.png")


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating normalization diagrams...")
    draw_0nf()
    draw_1nf()
    draw_2nf()
    draw_3nf()
    draw_bcnf()
    draw_4nf()
    draw_5nf()
    draw_summary_flow()
    print("\nDone! All diagrams saved to:", OUTPUT_DIR)
