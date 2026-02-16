#!/usr/bin/env python3
"""
Generate diagrams for PYTANIE 1: Automata and language classes.
  1. FA recognition example — DFA for strings ending in "ab"
  2. PDA recognition example — PDA for aⁿbⁿ
  3. LBA recognition example — LBA for aⁿbⁿcⁿ
  4. TM recognition example — TM for 0ⁿ1ⁿ

All: A4-compatible, B&W, 300 DPI, laser-printer-friendly.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import os

DPI = 300
BG = 'white'
LN = 'black'
FS = 8
FS_TITLE = 11
FS_SMALL = 6.5
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRAY1 = '#E8E8E8'
GRAY2 = '#D0D0D0'
GRAY3 = '#B8B8B8'
GRAY4 = '#F5F5F5'
GRAY5 = '#C0C0C0'
LIGHT_GREEN = '#D5E8D4'
LIGHT_RED = '#F8D7DA'
LIGHT_BLUE = '#D6EAF8'
LIGHT_YELLOW = '#FFF9C4'


def draw_state_circle(ax, x, y, r, label, accepting=False, initial=False,
                      fillcolor='white', fontsize=FS):
    """Draw an automaton state circle."""
    circle = plt.Circle((x, y), r, fill=True, facecolor=fillcolor,
                        edgecolor=LN, linewidth=1.5, zorder=3)
    ax.add_patch(circle)
    if accepting:
        inner = plt.Circle((x, y), r * 0.82, fill=False,
                           edgecolor=LN, linewidth=1.2, zorder=3)
        ax.add_patch(inner)
    if initial:
        ax.annotate("", xy=(x - r, y), xytext=(x - r - 0.4, y),
                    arrowprops=dict(arrowstyle='->', color=LN, lw=1.5),
                    zorder=4)
    ax.text(x, y, label, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', zorder=5)


def draw_curved_arrow(ax, x1, y1, x2, y2, label, r=0.25,
                      connectionstyle="arc3,rad=0.3", fontsize=FS_SMALL,
                      label_offset=(0, 0)):
    """Draw a curved arrow between points with label."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=LN, lw=1.2,
                                connectionstyle=connectionstyle),
                zorder=2)
    mx = (x1 + x2) / 2 + label_offset[0]
    my = (y1 + y2) / 2 + label_offset[1]
    ax.text(mx, my, label, ha='center', va='center', fontsize=fontsize,
            fontstyle='italic', zorder=5,
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                      edgecolor='none', alpha=0.9))


def draw_self_loop(ax, x, y, r, label, direction='top', fontsize=FS_SMALL):
    """Draw a self-loop on a state."""
    if direction == 'top':
        loop = mpatches.FancyArrowPatch(
            (x - 0.12, y + r), (x + 0.12, y + r),
            connectionstyle="arc3,rad=-1.8",
            arrowstyle='->', mutation_scale=12, lw=1.2, color=LN, zorder=2)
        ax.add_patch(loop)
        ax.text(x, y + r + 0.35, label, ha='center', va='center',
                fontsize=fontsize, fontstyle='italic', zorder=5)
    elif direction == 'bottom':
        loop = mpatches.FancyArrowPatch(
            (x - 0.12, y - r), (x + 0.12, y - r),
            connectionstyle="arc3,rad=1.8",
            arrowstyle='->', mutation_scale=12, lw=1.2, color=LN, zorder=2)
        ax.add_patch(loop)
        ax.text(x, y - r - 0.35, label, ha='center', va='center',
                fontsize=fontsize, fontstyle='italic', zorder=5)


# ============================================================
# 1. FA Recognition Example — DFA for strings ending in "ab"
# ============================================================
def draw_fa_recognition():
    """FA state diagram + step-by-step trace for 'baab'."""
    fig, axes = plt.subplots(1, 2, figsize=(11.69, 4),
                             gridspec_kw={'width_ratios': [1, 1.3]})

    # --- Left: State diagram ---
    ax = axes[0]
    ax.set_xlim(-1, 5.5)
    ax.set_ylim(-1.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('DFA — diagram stanów\nL = {słowa nad {a,b} kończące się na "ab"}',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    R = 0.35
    # States positions
    states = {'q₀': (0.8, 0.5), 'q₁': (2.8, 0.5), 'q₂': (4.8, 0.5)}

    draw_state_circle(ax, *states['q₀'], R, 'q₀', initial=True)
    draw_state_circle(ax, *states['q₁'], R, 'q₁')
    draw_state_circle(ax, *states['q₂'], R, 'q₂', accepting=True,
                      fillcolor=LIGHT_GREEN)

    # Transitions
    # q₀ --a--> q₁
    draw_curved_arrow(ax, states['q₀'][0] + R, states['q₀'][1] + 0.05,
                      states['q₁'][0] - R, states['q₁'][1] + 0.05,
                      'a', connectionstyle="arc3,rad=0.15",
                      label_offset=(0, 0.25))
    # q₁ --b--> q₂
    draw_curved_arrow(ax, states['q₁'][0] + R, states['q₁'][1] + 0.05,
                      states['q₂'][0] - R, states['q₂'][1] + 0.05,
                      'b', connectionstyle="arc3,rad=0.15",
                      label_offset=(0, 0.25))
    # q₂ --a--> q₁
    draw_curved_arrow(ax, states['q₂'][0] - R, states['q₂'][1] - 0.05,
                      states['q₁'][0] + R, states['q₁'][1] - 0.05,
                      'a', connectionstyle="arc3,rad=0.15",
                      label_offset=(0, -0.3))
    # q₂ --b--> q₀
    draw_curved_arrow(ax, states['q₂'][0] - 0.2, states['q₂'][1] - R,
                      states['q₀'][0] + 0.2, states['q₀'][1] - R,
                      'b', connectionstyle="arc3,rad=0.4",
                      label_offset=(0, -0.4))
    # q₀ --b--> q₀ (self-loop)
    draw_self_loop(ax, *states['q₀'], R, 'b', direction='top')
    # q₁ --a--> q₁ (self-loop)
    draw_self_loop(ax, *states['q₁'], R, 'a', direction='top')

    # Legend
    ax.text(0.3, -1.0, '→ = start    ◎ = akceptujący',
            fontsize=FS_SMALL, ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    # --- Right: Step-by-step trace ---
    ax2 = axes[1]
    ax2.axis('off')
    ax2.set_title('Ślad wykonania — wejście: "baab"',
                  fontsize=FS_TITLE, fontweight='bold', pad=10)

    trace_data = [
        ['Krok', 'Czytam', 'Stan przed', 'Przejście', 'Stan po'],
        ['—', '—', 'q₀ (start)', '—', 'q₀'],
        ['1', 'b', 'q₀', 'δ(q₀, b) = q₀', 'q₀'],
        ['2', 'a', 'q₀', 'δ(q₀, a) = q₁', 'q₁'],
        ['3', 'a', 'q₁', 'δ(q₁, a) = q₁', 'q₁'],
        ['4', 'b', 'q₁', 'δ(q₁, b) = q₂', 'q₂ ✓'],
    ]

    colors = [GRAY2] + ['white'] * 4 + [LIGHT_GREEN]
    table = ax2.table(cellText=trace_data, cellLoc='center',
                      loc='center', bbox=[0.05, 0.15, 0.9, 0.75])
    table.auto_set_font_size(False)
    table.set_fontsize(FS)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(GRAY3)
        if row == 0:
            cell.set_facecolor(GRAY2)
            cell.set_text_props(fontweight='bold')
        else:
            cell.set_facecolor(colors[row])
        cell.set_height(0.12)

    ax2.text(0.5, 0.05, 'Wynik: q₂ ∈ F → "baab" AKCEPTOWANE ✓',
             ha='center', va='center', fontsize=FS + 1, fontweight='bold',
             transform=ax2.transAxes,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_GREEN,
                       edgecolor=LN))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fa_recognition_example.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ fa_recognition_example.png")


# ============================================================
# 2. PDA Recognition Example — PDA for aⁿbⁿ
# ============================================================
def draw_pda_recognition():
    """PDA state diagram + step-by-step trace with stack visualization for 'aabb'."""
    fig, axes = plt.subplots(1, 2, figsize=(11.69, 5.5),
                             gridspec_kw={'width_ratios': [1, 1.4]})

    # --- Left: State diagram ---
    ax = axes[0]
    ax.set_xlim(-1, 5.5)
    ax.set_ylim(-2, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('PDA — diagram stanów\nL = {aⁿbⁿ | n ≥ 1}',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    R = 0.38
    states = {'q₀': (0.8, 0.5), 'q₁': (2.8, 0.5), 'q₂': (4.8, 0.5)}

    draw_state_circle(ax, *states['q₀'], R, 'q₀', initial=True)
    draw_state_circle(ax, *states['q₁'], R, 'q₁')
    draw_state_circle(ax, *states['q₂'], R, 'q₂', accepting=True,
                      fillcolor=LIGHT_GREEN)

    # q₀ --b,A/ε--> q₁
    draw_curved_arrow(ax, states['q₀'][0] + R, states['q₀'][1],
                      states['q₁'][0] - R, states['q₁'][1],
                      'b, A → ε\n(pop A)', connectionstyle="arc3,rad=0.0",
                      label_offset=(0, 0.4))
    # q₁ --ε,Z₀/Z₀--> q₂
    draw_curved_arrow(ax, states['q₁'][0] + R, states['q₁'][1],
                      states['q₂'][0] - R, states['q₂'][1],
                      'ε, Z₀ → Z₀\n(akceptuj)', connectionstyle="arc3,rad=0.0",
                      label_offset=(0, 0.45))
    # q₀ self-loop: a, Z₀/AZ₀ and a, A/AA
    draw_self_loop(ax, *states['q₀'], R, 'a, Z₀ → AZ₀\na, A → AA\n(push A)',
                   direction='top')
    # q₁ self-loop: b, A/ε
    draw_self_loop(ax, *states['q₁'], R, 'b, A → ε\n(pop A)', direction='top')

    # Key explanation
    ax.text(0.3, -1.3, 'Notacja: symbol_wejścia, szczyt_stosu → nowy_szczyt\n'
            'ε = brak symbolu (przejście spontaniczne lub pusty stos)',
            fontsize=FS_SMALL, ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    # --- Right: Step trace with stack ---
    ax2 = axes[1]
    ax2.axis('off')
    ax2.set_title('Ślad wykonania z wizualizacją stosu — wejście: "aabb"',
                  fontsize=FS_TITLE, fontweight='bold', pad=10)

    trace_data = [
        ['Krok', 'Czytam', 'Stan', 'Stos (szczyt→)', 'Operacja'],
        ['start', '—', 'q₀', '[Z₀]', '—'],
        ['1', 'a', 'q₀', '[A, Z₀]', 'push A'],
        ['2', 'a', 'q₀', '[A, A, Z₀]', 'push A'],
        ['3', 'b', 'q₁', '[A, Z₀]', 'pop A'],
        ['4', 'b', 'q₁', '[Z₀]', 'pop A'],
        ['5', 'ε', 'q₂', '[Z₀]', 'akceptuj!'],
    ]

    colors = [GRAY2, 'white', LIGHT_BLUE, LIGHT_BLUE, LIGHT_YELLOW, LIGHT_YELLOW, LIGHT_GREEN]
    table = ax2.table(cellText=trace_data, cellLoc='center',
                      loc='center', bbox=[0.02, 0.08, 0.96, 0.82])
    table.auto_set_font_size(False)
    table.set_fontsize(FS)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(GRAY3)
        if row == 0:
            cell.set_facecolor(GRAY2)
            cell.set_text_props(fontweight='bold')
        else:
            cell.set_facecolor(colors[row])
        cell.set_height(0.11)

    ax2.text(0.5, 0.0, 'Wynik: q₂ ∈ F, stos=[Z₀] → "aabb" AKCEPTOWANE ✓\n'
             'Intuicja: 2× push A (za "aa") + 2× pop A (za "bb") = stos pusty = OK',
             ha='center', va='center', fontsize=FS, fontweight='bold',
             transform=ax2.transAxes,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_GREEN,
                       edgecolor=LN))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'pda_recognition_example.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ pda_recognition_example.png")


# ============================================================
# 3. LBA Recognition Example — LBA for aⁿbⁿcⁿ
# ============================================================
def draw_lba_recognition():
    """LBA tape visualization showing marking rounds for 'aabbcc'."""
    fig, ax = plt.subplots(1, 1, figsize=(11.69, 6.5))
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-1, 10.5)
    ax.axis('off')
    ax.set_title('LBA — rozpoznawanie aⁿbⁿcⁿ (n=2)\n'
                 'Strategia: w każdej rundzie zaznacz jedno a, b, c',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    CELL_W = 0.9
    CELL_H = 0.7
    TAPE_X0 = 1.5
    HEAD_COLOR = '#FFD700'

    def draw_tape(y, cells, head_pos, label, step_label=""):
        """Draw a tape row with cells, head position highlighted."""
        ax.text(0.2, y + CELL_H/2, label, ha='right', va='center',
                fontsize=FS, fontweight='bold')
        for i, (sym, color) in enumerate(cells):
            x = TAPE_X0 + i * CELL_W
            fc = HEAD_COLOR if i == head_pos else color
            rect = mpatches.FancyBboxPatch((x, y), CELL_W, CELL_H,
                                           boxstyle="round,pad=0.03",
                                           lw=1.2, edgecolor=LN, facecolor=fc)
            ax.add_patch(rect)
            ax.text(x + CELL_W/2, y + CELL_H/2, sym,
                    ha='center', va='center', fontsize=FS + 2,
                    fontweight='bold' if sym in ('X', 'Y', 'Z') else 'normal',
                    family='monospace')
        if head_pos is not None:
            hx = TAPE_X0 + head_pos * CELL_W + CELL_W/2
            ax.annotate('▼', xy=(hx, y + CELL_H), xytext=(hx, y + CELL_H + 0.25),
                        ha='center', va='bottom', fontsize=8, color='black')
        if step_label:
            sx = TAPE_X0 + 6 * CELL_W + 0.5
            ax.text(sx, y + CELL_H/2, step_label, ha='left', va='center',
                    fontsize=FS_SMALL,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4,
                              edgecolor=GRAY3))

    W = 'white'
    MK = GRAY1  # marked cell color

    # Row 1: Initial tape
    y = 9.0
    draw_tape(y, [('a', W), ('a', W), ('b', W), ('b', W), ('c', W), ('c', W)],
              0, 'Początek', 'taśma = [a, a, b, b, c, c], głowica na 0')

    # Row 2: After marking first 'a'
    y = 7.8
    draw_tape(y, [('X', MK), ('a', W), ('b', W), ('b', W), ('c', W), ('c', W)],
              1, 'R1, krok 1', 'zaznacz a→X, szukaj b')

    # Row 3: After marking first 'b'
    y = 6.6
    draw_tape(y, [('X', MK), ('a', W), ('Y', MK), ('b', W), ('c', W), ('c', W)],
              3, 'R1, krok 2', 'zaznacz b→Y, szukaj c')

    # Row 4: After marking first 'c'
    y = 5.4
    draw_tape(y, [('X', MK), ('a', W), ('Y', MK), ('b', W), ('Z', MK), ('c', W)],
              0, 'R1, krok 3', 'zaznacz c→Z, wróć na początek')

    # Runda 2 header
    y = 4.5
    ax.text(TAPE_X0 + 3 * CELL_W, y + 0.3, '═══ RUNDA 2 ═══',
            ha='center', va='center', fontsize=FS, fontweight='bold',
            color=LN)

    # Row 5: After marking second 'a'
    y = 3.6
    draw_tape(y, [('X', MK), ('X', MK), ('Y', MK), ('b', W), ('Z', MK), ('c', W)],
              2, 'R2, krok 1', 'pomiń X, zaznacz a→X, szukaj b')

    # Row 6: After marking second 'b'
    y = 2.4
    draw_tape(y, [('X', MK), ('X', MK), ('Y', MK), ('Y', MK), ('Z', MK), ('c', W)],
              4, 'R2, krok 2', 'pomiń Y, zaznacz b→Y, szukaj c')

    # Row 7: After marking second 'c'
    y = 1.2
    draw_tape(y, [('X', MK), ('X', MK), ('Y', MK), ('Y', MK), ('Z', MK), ('Z', MK)],
              None, 'R2, krok 3', 'zaznacz c→Z, wróć na początek')

    # Result
    y = 0.0
    ax.text(TAPE_X0 + 3 * CELL_W, y + 0.3,
            'Wszystko zaznaczone → q_acc → "aabbcc" AKCEPTOWANE ✓',
            ha='center', va='center', fontsize=FS + 1, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_GREEN,
                      edgecolor=LN))

    # Key
    ax.text(TAPE_X0 + 6 * CELL_W + 0.5, y + 0.3,
            'Ograniczenie LBA:\ngłowica ≤ 6 komórek\n(= |w| = |"aabbcc"|)',
            ha='left', va='center', fontsize=FS_SMALL,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_YELLOW,
                      edgecolor=GRAY3))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'lba_recognition_example.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ lba_recognition_example.png")


# ============================================================
# 4. TM Recognition Example — TM for 0ⁿ1ⁿ
# ============================================================
def draw_tm_recognition():
    """TM tape visualization for 0ⁿ1ⁿ with infinite tape shown."""
    fig, ax = plt.subplots(1, 1, figsize=(11.69, 6.5))
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-1, 10.5)
    ax.axis('off')
    ax.set_title('TM — rozpoznawanie 0ⁿ1ⁿ (n=2)\n'
                 'Strategia: zaznacz jedno 0 i jedno 1 w każdej rundzie',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    CELL_W = 0.9
    CELL_H = 0.7
    TAPE_X0 = 1.5
    HEAD_COLOR = '#FFD700'

    def draw_tape(y, cells, head_pos, label, step_label=""):
        ax.text(0.2, y + CELL_H/2, label, ha='right', va='center',
                fontsize=FS, fontweight='bold')
        for i, (sym, color) in enumerate(cells):
            x = TAPE_X0 + i * CELL_W
            fc = HEAD_COLOR if i == head_pos else color
            lw = 1.2
            ls = '-'
            if sym == '⊔':
                ls = '--'
            rect = mpatches.FancyBboxPatch((x, y), CELL_W, CELL_H,
                                           boxstyle="round,pad=0.03",
                                           lw=lw, edgecolor=LN, facecolor=fc,
                                           linestyle=ls)
            ax.add_patch(rect)
            ax.text(x + CELL_W/2, y + CELL_H/2, sym,
                    ha='center', va='center', fontsize=FS + 2,
                    fontweight='bold' if sym in ('X', 'Y') else 'normal',
                    family='monospace',
                    color=GRAY3 if sym == '⊔' else LN)
        # ∞ arrow
        last_x = TAPE_X0 + len(cells) * CELL_W
        ax.annotate('→ ∞', xy=(last_x + 0.3, y + CELL_H/2),
                    fontsize=FS, ha='left', va='center', color=GRAY3)
        if head_pos is not None:
            hx = TAPE_X0 + head_pos * CELL_W + CELL_W/2
            ax.annotate('▼', xy=(hx, y + CELL_H), xytext=(hx, y + CELL_H + 0.25),
                        ha='center', va='bottom', fontsize=8, color='black')
        if step_label:
            sx = TAPE_X0 + 8 * CELL_W + 0.8
            ax.text(sx, y + CELL_H/2, step_label, ha='left', va='center',
                    fontsize=FS_SMALL,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4,
                              edgecolor=GRAY3))

    W = 'white'
    MK = GRAY1
    BL = '#F0F0F0'  # blank cell

    # Row 1: Initial
    y = 9.0
    draw_tape(y, [('0', W), ('0', W), ('1', W), ('1', W), ('⊔', BL), ('⊔', BL), ('⊔', BL)],
              0, 'Początek', 'taśma = [0,0,1,1,⊔,⊔,...∞]')

    # Row 2: Mark first 0
    y = 7.8
    draw_tape(y, [('X', MK), ('0', W), ('1', W), ('1', W), ('⊔', BL), ('⊔', BL), ('⊔', BL)],
              1, 'R1, krok 1', 'zaznacz 0→X, idź w prawo')

    # Row 3: Skip to first 1, mark it
    y = 6.6
    draw_tape(y, [('X', MK), ('0', W), ('Y', MK), ('1', W), ('⊔', BL), ('⊔', BL), ('⊔', BL)],
              0, 'R1, krok 2', 'zaznacz 1→Y, wróć na początek')

    # Runda 2 header
    y = 5.8
    ax.text(TAPE_X0 + 3.5 * CELL_W, y + 0.3, '═══ RUNDA 2 ═══',
            ha='center', va='center', fontsize=FS, fontweight='bold')

    # Row 4: Mark second 0
    y = 4.8
    draw_tape(y, [('X', MK), ('X', MK), ('Y', MK), ('1', W), ('⊔', BL), ('⊔', BL), ('⊔', BL)],
              2, 'R2, krok 1', 'pomiń X, zaznacz 0→X')

    # Row 5: Mark second 1
    y = 3.6
    draw_tape(y, [('X', MK), ('X', MK), ('Y', MK), ('Y', MK), ('⊔', BL), ('⊔', BL), ('⊔', BL)],
              0, 'R2, krok 2', 'pomiń Y, zaznacz 1→Y, wróć')

    # Row 6: Check — all marked
    y = 2.4
    draw_tape(y, [('X', MK), ('X', MK), ('Y', MK), ('Y', MK), ('⊔', BL), ('⊔', BL), ('⊔', BL)],
              None, 'Sprawdzenie', 'brak niezaznaczonych → q_acc')

    # Result + TM vs LBA comparison
    y = 0.8
    ax.text(TAPE_X0 + 3.5 * CELL_W, y + 0.3,
            '"0011" AKCEPTOWANE ✓',
            ha='center', va='center', fontsize=FS + 1, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_GREEN,
                      edgecolor=LN))

    y = -0.3
    ax.text(TAPE_X0 + 3.5 * CELL_W, y + 0.3,
            'Różnica TM vs LBA: taśma TM jest nieskończona (⊔ → ∞)\n'
            'LBA: głowica ograniczona do |w| komórek\n'
            'TM: głowica może wyjść POZA wejście i pisać na pustych ⊔',
            ha='center', va='center', fontsize=FS_SMALL,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_YELLOW,
                      edgecolor=GRAY3))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'tm_recognition_example.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ tm_recognition_example.png")


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating automata diagrams for PYTANIE 1...")
    draw_fa_recognition()
    draw_pda_recognition()
    draw_lba_recognition()
    draw_tm_recognition()
    print(f"\nAll diagrams saved to {OUTPUT_DIR}/")
