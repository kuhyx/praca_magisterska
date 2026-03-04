#!/usr/bin/env python3
"""
Generate thesis-bridge diagrams for exam questions.
Shows how exam concepts connect to the master's thesis
(Unity vs Unreal game engine comparison).

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
FS = 9
FS_TITLE = 13
FS_SMALL = 7.5
FS_TINY = 6.5
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
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                              lw=lw, edgecolor=LN, facecolor=fill)
    else:
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                        lw=lw, edgecolor=LN, facecolor=fill)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha=ha, va=va, fontsize=fontsize,
            fontweight=fontweight, wrap=True,
            bbox=dict(facecolor='none', edgecolor='none', pad=0))
    return rect


def arrow(ax, x1, y1, x2, y2, style='->', lw=1.2, color=LN):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, lw=lw, color=color))


# ─────────────────────────────────────────────────────────────
# DIAGRAM 1: Game Engine Thread Architecture (for Q9)
# ─────────────────────────────────────────────────────────────
def draw_game_engine_threads():
    fig, ax = plt.subplots(1, 1, figsize=(8, 5.5), dpi=DPI)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(5, 6.7, 'Wątki w silniku gier — Game Loop Architecture',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    # Main Game Loop box
    draw_box(ax, 0.3, 5.0, 9.4, 1.3, '', fill=GRAY4, lw=2)
    ax.text(5, 6.0, 'GAME LOOP (Main Thread)', ha='center',
            fontsize=FS, fontweight='bold')
    ax.text(5, 5.45, 'Input → Update → Physics → Render → Present   (every frame)',
            ha='center', fontsize=FS_SMALL)

    # Sub-threads
    threads = [
        (0.5, 3.2, 2.0, 1.4, 'Render\nThread', GRAY1,
         'GPU commands\nDraw calls\nShader dispatch'),
        (2.8, 3.2, 2.0, 1.4, 'Physics\nThread', GRAY2,
         'Collision detection\nRigidbody sim\nRaycast'),
        (5.1, 3.2, 2.0, 1.4, 'Audio\nThread', GRAY1,
         'Sound mixing\nDSP effects\n3D spatialization'),
        (7.4, 3.2, 2.0, 1.4, 'Worker Pool\n(Job System)', GRAY2,
         'AI pathfinding\nAnimation\nAsset loading'),
    ]

    for x, y, w, h, label, fill, detail in threads:
        draw_box(ax, x, y, w, h, '', fill=fill)
        ax.text(x + w/2, y + h - 0.3, label, ha='center', fontsize=FS,
                fontweight='bold')
        ax.text(x + w/2, y + 0.3, detail, ha='center', fontsize=FS_TINY,
                color='#333333')
        arrow(ax, x + w/2, 5.0, x + w/2, y + h, '->', lw=1.0)

    # Engine comparison
    draw_box(ax, 0.3, 0.5, 4.3, 2.3, '', fill=WHITE, lw=1.5)
    ax.text(2.45, 2.5, 'UNITY', ha='center', fontsize=FS, fontweight='bold')
    ax.text(2.45, 2.0, 'C# + Job System (DOTS)', ha='center', fontsize=FS_SMALL)
    ax.text(2.45, 1.6, 'Main thread: MonoBehaviour', ha='center', fontsize=FS_SMALL)
    ax.text(2.45, 1.2, 'Workers: Burst Compiler', ha='center', fontsize=FS_SMALL)
    ax.text(2.45, 0.8, 'GC pauses freeze main thread!', ha='center',
            fontsize=FS_SMALL, fontweight='bold', style='italic')

    draw_box(ax, 5.4, 0.5, 4.3, 2.3, '', fill=WHITE, lw=1.5)
    ax.text(7.55, 2.5, 'UNREAL ENGINE', ha='center', fontsize=FS, fontweight='bold')
    ax.text(7.55, 2.0, 'C++ + TaskGraph', ha='center', fontsize=FS_SMALL)
    ax.text(7.55, 1.6, 'GameThread + RenderThread', ha='center', fontsize=FS_SMALL)
    ax.text(7.55, 1.2, 'Parallel rendering pipeline', ha='center', fontsize=FS_SMALL)
    ax.text(7.55, 0.8, 'No GC — deterministic timing', ha='center',
            fontsize=FS_SMALL, fontweight='bold', style='italic')

    out = os.path.join(OUTPUT_DIR, 'q9_game_engine_threads.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 2: Memory Management — Unity GC vs Unreal Manual (Q10)
# ─────────────────────────────────────────────────────────────
def draw_memory_gc_vs_manual():
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), dpi=DPI)
    fig.patch.set_facecolor(BG)
    fig.suptitle('Zarządzanie pamięcią w silnikach gier — GC vs Manual',
                 fontsize=FS_TITLE, fontweight='bold', y=0.98)

    # Left: Unity GC
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Unity (C# — Garbage Collector)', fontsize=FS, fontweight='bold', pad=10)

    # Heap visualization
    colors = [GRAY1, GRAY3, GRAY1, WHITE, GRAY3, GRAY1, WHITE, GRAY3, GRAY1, WHITE]
    labels = ['Obj', 'Bullet', 'Obj', 'FREE', 'Enemy', 'Obj', 'FREE', 'Bullet', 'Obj', 'FREE']
    for i, (c, l) in enumerate(zip(colors, labels)):
        y = 8.5 - i * 0.7
        draw_box(ax, 1, y, 5, 0.6, l, fill=c, fontsize=FS_SMALL)

    ax.text(0.5, 9.3, 'MANAGED HEAP', ha='left', fontsize=FS, fontweight='bold')
    ax.text(7, 9.0, 'Problem:', ha='left', fontsize=FS, fontweight='bold')
    ax.text(7, 8.4, '• GC pause (stop-the-world)', ha='left', fontsize=FS_TINY)
    ax.text(7, 7.9, '• Fragmentacja heapa', ha='left', fontsize=FS_TINY)
    ax.text(7, 7.4, '• Spike\'y w frame time', ha='left', fontsize=FS_TINY)
    ax.text(7, 6.6, 'Rozwiązanie:', ha='left', fontsize=FS, fontweight='bold')
    ax.text(7, 6.0, '• Object Pooling!', ha='left', fontsize=FS_TINY,
            fontweight='bold')
    ax.text(7, 5.5, '  (BulletPool.cs)', ha='left', fontsize=FS_TINY,
            style='italic')
    ax.text(7, 5.0, '• Unikaj new w Update()', ha='left', fontsize=FS_TINY)
    ax.text(7, 4.5, '• Incremental GC (2019+)', ha='left', fontsize=FS_TINY)

    # GC arrow
    ax.annotate('GC\nPAUSE', xy=(3.5, 2.5), fontsize=FS,
                fontweight='bold', ha='center', color='black',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY3))

    # Right: Unreal Manual
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Unreal Engine (C++ — Manual / Smart Pointers)', fontsize=FS, fontweight='bold', pad=10)

    # Memory blocks - organized
    segments = [
        (8.5, 'TSharedPtr<T>', GRAY1, 'Reference-counted'),
        (7.5, 'TUniquePtr<T>', GRAY2, 'Exclusive ownership'),
        (6.5, 'TWeakPtr<T>', GRAY1, 'Non-owning observer'),
        (5.5, 'FMemory::Malloc', GRAY3, 'Raw allocation'),
        (4.5, 'UObject (GC)', GRAY2, 'Reflected objects'),
    ]

    ax.text(0.5, 9.3, 'MEMORY MODEL', ha='left', fontsize=FS, fontweight='bold')
    for y, label, fill, desc in segments:
        draw_box(ax, 1, y, 3.5, 0.7, label, fill=fill, fontsize=FS_SMALL,
                 fontweight='bold')
        ax.text(5, y + 0.35, f'← {desc}', ha='left', fontsize=FS_TINY, va='center')

    ax.text(7, 9.0, 'Zalety:', ha='left', fontsize=FS, fontweight='bold')
    ax.text(7, 8.4, '• Deterministic destruction', ha='left', fontsize=FS_TINY)
    ax.text(7, 7.9, '• Brak GC pauses', ha='left', fontsize=FS_TINY)
    ax.text(7, 7.4, '• Custom allocators', ha='left', fontsize=FS_TINY)
    ax.text(7, 6.6, 'Cena:', ha='left', fontsize=FS, fontweight='bold')
    ax.text(7, 6.0, '• Manual lifecycle mgmt', ha='left', fontsize=FS_TINY)
    ax.text(7, 5.5, '• Use-after-free risk', ha='left', fontsize=FS_TINY)
    ax.text(7, 5.0, '• Memory leaks possible', ha='left', fontsize=FS_TINY)

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    out = os.path.join(OUTPUT_DIR, 'q10_gc_vs_manual_memory.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 3: Object Pooling — BulletPool pattern (Q10)
# ─────────────────────────────────────────────────────────────
def draw_object_pooling():
    fig, ax = plt.subplots(1, 1, figsize=(9, 4.5), dpi=DPI)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(6, 5.7, 'Object Pooling — eliminacja alokacji w runtime',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    # WITHOUT pool
    draw_box(ax, 0.2, 3.2, 5.4, 2.2, '', fill=GRAY4, lw=1.5)
    ax.text(2.9, 5.0, 'BEZ POOLINGU', ha='center', fontsize=FS, fontweight='bold')
    ax.text(2.9, 4.5, 'Spawn() → new Bullet()   [ALLOC]', ha='center', fontsize=FS_SMALL)
    ax.text(2.9, 4.1, 'Despawn() → Destroy()    [FREE → GC]', ha='center', fontsize=FS_SMALL)
    ax.text(2.9, 3.6, '1000 bullets × 60 fps = 60k alloc/s', ha='center',
            fontsize=FS_SMALL, fontweight='bold', color='#333333')

    # WITH pool
    draw_box(ax, 6.4, 3.2, 5.4, 2.2, '', fill=WHITE, lw=1.5)
    ax.text(9.1, 5.0, 'Z OBJECT POOL', ha='center', fontsize=FS, fontweight='bold')
    ax.text(9.1, 4.5, 'Spawn() → pool.Get()     [REUSE]', ha='center', fontsize=FS_SMALL)
    ax.text(9.1, 4.1, 'Despawn() → pool.Return() [RECYCLE]', ha='center', fontsize=FS_SMALL)
    ax.text(9.1, 3.6, '0 alloc/s w steady state', ha='center',
            fontsize=FS_SMALL, fontweight='bold', color='#333333')

    # Pool visualization
    draw_box(ax, 2.5, 0.5, 7, 2.2, '', fill=GRAY1, lw=1.5)
    ax.text(6, 2.3, 'BulletPool (pre-allocated)', ha='center', fontsize=FS, fontweight='bold')

    pool_states = ['ACTIVE', 'ACTIVE', 'IDLE', 'IDLE', 'ACTIVE', 'IDLE', 'ACTIVE', 'IDLE']
    for i, state in enumerate(pool_states):
        x = 3.0 + i * 0.75
        fill = GRAY3 if state == 'ACTIVE' else WHITE
        draw_box(ax, x, 0.8, 0.6, 0.6, '', fill=fill, fontsize=FS_TINY)
        ax.text(x + 0.3, 1.6, state[0], ha='center', fontsize=FS_TINY,
                fontweight='bold')

    ax.text(10.3, 1.1, 'A = Active\nI = Idle', ha='left', fontsize=FS_TINY)

    out = os.path.join(OUTPUT_DIR, 'q10_object_pooling.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 4: OOP Composition in game engines (Q6)
# ─────────────────────────────────────────────────────────────
def draw_component_pattern():
    fig, ax = plt.subplots(1, 1, figsize=(9, 6), dpi=DPI)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(6, 7.7, 'Composition over Inheritance — Component Pattern w silnikach gier',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    # LEFT: Inheritance (bad)
    draw_box(ax, 0.3, 5.0, 5.0, 2.3, '', fill=GRAY4, lw=1.5)
    ax.text(2.8, 6.9, '[X] Dziedziczenie — kruche', ha='center',
            fontsize=FS, fontweight='bold')
    hierarchy = [
        (1.5, 6.2, 'GameObject'),
        (0.5, 5.5, 'Enemy'),
        (2.5, 5.5, 'FlyingEnemy'),
        (3.8, 5.5, 'ShootingFlyingEnemy??'),
    ]
    for x, y, label in hierarchy:
        draw_box(ax, x, y, 1.8 if '??' not in label else 2.5,
                 0.5, label, fill=WHITE, fontsize=FS_TINY)

    arrow(ax, 1.4, 5.75, 2.4, 6.2, '->', lw=0.8)
    arrow(ax, 3.4, 5.75, 2.9, 6.2, '->', lw=0.8)

    # RIGHT: Composition (good)
    draw_box(ax, 6.5, 3.7, 5.2, 3.8, '', fill=WHITE, lw=1.5)
    ax.text(9.1, 7.1, '[OK] Kompozycja — Component Pattern', ha='center',
            fontsize=FS, fontweight='bold')

    # Entity
    draw_box(ax, 7.5, 6.0, 3.2, 0.7, 'GameObject / AActor', fill=GRAY1,
             fontsize=FS_SMALL, fontweight='bold')

    # Components
    comps = [
        (6.8, 5.0, 'Transform'),
        (8.4, 5.0, 'SpriteRenderer'),
        (6.8, 4.3, 'Health'),
        (8.4, 4.3, 'BulletSpawner'),
        (6.8, 3.6, 'EnemyAI'),
        (8.4, 3.6, 'Collider2D'),
    ]
    for x, y, label in comps:
        draw_box(ax, x, y + 0.1, 1.5, 0.45, label, fill=GRAY2, fontsize=FS_TINY)
        arrow(ax, x + 0.75, y + 0.55, 9.1, 6.0, '->', lw=0.5, color='#666666')

    # Comparison table
    draw_box(ax, 0.3, 0.3, 11.4, 3.0, '', fill=GRAY4, lw=1.0)
    ax.text(6, 3.0, 'Unity vs Unreal — mechanizmy reużywalności', ha='center',
            fontsize=FS, fontweight='bold')

    table_data = [
        ('Mechanizm', 'Unity (C#)', 'Unreal (C++)'),
        ('Kompozycja', 'MonoBehaviour + GetComponent<T>()', 'UActorComponent'),
        ('Generics', 'List<T>, Dictionary<K,V>', 'TArray<T>, TMap<K,V>'),
        ('Interfejsy', 'interface IDamageable', 'UInterface'),
        ('Wzorce', 'Singleton, Observer (events)', 'Singleton, Delegate'),
        ('Pool', 'ObjectPool<T> / custom', 'FPooledObject / custom'),
    ]

    for i, (mech, unity_col, unreal_col) in enumerate(table_data):
        y_row = 2.55 - i * 0.4
        weight = 'bold' if i == 0 else 'normal'
        ax.text(1.8, y_row, mech, ha='center', fontsize=FS_TINY, fontweight=weight)
        ax.text(5.5, y_row, unity_col, ha='center', fontsize=FS_TINY, fontweight=weight)
        ax.text(9.5, y_row, unreal_col, ha='center', fontsize=FS_TINY, fontweight=weight)

    # Column separator lines
    ax.plot([3.5, 3.5], [0.5, 2.8], color=LN, lw=0.5, ls='--')
    ax.plot([7.5, 7.5], [0.5, 2.8], color=LN, lw=0.5, ls='--')
    ax.plot([0.5, 11.5], [2.3, 2.3], color=LN, lw=0.5)

    out = os.path.join(OUTPUT_DIR, 'q6_component_pattern_engines.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 5: STL vs Unreal Containers (Q5)
# ─────────────────────────────────────────────────────────────
def draw_stl_vs_unreal():
    fig, ax = plt.subplots(1, 1, figsize=(9, 5), dpi=DPI)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(6, 6.7, 'STL vs Unreal Engine Containers — porównanie',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    # Table
    rows = [
        ('Kategoria', 'C++ STL', 'Unreal Engine (C++)', 'Dlaczego UE zmienił?'),
        ('Tablica dynamiczna', 'std::vector<T>', 'TArray<T>', 'Custom allocator, reflection'),
        ('Hash map', 'std::unordered_map', 'TMap<K,V>', 'Gameplay serialization'),
        ('Hash set', 'std::unordered_set', 'TSet<T>', 'UPROPERTY support'),
        ('String', 'std::string', 'FString / FName / FText', 'FName: hashed, immutable (IDs)'),
        ('Smart pointer', 'shared_ptr<T>', 'TSharedPtr<T>', 'Thread-safe by default'),
        ('Optional', 'std::optional<T>', 'TOptional<T>', 'UE coding standard'),
        ('Iteratory', 'begin()/end()', 'begin()/end() (compatible)', 'Range-based for works'),
        ('Algorytmy', '<algorithm>', 'Algo:: namespace', 'Reduced header bloat'),
    ]

    y_start = 6.1
    row_h = 0.55
    col_x = [0.3, 2.5, 5.0, 7.5, 10.8]

    for i, (cat, stl, ue, why) in enumerate(rows):
        y = y_start - i * row_h
        fill = GRAY2 if i == 0 else (GRAY4 if i % 2 == 0 else WHITE)
        draw_box(ax, 0.2, y - 0.05, 11.6, row_h - 0.05, '', fill=fill,
                 lw=0.5, rounded=False)
        weight = 'bold' if i == 0 else 'normal'
        ax.text(col_x[0], y + row_h/2 - 0.05, cat, ha='left', fontsize=FS_TINY,
                fontweight=weight)
        ax.text(col_x[1], y + row_h/2 - 0.05, stl, ha='left', fontsize=FS_TINY,
                fontweight=weight, family='monospace' if i > 0 else 'sans-serif')
        ax.text(col_x[2], y + row_h/2 - 0.05, ue, ha='left', fontsize=FS_TINY,
                fontweight=weight, family='monospace' if i > 0 else 'sans-serif')
        ax.text(col_x[3], y + row_h/2 - 0.05, why, ha='left', fontsize=FS_TINY,
                fontweight=weight)

    # Bottom note
    ax.text(6, 0.6, 'Kluczowy wniosek: Unreal NIE używa STL — ma własne kontenery z identycznym API\n'
                     'ale dodatkowym wsparciem dla refleksji (UPROPERTY), serializacji i GC obiektów UObject.',
            ha='center', fontsize=FS_SMALL, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=GRAY4, edgecolor=LN, lw=0.8))

    out = os.path.join(OUTPUT_DIR, 'q5_stl_vs_unreal.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 6: Amdahl in Game Engine Rendering Pipeline (Q25)
# ─────────────────────────────────────────────────────────────
def draw_amdahl_game_pipeline():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5.5), dpi=DPI)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(6.5, 7.2, 'Prawo Amdahla w silniku gier — co można zrównoleglić?',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    # Pipeline stages — frame budget
    stages = [
        ('Input\n(seq)', 0.5, WHITE, True),
        ('Game Logic\n(seq)', 2.0, GRAY1, True),
        ('Physics\n(parallel)', 2.0, GRAY3, False),
        ('Animation\n(parallel)', 1.5, GRAY3, False),
        ('Culling\n(parallel)', 1.0, GRAY3, False),
        ('Rendering\n(parallel)', 3.0, GRAY3, False),
        ('Post-process\n(GPU)', 1.5, GRAY2, False),
        ('Present\n(seq)', 0.5, WHITE, True),
    ]

    x = 0.3
    y = 5.0
    h = 1.2
    for label, width, fill, is_seq in stages:
        draw_box(ax, x, y, width, h, label, fill=fill, fontsize=FS_TINY,
                 fontweight='bold' if is_seq else 'normal')
        if is_seq:
            ax.text(x + width/2, y - 0.25, 'SEQ', ha='center', fontsize=FS_TINY,
                    fontweight='bold')
        else:
            ax.text(x + width/2, y - 0.25, 'PAR', ha='center', fontsize=FS_TINY,
                    color='#444444')
        x += width + 0.15

    ax.text(6.5, 6.5, '← 16.67 ms frame budget @ 60 FPS →',
            ha='center', fontsize=FS_SMALL, style='italic')

    # Amdahl calculation
    draw_box(ax, 0.3, 1.5, 12.3, 2.8, '', fill=GRAY4, lw=1.5)
    ax.text(6.5, 4.0, 'Amdahl w praktyce — profiling z NVIDIA Nsight',
            ha='center', fontsize=FS, fontweight='bold')

    calc_lines = [
        'Sekwencyjna część (p_seq): Input + Game Logic + Present ≈ 25% frame time',
        'Równoległa część (p_par): Physics + Anim + Culling + Render ≈ 75% frame time',
        '',
        'S(n) = 1 / ((1 - p) + p/n)  →  S(4 cores) = 1 / (0.25 + 0.75/4) = 1 / 0.4375 ≈ 2.29x',
        'S(8 cores) ≈ 2.91x    S(16 cores) ≈ 3.37x    S(∞) = 1/0.25 = 4x MAX',
        '',
        'Wniosek: nawet z ∞ rdzeniami, 25% sekwencyjnego kodu limituje do 4x speedup!',
        'Nsight pozwala zmierzyć DOKŁADNIE ile czasu jest seq vs par per frame.',
    ]

    for i, line in enumerate(calc_lines):
        weight = 'bold' if 'Wniosek' in line or 'Nsight' in line else 'normal'
        ax.text(0.6, 3.5 - i * 0.28, line, ha='left', fontsize=FS_TINY,
                fontweight=weight, family='monospace' if '=' in line or '→' in line else 'sans-serif')

    out = os.path.join(OUTPUT_DIR, 'q25_amdahl_game_pipeline.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 7: Async/Sync in Game Engines — GPU/CPU (Q26)
# ─────────────────────────────────────────────────────────────
def draw_gpu_cpu_sync():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5.5), dpi=DPI)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(6.5, 7.2,
            'Synchroniczna vs Asynchroniczna komunikacja — CPU↔GPU w silnikach gier',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    # Timeline - Frame N
    ax.text(0.3, 6.5, 'Frame N', ha='left', fontsize=FS, fontweight='bold')

    # CPU timeline
    ax.text(0.3, 5.8, 'CPU:', ha='left', fontsize=FS, fontweight='bold')
    cpu_blocks = [
        (1.5, 5.5, 2.5, 0.6, 'Game Logic\n(Update)', GRAY1),
        (4.2, 5.5, 2.0, 0.6, 'Prepare\nDraw Calls', GRAY2),
        (6.4, 5.5, 1.5, 0.6, 'Submit to\nGPU', GRAY3),
        (8.1, 5.5, 2.5, 0.6, 'IDLE (wait)\nor next frame', WHITE),
    ]
    for x, y, w, h, label, fill in cpu_blocks:
        draw_box(ax, x, y, w, h, label, fill=fill, fontsize=FS_TINY)

    # GPU timeline
    ax.text(0.3, 4.6, 'GPU:', ha='left', fontsize=FS, fontweight='bold')
    gpu_blocks = [
        (1.5, 4.3, 3.5, 0.6, 'Rendering Frame N-1', GRAY3),
        (5.2, 4.3, 1.0, 0.6, 'IDLE', WHITE),
        (6.4, 4.3, 4.2, 0.6, 'Rendering Frame N', GRAY2),
    ]
    for x, y, w, h, label, fill in gpu_blocks:
        draw_box(ax, x, y, w, h, label, fill=fill, fontsize=FS_TINY)

    # Sync point
    ax.plot([6.4, 6.4], [4.3, 6.1], color=LN, lw=1.5, ls='--')
    ax.text(6.4, 6.2, 'SYNC\nPOINT', ha='center', fontsize=FS_TINY,
            fontweight='bold')

    # Comparison table
    draw_box(ax, 0.3, 0.5, 12.3, 3.3, '', fill=GRAY4, lw=1.0)
    ax.text(6.5, 3.5, 'Asynchroniczne mechanizmy w grach — analogia do MPI',
            ha='center', fontsize=FS, fontweight='bold')

    table = [
        ('Mechanizm', 'Sync/Async', 'Blokujący?', 'Analogia MPI', 'Silnik'),
        ('glFinish()', 'SYNC', 'TAK', 'MPI_Ssend', 'OpenGL'),
        ('Unity Coroutine', 'ASYNC', 'NIE', 'MPI_Isend+Wait', 'Unity'),
        ('C# async/await', 'ASYNC', 'NIE', 'MPI_Irecv+Wait', 'Unity'),
        ('GPU Fence', 'SYNC', 'TAK (check)', 'MPI_Barrier', 'Oba'),
        ('Command Buffer', 'ASYNC', 'NIE (queue)', 'MPI_Bsend', 'Oba'),
        ('UE TaskGraph', 'ASYNC', 'NIE (deps)', 'DAG scheduling', 'Unreal'),
    ]

    col_xs = [0.6, 3.8, 5.8, 7.8, 10.0]
    for i, row in enumerate(table):
        y = 3.0 - i * 0.33
        weight = 'bold' if i == 0 else 'normal'
        for j, val in enumerate(row):
            ax.text(col_xs[j], y, val, ha='left', fontsize=FS_TINY,
                    fontweight=weight)

    out = os.path.join(OUTPUT_DIR, 'q26_gpu_cpu_sync_async.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 8: Game Engine Architecture — C4 model (Q13/27)
# ─────────────────────────────────────────────────────────────
def draw_engine_c4():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6.5), dpi=DPI)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(6.5, 8.2,
            'Modelowanie architektury silnika gier — podejście C4',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    # Level 1: Context
    draw_box(ax, 0.3, 6.3, 12.3, 1.6, '', fill=GRAY4, lw=1.5)
    ax.text(6.5, 7.6, 'C1: Context — System w otoczeniu', ha='center',
            fontsize=FS, fontweight='bold')
    ctx_items = [
        (1.5, 6.5, 'Gracz\n(Input)'),
        (4.0, 6.5, 'Game Engine\n(Unity/Unreal)'),
        (7.0, 6.5, 'GPU / OS\n(Platform)'),
        (10.0, 6.5, 'Asset Pipeline\n(Blender, PS)'),
    ]
    for x, y, label in ctx_items:
        draw_box(ax, x, y, 2.0, 0.9, label, fill=WHITE, fontsize=FS_TINY)

    arrow(ax, 3.5, 6.95, 4.0, 6.95, '->')
    arrow(ax, 6.0, 6.95, 7.0, 6.95, '->')
    arrow(ax, 9.0, 6.95, 10.0, 6.95, '<-')

    # Level 2: Containers
    draw_box(ax, 0.3, 3.8, 12.3, 2.2, '', fill=WHITE, lw=1.5)
    ax.text(6.5, 5.7, 'C2: Containers — Główne podsystemy silnika',
            ha='center', fontsize=FS, fontweight='bold')
    containers = [
        (0.5, 4.0, 'Rendering\nEngine', GRAY3),
        (2.5, 4.0, 'Physics\nEngine', GRAY2),
        (4.5, 4.0, 'Scripting\nRuntime', GRAY1),
        (6.5, 4.0, 'Audio\nEngine', GRAY2),
        (8.5, 4.0, 'Scene\nGraph', GRAY1),
        (10.5, 4.0, 'Resource\nManager', GRAY3),
    ]
    for x, y, label, fill in containers:
        draw_box(ax, x, y, 1.8, 1.2, label, fill=fill, fontsize=FS_TINY,
                 fontweight='bold')

    # Level 3: Components (zoomed into Scripting Runtime)
    draw_box(ax, 0.3, 1.2, 12.3, 2.3, '', fill=GRAY4, lw=1.5)
    ax.text(6.5, 3.2, 'C3: Components — Porównanie Scripting Runtime',
            ha='center', fontsize=FS, fontweight='bold')

    # Unity side
    unity_comps = [
        (0.8, 1.4, 'Mono/.NET\nRuntime'),
        (2.8, 1.4, 'C# Scripts\n(MonoBehaviour)'),
        (4.8, 1.4, 'IL2CPP\n(AOT compile)'),
    ]
    ax.text(3.3, 2.7, 'UNITY', ha='center', fontsize=FS_SMALL, fontweight='bold')
    for x, y, label in unity_comps:
        draw_box(ax, x, y, 1.8, 0.9, label, fill=GRAY1, fontsize=FS_TINY)

    # Unreal side
    unreal_comps = [
        (7.3, 1.4, 'Native C++\nRuntime'),
        (9.3, 1.4, 'Blueprint\nVM'),
        (11.1, 1.4, 'UObject\nReflection'),
    ]
    ax.text(9.8, 2.7, 'UNREAL', ha='center', fontsize=FS_SMALL, fontweight='bold')
    for x, y, label in unreal_comps:
        draw_box(ax, x, y, 1.8, 0.9, label, fill=GRAY2, fontsize=FS_TINY)

    # Divider
    ax.plot([6.5, 6.5], [1.3, 3.0], color=LN, lw=1.0, ls='--')

    # ADR note
    ax.text(6.5, 0.6,
            'Kluczowe ADR-y: „C# z GC vs C++ manual" | „Component vs Actor model" | '
            '„Managed heap vs custom allocators"',
            ha='center', fontsize=FS_TINY, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=LN, lw=0.8))

    out = os.path.join(OUTPUT_DIR, 'q13_engine_c4_architecture.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
# DIAGRAM 9: Architectural Patterns in Game Engines (Q14/28)
# ─────────────────────────────────────────────────────────────
def draw_engine_patterns():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=DPI)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    ax.text(6.5, 7.7,
            'Wzorce architektoniczne w silnikach gier — mapa wzorców',
            ha='center', fontsize=FS_TITLE, fontweight='bold')

    patterns = [
        ('Component\nPattern', 1.0, 5.5, GRAY1,
         'Unity: MonoBehaviour\nUnreal: UActorComponent\n→ Composition over Inheritance'),
        ('Object Pool', 4.5, 5.5, GRAY2,
         'Unity: BulletPool.cs\nUnreal: FPooledObject\n→ Eliminacja GC spikes'),
        ('Observer /\nEvent-Driven', 8.0, 5.5, GRAY3,
         'Unity: C# event/delegate\nUnreal: FMulticastDelegate\n→ Loose coupling'),
        ('Singleton', 1.0, 3.0, GRAY2,
         'Unity: GameDirector.Instance\nUnreal: UGameInstance\n→ Global state access'),
        ('Game Loop', 4.5, 3.0, GRAY1,
         'Update() → FixedUpdate()\nTick() → TickComponent()\n→ Frame-based execution'),
        ('Entity-\nComponent-\nSystem (ECS)', 8.0, 3.0, GRAY3,
         'Unity DOTS / Burst\nUnreal Mass Entity\n→ Data-oriented, cache-friendly'),
    ]

    for label, x, y, fill, desc in patterns:
        draw_box(ax, x, y, 2.8, 1.8, '', fill=fill, lw=1.5)
        ax.text(x + 1.4, y + 1.45, label, ha='center', fontsize=FS_SMALL,
                fontweight='bold')
        lines = desc.split('\n')
        for i, line in enumerate(lines):
            ax.text(x + 1.4, y + 0.9 - i * 0.28, line, ha='center',
                    fontsize=FS_TINY)

    # Bottom: catalog mapping
    draw_box(ax, 0.3, 0.3, 12.3, 2.2, '', fill=GRAY4, lw=1.0)
    ax.text(6.5, 2.2, 'Katalogi wzorców — gdzie je znaleźć?', ha='center',
            fontsize=FS, fontweight='bold')
    catalog_info = [
        'Game Loop, Component, Object Pool  →  Game Programming Patterns (Robert Nystrom, 2014)',
        'Observer, Singleton, Strategy       →  GoF (Gang of Four, 1994)',
        'ECS, Data-Oriented Design           →  Unity DOTS docs / Mike Acton GDC 2014',
        'Event-Driven, Pub-Sub               →  EIP (Hohpe & Woolf, 2003)',
    ]
    for i, line in enumerate(catalog_info):
        ax.text(0.6, 1.8 - i * 0.35, line, ha='left', fontsize=FS_TINY)

    out = os.path.join(OUTPUT_DIR, 'q14_engine_patterns_map.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Generating thesis-bridge diagrams...')
    draw_game_engine_threads()
    draw_memory_gc_vs_manual()
    draw_object_pooling()
    draw_component_pattern()
    draw_stl_vs_unreal()
    draw_amdahl_game_pipeline()
    draw_gpu_cpu_sync()
    draw_engine_c4()
    draw_engine_patterns()
    print('Done! All diagrams in pytania/img/')
