# Pytanie 29: Prawo Amdahla - przyśpieszenie programów równoległych

## Pytanie
**"Oszacować ilościowo przyśpieszenie wykonania programu sekwencyjnego z fragmentami równoległymi na maszynie wielordzeniowej. Co osłabia to ograniczenie?"**

Przedmiot: PORR (Programowanie Równoległe i Rozproszone)

---

## 📚 Odpowiedź główna

### 1. Prawo Amdahla

#### Formuła

$$S(n) = \frac{1}{(1-p) + \frac{p}{n}}$$

Gdzie:
- $S(n)$ = przyśpieszenie (speedup)
- $p$ = część programu, która może być zrównoleglona (0 ≤ p ≤ 1)
- $n$ = liczba procesorów/rdzeni
- $(1-p)$ = część sekwencyjna

#### Interpretacja graficzna

```
Czas wykonania:

Sekwencyjny (1 procesor):
├────────────────────────────────────────────────────────────────┤
│      Sekwencyjna (1-p)     │        Równoległa (p)            │
│          20%               │              80%                  │
├────────────────────────────┴────────────────────────────────────┤
                        T₁ = 100%

Równoległy (4 procesory):
├────────────────────────────┬────────────────────┤
│      Sekwencyjna (1-p)     │   Równoległa (p/n) │
│          20%               │     80%/4 = 20%    │
├────────────────────────────┴────────────────────┤
                        T₄ = 40%

Speedup = T₁/T₄ = 100/40 = 2.5x
```

#### Przykłady liczbowe

| p (równoległa) | n=2 | n=4 | n=8 | n=∞ |
|----------------|-----|-----|-----|-----|
| 50% | 1.33 | 1.60 | 1.78 | 2.00 |
| 75% | 1.60 | 2.29 | 3.20 | 4.00 |
| 90% | 1.82 | 3.08 | 4.71 | 10.00 |
| 95% | 1.90 | 3.48 | 5.93 | 20.00 |
| 99% | 1.98 | 3.88 | 7.48 | 100.00 |

#### Maksymalne przyśpieszenie (n → ∞)

$$S_{max} = \lim_{n \to \infty} S(n) = \frac{1}{1-p}$$

```
Dla p = 90% (10% sekwencyjnej):
S_max = 1/0.1 = 10x

Nawet z nieskończoną liczbą procesorów,
10% kodu sekwencyjnego limituje speedup do 10x!
```

---

### 2. Wizualizacja ograniczenia

```
Speedup
   ↑
20 ┤                                    ........... p=99%
   │                              ......
   │                        ......
15 ┤                   .....
   │              .....
   │          ....                       ______ p=95%
10 ┤      ....                     _____/
   │   ...                   _____/
   │  ..              ______/              _____ p=90%
 5 ┤ .          _____/               _____/
   │.     _____/               _____/
   │ ____/               _____/              ____ p=75%
 2 ┼/           ________/_______________/____
 1 ┼────────────────────────────────────────────→ Procesory (n)
   1    4    8    16   32   64   128  256
```

**Obserwacja:** Krzywe szybko się spłaszczają - dodawanie procesorów daje coraz mniejszy zysk.

---

### 3. Co osłabia ograniczenie Amdahla?

#### 3.1 Prawo Gustafsona-Barsisa (Scaled Speedup)

```
Amdahl: Stały problem, więcej procesorów
Gustafson: Większy problem, stały czas

S_scaled(n) = n - (1-p)(n-1) = 1 - p + p·n

Dla p = 90%, n = 100:
S_scaled = 1 - 0.9 + 0.9·100 = 90.1x (vs Amdahl: ~10x)

Zastosowanie: Symulacje, rendering, ML training
- Większy dataset
- Więcej iteracji
- Wyższa rozdzielczość
```

#### 3.2 Techniki zmniejszania części sekwencyjnej

| Technika | Opis |
|----------|------|
| **Algorytmy równoległe** | Zamiana algorytmu sekwencyjnego na równoległy |
| **Lock-free structures** | Unikanie synchronizacji blokującej |
| **Pipelining** | Nakładanie faz obliczeń |
| **Speculative execution** | Równoległe wykonanie alternatyw |
| **Data parallelism** | Podział danych zamiast zadań |

#### 3.3 Ukrywanie latencji

```
Sekwencyjne I/O:
CPU: ────compute────│wait│────compute────│wait│────
                    ↑ I/O               ↑ I/O

Overlapping (prefetching, async I/O):
CPU: ────compute────────compute────────compute────
I/O:     └──fetch──┘   └──fetch──┘   └──fetch──┘

Efektywnie zmniejsza (1-p)!
```

---

### 4. Czynniki zmniejszające rzeczywiste przyśpieszenie

```
S_real < S_Amdahl ze względu na:

┌─────────────────────────────────────────────────────────────────┐
│ 1. OVERHEAD SYNCHRONIZACJI                                      │
│    - Mutex, semaphore contention                               │
│    - Barrier wait time                                          │
│    - Lock granularity (coarse vs fine)                         │
├─────────────────────────────────────────────────────────────────┤
│ 2. KOMUNIKACJA                                                  │
│    - Przesyłanie danych między wątkami/procesami               │
│    - Bandwidth limitations                                      │
│    - Latency (szczególnie distributed)                         │
├─────────────────────────────────────────────────────────────────┤
│ 3. LOAD IMBALANCE                                               │
│    - Nierówny podział pracy                                    │
│    - Różne czasy wykonania task'ów                             │
├─────────────────────────────────────────────────────────────────┤
│ 4. CACHE EFFECTS                                                │
│    - False sharing                                              │
│    - Cache coherency traffic                                   │
│    - NUMA effects                                               │
├─────────────────────────────────────────────────────────────────┤
│ 5. THREAD MANAGEMENT                                            │
│    - Tworzenie/niszczenie wątków                               │
│    - Context switching                                          │
│    - Thread pool overhead                                       │
└─────────────────────────────────────────────────────────────────┘
```

#### False Sharing

```c
// Zły kod - false sharing
struct Counter {
    int count;  // Te pola są w tej samej linii cache!
} counters[NUM_THREADS];

// Thread i:
counters[i].count++;  // Invaliduje cache innych wątków!

// Dobry kod - padding
struct Counter {
    int count;
    char padding[60];  // Separacja na osobne linie cache
} counters[NUM_THREADS];
```

---

### 5. Efektywność równoległa

$$E(n) = \frac{S(n)}{n} = \frac{1}{n \cdot (1-p) + p}$$

| p | n=4 | n=16 | n=64 |
|---|-----|------|------|
| 90% | 77% | 36% | 13% |
| 95% | 87% | 55% | 24% |
| 99% | 97% | 86% | 61% |

**Wniosek:** Efektywność spada z liczbą procesorów. Trzeba zwiększać problem (Gustafson) lub zmniejszać (1-p).

---

### 6. Rozszerzone prawo Amdahla (z overhead)

$$S(n) = \frac{1}{(1-p) + \frac{p}{n} + O(n)}$$

Gdzie $O(n)$ = overhead zależny od n (komunikacja, synchronizacja).

```
Przykład: O(n) = 0.001·n (liniowy overhead)

n=10:   S = 1/(0.1 + 0.09 + 0.01) = 5.0
n=100:  S = 1/(0.1 + 0.009 + 0.1) = 4.8
n=1000: S = 1/(0.1 + 0.0009 + 1) = 0.9 (slowdown!)

Punkt optymalny: istnieje n* maksymalizujące S!
```

---

## 🧠 Mnemoniki

### "Amdahl = Sequential is the limit":
Część sekwencyjna limituje maksymalne przyśpieszenie

### "S_max = 1/(1-p)":
10% sekwencyjnej → max 10x speedup

### "Gustafson = Scale the problem":
Większy problem → lepsze wykorzystanie procesorów

### "FLOP = False sharing, Load imbalance, Overhead, Poor locality":
Główne przyczyny sublinearnego speedup

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy Gustafson jest lepszy od Amdahla?"
**Odpowiedź:** Gdy problem można skalować (więcej danych, iteracji). Symulacje fizyczne, rendering, ML training. Amdahl zakłada stały problem - pesymistyczny dla HPC.

### Q2: "Jak zmierzyć rzeczywiste p?"
**Odpowiedź:** Profilowanie (perf, VTune). Zmierz czas sekwencyjny vs równoległy. p ≈ 1 - T_seq/T_total. Uwaga: p może zależeć od danych wejściowych.

### Q3: "Co to jest strong vs weak scaling?"
**Odpowiedź:** Strong: stały problem, więcej proc. (Amdahl). Weak: problem rośnie proporcjonalnie do proc. (Gustafson). Weak scaling łatwiejsze do osiągnięcia.

---

## 🎯 Kluczowe punkty

1. **Amdahl:** $S = 1/((1-p) + p/n)$, max = $1/(1-p)$
2. **Sekwencyjna część limituje** - 10% seq → max 10x
3. **Gustafson:** Skaluj problem, nie procesory
4. **Overhead:** Sync, komunikacja, cache, load imbalance
5. **Efektywność spada** z liczbą procesorów

---

## 📖 Źródła

1. Amdahl - "Validity of the Single Processor Approach" (1967)
2. Gustafson - "Reevaluating Amdahl's Law" (1988)
3. Hennessy, Patterson - "Computer Architecture"
