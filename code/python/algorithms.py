"""
Shortest-path algorithms: Dijkstra, Bellman-Ford, A*
Pure implementations — no GUI dependencies.
"""

import heapq
import math
from dataclasses import dataclass, field
from typing import Optional

INF = float("inf")

# ─── Graph ───────────────────────────────────────────────────────────────

NODES: dict[str, tuple[int, int]] = {
    "S": (80, 350),  "A": (270, 130), "B": (270, 570),
    "C": (500, 80),  "D": (500, 350), "E": (500, 620),
    "F": (730, 180),  "G": (730, 520), "T": (950, 350),
}

EDGES: list[tuple[str, str, int]] = [
    ("S", "A", 4),  ("S", "B", 2),  ("A", "C", 5),  ("A", "D", 10),
    ("B", "D", 3),  ("B", "E", 8),  ("C", "F", 3),  ("D", "F", 7),
    ("D", "G", 4),  ("E", "G", 2),  ("F", "T", 4),  ("G", "T", 6),
    ("C", "D", 2),
]

ADJ: dict[str, list[tuple[str, int]]] = {n: [] for n in NODES}
for _u, _v, _w in EDGES:
    ADJ[_u].append((_v, _w))
    ADJ[_v].append((_u, _w))

SOURCE = "S"
GOAL = "T"


def heuristic(node: str) -> float:
    x1, y1 = NODES[node]
    x2, y2 = NODES[GOAL]
    return math.hypot(x2 - x1, y2 - y1) / 100


# ─── State ───────────────────────────────────────────────────────────────

@dataclass
class AlgoState:
    dist: dict[str, float] = field(default_factory=dict)
    prev: dict[str, Optional[str]] = field(default_factory=dict)
    visited: set[str] = field(default_factory=set)
    finished: bool = False
    step: int = 0
    message: str = ""
    path: list[str] = field(default_factory=list)
    relaxed_edges: set[tuple[str, str]] = field(default_factory=set)
    current_node: Optional[str] = None
    f_score: dict[str, float] = field(default_factory=dict)
    frontier: list = field(default_factory=list)  # heap for Dijkstra/A*
    bf_iteration: int = 0

    def _reconstruct_path(self) -> None:
        path: list[str] = []
        node: Optional[str] = GOAL
        while node is not None:
            path.append(node)
            node = self.prev.get(node)
        path.reverse()
        self.path = path if path and path[0] == SOURCE else []


# ─── Dijkstra ────────────────────────────────────────────────────────────

def dijkstra_init() -> AlgoState:
    st = AlgoState()
    st.dist = {n: INF for n in NODES}
    st.prev = {n: None for n in NODES}
    st.dist[SOURCE] = 0
    st.frontier = [(0, SOURCE)]
    st.message = f"Dijkstra: start from {SOURCE}, dist[{SOURCE}]=0"
    return st


def dijkstra_step(st: AlgoState) -> None:
    if st.finished or not st.frontier:
        st.finished = True
        st._reconstruct_path()
        c = st.dist.get(GOAL, INF)
        st.message = (f"Dijkstra done! Path: {'→'.join(st.path)}, cost={c:.0f}"
                      if st.path else "Dijkstra done! No path.")
        return

    st.current_node = None
    while st.frontier:
        d, u = heapq.heappop(st.frontier)
        if u in st.visited:
            continue
        st.visited.add(u)
        st.step += 1
        st.current_node = u
        st.message = f"Step {st.step}: visit {u} (dist={st.dist[u]:.0f})"

        for v, w in ADJ[u]:
            if v not in st.visited:
                nd = st.dist[u] + w
                if nd < st.dist[v]:
                    st.dist[v] = nd
                    st.prev[v] = u
                    heapq.heappush(st.frontier, (nd, v))
                    st.relaxed_edges.add((u, v))
                    st.message += f" | relax {u}->{v}:{nd:.0f}"
        return

    st.finished = True
    st._reconstruct_path()
    c = st.dist.get(GOAL, INF)
    st.message = (f"Dijkstra done! Path: {'→'.join(st.path)}, cost={c:.0f}"
                  if st.path else "Dijkstra done! No path.")


# ─── Bellman-Ford ────────────────────────────────────────────────────────

def bellman_ford_init() -> AlgoState:
    st = AlgoState()
    st.dist = {n: INF for n in NODES}
    st.prev = {n: None for n in NODES}
    st.dist[SOURCE] = 0
    st.message = (f"Bellman-Ford: {len(NODES)-1} iterations "
                  f"over {len(EDGES)*2} directed edges")
    return st


def bellman_ford_step(st: AlgoState) -> None:
    if st.finished:
        return

    V = len(NODES)
    all_edges = ([(u, v, w) for u, v, w in EDGES]
                 + [(v, u, w) for u, v, w in EDGES])

    if st.bf_iteration < V - 1:
        changed = False
        for src, dst, w in all_edges:
            if st.dist[src] + w < st.dist[dst]:
                st.dist[dst] = st.dist[src] + w
                st.prev[dst] = src
                st.relaxed_edges.add((src, dst))
                st.visited.add(src)
                st.visited.add(dst)
                changed = True
        st.bf_iteration += 1
        st.step += 1
        st.current_node = None
        label = "changes made" if changed else "no changes (stable)"
        st.message = f"Iteration {st.bf_iteration}/{V-1}: {label}"

        if not changed:
            st.finished = True
            st._reconstruct_path()
            c = st.dist.get(GOAL, INF)
            st.message += (f" -> Early stop! Path: {'→'.join(st.path)}, cost={c:.0f}"
                           if st.path else " -> Early stop!")
    else:
        neg = any(st.dist[s] + w < st.dist[d] for s, d, w in all_edges)
        st.finished = True
        if neg:
            st.message = "Negative cycle detected!"
        else:
            st._reconstruct_path()
            c = st.dist.get(GOAL, INF)
            st.message = (f"Bellman-Ford done! Path: {'→'.join(st.path)}, cost={c:.0f}"
                          if st.path else "Bellman-Ford done! No path.")


# ─── A* ──────────────────────────────────────────────────────────────────

def astar_init() -> AlgoState:
    st = AlgoState()
    st.dist = {n: INF for n in NODES}
    st.prev = {n: None for n in NODES}
    st.f_score = {n: INF for n in NODES}
    st.dist[SOURCE] = 0
    h = heuristic(SOURCE)
    st.f_score[SOURCE] = h
    st.frontier = [(h, SOURCE)]
    st.message = f"A*: start={SOURCE}, goal={GOAL}, h({SOURCE})={h:.1f}"
    return st


def astar_step(st: AlgoState) -> None:
    if st.finished or not st.frontier:
        st.finished = True
        st._reconstruct_path()
        c = st.dist.get(GOAL, INF)
        st.message = (f"A* done! Path: {'→'.join(st.path)}, cost={c:.0f}"
                      if st.path else "A* done! No path.")
        return

    st.current_node = None
    while st.frontier:
        f, u = heapq.heappop(st.frontier)
        if u in st.visited:
            continue
        st.visited.add(u)
        st.step += 1
        st.current_node = u

        if u == GOAL:
            st.finished = True
            st._reconstruct_path()
            st.message = (f"Step {st.step}: GOAL reached! "
                          f"Path: {'→'.join(st.path)}, cost={st.dist[GOAL]:.0f}")
            return

        h = heuristic(u)
        st.message = (f"Step {st.step}: visit {u} "
                      f"(g={st.dist[u]:.0f}, h={h:.1f}, f={f:.1f})")

        for v, w in ADJ[u]:
            if v not in st.visited:
                nd = st.dist[u] + w
                if nd < st.dist[v]:
                    st.dist[v] = nd
                    st.prev[v] = u
                    fv = nd + heuristic(v)
                    st.f_score[v] = fv
                    heapq.heappush(st.frontier, (fv, v))
                    st.relaxed_edges.add((u, v))
                    st.message += f" | relax {u}->{v}: g={nd:.0f}, f={fv:.1f}"
        return

    st.finished = True
    st._reconstruct_path()
    st.message = "A* done! No path."
