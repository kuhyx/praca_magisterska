#!/usr/bin/env python3
"""
Generate ALL diagrams for PYTANIE 24: Detekcja obiektów.
Monochrome, A4-printable PNGs (300 DPI).
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
FS_LABEL = 9
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRAY1 = '#E8E8E8'
GRAY2 = '#D0D0D0'
GRAY3 = '#B8B8B8'
GRAY4 = '#F5F5F5'
GRAY5 = '#C0C0C0'


def draw_box(ax, x, y, w, h, text, fill='white', lw=1.2, fontsize=FS,
             fontweight='normal', ha='center', va='center', rounded=True,
             edgecolor=LN, linestyle='-'):
    if rounded:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              lw=lw, edgecolor=edgecolor, facecolor=fill,
                              linestyle=linestyle)
    else:
        rect = mpatches.Rectangle((x, y), w, h, lw=lw, edgecolor=edgecolor,
                                  facecolor=fill, linestyle=linestyle)
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


def draw_table(ax, headers, rows, x0, y0, col_widths, row_h=0.4,
               header_fill=GRAY2, row_fills=None, fontsize=FS, header_fontsize=None):
    if header_fontsize is None:
        header_fontsize = fontsize
    n_cols = len(headers)
    cx = x0
    for j, hdr in enumerate(headers):
        draw_box(ax, cx, y0, col_widths[j], row_h, hdr, fill=header_fill,
                 fontsize=header_fontsize, fontweight='bold', rounded=False)
        cx += col_widths[j]
    for i, row in enumerate(rows):
        cy = y0 - (i + 1) * row_h
        cx = x0
        fill = GRAY4 if (i % 2 == 0) else 'white'
        if row_fills and i < len(row_fills):
            fill = row_fills[i]
        for j, cell in enumerate(row):
            fw = 'bold' if j == 0 else 'normal'
            draw_box(ax, cx, cy, col_widths[j], row_h, cell, fill=fill,
                     fontsize=fontsize, fontweight=fw, rounded=False)
            cx += col_widths[j]


# ============================================================
# 1. HOG + SVM Pipeline
# ============================================================
def draw_hog_svm_pipeline():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('HOG + SVM — pipeline detekcji pieszych', fontsize=FS_TITLE,
                 fontweight='bold', pad=12)

    # Step 1: Image with sliding window
    ax.add_patch(mpatches.Rectangle((0, 1.5), 2, 2, lw=1.5, edgecolor=LN,
                                     facecolor=GRAY1))
    ax.text(1, 2.5, 'Obraz\nwejściowy', ha='center', va='center', fontsize=FS)
    # sliding window overlay
    ax.add_patch(mpatches.Rectangle((0.3, 1.8), 0.8, 1.2, lw=1.5, edgecolor='black',
                                     facecolor='none', linestyle='--'))
    ax.text(0.7, 1.35, 'okno 64×128', ha='center', va='center', fontsize=FS_SMALL,
            style='italic')

    draw_arrow(ax, 2.1, 2.5, 2.8, 2.5, lw=1.5)
    ax.text(2.45, 2.75, '①', ha='center', fontsize=FS_LABEL, fontweight='bold')

    # Step 2: Gradient computation
    draw_box(ax, 2.9, 1.8, 1.6, 1.4, 'Oblicz\ngradienty\nGx, Gy', fill=GRAY4,
             fontsize=FS)
    ax.text(3.7, 1.55, 'kierunek + siła', ha='center', fontsize=FS_SMALL, style='italic')

    draw_arrow(ax, 4.6, 2.5, 5.2, 2.5, lw=1.5)
    ax.text(4.9, 2.75, '②', ha='center', fontsize=FS_LABEL, fontweight='bold')

    # Step 3: HOG histogram
    draw_box(ax, 5.3, 1.8, 1.6, 1.4, 'Histogramy\nkierunkowe\n9 binów/cel',
             fill=GRAY4, fontsize=FS)
    ax.text(6.1, 1.55, 'komórki 8×8 px', ha='center', fontsize=FS_SMALL, style='italic')

    draw_arrow(ax, 7.0, 2.5, 7.6, 2.5, lw=1.5)
    ax.text(7.3, 2.75, '③', ha='center', fontsize=FS_LABEL, fontweight='bold')

    # Step 4: SVM
    draw_box(ax, 7.7, 1.8, 1.4, 1.4, 'SVM\nklasyfikator\npieszy/tło',
             fill=GRAY3, fontsize=FS, fontweight='bold')

    draw_arrow(ax, 9.2, 2.5, 9.7, 2.5, lw=1.5)
    ax.text(9.45, 2.75, '④', ha='center', fontsize=FS_LABEL, fontweight='bold')

    # Step 5: NMS + output
    draw_box(ax, 9.3, 2.0, 1.0, 1.0, 'NMS\n→ wynik', fill=GRAY1, fontsize=FS)

    # Bottom: HOG feature vector illustration
    ax.text(5.0, 0.7, 'Wektor HOG: 3780 cech = 105 bloków × 4 komórki × 9 binów',
            ha='center', fontsize=FS, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    # Show small histogram bars
    bar_x = 3.2
    bar_y = 0.0
    angles = [0, 20, 40, 60, 80, 100, 120, 140, 160]
    values = [0.3, 0.1, 0.5, 0.8, 0.2, 0.6, 0.15, 0.4, 0.25]
    for i, (a, v) in enumerate(zip(angles, values)):
        ax.add_patch(mpatches.Rectangle((bar_x + i*0.18, bar_y), 0.15, v*0.6,
                     facecolor=GRAY3, edgecolor=LN, lw=0.5))
    ax.text(bar_x + 0.8, -0.2, '9 binów (0°–160°)', ha='center', fontsize=FS_SMALL)

    save_fig(fig, 'q24_hog_svm_pipeline.png')


# ============================================================
# 2. HOG Gradient Step-by-Step
# ============================================================
def draw_hog_gradient_steps():
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.5))
    fig.suptitle('HOG — kroki obliczania cech', fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # Step 1: Original patch
    ax = axes[0]
    patch = np.array([[50, 50, 200],
                      [50, 50, 200],
                      [50, 50, 200]])
    ax.imshow(patch, cmap='gray', vmin=0, vmax=255)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(patch[i, j]), ha='center', va='center',
                    fontsize=FS_LABEL, fontweight='bold',
                    color='white' if patch[i, j] > 127 else 'black')
    ax.set_title('① Fragment obrazu\n(jasność pikseli)', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Step 2: Gradient magnitude
    ax = axes[1]
    gx = np.array([[0, 150, 0],
                   [0, 150, 0],
                   [0, 150, 0]])
    ax.imshow(gx, cmap='gray', vmin=0, vmax=255)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(gx[i, j]), ha='center', va='center',
                    fontsize=FS_LABEL, fontweight='bold',
                    color='white' if gx[i, j] > 100 else 'black')
    ax.set_title('② Gradient Gx\n(krawędź pionowa!)', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Step 3: Cell histogram
    ax = axes[2]
    angles = ['0°', '20°', '40°', '60°', '80°', '100°', '120°', '140°', '160°']
    values = [150, 0, 0, 0, 0, 0, 0, 0, 0]
    bars = ax.bar(range(9), values, color=GRAY3, edgecolor=LN, linewidth=0.5)
    bars[0].set_facecolor(GRAY5)
    ax.set_xticks(range(9))
    ax.set_xticklabels(angles, fontsize=5, rotation=45)
    ax.set_title('③ Histogram komórki\n(bin 0° = krawędź pionowa)', fontsize=FS, fontweight='bold')
    ax.set_ylabel('siła', fontsize=FS_SMALL)

    # Step 4: Block normalization
    ax = axes[3]
    # 2x2 block of cells
    for i in range(2):
        for j in range(2):
            rect = mpatches.Rectangle((j*1.2, (1-i)*1.2), 1.0, 1.0,
                                       lw=1.2, edgecolor=LN, facecolor=GRAY4)
            ax.add_patch(rect)
            ax.text(j*1.2+0.5, (1-i)*1.2+0.5, f'hist\n{i*2+j+1}',
                    ha='center', va='center', fontsize=FS_SMALL)
    ax.add_patch(mpatches.Rectangle((-0.1, -0.1), 2.6, 2.6,
                                     lw=2, edgecolor=LN, facecolor='none',
                                     linestyle='--'))
    ax.text(1.2, -0.4, 'blok 2×2 → L2-norm', ha='center', fontsize=FS_SMALL,
            fontweight='bold')
    ax.set_xlim(-0.3, 2.8)
    ax.set_ylim(-0.7, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('④ Normalizacja bloków\n(odporność na oświetlenie)', fontsize=FS,
                 fontweight='bold')

    fig.tight_layout()
    save_fig(fig, 'q24_hog_gradient_steps.png')


# ============================================================
# 3. Viola-Jones Cascade
# ============================================================
def draw_viola_jones_cascade():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1.5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Viola-Jones — kaskada klasyfikatorów (SITO)', fontsize=FS_TITLE,
                 fontweight='bold', pad=12)

    # Input
    draw_box(ax, -0.3, 2.5, 1.5, 1.2, '500 000\nokien', fill=GRAY1, fontsize=FS,
             fontweight='bold')

    stages = [
        ('Etap 1\n2 cechy', '50%\nodrzucone', '250 000', GRAY4),
        ('Etap 2\n10 cech', '80%\nodrzucone', '50 000', GRAY4),
        ('Etap 3\n25 cech', '90%\nodrzucone', '5 000', GRAY4),
        ('Etap 25\n200 cech', '99%\nodrzucone', '50', GRAY3),
    ]

    x_pos = 1.6
    for i, (label, reject, remain, col) in enumerate(stages):
        # Stage box
        draw_box(ax, x_pos, 2.5, 1.6, 1.2, label, fill=col, fontsize=FS,
                 fontweight='bold')

        # Arrow from previous
        draw_arrow(ax, x_pos - 0.3, 3.1, x_pos - 0.05, 3.1, lw=1.5)

        # Reject arrow down
        draw_arrow(ax, x_pos + 0.8, 2.45, x_pos + 0.8, 1.6, lw=1.2)
        ax.text(x_pos + 0.8, 1.3, reject, ha='center', fontsize=FS_SMALL,
                color='black', style='italic')
        ax.text(x_pos + 0.8, 0.8, '✗ NIE-TWARZ', ha='center', fontsize=FS_SMALL,
                fontweight='bold')

        # Remaining count above
        if i < len(stages) - 1:
            ax.text(x_pos + 2.0, 3.9, f'→ {remain}', ha='center', fontsize=FS_SMALL,
                    style='italic')

        # Dots between stage 3 and stage 25
        if i == 2:
            ax.text(x_pos + 2.0, 3.1, '· · ·', ha='center', fontsize=12,
                    fontweight='bold')
            x_pos += 2.5
        else:
            x_pos += 2.1

    # Final output
    draw_arrow(ax, x_pos + 0.3, 3.1, x_pos + 0.9, 3.1, lw=1.5)
    draw_box(ax, x_pos + 0.5, 2.5, 1.3, 1.2, '~50\nTWARZE\n✓', fill=GRAY2,
             fontsize=FS, fontweight='bold')

    # Timing info
    ax.text(5.0, -0.5, 'Czas: 99% okien odrzucone w etapach 1-3 (~5 μs każde)\n'
            'Tylko 0.01% dochodzi do etapu 25 → cały obraz w ~30 ms = 30+ fps',
            ha='center', fontsize=FS, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=GRAY4, edgecolor=GRAY3))

    save_fig(fig, 'q24_viola_jones_cascade.png')


# ============================================================
# 4. Haar Features
# ============================================================
def draw_haar_features():
    fig, axes = plt.subplots(1, 4, figsize=(11, 3))
    fig.suptitle('Cechy Haar — typy i zastosowanie na twarzy', fontsize=FS_TITLE,
                 fontweight='bold', y=1.02)

    # Feature 1: Vertical edge
    ax = axes[0]
    ax.add_patch(mpatches.Rectangle((0, 0), 1, 2, facecolor=GRAY4, edgecolor=LN, lw=1.5))
    ax.add_patch(mpatches.Rectangle((1, 0), 1, 2, facecolor=GRAY3, edgecolor=LN, lw=1.5))
    ax.text(0.5, 1, '+Σ₁', ha='center', va='center', fontsize=FS_LABEL, fontweight='bold')
    ax.text(1.5, 1, '−Σ₂', ha='center', va='center', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xlim(-0.2, 2.2)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Krawędź pionowa\nwartość = Σ₁ − Σ₂', fontsize=FS)

    # Feature 2: Horizontal edge
    ax = axes[1]
    ax.add_patch(mpatches.Rectangle((0, 1), 2, 1, facecolor=GRAY4, edgecolor=LN, lw=1.5))
    ax.add_patch(mpatches.Rectangle((0, 0), 2, 1, facecolor=GRAY3, edgecolor=LN, lw=1.5))
    ax.text(1, 1.5, '+Σ₁', ha='center', va='center', fontsize=FS_LABEL, fontweight='bold')
    ax.text(1, 0.5, '−Σ₂', ha='center', va='center', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xlim(-0.2, 2.2)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Krawędź pozioma\n(oczy vs czoło)', fontsize=FS)

    # Feature 3: Three-rectangle (line)
    ax = axes[2]
    ax.add_patch(mpatches.Rectangle((0, 0), 0.7, 2, facecolor=GRAY3, edgecolor=LN, lw=1.5))
    ax.add_patch(mpatches.Rectangle((0.7, 0), 0.7, 2, facecolor=GRAY4, edgecolor=LN, lw=1.5))
    ax.add_patch(mpatches.Rectangle((1.4, 0), 0.7, 2, facecolor=GRAY3, edgecolor=LN, lw=1.5))
    ax.text(0.35, 1, '−Σ₁', ha='center', va='center', fontsize=FS_SMALL, fontweight='bold')
    ax.text(1.05, 1, '+Σ₂', ha='center', va='center', fontsize=FS_SMALL, fontweight='bold')
    ax.text(1.75, 1, '−Σ₃', ha='center', va='center', fontsize=FS_SMALL, fontweight='bold')
    ax.set_xlim(-0.2, 2.3)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Linia (3 prostokąty)\n(nos vs policzki)', fontsize=FS)

    # Feature 4: Application on face (schematic)
    ax = axes[3]
    # Draw face outline (oval)
    face = mpatches.Ellipse((1.2, 1.2), 2.0, 2.4, facecolor=GRAY4,
                             edgecolor=LN, lw=1.5)
    ax.add_patch(face)
    # Eyes (dark)
    ax.add_patch(mpatches.Ellipse((0.7, 1.6), 0.4, 0.2, facecolor=GRAY3,
                                   edgecolor=LN, lw=1))
    ax.add_patch(mpatches.Ellipse((1.7, 1.6), 0.4, 0.2, facecolor=GRAY3,
                                   edgecolor=LN, lw=1))
    # Nose (light)
    ax.plot([1.2, 1.1, 1.3], [1.3, 0.9, 0.9], color=LN, lw=1)
    # Mouth
    ax.plot([0.8, 1.0, 1.2, 1.4, 1.6], [0.55, 0.5, 0.55, 0.5, 0.55],
            color=LN, lw=1)
    # Haar feature overlay on eyes
    ax.add_patch(mpatches.Rectangle((0.3, 1.4), 1.8, 0.4, facecolor='none',
                                     edgecolor=LN, lw=2, linestyle='--'))
    ax.annotate('cechy Haar\n(oczy ciemne\nvs czoło jasne)', xy=(1.2, 1.85),
                xytext=(2.2, 2.3), fontsize=FS_SMALL, ha='center',
                arrowprops=dict(arrowstyle='->', color=LN, lw=1))
    ax.set_xlim(-0.2, 3.0)
    ax.set_ylim(-0.2, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Zastosowanie na twarzy', fontsize=FS)

    fig.tight_layout()
    save_fig(fig, 'q24_haar_features.png')


# ============================================================
# 5. Integral Image
# ============================================================
def draw_integral_image():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
    fig.suptitle('Integral Image — suma prostokąta w O(1)', fontsize=FS_TITLE,
                 fontweight='bold', y=1.02)

    # Original image
    ax = axes[0]
    data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    ax.imshow(data, cmap='gray', vmin=0, vmax=10)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(data[i, j]), ha='center', va='center',
                    fontsize=12, fontweight='bold', color='white' if data[i,j] > 5 else 'black')
    ax.set_title('① Obraz oryginalny', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Integral image
    ax = axes[1]
    ii = np.array([[1, 3, 6], [5, 12, 21], [12, 27, 45]])
    ax.imshow(ii, cmap='gray', vmin=0, vmax=50)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(ii[i, j]), ha='center', va='center',
                    fontsize=12, fontweight='bold',
                    color='white' if ii[i,j] > 25 else 'black')
    ax.set_title('② Integral Image\n(sumy kumulatywne)', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Formula illustration
    ax = axes[2]
    ax.axis('off')
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    # Draw rectangle
    ax.add_patch(mpatches.Rectangle((0.5, 0.5), 3, 3, facecolor='white',
                                     edgecolor=LN, lw=1))
    ax.add_patch(mpatches.Rectangle((1.5, 0.5), 2, 2, facecolor=GRAY3,
                                     edgecolor=LN, lw=2))
    # Labels
    ax.text(0.3, 3.7, 'A', fontsize=12, fontweight='bold')
    ax.text(3.6, 3.7, 'B', fontsize=12, fontweight='bold')
    ax.text(0.3, 0.3, 'C', fontsize=12, fontweight='bold')
    ax.text(3.6, 0.3, 'D', fontsize=12, fontweight='bold')
    ax.text(2.5, 1.5, 'SZUKANA\nSUMA', ha='center', va='center',
            fontsize=FS, fontweight='bold')
    ax.text(2.0, -0.3, 'Suma = D − B − C + A\n= 4 odczyty → O(1) ZAWSZE!',
            ha='center', fontsize=FS, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))
    ax.set_title('③ Formuła: 4 odczyty\n= O(1) niezależnie od rozmiaru', fontsize=FS,
                 fontweight='bold')

    fig.tight_layout()
    save_fig(fig, 'q24_integral_image.png')


# ============================================================
# 6. R-CNN Evolution
# ============================================================
def draw_rcnn_evolution():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Ewolucja R-CNN: od 50s do 0.2s na obraz', fontsize=FS_TITLE,
                 fontweight='bold', pad=12)

    y_positions = [5.5, 3.0, 0.5]
    labels = ['R-CNN (2014) — 50 s/obraz', 'Fast R-CNN (2015) — 2 s/obraz',
              'Faster R-CNN (2015) — 0.2 s/obraz']

    # R-CNN
    y = y_positions[0]
    ax.text(0, y + 1.3, labels[0], fontsize=FS_LABEL, fontweight='bold')
    draw_box(ax, 0, y, 2, 0.9, 'Selective\nSearch', fill=GRAY2, fontsize=FS)
    draw_arrow(ax, 2.1, y+0.45, 2.5, y+0.45)
    ax.text(2.3, y+0.8, '~2000', ha='center', fontsize=FS_SMALL, style='italic')
    draw_box(ax, 2.6, y, 1.5, 0.9, 'Resize\n224×224', fill=GRAY4, fontsize=FS)
    draw_arrow(ax, 4.2, y+0.45, 4.6, y+0.45)
    draw_box(ax, 4.7, y, 1.5, 0.9, 'CNN\n×2000!', fill=GRAY3, fontsize=FS, fontweight='bold')
    draw_arrow(ax, 6.3, y+0.45, 6.7, y+0.45)
    draw_box(ax, 6.8, y, 1.3, 0.9, 'SVM\nklasyf.', fill=GRAY4, fontsize=FS)
    draw_arrow(ax, 8.2, y+0.45, 8.6, y+0.45)
    draw_box(ax, 8.7, y, 1.0, 0.9, 'NMS', fill=GRAY1, fontsize=FS)
    # Problem annotation
    ax.text(5.5, y - 0.4, '⚠ CNN uruchamiane 2000× → 50 sek!',
            ha='center', fontsize=FS_SMALL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    # Fast R-CNN
    y = y_positions[1]
    ax.text(0, y + 1.3, labels[1], fontsize=FS_LABEL, fontweight='bold')
    draw_box(ax, 0, y, 2, 0.9, 'Selective\nSearch', fill=GRAY2, fontsize=FS)
    draw_arrow(ax, 2.1, y+0.45, 2.5, y+0.45)
    draw_box(ax, 2.6, y, 1.5, 0.9, 'CNN\n×1 (RAZ!)', fill=GRAY3, fontsize=FS,
             fontweight='bold')
    draw_arrow(ax, 4.2, y+0.45, 4.6, y+0.45)
    draw_box(ax, 4.7, y, 1.5, 0.9, 'ROI\nPooling', fill=GRAY1, fontsize=FS,
             fontweight='bold')
    draw_arrow(ax, 6.3, y+0.45, 6.7, y+0.45)
    draw_box(ax, 6.8, y, 1.3, 0.9, 'FC\nklasa+bbox', fill=GRAY4, fontsize=FS)
    draw_arrow(ax, 8.2, y+0.45, 8.6, y+0.45)
    draw_box(ax, 8.7, y, 1.0, 0.9, 'NMS', fill=GRAY1, fontsize=FS)
    ax.text(3.8, y - 0.4, '✓ CNN RAZ na cały obraz → 25× szybciej',
            ha='center', fontsize=FS_SMALL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    # Faster R-CNN
    y = y_positions[2]
    ax.text(0, y + 1.3, labels[2], fontsize=FS_LABEL, fontweight='bold')
    draw_box(ax, 0.5, y, 1.5, 0.9, 'CNN\nBackbone', fill=GRAY3, fontsize=FS,
             fontweight='bold')
    draw_arrow(ax, 2.1, y+0.45, 2.5, y+0.45)
    draw_box(ax, 2.6, y, 1.5, 0.9, 'Feature\nMap', fill=GRAY1, fontsize=FS)
    draw_arrow(ax, 4.2, y+0.45, 4.6, y+0.45)
    draw_box(ax, 4.7, y, 1.3, 0.9, 'RPN\n(w sieci!)', fill=GRAY2, fontsize=FS,
             fontweight='bold')
    draw_arrow(ax, 6.1, y+0.45, 6.5, y+0.45)
    draw_box(ax, 6.6, y, 1.3, 0.9, 'ROI\nPooling', fill=GRAY1, fontsize=FS)
    draw_arrow(ax, 8.0, y+0.45, 8.4, y+0.45)
    draw_box(ax, 8.5, y, 1.3, 0.9, 'FC\nklasa+bbox', fill=GRAY4, fontsize=FS)
    ax.text(5.0, y - 0.4, '✓ RPN zastępuje Selective Search → end-to-end',
            ha='center', fontsize=FS_SMALL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    save_fig(fig, 'q24_rcnn_evolution.png')


# ============================================================
# 7. YOLO Grid
# ============================================================
def draw_yolo_grid():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle('YOLO — detekcja jednoetapowa (siatka S×S)', fontsize=FS_TITLE,
                 fontweight='bold', y=1.02)

    # Grid on image
    ax = axes[0]
    S = 7
    ax.set_xlim(0, S)
    ax.set_ylim(0, S)
    for i in range(S + 1):
        ax.axhline(y=i, color=LN, lw=0.5, alpha=0.5)
        ax.axvline(x=i, color=LN, lw=0.5, alpha=0.5)
    ax.add_patch(mpatches.Rectangle((0, 0), S, S, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    # Highlight one cell
    ax.add_patch(mpatches.Rectangle((3, 3), 1, 1, facecolor=GRAY2,
                                     edgecolor=LN, lw=2))
    # Object center dot
    ax.plot(3.5, 3.5, 'ko', markersize=8)
    # Bounding box from that cell
    ax.add_patch(mpatches.Rectangle((2.0, 2.2), 3.0, 2.6, facecolor='none',
                                     edgecolor=LN, lw=2, linestyle='--'))
    ax.text(3.5, 1.8, 'bbox z komórki (3,3)', ha='center', fontsize=FS_SMALL,
            fontweight='bold')
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_title('① Siatka 7×7\nna obrazie', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Cell prediction
    ax = axes[1]
    ax.axis('off')
    ax.set_xlim(0, 6)
    ax.set_ylim(-1, 5)

    # Draw prediction vector
    labels = ['x', 'y', 'w', 'h', 'conf', 'x', 'y', 'w', 'h', 'conf',
              'P(c₁)', '...', 'P(c₂₀)']
    colors_vec = [GRAY4]*5 + [GRAY2]*5 + [GRAY1]*3

    bw = 0.42
    for i, (l, c) in enumerate(zip(labels, colors_vec)):
        x_pos = 0.3 + i * bw
        ax.add_patch(mpatches.Rectangle((x_pos, 2.5), bw-0.02, 0.6,
                                         facecolor=c, edgecolor=LN, lw=0.8))
        ax.text(x_pos + bw/2, 2.8, l, ha='center', va='center',
                fontsize=5, fontweight='bold')

    # Brackets for grouping
    ax.annotate('', xy=(0.3, 2.4), xytext=(2.4, 2.4),
                arrowprops=dict(arrowstyle='-', lw=1))
    ax.text(1.35, 2.15, 'bbox 1 (5 wartości)', ha='center', fontsize=FS_SMALL)

    ax.annotate('', xy=(2.4, 2.4), xytext=(4.5, 2.4),
                arrowprops=dict(arrowstyle='-', lw=1))
    ax.text(3.45, 2.15, 'bbox 2 (5 wartości)', ha='center', fontsize=FS_SMALL)

    ax.annotate('', xy=(4.5, 2.4), xytext=(5.8, 2.4),
                arrowprops=dict(arrowstyle='-', lw=1))
    ax.text(5.15, 2.15, '20 klas', ha='center', fontsize=FS_SMALL)

    ax.text(3.0, 3.5, 'Każda komórka → 30 wartości\n= 2×(x,y,w,h,conf) + 20 klas',
            ha='center', fontsize=FS, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    ax.set_title('② Predykcja jednej komórki\n(S=7, B=2, C=20)', fontsize=FS,
                 fontweight='bold')

    # Speed comparison
    ax = axes[2]
    ax.axis('off')
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)

    methods = ['R-CNN', 'Fast R-CNN', 'Faster R-CNN', 'YOLO', 'YOLOv8']
    fps_vals = [0.02, 0.5, 5, 45, 100]
    bar_colors = [GRAY3, GRAY3, GRAY3, GRAY2, GRAY1]

    for i, (m, f, c) in enumerate(zip(methods, fps_vals, bar_colors)):
        bar_w = f / 100 * 4.0
        y_pos = 4.0 - i * 0.8
        ax.add_patch(mpatches.Rectangle((0.5, y_pos), max(bar_w, 0.1), 0.5,
                     facecolor=c, edgecolor=LN, lw=0.8))
        ax.text(0.4, y_pos + 0.25, m, ha='right', va='center', fontsize=FS,
                fontweight='bold')
        ax.text(max(0.7, 0.5 + bar_w + 0.1), y_pos + 0.25, f'{f} fps',
                ha='left', va='center', fontsize=FS)

    ax.set_title('③ Porównanie szybkości\n(fps = klatki/sek)', fontsize=FS,
                 fontweight='bold')

    fig.tight_layout()
    save_fig(fig, 'q24_yolo_grid.png')


# ============================================================
# 8. IoU Diagram
# ============================================================
def draw_iou_diagram():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
    fig.suptitle('IoU (Intersection over Union) — miara nakładania bboxów',
                 fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # Low IoU
    ax = axes[0]
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 3, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5, label='A'))
    ax.add_patch(mpatches.Rectangle((2.5, 2.5), 3, 3, facecolor=GRAY2,
                                     edgecolor=LN, lw=1.5, alpha=0.7, label='B'))
    # Intersection
    ax.add_patch(mpatches.Rectangle((2.5, 2.5), 0.5, 0.5, facecolor=GRAY3,
                                     edgecolor=LN, lw=2))
    ax.text(1.5, 1.5, 'A', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(4, 4, 'B', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.5, 6)
    ax.set_ylim(-0.5, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('IoU ≈ 0.04\n(prawie się nie nakładają)', fontsize=FS, fontweight='bold')

    # Medium IoU
    ax = axes[1]
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 3, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    ax.add_patch(mpatches.Rectangle((1.5, 1.5), 3, 3, facecolor=GRAY2,
                                     edgecolor=LN, lw=1.5, alpha=0.7))
    ax.add_patch(mpatches.Rectangle((1.5, 1.5), 1.5, 1.5, facecolor=GRAY3,
                                     edgecolor=LN, lw=2))
    ax.text(0.7, 0.7, 'A', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(3.5, 3.5, 'B', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(2.25, 2.25, '∩', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('IoU ≈ 0.14\n(częściowe nakładanie)', fontsize=FS, fontweight='bold')

    # High IoU
    ax = axes[2]
    ax.add_patch(mpatches.Rectangle((0, 0), 3, 3, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    ax.add_patch(mpatches.Rectangle((0.3, 0.3), 3, 3, facecolor=GRAY2,
                                     edgecolor=LN, lw=1.5, alpha=0.7))
    ax.add_patch(mpatches.Rectangle((0.3, 0.3), 2.7, 2.7, facecolor=GRAY3,
                                     edgecolor=LN, lw=2))
    ax.text(-0.3, -0.3, 'A', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(3.5, 3.5, 'B', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(1.65, 1.65, '∩', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.set_xlim(-0.8, 4)
    ax.set_ylim(-0.8, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('IoU ≈ 0.74\n(duże nakładanie → duplikat!)', fontsize=FS, fontweight='bold')

    fig.tight_layout()
    save_fig(fig, 'q24_iou_diagram.png')


# ============================================================
# 9. NMS Step-by-Step
# ============================================================
def draw_nms_steps():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle('NMS (Non-Maximum Suppression) — usuwanie duplikatów',
                 fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # Before NMS
    ax = axes[0]
    ax.add_patch(mpatches.Rectangle((0, 0), 6, 5, facecolor=GRAY4,
                                     edgecolor=LN, lw=1))
    # Multiple overlapping boxes for same object
    ax.add_patch(mpatches.Rectangle((1, 1), 2.5, 3, facecolor='none',
                                     edgecolor=LN, lw=2))
    ax.text(2.25, 4.2, 'conf=0.95', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.add_patch(mpatches.Rectangle((1.2, 1.3), 2.3, 2.8, facecolor='none',
                                     edgecolor=LN, lw=1.5, linestyle='--'))
    ax.text(2.35, 1.1, 'conf=0.90', ha='center', fontsize=FS_SMALL)
    ax.add_patch(mpatches.Rectangle((0.8, 0.8), 2.7, 3.2, facecolor='none',
                                     edgecolor=LN, lw=1, linestyle=':'))
    ax.text(2.15, 0.6, 'conf=0.85', ha='center', fontsize=FS_SMALL)
    # Different object
    ax.add_patch(mpatches.Rectangle((4, 2), 1.5, 1.5, facecolor='none',
                                     edgecolor=LN, lw=1.5))
    ax.text(4.75, 3.7, 'conf=0.80', ha='center', fontsize=FS_SMALL)
    ax.text(2, 0.2, '⚠ 4 detekcje (3 duplikaty!)', ha='center', fontsize=FS_SMALL,
            fontweight='bold')
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.3, 5.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('① Przed NMS\n(wiele nakładających się)', fontsize=FS, fontweight='bold')

    # NMS process
    ax = axes[1]
    ax.axis('off')
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5)

    steps = [
        ('1. Sortuj: [0.95, 0.90, 0.85, 0.80]', 4.5),
        ('2. Weź najlepszą (0.95) → ZACHOWAJ', 3.7),
        ('3. IoU(0.95, 0.90)=0.82 > 0.5 → USUŃ', 2.9),
        ('4. IoU(0.95, 0.85)=0.75 > 0.5 → USUŃ', 2.1),
        ('5. IoU(0.95, 0.80)=0.10 < 0.5 → ZACHOWAJ', 1.3),
    ]
    colors = [GRAY4, GRAY2, GRAY4, GRAY4, GRAY2]
    for (text, yp), c in zip(steps, colors):
        ax.text(3.0, yp, text, ha='center', fontsize=FS,
                bbox=dict(boxstyle='round,pad=0.2', facecolor=c, edgecolor=GRAY3))

    ax.set_title('② Algorytm NMS\n(próg IoU = 0.5)', fontsize=FS, fontweight='bold')

    # After NMS
    ax = axes[2]
    ax.add_patch(mpatches.Rectangle((0, 0), 6, 5, facecolor=GRAY4,
                                     edgecolor=LN, lw=1))
    # Only best box for each object
    ax.add_patch(mpatches.Rectangle((1, 1), 2.5, 3, facecolor='none',
                                     edgecolor=LN, lw=2.5))
    ax.text(2.25, 4.2, 'conf=0.95 ✓', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.add_patch(mpatches.Rectangle((4, 2), 1.5, 1.5, facecolor='none',
                                     edgecolor=LN, lw=2.5))
    ax.text(4.75, 3.7, 'conf=0.80 ✓', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.text(3, 0.2, '✓ 2 unikalne obiekty', ha='center', fontsize=FS_SMALL,
            fontweight='bold')
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.3, 5.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('③ Po NMS\n(1 bbox na obiekt)', fontsize=FS, fontweight='bold')

    fig.tight_layout()
    save_fig(fig, 'q24_nms_steps.png')


# ============================================================
# 10. Detector from Classifier — 3 approaches
# ============================================================
def draw_detector_from_classifier():
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-1, 9.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Jak zbudować detektor z klasyfikatora? — 3 podejścia',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # ---- Approach 1: Sliding Window ----
    y = 7.0
    ax.text(0, y + 1.5, '① Sliding Window (NAJWOLNIEJSZE)', fontsize=FS_LABEL,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    # Image with sliding window
    ax.add_patch(mpatches.Rectangle((0, y - 0.6), 1.8, 1.8, facecolor=GRAY1,
                                     edgecolor=LN, lw=1.5))
    ax.text(0.9, y + 0.3, 'obraz', ha='center', fontsize=FS_SMALL)
    # Sliding windows
    for dx, dy in [(0.1, 0.1), (0.4, 0.1), (0.7, 0.1), (0.1, 0.5), (0.4, 0.5)]:
        ax.add_patch(mpatches.Rectangle((dx, y - 0.5 + dy), 0.5, 0.5,
                     facecolor='none', edgecolor=LN, lw=0.8, linestyle='--'))

    draw_arrow(ax, 2.0, y + 0.3, 2.7, y + 0.3, lw=1.2)
    ax.text(2.35, y + 0.6, '×miliony', fontsize=FS_SMALL, style='italic')

    draw_box(ax, 2.8, y - 0.3, 1.8, 1.2, 'Klasyfikator\n(ResNet)\n"kot? pies? tło?"',
             fill=GRAY4, fontsize=FS)
    draw_arrow(ax, 4.7, y + 0.3, 5.3, y + 0.3, lw=1.2)
    draw_box(ax, 5.4, y - 0.3, 1.2, 1.2, 'NMS', fill=GRAY1, fontsize=FS)
    draw_arrow(ax, 6.7, y + 0.3, 7.3, y + 0.3, lw=1.2)
    ax.text(8.5, y + 0.3, '~3.3h / obraz!\n⚠ NIEPRAKTYCZNE',
            ha='center', fontsize=FS, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    # ---- Approach 2: Region Proposals ----
    y = 3.8
    ax.text(0, y + 1.5, '② Region Proposals + Klasyfikator (= R-CNN)', fontsize=FS_LABEL,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    ax.add_patch(mpatches.Rectangle((0, y - 0.6), 1.8, 1.8, facecolor=GRAY1,
                                     edgecolor=LN, lw=1.5))
    ax.text(0.9, y + 0.3, 'obraz', ha='center', fontsize=FS_SMALL)
    # A few smart regions
    ax.add_patch(mpatches.Rectangle((0.1, y - 0.4), 0.7, 0.9, facecolor='none',
                                     edgecolor=LN, lw=1.5))
    ax.add_patch(mpatches.Rectangle((0.9, y + 0.0), 0.7, 0.6, facecolor='none',
                                     edgecolor=LN, lw=1.5))

    draw_arrow(ax, 2.0, y + 0.3, 2.7, y + 0.3, lw=1.2)
    draw_box(ax, 2.8, y - 0.3, 1.6, 1.2, 'Selective\nSearch\n~2000 regionów',
             fill=GRAY2, fontsize=FS)
    draw_arrow(ax, 4.5, y + 0.3, 5.1, y + 0.3, lw=1.2)
    ax.text(4.8, y + 0.6, '×2000', fontsize=FS_SMALL, style='italic')
    draw_box(ax, 5.2, y - 0.3, 1.5, 1.2, 'Klasyfikator\n(CNN)', fill=GRAY4, fontsize=FS)
    draw_arrow(ax, 6.8, y + 0.3, 7.4, y + 0.3, lw=1.2)
    draw_box(ax, 7.5, y - 0.3, 1.0, 1.2, 'NMS', fill=GRAY1, fontsize=FS)
    draw_arrow(ax, 8.6, y + 0.3, 9.0, y + 0.3, lw=1.2)
    ax.text(10.0, y + 0.3, '~20-50 s/obraz\n(250× szybciej)',
            ha='center', fontsize=FS, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    # ---- Approach 3: Fine-tune backbone ----
    y = 0.5
    ax.text(0, y + 1.5, '③ Fine-tune backbone + detection head (NAJLEPSZE)',
            fontsize=FS_LABEL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY2, edgecolor=GRAY3))

    ax.add_patch(mpatches.Rectangle((0, y - 0.6), 1.8, 1.8, facecolor=GRAY1,
                                     edgecolor=LN, lw=1.5))
    ax.text(0.9, y + 0.3, 'obraz', ha='center', fontsize=FS_SMALL)

    draw_arrow(ax, 2.0, y + 0.3, 2.7, y + 0.3, lw=1.2)
    draw_box(ax, 2.8, y - 0.3, 1.8, 1.2, 'Pretrained\nbackbone\n(ResNet)',
             fill=GRAY3, fontsize=FS, fontweight='bold')
    draw_arrow(ax, 4.7, y + 0.3, 5.3, y + 0.3, lw=1.2)

    # Two heads from feature map
    draw_box(ax, 5.4, y + 0.3, 1.6, 0.6, 'cls head\nP(klasa)', fill=GRAY4, fontsize=FS)
    draw_box(ax, 5.4, y - 0.5, 1.6, 0.6, 'bbox head\nΔx,Δy,Δw,Δh', fill=GRAY4, fontsize=FS)

    draw_arrow(ax, 7.1, y + 0.6, 7.7, y + 0.6, lw=1.0)
    draw_arrow(ax, 7.1, y - 0.2, 7.7, y - 0.2, lw=1.0)
    draw_box(ax, 7.8, y - 0.3, 1.0, 1.2, 'NMS', fill=GRAY1, fontsize=FS)

    draw_arrow(ax, 8.9, y + 0.3, 9.3, y + 0.3, lw=1.2)
    ax.text(10.2, y + 0.3, '5-155 fps!\n✓ NAJLEPSZE',
            ha='center', fontsize=FS, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY2, edgecolor=GRAY3))

    save_fig(fig, 'q24_detector_from_classifier.png')


# ============================================================
# 11. SVM Hyperplane
# ============================================================
def draw_svm_hyperplane():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_title('SVM — hiperpłaszczyzna i margines', fontsize=FS_TITLE,
                 fontweight='bold', pad=12)

    np.random.seed(42)
    # Class +1 (top-right)
    x_pos = np.random.randn(15) * 0.5 + 3
    y_pos = np.random.randn(15) * 0.5 + 3
    ax.scatter(x_pos, y_pos, marker='o', s=50, facecolors='white',
               edgecolors=LN, linewidths=1.5, label='klasa +1 (pieszy)', zorder=3)

    # Class -1 (bottom-left)
    x_neg = np.random.randn(15) * 0.5 + 1
    y_neg = np.random.randn(15) * 0.5 + 1
    ax.scatter(x_neg, y_neg, marker='x', s=50, c=LN, linewidths=1.5,
               label='klasa -1 (tło)', zorder=3)

    # Hyperplane (decision boundary)
    x_line = np.linspace(-0.5, 5, 100)
    y_line = -x_line + 4.0
    ax.plot(x_line, y_line, 'k-', lw=2, label='hiperpłaszczyzna')

    # Margin lines
    ax.plot(x_line, y_line + 0.7, 'k--', lw=1, alpha=0.5)
    ax.plot(x_line, y_line - 0.7, 'k--', lw=1, alpha=0.5)

    # Margin annotation
    ax.annotate('', xy=(2.5, 1.5 + 0.7), xytext=(2.5, 1.5 - 0.7),
                arrowprops=dict(arrowstyle='<->', color=LN, lw=1.5))
    ax.text(2.8, 1.5, 'margines\n(MAX!)', fontsize=FS, fontweight='bold')

    # Support vectors (highlight closest points)
    # Find points closest to the line
    ax.scatter([2.5], [2.2], marker='o', s=120, facecolors='none',
               edgecolors=LN, linewidths=2.5, zorder=4)
    ax.scatter([1.5], [1.8], marker='x', s=120, c=LN, linewidths=2.5, zorder=4)
    ax.annotate('support\nvectors', xy=(1.5, 1.8), xytext=(0.2, 3.0),
                fontsize=FS, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=LN, lw=1))

    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 5)
    ax.set_xlabel('cecha 1 (np. gradient pionowy)', fontsize=FS)
    ax.set_ylabel('cecha 2 (np. gradient poziomy)', fontsize=FS)
    ax.legend(fontsize=FS_SMALL, loc='lower right')
    ax.set_aspect('equal')

    save_fig(fig, 'q24_svm_hyperplane.png')


# ============================================================
# 12. Two-stage vs One-stage comparison table
# ============================================================
def draw_two_vs_one_stage():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Two-stage vs One-stage — porównanie', fontsize=FS_TITLE,
                 fontweight='bold', pad=8)

    headers = ['Cecha', 'Two-stage\n(Faster R-CNN)', 'One-stage\n(YOLO)']
    rows = [
        ['Szybkość', '~5 fps', '45-155 fps'],
        ['Dokładność (mAP)', 'wyższa (historycznie)', 'dorównuje (YOLOv8)'],
        ['Małe obiekty', 'lepszy', 'gorszy (SSD/FPN pomaga)'],
        ['Architektura', '2 etapy + NMS', '1 etap + NMS'],
        ['Real-time?', 'NIE', 'TAK'],
    ]
    col_widths = [2.5, 3.5, 3.5]
    draw_table(ax, headers, rows, 0.2, 3.8, col_widths, row_h=0.65,
               fontsize=FS, header_fontsize=FS)

    save_fig(fig, 'q24_two_vs_one_stage.png')


# ============================================================
# 13. ROI Pooling illustration
# ============================================================
def draw_roi_pooling():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle('ROI Pooling — dowolny rozmiar → stały rozmiar',
                 fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # Feature map with ROI
    ax = axes[0]
    # Draw feature map grid
    fm = np.random.randint(0, 10, (8, 8))
    ax.imshow(fm, cmap='gray', vmin=0, vmax=10, alpha=0.3)
    for i in range(9):
        ax.axhline(y=i-0.5, color=LN, lw=0.3)
        ax.axvline(x=i-0.5, color=LN, lw=0.3)
    # ROI rectangle
    ax.add_patch(mpatches.Rectangle((1.5, 1.5), 4, 4, facecolor='none',
                                     edgecolor=LN, lw=3, linestyle='-'))
    ax.text(3.5, 0.8, 'ROI', ha='center', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(7.5, -0.5)
    ax.set_title('① Feature map\nz zaznaczonym ROI', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # ROI divided into grid
    ax = axes[1]
    roi_data = np.array([
        [1, 3, 2, 1],
        [0, 5, 1, 6],
        [0, 4, 1, 0],
        [7, 2, 9, 1],
    ])
    ax.imshow(roi_data, cmap='gray', vmin=0, vmax=10)
    for i in range(5):
        ax.axhline(y=i-0.5, color=LN, lw=1)
        ax.axvline(x=i-0.5, color=LN, lw=1)
    # Grid lines for 2x2 pooling
    ax.axhline(y=0.5, color=LN, lw=3, linestyle='--')
    ax.axvline(x=0.5, color=LN, lw=3, linestyle='--')
    for i in range(4):
        for j in range(4):
            ax.text(j, i, str(roi_data[i, j]), ha='center', va='center',
                    fontsize=10, fontweight='bold',
                    color='white' if roi_data[i, j] > 5 else 'black')
    ax.set_title('② ROI podzielony\nna siatkę 2×2', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Output after pooling
    ax = axes[2]
    out = np.array([[5, 6], [7, 9]])
    ax.imshow(out, cmap='gray', vmin=0, vmax=10)
    for i in range(3):
        ax.axhline(y=i-0.5, color=LN, lw=1.5)
        ax.axvline(x=i-0.5, color=LN, lw=1.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(out[i, j]), ha='center', va='center',
                    fontsize=14, fontweight='bold',
                    color='white' if out[i, j] > 5 else 'black')
    ax.set_title('③ Po ROI Pool 2×2\n(max z każdej komórki)', fontsize=FS, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    fig.tight_layout()
    save_fig(fig, 'q24_roi_pooling.png')


# ============================================================
# 14. DETR Pipeline
# ============================================================
def draw_detr_pipeline():
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(-1, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('DETR — Transformer do detekcji (bez NMS, bez anchorów)',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Pipeline
    draw_box(ax, 0, 1.5, 1.5, 1.5, 'Obraz\nwejściowy', fill=GRAY1, fontsize=FS)
    draw_arrow(ax, 1.6, 2.25, 2.1, 2.25, lw=1.5)

    draw_box(ax, 2.2, 1.5, 1.5, 1.5, 'CNN\nBackbone\n(ResNet)', fill=GRAY3,
             fontsize=FS, fontweight='bold')
    draw_arrow(ax, 3.8, 2.25, 4.3, 2.25, lw=1.5)

    draw_box(ax, 4.4, 1.5, 1.8, 1.5, 'Transformer\nEncoder\n(self-attention)',
             fill=GRAY2, fontsize=FS)
    draw_arrow(ax, 6.3, 2.25, 6.8, 2.25, lw=1.5)

    draw_box(ax, 6.9, 1.5, 1.8, 1.5, 'Transformer\nDecoder\n(N=100 queries)',
             fill=GRAY2, fontsize=FS, fontweight='bold')

    # Output branches
    draw_arrow(ax, 8.8, 2.5, 9.5, 3.0, lw=1.2)
    draw_box(ax, 9.6, 2.7, 1.5, 0.7, 'klasa₁...klasa₁₀₀', fill=GRAY4, fontsize=FS_SMALL)

    draw_arrow(ax, 8.8, 2.0, 9.5, 1.5, lw=1.2)
    draw_box(ax, 9.6, 1.2, 1.5, 0.7, 'bbox₁...bbox₁₀₀', fill=GRAY4, fontsize=FS_SMALL)

    # Annotations
    ax.text(7.8, 0.5, '100 object queries → 5 obiektów + 95× "brak"',
            ha='center', fontsize=FS, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    ax.text(5.5, 0.0, 'Hungarian matching (trening): optymalne dopasowanie predykcji do GT',
            ha='center', fontsize=FS_SMALL, style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    # Big benefit box
    ax.text(5.5, 4.0, 'BEZ anchorów • BEZ NMS • end-to-end • prosty pipeline',
            ha='center', fontsize=FS, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY2, edgecolor=GRAY3))

    save_fig(fig, 'q24_detr_pipeline.png')


# ============================================================
# 15. Sliding Window illustration
# ============================================================
def draw_sliding_window():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle('Sliding Window — najprostsze podejście do detekcji',
                 fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # Multi-position
    ax = axes[0]
    ax.add_patch(mpatches.Rectangle((0, 0), 8, 6, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    # Grid of sliding windows
    for i in range(4):
        for j in range(3):
            ax.add_patch(mpatches.Rectangle((i*1.8 + 0.2, j*1.8 + 0.2), 1.5, 1.5,
                         facecolor='none', edgecolor=LN, lw=0.6, linestyle='--'))
    # Highlight current window
    ax.add_patch(mpatches.Rectangle((2.0, 2.0), 1.5, 1.5, facecolor='none',
                                     edgecolor=LN, lw=2.5))
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('① Wiele pozycji\n(krok co 8 px)', fontsize=FS, fontweight='bold')

    # Multi-scale
    ax = axes[1]
    ax.add_patch(mpatches.Rectangle((0, 0), 6, 5, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    sizes = [(0.8, 0.8), (1.5, 1.5), (2.5, 2.5), (3.5, 3.5)]
    for i, (w, h) in enumerate(sizes):
        ax.add_patch(mpatches.Rectangle((0.3 + i*0.3, 0.3 + i*0.3), w, h,
                     facecolor='none', edgecolor=LN, lw=1 + i*0.3,
                     linestyle=[':', '--', '-.', '-'][i]))
    ax.text(3, 0, '4+ skal', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('② Wiele skal\n(obiekty mają różne rozmiary)', fontsize=FS,
                 fontweight='bold')

    # Count
    ax = axes[2]
    ax.axis('off')
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5)

    lines = [
        ('Obraz: 640 × 480 px', 4.5),
        ('Okno: 64 × 64 px, krok 8 px', 3.8),
        ('Pozycje: ~72 × 52 = 3 744', 3.1),
        ('× 5 skal = 18 720 okien', 2.4),
        ('× klasyfikacja = WOLNE!', 1.7),
        ('→ ~3h na jeden obraz', 0.8),
    ]
    for text, yp in lines:
        fw = 'bold' if '~3h' in text or 'WOLNE' in text else 'normal'
        col = GRAY2 if 'WOLNE' in text or '~3h' in text else GRAY4
        ax.text(3.0, yp, text, ha='center', fontsize=FS,
                fontweight=fw,
                bbox=dict(boxstyle='round,pad=0.2', facecolor=col, edgecolor=GRAY3))

    ax.set_title('③ Dlaczego wolne?\n(miliony klasyfikacji)', fontsize=FS, fontweight='bold')

    fig.tight_layout()
    save_fig(fig, 'q24_sliding_window.png')


# ============================================================
# 16. FPN (Feature Pyramid Network)
# ============================================================
def draw_fpn():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('FPN (Feature Pyramid Network) — detekcja obiektów wszystkich rozmiarów',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Bottom-up (backbone)
    levels = [
        (0, 0, 2.0, 2.0, 'C2\n56×56', 'duże\ndetale'),
        (0, 2.2, 1.5, 1.5, 'C3\n28×28', ''),
        (0, 3.9, 1.0, 1.0, 'C4\n14×14', ''),
        (0, 5.1, 0.6, 0.6, 'C5\n7×7', 'kontekst'),
    ]

    for x, y, w, h, label, note in levels:
        ax.add_patch(mpatches.Rectangle((x, y - h), w, h, facecolor=GRAY4,
                                         edgecolor=LN, lw=1.5))
        ax.text(x + w/2, y - h/2, label, ha='center', va='center',
                fontsize=FS_SMALL, fontweight='bold')
        if note:
            ax.text(x + w + 0.15, y - h/2, note, ha='left', va='center',
                    fontsize=5, style='italic')

    ax.text(1.0, -0.3, 'Bottom-up\n(backbone)', ha='center', fontsize=FS,
            fontweight='bold')

    # Top-down + lateral
    td_levels = [
        (4.5, 5.1, 0.6, 0.6, 'P5'),
        (4.5, 3.9, 1.0, 1.0, 'P4'),
        (4.5, 2.2, 1.5, 1.5, 'P3'),
        (4.5, 0, 2.0, 2.0, 'P2'),
    ]

    for x, y, w, h, label in td_levels:
        ax.add_patch(mpatches.Rectangle((x, y - h + h), w, h, facecolor=GRAY2,
                                         edgecolor=LN, lw=1.5))
        ax.text(x + w/2, y - h/2 + h, label, ha='center', va='center',
                fontsize=FS_SMALL, fontweight='bold')

    # Lateral connections
    for (_, y1, w1, h1, _, _), (x2, y2, w2, h2, _) in zip(levels, td_levels):
        draw_arrow(ax, w1 + 0.2, y1 - h1/2, x2 - 0.1, y2 + h2/2, lw=1, style='->')

    # Top-down arrows
    for i in range(len(td_levels) - 1):
        x2, y2, w2, h2, _ = td_levels[i]
        x3, y3, w3, h3, _ = td_levels[i + 1]
        draw_arrow(ax, x2 + w2/2, y2, x3 + w3/2, y3 + h3 + 0.1, lw=1.2,
                   style='->', color=GRAY3)

    ax.text(5.5, -0.3, 'Top-down + lateral\n(FPN)', ha='center', fontsize=FS,
            fontweight='bold')

    # Detection outputs
    det_labels = ['małe obj.', 'średnie', 'duże', 'b. duże']
    for i, (x, y, w, h, label) in enumerate(td_levels):
        draw_arrow(ax, x + w + 0.1, y + h/2, 7.5, y + h/2, lw=0.8)
        ax.text(7.7, y + h/2, f'detekcja:\n{det_labels[3-i]}', fontsize=FS_SMALL,
                va='center')

    save_fig(fig, 'q24_fpn.png')


# ============================================================
# 17. Anchor boxes
# ============================================================
def draw_anchor_boxes():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_title('Anchor boxes — predefiniowane kształty', fontsize=FS_TITLE,
                 fontweight='bold', pad=12)

    ax.add_patch(mpatches.Rectangle((0, 0), 6, 5, facecolor=GRAY4,
                                     edgecolor=LN, lw=1))

    # Center point
    cx, cy = 3, 2.5
    ax.plot(cx, cy, 'ko', markersize=8, zorder=5)
    ax.text(cx + 0.15, cy + 0.15, '(x, y)', fontsize=FS, fontweight='bold')

    # 9 anchors: 3 sizes × 3 ratios
    anchors = [
        # (w, h, style, label)
        (0.8, 0.8, '-', '1:1 small'),
        (1.6, 1.6, '-', '1:1 medium'),
        (2.4, 2.4, '-', '1:1 large'),
        (0.6, 1.2, '--', '1:2 small'),
        (1.2, 2.4, '--', '1:2 medium'),
        (1.8, 3.6, '--', '1:2 large'),
        (1.2, 0.6, ':', '2:1 small'),
        (2.4, 1.2, ':', '2:1 medium'),
        (3.6, 1.8, ':', '2:1 large'),
    ]

    drawn = []
    for w, h, ls, label in anchors:
        rect = mpatches.Rectangle((cx - w/2, cy - h/2), w, h,
                                   facecolor='none', edgecolor=LN,
                                   lw=1.2, linestyle=ls)
        ax.add_patch(rect)

    # Legend-style labels
    ax.text(3, -0.5, '9 anchorów = 3 rozmiary × 3 proporcje (1:1, 1:2, 2:1)\n'
            'Sieć predykuje PRZESUNIĘCIE od najbliższego anchora',
            ha='center', fontsize=FS, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-1.2, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, 'q24_anchor_boxes.png')


# ============================================================
# 18. Detection task comparison
# ============================================================
def draw_detection_tasks():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle('Klasyfikacja vs Detekcja vs Segmentacja',
                 fontsize=FS_TITLE, fontweight='bold', y=1.02)

    # Classification
    ax = axes[0]
    ax.add_patch(mpatches.Rectangle((0, 0), 4, 4, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    # Simple cat silhouette
    ax.add_patch(mpatches.Ellipse((2, 2), 2, 1.5, facecolor=GRAY3,
                                   edgecolor=LN, lw=1))
    ax.add_patch(mpatches.Ellipse((2, 3), 1, 0.8, facecolor=GRAY3,
                                   edgecolor=LN, lw=1))
    # Ears
    ax.plot([1.6, 1.5, 1.8], [3.3, 3.8, 3.4], color=LN, lw=1.5)
    ax.plot([2.2, 2.5, 2.4], [3.3, 3.8, 3.4], color=LN, lw=1.5)
    ax.text(2, -0.4, '→ "KOT" (jedna etykieta)', ha='center',
            fontsize=FS, fontweight='bold')
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.8, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Klasyfikacja\n(co?)', fontsize=FS, fontweight='bold')

    # Detection
    ax = axes[1]
    ax.add_patch(mpatches.Rectangle((0, 0), 4, 4, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    # Cat
    ax.add_patch(mpatches.Ellipse((1.2, 2), 1.2, 1, facecolor=GRAY3,
                                   edgecolor=LN, lw=1))
    ax.add_patch(mpatches.Ellipse((1.2, 2.8), 0.7, 0.5, facecolor=GRAY3,
                                   edgecolor=LN, lw=1))
    # Dog
    ax.add_patch(mpatches.Ellipse((3, 1.5), 1.2, 1, facecolor=GRAY2,
                                   edgecolor=LN, lw=1))
    ax.add_patch(mpatches.Ellipse((3, 2.3), 0.7, 0.5, facecolor=GRAY2,
                                   edgecolor=LN, lw=1))
    # Bounding boxes
    ax.add_patch(mpatches.Rectangle((0.3, 1.2), 1.8, 2.2, facecolor='none',
                                     edgecolor=LN, lw=2.5))
    ax.text(1.2, 3.5, 'KOT', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.add_patch(mpatches.Rectangle((2.1, 0.8), 1.7, 2.0, facecolor='none',
                                     edgecolor=LN, lw=2.5))
    ax.text(3.0, 2.9, 'PIES', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.text(2, -0.4, '→ bbox + klasa (N obiektów)', ha='center',
            fontsize=FS, fontweight='bold')
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.8, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Detekcja\n(co? + gdzie?)', fontsize=FS, fontweight='bold')

    # Segmentation
    ax = axes[2]
    ax.add_patch(mpatches.Rectangle((0, 0), 4, 4, facecolor=GRAY4,
                                     edgecolor=LN, lw=1.5))
    # Cat mask (detailed)
    theta = np.linspace(0, 2*np.pi, 30)
    cat_x = 1.2 + 0.6*np.cos(theta) + 0.1*np.sin(3*theta)
    cat_y = 2 + 0.5*np.sin(theta) + 0.1*np.cos(2*theta)
    ax.fill(cat_x, cat_y, facecolor=GRAY3, edgecolor=LN, lw=1.5)
    # Dog mask
    dog_x = 3.0 + 0.6*np.cos(theta) + 0.05*np.sin(4*theta)
    dog_y = 1.5 + 0.5*np.sin(theta) + 0.08*np.cos(3*theta)
    ax.fill(dog_x, dog_y, facecolor=GRAY2, edgecolor=LN, lw=1.5)
    ax.text(1.2, 2, 'KOT', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.text(3.0, 1.5, 'PIES', ha='center', fontsize=FS_SMALL, fontweight='bold')
    ax.text(2, -0.4, '→ maska pikseli (per piksel)', ha='center',
            fontsize=FS, fontweight='bold')
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.8, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Segmentacja\n(dokładna maska)', fontsize=FS, fontweight='bold')

    fig.tight_layout()
    save_fig(fig, 'q24_detection_tasks.png')


# ============================================================
# 19. CNN Architecture overview
# ============================================================
def draw_cnn_architecture():
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-1, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('CNN — od obrazu do predykcji (architektura)', fontsize=FS_TITLE,
                 fontweight='bold', pad=12)

    # Input image
    draw_box(ax, 0, 0.5, 1.5, 3, 'Obraz\n224×224×3', fill=GRAY1, fontsize=FS)

    # Conv1
    draw_arrow(ax, 1.6, 2.0, 2.1, 2.0, lw=1.2)
    draw_box(ax, 2.2, 0.8, 1.2, 2.4, 'Conv1\n+ReLU\n55×55×96', fill=GRAY4, fontsize=FS_SMALL)

    # Pool1
    draw_arrow(ax, 3.5, 2.0, 3.9, 2.0, lw=1.2)
    draw_box(ax, 4.0, 1.0, 1.0, 2.0, 'Pool\n27×27\n×96', fill=GRAY2, fontsize=FS_SMALL)

    # Conv2
    draw_arrow(ax, 5.1, 2.0, 5.5, 2.0, lw=1.2)
    draw_box(ax, 5.6, 0.8, 1.2, 2.4, 'Conv2\n+ReLU\n27×27\n×256', fill=GRAY4, fontsize=FS_SMALL)

    # Pool2
    draw_arrow(ax, 6.9, 2.0, 7.3, 2.0, lw=1.2)
    draw_box(ax, 7.4, 1.2, 0.8, 1.6, 'Pool\n13×13\n×256', fill=GRAY2, fontsize=FS_SMALL)

    # More conv...
    draw_arrow(ax, 8.3, 2.0, 8.7, 2.0, lw=1.2)
    ax.text(9.0, 2.0, '...', fontsize=14, ha='center', va='center')
    draw_arrow(ax, 9.3, 2.0, 9.7, 2.0, lw=1.2)

    # FC
    draw_box(ax, 9.8, 1.2, 1.0, 1.6, 'FC\n4096', fill=GRAY3, fontsize=FS)

    draw_arrow(ax, 10.9, 2.0, 11.3, 2.0, lw=1.2)

    # Output
    draw_box(ax, 11.4, 1.5, 1.0, 1.0, 'Softmax\n1000 klas', fill=GRAY1, fontsize=FS_SMALL)

    # Annotations below
    ax.text(3.0, 0.0, 'rozmiar maleje\n224→55→27→13→6', ha='center', fontsize=FS_SMALL,
            style='italic')
    ax.text(6.0, 0.0, 'kanały rosną\n3→96→256→384', ha='center', fontsize=FS_SMALL,
            style='italic')
    ax.text(10.0, 0.0, 'decyzja\nkońcowa', ha='center', fontsize=FS_SMALL,
            style='italic')

    # hierarchy
    ax.text(6.0, 4.0, 'Hierarchia: krawędzie → rogi → fragmenty → obiekty (K-R-F-O)',
            ha='center', fontsize=FS, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    save_fig(fig, 'q24_cnn_architecture.png')


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Generating PYTANIE 24 diagrams...")
    draw_hog_svm_pipeline()
    draw_hog_gradient_steps()
    draw_viola_jones_cascade()
    draw_haar_features()
    draw_integral_image()
    draw_rcnn_evolution()
    draw_yolo_grid()
    draw_iou_diagram()
    draw_nms_steps()
    draw_detector_from_classifier()
    draw_svm_hyperplane()
    draw_two_vs_one_stage()
    draw_roi_pooling()
    draw_detr_pipeline()
    draw_sliding_window()
    draw_fpn()
    draw_anchor_boxes()
    draw_detection_tasks()
    draw_cnn_architecture()
    print("\nAll PYTANIE 24 diagrams generated!")
