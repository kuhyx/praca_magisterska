# Shortest Path Algorithms — Pseudocode

## 1. Dijkstra's Algorithm

Finds shortest paths from a single source to all nodes.
**Requirement:** all edge weights must be non-negative.

```
DIJKSTRA(Graph, source):
    for each node v in Graph:
        dist[v] ← ∞
        prev[v] ← NULL
    dist[source] ← 0

    PQ ← min-priority queue ordered by dist
    PQ.insert(source, 0)
    visited ← ∅

    while PQ is not empty:
        u ← PQ.extract_min()

        if u ∈ visited:
            continue
        visited ← visited ∪ {u}

        for each neighbour v of u with edge weight w:
            if dist[u] + w < dist[v]:
                dist[v] ← dist[u] + w
                prev[v] ← u
                PQ.insert(v, dist[v])

    return dist, prev
```

**Complexity:** O((V + E) log V) with a binary heap.


## 2. Bellman-Ford Algorithm

Finds shortest paths from a single source to all nodes.
**Advantage over Dijkstra:** handles negative edge weights.

```
BELLMAN_FORD(Graph, source):
    for each node v in Graph:
        dist[v] ← ∞
        prev[v] ← NULL
    dist[source] ← 0

    repeat |V| - 1 times:                         ← main relaxation loop
        for each edge (u, v, w) in Graph:
            if dist[u] + w < dist[v]:
                dist[v] ← dist[u] + w
                prev[v] ← u

    for each edge (u, v, w) in Graph:              ← negative cycle check
        if dist[u] + w < dist[v]:
            error "Graph contains a negative cycle"

    return dist, prev
```

**Complexity:** O(V · E).


## 3. A* Algorithm

Finds the shortest path from source to a specific goal node.
Uses a heuristic h(n) that estimates the cost from n to the goal.
**Requirement:** h(n) must be admissible (never overestimates).

```
A_STAR(Graph, source, goal, h):
    for each node v in Graph:
        g[v] ← ∞                                  ← actual cost from source
        prev[v] ← NULL
    g[source] ← 0

    PQ ← min-priority queue ordered by f(v) = g[v] + h(v)
    PQ.insert(source, g[source] + h(source))
    visited ← ∅

    while PQ is not empty:
        u ← PQ.extract_min()

        if u = goal:
            return reconstruct_path(prev, goal), g[goal]

        if u ∈ visited:
            continue
        visited ← visited ∪ {u}

        for each neighbour v of u with edge weight w:
            tentative ← g[u] + w
            if tentative < g[v]:
                g[v] ← tentative
                prev[v] ← u
                f[v] ← g[v] + h(v)
                PQ.insert(v, f[v])

    return "no path found"
```

**Complexity:** depends on heuristic quality; worst case O((V + E) log V), same as Dijkstra.


## Path Reconstruction (used by all three)

```
RECONSTRUCT_PATH(prev, target):
    path ← []
    node ← target
    while node ≠ NULL:
        path.prepend(node)
        node ← prev[node]
    return path
```


## Quick Comparison

| Property              | Dijkstra       | Bellman-Ford   | A*                    |
|-----------------------|----------------|----------------|-----------------------|
| Negative weights      | ✗              | ✓              | ✗                     |
| Negative cycle detect | ✗              | ✓              | ✗                     |
| Heuristic required    | no             | no             | yes (admissible h)    |
| Finds path to         | all nodes      | all nodes      | single goal node      |
| Time complexity       | O((V+E) log V) | O(V · E)       | O((V+E) log V) best   |
| Best use case         | general SSSP   | negative edges | known goal + good h   |
