#!/usr/bin/env python3
"""
Pygame GUI for shortest-path algorithm visualization.

Controls:
  1 / 2 / 3  — Dijkstra / Bellman-Ford / A*
  SPACE      — advance one step
  R          — reset
  Q / ESC    — quit
"""

import math
import sys
import pygame

from algorithms import (
    NODES, EDGES, GOAL, INF, AlgoState, heuristic,
    dijkstra_init, dijkstra_step,
    bellman_ford_init, bellman_ford_step,
    astar_init, astar_step,
)

# ─── Constants ───────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1100, 700
NODE_RADIUS = 28
FONT_SIZE = 18

# Colours
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
LIGHT_GREY  = (230, 230, 230)
DARK_GREY   = (100, 100, 100)
BLUE        = (60, 100, 220)
ORANGE      = (240, 140, 40)
VISITED_COL = (180, 220, 255)
PATH_COL    = (60, 200, 120)
CURRENT_COL = (255, 220, 80)
EDGE_DEFAULT= (160, 160, 160)
EDGE_RELAXED= (60, 160, 60)
EDGE_PATH   = (40, 180, 100)
BG          = (245, 245, 250)

ALGO_NAMES = ["Dijkstra's Algorithm", "Bellman-Ford Algorithm", "A* Algorithm"]
ALGOS = [
    (dijkstra_init, dijkstra_step),
    (bellman_ford_init, bellman_ford_step),
    (astar_init, astar_step),
]


# ─── Drawing ─────────────────────────────────────────────────────────────

def draw_edge(screen: pygame.Surface, p1: tuple, p2: tuple,
              colour: tuple, width: int = 2) -> None:
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    start = (p1[0] + ux * NODE_RADIUS, p1[1] + uy * NODE_RADIUS)
    end   = (p2[0] - ux * NODE_RADIUS, p2[1] - uy * NODE_RADIUS)
    pygame.draw.line(screen, colour, start, end, width)


def render(screen: pygame.Surface, font: pygame.font.Font,
           small_font: pygame.font.Font, state: AlgoState,
           algo_idx: int) -> None:
    screen.fill(BG)

    # Title
    title_surf = font.render(ALGO_NAMES[algo_idx], True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 10))

    # Path edge set
    path_edges: set[tuple[str, str]] = set()
    for i in range(len(state.path) - 1):
        a, b = state.path[i], state.path[i + 1]
        path_edges.add((a, b))
        path_edges.add((b, a))

    # Edges
    for u, v, w in EDGES:
        p1, p2 = NODES[u], NODES[v]
        if (u, v) in path_edges:
            col, wd = EDGE_PATH, 5
        elif (u, v) in state.relaxed_edges or (v, u) in state.relaxed_edges:
            col, wd = EDGE_RELAXED, 3
        else:
            col, wd = EDGE_DEFAULT, 2
        draw_edge(screen, p1, p2, col, wd)

        # Weight label
        mx = (p1[0] + p2[0]) // 2
        my = (p1[1] + p2[1]) // 2
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = math.hypot(dx, dy)
        if length > 0:
            mx += int(-dy / length * 14)
            my += int(dx / length * 14)
        wt = small_font.render(str(w), True, DARK_GREY)
        screen.blit(wt, (mx - wt.get_width() // 2, my - wt.get_height() // 2))

    # Nodes
    for name, (x, y) in NODES.items():
        if name in state.path and state.finished:
            col = PATH_COL
        elif name == state.current_node:
            col = CURRENT_COL
        elif name in state.visited:
            col = VISITED_COL
        else:
            col = WHITE

        pygame.draw.circle(screen, col, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, BLACK, (x, y), NODE_RADIUS, 2)

        # Name
        label = font.render(name, True, BLACK)
        screen.blit(label, (x - label.get_width() // 2,
                            y - label.get_height() // 2 - 8))

        # Distance
        d = state.dist.get(name, INF)
        d_text = "inf" if d == INF else f"{d:.0f}"
        d_surf = small_font.render(f"d={d_text}", True, BLUE)
        screen.blit(d_surf, (x - d_surf.get_width() // 2, y + 8))

        # h(n) for A*
        if algo_idx == 2:
            h_surf = small_font.render(f"h={heuristic(name):.1f}", True, ORANGE)
            screen.blit(h_surf, (x + NODE_RADIUS + 4, y - 8))

    # Info bar
    pygame.draw.rect(screen, LIGHT_GREY, (0, HEIGHT - 80, WIDTH, 80))
    pygame.draw.line(screen, DARK_GREY, (0, HEIGHT - 80), (WIDTH, HEIGHT - 80), 2)

    info = font.render(state.message, True, BLACK)
    screen.blit(info, (20, HEIGHT - 70))

    hint = small_font.render(
        "[1] Dijkstra  [2] Bellman-Ford  [3] A*  "
        "[SPACE] Step  [R] Reset  [Q] Quit", True, DARK_GREY)
    screen.blit(hint, (20, HEIGHT - 35))

    pygame.display.flip()


# ─── Main ────────────────────────────────────────────────────────────────

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shortest Path Visualizer — Dijkstra / Bellman-Ford / A*")
    font = pygame.font.SysFont("DejaVu Sans", FONT_SIZE, bold=True)
    small_font = pygame.font.SysFont("DejaVu Sans", FONT_SIZE - 4)
    clock = pygame.time.Clock()

    current = 0
    state = ALGOS[current][0]()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                elif event.key == pygame.K_1:
                    current = 0; state = ALGOS[current][0]()
                elif event.key == pygame.K_2:
                    current = 1; state = ALGOS[current][0]()
                elif event.key == pygame.K_3:
                    current = 2; state = ALGOS[current][0]()
                elif event.key == pygame.K_r:
                    state = ALGOS[current][0]()
                elif event.key == pygame.K_SPACE:
                    if not state.finished:
                        ALGOS[current][1](state)

        render(screen, font, small_font, state, current)
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
