#!/usr/bin/env python3
"""
Generate diagrams for PYTANIE 17: Szeregowanie zadań (Scheduling).

Diagrams:
  1. Graham notation α|β|γ visual mnemonic map
  2. Johnson's algorithm Gantt chart (F2||Cmax example)
  3. SPT vs LPT comparison Gantt (1||ΣCⱼ)
  4. Flow shop vs Job shop visual comparison
  5. Scheduling complexity landscape

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
# 1. GRAHAM NOTATION α|β|γ — MNEMONIC MAP
# ============================================================
def draw_graham_notation():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Notacja Grahama  α | β | γ  — Mapa mnemoniczna',
                 fontsize=FS_TITLE + 1, fontweight='bold', pad=12)

    # === TOP: The three fields ===
    # Big formula bar
    bar_y = 12.5
    bar_h = 1.0
    # α box
    rect = FancyBboxPatch((0.5, bar_y), 2.5, bar_h, boxstyle="round,pad=0.08",
                          lw=2, edgecolor=LN, facecolor=GRAY1)
    ax.add_patch(rect)
    ax.text(1.75, bar_y + bar_h/2, 'α', fontsize=20, fontweight='bold',
            ha='center', va='center')
    ax.text(1.75, bar_y - 0.25, 'MASZYNY', fontsize=8, fontweight='bold',
            ha='center', va='top', color='#444444')

    # separator |
    ax.text(3.3, bar_y + bar_h/2, '|', fontsize=24, fontweight='bold',
            ha='center', va='center')

    # β box
    rect = FancyBboxPatch((3.7, bar_y), 2.5, bar_h, boxstyle="round,pad=0.08",
                          lw=2, edgecolor=LN, facecolor=GRAY2)
    ax.add_patch(rect)
    ax.text(4.95, bar_y + bar_h/2, 'β', fontsize=20, fontweight='bold',
            ha='center', va='center')
    ax.text(4.95, bar_y - 0.25, 'OGRANICZENIA', fontsize=8, fontweight='bold',
            ha='center', va='top', color='#444444')

    # separator |
    ax.text(6.5, bar_y + bar_h/2, '|', fontsize=24, fontweight='bold',
            ha='center', va='center')

    # γ box
    rect = FancyBboxPatch((6.9, bar_y), 2.5, bar_h, boxstyle="round,pad=0.08",
                          lw=2, edgecolor=LN, facecolor=GRAY3)
    ax.add_patch(rect)
    ax.text(8.15, bar_y + bar_h/2, 'γ', fontsize=20, fontweight='bold',
            ha='center', va='center')
    ax.text(8.15, bar_y - 0.25, 'CEL', fontsize=8, fontweight='bold',
            ha='center', va='top', color='#444444')

    # === SECTION α: MACHINES ===
    sec_y = 11.5
    ax.text(0.3, sec_y, 'α — „1 Prawdziwy Quasi-Rycerz Forsuje Jaskinię Orków"',
            fontsize=8, fontweight='bold', va='top',
            style='italic', color='#333333')

    alpha_items = [
        ('1', 'jedna maszyna', '●', GRAY4),
        ('Pm', 'identyczne Parallel', '●●●', GRAY1),
        ('Qm', 'Quasi-uniform\n(różne prędkości)', '●●◐', GRAY4),
        ('Rm', 'Random unrelated\n(czasy per para)', '●◆▲', GRAY1),
        ('Fm', 'Flow shop\n(ta sama kolejność)', '→→→', GRAY2),
        ('Jm', 'Job shop\n(indyw. trasy)', '↗↙↘', GRAY4),
        ('Om', 'Open shop\n(dowolna kolej.)', '?→?', GRAY1),
    ]

    col_w = 1.28
    box_h_a = 1.1
    start_x = 0.3
    start_y = 9.6

    for i, (symbol, desc, icon, fill) in enumerate(alpha_items):
        x = start_x + i * col_w
        y = start_y
        rect = FancyBboxPatch((x, y), col_w - 0.1, box_h_a,
                              boxstyle="round,pad=0.04",
                              lw=1, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(x + (col_w - 0.1)/2, y + box_h_a - 0.15, symbol,
                ha='center', va='top', fontsize=9, fontweight='bold')
        ax.text(x + (col_w - 0.1)/2, y + box_h_a/2 - 0.1, desc,
                ha='center', va='center', fontsize=5.5)
        ax.text(x + (col_w - 0.1)/2, y + 0.12, icon,
                ha='center', va='bottom', fontsize=7)

    # Complexity arrow under α
    arr_y = 9.35
    ax.annotate("", xy=(9.0, arr_y), xytext=(0.5, arr_y),
                arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5))
    ax.text(4.8, arr_y - 0.18, 'rosnąca złożoność →',
            ha='center', fontsize=6, color='#666666')

    # === SECTION β: CONSTRAINTS ===
    sec_y2 = 8.9
    ax.text(0.3, sec_y2, 'β — „Robak Daje Deadline: Przerwy Poprzedzają Pojedyncze Setup\'y"',
            fontsize=8, fontweight='bold', va='top',
            style='italic', color='#333333')

    beta_items = [
        ('rⱼ', 'release\ndates', 'Robak\ndostępne\nod czasu rⱼ', GRAY1),
        ('dⱼ', 'due\ndates', 'Daje\ntermin soft\n(kara za spóźn.)', GRAY4),
        ('d̄ⱼ', 'dead-\nlines', 'Deadline\ntermin hard\n(musi dotrzymać)', GRAY1),
        ('pmtn', 'preemp-\ntion', 'Przerwy\nmożna\nprzerwać', GRAY2),
        ('prec', 'prece-\ndencje', 'Poprzedzają\nA->B (DAG)', GRAY4),
        ('pⱼ=1', 'unit\ntime', 'Pojedyncze\nwszystkie = 1', GRAY1),
        ('sⱼₖ', 'setup\ntimes', "Setup'y\nprzezbrojenie\nmiędzy j->k", GRAY4),
    ]

    start_y2 = 7.0
    box_h_b = 1.4

    for i, (symbol, label, desc, fill) in enumerate(beta_items):
        x = start_x + i * col_w
        y = start_y2
        rect = FancyBboxPatch((x, y), col_w - 0.1, box_h_b,
                              boxstyle="round,pad=0.04",
                              lw=1, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(x + (col_w - 0.1)/2, y + box_h_b - 0.12, symbol,
                ha='center', va='top', fontsize=9, fontweight='bold')
        ax.text(x + (col_w - 0.1)/2, y + box_h_b/2 - 0.05, desc,
                ha='center', va='center', fontsize=5)

    # === SECTION γ: CRITERIA ===
    sec_y3 = 6.5
    ax.text(0.3, sec_y3, 'γ — „Ciężki Sum Ważony Lata, Tardiness Uderza"',
            fontsize=8, fontweight='bold', va='top',
            style='italic', color='#333333')

    gamma_items = [
        ('Cmax', 'makespan\nmax(Cⱼ)', 'Jak długo\ntrwa WSZYSTKO?', GRAY2),
        ('ΣCⱼ', 'suma\nukończeń', 'Średni czas\noczekiwania?', GRAY4),
        ('ΣwⱼCⱼ', 'ważona\nsuma', 'Priorytety\nzadań?', GRAY1),
        ('Lmax', 'max\nopóźnienie', 'Najgorsze\nspóźnienie?', GRAY2),
        ('ΣTⱼ', 'suma\nspóźnień', 'Łączne\nspóźnienia?', GRAY4),
        ('ΣUⱼ', 'liczba\nspóźnionych', 'Ile spóźnionych\nzadań?', GRAY1),
    ]

    start_y3 = 4.5
    box_h_g = 1.4
    col_w_g = 1.5

    for i, (symbol, label, question, fill) in enumerate(gamma_items):
        x = start_x + i * col_w_g
        y = start_y3
        rect = FancyBboxPatch((x, y), col_w_g - 0.1, box_h_g,
                              boxstyle="round,pad=0.04",
                              lw=1, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(x + (col_w_g - 0.1)/2, y + box_h_g - 0.1, symbol,
                ha='center', va='top', fontsize=9, fontweight='bold')
        ax.text(x + (col_w_g - 0.1)/2, y + box_h_g/2 - 0.05, label,
                ha='center', va='center', fontsize=6)
        ax.text(x + (col_w_g - 0.1)/2, y + 0.15, f'„{question}"',
                ha='center', va='bottom', fontsize=5, style='italic')

    # === BOTTOM: Example + Optimal methods ===
    ex_y = 3.5
    ax.text(0.3, ex_y, 'Przykłady zapisu i optymalne metody:',
            fontsize=8, fontweight='bold', va='top')

    examples = [
        ('1 || ΣCⱼ', 'SPT (najkrótsze\nnajpierw)', 'O(n log n)', GRAY1),
        ('1 || Lmax', 'EDD (najwcześniejszy\ntermin)', 'O(n log n)', GRAY4),
        ('F2 || Cmax', 'Algorytm\nJohnsona', 'O(n log n)', GRAY2),
        ('Pm || Cmax', 'LPT heurystyka\n(NP-trudny!)', 'NP-hard', GRAY3),
        ('Jm || Cmax', 'Branch & Bound\n(NP-trudny!)', 'NP-hard', GRAY5),
    ]

    ex_start_y = 1.8
    ex_box_w = 1.72
    ex_box_h = 1.4

    for i, (notation, method, complexity, fill) in enumerate(examples):
        x = start_x + i * (ex_box_w + 0.1)
        y = ex_start_y
        rect = FancyBboxPatch((x, y), ex_box_w, ex_box_h,
                              boxstyle="round,pad=0.04",
                              lw=1.2, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(x + ex_box_w/2, y + ex_box_h - 0.12, notation,
                ha='center', va='top', fontsize=8, fontweight='bold',
                fontfamily='monospace')
        ax.text(x + ex_box_w/2, y + ex_box_h/2 - 0.05, method,
                ha='center', va='center', fontsize=6)
        ax.text(x + ex_box_w/2, y + 0.12, complexity,
                ha='center', va='bottom', fontsize=6.5, fontweight='bold',
                color='#555555')

    # Footer mnemonic summary
    ax.text(5.0, 0.8, '„α|β|γ = Maszyny | Ograniczenia | Cel"',
            ha='center', fontsize=9, fontweight='bold', style='italic',
            color='#333333',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3, lw=1))

    ax.text(5.0, 0.2, 'α: ILE maszyn i JAKIE?    β: JAKIE ograniczenia zadań?    γ: CO minimalizujemy?',
            ha='center', fontsize=7, color='#555555')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'scheduling_graham_notation.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ scheduling_graham_notation.png")


# ============================================================
# 2. JOHNSON'S ALGORITHM GANTT CHART
# ============================================================
def draw_johnson_gantt():
    fig, axes = plt.subplots(2, 1, figsize=(8.27, 7), gridspec_kw={'height_ratios': [1, 1.8]})

    # --- Top: The decision process ---
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Algorytm Johnsona (F2 || Cmax) — Decyzja + Diagram Gantta',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Task table
    tasks = ['J1', 'J2', 'J3', 'J4', 'J5']
    a_times = [4, 2, 6, 1, 3]
    b_times = [5, 3, 2, 7, 4]
    min_vals = [min(a, b) for a, b in zip(a_times, b_times)]
    min_on   = ['M1' if a <= b else 'M2' for a, b in zip(a_times, b_times)]
    assign   = ['POCZątek' if m == 'M1' else 'KONIEC' for m in min_on]

    # Draw table
    col_w_t = 1.3
    row_h = 0.55
    headers = ['Zadanie', 'aⱼ (M1)', 'bⱼ (M2)', 'min', 'min na', 'Przydziel']
    table_x = 0.8
    table_y = 3.8

    for j, hdr in enumerate(headers):
        x = table_x + j * col_w_t
        rect = mpatches.Rectangle((x, table_y), col_w_t, row_h,
                                   lw=1, edgecolor=LN, facecolor=GRAY2)
        ax.add_patch(rect)
        ax.text(x + col_w_t/2, table_y + row_h/2, hdr,
                ha='center', va='center', fontsize=6.5, fontweight='bold')

    for i in range(5):
        row_data = [tasks[i], str(a_times[i]), str(b_times[i]),
                    str(min_vals[i]), min_on[i], assign[i]]
        for j, val in enumerate(row_data):
            x = table_x + j * col_w_t
            y = table_y - (i + 1) * row_h
            fill_c = GRAY1 if min_on[i] == 'M1' else GRAY4
            if j == 3:  # min column - highlight
                fill_c = GRAY3
            rect = mpatches.Rectangle((x, y), col_w_t, row_h,
                                       lw=0.8, edgecolor=LN, facecolor=fill_c)
            ax.add_patch(rect)
            fw = 'bold' if j >= 3 else 'normal'
            ax.text(x + col_w_t/2, y + row_h/2, val,
                    ha='center', va='center', fontsize=6.5, fontweight=fw)

    # Sorting result
    result_y = 0.7
    ax.text(5.0, result_y + 0.4, 'Sortuj → POCZĄTEK ↑aⱼ: J4(1), J2(2), J5(3), J1(4)  |  KONIEC ↓bⱼ: J3(2)',
            ha='center', fontsize=7, color='#333333')
    ax.text(5.0, result_y, 'Optymalna kolejność:   J4 → J2 → J5 → J1 → J3',
            ha='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY1, edgecolor=LN, lw=1.2))

    # --- Bottom: Gantt chart ---
    ax2 = axes[1]
    ax2.set_xlim(-1, 24)
    ax2.set_ylim(-1, 4)
    ax2.axis('off')

    # Machines labels
    m1_y = 2.5
    m2_y = 0.8
    bar_h = 0.9

    ax2.text(-0.8, m1_y + bar_h/2, 'M1', ha='center', va='center',
             fontsize=11, fontweight='bold')
    ax2.text(-0.8, m2_y + bar_h/2, 'M2', ha='center', va='center',
             fontsize=11, fontweight='bold')

    # Schedule: J4 → J2 → J5 → J1 → J3
    order = ['J4', 'J2', 'J5', 'J1', 'J3']
    a_ord = [1, 2, 3, 4, 6]  # M1 times in order
    b_ord = [7, 3, 4, 5, 2]  # M2 times in order
    fills = [GRAY1, GRAY2, GRAY4, GRAY3, GRAY5]
    hatches = ['', '///', '', '\\\\\\', 'xxx']

    # M1 schedule
    m1_starts = []
    t = 0
    for a in a_ord:
        m1_starts.append(t)
        t += a
    m1_ends = [s + a for s, a in zip(m1_starts, a_ord)]

    # M2 schedule (must wait for M1 finish AND previous M2 finish)
    m2_starts = []
    m2_ends = []
    prev_m2_end = 0
    for i, b in enumerate(b_ord):
        start = max(m1_ends[i], prev_m2_end)
        m2_starts.append(start)
        m2_ends.append(start + b)
        prev_m2_end = start + b

    # Draw M1 bars
    for i in range(5):
        rect = mpatches.Rectangle((m1_starts[i], m1_y), a_ord[i], bar_h,
                                   lw=1.2, edgecolor=LN, facecolor=fills[i],
                                   hatch=hatches[i])
        ax2.add_patch(rect)
        ax2.text(m1_starts[i] + a_ord[i]/2, m1_y + bar_h/2,
                 f'{order[i]}\n({a_ord[i]})',
                 ha='center', va='center', fontsize=7, fontweight='bold')

    # Draw M2 bars
    for i in range(5):
        rect = mpatches.Rectangle((m2_starts[i], m2_y), b_ord[i], bar_h,
                                   lw=1.2, edgecolor=LN, facecolor=fills[i],
                                   hatch=hatches[i])
        ax2.add_patch(rect)
        ax2.text(m2_starts[i] + b_ord[i]/2, m2_y + bar_h/2,
                 f'{order[i]}\n({b_ord[i]})',
                 ha='center', va='center', fontsize=7, fontweight='bold')

    # Draw idle regions on M2
    idle_starts = [0]
    idle_ends = [m2_starts[0]]
    for i in range(1, 5):
        if m2_starts[i] > m2_ends[i-1]:
            idle_starts.append(m2_ends[i-1])
            idle_ends.append(m2_starts[i])

    for s, e in zip(idle_starts, idle_ends):
        if e > s:
            rect = mpatches.Rectangle((s, m2_y), e - s, bar_h,
                                       lw=0.5, edgecolor='#AAAAAA',
                                       facecolor='white', linestyle='--')
            ax2.add_patch(rect)
            ax2.text(s + (e-s)/2, m2_y + bar_h/2, 'idle',
                     ha='center', va='center', fontsize=5, color='#999999')

    # Time axis
    ax_y = m2_y - 0.15
    ax2.plot([0, 23], [ax_y, ax_y], color=LN, lw=0.8)
    for t in range(0, 24, 2):
        ax2.plot([t, t], [ax_y - 0.08, ax_y + 0.08], color=LN, lw=0.8)
        ax2.text(t, ax_y - 0.25, str(t), ha='center', va='top', fontsize=6)
    ax2.text(11.5, ax_y - 0.55, 'czas', ha='center', fontsize=7)

    # Cmax annotation
    ax2.annotate(f'Cmax = {m2_ends[-1]}', xy=(m2_ends[-1], m2_y + bar_h),
                 xytext=(m2_ends[-1] + 0.5, m2_y + bar_h + 0.6),
                 fontsize=10, fontweight='bold', color='#333333',
                 arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))

    # Mnemonic at bottom
    ax2.text(11, -0.7,
             '„Krótki na M1 → START (szybko karmi M2)      Krótki na M2 → KONIEC (szybko kończy)"',
             ha='center', fontsize=7.5, fontweight='bold', style='italic',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3, lw=0.8))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'scheduling_johnson_gantt.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ scheduling_johnson_gantt.png")


# ============================================================
# 3. SPT vs LPT COMPARISON (1 || ΣCⱼ)
# ============================================================
def draw_spt_comparison():
    fig, axes = plt.subplots(2, 1, figsize=(8.27, 5.5))

    tasks_orig = [('J1', 5), ('J2', 3), ('J3', 8), ('J4', 2), ('J5', 6)]

    spt_order = sorted(tasks_orig, key=lambda x: x[1])
    lpt_order = sorted(tasks_orig, key=lambda x: -x[1])

    fills_map = {'J1': GRAY1, 'J2': GRAY2, 'J3': GRAY3, 'J4': GRAY4, 'J5': GRAY5}
    hatch_map = {'J1': '', 'J2': '///', 'J3': 'xxx', 'J4': '', 'J5': '\\\\\\'}

    for idx, (ax, order_list, title, is_optimal) in enumerate([
        (axes[0], spt_order, 'SPT (Shortest Processing Time) — OPTYMALNE', True),
        (axes[1], lpt_order, 'LPT (Longest Processing Time) — gorsze!', False)
    ]):
        ax.set_xlim(-2, 26)
        ax.set_ylim(-0.5, 2.5)
        ax.axis('off')
        color = '#222222' if is_optimal else '#666666'
        marker = '✓' if is_optimal else '✗'
        ax.set_title(f'{marker} {title}', fontsize=9, fontweight='bold',
                     loc='left', color=color, pad=5)

        bar_y = 1.0
        bar_h = 0.8
        t = 0
        completions = []

        for name, duration in order_list:
            rect = mpatches.Rectangle((t, bar_y), duration, bar_h,
                                       lw=1.2, edgecolor=LN,
                                       facecolor=fills_map[name],
                                       hatch=hatch_map[name])
            ax.add_patch(rect)
            ax.text(t + duration/2, bar_y + bar_h/2, f'{name}\n({duration})',
                    ha='center', va='center', fontsize=7, fontweight='bold')
            t += duration
            completions.append(t)

            # Completion time marker
            ax.plot([t, t], [bar_y - 0.15, bar_y], color=LN, lw=0.8)
            ax.text(t, bar_y - 0.25, f'C={t}', ha='center', va='top',
                    fontsize=6, color='#555555')

        total = sum(completions)
        # Time axis
        ax.plot([0, 25], [bar_y - 0.05, bar_y - 0.05], color=LN, lw=0.5)

        # Sum annotation
        comp_str = ' + '.join(str(c) for c in completions)
        ax.text(25, bar_y + bar_h/2,
                f'ΣCⱼ = {comp_str}\n    = {total}',
                ha='left', va='center', fontsize=7,
                fontweight='bold' if is_optimal else 'normal',
                color=color,
                bbox=dict(boxstyle='round,pad=0.2',
                         facecolor=GRAY1 if is_optimal else 'white',
                         edgecolor=color, lw=1))

    # Bottom annotation
    fig.text(0.5, 0.02,
             '„Short People To the front" — krótkie najpierw, jak niskie osoby w zdjęciu klasowym',
             ha='center', fontsize=8, fontweight='bold', style='italic',
             color='#444444')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(os.path.join(OUTPUT_DIR, 'scheduling_spt_comparison.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ scheduling_spt_comparison.png")


# ============================================================
# 4. FLOW SHOP vs JOB SHOP
# ============================================================
def draw_flow_vs_job():
    fig, axes = plt.subplots(1, 2, figsize=(8.27, 4.5))

    # --- LEFT: Flow Shop ---
    ax = axes[0]
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Flow Shop (Fm)', fontsize=10, fontweight='bold', pad=8)

    # Machines in a row
    machines_x = [1, 3, 5]
    machines_y = 3
    mach_r = 0.4

    for i, mx in enumerate(machines_x):
        circle = plt.Circle((mx, machines_y), mach_r,
                            facecolor=GRAY2, edgecolor=LN, lw=1.5)
        ax.add_patch(circle)
        ax.text(mx, machines_y, f'M{i+1}', ha='center', va='center',
                fontsize=9, fontweight='bold')

    # Arrows between machines
    for i in range(len(machines_x) - 1):
        draw_arrow(ax, machines_x[i] + mach_r + 0.05, machines_y,
                   machines_x[i+1] - mach_r - 0.05, machines_y, lw=2)

    # Jobs all flowing the same way
    jobs_flow = ['J1', 'J2', 'J3']
    for j, (job, y_off) in enumerate(zip(jobs_flow, [0.8, 0, -0.8])):
        ax.text(0.2, machines_y + y_off, job, ha='center', va='center',
                fontsize=7, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', facecolor=GRAY1, edgecolor=LN))
        # Dashed flow line
        ax.annotate("", xy=(5.5, machines_y + y_off * 0.3),
                    xytext=(0.5, machines_y + y_off),
                    arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8,
                                   linestyle='dashed'))

    ax.text(3, 1.2, 'Wszystkie zadania:\nM1 → M2 → M3',
            ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    ax.text(3, 0.4, 'Jak taśma montażowa',
            ha='center', fontsize=7, style='italic', color='#666666')

    # --- RIGHT: Job Shop ---
    ax = axes[1]
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Job Shop (Jm)', fontsize=10, fontweight='bold', pad=8)

    # Machines scattered
    m_positions = [(1.5, 4.2), (4.5, 4.2), (3, 2.5)]

    for i, (mx, my) in enumerate(m_positions):
        circle = plt.Circle((mx, my), mach_r,
                            facecolor=GRAY2, edgecolor=LN, lw=1.5)
        ax.add_patch(circle)
        ax.text(mx, my, f'M{i+1}', ha='center', va='center',
                fontsize=9, fontweight='bold')

    # J1: M1 → M2 → M3 (solid)
    route1 = [(1.5, 4.2), (4.5, 4.2), (3, 2.5)]
    for i in range(len(route1) - 1):
        x1, y1 = route1[i]
        x2, y2 = route1[i+1]
        dx = x2 - x1
        dy = y2 - y1
        d = (dx**2 + dy**2)**0.5
        draw_arrow(ax, x1 + mach_r * dx/d + 0.05, y1 + mach_r * dy/d,
                   x2 - mach_r * dx/d - 0.05, y2 - mach_r * dy/d,
                   lw=1.5)
    ax.text(0.3, 4.8, 'J1: M1→M2→M3', fontsize=7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.1', facecolor=GRAY1, edgecolor=LN))

    # J2: M2 → M3 → M1 (dashed)
    route2 = [(4.5, 4.2), (3, 2.5), (1.5, 4.2)]
    for i in range(len(route2) - 1):
        x1, y1 = route2[i]
        x2, y2 = route2[i+1]
        dx = x2 - x1
        dy = y2 - y1
        d = (dx**2 + dy**2)**0.5
        off = 0.15  # offset to avoid overlap
        ax.annotate("", xy=(x2 - mach_r * dx/d - 0.05, y2 - mach_r * dy/d + off),
                    xytext=(x1 + mach_r * dx/d + 0.05, y1 + mach_r * dy/d + off),
                    arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5,
                                   linestyle='dashed'))
    ax.text(3.8, 5.2, 'J2: M2→M3→M1', fontsize=7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.1', facecolor=GRAY4, edgecolor=LN))

    ax.text(3, 1.2, 'Każde zadanie:\nwłasna trasa!',
            ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    ax.text(3, 0.4, 'NP-trudny już dla 3 maszyn',
            ha='center', fontsize=7, style='italic', color='#666666')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'scheduling_flow_vs_job.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ scheduling_flow_vs_job.png")


# ============================================================
# 5. SCHEDULING COMPLEXITY LANDSCAPE
# ============================================================
def draw_complexity_map():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Złożoność problemów szeregowania — od łatwych do NP-trudnych',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Gradient arrow at the top
    ax.annotate("", xy=(9.5, 6.2), xytext=(0.5, 6.2),
                arrowprops=dict(arrowstyle='->', color=LN, lw=2))
    ax.text(5, 6.5, 'Rosnąca złożoność', ha='center', fontsize=9,
            fontweight='bold')

    # Easy (polynomial) region
    easy_rect = FancyBboxPatch((0.3, 2.8), 4.0, 3.0,
                                boxstyle="round,pad=0.15",
                                lw=1.5, edgecolor='#666666',
                                facecolor=GRAY4, linestyle='-')
    ax.add_patch(easy_rect)
    ax.text(2.3, 5.5, 'WIELOMIANOWE  O(n log n)', ha='center',
            fontsize=9, fontweight='bold', color='#444444')

    easy_problems = [
        ('1 || ΣCⱼ', 'SPT', GRAY1, 4.8),
        ('1 || Lmax', 'EDD', GRAY2, 4.0),
        ('F2 || Cmax', 'Johnson', GRAY1, 3.2),
    ]
    for prob, method, fill, y in easy_problems:
        rect = FancyBboxPatch((0.6, y), 3.5, 0.6,
                              boxstyle="round,pad=0.05",
                              lw=1, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(1.2, y + 0.3, prob, ha='center', va='center',
                fontsize=8, fontweight='bold', fontfamily='monospace')
        ax.text(3.0, y + 0.3, f'→ {method}', ha='center', va='center',
                fontsize=8)

    # Hard (NP) region
    hard_rect = FancyBboxPatch((5.3, 2.8), 4.3, 3.0,
                                boxstyle="round,pad=0.15",
                                lw=1.5, edgecolor='#444444',
                                facecolor=GRAY3, linestyle='-')
    ax.add_patch(hard_rect)
    ax.text(7.45, 5.5, 'NP-TRUDNE', ha='center',
            fontsize=9, fontweight='bold', color='#333333')

    hard_problems = [
        ('Pm || Cmax\n(m≥2)', 'LPT heuryst.', GRAY2, 4.5),
        ('1 || ΣTⱼ', 'branch&bound', GRAY4, 3.7),
        ('Jm || Cmax\n(m≥3)', 'metaheuryst.', GRAY5, 2.9),
    ]
    for prob, method, fill, y in hard_problems:
        rect = FancyBboxPatch((5.6, y), 3.7, 0.7,
                              boxstyle="round,pad=0.05",
                              lw=1, edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(6.5, y + 0.35, prob, ha='center', va='center',
                fontsize=7, fontweight='bold', fontfamily='monospace')
        ax.text(8.2, y + 0.35, f'→ {method}', ha='center', va='center',
                fontsize=7)

    # Arrow connecting
    draw_arrow(ax, 4.4, 4.0, 5.2, 4.0, lw=2, color='#888888')
    ax.text(4.8, 4.25, '+1\nmaszyna', ha='center', fontsize=6, color='#888888')

    # Bottom: key insight
    ax.text(5.0, 1.8, '„Dodanie jednej maszyny lub jednego ograniczenia\n'
                       'może zmienić problem z łatwego na NP-trudny!"',
            ha='center', fontsize=8, fontweight='bold', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3, lw=1))

    # Bottom examples
    ax.text(5.0, 0.8,
            '1 maszyna → łatwe (sortuj)  |  ≥2 maszyny równoległe → NP-trudne\n'
            'Flow shop 2 maszyny → Johnson O(n log n)  |  Flow shop 3 maszyny → NP-trudne',
            ha='center', fontsize=7, color='#555555')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'scheduling_complexity_map.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ scheduling_complexity_map.png")


# ============================================================
# 6. EDD EXAMPLE (1 || Lmax)
# ============================================================
def draw_edd_example():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 4))
    ax.set_xlim(-2, 28)
    ax.set_ylim(-2, 4)
    ax.axis('off')
    ax.set_title('EDD (Earliest Due Date) — 1 || Lmax  — Przykład',
                 fontsize=FS_TITLE, fontweight='bold', pad=8)

    # Tasks: name, processing time, due date
    tasks = [('J1', 4, 10), ('J2', 2, 6), ('J3', 6, 15), ('J4', 3, 8), ('J5', 5, 18)]
    # EDD: sort by due date
    edd_order = sorted(tasks, key=lambda x: x[2])

    bar_y = 1.5
    bar_h = 0.8
    t = 0
    fills_edd = [GRAY1, GRAY2, GRAY4, GRAY3, GRAY5]

    lateness_vals = []
    for i, (name, p, d) in enumerate(edd_order):
        rect = mpatches.Rectangle((t, bar_y), p, bar_h,
                                   lw=1.2, edgecolor=LN, facecolor=fills_edd[i])
        ax.add_patch(rect)
        ax.text(t + p/2, bar_y + bar_h/2, f'{name}\np={p}, d={d}',
                ha='center', va='center', fontsize=6.5, fontweight='bold')
        t += p
        L = t - d
        lateness_vals.append(L)

        # Due date marker
        ax.plot([d, d], [bar_y - 0.4, bar_y - 0.1], color='#888888',
                lw=0.8, linestyle='--')
        ax.text(d, bar_y - 0.5, f'd={d}', ha='center', va='top',
                fontsize=5.5, color='#888888')

        # Completion + lateness
        ax.plot([t, t], [bar_y + bar_h, bar_y + bar_h + 0.15], color=LN, lw=0.8)
        ax.text(t, bar_y + bar_h + 0.2, f'C={t}\nL={L}',
                ha='center', va='bottom', fontsize=5.5)

    # Time axis
    ax.plot([0, 22], [bar_y - 0.05, bar_y - 0.05], color=LN, lw=0.5)

    Lmax = max(lateness_vals)
    ax.text(22, bar_y + bar_h/2, f'Lmax = {Lmax}',
            ha='left', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY1, edgecolor=LN))

    # Bottom mnemonic
    ax.text(10, -1.3, '„Early Due Date Does it first" — najpilniejszy deadline idzie pierwszy',
            ha='center', fontsize=8, fontweight='bold', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3, lw=0.8))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'scheduling_edd_example.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ scheduling_edd_example.png")


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Generating scheduling diagrams for PYTANIE 17...")
    draw_graham_notation()
    draw_johnson_gantt()
    draw_spt_comparison()
    draw_flow_vs_job()
    draw_complexity_map()
    draw_edd_example()
    print("Done! All diagrams saved to:", OUTPUT_DIR)
