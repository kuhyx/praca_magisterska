# Pytanie 41: Interaktywne wspomaganie decyzji w warunkach ryzyka

## Pytanie
**"Przedstawić metody interaktywne wspomagania decyzji w warunkach ryzyka."**

Przedmiot: WDWR (Wspomaganie Decyzji w Warunkach Ryzyka)

---

## 📚 Odpowiedź główna

### 1. Decyzje w warunkach ryzyka

```
┌─────────────────────────────────────────────────────────────────┐
│           WARUNKI PODEJMOWANIA DECYZJI                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ PEWNOŚĆ:      Znamy dokładnie wyniki każdej decyzji            │
│               (deterministyczne)                                │
│                                                                 │
│ RYZYKO:       Znamy możliwe wyniki i ich prawdopodobieństwa    │
│               (stochastyczne, rozkłady znane)                  │
│                                                                 │
│ NIEPEWNOŚĆ:   Możliwe wyniki znane, prawdopodobieństwa nie     │
│               (scenariusze bez prawdopodobieństw)              │
│                                                                 │
│ Decyzja w warunkach ryzyka:                                     │
│ • Wybór między loteriami (gambles)                             │
│ • Każda loteria: zbiór wyników z prawdopodobieństwami          │
│ • Decydent ma preferencje dotyczące ryzyka                     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Metody interaktywne - przegląd

```
┌─────────────────────────────────────────────────────────────────┐
│ INTERAKTYWNE = Dialog z decydentem                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐         ┌──────────────┐                    │
│   │   DECYDENT   │ ←─────→ │   SYSTEM     │                    │
│   │ (preferencje)│         │  (analiza)   │                    │
│   └──────────────┘         └──────────────┘                    │
│         │                        │                              │
│         ↓                        ↓                              │
│   Odpowiedzi na           Generowanie pytań,                   │
│   pytania, wybory         eliminacja opcji,                    │
│   porównawcze             rekomendacje                         │
│                                                                 │
│ Cel: Odkryć preferencje decydenta (funkcję użyteczności)       │
│      bez wymagania pełnej specyfikacji z góry                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3. Metoda loterii (Lottery Method)

```
┌─────────────────────────────────────────────────────────────────┐
│ ELICYTACJA FUNKCJI UŻYTECZNOŚCI                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Cel: Wyznaczyć U(x) dla różnych wartości x                     │
│                                                                 │
│ Procedura:                                                      │
│ 1. Ustal U(x_worst) = 0, U(x_best) = 1                         │
│                                                                 │
│ 2. Dla wartości pośredniej x_mid, pytaj:                       │
│    "Wolisz x_mid na pewno, czy loterię                         │
│     (p: x_best, 1-p: x_worst)?"                                │
│                                                                 │
│ 3. Znajdź p* gdzie decydent jest obojętny:                     │
│    U(x_mid) = p* × U(x_best) + (1-p*) × U(x_worst)            │
│    U(x_mid) = p* × 1 + (1-p*) × 0 = p*                        │
│                                                                 │
│ 4. Powtórz dla kolejnych punktów                               │
│                                                                 │
│ Przykład:                                                       │
│ x_worst = 0 PLN, x_best = 1000 PLN, x_mid = 500 PLN           │
│ Pytanie: "500 PLN na pewno czy loteria (p: 1000, 1-p: 0)?"    │
│ Jeśli obojętny przy p* = 0.6 → U(500) = 0.6                   │
│ (risk averse: 0.6 < 0.5 liniowego)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. Metoda pewnego ekwiwalentu (Certainty Equivalent)

```
CE (Certainty Equivalent) = pewna kwota równoważna loterii

Dla loterii L = (p₁: x₁, p₂: x₂, ...):
  CE(L) taki że U(CE) = E[U(L)] = Σ pᵢ U(xᵢ)

Pytanie interaktywne:
"Ile PLN na pewno jest dla Ciebie równoważne loterii
 (50%: 1000 PLN, 50%: 0 PLN)?"

Odpowiedź CE = 400 PLN oznacza:
  U(400) = 0.5 × U(1000) + 0.5 × U(0) = 0.5

Risk Premium = E[X] - CE = 500 - 400 = 100 PLN
  (ile decydent "płaci" za uniknięcie ryzyka)

┌─────────────────────────────────────────────────────────────────┐
│ U(x)                                                            │
│  ↑     Risk Averse        Risk Neutral       Risk Seeking      │
│  │        ╭───             /                      ───╮         │
│  │      ╭─╯               /                         ╰─╮        │
│  │    ╭─╯                /                             ╰─╮     │
│  │  ╭─╯                 /                                 ╰─╮  │
│  │╭─╯                  /                                     ╰╮│
│  └──────────────────────────────────────────────────────────→ x│
│    CE < E[X]          CE = E[X]              CE > E[X]         │
└─────────────────────────────────────────────────────────────────┘
```

---

### 5. Metoda AHP (Analytic Hierarchy Process)

```
┌─────────────────────────────────────────────────────────────────┐
│ AHP - Hierarchiczna struktura problemu (Saaty)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌─────────────┐                             │
│                    │    CEL      │                             │
│                    └──────┬──────┘                             │
│           ┌───────────────┼───────────────┐                    │
│           ↓               ↓               ↓                    │
│     ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│     │Kryterium1│   │Kryterium2│   │Kryterium3│               │
│     └────┬─────┘   └────┬─────┘   └────┬─────┘               │
│          └──────────────┼──────────────┘                       │
│                         ↓                                       │
│            ┌─────┬─────┬─────┐                                 │
│            │Alt A│Alt B│Alt C│                                 │
│            └─────┴─────┴─────┘                                 │
│                                                                 │
│ Porównania parami (skala 1-9):                                 │
│ "Ile razy kryterium K1 jest ważniejsze od K2?"                 │
│                                                                 │
│ Macierz porównań → eigenvalue → wagi                          │
│ Consistency Ratio CR < 0.1 (sprawdzenie spójności)            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6. Metoda PROMETHEE

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMETHEE - Preference Ranking Organization Method             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. Dla każdego kryterium j, definiuj funkcję preferencji Pⱼ   │
│    Pⱼ(a,b) = P(dⱼ) gdzie dⱼ = fⱼ(a) - fⱼ(b)                  │
│                                                                 │
│ Typy funkcji preferencji:                                      │
│    │                  │      ____                              │
│    │     ____         │     /                                  │
│    │    /             │    /                                   │
│    │___/              │___/                                    │
│    Próg (threshold)    Liniowa (V-shape)                       │
│                                                                 │
│ 2. Agregacja:                                                   │
│    π(a,b) = Σⱼ wⱼ Pⱼ(a,b)  (indeks preferencji)              │
│                                                                 │
│ 3. Przepływy:                                                   │
│    Φ⁺(a) = Σᵦ π(a,b)  (outranking flow)                       │
│    Φ⁻(a) = Σᵦ π(b,a)  (outranked flow)                        │
│    Φ(a) = Φ⁺(a) - Φ⁻(a)  (net flow)                           │
│                                                                 │
│ 4. Ranking wg Φ(a)                                             │
│                                                                 │
│ Interaktywność: wybór funkcji preferencji, progów, wag        │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7. Metoda ELECTRE

```
┌─────────────────────────────────────────────────────────────────┐
│ ELECTRE - ELimination Et Choix Traduisant la REalité          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Outranking: "a jest co najmniej tak dobra jak b" (aSb)        │
│                                                                 │
│ Concordance Index C(a,b):                                      │
│   C(a,b) = Σ{wⱼ : fⱼ(a) ≥ fⱼ(b)} / Σwⱼ                       │
│   (suma wag kryteriów gdzie a ≥ b)                            │
│                                                                 │
│ Discordance Index D(a,b):                                      │
│   D(a,b) = max{(fⱼ(b) - fⱼ(a)) / Δⱼ}                          │
│   (największa przewaga b nad a, znormalizowana)               │
│                                                                 │
│ Outranking:                                                     │
│   aSb ⟺ C(a,b) ≥ c* AND D(a,b) ≤ d*                          │
│   (wystarczająca zgodność, brak silnego sprzeciwu)            │
│                                                                 │
│ Interaktywność: progi c*, d*, wagi wⱼ                          │
└─────────────────────────────────────────────────────────────────┘
```

---

### 8. Porównanie metod

| Metoda | Typ | Interakcja | Zastosowanie |
|--------|-----|------------|--------------|
| **Lottery** | Utility | Porównania z loteriami | Elicytacja U(x) |
| **CE** | Utility | Pewne ekwiwalenty | Pomiar ryzyka |
| **AHP** | MCDM | Porównania parami | Hierarchie, wagi |
| **PROMETHEE** | Outranking | Funkcje preferencji | Ranking |
| **ELECTRE** | Outranking | Progi zgodności | Eliminacja |

---

## 🧠 Mnemoniki

### "CE = Certain Equivalent":
Pewna kwota równoważna loterii

### "AHP = Ask, Hierarchize, Prioritize":
Pytaj, buduj hierarchię, ustal priorytety

### "PROMETHEE = Przepływy":
Φ⁺ (outgoing), Φ⁻ (incoming), Φ (net)

---

## ❓ Pytania dodatkowe

### Q1: "Jak wykryć niespójność odpowiedzi decydenta?"
**Odpowiedź:** AHP: Consistency Ratio (CR < 0.1). Utility: sprawdzenie monotoniczności, przechodniości preferencji. Cross-validation różnymi metodami elicytacji.

### Q2: "Co to jest awersja do ryzyka?"
**Odpowiedź:** Risk averse: U''(x) < 0 (funkcja wklęsła), CE < E[X], preferuje pewność nad loterię o tej samej wartości oczekiwanej. Miernik: Arrow-Pratt coefficient r(x) = -U''(x)/U'(x).

### Q3: "AHP vs PROMETHEE?"
**Odpowiedź:** AHP: hierarchiczna dekompozycja, porównania parami, pełna kompensacja. PROMETHEE: outranking, progi preferencji, częściowa kompensacja, lepsze dla nieporównywalnych kryteriów.

---

## 🎯 Kluczowe punkty

1. **Ryzyko:** Znane prawdopodobieństwa wyników
2. **Interaktywność:** Dialog z decydentem
3. **Loterie:** Elicytacja U(x) przez porównania
4. **CE:** Certainty Equivalent, miara awersji do ryzyka
5. **AHP/PROMETHEE/ELECTRE:** Metody wielokryterialne

---

## 📖 Źródła

1. von Neumann, Morgenstern - "Theory of Games and Economic Behavior"
2. Saaty - "The Analytic Hierarchy Process"
3. Brans, Vincke - "PROMETHEE Method"
4. Roy - "ELECTRE Methods"
