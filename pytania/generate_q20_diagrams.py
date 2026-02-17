#!/usr/bin/env python3
"""
Generate ALL diagrams for PYTANIE 20: Analityka danych strumieniowych.
Monochrome, A4-printable PNGs (300 DPI).
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
# 1. Batch vs Streaming concept
# ============================================================
def gen_batch_vs_streaming():
    fig, axes = plt.subplots(2, 1, figsize=(9, 5))
    fig.suptitle('Batch vs Streaming — dwa modele przetwarzania',
                 fontsize=FS_TITLE, fontweight='bold')

    # Batch
    ax = axes[0]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('BATCH (wsadowe)', fontsize=FS_LABEL, fontweight='bold')

    # Data collected
    draw_box(ax, 0.5, 0.8, 3.0, 1.4, 'Zbierz WSZYSTKIE\ndane\n(godziny / dni)',
             fill=GRAY1, fontsize=FS, fontweight='bold')
    draw_arrow(ax, 3.5, 1.5, 4.5, 1.5, lw=2)
    draw_box(ax, 4.5, 0.8, 2.5, 1.4, 'Analiza\n(batch job)',
             fill=GRAY2, fontsize=FS, fontweight='bold')
    draw_arrow(ax, 7.0, 1.5, 8.0, 1.5, lw=2)
    draw_box(ax, 8.0, 0.8, 2.5, 1.4, 'Wynik\n(jednorazowy)',
             fill=GRAY3, fontsize=FS, fontweight='bold')
    ax.text(11.0, 1.5, 'min-h', fontsize=FS, va='center', fontweight='bold')

    # Streaming
    ax = axes[1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('STREAMING (strumieniowe)', fontsize=FS_LABEL, fontweight='bold')

    # Events flowing
    events_x = [0.5, 1.5, 2.5, 3.5]
    for i, ex in enumerate(events_x):
        draw_box(ax, ex, 1.0, 0.8, 0.8, f'e{i+1}', fill=GRAY4,
                 fontsize=FS, fontweight='bold', rounded=False)
        if i < len(events_x) - 1:
            draw_arrow(ax, ex + 0.8, 1.4, ex + 1.0, 1.4, lw=1)

    ax.text(4.8, 1.4, '...', fontsize=FS_LABEL, va='center')
    draw_arrow(ax, 5.2, 1.4, 5.8, 1.4, lw=2)

    draw_box(ax, 5.8, 0.8, 2.8, 1.4, 'Analiza\nCIĄGŁA\n(event-by-event)',
             fill=GRAY2, fontsize=FS, fontweight='bold')
    draw_arrow(ax, 8.6, 1.5, 9.3, 1.5, lw=2)
    draw_box(ax, 9.3, 0.8, 2.0, 1.4, 'Wyniki\nciągłe',
             fill=GRAY3, fontsize=FS, fontweight='bold')
    ax.text(11.5, 0.5, 'ms-s', fontsize=FS, va='center', fontweight='bold')

    # Arrow marking infinity
    ax.annotate('', xy=(0.2, 1.4), xytext=(-0.3, 1.4),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(0.0, 2.3, '∞ zdarzeń', fontsize=FS_SMALL, ha='center', style='italic')

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save_fig(fig, 'q20_batch_vs_streaming.png')


# ============================================================
# 2. All 4 window types (TSSG)
# ============================================================
def gen_window_types():
    fig, axes = plt.subplots(4, 1, figsize=(9, 10))
    fig.suptitle('4 typy okien — TSSG', fontsize=FS_TITLE, fontweight='bold')

    # Events on a timeline (shared concept)
    events = list(range(1, 13))

    # --- Tumbling ---
    ax = axes[0]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Tumbling Window (okno przerzutne) — rozłączne, stały rozmiar',
                 fontsize=FS_LABEL, fontweight='bold')

    # Time axis
    ax.annotate('', xy=(13.5, 1.0), xytext=(0.3, 1.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(13.5, 0.6, 'czas', fontsize=FS_SMALL, ha='center')

    # Events
    for i, e in enumerate(events):
        x = 1.0 + i * 1.0
        ax.plot(x, 1.0, 'ko', markersize=5)
        ax.text(x, 0.5, f'e{e}', fontsize=FS_SMALL, ha='center')

    # Windows
    colors_w = [GRAY1, GRAY3, GRAY1, GRAY3]
    for w in range(4):
        x_start = 1.0 + w * 3.0 - 0.3
        rect = mpatches.FancyBboxPatch((x_start, 1.5), 3.0, 1.2,
                boxstyle="round,pad=0.1", facecolor=colors_w[w],
                edgecolor=LN, lw=1.5)
        ax.add_patch(rect)
        ax.text(x_start + 1.5, 2.1, f'Okno {w+1}', fontsize=FS,
                ha='center', fontweight='bold')
        # Braces down to events
        for j in range(3):
            ex = 1.0 + w * 3.0 + j * 1.0
            ax.plot([ex, ex], [1.0, 1.5], color=LN, lw=0.8, linestyle='--')

    ax.text(7.0, 3.2, 'Każde zdarzenie → DOKŁADNIE 1 okno. Zero nakładania.',
            fontsize=FS, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    # --- Sliding ---
    ax = axes[1]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Sliding Window (okno przesuwne) — nakładające, stały rozmiar + krok',
                 fontsize=FS_LABEL, fontweight='bold')

    ax.annotate('', xy=(13.5, 1.0), xytext=(0.3, 1.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(13.5, 0.6, 'czas', fontsize=FS_SMALL, ha='center')

    for i, e in enumerate(events[:8]):
        x = 1.0 + i * 1.0
        ax.plot(x, 1.0, 'ko', markersize=5)
        ax.text(x, 0.5, f'e{e}', fontsize=FS_SMALL, ha='center')

    # Sliding windows: size=4, slide=2
    slide_colors = [GRAY1, GRAY2, GRAY3]
    for w in range(3):
        x_start = 0.7 + w * 2.0
        y_base = 1.5 + w * 0.9
        rect = mpatches.FancyBboxPatch((x_start, y_base), 4.0, 0.7,
                boxstyle="round,pad=0.08", facecolor=slide_colors[w],
                edgecolor=LN, lw=1.5, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x_start + 2.0, y_base + 0.35, f'Okno {w+1} (size=4)',
                fontsize=FS_SMALL, ha='center', fontweight='bold')

    ax.text(10.5, 3.5, 'krok=2\nNakładanie!\ne3,e4 → w oknie 1 i 2',
            fontsize=FS, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    # --- Session ---
    ax = axes[2]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Session Window (okno sesji) — dynamiczny rozmiar, gap = przerwa',
                 fontsize=FS_LABEL, fontweight='bold')

    ax.annotate('', xy=(13.5, 1.0), xytext=(0.3, 1.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(13.5, 0.6, 'czas', fontsize=FS_SMALL, ha='center')

    # Cluster 1: events close together
    cluster1 = [1.0, 1.8, 2.3, 3.0]
    for x in cluster1:
        ax.plot(x, 1.0, 'ko', markersize=5)

    # Gap
    ax.annotate('', xy=(7.0, 0.7), xytext=(4.0, 0.7),
                arrowprops=dict(arrowstyle='<->', lw=1, color=LN))
    ax.text(5.5, 0.3, 'GAP > timeout', fontsize=FS, ha='center',
            fontweight='bold', style='italic')

    # Cluster 2
    cluster2 = [8.0, 8.8, 9.5]
    for x in cluster2:
        ax.plot(x, 1.0, 'ko', markersize=5)

    # Session boxes
    rect1 = mpatches.FancyBboxPatch((0.7, 1.4), 2.6, 1.0,
            boxstyle="round,pad=0.1", facecolor=GRAY1, edgecolor=LN, lw=1.5)
    ax.add_patch(rect1)
    ax.text(2.0, 1.9, 'Sesja 1\n(4 zdarzenia)', fontsize=FS, ha='center',
            fontweight='bold')

    rect2 = mpatches.FancyBboxPatch((7.7, 1.4), 2.1, 1.0,
            boxstyle="round,pad=0.1", facecolor=GRAY3, edgecolor=LN, lw=1.5)
    ax.add_patch(rect2)
    ax.text(8.75, 1.9, 'Sesja 2\n(3 zdarzenia)', fontsize=FS, ha='center',
            fontweight='bold')

    ax.text(5.5, 3.0, 'Nowa sesja po przerwie > gap',
            fontsize=FS, ha='center', style='italic')

    # --- Global ---
    ax = axes[3]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Global Window — jedno okno na cały strumień + trigger',
                 fontsize=FS_LABEL, fontweight='bold')

    ax.annotate('', xy=(13.5, 1.0), xytext=(0.3, 1.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(13.5, 0.6, 'czas', fontsize=FS_SMALL, ha='center')

    for i in range(12):
        x = 1.0 + i * 1.0
        ax.plot(x, 1.0, 'ko', markersize=5)

    # One big window
    rect = mpatches.FancyBboxPatch((0.5, 1.4), 12.5, 1.0,
            boxstyle="round,pad=0.1", facecolor=GRAY1, edgecolor=LN, lw=2)
    ax.add_patch(rect)
    ax.text(6.75, 1.9, 'GLOBAL WINDOW (cały strumień)', fontsize=FS,
            ha='center', fontweight='bold')

    # Trigger markers
    for tx in [4.0, 8.0, 12.0]:
        ax.plot([tx, tx], [1.4, 2.4], color=LN, lw=2, linestyle='--')
        ax.text(tx, 2.7, 'EMIT', fontsize=FS_SMALL, ha='center',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.1', facecolor=GRAY3, edgecolor=LN))

    ax.text(6.75, 3.3, 'Trigger decyduje kiedy emitować (np. co N zdarzeń)',
            fontsize=FS, ha='center', style='italic')

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save_fig(fig, 'q20_window_types.png')


# ============================================================
# 3. Event Time vs Processing Time scatter + watermark
# ============================================================
def gen_event_vs_processing_time():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle('Event Time vs Processing Time + Watermark',
                 fontsize=FS_TITLE, fontweight='bold')

    # --- Panel 1: Ideal vs Real ---
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_xlabel('Event Time', fontsize=FS_LABEL)
    ax.set_ylabel('Processing Time', fontsize=FS_LABEL)
    ax.set_title('Idealny vs Realny świat', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Ideal line
    ax.plot([0, 9], [0, 9], 'k--', lw=1.5, label='ideał (brak opóźnień)')

    # Real scattered points (processing >= event, some out of order)
    np.random.seed(42)
    event_times = np.sort(np.random.uniform(1, 8, 15))
    proc_times = event_times + np.random.exponential(0.5, 15)
    # Make some out of order
    idx = [3, 7, 11]
    for i in idx:
        proc_times[i] += 1.5

    ax.scatter(event_times, proc_times, c='black', s=30, zorder=5,
               label='zdarzenia (realne)')

    # Highlight out-of-order
    for i in idx:
        ax.annotate('out-of-order', xy=(event_times[i], proc_times[i]),
                    xytext=(event_times[i] + 0.8, proc_times[i] + 0.5),
                    fontsize=FS_SMALL, ha='left',
                    arrowprops=dict(arrowstyle='->', lw=0.8, color='#555'))

    ax.legend(fontsize=FS_SMALL, loc='upper left')
    ax.text(7, 2, 'Opóźnienie\nsieciowe ↑', fontsize=FS, ha='center',
            style='italic', color='#555')

    # --- Panel 2: Watermark concept ---
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_xlabel('Event Time', fontsize=FS_LABEL)
    ax.set_ylabel('Processing Time', fontsize=FS_LABEL)
    ax.set_title('Watermark — granica postępu', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])

    # Events
    ax.scatter(event_times, proc_times, c='black', s=30, zorder=5)

    # Watermark line (below most points, tracks progress)
    wm_x = np.linspace(0, 9, 50)
    wm_y = wm_x + 0.3  # watermark slightly above ideal
    ax.plot(wm_x, wm_y, 'k-', lw=2.5, label='Watermark')
    ax.fill_between(wm_x, 0, wm_y, alpha=0.15, color='gray')

    ax.text(2.0, 1.0, 'PONIŻEJ watermark:\n„na pewno dotarło"',
            fontsize=FS, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    # Late event
    late_x, late_y = event_times[7], proc_times[7]
    ax.scatter([late_x], [late_y], c='white', s=80, zorder=6,
               edgecolors='black', linewidths=2)
    ax.annotate('LATE DATA!\n(po watermarku)', xy=(late_x, late_y),
                xytext=(late_x + 1.2, late_y + 0.8),
                fontsize=FS_SMALL, ha='left', fontweight='bold',
                arrowprops=dict(arrowstyle='->', lw=1, color=LN))

    ax.legend(fontsize=FS_SMALL, loc='upper left')

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save_fig(fig, 'q20_event_vs_processing_time.png')


# ============================================================
# 4. Tumbling window example — fraud detection
# ============================================================
def gen_tumbling_fraud():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Tumbling Window — fraud detection (okno = 1 min)',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Time axis
    ax.annotate('', xy=(11.5, 1.0), xytext=(0.5, 1.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    ax.text(6.0, 0.4, 'czas', fontsize=FS, ha='center')

    # Window 1: normal
    draw_box(ax, 1.0, 1.5, 4.5, 3.0, '', fill=GRAY4, rounded=True, lw=2)
    ax.text(3.25, 4.2, '[14:00 — 14:01]', fontsize=FS_LABEL, ha='center',
            fontweight='bold')
    # Transactions
    txns1 = ['Sklep A: 50 zł', 'Sklep B: 30 zł', 'Stacja: 80 zł']
    for i, t in enumerate(txns1):
        draw_box(ax, 1.3, 3.3 - i * 0.55, 4.0, 0.45, t, fill=GRAY1,
                 fontsize=FS_SMALL, rounded=False)
    ax.text(3.25, 1.7, 'count = 3  →  OK', fontsize=FS, ha='center',
            fontweight='bold', color='#2E7D32',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#E8F5E9', edgecolor='#2E7D32'))

    # Window 2: fraud!
    draw_box(ax, 6.0, 1.5, 4.5, 3.0, '', fill=GRAY1, rounded=True, lw=2)
    ax.text(8.25, 4.2, '[14:01 — 14:02]', fontsize=FS_LABEL, ha='center',
            fontweight='bold')
    txns2 = ['ATM Warszawa: 500 zł', 'ATM Kraków: 500 zł', '... +45 transakcji']
    for i, t in enumerate(txns2):
        draw_box(ax, 6.3, 3.3 - i * 0.55, 4.0, 0.45, t, fill=GRAY3,
                 fontsize=FS_SMALL, rounded=False)
    ax.text(8.25, 1.7, 'count = 47  →  ALERT!', fontsize=FS, ha='center',
            fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#F8D7DA', edgecolor='#C62828'))

    save_fig(fig, 'q20_tumbling_fraud.png')


# ============================================================
# 5. Sliding window — SLA monitoring
# ============================================================
def gen_sliding_sla():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Sliding Window — monitoring SLA (okno=5min, krok=1min)',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Time axis
    ax.annotate('', xy=(11.5, 0.5), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))
    times = ['14:05', '14:06', '14:07', '14:08', '14:09']
    latencies = [120, 180, 340, 290, 150]
    sla = 200

    for i, (t, lat) in enumerate(zip(times, latencies)):
        x = 1.5 + i * 2.0
        ax.text(x, 0.1, t, fontsize=FS, ha='center')

        # Bar proportional to latency
        bar_h = lat / 100.0
        is_breach = lat > sla
        fill = '#F8D7DA' if is_breach else GRAY1
        edge = '#C62828' if is_breach else LN
        draw_box(ax, x - 0.5, 1.0, 1.0, bar_h, '', fill=fill,
                 rounded=False, edgecolor=edge, lw=1.5)
        ax.text(x, 1.0 + bar_h + 0.15, f'{lat}ms', fontsize=FS,
                ha='center', fontweight='bold',
                color='#C62828' if is_breach else LN)

        # Status
        status = 'ALERT!' if is_breach else 'OK'
        ax.text(x, 1.0 + bar_h + 0.55, status, fontsize=FS_SMALL,
                ha='center', fontweight='bold',
                color='#C62828' if is_breach else '#2E7D32')

    # SLA line
    sla_y = 1.0 + sla / 100.0
    ax.plot([0.8, 11.2], [sla_y, sla_y], 'k--', lw=1.5)
    ax.text(11.3, sla_y, f'SLA={sla}ms', fontsize=FS, va='center',
            fontweight='bold')

    # Sliding window bracket
    ax.annotate('', xy=(1.0, 5.3), xytext=(5.0, 5.3),
                arrowprops=dict(arrowstyle='<->', lw=1.5, color=LN))
    ax.text(3.0, 5.6, 'okno = 5 min', fontsize=FS, ha='center',
            fontweight='bold')

    ax.annotate('', xy=(3.0, 4.8), xytext=(5.0, 4.8),
                arrowprops=dict(arrowstyle='<->', lw=1, color='#555'))
    ax.text(4.0, 4.4, 'krok = 1 min\n(nakładanie!)', fontsize=FS_SMALL,
            ha='center', style='italic')

    save_fig(fig, 'q20_sliding_sla.png')


# ============================================================
# 6. Session window — user sessions
# ============================================================
def gen_session_users():
    fig, axes = plt.subplots(2, 1, figsize=(10, 5))
    fig.suptitle('Session Window — sesje użytkowników (gap = 30 min)',
                 fontsize=FS_TITLE, fontweight='bold')

    # Anna: 2 sessions
    ax = axes[0]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 3.5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Użytkownik Anna', fontsize=FS_LABEL, fontweight='bold')

    ax.annotate('', xy=(13.5, 1.0), xytext=(0.3, 1.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))

    # Clicks cluster 1
    for x in [1.0, 1.8, 2.5, 3.2]:
        ax.plot(x, 1.0, 'ko', markersize=6)
    # Clicks cluster 2
    for x in [9.0, 9.8, 10.5]:
        ax.plot(x, 1.0, 'ko', markersize=6)

    # Sessions
    rect1 = mpatches.FancyBboxPatch((0.7, 1.5), 2.8, 1.2,
            boxstyle="round,pad=0.1", facecolor=GRAY1, edgecolor=LN, lw=1.5)
    ax.add_patch(rect1)
    ax.text(2.1, 2.1, 'Sesja 1\n4 kliknięcia, 12 min', fontsize=FS,
            ha='center', fontweight='bold')

    rect2 = mpatches.FancyBboxPatch((8.7, 1.5), 2.1, 1.2,
            boxstyle="round,pad=0.1", facecolor=GRAY3, edgecolor=LN, lw=1.5)
    ax.add_patch(rect2)
    ax.text(9.75, 2.1, 'Sesja 2\n3 kliknięcia, 8 min', fontsize=FS,
            ha='center', fontweight='bold')

    # Gap
    ax.annotate('', xy=(8.5, 0.5), xytext=(3.8, 0.5),
                arrowprops=dict(arrowstyle='<->', lw=1.5, color=LN))
    ax.text(6.15, 0.1, 'cisza 45 min > gap(30)', fontsize=FS, ha='center',
            fontweight='bold', style='italic')

    # Bob: 1 session
    ax = axes[1]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 3.5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Użytkownik Bob', fontsize=FS_LABEL, fontweight='bold')

    ax.annotate('', xy=(13.5, 1.0), xytext=(0.3, 1.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color=LN))

    # Clicks spread evenly
    bobs = [1.0, 2.5, 4.0, 5.5, 7.0, 8.5, 10.0]
    for x in bobs:
        ax.plot(x, 1.0, 'ko', markersize=6)

    rect = mpatches.FancyBboxPatch((0.7, 1.5), 9.6, 1.2,
            boxstyle="round,pad=0.1", facecolor=GRAY1, edgecolor=LN, lw=2)
    ax.add_patch(rect)
    ax.text(5.5, 2.1, 'Sesja 1 (ciągła) — 7 kliknięć, każde < 30 min od poprzedniego',
            fontsize=FS, ha='center', fontweight='bold')

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save_fig(fig, 'q20_session_users.png')


# ============================================================
# 7. Streaming ecosystem overview
# ============================================================
def gen_streaming_ecosystem():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Ekosystem przetwarzania strumieniowego',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Source
    draw_box(ax, 0.3, 2.5, 2.0, 3.0, 'Kafka\nTopics\n(źródło)', fill=GRAY2,
             fontsize=FS, fontweight='bold')

    # Engines
    engines = [
        ('Kafka Streams\n(library w JVM)', GRAY1, 4.7),
        ('Apache Flink\n(klaster)', GRAY3, 3.2),
        ('Spark Streaming\n(klaster)', GRAY5, 1.7),
    ]
    for label, color, y in engines:
        draw_box(ax, 4.0, y, 3.0, 1.2, label, fill=color,
                 fontsize=FS, fontweight='bold')
        draw_arrow(ax, 2.3, 4.0, 4.0, y + 0.6, lw=1.5)

    # Sinks
    sinks = [
        ('Kafka topic\n/ baza danych', GRAY4, 4.7),
        ('DB / Kafka\n/ S3', GRAY4, 3.2),
        ('HDFS / DB\n/ dashboard', GRAY4, 1.7),
    ]
    for label, color, y in sinks:
        draw_box(ax, 8.5, y, 2.5, 1.2, label, fill=color,
                 fontsize=FS)
        draw_arrow(ax, 7.0, y + 0.6, 8.5, y + 0.6, lw=1.5)

    # Labels
    ax.text(1.3, 6.0, 'ŹRÓDŁO', fontsize=FS_LABEL, ha='center', fontweight='bold')
    ax.text(5.5, 6.2, 'SILNIK', fontsize=FS_LABEL, ha='center', fontweight='bold')
    ax.text(9.75, 6.2, 'WYNIK', fontsize=FS_LABEL, ha='center', fontweight='bold')

    # Latency annotations
    ax.text(5.5, 5.95, '~1-10 ms', fontsize=FS_SMALL, ha='center', style='italic')
    ax.text(5.5, 4.5, '<10 ms', fontsize=FS_SMALL, ha='center', style='italic')
    ax.text(5.5, 3.0, '~100 ms', fontsize=FS_SMALL, ha='center', style='italic')

    save_fig(fig, 'q20_streaming_ecosystem.png')


# ============================================================
# 8. True streaming vs Micro-batch
# ============================================================
def gen_true_vs_microbatch():
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.5))
    fig.suptitle('True Streaming vs Micro-Batch',
                 fontsize=FS_TITLE, fontweight='bold')

    # True streaming
    ax = axes[0]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('TRUE STREAMING (Flink, Kafka Streams) — event-by-event',
                 fontsize=FS_LABEL, fontweight='bold')

    for i in range(6):
        x = 1.0 + i * 1.8
        # Event
        draw_box(ax, x, 2.0, 0.8, 0.7, f'e{i+1}', fill=GRAY1,
                 fontsize=FS, fontweight='bold', rounded=False)
        # Arrow down
        draw_arrow(ax, x + 0.4, 2.0, x + 0.4, 1.4, lw=1)
        # Result
        draw_box(ax, x, 0.5, 0.8, 0.7, f'r{i+1}', fill=GRAY3,
                 fontsize=FS, fontweight='bold', rounded=False)
        # Latency label
        ax.text(x + 0.4, 1.6, '~ms', fontsize=5, ha='center', color='#555')

    ax.text(11.5, 1.3, 'Latencja:\n< 10 ms', fontsize=FS, ha='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    # Micro-batch
    ax = axes[1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('MICRO-BATCH (Spark Streaming) — grupami co ~100ms',
                 fontsize=FS_LABEL, fontweight='bold')

    batch_colors = [GRAY1, GRAY2, GRAY3]
    for b in range(3):
        bx = 0.8 + b * 3.5
        # Batch boundary
        draw_box(ax, bx, 1.8, 3.0, 1.0, '', fill=batch_colors[b],
                 rounded=True, lw=1.5)
        ax.text(bx + 1.5, 2.6, f'Batch {b+1}', fontsize=FS,
                ha='center', fontweight='bold')
        for j in range(3):
            ex = bx + 0.3 + j * 0.9
            draw_box(ax, ex, 2.0, 0.7, 0.5, f'e{b*3+j+1}', fill='white',
                     fontsize=FS_SMALL, rounded=False)

        # Arrow down
        draw_arrow(ax, bx + 1.5, 1.8, bx + 1.5, 1.2, lw=1.5)
        # Result
        draw_box(ax, bx + 0.5, 0.4, 2.0, 0.7, f'result {b+1}', fill=GRAY4,
                 fontsize=FS, fontweight='bold')

    ax.text(11.5, 1.3, 'Latencja:\n~100ms–s', fontsize=FS, ha='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save_fig(fig, 'q20_true_vs_microbatch.png')


# ============================================================
# 9. Platform comparison table
# ============================================================
def gen_platform_comparison():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(-6, 1)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Porównanie platform strumieniowych',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    headers = ['Cecha', 'Kafka Streams', 'Apache Flink', 'Spark Streaming']
    col_w = [2.5, 2.8, 2.8, 2.8]
    rows = [
        ['Model', 'event-by-event', 'event-by-event', 'micro-batch (~100ms)'],
        ['Deployment', 'library (w JVM)', 'klaster', 'klaster'],
        ['Latencja', '~1–10 ms', '< 10 ms', '100 ms – sekundy'],
        ['Exactly-once', 'Kafka TXN', 'checkpointing', 'WAL'],
        ['State', 'RocksDB local', 'RocksDB + ckpt', 'in-memory / ext'],
        ['Okna', 'T, S, Session', 'wszystkie + custom', 'T, S'],
        ['Use case', 'Kafka → Kafka', 'złożona analityka', 'ETL + ML / SQL'],
    ]
    draw_table(ax, headers, rows, x0=0.25, y0=0.5, col_widths=col_w,
               row_h=0.6, fontsize=7, header_fontsize=8)

    save_fig(fig, 'q20_platform_comparison.png')


# ============================================================
# 10. Kafka Streams architecture
# ============================================================
def gen_kafka_streams_arch():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Kafka Streams — architektura (library w JVM)',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Outer box: Your Java application
    draw_box(ax, 0.5, 0.5, 11.0, 5.5, '', fill=GRAY4, rounded=True, lw=2.5)
    ax.text(6.0, 5.7, 'Twoja aplikacja Java (JVM)', fontsize=FS_LABEL,
            ha='center', fontweight='bold')

    # Kafka Consumer
    draw_box(ax, 1.0, 3.0, 2.5, 1.5, 'Kafka\nConsumer\n(input topic)',
             fill=GRAY1, fontsize=FS, fontweight='bold')

    # Processing
    draw_box(ax, 4.5, 3.0, 2.5, 1.5, 'Kafka Streams\n(logika\nbiznesowa)',
             fill=GRAY2, fontsize=FS, fontweight='bold')

    # Kafka Producer
    draw_box(ax, 8.0, 3.0, 2.5, 1.5, 'Kafka\nProducer\n(output topic)',
             fill=GRAY1, fontsize=FS, fontweight='bold')

    # Arrows
    draw_arrow(ax, 3.5, 3.75, 4.5, 3.75, lw=2)
    draw_arrow(ax, 7.0, 3.75, 8.0, 3.75, lw=2)

    # RocksDB state store
    draw_box(ax, 4.5, 1.0, 2.5, 1.3, 'RocksDB\n(stan lokalny)',
             fill=GRAY3, fontsize=FS, fontweight='bold')
    ax.plot([5.75, 5.75], [3.0, 2.3], color=LN, lw=1.5)
    ax.text(7.3, 1.6, 'okna, joiny,\nagregacje', fontsize=FS_SMALL,
            style='italic', va='center')

    # Key message
    ax.text(6.0, 0.2, 'NIE potrzebujesz osobnego klastra!  '
            'Skalujesz = więcej instancji JVM.', fontsize=FS, ha='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=LN))

    save_fig(fig, 'q20_kafka_streams_arch.png')


# ============================================================
# 11. Flink architecture + checkpointing
# ============================================================
def gen_flink_arch():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Apache Flink — architektura klastra + checkpointing',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Cluster border
    draw_box(ax, 0.3, 1.0, 11.4, 6.2, '', fill=GRAY4, rounded=True, lw=2.5)
    ax.text(6.0, 6.95, 'FLINK CLUSTER', fontsize=FS_LABEL,
            ha='center', fontweight='bold')

    # Job Manager
    draw_box(ax, 1.0, 5.5, 3.0, 1.2, 'Job Manager\n(koordynacja,\ncheckpointy)',
             fill=GRAY2, fontsize=FS, fontweight='bold')

    # Task Managers
    draw_box(ax, 1.0, 3.0, 10.0, 2.0, '', fill='white', rounded=True, lw=1.5)
    ax.text(6.0, 4.7, 'Task Managers (workery)', fontsize=FS,
            ha='center', fontweight='bold')

    slots = ['source\n& map()', 'map()', 'window()\n& reduce', 'sink()']
    for i, s in enumerate(slots):
        x = 1.5 + i * 2.4
        draw_box(ax, x, 3.3, 2.0, 1.2, f'Slot {i+1}\n{s}', fill=GRAY1,
                 fontsize=FS_SMALL, fontweight='bold')

    draw_arrow(ax, 2.5, 5.5, 6.0, 5.0, lw=1.5, style='->')
    ax.text(5.0, 5.5, 'przydziela\npodzadania', fontsize=FS_SMALL,
            style='italic')

    # Checkpoint storage
    draw_box(ax, 5.5, 1.2, 3.5, 1.2, 'Checkpoint Storage\n(HDFS / S3)',
             fill=GRAY3, fontsize=FS, fontweight='bold')
    ax.plot([7.25, 7.25], [2.4, 3.3], color=LN, lw=1.5, linestyle='--')
    ax.text(8.0, 2.7, 'snapshoty\nstanu', fontsize=FS_SMALL, style='italic')

    # Barrier concept at bottom
    ax.text(3.0, 1.6, 'Barrier:', fontsize=FS, fontweight='bold')
    barrier_boxes = ['source', '|B|', 'map', '|B|', 'sink']
    bx = 0.8
    for i, b in enumerate(barrier_boxes):
        if b == '|B|':
            ax.text(bx + 0.3, 1.5, b, fontsize=FS, ha='center',
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.1', facecolor=GRAY5,
                              edgecolor=LN))
            draw_arrow(ax, bx, 1.5, bx + 0.1, 1.5, lw=1)
            bx += 0.7
        else:
            draw_box(ax, bx, 1.3, 1.0, 0.45, b, fill=GRAY1,
                     fontsize=FS_SMALL, fontweight='bold')
            bx += 1.2

    save_fig(fig, 'q20_flink_arch.png')


# ============================================================
# 12. Spark Streaming architecture
# ============================================================
def gen_spark_streaming_arch():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Spark Streaming — architektura (micro-batch)',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Cluster border
    draw_box(ax, 0.3, 0.5, 11.4, 5.8, '', fill=GRAY4, rounded=True, lw=2.5)
    ax.text(6.0, 6.0, 'SPARK CLUSTER', fontsize=FS_LABEL,
            ha='center', fontweight='bold')

    # Driver
    draw_box(ax, 1.0, 4.5, 3.0, 1.2, 'Driver\n(planuje mini-batche)',
             fill=GRAY2, fontsize=FS, fontweight='bold')

    draw_arrow(ax, 2.5, 4.5, 6.0, 4.0, lw=1.5)

    # Batches
    batches = ['batch 1\n(e1,e2,e3)', 'batch 2\n(e4,e5,e6)', 'batch 3\n(e7,e8,e9)']
    for i, b in enumerate(batches):
        y = 2.8 - i * 1.0
        draw_box(ax, 4.5, y, 2.5, 0.8, b, fill=GRAY1,
                 fontsize=FS_SMALL, fontweight='bold')
        # map → reduce
        draw_arrow(ax, 7.0, y + 0.4, 7.5, y + 0.4, lw=1)
        draw_box(ax, 7.5, y, 1.3, 0.8, 'map→\nreduce', fill=GRAY3,
                 fontsize=5.5)
        draw_arrow(ax, 8.8, y + 0.4, 9.3, y + 0.4, lw=1)
        draw_box(ax, 9.3, y, 1.5, 0.8, f'result {i+1}', fill='white',
                 fontsize=FS_SMALL)

    # Spark ecosystem
    draw_box(ax, 1.0, 1.0, 3.0, 1.0, 'Spark SQL / MLlib\n(ten sam ekosystem!)',
             fill=GRAY5, fontsize=FS, fontweight='bold')

    ax.text(6.0, 0.3, 'ZALETA: batch API    |    WADA: latencja ≥ batch interval (~100ms)',
            fontsize=FS, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=LN))

    save_fig(fig, 'q20_spark_streaming_arch.png')


# ============================================================
# 13. Lambda vs Kappa architecture
# ============================================================
def gen_lambda_vs_kappa():
    fig, axes = plt.subplots(2, 1, figsize=(10, 7))
    fig.suptitle('Architektura Lambda vs Kappa',
                 fontsize=FS_TITLE, fontweight='bold')

    # --- Lambda ---
    ax = axes[0]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('LAMBDA — 2 ścieżki (batch + speed)',
                 fontsize=FS_LABEL, fontweight='bold')

    # Source
    draw_box(ax, 0.3, 1.8, 2.0, 1.5, 'Źródło\ndanych', fill=GRAY2,
             fontsize=FS, fontweight='bold')

    # Batch layer (top)
    draw_box(ax, 3.5, 3.3, 3.0, 1.2, 'Batch Layer\n(Spark)\nprzelicza co godzinę',
             fill=GRAY1, fontsize=FS_SMALL, fontweight='bold')
    draw_arrow(ax, 2.3, 3.0, 3.5, 3.9, lw=1.5)

    # Speed layer (bottom)
    draw_box(ax, 3.5, 0.8, 3.0, 1.2, 'Speed Layer\n(Flink)\nreal-time',
             fill=GRAY3, fontsize=FS_SMALL, fontweight='bold')
    draw_arrow(ax, 2.3, 2.2, 3.5, 1.4, lw=1.5)

    # Results
    draw_box(ax, 7.5, 3.3, 2.0, 1.2, 'Dokładne\nwyniki\n(wolne)',
             fill=GRAY4, fontsize=FS_SMALL)
    draw_arrow(ax, 6.5, 3.9, 7.5, 3.9, lw=1.5)

    draw_box(ax, 7.5, 0.8, 2.0, 1.2, 'Przybliżone\nwyniki\n(szybkie)',
             fill=GRAY4, fontsize=FS_SMALL)
    draw_arrow(ax, 6.5, 1.4, 7.5, 1.4, lw=1.5)

    # Merge
    draw_box(ax, 10.0, 2.0, 1.5, 1.5, 'MERGE\n→ UI', fill=GRAY5,
             fontsize=FS, fontweight='bold')
    draw_arrow(ax, 9.5, 3.5, 10.0, 3.0, lw=1.5)
    draw_arrow(ax, 9.5, 1.8, 10.0, 2.5, lw=1.5)

    ax.text(6.0, 0.1, '2 systemy, 2 kody — złożone ale pewne',
            fontsize=FS, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    # --- Kappa ---
    ax = axes[1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('KAPPA — 1 ścieżka (streaming only)',
                 fontsize=FS_LABEL, fontweight='bold')

    # Source
    draw_box(ax, 0.3, 1.3, 2.0, 1.5, 'Źródło\ndanych', fill=GRAY2,
             fontsize=FS, fontweight='bold')

    # Single streaming layer
    draw_box(ax, 3.5, 1.3, 3.5, 1.5, 'Streaming Layer\n(Flink)\n+ replay z Kafka log',
             fill=GRAY1, fontsize=FS, fontweight='bold')
    draw_arrow(ax, 2.3, 2.05, 3.5, 2.05, lw=2)

    # Output
    draw_box(ax, 8.0, 1.3, 2.5, 1.5, 'Wyniki\n→ UI', fill=GRAY4,
             fontsize=FS, fontweight='bold')
    draw_arrow(ax, 7.0, 2.05, 8.0, 2.05, lw=2)

    # Replay arrow
    ax.annotate('', xy=(3.5, 1.0), xytext=(7.0, 1.0),
                arrowprops=dict(arrowstyle='<-', lw=1.5, color=LN,
                                connectionstyle='arc3,rad=0.3', linestyle='--'))
    ax.text(5.25, 0.3, 'Replay z Kafka\n(przetwórz historię od nowa)',
            fontsize=FS_SMALL, ha='center', style='italic')

    ax.text(6.0, 3.3, '1 system, 1 kod — prostsze, ale replay = dużo I/O',
            fontsize=FS, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save_fig(fig, 'q20_lambda_vs_kappa.png')


# ============================================================
# 14. Lambda vs Kappa comparison table
# ============================================================
def gen_lambda_kappa_table():
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(-4.5, 1)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Lambda vs Kappa — porównanie',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    headers = ['Cecha', 'Lambda', 'Kappa']
    col_w = [2.5, 3.5, 3.5]
    rows = [
        ['Ścieżki', '2 (batch + speed)', '1 (streaming)'],
        ['Kod', '2 implementacje', '1 implementacja'],
        ['Złożoność', 'wysoka', 'niska'],
        ['Replay', 'batch przelicza', 'Kafka replay'],
        ['Spójność', 'merge wymagany', 'natywna'],
        ['Przykład', 'Netflix, LinkedIn', 'Uber, Confluent'],
    ]
    draw_table(ax, headers, rows, x0=0.25, y0=0.5, col_widths=col_w,
               row_h=0.55, fontsize=7.5)

    save_fig(fig, 'q20_lambda_kappa_table.png')


# ============================================================
# 15. Exactly-once comparison
# ============================================================
def gen_exactly_once():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Exactly-Once — mechanizmy na 3 platformach',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Flink
    draw_box(ax, 0.3, 4.3, 11.0, 2.0, '', fill=GRAY4, rounded=True, lw=1.5)
    ax.text(1.0, 5.9, 'Flink — Distributed Snapshots (Chandy-Lamport)',
            fontsize=FS, fontweight='bold')

    flink_steps = ['source', '|B|', 'map()', '|B|', 'sink()']
    bx = 1.0
    for s in flink_steps:
        if s == '|B|':
            ax.text(bx + 0.25, 4.85, s, fontsize=FS, ha='center',
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.1', facecolor=GRAY5,
                              edgecolor=LN))
            draw_arrow(ax, bx - 0.1, 4.85, bx + 0.05, 4.85, lw=1)
            bx += 0.7
        else:
            draw_box(ax, bx, 4.6, 1.5, 0.55, s, fill=GRAY1,
                     fontsize=FS_SMALL, fontweight='bold')
            bx += 1.8
    ax.text(8.5, 5.0, 'barrier → save state\n→ checkpoint (HDFS/S3)',
            fontsize=FS_SMALL, style='italic')

    # Kafka Streams
    draw_box(ax, 0.3, 2.3, 11.0, 1.5, '', fill=GRAY1, rounded=True, lw=1.5)
    ax.text(1.0, 3.5, 'Kafka Streams — Transakcje Kafka',
            fontsize=FS, fontweight='bold')
    ax.text(1.5, 2.85, 'idempotent producer + begin TX → produce → commit TX → '
            'consumer offsets w TX', fontsize=FS_SMALL)

    # Spark
    draw_box(ax, 0.3, 0.5, 11.0, 1.5, '', fill=GRAY3, rounded=True, lw=1.5)
    ax.text(1.0, 1.7, 'Spark Streaming — Write-Ahead Log (WAL)',
            fontsize=FS, fontweight='bold')
    ax.text(1.5, 1.05, 'WAL + checkpointing micro-batchów + idempotent sinks '
            '(np. upsert do DB)', fontsize=FS_SMALL)

    save_fig(fig, 'q20_exactly_once.png')


# ============================================================
# 16. Late data strategies (DRAS)
# ============================================================
def gen_late_data_strategies():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Late Data — 4 strategie (mnemonik DRAS)',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Setup: window closed, late event arrives
    draw_box(ax, 0.5, 5.5, 4.5, 1.0, 'Okno [14:00–14:05]\nZAMKNIĘTE o 14:05',
             fill=GRAY2, fontsize=FS, fontweight='bold')
    draw_box(ax, 6.0, 5.5, 4.5, 1.0, 'Spóźnione zdarzenie\nevent_time=14:00:03\narrives=14:05:30',
             fill='#F8D7DA', fontsize=FS_SMALL, fontweight='bold')
    draw_arrow(ax, 10.5, 6.0, 5.0, 6.0, lw=2, color='#C62828', style='->')
    ax.text(7.5, 5.2, 'LATE!', fontsize=FS_LABEL, ha='center',
            fontweight='bold', color='#C62828')

    # 4 strategies
    strategies = [
        ('D — Drop', 'Odrzuć spóźnione', '/dev/null', GRAY4),
        ('R — Recompute', 'Przelicz okno ponownie', 'poprawne ale kosztowne', GRAY1),
        ('A — Allowed lateness', 'Czekaj dodatkowy czas\n(np. +2 min)', 'kompromis pamięci', GRAY2),
        ('S — Side output', 'Przekieruj do osobnej\nkolejki', 'elastyczne, ręczna analiza', GRAY3),
    ]
    for i, (name, desc, tradeoff, color) in enumerate(strategies):
        y = 3.8 - i * 1.1
        draw_box(ax, 0.5, y, 2.5, 0.9, name, fill=color, fontsize=FS,
                 fontweight='bold')
        ax.text(3.3, y + 0.45, desc, fontsize=FS_SMALL, va='center')
        ax.text(8.5, y + 0.45, tradeoff, fontsize=FS_SMALL, va='center',
                style='italic', color='#555')

    save_fig(fig, 'q20_late_data_strategies.png')


# ============================================================
# 17. Decision tree — which platform
# ============================================================
def gen_decision_tree():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title('Drzewo decyzyjne — wybór platformy',
                 fontsize=FS_TITLE, fontweight='bold', pad=10)

    # Root question
    draw_box(ax, 3.5, 5.5, 4.5, 1.0, 'Latencja < 10ms\nwymagana?',
             fill=GRAY2, fontsize=FS, fontweight='bold')

    # TAK branch
    draw_arrow(ax, 3.5, 5.7, 2.0, 5.0, lw=1.5)
    ax.text(2.3, 5.3, 'TAK', fontsize=FS, fontweight='bold')

    draw_box(ax, 0.3, 3.5, 3.5, 1.0, 'Dane już w Kafce?\nProste transformacje?',
             fill=GRAY1, fontsize=FS, fontweight='bold')

    # TAK → Kafka Streams
    draw_arrow(ax, 0.3, 3.7, -0.1, 3.0, lw=1.5)
    ax.text(0.0, 3.3, 'TAK', fontsize=FS_SMALL, fontweight='bold')
    draw_box(ax, -0.3, 1.8, 2.5, 1.0, 'Kafka\nStreams', fill=GRAY5,
             fontsize=FS_LABEL, fontweight='bold')

    # NIE → Flink
    draw_arrow(ax, 3.8, 3.7, 4.5, 3.0, lw=1.5)
    ax.text(4.0, 3.3, 'NIE\n(złożona logika)', fontsize=FS_SMALL)
    draw_box(ax, 3.0, 1.8, 2.5, 1.0, 'Apache\nFlink', fill=GRAY5,
             fontsize=FS_LABEL, fontweight='bold')

    # NIE branch
    draw_arrow(ax, 8.0, 5.7, 9.5, 5.0, lw=1.5)
    ax.text(8.7, 5.3, 'NIE', fontsize=FS, fontweight='bold')

    draw_box(ax, 7.5, 3.5, 4.2, 1.0, '~100ms–1s OK?\nPotrzeba ML / SQL?',
             fill=GRAY1, fontsize=FS, fontweight='bold')

    # TAK + ML → Spark
    draw_arrow(ax, 9.5, 3.5, 9.5, 3.0, lw=1.5)
    ax.text(10.0, 3.3, 'TAK + ML/SQL', fontsize=FS_SMALL)
    draw_box(ax, 8.0, 1.8, 2.5, 1.0, 'Spark\nStreaming', fill=GRAY5,
             fontsize=FS_LABEL, fontweight='bold')

    # TAK + proste → Kafka Streams too
    draw_arrow(ax, 7.5, 3.7, 6.5, 3.0, lw=1.5)
    ax.text(6.3, 3.3, 'proste + TAK', fontsize=FS_SMALL)
    draw_box(ax, 5.8, 1.8, 2.0, 1.0, 'Kafka\nStreams', fill=GRAY5,
             fontsize=FS, fontweight='bold')

    # Legend
    ax.text(6.0, 0.7, 'Reguła: Kafka Streams = najprostsze (library) | '
            'Flink = najpotężniejszy (true streaming) | Spark = ekosystem ML',
            fontsize=FS, ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=GRAY4, edgecolor=GRAY5))

    save_fig(fig, 'q20_decision_tree.png')


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Generating ALL PYTANIE 20 diagrams...")
    gen_batch_vs_streaming()
    gen_window_types()
    gen_event_vs_processing_time()
    gen_tumbling_fraud()
    gen_sliding_sla()
    gen_session_users()
    gen_streaming_ecosystem()
    gen_true_vs_microbatch()
    gen_platform_comparison()
    gen_kafka_streams_arch()
    gen_flink_arch()
    gen_spark_streaming_arch()
    gen_lambda_vs_kappa()
    gen_lambda_kappa_table()
    gen_exactly_once()
    gen_late_data_strategies()
    gen_decision_tree()
    print("\nAll 17 PYTANIE 20 diagrams generated successfully!")
