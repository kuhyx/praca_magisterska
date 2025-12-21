# Pytanie 37: Modele sieci złożonych

## Pytanie
**"Porównać podstawowe modele sieci złożonych. Jak odpowiadają one własnościom rzeczywistych sieci?"**

Przedmiot: TASS (Technologie i Algorytmy dla Sieci Społecznościowych)

---

## 📚 Odpowiedź główna

### 1. Właściwości rzeczywistych sieci

```
┌─────────────────────────────────────────────────────────────────┐
│         TYPOWE CECHY SIECI RZECZYWISTYCH                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. SMALL-WORLD EFFECT:                                         │
│    "Six degrees of separation"                                  │
│    Średnia ścieżka ~ log(N)                                    │
│                                                                 │
│ 2. HIGH CLUSTERING:                                             │
│    "Znajomi moich znajomych są znajomymi"                      │
│    Współczynnik grupowania C >> C_random                       │
│                                                                 │
│ 3. SCALE-FREE (Power-law degree distribution):                 │
│    P(k) ~ k^(-γ), gdzie γ ∈ [2, 3]                             │
│    Kilka hubów, wiele węzłów o małym stopniu                   │
│                                                                 │
│ 4. COMMUNITY STRUCTURE:                                         │
│    Gęste grupy połączone rzadkimi mostami                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Model Erdős-Rényi (Random Graph)

```
┌─────────────────────────────────────────────────────────────────┐
│ G(n, p) - Graf losowy                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Konstrukcja:                                                    │
│ - n węzłów                                                      │
│ - Każda krawędź z prawdopodobieństwem p                        │
│                                                                 │
│ Właściwości:                                                    │
│ ┌─────────────────────────────────────────┐                    │
│ │ Średni stopień:     <k> = p(n-1)        │                    │
│ │ Rozkład stopni:     Poisson (dla dużych n)│                  │
│ │ Clustering:         C = p (niski!)       │                    │
│ │ Średnia ścieżka:    L ~ log(n)/log(<k>) │                    │
│ │ Giant component:    istnieje gdy <k> > 1 │                    │
│ └─────────────────────────────────────────┘                    │
│                                                                 │
│ Rozkład stopni P(k):                                           │
│                                                                 │
│ P(k)                                                            │
│   ↑     ●                                                       │
│   │    ●●●                                                      │
│   │   ●●●●●●       Rozkład Poissona                            │
│   │  ●●●●●●●●      (symetryczny, wąski)                        │
│   │ ●●●●●●●●●●                                                  │
│   └────────────────→ k                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Porównanie z rzeczywistością

| Cecha | ER Model | Rzeczywiste sieci |
|-------|----------|-------------------|
| **Clustering** | C = p (niski) | C >> p (wysoki) ❌ |
| **Średnia ścieżka** | L ~ log(n) ✓ | L ~ log(n) ✓ |
| **Rozkład stopni** | Poisson | Power-law ❌ |
| **Huby** | Brak | Istnieją ❌ |

---

### 3. Model Watts-Strogatz (Small-World)

```
┌─────────────────────────────────────────────────────────────────┐
│ SMALL-WORLD MODEL                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Konstrukcja:                                                    │
│ 1. Zacznij od regularnej kratki (ring lattice)                 │
│ 2. Każda krawędź przepinana z prawdop. p                       │
│                                                                 │
│  p=0 (regular)        p~0.01           p=1 (random)            │
│                                                                 │
│    ●───●───●          ●───●───●          ●   ●   ●             │
│   /│   │   │\        /│ \ │   │\        /│\ /│\ /│\            │
│  ● │   │   │ ●      ● │   │   │ ●      ● │ X │ X │ ●           │
│   \│   │   │/        \│   │ / │/        \│/ \│/ \│/            │
│    ●───●───●          ●───●───●          ●   ●   ●             │
│                                                                 │
│  C: high              C: high            C: low                 │
│  L: high              L: low             L: low                 │
│                       ↑                                         │
│                  SMALL-WORLD                                    │
│                  (best of both!)                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Właściwości

```
Dla małych p (np. p = 0.01):

L(p)     C(p)
  ↑        ↑
  │●       │●●●●●●●●●●●●●●●●●
  │ ●      │              ●
  │  ●●    │               ●●
  │    ●●●●│                 ●●●●●
  └────────→ p    └────────────────→ p
  
L spada szybko przy małych p (shortcuts)
C pozostaje wysoki do większych p
```

### Porównanie z rzeczywistością

| Cecha | WS Model | Rzeczywiste sieci |
|-------|----------|-------------------|
| **Clustering** | Wysoki ✓ | Wysoki ✓ |
| **Średnia ścieżka** | L ~ log(n) ✓ | L ~ log(n) ✓ |
| **Rozkład stopni** | Wąski (quasi-regular) | Power-law ❌ |
| **Huby** | Brak | Istnieją ❌ |

---

### 4. Model Barabási-Albert (Scale-Free)

```
┌─────────────────────────────────────────────────────────────────┐
│ PREFERENTIAL ATTACHMENT MODEL                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Konstrukcja:                                                    │
│ 1. Zacznij od małego grafu (m₀ węzłów)                         │
│ 2. Dodawaj węzły jeden po drugim                               │
│ 3. Nowy węzeł łączy się z m istniejącymi                       │
│ 4. Prawdopodobieństwo połączenia z węzłem i:                   │
│                                                                 │
│              kᵢ                                                 │
│    Π(i) = ─────────     "Rich get richer"                      │
│            Σⱼ kⱼ                                                │
│                                                                 │
│ Rozkład stopni P(k):                                           │
│                                                                 │
│ log P(k)                                                        │
│   ↑  ●                                                          │
│   │   ●                                                         │
│   │    ●                Power-law:                              │
│   │     ●               P(k) ~ k^(-3)                          │
│   │      ●●                                                     │
│   │        ●●●                                                  │
│   │           ●●●●●●●●                                          │
│   └───────────────────→ log k                                   │
│                                                                 │
│ Huby (węzły o wysokim stopniu) pojawiają się naturalnie!       │
└─────────────────────────────────────────────────────────────────┘
```

### Właściwości

| Właściwość | Wartość |
|------------|---------|
| **Rozkład stopni** | P(k) ~ k^(-γ), γ = 3 |
| **Średnia ścieżka** | L ~ log(n)/log(log(n)) (ultra-small) |
| **Clustering** | C ~ (log n)² / n (niski!) |
| **Odporność** | Odporna na losowe awarie, wrażliwa na celowe ataki |

### Porównanie z rzeczywistością

| Cecha | BA Model | Rzeczywiste sieci |
|-------|----------|-------------------|
| **Clustering** | Niski ❌ | Wysoki |
| **Średnia ścieżka** | Ultra-short ✓ | Short ✓ |
| **Rozkład stopni** | Power-law ✓ | Power-law ✓ |
| **Huby** | Tak ✓ | Tak ✓ |

---

### 5. Porównanie zbiorcze

```
┌──────────────┬───────────────┬───────────────┬───────────────┐
│ Właściwość   │ Erdős-Rényi   │ Watts-Strogatz│ Barabási-Albert│
├──────────────┼───────────────┼───────────────┼───────────────┤
│ Clustering   │ Niski (C=p)   │ Wysoki        │ Niski         │
│ Śr. ścieżka  │ log(n)        │ log(n)        │ log(n)/loglog │
│ Rozkład      │ Poisson       │ Quasi-regular │ Power-law     │
│ Huby         │ Nie           │ Nie           │ Tak           │
│ Small-world  │ Tak           │ Tak           │ Ultra-small   │
│ Mechanizm    │ Losowość      │ Rewiring      │ Pref. attach. │
└──────────────┴───────────────┴───────────────┴───────────────┘

Rzeczywiste sieci (WWW, social, biological):
• Wysoki clustering     → WS lepszy
• Power-law            → BA lepszy
• Short paths          → wszystkie OK

Żaden pojedynczy model nie oddaje wszystkich cech!
```

---

### 6. Modele rozszerzone

```
┌─────────────────────────────────────────────────────────────────┐
│ HOLME-KIM MODEL (BA + clustering):                             │
│   Po preferential attachment → dodaj trójkąt z prawdop. p      │
│   Łączy power-law z wysokim clustering                         │
├─────────────────────────────────────────────────────────────────┤
│ HIERARCHICAL MODELS:                                            │
│   Rekurencyjna struktura (fraktalna)                           │
│   Modeluje hierarchie w organizacjach                          │
├─────────────────────────────────────────────────────────────────┤
│ STOCHASTIC BLOCK MODEL:                                        │
│   Podział na grupy z różnymi p wewnątrz/między                 │
│   Modeluje community structure                                  │
├─────────────────────────────────────────────────────────────────┤
│ CONFIGURATION MODEL:                                            │
│   Generuj graf z zadanym rozkładem stopni                      │
│   Elastyczny, ale brak mechanizmu wzrostu                      │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7. Przykłady rzeczywistych sieci

| Sieć | N | <k> | C | L | γ |
|------|---|-----|---|---|---|
| **WWW** | 10⁹ | ~7 | 0.11 | 11.2 | 2.1 |
| **Facebook** | 10⁹ | ~200 | 0.16 | 4.7 | ~3 |
| **Internet (AS)** | 10⁴ | ~6 | 0.24 | 3.7 | 2.2 |
| **C. elegans** | 282 | 14 | 0.28 | 2.7 | - |
| **Power grid** | 4941 | 2.7 | 0.08 | 18.7 | exp |

---

## 🧠 Mnemoniki

### "ER = Equal Random":
Erdős-Rényi - równe prawdopodobieństwo krawędzi

### "WS = Wires Switched":
Watts-Strogatz - przepinanie krawędzi

### "BA = Big Attract":
Barabási-Albert - duże węzły przyciągają więcej

### "Scale-free = -3 power":
P(k) ~ k^(-3) dla BA modelu

---

## ❓ Pytania dodatkowe

### Q1: "Dlaczego BA ma niski clustering?"
**Odpowiedź:** Preferential attachment łączy nowe węzły głównie z hubami, nie tworząc trójkątów między sąsiadami. Rozwiązanie: Holme-Kim model dodaje krok "triad formation".

### Q2: "Co to jest robustness vs vulnerability?"
**Odpowiedź:** Scale-free sieci są odporne na losowe awarie (większość węzłów ma mały stopień), ale wrażliwe na celowane ataki na huby. ER sieci są bardziej jednolite w obu przypadkach.

### Q3: "Jak mierzyć small-world property?"
**Odpowiedź:** Współczynnik σ = (C/C_random) / (L/L_random). Jeśli σ >> 1 → small-world. C wysoki jak w kratce, L niski jak w random graph.

---

## 🎯 Kluczowe punkty

1. **ER:** Random, Poisson degree, low clustering
2. **WS:** Rewiring, high clustering + short paths
3. **BA:** Preferential attachment, power-law, huby
4. **Real networks:** Power-law + high clustering + short paths
5. **Żaden model nie jest kompletny** - łączone modele

---

## 📖 Źródła

1. Barabási - "Network Science" (networkscience.com)
2. Newman - "Networks: An Introduction"
3. Watts, Strogatz - "Collective dynamics of small-world networks" (1998)
4. Barabási, Albert - "Emergence of Scaling in Random Networks" (1999)
