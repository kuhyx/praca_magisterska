# Pytanie 2: Algorytmy najkrótszej ścieżki

## Pytanie
**"Omówić i porównać algorytmy najkrótszej ścieżki wskazując ich kluczowe właściwości i logikę budowy: Dijkstry, Belmana-Forda, A*."**

Przedmiot: AISDI (Algorytmy i Struktury Danych)

---

## 📚 Odpowiedź główna

### Wprowadzenie - problem najkrótszej ścieżki

**Problem:** Dany jest graf G = (V, E) z funkcją wag w: E → ℝ. Znajdź ścieżkę z wierzchołka źródłowego s do wierzchołka docelowego t o minimalnej sumie wag krawędzi.

**Warianty problemu:**
1. **Single-Source Shortest Path (SSSP)** - z jednego źródła do wszystkich wierzchołków
2. **Single-Pair Shortest Path** - z s do konkretnego t
3. **All-Pairs Shortest Path (APSP)** - między wszystkimi parami (Floyd-Warshall)

---

## 1. Algorytm Dijkstry

### Charakterystyka
- **Autor:** Edsger Dijkstra (1956, opublikowany 1959)
- **Typ:** Zachłanny (greedy)
- **Problem:** SSSP - najkrótsze ścieżki z jednego źródła do wszystkich wierzchołków
- **Ograniczenie:** ⚠️ **Tylko nieujemne wagi krawędzi** (w(e) ≥ 0)

### Idea algorytmu (logika budowy)
1. **Relaksacja:** Stopniowe ulepszanie oszacowań odległości
2. **Zachłanność:** W każdym kroku wybieramy wierzchołek o najmniejszej znanej odległości
3. **Optymalna podstruktura:** Najkrótsza ścieżka składa się z najkrótszych podścieżek

### Pseudokod

```
DIJKSTRA(G, w, s):
    // Inicjalizacja
    for each v ∈ V:
        d[v] ← ∞
        π[v] ← NIL
    d[s] ← 0
    
    Q ← priority_queue(V)  // min-heap według d[v]
    S ← ∅                  // zbiór przetworzonych
    
    while Q ≠ ∅:
        u ← EXTRACT-MIN(Q)
        S ← S ∪ {u}
        
        for each v ∈ Adj[u]:    // relaksacja
            if d[u] + w(u,v) < d[v]:
                d[v] ← d[u] + w(u,v)
                π[v] ← u
                DECREASE-KEY(Q, v, d[v])
    
    return d, π
```

### Złożoność czasowa

| Implementacja kolejki | EXTRACT-MIN | DECREASE-KEY | Całkowita |
|----------------------|-------------|--------------|-----------|
| Lista/tablica | O(V) | O(1) | **O(V²)** |
| Kopiec binarny | O(log V) | O(log V) | **O((V + E) log V)** |
| Kopiec Fibonacciego | O(log V)* | O(1)* | **O(V log V + E)** |

*amortyzowane

### Dlaczego nie działa dla ujemnych wag?

```
    A ---(-5)--- B
    |            |
   (1)          (1)
    |            |
    S -----------C
         (2)
```

Dijkstra przetwarza wierzchołki w kolejności rosnącej odległości i oznacza je jako "zakończone". Jeśli waga może być ujemna, późniejszy wierzchołek może "poprawić" już zakończony.

**Przykład:** S→C = 2 (Dijkstra ustala jako finalne), ale S→A→B→C = 1 + (-5) + 1 = -3 < 2

---

## 2. Algorytm Bellmana-Forda

### Charakterystyka
- **Autorzy:** Richard Bellman, Lester Ford Jr. (1958)
- **Typ:** Programowanie dynamiczne
- **Problem:** SSSP z wykrywaniem cykli ujemnych
- **Zaleta:** ✅ **Działa dla ujemnych wag**
- **Ograniczenie:** ⚠️ Graf nie może mieć cyklu o ujemnej sumie wag (ale algorytm go wykrywa!)

### Idea algorytmu (logika budowy)
1. **Indukcja po liczbie krawędzi:** d^(k)[v] = najkrótsza ścieżka do v używająca ≤ k krawędzi
2. **|V|-1 iteracji:** Najkrótsza ścieżka bez cykli ma co najwyżej |V|-1 krawędzi
3. **Relaksacja wszystkich krawędzi:** W każdej iteracji relaksujemy każdą krawędź

### Pseudokod

```
BELLMAN-FORD(G, w, s):
    // Inicjalizacja
    for each v ∈ V:
        d[v] ← ∞
        π[v] ← NIL
    d[s] ← 0
    
    // Główna pętla: |V|-1 iteracji
    for i ← 1 to |V| - 1:
        for each edge (u, v) ∈ E:
            if d[u] + w(u,v) < d[v]:    // relaksacja
                d[v] ← d[u] + w(u,v)
                π[v] ← u
    
    // Wykrywanie cyklu ujemnego
    for each edge (u, v) ∈ E:
        if d[u] + w(u,v) < d[v]:
            return "CYKL UJEMNY"
    
    return d, π
```

### Złożoność czasowa
**O(V · E)** - zawsze, niezależnie od implementacji

Dla grafów gęstych (E ≈ V²): O(V³) - wolniejszy niż Dijkstra O(V²)

### Wykrywanie cyklu ujemnego
Po |V|-1 iteracjach, wszystkie najkrótsze ścieżki (bez cykli) są znalezione.
Jeśli w iteracji |V| nadal można zrelaksować krawędź → istnieje cykl ujemny.

### Optymalizacja: wczesne zakończenie
```
for i ← 1 to |V| - 1:
    changed ← false
    for each edge (u, v) ∈ E:
        if d[u] + w(u,v) < d[v]:
            d[v] ← d[u] + w(u,v)
            π[v] ← u
            changed ← true
    if not changed:
        break  // Brak zmian = gotowe wcześniej
```

---

## 3. Algorytm A* (A-star)

### Charakterystyka
- **Autorzy:** Peter Hart, Nils Nilsson, Bertram Raphael (1968)
- **Typ:** Heurystyczny (informed search)
- **Problem:** Single-Pair - najkrótsza ścieżka z s do konkretnego t
- **Zaleta:** ✅ **Znacznie szybszy niż Dijkstra** dla problemu s→t
- **Wymóg:** Heurystyka dopuszczalna (admissible)

### Idea algorytmu (logika budowy)
1. **Rozszerzenie Dijkstry:** Dodajemy funkcję heurystyczną
2. **f(n) = g(n) + h(n):**
   - g(n) = koszt dotarcia do n (znany)
   - h(n) = heurystyczne oszacowanie kosztu n → cel (szacowany)
   - f(n) = całkowite oszacowanie kosztu ścieżki przez n
3. **Wybieramy wierzchołek o minimalnym f(n)** zamiast minimalnym g(n)

### Pseudokod

```
A-STAR(G, w, s, t, h):
    // Inicjalizacja
    for each v ∈ V:
        g[v] ← ∞
        f[v] ← ∞
        π[v] ← NIL
    g[s] ← 0
    f[s] ← h(s)
    
    OPEN ← priority_queue({s})  // min-heap według f[v]
    CLOSED ← ∅
    
    while OPEN ≠ ∅:
        u ← EXTRACT-MIN(OPEN)
        
        if u = t:
            return RECONSTRUCT-PATH(π, t)
        
        CLOSED ← CLOSED ∪ {u}
        
        for each v ∈ Adj[u]:
            if v ∈ CLOSED:
                continue
                
            tentative_g ← g[u] + w(u, v)
            
            if v ∉ OPEN:
                OPEN ← OPEN ∪ {v}
            else if tentative_g ≥ g[v]:
                continue
            
            π[v] ← u
            g[v] ← tentative_g
            f[v] ← g[v] + h(v)
    
    return "BRAK ŚCIEŻKI"
```

### Heurystyka - kluczowy element

#### Wymagane właściwości:

1. **Dopuszczalność (Admissibility):**
   h(n) ≤ h*(n) dla każdego n
   
   gdzie h*(n) = rzeczywisty koszt n → cel
   
   → Gwarantuje optymalność rozwiązania

2. **Spójność/Monotoniczność (Consistency):**
   h(n) ≤ w(n, m) + h(m) dla każdej krawędzi (n, m)
   
   → Gwarantuje, że węzeł nie musi być ponownie otwarty
   → Spójność implikuje dopuszczalność

#### Popularne heurystyki (dla siatek 2D):

| Heurystyka | Wzór | Ruch |
|------------|------|------|
| **Manhattan** | \|x₁-x₂\| + \|y₁-y₂\| | 4 kierunki |
| **Euklidesowa** | √((x₁-x₂)² + (y₁-y₂)²) | dowolny kąt |
| **Czebyszewa** | max(\|x₁-x₂\|, \|y₁-y₂\|) | 8 kierunków |
| **Oktylowa** | max(Δx, Δy) + (√2-1)·min(Δx, Δy) | 8 kier. + przekątne |

### Złożoność czasowa
- **Najgorszy przypadek:** O((V + E) log V) - jak Dijkstra
- **Praktycznie:** Znacznie lepiej dzięki heurystyce - przeszukuje mniej wierzchołków
- **Zależy od jakości h:** Im lepsza heurystyka, tym mniej eksploracji

### Przypadki specjalne:
- **h(n) = 0:** A* = Dijkstra
- **h(n) = h*(n):** A* idzie prosto do celu (idealna heurystyka)
- **h(n) > h*(n):** Może nie znaleźć optymalnej ścieżki!

---

## 📊 Tabela porównawcza

| Cecha | Dijkstra | Bellman-Ford | A* |
|-------|----------|--------------|-----|
| **Typ** | Zachłanny | Prog. dynamiczne | Heurystyczny |
| **Problem** | SSSP | SSSP | Single-pair (s→t) |
| **Ujemne wagi** | ❌ NIE | ✅ TAK | ❌ NIE |
| **Cykle ujemne** | Błędny wynik | Wykrywa | Błędny wynik |
| **Złożoność** | O(V log V + E) | O(V·E) | O((V+E) log V)* |
| **Pamięć** | O(V) | O(V) | O(V) |
| **Optymalizacja** | Kolejka priorytetowa | Wczesne zakończenie | Heurystyka |
| **Zastosowanie** | Grafy nieujemne | Grafy z ujemnymi | Pathfinding w grach |

*praktycznie często znacznie mniej

---

## 🎮 Zastosowania praktyczne

### Dijkstra
- **Nawigacja GPS** (drogi nie mają ujemnych odległości)
- **Routing w sieciach** (OSPF protocol)
- **Mapy Google/Apple** (dla małych obszarów)

### Bellman-Ford
- **Routing w sieciach** (RIP protocol - prostszy)
- **Arbitraż walutowy** (szukanie cykli ujemnych = zysk!)
- **Systemy z "karami"** (ujemne wagi = bonusy)

### A*
- **Gry komputerowe** - pathfinding NPC, RTS
- **Robotyka** - planowanie ruchu
- **Puzzle** - 8-puzzle, 15-puzzle
- **Nawigacja** - gdy znamy pozycję celu

---

## 🔄 Relaksacja - wspólny element

Wszystkie trzy algorytmy używają **relaksacji krawędzi**:

```
RELAX(u, v, w):
    if d[u] + w(u,v) < d[v]:
        d[v] ← d[u] + w(u,v)
        π[v] ← u
```

**Różnica w kolejności relaksacji:**
- **Dijkstra:** Relaksuje krawędzie wychodzące z wierzchołka o minimalnym d[v]
- **Bellman-Ford:** Relaksuje wszystkie krawędzie w każdej z |V|-1 iteracji
- **A*:** Relaksuje krawędzie wychodzące z wierzchołka o minimalnym f[v] = g[v] + h[v]

---

## 🧠 Mnemoniki

### "DBF - Dijkstra Bellman Ford"
- **D**ijkstra = **D**odatnie wagi tylko
- **B**ellman-Ford = **B**ez ograniczeń (ujemne OK)
- **F**ind cycles = wykrywa cykle ujemne

### "A* = A sterowana"
- **A**lgorytm **A**sterowany heurystyką
- **A**le heurystyka musi być **A**dmissible

### "GREP" dla Dijkstry:
- **G**reedy (zachłanny)
- **R**elaksacja krawędzi
- **E**xtract-min z kolejki
- **P**riority queue kluczowa

### "VE" dla Bellman-Ford:
- **V**-1 iteracji
- **E** krawędzi relaksowanych w każdej

### "HIG" dla A*:
- **H**eurystyka kieruje
- **I**nformed search
- **G**oal-oriented (zorientowany na cel)

### Złożoność - "Dijkstra lubi VlogV, Bellman lubi VE":
- Dijkstra: O(V log V + E) z kopcem Fibonacciego
- Bellman-Ford: O(V · E)

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Pokaż działanie algorytmu Dijkstry na przykładzie"

**Odpowiedź:**

```
Graf:
    A ---(1)--- B
    |           |
   (4)         (2)
    |           |
    S ---(2)--- C ---(1)--- D
```

| Krok | Przetwarzany | d[S] | d[A] | d[B] | d[C] | d[D] |
|------|--------------|------|------|------|------|------|
| Init | - | 0 | ∞ | ∞ | ∞ | ∞ |
| 1 | S | 0 | 4 | ∞ | 2 | ∞ |
| 2 | C | 0 | 4 | 4 | 2 | 3 |
| 3 | D | 0 | 4 | 4 | 2 | 3 |
| 4 | A | 0 | 4 | 4 | 2 | 3 |
| 5 | B | 0 | 4 | 4 | 2 | 3 |

Najkrótsza ścieżka S→D: S → C → D (koszt 3)

---

### Q2: "Jak wykryć ujemny cykl algorytmem Bellman-Forda?"

**Odpowiedź:**

Po |V|-1 iteracjach, wykonujemy jeszcze jedną iterację po wszystkich krawędziach:

```python
# Po głównej pętli
for (u, v) in edges:
    if d[u] + w[u][v] < d[v]:
        return "UJEMNY CYKL ISTNIEJE"
```

**Dlaczego to działa?**
- Najkrótsza ścieżka prosta (bez cykli) ma co najwyżej |V|-1 krawędzi
- Po |V|-1 iteracjach wszystkie takie ścieżki są znalezione
- Jeśli |V|-ta iteracja poprawia cokolwiek → ścieżka przez cykl jest krótsza → cykl ujemny

---

### Q3: "Dlaczego heurystyka musi być dopuszczalna w A*?"

**Odpowiedź:**

**Dopuszczalność:** h(n) ≤ h*(n) - nigdy nie przeszacowujemy kosztu

**Dowód optymalności:**
1. Załóżmy, że A* zwraca ścieżkę P o koszcie g(P)
2. Niech P* będzie optymalną ścieżką o koszcie g(P*)
3. Jeśli g(P) > g(P*), to w momencie zwrócenia P:
   - Jakiś węzeł n na P* był w OPEN
   - f(n) = g(n) + h(n) ≤ g(n) + h*(n) = g(P*) < g(P) = f(goal)
   - Ale A* wybrał goal zamiast n → sprzeczność!

**Przykład niedopuszczalnej heurystyki:**
```
S ---(1)--- A ---(1)--- T
     \                 /
      \---(10)--------/
```
Jeśli h(A) = 5 (a h*(A) = 1), A* może wybrać ścieżkę S→T (koszt 10) zamiast S→A→T (koszt 2).

---

### Q4: "Porównaj A* z Dijkstrą - kiedy użyć którego?"

**Odpowiedź:**

| Sytuacja | Lepszy algorytm |
|----------|-----------------|
| Szukam ścieżki do WSZYSTKICH wierzchołków | **Dijkstra** |
| Szukam ścieżki do JEDNEGO celu | **A*** |
| Nie mam dobrej heurystyki | **Dijkstra** |
| Graf ma strukturę geometryczną (mapa 2D) | **A*** |
| Graf abstrakcyjny (np. stanów) | Zależy od heurystyki |
| Potrzebuję gwarancji optymalności | Oba (A* z dopuszczalną h) |

**Praktycznie:**
- A* z h(n)=0 to Dijkstra
- Dobra heurystyka może zredukować eksplorację o rzędy wielkości
- W grach A* jest standardem (Unity NavMesh używa wariantu A*)

---

### Q5: "Co to jest algorytm Floyd-Warshalla i jak się ma do omawianych?"

**Odpowiedź:**

**Floyd-Warshall** rozwiązuje **All-Pairs Shortest Path (APSP)**:
- Znajduje najkrótsze ścieżki między WSZYSTKIMI parami wierzchołków
- Złożoność: O(V³)
- Działa z ujemnymi wagami (wykrywa cykle ujemne)
- Programowanie dynamiczne

```
for k ← 1 to V:
    for i ← 1 to V:
        for j ← 1 to V:
            d[i][j] ← min(d[i][j], d[i][k] + d[k][j])
```

**Porównanie:**
- SSSP z dodatnimi wagami: Dijkstra O(V log V + E)
- SSSP z ujemnymi wagami: Bellman-Ford O(VE)
- APSP: Floyd-Warshall O(V³) lub V × Dijkstra O(V² log V + VE)

---

### Q6: "Jakie są warianty algorytmu Dijkstry?"

**Odpowiedź:**

1. **Bidirectional Dijkstra:**
   - Równoczesne przeszukiwanie z s i z t
   - Spotykają się w środku
   - ~2× szybszy w praktyce

2. **Dial's Algorithm:**
   - Dla małych, całkowitych wag [0, C]
   - O(V + E + C) zamiast O((V+E) log V)
   - Używa "bucket queue"

3. **Johnson's Algorithm:**
   - APSP dla grafów rzadkich
   - Używa Bellman-Ford + V × Dijkstra
   - O(VE + V² log V) - lepszy niż Floyd-Warshall dla rzadkich grafów

---

## 🎯 Kluczowe punkty do zapamiętania

1. **Dijkstra** = zachłanny, tylko nieujemne wagi, najszybszy dla SSSP
2. **Bellman-Ford** = prog. dynamiczne, ujemne wagi OK, wykrywa cykle ujemne
3. **A*** = Dijkstra + heurystyka, szybki dla single-pair, wymaga h admissible
4. **Relaksacja** = wspólna operacja, różnica w kolejności
5. **Złożoność:** Dijkstra O(V log V + E), BF O(VE), A* zależy od h

---

## 📖 Źródła do pogłębienia

1. Cormen, Leiserson, Rivest, Stein - "Introduction to Algorithms" (CLRS)
2. Sedgewick, Wayne - "Algorithms"
3. Hart, Nilsson, Raphael - "A Formal Basis for the Heuristic Determination of Minimum Cost Paths" (1968)
4. Red Blob Games - "Introduction to A*" (online, interaktywny)
