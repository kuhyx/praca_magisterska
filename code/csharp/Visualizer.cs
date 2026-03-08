/*
 * Raylib GUI for shortest-path algorithm visualization (C#).
 *
 * Controls:
 *   1 / 2 / 3   — Dijkstra / Bellman-Ford / A*
 *   SPACE        — advance one step
 *   R            — reset
 *   Q / ESC      — quit
 */

using System;
using System.Collections.Generic;
using System.Numerics;
using Raylib_cs;

namespace ShortestPathViz;

static class Visualizer
{
    const int W = 1100;
    const int H = 700;
    const float NodeR = 28f;
    const int FSiz = 20;
    const int FSizS = 16;

    // Colours
    static readonly Color BgCol     = new(245, 245, 250, 255);
    static readonly Color EdgeDef   = new(160, 160, 160, 255);
    static readonly Color EdgeRel   = new( 60, 160,  60, 255);
    static readonly Color EdgePath  = new( 40, 180, 100, 255);
    static readonly Color NodeDef   = new(255, 255, 255, 255);
    static readonly Color NodeVis   = new(180, 220, 255, 255);
    static readonly Color NodeCur   = new(255, 220,  80, 255);
    static readonly Color NodePath  = new( 60, 200, 120, 255);
    static readonly Color ColBlue   = new( 60, 100, 220, 255);
    static readonly Color ColOrange = new(240, 140,  40, 255);
    static readonly Color BarCol    = new(230, 230, 230, 255);

    static readonly string[] AlgoNames =
        ["Dijkstra's Algorithm", "Bellman-Ford Algorithm", "A* Algorithm"];

    delegate AlgoState InitFn();
    delegate void StepFn(AlgoState st);

    static readonly InitFn[] Inits =
        [Algorithms.DijkstraInit, Algorithms.BellmanFordInit, Algorithms.AStarInit];
    static readonly StepFn[] Steps =
        [Algorithms.DijkstraStep, Algorithms.BellmanFordStep, Algorithms.AStarStep];

    // ── Edge drawing ────────────────────────────────────────────────────

    static void DrawEdge(Vector2 p1, Vector2 p2, Color col, float thick)
    {
        float dx = p2.X - p1.X, dy = p2.Y - p1.Y;
        float len = MathF.Sqrt(dx * dx + dy * dy);
        if (len < 1f) return;
        float ux = dx / len, uy = dy / len;
        var a = new Vector2(p1.X + ux * NodeR, p1.Y + uy * NodeR);
        var b = new Vector2(p2.X - ux * NodeR, p2.Y - uy * NodeR);
        Raylib.DrawLineEx(a, b, thick, col);
    }

    // ── Render ──────────────────────────────────────────────────────────

    static void Render(AlgoState st, int algo)
    {
        Raylib.BeginDrawing();
        Raylib.ClearBackground(BgCol);

        // Title
        string title = AlgoNames[algo];
        int tw = Raylib.MeasureText(title, FSiz + 4);
        Raylib.DrawText(title, W / 2 - tw / 2, 10, FSiz + 4, Color.Black);

        // Path edge set
        var pathEdges = new HashSet<(string, string)>();
        for (int i = 0; i < st.Path.Count - 1; i++)
        {
            pathEdges.Add((st.Path[i], st.Path[i + 1]));
            pathEdges.Add((st.Path[i + 1], st.Path[i]));
        }

        // Edges
        foreach (var e in Graph.Edges)
        {
            var p1v = Graph.Nodes[e.Src];
            var p2v = Graph.Nodes[e.Dst];
            var p1 = new Vector2(p1v.X, p1v.Y);
            var p2 = new Vector2(p2v.X, p2v.Y);

            Color col = EdgeDef; float thick = 2f;
            if (pathEdges.Contains((e.Src, e.Dst)))
            { col = EdgePath; thick = 5f; }
            else if (st.RelaxedEdges.Contains((e.Src, e.Dst)) ||
                     st.RelaxedEdges.Contains((e.Dst, e.Src)))
            { col = EdgeRel; thick = 3f; }

            DrawEdge(p1, p2, col, thick);

            // Weight label
            float mx = (p1.X + p2.X) / 2;
            float my = (p1.Y + p2.Y) / 2;
            float dx = p2.X - p1.X, dy = p2.Y - p1.Y;
            float len = MathF.Sqrt(dx * dx + dy * dy);
            if (len > 0) { mx += (-dy / len) * 14; my += (dx / len) * 14; }
            string wt = e.Weight.ToString();
            int wtw = Raylib.MeasureText(wt, FSizS);
            Raylib.DrawText(wt, (int)mx - wtw / 2, (int)my - FSizS / 2,
                            FSizS, Color.DarkGray);
        }

        // Nodes
        foreach (var (name, pos) in Graph.Nodes)
        {
            Color col = NodeDef;
            if (st.Path.Contains(name) && st.Finished)
                col = NodePath;
            else if (name == st.CurrentNode)
                col = NodeCur;
            else if (st.Visited.Contains(name))
                col = NodeVis;

            Raylib.DrawCircle(pos.X, pos.Y, NodeR, col);
            Raylib.DrawCircleLines(pos.X, pos.Y, NodeR, Color.Black);

            // Name
            int nw = Raylib.MeasureText(name, FSiz);
            Raylib.DrawText(name, pos.X - nw / 2, pos.Y - FSiz / 2 - 8,
                            FSiz, Color.Black);

            // Distance
            double d = st.Dist.GetValueOrDefault(name, double.PositiveInfinity);
            string dtxt = double.IsPositiveInfinity(d) ? "d=inf" : $"d={d:F0}";
            int dw = Raylib.MeasureText(dtxt, FSizS);
            Raylib.DrawText(dtxt, pos.X - dw / 2, pos.Y + 8, FSizS, ColBlue);

            // h(n) for A*
            if (algo == 2)
            {
                string ht = $"h={Graph.Heuristic(name):F1}";
                Raylib.DrawText(ht, pos.X + (int)NodeR + 4, pos.Y - 8,
                                FSizS, ColOrange);
            }
        }

        // Info bar
        Raylib.DrawRectangle(0, H - 80, W, 80, BarCol);
        Raylib.DrawLine(0, H - 80, W, H - 80, Color.DarkGray);
        Raylib.DrawText(st.Message, 20, H - 70, FSiz, Color.Black);
        Raylib.DrawText("[1] Dijkstra  [2] Bellman-Ford  [3] A*  " +
                        "[SPACE] Step  [R] Reset  [Q] Quit",
                        20, H - 35, FSizS, Color.DarkGray);

        Raylib.EndDrawing();
    }

    // ── Main ────────────────────────────────────────────────────────────

    static void Main()
    {
        Raylib.InitWindow(W, H, "Shortest Path Visualizer");
        Raylib.SetTargetFPS(60);

        int algo = 0;
        AlgoState state = Inits[0]();

        while (!Raylib.WindowShouldClose())
        {
            if (Raylib.IsKeyPressed(KeyboardKey.Q))     break;
            if (Raylib.IsKeyPressed(KeyboardKey.One))   { algo = 0; state = Inits[0](); }
            if (Raylib.IsKeyPressed(KeyboardKey.Two))   { algo = 1; state = Inits[1](); }
            if (Raylib.IsKeyPressed(KeyboardKey.Three)) { algo = 2; state = Inits[2](); }
            if (Raylib.IsKeyPressed(KeyboardKey.R))     state = Inits[algo]();
            if (Raylib.IsKeyPressed(KeyboardKey.Space) && !state.Finished)
                Steps[algo](state);

            Render(state, algo);
        }

        Raylib.CloseWindow();
    }
}
