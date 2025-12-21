# Pytanie 31: Wypukłość i nieliniowość w systemach decyzyjnych

## Pytanie
**"Wyjaśnić główne zagadnienia modelowania matematycznego w systemach decyzyjnych z wykorzystaniem pojęć (nie)wypukłości i (nie)liniowości."**

Przedmiot: MOM (Metody Optymalizacji Matematycznej)

---

## 📚 Odpowiedź główna

### 1. Klasyfikacja problemów optymalizacyjnych

```
┌─────────────────────────────────────────────────────────────────┐
│                    KLASYFIKACJA PROBLEMÓW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                 LINIOWE                    NIELINIOWE           │
│              ┌─────────────┐            ┌─────────────┐        │
│              │     LP      │            │     NLP     │        │
│              │  Simplex,   │            │  Gradient,  │        │
│              │  Interior   │            │  Newton,    │        │
│              │  Point      │            │  SQP        │        │
│              └─────────────┘            └──────┬──────┘        │
│                                                │                │
│                                    ┌───────────┴───────────┐   │
│                                    │                       │   │
│                              WYPUKŁE               NIEWYPUKŁE  │
│                           ┌─────────────┐      ┌─────────────┐ │
│                           │ Convex NLP  │      │ Non-convex  │ │
│                           │ Global opt  │      │ Local opt   │ │
│                           │ gwarantowane│      │ NP-trudne   │ │
│                           └─────────────┘      └─────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Definicje kluczowe

#### Zbiór wypukły

$$S \text{ wypukły} \Leftrightarrow \forall x,y \in S, \forall \lambda \in [0,1]: \lambda x + (1-\lambda)y \in S$$

```
WYPUKŁY:                    NIEWYPUKŁY:
    ●───────●                  ●───────●
   /         \                /    ↗    \
  /           \              /   /       \
 /             \            /___/         \
●               ●          ●               ●
  Każdy odcinek              Odcinek wychodzi
  wewnątrz zbioru            poza zbiór
```

#### Funkcja wypukła

$$f \text{ wypukła} \Leftrightarrow f(\lambda x + (1-\lambda)y) \leq \lambda f(x) + (1-\lambda) f(y)$$

```
      f(x)
        ↑
        │    Funkcja wypukła
        │         /\
        │        /  \
        │       /    \      Cięciwa zawsze
        │      /──────\     powyżej wykresu
        │     /        \
        │    /          \
        └────────────────→ x

      f(x)
        ↑    Funkcja wklęsła (concave)
        │    ________
        │   /        \
        │  /          \    Cięciwa zawsze
        │ /────────────\   poniżej wykresu
        │/              \
        └────────────────→ x
```

---

### 3. Znaczenie wypukłości

#### Własności problemów wypukłych

| Własność | Opis |
|----------|------|
| **Global = Local** | Każde minimum lokalne jest globalne |
| **Jednoznaczność** | Zbiór optymalnych jest wypukły |
| **Efektywność** | Algorytmy wielomianowe (interior point) |
| **Dualność** | Silna dualność (zero duality gap) |
| **Warunki KKT** | Wystarczające dla optimum |

#### Porównanie złożoności

```
Problem          │ Złożoność      │ Gwarancja
─────────────────┼────────────────┼──────────────
LP               │ Wielomianowa   │ Globalne opt.
Convex QP        │ Wielomianowa   │ Globalne opt.
Convex NLP       │ Wielomianowa   │ Globalne opt.
Non-convex NLP   │ NP-trudna      │ Lokalne opt.
MINLP            │ NP-trudna      │ (zależy)
```

---

### 4. Liniowość vs nieliniowość

#### Programowanie liniowe (LP)

$$\min c^T x \quad \text{s.t.} \quad Ax \leq b, \quad x \geq 0$$

```
Cechy LP:
✓ Optimum w wierzchołku (jeśli istnieje)
✓ Simplex: pivotuje między wierzchołkami
✓ Interior Point: przez wnętrze
✓ Zawsze wypukłe
✓ Silna dualność
```

#### Programowanie nieliniowe (NLP)

$$\min f(x) \quad \text{s.t.} \quad g_i(x) \leq 0, \quad h_j(x) = 0$$

```
Typy nieliniowości:

1. Kwadratowa (QP):
   min x'Qx + c'x  s.t. Ax ≤ b
   
   Q ≻ 0 (dodatnio określona) → wypukłe
   Q ma ujemne eigenvalues → niewypukłe

2. Ogólna nieliniowa:
   min sin(x) + x²·y
   s.t. x² + y² ≤ 1
   
   Może być wypukła lub nie
```

---

### 5. Testowanie wypukłości

#### Dla funkcji

```
f(x) jest wypukła jeśli:

1. HESJAN: H = ∇²f(x) ≽ 0 (dodatnio półokreślony) dla wszystkich x

2. Kompozycja:
   - Suma wypukłych → wypukła
   - max(f, g) gdzie f, g wypukłe → wypukła
   - f(Ax+b) gdzie f wypukła → wypukła

3. Znane funkcje wypukłe:
   - x², eˣ, -log(x), |x|, max(x,0)
   - Normy: ||x||₁, ||x||₂
```

#### Dla zbiorów

```
Zbiór S jest wypukły jeśli:

1. Przekrój wypukłych → wypukły
2. {x: Ax ≤ b} → wielościan (wypukły)
3. {x: ||x||₂ ≤ r} → kula (wypukła)
4. {x: f(x) ≤ α} gdzie f wypukła → sublevel set (wypukły)
```

---

### 6. Problemy niewypukłe

#### Konsekwencje

```
┌─────────────────────────────────────────────────────────────────┐
│ PROBLEM NIEWYPUKŁY:                                             │
│                                                                 │
│ f(x)                                                            │
│   ↑        ●                                                    │
│   │       / \      ●  ← lokalne minimum                        │
│   │      /   \    /│\                                           │
│   │     /     \  / │ \                                          │
│   │    /       \/  │  \                                         │
│   │   /    ●      │   \    ● ← globalne minimum                │
│   │  /   local    │    \  /                                     │
│   │ /     min     │     \/                                      │
│   └────────────────────────→ x                                  │
│                                                                 │
│ Algorytmy gradientowe znajdą LOKALNE minimum!                   │
│ Nie ma gwarancji znalezienia globalnego.                        │
└─────────────────────────────────────────────────────────────────┘
```

#### Strategie dla niewypukłych

| Strategia | Opis |
|-----------|------|
| **Multi-start** | Wiele punktów startowych |
| **Global solvers** | BARON, Couenne, SCIP |
| **Relaxation** | Convex relaxation + B&B |
| **Metaheurystyki** | GA, SA, PSO |
| **Reformulation** | Przeformułuj na wypukły |

---

### 7. Przykłady praktyczne

#### Wypukły - Portfolio optimization

```
Markowitz:
min  x'Σx          (wariancja, Q = Σ ≻ 0 → wypukłe!)
s.t. μ'x ≥ r       (minimalny zwrot)
     Σx_i = 1      (pełna inwestycja)
     x ≥ 0         (brak short selling)

Jest WYPUKŁY → globalne optimum gwarantowane
```

#### Niewypukły - Pooling problem

```
Mieszanie strumieni o różnych jakościach:

q_out = Σ(q_i · flow_i) / Σ flow_i

Zawiera ILOCZYN zmiennych (bilinear) → NIEWYPUKŁY
Tylko lokalne optimum gwarantowane (chyba że global solver)
```

#### Granica - SVM

```
Hard margin SVM (separowalne dane):
min  ||w||²
s.t. y_i(w·x_i + b) ≥ 1

Jest WYPUKŁY (QP z liniowymi ograniczeniami)

Kernel SVM - nadal wypukły w przestrzeni dualnej!
```

---

### 8. Dualność

```
Primal (P):               Dual (D):
min f(x)                  max L(λ, μ)
s.t. g(x) ≤ 0             s.t. λ ≥ 0
     h(x) = 0

Lagrangian: L(x,λ,μ) = f(x) + λᵀg(x) + μᵀh(x)

SŁABA DUALNOŚĆ (zawsze):
  d* ≤ p*  (dual ≤ primal)

SILNA DUALNOŚĆ (dla wypukłych + constraint qualification):
  d* = p*  (zero duality gap)

Duality gap dla niewypukłych może być > 0!
```

---

## 🧠 Mnemoniki

### "Convex = Global Local":
Dla wypukłych: każde lokalne = globalne

### "Hesjan ≻ 0 = wypukłe":
Dodatnio określona macierz drugich pochodnych

### "LP ⊂ QP ⊂ Convex NLP":
Każdy LP jest QP, każdy QP (z Q≥0) jest Convex NLP

---

## ❓ Pytania dodatkowe

### Q1: "Jak rozpoznać czy problem jest wypukły?"
**Odpowiedź:** Sprawdź: (1) czy f celu ma Hesjan ≥ 0, (2) czy ograniczenia nierównościowe g_i są wypukłe, (3) czy ograniczenia równościowe h_j są liniowe. Jeśli wszystkie TAK → wypukły.

### Q2: "Co zrobić gdy problem jest niewypukły?"
**Odpowiedź:** Multi-start, global solvers (BARON), convex relaxation, reformulation (np. SDP relaxation dla QCQP), metaheurystyki, decomposition methods.

### Q3: "Czy MILP jest wypukły?"
**Odpowiedź:** Nie w klasycznym sensie (zmienne dyskretne). Ale LP relaxation jest wypukła. Branch & Bound wykorzystuje wypukłość relaksacji do pruning.

---

## 🎯 Kluczowe punkty

1. **Wypukłość:** Global = Local, efektywne algorytmy
2. **Niewypukłość:** Wiele minimów lokalnych, NP-trudne
3. **Hesjan:** ∇²f ≥ 0 → funkcja wypukła
4. **LP zawsze wypukły**, QP zależy od Q
5. **Silna dualność** dla wypukłych

---

## 📖 Źródła

1. Boyd, Vandenberghe - "Convex Optimization"
2. Nocedal, Wright - "Numerical Optimization"
3. Bazaraa et al. - "Nonlinear Programming"
