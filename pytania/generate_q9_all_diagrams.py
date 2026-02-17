#!/usr/bin/env python3
"""
Generate ALL diagrams for PYTANIE 9: Procesy i wątki (SOI).
Replaces every ASCII diagram with a monochrome A4-printable PNG (300 DPI).
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


def draw_double_arrow(ax, x1, y1, x2, y2, lw=1.2, color=LN):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='<->', color=color, lw=lw))


def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG, pad_inches=0.15)
    plt.close(fig)
    print(f"  Saved: {path}")


def draw_table(ax, headers, rows, x0, y0, col_widths, row_h=0.4,
               header_fill=GRAY2, row_fills=None, fontsize=FS, header_fontsize=None):
    """Draw a clean table on axes."""
    if header_fontsize is None:
        header_fontsize = fontsize
    n_cols = len(headers)
    n_rows = len(rows)
    total_w = sum(col_widths)

    # Header
    cx = x0
    for j, hdr in enumerate(headers):
        draw_box(ax, cx, y0, col_widths[j], row_h, hdr, fill=header_fill,
                 fontsize=header_fontsize, fontweight='bold', rounded=False)
        cx += col_widths[j]

    # Rows
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
# 1. Process vs Thread comparison table
# ============================================================
def gen_process_vs_thread():
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(-4.5, 1.5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Proces vs Wątek — porównanie', fontsize=FS_TITLE, fontweight='bold', pad=10)

    headers = ['Cecha', 'Proces', 'Wątek']
    col_w = [2.5, 3.5, 3.5]
    rows = [
        ['Pamięć', 'Własna, izolowana', 'Współdzielona (heap)'],
        ['Tworzenie', '~1–10 ms', '~10–100 μs (100× szybciej)'],
        ['Przełączanie', '~1–5 μs (TLB flush)', '~0.1–0.5 μs (10×)'],
        ['Komunikacja', 'IPC (pipe, socket, shm)', 'Bezpośrednia (wspólna pam.)'],
        ['Izolacja', 'Pełna — awaria izolowana', 'Brak — może zabić proces'],
        ['Zastosowanie', 'Bezpieczeństwo, izolacja', 'Wydajność, współdzielenie'],
    ]
    draw_table(ax, headers, rows, x0=0.25, y0=0.8, col_widths=col_w, row_h=0.55,
               fontsize=7.5, header_fontsize=FS_LABEL)

    # Analogy at bottom
    ax.text(5.0, -4.2, 'Analogia:  Proces = mieszkanie (własny adres)     '
            'Wątek = pokój w mieszkaniu (wspólna kuchnia = heap)',
            ha='center', fontsize=FS, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    save_fig(fig, 'q9_process_vs_thread.png')


# ============================================================
# 2. Memory segments layout
# ============================================================
def gen_memory_layout():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Segmenty pamięci procesu', fontsize=FS_TITLE, fontweight='bold', pad=10)

    segments = [
        ('STACK ↓', 'zmienne lokalne, adresy\npowrotu (każdy wątek WŁASNY)', GRAY1),
        ('...', '(wolna przestrzeń)', 'white'),
        ('HEAP ↑', 'malloc/new — dynamiczna\nalokacja (współdzielony)', GRAY4),
        ('BSS', 'zmienne globalne\nniezainicjalizowane (zerowane)', GRAY2),
        ('DATA', 'zmienne globalne\nzainicjalizowane', GRAY3),
        ('TEXT', 'kod maszynowy\n(read-only, współdzielony)', GRAY5),
    ]
    bx, bw = 2.0, 2.5
    seg_h = 0.9
    gap = 0.05
    top_y = 7.0

    for i, (name, desc, color) in enumerate(segments):
        y = top_y - i * (seg_h + gap)
        draw_box(ax, bx, y, bw, seg_h, name, fill=color, fontsize=FS_LABEL,
                 fontweight='bold', rounded=False)
        ax.text(bx + bw + 0.3, y + seg_h / 2, desc, fontsize=7.5, va='center')

    # Address labels
    ax.text(bx - 0.2, top_y + seg_h / 2, 'wysoki\nadres', fontsize=FS_SMALL,
            va='center', ha='right', style='italic')
    bottom_y = top_y - 5 * (seg_h + gap)
    ax.text(bx - 0.2, bottom_y + seg_h / 2, 'niski\nadres', fontsize=FS_SMALL,
            va='center', ha='right', style='italic')

    # Arrows for growth
    ax.annotate('', xy=(bx - 0.5, top_y - 0.1), xytext=(bx - 0.5, top_y + seg_h + 0.1),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(bx - 0.9, top_y + 0.4, 'rośnie\nw dół', fontsize=FS_SMALL, ha='center')

    heap_y = top_y - 2 * (seg_h + gap)
    ax.annotate('', xy=(bx - 0.5, heap_y + seg_h + 0.1), xytext=(bx - 0.5, heap_y - 0.1),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(bx - 0.9, heap_y + 0.5, 'rośnie\nw górę', fontsize=FS_SMALL, ha='center')

    save_fig(fig, 'q9_memory_layout.png')


# ============================================================
# 3. Process states diagram
# ============================================================
def gen_process_states():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Stany procesu — diagram przejść', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    states = {
        'NEW':        (1.0, 2.5),
        'READY':      (3.5, 2.5),
        'RUNNING':    (6.5, 2.5),
        'BLOCKED':    (6.5, 0.5),
        'TERMINATED': (10.0, 2.5),
    }
    fills = {
        'NEW': GRAY4, 'READY': GRAY1, 'RUNNING': GRAY3,
        'BLOCKED': GRAY2, 'TERMINATED': GRAY5,
    }
    bw, bh = 1.8, 0.9
    for name, (x, y) in states.items():
        draw_box(ax, x, y, bw, bh, name, fill=fills[name], fontsize=FS_LABEL,
                 fontweight='bold')

    # Transitions
    transitions = [
        ('NEW', 'READY', 'admit'),
        ('READY', 'RUNNING', 'dispatch\n(scheduler)'),
        ('RUNNING', 'TERMINATED', 'exit'),
        ('RUNNING', 'BLOCKED', 'I/O wait'),
    ]
    for src, dst, label in transitions:
        sx, sy = states[src]
        dx, dy = states[dst]
        if sy == dy:  # horizontal
            draw_arrow(ax, sx + bw, sy + bh/2, dx, dy + bh/2, lw=1.5)
            mx = (sx + bw + dx) / 2
            ax.text(mx, sy + bh/2 + 0.25, label, fontsize=FS_SMALL,
                    ha='center', va='bottom')
        else:  # vertical
            draw_arrow(ax, sx + bw/2, sy, dx + bw/2, dy + bh, lw=1.5)
            ax.text(sx + bw + 0.2, (sy + dy + bh) / 2, label,
                    fontsize=FS_SMALL, ha='left', va='center')

    # BLOCKED → READY
    bx, by = states['BLOCKED']
    rx, ry = states['READY']
    ax.annotate("", xy=(rx + bw/2, ry), xytext=(bx - 0.3, by + bh/2),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN,
                                connectionstyle='arc3,rad=0.3'))
    ax.text(3.5, 0.7, 'I/O done', fontsize=FS_SMALL, ha='center')

    # RUNNING → READY (preemption)
    rux, ruy = states['RUNNING']
    draw_arrow(ax, rux, ruy + bh, rx + bw, ry + bh, lw=1.2)
    ax.text(5.0, 3.7, 'preempt /\ntimeout', fontsize=FS_SMALL, ha='center')

    save_fig(fig, 'q9_process_states.png')


# ============================================================
# 4. Thread structure within process
# ============================================================
def gen_thread_structure():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Wątki wewnątrz procesu (PID=42)', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    # Shared memory region
    draw_box(ax, 0.5, 3.5, 9.0, 1.8, '', fill=GRAY1, rounded=False, lw=2)
    ax.text(5.0, 5.0, 'WSPÓŁDZIELONE', fontsize=FS, fontweight='bold', ha='center')

    labels_shared = ['TEXT', 'DATA', 'BSS', 'HEAP', 'pliki', 'PID']
    for i, lab in enumerate(labels_shared):
        x = 1.0 + i * 1.4
        draw_box(ax, x, 3.8, 1.1, 0.6, lab, fill=GRAY3, fontsize=FS,
                 fontweight='bold', rounded=False)
        ax.text(x + 0.55, 4.6, lab, fontsize=FS_SMALL, ha='center', color='#555555')

    # Per-thread regions
    draw_box(ax, 0.5, 0.5, 9.0, 2.7, '', fill='white', rounded=False, lw=2,
             linestyle='--')
    ax.text(5.0, 2.95, 'PRYWATNE (każdy wątek)', fontsize=FS, fontweight='bold',
            ha='center')

    for i in range(3):
        x = 1.0 + i * 3.0
        tid = i + 1
        draw_box(ax, x, 0.7, 2.3, 2.0, '', fill=GRAY4, rounded=False)
        ax.text(x + 1.15, 2.4, f'Wątek {tid}', fontsize=FS_LABEL,
                fontweight='bold', ha='center')
        items = [f'stos_{tid}', f'rejestry_{tid}', f'PC_{tid}', f'TID={40+tid}']
        for j, item in enumerate(items):
            ax.text(x + 1.15, 2.0 - j * 0.35, item, fontsize=FS_SMALL,
                    ha='center', family='monospace')

    save_fig(fig, 'q9_thread_structure.png')


# ============================================================
# 5. PCB structure
# ============================================================
def gen_pcb_structure():
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5.5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('PCB (Process Control Block)', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    fields = [
        ('PID', '42'),
        ('Stan', 'READY / RUNNING / BLOCKED'),
        ('Rejestry CPU', 'EAX, EBX, ESP, EIP ...'),
        ('Tablice stron', 'mapowanie wirtualne → fizyczne'),
        ('Otwarte pliki', 'fd[0], fd[1], fd[2] ...'),
        ('Priorytety', 'nice value, scheduling class'),
        ('Statystyki', 'CPU time, I/O count'),
    ]

    top_y = 4.8
    for i, (field, value) in enumerate(fields):
        y = top_y - i * 0.55
        draw_box(ax, 0.5, y, 2.2, 0.45, field, fill=GRAY2, fontsize=FS,
                 fontweight='bold', rounded=False)
        draw_box(ax, 2.7, y, 4.5, 0.45, value, fill=GRAY4, fontsize=FS,
                 rounded=False)

    ax.text(4.0, 0.3, 'Context switch = zapisz PCB starego → wczytaj PCB nowego',
            fontsize=FS_SMALL, ha='center', style='italic')

    save_fig(fig, 'q9_pcb_structure.png')


# ============================================================
# 6. Speed comparison
# ============================================================
def gen_speed_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    fig.suptitle('Szybkość — procesy vs wątki (benchmarki Linux)',
                 fontsize=FS_TITLE, fontweight='bold')

    # Left: creation
    ax = axes[0]
    ops = ['fork()\n(nowy proces)', 'pthread_create()\n(nowy wątek)']
    times = [3.0, 0.05]  # ms
    colors = [GRAY3, GRAY1]
    bars = ax.barh(ops, times, color=colors, edgecolor=LN, height=0.5, linewidth=1.2)
    ax.set_xlabel('Czas [ms]', fontsize=FS)
    ax.set_title('Tworzenie', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xlim(0, 4.5)
    for bar, t in zip(bars, times):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f'{t} ms', va='center', fontsize=FS)
    ax.text(2.5, -0.6, '~100× szybciej', fontsize=FS, ha='center',
            fontweight='bold', transform=ax.get_xaxis_transform())
    ax.tick_params(labelsize=FS)

    # Right: context switch
    ax = axes[1]
    ops2 = ['Proces→Proces\n(TLB flush)', 'Wątek→Wątek\n(TLB warm)']
    times2 = [3000, 300]  # ns
    bars2 = ax.barh(ops2, times2, color=colors, edgecolor=LN, height=0.5, linewidth=1.2)
    ax.set_xlabel('Czas [ns]', fontsize=FS)
    ax.set_title('Przełączanie kontekstu', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xlim(0, 4500)
    for bar, t in zip(bars2, times2):
        ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
                f'{t} ns', va='center', fontsize=FS)
    ax.text(2500, -0.6, '~10× szybciej', fontsize=FS, ha='center',
            fontweight='bold', transform=ax.get_xaxis_transform())
    ax.tick_params(labelsize=FS)

    fig.tight_layout(rect=[0, 0.05, 1, 0.92])
    save_fig(fig, 'q9_speed_comparison.png')


# ============================================================
# 7. Scenario table (when to use process vs thread)
# ============================================================
def gen_scenario_table():
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(-5.5, 1)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Kiedy proces, kiedy wątek? — typowe scenariusze',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    headers = ['Scenariusz', 'Wybór', 'Dlaczego?']
    col_w = [3.5, 2.5, 4.5]
    rows = [
        ['Serwer WWW (Apache)', 'Proces', 'izolacja klientów'],
        ['Serwer WWW (nginx)', 'Wątek / async', 'szybkość, cooperacja'],
        ['Przeglądarka (karty)', 'Proces', 'crash isolation'],
        ['Przeglądarka (JS+render)', 'Wątek', 'współdzielony DOM'],
        ['Gra (fizyka+rendering)', 'Wątek', 'współdzielony świat gry'],
        ['Kompilacja (make -j8)', 'Proces', 'izolacja, prostota'],
        ['Baza danych (zapytania)', 'Wątek', 'współdzielony cache'],
        ['Microservices', 'Proces (kontener)', 'izolacja, deployment'],
    ]
    draw_table(ax, headers, rows, x0=0.25, y0=0.5, col_widths=col_w,
               row_h=0.5, fontsize=7)

    save_fig(fig, 'q9_scenario_table.png')


# ============================================================
# 8. IPC details: pipe, shared memory, socket (3-panel)
# ============================================================
def gen_ipc_details():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
    fig.suptitle('Mechanizmy IPC — szczegóły', fontsize=FS_TITLE, fontweight='bold')

    # Panel 1: Pipe
    ax = axes[0]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Pipe (potok)', fontsize=FS_LABEL, fontweight='bold')

    draw_box(ax, 0.2, 2.0, 1.8, 1.2, 'Proces A\n(ls)\nstdout', fill=GRAY1,
             fontsize=FS)
    draw_box(ax, 3.0, 2.0, 1.8, 1.2, 'Bufor\njądra\n(4 KB)', fill=GRAY2,
             fontsize=FS, fontweight='bold')
    draw_box(ax, 5.8, 2.0, 1.8, 1.2, 'Proces B\n(grep)\nstdin', fill=GRAY1,
             fontsize=FS)
    draw_arrow(ax, 2.0, 2.6, 3.0, 2.6, lw=1.5)
    ax.text(2.5, 3.0, 'write()\nfd[1]', fontsize=FS_SMALL, ha='center')
    draw_arrow(ax, 4.8, 2.6, 5.8, 2.6, lw=1.5)
    ax.text(5.3, 3.0, 'read()\nfd[0]', fontsize=FS_SMALL, ha='center')
    ax.text(4.0, 0.8, 'Jednokierunkowy\nBufor pełny → write() blokuje',
            fontsize=FS_SMALL, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    # Panel 2: Shared Memory
    ax = axes[1]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Shared Memory', fontsize=FS_LABEL, fontweight='bold')

    draw_box(ax, 0.3, 3.0, 2.2, 1.2, 'Proces A\nstrona 7', fill=GRAY1, fontsize=FS)
    draw_box(ax, 5.5, 3.0, 2.2, 1.2, 'Proces B\nstrona 3', fill=GRAY1, fontsize=FS)
    draw_box(ax, 2.8, 1.0, 2.4, 1.2, 'RAM\nramka 42', fill=GRAY3, fontsize=FS,
             fontweight='bold')
    draw_arrow(ax, 2.0, 3.0, 3.5, 2.2, lw=1.5)
    draw_arrow(ax, 6.0, 3.0, 4.5, 2.2, lw=1.5)
    ax.text(4.0, 0.3, 'Zero kopiowania!\nA pisze → B widzi od razu\n'
            'Wymaga synchronizacji (semafor)',
            fontsize=FS_SMALL, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    # Panel 3: Socket
    ax = axes[2]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Socket', fontsize=FS_LABEL, fontweight='bold')

    # Network socket
    draw_box(ax, 0.3, 3.2, 1.8, 0.9, 'Klient', fill=GRAY1, fontsize=FS, fontweight='bold')
    draw_box(ax, 5.5, 3.2, 1.8, 0.9, 'Serwer', fill=GRAY1, fontsize=FS, fontweight='bold')
    draw_double_arrow(ax, 2.1, 3.65, 5.5, 3.65, lw=1.5)
    ax.text(3.8, 4.3, 'TCP/IP (sieciowy)', fontsize=FS, ha='center', fontweight='bold')

    # Unix socket
    draw_box(ax, 0.3, 1.3, 1.8, 0.9, 'Proces A', fill=GRAY4, fontsize=FS, fontweight='bold')
    draw_box(ax, 5.5, 1.3, 1.8, 0.9, 'Proces B', fill=GRAY4, fontsize=FS, fontweight='bold')
    draw_double_arrow(ax, 2.1, 1.75, 5.5, 1.75, lw=1.5)
    ax.text(3.8, 2.4, 'Unix domain socket\n(/tmp/app.sock)', fontsize=FS,
            ha='center', fontweight='bold')

    ax.text(3.8, 0.5, 'Dwukierunkowy\nNajbardziej uniwersalny IPC',
            fontsize=FS_SMALL, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    fig.tight_layout(rect=[0, 0, 1, 0.9])
    save_fig(fig, 'q9_ipc_details.png')


# ============================================================
# 9. IPC comparison table
# ============================================================
def gen_ipc_table():
    fig, ax = plt.subplots(figsize=(8.5, 3.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(-4.5, 1)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Porównanie mechanizmów IPC', fontsize=FS_TITLE, fontweight='bold', pad=10)

    headers = ['Mechanizm', 'Kierunek', 'Szybkość', 'Zastosowanie']
    col_w = [2.5, 2.0, 2.5, 3.5]
    rows = [
        ['Pipe', 'jednokierunkowy', 'średnia', 'ls | grep'],
        ['Named Pipe', 'jednokierunkowy', 'średnia', 'demon → klient'],
        ['Shared Memory', 'dwukierunkowy', 'NAJSZYBSZA', 'video, bazy danych'],
        ['Message Queue', 'dwukierunkowy', 'średnia', 'wieloproducentowe'],
        ['Socket', 'dwukierunkowy', 'wolna (sieć)', 'klient-serwer'],
        ['Signal', 'jednokierunkowy', 'natychmiastowa', 'powiadomienia (nr)'],
    ]
    draw_table(ax, headers, rows, x0=0.25, y0=0.5, col_widths=col_w,
               row_h=0.5, fontsize=7.5)

    save_fig(fig, 'q9_ipc_table.png')


# ============================================================
# 10. Race condition (simple x + bank timeline)
# ============================================================
def gen_race_condition():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle('Wyścig (Race Condition) — przykłady', fontsize=FS_TITLE,
                 fontweight='bold')

    # Panel 1: simple x increment
    ax = axes[0]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Prosty wyścig: x = x + 1', fontsize=FS_LABEL, fontweight='bold')

    # Timeline
    steps_a = ['czytaj x (=0)', 'dodaj 1', 'zapisz x (=1)']
    steps_b = ['czytaj x (=0)', 'dodaj 1', 'zapisz x (=1)']
    ax.text(2.0, 6.3, 'Wątek A', fontsize=FS_LABEL, ha='center', fontweight='bold')
    ax.text(6.0, 6.3, 'Wątek B', fontsize=FS_LABEL, ha='center', fontweight='bold')
    ax.plot([2, 2], [0.8, 6.0], color=LN, lw=1)
    ax.plot([6, 6], [0.8, 6.0], color=LN, lw=1)

    for i, (sa, sb) in enumerate(zip(steps_a, steps_b)):
        y = 5.3 - i * 1.2
        draw_box(ax, 0.5, y, 3.0, 0.6, sa, fill=GRAY4, fontsize=FS)
        draw_box(ax, 4.5, y - 0.3, 3.0, 0.6, sb, fill=GRAY1, fontsize=FS)

    ax.text(4.0, 0.4, 'Wynik: x = 1  (powinno 2!)',
            fontsize=FS, ha='center', fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round', facecolor='#F8D7DA', edgecolor='#C62828'))

    # Panel 2: bank account
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Konto bankowe: saldo = 1000 zł', fontsize=FS_LABEL, fontweight='bold')

    ax.text(2.5, 6.3, 'Wątek A (+500)', fontsize=FS, ha='center', fontweight='bold')
    ax.text(7.5, 6.3, 'Wątek B (−200)', fontsize=FS, ha='center', fontweight='bold')
    ax.plot([2.5, 2.5], [0.8, 6.0], color=LN, lw=1)
    ax.plot([7.5, 7.5], [0.8, 6.0], color=LN, lw=1)

    events = [
        ('t1', 'czytaj → 1000', '', 5.3),
        ('t2', '', 'czytaj → 1000', 4.6),
        ('t3', '1000+500=1500', '', 3.9),
        ('t4', '', '1000−200=800', 3.2),
        ('t5', 'zapisz 1500', '', 2.5),
        ('t6', '', 'zapisz 800 ✗', 1.8),
    ]
    for t, a, b, y in events:
        ax.text(0.3, y + 0.15, t, fontsize=FS_SMALL, fontweight='bold', va='center')
        if a:
            draw_box(ax, 1.0, y, 3.0, 0.45, a, fill=GRAY4, fontsize=FS_SMALL)
        if b:
            fill = '#F8D7DA' if '✗' in b else GRAY1
            draw_box(ax, 6.0, y, 3.0, 0.45, b, fill=fill, fontsize=FS_SMALL)

    ax.text(5.0, 0.4, 'Wynik: 800 zł  (powinno 1300!)',
            fontsize=FS, ha='center', fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round', facecolor='#F8D7DA', edgecolor='#C62828'))

    fig.tight_layout(rect=[0, 0, 1, 0.9])
    save_fig(fig, 'q9_race_condition.png')


# ============================================================
# 11. Deadlock scenario + cycle
# ============================================================
def gen_deadlock_scenario():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle('Zakleszczenie (Deadlock)', fontsize=FS_TITLE, fontweight='bold')

    # Panel 1: timeline
    ax = axes[0]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Scenariusz z 2 mutexami', fontsize=FS_LABEL, fontweight='bold')

    ax.text(2.5, 5.3, 'Wątek A', fontsize=FS_LABEL, ha='center', fontweight='bold')
    ax.text(6.0, 5.3, 'Wątek B', fontsize=FS_LABEL, ha='center', fontweight='bold')

    steps = [
        ('lock(mutex1) OK', '', 'trzyma', False, 4.5),
        ('', 'lock(mutex2) OK', 'trzyma', False, 3.7),
        ('lock(mutex2) ...WAIT', '', 'CZEKA!', True, 2.9),
        ('', 'lock(mutex1) ...WAIT', 'CZEKA!', True, 2.1),
    ]
    for a_text, b_text, note, is_wait, y in steps:
        if a_text:
            fill = '#F8D7DA' if is_wait else GRAY4
            draw_box(ax, 0.5, y, 3.3, 0.55, a_text, fill=fill, fontsize=FS_SMALL)
        if b_text:
            fill = '#F8D7DA' if is_wait else GRAY4
            draw_box(ax, 4.3, y, 3.3, 0.55, b_text, fill=fill, fontsize=FS_SMALL)

    ax.text(4.0, 1.2, 'DEADLOCK!\nŻaden nie odpuści',
            fontsize=FS, ha='center', fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round', facecolor='#F8D7DA', edgecolor='#C62828'))

    # Panel 2: cycle diagram
    ax = axes[1]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Cykl oczekiwania', fontsize=FS_LABEL, fontweight='bold')

    # Thread boxes
    draw_box(ax, 0.5, 3.5, 2.2, 1.2, 'Wątek A\ntrzyma Mutex 1', fill=GRAY1,
             fontsize=FS, fontweight='bold')
    draw_box(ax, 5.3, 3.5, 2.2, 1.2, 'Wątek B\ntrzyma Mutex 2', fill=GRAY1,
             fontsize=FS, fontweight='bold')

    # Mutex boxes
    draw_box(ax, 0.5, 1.0, 2.2, 1.0, 'Mutex 1', fill=GRAY3, fontsize=FS,
             fontweight='bold')
    draw_box(ax, 5.3, 1.0, 2.2, 1.0, 'Mutex 2', fill=GRAY3, fontsize=FS,
             fontweight='bold')

    # holds arrows (down)
    draw_arrow(ax, 1.6, 3.5, 1.6, 2.0, lw=2)
    ax.text(0.9, 2.7, 'trzyma', fontsize=FS_SMALL, rotation=90, va='center')
    draw_arrow(ax, 6.4, 3.5, 6.4, 2.0, lw=2)
    ax.text(7.0, 2.7, 'trzyma', fontsize=FS_SMALL, rotation=90, va='center')

    # waits-for arrows (across, red)
    draw_arrow(ax, 2.7, 4.3, 5.3, 4.3, lw=2.5, color='#C62828')
    ax.text(4.0, 4.7, 'czeka na Mutex 2', fontsize=FS_SMALL, ha='center',
            fontweight='bold', color='#C62828')
    draw_arrow(ax, 5.3, 3.7, 2.7, 3.7, lw=2.5, color='#C62828')
    ax.text(4.0, 3.1, 'czeka na Mutex 1', fontsize=FS_SMALL, ha='center',
            fontweight='bold', color='#C62828')

    fig.tight_layout(rect=[0, 0, 1, 0.9])
    save_fig(fig, 'q9_deadlock_scenario.png')


# ============================================================
# 12. Coffman conditions + prevention strategies
# ============================================================
def gen_coffman_strategies():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(-3.5, 1)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Warunki Coffmana — zapobieganie deadlockowi',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    headers = ['Warunek', 'Opis', 'Jak złamać', 'Przykład']
    col_w = [2.5, 2.5, 3.0, 3.0]
    rows = [
        ['1. Mutual Exclusion', 'zasób wyłączny', 'współdzielony zasób', 'Read-write lock'],
        ['2. Hold and Wait', 'trzymaj + czekaj', 'bierz WSZYSTKIE naraz', 'lock(m1,m2) atomowo'],
        ['3. No Preemption', 'nie zabierzesz siłą', 'timeout / trylock', 'pthread_mutex_trylock()'],
        ['4. Circular Wait', 'cykliczne oczekiw.', 'porządek liniowy', 'zawsze m1 przed m2'],
    ]
    draw_table(ax, headers, rows, x0=0.25, y0=0.5, col_widths=col_w,
               row_h=0.6, fontsize=7)

    ax.text(5.75, -3.1, '▸ Najczęstsza strategia: PORZĄDEK LINIOWY — '
            'numeruj mutexy, zawsze blokuj rosnąco',
            fontsize=FS, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    save_fig(fig, 'q9_coffman_strategies.png')


# ============================================================
# 13. Starvation + Priority Inversion (2-panel)
# ============================================================
def gen_starvation_priority():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle('Zagłodzenie i Inwersja priorytetów', fontsize=FS_TITLE,
                 fontweight='bold')

    # Panel 1: Starvation + aging
    ax = axes[0]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Zagłodzenie (Starvation)', fontsize=FS_LABEL, fontweight='bold')

    threads = [
        ('Wątek HIGH', 'prio=10', GRAY5, 3.0),
        ('Wątek HIGH', 'prio=9', GRAY3, 2.2),
        ('Wątek MED', 'prio=5', GRAY2, 1.4),
        ('Wątek LOW', 'prio=1 → głoduje!', '#F8D7DA', 0.6),
    ]
    for name, prio, color, y in threads:
        draw_box(ax, 0.5, y, 2.0, 0.6, name, fill=color, fontsize=FS_SMALL,
                 fontweight='bold')
        ax.text(2.8, y + 0.3, prio, fontsize=FS_SMALL, va='center')

    ax.text(1.5, 4.2, 'CPU zawsze\ndostaje HIGH!', fontsize=FS,
            ha='center', fontweight='bold')
    draw_arrow(ax, 1.5, 3.9, 1.5, 3.65, lw=1.5)

    # Aging solution
    draw_box(ax, 4.5, 1.5, 3.2, 2.5, '', fill=GRAY4, rounded=True)
    ax.text(6.1, 3.7, 'Rozwiązanie: AGING', fontsize=FS, fontweight='bold', ha='center')
    aging = ['t=0:    prio=1', 't=100ms: prio=2', 't=200ms: prio=3', '...', 'w końcu → CPU!']
    for i, line in enumerate(aging):
        ax.text(6.1, 3.2 - i * 0.4, line, fontsize=FS_SMALL, ha='center',
                family='monospace')

    # Panel 2: Priority Inversion
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Inwersja priorytetów', fontsize=FS_LABEL, fontweight='bold')

    # Timeline
    labels = ['H (wysoki)', 'M (średni)', 'L (niski)']
    ys = [4.2, 2.8, 1.4]
    for label, y in zip(labels, ys):
        ax.text(0.3, y + 0.2, label, fontsize=FS, fontweight='bold', va='center')

    # L runs and locks mutex
    draw_box(ax, 2.0, ys[2], 1.2, 0.5, 'lock(m)', fill=GRAY1, fontsize=FS_SMALL)

    # M preempts L
    draw_box(ax, 3.5, ys[1], 3.0, 0.5, 'M pracuje...', fill=GRAY3, fontsize=FS_SMALL)

    # H waits for mutex
    draw_box(ax, 3.5, ys[0], 3.0, 0.5, 'CZEKA na mutex!', fill='#F8D7DA',
             fontsize=FS_SMALL, fontweight='bold')

    # M finishes, L continues, unlocks
    draw_box(ax, 6.8, ys[2], 1.5, 0.5, 'unlock(m)', fill=GRAY1, fontsize=FS_SMALL)
    draw_box(ax, 8.5, ys[0], 1.2, 0.5, 'H runs', fill=GRAY4, fontsize=FS_SMALL)

    # Explanation
    ax.text(5.0, 0.5, 'H czeka na M (mimo H > M)!\n'
            'Rozwiązanie: Priority Inheritance\n'
            'L dziedziczy priorytet H → M nie wypycha L',
            fontsize=FS_SMALL, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    ax.text(5.0, 0.0, 'Mars Pathfinder (1997) — klasyczny bug!',
            fontsize=FS_SMALL, ha='center', fontweight='bold')

    fig.tight_layout(rect=[0, 0, 1, 0.9])
    save_fig(fig, 'q9_starvation_priority.png')


# ============================================================
# 14. Bounded buffer + readers-writers + philosophers
# ============================================================
def gen_classic_problems():
    fig, axes = plt.subplots(1, 3, figsize=(12, 5))
    fig.suptitle('Klasyczne problemy synchronizacji', fontsize=FS_TITLE,
                 fontweight='bold')

    # Panel 1: Bounded Buffer with semaphores
    ax = axes[0]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Producent-Konsument\n(Bounded Buffer, N=4)', fontsize=FS,
                 fontweight='bold')

    draw_box(ax, 0.2, 4.0, 2.0, 1.2, 'Producent\nP(empty)\nP(mutex)\nwstaw()\nV(mutex)\nV(full)',
             fill=GRAY1, fontsize=5.5)
    # Buffer
    items = ['A', 'B', '', '']
    for i, item in enumerate(items):
        x = 2.8 + i * 0.9
        fill = GRAY3 if item else 'white'
        draw_box(ax, x, 4.3, 0.9, 0.7, item, fill=fill, fontsize=FS,
                 fontweight='bold', rounded=False)
    ax.text(4.6, 5.2, 'Bufor (N=4)', fontsize=FS_SMALL, ha='center',
            fontweight='bold')
    draw_box(ax, 6.0, 4.0, 2.0, 1.2, 'Konsument\nP(full)\nP(mutex)\npobierz()\nV(mutex)\nV(empty)',
             fill=GRAY4, fontsize=5.5)
    draw_arrow(ax, 2.2, 4.6, 2.8, 4.65, lw=1.2)
    draw_arrow(ax, 6.4, 4.65, 6.0, 4.6, lw=1.2)

    # Semaphores
    sems = [('mutex = 1', GRAY2), ('empty = N', GRAY1), ('full = 0', GRAY3)]
    for i, (s, c) in enumerate(sems):
        draw_box(ax, 2.0, 2.5 - i * 0.6, 4.0, 0.45, s, fill=c, fontsize=FS_SMALL,
                 fontweight='bold')

    ax.text(4.0, 0.5, 'KOLEJNOŚĆ: P(empty/full)\nPRZED P(mutex)!\nOdwrotnie = DEADLOCK',
            fontsize=5.5, ha='center', fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round', facecolor='#F8D7DA', edgecolor='#C62828'))

    # Panel 2: Readers-Writers
    ax = axes[1]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Czytelnicy-Pisarze\n(Readers-Writers)', fontsize=FS,
                 fontweight='bold')

    # Resource
    draw_box(ax, 2.5, 3.5, 3.0, 1.5, 'Dane\n(współdzielone)', fill=GRAY2,
             fontsize=FS, fontweight='bold')

    # Readers
    for i in range(3):
        x = 0.3 + i * 1.0
        draw_box(ax, x, 5.5, 0.8, 0.7, f'R{i+1}', fill=GRAY4, fontsize=FS,
                 fontweight='bold')
        draw_arrow(ax, x + 0.4, 5.5, 3.0 + i * 0.5, 5.0, lw=1)

    ax.text(1.5, 6.5, 'Czytelnicy (wielu naraz)', fontsize=FS_SMALL,
            ha='center', fontweight='bold')

    # Writer
    draw_box(ax, 5.5, 5.5, 1.5, 0.7, 'Pisarz', fill=GRAY5, fontsize=FS,
             fontweight='bold')
    draw_arrow(ax, 6.25, 5.5, 5.0, 5.0, lw=1.5)
    ax.text(6.25, 6.5, 'WYŁĄCZNY', fontsize=FS_SMALL, ha='center',
            fontweight='bold', color='#C62828')

    # Rules
    rules = ['Wielu czytelników = OK', 'Jeden pisarz = wyłączny',
             'Czytelnik + Pisarz = ✗', 'Problem: pisarze głodują']
    for i, r in enumerate(rules):
        ax.text(4.0, 2.5 - i * 0.45, r, fontsize=FS_SMALL, ha='center')

    ax.text(4.0, 0.5, 'Rozwiązanie:\nrw_mutex + count_mutex\n+ zmienna readers',
            fontsize=5.5, ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    # Panel 3: Dining Philosophers
    ax = axes[2]
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Ucztujący filozofowie\n(Dining Philosophers)', fontsize=FS,
                 fontweight='bold')

    # Draw circular table
    cx, cy, r = 4.0, 3.8, 1.8
    table = plt.Circle((cx, cy), 0.8, fill=True, facecolor=GRAY2,
                        edgecolor=LN, lw=1.5)
    ax.add_patch(table)
    ax.text(cx, cy, 'Stół', fontsize=FS, ha='center', fontweight='bold')

    # 5 philosophers around table
    for i in range(5):
        angle = np.pi/2 + i * 2 * np.pi / 5
        px = cx + r * np.cos(angle)
        py = cy + r * np.sin(angle)
        circle = plt.Circle((px, py), 0.35, fill=True, facecolor=GRAY1,
                            edgecolor=LN, lw=1.2)
        ax.add_patch(circle)
        ax.text(px, py, f'F{i}', ha='center', va='center', fontsize=FS,
                fontweight='bold')

        # Fork between philosophers
        fork_angle = np.pi/2 + (i + 0.5) * 2 * np.pi / 5
        fx = cx + (r * 0.6) * np.cos(fork_angle)
        fy = cy + (r * 0.6) * np.sin(fork_angle)
        ax.plot([fx - 0.1, fx + 0.1], [fy - 0.15, fy + 0.15], color=LN,
                lw=2.5, solid_capstyle='round')
        ax.text(fx + 0.2, fy + 0.15, f'w{i}', fontsize=5, color='#555555')

    # Rules
    rules = ['Jedzenie = 2 widelce', 'Naiwne → DEADLOCK',
             'Fix: F4 bierze odwrotnie',
             'Alt: semafor(4)']
    for i, r in enumerate(rules):
        ax.text(4.0, 1.2 - i * 0.35, r, fontsize=FS_SMALL, ha='center')

    fig.tight_layout(rect=[0, 0, 1, 0.88])
    save_fig(fig, 'q9_classic_problems.png')


# ============================================================
# 15. Sync mechanisms comparison + mutex/sem/spinlock
# ============================================================
def gen_sync_comparison():
    fig, axes = plt.subplots(2, 1, figsize=(9, 7))

    # Top: comparison table
    ax = axes[0]
    ax.set_xlim(0, 11.5)
    ax.set_ylim(-5, 1)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Mechanizmy synchronizacji — porównanie', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    headers = ['Mechanizm', 'Opis', 'Kiedy używać']
    col_w = [2.5, 4.5, 4.0]
    rows = [
        ['Mutex', 'Zamek: 1 wątek w sekcji', 'Sekcja krytyczna'],
        ['Semafor(n)', 'Licznik: max n wątków', 'Ograniczone zasoby (n miejsc)'],
        ['Monitor', 'Obiekt z wbudowanym mutex', 'Java synchronized'],
        ['Cond. Variable', 'wait()/signal() na warunek', 'Producent-konsument'],
        ['Spinlock', 'Aktywne czekanie (busy-wait)', 'Bardzo krótkie sekcje (<1 μs)'],
        ['RW Lock', 'Wielu czytelników LUB 1 pisarz', 'Bazy danych, cache'],
        ['Barrier', 'Czekaj aż wszyscy dotrą', 'Obliczenia równoległe'],
    ]
    draw_table(ax, headers, rows, x0=0.25, y0=0.5, col_widths=col_w,
               row_h=0.5, fontsize=7)

    # Bottom: mutex vs semafor vs spinlock
    ax = axes[1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Mutex vs Semafor vs Spinlock', fontsize=FS_TITLE,
                 fontweight='bold', pad=5)

    # Mutex
    draw_box(ax, 0.3, 2.5, 3.5, 2.0, '', fill=GRAY4)
    ax.text(2.05, 4.2, 'MUTEX', fontsize=FS_LABEL, fontweight='bold', ha='center')
    ax.text(2.05, 3.6, '= klucz do łazienki\n(1 osoba)', fontsize=FS, ha='center')
    ax.text(2.05, 2.8, 'Wątek ZASYPIA gdy czeka\nOS go obudzi (~μs)', fontsize=FS_SMALL,
            ha='center', style='italic')

    # Semafor
    draw_box(ax, 4.3, 2.5, 3.5, 2.0, '', fill=GRAY1)
    ax.text(6.05, 4.2, 'SEMAFOR(n)', fontsize=FS_LABEL, fontweight='bold', ha='center')
    ax.text(6.05, 3.6, '= parking na n miejsc\n(n wątków naraz)', fontsize=FS, ha='center')
    ax.text(6.05, 2.8, 'Semafor(1) = mutex\nP() = zmniejsz, V() = zwiększ',
            fontsize=FS_SMALL, ha='center', style='italic')

    # Spinlock
    draw_box(ax, 8.3, 2.5, 3.5, 2.0, '', fill=GRAY2)
    ax.text(10.05, 4.2, 'SPINLOCK', fontsize=FS_LABEL, fontweight='bold', ha='center')
    ax.text(10.05, 3.6, '= obrotowe drzwi\n(kręcisz się w kółko)', fontsize=FS, ha='center')
    ax.text(10.05, 2.8, 'Wątek KRĘCI się w pętli\nLepszy gdy sekcja < 1 μs',
            fontsize=FS_SMALL, ha='center', style='italic')

    # Dividing rule
    ax.text(6.0, 1.5, 'Reguła kciuka:  sekcja > 1 μs → MUTEX  |  '
            'sekcja < 1 μs → SPINLOCK  |  n jednocześnie → SEMAFOR(n)',
            fontsize=FS, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    fig.tight_layout()
    save_fig(fig, 'q9_sync_comparison.png')


# ============================================================
# 16. Semaphore concept diagram
# ============================================================
def gen_semaphore_concept():
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Semafor — koncepcja (parking na 3 miejsca)', fontsize=FS_TITLE,
                 fontweight='bold', pad=10)

    # Parking slots
    for i in range(3):
        x = 2.0 + i * 2.0
        occupied = i < 2  # 2 occupied, 1 free
        fill = GRAY3 if occupied else 'white'
        label = f'Wątek {i+1}' if occupied else '(wolne)'
        draw_box(ax, x, 2.5, 1.5, 1.2, label, fill=fill, fontsize=FS,
                 fontweight='bold' if occupied else 'normal', rounded=False)

    ax.text(5.0, 4.2, 'semafor(3): counter = 1 (jedno wolne miejsce)',
            fontsize=FS, ha='center', fontweight='bold')

    # Waiting thread
    draw_box(ax, 0.2, 0.5, 1.5, 0.8, 'Wątek 4\nP() → czeka', fill='#F8D7DA',
             fontsize=FS_SMALL)
    draw_arrow(ax, 1.7, 0.9, 2.0, 2.5, lw=1.2, color='#C62828')

    ax.text(5.0, 0.6, 'P() = counter−−  (jeśli 0 → czekaj)\n'
            'V() = counter++  (obudź czekającego)',
            fontsize=FS, ha='center', family='monospace',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY3))

    save_fig(fig, 'q9_semaphore_concept.png')


# ============================================================
# MAIN — generate all
# ============================================================
if __name__ == '__main__':
    print("Generating ALL PYTANIE 9 diagrams...")
    gen_process_vs_thread()
    gen_memory_layout()
    gen_process_states()
    gen_thread_structure()
    gen_pcb_structure()
    gen_speed_comparison()
    gen_scenario_table()
    gen_ipc_details()
    gen_ipc_table()
    gen_race_condition()
    gen_deadlock_scenario()
    gen_coffman_strategies()
    gen_starvation_priority()
    gen_classic_problems()
    gen_sync_comparison()
    gen_semaphore_concept()
    print("\nAll 16 PYTANIE 9 diagrams generated successfully!")
