# Pytanie 42: Dominacja stochastyczna

## Pytanie
**"Scharakteryzować relacje dominacji stochastycznej pierwszego i drugiego rzędu. Jak mogą być użyte w modelach wyboru w warunkach ryzyka?"**

Przedmiot: WDWR (Wspomaganie Decyzji w Warunkach Ryzyka)

---

## 📚 Odpowiedź główna

### 1. Idea dominacji stochastycznej

```
┌─────────────────────────────────────────────────────────────────┐
│ DOMINACJA STOCHASTYCZNA (Stochastic Dominance)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Cel: Porównać rozkłady prawdopodobieństwa (loterie)           │
│      BEZ znajomości dokładnej funkcji użyteczności            │
│                                                                 │
│ Pytanie: "Czy loteria A jest lepsza od loterii B              │
│           dla KAŻDEGO racjonalnego decydenta?"                 │
│                                                                 │
│ Jeśli A dominuje B → KAŻDY wybierze A (niezależnie od U)      │
│                                                                 │
│ Hierarchia:                                                     │
│   FSD (First-order) ⊂ SSD (Second-order) ⊂ TSD (Third-order)  │
│                                                                 │
│   FSD implikuje SSD, ale nie odwrotnie                        │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Dominacja stochastyczna pierwszego rzędu (FSD)

#### Definicja

$$A \succeq_{FSD} B \Leftrightarrow F_A(x) \leq F_B(x) \quad \forall x$$

gdzie $F(x) = P(X \leq x)$ to dystrybuanta (CDF)

```
┌─────────────────────────────────────────────────────────────────┐
│ FSD: "A dominuje B jeśli F_A jest zawsze poniżej F_B"          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  F(x)                                                           │
│    ↑                                                            │
│  1 │                    ╭───── F_B                              │
│    │                 ╭──╯                                       │
│    │              ╭──╯                                          │
│    │           ╭──╯                                             │
│    │        ╭──╯        ╭───── F_A                              │
│    │     ╭──╯        ╭──╯                                       │
│    │  ╭──╯        ╭──╯                                          │
│    │──╯        ╭──╯                                             │
│  0 └──────────────────────────────────────────────→ x          │
│                                                                 │
│    F_A(x) ≤ F_B(x) dla każdego x → A dominuje B (FSD)         │
│                                                                 │
│    Interpretacja: A ma zawsze większe prawdopodobieństwo       │
│                   przekroczenia dowolnego progu x              │
└─────────────────────────────────────────────────────────────────┘
```

#### Charakterystyka FSD

| Aspekt | Opis |
|--------|------|
| **Warunek na U** | U'(x) ≥ 0 (monotoniczność, "więcej = lepiej") |
| **Klasa decydentów** | WSZYSCY racjonalni (nienasyceni) |
| **Siła** | Najsilniejsza dominacja |
| **Częstość** | Rzadko występuje w praktyce |

#### Równoważna definicja

$$E[U(A)] \geq E[U(B)] \quad \forall U: U' \geq 0$$

---

### 3. Dominacja stochastyczna drugiego rzędu (SSD)

#### Definicja

$$A \succeq_{SSD} B \Leftrightarrow \int_{-\infty}^{x} F_A(t) dt \leq \int_{-\infty}^{x} F_B(t) dt \quad \forall x$$

```
┌─────────────────────────────────────────────────────────────────┐
│ SSD: "Skumulowane pole pod F_A ≤ pole pod F_B"                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  F(x)                     ∫F(t)dt                              │
│    ↑                         ↑                                  │
│    │    ╭── F_B              │         ╭── ∫F_B               │
│    │  ╭─╯                    │       ╭─╯                       │
│    │ ╱   ╭── F_A             │     ╭─╯                         │
│    │╱  ╭─╯                   │   ╭─╯   ╭── ∫F_A               │
│    ┼──────────→ x            │ ╭─╯   ╭─╯                       │
│                              │─╯───╭─╯                         │
│    Krzywe mogą              └───────────────→ x               │
│    się przecinać!           Skumulowane nie!                   │
│                                                                 │
│ SSD dopuszcza przecięcia CDF, ale całki muszą zachować relację│
└─────────────────────────────────────────────────────────────────┘
```

#### Charakterystyka SSD

| Aspekt | Opis |
|--------|------|
| **Warunek na U** | U' ≥ 0 i U'' ≤ 0 (monotoniczne + wklęsłe) |
| **Klasa decydentów** | Risk-averse (awersja do ryzyka) |
| **Siła** | Słabsza niż FSD |
| **Częstość** | Częstsza niż FSD |

#### Równoważna definicja

$$E[U(A)] \geq E[U(B)] \quad \forall U: U' \geq 0, U'' \leq 0$$

---

### 4. Porównanie FSD i SSD

```
┌─────────────────────────────────────────────────────────────────┐
│                    FSD vs SSD                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Przykład 1: FSD                                                │
│   A: 50% szans na 100, 50% na 200                              │
│   B: 50% szans na 50, 50% na 150                               │
│   A dominuje B (FSD) - zawsze lepsze wyniki                    │
│                                                                 │
│ Przykład 2: SSD (ale nie FSD)                                  │
│   A: 100 na pewno                                               │
│   B: 50% szans na 50, 50% na 150                               │
│   E[A] = 100 = E[B], ale A ma mniejszą wariancję              │
│   A dominuje B (SSD) dla risk-averse                           │
│   NIE dominuje (FSD) - B może dać 150 > 100                    │
│                                                                 │
│ Przykład 3: Mean-Preserving Spread (MPS)                       │
│   B = A + ε, gdzie E[ε|A] = 0 (noise)                         │
│   A dominuje B (SSD) - ta sama średnia, większy rozrzut B     │
└─────────────────────────────────────────────────────────────────┘
```

| Cecha | FSD | SSD |
|-------|-----|-----|
| **Warunek** | F_A(x) ≤ F_B(x) ∀x | ∫F_A ≤ ∫F_B ∀x |
| **Na U** | U' ≥ 0 | U' ≥ 0, U'' ≤ 0 |
| **Decydenci** | Wszyscy racjonalni | Risk-averse |
| **Implikacja** | FSD ⟹ SSD | SSD ⇏ FSD |
| **Praktyka** | Rzadka | Częstsza |

---

### 5. Zastosowanie w modelach wyboru

#### Portfolio Selection

```
┌─────────────────────────────────────────────────────────────────┐
│ WYBÓR PORTFELA                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Problem: Wybór między portfelami P₁, P₂, ..., Pₙ               │
│                                                                 │
│ Krok 1: Sprawdź FSD                                            │
│   Jeśli Pᵢ FSD Pⱼ → wyeliminuj Pⱼ                             │
│   (żaden racjonalny inwestor nie wybierze Pⱼ)                  │
│                                                                 │
│ Krok 2: Sprawdź SSD (dla risk-averse)                          │
│   Jeśli Pᵢ SSD Pⱼ → wyeliminuj Pⱼ dla risk-averse            │
│                                                                 │
│ Krok 3: Dla pozostałych - potrzebna specyfikacja U             │
│                                                                 │
│ Efektywny zbiór SD = portfele niezdominowane                   │
└─────────────────────────────────────────────────────────────────┘
```

#### Ocena inwestycji

```
Inwestycja A: Zwrot ~ N(10%, 15%)
Inwestycja B: Zwrot ~ N(8%, 20%)

Test SSD:
• E[A] = 10% > E[B] = 8%  ✓
• σ[A] = 15% < σ[B] = 20%  ✓

Dla rozkładów normalnych z E[A] > E[B] i σ[A] < σ[B]:
  A dominuje B (SSD)

Wniosek: Każdy risk-averse inwestor wybierze A
```

#### Ubezpieczenia

```
Bez ubezpieczenia: Loteria L z ryzykiem straty
Z ubezpieczeniem: CE (pewna strata = składka)

Jeśli składka = "fair" (E[składka] = E[straty]):
  Ubezpieczenie SSD dominuje brak ubezpieczenia
  dla każdego risk-averse decydenta

Uzasadnienie zakupu ubezpieczenia bez znajomości U!
```

---

### 6. Testowanie dominacji

```
┌─────────────────────────────────────────────────────────────────┐
│ ALGORYTM SPRAWDZANIA SD                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Dane: Dwa rozkłady empiryczne (próbki x₁,...,xₙ i y₁,...,yₘ)  │
│                                                                 │
│ FSD Test:                                                       │
│ 1. Oblicz empiryczne CDF: F̂_X(t), F̂_Y(t)                      │
│ 2. Sprawdź czy F̂_X(t) ≤ F̂_Y(t) dla wszystkich t              │
│                                                                 │
│ SSD Test:                                                       │
│ 1. Oblicz ∫F̂_X(t)dt i ∫F̂_Y(t)dt                              │
│ 2. Sprawdź czy pierwsza ≤ druga dla wszystkich punktów        │
│                                                                 │
│ Testy statystyczne:                                             │
│ • Kolmogorov-Smirnov (FSD)                                     │
│ • Barrett-Donald test                                           │
│ • Linton-Maasoumi-Whang test                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7. Ograniczenia

| Ograniczenie | Opis |
|--------------|------|
| **Częściowe uporządkowanie** | Nie wszystkie pary porównywalne |
| **Konserwatywność** | Wiele par bez dominacji |
| **Wymóg pełnego rozkładu** | Potrzebna cała dystrybuanta |
| **Brak dominacji ≠ obojętność** | Brak dominacji nie znaczy równoważność |

---

## 🧠 Mnemoniki

### "FSD = F always ≤":
First-order: dystrybuanta A zawsze ≤ B

### "SSD = Second = Sum (integral)":
Second-order: całka z F_A ≤ całka z F_B

### "FSD = wszyscy, SSD = risk-averse":
FSD: U' ≥ 0, SSD: U' ≥ 0, U'' ≤ 0

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy FSD a kiedy SSD?"
**Odpowiedź:** FSD: gdy jeden rozkład jest jednoznacznie lepszy (przesunięty w prawo). SSD: gdy różnica w ryzyku (rozproszeniu) kompensuje różnicę w średniej dla risk-averse.

### Q2: "Co jeśli ani FSD ani SSD?"
**Odpowiedź:** Rozkłady są nieporównywalne w sensie SD. Potrzebna dokładniejsza specyfikacja preferencji (konkretna funkcja użyteczności) lub TSD (trzeci rząd).

### Q3: "Związek SD z mean-variance?"
**Odpowiedź:** Mean-variance (Markowitz) to przybliżenie. SSD jest bardziej ogólne - nie wymaga założenia normalności rozkładu. Dla rozkładów normalnych: SSD ≈ dominacja mean-variance.

---

## 🎯 Kluczowe punkty

1. **FSD:** F_A(x) ≤ F_B(x) ∀x, dla U' ≥ 0
2. **SSD:** ∫F_A ≤ ∫F_B, dla U' ≥ 0, U'' ≤ 0
3. **FSD ⟹ SSD** (ale nie odwrotnie)
4. **Zastosowanie:** Eliminacja zdominowanych opcji
5. **Bez znajomości U:** Decyzja dla klasy decydentów

---

## 📖 Źródła

1. Hadar, Russell - "Rules for Ordering Uncertain Prospects"
2. Levy - "Stochastic Dominance"
3. Rothschild, Stiglitz - "Increasing Risk"
