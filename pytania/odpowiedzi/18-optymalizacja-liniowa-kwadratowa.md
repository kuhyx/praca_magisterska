# Pytanie 18: Optymalizacja liniowa i kwadratowa

## Pytanie
**"Omówić metody rozwiązywania zadań liniowych i kwadratowych optymalizacji."**

Przedmiot: AMO (Analiza i Metody Optymalizacji)

---

## 📚 Odpowiedź główna

### 1. Programowanie liniowe (LP)

#### Postać standardowa
$$\min c^T x$$
$$\text{s.t. } Ax = b, \quad x \geq 0$$

#### Metoda Simplex

```
Idea: Przechodzenie po wierzchołkach wielościanu dopuszczalnego

    c^T x = const
        ↘
         ●───────●
        /│      /│
       / │     / │    Wielościan dopuszczalny
      ●──┼────●  │
      │  ●────┼──●
      │ /     │ /
      │/      │/
      ●───────● ← optimum (wierzchołek)
```

**Algorytm:**
1. Znajdź bazowe rozwiązanie dopuszczalne (BFS)
2. Sprawdź optymalność (reduced costs ≥ 0)
3. Wybierz zmienną wchodzącą (pivot column)
4. Wybierz zmienną wychodzącą (ratio test)
5. Wykonaj pivot, powtórz

**Złożoność:** O(2^n) worst-case, ale praktycznie bardzo szybki

#### Metoda punktu wewnętrznego (Interior Point)

```
Start wewnątrz wielościanu, zbieżność do optimum przez wnętrze:

      ●───────────●
     /│          /│
    / │   ●→●→● / │    Ścieżka centralna
   ●──┼───────●  │
   │  ●───────┼──●
   │ /        │ /
   │/         │/
   ●──────────● ← optimum
```

**Algorytm Barrier:**
$$\min c^T x - \mu \sum_{i} \ln(x_i)$$

Zmniejszaj μ → 0, rozwiązuj układy Newtona

**Złożoność:** O(n^3.5 L) - wielomianowa

#### Porównanie LP

| Cecha | Simplex | Interior Point |
|-------|---------|----------------|
| Złożoność teoretyczna | Wykładnicza | Wielomianowa |
| Praktyczna wydajność | Bardzo dobra | Dobra dla dużych |
| Warm start | Tak | Nie |
| Rozwiązanie bazowe | Tak | Nie (wewnętrzne) |

---

### 2. Programowanie kwadratowe (QP)

#### Postać ogólna
$$\min \frac{1}{2} x^T Q x + c^T x$$
$$\text{s.t. } Ax \leq b, \quad Ex = d$$

Gdzie Q jest macierzą symetryczną.

#### Klasyfikacja

| Q | Typ | Rozwiązywalność |
|---|-----|-----------------|
| Q ≻ 0 (dodatnio określona) | Wypukły QP | Globalnie jednoznaczne |
| Q ⪰ 0 (półdodatnia) | Wypukły QP | Może wiele rozwiązań |
| Q nieokreślona | Niewypukły QP | NP-trudny |

---

### 3. Metody rozwiązywania QP

#### Active Set Method

```
Idea: Traktuj aktywne ograniczenia jako równości

1. Zgadnij zbiór aktywnych ograniczeń W
2. Rozwiąż QP z ograniczeniami W jako równości
3. Sprawdź:
   - Czy rozwiązanie dopuszczalne? (jeśli nie: usuń z W)
   - Czy mnożniki ≥ 0? (jeśli nie: dodaj do W)
4. Powtarzaj do zbieżności
```

**Zalety:** Dokładne rozwiązanie, warm start
**Wady:** Liczba iteracji zależy od kombinatoryki

#### Metody punktu wewnętrznego dla QP

```
Barrier problem:
min ½x^TQx + c^Tx - μ Σ ln(s_i)
s.t. Ax + s = b

KKT system → rozwiązuj Newton
Zmniejszaj μ → 0
```

**Złożoność:** O(n^3) per iteracja, O(√n) iteracji

#### Gradient Projection Method

```
Dla QP z prostymi ograniczeniami (x ∈ [l, u]):

1. Kierunek: d = -∇f(x) = -(Qx + c)
2. Krok: x_{k+1} = P[x_k + α_k d_k]

Gdzie P[·] = projekcja na [l, u]
```

---

### 4. Przypadki szczególne

#### Least Squares (najmniejsze kwadraty)
$$\min \|Ax - b\|_2^2 = \min x^T A^T A x - 2b^T A x + b^T b$$

**Rozwiązanie:** $(A^T A)x = A^T b$ (równanie normalne)

#### Support Vector Machine (SVM)
$$\min \frac{1}{2}\|w\|^2$$
$$\text{s.t. } y_i(w^T x_i + b) \geq 1$$

→ QP z dodatnio określoną macierzą

#### Portfolio Optimization (Markowitz)
$$\min \frac{1}{2} x^T \Sigma x \quad \text{(ryzyko)}$$
$$\text{s.t. } \mu^T x \geq r, \quad \sum x_i = 1, \quad x \geq 0$$

---

### 5. Narzędzia

| Narzędzie | Typ | Metody |
|-----------|-----|--------|
| **CPLEX** | Komercyjny | Simplex, Barrier, QP |
| **Gurobi** | Komercyjny | Simplex, Barrier, QP |
| **GLPK** | Open source | Simplex |
| **OSQP** | Open source | ADMM dla QP |
| **CVXPY** | Python | Interfejs do solverów |

---

## 🧠 Mnemoniki

### "Simplex = Surface walking":
Chodzi po wierzchołkach (powierzchni) wielościanu

### "Interior Point = Inside path":
Idzie przez wnętrze do optimum

### "Q dodatnia = QP wypukły = łatwy":
Macierz Q określa trudność problemu

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy Simplex jest lepszy od Interior Point?"
**Odpowiedź:** Małe/średnie problemy, warm start (sekwencja podobnych LP), potrzeba rozwiązania bazowego. Interior Point lepszy dla bardzo dużych, rzadkich problemów.

### Q2: "Co to jest dualność w LP?"
**Odpowiedź:** Każdy LP (primal) ma dual. Silna dualność: opt(primal) = opt(dual). Mnożniki Lagrange'a = zmienne dualne. Complementary slackness: x_i > 0 ⟹ ograniczenie dualne aktywne.

### Q3: "Jak rozwiązać niewypukły QP?"
**Odpowiedź:** NP-trudny, metody: Branch & Bound, SDP relaxation, lokalne metody (wiele startów). Brak gwarancji globalnego optimum w czasie wielomianowym.

---

## 🎯 Kluczowe punkty

1. **LP:** Simplex (wierzchołki), Interior Point (wnętrze)
2. **QP wypukły:** Q ⪰ 0, Active Set lub Interior Point
3. **QP niewypukły:** NP-trudny
4. **Narzędzia:** CPLEX, Gurobi, GLPK, OSQP

---

## 📖 Źródła

1. Nocedal, Wright - "Numerical Optimization"
2. Boyd, Vandenberghe - "Convex Optimization"
3. Bertsimas, Tsitsiklis - "Introduction to Linear Optimization"
