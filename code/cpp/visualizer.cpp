/*
 * Raylib GUI for shortest-path algorithm visualization.
 *
 * Controls:
 *   1 / 2 / 3   — Dijkstra / Bellman-Ford / A*
 *   SPACE        — advance one step
 *   R            — reset
 *   Q / ESC      — quit
 */

#include "algorithms.h"
#include "raylib.h"
#include <algorithm>
#include <cmath>
#include <string>

static const int W = 1100;
static const int H = 700;
static const float NODE_R = 28.0f;
static const int FSIZ = 20;
static const int FSIZ_S = 16;

// Colours
static const Color BG_COL       = {245, 245, 250, 255};
static const Color EDGE_DEF     = {160, 160, 160, 255};
static const Color EDGE_REL     = { 60, 160,  60, 255};
static const Color EDGE_PATH    = { 40, 180, 100, 255};
static const Color NODE_DEF     = {255, 255, 255, 255};
static const Color NODE_VIS     = {180, 220, 255, 255};
static const Color NODE_CUR     = {255, 220,  80, 255};
static const Color NODE_PATH    = { 60, 200, 120, 255};
static const Color COL_BLUE     = { 60, 100, 220, 255};
static const Color COL_ORANGE   = {240, 140,  40, 255};
static const Color BAR_COL      = {230, 230, 230, 255};

static const char* ALGO_NAMES[] = {
    "Dijkstra's Algorithm",
    "Bellman-Ford Algorithm",
    "A* Algorithm",
};

// ─── Edge drawing (clipped to node radius) ──────────────────────────────

static void draw_edge(Vector2 p1, Vector2 p2, Color col, float thick) {
    float dx = p2.x - p1.x, dy = p2.y - p1.y;
    float len = sqrtf(dx * dx + dy * dy);
    if (len < 1.0f) return;
    float ux = dx / len, uy = dy / len;
    Vector2 a = {p1.x + ux * NODE_R, p1.y + uy * NODE_R};
    Vector2 b = {p2.x - ux * NODE_R, p2.y - uy * NODE_R};
    DrawLineEx(a, b, thick, col);
}

// ─── Render ─────────────────────────────────────────────────────────────

static void render(const AlgoState& st, int algo) {
    BeginDrawing();
    ClearBackground(BG_COL);

    // Title
    const char* title = ALGO_NAMES[algo];
    int tw = MeasureText(title, FSIZ + 4);
    DrawText(title, W / 2 - tw / 2, 10, FSIZ + 4, BLACK);

    // Build path edge set
    std::set<std::pair<std::string, std::string>> path_edges;
    for (size_t i = 0; i + 1 < st.path.size(); i++) {
        path_edges.insert({st.path[i], st.path[i + 1]});
        path_edges.insert({st.path[i + 1], st.path[i]});
    }

    // Edges
    for (auto& e : EDGES) {
        auto p1v = NODES.at(e.src);
        auto p2v = NODES.at(e.dst);
        Vector2 p1 = {(float)p1v.x, (float)p1v.y};
        Vector2 p2 = {(float)p2v.x, (float)p2v.y};

        Color col = EDGE_DEF; float thick = 2.0f;
        if (path_edges.count({e.src, e.dst})) {
            col = EDGE_PATH; thick = 5.0f;
        } else if (st.relaxed_edges.count({e.src, e.dst}) ||
                   st.relaxed_edges.count({e.dst, e.src})) {
            col = EDGE_REL; thick = 3.0f;
        }
        draw_edge(p1, p2, col, thick);

        // Weight label
        float mx = (p1.x + p2.x) / 2;
        float my = (p1.y + p2.y) / 2;
        float dx = p2.x - p1.x, dy = p2.y - p1.y;
        float len = sqrtf(dx * dx + dy * dy);
        if (len > 0) { mx += (-dy / len) * 14; my += (dx / len) * 14; }
        const char* wt = TextFormat("%d", e.weight);
        int wtw = MeasureText(wt, FSIZ_S);
        DrawText(wt, (int)mx - wtw / 2, (int)my - FSIZ_S / 2, FSIZ_S, DARKGRAY);
    }

    // Nodes
    for (auto& [name, pos] : NODES) {
        Color col = NODE_DEF;
        if (std::find(st.path.begin(), st.path.end(), name) != st.path.end()
            && st.finished)
            col = NODE_PATH;
        else if (name == st.current_node)
            col = NODE_CUR;
        else if (st.visited.count(name))
            col = NODE_VIS;

        DrawCircle(pos.x, pos.y, NODE_R, col);
        DrawCircleLines(pos.x, pos.y, NODE_R, BLACK);

        // Name
        int nw = MeasureText(name.c_str(), FSIZ);
        DrawText(name.c_str(), pos.x - nw / 2, pos.y - FSIZ / 2 - 8,
                 FSIZ, BLACK);

        // Distance
        double d = INF_VAL;
        auto it = st.dist.find(name);
        if (it != st.dist.end()) d = it->second;
        const char* dtxt = (d >= INF_VAL) ? "d=inf" : TextFormat("d=%d", (int)d);
        int dw = MeasureText(dtxt, FSIZ_S);
        DrawText(dtxt, pos.x - dw / 2, pos.y + 8, FSIZ_S, COL_BLUE);

        // h(n) for A*
        if (algo == 2) {
            const char* ht = TextFormat("h=%.1f", heuristic(name));
            DrawText(ht, pos.x + (int)NODE_R + 4, pos.y - 8, FSIZ_S, COL_ORANGE);
        }
    }

    // Info bar
    DrawRectangle(0, H - 80, W, 80, BAR_COL);
    DrawLine(0, H - 80, W, H - 80, DARKGRAY);
    DrawText(st.message.c_str(), 20, H - 70, FSIZ, BLACK);
    DrawText("[1] Dijkstra  [2] Bellman-Ford  [3] A*  "
             "[SPACE] Step  [R] Reset  [Q] Quit",
             20, H - 35, FSIZ_S, DARKGRAY);

    EndDrawing();
}

// ─── Main ───────────────────────────────────────────────────────────────

int main() {
    InitWindow(W, H, "Shortest Path Visualizer");
    SetTargetFPS(60);

    int algo = 0;
    AlgoState state = dijkstra_init();

    using StepFn = void(*)(AlgoState&);
    using InitFn = AlgoState(*)();

    InitFn inits[] = {dijkstra_init, bellman_ford_init, astar_init};
    StepFn steps[] = {dijkstra_step, bellman_ford_step, astar_step};

    while (!WindowShouldClose()) {
        if (IsKeyPressed(KEY_Q))     break;
        if (IsKeyPressed(KEY_ONE))   { algo = 0; state = inits[0](); }
        if (IsKeyPressed(KEY_TWO))   { algo = 1; state = inits[1](); }
        if (IsKeyPressed(KEY_THREE)) { algo = 2; state = inits[2](); }
        if (IsKeyPressed(KEY_R))     { state = inits[algo](); }
        if (IsKeyPressed(KEY_SPACE) && !state.finished)
            steps[algo](state);

        render(state, algo);
    }

    CloseWindow();
    return 0;
}
