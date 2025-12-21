# Pytanie 30: Modelowanie matematyczne dla problemów decyzyjnych

## Pytanie
**"Omówić metody oraz typowe problemy w modelowaniu matematycznym dla problemów decyzyjnych i optymalizacyjnych."**

Przedmiot: MOM (Metody Optymalizacji Matematycznej)

---

## 📚 Odpowiedź główna

### 1. Struktura modelu matematycznego

```
┌─────────────────────────────────────────────────────────────────┐
│            MODEL OPTYMALIZACYJNY                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   min/max  f(x)           ← Funkcja celu                       │
│                                                                 │
│   subject to:                                                   │
│      g_i(x) ≤ 0           ← Ograniczenia nierównościowe        │
│      h_j(x) = 0           ← Ograniczenia równościowe           │
│      x ∈ X                ← Dziedzina zmiennych                │
│                                                                 │
│   gdzie x = (x₁, x₂, ..., xₙ) ∈ ℝⁿ (lub ℤⁿ, {0,1}ⁿ)          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Metody modelowania

#### 2.1 Etapy tworzenia modelu

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  PROBLEM    │ → │  MODEL      │ → │  ROZWIĄZANIE│ → │  WALIDACJA  │
│  RZECZYWISTY│   │  MATEMATYCZNY│   │  OPTYMALNE  │   │  I WDROŻENIE│
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
      │                 │                 │                 │
      ↓                 ↓                 ↓                 ↓
  Analiza          Zmienne,           Solver,          Interpretacja,
  wymagań          funkcja celu,      algorytm         analiza wrażliwości
                   ograniczenia
```

#### 2.2 Typy modeli

| Typ | Charakterystyka | Przykład |
|-----|-----------------|----------|
| **LP** (Linear Programming) | Liniowa f(x), liniowe g, h | Transport, alokacja |
| **QP** (Quadratic) | Kwadratowa f(x), liniowe ograniczenia | Portfolio |
| **NLP** (Nonlinear) | Nieliniowe f, g lub h | Engineering design |
| **MIP** (Mixed Integer) | Zmienne ciągłe + całkowite | Scheduling, routing |
| **MINLP** | Całkowitoliczbowe + nieliniowe | Najtrudniejsze |

---

### 3. Typowe problemy w modelowaniu

#### 3.1 Wybór zmiennych decyzyjnych

```
Problem: Ile zmiennych? Jakie typy?

Przykład - planowanie produkcji:

Źle: x = "plan produkcji"  (zbyt ogólne)

Dobrze:
x_it = ilość produktu i w okresie t (ciągła)
y_it = czy produkujemy i w t (binarna)
z_ijt = transport z i do j w t (całkowita)

Zasady:
✓ Zmienne muszą być mierzalne
✓ Zmienne muszą być kontrolowalne
✓ Minimalna liczba dla pełnego opisu
```

#### 3.2 Problem Big-M

```
Modelowanie implikacji: y=1 → x ≤ 5

Zła formulacja (słaba relaksacja):
x ≤ 5 + M(1-y), gdzie M = 10^6

Lepsza formulacja:
x ≤ 5 + (UB_x - 5)(1-y), gdzie UB_x = upper bound na x

Indicator constraints (jeśli solver wspiera):
y = 1 → x ≤ 5  (bezpośrednio)

Problem: Duże M → słaba LP relaxation → wolny B&B
```

#### 3.3 Symetria

```
Problem: Wiele równoważnych rozwiązań optymalnych

Przykład - bin packing:
  Bin 1: {A, B}, Bin 2: {C}
  Bin 1: {C}, Bin 2: {A, B}  ← ta sama wartość!

Rozwiązanie - symmetry breaking:
  x[i][1] ≥ x[i][2] ≥ x[i][3] ...  (lexicographic ordering)
  
Lub: użyj indeksu pierwszego użycia pojemnika
```

#### 3.4 Walidacja modelu

| Test | Opis |
|------|------|
| **Extreme cases** | Czy model działa dla skrajnych danych? |
| **Known solutions** | Czy odtwarza znane rozwiązania? |
| **Dimensional analysis** | Czy jednostki się zgadzają? |
| **Sensitivity analysis** | Jak rozwiązanie reaguje na zmiany? |
| **Infeasibility** | Czy model ma rozwiązanie dopuszczalne? |

---

### 4. Techniki modelowania

#### 4.1 Linearyzacja

```
Problem: xy (iloczyn zmiennych ciągłych)

McCormick envelopes:
w ≥ x·LB_y + y·LB_x - LB_x·LB_y
w ≥ x·UB_y + y·UB_x - UB_x·UB_y
w ≤ x·LB_y + y·UB_x - LB_y·UB_x
w ≤ x·UB_y + y·LB_x - UB_y·LB_x

Problem: |x| (wartość bezwzględna)

Modelowanie:
min z
z ≥ x
z ≥ -x
```

#### 4.2 Modelowanie warunków logicznych

```
Alternatywa (OR): x ≤ 5 ∨ y ≤ 3

x ≤ 5 + M(1-z)
y ≤ 3 + Mz
z ∈ {0,1}

Koniunkcja (AND): x ≤ 5 ∧ y ≤ 3

x ≤ 5
y ≤ 3  (po prostu oba ograniczenia)
```

#### 4.3 Piece-wise linear functions

```
f(x) = różne liniowe segmenty

      f(x)
        ↑
        │    /
        │   /
        │  /
        │ /____
        │/
        └────────→ x

Modelowanie SOS2 (Special Ordered Set type 2):
f(x) = Σ λ_i · f(breakpoint_i)
x = Σ λ_i · breakpoint_i
Σ λ_i = 1
λ ≥ 0, max 2 sąsiednie λ_i > 0
```

---

### 5. Wielokryterialne podejmowanie decyzji

```
min f₁(x), f₂(x), ..., f_k(x)  ← konfliktujące cele

Metody:

1. WEIGHTED SUM:
   min Σ w_i · f_i(x)
   Problem: nie znajduje wszystkich Pareto-optymalnych

2. ε-CONSTRAINT:
   min f₁(x)
   s.t. f_i(x) ≤ ε_i, i=2..k

3. GOAL PROGRAMMING:
   min Σ |f_i(x) - target_i|

4. PARETO FRONT:
   Znajdź wszystkie niezdominowane rozwiązania
```

---

### 6. Analiza wrażliwości

```
┌─────────────────────────────────────────────────────────────────┐
│ Co się zmieni gdy zmienią się dane wejściowe?                  │
├─────────────────────────────────────────────────────────────────┤
│ Shadow price (dual variable):                                   │
│   - Ile warta jest jednostka zasobu?                           │
│   - Δf = λ · Δb (dla małych zmian RHS)                        │
│                                                                 │
│ Reduced cost:                                                   │
│   - O ile musi się zmienić c_j żeby x_j wszedł do bazy?       │
│                                                                 │
│ Range analysis:                                                 │
│   - Przedział zmian parametrów bez zmiany optymalnej bazy     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7. Częste błędy

| Błąd | Konsekwencja | Rozwiązanie |
|------|--------------|-------------|
| **Brak bounds** | Unbounded lub słaba relaxation | Zawsze definiuj LB, UB |
| **Za duże M** | Numerical issues, wolne | Tight big-M |
| **Redundantne ograniczenia** | Wolniejsze, confusion | Minimalizuj |
| **Zła skala** | Numerical instability | Scaling, rescaling |
| **Over-modeling** | Za złożone, wolne | Simplify, aggregate |

---

## 🧠 Mnemoniki

### "VCO = Variables, Constraints, Objective":
Trzy elementy modelu matematycznego

### "Big-M = Big Mistake (jeśli źle użyte)":
Unikaj dużych M, tight bounds

### "PASS = Pareto, Analysis, Sensitivity, Symmetry":
Kluczowe zagadnienia zaawansowane

---

## ❓ Pytania dodatkowe

### Q1: "Jak sprawdzić czy model jest poprawny?"
**Odpowiedź:** Testy na znanych instancjach, extreme cases, dimensional analysis, sprawdzenie czy relaksacja LP daje sensowne wyniki, analiza IIS dla infeasible.

### Q2: "Kiedy linearyzować a kiedy użyć NLP?"
**Odpowiedź:** Linearyzuj gdy: nieliniowość jest "miękka", solver MIP szybszy niż NLP, potrzebujesz gwarancji optimum. NLP gdy: silna nieliniowość, ciągłe zmienne, akceptowalny local optimum.

### Q3: "Jak obsłużyć niepewność w modelu?"
**Odpowiedź:** Stochastic programming (scenariusze), robust optimization (worst-case), chance constraints, sensitivity analysis. Wybór zależy od charakteru niepewności.

---

## 🎯 Kluczowe punkty

1. **Model:** Zmienne + funkcja celu + ograniczenia
2. **Big-M:** Unikaj dużych M, tight formulation
3. **Symetria:** Symmetry breaking constraints
4. **Walidacja:** Extreme cases, known solutions
5. **Wrażliwość:** Shadow prices, reduced costs

---

## 📖 Źródła

1. Williams - "Model Building in Mathematical Programming"
2. Wolsey - "Integer Programming"
3. Nemhauser, Wolsey - "Integer and Combinatorial Optimization"
