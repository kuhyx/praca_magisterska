#!/usr/bin/env python3
"""
Generate architecture modeling diagrams for PYTANIE 13 (AIS):
  1. TOGAF ADM cycle
  2. 4+1 View Model (Kruchten)
  3. C4 Model — 4 zoom levels
  4. Zachman Framework grid
  5. ArchiMate layers

All: A4-compatible, B&W, 300 DPI, laser-printer-friendly.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon, Wedge, Arc
from matplotlib.path import Path
import numpy as np
import os

DPI = 300
BG = 'white'
LN = 'black'
FS = 9
FS_TITLE = 14
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Light grays for B&W contrast
GRAY1 = '#E8E8E8'
GRAY2 = '#D0D0D0'
GRAY3 = '#B8B8B8'
GRAY4 = '#F5F5F5'


def draw_arrow(ax, x1, y1, x2, y2, lw=1.3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=LN, lw=lw))


def draw_line(ax, x1, y1, x2, y2, lw=1.3, ls='-'):
    ax.plot([x1, x2], [y1, y2], color=LN, lw=lw, linestyle=ls)


def draw_box(ax, x, y, w, h, text, fill='white', lw=1.5, fontsize=FS,
             fontweight='normal', ha='center', va='center', rounded=False):
    if rounded:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                              lw=lw, edgecolor=LN, facecolor=fill)
    else:
        rect = plt.Rectangle((x, y), w, h, lw=lw, edgecolor=LN, facecolor=fill)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha=ha, va=va, fontsize=fontsize,
            fontweight=fontweight, wrap=True)


# =========================================================================
# 1. TOGAF ADM Cycle
# =========================================================================
def generate_togaf_adm():
    fig, ax = plt.subplots(figsize=(8.27, 8.27))
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    ax.set_title("TOGAF ADM (Architecture Development Method)",
                 fontsize=FS_TITLE, fontweight='bold', pad=15)

    # Center: Requirements Management
    c = plt.Circle((0, 0), 2.5, lw=2, edgecolor=LN, facecolor=GRAY2)
    ax.add_patch(c)
    ax.text(0, 0, "Requirements\nManagement", ha='center', va='center',
            fontsize=8, fontweight='bold')

    # Phases around the circle
    phases = [
        ("Preliminary", 90),
        ("A: Architecture\nVision", 45),
        ("B: Business\nArchitecture", 0),
        ("C: Information\nSystems Arch.", -45),
        ("D: Technology\nArchitecture", -90),
        ("E: Opportunities\n& Solutions", -135),
        ("F: Migration\nPlanning", 180),
        ("G: Implementation\nGovernance", 135),
    ]
    # H: Architecture Change Management between G and Preliminary
    # Put it at ~112 degrees

    R = 8  # radius of phase placement
    box_w = 4.5
    box_h = 2.2

    for i, (label, angle_deg) in enumerate(phases):
        angle = np.radians(angle_deg)
        cx = R * np.cos(angle)
        cy = R * np.sin(angle)

        fill = GRAY1 if i % 2 == 0 else GRAY4
        rect = FancyBboxPatch((cx - box_w/2, cy - box_h/2), box_w, box_h,
                              boxstyle="round,pad=0.2", lw=1.5,
                              edgecolor=LN, facecolor=fill)
        ax.add_patch(rect)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=7,
                fontweight='bold')

        # Arrow from this phase toward center (representing link to Requirements)
        inner_r = 2.8
        ix = inner_r * np.cos(angle)
        iy = inner_r * np.sin(angle)
        outer_r = R - box_w/2 - 0.3
        ox = outer_r * np.cos(angle)
        oy = outer_r * np.sin(angle)
        # Dashed line to center
        draw_line(ax, ix, iy, ox * 0.75, oy * 0.75, lw=0.6, ls='--')

    # Curved arrows between successive phases (outer ring)
    for i in range(len(phases)):
        a1 = np.radians(phases[i][1])
        a2 = np.radians(phases[(i + 1) % len(phases)][1])

        # Midpoint arc arrow
        mid_angle = (a1 + a2) / 2
        if phases[i][1] < phases[(i + 1) % len(phases)][1]:
            mid_angle += np.pi  # handle wrap
        ar = R + 0.3
        mx = ar * np.cos(mid_angle)
        my = ar * np.sin(mid_angle)

        # Simple arrow from phase i endpoint to phase i+1 start
        r_arr = R
        # arrow a bit outside the boxes
        src_angle = a1 - np.radians(18)
        dst_angle = a2 + np.radians(18)
        sx = (R + 2.8) * np.cos(src_angle)
        sy = (R + 2.8) * np.sin(src_angle)
        dx = (R + 2.8) * np.cos(dst_angle)
        dy = (R + 2.8) * np.sin(dst_angle)

        ax.annotate("", xy=(dx, dy), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='->', color=LN, lw=1,
                                   connectionstyle="arc3,rad=0.3"))

    # Legend note
    ax.text(0, -11.5, "Cykl iteracyjny: ka\u017cda faza mo\u017ce wraca\u0107 do wcze\u015bniejszych.\n"
            "Requirements Management w centrum \u2014 wp\u0142ywa na ka\u017cd\u0105 faz\u0119.",
            ha='center', va='center', fontsize=7, fontstyle='italic')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'togaf_adm.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK TOGAF ADM")


# =========================================================================
# 2. 4+1 View Model  (Kruchten)
# =========================================================================
def generate_4plus1():
    fig, ax = plt.subplots(figsize=(8.27, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 65)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    ax.set_title("4+1 View Model (Kruchten, 1995)",
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    cx, cy = 50, 32
    # Center: Scenarios (+1)
    cw, ch = 18, 8
    draw_box(ax, cx - cw/2, cy - ch/2, cw, ch, "+1\nScenarios\n(Use Cases)",
             fill=GRAY2, lw=2, fontsize=9, fontweight='bold', rounded=True)

    # 4 views around
    views = [
        ("Logical View\n(Funkcjonalno\u015b\u0107:\nklasy, modu\u0142y)", cx, cy + 18, "Programista"),
        ("Process View\n(Wsp\u00f3\u0142bie\u017cno\u015b\u0107,\nprzep\u0142yw danych)", cx + 28, cy, "Integrator"),
        ("Development View\n(Organizacja kodu:\npakiety, warstwy)", cx, cy - 18, "Developer"),
        ("Physical View\n(Wdro\u017cenie:\nserwery, kontenery)", cx - 28, cy, "Admin/DevOps"),
    ]

    bw, bh = 22, 10
    for label, vx, vy, stakeholder in views:
        draw_box(ax, vx - bw/2, vy - bh/2, bw, bh, label,
                 fill=GRAY1, lw=1.5, fontsize=8, fontweight='bold', rounded=True)
        # Label stakeholder below/beside
        if vy > cy:
            ax.text(vx, vy + bh/2 + 1.5, f"\u2190 {stakeholder}", fontsize=7,
                    ha='center', fontstyle='italic')
        elif vy < cy:
            ax.text(vx, vy - bh/2 - 1.5, f"\u2190 {stakeholder}", fontsize=7,
                    ha='center', fontstyle='italic')
        elif vx > cx:
            ax.text(vx + bw/2 + 1, vy, f"\u2190 {stakeholder}", fontsize=7,
                    va='center', fontstyle='italic')
        else:
            ax.text(vx - bw/2 - 1, vy, f"{stakeholder} \u2192", fontsize=7,
                    va='center', ha='right', fontstyle='italic')

        # Arrow from view to center
        # Calculate direction
        dx = cx - vx
        dy = cy - vy
        dist = np.sqrt(dx**2 + dy**2)
        ndx, ndy = dx/dist, dy/dist
        # Start from edge of view box, end at edge of center box
        sx = vx + ndx * (bw/2 + 0.5) if abs(dx) > abs(dy) else vx + ndx * 2
        sy = vy + ndy * (bh/2 + 0.5) if abs(dy) > abs(dx) else vy + ndy * 2
        ex = cx - ndx * (cw/2 + 0.5) if abs(dx) > abs(dy) else cx - ndx * 2
        ey = cy - ndy * (ch/2 + 0.5) if abs(dy) > abs(dx) else cy - ndy * 2

        draw_arrow(ax, sx, sy, ex, ey, lw=1.2)

    # Note
    ax.text(50, 2, "Ka\u017cdy widok odpowiada innemu interesariuszowi.\n"
            "Scenarios (\u0142\u0105cz\u0105cy +1) weryfikuj\u0105 sp\u00f3jno\u015b\u0107 4 widok\u00f3w.",
            ha='center', fontsize=7, fontstyle='italic')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, '4plus1_view_model.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK 4+1 View Model")


# =========================================================================
# 3. C4 Model — 4 Zoom Levels
# =========================================================================
def generate_c4():
    fig, axes = plt.subplots(2, 2, figsize=(8.27, 10))
    fig.patch.set_facecolor(BG)
    fig.suptitle("C4 Model (Simon Brown) \u2014 4 poziomy zoomu",
                 fontsize=FS_TITLE, fontweight='bold', y=0.98)

    titles = [
        "Level 1: System Context",
        "Level 2: Container",
        "Level 3: Component",
        "Level 4: Code (UML)"
    ]

    for idx, ax_item in enumerate(axes.flat):
        ax_item.set_xlim(0, 100)
        ax_item.set_ylim(0, 80)
        ax_item.set_aspect('equal')
        ax_item.axis('off')
        ax_item.set_title(titles[idx], fontsize=10, fontweight='bold', pad=8)

    # --- Level 1: System Context ---
    ax1 = axes[0, 0]
    # Person
    ax1.add_patch(plt.Circle((20, 55), 4, lw=1.5, edgecolor=LN, facecolor=GRAY1))
    # Head (smaller circle on top)
    ax1.add_patch(plt.Circle((20, 57.5), 1.5, lw=1.2, edgecolor=LN, facecolor='white'))
    # Body (lines)
    draw_line(ax1, 20, 56, 20, 52.5, lw=1.2)
    draw_line(ax1, 17, 55, 23, 55, lw=1.2)
    ax1.text(20, 48, "Klient", ha='center', fontsize=8, fontweight='bold')

    # System
    draw_box(ax1, 38, 43, 24, 18, "System\nE-commerce", fill=GRAY2, lw=2,
             fontsize=9, fontweight='bold', rounded=True)

    # External
    draw_box(ax1, 72, 48, 20, 12, "System\nP\u0142atno\u015bci\n(zewn.)",
             fill=GRAY4, lw=1.5, fontsize=7, rounded=True)
    ax1.add_patch(plt.Rectangle((72, 48), 20, 12, lw=1.5, edgecolor=LN,
                                facecolor='none', linestyle='--'))

    draw_arrow(ax1, 24, 54, 38, 54)
    ax1.text(31, 56, "sk\u0142ada\nzam\u00f3wienia", fontsize=6, ha='center')
    draw_arrow(ax1, 62, 54, 72, 54)
    ax1.text(67, 56, "API", fontsize=6, ha='center')

    ax1.text(50, 20, "Kto u\u017cywa systemu?\nZ czym si\u0119 integruje?",
             ha='center', fontsize=7, fontstyle='italic',
             bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=LN, lw=0.5))

    # --- Level 2: Container ---
    ax2 = axes[0, 1]
    # Big system boundary
    ax2.add_patch(plt.Rectangle((5, 15), 90, 58, lw=1.5, edgecolor=LN,
                                facecolor='none', linestyle='--'))
    ax2.text(50, 75, "System E-commerce", ha='center', fontsize=8,
             fontweight='bold', fontstyle='italic')

    containers = [
        ("SPA\n(React)", 15, 50, 18, 12, GRAY1),
        ("API\nServer\n(Node.js)", 42, 50, 18, 12, GRAY2),
        ("Database\n(PostgreSQL)", 70, 50, 18, 12, GRAY3),
        ("Worker\n(Python)", 42, 25, 18, 12, GRAY1),
    ]
    for label, x, y, w, h, fill in containers:
        draw_box(ax2, x, y, w, h, label, fill=fill, lw=1.5, fontsize=7,
                 fontweight='bold', rounded=True)

    draw_arrow(ax2, 33, 56, 42, 56)
    ax2.text(37.5, 58, "REST", fontsize=6, ha='center')
    draw_arrow(ax2, 60, 56, 70, 56)
    ax2.text(65, 58, "SQL", fontsize=6, ha='center')
    draw_arrow(ax2, 51, 50, 51, 37)
    ax2.text(53, 44, "async", fontsize=6)

    ax2.text(50, 8, "Jakie kontenery techniczne\nsk\u0142adaj\u0105 si\u0119 na system?",
             ha='center', fontsize=7, fontstyle='italic',
             bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=LN, lw=0.5))

    # --- Level 3: Component ---
    ax3 = axes[1, 0]
    ax3.add_patch(plt.Rectangle((5, 15), 90, 58, lw=1.5, edgecolor=LN,
                                facecolor='none', linestyle='--'))
    ax3.text(50, 75, "API Server (Node.js)", ha='center', fontsize=8,
             fontweight='bold', fontstyle='italic')

    components = [
        ("OrderController", 10, 50, 22, 10, GRAY1),
        ("AuthService", 40, 50, 22, 10, GRAY2),
        ("PaymentGateway\n(adapter)", 70, 50, 22, 10, GRAY1),
        ("OrderRepository", 25, 25, 22, 10, GRAY2),
        ("NotificationService", 57, 25, 22, 10, GRAY1),
    ]
    for label, x, y, w, h, fill in components:
        draw_box(ax3, x, y, w, h, label, fill=fill, lw=1.5, fontsize=6.5,
                 fontweight='bold', rounded=True)

    draw_arrow(ax3, 32, 55, 40, 55)
    draw_arrow(ax3, 62, 55, 70, 55)
    draw_arrow(ax3, 21, 50, 30, 35)
    draw_arrow(ax3, 51, 50, 62, 35)

    ax3.text(50, 8, "Jakie modu\u0142y/komponenty\nwewn\u0105trz kontenera?",
             ha='center', fontsize=7, fontstyle='italic',
             bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=LN, lw=0.5))

    # --- Level 4: Code ---
    ax4 = axes[1, 1]
    # UML-style class boxes
    def draw_class(ax, x, y, name, attrs, methods, w=28, fill=GRAY1):
        h_name = 6
        h_attr = len(attrs) * 4 + 2
        h_meth = len(methods) * 4 + 2
        h_total = h_name + h_attr + h_meth
        # Name
        ax.add_patch(plt.Rectangle((x, y), w, h_total, lw=1.5,
                                   edgecolor=LN, facecolor=fill))
        ax.plot([x, x+w], [y + h_total - h_name, y + h_total - h_name],
                color=LN, lw=1)
        ax.text(x + w/2, y + h_total - h_name/2, name, ha='center', va='center',
                fontsize=7, fontweight='bold')
        # Attrs
        ax.plot([x, x+w], [y + h_meth, y + h_meth], color=LN, lw=1)
        for i, a in enumerate(attrs):
            ax.text(x + 2, y + h_total - h_name - 2 - i*4, a,
                    fontsize=6, va='top', family='monospace')
        # Methods
        for i, m in enumerate(methods):
            ax.text(x + 2, y + h_meth - 2 - i*4, m,
                    fontsize=6, va='top', family='monospace')

    draw_class(ax4, 5, 40, "\u00abinterface\u00bb\nIOrderRepository",
               [], ["+save(order)", "+findById(id)"], w=32, fill=GRAY4)
    draw_class(ax4, 55, 40, "OrderRepository",
               ["-db: Database"], ["+save(order)", "+findById(id)"], w=32, fill=GRAY1)
    draw_class(ax4, 30, 10, "Order",
               ["-id: UUID", "-items: List", "-total: Money"],
               ["+addItem(item)", "+calculateTotal()"], w=32, fill=GRAY2)

    # Implements arrow (dashed)
    ax4.annotate("", xy=(37, 46), xytext=(55, 50),
                 arrowprops=dict(arrowstyle='-|>', color=LN, lw=1.2, linestyle='--'))
    ax4.text(46, 52, "\u00abimplements\u00bb", fontsize=6, ha='center', fontstyle='italic')

    # Dependency
    draw_arrow(ax4, 71, 40, 50, 24)
    ax4.text(64, 32, "uses", fontsize=6, fontstyle='italic')

    ax4.text(50, 3, "Diagramy klas UML\n(opcjonalny poziom szczeg\u00f3\u0142owo\u015bci)",
             ha='center', fontsize=7, fontstyle='italic',
             bbox=dict(boxstyle='round', facecolor=GRAY4, edgecolor=LN, lw=0.5))

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(OUTPUT_DIR, 'c4_model.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK C4 Model")


# =========================================================================
# 4. Zachman Framework Grid
# =========================================================================
def generate_zachman():
    fig, ax = plt.subplots(figsize=(8.27, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 65)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    ax.set_title("Zachman Framework \u2014 taksonomia architektury",
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    rows = ["Kontekst\n(Planner)", "Konceptualny\n(Owner)", "Logiczny\n(Designer)",
            "Fizyczny\n(Builder)", "Szczeg\u00f3\u0142owy\n(Subcontractor)"]
    cols = ["Co?\n(dane)", "Jak?\n(funkcje)", "Gdzie?\n(sie\u0107)", "Kto?\n(ludzie)",
            "Kiedy?\n(czas)", "Dlaczego?\n(cel)"]

    n_rows = len(rows)
    n_cols = len(cols)

    x0 = 18
    y0 = 5
    cw = 12.5  # cell width
    ch = 9     # cell height
    rh_label = 14  # row label width

    # Column headers
    for j, col in enumerate(cols):
        x = x0 + j * cw
        draw_box(ax, x, y0 + n_rows * ch, cw, 7, col, fill=GRAY2, lw=1.5,
                 fontsize=6.5, fontweight='bold')

    # Row headers
    for i, row in enumerate(rows):
        y = y0 + (n_rows - 1 - i) * ch
        draw_box(ax, x0 - rh_label, y, rh_label, ch, row, fill=GRAY2, lw=1.5,
                 fontsize=6.5, fontweight='bold')

    # Cells
    fills = [GRAY4, 'white']
    for i in range(n_rows):
        for j in range(n_cols):
            x = x0 + j * cw
            y = y0 + (n_rows - 1 - i) * ch
            fill = fills[(i + j) % 2]
            ax.add_patch(plt.Rectangle((x, y), cw, ch, lw=0.8,
                                       edgecolor=LN, facecolor=fill))

    # Sample content in a few cells
    examples = {
        (0, 0): "Lista\nencji",
        (0, 1): "Lista\nproces\u00f3w",
        (0, 2): "Lokalizacje",
        (1, 0): "Model\npoj\u0119ciowy",
        (1, 1): "Model\nproces\u00f3w",
        (2, 0): "ERD",
        (2, 1): "Data Flow",
        (3, 0): "Schemat\nDB",
        (3, 1): "Kod\nprogramu",
        (0, 3): "Role",
        (1, 3): "Org chart",
        (0, 4): "Harmonogram",
        (0, 5): "Cele\nbiznesowe",
    }
    for (i, j), text in examples.items():
        x = x0 + j * cw
        y = y0 + (n_rows - 1 - i) * ch
        ax.text(x + cw/2, y + ch/2, text, ha='center', va='center',
                fontsize=5.5, fontstyle='italic', color='#444444')

    # Note
    ax.text(50, 1, "Ka\u017cda kom\u00f3rka = artefakt opisuj\u0105cy system z danej perspektywy i aspektu.\n"
            "Zachman nie m\u00f3wi JAK modelowa\u0107 \u2014 m\u00f3wi CO nale\u017cy udokumentowa\u0107.",
            ha='center', fontsize=7, fontstyle='italic')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'zachman_framework.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK Zachman Framework")


# =========================================================================
# 5. ArchiMate Layers
# =========================================================================
def generate_archimate():
    fig, ax = plt.subplots(figsize=(8.27, 9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    ax.set_title("ArchiMate \u2014 3 warstwy \u00d7 3 aspekty",
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Column headers (aspects)
    headers = [
        ("Active Structure\n(KTO?)", 0),
        ("Behavior\n(CO robi?)", 1),
        ("Passive Structure\n(NA CZYM?)", 2),
    ]

    x0 = 10
    y0 = 10
    cw = 26
    ch = 20
    gap = 1
    header_h = 8
    row_label_w = 14

    # Column headers
    for label, j in headers:
        x = x0 + row_label_w + j * (cw + gap)
        draw_box(ax, x, y0 + 3 * (ch + gap), cw, header_h, label,
                 fill=GRAY3, lw=1.5, fontsize=8, fontweight='bold')

    # Layers (rows)
    layers = [
        ("Business\nLayer", GRAY1, [
            ("Business\nActor", "Business\nProcess", "Business\nObject"),
            ("(Kto wykonuje?)", "(Co si\u0119 dzieje?)", "(Na czym dzia\u0142a?)"),
            ("np. Klient,\nHandlowiec", "np. Obs\u0142uga\nzam\u00f3wienia", "np. Zam\u00f3wienie,\nFaktura"),
        ]),
        ("Application\nLayer", GRAY4, [
            ("Application\nComponent", "Application\nService", "Data\nObject"),
            ("(Jaki modu\u0142?)", "(Jaka us\u0142uga?)", "(Jakie dane?)"),
            ("np. CRM,\nERP", "np. API\nzam\u00f3wie\u0144", "np. tabela\nOrders"),
        ]),
        ("Technology\nLayer", 'white', [
            ("Node /\nDevice", "Infrastructure\nService", "Artifact"),
            ("(Jaki sprz\u0119t?)", "(Jaka infra?)", "(Jaki plik?)"),
            ("np. Serwer\nLinux, K8s", "np. Load\nBalancer", "np. .jar,\n.war, image"),
        ]),
    ]

    for i, (layer_name, fill, cells) in enumerate(layers):
        y = y0 + (2 - i) * (ch + gap)

        # Row label
        draw_box(ax, x0, y, row_label_w, ch, layer_name,
                 fill=GRAY2, lw=1.5, fontsize=8, fontweight='bold')

        for j in range(3):
            x = x0 + row_label_w + j * (cw + gap)
            ax.add_patch(plt.Rectangle((x, y), cw, ch, lw=1.5,
                                       edgecolor=LN, facecolor=fill))
            # Element name (bold)
            ax.text(x + cw/2, y + ch - 3, cells[0][j], ha='center', va='top',
                    fontsize=7, fontweight='bold')
            # Role description
            ax.text(x + cw/2, y + ch/2, cells[1][j], ha='center', va='center',
                    fontsize=6, fontstyle='italic', color='#555555')
            # Example
            ax.text(x + cw/2, y + 3, cells[2][j], ha='center', va='bottom',
                    fontsize=6, color='#333333')

    # Vertical arrows between layers
    for j in range(3):
        x = x0 + row_label_w + j * (cw + gap) + cw/2
        for i in range(2):
            y_top = y0 + (2 - i) * (ch + gap)
            y_bot = y0 + (2 - i - 1) * (ch + gap) + ch
            draw_arrow(ax, x, y_top, x, y_bot + 0.3, lw=1)

    # Arrow labels
    mid_x = x0 + row_label_w - 3
    ax.text(mid_x, y0 + 2 * (ch + gap) - gap/2,
            "realizacja \u2193", fontsize=6, ha='right', va='center',
            fontstyle='italic', rotation=90)
    ax.text(mid_x, y0 + 1 * (ch + gap) - gap/2,
            "realizacja \u2193", fontsize=6, ha='right', va='center',
            fontstyle='italic', rotation=90)

    # Note
    ax.text(50, 4, "Warstwy czytamy z g\u00f3ry (biznes) na d\u00f3\u0142 (technologia).\n"
            "Ni\u017csze warstwy REALIZUJ\u0104 wy\u017csze. "
            "ArchiMate jest komplementarny z TOGAF.",
            ha='center', fontsize=7, fontstyle='italic')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'archimate_layers.png'),
                dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print("  OK ArchiMate")


# =========================================================================
if __name__ == '__main__':
    print(f"Generating architecture diagrams to {OUTPUT_DIR}/...")
    generate_togaf_adm()
    generate_4plus1()
    generate_c4()
    generate_zachman()
    generate_archimate()
    print(f"\nAll diagrams saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if 'togaf' in f or '4plus1' in f or 'c4' in f or 'zachman' in f or 'archimate' in f:
            size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
            print(f"  {f} ({size_kb:.0f} KB)")
