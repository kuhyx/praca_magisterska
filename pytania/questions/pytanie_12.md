## PYTANIE 12: Sieciowe modele optymalizacji (WSYZ)

**Przedstawić sieciowe modele optymalizacji stosowane w systemach zarządzania.**

---

### Tło pojęciowe — słowniczek

**Graf (graph)** — struktura: zbiór **węzłów** (vertices) połączonych **krawędziami** (edges). Podstawowa abstrakcja dla wszystkich modeli sieciowych. Krawędzie mogą mieć wagi (koszt, odległość, przepustowość) i kierunek (graf skierowany).

    A──5──B──3──C       graf ważony nieskierowany
    │           │       węzły: A,B,C,D
    2           4       krawędzie z wagami
    │           │
    D─────7─────┘

**Sieć (network)** — graf z interpretacją: węzły = lokalizacje/zadania, krawędzie = połączenia/trasy, wagi = koszty/czasy/przepustowości. Modele sieciowe rozwiązują problemy optymalizacyjne na takich grafach.

**Optymalizacja** — znalezienie najlepszego rozwiązania (minimum lub maksimum funkcji celu) przy zadanych ograniczeniach. W kontekście sieciowym: najkrótsza trasa, maksymalny przepływ, minimalny koszt itp.

---

**Najkrótsza ścieżka (shortest path)** — znajdź ścieżkę od źródła do celu o minimalnej sumie wag. Zastosowanie: GPS, routing sieciowy.

**Dijkstra** — algorytm zachłanny. Bierze najbliższy nieodwiedzony węzeł, aktualizuje odległości sąsiadów. Wymaga wag ≥ 0. Złożoność: O(E log V) z kopcem. Dla V=1000, E=5000: ~60 000 operacji.

**Bellman-Ford** — obsługuje ujemne wagi. Relaksuje wszystkie krawędzie V-1 razy. O(VE). Wykrywa cykle ujemne.

**A\*** — rozszerzenie Dijkstry z heurystyką (szacuje odległość do celu). Szybszy w praktyce, bo eksploruje w kierunku celu. Używany w nawigacji, grach.

---

**Maksymalny przepływ (max flow)** — znajdź największy przepływ od źródła (s) do ujścia (t) w sieci z ograniczonymi przepustowościami krawędzi. Zastosowanie: przepustowość linii, ruch sieciowy, planowanie.

**Ford-Fulkerson** — metoda: znajdź ścieżkę powiększającą (augmenting path) w sieci rezydualnej, powiększ przepływ, powtarzaj. Twierdzenie max-flow min-cut: max. przepływ = min. przepustowość przekroju.

**Edmonds-Karp** — implementacja Ford-Fulkerson z BFS (zamiast DFS). Gwarantuje O(VE²). Dla V=100, E=500: ~25 000 000 operacji max.

---

**Problem przydziału (assignment problem)** — przydziel n zadań do n pracowników, minimalizując łączny koszt. Każdy pracownik dostaje dokładnie jedno zadanie. Macierz kosztów n×n.

    Pracownik   Z1   Z2   Z3
    A           8    4    7
    B           5    2    3
    C           9    4    8
    Optymalne: A→Z2(4), B→Z3(3), C→Z1(9) = 16

**Algorytm węgierski (Hungarian algorithm)** — rozwiązuje problem przydziału optymalnie w O(n³). Nazwa od prac matematyków węgierskich: Kőnig i Egerváry.

---

**TSP (Travelling Salesman Problem / problem komiwojażera)** — odwiedź wszystkie miasta dokładnie raz i wróć do startu, minimalizując trasę. **NP-trudny** — nie ma znanego algorytmu wielomianowego. Dla n=20 miast: 20!/2 ≈ 1.2×10¹⁸ tras do sprawdzenia brute-force! W praktyce: heurystyki (nearest neighbor, 2-opt, simulated annealing, algorytmy genetyczne).

**NP-trudny (NP-hard)** — klasa problemów, dla których nie znamy algorytmu rozwiązującego w czasie wielomianowym. Nie oznacza „niemożliwe" — oznacza „nie da się szybko dla dużych instancji" (czas rośnie wykładniczo). Stosuje się heurystyki i przybliżenia.

---

**CPM (Critical Path Method)** — metoda harmonogramowania projektów. Wyznacza **ścieżkę krytyczną** = najdłuższą ścieżkę w grafie zadań. Opóźnienie zadania na ścieżce krytycznej opóźnia cały projekt. O(V+E). Zastosowanie: budownictwo, inżynieria.

**PERT (Program Evaluation and Review Technique)** — podobna do CPM, ale z niepewnością czasu (optymistyczny, pesymistyczny, prawdopodobny → rozkład β). Opracowana dla US Navy (program Polaris, 1958).

**MST (Minimum Spanning Tree / minimalne drzewo rozpinające)** — połącz wszystkie węzły grafu minimalnym kosztem (bez cykli). Zastosowanie: sieci telekomunikacyjne, elektryczne, wodociągowe.

**Kruskal** — sortuj krawędzie rosnąco, dodawaj najlżejszą nie tworzącą cyklu. O(E log E). Używa Union-Find.
**Prim** — startuj od węzła, dodawaj najtańszą krawędź prowadzącą na zewnątrz drzewa. O(E log V) z kopcem.

**Minimalny koszt przepływu (min-cost flow)** — połączenie max flow i najkrótszej ścieżki: przesyłaj zadany przepływ od s do t z minimalnym łącznym kosztem. Zastosowanie: transport, logistics.

---

### 1. Najkrótsza ścieżka — GPS, routing (Dijkstra, Bellman-Ford, A*)
### 2. Maksymalny przepływ — przepustowość linii, dystrybucja (Ford-Fulkerson, Edmonds-Karp)
### 3. Minimalny koszt przepływu — minimalizacja kosztów transportu przy zadanym przepływie
### 4. Problem przydziału — n zadań do n osób, minimalizacja kosztów (algorytm węgierski, O(n³))
### 5. TSP (komiwojażer) — odwiedź wszystkie miasta raz, minimalizuj trasę (NP-trudny, heurystyki)
### 6. CPM/PERT — harmonogramowanie projektów, ścieżka krytyczna
### 7. MST (drzewo rozpinające) — połącz wszystkie węzły minimalnym kosztem (Kruskal, Prim)

---

![Sieciowe modele optymalizacji — schemat mnemoniczny](img/network_models_mnemonic.png)

### MNEMONIK: „**Nasz Mały Mikołaj Przydzielił Trasy Ciężarówkom Mapując**" (NMMPTyCM)

Wyobraź sobie firmę kurierską „Nasz Mały Mikołaj" — Mikołaj musi:

| # | Litera | Model | Analogia Mikołaja | Pytanie, które rozwiązuje |
|---|--------|-------|--------------------|--------------------------|
| 1 | **N**asz | **N**ajkrótsza ścieżka | Mikołaj szuka najkrótszej drogi do domu Janka | „Jak dojechać NAJSZYBCIEJ z A do B?" |
| 2 | **M**ały | **M**aksymalny przepływ | W rurkach do fabryki może płynąć max X czekolady/h | „Ile max mogę przesłać od źródła do ujścia?" |
| 3 | **M**ikołaj | **M**inimalny koszt przepływu | Muszę wysłać 1000 paczek — NAJTANIEJ | „Jak przesłać X jednostek najtaniej?" |
| 4 | **P**rzydzielił | **P**rzydział (assignment) | Przydziel 5 elfów do 5 stanowisk (każdy 1 zadanie) | „Kto robi co? (n:n, min koszt)" |
| 5 | **T**rasy | **T**SP (komiwojażer) | Mikołaj musi odwiedzić WSZYSTKIE domy w jedną noc | „Objazd WSZYSTKICH punktów — najkrótsza trasa?" |
| 6 | **C**iężarówkom | **C**PM/PERT | Harmonogram budowy nowej fabryki zabawek | „Ile MIN trwa projekt? Co jest krytyczne?" |
| 7 | **M**apując | **M**ST (min spanning tree) | Połącz WSZYSTKIE wioski drogami za MIN koszt | „Jak połączyć WSZYSTKO najnajtaniej?" |

**Wizualna historia do zapamiętania (wyobraź sobie sceny jak komiks):**

    Scena 1  (N) — Mikołaj w GPS → najkrótsza ścieżka
    Scena 2  (M) — Rury z czekoladą → max flow
    Scena 3  (M) — Paczki z ceną → min cost flow
    Scena 4  (P) — Tablica z elfami → assignment
    Scena 5  (T) — Sanie oblatujące glob → TSP
    Scena 6  (C) — Kalendarz budowy → CPM/PERT
    Scena 7  (M) — Mapa z drogami → MST

**Alternatywna pamięciówka — pytania (do szybkiego mappowania):**

Dostałeś pytanie → które to pytanie → który model?
1. „Jak dojechać z A do B?" → **Najkrótsza ścieżka** (Dijkstra)
2. „Ile max przesłać?" → **Max flow** (Ford-Fulkerson)
3. „Jak najtaniej przesłać X?" → **Min cost flow**
4. „Kto robi co? (1:1)" → **Przydział** (węgierski)
5. „Objazd wszystkiego" → **TSP** (heurystyki)
6. „Ile trwa projekt?" → **CPM/PERT**
7. „Połącz wszystko najtaniej" → **MST** (Kruskal/Prim)

**Trik: 2 i 3 to warianty PRZEPŁYWU** (max flow vs min-cost flow). Pamiętaj: „PRZEPŁYW ma 2 wersje: max ilość vs min cena". Więc naprawdę musisz zapamiętać 6 UNIKALNYCH modeli + 1 wariant.

**Trik: paruj modele w 3 pary + 1:**
- DROGI: Najkrótsza ścieżka + MST (oba dotyczą krawędzi grafu)
- PRZEPŁYW: Max flow + Min cost flow (oba o przepustowości)
- ZARZĄDZANIE: Przydział + CPM/PERT (oba o organizacji pracy)
- SAM: TSP (jedyny NP-trudny, „komiwojażer")

---

| Model               | Złożoność       | Zastosowanie              |
|----------------------|-----------------|---------------------------|
| Najkrótsza ścieżka  | O(E log V)      | Logistyka, routing        |
| Max Flow             | O(VE²)          | Planowanie, dystrybucja   |
| Przydział            | O(n³)           | HR, grafiki               |
| TSP                  | NP-trudny       | Trasy kurierów            |
| CPM                  | O(V+E)          | Zarządzanie projektami    |
| MST                  | O(E log V)      | Sieci infrastrukturalne   |

### Etymologia

**Ford-Fulkerson** — Lester Ford Jr. + Delbert Fulkerson (1956). **Edmonds-Karp** — Jack Edmonds + Richard Karp (1972); BFS-owa wersja Ford-Fulkerson. **TSP (komiwojażer)** — z XIX-wiecznych niemieckich podręczników dla handlowców. **CPM** — Critical Path Method (DuPont, 1957). **PERT** — Program Evaluation and Review Technique (US Navy, Polaris, 1958). **Kruskal** — Joseph Kruskal (1956). **Prim** — Robert Prim (1957; niezależnie Jarník 1930). **Algorytm węgierski** — Harold Kuhn (1955); od prac Węgrów: Kőniga i Egerváry'ego.

### Jak zapamiętać

- **Mnemonik: „Nasz Mały Mikołaj Przydzielił Trasy Ciężarówkom Mapując"**
  - **N**ajkrótsza ścieżka, **M**ax flow, **M**in cost flow, **P**rzydział, **T**SP, **C**PM, **M**ST
- **3 pary + 1:** DROGI (ścieżka+MST), PRZEPŁYW (max+min cost), ZARZĄDZANIE (przydział+CPM) + TSP sam
- **6 modeli na grafach + 1 wariant:** Wszystko = „węzły + krawędzie + wagi → optymalizuj"
- **Pytanie-klucz:** „Jak dojechać?"=ścieżka, „ile max?"=flow, „kto co?"=przydział, „objazd?"=TSP, „ile trwa?"=CPM, „połącz?"=MST

