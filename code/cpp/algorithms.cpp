/*
 * Shortest-path algorithms: Dijkstra, Bellman-Ford, A*
 * Implementations — no GUI dependencies.
 */

#include "algorithms.h"
#include <algorithm>
#include <cmath>
#include <sstream>

// ─── Adjacency list (internal) ──────────────────────────────────────────

using AdjList = std::map<std::string, std::vector<std::pair<std::string, int>>>;

static AdjList build_adj() {
    AdjList adj;
    for (auto& n : NODE_ORDER) adj[n] = {};
    for (auto& e : EDGES) {
        adj[e.src].emplace_back(e.dst, e.weight);
        adj[e.dst].emplace_back(e.src, e.weight);
    }
    return adj;
}

static const AdjList ADJ = build_adj();

// ─── Helpers ────────────────────────────────────────────────────────────

static std::string join_path(const std::vector<std::string>& p) {
    std::string s;
    for (size_t i = 0; i < p.size(); i++) {
        if (i) s += "->";
        s += p[i];
    }
    return s;
}

void AlgoState::init_dists() {
    for (auto& n : NODE_ORDER) {
        dist[n] = INF_VAL;
        prev[n] = "";
    }
}

void AlgoState::reconstruct_path() {
    path.clear();
    std::string node = GOAL;
    while (!node.empty()) {
        path.insert(path.begin(), node);
        auto it = prev.find(node);
        node = (it != prev.end() && !it->second.empty()) ? it->second : "";
    }
    if (path.empty() || path[0] != SOURCE) path.clear();
}

double heuristic(const std::string& node) {
    auto pn = NODES.at(node);
    auto pg = NODES.at(GOAL);
    return std::hypot(pg.x - pn.x, pg.y - pn.y) / 100.0;
}

// ─── Dijkstra ───────────────────────────────────────────────────────────

AlgoState dijkstra_init() {
    AlgoState st;
    st.init_dists();
    st.dist[SOURCE] = 0;
    st.frontier.push({0, SOURCE});
    st.message = "Dijkstra: start from " + SOURCE;
    return st;
}

void dijkstra_step(AlgoState& st) {
    auto finish = [&]() {
        st.finished = true;
        st.reconstruct_path();
        st.message = st.path.empty()
            ? "Dijkstra done! No path."
            : "Dijkstra done! Path: " + join_path(st.path) +
              ", cost=" + std::to_string((int)st.dist[GOAL]);
    };

    if (st.finished || st.frontier.empty()) { finish(); return; }

    st.current_node = "";
    while (!st.frontier.empty()) {
        auto [d, u] = st.frontier.top();
        st.frontier.pop();
        if (st.visited.count(u)) continue;

        st.visited.insert(u);
        st.step++;
        st.current_node = u;
        st.message = "Step " + std::to_string(st.step) +
                     ": visit " + u + " (dist=" +
                     std::to_string((int)st.dist[u]) + ")";

        for (auto& [v, w] : ADJ.at(u)) {
            if (!st.visited.count(v)) {
                double nd = st.dist[u] + w;
                if (nd < st.dist[v]) {
                    st.dist[v] = nd;
                    st.prev[v] = u;
                    st.frontier.push({nd, v});
                    st.relaxed_edges.insert({u, v});
                    st.message += " | relax " + u + "->" + v + ":" +
                                  std::to_string((int)nd);
                }
            }
        }
        return;
    }
    finish();
}

// ─── Bellman-Ford ───────────────────────────────────────────────────────

AlgoState bellman_ford_init() {
    AlgoState st;
    st.init_dists();
    st.dist[SOURCE] = 0;
    st.message = "Bellman-Ford: " + std::to_string(NODE_ORDER.size() - 1) +
                 " iterations over all edges";
    return st;
}

void bellman_ford_step(AlgoState& st) {
    if (st.finished) return;

    int V = (int)NODE_ORDER.size();

    std::vector<Edge> all_edges;
    for (auto& e : EDGES) {
        all_edges.push_back(e);
        all_edges.push_back({e.dst, e.src, e.weight});
    }

    if (st.bf_iteration < V - 1) {
        bool changed = false;
        for (auto& e : all_edges) {
            if (st.dist[e.src] + e.weight < st.dist[e.dst]) {
                st.dist[e.dst] = st.dist[e.src] + e.weight;
                st.prev[e.dst] = e.src;
                st.relaxed_edges.insert({e.src, e.dst});
                st.visited.insert(e.src);
                st.visited.insert(e.dst);
                changed = true;
            }
        }
        st.bf_iteration++;
        st.step++;
        st.current_node = "";
        st.message = "Iteration " + std::to_string(st.bf_iteration) + "/" +
                     std::to_string(V - 1) + ": " +
                     (changed ? "changes made" : "no changes (stable)");

        if (!changed) {
            st.finished = true;
            st.reconstruct_path();
            if (!st.path.empty())
                st.message += " -> Early stop! Path: " + join_path(st.path) +
                              ", cost=" + std::to_string((int)st.dist[GOAL]);
            else
                st.message += " -> Early stop!";
        }
    } else {
        bool neg = false;
        for (auto& e : all_edges) {
            if (st.dist[e.src] + e.weight < st.dist[e.dst]) { neg = true; break; }
        }
        st.finished = true;
        if (neg) {
            st.message = "Negative cycle detected!";
        } else {
            st.reconstruct_path();
            st.message = st.path.empty()
                ? "Bellman-Ford done! No path."
                : "Bellman-Ford done! Path: " + join_path(st.path) +
                  ", cost=" + std::to_string((int)st.dist[GOAL]);
        }
    }
}

// ─── A* ─────────────────────────────────────────────────────────────────

AlgoState astar_init() {
    AlgoState st;
    st.init_dists();
    st.dist[SOURCE] = 0;
    double h = heuristic(SOURCE);
    st.f_score[SOURCE] = h;
    st.frontier.push({h, SOURCE});
    char buf[64];
    snprintf(buf, sizeof(buf), "A*: start=%s, goal=%s, h(S)=%.1f",
             SOURCE.c_str(), GOAL.c_str(), h);
    st.message = buf;
    return st;
}

void astar_step(AlgoState& st) {
    auto finish = [&]() {
        st.finished = true;
        st.reconstruct_path();
        st.message = st.path.empty()
            ? "A* done! No path."
            : "A* done! Path: " + join_path(st.path) +
              ", cost=" + std::to_string((int)st.dist[GOAL]);
    };

    if (st.finished || st.frontier.empty()) { finish(); return; }

    st.current_node = "";
    while (!st.frontier.empty()) {
        auto [f, u] = st.frontier.top();
        st.frontier.pop();
        if (st.visited.count(u)) continue;

        st.visited.insert(u);
        st.step++;
        st.current_node = u;

        if (u == GOAL) {
            st.finished = true;
            st.reconstruct_path();
            st.message = "Step " + std::to_string(st.step) +
                         ": GOAL reached! Path: " + join_path(st.path) +
                         ", cost=" + std::to_string((int)st.dist[GOAL]);
            return;
        }

        char buf[200];
        double h = heuristic(u);
        snprintf(buf, sizeof(buf),
                 "Step %d: visit %s (g=%.0f, h=%.1f, f=%.1f)",
                 st.step, u.c_str(), st.dist[u], h, f);
        st.message = buf;

        for (auto& [v, w] : ADJ.at(u)) {
            if (!st.visited.count(v)) {
                double nd = st.dist[u] + w;
                if (nd < st.dist[v]) {
                    st.dist[v] = nd;
                    st.prev[v] = u;
                    double fv = nd + heuristic(v);
                    st.f_score[v] = fv;
                    st.frontier.push({fv, v});
                    st.relaxed_edges.insert({u, v});
                    char b2[100];
                    snprintf(b2, sizeof(b2),
                             " | relax %s->%s: g=%.0f, f=%.1f",
                             u.c_str(), v.c_str(), nd, fv);
                    st.message += b2;
                }
            }
        }
        return;
    }
    finish();
}
