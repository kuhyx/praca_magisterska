# Pytanie 26: Narzędzia optymalizacji dyskretnej

## Pytanie
**"Scharakteryzować informatyczne narzędzia optymalizacji dyskretnej. Jakie są warunki i wymagania, jakie możliwości oraz trudności wiążą się ze stosowaniem gotowych narzędzi."**

Przedmiot: MOD (Metody Optymalizacji Dyskretnej)

---

## 📚 Odpowiedź główna

### 1. Kategorie narzędzi

```
┌─────────────────────────────────────────────────────────────────┐
│             NARZĘDZIA OPTYMALIZACJI DYSKRETNEJ                  │
├─────────────────────────────────────────────────────────────────┤
│  SOLVERY MIP          │  SOLVERY CP         │  METAHEURYSTYKI  │
│  (Mixed Integer       │  (Constraint        │                  │
│   Programming)        │   Programming)      │                  │
│  ─────────────────    │  ──────────────     │  ──────────────  │
│  CPLEX, Gurobi        │  CP-SAT (Google)    │  LocalSolver     │
│  SCIP, CBC            │  Chuffed, Gecode    │  OptaPlanner     │
│                       │  MiniZinc           │  OR-Tools        │
├─────────────────────────────────────────────────────────────────┤
│  JĘZYKI MODELOWANIA   │  SAT/SMT SOLVERY    │  FRAMEWORKI      │
│  ─────────────────    │  ──────────────     │  ──────────────  │
│  AMPL, GAMS           │  Z3, CVC5           │  PuLP (Python)   │
│  Pyomo, JuMP          │  MiniSat, Glucose   │  CVXPY           │
│  MiniZinc             │                     │  OR-Tools        │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Solvery MIP

| Solver | Licencja | Cechy |
|--------|----------|-------|
| **CPLEX** | Komercyjny (IBM) | Najszybszy dla dużych MIP |
| **Gurobi** | Komercyjny (academic free) | Bardzo szybki, dobry API |
| **SCIP** | Open source (ZIB) | Framework extensible |
| **CBC** | Open source (COIN-OR) | Dobry darmowy solver |
| **HiGHS** | Open source | Nowoczesny, szybki LP/MIP |
| **GLPK** | Open source | Prosty, portable |

### Porównanie wydajności (benchmark)

```
Typowe czasy dla problemów MIPLIB (średnie):

CPLEX    ████████████████████████████  100%
Gurobi   ███████████████████████████   98%
SCIP     ████████████████              60%
CBC      ████████████                  45%
GLPK     ████████                      30%
```

---

### 3. Solvery Constraint Programming

| Solver | Język | Cechy |
|--------|-------|-------|
| **CP-SAT** | Python/C++ | Google, bardzo szybki |
| **Gecode** | C++ | Akademicki, elastyczny |
| **Chuffed** | MiniZinc | Lazy clause generation |
| **OR-Tools** | Multi | Google, CP + routing + MIP |

### Kiedy CP vs MIP?

| Aspekt | MIP | CP |
|--------|-----|-----|
| **Ograniczenia globalne** | Słabo | Świetnie (alldiff, cumulative) |
| **Relaksacja** | LP (silna) | Słabsza |
| **Scheduling** | Średnio | Świetnie |
| **Kombinatoryczne** | Dobrze | Bardzo dobrze |

---

### 4. Języki modelowania

#### AMPL
```ampl
set PRODUCTS;
param profit{PRODUCTS};
param capacity;

var produce{PRODUCTS} >= 0 integer;

maximize total_profit: 
    sum{p in PRODUCTS} profit[p] * produce[p];

subject to capacity_limit:
    sum{p in PRODUCTS} produce[p] <= capacity;
```

#### Pyomo (Python)
```python
from pyomo.environ import *

model = ConcreteModel()
model.x = Var([1,2,3], domain=NonNegativeIntegers)
model.obj = Objective(expr=sum(model.x[i] for i in [1,2,3]), 
                      sense=maximize)
model.con = Constraint(expr=model.x[1] + model.x[2] <= 10)

solver = SolverFactory('gurobi')
solver.solve(model)
```

#### OR-Tools (Python)
```python
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
x = solver.IntVar(0, 10, 'x')
y = solver.IntVar(0, 10, 'y')
solver.Add(x + y <= 15)
solver.Maximize(3*x + 4*y)
solver.Solve()
```

---

### 5. Warunki i wymagania

| Wymaganie | Opis |
|-----------|------|
| **Licencja** | Komercyjne (CPLEX, Gurobi) vs Open source |
| **API/Język** | Python, C++, Java, Julia |
| **Format modelu** | MPS, LP, AMPL, własny |
| **Pamięć** | Duże modele = duże wymagania RAM |
| **Wielowątkowość** | Parallel B&B, concurrent LP |

### Typowe wymagania sprzętowe

```
Mały problem (< 1000 zmiennych):
  - RAM: 4 GB
  - CPU: dowolny
  - Czas: sekundy

Średni problem (1000-100k zmiennych):
  - RAM: 16-32 GB
  - CPU: multi-core
  - Czas: minuty-godziny

Duży problem (> 100k zmiennych):
  - RAM: 64+ GB
  - CPU: wiele rdzeni
  - Czas: godziny-dni
  - Czasem: cluster computing
```

---

### 6. Możliwości

| Możliwość | Opis |
|-----------|------|
| **Gwarancja optimum** | Metody dokładne (B&B, B&C) |
| **Gap tracking** | Śledzenie jakości rozwiązania |
| **Callbacks** | Własne cięcia, heurystyki, lazy constraints |
| **Warm start** | Start od znanego rozwiązania |
| **Tuning** | Automatyczne dostrajanie parametrów |
| **Solution pool** | Wiele rozwiązań (k-best) |

---

### 7. Trudności

| Trudność | Opis | Rozwiązanie |
|----------|------|-------------|
| **Czas obliczeń** | NP-trudność | Heurystyki, time limit |
| **Słaba formulacja** | Duży integrality gap | Silniejsze modele, cięcia |
| **Symetria** | Wiele równoważnych rozw. | Symmetry breaking |
| **Numeryka** | Błędy zaokrągleń | Tolerancje, scaling |
| **Pamięć** | Duże drzewa B&B | Limity węzłów, DFS |
| **Debugowanie** | Infeasible/unbounded | IIS (Irreducible Infeasible Set) |

### Diagnostyka problemów

```
Problem: Model INFEASIBLE

Diagnoza:
1. solver.computeIIS()  # znajdź konflikt
2. Sprawdź constraints
3. Poluzuj ograniczenia

Problem: Zbyt długi czas

Diagnoza:
1. Gap się nie zmniejsza → słaba formulacja
2. Dużo węzłów B&B → symetria
3. LP wolne → presolve, scaling
```

---

### 8. Best practices

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. FORMULACJA                                                   │
│    - Unikaj big-M (słaba relaksacja)                           │
│    - Używaj wskaźnikowych (indicator constraints)              │
│    - Tight bounds na zmienne                                   │
│                                                                 │
│ 2. PREPROCESSING                                                │
│    - Presolve (solver robi automatycznie)                      │
│    - Agregacja zmiennych                                        │
│    - Eliminacja redundancji                                     │
│                                                                 │
│ 3. PARAMETRY SOLVERA                                           │
│    - MIPGap: akceptowalny gap (np. 1%)                        │
│    - TimeLimit: maksymalny czas                                │
│    - Threads: liczba wątków                                    │
│    - Emphasis: feasibility vs optimality                       │
│                                                                 │
│ 4. DEBUGGING                                                    │
│    - Zacznij od małej instancji                                │
│    - Sprawdź relaxację LP                                       │
│    - Użyj IIS dla infeasible                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mnemoniki

### "CPLEX/Gurobi = Commercial Power":
Najszybsze, ale płatne (academic free)

### "SCIP = Swiss army knife":
Open source, extensible, framework

### "CP for Scheduling, MIP for Planning":
CP świetny dla harmonogramowania

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy używać metaheurystyk zamiast solverów?"
**Odpowiedź:** Bardzo duże instancje (miliony zmiennych), brak dobrej formulacji MIP, potrzeba szybkiego "dobrego" rozwiązania bez gwarancji, problemy z wieloma celami, problemy dynamiczne.

### Q2: "Co to jest callback w solverze MIP?"
**Odpowiedź:** Funkcja wywoływana przez solver w trakcie B&B. Typy: lazy constraints (dodaj ograniczenie gdy naruszone), user cuts (wzmocnij relaksację), heuristic (znajdź rozwiązanie), branching (własna strategia).

### Q3: "Jak poprawić słabą formulację?"
**Odpowiedź:** Dodaj valid inequalities (cięcia), zastąp big-M przez indicator constraints, wprowadź dodatkowe zmienne (extended formulation), użyj disaggregation.

---

## 🎯 Kluczowe punkty

1. **MIP solvery:** CPLEX, Gurobi (komercyjne), SCIP, CBC (open source)
2. **CP solvery:** CP-SAT, Gecode - dobre dla scheduling
3. **Języki:** AMPL, Pyomo, OR-Tools
4. **Trudności:** Czas, słaba formulacja, symetria
5. **Best practice:** Tight formulation, callbacks, proper tuning

---

## 📖 Źródła

1. CPLEX User Manual
2. Gurobi Reference Manual
3. Williams - "Model Building in Mathematical Programming"
4. OR-Tools documentation - developers.google.com/optimization
