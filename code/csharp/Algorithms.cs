/*
 * Shortest-path algorithms: Dijkstra, Bellman-Ford, A*
 * Pure C# implementations — no GUI dependencies.
 */

using System;
using System.Collections.Generic;
using System.Linq;

namespace ShortestPathViz;

// ─── Graph ──────────────────────────────────────────────────────────────

public record struct Vec2(int X, int Y);
public record struct EdgeDef(string Src, string Dst, int Weight);

public static class Graph
{
    public static readonly Dictionary<string, Vec2> Nodes = new()
    {
        ["S"] = new(80, 350),  ["A"] = new(270, 130), ["B"] = new(270, 570),
        ["C"] = new(500, 80),  ["D"] = new(500, 350), ["E"] = new(500, 620),
        ["F"] = new(730, 180), ["G"] = new(730, 520), ["T"] = new(950, 350),
    };

    public static readonly string[] NodeOrder =
        ["S", "A", "B", "C", "D", "E", "F", "G", "T"];

    public static readonly EdgeDef[] Edges =
    [
        new("S","A",4), new("S","B",2), new("A","C",5), new("A","D",10),
        new("B","D",3), new("B","E",8), new("C","F",3), new("D","F",7),
        new("D","G",4), new("E","G",2), new("F","T",4), new("G","T",6),
        new("C","D",2),
    ];

    public static readonly string Source = "S";
    public static readonly string Goal = "T";

    public static readonly Dictionary<string, List<(string N, int W)>> Adj = BuildAdj();

    private static Dictionary<string, List<(string, int)>> BuildAdj()
    {
        var adj = NodeOrder.ToDictionary(n => n, _ => new List<(string, int)>());
        foreach (var e in Edges)
        {
            adj[e.Src].Add((e.Dst, e.Weight));
            adj[e.Dst].Add((e.Src, e.Weight));
        }
        return adj;
    }

    public static double Heuristic(string node)
    {
        var p = Nodes[node];
        var g = Nodes[Goal];
        return Math.Sqrt(Math.Pow(g.X - p.X, 2) + Math.Pow(g.Y - p.Y, 2)) / 100.0;
    }
}

// ─── State ──────────────────────────────────────────────────────────────

public class AlgoState
{
    public Dictionary<string, double> Dist = new();
    public Dictionary<string, string?> Prev = new();
    public HashSet<string> Visited = new();
    public bool Finished;
    public int Step;
    public string Message = "";
    public List<string> Path = new();
    public HashSet<(string, string)> RelaxedEdges = new();
    public string? CurrentNode;
    public Dictionary<string, double> FScore = new();
    public PriorityQueue<string, double> Frontier = new();
    public int BfIteration;

    public void InitDists()
    {
        foreach (var n in Graph.NodeOrder)
        {
            Dist[n] = double.PositiveInfinity;
            Prev[n] = null;
        }
    }

    public void ReconstructPath()
    {
        Path.Clear();
        string? node = Graph.Goal;
        while (node != null)
        {
            Path.Insert(0, node);
            node = Prev.GetValueOrDefault(node);
        }
        if (Path.Count == 0 || Path[0] != Graph.Source)
            Path.Clear();
    }

    private static string JoinPath(List<string> p) => string.Join("->", p);

    public string PathString() => JoinPath(Path);
}

// ─── Algorithms ─────────────────────────────────────────────────────────

public static class Algorithms
{
    // ── Dijkstra ──

    public static AlgoState DijkstraInit()
    {
        var st = new AlgoState();
        st.InitDists();
        st.Dist[Graph.Source] = 0;
        st.Frontier.Enqueue(Graph.Source, 0);
        st.Message = $"Dijkstra: start from {Graph.Source}";
        return st;
    }

    public static void DijkstraStep(AlgoState st)
    {
        void Finish()
        {
            st.Finished = true;
            st.ReconstructPath();
            st.Message = st.Path.Count > 0
                ? $"Dijkstra done! Path: {st.PathString()}, cost={st.Dist[Graph.Goal]:F0}"
                : "Dijkstra done! No path.";
        }

        if (st.Finished || st.Frontier.Count == 0) { Finish(); return; }

        st.CurrentNode = null;
        while (st.Frontier.Count > 0)
        {
            var u = st.Frontier.Dequeue();
            if (st.Visited.Contains(u)) continue;
            st.Visited.Add(u);
            st.Step++;
            st.CurrentNode = u;
            st.Message = $"Step {st.Step}: visit {u} (dist={st.Dist[u]:F0})";

            foreach (var (v, w) in Graph.Adj[u])
            {
                if (!st.Visited.Contains(v))
                {
                    double nd = st.Dist[u] + w;
                    if (nd < st.Dist[v])
                    {
                        st.Dist[v] = nd;
                        st.Prev[v] = u;
                        st.Frontier.Enqueue(v, nd);
                        st.RelaxedEdges.Add((u, v));
                        st.Message += $" | relax {u}->{v}:{nd:F0}";
                    }
                }
            }
            return;
        }
        Finish();
    }

    // ── Bellman-Ford ──

    public static AlgoState BellmanFordInit()
    {
        var st = new AlgoState();
        st.InitDists();
        st.Dist[Graph.Source] = 0;
        st.Message = $"Bellman-Ford: {Graph.Nodes.Count - 1} iterations over all edges";
        return st;
    }

    public static void BellmanFordStep(AlgoState st)
    {
        if (st.Finished) return;

        int V = Graph.Nodes.Count;
        var allEdges = Graph.Edges
            .SelectMany(e => new[] { (e.Src, e.Dst, e.Weight), (e.Dst, e.Src, e.Weight) })
            .ToList();

        if (st.BfIteration < V - 1)
        {
            bool changed = false;
            foreach (var (s, d, w) in allEdges)
            {
                if (st.Dist[s] + w < st.Dist[d])
                {
                    st.Dist[d] = st.Dist[s] + w;
                    st.Prev[d] = s;
                    st.RelaxedEdges.Add((s, d));
                    st.Visited.Add(s);
                    st.Visited.Add(d);
                    changed = true;
                }
            }
            st.BfIteration++;
            st.Step++;
            st.CurrentNode = null;
            st.Message = $"Iteration {st.BfIteration}/{V - 1}: " +
                         (changed ? "changes made" : "no changes (stable)");

            if (!changed)
            {
                st.Finished = true;
                st.ReconstructPath();
                st.Message += st.Path.Count > 0
                    ? $" -> Early stop! Path: {st.PathString()}, cost={st.Dist[Graph.Goal]:F0}"
                    : " -> Early stop!";
            }
        }
        else
        {
            bool neg = allEdges.Any(e => st.Dist[e.Item1] + e.Item3 < st.Dist[e.Item2]);
            st.Finished = true;
            if (neg)
            {
                st.Message = "Negative cycle detected!";
            }
            else
            {
                st.ReconstructPath();
                st.Message = st.Path.Count > 0
                    ? $"Bellman-Ford done! Path: {st.PathString()}, cost={st.Dist[Graph.Goal]:F0}"
                    : "Bellman-Ford done! No path.";
            }
        }
    }

    // ── A* ──

    public static AlgoState AStarInit()
    {
        var st = new AlgoState();
        st.InitDists();
        foreach (var n in Graph.NodeOrder)
            st.FScore[n] = double.PositiveInfinity;
        st.Dist[Graph.Source] = 0;
        double h = Graph.Heuristic(Graph.Source);
        st.FScore[Graph.Source] = h;
        st.Frontier.Enqueue(Graph.Source, h);
        st.Message = $"A*: start={Graph.Source}, goal={Graph.Goal}, h(S)={h:F1}";
        return st;
    }

    public static void AStarStep(AlgoState st)
    {
        void Finish()
        {
            st.Finished = true;
            st.ReconstructPath();
            st.Message = st.Path.Count > 0
                ? $"A* done! Path: {st.PathString()}, cost={st.Dist[Graph.Goal]:F0}"
                : "A* done! No path.";
        }

        if (st.Finished || st.Frontier.Count == 0) { Finish(); return; }

        st.CurrentNode = null;
        while (st.Frontier.Count > 0)
        {
            var u = st.Frontier.Dequeue();
            if (st.Visited.Contains(u)) continue;
            st.Visited.Add(u);
            st.Step++;
            st.CurrentNode = u;

            if (u == Graph.Goal)
            {
                st.Finished = true;
                st.ReconstructPath();
                st.Message = $"Step {st.Step}: GOAL reached! " +
                             $"Path: {st.PathString()}, cost={st.Dist[Graph.Goal]:F0}";
                return;
            }

            double hu = Graph.Heuristic(u);
            double fu = st.Dist[u] + hu;
            st.Message = $"Step {st.Step}: visit {u} (g={st.Dist[u]:F0}, h={hu:F1}, f={fu:F1})";

            foreach (var (v, w) in Graph.Adj[u])
            {
                if (!st.Visited.Contains(v))
                {
                    double nd = st.Dist[u] + w;
                    if (nd < st.Dist[v])
                    {
                        st.Dist[v] = nd;
                        st.Prev[v] = u;
                        double fv = nd + Graph.Heuristic(v);
                        st.FScore[v] = fv;
                        st.Frontier.Enqueue(v, fv);
                        st.RelaxedEdges.Add((u, v));
                        st.Message += $" | relax {u}->{v}: g={nd:F0}, f={fv:F1}";
                    }
                }
            }
            return;
        }
        Finish();
    }
}
