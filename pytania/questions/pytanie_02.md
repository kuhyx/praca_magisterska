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

**Dijkstra:**

    def dijkstra(graph, start):              # graph = słownik, klucz = wierzchołek,
                                             #   wartość = lista par (sąsiad, waga)
                                             #   np. graph = {'A': [('B',2), ('C',4)],
                                             #                'B': [('D',3)], ...}
                                             # start = wierzchołek startowy, np. 'A'

        d = {v: float('inf') for v in graph} # d = słownik odległości (distance)
                                             # Klucz: wierzchołek v
                                             # Wartość: najkrótsza DOTYCHCZAS ZNANA
                                             #   odległość od start do v
                                             # Na początku: ∞ (nieskończoność) dla
                                             #   wszystkich — bo jeszcze niczego
                                             #   nie odkryliśmy
                                             # float('inf') = Python-owa nieskończoność,
                                             #   każda liczba jest od niej mniejsza

        d[start] = 0                         # odległość od startu do samego siebie = 0

        visited = set()                      # visited = zbiór ZAMKNIĘTYCH wierzchołków
                                             # (już przetworzonych, nie wracamy do nich)
                                             # set() = pusty zbiór Pythona — O(1) lookup

        for _ in range(len(graph)):          # powtórz V razy (raz na każdy wierzchołek)
                                             # W każdej iteracji wybieramy JEDEN
                                             # wierzchołek o min d[v] i go przetwarzamy

            # --- Szukanie minimum w tablicy d --- → O(V) na każde szukanie
            u = None                         # u = wierzchołek o najmniejszej odległości
                                             # (jeszcze nie odwiedzony)
            for v in graph:                  # przejrzyj WSZYSTKIE wierzchołki
                if v not in visited:         # pomiń już odwiedzone
                    if u is None or d[v] < d[u]:  # jeśli v ma mniejszą odległość
                        u = v                # zapamiętaj go jako kandydata
            # Po tej pętli: u = wierzchołek z min d, spośród nieodwiedzonych
            # To jest O(V) — przeszukujemy całą tablicę!

            if d[u] == float('inf'):          # jeśli minimum to ∞, reszta jest
                break                        # nieosiągalna — koniec

            visited.add(u)                   # oznacz u jako odwiedzony (zamknięty)
                                             # NIE WRACAMY do u — to jest ZACHŁANNOŚĆ
                                             # Dijkstry (i dlatego ujemne wagi psują!)

            for v, w in graph[u]:            # iteruj po sąsiadach wierzchołka u
                                             # v = sąsiad (vertex), w = waga krawędzi u→v
                                             # np. graph['A'] = [('B',2), ('C',4)]
                                             #   → v='B', w=2, potem v='C', w=4

                if d[u] + w < d[v]:          # RELAKSACJA: czy droga do v PRZEZ u
                                             #   jest krótsza niż dotychczas znana?
                                             #   d[u] = koszt dotarcia do u
                                             #   w = koszt krawędzi u→v
                                             #   d[u]+w = koszt drogi start→u→v
                                             #   d[v] = dotychczasowy najlepszy koszt do v

                    d[v] = d[u] + w          # TAK, jest krótsza → zaktualizuj!
                                             # (tablica d pełni tu rolę kolejki
                                             #  priorytetowej — po prostu szukamy
                                             #  minimum w niej w każdej iteracji)

        return d                             # zwróć słownik najkrótszych odległości
                                             # np. {'A': 0, 'B': 2, 'C': 4, 'D': 5}
                                             # Złożoność: O(V²) — V szukań min × O(V) każde

![Przejście grafu algorytmem Dijkstry — krok po kroku](img/dijkstra_traversal.png)

**Bellman-Ford:**

    def bellman_ford(vertices, edges, start): # vertices = lista wierzchołków, np. ['A','B','C','D']
                                              # edges = lista krawędzi, każda to (skąd, dokąd, waga)
                                              #   np. [('A','B',2), ('A','C',4), ('B','D',3), ...]
                                              # start = wierzchołek startowy
                                              # UWAGA: format inny niż w Dijkstrze!
                                              #   Dijkstra: graf jako słownik sąsiedztwa
                                              #   B-F: explicite lista krawędzi

        d = {v: float('inf') for v in vertices}  # d = słownik odległości — identycznie
                                              # jak w Dijkstrze. Klucz = wierzchołek,
                                              # wartość = najkrótsza znana odległość.
                                              # Na starcie: ∞ dla wszystkich.

        d[start] = 0                          # odległość do siebie = 0

        for _ in range(len(vertices) - 1):    # powtórz V−1 razy (V = liczba wierzchołków)
                                              # DLACZEGO V−1? Bo najdłuższa najkrótsza
                                              # ścieżka (bez cykli) ma co najwyżej V−1
                                              # krawędzi. Po k iteracjach mamy poprawne
                                              # odległości dla ścieżek o ≤ k krawędziach.
                                              # _ = zmienna, której nie używamy (konwencja)

            for u, v, w in edges:             # w KAŻDEJ iteracji przejrzyj WSZYSTKIE krawędzie
                                              # u = początek krawędzi, v = koniec, w = waga
                                              # To jest brute-force — stąd O(V·E)

                if d[u] + w < d[v]:           # RELAKSACJA — identyczna jak w Dijkstrze:
                                              # czy droga start→u→v jest krótsza niż d[v]?

                    d[v] = d[u] + w           # TAK → zaktualizuj

        # --- Wykrywanie cyklu ujemnego ---
        for u, v, w in edges:                 # dodatkowe (V-te) przejście po krawędziach
                                              # Jeśli NADAL da się poprawić odległość,
                                              # to znaczy, że istnieje cykl ujemny!
                                              # (po V−1 iteracjach powinno być stabilne)

            if d[u] + w < d[v]:               # nadal można polepszyć? → cykl ujemny!
                return None                   # zwróć None = sygnał "cykl ujemny wykryty"

        return d                              # zwróć słownik odległości (jak Dijkstra)

![Przejście grafu algorytmem Bellmana-Forda — krok po kroku](img/bellman_ford_traversal.png)

**A*:**

    def a_star(graph, start, goal, h):        # graph = słownik sąsiedztwa (jak Dijkstra)
                                              # start = wierzchołek startowy
                                              # goal = wierzchołek DOCELOWY (cel)
                                              #   → to jedyna różnica od Dijkstry:
                                              #     szukamy ścieżki do JEDNEGO celu
                                              # h = FUNKCJA heurystyczna: h(v) zwraca
                                              #   oszacowanie odległości od v do goal
                                              #   np. h = lambda v: odl_euklidesowa(v, goal)

        d = {start: 0}                        # d = słownik g(n) = faktyczny koszt
                                              #   dotarcia od start do n
                                              # Tu trzymamy TYLKO odkryte wierzchołki
                                              # (nie inicjalizujemy ∞ dla reszty)

        f = {start: h(start)}                 # f = słownik f(n) = g(n) + h(n)
                                              # f to szacunkowy ŁĄCZNY koszt ścieżki:
                                              #   dotychczasowy koszt g + heurystyka h
                                              # Sortujemy po f (nie po g!) — to kieruje
                                              #   przeszukiwanie W STRONĘ CELU
                                              # Na starcie: f(start) = 0 + h(start)

        came_from = {}                        # came_from = słownik "skąd przyszliśmy"
                                              # Klucz: wierzchołek v
                                              # Wartość: wierzchołek, z którego dotarliśmy do v
                                              # Służy do ODTWORZENIA ścieżki po znalezieniu celu
                                              # np. came_from = {'B':'A', 'D':'B'}
                                              #   → ścieżka: A → B → D

        visited = set()                       # visited = zbiór zamkniętych wierzchołków
                                              # (już przetworzonych)

        while f:                              # dopóki są odkryte, nieprzetworzone wierzchołki
                                              # (f zawiera tylko te, do których dotarliśmy)

            # --- Szukanie minimum f w tablicy --- → O(V)
            u = min(f, key=f.get)             # u = wierzchołek o najniższym f(n)
                                              # min() przeszukuje WSZYSTKIE klucze w f
                                              # key=f.get → porównuj po wartościach f[v]
                                              # Równoważne: for v in f: if f[v] < f[best]...
            del f[u]                          # usuń u z open set (przetwarzamy go teraz)

            if u == goal: break               # ZNALEZIONO CEL! → przerwij
                                              # Kluczowa optymalizacja A*:
                                              # Dijkstra przetwarza WSZYSTKIE wierzchołki,
                                              # A* KOŃCZY gdy dotrze do celu

            visited.add(u)                    # oznacz u jako przetworzony

            for v, w in graph[u]:             # iteruj po sąsiadach u
                                              # v = sąsiad, w = waga krawędzi u→v

                if v in visited:              # jeśli v już przetworzony → pomiń
                    continue

                g_new = d[u] + w              # g_new = potencjalny nowy koszt dotarcia do v
                                              # (koszt do u + krawędź u→v)

                if v not in d or g_new < d[v]:  # jeśli v jeszcze nie odkryty
                                              # LUB znaleźliśmy krótszą drogę

                    d[v] = g_new              # zaktualizuj g(v) = faktyczny koszt do v

                    f[v] = g_new + h(v)       # zaktualizuj f(v) = g(v) + h(v)
                                              # f kieruje przeszukiwanie:
                                              #   niskie f = „obiecujący" wierzchołek
                                              #   (blisko celu wg heurystyki)

                    came_from[v] = u          # zapamiętaj: do v dotarliśmy z u
                                              # (do odtworzenia ścieżki)

        return came_from, d.get(goal)         # came_from = mapa do odtworzenia ścieżki
                                              # d.get(goal) = koszt najkrótszej ścieżki
                                              #   do celu (None jeśli nieosiągalny)
                                              # Złożoność: O(V²) z tablicą, ale w praktyce
                                              #   dużo szybciej dzięki heurystyce

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

