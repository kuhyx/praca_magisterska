#!/usr/bin/env python3
"""
Generate Bellman-Ford negative-weights & negative-cycle diagram for PYTANIE 2.

Two-part figure:
  Part 1: Graph with negative edge, Dijkstra WRONG vs Bellman-Ford CORRECT
  Part 2: Negative cycle detection (add C→B(−3))

A4-compatible, monochrome-friendly, 300 DPI.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

DPI = 300
BG = 'white'
LN = 'black'
FS = 8
FS_TITLE = 10
FS_SMALL = 6.5
FS_EDGE = 9
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRAY1 = '#E8E8E8'
GRAY2 = '#D0D0D0'
GRAY3 = '#B8B8B8'
GRAY4 = '#F5F5F5'
LIGHT_GREEN = '#D5E8D4'
LIGHT_RED = '#F8D7DA'
LIGHT_YELLOW = '#FFF9C4'

# --- Graph layout for negative-weight example ---
# S→A(2), A→C(3), S→B(5), B→A(−4)
NEG_POS = {'S': (0.8, 2), 'A': (3.3, 3.2), 'B': (3.3, 0.8), 'C': (5.8, 2)}
NEG_EDGES = [('S', 'A', 2), ('A', 'C', 3), ('S', 'B', 5), ('B', 'A', -4)]


def draw_node(ax, name, pos, color='white', current=False, visited=False,
              dist_label=None, fontsize=12, error=False):
    x, y = pos
    r = 0.35
    lw = 2.5 if current else 1.5
    ec = '#D32F2F' if current else ('#D32F2F' if error else LN)
    fc = LIGHT_YELLOW if current else (LIGHT_GREEN if visited else color)
    if error:
        fc = LIGHT_RED

    circle = plt.Circle((x, y), r, fill=True, facecolor=fc,
                        edgecolor=ec, linewidth=lw, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', zorder=6)

    if dist_label is not None:
        bbox_ec = '#D32F2F' if error else GRAY3
        bbox_fc = LIGHT_RED if error else 'white'
        ax.text(x, y - 0.55, f'd={dist_label}', ha='center', va='center',
                fontsize=FS, zorder=6,
                bbox=dict(boxstyle='round,pad=0.15', facecolor=bbox_fc,
                          edgecolor=bbox_ec, alpha=0.95))


def draw_edge(ax, pos1, pos2, weight, highlighted=False, relaxed=False,
              negative=False, cycle_edge=False, offset=0.0):
    x1, y1 = pos1
    x2, y2 = pos2

    dx, dy = x2 - x1, y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    r = 0.38
    sx = x1 + r * dx / length
    sy = y1 + r * dy / length
    ex = x2 - r * dx / length
    ey = y2 - r * dy / length

    # Offset perpendicular for parallel edges
    if offset != 0:
        perp_x = -dy / length * offset
        perp_y = dx / length * offset
        sx += perp_x; sy += perp_y
        ex += perp_x; ey += perp_y

    if cycle_edge:
        color = '#D32F2F'
        lw = 2.5
        ls = '--'
    elif negative:
        color = '#D32F2F'
        lw = 2.5
        ls = '-'
    elif relaxed:
        color = '#D32F2F'
        lw = 2.5
        ls = '-'
    elif highlighted:
        color = '#1565C0'
        lw = 2.0
        ls = '-'
    else:
        color = GRAY3
        lw = 1.5
        ls = '-'

    # Arrow
    ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0),
                zorder=2)

    # Weight label
    mx = (sx + ex) / 2
    my = (sy + ey) / 2
    perp_x = -dy / length * 0.22
    perp_y = dx / length * 0.22
    if offset != 0:
        perp_x *= 0.5
        perp_y *= 0.5

    weight_str = str(weight)
    edge_fc = LIGHT_RED if negative or cycle_edge else 'white'
    edge_ec = '#D32F2F' if negative or cycle_edge else GRAY3
    ax.text(mx + perp_x, my + perp_y, weight_str, ha='center', va='center',
            fontsize=FS_EDGE, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', facecolor=edge_fc,
                      edgecolor=edge_ec, alpha=0.95),
            zorder=4)


def draw_neg_graph(ax, edges, title="", dist=None, current=None, visited=None,
                   relaxed_edges=None, error_nodes=None, extra_edges=None,
                   node_positions=None):
    if visited is None:
        visited = set()
    if relaxed_edges is None:
        relaxed_edges = set()
    if dist is None:
        dist = {}
    if error_nodes is None:
        error_nodes = set()
    if node_positions is None:
        node_positions = NEG_POS

    ax.set_xlim(-0.5, 7.0)
    ax.set_ylim(-0.8, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=FS, fontweight='bold', pad=5)

    all_edges = list(edges)
    if extra_edges:
        all_edges += extra_edges

    for u, v, w in all_edges:
        rl = (u, v) in relaxed_edges
        neg = w < 0
        cycle = extra_edges and (u, v, w) in extra_edges
        # If B→A and A→B both exist, offset them
        off = 0.0
        draw_edge(ax, node_positions[u], node_positions[v], w,
                  relaxed=rl, negative=neg, cycle_edge=cycle, offset=off)

    for name, pos in node_positions.items():
        is_current = (name == current)
        is_visited = (name in visited)
        d_label = dist.get(name, None)
        is_error = (name in error_nodes)
        draw_node(ax, name, pos, current=is_current, visited=is_visited,
                  dist_label=d_label, error=is_error)


def generate_bf_negative_weights():
    """
    Two-row figure:
    Row 1: Graph structure + Dijkstra WRONG + Bellman-Ford CORRECT
    Row 2: B-F iterations 1-3 step by step
    """
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('Bellman-Ford — ujemne wagi vs Dijkstra\n'
                 'Graf: S→A(2), A→C(3), S→B(5), B→A(−4). Start = S',
                 fontsize=FS_TITLE + 1, fontweight='bold', y=0.99)

    # ---- Row 1: Graph + Dijkstra wrong + BF correct ----

    # Panel 1: The graph structure
    ax1 = fig.add_subplot(2, 3, 1)
    draw_neg_graph(ax1, NEG_EDGES,
                   title='Graf z ujemną wagą\n(B→A = −4, zaznaczona na czerwono)',
                   dist={'S': '0', 'A': '?', 'B': '?', 'C': '?'})
    # START label
    ax1.annotate("START", xy=(NEG_POS['S'][0] - 0.35, NEG_POS['S'][1]),
                 xytext=(NEG_POS['S'][0] - 1.2, NEG_POS['S'][1]),
                 fontsize=FS, fontweight='bold', color='#D32F2F',
                 arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2),
                 va='center')

    # Panel 2: Dijkstra — WRONG
    ax2 = fig.add_subplot(2, 3, 2)
    draw_neg_graph(ax2, NEG_EDGES,
                   title='Dijkstra — BŁĘDNY wynik\nA zamknięty z d=2, nie poprawia przy B→A',
                   dist={'S': '0', 'A': '2', 'B': '5', 'C': '5'},
                   visited={'S', 'A', 'B', 'C'},
                   error_nodes={'A', 'C'})
    # Add "WRONG" annotations
    ax2.text(NEG_POS['A'][0] + 0.6, NEG_POS['A'][1] + 0.3, '✗ powinno 1',
             fontsize=FS_SMALL, color='#D32F2F', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.1', facecolor=LIGHT_RED,
                       edgecolor='#D32F2F', alpha=0.9, lw=0.5))
    ax2.text(NEG_POS['C'][0] + 0.05, NEG_POS['C'][1] + 0.55, '✗ powinno 4',
             fontsize=FS_SMALL, color='#D32F2F', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.1', facecolor=LIGHT_RED,
                       edgecolor='#D32F2F', alpha=0.9, lw=0.5))

    # Panel 3: Bellman-Ford — CORRECT
    ax3 = fig.add_subplot(2, 3, 3)
    draw_neg_graph(ax3, NEG_EDGES,
                   title='Bellman-Ford — POPRAWNY wynik\nUjemna waga B→A poprawnie propagowana',
                   dist={'S': '0', 'A': '1', 'B': '5', 'C': '4'},
                   visited={'S', 'A', 'B', 'C'},
                   relaxed_edges={('B', 'A')})
    ax3.text(NEG_POS['A'][0] + 0.6, NEG_POS['A'][1] + 0.3, '✓ poprawne!',
             fontsize=FS_SMALL, color='#006400', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.1', facecolor=LIGHT_GREEN,
                       edgecolor='#006400', alpha=0.9, lw=0.5))
    ax3.text(NEG_POS['C'][0] + 0.05, NEG_POS['C'][1] + 0.55, '✓ poprawne!',
             fontsize=FS_SMALL, color='#006400', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.1', facecolor=LIGHT_GREEN,
                       edgecolor='#006400', alpha=0.9, lw=0.5))

    # ---- Row 2: B-F iterations step by step ----
    iterations = [
        {
            'title': 'B-F Iteracja 1\nRelaksuj WSZYSTKIE krawędzie',
            'dist': {'S': '0', 'A': '1', 'B': '5', 'C': '5'},
            'relaxed': {('S', 'A'), ('A', 'C'), ('S', 'B'), ('B', 'A')},
            'detail': ('S→A: 0+2=2<∞ → A=2\n'
                       'A→C: 2+3=5<∞ → C=5\n'
                       'S→B: 0+5=5<∞ → B=5\n'
                       'B→A: 5−4=1<2 → A=1 ✓'),
        },
        {
            'title': 'B-F Iteracja 2\nPropagacja poprawionego A',
            'dist': {'S': '0', 'A': '1', 'B': '5', 'C': '4'},
            'relaxed': {('A', 'C')},
            'detail': ('S→A: 0+2=2>1 ✗\n'
                       'A→C: 1+3=4<5 → C=4 ✓\n'
                       'S→B: 0+5=5=5 ✗\n'
                       'B→A: 5−4=1=1 ✗'),
        },
        {
            'title': 'B-F Iteracja 3\nBrak zmian → stabilne!',
            'dist': {'S': '0', 'A': '1', 'B': '5', 'C': '4'},
            'relaxed': set(),
            'detail': ('Wszystkie krawędzie:\n'
                       'brak poprawy ✗\n'
                       '→ wynik stabilny\n'
                       '→ BRAK cyklu ujemnego'),
        },
    ]

    for i, it in enumerate(iterations):
        ax = fig.add_subplot(2, 3, i + 4)
        draw_neg_graph(ax, NEG_EDGES, title=it['title'],
                       dist=it['dist'],
                       visited={'S', 'A', 'B', 'C'},
                       relaxed_edges=it['relaxed'])
        # Detail text below graph
        ax.text(3.2, -0.5, it['detail'], ha='center', va='top',
                fontsize=FS_SMALL, family='monospace',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4,
                          edgecolor=GRAY3))

    # Bottom note
    fig.text(0.5, 0.01,
             'Dijkstra zamyka wierzchołki na stałe (zachłanność) → ujemna waga B→A(−4) nie może poprawić zamkniętego A.\n'
             'Bellman-Ford relaksuje WSZYSTKIE krawędzie w każdej iteracji → ujemne wagi propagują się poprawnie.',
             ha='center', fontsize=FS, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_YELLOW, edgecolor=LN))

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(os.path.join(OUTPUT_DIR, 'bellman_ford_negative_weights.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ bellman_ford_negative_weights.png")


def generate_bf_negative_cycle():
    """
    Figure showing negative cycle detection.
    Graph: S→A(2), A→C(3), S→B(5), B→A(−4), C→B(−3)  [added edge]
    Cycle: B→A→C→B = −4+3+(−3) = −4 < 0
    """
    cycle_edges = NEG_EDGES + [('C', 'B', -3)]

    fig = plt.figure(figsize=(14, 5.5))
    fig.suptitle('Bellman-Ford — wykrywanie cyklu ujemnego\n'
                 'Dodano krawędź C→B(−3). Cykl: B→A→C→B = −4+3+(−3) = −4 < 0',
                 fontsize=FS_TITLE + 1, fontweight='bold', y=0.99)

    # Panel 1: Graph with cycle highlighted
    ax1 = fig.add_subplot(1, 3, 1)
    draw_neg_graph(ax1, NEG_EDGES,
                   title='Graf z cyklem ujemnym\nDodana krawędź C→B(−3) — przerywana',
                   dist={'S': '0', 'A': '?', 'B': '?', 'C': '?'},
                   extra_edges=[('C', 'B', -3)])
    # Mark cycle
    ax1.annotate("CYKL\n−4+3+(−3)=−4<0",
                 xy=(3.3, 2.0),
                 fontsize=FS, fontweight='bold', color='#D32F2F',
                 ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_RED,
                           edgecolor='#D32F2F', alpha=0.9))

    # Panel 2: After V−1 iterations — still changing
    ax2 = fig.add_subplot(1, 3, 2)
    draw_neg_graph(ax2, NEG_EDGES,
                   title='Po V−1=3 iteracjach\ndist wciąż maleje (niestabilne!)',
                   dist={'S': '0', 'A': '−7', 'B': '−4', 'C': '−4'},
                   visited={'S', 'A', 'B', 'C'},
                   error_nodes={'A', 'B', 'C'},
                   extra_edges=[('C', 'B', -3)])
    ax2.text(3.2, -0.4,
             'Każde okrążenie cyklu\nzmniejsza dist o 4.\n'
             'Dist → −∞ (brak minimum!)',
             ha='center', va='top', fontsize=FS_SMALL, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_RED,
                       edgecolor='#D32F2F'))

    # Panel 3: V-th iteration detects
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.axis('off')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)

    detection_text = (
        "V-ta iteracja (sprawdzenie):\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "for (src, dst, w) in edges:\n"
        "  if dist[src]+w < dist[dst]:\n"
        "    return None  # CYKL!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Sprawdzamy np. krawędź B→A:\n"
        "  dist[B] + (−4) = −4 + (−4) = −8\n"
        "  −8 < dist[A] = −7\n"
        "  → NADAL SIĘ POPRAWIA!\n"
        "  → CYKL UJEMNY WYKRYTY!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Wynik: return None\n"
        "(najkrótsza ścieżka nie istnieje)"
    )
    ax3.text(5, 5, detection_text, ha='center', va='center',
             fontsize=FS + 0.5, family='monospace',
             bbox=dict(boxstyle='round,pad=0.6', facecolor=LIGHT_RED,
                       edgecolor='#D32F2F', lw=2))
    ax3.set_title('Wykrywanie — V-ta iteracja\nJeśli cokolwiek się poprawia → cykl ujemny!',
                  fontsize=FS, fontweight='bold', pad=5)

    # Bottom note
    fig.text(0.5, 0.01,
             'Bez cyklu ujemnego: po V−1 iteracjach dist jest stabilne. '
             'Z cyklem ujemnym: dist maleje w nieskończoność → V-ta iteracja to wykrywa.',
             ha='center', fontsize=FS, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_YELLOW, edgecolor=LN))

    plt.tight_layout(rect=[0, 0.06, 1, 0.94])
    plt.savefig(os.path.join(OUTPUT_DIR, 'bellman_ford_negative_cycle.png'),
                dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ bellman_ford_negative_cycle.png")


if __name__ == '__main__':
    print("Generating Bellman-Ford negative weight diagrams...")
    generate_bf_negative_weights()
    generate_bf_negative_cycle()
    print(f"\nAll diagrams saved to {OUTPUT_DIR}/")
