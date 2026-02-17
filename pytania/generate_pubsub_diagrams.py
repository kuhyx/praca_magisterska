#!/usr/bin/env python3
"""
Generate Pub/Sub diagrams for PYTANIE 19:
  Subscription types (4 separate images):
    1. Topic-based
    2. Content-based
    3. Type-based
    4. Hierarchical (wildcards)
  Delivery guarantees (3 separate images):
    5. At-most-once
    6. At-least-once
    7. Exactly-once

All: A4-width, B&W, 300 DPI, laser-printer-friendly.
One diagram per image — no cramming.
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
FS = 9
FS_TITLE = 13
FIG_W = 8.27  # A4 width in inches
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


def draw_arrow(ax, x1, y1, x2, y2, lw=1.2, style='->', color=LN, label='',
               label_offset=0.15, label_fs=8):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + label_offset
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=label_fs, color=color)


def draw_dashed_arrow(ax, x1, y1, x2, y2, lw=1.0, color=LN, label='',
                      label_offset=0.15, label_fs=8):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                linestyle='dashed'))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + label_offset
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=label_fs, color=color)


def draw_cross(ax, x, y, size=0.15, lw=2.5, color='black'):
    ax.plot([x - size, x + size], [y - size, y + size], color=color, lw=lw)
    ax.plot([x - size, x + size], [y + size, y - size], color=color, lw=lw)


def draw_check(ax, x, y, size=0.15, lw=2.5, color='black'):
    ax.plot([x - size, x - size*0.2], [y, y - size*0.7], color=color, lw=lw)
    ax.plot([x - size*0.2, x + size], [y - size*0.7, y + size*0.5], color=color, lw=lw)


def save(fig, name):
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, name), dpi=DPI,
                bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {name}")


# ============================================================
# 1. Topic-based subscription
# ============================================================
def draw_sub_topic():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, 4.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Subskrypcja topic-based — routing po nazwie tematu',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Publisher + messages
    draw_box(ax, 0.2, 3.2, 2.4, 1.1, 'Publisher', fill=GRAY1, fontsize=10, fontweight='bold')
    draw_box(ax, 0.3, 1.8, 2.2, 0.8, 'topic: "orders"', fill=GRAY4, fontsize=8)
    draw_box(ax, 0.3, 0.7, 2.2, 0.8, 'topic: "payments"', fill=GRAY4, fontsize=8)

    # Broker
    draw_box(ax, 4.2, 1.5, 2.8, 2.2, 'BROKER\n\ntopic routing', fill=GRAY2, fontsize=10, fontweight='bold')

    # Subscribers
    draw_box(ax, 8.5, 3.8, 3.0, 1.0, 'Subscriber A\nsubskrybuje: "orders"', fill=GRAY1, fontsize=8.5)
    draw_box(ax, 8.5, 2.2, 3.0, 1.0, 'Subscriber B\nsubskrybuje: "payments"', fill=GRAY1, fontsize=8.5)
    draw_box(ax, 8.5, 0.6, 3.0, 1.0, 'Subscriber C\nsubskrybuje: "orders"', fill=GRAY1, fontsize=8.5)

    # Arrows: publisher → broker
    draw_arrow(ax, 2.6, 2.2, 4.2, 2.8, label_fs=8)
    draw_arrow(ax, 2.6, 1.1, 4.2, 2.2, label_fs=8)

    # Arrows: broker → subscribers
    draw_arrow(ax, 7.0, 3.4, 8.5, 4.2, label='"orders"', label_fs=8)
    draw_arrow(ax, 7.0, 2.6, 8.5, 2.7, label='"payments"', label_fs=8)
    draw_arrow(ax, 7.0, 2.2, 8.5, 1.2, label='"orders"', label_fs=8)

    # Explanation
    ax.text(6.0, 0.1, 'Subscriber deklaruje nazwę tematu. Broker kieruje wiadomości\n'
            'do WSZYSTKICH subscriberów danego tematu. Najprostszy model.',
            ha='center', va='bottom', fontsize=8.5, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    save(fig, 'pubsub_sub_topic.png')


# ============================================================
# 2. Content-based subscription
# ============================================================
def draw_sub_content():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Subskrypcja content-based — filtrowanie po treści wiadomości',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Publisher + message
    draw_box(ax, 0.2, 3.5, 2.4, 1.1, 'Publisher', fill=GRAY1, fontsize=10, fontweight='bold')
    draw_box(ax, 0.2, 1.8, 2.4, 1.2, 'price: 150\ntype: "book"\ncategory: "IT"', fill=GRAY4, fontsize=8.5)

    # Broker
    draw_box(ax, 4.0, 2.0, 3.0, 2.5, 'BROKER\n\newaluuje filtry\nkażdego subscribera', fill=GRAY2, fontsize=9, fontweight='bold')

    # Subscribers with filters
    draw_box(ax, 8.5, 4.2, 3.2, 1.0, 'Sub A\nfiltr: price > 100', fill=GRAY1, fontsize=9)
    draw_box(ax, 8.5, 2.6, 3.2, 1.0, 'Sub B\nfiltr: type = "food"', fill=GRAY1, fontsize=9)
    draw_box(ax, 8.5, 1.0, 3.2, 1.0, 'Sub C\nfiltr: price < 50', fill=GRAY1, fontsize=9)

    # Arrows
    draw_arrow(ax, 2.6, 2.4, 4.0, 3.0)
    draw_arrow(ax, 7.0, 4.0, 8.5, 4.6, label='150 > 100  ✓  dostarczono', label_fs=8)
    draw_dashed_arrow(ax, 7.0, 3.2, 8.5, 3.1, label='"book" ≠ "food"  ✗  odrzucono', label_fs=8)
    draw_dashed_arrow(ax, 7.0, 2.5, 8.5, 1.6, label='150 < 50  ✗  odrzucono', label_fs=8)

    ax.text(6.0, 0.2, 'Broker analizuje TREŚĆ wiadomości i ewaluuje predykaty.\n'
            'Bardziej elastyczny niż topic-based, ale wolniejszy (koszt ewaluacji).',
            ha='center', va='bottom', fontsize=8.5, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    save(fig, 'pubsub_sub_content.png')


# ============================================================
# 3. Type-based subscription
# ============================================================
def draw_sub_type():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, 5.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Subskrypcja type-based — routing po typie (klasie) obiektu',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Publisher
    draw_box(ax, 0.2, 4.2, 2.4, 1.1, 'Publisher', fill=GRAY1, fontsize=10, fontweight='bold')

    # Messages
    draw_box(ax, 0.1, 2.8, 2.6, 0.9, 'new OrderEvent()', fill=GRAY4, fontsize=9)
    draw_box(ax, 0.1, 1.5, 2.6, 0.9, 'new PaymentEvent()', fill=GRAY4, fontsize=9)

    # Broker
    draw_box(ax, 4.0, 2.3, 3.0, 2.4, 'BROKER\n\nrouting po\ntypie klasy', fill=GRAY2, fontsize=10, fontweight='bold')

    # Subscribers
    draw_box(ax, 8.5, 4.8, 3.2, 1.0, 'Sub A\n→ OrderEvent', fill=GRAY1, fontsize=9)
    draw_box(ax, 8.5, 3.2, 3.2, 1.0, 'Sub B\n→ PaymentEvent', fill=GRAY1, fontsize=9)
    draw_box(ax, 8.5, 1.6, 3.2, 1.0, 'Sub C\n→ Event (base)', fill=GRAY1, fontsize=9)

    # Arrows
    draw_arrow(ax, 2.7, 3.2, 4.0, 3.8)
    draw_arrow(ax, 2.7, 2.0, 4.0, 3.0)
    draw_arrow(ax, 7.0, 4.3, 8.5, 5.2, label='OrderEvent', label_fs=8)
    draw_arrow(ax, 7.0, 3.5, 8.5, 3.7, label='PaymentEvent', label_fs=8)
    draw_arrow(ax, 7.0, 3.0, 8.5, 2.2, label='oba (dziedziczenie!)', label_fs=8)

    # Class hierarchy inset
    hx, hy = 0.5, 0.0
    draw_box(ax, hx + 2.0, hy + 0.2, 1.8, 0.6, 'Event', fill=GRAY3, fontsize=8, fontweight='bold')
    draw_box(ax, hx + 0.0, hy + 0.2, 1.8, 0.6, 'OrderEvent', fill=GRAY4, fontsize=7.5)
    draw_box(ax, hx + 4.0, hy + 0.2, 2.0, 0.6, 'PaymentEvent', fill=GRAY4, fontsize=7.5)
    draw_arrow(ax, hx + 2.9, hy + 0.2, hx + 0.9, hy + 0.2, lw=1.0, style='->', label='extends', label_offset=-0.3, label_fs=7)
    draw_arrow(ax, hx + 2.9, hy + 0.2, hx + 5.0, hy + 0.2, lw=1.0, style='->', label='extends', label_offset=-0.3, label_fs=7)

    ax.text(9.5, 0.5, 'Sub C subskrybuje bazowy Event\n→ otrzymuje WSZYSTKIE podtypy',
            ha='center', va='center', fontsize=8.5, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY4, edgecolor=GRAY3))

    save(fig, 'pubsub_sub_type.png')


# ============================================================
# 4. Hierarchical / Wildcards subscription
# ============================================================
def draw_sub_hierarchical():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Subskrypcja hierarchiczna (wildcards) — wzorce tematów',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Topic tree
    draw_box(ax, 4.5, 5.8, 2.4, 0.8, 'sensors/', fill=GRAY2, fontsize=10, fontweight='bold')

    draw_box(ax, 1.5, 4.2, 2.4, 0.8, 'temperature/', fill=GRAY3, fontsize=9)
    draw_box(ax, 7.5, 4.2, 2.4, 0.8, 'humidity/', fill=GRAY3, fontsize=9)

    draw_box(ax, 0.2, 2.8, 1.8, 0.7, 'room1', fill=GRAY4, fontsize=8.5)
    draw_box(ax, 2.4, 2.8, 1.8, 0.7, 'room2', fill=GRAY4, fontsize=8.5)
    draw_box(ax, 6.8, 2.8, 1.8, 0.7, 'room1', fill=GRAY4, fontsize=8.5)
    draw_box(ax, 9.0, 2.8, 1.8, 0.7, 'room2', fill=GRAY4, fontsize=8.5)

    # Tree edges
    draw_arrow(ax, 5.7, 5.8, 2.7, 5.0, lw=1.0)
    draw_arrow(ax, 5.7, 5.8, 8.7, 5.0, lw=1.0)
    draw_arrow(ax, 2.2, 4.2, 1.1, 3.5, lw=1.0)
    draw_arrow(ax, 3.2, 4.2, 3.3, 3.5, lw=1.0)
    draw_arrow(ax, 8.2, 4.2, 7.7, 3.5, lw=1.0)
    draw_arrow(ax, 9.2, 4.2, 9.9, 3.5, lw=1.0)

    # Full paths
    ax.text(1.1, 2.4, 'sensors/temperature/room1', fontsize=7, ha='center',
            fontfamily='monospace', style='italic')
    ax.text(3.3, 2.4, 'sensors/temperature/room2', fontsize=7, ha='center',
            fontfamily='monospace', style='italic')

    # Wildcard examples
    ax.text(0.3, 1.5, 'Wzorce subskrypcji (MQTT-style):', fontsize=10, fontweight='bold')

    patterns = [
        ('"sensors/temperature/room1"', '→ TYLKO room1', '(dokładne dopasowanie)'),
        ('"sensors/temperature/*"',     '→ room1, room2',  '( * = jeden poziom)'),
        ('"sensors/#"',                 '→ WSZYSTKO',      '( # = dowolna głębokość)'),
    ]
    for i, (pat, result, note) in enumerate(patterns):
        yy = 0.9 - i * 0.55
        ax.text(0.5, yy, pat, fontsize=9, fontweight='bold', fontfamily='monospace')
        ax.text(7.0, yy, result, fontsize=9, fontweight='bold')
        ax.text(9.5, yy, note, fontsize=8, style='italic')

    save(fig, 'pubsub_sub_hierarchical.png')


# ============================================================
# 5. At-most-once (QoS 0)
# ============================================================
def draw_qos_at_most_once():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('QoS: At-most-once — „wyślij i zapomnij" (0 lub 1 dostarczenie)',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    # Actors
    px, bx, sx = 1.0, 4.8, 8.5
    pw, bw, sw = 2.0, 2.2, 2.0
    bh = 0.8
    draw_box(ax, px, 5.0, pw, bh, 'Publisher', fill=GRAY1, fontsize=10, fontweight='bold')
    draw_box(ax, bx, 5.0, bw, bh, 'Broker', fill=GRAY2, fontsize=10, fontweight='bold')
    draw_box(ax, sx, 5.0, sw, bh, 'Subscriber', fill=GRAY1, fontsize=10, fontweight='bold')

    # Timelines
    for xc in [px + pw/2, bx + bw/2, sx + sw/2]:
        ax.plot([xc, xc], [5.0, 1.2], color=GRAY3, lw=1, linestyle=':')

    # Scenario A: success
    y = 4.3
    ax.text(0.2, y + 0.15, 'Scenariusz A:', fontsize=8.5, fontweight='bold')
    draw_arrow(ax, px + pw/2, y, bx + bw/2, y, label='MSG', label_fs=9)
    draw_arrow(ax, bx + bw/2, y - 0.6, sx + sw/2, y - 0.6, label='MSG', label_fs=9)
    draw_check(ax, sx + sw/2 + 0.4, y - 0.6, size=0.18)
    ax.text(sx + sw/2 + 0.7, y - 0.6, 'OK', fontsize=9, fontweight='bold')

    # Scenario B: lost
    y = 2.6
    ax.text(0.2, y + 0.15, 'Scenariusz B:', fontsize=8.5, fontweight='bold')
    draw_arrow(ax, px + pw/2, y, bx + bw/2, y, label='MSG', label_fs=9)
    draw_dashed_arrow(ax, bx + bw/2, y - 0.6, 7.5, y - 0.6)
    draw_cross(ax, 7.8, y - 0.6, size=0.2)
    ax.text(8.2, y - 0.55, 'UTRACONA', fontsize=9, fontweight='bold')
    ax.text(8.2, y - 1.0, '(brak retransmisji)', fontsize=8, style='italic')

    # Summary
    ax.text(6.0, 0.5, 'Brak ACK, brak retransmisji. Najszybszy. Use case: logi, metryki, telemetria.',
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=GRAY4, edgecolor=GRAY3))

    save(fig, 'pubsub_qos_at_most_once.png')


# ============================================================
# 6. At-least-once (QoS 1)
# ============================================================
def draw_qos_at_least_once():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, 5.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('QoS: At-least-once — „powtarzaj aż potwierdzą" (≥1 dostarczenie)',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    bx, bw = 3.5, 2.2
    sx, sw = 8.0, 2.2
    bh = 0.8
    draw_box(ax, bx, 5.5, bw, bh, 'Broker', fill=GRAY2, fontsize=10, fontweight='bold')
    draw_box(ax, sx, 5.5, sw, bh, 'Subscriber', fill=GRAY1, fontsize=10, fontweight='bold')

    # Timelines
    for xc in [bx + bw/2, sx + sw/2]:
        ax.plot([xc, xc], [5.5, 0.8], color=GRAY3, lw=1, linestyle=':')

    # Step 1: send MSG
    y1 = 4.8
    draw_arrow(ax, bx + bw/2, y1, sx + sw/2, y1, label='MSG #1', label_fs=9)
    draw_check(ax, sx + sw + 0.2, y1, size=0.15)
    ax.text(sx + sw + 0.5, y1, 'odebrano', fontsize=8)

    # Step 2: ACK lost
    y2 = 3.9
    draw_dashed_arrow(ax, sx + sw/2, y2, bx + bw + 1.2, y2)
    ax.text((bx + bw/2 + sx + sw/2)/2, y2 + 0.18, 'ACK', fontsize=9)
    draw_cross(ax, bx + bw + 0.8, y2, size=0.18)
    ax.text(bx + 0.3, y2 - 0.35, 'ACK utracony!', fontsize=8.5, style='italic')

    # Step 3: timeout → retry
    y3 = 2.9
    ax.text(bx + bw/2, y3 + 0.45, 'timeout...', fontsize=8.5, style='italic', ha='center')
    draw_arrow(ax, bx + bw/2, y3, sx + sw/2, y3, label='MSG #1 (retry)', label_fs=9)
    draw_check(ax, sx + sw + 0.2, y3, size=0.15)
    ax.text(sx + sw + 0.5, y3, 'odebrano\n(ponownie!)', fontsize=8)

    # Step 4: ACK ok
    y4 = 2.0
    draw_arrow(ax, sx + sw/2, y4, bx + bw/2, y4, label='ACK', label_fs=9)
    draw_check(ax, bx + bw/2 - 0.5, y4, size=0.18)

    # Duplicate bracket
    ax.annotate('', xy=(sx + sw + 1.3, y1), xytext=(sx + sw + 1.3, y3),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(sx + sw + 1.6, (y1 + y3)/2, 'DUPLIKAT!\nSubscriber\notrzymał 2×',
            fontsize=9, ha='left', va='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor=GRAY4, edgecolor=GRAY3))

    # Summary
    ax.text(6.0, 0.5, 'Broker czeka na ACK, retransmituje po timeout. Mogą być duplikaty!\n'
            'Use case: zamówienia, płatności (subscriber musi być idempotentny).',
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=GRAY4, edgecolor=GRAY3))

    save(fig, 'pubsub_qos_at_least_once.png')


# ============================================================
# 7. Exactly-once (QoS 2)
# ============================================================
def draw_qos_exactly_once():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('QoS: Exactly-once — 4-krokowy handshake (dokładnie 1 dostarczenie)',
                 fontsize=FS_TITLE, fontweight='bold', pad=12)

    bx, bw = 2.5, 2.2
    sx, sw = 7.5, 2.2
    bh = 0.8
    draw_box(ax, bx, 6.0, bw, bh, 'Broker', fill=GRAY2, fontsize=10, fontweight='bold')
    draw_box(ax, sx, 6.0, sw, bh, 'Subscriber', fill=GRAY1, fontsize=10, fontweight='bold')

    # Timelines
    for xc in [bx + bw/2, sx + sw/2]:
        ax.plot([xc, xc], [6.0, 1.0], color=GRAY3, lw=1, linestyle=':')

    # 4-step handshake
    steps = [
        (5.2, 'right', 'PUBLISH  (msg_id=42)',       'Broker wysyła wiadomość'),
        (4.2, 'left',  'PUBREC  (otrzymałem id=42)', 'Sub potwierdza odbiór, zapisuje id'),
        (3.2, 'right', 'PUBREL  (możesz przetworzyć)', 'Broker zwalnia wiadomość'),
        (2.2, 'left',  'PUBCOMP  (zakończone)',       'Sub potwierdza przetworzenie'),
    ]

    for i, (y, direction, label, desc) in enumerate(steps):
        # Step number
        ax.text(bx + bw/2 - 0.7, y, f'{i+1}', fontsize=9,
                fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle='circle,pad=0.18', facecolor=GRAY3, edgecolor=LN))

        if direction == 'right':
            draw_arrow(ax, bx + bw/2, y, sx + sw/2, y, label=label, label_fs=9)
        else:
            draw_arrow(ax, sx + sw/2, y, bx + bw/2, y, label=label, label_fs=9)

        # Side description
        ax.text(sx + sw + 0.3, y, desc, fontsize=8, ha='left', va='center', style='italic')

    # Summary
    ax.text(6.0, 0.6, 'Deduplikacja po msg_id. Sub nie przetwarza przed PUBREL.\n'
            'Najkosztowniejszy (4 pakiety). Use case: transakcje finansowe, krytyczne zdarzenia.',
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=GRAY4, edgecolor=GRAY3))

    save(fig, 'pubsub_qos_exactly_once.png')


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating Pub/Sub diagrams (7 separate images)...")
    draw_sub_topic()
    draw_sub_content()
    draw_sub_type()
    draw_sub_hierarchical()
    draw_qos_at_most_once()
    draw_qos_at_least_once()
    draw_qos_exactly_once()
    print("Done!")
