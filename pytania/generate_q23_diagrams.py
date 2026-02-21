#!/usr/bin/env python3
"""
Generate all diagrams for PYTANIE 23: Segmentacja obrazu.

A4-compatible, monochrome-friendly (grays + one accent), 300 DPI.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import os

DPI = 300
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color palette — monochrome-friendly
BLACK = '#000000'
WHITE = '#FFFFFF'
GRAY1 = '#F5F5F5'
GRAY2 = '#E0E0E0'
GRAY3 = '#BDBDBD'
GRAY4 = '#9E9E9E'
GRAY5 = '#757575'
GRAY6 = '#424242'
ACCENT = '#4A90D9'   # single blue accent for highlights
ACCENT_LIGHT = '#B3D4FC'
RED_ACCENT = '#D32F2F'
GREEN_ACCENT = '#388E3C'

FS = 9
FS_TITLE = 11
FS_SMALL = 7
FS_TINY = 6


# ============================================================
# 1. OTSU — Bimodal histogram + within-class variance
# ============================================================
def generate_otsu_bimodal():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))

    # --- Panel 1: Bimodal histogram ---
    ax = axes[0]
    np.random.seed(42)
    dark = np.random.normal(60, 20, 3000).clip(0, 255)
    bright = np.random.normal(190, 25, 2000).clip(0, 255)
    all_pixels = np.concatenate([dark, bright])

    counts, bins, bars = ax.hist(all_pixels, bins=64, color=GRAY3, edgecolor=GRAY5, linewidth=0.5)
    ax.axvline(x=128, color=RED_ACCENT, linewidth=2, linestyle='--', label='Próg Otsu T=128')
    ax.fill_betweenx([0, max(counts)*1.1], 0, 128, alpha=0.12, color=ACCENT)
    ax.fill_betweenx([0, max(counts)*1.1], 128, 255, alpha=0.12, color=RED_ACCENT)
    ax.text(45, max(counts)*0.85, 'Klasa 0\n(tło)', ha='center', fontsize=FS, fontweight='bold', color=ACCENT)
    ax.text(195, max(counts)*0.85, 'Klasa 1\n(obiekt)', ha='center', fontsize=FS, fontweight='bold', color=RED_ACCENT)
    ax.annotate('Garb 1', xy=(60, max(counts)*0.6), fontsize=FS_SMALL, ha='center',
                arrowprops=dict(arrowstyle='->', color=GRAY5), xytext=(30, max(counts)*0.45))
    ax.annotate('Garb 2', xy=(190, max(counts)*0.5), fontsize=FS_SMALL, ha='center',
                arrowprops=dict(arrowstyle='->', color=GRAY5), xytext=(220, max(counts)*0.35))
    ax.set_xlabel('Jasność piksela (0–255)', fontsize=FS)
    ax.set_ylabel('Liczba pikseli', fontsize=FS)
    ax.set_title('Histogram bimodalny', fontsize=FS_TITLE, fontweight='bold')
    ax.legend(fontsize=FS_SMALL, loc='upper right')
    ax.set_xlim(0, 255)

    # --- Panel 2: Within-class variance explanation ---
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Wariancja wewnątrzklasowa', fontsize=FS_TITLE, fontweight='bold')

    y = 9.2
    texts = [
        ('Wariancja = jak bardzo wartości\nróżnią się od średniej', FS, 'black', 'normal'),
        ('', 0, 'black', 'normal'),
        ('Klasa 0 (piksele ≤ T):', FS, ACCENT, 'bold'),
        ('  wartości: 30, 50, 45, 60, 55', FS_SMALL, 'black', 'normal'),
        ('  średnia μ₀ = 48', FS_SMALL, 'black', 'normal'),
        ('  σ₀² = ((30-48)²+(50-48)²+...)/5 = 108', FS_SMALL, 'black', 'normal'),
        ('', 0, 'black', 'normal'),
        ('Klasa 1 (piksele > T):', FS, RED_ACCENT, 'bold'),
        ('  wartości: 180, 200, 190, 210, 195', FS_SMALL, 'black', 'normal'),
        ('  średnia μ₁ = 195', FS_SMALL, 'black', 'normal'),
        ('  σ₁² = ((180-195)²+...)/5 = 100', FS_SMALL, 'black', 'normal'),
        ('', 0, 'black', 'normal'),
        ('σ²_wewnątrz = w₀·σ₀² + w₁·σ₁²', FS, BLACK, 'bold'),
        ('= 0.6·108 + 0.4·100 = 104.8', FS_SMALL, 'black', 'normal'),
        ('', 0, 'black', 'normal'),
        ('Otsu próbuje KAŻDE T: 0,1,...,255', FS_SMALL, GREEN_ACCENT, 'bold'),
        ('Wybiera T dające MINIMUM σ²_wewnątrz', FS_SMALL, GREEN_ACCENT, 'bold'),
    ]
    for txt, size, color, weight in texts:
        if txt == '':
            y -= 0.25
            continue
        ax.text(0.3, y, txt, fontsize=size, color=color, fontweight=weight,
                va='top', transform=ax.transAxes if False else None)
        y -= 0.55

    # --- Panel 3: Jednorodność explanation ---
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('"Jednorodne" = małe σ²', fontsize=FS_TITLE, fontweight='bold')

    # Draw two clusters
    np.random.seed(7)
    # Good separation
    c0 = np.random.normal(2, 0.4, 15)
    c1 = np.random.normal(7, 0.4, 15)
    y_pos_0 = np.random.uniform(6, 8, 15)
    y_pos_1 = np.random.uniform(6, 8, 15)
    ax.scatter(c0, y_pos_0, c=ACCENT, s=30, zorder=5, label='Klasa 0')
    ax.scatter(c1, y_pos_1, c=RED_ACCENT, s=30, zorder=5, label='Klasa 1')
    ax.axvline(x=4.5, color=GREEN_ACCENT, linewidth=2, linestyle='--')
    ax.text(4.5, 8.8, 'T optymalny', ha='center', fontsize=FS_SMALL, color=GREEN_ACCENT, fontweight='bold')
    ax.text(2, 5.3, 'σ₀² mała\n(skupione)', ha='center', fontsize=FS_SMALL, color=ACCENT)
    ax.text(7, 5.3, 'σ₁² mała\n(skupione)', ha='center', fontsize=FS_SMALL, color=RED_ACCENT)
    ax.text(5, 4, '→ σ²_wewnątrz MINIMALNA\n→ klasy JEDNORODNE\n→ dobra segmentacja!',
            ha='center', fontsize=FS, fontweight='bold', color=GREEN_ACCENT)

    # Bad separation
    c0b = np.random.normal(3.5, 1.5, 15)
    c1b = np.random.normal(6, 1.5, 15)
    y_pos_0b = np.random.uniform(1, 3, 15)
    y_pos_1b = np.random.uniform(1, 3, 15)
    ax.scatter(c0b, y_pos_0b, c=ACCENT, s=30, marker='x', zorder=5)
    ax.scatter(c1b, y_pos_1b, c=RED_ACCENT, s=30, marker='x', zorder=5)
    ax.axvline(x=4.5, color=GRAY4, linewidth=1, linestyle=':', ymin=0, ymax=0.35)
    ax.text(5, 0.3, 'σ²_wewnątrz DUŻA → klasy mieszają się → zły próg',
            ha='center', fontsize=FS_SMALL, color=GRAY5)

    ax.legend(fontsize=FS_SMALL, loc='upper left')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_otsu_bimodal.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_otsu_bimodal.png")


# ============================================================
# 2. WATERSHED — Topographic flooding (not ASCII!)
# ============================================================
def generate_watershed():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))

    # --- Panel 1: Image as topographic surface ---
    ax = axes[0]
    x = np.linspace(0, 10, 200)
    # Create a surface with two valleys and a ridge
    surface = 3 * np.exp(-((x - 3)**2) / 1.5) + 4 * np.exp(-((x - 7)**2) / 1.2) + \
              0.5 * np.sin(x * 2) + 1
    # Invert: valleys at objects (dark), peaks at boundaries (bright)
    surface_inv = 6 - surface + 1

    ax.fill_between(x, 0, surface_inv, color=GRAY2, alpha=0.7)
    ax.plot(x, surface_inv, color=BLACK, linewidth=1.5)

    # Mark valleys
    ax.annotate('Dolina 1\n(obiekt A)', xy=(3, surface_inv[60]), fontsize=FS_SMALL,
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color=ACCENT), xytext=(1.5, 5.5))
    ax.annotate('Dolina 2\n(obiekt B)', xy=(7, surface_inv[140]), fontsize=FS_SMALL,
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color=RED_ACCENT), xytext=(8.5, 5.5))
    # Mark ridge
    ax.annotate('Grań\n(granica)', xy=(5, surface_inv[100]), fontsize=FS_SMALL,
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color=GREEN_ACCENT), xytext=(5, 6.5))

    ax.set_xlabel('Pozycja piksela', fontsize=FS)
    ax.set_ylabel('Jasność (= wysokość)', fontsize=FS)
    ax.set_title('Krok 1: obraz → teren', fontsize=FS_TITLE, fontweight='bold')
    ax.set_ylim(0, 7)

    # --- Panel 2: Flooding ---
    ax = axes[1]
    ax.fill_between(x, 0, surface_inv, color=GRAY2, alpha=0.7)
    ax.plot(x, surface_inv, color=BLACK, linewidth=1.5)

    # Water level
    water_level = 3.2
    water_mask_1 = (x < 5) & (surface_inv < water_level)
    water_mask_2 = (x >= 5) & (surface_inv < water_level)

    # Fill water in valley 1
    x_v1 = x[(x > 1) & (x < 5)]
    s_v1 = surface_inv[(x > 1) & (x < 5)]
    ax.fill_between(x_v1, s_v1, water_level, where=s_v1 < water_level,
                    color=ACCENT_LIGHT, alpha=0.6)
    # Fill water in valley 2
    x_v2 = x[(x > 5) & (x < 9)]
    s_v2 = surface_inv[(x > 5) & (x < 9)]
    ax.fill_between(x_v2, s_v2, water_level, where=s_v2 < water_level,
                    color='#FFCDD2', alpha=0.6)

    ax.axhline(y=water_level, color=ACCENT, linewidth=1, linestyle='--', alpha=0.5)
    ax.text(3, 2.5, 'Woda A', fontsize=FS, ha='center', color=ACCENT, fontweight='bold')
    ax.text(7, 2.2, 'Woda B', fontsize=FS, ha='center', color=RED_ACCENT, fontweight='bold')
    ax.annotate('Tu się spotkają!\n→ GRANICA', xy=(5, surface_inv[100]), fontsize=FS_SMALL,
                ha='center', color=GREEN_ACCENT, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=GREEN_ACCENT), xytext=(5, 6.2))

    ax.set_xlabel('Pozycja piksela', fontsize=FS)
    ax.set_title('Krok 2: zalewanie', fontsize=FS_TITLE, fontweight='bold')
    ax.set_ylim(0, 7)

    # --- Panel 3: Result with problem ---
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Krok 3: wynik', fontsize=FS_TITLE, fontweight='bold')

    # Good result
    rect1 = FancyBboxPatch((0.5, 6), 3.5, 3.2, boxstyle="round,pad=0.1",
                            facecolor=ACCENT_LIGHT, edgecolor=BLACK, linewidth=1)
    ax.add_patch(rect1)
    ax.text(2.25, 8.8, 'Ideał: 2 segmenty', fontsize=FS, ha='center', fontweight='bold')
    ax.text(2.25, 7.5, 'Segment A    Segment B', fontsize=FS_SMALL, ha='center')
    ax.text(2.25, 6.7, '(po marker-controlled)', fontsize=FS_SMALL, ha='center', color=GREEN_ACCENT)

    # Bad result (over-segmentation)
    rect2 = FancyBboxPatch((5.5, 6), 4, 3.2, boxstyle="round,pad=0.1",
                            facecolor='#FFCDD2', edgecolor=BLACK, linewidth=1)
    ax.add_patch(rect2)
    ax.text(7.5, 8.8, 'Problem: over-segmentation', fontsize=FS, ha='center', fontweight='bold',
            color=RED_ACCENT)
    ax.text(7.5, 7.8, '47 regionów zamiast 2!', fontsize=FS_SMALL, ha='center', color=RED_ACCENT)
    ax.text(7.5, 7.1, 'Każde mini-minimum', fontsize=FS_SMALL, ha='center')
    ax.text(7.5, 6.5, '→ osobna „dolina"', fontsize=FS_SMALL, ha='center')

    # Solution: markers
    rect3 = FancyBboxPatch((1, 0.5), 8, 4.5, boxstyle="round,pad=0.15",
                            facecolor=GRAY1, edgecolor=GREEN_ACCENT, linewidth=1.5)
    ax.add_patch(rect3)
    ax.text(5, 4.3, 'Rozwiązanie: Marker-controlled watershed', fontsize=FS,
            ha='center', fontweight='bold', color=GREEN_ACCENT)
    ax.text(5, 3.4, '1. Zaznacz ręcznie „seeds" (markery) w każdym obiekcie', fontsize=FS_SMALL, ha='center')
    ax.text(5, 2.7, '2. Zalewaj TYLKO od tych markerów (nie od wszystkich minimów)', fontsize=FS_SMALL, ha='center')
    ax.text(5, 2.0, '3. Eliminuje fałszywe doliny z szumu', fontsize=FS_SMALL, ha='center')
    ax.text(5, 1.2, 'Wynik: tyle segmentów, ile podano markerów', fontsize=FS_SMALL, ha='center',
            fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_watershed.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_watershed.png")


# ============================================================
# 3. MEAN SHIFT — Kernel, density, feature space
# ============================================================
def generate_mean_shift():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    # --- Panel 1: Feature space concept ---
    ax = axes[0]
    np.random.seed(42)
    # Three clusters in 2D feature space (brightness, x-position)
    c1x = np.random.normal(2, 0.5, 40)
    c1y = np.random.normal(2, 0.5, 40)
    c2x = np.random.normal(6, 0.6, 35)
    c2y = np.random.normal(7, 0.5, 35)
    c3x = np.random.normal(8, 0.4, 25)
    c3y = np.random.normal(3, 0.6, 25)

    ax.scatter(c1x, c1y, c=GRAY4, s=15, alpha=0.7, zorder=3)
    ax.scatter(c2x, c2y, c=GRAY4, s=15, alpha=0.7, zorder=3)
    ax.scatter(c3x, c3y, c=GRAY4, s=15, alpha=0.7, zorder=3)

    # Label peaks
    ax.scatter([2], [2], c=RED_ACCENT, s=80, marker='*', zorder=5, label='Max gęstości')
    ax.scatter([6], [7], c=RED_ACCENT, s=80, marker='*', zorder=5)
    ax.scatter([8], [3], c=RED_ACCENT, s=80, marker='*', zorder=5)

    ax.set_xlabel('Cecha 1: jasność', fontsize=FS)
    ax.set_ylabel('Cecha 2: pozycja x', fontsize=FS)
    ax.set_title('Przestrzeń cech', fontsize=FS_TITLE, fontweight='bold')
    ax.text(2, 0.3, 'Klaster 1\n(ciemne, lewo)', ha='center', fontsize=FS_TINY, color=GRAY6)
    ax.text(6, 5.3, 'Klaster 2\n(jasne, prawo)', ha='center', fontsize=FS_TINY, color=GRAY6)
    ax.text(8, 1.3, 'Klaster 3\n(jasne, dół)', ha='center', fontsize=FS_TINY, color=GRAY6)
    ax.legend(fontsize=FS_SMALL, loc='upper left')

    # --- Panel 2: Kernel/window moving ---
    ax = axes[1]
    ax.scatter(c1x, c1y, c=ACCENT_LIGHT, s=15, alpha=0.7, zorder=3)
    ax.scatter(c2x, c2y, c=GRAY3, s=15, alpha=0.7, zorder=3)
    ax.scatter(c3x, c3y, c=GRAY3, s=15, alpha=0.7, zorder=3)

    # Show kernel movement
    path_x = [4.5, 3.8, 3.0, 2.3, 2.05]
    path_y = [4.0, 3.3, 2.7, 2.2, 2.03]

    for i, (px, py) in enumerate(zip(path_x, path_y)):
        alpha = 0.3 + 0.15 * i
        circle = plt.Circle((px, py), 1.2, fill=False, edgecolor=ACCENT,
                            linewidth=1.5, linestyle='--' if i < len(path_x)-1 else '-',
                            alpha=alpha)
        ax.add_patch(circle)
        if i < len(path_x) - 1:
            ax.annotate('', xy=(path_x[i+1], path_y[i+1]),
                       xytext=(px, py),
                       arrowprops=dict(arrowstyle='->', color=RED_ACCENT, lw=1.5))

    ax.scatter([path_x[0]], [path_y[0]], c=ACCENT, s=50, marker='o', zorder=5)
    ax.scatter([path_x[-1]], [path_y[-1]], c=RED_ACCENT, s=80, marker='*', zorder=5)

    ax.text(4.5, 5.2, 'Start: losowy\npiksel', fontsize=FS_SMALL, ha='center', color=ACCENT)
    ax.text(2.05, 0.5, 'Koniec: max\ngęstości', fontsize=FS_SMALL, ha='center', color=RED_ACCENT,
            fontweight='bold')
    ax.text(7, 8, 'Okno (jądro)\nprzesuwa się\ndo skupiska', fontsize=FS_SMALL, ha='center',
            color=GRAY6,
            bbox=dict(boxstyle='round', facecolor=GRAY1, edgecolor=GRAY3))

    ax.set_xlabel('Cecha 1', fontsize=FS)
    ax.set_ylabel('Cecha 2', fontsize=FS)
    ax.set_title('Jądro → max gęstości', fontsize=FS_TITLE, fontweight='bold')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)

    # --- Panel 3: Why no K parameter ---
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Dlaczego bez K?', fontsize=FS_TITLE, fontweight='bold')

    y = 9.0
    lines = [
        ('K-means wymaga:', FS, RED_ACCENT, 'bold'),
        ('  „Podaj K=3 klastry"', FS_SMALL, 'black', 'normal'),
        ('  Problem: skąd wiesz ile klastrów?', FS_SMALL, GRAY5, 'normal'),
        ('', 0, '', ''),
        ('Mean Shift NIE wymaga K:', FS, GREEN_ACCENT, 'bold'),
        ('  Każdy piksel startuje → toczy się', FS_SMALL, 'black', 'normal'),
        ('  → trafia do najbliższego szczytu', FS_SMALL, 'black', 'normal'),
        ('  → ile szczytów = tyle segmentów', FS_SMALL, 'black', 'normal'),
        ('  → automatycznie!', FS_SMALL, GREEN_ACCENT, 'bold'),
        ('', 0, '', ''),
        ('Parametr: bandwidth (szerokość okna)', FS, 'black', 'bold'),
        ('  Duże okno → mało segmentów', FS_SMALL, 'black', 'normal'),
        ('  Małe okno → dużo segmentów', FS_SMALL, 'black', 'normal'),
        ('', 0, '', ''),
        ('Okno = jądro (kernel):', FS, 'black', 'bold'),
        ('  Koło o promieniu h wokół punktu.', FS_SMALL, 'black', 'normal'),
        ('  Oblicz średnią pikseli W oknie.', FS_SMALL, 'black', 'normal'),
        ('  Przesuń okno na tę średnią.', FS_SMALL, 'black', 'normal'),
        ('  Powtórz aż się zatrzyma.', FS_SMALL, 'black', 'normal'),
    ]
    for txt, size, color, weight in lines:
        if txt == '':
            y -= 0.2
            continue
        ax.text(0.5, y, txt, fontsize=size, color=color, fontweight=weight, va='top')
        y -= 0.5

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_mean_shift.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_mean_shift.png")


# ============================================================
# 4. NORMALIZED CUTS — Graph cut visualization
# ============================================================
def generate_normalized_cuts():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    # --- Panel 1: Image as graph ---
    ax = axes[0]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.set_title('Obraz → graf', fontsize=FS_TITLE, fontweight='bold')

    # Draw 4x4 pixel grid with colors
    pixel_vals = np.array([
        [30, 35, 180, 190],
        [40, 30, 185, 200],
        [170, 180, 40, 35],
        [190, 175, 30, 45],
    ])
    for i in range(4):
        for j in range(4):
            v = pixel_vals[i, j]
            gray_val = v / 255.0
            color = str(gray_val)
            rect = patches.Rectangle((j - 0.4, 3 - i - 0.4), 0.8, 0.8,
                                      facecolor=(gray_val, gray_val, gray_val),
                                      edgecolor=BLACK, linewidth=0.8)
            ax.add_patch(rect)
            text_color = 'white' if v < 100 else 'black'
            ax.text(j, 3 - i, str(v), ha='center', va='center', fontsize=FS_SMALL,
                    color=text_color, fontweight='bold')

    # Draw edges between adjacent pixels
    for i in range(4):
        for j in range(4):
            # Right neighbor
            if j < 3:
                similarity = max(0, 1 - abs(pixel_vals[i, j] - pixel_vals[i, j+1]) / 255)
                lw = similarity * 2.5 + 0.3
                alpha = similarity * 0.8 + 0.2
                ax.plot([j + 0.4, j + 0.6], [3 - i, 3 - i], color=GRAY5,
                       linewidth=lw, alpha=alpha)
            # Bottom neighbor
            if i < 3:
                similarity = max(0, 1 - abs(pixel_vals[i, j] - pixel_vals[i+1, j]) / 255)
                lw = similarity * 2.5 + 0.3
                alpha = similarity * 0.8 + 0.2
                ax.plot([j, j], [3 - i - 0.4, 3 - i - 0.6], color=GRAY5,
                       linewidth=lw, alpha=alpha)

    ax.text(2, -0.8, 'Grube linie = duże podobieństwo\n(silna krawędź grafu)',
            ha='center', fontsize=FS_TINY, color=GRAY5)
    ax.axis('off')

    # --- Panel 2: Cut concept ---
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Cięcie grafu (graph cut)', fontsize=FS_TITLE, fontweight='bold')

    # Draw two groups of nodes
    # Group A (dark pixels)
    positions_A = [(2, 7), (3, 8), (2, 5), (3, 6)]
    positions_B = [(7, 7), (8, 8), (7, 5), (8, 6)]

    # Intra-group edges (thick = similar)
    for i, (x1, y1) in enumerate(positions_A):
        for x2, y2 in positions_A[i+1:]:
            ax.plot([x1, x2], [y1, y2], color=ACCENT, linewidth=2, alpha=0.5)
    for i, (x1, y1) in enumerate(positions_B):
        for x2, y2 in positions_B[i+1:]:
            ax.plot([x1, x2], [y1, y2], color=RED_ACCENT, linewidth=2, alpha=0.5)

    # Inter-group edges (thin = dissimilar) — these get cut
    cut_edges = [((3, 8), (7, 7)), ((3, 6), (7, 5)), ((2, 5), (7, 5))]
    for (x1, y1), (x2, y2) in cut_edges:
        ax.plot([x1, x2], [y1, y2], color=GRAY4, linewidth=0.8, linestyle='--')

    # Draw nodes
    for x, y in positions_A:
        ax.scatter(x, y, c=ACCENT, s=120, zorder=5, edgecolors=BLACK, linewidth=0.8)
    for x, y in positions_B:
        ax.scatter(x, y, c='#FFCDD2', s=120, zorder=5, edgecolors=BLACK, linewidth=0.8)

    # Cut line
    ax.plot([5, 5], [3.5, 9.5], color=RED_ACCENT, linewidth=2.5, linestyle='-',
            zorder=4)
    ax.text(5, 9.8, 'CIĘCIE', ha='center', fontsize=FS, fontweight='bold', color=RED_ACCENT)

    ax.text(2.5, 3.8, 'Segment A\n(ciemne piksele)', ha='center', fontsize=FS_SMALL, color=ACCENT)
    ax.text(7.5, 3.8, 'Segment B\n(jasne piksele)', ha='center', fontsize=FS_SMALL, color=RED_ACCENT)

    # Formula
    ax.text(5, 1.8, 'Ncut(A,B) = cut(A,B)/assoc(A,V)\n                + cut(A,B)/assoc(B,V)',
            ha='center', fontsize=FS_SMALL, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=GRAY1, edgecolor=GRAY3))
    ax.text(5, 0.5, 'Minimalizuj Ncut → tnij SŁABE krawędzie\nzachowuj SILNE (wewnątrz grupy)',
            ha='center', fontsize=FS_TINY, color=GRAY5)

    # --- Panel 3: Algorithm summary ---
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Algorytm Normalized Cuts', fontsize=FS_TITLE, fontweight='bold')

    steps = [
        ('1. Zbuduj graf', 'Piksele = węzły\nKrawędzie = podobieństwo sąsiadów\n(kolor, jasność, odległość)'),
        ('2. Macierz podobieństwa W', 'W[i,j] = exp(-|kolori - kolorj|² / σ²)\n→ im podobniejsze, tym wyższa waga'),
        ('3. Macierz stopni D', 'D[i,i] = Σ W[i,j]\n(suma wszystkich wag z węzła i)'),
        ('4. Rozwiąż problem własny', '(D-W)·y = λ·D·y\n→ drugi najm. wektor własny y'),
        ('5. Podziel wg y', 'y[i] > 0 → segment A\ny[i] ≤ 0 → segment B'),
    ]

    y = 9.5
    for title, desc in steps:
        ax.text(0.5, y, title, fontsize=FS, fontweight='bold', va='top')
        y -= 0.4
        ax.text(0.8, y, desc, fontsize=FS_TINY, va='top', color=GRAY6)
        y -= 1.2

    ax.text(5, 0.3, 'Złożoność: O(n³) — wymaga eigen decomposition!',
            ha='center', fontsize=FS_SMALL, fontweight='bold', color=RED_ACCENT)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_normalized_cuts.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_normalized_cuts.png")


# ============================================================
# 5. RELU — Function plot
# ============================================================
def generate_relu():
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))

    # --- Panel 1: ReLU plot ---
    ax = axes[0]
    x = np.linspace(-5, 5, 200)
    relu = np.maximum(0, x)
    ax.plot(x, relu, color=ACCENT, linewidth=2.5, label='ReLU(x) = max(0, x)')
    ax.axhline(y=0, color=GRAY3, linewidth=0.5)
    ax.axvline(x=0, color=GRAY3, linewidth=0.5)
    ax.fill_between(x[x < 0], 0, 0, color=RED_ACCENT, alpha=0.1)
    ax.fill_between(x[x >= 0], 0, relu[x >= 0], color=ACCENT, alpha=0.1)

    # Annotations
    ax.annotate('x < 0 → output = 0\n(neuron „wyłączony")', xy=(-3, 0),
                fontsize=FS_SMALL, ha='center', va='bottom', color=RED_ACCENT,
                arrowprops=dict(arrowstyle='->', color=RED_ACCENT), xytext=(-3, 2))
    ax.annotate('x ≥ 0 → output = x\n(neuron „włączony")', xy=(3, 3),
                fontsize=FS_SMALL, ha='center', va='bottom', color=ACCENT,
                arrowprops=dict(arrowstyle='->', color=ACCENT), xytext=(3, 4.5))
    ax.scatter([0], [0], c=BLACK, s=40, zorder=5)
    ax.text(0.3, -0.5, '(0,0)', fontsize=FS_SMALL, color=GRAY5)
    ax.set_xlabel('x (wejście neuronu)', fontsize=FS)
    ax.set_ylabel('ReLU(x)', fontsize=FS)
    ax.set_title('ReLU — Rectified Linear Unit', fontsize=FS_TITLE, fontweight='bold')
    ax.legend(fontsize=FS_SMALL, loc='upper left')
    ax.set_ylim(-1, 6)
    ax.grid(True, alpha=0.2)

    # --- Panel 2: Why ReLU ---
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Dlaczego ReLU?', fontsize=FS_TITLE, fontweight='bold')

    y = 9.0
    lines = [
        ('Neuron oblicza:', FS, BLACK, 'bold'),
        ('  z = w₁·x₁ + w₂·x₂ + ... + bias', FS_SMALL, BLACK, 'normal'),
        ('  output = ReLU(z) = max(0, z)', FS_SMALL, ACCENT, 'bold'),
        ('', 0, '', ''),
        ('Przykład:', FS, BLACK, 'bold'),
        ('  wagi: w₁=0.5, w₂=-0.3, bias=0.1', FS_SMALL, BLACK, 'normal'),
        ('  wejścia: x₁=2.0, x₂=4.0', FS_SMALL, BLACK, 'normal'),
        ('  z = 0.5·2 + (-0.3)·4 + 0.1 = -0.1', FS_SMALL, BLACK, 'normal'),
        ('  ReLU(-0.1) = max(0, -0.1) = 0', FS_SMALL, RED_ACCENT, 'bold'),
        ('  → neuron milczy (wejście nieistotne)', FS_SMALL, GRAY5, 'normal'),
        ('', 0, '', ''),
        ('Gdyby z = 2.3:', FS, BLACK, 'bold'),
        ('  ReLU(2.3) = max(0, 2.3) = 2.3', FS_SMALL, GREEN_ACCENT, 'bold'),
        ('  → neuron aktywny! Przekazuje sygnał', FS_SMALL, GRAY5, 'normal'),
        ('', 0, '', ''),
        ('Szybsza niż sigmoid/tanh', FS_SMALL, GRAY5, 'normal'),
        ('(brak exp() → szybkie obliczenia)', FS_SMALL, GRAY5, 'normal'),
    ]
    for txt, size, color, weight in lines:
        if txt == '':
            y -= 0.2
            continue
        ax.text(0.5, y, txt, fontsize=size, color=color, fontweight=weight, va='top')
        y -= 0.5

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_relu.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_relu.png")


# ============================================================
# 6. DOT PRODUCT — Iloczyn skalarny visual
# ============================================================
def generate_dot_product():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))

    # --- Panel 1: Concept ---
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Iloczyn skalarny\n(dot product)', fontsize=FS_TITLE, fontweight='bold')

    y = 8.5
    lines = [
        ('Dwa wektory (listy liczb) → JEDNA liczba', FS, BLACK, 'bold'),
        ('', 0, '', ''),
        ('a = [a₁, a₂, a₃]    b = [b₁, b₂, b₃]', FS, ACCENT, 'normal'),
        ('', 0, '', ''),
        ('a · b = a₁·b₁ + a₂·b₂ + a₃·b₃', FS, BLACK, 'bold'),
        ('', 0, '', ''),
        ('Przykład:', FS, BLACK, 'bold'),
        ('a = [1, 3, -2]    b = [4, -1, 5]', FS_SMALL, BLACK, 'normal'),
        ('a·b = 1·4 + 3·(-1) + (-2)·5', FS_SMALL, BLACK, 'normal'),
        ('    = 4 + (-3) + (-10) = -9', FS_SMALL, RED_ACCENT, 'bold'),
        ('', 0, '', ''),
        ('Duży wynik → wektory „podobne" (w tym samym kierunku)', FS_SMALL, GREEN_ACCENT, 'normal'),
        ('Mały/ujemny → wektory „różne"', FS_SMALL, RED_ACCENT, 'normal'),
    ]
    for txt, size, color, weight in lines:
        if txt == '':
            y -= 0.25
            continue
        ax.text(0.5, y, txt, fontsize=size, color=color, fontweight=weight, va='top')
        y -= 0.55

    # --- Panel 2: Convolution as dot product ---
    ax = axes[1]
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_aspect('equal')
    ax.set_title('Konwolucja = iloczyn skalarny\nfiltra × fragment obrazu', fontsize=FS_TITLE, fontweight='bold')

    # Filter 3x3
    filter_vals = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    for i in range(3):
        for j in range(3):
            rect = patches.Rectangle((j - 0.4, 4 - i - 0.4), 0.8, 0.8,
                                      facecolor=ACCENT_LIGHT, edgecolor=BLACK, linewidth=0.8)
            ax.add_patch(rect)
            ax.text(j, 4 - i, str(filter_vals[i][j]), ha='center', va='center',
                    fontsize=FS, fontweight='bold')

    ax.text(1, 1.5, 'Filtr', ha='center', fontsize=FS, fontweight='bold', color=ACCENT)

    # Image patch
    img_vals = [[50, 50, 200], [50, 50, 200], [50, 50, 200]]
    for i in range(3):
        for j in range(3):
            rect = patches.Rectangle((j + 2.6, 4 - i - 0.4), 0.8, 0.8,
                                      facecolor=GRAY2, edgecolor=BLACK, linewidth=0.8)
            ax.add_patch(rect)
            ax.text(j + 3, 4 - i, str(img_vals[i][j]), ha='center', va='center',
                    fontsize=FS, fontweight='bold')

    ax.text(4, 1.5, 'Fragment\nobrazu', ha='center', fontsize=FS, fontweight='bold', color=GRAY5)

    ax.text(2.5, 0.5, '(-1)·50 + 0·50 + 1·200 +\n(-1)·50 + 0·50 + 1·200 +\n(-1)·50 + 0·50 + 1·200\n= 450 (krawędź!)',
            ha='center', fontsize=FS_TINY, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=GRAY1, edgecolor=GREEN_ACCENT))

    ax.axis('off')

    # --- Panel 3: Vector visualization ---
    ax = axes[2]
    # Draw two vectors
    ax.quiver(0, 0, 3, 4, angles='xy', scale_units='xy', scale=1,
              color=ACCENT, width=0.025, label='a = [3, 4]')
    ax.quiver(0, 0, 4, 1, angles='xy', scale_units='xy', scale=1,
              color=RED_ACCENT, width=0.025, label='b = [4, 1]')

    # Show angle
    theta = np.linspace(np.arctan2(1, 4), np.arctan2(4, 3), 30)
    r = 1.5
    ax.plot(r * np.cos(theta), r * np.sin(theta), color=GREEN_ACCENT, linewidth=1.5)
    ax.text(1.8, 1.3, 'θ', fontsize=FS, color=GREEN_ACCENT, fontweight='bold')

    ax.text(3.2, 4.2, 'a', fontsize=FS, color=ACCENT, fontweight='bold')
    ax.text(4.2, 1.2, 'b', fontsize=FS, color=RED_ACCENT, fontweight='bold')

    ax.text(2.5, -1.0, 'a · b = |a|·|b|·cos(θ)\n= 3·4 + 4·1 = 16',
            ha='center', fontsize=FS_SMALL, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=GRAY1, edgecolor=GRAY3))
    ax.text(2.5, -2.0, 'Mały kąt θ → duży dot product\n= wektory „zgadają się"',
            ha='center', fontsize=FS_TINY, color=GRAY5)

    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-2.5, 5.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.legend(fontsize=FS_SMALL, loc='upper left')
    ax.set_title('Geometrycznie: kąt', fontsize=FS_TITLE, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_dot_product.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_dot_product.png")


# ============================================================
# 7. FCN — FC vs Conv 1x1, skip connections
# ============================================================
def generate_fcn():
    fig, axes = plt.subplots(2, 1, figsize=(10, 7))

    # --- Panel 1: FC vs Conv 1x1 ---
    ax = axes[0]
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('FC (Fully Connected) vs Conv 1×1', fontsize=FS_TITLE, fontweight='bold')

    # Classic CNN with FC
    layer_info_fc = [
        (1.5, 'Obraz\n224×224×3', 2.2, GRAY2),
        (4.5, 'Conv+Pool\n112×112×64', 1.8, GRAY2),
        (7.5, 'Conv+Pool\n7×7×512', 1.0, GRAY2),
        (10, 'Flatten\n25088', 0.5, ACCENT_LIGHT),
        (12, 'FC\n4096', 0.5, ACCENT_LIGHT),
        (14, 'FC\n1000', 0.3, ACCENT_LIGHT),
        (16, '"Kot"', 0.3, '#FFCDD2'),
    ]

    y_fc = 4.5
    for i, (x, label, w, color) in enumerate(layer_info_fc):
        rect = FancyBboxPatch((x - w/2, y_fc - 0.6), w, 1.2,
                               boxstyle="round,pad=0.05", facecolor=color,
                               edgecolor=BLACK, linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x, y_fc, label, ha='center', va='center', fontsize=FS_TINY)
        if i < len(layer_info_fc) - 1:
            next_x = layer_info_fc[i + 1][0]
            ax.annotate('', xy=(next_x - layer_info_fc[i+1][2]/2, y_fc),
                       xytext=(x + w/2, y_fc),
                       arrowprops=dict(arrowstyle='->', color=GRAY5, lw=1))

    ax.text(0.3, y_fc, 'CNN:', fontsize=FS, fontweight='bold', color=RED_ACCENT, va='center')
    ax.text(12, y_fc + 1, 'PROBLEM: FC wymaga\nSTAŁEGO rozmiaru\n(np. 224×224)',
            ha='center', fontsize=FS_SMALL, color=RED_ACCENT, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#FFCDD2', edgecolor=RED_ACCENT, alpha=0.3))

    # FCN with Conv 1x1
    layer_info_fcn = [
        (1.5, 'Obraz\nH×W×3', 2.2, GRAY2),
        (4.5, 'Conv+Pool\nH/2 × W/2\n×64', 1.8, GRAY2),
        (7.5, 'Conv+Pool\nH/32 × W/32\n×512', 1.0, GRAY2),
        (10.5, 'Conv 1×1\nH/32 × W/32\n×C', 0.8, '#C8E6C9'),
        (13.5, 'Upsample\nH×W×C', 1.8, '#C8E6C9'),
        (16.5, 'Mapa\nsegmentacji', 1.5, '#C8E6C9'),
    ]

    y_fcn = 1.5
    for i, (x, label, w, color) in enumerate(layer_info_fcn):
        rect = FancyBboxPatch((x - w/2, y_fcn - 0.7), w, 1.4,
                               boxstyle="round,pad=0.05", facecolor=color,
                               edgecolor=BLACK, linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x, y_fcn, label, ha='center', va='center', fontsize=FS_TINY)
        if i < len(layer_info_fcn) - 1:
            next_x = layer_info_fcn[i + 1][0]
            ax.annotate('', xy=(next_x - layer_info_fcn[i+1][2]/2, y_fcn),
                       xytext=(x + w/2, y_fcn),
                       arrowprops=dict(arrowstyle='->', color=GRAY5, lw=1))

    ax.text(0.3, y_fcn, 'FCN:', fontsize=FS, fontweight='bold', color=GREEN_ACCENT, va='center')
    ax.text(10.5, y_fcn + 1.2, 'Conv 1×1:\nkażdy piksel\nosobno × wagi\n(jak FC ale\nzachowuje H×W)',
            ha='center', fontsize=FS_TINY, color=GREEN_ACCENT,
            bbox=dict(boxstyle='round', facecolor='#C8E6C9', edgecolor=GREEN_ACCENT, alpha=0.3))

    # --- Panel 2: What FC and Conv do ---
    ax = axes[1]
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('Co robi warstwa FC? Co robi konwolucja?', fontsize=FS_TITLE, fontweight='bold')

    # FC explanation
    rect = FancyBboxPatch((0.3, 3.2), 9, 2.5, boxstyle="round,pad=0.15",
                            facecolor=ACCENT_LIGHT, edgecolor=ACCENT, linewidth=1)
    ax.add_patch(rect)
    ax.text(4.8, 5.2, 'Fully Connected (FC)', fontsize=FS, fontweight='bold', ha='center')
    ax.text(4.8, 4.5, 'KAŻDY neuron połączony z KAŻDYM wejściem\n'
            '25 088 wejść × 4 096 neuronów = ~103 MLN wag!\n'
            'Traci informację GDZIE (przestrzenną)\n'
            'Wymaga STAŁEGO rozmiaru wejścia',
            fontsize=FS_TINY, ha='center', va='top')

    # Conv explanation
    rect = FancyBboxPatch((10.3, 3.2), 9, 2.5, boxstyle="round,pad=0.15",
                            facecolor='#C8E6C9', edgecolor=GREEN_ACCENT, linewidth=1)
    ax.add_patch(rect)
    ax.text(14.8, 5.2, 'Konwolucja (Conv)', fontsize=FS, fontweight='bold', ha='center')
    ax.text(14.8, 4.5, 'Filtr (np. 3×3) „jedzie" po obrazie\n'
            'Te same wagi dla KAŻDEJ pozycji\n'
            'Zachowuje informację GDZIE\n'
            'Akceptuje DOWOLNY rozmiar wejścia',
            fontsize=FS_TINY, ha='center', va='top')

    # Conv 1x1 explanation
    rect = FancyBboxPatch((3, 0.3), 14, 2.2, boxstyle="round,pad=0.15",
                            facecolor=GRAY1, edgecolor=BLACK, linewidth=1)
    ax.add_patch(rect)
    ax.text(10, 2.1, 'Conv 1×1 = „FC per piksel"', fontsize=FS, fontweight='bold', ha='center')
    ax.text(10, 1.5, 'Filtr 1×1: patrzy na JEDEN piksel, ale WSZYSTKIE kanały (512→C klas)\n'
            'Działa jak FC ale zachowuje mapę H×W → każdy piksel osobno klasyfikowany\n'
            'FCN: zamień FC na Conv1×1 → koniec z wymogiem stałego rozmiaru!',
            fontsize=FS_TINY, ha='center', va='top')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_fc_vs_conv1x1.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_fc_vs_conv1x1.png")


# ============================================================
# 8. U-NET ARCHITECTURE — Proper U-shaped diagram
# ============================================================
def generate_unet():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(-1, 21)
    ax.set_ylim(-1, 12)
    ax.axis('off')
    ax.set_title('U-Net: architektura w kształcie litery U', fontsize=FS_TITLE + 1, fontweight='bold')

    # Encoder layers (going DOWN-LEFT)
    encoder_layers = [
        (2, 10, 2.5, 1.5, '572×572×1\n(wejście)', 64),
        (2, 7.5, 2.2, 1.3, '284×284\n×64', 64),
        (2, 5, 1.8, 1.1, '140×140\n×128', 128),
        (2, 2.5, 1.5, 1.0, '68×68\n×256', 256),
    ]

    # Bottleneck
    bottleneck = (8, 0.5, 2.5, 1.2, '32×32×512\n(bottleneck)', 512)

    # Decoder layers (going UP-RIGHT)
    decoder_layers = [
        (14, 2.5, 1.5, 1.0, '68×68\n×256', 256),
        (14, 5, 1.8, 1.1, '140×140\n×128', 128),
        (14, 7.5, 2.2, 1.3, '284×284\n×64', 64),
        (14, 10, 2.5, 1.5, '572×572×C\n(mapa seg.)', 'C'),
    ]

    def draw_block(ax, x, y, w, h, label, color):
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                               boxstyle="round,pad=0.05", facecolor=color,
                               edgecolor=BLACK, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=FS_TINY)

    # Draw encoder
    for x, y, w, h, label, channels in encoder_layers:
        draw_block(ax, x, y, w, h, label, ACCENT_LIGHT)

    # Draw arrows down (encoder)
    for i in range(len(encoder_layers) - 1):
        x1, y1 = encoder_layers[i][0], encoder_layers[i][1] - encoder_layers[i][3]/2
        x2, y2 = encoder_layers[i+1][0], encoder_layers[i+1][1] + encoder_layers[i+1][3]/2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2))
        ax.text(x1 - 1.7, (y1 + y2) / 2, 'MaxPool\n2×2\n↓ zmniejsz', fontsize=FS_TINY,
                ha='center', color=ACCENT, fontweight='bold')

    # Encoder to bottleneck
    x1, y1 = encoder_layers[-1][0], encoder_layers[-1][1] - encoder_layers[-1][3]/2
    draw_block(ax, bottleneck[0], bottleneck[1], bottleneck[2], bottleneck[3],
               bottleneck[4], GRAY2)
    ax.annotate('', xy=(bottleneck[0] - bottleneck[2]/2, bottleneck[1] + bottleneck[3]/2),
               xytext=(x1, y1),
               arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2))

    # Bottleneck to decoder
    ax.annotate('', xy=(decoder_layers[0][0] - decoder_layers[0][2]/2,
                        decoder_layers[0][1] - decoder_layers[0][3]/2),
               xytext=(bottleneck[0] + bottleneck[2]/2, bottleneck[1] + bottleneck[3]/2),
               arrowprops=dict(arrowstyle='->', color=RED_ACCENT, lw=2))

    # Draw decoder
    for x, y, w, h, label, channels in decoder_layers:
        color = '#C8E6C9' if channels != 'C' else '#A5D6A7'
        draw_block(ax, x, y, w, h, label, color)

    # Draw arrows up (decoder)
    for i in range(len(decoder_layers) - 1):
        x1, y1 = decoder_layers[i][0], decoder_layers[i][1] + decoder_layers[i][3]/2
        x2, y2 = decoder_layers[i+1][0], decoder_layers[i+1][1] - decoder_layers[i+1][3]/2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color=GREEN_ACCENT, lw=2))
        ax.text(x1 + 2, (y1 + y2) / 2, 'UpConv\n2×2\n↑ zwiększ', fontsize=FS_TINY,
                ha='center', color=GREEN_ACCENT, fontweight='bold')

    # Skip connections (horizontal arrows)
    skip_colors = [GRAY5, GRAY5, GRAY5, GRAY5]
    for i in range(len(encoder_layers)):
        enc = encoder_layers[i]
        dec = decoder_layers[len(decoder_layers) - 1 - i]
        ax.annotate('', xy=(dec[0] - dec[2]/2, dec[1]),
                   xytext=(enc[0] + enc[2]/2, enc[1]),
                   arrowprops=dict(arrowstyle='->', color=GRAY5, lw=1.5,
                                 linestyle='dashed'))
        mid_x = (enc[0] + enc[2]/2 + dec[0] - dec[2]/2) / 2
        ax.text(mid_x, enc[1] + 0.6, 'skip\n(concat)', fontsize=FS_TINY,
                ha='center', color=GRAY5, fontweight='bold')

    # Labels
    ax.text(0, 11.5, 'ENCODER\n(↓ zmniejsza)', fontsize=FS, fontweight='bold', color=ACCENT,
            ha='center')
    ax.text(17, 11.5, 'DECODER\n(↑ zwiększa)', fontsize=FS, fontweight='bold', color=GREEN_ACCENT,
            ha='center')
    ax.text(8, -0.8, 'Kształt litery „U": encoder schodzi ↓ → bottleneck na dnie → decoder wraca ↑',
            fontsize=FS_SMALL, ha='center', color=GRAY5, fontweight='bold')

    # Concatenation explanation
    rect = FancyBboxPatch((17.5, 3), 3, 5, boxstyle="round,pad=0.15",
                            facecolor=GRAY1, edgecolor=GRAY5, linewidth=1, linestyle='--')
    ax.add_patch(rect)
    ax.text(19, 7.5, 'Concatenation:', fontsize=FS_SMALL, ha='center', fontweight='bold')
    ax.text(19, 6.5, 'Encoder: 64 kanały\nDecoder: 64 kanały\n→ concat → 128 kanałów\n\n'
            'Jak sklejenie\ndwóch stosów\nkart:', fontsize=FS_TINY, ha='center')
    ax.text(19, 3.7, '[enc₁|enc₂|...|dec₁|dec₂|...]', fontsize=FS_TINY - 1, ha='center',
            fontweight='bold', color=ACCENT)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_unet_arch.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_unet_arch.png")


# ============================================================
# 9. RECEPTIVE FIELD — with dilation
# ============================================================
def generate_receptive_field():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    def draw_grid(ax, size, highlight_cells, highlight_color, title, grid_offset=(0, 0)):
        ox, oy = grid_offset
        for i in range(size):
            for j in range(size):
                color = WHITE
                if (i, j) in highlight_cells:
                    color = highlight_color
                rect = patches.Rectangle((ox + j, oy + size - 1 - i), 1, 1,
                                          facecolor=color, edgecolor=GRAY4, linewidth=0.5)
                ax.add_patch(rect)
        ax.set_title(title, fontsize=FS_TITLE, fontweight='bold')

    # --- Panel 1: Standard 3x3 conv receptive field ---
    ax = axes[0]
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-1, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    # 7x7 input grid
    highlight_3x3 = [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4)]
    draw_grid(ax, 7, highlight_3x3, ACCENT_LIGHT, 'Zwykła conv 3×3')
    ax.text(3.5, -0.5, 'RF = 3×3 pikseli', fontsize=FS, ha='center', fontweight='bold', color=ACCENT)

    # --- Panel 2: Dilated conv (rate=2) ---
    ax = axes[1]
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-1, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    # 7x7 input grid with dilated highlights
    highlight_dilated = [(1, 1), (1, 3), (1, 5), (3, 1), (3, 3), (3, 5), (5, 1), (5, 3), (5, 5)]
    draw_grid(ax, 7, highlight_dilated, '#FFCDD2', 'Dilated conv 3×3\n(rate=2)')
    ax.text(3.5, -0.5, 'RF = 5×5, ale 9 parametrów!', fontsize=FS, ha='center',
            fontweight='bold', color=RED_ACCENT)

    # Connect dots to show pattern
    dots_x = [1.5, 3.5, 5.5, 1.5, 3.5, 5.5, 1.5, 3.5, 5.5]
    dots_y = [5.5, 5.5, 5.5, 3.5, 3.5, 3.5, 1.5, 1.5, 1.5]
    ax.scatter(dots_x, dots_y, c=RED_ACCENT, s=30, zorder=5)

    # --- Panel 3: Comparison ---
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Receptive Field\n(pole widzenia neuronu)', fontsize=FS_TITLE, fontweight='bold')

    y = 8.5
    lines = [
        ('RF = ile pikseli WEJŚCIOWYCH', FS, BLACK, 'bold'),
        ('wpływa na JEDEN piksel wyjścia', FS, BLACK, 'bold'),
        ('', 0, '', ''),
        ('Rate (współczynnik dylatacji):', FS, BLACK, 'bold'),
        ('  rate=1: filtr „dotyka" sąsiadów', FS_SMALL, BLACK, 'normal'),
        ('  rate=2: co drugi piksel → RF = 5×5', FS_SMALL, BLACK, 'normal'),
        ('  rate=3: co trzeci → RF = 7×7', FS_SMALL, BLACK, 'normal'),
        ('  WIĘCEJ kontekstu, TE SAME wagi!', FS_SMALL, GREEN_ACCENT, 'bold'),
        ('', 0, '', ''),
        ('Dlaczego ważne w segmentacji?', FS, BLACK, 'bold'),
        ('  Piksel sam nie wie czym jest.', FS_SMALL, BLACK, 'normal'),
        ('  Potrzebuje KONTEKSTU (otoczenia).', FS_SMALL, BLACK, 'normal'),
        ('  Większe RF → widzi obok budynki', FS_SMALL, BLACK, 'normal'),
        ('  → wie, że TEN piksel to „droga"', FS_SMALL, GREEN_ACCENT, 'bold'),
        ('', 0, '', ''),
        ('Global Average Pooling:', FS, BLACK, 'bold'),
        ('  Mapa H×W×C → 1×1×C', FS_SMALL, BLACK, 'normal'),
        ('  Średnia z CAŁEGO feature map', FS_SMALL, BLACK, 'normal'),
        ('  RF = nieskończone (cały obraz)', FS_SMALL, GREEN_ACCENT, 'bold'),
    ]
    for txt, size, color, weight in lines:
        if txt == '':
            y -= 0.2
            continue
        ax.text(0.5, y, txt, fontsize=size, color=color, fontweight=weight, va='top')
        y -= 0.45

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_receptive_field.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_receptive_field.png")


# ============================================================
# 10. TRANSFORMER / Self-attention / SOTA
# ============================================================
def generate_transformer():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    # --- Panel 1: CNN local vs Transformer global ---
    ax = axes[0]
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-1.5, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('CNN: widzi LOKALNIE', fontsize=FS_TITLE, fontweight='bold')

    # Draw 8x8 grid
    for i in range(8):
        for j in range(8):
            color = WHITE
            if 3 <= i <= 5 and 3 <= j <= 5:
                color = ACCENT_LIGHT
            rect = patches.Rectangle((j, 7 - i), 1, 1,
                                      facecolor=color, edgecolor=GRAY3, linewidth=0.3)
            ax.add_patch(rect)

    # Highlight center
    rect = patches.Rectangle((4, 4), 1, 1, facecolor=RED_ACCENT, edgecolor=BLACK, linewidth=1.5, alpha=0.7)
    ax.add_patch(rect)
    ax.text(4.5, 4.5, '?', ha='center', va='center', fontsize=FS, fontweight='bold', color=WHITE)
    ax.text(4.5, -0.8, 'Filtr 3×3 widzi tylko\n9 sąsiednich pikseli', fontsize=FS_SMALL,
            ha='center', color=ACCENT)

    # --- Panel 2: Transformer global ---
    ax = axes[1]
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-1.5, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Transformer: widzi GLOBALNIE', fontsize=FS_TITLE, fontweight='bold')

    # Draw 8x8 grid all highlighted
    for i in range(8):
        for j in range(8):
            color = '#FFCDD2'
            rect = patches.Rectangle((j, 7 - i), 1, 1,
                                      facecolor=color, edgecolor=GRAY3, linewidth=0.3)
            ax.add_patch(rect)

    rect = patches.Rectangle((4, 4), 1, 1, facecolor=RED_ACCENT, edgecolor=BLACK, linewidth=1.5, alpha=0.9)
    ax.add_patch(rect)
    ax.text(4.5, 4.5, '?', ha='center', va='center', fontsize=FS, fontweight='bold', color=WHITE)
    ax.text(4.5, -0.8, 'Self-attention „pyta"\nALL 64 piksele naraz', fontsize=FS_SMALL,
            ha='center', color=RED_ACCENT)

    # --- Panel 3: SOTA + Transformer explanation ---
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Transformer & SOTA', fontsize=FS_TITLE, fontweight='bold')

    y = 9.2
    lines = [
        ('Transformer:', FS, BLACK, 'bold'),
        ('  Architektura z 2017 (Vaswani et al.)', FS_SMALL, BLACK, 'normal'),
        ('  Oryginalnie do NLP (tłumaczenie)', FS_SMALL, BLACK, 'normal'),
        ('  Kluczowy mechanizm: SELF-ATTENTION', FS_SMALL, ACCENT, 'bold'),
        ('', 0, '', ''),
        ('Self-attention w skrócie:', FS, BLACK, 'bold'),
        ('  Każdy piksel tworzy trzy wektory:', FS_SMALL, BLACK, 'normal'),
        ('    Q (Query — „czego szukam?")', FS_SMALL, ACCENT, 'normal'),
        ('    K (Key — „co oferuję innych")', FS_SMALL, RED_ACCENT, 'normal'),
        ('    V (Value — „moja wartość")', FS_SMALL, GREEN_ACCENT, 'normal'),
        ('  Attention = softmax(Q·Kᵀ/√d)·V', FS_SMALL, BLACK, 'bold'),
        ('  Koszt: O(n²) — n=liczba pikseli', FS_SMALL, RED_ACCENT, 'normal'),
        ('', 0, '', ''),
        ('SOTA = State Of The Art:', FS, BLACK, 'bold'),
        ('  Najlepszy znany wynik na benchmarku', FS_SMALL, BLACK, 'normal'),
        ('  Np. „mIoU 85.1% na ADE20K = SOTA"', FS_SMALL, BLACK, 'normal'),
        ('  Ciągle się zmienia (nowy paper', FS_SMALL, GRAY5, 'normal'),
        ('  → nowy SOTA)', FS_SMALL, GRAY5, 'normal'),
    ]
    for txt, size, color, weight in lines:
        if txt == '':
            y -= 0.15
            continue
        ax.text(0.3, y, txt, fontsize=size, color=color, fontweight=weight, va='top')
        y -= 0.45

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_transformer_attention.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_transformer_attention.png")


# ============================================================
# 11. REGION GROWING — seed selection + BFS
# ============================================================
def generate_region_growing():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.2))

    # --- Panel 1: Manual vs automatic seed ---
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Seed: ręcznie vs automatycznie', fontsize=FS_TITLE, fontweight='bold')

    y = 9.2
    lines = [
        ('Ręczny seed:', FS, ACCENT, 'bold'),
        ('  Użytkownik klika na obraz', FS_SMALL, BLACK, 'normal'),
        ('  → „tu jest obiekt, od tego zacznij"', FS_SMALL, BLACK, 'normal'),
        ('  Użycie: segmentacja interaktywna', FS_SMALL, GRAY5, 'normal'),
        ('  (np. Photoshop — magic wand tool)', FS_SMALL, GRAY5, 'normal'),
        ('', 0, '', ''),
        ('Automatyczny seed:', FS, RED_ACCENT, 'bold'),
        ('  1. Histogram → lokalne maxima', FS_SMALL, BLACK, 'normal'),
        ('     (najczęstsza jasność → seed)', FS_SMALL, GRAY5, 'normal'),
        ('  2. Grid: siatka co N pikseli', FS_SMALL, BLACK, 'normal'),
        ('     (np. seed co 50 px → 100 seedów)', FS_SMALL, GRAY5, 'normal'),
        ('  3. Losowe próbkowanie', FS_SMALL, BLACK, 'normal'),
        ('  4. Ekstrema lokalne gradientu', FS_SMALL, BLACK, 'normal'),
        ('', 0, '', ''),
        ('Dlaczego OR?', FS, GREEN_ACCENT, 'bold'),
        ('  Ręczny → precyzyjny, ale wolny', FS_SMALL, BLACK, 'normal'),
        ('  Auto → szybki, ale over-segmentation', FS_SMALL, BLACK, 'normal'),
    ]
    for txt, size, color, weight in lines:
        if txt == '':
            y -= 0.15
            continue
        ax.text(0.3, y, txt, fontsize=size, color=color, fontweight=weight, va='top')
        y -= 0.45

    # --- Panel 2: Region growing step by step ---
    ax = axes[1]
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-1.5, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Region Growing: krok po kroku', fontsize=FS_TITLE, fontweight='bold')

    # 6x6 grid with values
    pixel_grid = np.array([
        [150, 153, 148, 200, 210, 205],
        [147, 155, 152, 195, 208, 200],
        [145, 148, 160, 190, 195, 210],
        [200, 195, 190, 155, 148, 150],
        [210, 205, 200, 150, 152, 145],
        [215, 208, 195, 148, 147, 155],
    ])

    # Region grown from seed (2,1) with threshold 20
    region_mask = np.array([
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1],
    ])

    for i in range(6):
        for j in range(6):
            v = pixel_grid[i, j]
            if region_mask[i, j] == 1 and v < 170:
                color = ACCENT_LIGHT
            elif region_mask[i, j] == 1:
                color = GRAY2
            else:
                color = WHITE
            if i == 1 and j == 1:
                color = '#FFD54F'  # Seed
            rect = patches.Rectangle((j, 5 - i), 1, 1,
                                      facecolor=color, edgecolor=GRAY4, linewidth=0.5)
            ax.add_patch(rect)
            ax.text(j + 0.5, 5 - i + 0.5, str(v), ha='center', va='center',
                    fontsize=FS_TINY, fontweight='bold')

    # Mark seed
    ax.annotate('SEED\n(155)', xy=(1.5, 4.5), fontsize=FS_SMALL,
                ha='center', color=RED_ACCENT, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=RED_ACCENT), xytext=(-0.5, 7))

    ax.text(3, -0.8, 'Próg = 20\nNiebieski = region (|val - seed| < 20)',
            fontsize=FS_TINY, ha='center', color=ACCENT)

    # --- Panel 3: BFS expansion ---
    ax = axes[2]
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-1.5, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Rosnący region (BFS)', fontsize=FS_TITLE, fontweight='bold')

    # Show expansion waves
    wave_colors = ['#FFD54F', '#FFF176', '#FFF9C4', ACCENT_LIGHT, '#B3D4FC']
    wave_labels = ['Seed', 'Fala 1', 'Fala 2', 'Fala 3', 'Fala 4']
    waves = [
        [(1, 1)],  # seed
        [(0, 1), (1, 0), (1, 2), (2, 1)],  # wave 1
        [(0, 0), (0, 2), (2, 0), (2, 2)],  # wave 2
    ]

    for i in range(6):
        for j in range(6):
            color = WHITE
            for w_idx, wave in enumerate(waves):
                if (i, j) in wave:
                    color = wave_colors[w_idx]
            rect = patches.Rectangle((j, 5 - i), 1, 1,
                                      facecolor=color, edgecolor=GRAY4, linewidth=0.5)
            ax.add_patch(rect)

    # Draw BFS arrows from seed
    seed_x, seed_y = 1.5, 4.5
    for dx, dy, label in [(0, 1, ''), (0, -1, ''), (1, 0, ''), (-1, 0, '')]:
        ax.annotate('', xy=(seed_x + dx * 0.7, seed_y + dy * 0.7),
                   xytext=(seed_x, seed_y),
                   arrowprops=dict(arrowstyle='->', color=RED_ACCENT, lw=1.2))

    ax.text(3, -0.5, 'BFS: sprawdzaj sąsiadów,\ndodawaj podobne do kolejki',
            fontsize=FS_TINY, ha='center', color=GRAY5)

    # Legend
    for w_idx, (color, label) in enumerate(zip(wave_colors[:3], wave_labels[:3])):
        rect = patches.Rectangle((4, 6.5 - w_idx * 0.7), 0.5, 0.5,
                                  facecolor=color, edgecolor=GRAY4, linewidth=0.5)
        ax.add_patch(rect)
        ax.text(4.8, 6.75 - w_idx * 0.7, label, fontsize=FS_TINY, va='center')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_region_growing.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_region_growing.png")


# ============================================================
# 12. DIY THRESHOLDING — Step-by-step example
# ============================================================
def generate_diy_thresholding():
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))

    np.random.seed(42)

    # Create a simple synthetic image: dark circle on bright background
    size = 64
    img = np.ones((size, size)) * 200  # bright background
    yy, xx = np.mgrid[:size, :size]
    mask = ((xx - 32)**2 + (yy - 32)**2) < 15**2
    img[mask] = 60  # dark circle
    # Add some noise
    img += np.random.normal(0, 10, img.shape)
    img = np.clip(img, 0, 255)

    # --- Panel 1: Original image ---
    ax = axes[0, 0]
    ax.imshow(img, cmap='gray', vmin=0, vmax=255)
    ax.set_title('Krok 1: obraz wejściowy', fontsize=FS, fontweight='bold')
    ax.axis('off')
    ax.text(32, -3, '64×64 pikseli, szare', fontsize=FS_TINY, ha='center')

    # --- Panel 2: Histogram ---
    ax = axes[0, 1]
    counts, bins, _ = ax.hist(img.ravel(), bins=50, color=GRAY3, edgecolor=GRAY5, linewidth=0.5)
    ax.axvline(x=128, color=RED_ACCENT, linewidth=2, linestyle='--', label='T=128 (Otsu)')
    ax.set_xlabel('Jasność', fontsize=FS_SMALL)
    ax.set_ylabel('Piksele', fontsize=FS_SMALL)
    ax.set_title('Krok 2: histogram\n(bimodalny!)', fontsize=FS, fontweight='bold')
    ax.legend(fontsize=FS_TINY)
    ax.annotate('Garb 1\n(obiekt)', xy=(60, max(counts)*0.5), fontsize=FS_TINY, ha='center',
                color=ACCENT, fontweight='bold')
    ax.annotate('Garb 2\n(tło)', xy=(200, max(counts)*0.5), fontsize=FS_TINY, ha='center',
                color=RED_ACCENT, fontweight='bold')

    # --- Panel 3: Thresholding result ---
    ax = axes[0, 2]
    binary = (img > 128).astype(float)
    ax.imshow(binary, cmap='gray', vmin=0, vmax=1)
    ax.set_title('Krok 3: progowanie T=128', fontsize=FS, fontweight='bold')
    ax.axis('off')
    ax.text(32, -3, 'Biały = tło, Czarny = obiekt', fontsize=FS_TINY, ha='center')

    # --- Panel 4: What Otsu does (variance plot) ---
    ax = axes[1, 0]
    # Compute within-class variance for each threshold
    thresholds = range(10, 245)
    variances = []
    for t in thresholds:
        c0 = img[img <= t].ravel()
        c1 = img[img > t].ravel()
        if len(c0) == 0 or len(c1) == 0:
            variances.append(np.nan)
            continue
        w0 = len(c0) / len(img.ravel())
        w1 = len(c1) / len(img.ravel())
        var = w0 * np.var(c0) + w1 * np.var(c1)
        variances.append(var)

    ax.plot(list(thresholds), variances, color=ACCENT, linewidth=1.5)
    best_t = list(thresholds)[np.nanargmin(variances)]
    ax.axvline(x=best_t, color=RED_ACCENT, linewidth=1.5, linestyle='--', label=f'Otsu T={best_t}')
    ax.scatter([best_t], [np.nanmin(variances)], c=RED_ACCENT, s=60, zorder=5)
    ax.set_xlabel('Próg T', fontsize=FS_SMALL)
    ax.set_ylabel('σ² wewnątrzklasowa', fontsize=FS_SMALL)
    ax.set_title('Krok 4: Otsu szuka min σ²', fontsize=FS, fontweight='bold')
    ax.legend(fontsize=FS_TINY)

    # --- Panel 5: Pseudocode ---
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Pseudokod Otsu', fontsize=FS, fontweight='bold')

    code_lines = [
        'best_T = 0',
        'min_var = ∞',
        '',
        'for T in 0..255:',
        '  c0 = piksele z jasność ≤ T',
        '  c1 = piksele z jasność > T',
        '  w0 = len(c0) / len(all)',
        '  w1 = len(c1) / len(all)',
        '  var = w0·var(c0) + w1·var(c1)',
        '  if var < min_var:',
        '     min_var = var',
        '     best_T = T',
        '',
        'return best_T  # optymalny próg',
    ]
    for i, line in enumerate(code_lines):
        color = ACCENT if 'best_T = T' in line or 'return' in line else BLACK
        ax.text(0.5, 9.5 - i * 0.65, line, fontsize=FS_TINY, fontfamily='monospace',
                color=color, fontweight='bold' if color == ACCENT else 'normal')

    # --- Panel 6: Final result with Otsu ---
    ax = axes[1, 2]
    binary_otsu = (img > best_t).astype(float)
    ax.imshow(binary_otsu, cmap='gray', vmin=0, vmax=1)
    ax.set_title(f'Krok 5: wynik Otsu (T={best_t})', fontsize=FS, fontweight='bold')
    ax.axis('off')
    ax.text(32, -3, 'Automatyczny próg!', fontsize=FS_TINY, ha='center',
            color=GREEN_ACCENT, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_diy_thresholding.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_diy_thresholding.png")


# ============================================================
# 13. DIY U-NET — Simplified step-by-step
# ============================================================
def generate_diy_unet():
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))

    np.random.seed(42)
    size = 64

    # Create synthetic image with two regions
    img = np.ones((size, size, 3), dtype=np.uint8) * 200  # bright bg
    # Dark region (object 1)
    yy, xx = np.mgrid[:size, :size]
    mask1 = ((xx - 20)**2 + (yy - 30)**2) < 12**2
    img[mask1] = [60, 60, 60]
    # Medium region (object 2)
    mask2 = ((xx - 45)**2 + (yy - 25)**2) < 8**2
    img[mask2] = [120, 120, 120]

    gt = np.zeros((size, size), dtype=np.uint8)
    gt[mask1] = 1  # class 1
    gt[mask2] = 2  # class 2

    # --- Panel 1: Input image ---
    ax = axes[0, 0]
    ax.imshow(img)
    ax.set_title('Krok 1: obraz RGB\n64×64×3', fontsize=FS, fontweight='bold')
    ax.axis('off')

    # --- Panel 2: Encoder shrinks ---
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Krok 2: Encoder ZMNIEJSZA', fontsize=FS, fontweight='bold')

    sizes = [(64, 3), (32, 64), (16, 128), (8, 256)]
    y_pos = 8.5
    for i, (s, c) in enumerate(sizes):
        w = s / 64 * 4
        h = 0.8
        rect = FancyBboxPatch((5 - w/2, y_pos), w, h,
                               boxstyle="round,pad=0.05", facecolor=ACCENT_LIGHT,
                               edgecolor=ACCENT, linewidth=1)
        ax.add_patch(rect)
        ax.text(5, y_pos + h/2, f'{s}×{s}×{c}', ha='center', va='center',
                fontsize=FS_SMALL, fontweight='bold')
        if i < len(sizes) - 1:
            ax.annotate('', xy=(5, y_pos - 0.3), xytext=(5, y_pos),
                       arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))
            ax.text(7, y_pos - 0.15, 'Conv+Pool', fontsize=FS_TINY, color=ACCENT)
        y_pos -= 2.2

    ax.text(5, 0.3, 'Wyciąga cechy:\nkrawędzie → tekstury → obiekty',
            ha='center', fontsize=FS_TINY, color=GRAY5)

    # --- Panel 3: Bottleneck ---
    ax = axes[0, 2]
    # Show feature maps at bottleneck (abstract)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Krok 3: Bottleneck\n(najbardziej abstrakcyjne cechy)', fontsize=FS, fontweight='bold')

    # Show small abstract feature maps
    for k in range(4):
        small = np.random.rand(4, 4)
        ax_inset = fig.add_axes([0.68 + (k % 2) * 0.08, 0.72 - (k // 2) * 0.1, 0.06, 0.06])
        ax_inset.imshow(small, cmap='gray')
        ax_inset.axis('off')

    ax.text(5, 5, '8×8×256\n\nMałe mapy, ale DUŻO kanałów\nKażdy kanał = jedna „cecha"\n'
            '(np. kanał 42 = „wykrył koło"\n  kanał 78 = „wykrył krawędź")\n\n'
            'Wie CO jest na obrazie\nale nie wie GDZIE dokładnie',
            ha='center', va='center', fontsize=FS_SMALL,
            bbox=dict(boxstyle='round', facecolor=GRAY1, edgecolor=GRAY3))

    # --- Panel 4: Decoder enlarges ---
    ax = axes[1, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Krok 4: Decoder ZWIĘKSZA\n(+ skip connections!)', fontsize=FS, fontweight='bold')

    sizes_dec = [(8, 256), (16, 128), (32, 64), (64, 3)]
    y_pos = 8.5
    for i, (s, c) in enumerate(sizes_dec):
        w = s / 64 * 4
        h = 0.8
        rect = FancyBboxPatch((5 - w/2, y_pos), w, h,
                               boxstyle="round,pad=0.05", facecolor='#C8E6C9',
                               edgecolor=GREEN_ACCENT, linewidth=1)
        ax.add_patch(rect)
        label = f'{s}×{s}×{c}'
        if i < len(sizes_dec) - 1:
            label += ' + skip!'
        ax.text(5, y_pos + h/2, label, ha='center', va='center',
                fontsize=FS_SMALL, fontweight='bold')
        if i < len(sizes_dec) - 1:
            ax.annotate('', xy=(5, y_pos - 0.3), xytext=(5, y_pos),
                       arrowprops=dict(arrowstyle='->', color=GREEN_ACCENT, lw=1.5))
            ax.text(7, y_pos - 0.15, 'UpConv+Concat', fontsize=FS_TINY, color=GREEN_ACCENT)
        y_pos -= 2.2

    ax.text(5, 0.3, 'Odtwarza rozdzielczość:\nskip → przywraca krawędzie',
            ha='center', fontsize=FS_TINY, color=GRAY5)

    # --- Panel 5: Output segmentation map ---
    ax = axes[1, 1]
    cmap = plt.cm.colors.ListedColormap([WHITE, ACCENT_LIGHT, '#FFCDD2'])
    ax.imshow(gt, cmap=cmap, interpolation='nearest')
    ax.set_title('Krok 5: mapa segmentacji\n64×64 (3 klasy)', fontsize=FS, fontweight='bold')
    ax.axis('off')
    ax.text(20, -3, 'Tło=0, obiekt A=1, obiekt B=2', fontsize=FS_TINY, ha='center')

    # --- Panel 6: Summary pseudocode ---
    ax = axes[1, 2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Pseudokod U-Net', fontsize=FS, fontweight='bold')

    code_lines = [
        '# ENCODER',
        'e1 = conv_block(input, 64)   # 64×64',
        'e2 = conv_block(pool(e1), 128) # 32×32',
        'e3 = conv_block(pool(e2), 256) # 16×16',
        '',
        '# BOTTLENECK',
        'b = conv_block(pool(e3), 512)  # 8×8',
        '',
        '# DECODER + SKIP',
        'd3 = conv_block(concat(',
        '       upconv(b), e3), 256)   # 16×16',
        'd2 = conv_block(concat(',
        '       upconv(d3), e2), 128)  # 32×32',
        'd1 = conv_block(concat(',
        '       upconv(d2), e1), 64)   # 64×64',
        '',
        'output = conv_1x1(d1, n_classes)',
    ]
    for i, line in enumerate(code_lines):
        color = ACCENT if 'concat' in line else (GREEN_ACCENT if 'output' in line else BLACK)
        ax.text(0.3, 9.5 - i * 0.55, line, fontsize=FS_TINY, fontfamily='monospace',
                color=color)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_diy_unet.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_diy_unet.png")


# ============================================================
# 14. MNEMONICS — Visual mnemonic summary
# ============================================================
def generate_mnemonics():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.axis('off')
    ax.set_title('Mnemoniki — segmentacja obrazu', fontsize=FS_TITLE + 2, fontweight='bold')

    def draw_card(ax, x, y, w, h, title, mnemonic, color, detail=''):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                               facecolor=color, edgecolor=BLACK, linewidth=1)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.3, title, ha='center', va='top',
                fontsize=FS, fontweight='bold')
        ax.text(x + w/2, y + h/2 - 0.1, mnemonic, ha='center', va='center',
                fontsize=FS_SMALL, fontstyle='italic', color=GRAY6)
        if detail:
            ax.text(x + w/2, y + 0.4, detail, ha='center', va='bottom',
                    fontsize=FS_TINY, color=GRAY5)

    # Title: STRATEGIE KLASYCZNE
    ax.text(5, 15.5, 'STRATEGIE KLASYCZNE', fontsize=FS_TITLE, fontweight='bold',
            color=ACCENT, ha='center')

    cards_classic = [
        (0.2, 12.5, 4.5, 2.5, 'Thresholding', '„PRÓG na bramce"\nPrzepuszcza > T,\nblokuje ≤ T',
         ACCENT_LIGHT, 'jasne=1, ciemne=0'),
        (5, 12.5, 4.5, 2.5, 'Otsu', '„AUTO-bramkarz"\nSam dobiera próg\nmin σ² wewnątrz',
         ACCENT_LIGHT, 'histogram bimodalny'),
        (0.2, 9.5, 4.5, 2.5, 'Region Growing', '„PLAMA rozlana"\nSeed → BFS po\npodobnych sąsiadach',
         ACCENT_LIGHT, 'jak atrament na papierze'),
        (5, 9.5, 4.5, 2.5, 'Watershed', '„ZALEWANIE terenu"\nDoliny=obiekty\nGranie=granice',
         ACCENT_LIGHT, 'woda + geography'),
        (0.2, 6.5, 4.5, 2.5, 'Mean Shift', '„KULKI toczą się"\nKażda → max gęstości\nBez K!',
         ACCENT_LIGHT, 'bandwidth = okno'),
        (5, 6.5, 4.5, 2.5, 'Normalized Cuts', '„CIĘCIE sznurków"\nGraf: tnij słabe\nkrawędzie (O(n³)!)',
         ACCENT_LIGHT, 'eigenvector problem'),
    ]

    for args in cards_classic:
        draw_card(ax, *args)

    # Title: SIECI NEURONOWE
    ax.text(15, 15.5, 'SIECI NEURONOWE', fontsize=FS_TITLE, fontweight='bold',
            color=GREEN_ACCENT, ha='center')

    cards_nn = [
        (10.5, 12.5, 4.5, 2.5, 'FCN (2015)', '„FC → Conv 1×1"\nPierwsza end-to-end\nDowolny rozmiar',
         '#C8E6C9', 'skip connections'),
        (15.3, 12.5, 4.5, 2.5, 'U-Net (2015)', '„Litera U"\nEncoder↓ Decoder↑\nSkip = concat',
         '#C8E6C9', 'medycyna, małe dane'),
        (10.5, 9.5, 4.5, 2.5, 'DeepLab v3+', '„DZIURY w filtrze"\nAtrous conv (rate)\nASPP multi-scale',
         '#C8E6C9', 'à trous = z dziurami'),
        (15.3, 9.5, 4.5, 2.5, 'Transformer', '„WSZYSCY ze\nWSZYSTKIMI"\nSelf-attention O(n²)',
         '#C8E6C9', 'SegFormer, Mask2Former'),
    ]

    for args in cards_nn:
        draw_card(ax, *args)

    # Metryki
    ax.text(10, 8.3, 'METRYKI I LOSS', fontsize=FS_TITLE, fontweight='bold',
            color=RED_ACCENT, ha='center')

    cards_metrics = [
        (10.5, 6.5, 4.5, 1.6, 'mIoU', '„Nakładka / Suma"\nIoU = A∩B / A∪B',
         '#FFCDD2', ''),
        (15.3, 6.5, 4.5, 1.6, 'Dice / Focal', '„Dice=2·nakładka"\nFocal=trudne px',
         '#FFCDD2', ''),
    ]

    for args in cards_metrics:
        draw_card(ax, *args)

    # Master mnemonic at bottom
    rect = FancyBboxPatch((1, 0.3), 18, 5.5, boxstyle="round,pad=0.2",
                            facecolor=GRAY1, edgecolor=BLACK, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(10, 5.3, 'SUPER-MNEMONIK: kolejność algorytmów segmentacji',
            ha='center', fontsize=FS, fontweight='bold')
    ax.text(10, 4.5, '„TORW-MN  FUD-T"', ha='center', fontsize=FS_TITLE + 2,
            fontweight='bold', color=RED_ACCENT)
    ax.text(10, 3.5, 'Klasyczne: Thresholding → Otsu → Region growing → Watershed → Mean shift → Norm. cuts',
            ha='center', fontsize=FS_SMALL)
    ax.text(10, 2.8, 'Neuronowe: FCN → U-Net → DeepLab → Transformer',
            ha='center', fontsize=FS_SMALL)
    ax.text(10, 1.8, '„Turyści Oglądają Rzekę, Wodospad, Morze, Nurt — Fotografują Uroczy Dwór Tajemnic"',
            ha='center', fontsize=FS_SMALL, fontstyle='italic', color=ACCENT)
    ax.text(10, 1.0, 'Klasyczne: proste→auto→BFS→flood→gęstość→graf   |   Neuronowe: FC→U-skip→dilated→attention',
            ha='center', fontsize=FS_TINY, color=GRAY5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'q23_mnemonics.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print("  ✓ q23_mnemonics.png")


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Generating PYTANIE 23 diagrams...")
    generate_otsu_bimodal()
    generate_watershed()
    generate_mean_shift()
    generate_normalized_cuts()
    generate_relu()
    generate_dot_product()
    generate_fcn()
    generate_unet()
    generate_receptive_field()
    generate_transformer()
    generate_region_growing()
    generate_diy_thresholding()
    generate_diy_unet()
    generate_mnemonics()
    print(f"\nAll diagrams saved to: {OUTPUT_DIR}")
