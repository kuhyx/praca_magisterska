#!/usr/bin/env python3
"""
Generate pattern cataloguing diagrams for PYTANIE 14 (AIS):
  1. Pattern Template Structure — the standard fields every pattern has
  2. Catalog Classification Map — catalogs arranged by scope & domain
  3. Pattern Language Network — how patterns reference each other

All: A4-compatible, B&W, 300 DPI, laser-printer-friendly.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

DPI = 300
BG = 'white'
LN = 'black'
FS = 9
FS_TITLE = 13
FS_SMALL = 7.5
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRAY1 = '#E8E8E8'
GRAY2 = '#D0D0D0'
GRAY3 = '#B8B8B8'
GRAY4 = '#F5F5F5'
GRAY5 = '#C0C0C0'


def draw_box(ax, x, y, w, h, text, fill='white', lw=1.2, fontsize=FS,
             fontweight='normal', ha='center', va='center', rounded=True):
    if rounded:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                              lw=lw, edgecolor=LN, facecolor=fill)
    else:
        rect = mpatches.Rectangle((x, y), w, h, lw=lw, edgecolor=LN, facecolor=fill)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha=ha, va=va, fontsize=fontsize,
            fontweight=fontweight, wrap=True)


def draw_arrow(ax, x1, y1, x2, y2, lw=1.2, style='->', color=LN):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))


# ============================================================
# 1. Pattern Template Structure (NaPSiRoKo mnemonic)
# ============================================================
def generate_pattern_template():
    fig, ax = plt.subplots(figsize=(8.27, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    ax.set_title('Szablon opisu wzorca \u2014 \u201eNaPSiRoKo\u201d',
                 fontsize=FS_TITLE, fontweight='bold', pad=15)

    # Main card outline
    card_x, card_y, card_w, card_h = 1.5, 0.5, 7, 7
    card = FancyBboxPatch((card_x, card_y), card_w, card_h,
                          boxstyle="round,pad=0.15", lw=2.5,
                          edgecolor=LN, facecolor=GRAY4)
    ax.add_patch(card)

    # Title of card
    ax.text(card_x + card_w / 2, card_y + card_h - 0.35,
            "KARTA WZORCA", ha='center', va='center',
            fontsize=FS_TITLE, fontweight='bold')

    # Fields as horizontal bands
    fields = [
        ("Na", "NAZWA", "Layered, Observer, Microservices", GRAY1),
        ("P",  "PROBLEM / KONTEKST", "Kiedy stosować? Jaki problem rozwiązuje?", 'white'),
        ("Si", "SIŁY (forces)", "Konkurencyjne wymagania do pogodzenia\n(np. testowalność vs wydajność)", GRAY1),
        ("Ro", "ROZWIĄZANIE", "Struktura, diagram, zachowanie", 'white'),
        ("Ko", "KONSEKWENCJE", "Tradeoffs: co zyskujemy, co tracimy", GRAY1),
    ]

    band_x = card_x + 0.3
    band_w = card_w - 0.6
    band_h = 1.05
    start_y = card_y + card_h - 1.1

    for i, (abbr, title, desc, fill) in enumerate(fields):
        by = start_y - i * (band_h + 0.15)

        # Abbreviation circle on the left
        circle = plt.Circle((band_x + 0.35, by + band_h / 2), 0.28,
                            lw=1.5, edgecolor=LN, facecolor=GRAY2)
        ax.add_patch(circle)
        ax.text(band_x + 0.35, by + band_h / 2, abbr, ha='center', va='center',
                fontsize=10, fontweight='bold')

        # Field box
        fx = band_x + 0.8
        fw = band_w - 0.8
        rect = FancyBboxPatch((fx, by), fw, band_h,
                              boxstyle="round,pad=0.06", lw=1,
                              edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(fx + 0.15, by + band_h - 0.25, title, ha='left', va='center',
                fontsize=FS, fontweight='bold')
        ax.text(fx + 0.15, by + 0.25, desc, ha='left', va='center',
                fontsize=FS_SMALL, fontstyle='italic', color='#444444')

        # Arrow connecting fields
        if i < len(fields) - 1:
            draw_arrow(ax, band_x + 0.35, by - 0.02,
                       band_x + 0.35, by - 0.13, lw=1.0)

    # Extra fields note at bottom
    ax.text(card_x + card_w / 2, card_y + 0.25,
            "+ Powiązane wzorce  •  Znane zastosowania  •  Warianty",
            ha='center', va='center', fontsize=FS_SMALL, fontstyle='italic')

    # Mnemonic reminder on the right
    ax.text(9.8, 4, "Mnemonik:\nNaPSiRoKo",
            ha='center', va='center', fontsize=10, fontweight='bold',
            rotation=90, color='#666666')

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'q14_pattern_template.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {out}")


# ============================================================
# 2. Catalog Classification Map
# ============================================================
def generate_catalog_map():
    fig, ax = plt.subplots(figsize=(8.27, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    ax.set_title('Mapa katalog\u00f3w wzorc\u00f3w \u2014 \u201ePawe\u0142 Gra\u0142 Efektownie Pod Chmurami\u201d',
                 fontsize=FS_TITLE, fontweight='bold', pad=15)

    # Y-axis: Scale (architectural → design → idiom)
    ax.text(0.3, 7.8, "SKALA", fontsize=10, fontweight='bold',
            ha='center', va='center', rotation=90)
    ax.annotate("", xy=(0.3, 2.0), xytext=(0.3, 7.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))

    scale_labels = [
        (7.0, "Architektoniczny\n(cały system)"),
        (5.0, "Projektowy\n(klasa/obiekt)"),
        (3.0, "Idiomatyczny\n(linia kodu)"),
    ]
    for sy, label in scale_labels:
        ax.text(1.0, sy, label, fontsize=FS_SMALL, ha='left', va='center',
                fontstyle='italic')
        ax.plot([0.15, 0.45], [sy, sy], color=GRAY3, lw=0.8, ls='--')

    # X-axis: Domain
    ax.text(6.5, 1.2, "DOMENA ZASTOSOWANIA", fontsize=10, fontweight='bold',
            ha='center', va='center')
    ax.annotate("", xy=(11.5, 1.5), xytext=(2.0, 1.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))

    # Catalog boxes positioned by scale × domain
    catalogs = [
        # (x, y, w, h, name, subtitle, fill, mnemonic_letter)
        (2.5, 6.2, 2.5, 1.4, "POSA", "1996 • Buschmann\nLayers, Broker,\nPipes & Filters, MVC", GRAY1, "P"),
        (2.5, 4.2, 2.5, 1.4, "GoF", "1994 • Gamma et al.\n23 wzorce:\n5 kreac. / 7 strukt. / 11 behaw.", GRAY2, "G"),
        (5.5, 6.2, 2.5, 1.4, "EIP", "2003 • Hohpe & Woolf\nMessage Channel,\nRouter, Aggregator", GRAY1, "E"),
        (5.5, 4.2, 2.5, 1.4, "PoEAA", "2002 • M. Fowler\nRepository, Unit of Work,\nDomain Model", 'white', "P"),
        (8.5, 6.2, 2.8, 1.4, "Cloud\nPatterns", "~2015 • Azure/AWS\nCircuit Breaker,\nSaga, Sidecar", GRAY1, "C"),
    ]

    for cx, cy, cw, ch, name, sub, fill, ml in catalogs:
        rect = FancyBboxPatch((cx, cy), cw, ch, boxstyle="round,pad=0.1",
                              lw=1.5, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(cx + cw / 2, cy + ch - 0.3, name, ha='center', va='center',
                fontsize=10, fontweight='bold')
        ax.text(cx + cw / 2, cy + 0.4, sub, ha='center', va='center',
                fontsize=FS_SMALL, linespacing=1.3)

        # Mnemonic letter in corner
        circle = plt.Circle((cx + 0.25, cy + ch - 0.25), 0.2,
                            lw=1, edgecolor=LN, facecolor=GRAY5)
        ax.add_patch(circle)
        ax.text(cx + 0.25, cy + ch - 0.25, ml, ha='center', va='center',
                fontsize=8, fontweight='bold')

    # Mnemonic bar at bottom
    mnem_y = 2.2
    ax.text(6.0, mnem_y, "PGEP+C → Paweł Grał Efektownie Pod Chmurami",
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=LN, lw=1.5))

    # Domain labels along x-axis
    domains = [
        (3.75, 1.7, "Architektura"),
        (6.75, 1.7, "Integracja / Enterprise"),
        (9.9, 1.7, "Chmura"),
    ]
    for dx, dy, dlabel in domains:
        ax.text(dx, dy, dlabel, ha='center', va='center',
                fontsize=FS_SMALL, fontstyle='italic')

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'q14_catalog_map.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {out}")


# ============================================================
# 3. Three Pillars of Cataloguing
# ============================================================
def generate_three_pillars():
    fig, ax = plt.subplots(figsize=(8.27, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    ax.set_title("Jak są katalogowane wzorce? — Trzy filary",
                 fontsize=FS_TITLE, fontweight='bold', pad=15)

    # Roof / banner
    roof_pts = np.array([[1, 5.5], [6, 6.8], [11, 5.5]])
    roof = plt.Polygon(roof_pts, closed=True, lw=2,
                       edgecolor=LN, facecolor=GRAY4)
    ax.add_patch(roof)
    ax.text(6, 6.0, "KATALOGOWANIE WZORCÓW",
            ha='center', va='center', fontsize=11, fontweight='bold')

    # Three pillars
    pillars = [
        (1.3, "1. SZABLON\nOPISU",
         "Każdy wzorzec ma\nte same pola:\nNazwa → Problem\n→ Siły → Rozwiązanie\n→ Konsekwencje",
         "Analogia:\nformatka\nencyklopedii"),
        (4.8, "2. KLASYFIKACJA\nWIELOOSIOWA",
         "Osie podziału:\n• Skala (arch/proj/idiom)\n• Domena problemu\n• Atrybut jakościowy\n• Domena zastosowania",
         "Analogia:\nkategorie\nw bibliotece"),
        (8.3, "3. JĘZYK\nWZORCÓW",
         "Wzorce referują się\nwzajemnie tworząc\nsieć/graf:\nA → wymaga → B\nB → wariant → C",
         "Analogia:\n\u201ezobacz te\u017c\u201d\nw encyklopedii"),
    ]

    for px, title, desc, analogy in pillars:
        pw, ph = 2.8, 5.0
        py = 0.5

        # Pillar rectangle
        rect = FancyBboxPatch((px, py), pw, ph, boxstyle="round,pad=0.1",
                              lw=1.8, edgecolor=LN, facecolor='white')
        ax.add_patch(rect)

        # Title
        ax.text(px + pw / 2, py + ph - 0.55, title, ha='center', va='center',
                fontsize=9, fontweight='bold')

        # Horizontal line under title
        ax.plot([px + 0.2, px + pw - 0.2], [py + ph - 1.0, py + ph - 1.0],
                color=LN, lw=0.8)

        # Description
        ax.text(px + pw / 2, py + ph / 2 - 0.3, desc, ha='center', va='center',
                fontsize=FS_SMALL, linespacing=1.4)

        # Analogy box at bottom
        analogy_rect = FancyBboxPatch((px + 0.2, py + 0.15), pw - 0.4, 1.0,
                                      boxstyle="round,pad=0.06", lw=0.8,
                                      edgecolor=GRAY3, facecolor=GRAY1)
        ax.add_patch(analogy_rect)
        ax.text(px + pw / 2, py + 0.65, analogy, ha='center', va='center',
                fontsize=FS_SMALL, fontstyle='italic', color='#555555')

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'q14_three_pillars.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {out}")


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating PYTANIE 14 diagrams...")
    generate_pattern_template()
    generate_catalog_map()
    generate_three_pillars()
    print("Done!")
