#!/usr/bin/env python3
"""
Generate diagrams for:
  PYTANIE 9:  Processes & Threads (IPC mechanisms, deadlock, producer-consumer)
  PYTANIE 12: Network optimization models (Ford-Fulkerson, Hungarian, CPM, Kruskal, TSP, Min-cost flow)

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
FS = 8
FS_TITLE = 11
FS_SMALL = 6.5
FS_EDGE = 9
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
LIGHT_ORANGE = '#FFE0B2'


def draw_box(ax, x, y, w, h, text, fill='white', lw=1.2, fontsize=FS,
             fontweight='normal', ha='center', va='center', rounded=True, edgecolor=LN):
    if rounded:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              lw=lw, edgecolor=edgecolor, facecolor=fill)
    else:
        rect = mpatches.Rectangle((x, y), w, h, lw=lw, edgecolor=edgecolor, facecolor=fill)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha=ha, va=va, fontsize=fontsize,
            fontweight=fontweight, wrap=True)


def draw_arrow(ax, x1, y1, x2, y2, lw=1.2, style='->', color=LN):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))


def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
    plt.close(fig)
    print(f"  Saved: {path}")


# ============================================================
# PYTANIE 9 DIAGRAMS
# ============================================================

def gen_ipc_mechanisms():
    """IPC mechanisms comparison diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Mechanizmy IPC — porównanie', fontsize=FS_TITLE, fontweight='bold', pad=10)

    mechanisms = [
        ('Pipe', '→ jednokierunkowy\n→ bufor w jądrze\n→ spokrewnione procesy',
         'ls | grep txt', GRAY1),
        ('Shared\nMemory', '→ wspólna ramka RAM\n→ zero kopiowania\n→ wymaga synchronizacji',
         'mmap() / shm_open()', LIGHT_GREEN),
        ('Message\nQueue', '→ strukturalne wiad.\n→ asynchroniczna\n→ filtrowanie typów',
         'msgsnd() / msgrcv()', LIGHT_BLUE),
        ('Socket', '→ dwukierunkowy\n→ lokalny lub sieciowy\n→ TCP/UDP',
         'connect() / accept()', LIGHT_YELLOW),
    ]

    for i, (name, desc, example, color) in enumerate(mechanisms):
        x = 0.3
        y = 5.5 - i * 1.5
        # Box for mechanism name
        draw_box(ax, x, y, 1.5, 1.0, name, fill=color, fontsize=9, fontweight='bold')
        # Description
        ax.text(x + 2.0, y + 0.5, desc, fontsize=FS, va='center', ha='left',
                family='monospace')
        # Example
        draw_box(ax, 6.5, y + 0.15, 3.0, 0.7, example, fill=GRAY4, fontsize=FS_SMALL)

    # Draw process boxes for pipe illustration at top
    y_top = 6.3
    ax.text(5.0, y_top, 'Proces A  ──bufor jądra──▶  Proces B',
            fontsize=FS, ha='center', va='center', family='monospace',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY1, edgecolor=GRAY3))

    # Legend
    ax.text(0.3, 0.3, 'Szybkość: Shared Memory > Pipe ≈ MsgQueue > Socket (sieciowy)',
            fontsize=FS, va='center', style='italic')

    save_fig(fig, 'ipc_mechanisms.png')


def gen_deadlock_illustration():
    """Deadlock circular wait diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Zakleszczenie (Deadlock) — cykliczne oczekiwanie', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    # Thread boxes
    draw_box(ax, 0.5, 3.5, 2.0, 1.2, 'Wątek A\n(trzyma Mutex 1)', fill=LIGHT_BLUE,
             fontsize=9, fontweight='bold')
    draw_box(ax, 5.5, 3.5, 2.0, 1.2, 'Wątek B\n(trzyma Mutex 2)', fill=LIGHT_ORANGE,
             fontsize=9, fontweight='bold')

    # Resource boxes
    draw_box(ax, 0.5, 0.8, 2.0, 1.0, 'Mutex 1\nzablokowany', fill=GRAY2,
             fontsize=8, fontweight='bold')
    draw_box(ax, 5.5, 0.8, 2.0, 1.0, 'Mutex 2\nzablokowany', fill=GRAY2,
             fontsize=8, fontweight='bold')

    # Arrows: "holds" (down)
    draw_arrow(ax, 1.5, 3.5, 1.5, 1.8, lw=2.0, color='#333333')
    ax.text(0.3, 2.65, 'trzyma', fontsize=FS, ha='center', rotation=90, color='#333333')

    draw_arrow(ax, 6.5, 3.5, 6.5, 1.8, lw=2.0, color='#333333')
    ax.text(7.7, 2.65, 'trzyma', fontsize=FS, ha='center', rotation=90, color='#333333')

    # Arrows: "waits for" (across, with red)
    draw_arrow(ax, 2.5, 4.3, 5.5, 4.3, lw=2.5, color='#C62828')
    ax.text(4.0, 4.6, 'czeka na Mutex 2', fontsize=FS, ha='center', color='#C62828',
            fontweight='bold')

    draw_arrow(ax, 5.5, 3.7, 2.5, 3.7, lw=2.5, color='#C62828')
    ax.text(4.0, 3.2, 'czeka na Mutex 1', fontsize=FS, ha='center', color='#C62828',
            fontweight='bold')

    # Coffman conditions
    conditions = [
        '1. Mutual Exclusion — zasoby wyłączne',
        '2. Hold and Wait — trzymaj + czekaj',
        '3. No Preemption — nie można zabrać siłą',
        '4. Circular Wait — cykl oczekiwania ← złam ten!'
    ]
    for i, cond in enumerate(conditions):
        color_c = '#C62828' if i == 3 else LN
        fw = 'bold' if i == 3 else 'normal'
        ax.text(0.5, 0.5 - i * 0.25 + 0.2, cond, fontsize=FS_SMALL, color=color_c,
                fontweight=fw, va='center')

    save_fig(fig, 'deadlock_illustration.png')


def gen_producer_consumer():
    """Producer-consumer with bounded buffer diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Producent-Konsument z buforem cyklicznym (N=4)', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    # Producer
    draw_box(ax, 0.3, 2.0, 1.8, 1.5, 'Producent\n\nwstaw(elem)\nV(full)\nV(mutex)',
             fill=LIGHT_GREEN, fontsize=FS, fontweight='bold')

    # Buffer slots
    buf_x = 3.0
    buf_y = 2.5
    slot_w = 1.0
    slot_h = 0.8
    items = ['A', 'B', '', '']
    fills = [LIGHT_BLUE, LIGHT_BLUE, 'white', 'white']
    for i, (item, fc) in enumerate(zip(items, fills)):
        x = buf_x + i * slot_w
        draw_box(ax, x, buf_y, slot_w, slot_h, item, fill=fc, fontsize=10,
                 fontweight='bold', rounded=False)

    ax.text(buf_x + 2.0, buf_y + slot_h + 0.3, 'Bufor (N=4)',
            fontsize=9, ha='center', fontweight='bold')
    ax.text(buf_x + 2.0, buf_y - 0.3, 'full=2, empty=2',
            fontsize=FS, ha='center', family='monospace')

    # Consumer
    draw_box(ax, 7.8, 2.0, 1.8, 1.5, 'Konsument\n\npobierz()\nV(empty)\nV(mutex)',
             fill=LIGHT_YELLOW, fontsize=FS, fontweight='bold')

    # Arrows
    draw_arrow(ax, 2.1, 2.75, 3.0, 2.9, lw=1.5)
    draw_arrow(ax, 7.0, 2.9, 7.8, 2.75, lw=1.5)

    # Semaphores
    sems = [
        ('mutex = 1', 'wyłączny dostęp do bufora', GRAY2),
        ('empty = 2', 'wolne sloty (P = czekaj, V = +1)', LIGHT_GREEN),
        ('full = 2', 'pełne sloty (P = czekaj, V = +1)', LIGHT_BLUE),
    ]
    for i, (name, desc, color) in enumerate(sems):
        y = 1.2 - i * 0.45
        draw_box(ax, 3.0, y, 1.5, 0.35, name, fill=color, fontsize=FS_SMALL,
                 fontweight='bold')
        ax.text(4.7, y + 0.17, desc, fontsize=FS_SMALL, va='center')

    # Warning
    ax.text(0.3, 4.8, 'KOLEJNOŚĆ: P(empty/full) PRZED P(mutex)!  Odwrotnie = DEADLOCK',
            fontsize=FS, fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=LIGHT_RED, edgecolor='#C62828'))

    save_fig(fig, 'producer_consumer.png')


# ============================================================
# PYTANIE 12 DIAGRAMS
# ============================================================

def draw_network_node(ax, name, pos, color='white', fontsize=10, r=0.3):
    """Draw a network node (circle)."""
    x, y = pos
    circle = plt.Circle((x, y), r, fill=True, facecolor=color,
                        edgecolor=LN, linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', zorder=6)


def draw_network_edge(ax, pos1, pos2, label='', color=LN, lw=1.5, offset=0.0,
                      directed=True, r=0.33, label_bg='white'):
    """Draw a directed edge with label."""
    x1, y1 = pos1
    x2, y2 = pos2
    dx, dy = x2 - x1, y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    if length == 0:
        return
    sx = x1 + r * dx / length
    sy = y1 + r * dy / length
    ex = x2 - r * dx / length
    ey = y2 - r * dy / length

    if directed:
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw))
    else:
        ax.plot([sx, ex], [sy, ey], color=color, linewidth=lw, zorder=2)

    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        perp_x = -dy / length * (0.2 + offset)
        perp_y = dx / length * (0.2 + offset)
        ax.text(mx + perp_x, my + perp_y, str(label), ha='center', va='center',
                fontsize=FS_EDGE, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.1', facecolor=label_bg,
                          edgecolor=GRAY3, alpha=0.95), zorder=4)


def gen_ford_fulkerson():
    """Ford-Fulkerson max flow step-by-step."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('Ford-Fulkerson — Maksymalny przepływ (krok po kroku)',
                 fontsize=FS_TITLE, fontweight='bold')

    pos = {'s': (0.5, 1.5), 'A': (2.5, 2.5), 'B': (2.5, 0.5), 't': (4.5, 1.5)}

    steps = [
        {
            'title': 'Krok 0: Sieć wejściowa\n(przepustowości)',
            'edges': [('s','A','10'), ('s','B','8'), ('A','t','6'),
                      ('B','t','10'), ('B','A','2')],
            'flows': {},
            'path': [],
            'note': 'Szukamy ścieżki s→...→t'
        },
        {
            'title': 'Krok 1: Ścieżka s→A→t\nPrzepływ: +6 (min(10,6))',
            'edges': [('s','A','4/10'), ('s','B','0/8'), ('A','t','6/6'),
                      ('B','t','0/10'), ('B','A','0/2')],
            'flows': {},
            'path': [('s','A'), ('A','t')],
            'note': 'Łączny przepływ: 6'
        },
        {
            'title': 'Krok 2: Ścieżka s→B→t\nPrzepływ: +8 (min(8,10))',
            'edges': [('s','A','4/10'), ('s','B','8/8'), ('A','t','6/6'),
                      ('B','t','8/10'), ('B','A','0/2')],
            'flows': {},
            'path': [('s','B'), ('B','t')],
            'note': 'Łączny przepływ: 14'
        },
        {
            'title': 'Krok 3: Brak ścieżki powiększającej\nMAX FLOW = 14',
            'edges': [('s','A','4/10'), ('s','B','8/8'), ('A','t','6/6'),
                      ('B','t','8/10'), ('B','A','0/2')],
            'flows': {},
            'path': [],
            'note': 'Min-cut: {s,A,B}|{t}\nA→t(6)+B→t(10)=16? Nie!\ns→B(8)+A→t(6)=14 ✓'
        },
    ]

    for idx, (ax, step) in enumerate(zip(axes.flat, steps)):
        ax.set_xlim(-0.3, 5.3)
        ax.set_ylim(-0.3, 3.3)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(step['title'], fontsize=FS, fontweight='bold', pad=5)

        path_set = set(step['path'])

        for e in step['edges']:
            u, v, label = e
            is_path = (u, v) in path_set
            c = '#C62828' if is_path else LN
            w = 2.5 if is_path else 1.5
            draw_network_edge(ax, pos[u], pos[v], label=label, color=c, lw=w)

        for name, p in pos.items():
            if name == 's':
                c = LIGHT_GREEN
            elif name == 't':
                c = LIGHT_RED
            else:
                c = 'white'
            draw_network_node(ax, name, p, color=c)

        ax.text(2.5, -0.15, step['note'], fontsize=FS_SMALL, ha='center',
                va='center', style='italic',
                bbox=dict(boxstyle='round,pad=0.15', facecolor=GRAY4, edgecolor=GRAY3))

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save_fig(fig, 'ford_fulkerson_example.png')


def gen_hungarian():
    """Hungarian algorithm step-by-step."""
    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    fig.suptitle('Algorytm węgierski — Problem przydziału (krok po kroku)',
                 fontsize=FS_TITLE, fontweight='bold')

    matrices = [
        {
            'title': 'Macierz kosztów (wejściowa)',
            'data': [[8, 4, 7], [5, 2, 3], [9, 4, 8]],
            'highlight': [],
            'note': 'Minimalizuj łączny koszt przydziału',
        },
        {
            'title': 'Krok 1: Redukcja wierszy\n(odejmij min z wiersza)',
            'data': [[4, 0, 3], [3, 0, 1], [5, 0, 4]],
            'highlight': [(0,1), (1,1), (2,1)],
            'note': 'min: A=4, B=2, C=4',
        },
        {
            'title': 'Krok 2: Redukcja kolumn\n(odejmij min z kolumny)',
            'data': [[1, 0, 2], [0, 0, 0], [2, 0, 3]],
            'highlight': [(1,0), (0,1), (1,1), (2,1), (1,2)],
            'note': 'min: Z1=3, Z2=0, Z3=1',
        },
        {
            'title': 'Krok 3: Optymalne przypisanie\nA→Z2(4), B→Z1(5), C=?',
            'data': [[0, 0, 1], [0, 1, 0], [1, 0, 2]],
            'highlight': [(0,1), (1,0), (2,1)],
            'note': 'Optymalne: A→Z1(8) + B→Z3(3) + C→Z2(4) = 15',
        },
    ]

    rows = ['A', 'B', 'C']
    cols = ['Z1', 'Z2', 'Z3']

    for ax, m in zip(axes.flat, matrices):
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-1, 4.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(m['title'], fontsize=FS, fontweight='bold', pad=5)

        # Column headers
        for j, col in enumerate(cols):
            ax.text(j + 1.5, 3.8, col, ha='center', va='center', fontsize=9,
                    fontweight='bold')

        # Row headers and data
        for i, row in enumerate(rows):
            y = 2.8 - i
            ax.text(0.3, y, row, ha='center', va='center', fontsize=9,
                    fontweight='bold')
            for j in range(3):
                val = m['data'][i][j]
                is_zero = val == 0
                is_hl = (i, j) in m['highlight']
                fc = LIGHT_GREEN if is_hl else ('white' if not is_zero else LIGHT_YELLOW)
                rect = FancyBboxPatch((j + 1.0, y - 0.35), 1.0, 0.7,
                                     boxstyle="round,pad=0.05", lw=1.2,
                                     edgecolor=LN if not is_hl else '#1B5E20',
                                     facecolor=fc)
                ax.add_patch(rect)
                ax.text(j + 1.5, y, str(val), ha='center', va='center',
                        fontsize=10, fontweight='bold' if is_hl else 'normal')

        ax.text(2.0, -0.6, m['note'], fontsize=FS_SMALL, ha='center', va='center',
                style='italic',
                bbox=dict(boxstyle='round,pad=0.15', facecolor=GRAY4, edgecolor=GRAY3))

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save_fig(fig, 'hungarian_example.png')


def gen_cpm():
    """CPM critical path diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-0.5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('CPM — Ścieżka krytyczna projektu IT', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    # Task positions: (x, y)
    tasks = {
        'START': (0.5, 2.5),
        'A\n3 tyg': (2.5, 2.5),
        'B\n4 tyg': (5.0, 3.8),
        'C\n5 tyg': (5.0, 1.2),
        'D\n6 tyg': (7.5, 3.8),
        'E\n2 tyg': (9.5, 2.5),
        'F\n1 tyg': (11.5, 2.5),
    }

    # Critical path: START→A→B→D→E→F
    critical = {'START', 'A\n3 tyg', 'B\n4 tyg', 'D\n6 tyg', 'E\n2 tyg', 'F\n1 tyg'}
    critical_edges = {
        ('START', 'A\n3 tyg'), ('A\n3 tyg', 'B\n4 tyg'),
        ('B\n4 tyg', 'D\n6 tyg'), ('D\n6 tyg', 'E\n2 tyg'),
        ('E\n2 tyg', 'F\n1 tyg'),
    }

    edges = [
        ('START', 'A\n3 tyg'),
        ('A\n3 tyg', 'B\n4 tyg'),
        ('A\n3 tyg', 'C\n5 tyg'),
        ('B\n4 tyg', 'D\n6 tyg'),
        ('C\n5 tyg', 'E\n2 tyg'),
        ('D\n6 tyg', 'E\n2 tyg'),
        ('E\n2 tyg', 'F\n1 tyg'),
    ]

    # Draw edges
    for u, v in edges:
        is_crit = (u, v) in critical_edges
        c = '#C62828' if is_crit else GRAY3
        w = 2.5 if is_crit else 1.2
        draw_network_edge(ax, tasks[u], tasks[v], color=c, lw=w, r=0.5)

    # Draw nodes
    for name, p in tasks.items():
        is_crit = name in critical
        c = LIGHT_RED if is_crit else LIGHT_BLUE
        r = 0.45
        circle = plt.Circle(p, r, fill=True, facecolor=c,
                           edgecolor='#C62828' if is_crit else LN,
                           linewidth=2.0 if is_crit else 1.2, zorder=5)
        ax.add_patch(circle)
        ax.text(p[0], p[1], name, ha='center', va='center',
                fontsize=7 if '\n' in name else 8,
                fontweight='bold', zorder=6)

    # ES/EF labels
    es_ef = [
        ('A\n3 tyg', 'ES=0, EF=3'),
        ('B\n4 tyg', 'ES=3, EF=7'),
        ('C\n5 tyg', 'ES=3, EF=8\nzapas=5'),
        ('D\n6 tyg', 'ES=7, EF=13'),
        ('E\n2 tyg', 'ES=13, EF=15'),
        ('F\n1 tyg', 'ES=15, EF=16'),
    ]
    for name, label in es_ef:
        x, y = tasks[name]
        offset_y = 0.7 if y > 2.5 else -0.7
        ax.text(x, y + offset_y, label, ha='center', va='center', fontsize=FS_SMALL,
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                          edgecolor=GRAY3, alpha=0.95))

    # Legend
    ax.text(0.5, -0.2, 'Ścieżka krytyczna: A→B→D→E→F (16 tyg)',
            fontsize=9, fontweight='bold', color='#C62828')
    ax.text(0.5, -0.6, 'C ma 5 tyg zapasu — może się opóźnić bez wpływu na projekt',
            fontsize=FS, style='italic')

    save_fig(fig, 'cpm_example.png')


def gen_kruskal():
    """Kruskal MST construction step-by-step."""
    fig, axes = plt.subplots(2, 2, figsize=(9, 8))
    fig.suptitle('Kruskal — budowa MST krok po kroku', fontsize=FS_TITLE, fontweight='bold')

    pos = {'A': (0.5, 2.5), 'B': (3.0, 2.5), 'C': (3.0, 0.5), 'D': (0.5, 0.5)}

    all_edges = [
        ('C', 'D', 1), ('A', 'C', 2), ('A', 'B', 4),
        ('B', 'C', 6), ('B', 'D', 7), ('A', 'D', 8)
    ]

    steps = [
        {
            'title': 'Graf wejściowy\n(6 krawędzi)',
            'mst': [],
            'consider': None,
            'note': 'Posortowane: CD(1), AC(2), AB(4), BC(6), BD(7), AD(8)'
        },
        {
            'title': 'Krok 1: Dodaj C-D (waga 1)\nNajlżejsza krawędź',
            'mst': [('C', 'D', 1)],
            'consider': ('C', 'D'),
            'note': 'MST = {C-D}, koszt = 1'
        },
        {
            'title': 'Krok 2: Dodaj A-C (waga 2)\nA nie w {C,D}',
            'mst': [('C', 'D', 1), ('A', 'C', 2)],
            'consider': ('A', 'C'),
            'note': 'MST = {C-D, A-C}, koszt = 3'
        },
        {
            'title': 'Krok 3: Dodaj A-B (waga 4)\nB nie w {A,C,D} → KONIEC',
            'mst': [('C', 'D', 1), ('A', 'C', 2), ('A', 'B', 4)],
            'consider': ('A', 'B'),
            'note': 'MST = {C-D, A-C, A-B}, koszt = 7 ✓'
        },
    ]

    for ax, step in zip(axes.flat, steps):
        ax.set_xlim(-0.5, 4.0)
        ax.set_ylim(-0.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(step['title'], fontsize=FS, fontweight='bold', pad=5)

        mst_set = set((u, v) for u, v, _ in step['mst'])

        for u, v, w in all_edges:
            in_mst = (u, v) in mst_set or (v, u) in mst_set
            is_cur = step['consider'] and ((u, v) == step['consider'] or (v, u) == step['consider'])
            if is_cur:
                c, lw = '#C62828', 3.0
            elif in_mst:
                c, lw = '#1B5E20', 2.5
            else:
                c, lw = GRAY3, 1.0
            draw_network_edge(ax, pos[u], pos[v], label=str(w), color=c, lw=lw,
                             directed=False, label_bg=LIGHT_GREEN if in_mst else 'white')

        for name, p in pos.items():
            # Check if in current MST component
            in_mst = any(name in (u, v) for u, v, _ in step['mst'])
            c = LIGHT_GREEN if in_mst else 'white'
            draw_network_node(ax, name, p, color=c, r=0.3)

        ax.text(1.75, -0.3, step['note'], fontsize=FS_SMALL, ha='center',
                va='center', style='italic',
                bbox=dict(boxstyle='round,pad=0.15', facecolor=GRAY4, edgecolor=GRAY3))

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save_fig(fig, 'kruskal_example.png')


def gen_tsp():
    """TSP nearest neighbor heuristic."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    fig.suptitle('TSP — heurystyka Nearest Neighbor (5 miast)',
                 fontsize=FS_TITLE, fontweight='bold')

    pos = {
        'A': (0.5, 3.0), 'B': (2.0, 4.0), 'C': (4.0, 3.5),
        'D': (3.5, 1.0), 'E': (1.5, 1.5)
    }

    dist = {
        ('A','B'): 20, ('A','C'): 42, ('A','D'): 35, ('A','E'): 12,
        ('B','C'): 30, ('B','D'): 34, ('B','E'): 10,
        ('C','D'): 12, ('C','E'): 40,
        ('D','E'): 25,
    }

    # Left: full graph with all distances
    ax = axes[0]
    ax.set_xlim(-0.5, 5.0)
    ax.set_ylim(0, 5.0)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Graf pełny (odległości)', fontsize=FS, fontweight='bold')

    for (u, v), d in dist.items():
        draw_network_edge(ax, pos[u], pos[v], label=str(d), color=GRAY3, lw=0.8,
                         directed=False, r=0.3)

    for name, p in pos.items():
        draw_network_node(ax, name, p, color=LIGHT_BLUE, r=0.3)

    # Right: NN solution
    ax = axes[1]
    ax.set_xlim(-0.5, 5.0)
    ax.set_ylim(0, 5.0)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Nearest Neighbor (start A)\nTrasa: A→E→B→C→D→A = 99', fontsize=FS,
                 fontweight='bold')

    nn_path = [('A','E',12), ('E','B',10), ('B','C',30), ('C','D',12), ('D','A',35)]
    colors = ['#C62828', '#1B5E20', '#1565C0', '#E65100', '#4A148C']

    for i, (u, v, d) in enumerate(nn_path):
        draw_network_edge(ax, pos[u], pos[v], label=f'{d}',
                         color=colors[i], lw=2.0, directed=True, r=0.3)
        # Step number
        mx = (pos[u][0] + pos[v][0]) / 2
        my = (pos[u][1] + pos[v][1]) / 2
        dx = pos[v][0] - pos[u][0]
        dy = pos[v][1] - pos[u][1]
        length = np.sqrt(dx**2 + dy**2)
        ox = dy / length * 0.45
        oy = -dx / length * 0.45
        ax.text(mx + ox, my + oy, f'#{i+1}', fontsize=FS_SMALL, ha='center',
                color=colors[i], fontweight='bold')

    for name, p in pos.items():
        c = LIGHT_GREEN if name == 'A' else LIGHT_BLUE
        draw_network_node(ax, name, p, color=c, r=0.3)

    fig.tight_layout(rect=[0, 0, 1, 0.9])
    save_fig(fig, 'tsp_nearest_neighbor.png')


def gen_min_cost_flow():
    """Min-cost flow example."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle('Minimalny koszt przepływu — transport 10 ton',
                 fontsize=FS_TITLE, fontweight='bold')

    pos = {'s': (0.5, 1.5), 'A': (2.5, 2.5), 'B': (2.5, 0.5), 't': (4.5, 1.5)}

    # Left: network with capacities and costs
    ax = axes[0]
    ax.set_xlim(-0.3, 5.3)
    ax.set_ylim(-0.3, 3.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Sieć (przepustowość, koszt/t)', fontsize=FS, fontweight='bold')

    edges_info = [
        ('s', 'A', '(8, 2zł)'), ('s', 'B', '(5, 4zł)'),
        ('A', 't', '(6, 3zł)'), ('B', 't', '(5, 1zł)'),
    ]
    for u, v, label in edges_info:
        draw_network_edge(ax, pos[u], pos[v], label=label, r=0.33)

    for name, p in pos.items():
        c = LIGHT_GREEN if name == 's' else (LIGHT_RED if name == 't' else 'white')
        draw_network_node(ax, name, p, color=c)

    # Right: optimal flow
    ax = axes[1]
    ax.set_xlim(-0.3, 5.3)
    ax.set_ylim(-0.3, 3.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Optymalny przepływ (koszt = 50 zł)', fontsize=FS, fontweight='bold')

    opt_edges = [
        ('s', 'A', '5/8', '#1B5E20'), ('s', 'B', '5/5', '#C62828'),
        ('A', 't', '5/6', '#1B5E20'), ('B', 't', '5/5', '#C62828'),
    ]
    for u, v, label, color in opt_edges:
        draw_network_edge(ax, pos[u], pos[v], label=label, color=color, lw=2.0, r=0.33)

    for name, p in pos.items():
        c = LIGHT_GREEN if name == 's' else (LIGHT_RED if name == 't' else 'white')
        draw_network_node(ax, name, p, color=c)

    ax.text(2.5, -0.15, '5t×(2+3)=25zł + 5t×(4+1)=25zł = 50zł',
            fontsize=FS, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.15', facecolor=GRAY4, edgecolor=GRAY3))

    fig.tight_layout(rect=[0, 0, 1, 0.9])
    save_fig(fig, 'min_cost_flow_example.png')


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("Generating PYTANIE 9 diagrams...")
    gen_ipc_mechanisms()
    gen_deadlock_illustration()
    gen_producer_consumer()

    print("\nGenerating PYTANIE 12 diagrams...")
    gen_ford_fulkerson()
    gen_hungarian()
    gen_cpm()
    gen_kruskal()
    gen_tsp()
    gen_min_cost_flow()

    print("\nAll diagrams generated successfully!")
