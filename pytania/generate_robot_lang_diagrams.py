#!/usr/bin/env python3
"""
Generate diagrams for PYTANIE 16: Języki programowania robotów.
A4-compatible, B&W, 300 DPI, laser-printer-friendly.

Diagrams:
  1. T-R-M-S abstraction pyramid
  2. Vendor languages comparison chart
  3. Robot movement types (PTP, LIN, CIRC)
  4. Online vs Offline programming flowchart
  5. ROS architecture (pub/sub nodes)
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
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRAY1 = '#E8E8E8'
GRAY2 = '#D0D0D0'
GRAY3 = '#B8B8B8'
GRAY4 = '#F5F5F5'
GRAY5 = '#C0C0C0'
WHITE = 'white'


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
# 1. T-R-M-S Abstraction Pyramid
# ============================================================
def draw_trms_pyramid():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Poziomy abstrakcji języków programowania robotów (T-R-M-S)',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Pyramid layers (bottom to top)
    layers = [
        # (y, left_x, right_x, label, sublabel, fill, examples, timing)
        (0.5, 1.0, 9.0, 'SERVO-LEVEL', 'Sterowanie silnikami',
         GRAY3, 'C/C++, FPGA, VHDL\nPID, PWM', '~1 ms'),
        (2.0, 1.8, 8.2, 'MOTION-LEVEL', 'Planowanie trajektorii',
         GRAY2, 'MoveIt, OMPL\nIK, collision avoidance', '~20 ms'),
        (3.5, 2.6, 7.4, 'ROBOT-LEVEL', 'Komendy ruchu',
         GRAY1, 'RAPID, KRL, Karel\nPDL2, URScript, ROS', '~100 ms'),
        (5.0, 3.4, 6.6, 'TASK-LEVEL', 'Opis celu',
         GRAY4, 'PDDL, BT, STRIPS\nplanowanie AI', '~sekundy'),
    ]

    h = 1.3
    for y, lx, rx, label, sublabel, fill, examples, timing in layers:
        w = rx - lx
        # Draw trapezoid
        trap = plt.Polygon([
            (lx, y), (rx, y),
            (rx - 0.4, y + h), (lx + 0.4, y + h)
        ], closed=True, facecolor=fill, edgecolor=LN, lw=1.5)
        ax.add_patch(trap)

        # Label
        ax.text((lx + rx) / 2, y + h * 0.65, label,
                ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text((lx + rx) / 2, y + h * 0.35, sublabel,
                ha='center', va='center', fontsize=7, style='italic')

        # Examples - right side
        ax.text(rx + 0.2, y + h * 0.5, examples,
                ha='left', va='center', fontsize=6.5, color='#333333')

        # Timing - left side
        ax.text(lx - 0.2, y + h * 0.5, timing,
                ha='right', va='center', fontsize=7, fontweight='bold',
                color='#333333')

    # Arrow on left
    ax.annotate('', xy=(0.5, 6.2), xytext=(0.5, 0.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(0.5, 3.5, 'Abstrakcja\nrośnie',
            ha='center', va='center', fontsize=7, rotation=90,
            fontweight='bold')

    # Arrow on right side for timing
    ax.annotate('', xy=(9.7, 0.8), xytext=(9.7, 6.2),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(9.7, 3.5, 'Szybkość\nreakcji',
            ha='center', va='center', fontsize=7, rotation=270,
            fontweight='bold')

    # Mnemonic at bottom
    ax.text(5.0, 0.0, 'Mnemonik: „Tomek Robi Mechaniczne Serwa" (T→R→M→S, od góry do dołu)',
            ha='center', va='center', fontsize=7, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=LN, lw=0.8))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'robot_trms_pyramid.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print("  ✓ robot_trms_pyramid.png")


# ============================================================
# 2. Vendor Languages Comparison
# ============================================================
def draw_vendor_comparison():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.axis('off')
    ax.set_title('Języki producentów robotów — porównanie',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Table headers
    headers = ['Cecha', 'RAPID\n(ABB)', 'KRL\n(KUKA)', 'Karel\n(FANUC)', 'PDL2\n(Comau)', 'URScript\n(UR)']
    col_widths = [1.8, 1.6, 1.6, 1.6, 1.6, 1.6]
    col_x = [0.1]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w)

    row_h = 0.7
    header_y = 6.3
    rows = [
        ['Składnia', 'typ własny\nstrukturalna', 'Pascal-like\nstrukturalna', 'Pascal-like\nstrukturalna', 'proceduralna\nC-like', 'Python-like\nskryptowy'],
        ['Ruch liniowy', 'MoveL', 'LIN', 'MOVE TO\nw/LINEAR', 'MOVE\nLINEAR TO', 'movel()'],
        ['Ruch joint', 'MoveJ', 'PTP', 'MOVE TO', 'MOVE TO', 'movej()'],
        ['Ruch kołowy', 'MoveC', 'CIRC', '(brak\nwbudow.)', 'MOVE\nCIRCULAR', 'movec()'],
        ['I/O', 'SetDO/\nWaitDI', 'OUT/IN', 'DOUT/DIN', 'OUT/IN', 'set_digital\n_out()'],
        ['Zmienne', 'num, robtarget\nstring, bool', 'INT, REAL\nPOS, E6POS', 'INTEGER\nPOSITION', 'INTEGER\nPOSITION', 'int, float\npose'],
        ['Symulator', 'RobotStudio', 'KUKA.Sim', 'ROBOGUIDE', 'RoboSim', 'URSim\n(darmowy)'],
    ]

    # Draw header row
    for j, (hdr, w) in enumerate(zip(headers, col_widths)):
        x = col_x[j]
        fill = GRAY2 if j == 0 else GRAY1
        draw_box(ax, x, header_y, w - 0.05, row_h, hdr, fill=fill,
                 fontsize=7, fontweight='bold', rounded=False)

    # Draw data rows
    for i, row in enumerate(rows):
        y = header_y - (i + 1) * row_h
        for j, (cell, w) in enumerate(zip(row, col_widths)):
            x = col_x[j]
            fill = GRAY4 if j == 0 else (WHITE if i % 2 == 0 else GRAY4)
            fw = 'bold' if j == 0 else 'normal'
            draw_box(ax, x, y, w - 0.05, row_h - 0.02, cell, fill=fill,
                     fontsize=6, fontweight=fw, rounded=False)

    # Note
    ax.text(5.0, 0.5, 'Vendor lock-in: program w RAPID ≠ działa na KUKA. '
            'ROS/ROS 2 jako warstwa unifikująca.',
            ha='center', va='center', fontsize=7, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=LN, lw=0.8))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'robot_vendor_comparison.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print("  ✓ robot_vendor_comparison.png")


# ============================================================
# 3. Robot Movement Types (PTP, LIN, CIRC)
# ============================================================
def draw_movement_types():
    fig, axes = plt.subplots(1, 3, figsize=(8.27, 3.2))
    fig.suptitle('Typy ruchu robota: PTP, LIN, CIRC',
                 fontsize=FS_TITLE, fontweight='bold', y=0.98)

    # --- PTP (Point-to-Point) ---
    ax = axes[0]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.set_title('PTP (Point-to-Point)\nMoveJ / PTP', fontsize=8, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Start and end
    start = (0.5, 0.5)
    end = (3.5, 3.5)
    ax.plot(*start, 'ko', ms=10, zorder=5)
    ax.plot(*end, 'ks', ms=10, zorder=5)
    ax.text(start[0] - 0.3, start[1] - 0.3, 'Start', fontsize=7, ha='center')
    ax.text(end[0] + 0.3, end[1] + 0.3, 'Cel', fontsize=7, ha='center')

    # Curved path (joint space = not necessarily straight in Cartesian)
    t = np.linspace(0, 1, 50)
    x_ptp = start[0] + (end[0] - start[0]) * t + 0.8 * np.sin(np.pi * t)
    y_ptp = start[1] + (end[1] - start[1]) * t - 0.3 * np.sin(np.pi * t)
    ax.plot(x_ptp, y_ptp, 'k-', lw=2)
    ax.annotate('', xy=(x_ptp[-1], y_ptp[-1]), xytext=(x_ptp[-3], y_ptp[-3]),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    ax.text(2.8, 1.2, 'Ścieżka\nw kartezjańskiej\nnieokreślona!', fontsize=6,
            ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=GRAY5))
    ax.text(2.0, -0.3, 'Najszybszy, ale\nścieżka nieprzewidywalna', fontsize=6,
            ha='center', style='italic')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelsize=6)

    # --- LIN (Linear) ---
    ax = axes[1]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.set_title('LIN (Linear)\nMoveL / LIN', fontsize=8, fontweight='bold')
    ax.grid(True, alpha=0.3)

    start = (0.5, 1.0)
    end = (3.5, 3.5)
    ax.plot(*start, 'ko', ms=10, zorder=5)
    ax.plot(*end, 'ks', ms=10, zorder=5)
    ax.text(start[0] - 0.3, start[1] - 0.3, 'Start', fontsize=7, ha='center')
    ax.text(end[0] + 0.3, end[1] + 0.3, 'Cel', fontsize=7, ha='center')

    # Straight line
    ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', lw=2)
    ax.annotate('', xy=end, xytext=(start[0] + 0.9*(end[0]-start[0]),
                start[1] + 0.9*(end[1]-start[1])),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    # Show intermediate points
    for frac in [0.25, 0.5, 0.75]:
        px = start[0] + frac * (end[0] - start[0])
        py = start[1] + frac * (end[1] - start[1])
        ax.plot(px, py, 'k.', ms=6)

    ax.text(2.0, -0.3, 'Prosta linia TCP\nIK w każdym punkcie', fontsize=6,
            ha='center', style='italic')
    ax.tick_params(labelsize=6)

    # --- CIRC (Circular) ---
    ax = axes[2]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.set_title('CIRC (Circular)\nMoveC / CIRC', fontsize=8, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Arc through 3 points
    center = (2.0, 1.5)
    r = 2.0
    theta_start = np.radians(20)
    theta_end = np.radians(160)
    theta = np.linspace(theta_start, theta_end, 50)
    x_circ = center[0] + r * np.cos(theta)
    y_circ = center[1] + r * np.sin(theta)

    ax.plot(x_circ, y_circ, 'k-', lw=2)
    ax.annotate('', xy=(x_circ[-1], y_circ[-1]), xytext=(x_circ[-3], y_circ[-3]),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    # Start, auxiliary, end points
    ax.plot(x_circ[0], y_circ[0], 'ko', ms=10, zorder=5)
    ax.plot(x_circ[24], y_circ[24], 'k^', ms=8, zorder=5)
    ax.plot(x_circ[-1], y_circ[-1], 'ks', ms=10, zorder=5)
    ax.text(x_circ[0] + 0.3, y_circ[0] - 0.3, 'Start', fontsize=7)
    ax.text(x_circ[24] + 0.05, y_circ[24] + 0.25, 'Pkt\npomocniczy', fontsize=6, ha='center')
    ax.text(x_circ[-1] - 0.5, y_circ[-1] - 0.3, 'Cel', fontsize=7)

    # Center
    ax.plot(*center, 'k+', ms=8, mew=1.5)
    ax.text(center[0], center[1] - 0.3, 'środek', fontsize=6, ha='center')

    ax.text(2.0, -0.3, 'Łuk wyznaczony\nprzez 3 punkty', fontsize=6,
            ha='center', style='italic')
    ax.tick_params(labelsize=6)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'robot_movement_types.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print("  ✓ robot_movement_types.png")


# ============================================================
# 4. Online vs Offline Programming
# ============================================================
def draw_online_offline():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Programowanie robotów: Online (teach-in) vs Offline',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # === ONLINE side (left) ===
    # Title
    draw_box(ax, 0.3, 5.2, 4.2, 0.8, 'ONLINE\n(teach-in / pendant)',
             fill=GRAY2, fontsize=9, fontweight='bold')

    steps_online = [
        (4.2, 'Operator przy robocie\nz teach pendantem'),
        (3.2, 'Prowadzi ramię\n„za rękę" do punktów'),
        (2.2, 'Robot zapamiętuje\npozycje (record)'),
        (1.2, 'Odtwarzanie\nzapisanej ścieżki'),
    ]
    for y, txt in steps_online:
        draw_box(ax, 0.5, y, 3.8, 0.8, txt, fill=WHITE, fontsize=7)

    for i in range(len(steps_online) - 1):
        draw_arrow(ax, 2.4, steps_online[i][0], 2.4, steps_online[i+1][0] + 0.8)

    # Pros/cons
    ax.text(2.4, 0.6, '✓ Proste, intuicyjne\n✗ Wymaga zatrzymania produkcji\n✗ Niska precyzja',
            ha='center', va='center', fontsize=6.5,
            bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=GRAY5, lw=0.8))

    # Divider
    ax.plot([4.9, 4.9], [0.3, 6.2], 'k--', lw=1, alpha=0.5)

    # === OFFLINE side (right) ===
    draw_box(ax, 5.3, 5.2, 4.2, 0.8, 'OFFLINE\n(symulacja / CAD/CAM)',
             fill=GRAY2, fontsize=9, fontweight='bold')

    steps_offline = [
        (4.2, 'Model 3D robota +\nśrodowisko w symulatorze'),
        (3.2, 'Programowanie ścieżek\nw środowisku wirtualnym'),
        (2.2, 'Weryfikacja kolizji\ni optymalizacja'),
        (1.2, 'Transfer na\nrzeczywistego robota'),
    ]
    for y, txt in steps_offline:
        draw_box(ax, 5.5, y, 3.8, 0.8, txt, fill=WHITE, fontsize=7)

    for i in range(len(steps_offline) - 1):
        draw_arrow(ax, 7.4, steps_offline[i][0], 7.4, steps_offline[i+1][0] + 0.8)

    ax.text(7.4, 0.6, '✓ Bez zatrzymania produkcji\n✓ Wysoka precyzja, symulacja\n✗ Wymaga kalibracji',
            ha='center', va='center', fontsize=6.5,
            bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=GRAY5, lw=0.8))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'robot_online_offline.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print("  ✓ robot_online_offline.png")


# ============================================================
# 5. ROS Architecture (pub/sub)
# ============================================================
def draw_ros_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('ROS — architektura publish/subscribe',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Nodes
    nodes = [
        (1.0, 4.5, 'Czujnik\n(LiDAR)', GRAY1),
        (1.0, 2.5, 'Kamera\n(RGB-D)', GRAY1),
        (4.0, 4.5, 'Lokalizacja\n(SLAM)', GRAY4),
        (4.0, 2.5, 'Percepcja\n(detekcja)', GRAY4),
        (7.0, 3.5, 'Planowanie\nruchu (MoveIt)', GRAY2),
        (7.0, 1.0, 'Sterownik\nsilników', GRAY3),
    ]

    for x, y, txt, fill in nodes:
        draw_box(ax, x, y, 2.2, 1.0, txt, fill=fill, fontsize=7, fontweight='bold')

    # Topics (arrows with labels)
    topics = [
        # (from_x, from_y, to_x, to_y, label)
        (3.2, 5.0, 4.0, 5.0, '/scan'),
        (3.2, 3.0, 4.0, 3.0, '/image'),
        (6.2, 5.0, 7.0, 4.3, '/pose'),
        (6.2, 3.0, 7.0, 3.8, '/objects'),
        (8.0, 3.5, 8.0, 2.0, '/cmd_vel'),
    ]

    for x1, y1, x2, y2, label in topics:
        draw_arrow(ax, x1, y1, x2, y2, lw=1.5)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.2, label, ha='center', va='bottom', fontsize=6,
                fontweight='bold', style='italic',
                bbox=dict(boxstyle='round,pad=0.15', facecolor=WHITE,
                          edgecolor=GRAY5, lw=0.5))

    # ROS Master / roscore
    draw_box(ax, 3.5, 0.3, 3.0, 0.8, 'ROS Master (roscore)\nRejestr węzłów i tematów',
             fill=GRAY2, fontsize=7, fontweight='bold')

    # Dashed lines to master
    for x, y, _, _ in nodes[:4]:
        ax.plot([x + 1.1, 5.0], [y, 1.1], 'k:', lw=0.5, alpha=0.4)

    # Legend
    ax.text(0.3, 0.8, 'Węzeł (Node) = proces\n'
            'Temat (Topic) = kanał pub/sub\n'
            'Wiadomość = typowany komunikat',
            ha='left', va='center', fontsize=6,
            bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=LN, lw=0.8))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'robot_ros_architecture.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print("  ✓ robot_ros_architecture.png")


# ============================================================
# 6. RAPID program structure example
# ============================================================
def draw_rapid_structure():
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Struktura programu RAPID (ABB) — przykład pick & place',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Program structure blocks
    y = 7.0
    blocks = [
        ('MODULE MainModule', GRAY2, 0.5, 9.0, [
            ('! Deklaracja danych', GRAY4, 1.0, 8.5, [
                'CONST robtarget pHome := [...];',
                'CONST robtarget pPick := [...];',
                'CONST robtarget pPlace := [...];',
                'VAR num nCycles := 0;',
            ]),
            ('PROC main()', GRAY1, 1.0, 8.5, [
                'MoveJ pHome, v1000, z50, tool1;',
                'WHILE TRUE DO',
                '    PickPart;',
                '    PlacePart;',
                '    Incr nCycles;',
                'ENDWHILE',
            ]),
            ('PROC PickPart()', GRAY1, 1.0, 8.5, [
                'MoveL Offs(pPick,0,0,50), v500, z10, tool1;',
                'MoveL pPick, v100, fine, tool1;',
                'SetDO doGripper, 1;  ! zamknij chwytak',
                'WaitTime 0.5;',
                'MoveL Offs(pPick,0,0,50), v500, z10, tool1;',
            ]),
        ]),
    ]

    # Simplified: just draw code blocks
    code_sections = [
        ('Deklaracje danych (stałe, zmienne)', GRAY4, [
            'CONST robtarget pHome := [[500,0,600],[1,0,0,0],...];',
            'CONST robtarget pPick := [[400,200,100],[1,0,0,0],...];',
            'CONST robtarget pPlace := [[400,-200,100],[1,0,0,0],...];',
            'VAR num nCycles := 0;',
            'PERS tooldata tGripper := [...];',
        ]),
        ('Procedura główna: main()', GRAY1, [
            'PROC main()',
            '    MoveJ pHome, v1000, z50, tGripper;',
            '    WHILE TRUE DO',
            '        PickPart;',
            '        PlacePart;',
            '        Incr nCycles;',
            '    ENDWHILE',
            'ENDPROC',
        ]),
        ('Podprocedura: PickPart()', GRAY1, [
            'PROC PickPart()',
            '    MoveL Offs(pPick,0,0,50), v500, z10, tGripper;',
            '    MoveL pPick, v100, fine, tGripper;',
            '    SetDO doGripper, 1;    ! zamknij chwytak',
            '    WaitTime 0.5;',
            '    MoveL Offs(pPick,0,0,50), v500, z10, tGripper;',
            'ENDPROC',
        ]),
    ]

    y_cur = 7.2
    for title, fill, lines in code_sections:
        h = 0.25 * len(lines) + 0.5
        # Title bar
        draw_box(ax, 0.5, y_cur - 0.35, 9.0, 0.35, title, fill=fill,
                 fontsize=7, fontweight='bold', rounded=False)
        y_cur -= 0.35

        # Code lines
        for i, line in enumerate(lines):
            y_cur -= 0.25
            ax.text(0.7, y_cur + 0.12, line, fontsize=5.5,
                    fontfamily='monospace', va='center')

        # Border around code
        code_h = 0.25 * len(lines)
        rect = mpatches.Rectangle((0.5, y_cur - 0.05), 9.0, code_h + 0.15,
                                  lw=0.8, edgecolor=GRAY5, facecolor=WHITE,
                                  zorder=-1)
        ax.add_patch(rect)

        y_cur -= 0.3

    # Annotations on right
    annotations = [
        (6.5, 'robtarget = pozycja\nkartezjańska + orientacja\n+ konfiguracja ramienia'),
        (4.5, 'v500 = prędkość 500 mm/s\nz10 = strefa zbliżenia 10mm\nfine = dokładne dojście'),
        (2.5, 'SetDO = Digital Output\nSterowanie I/O\n(chwytak, zawory)'),
    ]

    for yy, txt in annotations:
        ax.text(9.8, yy, txt, fontsize=5.5, ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4,
                          edgecolor=GRAY5, lw=0.5))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'robot_rapid_example.png'), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print("  ✓ robot_rapid_example.png")


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating PYTANIE 16 diagrams...")
    draw_trms_pyramid()
    draw_vendor_comparison()
    draw_movement_types()
    draw_online_offline()
    draw_ros_architecture()
    draw_rapid_structure()
    print("Done! All diagrams saved to", OUTPUT_DIR)
