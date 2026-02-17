#!/usr/bin/env python3
"""
Generate diagrams for PYTANIE 15: Agent upostaciowiony w robotyce.

Diagrams:
  1. See-Think-Act cycle of an embodied agent
  2. 3T Architecture (Planner / Sequencer / Controller)
  3. Behavior Tree example (robot pick-and-place)
  4. BDI model flow

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


def draw_arrow(ax, x1, y1, x2, y2, lw=1.2, style='->', color=LN, label='', label_offset=0.12):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + label_offset
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=6.5, color=color)


def draw_dashed_arrow(ax, x1, y1, x2, y2, lw=1.0, color=LN, label='', label_offset=0.12):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                linestyle='dashed'))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + label_offset
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=6.5, color=color)


# ─── DIAGRAM 1: See-Think-Act Cycle ──────────────────────────────
def draw_see_think_act():
    fig, ax = plt.subplots(1, 1, figsize=(7, 4.5), facecolor=BG)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 4.5)
    ax.axis('off')
    ax.set_title("Cykl agenta upostaciowionego: Percepcja → Deliberacja → Akcja",
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Environment box (large background)
    env_rect = FancyBboxPatch((0.2, 0.2), 6.6, 1.0, boxstyle="round,pad=0.08",
                               lw=1.5, edgecolor=LN, facecolor=GRAY1,
                               linestyle='--')
    ax.add_patch(env_rect)
    ax.text(3.5, 0.7, "ŚRODOWISKO FIZYCZNE\n(przeszkody, obiekty, ludzie)",
            ha='center', va='center', fontsize=FS, fontstyle='italic')

    # Agent body (large rounded box)
    agent_rect = FancyBboxPatch((0.5, 1.5), 6.0, 2.6, boxstyle="round,pad=0.1",
                                 lw=2.0, edgecolor=LN, facecolor=GRAY4)
    ax.add_patch(agent_rect)
    ax.text(3.5, 3.85, "AGENT UPOSTACIOWIONY (robot)", ha='center', va='center',
            fontsize=9, fontweight='bold')

    # Three main phases
    bw = 1.4
    bh = 0.7
    by = 2.2

    # SEE
    draw_box(ax, 0.8, by, bw, bh, "SEE\n(Percepcja)", fill=GRAY2,
             fontsize=8, fontweight='bold')
    ax.text(1.5, by - 0.2, "kamery, LIDAR\nczujniki dotyku", ha='center',
            va='top', fontsize=6, fontstyle='italic')

    # THINK
    draw_box(ax, 2.8, by, bw, bh, "THINK\n(Deliberacja)", fill=GRAY3,
             fontsize=8, fontweight='bold')
    ax.text(3.5, by - 0.2, "planowanie trasy\nmodel BDI", ha='center',
            va='top', fontsize=6, fontstyle='italic')

    # ACT
    draw_box(ax, 4.8, by, bw, bh, "ACT\n(Akcja)", fill=GRAY2,
             fontsize=8, fontweight='bold')
    ax.text(5.5, by - 0.2, "silniki, chwytaki\nkomendy PWM", ha='center',
            va='top', fontsize=6, fontstyle='italic')

    # Arrows between phases
    draw_arrow(ax, 0.8 + bw, by + bh/2, 2.8, by + bh/2, lw=1.5,
               label='dane sensoryczne')
    draw_arrow(ax, 2.8 + bw, by + bh/2, 4.8, by + bh/2, lw=1.5,
               label='komendy sterujące')

    # Arrows to/from environment
    draw_arrow(ax, 1.5, 1.2, 1.5, by, lw=1.3, label='odczyt', label_offset=0.08)
    draw_arrow(ax, 5.5, by, 5.5, 1.2, lw=1.3, label='działanie', label_offset=0.08)

    # Feedback loop arrow (from ACT back to environment back to SEE)
    ax.annotate("", xy=(1.5, 1.15), xytext=(5.5, 1.15),
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1.0,
                                linestyle='dashed',
                                connectionstyle="arc3,rad=-0.15"))
    ax.text(3.5, 0.35, "← sprzężenie zwrotne (efekt akcji zmienia środowisko) →",
            ha='center', va='center', fontsize=6, color='#555555')

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'agent_see_think_act.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─── DIAGRAM 2: 3T Architecture ─────────────────────────────────
def draw_3t_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(7, 5.5), facecolor=BG)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_title("Architektura 3T sterownika robota (3-Layer Architecture)",
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    layers = [
        {"y": 4.0, "name": "WARSTWA 3: PLANNER\n(Deliberacja)",
         "time": "sekundy \u2013 minuty", "fill": GRAY1,
         "example": 'Cel: "Jed\u017a do kuchni po kubek"\nPlanowanie trasy A \u2192 B \u2192 C',
         "tech": "Planowanie symboliczne\nA*, graf zada\u0144"},
        {"y": 2.6, "name": "WARSTWA 2: SEQUENCER\n(Wykonawca)",
         "time": "100 ms \u2013 sekundy", "fill": GRAY2,
         "example": "Sekwencja: Jed\u017a do drzwi \u2192\nOtw\u00f3rz \u2192 Jed\u017a do blatu \u2192 Chwy\u0107",
         "tech": "FSM, Behavior Trees\nkoordynacja zachowa\u0144"},
        {"y": 1.2, "name": "WARSTWA 1: CONTROLLER\n(Reaktywny)",
         "time": "milisekundy", "fill": GRAY3,
         "example": "PID: utrzymaj pr\u0119dko\u015b\u0107 0.5 m/s\nUnikaj kolizji (emergency stop)",
         "tech": "PID, regulacja\nbezpo\u015brednie I/O"},
    ]

    bw = 4.0
    bh = 0.85

    for i, layer in enumerate(layers):
        y = layer["y"]
        # Main layer box
        draw_box(ax, 0.3, y, bw, bh, layer["name"], fill=layer["fill"],
                 fontsize=8, fontweight='bold')

        # Time label (left)
        ax.text(0.15, y + bh/2, layer["time"], ha='right', va='center',
                fontsize=6, fontstyle='italic', rotation=0,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=LN, lw=0.5))

        # Example (right side)
        draw_box(ax, 4.5, y, 2.3, bh, layer["example"], fill='white',
                 fontsize=6.5)

        # Technology used
        # ax.text(4.5 + 1.15, y - 0.12, layer["tech"], ha='center', va='top',
        #         fontsize=5.5, fontstyle='italic', color='#555555')

    # Arrows between layers (downward = commands, upward = status)
    for i in range(len(layers) - 1):
        y_top = layers[i]["y"]
        y_bot = layers[i+1]["y"] + 0.85
        # Command arrow (down)
        draw_arrow(ax, 1.8, y_top, 1.8, y_bot, lw=1.3, label='polecenia ↓', label_offset=0.02)
        # Status arrow (up)
        draw_arrow(ax, 2.8, y_bot, 2.8, y_top, lw=1.0, style='->', color='#666666',
                   label='↑ status', label_offset=0.02)

    # Environment at bottom
    env_rect = FancyBboxPatch((0.3, 0.3), bw, 0.6, boxstyle="round,pad=0.05",
                               lw=1.5, edgecolor=LN, facecolor=GRAY4, linestyle='--')
    ax.add_patch(env_rect)
    ax.text(0.3 + bw/2, 0.6, "SPRZĘT: silniki, czujniki, efektory",
            ha='center', va='center', fontsize=7, fontstyle='italic')

    # Arrow from controller to hardware
    draw_arrow(ax, 2.3, 1.2, 2.3, 0.9, lw=1.3)

    # Abstraction label on the right
    ax.annotate("", xy=(6.9, 4.8), xytext=(6.9, 0.5),
                arrowprops=dict(arrowstyle='<->', color='#888888', lw=1.0))
    ax.text(6.95, 2.65, "abstrakcja", ha='left', va='center', fontsize=7,
            rotation=90, color='#888888')

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'agent_3t_architecture.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─── DIAGRAM 3: Behavior Tree Example ────────────────────────────
def draw_behavior_tree():
    fig, ax = plt.subplots(1, 1, figsize=(7.5, 4.5), facecolor=BG)
    ax.set_xlim(0, 7.5)
    ax.set_ylim(0, 4.5)
    ax.axis('off')
    ax.set_title("Behavior Tree: robot przenoszący obiekt (pick-and-place)",
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Node positions: (x, y, text, shape_type)
    # shape_type: 'seq' = sequence (→), 'sel' = selector (?), 'act' = action, 'cond' = condition

    def draw_bt_node(ax, x, y, text, ntype='act', w=1.0, h=0.45):
        """Draw a behavior tree node."""
        if ntype == 'seq':
            # Sequence = box with →
            rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.06", lw=1.5,
                                   edgecolor=LN, facecolor=GRAY2)
            ax.add_patch(rect)
            ax.text(x, y, f"→ {text}", ha='center', va='center',
                    fontsize=7, fontweight='bold')
        elif ntype == 'sel':
            # Selector = box with ?
            rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.06", lw=1.5,
                                   edgecolor=LN, facecolor=GRAY3)
            ax.add_patch(rect)
            ax.text(x, y, f"? {text}", ha='center', va='center',
                    fontsize=7, fontweight='bold')
        elif ntype == 'cond':
            # Condition = diamond-ish / oval with dashed border
            rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.06", lw=1.0,
                                   edgecolor=LN, facecolor='white',
                                   linestyle='--')
            ax.add_patch(rect)
            ax.text(x, y, text, ha='center', va='center',
                    fontsize=6.5, fontstyle='italic')
        else:  # action
            rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.06", lw=1.0,
                                   edgecolor=LN, facecolor=GRAY1)
            ax.add_patch(rect)
            ax.text(x, y, text, ha='center', va='center', fontsize=6.5)
        return x, y

    # Root: Sequence "Przenieś obiekt"
    root = draw_bt_node(ax, 3.75, 3.8, "Przenieś obiekt", 'seq', w=1.6)

    # Level 2 children
    find = draw_bt_node(ax, 1.2, 2.8, "Znajdź obiekt", 'sel', w=1.3)
    nav = draw_bt_node(ax, 3.75, 2.8, "Jedź do obiektu", 'act', w=1.3)
    pick = draw_bt_node(ax, 6.3, 2.8, "Chwyć i dostarcz", 'seq', w=1.4)

    # Arrows from root
    draw_arrow(ax, root[0], root[1] - 0.225, find[0], find[1] + 0.225, lw=1.0)
    draw_arrow(ax, root[0], root[1] - 0.225, nav[0], nav[1] + 0.225, lw=1.0)
    draw_arrow(ax, root[0], root[1] - 0.225, pick[0], pick[1] + 0.225, lw=1.0)

    # Level 3: children of "Znajdź obiekt" (selector)
    vis = draw_bt_node(ax, 0.55, 1.7, "Widzę\nobiekt?", 'cond', w=0.85, h=0.5)
    scan = draw_bt_node(ax, 1.85, 1.7, "Skanuj\notoczenie", 'act', w=0.85, h=0.5)
    draw_arrow(ax, find[0], find[1] - 0.225, vis[0], vis[1] + 0.25, lw=0.8)
    draw_arrow(ax, find[0], find[1] - 0.225, scan[0], scan[1] + 0.25, lw=0.8)

    # Level 3: children of "Chwyć i dostarcz" (sequence)
    grasp = draw_bt_node(ax, 5.4, 1.7, "Chwyć\nobject", 'act', w=0.85, h=0.5)
    deliver = draw_bt_node(ax, 6.5, 1.7, "Jedź do\ncelu", 'act', w=0.85, h=0.5)
    release = draw_bt_node(ax, 7.2, 1.7, "Puść", 'act', w=0.55, h=0.5)
    draw_arrow(ax, pick[0], pick[1] - 0.225, grasp[0], grasp[1] + 0.25, lw=0.8)
    draw_arrow(ax, pick[0], pick[1] - 0.225, deliver[0], deliver[1] + 0.25, lw=0.8)
    draw_arrow(ax, pick[0], pick[1] - 0.225, release[0], release[1] + 0.25, lw=0.8)

    # Legend
    leg_y = 0.5
    draw_bt_node(ax, 0.8, leg_y, "→ Sequence", 'seq', w=1.1, h=0.35)
    draw_bt_node(ax, 2.3, leg_y, "? Selector", 'sel', w=1.0, h=0.35)
    draw_bt_node(ax, 3.6, leg_y, "Akcja", 'act', w=0.8, h=0.35)
    draw_bt_node(ax, 4.8, leg_y, "Warunek", 'cond', w=0.8, h=0.35)

    ax.text(0.3, leg_y, "Legenda:", ha='left', va='center', fontsize=6.5,
            fontweight='bold')

    # Execution note
    ax.text(3.75, 0.05, "Wykonanie: od lewej do prawej. Sequence (→) = wszystkie po kolei. "
            "Selector (?) = pierwszy sukces.",
            ha='center', va='center', fontsize=6, fontstyle='italic', color='#555555')

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'agent_behavior_tree.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─── DIAGRAM 4: BDI Model ────────────────────────────────────────
def draw_bdi_model():
    fig, ax = plt.subplots(1, 1, figsize=(7, 4), facecolor=BG)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_title("Model BDI agenta (Beliefs–Desires–Intentions)",
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    bw = 1.6
    bh = 1.4

    # BELIEFS box
    draw_box(ax, 0.3, 1.3, bw, bh, "", fill=GRAY1, fontsize=8, fontweight='bold')
    ax.text(0.3 + bw/2, 1.3 + bh - 0.15, "BELIEFS", ha='center', va='top',
            fontsize=9, fontweight='bold')
    ax.text(0.3 + bw/2, 1.3 + bh/2 - 0.1,
            '(wiedza o \u015bwiecie)\n\n\u2022 mapa pokoju\n\u2022 pozycja robota\n\u2022 drzwi zamkni\u0119te\n\u2022 bateria: 45%',
            ha='center', va='center', fontsize=6.5)

    # DESIRES box
    draw_box(ax, 2.7, 1.3, bw, bh, "", fill=GRAY2, fontsize=8, fontweight='bold')
    ax.text(2.7 + bw/2, 1.3 + bh - 0.15, "DESIRES", ha='center', va='top',
            fontsize=9, fontweight='bold')
    ax.text(2.7 + bw/2, 1.3 + bh/2 - 0.1,
            "(cele agenta)\n\n• dostarczyć paczkę\n  do pokoju 5\n• naładować baterię\n• unikać kolizji",
            ha='center', va='center', fontsize=6.5)

    # INTENTIONS box
    draw_box(ax, 5.1, 1.3, bw, bh, "", fill=GRAY3, fontsize=8, fontweight='bold')
    ax.text(5.1 + bw/2, 1.3 + bh - 0.15, "INTENTIONS", ha='center', va='top',
            fontsize=9, fontweight='bold')
    ax.text(5.1 + bw/2, 1.3 + bh/2 - 0.1,
            "(aktualny plan)\n\n→ jedź do drzwi\n  bocznych\n→ otwórz drzwi\n→ wjedź do pokoju 5",
            ha='center', va='center', fontsize=6.5)

    # Arrows
    draw_arrow(ax, 0.3 + bw, 1.3 + bh/2 + 0.15, 2.7, 1.3 + bh/2 + 0.15, lw=1.3,
               label='informuje', label_offset=0.08)
    draw_arrow(ax, 2.7 + bw, 1.3 + bh/2 + 0.15, 5.1, 1.3 + bh/2 + 0.15, lw=1.3,
               label='filtruje → wybiera', label_offset=0.08)

    # Feedback from intentions back to beliefs (update)
    ax.annotate("", xy=(0.3 + bw/2, 1.3), xytext=(5.1 + bw/2, 1.3),
                arrowprops=dict(arrowstyle='->', color='#666666', lw=1.0,
                                linestyle='dashed',
                                connectionstyle="arc3,rad=0.3"))
    ax.text(3.5, 0.75, "aktualizacja wiedzy po wykonaniu akcji",
            ha='center', va='center', fontsize=6, fontstyle='italic', color='#666666')

    # Sensor input arrow
    draw_arrow(ax, 0.3 + bw/2, 3.5, 0.3 + bw/2, 1.3 + bh, lw=1.3,
               label='percepcja (sensory)', label_offset=0.05)
    ax.text(0.3 + bw/2, 3.55, "ŚRODOWISKO", ha='center', va='bottom',
            fontsize=7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=LN, lw=0.8))

    # Action output arrow
    draw_arrow(ax, 5.1 + bw/2, 1.3 + bh, 5.1 + bw/2, 3.5, lw=1.3,
               label='akcja (efektory)', label_offset=0.05)
    ax.text(5.1 + bw/2, 3.55, "EFEKTORY", ha='center', va='bottom',
            fontsize=7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=LN, lw=0.8))

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'agent_bdi_model.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─── MAIN ────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Generating PYTANIE 15 diagrams...")
    draw_see_think_act()
    draw_3t_architecture()
    draw_behavior_tree()
    draw_bdi_model()
    print("Done! All diagrams saved to", OUTPUT_DIR)
