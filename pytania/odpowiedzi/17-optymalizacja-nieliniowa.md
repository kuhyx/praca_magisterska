# Pytanie 17: Optymalizacja nieliniowa - warunki optymalności

## Pytanie
**"Przedstawić warunki konieczne i dostateczne optymalności różniczkowalnych zadań optymalizacji bez ograniczeń i z ograniczeniami oraz warunki regularności i omówić metody poszukiwania rozwiązań zadań optymalizacji nieliniowej."**

Przedmiot: AMO (Analiza i Metody Optymalizacji)

---

## 📚 Odpowiedź główna

### 1. Optymalizacja bez ograniczeń

#### Problem
$$\min_{x \in \mathbb{R}^n} f(x)$$

#### Warunki konieczne (I rzędu)
Jeśli $x^*$ jest minimum lokalnym i $f$ jest różniczkowalna:
$$\nabla f(x^*) = 0$$

(Gradient zerowy - punkt stacjonarny)

#### Warunki dostateczne (II rzędu)
Jeśli $\nabla f(x^*) = 0$ oraz hesjan $H(x^*) = \nabla^2 f(x^*)$:

| Hesjan | Wniosek |
|--------|---------|
| $H \succ 0$ (dodatnio określony) | **Minimum lokalne** |
| $H \prec 0$ (ujemnie określony) | Maximum lokalne |
| $H$ nieokreślony | Punkt siodłowy |
| $H \succeq 0$ (półdodatni) | Brak wniosku |

**Sprawdzenie:** Wszystkie wartości własne $\lambda_i > 0 \Rightarrow H \succ 0$

---

### 2. Optymalizacja z ograniczeniami

#### Problem ogólny
$$\min_{x} f(x)$$
$$\text{s.t. } g_i(x) \leq 0, \quad i = 1, \ldots, m$$
$$\quad\quad h_j(x) = 0, \quad j = 1, \ldots, p$$

#### Lagrangian
$$L(x, \lambda, \mu) = f(x) + \sum_{i=1}^{m} \lambda_i g_i(x) + \sum_{j=1}^{p} \mu_j h_j(x)$$

---

### 3. Warunki KKT (Karush-Kuhn-Tucker)

#### Warunki konieczne I rzędu

Jeśli $x^*$ jest minimum i spełnione są warunki regularności:

1. **Stacjonarność:**
$$\nabla_x L(x^*, \lambda^*, \mu^*) = 0$$

2. **Dopuszczalność pierwotna:**
$$g_i(x^*) \leq 0, \quad h_j(x^*) = 0$$

3. **Dopuszczalność dualna:**
$$\lambda_i^* \geq 0$$

4. **Komplementarność:**
$$\lambda_i^* g_i(x^*) = 0 \quad \forall i$$

```
KKT interpretacja geometryczna:

     ∇f(x*)
        ↑
        │     ∇g₁(x*)
        │    ↗
   ─────●─────  (granica ograniczenia)
        x*

W optimum: ∇f = -λ∇g (przeciwne kierunki, λ≥0)
```

---

### 4. Warunki regularności (Constraint Qualification)

Warunki zapewniające, że KKT są konieczne:

| Warunek | Definicja |
|---------|-----------|
| **LICQ** (Linear Independence CQ) | Gradienty aktywnych ograniczeń liniowo niezależne |
| **MFCQ** (Mangasarian-Fromovitz CQ) | Słabsza wersja LICQ |
| **Slater** | Istnieje punkt ściśle wewnątrz (dla wypukłych) |

**LICQ:** $\{\nabla g_i(x^*) : g_i(x^*) = 0\} \cup \{\nabla h_j(x^*)\}$ są liniowo niezależne

---

### 5. Warunki dostateczne II rzędu

Jeśli spełnione KKT i dla hesjanu Lagrangianu:
$$d^T \nabla_{xx}^2 L(x^*, \lambda^*, \mu^*) d > 0$$

dla wszystkich $d \neq 0$ spełniających:
- $\nabla g_i(x^*)^T d = 0$ dla aktywnych $g_i$
- $\nabla h_j(x^*)^T d = 0$ dla wszystkich $h_j$

To $x^*$ jest **ścisłym minimum lokalnym**.

---

### 6. Metody optymalizacji nieliniowej

#### Metody gradientowe (bez ograniczeń)

| Metoda | Kierunek | Zbieżność |
|--------|----------|-----------|
| **Gradient Descent** | $d = -\nabla f$ | Liniowa |
| **Newton** | $d = -H^{-1}\nabla f$ | Kwadratowa |
| **BFGS** | Quasi-Newton | Superlinearna |
| **Conjugate Gradient** | Sprzężone kierunki | Superlinearna |

```
Gradient Descent:
x_{k+1} = x_k - α_k ∇f(x_k)

Newton:
x_{k+1} = x_k - [∇²f(x_k)]^{-1} ∇f(x_k)
```

#### Metody z ograniczeniami

| Metoda | Idea |
|--------|------|
| **Kary zewnętrznej** | $\min f(x) + \rho \sum \max(0, g_i)^2$ |
| **Kary wewnętrznej (Barrier)** | $\min f(x) - \mu \sum \log(-g_i)$ |
| **SQP** (Sequential Quadratic Programming) | Iteracyjne rozwiązywanie QP |
| **Interior Point** | Barrier + Newton |
| **Augmented Lagrangian** | Lagrangian + kara |

#### SQP - Algorytm

```
Repeat:
1. Rozwiąż podproblem QP:
   min  ∇f(x_k)^T d + ½ d^T H_k d
   s.t. g_i(x_k) + ∇g_i(x_k)^T d ≤ 0
        h_j(x_k) + ∇h_j(x_k)^T d = 0

2. x_{k+1} = x_k + α_k d_k

3. Aktualizuj H_k (BFGS)
```

---

### 7. Porównanie metod

| Metoda | Ograniczenia | Złożoność iter. | Zbieżność |
|--------|--------------|-----------------|-----------|
| **Gradient** | Bez | O(n) | Liniowa |
| **Newton** | Bez | O(n³) | Kwadratowa |
| **BFGS** | Bez | O(n²) | Superlinearna |
| **SQP** | Z | O(n³) per QP | Superlinearna |
| **Interior Point** | Z | O(n³) | Polinomialna |

---

## 🧠 Mnemoniki

### "KKT = Keep Killing Troubles":
- **K**ondycja stacjonarności (∇L = 0)
- **K**onieczność dopuszczalności (g ≤ 0, h = 0, λ ≥ 0)
- **T**rick komplementarności (λg = 0)

### "Hesjan dodatni = Minimum":
$H \succ 0$ → punkt jest minimum (jak miska)

### "LICQ = Linear Independence":
Gradienty aktywnych ograniczeń muszą być liniowo niezależne

---

## ❓ Pytania dodatkowe

### Q1: "Co oznacza warunek komplementarności λᵢgᵢ = 0?"
**Odpowiedź:** Albo ograniczenie nieaktywne ($g_i < 0$, wtedy $\lambda_i = 0$), albo aktywne ($g_i = 0$, wtedy $\lambda_i \geq 0$). Mnożnik niezerowy tylko dla "ciasnych" ograniczeń.

### Q2: "Kiedy KKT są warunkami dostatecznymi?"
**Odpowiedź:** Dla problemów wypukłych (f wypukła, g wypukłe, h liniowe). Wtedy każdy punkt KKT jest globalnym minimum.

### Q3: "Jaka jest przewaga BFGS nad Newtonem?"
**Odpowiedź:** BFGS nie wymaga obliczania hesjanu (tylko gradienty), przybliża hesjan iteracyjnie. O(n²) zamiast O(n³) per iteracja. Bardziej odporny na nieścisłości.

---

## 🎯 Kluczowe punkty

1. **Bez ograniczeń:** $\nabla f = 0$ (konieczny), $H \succ 0$ (dostateczny)
2. **Z ograniczeniami:** KKT = stacjonarność + dopuszczalność + komplementarność
3. **Regularność:** LICQ, Slater - warunki na poprawność KKT
4. **Metody:** Gradient, Newton, BFGS (bez), SQP, Interior Point (z)
5. **Wypukłość:** KKT konieczne i dostateczne

---

## 📖 Źródła

1. Boyd, Vandenberghe - "Convex Optimization"
2. Nocedal, Wright - "Numerical Optimization"
3. Bazaraa et al. - "Nonlinear Programming"
