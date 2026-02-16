## PYTANIE 21: Zegary logiczne i wektory stempli czasowych

**Koncepcja i przeznaczenie.**

---

### Tło pojęciowe — słowniczek

**Zegar (clock)** — urządzenie (lub mechanizm) mierzące upływ czasu. W informatyce rozróżniamy:
- **Zegar fizyczny (physical clock)** — kwarc, zegar atomowy, `System.currentTimeMillis()`. Mierzy czas rzeczywisty (sekundy), ale w systemie rozproszonym każdy węzeł ma WŁASNY zegar fizyczny i driftują (rozbieżność ~10–100 μs/s). Nie można na nich polegać do ustalenia kolejności zdarzeń.
- **Zegar logiczny (logical clock)** — abstrakcyjny licznik, który NIE mierzy czasu fizycznego, lecz **porządek zdarzeń** (co było wcześniej, co później). Nie odpowiada na „która godzina?", lecz na „czy A było przed B?".

    Zegar fizyczny:  "14:00:01.003"  → mówi KIEDY (ale niedokładnie!)
    Zegar logiczny:  "7"             → mówi CO KTÓRY RAZ (porządek)

**Zegar logiczny (logical clock)** — mechanizm przypisujący zdarzeniom wartości (stemple) tak, aby zachować porządek przyczynowy. Dwa warianty:
- **Zegar Lamporta** — każdy proces trzyma jeden licznik (skalar). Gwarantuje: a→b ⟹ C(a)<C(b). Ale NIE odwrotnie — nie wykrywa współbieżności.
- **Zegar wektorowy** — każdy z N procesów trzyma wektor N liczników. Gwarantuje: a→b **⟺** V(a)<V(b). Pełna informacja o porządku.

---

**Stempel czasowy (timestamp)** — wartość przypisana zdarzeniu przez zegar. W kontekście zegarów logicznych to NIE czas w sekundach, lecz wartość logiczna (liczba lub wektor liczb):

    Stempel fizyczny:  "2026-02-14T14:00:01.003Z"    (data/godzina)
    Stempel Lamporta:  7                               (jeden int)
    Stempel wektorowy: [3, 1, 5]                       (wektor intów)

**Wektor (vector)** — uporządkowana lista N liczb, po jednej per proces w systemie. W kontekście zegarów: V[i] oznacza „ile zdarzeń procesu i jest mi znanych".

    System z 3 procesami (P1, P2, P3):
    Wektor P1 = [3, 1, 0]
    Znaczenie: P1 wie o 3 swoich zdarzeniach, 1 zdarzeniu P2, 0 zdarzeniach P3

**Wektor stempli czasowych (vector timestamp / vector clock)** — stempel czasowy będący wektorem N wartości. Każde zdarzenie dostaje taki wektor. Porównując dwa wektory, możemy ustalić:
- **V(a) < V(b)** — każdy element V(a) ≤ odpowiedni V(b), i przynajmniej jeden <. Oznacza: **a → b** (a przyczynowo przed b).
- **V(a) || V(b)** — ani V(a)≤V(b), ani V(b)≤V(a). Oznacza: **współbieżne** (brak związku przyczynowego).

    Zdarzenie A: V(A) = [2, 0]
    Zdarzenie B: V(B) = [0, 1]
    Porównanie: 2>0 ale 0<1 → nieporównywalne → A || B (współbieżne!)

    Zdarzenie C: V(C) = [2, 1]
    Zdarzenie D: V(D) = [3, 2]
    Porównanie: 2≤3 i 1≤2, przynajmniej jeden < → V(C) < V(D) → C → D

---

**System rozproszony (distributed system)** — system, w którym wiele komputerów (węzłów) współpracuje przez sieć, ale nie współdzielą pamięci ani zegara. Przykłady: Cassandra, Dynamo, blockchain. Fundamentalny problem: jak ustalić kolejność zdarzeń, skoro nie ma wspólnego zegara?

**Brak globalnego zegara** — w systemie rozproszonym każdy węzeł ma własny zegar fizyczny. Zegary driftują (różnią się o milisekundy–sekundy). Nie można polegać na zegarze fizycznym do określenia „co było wcześniej". Dlatego potrzebne są zegary logiczne.

    Węzeł A: zegar 14:00:01.000
    Węzeł B: zegar 14:00:01.003  ← 3ms driftu!
    Czy zdarzenie A(14:00:01.002) było przed B(14:00:01.001)?
    Nie wiadomo — zegary fizyczne nie są zsynchronizowane!

---

**Zdarzenie (event)** — atomowa akcja w systemie: wykonanie instrukcji, wysłanie wiadomości, odebranie wiadomości. Zegary logiczne przypisują każdemu zdarzeniu „stempel czasowy" bez polegania na zegarze fizycznym.

**Relacja happened-before (→)** — porządek częściowy zdarzeń (Lamport, 1978):
1. Jeśli a i b są w tym samym procesie i a jest przed b → a → b
2. Jeśli a = wysłanie msg i b = odbiór tej msg → a → b
3. Przechodniość: a → b i b → c ⟹ a → c

**Zdarzenia współbieżne (a || b)** — dwa zdarzenia są współbieżne gdy ani a→b, ani b→a. Nie ma związku przyczynowego między nimi. Mogły zdarzyć się w dowolnej kolejności.

---

**Zegar Lamporta (Lamport clock)** — najprostszy zegar logiczny. Każdy proces ma jeden licznik (skalar). Algorytm:
1. Przed własnym zdarzeniem: C_i++
2. Przy wysyłaniu: dołącz timestamp C_i
3. Przy odbieraniu (timestamp t): C_i = max(C_i, t) + 1

**Co oznacza C_i?** C to nazwa „zegar" (Clock), a _i to indeks procesu. C_i to po prostu **lokalny licznik (integer) procesu i-tego**. Każdy proces P_i ma swój własny licznik C_i, startujący od 0. C(a) oznacza „wartość zegara Lamporta przypisana zdarzeniu a". Nie jest to czas w sekundach — to rosnąca liczba porządkowa.

    Proces P₁ ma zegar C₁ (startuje od 0)
    Proces P₂ ma zegar C₂ (startuje od 0)
    Zdarzenie a w procesie P₁ → C₁++ → C(a) = wartość C₁ w momencie zdarzenia a
    Zdarzenie b w procesie P₂ → C₂++ → C(b) = wartość C₂ w momencie zdarzenia b

**Krok po kroku — pełny przykład z 2 procesami:**

    Czas → → → → → → → → → → → → → → → → → →
    P₁:  C₁=0  [A: C₁=1] ─── wysyła msg(ts=1) ──→  [C: C₁=max(1,?)=1, C₁++=2]
                                                 ↗
    P₂:  C₂=0       [B: C₂=1] ──── [D: odbiera msg(ts=1), C₂=max(1,1)+1=2]

    Krok 1: P₁ robi zdarzenie A → C₁++ → C₁=1, więc C(A)=1
    Krok 2: P₂ robi zdarzenie B → C₂++ → C₂=1, więc C(B)=1
    Krok 3: P₁ wysyła msg do P₂, dołącza ts=C₁=1
    Krok 4: P₂ odbiera msg → C₂ = max(C₂=1, ts=1) + 1 = 2 → C(D)=2

    Wyniki: C(A)=1, C(B)=1, C(C)=2, C(D)=2

**Właściwość:**

a → b ⟹ C(a) < C(b) — **TAK**. Ale: C(a) < C(b) **NIE** implikuje a → b! Nie wykrywa współbieżności.

**DLACZEGO a → b ⟹ C(a) < C(b) (implikacja w przód DZIAŁA)?**

Dowód jest prosty — wynika wprost z algorytmu:
- Jeśli a i b są w TYM SAMYM procesie i a jest przed b → między a i b był co najmniej jeden C_i++ → C(a) < C(b). ✓
- Jeśli a = wysłanie msg i b = odbiór → C(b) = max(C_j, C(a)) + 1 ≥ C(a) + 1 > C(a). ✓
- Przechodniość: a→b→c ⟹ C(a) < C(b) < C(c). ✓

Innymi słowy: algorytm jest ZAPROJEKTOWANY tak, żeby każda kolejność przyczynowa była odzwierciedlona w wartościach zegarów.

**DLACZEGO C(a) < C(b) NIE implikuje a → b (implikacja w TYŁ NIE DZIAŁA)?**

Ponieważ Lamport to JEDEN licznik per proces — nie wie, co robią inne procesy. Dwa niezależne procesy mogą mieć te same wartości zegarów:

    P₁:  [A: C₁=1]     (P₁ zrobił swoje pierwsze zdarzenie)
    P₂:  [B: C₂=1]     (P₂ zrobił swoje pierwsze zdarzenie, niezależnie!)

    C(A)=1, C(B)=1 → C(A) = C(B)
    Ale nawet gdyby C(A)=1, C(B)=2, to nadal NIE WIEMY czy A→B!
    Bo B MOGŁO dostać C₂=2 z własnych wewnętrznych zdarzeń, niezwiązanych z A.

    Lamport widzi: C(A)=1, C(B)=1 → nie wie czy A||B, A→B, czy B→A
    → BRAK INFORMACJI o współbieżności — stracona!

---

**Zegar wektorowy (vector clock)** — każdy z N procesów utrzymuje wektor V[1..N]. Co to znaczy? Wyobraź sobie, że każdy proces ma **tablicę z N komórkami** — jedną per proces w systemie. V_i[j] = „ile zdarzeń procesu j jest mi (procesowi i) znanych".

**V_i** = wektor procesu i. **V_i[j]** = komórka j-ta w tym wektorze = „ile wiem o procesie j".

Algorytm (3 proste reguły):
1. **Własne zdarzenie:** V_i[i]++ — „zrobiłem coś, więc mój własny licznik rośnie"
2. **Wysyłanie msg:** dołącz CAŁY wektor V_i do wiadomości — „wysyłam swoją wiedzę o świecie"
3. **Odbieranie msg (wektor T):** V_i[j] = max(V_i[j], T[j]) dla KAŻDEGO j, potem V_i[i]++ — „aktualizuję swoją wiedzę na podstawie tego, co wie nadawca, a potem notuję, że sam coś zrobiłem (odbiór)"

![Zegary wektorowe — przykład z 3 procesami](img/vector_clock_timeline.png)

**Krok po kroku — pełna symulacja z 3 procesami (P₁, P₂, P₃):**

    Początek: V₁=[0,0,0], V₂=[0,0,0], V₃=[0,0,0]

    Krok 1: P₁ robi zdarzenie A
            V₁[1]++ → V₁=[1,0,0] → V(A) = [1,0,0]
            „P₁ wie o 1 swoim zdarzeniu, o P₂ i P₃ nic nie wie"

    Krok 2: P₂ robi zdarzenie B
            V₂[2]++ → V₂=[0,1,0] → V(B) = [0,1,0]
            „P₂ wie o 1 swoim zdarzeniu, o P₁ i P₃ nic nie wie"

    Krok 3: P₁ wysyła msg do P₂ (dołącza V₁=[1,0,0])
            P₂ odbiera: V₂ = max([0,1,0], [1,0,0]) = [1,1,0], potem V₂[2]++ = [1,2,0]
            Zdarzenie C (odbiór) → V(C) = [1,2,0]
            „P₂ teraz wie o 1 zdarzeniu P₁ (z msg), 2 swoich zdarzeniach, 0 o P₃"

    Krok 4: P₃ robi zdarzenie D
            V₃[3]++ → V₃=[0,0,1] → V(D) = [0,0,1]

**Teraz porównajmy — kto jest przed kim?**

    V(A)=[1,0,0] vs V(B)=[0,1,0]:
      Pozycja 1: 1 > 0 (A wygrywa)
      Pozycja 2: 0 < 1 (B wygrywa)
      → NIEPORÓWNYWALNE → A || B  (współbieżne!) ✓ (bo A i B były niezależne)

    V(A)=[1,0,0] vs V(C)=[1,2,0]:
      Pozycja 1: 1 ≤ 1 ✓
      Pozycja 2: 0 ≤ 2 ✓
      Przynajmniej jeden <: pozycja 2 → V(A) < V(C) → A → C ✓
      (bo C to odbiór msg od P₁, więc A przyczynowo wpłynęło na C)

    V(D)=[0,0,1] vs V(C)=[1,2,0]:
      Pozycja 1: 0 < 1 (C wygrywa), ale pozycja 3: 1 > 0 (D wygrywa)
      → NIEPORÓWNYWALNE → C || D ✓ (P₃ nie komunikował się z P₁/P₂)

**Formalne zasady porównywania wektorów:**

    V(a) < V(b) ⟺ ∀i: V(a)[i] ≤ V(b)[i]  AND  ∃j: V(a)[j] < V(b)[j]
    → Oznacza: a → b (a przyczynowo przed b)

    V(a) || V(b) ⟺ ¬(V(a) ≤ V(b)) ∧ ¬(V(b) ≤ V(a))
    → Oznacza: współbieżne (żaden nie „wie" wystarczająco o drugim)

**DLACZEGO V(a) < V(b) ⟺ a → b (równoważność DZIAŁA w obie strony)?**

Wektor niesie PEŁNĄ WIEDZĘ procesu o stanie systemu. Jeśli V(b) „wie" o wszystkim, co wie V(a), plus coś więcej — to znaczy, że informacja z a DOTARŁA do b (bezpośrednio lub pośrednio przez łańcuch wiadomości). Odwrotny kierunek: jeśli informacja z a NIE dotarła do b, to V(b) NIE będzie „wiedzieć" o a, więc będzie element, w którym V(b) < V(a) → wektory nieporównywalne → współbieżne.

Innymi słowy: wektor to „historia przyczynowa" — koduje WSZYSTKO, co dany proces widział. Dlatego porównanie wektorów daje PEŁNĄ informację o relacji między zdarzeniami.

Lamport tego nie potrafi, bo JEDNA liczba nie może zakodować N niezależnych historii.

---

**Porównanie Lamport vs Vector:**

    Cecha                  Lamport        Vector
    ───────────────────────────────────────────────
    Rozmiar per zdarzenie  O(1) (skalar)  O(N) (wektor)
    a→b ⟹ C(a)<C(b)       TAK            TAK
    C(a)<C(b) ⟹ a→b       NIE            TAK
    Wykrywa współbieżność  NIE            TAK

**Dlaczego Lamport NIE wykrywa współbieżności?**

Lamport kompresuje CAŁĄ historię do jednej liczby. To jak „kolejka w sklepie" — masz numerek 7, ktoś inny ma 8, ale nie wiesz, czy on przyszedł PO tobie, czy z innego wejścia (niezależnie). Jedna liczba nie koduje ŹRÓDŁA zdarzenia, tylko pewien porządek, który może być przypadkowy.

    P₁: A(C=1), B(C=2)     ← wewnętrzne zdarzenia P₁
    P₂: C(C=1), D(C=2)     ← wewnętrzne zdarzenia P₂ (niezależne od P₁!)

    Lamport widzi: C(A)=1 < C(D)=2 → „A przed D?"
    Ale NIE! A i D są WSPÓŁBIEŻNE — procesy działały niezależnie.
    Lamport zgubił tę informację, bo 1 < 2 nie implikuje związku przyczynowego.

**Dlaczego Vector Clock WSZYSTKO wykrywa?**

Vector przechowuje N liczb — osobną dla KAŻDEGO procesu. To jak „notatnik, w którym zapisujesz historię KAŻDEGO kolegi":

    V(A)=[1,0] → „wiem o 1 zdarzeniu P₁, 0 zdarzeniach P₂"
    V(D)=[0,2] → „wiem o 0 zdarzeniach P₁, 2 zdarzeniach P₂"

    Porównanie: pozycja 1 → 1>0 (A „wie więcej" o P₁)
                pozycja 2 → 0<2 (D „wie więcej" o P₂)
    → NIEPORÓWNYWALNE → A || D → WSPÓŁBIEŻNE! ✓

    Gdyby A wpłynęło na D (przez msg), to D wiedziałoby o zdarzeniach P₁
    → V(D)[1] ≥ 1 → ale V(D)[1]=0 → A NIE wpłynęło na D → współbieżne.

**Analogia: Lamport = jednokanałowe radio (słyszysz dźwięk, ale nie wiesz skąd). Vector = system GPS z N satelitami (dokładna pozycja przyczynowa w N-wymiarowej przestrzeni).**

---

**Porządek częściowy (partial order)** — relacja, w której nie wszystkie pary elementów są porównywalne. Happened-before to porządek częściowy: niektóre zdarzenia są współbieżne (nieporównywalne). Zegar wektorowy w pełni go reprezentuje.

**Porządek przyczynowy (causal order)** — wiadomości dostarczane w kolejności przyczynowej: jeśli wysłanie msg A → wysłanie msg B, to odbiorca widzi A przed B. Wymaga vector clocks.

**Version vectors / wektory wersji** — mechanizm replikacji danych w systemach rozproszonych (np. Amazon Dynamo). Każda replika utrzymuje wektor wersji obiektu. Przy konflikcie (wektory nieporównywalne = współbieżne zapisy) → system zwraca obie wersje do rozwiązania (siblings).

**Causal broadcast** — protokół rozsyłania wiadomości zachowujący porządek przyczynowy. Wiadomość B (zależna przyczynowo od A) jest dostarczana dopiero po A. Implementacja przez vector clocks.

---

### Problem: brak globalnego zegara w systemach rozproszonych (drift, opóźnienia)

### Relacja happened-before (→) — Lamport 1978
- a, b w jednym procesie, a przed b → a → b
- a = wysłanie msg, b = odbiór → a → b
- Przechodniość
- a || b (współbieżne) gdy ¬(a→b) ∧ ¬(b→a)

### Zegar Lamporta (skalarny)

Algorytm: przed zdarzeniem Cᵢ++; wysyłając dołącz Cᵢ; odbierając Cᵢ = max(Cᵢ, t) + 1.

| Właściwość                | Lamport |
|---------------------------|---------|
| a → b ⟹ C(a) < C(b)     | TAK     |
| C(a) < C(b) ⟹ a → b     | **NIE** |

### Zegary wektorowe

Każdy z N procesów ma wektor V[1..N]. Przed zdarzeniem: V[i]++; wysyłając dołącz V; odbierając: V[j] = max(V[j], T[j]) ∀j, potem V[i]++.

| Właściwość                    | Vector Clock |
|-------------------------------|-------------|
| a → b ⟺ V(a) < V(b)         | **TAK**     |
| Wykrycie współbieżności       | **TAK**     |

Porównanie: V ≤ W ⟺ ∀i: V[i] ≤ W[i]; V || W gdy ¬(V≤W) ∧ ¬(W≤V)

### Lamport: O(1) rozmiar, ale nie wykrywa współbieżności.
### Vector: O(N) rozmiar, ale pełna charakteryzacja happened-before.

### Zastosowania: replikacja (Dynamo — version vectors), causal broadcast, distributed debugging

### Etymologia

**Lamport** — Leslie Lamport (1978, „Time, Clocks, and the Ordering of Events..."); Turing Award 2013; twórca LaTeX-a! **Vector clocks** — Friedemann Mattern + Colin Fidge (niezależnie, 1988). **Happened-before** — Lamportowski termin; relacja częściowego porządku. **Dynamo** — Amazon (2007); wektory wersji do wykrywania konfliktów. **Causal broadcast** — „causal" od łac. „causa" = przyczyna; wiadomości dostarczane w porządku przyczynowym.

### Jak zapamiętać

- **Lamport = 1 liczba** — „wie że było wcześniej, ale nie wie czy współbieżnie"
- **Vector = wektor N liczb** — „każdy wie o każdym" → pełna informacja
- **V(a) < V(b) ⟺ a → b** — kluczowa równoważność vector clocks

