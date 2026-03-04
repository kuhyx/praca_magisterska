#!/usr/bin/env python3
"""
Generate supplementary diagrams for PYTANIE 9 'Budowa procesu' and 'Budowa wątku'.
Replaces ASCII art with monochrome A4-printable PNGs (300 DPI).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
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


# ============================================================
# 1. Memory layout with C code annotations
# ============================================================
def gen_memory_c_annotated():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Segmenty pamięci procesu — mapowanie kodu C',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Left side: memory segments stack
    seg_x = 1.0
    seg_w = 2.8
    seg_h = 0.95
    gap = 0.08

    segments = [
        ('STACK ↓', GRAY1, 'rośnie w dół'),
        ('...', 'white', 'wolna przestrzeń'),
        ('HEAP ↑', GRAY4, 'rośnie w górę'),
        ('BSS', GRAY2, 'zerowane'),
        ('DATA', GRAY3, 'zainicjalizowane'),
        ('TEXT', GRAY5, 'read-only'),
    ]

    seg_positions = {}
    top_y = 7.0
    for i, (name, color, note) in enumerate(segments):
        y = top_y - i * (seg_h + gap)
        draw_box(ax, seg_x, y, seg_w, seg_h, name, fill=color,
                 fontsize=FS_LABEL, fontweight='bold', rounded=False)
        ax.text(seg_x + seg_w + 0.15, y + seg_h / 2, note,
                fontsize=FS_SMALL, va='center', style='italic', color='#555')
        seg_positions[name.split()[0].replace('↓', '').replace('↑', '').strip()] = y + seg_h / 2

    # Address labels
    ax.text(seg_x - 0.15, top_y + seg_h / 2, 'wysoki\nadres',
            fontsize=FS_SMALL, va='center', ha='right', style='italic')
    ax.text(seg_x - 0.15, seg_positions['TEXT'], 'niski\nadres',
            fontsize=FS_SMALL, va='center', ha='right', style='italic')

    # Right side: C code with arrows pointing to segments
    code_x = 6.5
    code_lines = [
        ('int global_init = 42;', 'DATA', '→ DATA'),
        ('int global_uninit;', 'BSS', '→ BSS'),
        ('', None, ''),
        ('int main() {', 'TEXT', '→ TEXT'),
        ('    int local = 10;', 'STACK', '→ STACK'),
        ('    int *p = malloc(100);', 'HEAP', '  p → STACK\n  100B → HEAP'),
        ('    free(p);', None, ''),
        ('    return 0;', None, ''),
        ('}', None, ''),
    ]

    # Code box background
    code_top = 7.2
    code_line_h = 0.55
    total_code_h = len(code_lines) * code_line_h + 0.3
    rect = mpatches.FancyBboxPatch((code_x - 0.3, code_top - total_code_h),
                                    5.5, total_code_h,
                                    boxstyle="round,pad=0.1",
                                    lw=1.2, edgecolor=GRAY3, facecolor=GRAY4)
    ax.add_patch(rect)
    ax.text(code_x + 2.2, code_top + 0.15, 'Kod C — przykład',
            fontsize=FS, fontweight='bold', ha='center')

    for i, (line, seg, annotation) in enumerate(code_lines):
        y = code_top - (i + 1) * code_line_h
        ax.text(code_x, y, line, fontsize=7, va='center', family='monospace')

        if seg and seg in seg_positions:
            # Draw arrow from annotation to segment
            ann_x = code_x + 4.0
            seg_y = seg_positions[seg]
            ax.text(ann_x, y, annotation.split('\n')[0], fontsize=FS_SMALL,
                    va='center', fontweight='bold', color='#333')
            # Connecting line (dashed)
            ax.plot([seg_x + seg_w, ann_x - 0.1], [seg_y, y],
                    linestyle=':', color=GRAY3, lw=0.8)

    save_fig(fig, 'q9_memory_c_annotated.png')


# ============================================================
# 2. PCB detailed with concrete values
# ============================================================
def gen_pcb_detailed():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('PCB (Process Control Block) — dowód osobisty procesu',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # PCB outer box
    pcb_x, pcb_y, pcb_w, pcb_h = 1.0, 0.8, 8.0, 5.5
    rect = mpatches.FancyBboxPatch((pcb_x, pcb_y), pcb_w, pcb_h,
                                    boxstyle="round,pad=0.15",
                                    lw=2, edgecolor=LN, facecolor='white')
    ax.add_patch(rect)
    ax.text(pcb_x + pcb_w / 2, pcb_y + pcb_h + 0.15, 'PCB procesu PID=1234',
            fontsize=FS_LABEL, fontweight='bold', ha='center')

    fields = [
        ('PID', '1234', 'identyfikator procesu'),
        ('Stan', 'RUNNING', 'aktualny stan wykonania'),
        ('PC', '0x004015A0', 'następna instrukcja do wykonania'),
        ('Rejestry CPU', 'EAX=5, EBX=0, ESP=...', 'stan procesora'),
        ('Tablice stron', '[strona→ramka]', 'mapowanie pamięci wirtualnej'),
        ('Otwarte pliki', 'fd0, fd1, fd2, ...', 'deskryptory plików'),
        ('Priorytet', '20 (nice)', 'klasa schedulingu'),
        ('Czas CPU', '1.34 s', 'accounting / statystyki'),
    ]

    row_h = 0.55
    top_y = pcb_y + pcb_h - 0.4
    field_w = 2.3
    val_w = 3.0
    desc_x = pcb_x + field_w + val_w + 0.6

    for i, (field, value, desc) in enumerate(fields):
        y = top_y - i * (row_h + 0.05)
        # Field name box
        draw_box(ax, pcb_x + 0.3, y, field_w, row_h, field,
                 fill=GRAY2, fontsize=FS, fontweight='bold', rounded=False)
        # Value box
        draw_box(ax, pcb_x + 0.3 + field_w, y, val_w, row_h, value,
                 fill=GRAY4, fontsize=7.5, rounded=False)
        # Description
        ax.text(desc_x, y + row_h / 2, desc,
                fontsize=FS_SMALL, va='center', style='italic', color='#555')

    # Bottom note
    ax.text(5.0, 0.35, 'Context switch = zapisz PCB starego procesu → wczytaj PCB nowego',
            fontsize=FS, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.25', facecolor=GRAY4, edgecolor=GRAY3))

    save_fig(fig, 'q9_pcb_detailed.png')


# ============================================================
# 3. Process states with ALL transition labels
# ============================================================
def gen_process_states_labeled():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(-0.5, 6)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Stany procesu — diagram przejść z opisami',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    states = {
        'NEW':        (0.8,  3.0),
        'READY':      (3.8,  3.0),
        'RUNNING':    (7.3,  3.0),
        'BLOCKED':    (7.3,  0.5),
        'TERMINATED': (11.0, 3.0),
    }
    fills = {
        'NEW': GRAY4, 'READY': GRAY1, 'RUNNING': GRAY3,
        'BLOCKED': GRAY2, 'TERMINATED': GRAY5,
    }
    bw, bh = 2.0, 1.0

    for name, (x, y) in states.items():
        draw_box(ax, x, y, bw, bh, name, fill=fills[name], fontsize=FS_LABEL,
                 fontweight='bold')

    # Transition: NEW → READY
    sx, sy = states['NEW']
    dx, dy = states['READY']
    draw_arrow(ax, sx + bw, sy + bh/2, dx, dy + bh/2, lw=1.5)
    ax.text((sx + bw + dx) / 2, sy + bh/2 + 0.2, 'admit\n(utworzony)',
            fontsize=FS_SMALL, ha='center', va='bottom')

    # Transition: READY → RUNNING (dispatch)
    sx, sy = states['READY']
    dx, dy = states['RUNNING']
    draw_arrow(ax, sx + bw, sy + bh * 0.65, dx, dy + bh * 0.65, lw=1.5)
    ax.text((sx + bw + dx) / 2, sy + bh * 0.65 + 0.2, 'dispatch\n(scheduler → CPU)',
            fontsize=FS_SMALL, ha='center', va='bottom')

    # Transition: RUNNING → READY (preemption)
    draw_arrow(ax, dx, dy + bh * 0.35, sx + bw, sy + bh * 0.35, lw=1.5)
    ax.text((sx + bw + dx) / 2, sy + bh * 0.35 - 0.15, 'preempt\n(kwant czasu)',
            fontsize=FS_SMALL, ha='center', va='top')

    # Transition: RUNNING → TERMINATED
    sx, sy = states['RUNNING']
    dx, dy = states['TERMINATED']
    draw_arrow(ax, sx + bw, sy + bh/2, dx, dy + bh/2, lw=1.5)
    ax.text((sx + bw + dx) / 2, sy + bh/2 + 0.2, 'exit()',
            fontsize=FS_SMALL, ha='center', va='bottom')

    # Transition: RUNNING → BLOCKED
    sx, sy = states['RUNNING']
    dx, dy = states['BLOCKED']
    draw_arrow(ax, sx + bw/2, sy, dx + bw/2, dy + bh, lw=1.5)
    ax.text(sx + bw + 0.2, (sy + dy + bh) / 2, 'I/O wait\n(np. read z dysku)',
            fontsize=FS_SMALL, ha='left', va='center')

    # Transition: BLOCKED → READY
    bx, by = states['BLOCKED']
    rx, ry = states['READY']
    ax.annotate("", xy=(rx + bw/2, ry), xytext=(bx, by + bh/2),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN,
                                connectionstyle='arc3,rad=0.35'))
    ax.text(4.0, 1.0, 'I/O done\n(powrót do kolejki)',
            fontsize=FS_SMALL, ha='center')

    # Legend at bottom
    legend_items = [
        'NEW → READY: proces utworzony, gotowy',
        'READY → RUNNING: scheduler przydziela CPU',
        'RUNNING → READY: upłynął kwant czasu (preemption)',
        'RUNNING → BLOCKED: czeka na I/O',
        'BLOCKED → READY: I/O zakończone',
        'RUNNING → TERMINATED: proces kończy się',
    ]
    for i, item in enumerate(legend_items):
        col = i // 3
        row = i % 3
        ax.text(0.5 + col * 6.5, -0.1 - row * 0.35, f'• {item}',
                fontsize=FS_SMALL, va='center')

    save_fig(fig, 'q9_process_states_labeled.png')


# ============================================================
# 4. Thread shared vs private — annotated diagram
# ============================================================
def gen_thread_shared_private():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Wątki wewnątrz procesu — współdzielone vs prywatne',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Outer process box
    proc_rect = mpatches.FancyBboxPatch((0.5, 0.3), 11.0, 7.0,
                                         boxstyle="round,pad=0.15",
                                         lw=2.5, edgecolor=LN, facecolor='white')
    ax.add_patch(proc_rect)
    ax.text(6.0, 7.55, 'PROCES (PID = 1234)', fontsize=FS_LABEL,
            fontweight='bold', ha='center')

    # Shared region (top)
    shared_rect = mpatches.Rectangle((1.0, 4.5), 10.0, 2.5,
                                      lw=1.5, edgecolor=LN, facecolor=GRAY1)
    ax.add_patch(shared_rect)
    ax.text(6.0, 6.75, 'WSPÓŁDZIELONE (wszystkie wątki widzą to samo)',
            fontsize=FS, fontweight='bold', ha='center')

    shared_items = [
        ('TEXT', 'kod programu'),
        ('DATA', 'zm. globalne\nzainicjalizowane'),
        ('BSS', 'zm. globalne\nniezainicjalizowane'),
        ('HEAP', 'malloc/new\n(dynamiczna)'),
        ('Pliki', 'deskryptory\nfd[0..n]'),
        ('PID', 'identyfikator\nprocesu'),
    ]
    for i, (name, desc) in enumerate(shared_items):
        x = 1.4 + i * 1.6
        draw_box(ax, x, 4.7, 1.3, 0.7, name, fill=GRAY3,
                 fontsize=FS, fontweight='bold', rounded=False)
        ax.text(x + 0.65, 5.6, desc, fontsize=5.5, ha='center', va='center')

    # Private region (bottom) — 3 threads
    private_rect = mpatches.Rectangle((1.0, 0.6), 10.0, 3.5,
                                       lw=1.5, edgecolor=LN, facecolor='white',
                                       linestyle='--')
    ax.add_patch(private_rect)
    ax.text(6.0, 3.85, 'PRYWATNE (każdy wątek ma WŁASNE)',
            fontsize=FS, fontweight='bold', ha='center')

    thread_colors = [GRAY4, '#E0E0E0', GRAY4]
    for t in range(3):
        tx = 1.5 + t * 3.3
        tw = 2.8
        thread_rect = mpatches.FancyBboxPatch((tx, 0.8), tw, 2.7,
                                               boxstyle="round,pad=0.1",
                                               lw=1.5, edgecolor=LN,
                                               facecolor=thread_colors[t])
        ax.add_patch(thread_rect)
        tid = t + 1
        ax.text(tx + tw/2, 3.25, f'Wątek {tid} (TID={40+tid})',
                fontsize=FS, fontweight='bold', ha='center')

        private_items = [
            (f'Stos_{tid}', 'zmienne lokalne'),
            (f'Rejestry_{tid}', 'EAX, EBX, ESP...'),
            (f'PC_{tid}', 'pozycja w kodzie'),
        ]
        for j, (name, desc) in enumerate(private_items):
            y = 2.65 - j * 0.6
            draw_box(ax, tx + 0.15, y, tw - 0.3, 0.45, f'{name}',
                     fill='white', fontsize=7, fontweight='bold', rounded=False)
            ax.text(tx + tw/2, y - 0.1, desc, fontsize=5.5, ha='center',
                    va='top', color='#555')

    save_fig(fig, 'q9_thread_shared_private.png')


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Generating supplementary PYTANIE 9 'Budowa' diagrams...")
    gen_memory_c_annotated()
    gen_pcb_detailed()
    gen_process_states_labeled()
    gen_thread_shared_private()
    print("\nAll 4 supplementary diagrams generated!")
