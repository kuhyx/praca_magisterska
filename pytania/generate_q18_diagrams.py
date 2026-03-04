#!/usr/bin/env python3
"""
Generate EOQ diagrams for PYTANIE 18: Zarządzanie zapasami w łańcuchu dostaw.
Monochrome, A4-printable PNGs (300 DPI).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

DPI = 300
BG = 'white'
LN = 'black'
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_sawtooth_inventory():
    """Sawtooth inventory diagram showing Q dropping to 0 across cycles,
    with Q/2 average line and delivery markers."""

    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=DPI, facecolor=BG)

    Q = 1000
    n_cycles = 4
    cycle_len = 1.0  # arbitrary time unit per cycle

    for i in range(n_cycles):
        t_start = i * cycle_len
        t_end = (i + 1) * cycle_len
        ax.plot([t_start, t_end], [Q, 0], color=LN, lw=2, solid_capstyle='round')
        # Vertical jump at delivery (except the very first which starts at t=0)
        if i > 0:
            ax.plot([t_start, t_start], [0, Q], color=LN, lw=2,
                    linestyle='--', alpha=0.5)

    # Average inventory line
    ax.axhline(y=Q / 2, color='gray', linestyle='-.', lw=1.2, zorder=0)
    ax.text(n_cycles * cycle_len * 1.02, Q / 2,
            f'średni zapas = Q/2 = {Q // 2}',
            va='center', ha='left', fontsize=8, color='gray')

    # Delivery markers
    for i in range(n_cycles):
        ax.plot(i * cycle_len, Q, 'ko', markersize=5, zorder=5)
        ax.annotate('dostawa', xy=(i * cycle_len, Q),
                    xytext=(i * cycle_len + 0.05, Q + 60),
                    fontsize=7, ha='left', color='black',
                    arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

    # Labels
    ax.set_xlabel('Czas', fontsize=10)
    ax.set_ylabel('Poziom zapasu', fontsize=10)
    ax.set_title('Model EOQ — piłokształtny przebieg zapasu', fontsize=11,
                 fontweight='bold', pad=10)

    ax.set_xlim(-0.1, n_cycles * cycle_len + 0.6)
    ax.set_ylim(-50, Q + 150)
    ax.set_yticks([0, Q // 2, Q])
    ax.set_yticklabels(['0', 'Q/2', 'Q'], fontsize=9)
    ax.set_xticks([i * cycle_len for i in range(n_cycles + 1)])
    ax.set_xticklabels([f'T{i}' for i in range(n_cycles + 1)], fontsize=9)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'q18_eoq_sawtooth.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'Saved: {path}')


def generate_cost_curves():
    """EOQ cost curve: ordering cost, holding cost, and total cost
    with optimum Q* marked."""

    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=DPI, facecolor=BG)

    D = 10000
    K = 100
    h = 2
    Q_star = np.sqrt(2 * K * D / h)  # 1000

    Q = np.linspace(200, 2500, 500)
    ordering = K * D / Q
    holding = h * Q / 2
    total = ordering + holding

    ax.plot(Q, ordering, color='black', lw=1.8, linestyle='--',
            label='Koszt zamawiania  K·D/Q')
    ax.plot(Q, holding, color='black', lw=1.8, linestyle=':',
            label='Koszt utrzymania  h·Q/2')
    ax.plot(Q, total, color='black', lw=2.5, linestyle='-',
            label='Koszt całkowity  TC(Q)')

    # Mark optimum
    TC_star = np.sqrt(2 * K * D * h)
    ax.plot(Q_star, TC_star, 'ko', markersize=8, zorder=5)
    ax.annotate(f'Q* = {int(Q_star)}\nTC* = {int(TC_star)} PLN',
                xy=(Q_star, TC_star),
                xytext=(Q_star + 300, TC_star + 600),
                fontsize=9, fontweight='bold', ha='left',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#F0F0F0',
                          edgecolor='black', lw=0.8))

    # Vertical dashed line from Q* to x-axis
    ax.plot([Q_star, Q_star], [0, TC_star], color='gray', linestyle='-.',
            lw=0.8, zorder=0)

    # Show that ordering = holding at Q*
    cross_y = K * D / Q_star  # = h * Q_star / 2 = 1000
    ax.annotate('koszt zamawiania\n= koszt utrzymania',
                xy=(Q_star, cross_y),
                xytext=(Q_star - 500, cross_y + 800),
                fontsize=7.5, ha='center', style='italic',
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.8),
                color='gray')

    ax.set_xlabel('Wielkość zamówienia Q [szt]', fontsize=10)
    ax.set_ylabel('Koszt roczny [PLN]', fontsize=10)
    ax.set_title('Model EOQ — krzywe kosztów', fontsize=11,
                 fontweight='bold', pad=10)

    ax.legend(loc='upper right', fontsize=8.5, framealpha=0.9,
              edgecolor='black')
    ax.set_xlim(100, 2600)
    ax.set_ylim(0, 5500)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'q18_eoq_cost_curves.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'Saved: {path}')


if __name__ == '__main__':
    generate_sawtooth_inventory()
    generate_cost_curves()
    print('Done — all Q18 diagrams generated.')
