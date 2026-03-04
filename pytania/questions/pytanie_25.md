## PYTANIE 25: Prawo Amdahla — przyspieszenie równoległe

**Oszacować przyspieszenie. Co osłabia ograniczenie?**

---

### Tło pojęciowe — słowniczek

**Obliczenia równoległe (parallel computing)** — wykonanie wielu operacji jednocześnie na wielu procesorach/rdzeniach. Cel: przyspieszenie obliczeń. Nie każdy program da się w pełni zrównoleglić — zawsze jest część sekwencyjna (inicjalizacja, agregacja wyników, I/O).

    Sekwencyjnie (1 rdzeń): ████████████  12 sec
    Równolegle (4 rdzenie):  ███         3 sec (część równoległa)
                             ██           2 sec (część sekwencyjna)
                             Razem:       5 sec (nie 3!)

**Przyspieszenie (speedup)** — stosunek czasu sekwencyjnego do równoległego: S(n) = T_seq / T_par(n). Idealne przyspieszenie na n procesorach = n (liniowe). W praktyce zawsze mniej z powodu części sekwencyjnej i overheadów.

---

**Prawo Amdahla (Amdahl's Law)** — określa MAKSYMALNE przyspieszenie programu przy zrównolegleniu na n procesorach. Kluczowe parametry:
- **p** — część programu, którą DA SIĘ zrównoleglić (0 ≤ p ≤ 1)
- **(1-p)** — część sekwencyjna (nie do zrównoleglenia)
- **n** — liczba procesorów

**Wzór:**

    S(n) = 1 / ((1-p) + p/n)

**Dlaczego tak?** Czas sekwencyjny = 1. Część sekwencyjna zajmuje (1-p), nie przyspiesza. Część równoległa trwa p/n. Suma = nowy czas.

**Maksymalne przyspieszenie (n→∞):**

    S_max = 1/(1-p)

    p=90% (10% sekwencyjne) → S_max = 1/0.10 = 10x
    p=95% (5% sekwencyjne)  → S_max = 1/0.05 = 20x
    p=99% (1% sekwencyjne)  → S_max = 1/0.01 = 100x

**Kluczowy wniosek:** nawet z nieskończoną liczbą procesorów, 10% sekwencyjnego kodu ogranicza przyspieszenie do 10x! Sekwencyjna część dominuje.

**Przykład liczbowy: p=90%, n=4:**

    S(4) = 1 / (0.10 + 0.90/4) = 1 / (0.10 + 0.225) = 1/0.325 ≈ 3.08x
    Z 4 procesorów uzyskamy ~3.08x, NIE 4x!

---

**Prawo Gustafsona (Gustafson's Law)** — alternatywna perspektywa osłabiająca ograniczenie Amdahla. Zamiast „przyspiesz stały problem" → „rozwiąż WIĘKSZY problem w tym samym czasie".

    S = 1 − p + p·n    (scaled speedup)

Dla p=90%, n=100: Gustafson → S = 1 - 0.9 + 0.9×100 = 90.1x (vs Amdahl: ~10x!)

**Strong scaling (Amdahl)** — stały rozmiar problemu, więcej procesorów.
**Weak scaling (Gustafson)** — rozmiar problemu rośnie proporcjonalnie do procesorów. W praktyce: więcej rdzeni → większa symulacja, więcej danych, wyższa rozdzielczość.

---

**Efektywność (efficiency):** E(n) = S(n)/n — ile z dodanych procesorów jest naprawdę wykorzystane. E(4)=3.08/4=0.77 → 77% efektywności. Spada z n.

**Overhead synchronizacji** — dodatkowy koszt koordynacji między wątkami/procesami: mutex contention, bariery, komunikacja. Im więcej procesów, tym większy overhead.

**False sharing** — dwa rdzenie modyfikują różne zmienne, ale leżące w tej samej linii cache. Powoduje ciągłe invalidation cache — dramatyczny spadek wydajności.

    Core 0 pisze: x (cache line 42)
    Core 1 pisze: y (cache line 42!)  ← ta sama linia!
    → Pingpong cache line między rdzeniami

**NUMA (Non-Uniform Memory Access)** — architektura: pamięć „bliżej" jednego procesora jest szybsza dla niego. Odwołanie do pamięci zdalnej = wolniejsze. Programy muszą uwzględniać lokalność.

**Load imbalance (nierównomierne obciążenie)** — procesory kończą w różnych czasach. Najwolniejszy limituje cały czas. Rozwiązanie: dynamic scheduling, work stealing.

**Lock-free (bez blokad)** — struktury danych operujące na CAS (Compare-And-Swap) zamiast mutexów. Eliminują blokowanie, ale trudniejsze w implementacji.

**Pipelining** — podział pracy na etapy: każdy etap na osobnym rdzeniu. Jak taśma montażowa: etap 1 przetwarza dane N, etap 2 — dane N-1, etap 3 — dane N-2, jednocześnie.

---

### Prawo Amdahla

    S(n) = 1 / ((1-p) + p/n)

- p = część równoległa, n = procesory
- Maks. przyspieszenie (n→∞): **S_max = 1/(1-p)**
- 10% sekwencyjnego kodu → max **10x** nawet z ∞ procesorami!

### Tabela przykładów

| p     | n=4  | n=16 | n=∞   |
|-------|------|------|-------|
| 90%   | 3.08 | 5.93 | 10    |
| 95%   | 3.48 | 9.52 | 20    |
| 99%   | 3.88 |13.91 | 100   |

### Co osłabia ograniczenie?

**Prawo Gustafsona:** S = 1 − p + p·n. Skaluj problem (więcej danych), nie procesory. Dla p=90%, n=100 → S=90.1x (vs Amdahl: ~10x).

**Techniki:** algorytmy równoległe, lock-free structures, pipelining, speculative execution, ukrywanie latencji (async I/O, prefetching).

### Czynniki zmniejszające RZECZYWISTE przyspieszenie

- Overhead synchronizacji (mutex contention)
- Komunikacja (latencja, bandwidth)
- Load imbalance
- Cache effects (false sharing, NUMA)
- Thread management

### Efektywność: E(n) = S(n)/n — spada z n

---

### 🎮 Mostek do pracy magisterskiej — Amdahl w silnikach gier

> W pracy mierzę frame time silników Nsightem — to DOKŁADNIE problem Amdahla: ile z pipeline'u renderowania da się zrównoleglić?

![Amdahl w game pipeline — frame budget](img/q25_amdahl_game_pipeline.png)

#### Frame budget jako problem Amdahla

Cel: 60 FPS → frame budget = 16.67 ms. Pipeline w jednej klatce:

| Faza pipeline'u | Czas [ms] | Równoległa? |
|----------------|-----------|-------------|
| Input polling | 0.2 | NIE (sekw.) |
| Game Logic / AI | 2.0 | CZĘŚCIOWO (Job System) |
| Physics (FixedUpdate) | 3.0 | TAK (PhysX broadphase) |
| Rendering (draw calls) | 8.0 | TAK (GPU parallel) |
| Audio mixing | 1.0 | TAK (osobny wątek) |
| GC / Housekeeping | 1.5 | NIE (stop-the-world!) |
| **SUMA** | **15.7** | |

Część sekwencyjna: $s = (0.2 + 1.5) / 15.7 ≈ 0.108$ (10.8%)

Prawo Amdahla: $S_{max} = \frac{1}{0.108} ≈ 9.26×$ — nawet z ∞ rdzeni max 9.26× speedup!

#### Unity vs Unreal — różnica w „s" (część sekwencyjna)

| Czynnik | Unity (C#) | Unreal (C++) | Wpływ na Amdahla |
|---------|-----------|--------------|-------------------|
| GC pauses | ~2 ms/frame (Boehm) | 0 ms (brak GC) | Unity: s ↑ → S_max ↓ |
| Job System | Unity DOTS / Burst | TaskGraph | Oba: p ↑, ale API różne |
| Draw call batching | SRP Batcher (~40% mniej) | Nanite (auto-LOD) | Oba redukują czas GPU |
| Main thread lock | `Update()` jest single-thread | `Tick()` jest single-thread | Oba: s zawiera game logic |

#### Obliczenie z Nsight (dane z mojej pracy)

    Unity bullet-hell (500 pocisków):
      Seq: Input(0.2) + GC(1.8) + MainThread-Logic(1.5) = 3.5 ms
      Par: Physics(2.0) + Render(7.0) + Audio(0.8) = 9.8 ms
      Total = 13.3 ms → s = 3.5/13.3 = 0.263
      S_max = 1/0.263 ≈ 3.8×

    Unreal bullet-hell (500 pocisków):
      Seq: Input(0.2) + MainThread-Logic(1.2) = 1.4 ms
      Par: Physics(1.8) + Render(6.5) + Audio(0.7) = 9.0 ms
      Total = 10.4 ms → s = 1.4/10.4 = 0.135
      S_max = 1/0.135 ≈ 7.4×

**Wniosek**: Unreal ma mniejszą część sekwencyjną (brak GC!) → lepsze skalowanie.

#### Gustafson w gamedev — „zwiększ świat"

Podejście Gustafson: zamiast „jak szybko 500 pocisków?" → „ile pocisków przy stałym frame budget?"
- Unity (4 rdzenie): ~800 pocisków w 16.67ms
- Unreal (4 rdzenie): ~1200 pocisków w 16.67ms
- To **weak scaling** — typowe dla open-world gier

#### Mnemonik — „NSIGHT" = Naprawdę Sekwencyjna Część Ogranicza

- **N**ie da się przyspieszyć ponad 1/s
- **S**ekwencyjna = GC + Input + Main Thread
- **I**nstrukcje GPU = ta równoległa część
- **G**ustafson = zwiększ problem (więcej pocisków!)
- **H**ardware ma N rdzeni → E(n)=S(n)/n
- **T**est w Nsight → zmierz s i p empirycznie

Na obronie: *„Prawo Amdahla bezpośrednio tłumaczy wyniki moich benchmarków — Unity ma większą część sekwencyjną (GC stop-the-world), więc gorzej skaluje się wielowątkowo. Unreal bez GC osiąga prawie 2× lepsze teoretyczne speedup. To zmierzyłem Nsightem."*

---

### Etymologia

**Gene Amdahl** (IBM, 1967, „Validity of the single processor approach..."); współtwórca IBM System/360. **John Gustafson** (Sandia Labs, 1988, „Reevaluating Amdahl's Law"); weak scaling vs strong scaling. **Speedup (przyspieszenie)** — stosunek czasu sekwencyjnego do równoległego. **Efektywność** — ile z dodanych procesorów jest naprawdę wykorzystane. **Lock-free** — struktury danych bez blokad (CAS — Compare-And-Swap).

### Jak zapamiętać

- **S = 1/((1-p) + p/n)** — zapamiętaj wzór!
- **„10% seq = max 10x"** — sekwencyjna część limituje WSZYSTKO
- **Gustafson = „zwiększ problem, nie procesory"** — weak scaling
- **„FLOP" = False sharing, Load imbalance, Overhead, Poor locality**

