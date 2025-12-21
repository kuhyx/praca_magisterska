# Pytanie 12: Sieciowe modele optymalizacji w systemach zarządzania

## Pytanie
**"Przedstawić sieciowe modele optymalizacji stosowane w systemach zarządzania. Omówić ich właściwości."**

Przedmiot: WSYZ (Wstęp do Systemów Zarządzania)

---

## 📚 Odpowiedź główna

### Wprowadzenie

**Sieciowe modele optymalizacji** to matematyczne reprezentacje problemów decyzyjnych w postaci grafów (sieci), gdzie:
- **Węzły** = punkty decyzyjne, lokalizacje, zdarzenia
- **Krawędzie** = połączenia, przepływy, zależności
- **Wagi** = koszty, czasy, przepustowości

---

## 1. Problem najkrótszej ścieżki (Shortest Path)

### Definicja
Znaleźć ścieżkę o minimalnej sumie wag między węzłem źródłowym a docelowym.

```
        2
    A ────→ B
    │       │
  1 │       │ 3
    ↓       ↓
    C ────→ D
        1

Najkrótsza ścieżka A→D: A→C→D (koszt: 2)
```

### Algorytmy
| Algorytm | Złożoność | Wagi ujemne | Zastosowanie |
|----------|-----------|-------------|--------------|
| **Dijkstra** | O(V² lub E log V) | ❌ | GPS, routing |
| **Bellman-Ford** | O(VE) | ✅ | Finanse, arbitraż |
| **A*** | O(E) średnio | ❌ | Gry, nawigacja |

### Zastosowania w zarządzaniu
- Optymalizacja tras dostaw
- Planowanie logistyki
- Routing w sieciach telekomunikacyjnych

---

## 2. Problem maksymalnego przepływu (Max Flow)

### Definicja
Znaleźć maksymalny przepływ ze źródła (s) do ujścia (t) przy ograniczeniach przepustowości.

```
       10        10
   s ────→ A ────→ t
   │       ↑       ↑
 5 │     5 │       │ 10
   ↓       │       │
   B ──────┴───────┘
         15

Max flow = 15 (przez A: 10, przez B: 5)
```

### Algorytmy
| Algorytm | Złożoność | Uwagi |
|----------|-----------|-------|
| **Ford-Fulkerson** | O(E × max_flow) | Metoda ścieżek powiększających |
| **Edmonds-Karp** | O(VE²) | BFS dla ścieżek |
| **Dinic** | O(V²E) | Przepływy blokujące |

### Zastosowania
- Planowanie produkcji (przepustowość linii)
- Zarządzanie siecią dystrybucji
- Przydział zasobów

---

## 3. Problem minimalnego kosztu przepływu (Min Cost Flow)

### Definicja
Przepływ o zadanej wielkości przy minimalnym koszcie (każda krawędź ma przepustowość i koszt jednostkowy).

```
       (cap=10, cost=2)
   s ─────────────────→ A
   │                    │
   │(cap=5, cost=1)     │(cap=10, cost=3)
   ↓                    ↓
   B ─────────────────→ t
       (cap=15, cost=1)

Wymagany przepływ: 10
Min koszt = ?
```

### Zastosowania
- Transport towarów (minimalizacja kosztów)
- Przydział zadań pracownikom
- Optymalizacja łańcucha dostaw

---

## 4. Problem przydziału (Assignment Problem)

### Definicja
Przypisanie n zadań do n wykonawców przy minimalnym koszcie (jeden do jednego).

```
         Zadanie 1  Zadanie 2  Zadanie 3
Prac. A     8          4          7
Prac. B     5          2          3
Prac. C     9          6          4

Optymalny przydział: A→Z2, B→Z1, C→Z3 (koszt: 4+5+4=13)
```

### Algorytm węgierski (Hungarian)
- Złożoność: O(n³)
- Gwarantuje optimum

### Zastosowania
- Planowanie grafików pracy
- Przydział maszyn do zleceń
- Matching w HR (rekrutacja)

---

## 5. Problem komiwojażera (TSP - Travelling Salesman)

### Definicja
Odwiedzić wszystkie węzły dokładnie raz i wrócić do startu przy minimalnym koszcie.

```
    A ──5── B
    │╲    ╱│
   4│ ╲3╱  │6
    │  ╳   │
   2│ ╱ ╲  │7
    │╱    ╲│
    C ──8── D

Optymalna trasa: A→C→D→B→A (koszt: 2+8+6+5=21)
```

### Właściwości
- **NP-trudny** - brak algorytmu wielomianowego
- Dokładne: Branch & Bound, programowanie dynamiczne
- Heurystyki: Nearest Neighbor, 2-opt, symulowane wyżarzanie

### Zastosowania
- Planowanie tras kurierów
- Optymalizacja wizyt serwisowych
- Sekwencjonowanie produkcji

---

## 6. CPM/PERT - Harmonogramowanie projektów

### CPM (Critical Path Method)

```
        ┌──B(3)──┐
       ╱          ╲
A(2)──┤            ├──E(2)──F(1)
       ╲          ╱
        └──C(4)──D(1)

Ścieżka krytyczna: A→C→D→E→F (czas: 2+4+1+2+1=10)
```

### Właściwości
| Cecha | CPM | PERT |
|-------|-----|------|
| Czasy | Deterministyczne | Probabilistyczne (a,m,b) |
| Zastosowanie | Projekty powtarzalne | Projekty R&D |
| Wynik | Ścieżka krytyczna | Rozkład prawdopodobieństwa |

### Zastosowania
- Zarządzanie projektami budowlanymi
- Planowanie wdrożeń IT
- Koordynacja produkcji

---

## 7. Drzewo rozpinające (MST - Minimum Spanning Tree)

### Definicja
Połączyć wszystkie węzły przy minimalnym koszcie (bez cykli).

```
Przed:                Po (MST):
    2                     2
A──────B              A──────B
│╲    ╱│              │      
│3╲1╱ │4              │3     
│  C  │         →     │  C   
│ ╱╲  │               │ ╱    
│╱5 ╲6│               │╱5    
D──────E              D      E
    7                     

Koszt MST: 2+3+1+5=11
```

### Algorytmy
| Algorytm | Złożoność | Strategia |
|----------|-----------|-----------|
| **Kruskal** | O(E log E) | Sortuj krawędzie, Union-Find |
| **Prim** | O(E log V) | Rozbudowa od węzła |

### Zastosowania
- Projektowanie sieci (elektrycznych, telekomunikacyjnych)
- Klasteryzacja danych
- Minimalizacja okablowania

---

## 📊 Porównanie modeli

| Model | Typ problemu | Złożoność | Przykład zastosowania |
|-------|--------------|-----------|----------------------|
| Shortest Path | P | O(E log V) | Nawigacja GPS |
| Max Flow | P | O(V²E) | Planowanie produkcji |
| Min Cost Flow | P | O(V³) | Transport towarów |
| Assignment | P | O(n³) | Grafiki pracy |
| TSP | NP-hard | Wykładnicza | Trasy kurierów |
| CPM/PERT | P | O(V+E) | Projekty |
| MST | P | O(E log V) | Sieci infrastruktury |

---

## 🧠 Mnemoniki

### "SPAM-CT" - modele sieciowe:
- **S**hortest Path
- **P**rzepływ (Max Flow)
- **A**ssignment
- **M**ST
- **C**PM/PERT
- **T**SP

### "Graf = Węzły + Krawędzie + Wagi":
- Węzły = lokalizacje/decyzje
- Krawędzie = połączenia
- Wagi = koszty/czasy/przepustowości

---

## ❓ Możliwe pytania dodatkowe

### Q1: "Jaka jest różnica między CPM a PERT?"
**Odpowiedź:** CPM używa deterministycznych czasów (znanych), PERT używa trzech estymacji (optymistyczna, najbardziej prawdopodobna, pesymistyczna) i rozkładu beta. CPM dla projektów powtarzalnych, PERT dla R&D z niepewnością.

### Q2: "Kiedy stosować heurystyki zamiast algorytmów dokładnych?"
**Odpowiedź:** Gdy problem jest NP-trudny (TSP) lub dane wejściowe bardzo duże. Heurystyki dają "dość dobre" rozwiązanie w rozsądnym czasie. Przykład: 2-opt dla TSP daje rozwiązanie ~5% od optimum w O(n²).

### Q3: "Co to jest slack/float w CPM?"
**Odpowiedź:** Zapas czasu zadania = najpóźniejszy start − najwcześniejszy start. Zadania na ścieżce krytycznej mają slack=0 (opóźnienie opóźni cały projekt).

---

## 🎯 Kluczowe punkty

1. **Sieciowe modele** = problemy jako grafy (węzły, krawędzie, wagi)
2. **Shortest Path, Max Flow, MST** = rozwiązywalne w czasie wielomianowym
3. **TSP** = NP-trudny, wymaga heurystyk
4. **CPM/PERT** = harmonogramowanie, ścieżka krytyczna
5. **Assignment** = optymalne dopasowanie 1:1

---

## 📖 Źródła

1. Hillier, Lieberman - "Introduction to Operations Research"
2. Cormen et al. - "Introduction to Algorithms"
3. Winston - "Operations Research: Applications and Algorithms"
