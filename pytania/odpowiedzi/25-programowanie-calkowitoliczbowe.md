# Pytanie 25: Programowanie całkowitoliczbowe (MIP)

## Pytanie
**"Gdzie znajdują zastosowania zadania programowania matematycznego całkowitoliczbowego i jak można je rozwiązywać? Omówić wybraną metodę dokładną, wyjaśnić dla jakich praktycznych problemów ma ona zastosowanie i co może wpływać na jej efektywność."**

Przedmiot: MOD (Metody Optymalizacji Dyskretnej)

---

## 📚 Odpowiedź główna

### 1. Definicja MIP (Mixed Integer Programming)

```
Programowanie całkowitoliczbowe:

min  c^T x
s.t. Ax ≤ b
     x_i ∈ Z  dla i ∈ I  (zmienne całkowite)
     x_j ∈ R  dla j ∈ J  (zmienne ciągłe)
     x ≥ 0

Przypadki szczególne:
- IP (Integer Programming): wszystkie zmienne całkowite
- BIP (Binary IP): x_i ∈ {0,1}
- MIP (Mixed IP): część całkowite, część ciągłe
```

---

### 2. Zastosowania

| Dziedzina | Problem | Zmienne binarne |
|-----------|---------|-----------------|
| **Logistyka** | Vehicle Routing (VRP) | x_ij = czy trasa i→j |
| **Produkcja** | Scheduling, Lot sizing | y_t = czy produkować w t |
| **Transport** | Facility Location | y_i = czy otworzyć magazyn i |
| **Telekomunikacja** | Network Design | x_e = czy użyć krawędzi e |
| **Finanse** | Portfolio (min transakcji) | y_i = czy inwestować w i |
| **Energia** | Unit Commitment | y_t = czy uruchomić generator |

### Przykład: Problem plecakowy (Knapsack)

```
max  Σ v_i x_i       (wartość)
s.t. Σ w_i x_i ≤ C   (pojemność)
     x_i ∈ {0,1}     (brać lub nie)

Przedmioty: (wartość, waga)
Item 1: (60, 10)
Item 2: (100, 20)
Item 3: (120, 30)
Pojemność: C = 50

Optymalne: x = [1,1,1] niemożliwe (waga=60)
           x = [1,0,1] wartość=180, waga=40 ✓
```

---

### 3. Metody rozwiązywania

| Metoda | Typ | Gwarancja optimum |
|--------|-----|-------------------|
| **Branch and Bound** | Dokładna | ✅ |
| **Branch and Cut** | Dokładna | ✅ |
| **Branch and Price** | Dokładna | ✅ |
| **Cutting Planes** | Dokładna | ✅ |
| **Heurystyki** | Przybliżona | ❌ |
| **Metaheurystyki** | Przybliżona | ❌ |

---

### 4. Branch and Bound (B&B) - metoda dokładna

#### Idea

```
1. Relaksacja LP: rozwiąż bez ograniczeń całkowitoliczbowych
2. Jeśli rozwiązanie całkowite → gotowe
3. Jeśli nie → rozgałęź (branch) na zmiennej niecałkowitej
4. Przycinaj (bound) gdy dolne ograniczenie ≥ najlepsze znane

        LP relaxation
        x* = 2.7
            /\
           /  \
     x ≤ 2    x ≥ 3
        /        \
    LP: z=10    LP: z=8
       /           \
   (dalej)     (przycinaj jeśli
               najlepsze ≥ 8)
```

#### Algorytm szczegółowy

```
BranchAndBound(P):
  Q = {P}              // kolejka podproblemów
  best = -∞            // najlepsze rozwiązanie
  best_x = null
  
  while Q not empty:
    P' = select(Q)     // wybierz podproblem
    z, x = LP_relax(P') // rozwiąż relaksację
    
    if z ≤ best:       // BOUND: przycięcie
      continue
      
    if x is integer:   // rozwiązanie całkowite
      if z > best:
        best = z
        best_x = x
    else:              // BRANCH: rozgałęzienie
      i = fractional_var(x)  // wybierz zmienną
      P1 = P' + {x_i ≤ floor(x_i)}
      P2 = P' + {x_i ≥ ceil(x_i)}
      Q.add(P1, P2)
  
  return best_x
```

#### Przykład: Max 3x + 2y, x + y ≤ 4, x,y ∈ Z+

```
         Root: LP opt
         x=4, y=0, z=12
         (całkowite!) → DONE
         
Bardziej interesujący przykład:
max 5x + 8y
    x + y ≤ 6
    5x + 9y ≤ 45
    x, y ≥ 0, integer

LP: x=2.25, y=3.75, z=41.25
                │
        ┌───────┴───────┐
        y ≤ 3           y ≥ 4
        │               │
    x=3, y=3        x=1.8, y=4
    z=39 (int!)     z=41
        │               │
    incumbent=39    ┌───┴───┐
                    x≤1     x≥2
                    │       │
                  z=40    infeas.
                  x=1,y=4
                  (int!)
                  
Optimum: x=1, y=4, z=40
```

---

### 5. Czynniki wpływające na efektywność B&B

| Czynnik | Wpływ | Strategie |
|---------|-------|-----------|
| **Jakość relaksacji** | Lepsza → mniej węzłów | Silne formulacje, cutting planes |
| **Wybór zmiennej do branch** | Balans drzewa | Most fractional, strong branching |
| **Wybór węzła** | DFS vs BFS | Best-first (best bound) |
| **Przerywanie** | Jakość incumbent | Heurystyki, warm start |
| **Symetria** | Wiele równoważnych rozw. | Symmetry breaking constraints |

#### Strategie wyboru zmiennej (branching)

| Strategia | Opis |
|-----------|------|
| **Most fractional** | x_i najbliżej 0.5 |
| **First fractional** | Pierwsza niecałkowita |
| **Strong branching** | Testuj kandydatów przez LP |
| **Pseudocost** | Historia wpływu na bound |

#### Strategie wyboru węzła

| Strategia | Właściwości |
|-----------|-------------|
| **Best-first** | Najlepszy bound → mniej węzłów |
| **Depth-first** | Szybko znajduje rozwiązania |
| **Best-estimate** | Kombinacja bound + estimate |

---

### 6. Ulepszenia: Branch and Cut

```
Branch and Bound + Cutting Planes:

W każdym węźle:
1. Rozwiąż LP relaksację
2. Jeśli rozwiązanie niecałkowite:
   - Generuj cięcia (Gomory, Cover, Clique...)
   - Dodaj cięcia do LP
   - Powtórz do limitu
3. Jeśli nadal niecałkowite → branch

Cięcia zacieśniają relaksację LP bez odcinania
rozwiązań całkowitoliczbowych!

        ┌─────────────────────┐
        │   Politop LP        │
        │    ╱─────╲          │
        │   ╱       ╲ cięcie  │
        │  ●─────────●        │
        │  │ ●     ● │        │
        │  │   ● ●   │ rozw.  │
        │  │ ●     ● │ całk.  │
        │  ●─────────●        │
        └─────────────────────┘
```

---

### 7. Narzędzia

| Solver | Typ | Licencja |
|--------|-----|----------|
| **CPLEX** | Komercyjny | IBM |
| **Gurobi** | Komercyjny | Academic free |
| **SCIP** | Open source | ZIB |
| **CBC** | Open source | COIN-OR |
| **OR-Tools** | Open source | Google |

---

## 🧠 Mnemoniki

### "B&B = Branch by variable, Bound by LP":
Rozgałęziaj na zmiennej, przycinaj przez relaksację

### "MIP = Mix of Integer and continuous":
Część zmiennych całkowita, część ciągła

### "Tight LP = Fast B&B":
Lepsza relaksacja → mniej węzłów do sprawdzenia

---

## ❓ Pytania dodatkowe

### Q1: "Co to jest integrality gap?"
**Odpowiedź:** Różnica między optimum LP (relaksacja) a optimum IP. Mała luka = silna formulacja = szybki B&B. Gap = (LP_opt - IP_opt) / IP_opt.

### Q2: "Kiedy B&B jest nieefektywny?"
**Odpowiedź:** Słaba relaksacja (duży gap), dużo symetrii, wiele prawie równoważnych rozwiązań. Wtedy: miliony węzłów, długi czas. Rozwiązanie: silniejsze formulacje, symmetry breaking, heurystyki.

### Q3: "Co to jest cięcie Gomory'ego?"
**Odpowiedź:** Automatycznie generowane cięcie z tablicy simplex. Odcina aktualne rozwiązanie LP bez odcinania punktów całkowitych. Słabe dla dużych problemów, lepsze: cover cuts, clique cuts dla konkretnych struktur.

---

## 🎯 Kluczowe punkty

1. **MIP:** Optymalizacja ze zmiennymi całkowitymi (NP-trudna)
2. **Zastosowania:** Scheduling, routing, facility location
3. **B&B:** Relaksacja LP + branching + bounding
4. **Efektywność:** Jakość relaksacji, strategia branching, cięcia
5. **Narzędzia:** CPLEX, Gurobi, SCIP, CBC

---

## 📖 Źródła

1. Wolsey - "Integer Programming"
2. Nemhauser, Wolsey - "Integer and Combinatorial Optimization"
3. CPLEX User Manual
4. Achterberg - "SCIP: Solving Constraint Integer Programs"
