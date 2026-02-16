#!/usr/bin/env python3
"""
Generate diagrams for PYTANIE 2: Shortest path algorithms.
  1. Graph structure — the shared example graph (A,B,C,D)
  2. Dijkstra traversal — step-by-step on that graph
  3. Bellman-Ford traversal — step-by-step
  4. A* traversal — step-by-step with heuristics

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
LIGHT_PURPLE = '#E8D5F5'

# --- Shared graph layout ---
# Graph: A--2--B--3--D, A--4--C--5--D, D--1--C (directed: C->D has weight 5)
NODE_POS = {'A': (1, 2), 'B': (3.5, 3.2), 'C': (1, 0), 'D': (3.5, 0.8)}
EDGES = [('A', 'B', 2), ('A', 'C', 4), ('B', 'D', 3), ('C', 'D', 5)]


def draw_graph_node(ax, name, pos, color='white', current=False, visited=False,
                    dist_label=None, fontsize=12):
    """Draw a graph node (circle with label)."""
    x, y = pos
    r = 0.35
    lw = 2.5 if current else 1.5
    ec = '#D32F2F' if current else LN
    fc = LIGHT_GREEN if visited else color
    if current:
        fc = LIGHT_YELLOW

    circle = plt.Circle((x, y), r, fill=True, facecolor=fc,
                        edgecolor=ec, linewidth=lw, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', zorder=6)

    if dist_label is not None:
        ax.text(x, y - 0.55, f'd={dist_label}', ha='center', va='center',
                fontsize=FS, zorder=6,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                          edgecolor=GRAY3, alpha=0.95))


def draw_graph_edge(ax, pos1, pos2, weight, highlighted=False, relaxed=False):
    """Draw an edge between two nodes with weight label."""
    x1, y1 = pos1
    x2, y2 = pos2

    # Shorten line to not overlap node circles
    dx, dy = x2 - x1, y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    r = 0.38
    sx = x1 + r * dx / length
    sy = y1 + r * dy / length
    ex = x2 - r * dx / length
    ey = y2 - r * dy / length

    color = '#D32F2F' if relaxed else ('#1565C0' if highlighted else GRAY3)
    lw = 2.5 if (highlighted or relaxed) else 1.5
    ls = '-'

    ax.plot([sx, ex], [sy, ey], color=color, linewidth=lw, linestyle=ls, zorder=2)

    # Weight label
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # Offset perpendicular to edge
    perp_x = -dy / length * 0.2
    perp_y = dx / length * 0.2

    ax.text(mx + perp_x, my + perp_y, str(weight), ha='center', va='center',
            fontsize=FS_EDGE, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                      edgecolor=GRAY3 if not highlighted else color, alpha=0.95),
            zorder=4)


def draw_full_graph(ax, title="", dist=None, current=None, visited=None,
                    highlighted_edges=None, relaxed_edges=None):
    """Draw the complete graph with optional highlighting."""
    if visited is None:
        visited = set()
    if highlighted_edges is None:
        highlighted_edges = set()
    if relaxed_edges is None:
        relaxed_edges = set()
    if dist is None:
        dist = {}

    ax.set_xlim(-0.2, 4.7)
    ax.set_ylim(-0.8, 4.2)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=FS, fontweight='bold', pad=5)

    # Draw edges
    for u, v, w in EDGES:
        hl = (u, v) in highlighted_edges or (v, u) in highlighted_edges
        rl = (u, v) in relaxed_edges or (v, u) in relaxed_edges
        draw_graph_edge(ax, NODE_POS[u], NODE_POS[v], w,
                       highlighted=hl, relaxed=rl)

    # Draw nodes
    for name, pos in NODE_POS.items():
        is_current = (name == current)
        is_visited = (name in visited)
        d_label = dist.get(name, None)
        draw_graph_node(ax, name, pos, current=is_current, visited=is_visited,
                       dist_label=d_label)


# ============================================================
# 1. Graph structure diagram
# ============================================================
def draw_graph_structure():
    """The shared example graph used across all three algorithms."""
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    ax.set_xlim(-0.5, 5.0)
    ax.set_ylim(-1.2, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Przykładowy graf — wspólny dla wszystkich algorytmów\n'
                 'Wierzchołki: {A, B, C, D}, Start = A',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Draw edges
    for u, v, w in EDGES:
        draw_graph_edge(ax, NODE_POS[u], NODE_POS[v], w)

    # Draw nodes
    for name, pos in NODE_POS.items():
        draw_graph_node(ax, name, pos)

    # Start arrow
    ax.annotate("START", xy=(NODE_POS['A'][0] - 0.35, NODE_POS['A'][1]),
                xytext=(NODE_POS['A'][0] - 1.2, NODE_POS['A'][1]),
                fontsize=FS, fontweight='bold', color='#D32F2F',
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2),
                va='center')

    # Edge list
    ax.text(2.3, -0.8, 'Krawędzie: A→B(2), A→C(4), B→D(3), C→D(5)\n'
            '|V|=4, |E|=4, wagi ≥ 0',
            ha='center', va='center', fontsize=FS,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'graph_example_structure.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ graph_example_structure.png")


# ============================================================
# 2. Dijkstra traversal
# ============================================================
def draw_dijkstra_traversal():
    """Step-by-step Dijkstra on the shared graph."""
    steps = [
        {
            'title': 'Krok 0: Inicjalizacja\nd = {A:0, B:∞, C:∞, D:∞}',
            'dist': {'A': '0', 'B': '∞', 'C': '∞', 'D': '∞'},
            'current': 'A', 'visited': set(),
            'highlighted': set(), 'relaxed': set(),
        },
        {
            'title': 'Krok 1: Przetwarzam A (d=0)\nRelaksacja: A→B: 0+2=2<∞ ✓  A→C: 0+4=4<∞ ✓',
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '∞'},
            'current': 'A', 'visited': {'A'},
            'highlighted': set(), 'relaxed': {('A', 'B'), ('A', 'C')},
        },
        {
            'title': 'Krok 2: Przetwarzam B (d=2) — minimum\nRelaksacja: B→D: 2+3=5<∞ ✓',
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '5'},
            'current': 'B', 'visited': {'A', 'B'},
            'highlighted': set(), 'relaxed': {('B', 'D')},
        },
        {
            'title': 'Krok 3: Przetwarzam C (d=4)\nRelaksacja: C→D: 4+5=9 > 5 ✗ (nie poprawia)',
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '5'},
            'current': 'C', 'visited': {'A', 'B', 'C'},
            'highlighted': {('C', 'D')}, 'relaxed': set(),
        },
        {
            'title': 'Krok 4: WYNIK — wszystkie przetworzone\nd = {A:0, B:2, C:4, D:5}',
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '5'},
            'current': None, 'visited': {'A', 'B', 'C', 'D'},
            'highlighted': {('A', 'B'), ('B', 'D'), ('A', 'C')}, 'relaxed': set(),
        },
    ]

    fig, axes = plt.subplots(1, 5, figsize=(14, 3.5))
    fig.suptitle('Dijkstra — przejście grafu krok po kroku (zachłannie: zawsze bierz min d)',
                 fontsize=FS_TITLE, fontweight='bold', y=1.02)

    for i, (ax, step) in enumerate(zip(axes, steps)):
        draw_full_graph(ax, title=step['title'],
                       dist=step['dist'], current=step['current'],
                       visited=step['visited'],
                       highlighted_edges=step['highlighted'],
                       relaxed_edges=step['relaxed'])

    # Legend
    fig.text(0.5, -0.04,
             '[zolty] = aktualnie przetwarzany    [zielony] = odwiedzony (zamkniety)    '
             'czerwona krawedz = relaksacja OK    szara krawedz = nie poprawia',
             ha='center', fontsize=FS,
             bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'dijkstra_traversal.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ dijkstra_traversal.png")


# ============================================================
# 3. Bellman-Ford traversal
# ============================================================
def draw_bellman_ford_traversal():
    """Step-by-step Bellman-Ford on the shared graph."""
    fig = plt.figure(figsize=(14, 7))
    fig.suptitle('Bellman-Ford — przejście grafu krok po kroku\n'
                 '(V−1 = 3 iteracje, w każdej relaksuj WSZYSTKIE krawędzie)',
                 fontsize=FS_TITLE, fontweight='bold', y=0.98)

    # Data for each iteration
    iterations = [
        {
            'title': 'Inicjalizacja',
            'edges_detail': '—',
            'dist': {'A': '0', 'B': '∞', 'C': '∞', 'D': '∞'},
            'relaxed': set(),
        },
        {
            'title': 'Iteracja 1 (V−1=3)',
            'edges_detail': (
                'A→B: 0+2=2<∞ ✓\n'
                'A→C: 0+4=4<∞ ✓\n'
                'B→D: 2+3=5<∞ ✓\n'
                'C→D: 4+5=9>5 ✗'
            ),
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '5'},
            'relaxed': {('A', 'B'), ('A', 'C'), ('B', 'D')},
        },
        {
            'title': 'Iteracja 2',
            'edges_detail': (
                'A→B: 0+2=2=2 ✗\n'
                'A→C: 0+4=4=4 ✗\n'
                'B→D: 2+3=5=5 ✗\n'
                'C→D: 4+5=9>5 ✗'
            ),
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '5'},
            'relaxed': set(),
        },
        {
            'title': 'Iteracja 3',
            'edges_detail': (
                'Brak zmian → stabilne!\n'
                '(wczesne zakończenie\n'
                ' optymalizacja)'
            ),
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '5'},
            'relaxed': set(),
        },
    ]

    for i, it in enumerate(iterations):
        # Graph subplot
        ax_g = fig.add_subplot(2, 4, i + 1)
        draw_full_graph(ax_g, title=it['title'],
                       dist=it['dist'], current=None,
                       visited=set() if i == 0 else {'A', 'B', 'C', 'D'},
                       relaxed_edges=it['relaxed'])

        # Detail subplot below
        ax_d = fig.add_subplot(2, 4, i + 5)
        ax_d.axis('off')
        ax_d.text(0.5, 0.5, it['edges_detail'], ha='center', va='center',
                  fontsize=FS, family='monospace',
                  bbox=dict(boxstyle='round,pad=0.4', facecolor=GRAY4,
                            edgecolor=GRAY3))

    # Negative cycle check note
    fig.text(0.5, 0.01,
             'Po 3 iteracjach: sprawdź raz jeszcze — nic się nie zmienia → BRAK cyklu ujemnego → wynik poprawny',
             ha='center', fontsize=FS, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_GREEN, edgecolor=LN))

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(os.path.join(OUTPUT_DIR, 'bellman_ford_traversal.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ bellman_ford_traversal.png")


# ============================================================
# 4. A* traversal
# ============================================================
def draw_astar_traversal():
    """Step-by-step A* on the shared graph with heuristics."""
    # Heuristic values (straight-line distance to D)
    h_vals = {'A': 4, 'B': 2, 'C': 3, 'D': 0}

    fig = plt.figure(figsize=(14, 7.5))
    fig.suptitle('A* — przejście grafu krok po kroku (cel = D)\n'
                 'f(n) = g(n) + h(n), heurystyka h = oszacowana odległość do D',
                 fontsize=FS_TITLE, fontweight='bold', y=0.99)

    steps = [
        {
            'title': 'Krok 0: Inicjalizacja\nh(A)=4, h(B)=2, h(C)=3, h(D)=0',
            'detail': (
                'g(A)=0, f(A)=0+4=4\n'
                'pq = [(4, A)]\n'
                'h = oszacowanie\n'
                '  odl. do celu D'
            ),
            'dist': {'A': '0'},
            'f_vals': {'A': 'f=4'},
            'current': 'A', 'visited': set(), 'relaxed': set(),
        },
        {
            'title': 'Krok 1: pop A (f=4)\nA→B: g=2, f=2+2=4\nA→C: g=4, f=4+3=7',
            'detail': (
                'Relaksacja:\n'
                ' A→B: g=0+2=2\n'
                '  f=2+h(B)=2+2=4\n'
                ' A→C: g=0+4=4\n'
                '  f=4+h(C)=4+3=7\n'
                'pq = [(4,B), (7,C)]'
            ),
            'dist': {'A': '0', 'B': '2', 'C': '4'},
            'current': 'A', 'visited': {'A'},
            'relaxed': {('A', 'B'), ('A', 'C')},
        },
        {
            'title': 'Krok 2: pop B (f=4) — min!\nB→D: g=5, f=5+0=5',
            'detail': (
                'B ma f=4 < C(f=7)\n'
                '→ A* kieruje się\n'
                '  W STRONĘ celu!\n'
                'Relaksacja:\n'
                ' B→D: g=2+3=5\n'
                '  f=5+h(D)=5+0=5\n'
                'pq = [(5,D), (7,C)]'
            ),
            'dist': {'A': '0', 'B': '2', 'C': '4', 'D': '5'},
            'current': 'B', 'visited': {'A', 'B'},
            'relaxed': {('B', 'D')},
        },
        {
            'title': 'Krok 3: pop D (f=5)\nu == goal → STOP!',
            'detail': (
                'D to CEL → KONIEC!\n'
                'Nie przetwarzamy C\n'
                '  (f(C)=7 > f(D)=5)\n\n'
                'Ścieżka: A→B→D\n'
                'Koszt: 5\n\n'
                'Dijkstra odwi-\n'
                'edziłby też C!'
            ),
            'dist': {'A': '0', 'B': '2', 'D': '5'},
            'current': 'D', 'visited': {'A', 'B', 'D'},
            'relaxed': set(),
        },
    ]

    for i, step in enumerate(steps):
        # Graph
        ax_g = fig.add_subplot(2, 4, i + 1)
        draw_full_graph(ax_g, title=step['title'],
                       dist=step['dist'], current=step['current'],
                       visited=step['visited'],
                       relaxed_edges=step['relaxed'])

        # Add h values as small labels
        for name, pos in NODE_POS.items():
            ax_g.text(pos[0] + 0.35, pos[1] + 0.35, f'h={h_vals[name]}',
                     ha='center', va='center', fontsize=5.5, color='#1565C0',
                     fontweight='bold', zorder=7,
                     bbox=dict(boxstyle='round,pad=0.1', facecolor=LIGHT_BLUE,
                               edgecolor='#1565C0', alpha=0.9, lw=0.5))

        # Detail
        ax_d = fig.add_subplot(2, 4, i + 5)
        ax_d.axis('off')
        ax_d.text(0.5, 0.5, step['detail'], ha='center', va='center',
                  fontsize=FS, family='monospace',
                  bbox=dict(boxstyle='round,pad=0.4', facecolor=GRAY4,
                            edgecolor=GRAY3))

    # Comparison note
    fig.text(0.5, 0.01,
             'A* odwiedził 3 wierzchołki (A, B, D) — POMINĄŁ C!\n'
             'Dijkstra odwiedziłby wszystkie 4. Heurystyka h kieruje przeszukiwanie w stronę celu.',
             ha='center', fontsize=FS, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_BLUE, edgecolor='#1565C0'))

    plt.tight_layout(rect=[0, 0.06, 1, 0.95])
    plt.savefig(os.path.join(OUTPUT_DIR, 'astar_traversal.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ astar_traversal.png")


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating shortest path diagrams for PYTANIE 2...")
    draw_graph_structure()
    draw_dijkstra_traversal()
    draw_bellman_ford_traversal()
    draw_astar_traversal()
    print(f"\nAll diagrams saved to {OUTPUT_DIR}/")
