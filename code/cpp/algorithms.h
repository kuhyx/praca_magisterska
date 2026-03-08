#pragma once
/*
 * Shortest-path algorithms: Dijkstra, Bellman-Ford, A*
 * Pure data structures and declarations — no GUI dependencies.
 */

#include <cmath>
#include <functional>
#include <limits>
#include <map>
#include <queue>
#include <set>
#include <string>
#include <vector>

static constexpr double INF_VAL = std::numeric_limits<double>::infinity();

// ─── Graph ──────────────────────────────────────────────────────────────

struct Vec2 { int x, y; };

struct Edge { std::string src, dst; int weight; };

inline const std::vector<std::string> NODE_ORDER =
    {"S", "A", "B", "C", "D", "E", "F", "G", "T"};

inline const std::map<std::string, Vec2> NODES = {
    {"S", {80, 350}},  {"A", {270, 130}}, {"B", {270, 570}},
    {"C", {500, 80}},  {"D", {500, 350}}, {"E", {500, 620}},
    {"F", {730, 180}}, {"G", {730, 520}}, {"T", {950, 350}},
};

inline const std::vector<Edge> EDGES = {
    {"S","A",4}, {"S","B",2}, {"A","C",5}, {"A","D",10},
    {"B","D",3}, {"B","E",8}, {"C","F",3}, {"D","F",7},
    {"D","G",4}, {"E","G",2}, {"F","T",4}, {"G","T",6},
    {"C","D",2},
};

inline const std::string SOURCE = "S";
inline const std::string GOAL   = "T";

// ─── State ──────────────────────────────────────────────────────────────

using PQ = std::priority_queue<
    std::pair<double, std::string>,
    std::vector<std::pair<double, std::string>>,
    std::greater<std::pair<double, std::string>>>;

struct AlgoState {
    std::map<std::string, double>       dist;
    std::map<std::string, std::string>  prev;   // "" = no predecessor
    std::set<std::string>               visited;
    bool finished   = false;
    int  step       = 0;
    std::string message;
    std::vector<std::string> path;
    std::set<std::pair<std::string,std::string>> relaxed_edges;
    std::string current_node;                    // "" = none
    std::map<std::string, double> f_score;       // A* only
    PQ frontier;
    int bf_iteration = 0;                        // Bellman-Ford only

    void reconstruct_path();
    void init_dists();
};

// ─── Algorithm functions ────────────────────────────────────────────────

double      heuristic(const std::string& node);

AlgoState   dijkstra_init();
void        dijkstra_step(AlgoState& st);

AlgoState   bellman_ford_init();
void        bellman_ford_step(AlgoState& st);

AlgoState   astar_init();
void        astar_step(AlgoState& st);
