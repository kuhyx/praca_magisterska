#!/usr/bin/env python3
"""
Generate 4 process modeling diagrams (BPMN, UML Activity, EPC, Flowchart)
all representing the same process: "Obsluga reklamacji" (Complaint Handling).
Output: A4-compatible, black & white, laser-printer-friendly PNG files.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.path import Path
import os

# --- Common settings ---
DPI = 300
BG_COLOR = 'white'
LINE_COLOR = 'black'
FONT_SIZE = 9
TITLE_SIZE = 14
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=LINE_COLOR, lw=1.3))


def draw_line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=LINE_COLOR, lw=1.3, solid_capstyle='round')


def draw_rounded_rect(ax, x, y, w, h, text, fill='white', lw=1.5, fontsize=FONT_SIZE):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle="round,pad=0.3", linewidth=lw,
                          edgecolor=LINE_COLOR, facecolor=fill)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)


def draw_diamond(ax, x, y, size, text="", fill='white', fontsize=8):
    s = size
    diamond = Polygon([(x, y+s), (x+s, y), (x, y-s), (x-s, y)],
                      closed=True, linewidth=1.5,
                      edgecolor=LINE_COLOR, facecolor=fill)
    ax.add_patch(diamond)
    if text:
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
                fontweight='bold')


# =========================================================================
# 1. BPMN 2.0 Diagram
# =========================================================================
def generate_bpmn():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 75)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_title("BPMN 2.0 \u2014 Obs\u0142uga reklamacji", fontsize=TITLE_SIZE,
                 fontweight='bold', pad=12)

    # --- Pool outline ---
    pool_x, pool_y, pool_w, pool_h = 3, 3, 104, 68
    ax.add_patch(plt.Rectangle((pool_x, pool_y), pool_w, pool_h,
                               lw=2, edgecolor=LINE_COLOR, facecolor='white'))

    # Pool label
    label_strip = pool_x + 4
    ax.plot([label_strip, label_strip], [pool_y, pool_y + pool_h],
            color=LINE_COLOR, lw=1.5)
    ax.text(pool_x + 2, pool_y + pool_h/2, "FIRMA",
            fontsize=11, fontweight='bold', rotation=90, ha='center', va='center')

    # --- Lanes ---
    lane_top = pool_y + pool_h
    lane_mid1 = pool_y + pool_h * 2/3
    lane_mid2 = pool_y + pool_h * 1/3

    ax.plot([label_strip, pool_x + pool_w], [lane_mid1, lane_mid1],
            color=LINE_COLOR, lw=1)
    ax.plot([label_strip, pool_x + pool_w], [lane_mid2, lane_mid2],
            color=LINE_COLOR, lw=1)

    y_bok = (lane_top + lane_mid1) / 2
    y_jak = (lane_mid1 + lane_mid2) / 2
    y_mag = (lane_mid2 + pool_y) / 2

    ax.text(label_strip + 2.5, y_bok, "BOK", fontsize=8, ha='center', va='center',
            rotation=90, fontstyle='italic')
    ax.text(label_strip + 2.5, y_jak, "Jako\u015b\u0107", fontsize=8, ha='center',
            va='center', rotation=90, fontstyle='italic')
    ax.text(label_strip + 2.5, y_mag, "Magazyn", fontsize=8, ha='center', va='center',
            rotation=90, fontstyle='italic')

    content_left = label_strip + 5

    # --- Elements ---
    # Start event
    sx = content_left + 4
    ax.add_patch(plt.Circle((sx, y_bok), 2, lw=2, edgecolor=LINE_COLOR, facecolor='white'))
    ax.text(sx, y_bok - 3.5, "Reklamacja\nwp\u0142ywa", fontsize=6, ha='center')

    # Task 1: Przyjmij zg\u0142oszenie (BOK)
    t1x = sx + 14
    draw_rounded_rect(ax, t1x, y_bok, 14, 6, "Przyjmij\nzg\u0142oszenie")
    draw_arrow(ax, sx + 2, y_bok, t1x - 7, y_bok)

    # Task 2: Zweryfikuj zasadno\u015b\u0107 (Jako\u015b\u0107) \u2014 elbow routing
    t2x = t1x + 18
    draw_rounded_rect(ax, t2x, y_jak, 14, 6, "Zweryfikuj\nzasadno\u015b\u0107")
    elbow_x = t1x + 10
    draw_line(ax, t1x + 7, y_bok, elbow_x, y_bok)
    draw_line(ax, elbow_x, y_bok, elbow_x, y_jak)
    draw_arrow(ax, elbow_x, y_jak, t2x - 7, y_jak)

    # XOR Gateway (split)
    gx = t2x + 14
    draw_diamond(ax, gx, y_jak, 3.5, "X")
    draw_arrow(ax, t2x + 7, y_jak, gx - 3.5, y_jak)

    # YES: down to Magazyn
    t3x = gx + 14
    draw_rounded_rect(ax, t3x, y_mag, 14, 6, "Przygotuj\nwymian\u0119/zwrot")
    draw_line(ax, gx, y_jak - 3.5, gx, y_mag)
    draw_arrow(ax, gx, y_mag, t3x - 7, y_mag)
    ax.text(gx + 1.5, y_jak - 6, "Tak", fontsize=7, ha='left')

    # NO: right in Jako\u015b\u0107
    t4x = gx + 14
    draw_rounded_rect(ax, t4x, y_jak, 14, 6, "Odrzu\u0107\nreklamacj\u0119")
    draw_arrow(ax, gx + 3.5, y_jak, t4x - 7, y_jak)
    ax.text(gx + 4, y_jak + 2, "Nie", fontsize=7, ha='left')

    # XOR merge (in BOK)
    mx = t4x + 14
    draw_diamond(ax, mx, y_bok, 3.5, "X")
    # From Odrzu\u0107 up to merge
    draw_line(ax, t4x + 7, y_jak, mx, y_jak)
    draw_arrow(ax, mx, y_jak, mx, y_bok - 3.5)
    # From Przygotuj wymian\u0119 up to merge (offset to avoid overlap)
    draw_line(ax, t3x + 7, y_mag, mx - 4, y_mag)
    draw_line(ax, mx - 4, y_mag, mx - 4, y_bok)
    draw_arrow(ax, mx - 4, y_bok, mx - 3.5, y_bok)

    # Task 5: Powiadom klienta (BOK)
    t5x = mx + 13
    draw_rounded_rect(ax, t5x, y_bok, 14, 6, "Powiadom\nklienta")
    draw_arrow(ax, mx + 3.5, y_bok, t5x - 7, y_bok)

    # End event
    ex = t5x + 12
    ax.add_patch(plt.Circle((ex, y_bok), 2, lw=3, edgecolor=LINE_COLOR, facecolor='white'))
    draw_arrow(ax, t5x + 7, y_bok, ex - 2, y_bok)
    ax.text(ex, y_bok - 3.5, "Koniec", fontsize=6, ha='center')

    # --- Legend ---
    ly = 1
    ax.text(12, ly, "Legenda:", fontsize=7, fontweight='bold', va='center')
    ax.add_patch(plt.Circle((22, ly), 1, lw=2, edgecolor=LINE_COLOR, facecolor='white'))
    ax.text(24, ly, "Start", fontsize=6, va='center')
    ax.add_patch(plt.Circle((30, ly), 1, lw=3, edgecolor=LINE_COLOR, facecolor='white'))
    ax.text(32, ly, "Koniec", fontsize=6, va='center')
    draw_diamond(ax, 40, ly, 1.5, "X", fontsize=5)
    ax.text(43, ly, "Bramka XOR", fontsize=6, va='center')
    draw_rounded_rect(ax, 58, ly, 7, 2.5, "Zadanie", fontsize=6)
    ax.text(65, ly, "Sequence Flow \u2192", fontsize=6, va='center')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'bpmn_reklamacja.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK BPMN saved")


# =========================================================================
# 2. UML Activity Diagram
# =========================================================================
def generate_uml_activity():
    fig, ax = plt.subplots(figsize=(8.27, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_title("UML Activity Diagram \u2014 Obs\u0142uga reklamacji",
                 fontsize=TITLE_SIZE, fontweight='bold', pad=12)

    cx = 50
    y = 93
    step = 11

    # Initial node
    ax.add_patch(plt.Circle((cx, y), 1.8, facecolor='black', edgecolor='black'))

    # Action 1
    y -= step
    draw_rounded_rect(ax, cx, y, 28, 6, "Przyjmij zg\u0142oszenie reklamacji")
    draw_arrow(ax, cx, y + step - 1.8, cx, y + 3)

    # Action 2
    y -= step
    draw_rounded_rect(ax, cx, y, 28, 6, "Zweryfikuj zasadno\u015b\u0107")
    draw_arrow(ax, cx, y + step - 3, cx, y + 3)

    # Decision
    y -= step
    draw_diamond(ax, cx, y, 4)
    draw_arrow(ax, cx, y + step - 3, cx, y + 4)
    ax.text(cx + 6, y + 5, "[zasadna?]", fontsize=8, fontstyle='italic')

    dec_y = y
    branch_y = dec_y - step

    # Left [tak]
    left_x = cx - 24
    draw_rounded_rect(ax, left_x, branch_y, 22, 6, "Przygotuj\nwymian\u0119/zwrot")
    draw_line(ax, cx - 4, dec_y, left_x, dec_y)
    draw_arrow(ax, left_x, dec_y, left_x, branch_y + 3)
    ax.text(left_x + 2, dec_y + 1.5, "[tak]", fontsize=8, fontstyle='italic')

    # Right [nie]
    right_x = cx + 24
    draw_rounded_rect(ax, right_x, branch_y, 22, 6, "Odrzu\u0107\nreklamacj\u0119")
    draw_line(ax, cx + 4, dec_y, right_x, dec_y)
    draw_arrow(ax, right_x, dec_y, right_x, branch_y + 3)
    ax.text(right_x - 12, dec_y + 1.5, "[nie]", fontsize=8, fontstyle='italic')

    # Merge
    merge_y = branch_y - step
    draw_diamond(ax, cx, merge_y, 4)
    draw_line(ax, left_x, branch_y - 3, left_x, merge_y)
    draw_line(ax, left_x, merge_y, cx - 4, merge_y)
    draw_line(ax, right_x, branch_y - 3, right_x, merge_y)
    draw_line(ax, right_x, merge_y, cx + 4, merge_y)

    # Action: Powiadom
    y = merge_y - step
    draw_rounded_rect(ax, cx, y, 28, 6, "Powiadom klienta")
    draw_arrow(ax, cx, merge_y - 4, cx, y + 3)

    # Final node
    ey = y - step
    ax.add_patch(plt.Circle((cx, ey), 2.5, lw=2, facecolor='white', edgecolor='black'))
    ax.add_patch(plt.Circle((cx, ey), 1.5, facecolor='black', edgecolor='black'))
    draw_arrow(ax, cx, y - 3, cx, ey + 2.5)

    # Legend
    ly = 5
    ax.add_patch(plt.Circle((12, ly), 1.2, facecolor='black', edgecolor='black'))
    ax.text(15, ly, "= Pocz\u0105tek", fontsize=7, va='center')
    ax.add_patch(plt.Circle((32, ly), 1.3, lw=2, facecolor='white', edgecolor='black'))
    ax.add_patch(plt.Circle((32, ly), 0.8, facecolor='black', edgecolor='black'))
    ax.text(35, ly, "= Koniec", fontsize=7, va='center')
    draw_diamond(ax, 50, ly, 1.5)
    ax.text(53, ly, "= Decyzja/Merge", fontsize=7, va='center')
    draw_rounded_rect(ax, 78, ly, 9, 3, "Akcja", fontsize=7)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'uml_activity_reklamacja.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK UML Activity saved")


# =========================================================================
# 3. EPC (Event-driven Process Chain)
# =========================================================================
def generate_epc():
    fig, ax = plt.subplots(figsize=(8.27, 11))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_title("EPC (Event-driven Process Chain) \u2014 Obs\u0142uga reklamacji",
                 fontsize=TITLE_SIZE, fontweight='bold', pad=12)

    cx = 50
    y = 114
    step = 9.5

    def draw_epc_event(x, y, text):
        w, h = 26, 5.5
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=0.5", lw=1.5,
                              edgecolor=LINE_COLOR, facecolor='#D8D8D8')
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)

    def draw_epc_function(x, y, text):
        w, h = 26, 5.5
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=0.3", lw=2,
                              edgecolor=LINE_COLOR, facecolor='white')
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8,
                fontweight='bold')

    def draw_epc_connector(x, y, text):
        c = plt.Circle((x, y), 2.8, lw=1.5, edgecolor=LINE_COLOR, facecolor='white')
        ax.add_patch(c)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')

    # E1
    draw_epc_event(cx, y, "Reklamacja wp\u0142yn\u0119\u0142a")

    # F1
    y -= step
    draw_epc_function(cx, y, "Przyjmij zg\u0142oszenie")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)

    # E2
    y -= step
    draw_epc_event(cx, y, "Zg\u0142oszenie przyj\u0119te")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)

    # F2
    y -= step
    draw_epc_function(cx, y, "Zweryfikuj zasadno\u015b\u0107")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)

    # E3
    y -= step
    draw_epc_event(cx, y, "Zasadno\u015b\u0107 oceniona")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)

    # XOR split
    y -= step
    draw_epc_connector(cx, y, "XOR")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)
    split_y = y

    left_x = cx - 28
    right_x = cx + 28

    # Left branch
    by = split_y - step
    draw_epc_event(left_x, by, "Reklamacja zasadna")
    draw_line(ax, cx - 2.8, split_y, left_x, split_y)
    draw_arrow(ax, left_x, split_y, left_x, by + 2.8)

    by2 = by - step
    draw_epc_function(left_x, by2, "Przygotuj wymian\u0119/zwrot")
    draw_arrow(ax, left_x, by - 2.8, left_x, by2 + 2.8)

    by3 = by2 - step
    draw_epc_event(left_x, by3, "Wymiana przygotowana")
    draw_arrow(ax, left_x, by2 - 2.8, left_x, by3 + 2.8)

    # Right branch
    draw_epc_event(right_x, by, "Reklamacja niezasadna")
    draw_line(ax, cx + 2.8, split_y, right_x, split_y)
    draw_arrow(ax, right_x, split_y, right_x, by + 2.8)

    draw_epc_function(right_x, by2, "Odrzu\u0107 reklamacj\u0119")
    draw_arrow(ax, right_x, by - 2.8, right_x, by2 + 2.8)

    draw_epc_event(right_x, by3, "Reklamacja odrzucona")
    draw_arrow(ax, right_x, by2 - 2.8, right_x, by3 + 2.8)

    # XOR merge
    merge_y = by3 - step
    draw_epc_connector(cx, merge_y, "XOR")
    draw_line(ax, left_x, by3 - 2.8, left_x, merge_y)
    draw_line(ax, left_x, merge_y, cx - 2.8, merge_y)
    draw_line(ax, right_x, by3 - 2.8, right_x, merge_y)
    draw_line(ax, right_x, merge_y, cx + 2.8, merge_y)

    # F: Powiadom
    y = merge_y - step
    draw_epc_function(cx, y, "Powiadom klienta")
    draw_arrow(ax, cx, merge_y - 2.8, cx, y + 2.8)

    # E: Klient powiadomiony
    y -= step
    draw_epc_event(cx, y, "Klient powiadomiony")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)

    # Legend
    ly = 3
    draw_epc_event(16, ly, "Zdarzenie")
    draw_epc_function(46, ly, "Funkcja")
    draw_epc_connector(68, ly, "XOR")
    ax.text(72, ly, "= \u0141\u0105cznik logiczny", fontsize=7, va='center')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'epc_reklamacja.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK EPC saved")


# =========================================================================
# 4. Classic Flowchart
# =========================================================================
def generate_flowchart():
    fig, ax = plt.subplots(figsize=(8.27, 11))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 110)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_title("Schemat blokowy (Flowchart) \u2014 Obs\u0142uga reklamacji",
                 fontsize=TITLE_SIZE, fontweight='bold', pad=12)

    cx = 50
    y = 103
    step = 11

    def draw_terminal(x, y, text):
        w, h = 20, 5.5
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=1.0", lw=2,
                              edgecolor=LINE_COLOR, facecolor='#E0E0E0')
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=FONT_SIZE,
                fontweight='bold')

    def draw_process_box(x, y, text):
        w, h = 26, 6
        rect = plt.Rectangle((x - w/2, y - h/2), w, h,
                              lw=1.5, edgecolor=LINE_COLOR, facecolor='white')
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=FONT_SIZE)

    def draw_io_shape(x, y, text):
        w, h = 26, 5.5
        skew = 3
        verts = [(x - w/2 + skew, y + h/2),
                 (x + w/2 + skew, y + h/2),
                 (x + w/2 - skew, y - h/2),
                 (x - w/2 - skew, y - h/2),
                 (x - w/2 + skew, y + h/2)]
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        patch = mpatches.PathPatch(Path(verts, codes),
                                   facecolor='white', edgecolor=LINE_COLOR, lw=1.5)
        ax.add_patch(patch)
        ax.text(x, y, text, ha='center', va='center', fontsize=FONT_SIZE)

    # Start
    draw_terminal(cx, y, "START")

    # I/O
    y -= step
    draw_io_shape(cx, y, "Reklamacja od klienta")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)

    # Process
    y -= step
    draw_process_box(cx, y, "Przyjmij zg\u0142oszenie")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 3)

    # Process
    y -= step
    draw_process_box(cx, y, "Zweryfikuj zasadno\u015b\u0107")
    draw_arrow(ax, cx, y + step - 3, cx, y + 3)

    # Decision
    y -= step
    draw_diamond(ax, cx, y, 4.5, "Zasadna?")
    draw_arrow(ax, cx, y + step - 3, cx, y + 4.5)
    dec_y = y

    # Left: Tak
    left_x = cx - 26
    draw_process_box(left_x, dec_y, "Przygotuj wymian\u0119/zwrot")
    draw_line(ax, cx - 4.5, dec_y, left_x + 13, dec_y)
    ax.text(cx - 7, dec_y + 2, "Tak", fontsize=8, ha='center', fontweight='bold')

    # Right: Nie
    right_x = cx + 26
    draw_process_box(right_x, dec_y, "Odrzu\u0107 reklamacj\u0119")
    draw_line(ax, cx + 4.5, dec_y, right_x - 13, dec_y)
    ax.text(cx + 7, dec_y + 2, "Nie", fontsize=8, ha='center', fontweight='bold')

    # Merge
    merge_y = dec_y - step
    draw_line(ax, left_x, dec_y - 3, left_x, merge_y)
    draw_line(ax, right_x, dec_y - 3, right_x, merge_y)
    draw_line(ax, left_x, merge_y, right_x, merge_y)
    ax.plot(cx, merge_y, 'ko', markersize=4)

    # Process: Powiadom
    y = merge_y - step + 3
    draw_process_box(cx, y, "Powiadom klienta")
    draw_arrow(ax, cx, merge_y, cx, y + 3)

    # I/O
    y -= step
    draw_io_shape(cx, y, "Odpowied\u017a do klienta")
    draw_arrow(ax, cx, y + step - 3, cx, y + 2.8)

    # End
    y -= step
    draw_terminal(cx, y, "KONIEC")
    draw_arrow(ax, cx, y + step - 2.8, cx, y + 2.8)

    # Legend
    ly = 4
    ax.text(5, ly, "Legenda:", fontsize=7, fontweight='bold', va='center')
    draw_terminal(18, ly, "")
    ax.text(18, ly, "Start/\nKoniec", fontsize=5.5, ha='center', va='center')
    w, h = 9, 3
    ax.add_patch(plt.Rectangle((32 - w/2, ly - h/2), w, h,
                               lw=1.5, edgecolor=LINE_COLOR, facecolor='white'))
    ax.text(32, ly, "Proces", fontsize=6, ha='center', va='center')
    draw_diamond(ax, 46, ly, 2)
    ax.text(49.5, ly, "= Decyzja", fontsize=6, va='center')
    skew = 1.5
    w2, h2 = 9, 3
    verts = [(62 - w2/2 + skew, ly + h2/2), (62 + w2/2 + skew, ly + h2/2),
             (62 + w2/2 - skew, ly - h2/2), (62 - w2/2 - skew, ly - h2/2),
             (62 - w2/2 + skew, ly + h2/2)]
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    ax.add_patch(mpatches.PathPatch(Path(verts, codes),
                                     facecolor='white', edgecolor=LINE_COLOR, lw=1.2))
    ax.text(62, ly, "We/Wy", fontsize=6, ha='center', va='center')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'flowchart_reklamacja.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK Flowchart saved")


# =========================================================================
if __name__ == '__main__':
    print(f"Generating diagrams to {OUTPUT_DIR}/...")
    generate_bpmn()
    generate_uml_activity()
    generate_epc()
    generate_flowchart()
    print(f"\nAll 4 diagrams saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
            print(f"  {f} ({size_kb:.0f} KB)")
