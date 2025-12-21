# Pytanie 43: Klasyfikacja zadań szeregowania

## Pytanie
**"Jakie cechy zadań szeregowania wykorzystuje się do ich klasyfikacji? Omówić przykładową metodę dla wybranego problemu szeregowania."**

Przedmiot: ZBOP (Zarządzanie i Badania Operacyjne w Produkcji)

---

## 📚 Odpowiedź główna

### 1. Notacja Graham'a (α|β|γ)

```
┌─────────────────────────────────────────────────────────────────┐
│            NOTACJA KLASYFIKACJI ZADAŃ SZEREGOWANIA              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    α | β | γ                                    │
│                    │   │   │                                    │
│                    │   │   └── Kryterium optymalizacji         │
│                    │   └────── Charakterystyki zadań           │
│                    └────────── Środowisko maszynowe            │
│                                                                 │
│ Przykład: Pm | prec, pⱼ=1 | Cmax                               │
│           │     │     │      │                                  │
│           │     │     │      └── minimalizuj makespan          │
│           │     │     └── jednostkowe czasy                    │
│           │     └── ograniczenia kolejnościowe                 │
│           └── m maszyn równoległych                            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Pole α - Środowisko maszynowe

| Symbol | Opis |
|--------|------|
| **1** | Jedna maszyna |
| **P** | Maszyny równoległe identyczne |
| **Pm** | m maszyn równoległych identycznych |
| **Q** | Maszyny równoległe o różnych prędkościach |
| **R** | Maszyny niezwiązane (unrelated) |
| **F** | Flow shop (linia produkcyjna) |
| **Fm** | Flow shop z m maszynami |
| **J** | Job shop |
| **Jm** | Job shop z m maszynami |
| **O** | Open shop |

```
JEDNA MASZYNA (1):
  Job 1 ──→ ┌───┐
  Job 2 ──→ │ M │ ──→ Output
  Job 3 ──→ └───┘

MASZYNY RÓWNOLEGŁE (Pm):
  Job 1 ──→ ┌───┐
            │M1 │ ──→
  Job 2 ──→ ├───┤
            │M2 │ ──→ Output
  Job 3 ──→ ├───┤
            │M3 │ ──→
            └───┘

FLOW SHOP (F):
  Job 1 ──→ ┌───┐ ──→ ┌───┐ ──→ ┌───┐ ──→
            │M1 │     │M2 │     │M3 │
  Job 2 ──→ └───┘ ──→ └───┘ ──→ └───┘ ──→

JOB SHOP (J):
  Każde zadanie ma własną trasę przez maszyny
  Job 1: M1 → M3 → M2
  Job 2: M2 → M1 → M3
```

---

### 3. Pole β - Charakterystyki zadań

| Symbol | Opis |
|--------|------|
| **rⱼ** | Release dates (terminy dostępności) |
| **dⱼ** | Due dates (terminy wymagane) |
| **d̄ⱼ** | Deadlines (nieprzekraczalne terminy) |
| **prec** | Precedence constraints (kolejność) |
| **pmtn** | Preemption allowed (przerwanie dozwolone) |
| **pⱼ=1** | Unit processing times |
| **sᵢⱼ** | Setup times (czasy przezbrojeń) |
| **brkdwn** | Machine breakdowns |
| **batch** | Batch processing |

---

### 4. Pole γ - Kryteria optymalizacji

| Symbol | Nazwa | Formuła |
|--------|-------|---------|
| **Cmax** | Makespan | max Cⱼ |
| **ΣCⱼ** | Total completion time | Σ Cⱼ |
| **Σwⱼ Cⱼ** | Weighted completion | Σ wⱼ Cⱼ |
| **Lmax** | Max lateness | max(Cⱼ - dⱼ) |
| **Tmax** | Max tardiness | max(0, Cⱼ - dⱼ) |
| **ΣTⱼ** | Total tardiness | Σ max(0, Cⱼ - dⱼ) |
| **ΣUⱼ** | Number of tardy jobs | Σ 𝟙(Cⱼ > dⱼ) |

```
Cⱼ = Completion time zadania j
Lⱼ = Cⱼ - dⱼ (lateness, może być ujemne)
Tⱼ = max(0, Lⱼ) (tardiness, ≥ 0)
Uⱼ = 1 jeśli Tⱼ > 0, else 0 (unit penalty)
```

---

### 5. Złożoność obliczeniowa

```
┌─────────────────────────────────────────────────────────────────┐
│ ZŁOŻONOŚĆ WYBRANYCH PROBLEMÓW                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ WIELOMIANOWE (P):                                               │
│   1 || Cmax              O(n)        (dowolna kolejność)       │
│   1 || ΣCⱼ               O(n log n)  (SPT rule)                │
│   1 || Lmax              O(n log n)  (EDD rule)                │
│   Pm || Cmax             O(n log n)  (LPT heuristic)           │
│                                                                 │
│ NP-TRUDNE:                                                      │
│   1 || ΣTⱼ               NP-hard                               │
│   1 || ΣwⱼCⱼ (rⱼ)        NP-hard                               │
│   Pm || Cmax (m≥2)       NP-hard (ale PTAS istnieje)          │
│   Fm || Cmax (m≥3)       NP-hard (flow shop ≥3 maszyny)       │
│   Jm || Cmax             silnie NP-hard                        │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6. Przykładowa metoda: Problem 1 || ΣCⱼ

#### Problem

```
Jedna maszyna, n zadań, minimalizuj sumę czasów zakończenia

Dane:
  Zadanie:    J1   J2   J3   J4   J5
  Czas pⱼ:    5    3    8    2    6
```

#### Metoda: SPT (Shortest Processing Time)

```
┌─────────────────────────────────────────────────────────────────┐
│ REGUŁA SPT: Szereguj zadania w kolejności rosnących pⱼ        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Posortowane: J4(2), J2(3), J1(5), J5(6), J3(8)                │
│                                                                 │
│ Harmonogram:                                                    │
│                                                                 │
│ ├──J4──┼───J2───┼─────J1─────┼──────J5──────┼────────J3────────┤
│ 0      2        5           10            16                   24
│                                                                 │
│ Czasy zakończenia:                                              │
│   C₄ = 2                                                        │
│   C₂ = 2 + 3 = 5                                               │
│   C₁ = 5 + 5 = 10                                              │
│   C₅ = 10 + 6 = 16                                             │
│   C₃ = 16 + 8 = 24                                             │
│                                                                 │
│ ΣCⱼ = 2 + 5 + 10 + 16 + 24 = 57                               │
│                                                                 │
│ Dowód optymalności:                                             │
│   Zamiana sąsiednich i,j gdzie pᵢ > pⱼ zawsze zwiększa ΣC     │
│   SPT daje globalnie optymalne rozwiązanie                     │
└─────────────────────────────────────────────────────────────────┘
```

#### Dlaczego SPT jest optymalne?

```
Dla dwóch zadań i, j:
  Kolejność i→j: Cᵢ = pᵢ, Cⱼ = pᵢ + pⱼ → ΣC = 2pᵢ + pⱼ
  Kolejność j→i: Cⱼ = pⱼ, Cᵢ = pⱼ + pᵢ → ΣC = 2pⱼ + pᵢ

Różnica: (2pᵢ + pⱼ) - (2pⱼ + pᵢ) = pᵢ - pⱼ

Jeśli pᵢ < pⱼ → kolejność i→j lepsza (mniejsza ΣC)
Stąd: krótsze zadania najpierw!
```

---

### 7. Inne klasyczne reguły

| Reguła | Problem | Opis |
|--------|---------|------|
| **SPT** | 1 \|\| ΣCⱼ | Shortest Processing Time |
| **WSPT** | 1 \|\| ΣwⱼCⱼ | Weighted SPT (wⱼ/pⱼ malejąco) |
| **EDD** | 1 \|\| Lmax | Earliest Due Date |
| **LPT** | Pm \|\| Cmax | Longest Processing Time (heur.) |
| **Moore** | 1 \|\| ΣUⱼ | Minimalizacja spóźnionych |
| **Johnson** | F2 \|\| Cmax | 2-machine flow shop |

---

### 8. Algorytm Johnsona (F2 || Cmax)

```
┌─────────────────────────────────────────────────────────────────┐
│ ALGORYTM JOHNSONA - Flow shop 2 maszyny                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Dane: n zadań, czasy (a₁,b₁), (a₂,b₂), ..., (aₙ,bₙ)          │
│       aⱼ = czas na maszynie 1, bⱼ = czas na maszynie 2        │
│                                                                 │
│ Algorytm:                                                       │
│ 1. Podziel zadania na dwa zbiory:                              │
│    U = {j : aⱼ < bⱼ}  (krótszy czas na M1)                    │
│    V = {j : aⱼ ≥ bⱼ}  (krótszy czas na M2)                    │
│                                                                 │
│ 2. Sortuj U rosnąco wg aⱼ                                      │
│    Sortuj V malejąco wg bⱼ                                     │
│                                                                 │
│ 3. Harmonogram: [U posortowane] ++ [V posortowane]             │
│                                                                 │
│ Złożoność: O(n log n)                                          │
│ Optymalność: gwarantowana!                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mnemoniki

### "α|β|γ = Maszyny|Zadania|Cel":
Trzy pola notacji Graham'a

### "SPT = Short First":
Najkrótsze zadania najpierw dla ΣCⱼ

### "EDD = Early Due Date":
Najwcześniejszy termin najpierw dla Lmax

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy stosować heurystyki a kiedy optymalne?"
**Odpowiedź:** Optymalne (SPT, EDD, Johnson) gdy problem wielomianowy. Heurystyki (LPT, dispatching rules) dla NP-trudnych lub gdy wymagana szybkość. Metaheurystyki (GA, SA) dla trudnych instancji.

### Q2: "Co to jest preemption?"
**Odpowiedź:** Możliwość przerwania zadania i kontynuacji później. pmtn w notacji. Upraszcza niektóre problemy (1|pmtn,rⱼ|Lmax jest P, bez pmtn jest NP-hard).

### Q3: "Job shop vs Flow shop?"
**Odpowiedź:** Flow shop: wszystkie zadania ta sama trasa (M1→M2→...→Mm). Job shop: każde zadanie własna trasa. Job shop jest ogólniejszy i trudniejszy (silnie NP-hard nawet dla 3 maszyn).

---

## 🎯 Kluczowe punkty

1. **Notacja α|β|γ:** Maszyny | Zadania | Kryterium
2. **SPT:** Optymalne dla 1||ΣCⱼ, O(n log n)
3. **EDD:** Optymalne dla 1||Lmax
4. **Johnson:** Optymalne dla F2||Cmax
5. **Większość problemów NP-trudna**

---

## 📖 Źródła

1. Pinedo - "Scheduling: Theory, Algorithms, and Systems"
2. Brucker - "Scheduling Algorithms"
3. Graham et al. - "Optimization and Approximation in Deterministic Sequencing"
