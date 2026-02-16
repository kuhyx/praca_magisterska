#!/usr/bin/env python3
"""
Generate study diagrams for defense preparation:
  1. PYTANIE 12: Network optimization models (mnemonic overview)
  2. PYTANIE 21: Vector clock timeline
  3. PYTANIE 22: Linearizability vs Sequential consistency, Paxos flow
  4. PYTANIE 23: Segmentation types and over-segmentation
  5. PYTANIE 24: HOG pipeline, SVM margin, R-CNN vs YOLO architecture

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
FS_TITLE = 12
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
# PYTANIE 12: Network Optimization Models (Mnemonic Overview)
# ============================================================
def draw_network_models():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Sieciowe modele optymalizacji — „Nasz Mały Mikołaj Przydzielił Trasy Ciężarówkom Mapując"',
                 fontsize=10, fontweight='bold', pad=10)

    models = [
        (1, "Najkrótsza\nścieżka", "GPS, routing\nDijkstra, A*", "A→B najszybciej?", GRAY1),
        (2, "Maksymalny\nprzepływ", "Przepustowość\nFord-Fulkerson", "Ile max przesłać?", GRAY4),
        (3, "Min koszt\nprzepływu", "Najtańszy transport\nSieciowy simpleks", "X jednostek najtaniej?", GRAY4),
        (4, "Przydział\n(assignment)", "n→n, min koszt\nAlg. Węgierski O(n³)", "Kto robi co?", GRAY2),
        (5, "TSP\n(komiwojażer)", "Objazd miast\nNP-trudny, heurystyki", "Objazd wszystkiego?", GRAY3),
        (6, "CPM/PERT", "Harmonogram\nŚcieżka krytyczna", "Ile trwa projekt?", GRAY2),
        (7, "MST\n(drzewo rozp.)", "Min połączenie\nKruskal, Prim", "Połącz najtaniej?", GRAY1),
    ]

    # Layout: 3 pairs + 1, arranged in labeled groups
    group_positions = [
        # (group_label, [(model_idx, x, y), ...])
        ("DROGI", [(0, 0.3, 4.0), (6, 0.3, 1.5)]),
        ("PRZEPŁYW", [(1, 3.3, 4.0), (2, 3.3, 1.5)]),
        ("ZARZĄDZANIE", [(3, 6.3, 4.0), (5, 6.3, 1.5)]),
    ]

    box_w = 2.6
    box_h = 1.8

    for group_label, items in group_positions:
        xs = [x for _, x, y in items]
        ys = [y for _, x, y in items]
        gx = min(xs) - 0.15
        gy = min(ys) - 0.3
        gw = box_w + 0.3
        gh = max(ys) - min(ys) + box_h + 0.6
        rect = mpatches.FancyBboxPatch((gx, gy), gw, gh,
                                        boxstyle="round,pad=0.1",
                                        lw=0.8, edgecolor=GRAY3,
                                        facecolor='white', linestyle='--')
        ax.add_patch(rect)
        ax.text(gx + gw/2, gy + gh + 0.12, group_label, ha='center',
                fontsize=8, fontweight='bold', color='#555555')

        for idx, x, y in items:
            num, name, detail, question, fill = models[idx]
            draw_box(ax, x, y, box_w, box_h, '', fill=fill, fontsize=FS)
            ax.text(x + box_w/2, y + box_h - 0.25, f"{num}. {name}",
                    ha='center', va='top', fontsize=8, fontweight='bold')
            ax.text(x + box_w/2, y + box_h/2 - 0.1, detail,
                    ha='center', va='center', fontsize=7)
            ax.text(x + box_w/2, y + 0.2, f'→ „{question}"',
                    ha='center', va='bottom', fontsize=6.5, style='italic')

    # TSP alone at bottom center
    idx = 4
    x, y = 4.5, -0.1
    num, name, detail, question, fill = models[idx]
    rect = mpatches.FancyBboxPatch((x - 0.15, y - 0.15), box_w + 0.3, box_h + 0.3,
                                    boxstyle="round,pad=0.1",
                                    lw=0.8, edgecolor=GRAY3,
                                    facecolor='white', linestyle='--')
    ax.add_patch(rect)
    ax.text(x + box_w/2, y + box_h + 0.3, "SAM (NP-trudny)",
            ha='center', fontsize=8, fontweight='bold', color='#555555')
    draw_box(ax, x, y, box_w, box_h, '', fill=fill, fontsize=FS)
    ax.text(x + box_w/2, y + box_h - 0.25, f"{num}. {name}",
            ha='center', va='top', fontsize=8, fontweight='bold')
    ax.text(x + box_w/2, y + box_h/2 - 0.1, detail,
            ha='center', va='center', fontsize=7)
    ax.text(x + box_w/2, y + 0.2, f'→ „{question}"',
            ha='center', va='bottom', fontsize=6.5, style='italic')

    ax.set_ylim(-0.5, 7.2)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'network_models_mnemonic.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ network_models_mnemonic.png")


# ============================================================
# PYTANIE 21: Vector Clock Timeline
# ============================================================
def draw_vector_clock_timeline():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 4.5))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title('Zegary wektorowe — przykład z 3 procesami', fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Process lines
    procs = [('P₁', 3.5), ('P₂', 2.0), ('P₃', 0.5)]
    for name, y in procs:
        ax.plot([0.5, 10.5], [y, y], color=LN, lw=1.5)
        ax.text(0.1, y, name, ha='right', va='center', fontsize=10, fontweight='bold')

    # Events
    events = [
        # (name, process_y, x, vector, fill)
        ('A', 3.5, 1.5, '[1,0,0]', GRAY1),
        ('B', 2.0, 2.5, '[0,1,0]', GRAY2),
        ('C', 2.0, 5.0, '[1,2,0]', GRAY2),
        ('D', 0.5, 4.0, '[0,0,1]', GRAY3),
        ('E', 3.5, 6.5, '[2,0,0]', GRAY1),
        ('F', 2.0, 8.0, '[2,3,0]', GRAY2),
    ]

    for name, y, x, vec, fill in events:
        circle = plt.Circle((x, y), 0.25, facecolor=fill, edgecolor=LN, lw=1.5)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(x, y + 0.45, vec, ha='center', va='bottom', fontsize=7,
                fontfamily='monospace', color='#333333')

    # Messages (arrows between processes)
    # P1:A → P2:C  (msg sent after A, received at C)
    ax.annotate("", xy=(4.75, 2.0), xytext=(1.75, 3.5),
                arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5,
                               connectionstyle='arc3,rad=0.05'))
    ax.text(3.0, 3.0, 'msg₁', ha='center', fontsize=7, color='#444444', style='italic')

    # P1:E → P2:F
    ax.annotate("", xy=(7.75, 2.0), xytext=(6.75, 3.5),
                arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5,
                               connectionstyle='arc3,rad=0.05'))
    ax.text(7.0, 3.0, 'msg₂', ha='center', fontsize=7, color='#444444', style='italic')

    # Concurrency annotations
    ax.annotate('A ∥ B\n(współbieżne)', xy=(2.0, 1.2), fontsize=7, ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))
    ax.annotate('C ∥ D\n(współbieżne)', xy=(4.5, 0.9), fontsize=7, ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))
    ax.annotate('A → C\n(przyczynowe)', xy=(3.3, 4.2), fontsize=7, ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY1, edgecolor=GRAY3))

    # Time arrow
    ax.annotate("", xy=(10.5, -0.3), xytext=(0.5, -0.3),
                arrowprops=dict(arrowstyle='->', color=GRAY3, lw=1.0))
    ax.text(5.5, -0.45, 'czas →', ha='center', fontsize=8, color='#777777')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'vector_clock_timeline.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ vector_clock_timeline.png")


# ============================================================
# PYTANIE 22: Linearizability vs Sequential Consistency
# ============================================================
def draw_linearizability_vs_sequential():
    fig, axes = plt.subplots(2, 1, figsize=(8.27, 5.5))

    for i, (ax, title, subtitle, operations, result_text) in enumerate(zip(
        axes,
        ['Linearizability', 'Sequential Consistency'],
        ['Operacja „wygląda" atomowo w czasie rzeczywistym',
         'Globalny porządek zgodny z programem, ale NIE z czasem rzeczywistym'],
        [
            # Linearizability
            [
                ('Klient A', 1, 3, 'write(x,1)', GRAY1),
                ('Klient B', 2, 4, 'read(x)→1 ✓', GRAY2),
                ('Klient A', 5, 7, 'write(x,2)', GRAY1),
            ],
            # Sequential consistency
            [
                ('Klient A', 1, 3, 'write(x,1)', GRAY1),
                ('Klient B', 2, 4, 'read(x)→0 ✓', GRAY2),
                ('Klient A', 5, 7, 'write(x,2)', GRAY1),
            ],
        ],
        [
            'read MUSI zwrócić 1 (write zakończony w czasie rzeczywistym)',
            'read MOŻE zwrócić 0 (globalny porządek: read, write(1), write(2))',
        ]
    )):
        ax.set_xlim(0, 9)
        ax.set_ylim(-0.5, 3.5)
        ax.axis('off')
        ax.set_title(f'{title}', fontsize=10, fontweight='bold')
        ax.text(4.5, 3.2, subtitle, ha='center', fontsize=7, style='italic', color='#555555')

        # Time axis
        ax.plot([0.5, 8.5], [0, 0], color=GRAY3, lw=0.8)
        for t in range(1, 9):
            ax.plot([t, t], [-0.05, 0.05], color=GRAY3, lw=0.8)
            ax.text(t, -0.2, f't{t}', ha='center', fontsize=6, color='#999999')

        # Client labels
        clients = list(dict.fromkeys([op[0] for op in operations]))
        client_y = {c: 1.0 + idx * 1.2 for idx, c in enumerate(clients)}

        for client_name, y_pos in client_y.items():
            ax.text(0.3, y_pos, client_name, ha='right', va='center', fontsize=7, fontweight='bold')
            ax.plot([0.5, 8.5], [y_pos, y_pos], color=GRAY5, lw=0.5, linestyle=':')

        for client, t_start, t_end, label, fill in operations:
            y = client_y[client]
            rect = FancyBboxPatch((t_start, y - 0.2), t_end - t_start, 0.4,
                                  boxstyle="round,pad=0.05", lw=1.2,
                                  edgecolor=LN, facecolor=fill)
            ax.add_patch(rect)
            ax.text((t_start + t_end) / 2, y, label, ha='center', va='center', fontsize=7)

        # Result annotation
        ax.text(4.5, -0.45, result_text, ha='center', fontsize=7,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY5))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'linearizability_vs_sequential.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ linearizability_vs_sequential.png")


# ============================================================
# PYTANIE 22: Paxos Protocol Flow
# ============================================================
def draw_paxos_flow():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 5)
    ax.axis('off')
    ax.set_title('Paxos — uproszczony przebieg (zapis x=5)', fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Actors
    actors = [
        ('Proposer', 1.5, 4.0, GRAY1),
        ('A₁', 4.5, 4.0, GRAY2),
        ('A₂', 6.5, 4.0, GRAY2),
        ('A₃', 8.5, 4.0, GRAY2),
    ]
    for name, x, y, fill in actors:
        draw_box(ax, x - 0.6, y, 1.2, 0.6, name, fill=fill, fontsize=8, fontweight='bold')

    # Phase 1: Prepare
    ax.text(-0.3, 3.5, 'FAZA 1\nPrepare', ha='center', fontsize=7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    y_prep = 3.3
    for target_x in [4.5, 6.5, 8.5]:
        draw_arrow(ax, 2.1, y_prep + 0.15, target_x - 0.6, y_prep + 0.15, lw=1.0)
    ax.text(3.3, y_prep + 0.35, 'Prepare(n=1)', fontsize=6, ha='center')

    # Promises back
    y_prom = 2.7
    for target_x in [4.5, 6.5]:
        draw_arrow(ax, target_x - 0.6, y_prom + 0.15, 2.1, y_prom + 0.15, lw=1.0, color='#555555')
    ax.text(3.3, y_prom + 0.35, 'Promise(n=1) ✓', fontsize=6, ha='center', color='#555555')
    ax.text(8.5, y_prom + 0.15, '(slow)', fontsize=6, ha='center', color='#999999')

    ax.text(1.5, y_prom - 0.15, 'majority\n(2/3) ✓', fontsize=6, ha='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor=GRAY1, edgecolor=GRAY3))

    # Phase 2: Accept
    ax.text(-0.3, 1.8, 'FAZA 2\nAccept', ha='center', fontsize=7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    y_acc = 1.6
    for target_x in [4.5, 6.5, 8.5]:
        draw_arrow(ax, 2.1, y_acc + 0.15, target_x - 0.6, y_acc + 0.15, lw=1.0)
    ax.text(3.3, y_acc + 0.35, 'Accept(n=1, x=5)', fontsize=6, ha='center')

    # Accepted back
    y_accd = 1.0
    for target_x in [4.5, 6.5]:
        draw_arrow(ax, target_x - 0.6, y_accd + 0.15, 2.1, y_accd + 0.15, lw=1.0, color='#555555')
    ax.text(3.3, y_accd + 0.35, 'Accepted ✓', fontsize=6, ha='center', color='#555555')

    # Result
    ax.text(5.0, 0.1, 'x=5 UZGODNIONE (majority zaakceptowała) → Linearizable!',
            fontsize=8, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY1, edgecolor=LN))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'paxos_flow.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ paxos_flow.png")


# ============================================================
# PYTANIE 24: HOG Pipeline Overview
# ============================================================
def draw_hog_pipeline():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_title('HOG + SVM — pipeline detekcji pieszych', fontsize=FS_TITLE, fontweight='bold', pad=10)

    steps = [
        (0.3, 'Obraz\nwejściowy', GRAY4),
        (2.1, 'Oblicz\ngradienty\n(Gx, Gy)', GRAY1),
        (3.9, 'Podziel na\nkomórki 8×8\nhistogramy', GRAY2),
        (5.7, 'Normalizuj\nw blokach\n2×2', GRAY2),
        (7.5, 'Wektor\ncech\n(3780-dim)', GRAY3),
        (9.0, 'SVM\n→ pieszy\n/ nie', GRAY1),
    ]

    box_w = 1.5
    box_h = 1.8
    y = 1.2
    for i, (x, text, fill) in enumerate(steps):
        draw_box(ax, x, y, box_w, box_h, '', fill=fill)
        ax.text(x + box_w/2, y + box_h/2, text, ha='center', va='center', fontsize=7)
        if i < len(steps) - 1:
            next_x = steps[i+1][0]
            draw_arrow(ax, x + box_w + 0.02, y + box_h/2, next_x - 0.02, y + box_h/2)

    # Annotations below
    annotations = [
        (0.3 + box_w/2, 'pixel[x+1]-pixel[x-1]'),
        (2.1 + box_w/2, 'magnitude + direction'),
        (3.9 + box_w/2, '9 binów (0°-180°)'),
        (5.7 + box_w/2, 'L2-normalizacja'),
        (7.5 + box_w/2, 'wejście do SVM'),
        (9.0 + box_w/2, 'hiperpłaszczyzna'),
    ]
    for x, text in annotations:
        ax.text(x, y - 0.15, text, ha='center', fontsize=5.5, color='#666666', style='italic')

    # Title annotations
    ax.text(1.05, y + box_h + 0.15, '① Gradient', ha='center', fontsize=7, fontweight='bold')
    ax.text(2.85, y + box_h + 0.15, '② Histogram', ha='center', fontsize=7, fontweight='bold')
    ax.text(4.65, y + box_h + 0.15, '③ Normalize', ha='center', fontsize=7, fontweight='bold')
    ax.text(6.45, y + box_h + 0.15, '④ Feature vec', ha='center', fontsize=7, fontweight='bold')
    ax.text(8.1, y + box_h + 0.15, '⑤ Classify', ha='center', fontsize=7, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'hog_svm_pipeline.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ hog_svm_pipeline.png")


# ============================================================
# PYTANIE 24: R-CNN Evolution
# ============================================================
def draw_rcnn_evolution():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Ewolucja detektorów: R-CNN → Fast R-CNN → Faster R-CNN → YOLO',
                 fontsize=10, fontweight='bold', pad=10)

    models = [
        {
            'name': 'R-CNN (2014)',
            'y': 5.3,
            'steps': ['Selective\nSearch', '2000×\nCNN', '2000×\nSVM', 'NMS'],
            'speed': '~50 sec/img',
            'fill': GRAY4,
        },
        {
            'name': 'Fast R-CNN (2015)',
            'y': 3.7,
            'steps': ['Selective\nSearch', 'CNN\n(1× cały)', 'ROI\nPooling', 'FC + NMS'],
            'speed': '~2 sec/img',
            'fill': GRAY2,
        },
        {
            'name': 'Faster R-CNN (2015)',
            'y': 2.1,
            'steps': ['CNN\nbackbone', 'RPN\n(proposals)', 'ROI\nPooling', 'FC + NMS'],
            'speed': '~0.2 sec (5 fps)',
            'fill': GRAY1,
        },
        {
            'name': 'YOLO (2016)',
            'y': 0.5,
            'steps': ['CNN\nbackbone', 'Siatka\nS×S', 'bbox+klasa\nper komórka', 'NMS'],
            'speed': '~7-22 ms (45-155 fps)',
            'fill': GRAY3,
        },
    ]

    for model in models:
        y = model['y']
        ax.text(0.2, y + 0.4, model['name'], fontsize=8, fontweight='bold', va='center')
        ax.text(0.2, y + 0.05, model['speed'], fontsize=6, va='center', color='#666666')

        bw = 1.5
        bh = 0.8
        for i, step in enumerate(model['steps']):
            x = 2.5 + i * 1.9
            draw_box(ax, x, y, bw, bh, step, fill=model['fill'], fontsize=6.5)
            if i < len(model['steps']) - 1:
                draw_arrow(ax, x + bw + 0.02, y + bh/2, x + 1.9 - 0.02, y + bh/2, lw=0.8)

    # Speed improvement arrow on right
    ax.annotate("", xy=(9.5, 5.7), xytext=(9.5, 0.9),
                arrowprops=dict(arrowstyle='<->', color='#555555', lw=1.5))
    ax.text(9.7, 3.3, '250×\nszybciej!', fontsize=8, fontweight='bold',
            ha='center', va='center', rotation=90, color='#555555')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'rcnn_evolution.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ rcnn_evolution.png")


# ============================================================
# PYTANIE 23: Segmentation types comparison
# ============================================================
def draw_segmentation_types():
    fig, axes = plt.subplots(1, 4, figsize=(8.27, 2.5))
    fig.suptitle('Typy segmentacji obrazu', fontsize=FS_TITLE, fontweight='bold', y=1.02)

    titles = ['Obraz wejściowy', 'Semantic\nSegmentation', 'Instance\nSegmentation', 'Panoptic\nSegmentation']
    for ax, title in zip(axes, titles):
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=8, fontweight='bold', pad=5)

    # Image: sky (top), two cars (bottom), road
    # Semantic: all sky=one color, all cars=one color, road=one color
    # Instance: sky=one, car1=distinct, car2=distinct, road=one
    # Panoptic: both

    # Original image (stylized)
    ax = axes[0]
    ax.add_patch(mpatches.Rectangle((0, 4), 6, 2, facecolor='#DDDDDD', edgecolor=LN, lw=0.5))  # sky
    ax.text(3, 5, 'niebo', ha='center', va='center', fontsize=7)
    ax.add_patch(mpatches.Rectangle((0, 0), 6, 2.5, facecolor='#AAAAAA', edgecolor=LN, lw=0.5))  # road
    ax.text(3, 1, 'droga', ha='center', va='center', fontsize=7)
    ax.add_patch(mpatches.Rectangle((0.5, 2), 2, 1.5, facecolor='#888888', edgecolor=LN, lw=0.8))  # car1
    ax.text(1.5, 2.75, 'auto', ha='center', va='center', fontsize=7, color='white')
    ax.add_patch(mpatches.Rectangle((3.5, 2), 2, 1.5, facecolor='#666666', edgecolor=LN, lw=0.8))  # car2
    ax.text(4.5, 2.75, 'auto', ha='center', va='center', fontsize=7, color='white')

    # Semantic: same label for both cars
    ax = axes[1]
    ax.add_patch(mpatches.Rectangle((0, 4), 6, 2, facecolor='#E8E8E8', edgecolor=LN, lw=0.5))
    ax.text(3, 5, 'niebo', ha='center', va='center', fontsize=7)
    ax.add_patch(mpatches.Rectangle((0, 0), 6, 2.5, facecolor='#C8C8C8', edgecolor=LN, lw=0.5))
    ax.text(3, 1, 'droga', ha='center', va='center', fontsize=7)
    ax.add_patch(mpatches.Rectangle((0.5, 2), 2, 1.5, facecolor='#888888', edgecolor=LN, lw=0.8))
    ax.text(1.5, 2.75, 'auto', ha='center', va='center', fontsize=6, color='white')
    ax.add_patch(mpatches.Rectangle((3.5, 2), 2, 1.5, facecolor='#888888', edgecolor=LN, lw=0.8))
    ax.text(4.5, 2.75, 'auto', ha='center', va='center', fontsize=6, color='white')
    ax.text(3, -0.3, 'te same etykiety!', ha='center', fontsize=6, color='#555555', style='italic')

    # Instance: different labels for cars
    ax = axes[2]
    ax.add_patch(mpatches.Rectangle((0, 4), 6, 2, facecolor='#E8E8E8', edgecolor=LN, lw=0.5))
    ax.text(3, 5, '—', ha='center', va='center', fontsize=7, color='#999999')
    ax.add_patch(mpatches.Rectangle((0, 0), 6, 2.5, facecolor='#E8E8E8', edgecolor=LN, lw=0.5))
    ax.text(3, 1, '—', ha='center', va='center', fontsize=7, color='#999999')
    ax.add_patch(mpatches.Rectangle((0.5, 2), 2, 1.5, facecolor='#888888', edgecolor=LN, lw=0.8))
    ax.text(1.5, 2.75, 'auto#1', ha='center', va='center', fontsize=6, color='white')
    ax.add_patch(mpatches.Rectangle((3.5, 2), 2, 1.5, facecolor='#555555', edgecolor=LN, lw=0.8))
    ax.text(4.5, 2.75, 'auto#2', ha='center', va='center', fontsize=6, color='white')
    ax.text(3, -0.3, 'RÓŻNE instancje!', ha='center', fontsize=6, color='#555555', style='italic')

    # Panoptic: both semantic labels AND instance IDs
    ax = axes[3]
    ax.add_patch(mpatches.Rectangle((0, 4), 6, 2, facecolor='#E8E8E8', edgecolor=LN, lw=0.5))
    ax.text(3, 5, 'niebo (stuff)', ha='center', va='center', fontsize=6)
    ax.add_patch(mpatches.Rectangle((0, 0), 6, 2.5, facecolor='#C8C8C8', edgecolor=LN, lw=0.5))
    ax.text(3, 1, 'droga (stuff)', ha='center', va='center', fontsize=6)
    ax.add_patch(mpatches.Rectangle((0.5, 2), 2, 1.5, facecolor='#888888', edgecolor=LN, lw=0.8))
    ax.text(1.5, 2.75, 'auto#1\n(thing)', ha='center', va='center', fontsize=5.5, color='white')
    ax.add_patch(mpatches.Rectangle((3.5, 2), 2, 1.5, facecolor='#555555', edgecolor=LN, lw=0.8))
    ax.text(4.5, 2.75, 'auto#2\n(thing)', ha='center', va='center', fontsize=5.5, color='white')
    ax.text(3, -0.3, 'klasy + instancje!', ha='center', fontsize=6, color='#555555', style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'segmentation_types.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ segmentation_types.png")


# ============================================================
# PYTANIE 32: FSD and SSD visualization
# ============================================================
def draw_fsd_ssd():
    fig, axes = plt.subplots(1, 2, figsize=(8.27, 3.5))
    fig.suptitle('Dominacja stochastyczna — FSD i SSD', fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # FSD: CDF comparison
    ax = axes[0]
    ax.set_title('FSD: F_A(x) ≤ F_B(x) ∀x', fontsize=9, fontweight='bold')
    x = np.linspace(-2, 6, 200)
    # A ~ shifted right (better), B ~ shifted left
    from scipy.stats import norm
    F_A = norm.cdf(x, loc=2.5, scale=1.0)
    F_B = norm.cdf(x, loc=1.5, scale=1.0)
    ax.plot(x, F_A, 'k-', lw=2, label='F_A (lepsza — niżej)')
    ax.plot(x, F_B, 'k--', lw=2, label='F_B (gorsza — wyżej)')
    ax.fill_between(x, F_A, F_B, alpha=0.15, color='gray')
    ax.set_xlabel('x (wynik)', fontsize=8)
    ax.set_ylabel('F(x) = P(X ≤ x)', fontsize=8)
    ax.legend(fontsize=7, loc='lower right')
    ax.text(0, 0.8, 'A ≥_FSD B\nF_A zawsze pod F_B\n→ KAŻDY racjonalny\n   wybierze A',
            fontsize=7, bbox=dict(boxstyle='round', facecolor=GRAY4))
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=7)

    # SSD: CDFs can cross, but integral is less
    ax = axes[1]
    ax.set_title('SSD: ∫F_A ≤ ∫F_B ∀x (CDFs mogą się krzyżować)', fontsize=9, fontweight='bold')
    F_A2 = norm.cdf(x, loc=2.0, scale=0.8)
    F_B2 = norm.cdf(x, loc=2.0, scale=1.5)  # same mean, more spread
    ax.plot(x, F_A2, 'k-', lw=2, label='F_A (mniej ryzyka)')
    ax.plot(x, F_B2, 'k--', lw=2, label='F_B (więcej ryzyka)')
    ax.fill_between(x, F_A2, F_B2, where=F_A2 < F_B2, alpha=0.15, color='gray')
    ax.fill_between(x, F_A2, F_B2, where=F_A2 >= F_B2, alpha=0.08, color='gray',
                    hatch='///')
    ax.set_xlabel('x (wynik)', fontsize=8)
    ax.set_ylabel('F(x)', fontsize=8)
    ax.legend(fontsize=7, loc='lower right')
    ax.text(-1.5, 0.75, 'A ≥_SSD B\nCDFs się krzyżują,\nale ∫F_A ≤ ∫F_B\n→ risk-averse\n   wybierze A',
            fontsize=7, bbox=dict(boxstyle='round', facecolor=GRAY4))
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=7)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fsd_ssd_comparison.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close()
    print("  ✓ fsd_ssd_comparison.png")


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating study diagrams...")
    draw_network_models()
    draw_vector_clock_timeline()
    draw_linearizability_vs_sequential()
    draw_paxos_flow()
    draw_hog_pipeline()
    draw_rcnn_evolution()
    draw_segmentation_types()
    draw_fsd_ssd()
    print(f"\nAll diagrams saved to {OUTPUT_DIR}/")
