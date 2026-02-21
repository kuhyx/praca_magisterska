#!/usr/bin/env python3
"""
Generate diagrams for PYTANIE 31: Interaktywne wspomaganie decyzji w warunkach ryzyka.

Diagrams:
  1. Payoff matrix + all criteria results comparison (bar chart)
  2. Regret matrix construction step-by-step
  3. Hurwicz α interpolation between maximax and maximin
  4. Decision criteria mnemonic map
  5. Expected value criterion with probability-weighted bars
  6. Decision conditions spectrum (pewność → ryzyko → niepewność)

All: A4-compatible, B&W, 300 DPI, laser-printer-friendly.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

DPI = 300
BG = 'white'
LN = 'black'
FS = 8
FS_TITLE = 11
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
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              lw=lw, edgecolor=LN, facecolor=fill)
    else:
        rect = mpatches.Rectangle((x, y), w, h, lw=lw, edgecolor=LN, facecolor=fill)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha=ha, va=va, fontsize=fontsize,
            fontweight=fontweight, wrap=True)


def draw_arrow(ax, x1, y1, x2, y2, lw=1.2, style='->', color=LN):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))


# ============================================================
# 1. PAYOFF MATRIX + ALL CRITERIA BAR CHART
# ============================================================
def draw_criteria_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(8.27, 4.5), gridspec_kw={'width_ratios': [1.2, 1]})

    # -- Left: Payoff matrix as styled table --
    ax = axes[0]
    ax.axis('off')
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_title('Macierz wypłat (tys. zł)', fontsize=FS_TITLE, fontweight='bold', pad=8)

    # Headers
    headers_col = ['', 'S₁\n(dobra)', 'S₂\n(średnia)', 'S₃\n(zła)']
    rows = [
        ['A₁ (fabryka)', '200', '50', '−100'],
        ['A₂ (sklep)', '80', '70', '40'],
        ['A₃ (obligacje)', '30', '30', '30'],
    ]

    col_w = [1.8, 1.2, 1.2, 1.2]
    row_h = 0.7
    start_y = 4.5
    start_x = 0.2

    # Draw header row
    x = start_x
    for j, h in enumerate(headers_col):
        fill = GRAY2 if j > 0 else GRAY3
        rect = mpatches.Rectangle((x, start_y), col_w[j], row_h, lw=1, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(x + col_w[j]/2, start_y + row_h/2, h, ha='center', va='center',
                fontsize=FS, fontweight='bold')
        x += col_w[j]

    # Draw data rows
    for i, row in enumerate(rows):
        x = start_x
        y = start_y - (i+1) * row_h
        for j, val in enumerate(row):
            fill = GRAY4 if j == 0 else ('white' if i % 2 == 0 else GRAY1)
            # Highlight negative
            if val.startswith('−'):
                fill = '#D8D8D8'
            rect = mpatches.Rectangle((x, y), col_w[j], row_h, lw=1, edgecolor=LN, facecolor=fill)
            ax.add_patch(rect)
            fw = 'bold' if j == 0 else 'normal'
            ax.text(x + col_w[j]/2, y + row_h/2, val, ha='center', va='center',
                    fontsize=FS, fontweight=fw)
            x += col_w[j]

    # Probability row for EV
    x = start_x
    y = start_y - 4 * row_h
    probs = ['p (dla E[X]):', '0.5', '0.3', '0.2']
    for j, val in enumerate(probs):
        fill = GRAY5 if j > 0 else GRAY3
        rect = mpatches.Rectangle((x, y), col_w[j], row_h * 0.7, lw=1, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(x + col_w[j]/2, y + row_h*0.35, val, ha='center', va='center',
                fontsize=7, fontweight='bold', style='italic')
        x += col_w[j]

    # -- Right: Bar chart comparing criteria results --
    ax2 = axes[1]
    criteria = ['E[X]', 'Laplace', 'Maximax', 'Maximin', 'Hurwicz\nα=0.6', 'Savage']

    # Recalculate with probabilities 0.5, 0.3, 0.2
    # E[X]: A1=200*0.5+50*0.3+(-100)*0.2=100+15-20=95
    #        A2=80*0.5+70*0.3+40*0.2=40+21+8=69
    #        A3=30*0.5+30*0.3+30*0.2=15+9+6=30
    ev = [95, 69, 30]
    laplace = [50, 63.3, 30]
    maximax = [200, 80, 30]
    maximin = [-100, 40, 30]
    hurwicz = [80, 64, 30]  # α=0.6
    savage_maxregret = [140, 120, 170]  # lower = better

    # Which alternative wins for each criterion?
    winners = [0, 1, 0, 1, 0, 1]  # index of winning alternative
    winner_vals = [95, 63.3, 200, 40, 80, 120]

    # Display as grouped bar chart - each criterion shows the 3 alternatives
    x_pos = np.arange(len(criteria))
    width = 0.22
    hatches = ['///', '...', 'xxx']
    labels = ['A₁ (fabryka)', 'A₂ (sklep)', 'A₃ (obligacje)']

    all_vals = [
        [ev[0], laplace[0], maximax[0], maximin[0], hurwicz[0], savage_maxregret[0]],
        [ev[1], laplace[1], maximax[1], maximin[1], hurwicz[1], savage_maxregret[1]],
        [ev[2], laplace[2], maximax[2], maximin[2], hurwicz[2], savage_maxregret[2]],
    ]

    for i in range(3):
        bars = ax2.bar(x_pos + (i - 1) * width, all_vals[i], width,
                       label=labels[i], color='white', edgecolor=LN, hatch=hatches[i], lw=0.8)

    # Mark winners with star
    for c_idx in range(len(criteria)):
        w = winners[c_idx]
        val = all_vals[w][c_idx]
        ax2.text(x_pos[c_idx] + (w - 1) * width, val + 5, '★',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(criteria, fontsize=7)
    ax2.set_ylabel('Wartość kryterium', fontsize=8)
    ax2.set_title('Porównanie kryteriów', fontsize=FS_TITLE, fontweight='bold', pad=8)
    ax2.legend(fontsize=7, loc='upper right')
    ax2.axhline(y=0, color=LN, lw=0.5, ls='-')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.tick_params(labelsize=7)

    # Note about Savage
    ax2.text(5, -30, '(Savage: niżej\n= lepiej)', fontsize=6, ha='center',
             va='top', style='italic')

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'q31_criteria_comparison.png')
    fig.savefig(outpath, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {outpath}")


# ============================================================
# 2. REGRET MATRIX CONSTRUCTION
# ============================================================
def draw_regret_matrix():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 5))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_title('Kryterium Savage\'a — budowa macierzy żalu',
                 fontsize=FS_TITLE + 1, fontweight='bold', pad=10)

    # --- Step 1: Original payoff matrix (left) ---
    ax.text(2.2, 6.3, 'Krok 1: Macierz wypłat', fontsize=9, fontweight='bold',
            ha='center', va='center')

    col_w = 1.0
    row_h = 0.55
    headers = ['', 'S₁', 'S₂', 'S₃']
    data = [
        ['A₁', '200', '50', '−100'],
        ['A₂', '80', '70', '40'],
        ['A₃', '30', '30', '30'],
    ]
    start_x = 0.3
    start_y = 5.5

    for j, h in enumerate(headers):
        w = 0.7 if j == 0 else col_w
        x = start_x + (0 if j == 0 else 0.7 + (j-1)*col_w)
        rect = mpatches.Rectangle((x, start_y), w, row_h, lw=1, edgecolor=LN, facecolor=GRAY2)
        ax.add_patch(rect)
        ax.text(x + w/2, start_y + row_h/2, h, ha='center', va='center',
                fontsize=FS, fontweight='bold')

    for i, row in enumerate(data):
        y = start_y - (i+1) * row_h
        for j, val in enumerate(row):
            w = 0.7 if j == 0 else col_w
            x = start_x + (0 if j == 0 else 0.7 + (j-1)*col_w)
            fill = GRAY4 if j == 0 else 'white'
            rect = mpatches.Rectangle((x, y), w, row_h, lw=1, edgecolor=LN, facecolor=fill)
            ax.add_patch(rect)
            ax.text(x + w/2, y + row_h/2, val, ha='center', va='center', fontsize=FS)

    # Max per column annotation
    max_y = start_y - 3 * row_h - 0.1
    ax.text(start_x + 0.7 + 0.5*col_w, max_y, 'max=200', fontsize=7,
            ha='center', va='top', fontweight='bold', color='#333')
    ax.text(start_x + 0.7 + 1.5*col_w, max_y, 'max=70', fontsize=7,
            ha='center', va='top', fontweight='bold', color='#333')
    ax.text(start_x + 0.7 + 2.5*col_w, max_y, 'max=40', fontsize=7,
            ha='center', va='top', fontweight='bold', color='#333')

    # Arrow
    ax.annotate("", xy=(5.0, 4.8), xytext=(4.2, 4.8),
                arrowprops=dict(arrowstyle='->', color=LN, lw=2))
    ax.text(4.6, 5.0, 'rᵢⱼ = max − aᵢⱼ', fontsize=8, ha='center', va='bottom',
            fontweight='bold')

    # --- Step 2: Regret matrix (right) ---
    ax.text(7.5, 6.3, 'Krok 2: Macierz żalu', fontsize=9, fontweight='bold',
            ha='center', va='center')

    regret_data = [
        ['A₁', '0', '20', '140'],
        ['A₂', '120', '0', '0'],
        ['A₃', '170', '40', '10'],
    ]
    headers2 = ['', 'S₁', 'S₂', 'S₃', 'max rᵢ']
    start_x2 = 5.3

    for j, h in enumerate(headers2):
        w = 0.7 if j == 0 else (0.9 if j < 4 else 1.0)
        x = start_x2
        if j == 0:
            x = start_x2
        elif j <= 3:
            x = start_x2 + 0.7 + (j-1)*0.9
        else:
            x = start_x2 + 0.7 + 3*0.9
        rect = mpatches.Rectangle((x, start_y), w, row_h, lw=1, edgecolor=LN,
                                  facecolor=GRAY2 if j < 4 else GRAY3)
        ax.add_patch(rect)
        ax.text(x + w/2, start_y + row_h/2, h, ha='center', va='center',
                fontsize=FS, fontweight='bold')

    max_regrets = [140, 120, 170]
    for i, row in enumerate(regret_data):
        y = start_y - (i+1) * row_h
        for j, val in enumerate(row):
            w = 0.7 if j == 0 else 0.9
            x = start_x2 + (0 if j == 0 else 0.7 + (j-1)*0.9)
            fill = GRAY4 if j == 0 else 'white'
            # Highlight the max regret cell
            if j > 0 and int(val) == max_regrets[i]:
                fill = GRAY2
            rect = mpatches.Rectangle((x, y), w, row_h, lw=1, edgecolor=LN, facecolor=fill)
            ax.add_patch(rect)
            fw = 'bold' if (j > 0 and int(val) == max_regrets[i]) else 'normal'
            ax.text(x + w/2, y + row_h/2, val, ha='center', va='center',
                    fontsize=FS, fontweight=fw)

        # Max regret column
        x = start_x2 + 0.7 + 3*0.9
        w = 1.0
        fill = '#C8C8C8' if max_regrets[i] == min(max_regrets) else GRAY1
        rect = mpatches.Rectangle((x, y), w, row_h, lw=1.5 if max_regrets[i]==min(max_regrets) else 1,
                                  edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        marker = ' ★' if max_regrets[i] == min(max_regrets) else ''
        ax.text(x + w/2, y + row_h/2, f'{max_regrets[i]}{marker}', ha='center', va='center',
                fontsize=FS, fontweight='bold')

    # Bottom conclusion
    ax.text(5.0, 2.8, 'Krok 3: Wybierz min z max żalu → A₂ (max żal = 120)',
            fontsize=10, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY1, edgecolor=LN, lw=1.5))

    # Interpretatation examples
    ax.text(5.0, 2.0, 'Interpretacja żalu: r₁₃ = 140 oznacza:\n'
            '„Gdyby nastąpił S₃ (zła koniunktura), a wybrałbym A₁,\n'
            'żałowałbym, bo najlepszą opcją byłoby A₂ z wynikiem 40 — traciłbym 140"',
            fontsize=7.5, ha='center', va='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3, lw=0.8))

    # Mnemonic
    ax.text(5.0, 0.8, 'Mnemonik: Savage = „Żal jak nóż"\nMaksymalny żal to nóż '
            '— wybierz opcję z NAJMNIEJSZYM nożem',
            fontsize=8, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=LN, lw=1))

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'q31_regret_matrix.png')
    fig.savefig(outpath, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {outpath}")


# ============================================================
# 3. HURWICZ α INTERPOLATION
# ============================================================
def draw_hurwicz_interpolation():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 4))
    ax.set_title('Kryterium Hurwicza — wpływ α na wybór alternatywy',
                 fontsize=FS_TITLE + 1, fontweight='bold', pad=10)

    alphas = np.linspace(0, 1, 200)

    # V(Ai) = α * max_i + (1-α) * min_i
    # A1: max=200, min=-100
    # A2: max=80, min=40
    # A3: max=30, min=30
    v1 = alphas * 200 + (1 - alphas) * (-100)
    v2 = alphas * 80 + (1 - alphas) * 40
    v3 = alphas * 30 + (1 - alphas) * 30

    ax.plot(alphas, v1, 'k-', lw=2, label='A₁ (fabryka): V = 300α − 100')
    ax.plot(alphas, v2, 'k--', lw=2, label='A₂ (sklep): V = 40α + 40')
    ax.plot(alphas, v3, 'k:', lw=2, label='A₃ (obligacje): V = 30')

    # Find crossover points
    # A2 = A1: 40α + 40 = 300α - 100  →  140 = 260α  →  α = 140/260 ≈ 0.538
    alpha_cross_12 = 140 / 260
    v_cross_12 = 40 * alpha_cross_12 + 40

    # A2 = A3: 40α + 40 = 30  →  40α = -10  →  α = -0.25 (never — A2 always > A3)
    # A1 = A3: 300α - 100 = 30  →  300α = 130  →  α = 130/300 ≈ 0.433
    alpha_cross_13 = 130 / 300
    v_cross_13 = 30

    ax.plot(alpha_cross_12, v_cross_12, 'ko', markersize=8, zorder=5)
    ax.annotate(f'α ≈ {alpha_cross_12:.2f}\nA₁ = A₂', xy=(alpha_cross_12, v_cross_12),
                xytext=(alpha_cross_12 + 0.12, v_cross_12 - 30),
                fontsize=8, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=LN, lw=1))

    # Shade winning regions
    ax.axvspan(0, alpha_cross_12, alpha=0.08, color='black', label='_')
    ax.axvspan(alpha_cross_12, 1, alpha=0.15, color='black', label='_')

    ax.text(alpha_cross_12 / 2, -60, 'A₂ wygrywa\n(pesymistycznie)',
            fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=LN))
    ax.text((alpha_cross_12 + 1) / 2, 160, 'A₁ wygrywa\n(optymistycznie)',
            fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=LN))

    # Special α values
    ax.axvline(x=0, color=LN, lw=0.5, ls=':')
    ax.axvline(x=1, color=LN, lw=0.5, ls=':')
    ax.text(0, -115, 'α=0\nmaximin', fontsize=7, ha='center', va='top', fontweight='bold')
    ax.text(1, -115, 'α=1\nmaximax', fontsize=7, ha='center', va='top', fontweight='bold')

    ax.set_xlabel('Współczynnik optymizmu α', fontsize=9)
    ax.set_ylabel('V(Aᵢ) = α·max + (1−α)·min', fontsize=9)
    ax.legend(fontsize=8, loc='upper left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(-0.05, 1.05)
    ax.axhline(y=0, color=LN, lw=0.3, ls='-')
    ax.tick_params(labelsize=8)

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'q31_hurwicz_alpha.png')
    fig.savefig(outpath, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {outpath}")


# ============================================================
# 4. DECISION CRITERIA MNEMONIC MAP
# ============================================================
def draw_criteria_mnemonic():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Mapa mnemoniczna — 6 kryteriów decyzyjnych',
                 fontsize=FS_TITLE + 2, fontweight='bold', pad=10)

    # Central node
    draw_box(ax, 3.5, 3.5, 3, 1, 'MACIERZ\nWYPŁAT', fill=GRAY2, lw=2,
             fontsize=11, fontweight='bold')

    # Criteria boxes around the center
    criteria = [
        # (x, y, w, h, title, mnemonic, formula)
        (0, 6.5, 3, 1.2, 'WARTOŚĆ OCZEKIWANA', '„Mam prawdopodobieństwa"', 'E[Aᵢ] = Σ pⱼ·aᵢⱼ'),
        (3.5, 6.5, 3, 1.2, 'LAPLACE', '„Wszystko po równo"', 'V = Σaᵢⱼ / n'),
        (7, 6.5, 3, 1.2, 'MAXIMAX', '„Optymista: max z max"', 'max maxⱼ aᵢⱼ'),
        (0, 0.5, 3, 1.2, 'MAXIMIN (Wald)', '„Pesymista: max z min"', 'max minⱼ aᵢⱼ'),
        (3.5, 0.5, 3, 1.2, 'HURWICZ', '„α pomiędzy"', 'α·max + (1−α)·min'),
        (7, 0.5, 3, 1.2, 'SAVAGE', '„Min max żalu"', 'min maxⱼ rᵢⱼ'),
    ]

    fills = [GRAY3, GRAY1, 'white', 'white', GRAY1, GRAY3]

    for i, (x, y, w, h, title, mnem, formula) in enumerate(criteria):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                              lw=1.5, edgecolor=LN, facecolor=fills[i])
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.78, title, ha='center', va='center',
                fontsize=8, fontweight='bold')
        ax.text(x + w/2, y + h*0.45, mnem, ha='center', va='center',
                fontsize=7, style='italic')
        ax.text(x + w/2, y + h*0.15, formula, ha='center', va='center',
                fontsize=7, fontweight='bold', family='monospace')

        # Arrows from center to each box
        cx, cy = 5, 4  # center of macierz
        bx, by = x + w/2, y + h/2
        if by > cy:
            ax.annotate("", xy=(bx, y), xytext=(cx, 4.5),
                        arrowprops=dict(arrowstyle='->', color=LN, lw=1,
                                        connectionstyle='arc3,rad=0'))
        else:
            ax.annotate("", xy=(bx, y + h), xytext=(cx, 3.5),
                        arrowprops=dict(arrowstyle='->', color=LN, lw=1,
                                        connectionstyle='arc3,rad=0'))

    # Labels on arrows
    ax.text(1.2, 5.6, 'znane p', fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=GRAY3, lw=0.5))
    ax.text(5, 5.6, 'p = 1/n', fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=GRAY3, lw=0.5))
    ax.text(8.7, 5.6, 'max ↑', fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=GRAY3, lw=0.5))
    ax.text(1.2, 2.5, 'min ↑', fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=GRAY3, lw=0.5))
    ax.text(5, 2.5, 'podaj α', fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=GRAY3, lw=0.5))
    ax.text(8.7, 2.5, 'macierz\nżalu', fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=GRAY3, lw=0.5))

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'q31_criteria_mnemonic.png')
    fig.savefig(outpath, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {outpath}")


# ============================================================
# 5. EXPECTED VALUE CRITERION WITH PROBABILITY BARS
# ============================================================
def draw_expected_value():
    fig, axes = plt.subplots(1, 3, figsize=(8.27, 3.5), sharey=True)
    fig.suptitle('Kryterium wartości oczekiwanej E[X] — rozkład wyników per alternatywa',
                 fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # Probabilities: p1=0.5, p2=0.3, p3=0.2
    probs = [0.5, 0.3, 0.2]
    states = ['S₁\n(dobra)\np=0.5', 'S₂\n(średnia)\np=0.3', 'S₃\n(zła)\np=0.2']
    alts = [
        ('A₁ (fabryka)', [200, 50, -100], 95),
        ('A₂ (sklep)', [80, 70, 40], 69),
        ('A₃ (obligacje)', [30, 30, 30], 30),
    ]

    hatches = ['///', '...', 'xxx']

    for idx, (ax, (name, vals, ev)) in enumerate(zip(axes, alts)):
        # Bar: height = payoff, width proportional to probability
        x_positions = [0, 0.6, 1.0]
        widths = [p * 0.9 for p in probs]

        for i, (v, p, h) in enumerate(zip(vals, probs, hatches)):
            color = 'white' if v >= 0 else GRAY2
            bar = ax.bar(x_positions[i], v, width=widths[i], color=color,
                         edgecolor=LN, hatch=h, lw=0.8, align='edge')
            # Value label
            offset = 8 if v >= 0 else -12
            ax.text(x_positions[i] + widths[i]/2, v + offset, f'{v}',
                    ha='center', va='center', fontsize=8, fontweight='bold')
            # Probability contribution
            contrib = v * p
            ax.text(x_positions[i] + widths[i]/2, v/2,
                    f'{v}×{p}\n={contrib:.0f}', ha='center', va='center',
                    fontsize=6, style='italic')

        # Expected value line
        ax.axhline(y=ev, color=LN, lw=2, ls='--')
        ax.text(1.35, ev, f'E[X]={ev}', fontsize=8, fontweight='bold',
                va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.15', facecolor=GRAY1, edgecolor=LN))

        ax.set_title(name, fontsize=9, fontweight='bold')
        ax.set_xticks([0.225, 0.735, 1.09])
        ax.set_xticklabels(['S₁', 'S₂', 'S₃'], fontsize=7)
        ax.axhline(y=0, color=LN, lw=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=7)

        # Star on winner
        if ev == 95:
            ax.text(0.7, ev + 20, '★ MAX', fontsize=9, fontweight='bold',
                    ha='center', va='bottom')

    axes[0].set_ylabel('Wypłata (tys. zł)', fontsize=8)

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'q31_expected_value.png')
    fig.savefig(outpath, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {outpath}")


# ============================================================
# 6. DECISION CONDITIONS SPECTRUM
# ============================================================
def draw_conditions_spectrum():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Warunki decyzyjne — spektrum wiedzy decydenta',
                 fontsize=FS_TITLE + 1, fontweight='bold', pad=10)

    # Three zones
    zones = [
        (0.3, 1.5, 2.8, 2.5, 'PEWNOŚĆ', 'white', [
            'Znamy dokładny wynik',
            'Przykład: lokata 5%',
            'Metoda: po prostu wybierz',
            'najlepszy wynik'
        ]),
        (3.5, 1.5, 2.8, 2.5, 'RYZYKO', GRAY1, [
            'Znamy wyniki I prawdop.',
            'Przykład: gra w kości',
            'Metoda: wartość',
            'oczekiwana E[X]'
        ]),
        (6.7, 1.5, 2.8, 2.5, 'NIEPEWNOŚĆ', GRAY3, [
            'Znamy wyniki, ale',
            'NIE znamy prawdop.',
            'Metody: Laplace, maximax,',
            'maximin, Hurwicz, Savage'
        ]),
    ]

    for x, y, w, h, title, fill, lines in zones:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              lw=2, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.3, title, ha='center', va='center',
                fontsize=11, fontweight='bold')
        for i, line in enumerate(lines):
            ax.text(x + w/2, y + h - 0.7 - i*0.4, line, ha='center', va='center',
                    fontsize=7)

    # Arrows between zones
    ax.annotate("", xy=(3.4, 2.75), xytext=(3.15, 2.75),
                arrowprops=dict(arrowstyle='->', color=LN, lw=2))
    ax.annotate("", xy=(6.6, 2.75), xytext=(6.35, 2.75),
                arrowprops=dict(arrowstyle='->', color=LN, lw=2))

    # Bottom: knowledge gradient bar
    gradient_y = 0.5
    gradient_h = 0.5
    n_steps = 50
    for i in range(n_steps):
        x = 0.3 + i * (9.2 / n_steps)
        w = 9.2 / n_steps + 0.01
        gray_val = 1 - (i / n_steps) * 0.7
        rect = mpatches.Rectangle((x, gradient_y), w, gradient_h, lw=0,
                                  facecolor=str(gray_val))
        ax.add_patch(rect)

    rect = mpatches.Rectangle((0.3, gradient_y), 9.2, gradient_h, lw=1.5,
                              edgecolor=LN, facecolor='none')
    ax.add_patch(rect)

    ax.text(0.3, gradient_y - 0.15, 'Dużo wiedzy', fontsize=7, ha='left', va='top')
    ax.text(9.5, gradient_y - 0.15, 'Mało wiedzy', fontsize=7, ha='right', va='top')
    ax.text(4.95, gradient_y + gradient_h / 2, 'POZIOM WIEDZY DECYDENTA',
            fontsize=8, fontweight='bold', ha='center', va='center', color='white')

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'q31_conditions_spectrum.png')
    fig.savefig(outpath, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  Saved: {outpath}")


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Generating PYTANIE 31 diagrams...")
    draw_criteria_comparison()
    draw_regret_matrix()
    draw_hurwicz_interpolation()
    draw_criteria_mnemonic()
    draw_expected_value()
    draw_conditions_spectrum()
    print("Done! All Q31 diagrams saved to:", OUTPUT_DIR)
