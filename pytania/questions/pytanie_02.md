## PYTANIE 2: Algorytmy najkrótszej ścieżki (AISDI)

**Omówić i porównać algorytmy: Dijkstry, Bellmana-Forda, A*.**

---

### Tło pojęciowe — słowniczek

**Graf** — struktura danych składająca się z **wierzchołków** (vertices/nodes) połączonych **krawędziami** (edges). Np. mapa miast: miasta = wierzchołki, drogi = krawędzie.

**Wierzchołek (vertex, node)** — punkt w grafie. Oznaczany jako v, u, n, m itp. **V** = zbiór wszystkich wierzchołków; |V| = ich liczba.

**Krawędź (edge)** — połączenie między dwoma wierzchołkami. **E** = zbiór krawędzi; |E| = ich liczba. Krawędź może być skierowana (A→B ≠ B→A) lub nieskierowana (A↔B).

**Waga (weight)** — liczba przypisana do krawędzi, oznaczająca „koszt" przejścia. Np. odległość w km, czas podróży, opłata za przejazd. Graf z wagami = graf ważony.

**Koszt (cost)** — ogólne pojęcie „ceny" przejścia ścieżką. Koszt ścieżki = suma wag krawędzi na tej ścieżce. Cel algorytmów: znaleźć ścieżkę o **minimalnym koszcie**.

**SSSP (Single-Source Shortest Path)** — problem: mając JEDEN wierzchołek startowy (źródło), znajdź najkrótsze ścieżki do WSZYSTKICH pozostałych wierzchołków. Dijkstra i Bellman-Ford rozwiązują SSSP. **Single-Pair** — prostszy problem: znajdź najkrótszą ścieżkę z A do B (jednej konkretnej pary). A* rozwiązuje Single-Pair.

**d[v]** — tablica odległości. **d** = tablica (array), **v** = wierzchołek. d[v] przechowuje aktualnie najlepsze znane oszacowanie odległości od źródła do wierzchołka v. Na początku d[start] = 0, d[wszystko inne] = ∞. Algorytm stopniowo poprawia te wartości.

**Zachłanny (greedy)** — strategia algorytmiczna: w każdym kroku wybierz opcję, która TERAZ wygląda najlepiej (lokalnie optymalna), bez cofania się. Dijkstra jest zachłanny: zawsze bierze wierzchołek o najmniejszym d[v] i nigdy go nie rewiduje.

**Relaksacja krawędzi (edge relaxation)** — kluczowa operacja. Sprawdza: „czy droga do v przez u jest krótsza niż dotychczas znana?" Jeśli d[u] + waga(u,v) < d[v], to zaktualizuj d[v]. Nazwa od „rozluźniania" — górne ograniczenie na odległość się „rozluźnia" (maleje) w stronę prawdziwej wartości.

**Tablica (array)** — najprostsza struktura danych: ciągły blok pamięci. W Dijkstrze z tablicą: szukanie minimum d[v] wymaga przejrzenia WSZYSTKICH wierzchołków → O(V) na szukanie × V razy = **O(V²)**.

Przykład — graf z 4 wierzchołkami (A, B, C, D), start = A:

![Graf przykładowy — 4 wierzchołki z wagami](img/graph_example_structure.png)

    d = [ A:0,  B:∞,  C:∞,  D:∞ ]     ← tablica na starcie
         odwiedzone = {}

    Krok 1: przeszukaj CAŁĄ tablicę d → min = A (0)
            d = [ A:0, B:2, C:4, D:∞ ]   odw = {A}
                        ↑    ↑
                    A→B=2  A→C=4  (relaksacja sąsiadów A)

    Krok 2: przeszukaj CAŁĄ tablicę d (poza odw.) → min = B (2)
            d = [ A:0, B:2, C:4, D:5 ]   odw = {A,B}
                                  ↑
                            B→D=2+3=5 (relaksacja)

    Krok 3: przeszukaj tablicę → min = C (4)
            d = [ A:0, B:2, C:4, D:5 ]   odw = {A,B,C}
                                  ↑
                            C→D=4+5=9 > 5, nie zmieniaj

    Krok 4: min = D (5). Koniec! d = [A:0, B:2, C:4, D:5]

    Każdy krok = przejrzyj V elementów → 4 kroki × 4 elementy = 16 operacji = O(V²)

**Kopiec (heap)** — drzewiasta struktura danych, w której element minimalny jest zawsze na szczycie. Wyciąganie minimum: O(log n). W Dijkstrze z kopcem: szukanie min d[v] to O(log V) zamiast O(V) → **O((V+E) log V)**.

Przykład — ten sam graf, ale z kopcem (min-heap):

    Kopiec na starcie:      (0,A)          ← min zawsze na szczycie
                                           (reszta to ∞)

    Krok 1: pop (0,A) — O(log 4)=O(2), relaksuj sąsiadów:
            push (2,B), push (4,C)

            Kopiec:    (2,B)
                      /     \
                   (4,C)   ...

    Krok 2: pop (2,B) — O(log 4), relaksuj:
            push (5,D)

            Kopiec:    (4,C)
                      /
                   (5,D)

    Krok 3: pop (4,C) — O(log 4). C→D: 9 > 5, nie zmieniaj.
    Krok 4: pop (5,D) — O(log 4). Koniec!

    Każdy pop = O(log V), każdy push = O(log V)
    V popów + E pushów = O((V+E) log V)

**Kopiec Fibonacciego** — zaawansowany kopiec, w którym operacja „zmniejsz klucz" (decrease-key) działa w zamortyzowanym O(1) zamiast O(log V). Dijkstra robi decrease-key dla każdej krawędzi → z kopcem Fib: **O(V log V + E)** — E operacji po O(1) + V wyciągnięć po O(log V).

Przykład — kluczowa różnica: decrease-key:

    Zwykły kopiec — gdy znajdziesz krótszą drogę do D:
        d[D] zmienia się z 9 na 5
        Trzeba „naprawić" kopiec: przesuwaj D w górę → O(log V)

    Kopiec Fibonacciego — ta sama sytuacja:
        d[D] zmienia się z 9 na 5
        Po prostu odetnij D od rodzica i wstaw do listy korzeni → O(1)!
        (naprawienie struktury odłożone na później — „zamortyzowane")

    Różnica ma znaczenie przy GĘSTYCH grafach (E >> V):
    - Zwykły kopiec: E × O(log V) = O(E log V) na decrease-key
    - Kopiec Fib:    E × O(1)     = O(E)       na decrease-key
    Razem: O(V log V) [pop] + O(E) [decrease-key] = O(V log V + E)

**Złożoność — dlaczego takie wartości:**
- **O(V²)** z tablicą: V razy szukaj minimum (O(V) każdy) = V × V.
- **O((V+E) log V)** z kopcem: V wyciągnięć min (O(log V)) + E relaksacji z decrease-key (O(log V)).
- **O(V log V + E)** z kopcem Fib: V wyciągnięć min (O(log V)) + E decrease-key (O(1) zamortyzowane).

**Programowanie dynamiczne (DP)** — technika rozwiązywania problemów przez rozbicie na mniejsze podproblemy i zapamiętywanie wyników (żeby nie liczyć tego samego dwa razy). Bellman-Ford jest DP: podproblem = „najkrótsza ścieżka do v używająca ≤ k krawędzi"; rozwiązuje dla k = 1, 2, ..., V−1.

**Cykl** — ścieżka w grafie, która wraca do punktu wyjścia (A → B → C → A). **Cykl ujemny** — cykl, w którym suma wag < 0. Problem: za każdym obejściem cyklu „odległość" maleje — można iść w nieskończoność → najkrótsza ścieżka nie istnieje (= −∞).

**Dlaczego O(V·E) w Bellman-Ford:** Algorytm wykonuje |V|−1 iteracji (bo najdłuższa najkrótsza ścieżka bez cykli ma co najwyżej V−1 krawędzi). W każdej iteracji relaksuje WSZYSTKIE |E| krawędzi. Razem: (V−1) × E ≈ O(V·E).

**Heurystyczny** — wykorzystujący przybliżone oszacowanie (heurystykę) zamiast dokładnych obliczeń. A* jest heurystyczny: używa funkcji h(n) do zgadywania „ile jeszcze do celu".

**f(n), g(n), h(n) — co oznacza n i każda funkcja:**
- **n** = aktualnie rozpatrywany wierzchołek.
- **g(n)** = dotychczasowy koszt dotarcia od startu do n (znany, dokładny).
- **h(n)** = heurystyka: OSZACOWANIE kosztu od n do celu (przybliżone, „zgadywane"). Np. odległość w linii prostej do celu.
- **f(n) = g(n) + h(n)** = oszacowanie CAŁKOWITEGO kosztu ścieżki przez n. A* zawsze rozwija wierzchołek o najniższym f(n).

**Dopuszczalna (admissible)** — heurystyka h jest dopuszczalna, jeśli NIGDY nie przeszacowuje: h(n) ≤ prawdziwy koszt od n do celu. Gwarantuje, że A* znajdzie optymalną ścieżkę. Np. odległość w linii prostej jest dopuszczalna (nie da się dojechać krócej niż prosto).

**Rzeczywisty koszt** — prawdziwa najkrótsza odległość (nie oszacowanie). Np. faktyczna najkrótsza droga od n do celu, uwzględniając wszystkie krawędzie.

**n → cel** — od wierzchołka n do wierzchołka docelowego (cel = destination = target).

**Spójna (consistent / monotone)** — silniejszy warunek na heurystykę: h(n) ≤ w(n,m) + h(m) dla każdej krawędzi n→m. Tu **w(n,m)** = waga krawędzi z n do m, a **m** = sąsiad n. Spójność oznacza: oszacowanie z n nie jest „dużo lepsze" niż to co uzyskasz idąc jeden krok do m. Spójna ⇒ dopuszczalna (ale nie odwrotnie).

**Dlaczego O(V) w najlepszym przypadku A*:** Jeśli heurystyka jest idealna (h(n) = prawdziwy koszt), A* idzie prosto do celu, nie eksplorując zbędnych wierzchołków — odwiedza tylko te na optymalnej ścieżce ≈ O(V) jeśli ścieżka krótka. **Najgorszy przypadek** = h(n) = 0 dla wszystkich n → A* degeneruje się do Dijkstry.

### Pseudokod (Python)

**Dijkstra** (graph = słownik sąsiedztwa, np. `{'A': [('B',2), ('C',4)]}`):

    def dijkstra(graph, source):
        dist = {v: float('inf') for v in graph}
        dist[source] = 0
        visited = set()
        for _ in range(len(graph)):
            current = None  # szukaj nieodwiedzonego wierzchołka o min dist — O(V)
            for v in graph:
                if v not in visited and (current is None or dist[v] < dist[current]):
                    current = v
            if dist[current] == float('inf'):
                break  # reszta nieosiągalna
            visited.add(current)  # zamknij — NIE wracamy (zachłanność)
            for neighbor, weight in graph[current]:  # relaksacja sąsiadów
                if dist[current] + weight < dist[neighbor]:
                    dist[neighbor] = dist[current] + weight
        return dist  # O(V²) z tablicą

![Przejście grafu algorytmem Dijkstry — krok po kroku](img/dijkstra_traversal.png)

**Bellman-Ford** (vertices = lista wierzchołków, edges = lista krotek (src, dst, weight)):

    def bellman_ford(vertices, edges, source):
        dist = {v: float('inf') for v in vertices}
        dist[source] = 0
        for _ in range(len(vertices) - 1):  # V−1 iteracji (najdłuższa ścieżka = V−1 krawędzi)
            for src, dst, weight in edges:  # relaksuj WSZYSTKIE krawędzie
                if dist[src] + weight < dist[dst]:
                    dist[dst] = dist[src] + weight
        for src, dst, weight in edges:  # V-ta iteracja: wykrywanie cyklu ujemnego
            if dist[src] + weight < dist[dst]:
                return None  # cykl ujemny!
        return dist  # O(V·E)

Przykład — graf z ujemnymi wagami (Dijkstra daje ZŁY wynik, B-F poprawny):

    Graf: S→A(2), A→C(3), S→B(5), B→A(−4)

    Dijkstra:
      1. S(0): dist[A]=2, dist[B]=5
      2. A(2) zamknięty: dist[C]=5
      3. B(5): B→A = 5−4 = 1 < 2, ALE A już zamknięty → POMIJA!
      Wynik: A=2, C=5  ← BŁĄD (prawidłowe: A=1, C=4)

    Bellman-Ford — relaksuje WSZYSTKIE krawędzie, V−1 = 3 razy:
      Start: dist = [S:0, A:∞, B:∞, C:∞]

      Iteracja 1:
        S→A: 0+2=2  < ∞ → A=2
        A→C: 2+3=5  < ∞ → C=5
        S→B: 0+5=5  < ∞ → B=5
        B→A: 5−4=1  < 2 → A=1  ← ujemna waga poprawia!

      Iteracja 2:
        A→C: 1+3=4 < 5 → C=4  ← propagacja poprawionego A

      Iteracja 3: brak zmian → stabilne.
      Wynik: [S:0, A:1, B:5, C:4]  ← POPRAWNE

    Wykrywanie cyklu ujemnego — dodaj krawędź C→B(−3):
      Cykl B→A→C→B = −4 + 3 + (−3) = −4 < 0.
      Po V−1 iteracjach dist nadal maleje → V-ta iteracja:
        dist[src] + weight < dist[dst] → return None

![Przejście grafu algorytmem Bellmana-Forda — krok po kroku](img/bellman_ford_traversal.png)

**A\*** (graph jak Dijkstra; heuristic = h(v) → oszacowanie odl. do celu):

    def a_star(graph, source, goal, heuristic):
        cost_so_far = {source: 0}  # g(n) — faktyczny koszt dotarcia
        priority = {source: heuristic(source)}  # f(n) = g(n) + h(n)
        came_from = {}  # do odtworzenia ścieżki
        visited = set()
        while priority:
            current = min(priority, key=priority.get)  # wierzchołek o min f(n)
            del priority[current]
            if current == goal:
                break  # dotarliśmy — A* kończy (Dijkstra przetworzyłby wszystko)
            visited.add(current)
            for neighbor, weight in graph[current]:
                if neighbor in visited:
                    continue
                new_cost = cost_so_far[current] + weight
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority[neighbor] = new_cost + heuristic(neighbor)
                    came_from[neighbor] = current
        return came_from, cost_so_far.get(goal)  # ścieżka + koszt

![Przejście grafu algorytmem A* — krok po kroku](img/astar_traversal.png)

---

### Dijkstra — zachłanny, SSSP

**Ograniczenie:** wagi ≥ 0.
**Idea:** Relaksacja krawędzi; zawsze przetwarzaj wierzchołek o najmniejszym d[v].
**Złożoność:** O(V²) z tablicą, O((V+E) log V) z kopcem, O(V log V + E) z kopcem Fibonacciego.
**Dlaczego nie ujemne wagi?** Raz oznaczony wierzchołek nie jest rewidowany — ujemna krawędź może go poprawić.

### Bellman-Ford — programowanie dynamiczne, SSSP

**Zaleta:** obsługuje ujemne wagi + **wykrywa cykle ujemne**.
**Idea:** |V|−1 iteracji relaksacji WSZYSTKICH krawędzi. Jeśli w iteracji V nadal można poprawić → cykl ujemny.
**Złożoność:** O(V·E) — zawsze.

### A* — heurystyczny, Single-Pair

**Rozszerzenie Dijkstry:** f(n) = g(n) + h(n), gdzie h(n) to heurystyka.
**Wymóg:** h dopuszczalna (admissible): h(n) ≤ rzeczywisty koszt n→cel. Jeśli h spójna (consistent): h(n) ≤ w(n,m) + h(m) — optymalne.
**Złożoność:** zależy od h; najlepszy przypadek O(V), najgorszy jak Dijkstra.

### Porównanie

| Cecha           | Dijkstra         | Bellman-Ford    | A*                |
|-----------------|------------------|-----------------|-------------------|
| Typ             | Zachłanny        | Prog. dynamiczne| Heurystyczny      |
| Problem         | SSSP             | SSSP            | Single-pair       |
| Ujemne wagi     | NIE              | TAK             | NIE               |
| Wykrywa cykle-  | NIE              | TAK             | NIE               |
| Złożoność       | O((V+E)log V)    | O(VE)           | Zależy od h       |

### Etymologia

**Dijkstra** — Edsger W. Dijkstra (Holandia, 1959); pionier informatyki (Turing Award 1972). **Bellman-Ford** — Richard Bellman (twórca programowania dynamicznego) + Lester Ford Jr. (1956). **A*** — Hart, Nilsson, Raphael (Stanford, 1968); „A*" = ulepszona wersja algorytmu „A". **Zachłanny (Greedy)** — algorytm „chciwie" bierze lokalnie najlepszą opcję. **SSSP** — Single-Source Shortest Path. **Programowanie dynamiczne** — Bellman wybrał „dynamic" by brzmiało imponująco dla polityków (nie miało związku z dynamiką!). **Heurystyka** — grec. „heuriskein" = znajdować (to samo co „Eureka!" Archimedesa). **Relaksacja** — „rozluźnianie" górnego ograniczenia na odległość d[v].

### Jak zapamiętać

- **Dijkstra = chciwy**, bierze minimum — ale „nie patrzy wstecz" (stąd problem z ujemnymi wagami)
- **Bellman-Ford = brute force x (V−1)** — relaksuj wszystko, V−1 razy, bo najdłuższa ścieżka ma V−1 krawędzi
- **A* = Dijkstra + „GPS"** — heurystyka mówi w którą stronę jest cel

