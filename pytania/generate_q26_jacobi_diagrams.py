#!/usr/bin/env python3
"""
Generate diagrams explaining WHY parallel Jacobi needs ghost cells
and neighbor communication.
Output: A4-compatible, black & white, laser-printer-friendly PNG files.

Diagrams:
1. q26_jacobi_stencil.png    — 1D Jacobi stencil: x_new[i] depends on x[i-1] and x[i+1]
2. q26_domain_decomposition.png — domain split across processes, showing the boundary problem
3. q26_ghost_cell_exchange.png  — ghost cell exchange with Send/Recv
4. q26_deadlock_vs_solution.png — deadlock scenario vs Sendrecv solution
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# --- Common settings ---
DPI = 300
BG_COLOR = 'white'
LINE_COLOR = 'black'
FONT_SIZE = 10
TITLE_SIZE = 13
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

LIGHT_GRAY = '#D0D0D0'
MED_GRAY = '#A0A0A0'
DARK_GRAY = '#606060'
VERY_LIGHT = '#F0F0F0'
HIGHLIGHT = '#404040'


def draw_cell(ax, x, y, w, h, text, fill='white', edgecolor='black',
              lw=1.5, fontsize=FONT_SIZE, fontweight='normal', textcolor='black'):
    """Draw a rectangular cell with text."""
    rect = plt.Rectangle((x, y), w, h, lw=lw, edgecolor=edgecolor,
                          facecolor=fill, zorder=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight, color=textcolor, zorder=3)


def draw_arrow(ax, x1, y1, x2, y2, color='black', lw=1.5, style='->', zorder=4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw),
                zorder=zorder)


def draw_curvy_arrow(ax, x1, y1, x2, y2, color='black', lw=1.5,
                     connectionstyle="arc3,rad=0.3"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=connectionstyle),
                zorder=4)


# =========================================================================
# 1. JACOBI STENCIL — why x_new[i] needs neighbors
# =========================================================================
def generate_jacobi_stencil():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(-2.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_title("Szablon Jacobiego 1D — dlaczego potrzebujesz sąsiadów",
                 fontsize=TITLE_SIZE, fontweight='bold', pad=15)

    # Draw the 1D array: x[0], x[1], ..., x[7]
    cw = 1.0  # cell width
    ch = 0.8
    y_old = 2.5  # y for old array
    y_new = 0.0  # y for new array
    n = 8

    # Label rows
    ax.text(-0.4, y_old + ch/2, "Stara\niteracja:", ha='right', va='center',
            fontsize=FONT_SIZE, fontweight='bold')
    ax.text(-0.4, y_new + ch/2, "Nowa\niteracja:", ha='right', va='center',
            fontsize=FONT_SIZE, fontweight='bold')

    for i in range(n):
        x = i * cw
        # Old values row
        fill_old = LIGHT_GRAY if i in (2, 4) else 'white'
        if i == 3:
            fill_old = MED_GRAY
        draw_cell(ax, x, y_old, cw, ch, f"x[{i}]", fill=fill_old)

        # New values row
        fill_new = 'white'
        if i == 3:
            fill_new = DARK_GRAY
            draw_cell(ax, x, y_new, cw, ch, f"x'[{i}]", fill=fill_new,
                      textcolor='white', fontweight='bold')
        else:
            draw_cell(ax, x, y_new, cw, ch, f"x'[{i}]", fill=fill_new)

    # Arrows from x[2] and x[4] to x'[3]
    # x[2] → x'[3]
    draw_arrow(ax, 2*cw + cw/2, y_old, 3*cw + cw/2, y_new + ch, lw=2.5)
    # x[4] → x'[3]
    draw_arrow(ax, 4*cw + cw/2, y_old, 3*cw + cw/2, y_new + ch, lw=2.5)

    # Formula
    ax.text(4.0, -1.2,
            r"$x'[i] = \frac{1}{2}\,(x[i\!-\!1] + x[i\!+\!1])$",
            ha='center', va='center', fontsize=14,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=VERY_LIGHT,
                      edgecolor='black', lw=1.5))

    # Concrete example
    ax.text(4.0, -2.0,
            r"$x'[3] = \frac{1}{2}\,(x[2] + x[4])$"
            " — aby obliczyć nową wartość x'[3],\n"
            "potrzebujemy wartości lewego i prawego sąsiada.",
            ha='center', va='center', fontsize=9)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'q26_jacobi_stencil.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✓ {path}")


# =========================================================================
# 2. DOMAIN DECOMPOSITION — the boundary problem
# =========================================================================
def generate_domain_decomposition():
    fig, axes = plt.subplots(2, 1, figsize=(11, 7.5),
                             gridspec_kw={'height_ratios': [1, 1.5]})
    fig.patch.set_facecolor(BG_COLOR)
    fig.suptitle("Dekompozycja domeny — dlaczego proces potrzebuje danych od sąsiada",
                 fontsize=TITLE_SIZE, fontweight='bold', y=0.98)

    # ---------- TOP: Full domain (single process) ----------
    ax = axes[0]
    ax.set_xlim(-1, 13)
    ax.set_ylim(-1, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(-0.8, 1.4, "Jeden proces\n(cała domena):", ha='right', va='center',
            fontsize=9, fontweight='bold')

    cw, ch = 1.0, 0.8
    for i in range(12):
        draw_cell(ax, i, 1, cw, ch, f"x[{i}]", fontsize=8)

    ax.text(6, 0.2, "← Jeden proces ma WSZYSTKIE wartości → brak problemu",
            ha='center', fontsize=9, style='italic')

    # ---------- BOTTOM: Split across 3 processes ----------
    ax = axes[1]
    ax.set_xlim(-2.5, 14)
    ax.set_ylim(-3.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(6, 4.2, "Trzy procesy (domena podzielona):", ha='center',
            fontsize=11, fontweight='bold')

    # Process colors
    p_colors = [VERY_LIGHT, LIGHT_GRAY, '#E8E8E8']
    p_labels = ['Proces 0', 'Proces 1', 'Proces 2']
    p_ranges = [(0, 4), (4, 8), (8, 12)]

    y_proc = 2.5
    for pi, (start, end) in enumerate(p_ranges):
        # Background box for process
        bx = start * cw - 0.15
        bw = (end - start) * cw + 0.3
        bg = plt.Rectangle((bx, y_proc - 0.3), bw, ch + 0.6,
                            lw=2, edgecolor='black', facecolor=p_colors[pi],
                            linestyle='--', zorder=1)
        ax.add_patch(bg)
        ax.text(bx + bw/2, y_proc + ch + 0.55, p_labels[pi],
                ha='center', va='center', fontsize=9, fontweight='bold')

        for i in range(start, end):
            fill = 'white'
            fw = 'normal'
            # Highlight boundary cells
            if i == end - 1 and pi < 2:  # right boundary
                fill = MED_GRAY
                fw = 'bold'
            if i == start and pi > 0:  # left boundary
                fill = MED_GRAY
                fw = 'bold'
            draw_cell(ax, i * cw, y_proc, cw, ch, f"x[{i}]",
                      fill=fill, fontsize=8, fontweight=fw)

    # Show the PROBLEM: Process 0 computing x'[3]
    # x'[3] needs x[2] (has it) + x[4] (does NOT have it!)
    # Highlight the dependency
    y_explain = 0.3

    # Box showing calculation
    ax.text(2, y_explain + 0.6,
            "Proces 0 oblicza x'[3]:",
            ha='center', va='center', fontsize=10, fontweight='bold')

    ax.text(2, y_explain - 0.1,
            r"$x'[3] = \frac{1}{2}\,(x[2] + x[4])$",
            ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='black', lw=1.5))

    # Arrow from x[2] — "ma"
    draw_arrow(ax, 2.5, y_proc, 1.5, y_explain + 1.1, color='black', lw=1.5)
    ax.text(1.3, y_proc - 0.6, "MA ✓", ha='center', fontsize=9, fontweight='bold')

    # Arrow from x[4] — "NIE MA!"
    draw_arrow(ax, 4.5, y_proc, 3.0, y_explain + 1.1, color='black', lw=1.5)
    ax.text(4.5, y_proc - 0.6, "NIE MA ✗", ha='center', fontsize=9,
            fontweight='bold', color='black')

    # Explanation below
    ax.text(6, -1.2,
            "Problem: x[4] należy do Procesu 1, ale Proces 0 potrzebuje go\n"
            "do obliczenia x'[3]. → Proces 0 musi POPROSIĆ Proces 1 o wartość x[4].\n"
            "T\u0119 dodatkow\u0105 kopi\u0119 nazywamy \u201Ekom\u00F3rk\u0105-duchem\u201D (ghost cell).",
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=VERY_LIGHT,
                      edgecolor='black', lw=1))

    # Similarly for Process 1 needing x[3] from Process 0
    ax.text(6, -2.7,
            "Analogicznie: Proces 1 obliczając x'[4] potrzebuje x[3] od Procesu 0.\n"
            "→ Każda para sąsiadów musi wymienić po jednej wartości granicznej (w obie strony).",
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=VERY_LIGHT,
                      edgecolor='black', lw=1))

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    path = os.path.join(OUTPUT_DIR, 'q26_domain_decomposition.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✓ {path}")


# =========================================================================
# 3. GHOST CELL EXCHANGE — the communication pattern
# =========================================================================
def generate_ghost_cell_exchange():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(-2.5, 15)
    ax.set_ylim(-4.5, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_title("Wymiana komórek-duchów (ghost cell exchange) między procesami",
                 fontsize=TITLE_SIZE, fontweight='bold', pad=15)

    cw, ch = 1.0, 0.8

    # === BEFORE exchange ===
    y_before = 3.0
    ax.text(-2.0, y_before + ch/2, "PRZED\nwymianą:", ha='right', va='center',
            fontsize=9, fontweight='bold')

    # Process 0: x[0..3]
    for i in range(4):
        fill = MED_GRAY if i == 3 else 'white'
        draw_cell(ax, i * cw, y_before, cw, ch, f"x[{i}]", fill=fill, fontsize=8)
    # Empty ghost cell slot
    draw_cell(ax, 4 * cw, y_before, cw, ch, "?",
              fill=VERY_LIGHT, edgecolor=MED_GRAY,
              fontsize=10, fontweight='bold')
    ax.text(4.5, y_before + ch + 0.2, "ghost", ha='center', fontsize=7,
            style='italic', color=DARK_GRAY)

    # Gap
    ax.text(5.8, y_before + ch/2, "│", ha='center', fontsize=16, color=MED_GRAY)

    # Process 1: x[4..7]
    # Empty ghost cell slot
    draw_cell(ax, 6 * cw, y_before, cw, ch, "?",
              fill=VERY_LIGHT, edgecolor=MED_GRAY,
              fontsize=10, fontweight='bold')
    ax.text(6.5, y_before + ch + 0.2, "ghost", ha='center', fontsize=7,
            style='italic', color=DARK_GRAY)
    for i in range(4, 8):
        fill = MED_GRAY if i == 4 else 'white'
        draw_cell(ax, (i + 3) * cw, y_before, cw, ch, f"x[{i}]", fill=fill, fontsize=8)

    # Process labels
    ax.text(2, y_before - 0.5, "Proces 0", ha='center', fontsize=9, fontweight='bold')
    ax.text(9, y_before - 0.5, "Proces 1", ha='center', fontsize=9, fontweight='bold')

    # === ARROWS: the exchange ===
    y_mid = 1.3

    # x[3] → ghost of Process 1
    draw_curvy_arrow(ax, 3.5, y_before, 6.5, y_before,
                     connectionstyle="arc3,rad=-0.6", lw=2)
    ax.text(5, y_before + 1.8, "Send x[3]", ha='center', fontsize=9,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='black'))

    # x[4] → ghost of Process 0
    draw_curvy_arrow(ax, 7.5, y_before, 4.5, y_before,
                     connectionstyle="arc3,rad=-0.6", lw=2)
    ax.text(5, y_before - 1.5, "Send x[4]", ha='center', fontsize=9,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='black'))

    # === AFTER exchange ===
    y_after = -1.5
    ax.text(-2.0, y_after + ch/2, "PO\nwymianie:", ha='right', va='center',
            fontsize=9, fontweight='bold')

    # Process 0: x[0..3] + ghost x[4]
    for i in range(4):
        fill = MED_GRAY if i == 3 else 'white'
        draw_cell(ax, i * cw, y_after, cw, ch, f"x[{i}]", fill=fill, fontsize=8)
    draw_cell(ax, 4 * cw, y_after, cw, ch, "x[4]",
              fill=LIGHT_GRAY, edgecolor='black',
              fontsize=8, fontweight='bold')
    ax.text(4.5, y_after + ch + 0.2, "ghost ✓", ha='center', fontsize=7,
            style='italic', fontweight='bold')

    ax.text(5.8, y_after + ch/2, "│", ha='center', fontsize=16, color=MED_GRAY)

    # Process 1: ghost x[3] + x[4..7]
    draw_cell(ax, 6 * cw, y_after, cw, ch, "x[3]",
              fill=LIGHT_GRAY, edgecolor='black',
              fontsize=8, fontweight='bold')
    ax.text(6.5, y_after + ch + 0.2, "ghost ✓", ha='center', fontsize=7,
            style='italic', fontweight='bold')
    for i in range(4, 8):
        fill = MED_GRAY if i == 4 else 'white'
        draw_cell(ax, (i + 3) * cw, y_after, cw, ch, f"x[{i}]", fill=fill, fontsize=8)

    ax.text(2, y_after - 0.5, "Proces 0", ha='center', fontsize=9, fontweight='bold')
    ax.text(9, y_after - 0.5, "Proces 1", ha='center', fontsize=9, fontweight='bold')

    # Explanation
    ax.text(5.5, -3.5,
            "Teraz Proces 0 ma kopię x[4] (ghost cell) i może obliczyć x'[3] = ½(x[2] + x[4]).\n"
            "Proces 1 ma kopię x[3] (ghost cell) i może obliczyć x'[4] = ½(x[3] + x[5]).\n"
            "→ Ta wymiana musi się powtarzać W KAŻDEJ iteracji Jacobiego.",
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=VERY_LIGHT,
                      edgecolor='black', lw=1))

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'q26_ghost_cell_exchange.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✓ {path}")


# =========================================================================
# 4. DEADLOCK vs SOLUTION — side by side
# =========================================================================
def generate_deadlock_vs_solution():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    fig.patch.set_facecolor(BG_COLOR)
    fig.suptitle("Zakleszczenie (deadlock) vs rozwiązanie MPI_Sendrecv",
                 fontsize=TITLE_SIZE, fontweight='bold', y=0.98)

    # ---- LEFT: Deadlock ----
    ax = axes[0]
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("DEADLOCK — oba procesy w Ssend", fontsize=11, fontweight='bold')

    # Timeline
    # Proc 0 column at x=2, Proc 1 column at x=8
    px0, px1 = 2.5, 8.5
    y_top = 9.5
    y_bot = 1.0

    # Process headers
    draw_cell(ax, px0 - 1.2, y_top, 2.4, 0.8, "Proces 0",
              fill=LIGHT_GRAY, fontweight='bold', fontsize=10)
    draw_cell(ax, px1 - 1.2, y_top, 2.4, 0.8, "Proces 1",
              fill=LIGHT_GRAY, fontweight='bold', fontsize=10)

    # Timeline lines
    ax.plot([px0, px0], [y_top, y_bot], color='black', lw=2, zorder=1)
    ax.plot([px1, px1], [y_top, y_bot], color='black', lw=2, zorder=1)

    # Time arrow on the left
    ax.annotate("", xy=(0, y_bot), xytext=(0, y_top - 0.5),
                arrowprops=dict(arrowstyle='->', color=MED_GRAY, lw=1.5))
    ax.text(0, 5.5, "czas", ha='center', va='center', fontsize=8,
            rotation=90, color=DARK_GRAY)

    # Step 1: Both call Ssend
    y1 = 8.0
    draw_cell(ax, px0 - 1.3, y1 - 0.3, 2.6, 0.6, "Ssend(→P1)",
              fill='white', fontsize=9, fontweight='bold')
    draw_cell(ax, px1 - 1.3, y1 - 0.3, 2.6, 0.6, "Ssend(→P0)",
              fill='white', fontsize=9, fontweight='bold')

    # Arrows showing they wait for each other
    draw_curvy_arrow(ax, px0 + 1.3, y1, px1 - 1.3, y1,
                     connectionstyle="arc3,rad=0.15", lw=1.5)
    ax.text(5.5, y1 + 0.5, "czeka na\nRecv P1", ha='center', fontsize=7,
            style='italic')
    draw_curvy_arrow(ax, px1 - 1.3, y1 - 0.1, px0 + 1.3, y1 - 0.1,
                     connectionstyle="arc3,rad=0.15", lw=1.5)
    ax.text(5.5, y1 - 0.8, "czeka na\nRecv P0", ha='center', fontsize=7,
            style='italic')

    # Blocked indicators
    y2 = 5.5
    for px in [px0, px1]:
        ax.plot([px - 0.5, px + 0.5], [y2 - 0.3, y2 + 0.3],
                color='black', lw=3, zorder=5)
        ax.plot([px - 0.5, px + 0.5], [y2 + 0.3, y2 - 0.3],
                color='black', lw=3, zorder=5)
    ax.text(5.5, y2, "DEADLOCK!", ha='center', fontsize=14,
            fontweight='bold', color='black',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_GRAY,
                      edgecolor='black', lw=2))

    # Recv never reached
    y3 = 3.5
    draw_cell(ax, px0 - 1.3, y3 - 0.3, 2.6, 0.6, "Recv(←P1)",
              fill=VERY_LIGHT, edgecolor=MED_GRAY, fontsize=9)
    draw_cell(ax, px1 - 1.3, y3 - 0.3, 2.6, 0.6, "Recv(←P0)",
              fill=VERY_LIGHT, edgecolor=MED_GRAY, fontsize=9)
    ax.text(5.5, y3, "nigdy nie\nosiągnięte", ha='center', fontsize=8,
            style='italic', color=DARK_GRAY)

    # ---- RIGHT: Solution with MPI_Sendrecv ----
    ax = axes[1]
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("ROZWIĄZANIE — MPI_Sendrecv", fontsize=11, fontweight='bold')

    # Process headers
    draw_cell(ax, px0 - 1.2, y_top, 2.4, 0.8, "Proces 0",
              fill=LIGHT_GRAY, fontweight='bold', fontsize=10)
    draw_cell(ax, px1 - 1.2, y_top, 2.4, 0.8, "Proces 1",
              fill=LIGHT_GRAY, fontweight='bold', fontsize=10)

    # Timeline lines
    ax.plot([px0, px0], [y_top, y_bot], color='black', lw=2, zorder=1)
    ax.plot([px1, px1], [y_top, y_bot], color='black', lw=2, zorder=1)

    # Time arrow
    ax.annotate("", xy=(0, y_bot), xytext=(0, y_top - 0.5),
                arrowprops=dict(arrowstyle='->', color=MED_GRAY, lw=1.5))
    ax.text(0, 5.5, "czas", ha='center', va='center', fontsize=8,
            rotation=90, color=DARK_GRAY)

    # Step 1: Both call Sendrecv
    y1 = 7.5
    draw_cell(ax, px0 - 1.5, y1 - 0.4, 3.0, 0.8, "Sendrecv\n(→P1, ←P1)",
              fill='white', fontsize=9, fontweight='bold')
    draw_cell(ax, px1 - 1.5, y1 - 0.4, 3.0, 0.8, "Sendrecv\n(→P0, ←P0)",
              fill='white', fontsize=9, fontweight='bold')

    # Bidirectional arrows — simultaneous exchange
    draw_curvy_arrow(ax, px0 + 1.5, y1 + 0.15, px1 - 1.5, y1 + 0.15,
                     connectionstyle="arc3,rad=0.12", lw=2)
    draw_curvy_arrow(ax, px1 - 1.5, y1 - 0.15, px0 + 1.5, y1 - 0.15,
                     connectionstyle="arc3,rad=0.12", lw=2)
    ax.text(5.5, y1 + 0.9, "x[3] →", ha='center', fontsize=8)
    ax.text(5.5, y1 - 0.85, "← x[4]", ha='center', fontsize=8)

    # Step 2: Both complete
    y2 = 5.0
    ax.text(5.5, y2 + 0.3, "Wymiana zakończona ✓", ha='center', fontsize=10,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=VERY_LIGHT,
                      edgecolor='black', lw=1.5))

    # Step 3: Compute
    y3 = 3.5
    draw_cell(ax, px0 - 1.5, y3 - 0.4, 3.0, 0.8, "Oblicz x'[0..3]",
              fill='white', fontsize=9)
    draw_cell(ax, px1 - 1.5, y3 - 0.4, 3.0, 0.8, "Oblicz x'[4..7]",
              fill='white', fontsize=9)

    # Step 4: Next iteration
    y4 = 2.0
    ax.text(5.5, y4, "→ Następna iteracja", ha='center', fontsize=9,
            style='italic', color=DARK_GRAY)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    path = os.path.join(OUTPUT_DIR, 'q26_deadlock_vs_solution.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✓ {path}")


# =========================================================================
# 5. FULL JACOBI ITERATION — sequential pseudocode showing the dependency
# =========================================================================
def generate_jacobi_full_picture():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(-1, 16)
    ax.set_ylim(-5, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_title("Równoległy Jacobi — pełny obraz jednej iteracji",
                 fontsize=TITLE_SIZE, fontweight='bold', pad=15)

    cw, ch = 1.0, 0.7

    # === ROW 1: Old values (iteration k) ===
    y1 = 6.0
    ax.text(-0.8, y1 + ch/2, "Iteracja k\n(stare):", ha='right', va='center',
            fontsize=9, fontweight='bold')
    n = 12
    p_colors_cells = [VERY_LIGHT]*4 + [LIGHT_GRAY]*4 + ['#E8E8E8']*4
    for i in range(n):
        draw_cell(ax, i * cw, y1, cw, ch, f"x[{i}]", fill=p_colors_cells[i],
                  fontsize=7)

    # Process boundaries
    for bx in [4, 8]:
        ax.plot([bx, bx], [y1 - 0.3, y1 + ch + 0.3], color='black',
                lw=2.5, linestyle='--')

    ax.text(2, y1 + ch + 0.5, "Proces 0", ha='center', fontsize=9, fontweight='bold')
    ax.text(6, y1 + ch + 0.5, "Proces 1", ha='center', fontsize=9, fontweight='bold')
    ax.text(10, y1 + ch + 0.5, "Proces 2", ha='center', fontsize=9, fontweight='bold')

    # === STEP labels on the left ===
    # Step 1: Compute interior
    y2 = 3.5
    ax.text(6, y2 + 1.5, "Krok 1: Oblicz punkty wewnętrzne (bez ghost cells)",
            ha='center', fontsize=10, fontweight='bold')

    ax.text(-0.8, y2 + ch/2, "Iteracja k+1\n(nowe):", ha='right', va='center',
            fontsize=9, fontweight='bold')

    # Show computation arrows only for interior points
    for i in range(n):
        is_boundary = (i in [0, 3, 4, 7, 8, 11])
        if is_boundary:
            draw_cell(ax, i * cw, y2, cw, ch, "?",
                      fill=MED_GRAY, fontsize=9, fontweight='bold')
        else:
            fill = p_colors_cells[i]
            draw_cell(ax, i * cw, y2, cw, ch, f"x'[{i}]", fill=fill, fontsize=7)
            # Show dependency arrows from old row
            draw_arrow(ax, (i-1)*cw + cw/2, y1, i*cw + cw/2, y2 + ch,
                       color=DARK_GRAY, lw=0.8)
            draw_arrow(ax, (i+1)*cw + cw/2, y1, i*cw + cw/2, y2 + ch,
                       color=DARK_GRAY, lw=0.8)

    for bx in [4, 8]:
        ax.plot([bx, bx], [y2 - 0.3, y2 + ch + 0.3], color='black',
                lw=2.5, linestyle='--')

    # Label boundary cells
    ax.annotate("granica\n(potrzebuje\nghost cell)", xy=(3.5, y2), xytext=(3.5, y2 - 1.5),
                fontsize=7, ha='center', va='top',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))
    ax.annotate("granica\n(potrzebuje\nghost cell)", xy=(4.5, y2), xytext=(5.5, y2 - 1.5),
                fontsize=7, ha='center', va='top',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))

    # === Step 2: Exchange ghost cells ===
    y3 = -0.5
    ax.text(6, y3 + 2.0, "Krok 2: Wymień ghost cells → Krok 3: Oblicz punkty graniczne",
            ha='center', fontsize=10, fontweight='bold')

    for i in range(n):
        fill = p_colors_cells[i]
        draw_cell(ax, i * cw, y3, cw, ch, f"x'[{i}]", fill=fill, fontsize=7)

    for bx in [4, 8]:
        ax.plot([bx, bx], [y3 - 0.3, y3 + ch + 0.3], color='black',
                lw=2.5, linestyle='--')

    # Show exchange arrows at boundaries
    draw_curvy_arrow(ax, 3.5, y3 + ch + 0.05, 4.5, y3 + ch + 0.05,
                     connectionstyle="arc3,rad=-0.5", lw=1.5)
    draw_curvy_arrow(ax, 4.5, y3 - 0.05, 3.5, y3 - 0.05,
                     connectionstyle="arc3,rad=-0.5", lw=1.5)

    draw_curvy_arrow(ax, 7.5, y3 + ch + 0.05, 8.5, y3 + ch + 0.05,
                     connectionstyle="arc3,rad=-0.5", lw=1.5)
    draw_curvy_arrow(ax, 8.5, y3 - 0.05, 7.5, y3 - 0.05,
                     connectionstyle="arc3,rad=-0.5", lw=1.5)

    # Summary
    ax.text(6, y3 - 1.5,
            "Powtarzaj Krok 1→2→3 aż do zbieżności (|x' - x| < ε)",
            ha='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=VERY_LIGHT,
                      edgecolor='black', lw=1))

    # Pseudocode box
    pseudo = (
        "for iter = 1 to max_iter:\n"
        "    oblicz x'[wewnętrzne]  // nie wymaga ghost cells\n"
        "    wymień ghost cells z sąsiadami  // Send + Recv\n"
        "    oblicz x'[graniczne]   // teraz ghost cells dostępne\n"
        "    if |x' - x| < ε: break\n"
        "    x ← x'"
    )
    ax.text(6, -3.5, pseudo, ha='center', va='center', fontsize=8,
            family='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                      edgecolor='black', lw=1.5))

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'q26_jacobi_full_iteration.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✓ {path}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == '__main__':
    print("Generating Q26 Jacobi diagrams...")
    generate_jacobi_stencil()
    generate_domain_decomposition()
    generate_ghost_cell_exchange()
    generate_deadlock_vs_solution()
    generate_jacobi_full_picture()
    print("Done!")
