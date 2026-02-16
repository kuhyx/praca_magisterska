## PYTANIE 31: Interaktywne wspomaganie decyzji w warunkach ryzyka

**Przedstawić metody interaktywne.**

---

### Tło pojęciowe — słowniczek

**Decyzja (decision)** — wybór jednej opcji spośród co najmniej dwóch dostępnych alternatyw. W teorii decyzji to pojęcie formalne: mamy zbiór alternatyw $A = \{a_1, a_2, \dots, a_n\}$ i musimy wybrać „najlepszą" według pewnego kryterium.

    Przykład: „Kupić mieszkanie A za 400k, mieszkanie B za 350k, czy wynajmować?"
    3 alternatywy → 1 decyzja.

**Wspomaganie decyzji (decision support)** — dziedzina nauki o dostarczaniu decydentowi narzędzi, metod i modeli matematycznych, które pomagają mu podjąć lepszą (bardziej uzasadnioną) decyzję. NIE podejmujemy decyzji za niego — pomagamy mu zrozumieć problem, porównać alternatywy i ocenić ryzyko. Efekt: decydent podejmuje decyzję ŚWIADOMIE, znając konsekwencje.

    Bez wspomagania: „Czuję, że auto A jest lepsze" (intuicja)
    Ze wspomaganiem: „Auto A wygrywa 4 z 5 kryteriów, ale przegrywa ceną o 30%" (analiza)

**Warunki (conditions)** — w teorii decyzji „warunki" oznaczają POZIOM WIEDZY decydenta o konsekwencjach swoich wyborów. Nie chodzi o warunki atmosferyczne — chodzi o to, ile wiemy o przyszłości w momencie podejmowania decyzji.

**Ryzyko (risk)** — w potocznym języku „ryzyko" = zagrożenie. W teorii decyzji ma PRECYZYJNE znaczenie: sytuacja, w której znamy WSZYSTKIE możliwe wyniki każdej alternatywy ORAZ znamy ich PRAWDOPODOBIEŃSTWA. To kluczowe — ryzyko ≠ niepewność!

    Ryzyko: „Rzut kostką — wiem, że P(6) = 1/6, P(nie 6) = 5/6"
    Niepewność: „Nowy produkt na rynku — nie wiem nawet jakie są możliwe wyniki"

**Warunki ryzyka (conditions of risk)** — kontekst decyzyjny, w którym decydent zna możliwe scenariusze (stany natury) i ich prawdopodobieństwa, ale NIE wie, który scenariusz się zrealizuje. To środek spektrum między pewnością a niepewnością.

    Stan natury S₁ (p=0.6)    Stan natury S₂ (p=0.4)
    ──────────────────────────────────────────────────
    Alternatywa A:  +100 zł        −50 zł
    Alternatywa B:   +30 zł        +20 zł

    E[A] = 0.6×100 + 0.4×(−50) = 40 zł   ← wyższa średnia, ale ryzyko straty
    E[B] = 0.6×30  + 0.4×20    = 26 zł   ← niższa średnia, ale bezpieczna
    → Który wybrać? Zależy od PREFERENCJI decydenta wobec ryzyka!

**Metoda (method)** — w kontekście wspomagania decyzji: sformalizowany, powtarzalny algorytm (procedura krok po kroku), który prowadzi od danych wejściowych (alternatywy, kryteria, preferencje) do wyniku (ranking, wybór, klasyfikacja). Metoda musi być obiektywna i odtwarzalna — dwóch analityków z tymi samymi danymi dostaje ten sam wynik.

**Interaktywność (interactivity)** — cecha metody polegająca na DIALOGU z decydentem w trakcie procesu. Zamiast wymagać od decydenta podania WSZYSTKICH preferencji z góry (co jest trudne — ludzie nie znają swoich preferencji precyzyjnie), metoda interaktywna zadaje pytania krok po kroku i uczy się preferencji stopniowo.

    Metoda NIEinteraktywna (a priori):
    1. Decydent podaje wszystkie wagi/preferencje → [CZARNA SKRZYNKA] → wynik
    Problem: „Skąd mam wiedzieć, że cena jest 3× ważniejsza od komfortu?"

    Metoda interaktywna:
    1. System: „Wolisz A czy B?" → Decydent: „A"
    2. System: „A jest tańsze, ale mniej komfortowe. Ile komfortu poświęcisz za cenę?"
    3. Decydent: „Hmm, dużo" → System aktualizuje model preferencji
    4. System: „To może C? Tanie i w miarę komfortowe" → ...
    → Iteracyjne dochodzenie do najlepszej decyzji

**Interaktywne wspomaganie decyzji (interactive decision support)** — połączenie obu pojęć: pomagamy decydentowi wybrać najlepszą alternatywę przez DIALOG — zadajemy mu pytania o preferencje (np. „Wolisz X na pewno czy loterię Y?"), aktualizujemy model matematyczny, i proponujemy rozwiązanie. Proces powtarza się aż decydent jest usatysfakcjonowany.

    Cykl interaktywnego wspomagania:
    ┌──────────────────────────────────────────┐
    │  1. System proponuje pytanie/loterię     │
    │  2. Decydent odpowiada (preferencja)     │
    │  3. System aktualizuje model U(x)        │
    │  4. System proponuje rozwiązanie         │
    │  5. Decydent akceptuje? → TAK → KONIEC   │
    │                         → NIE → wróć do 1│
    └──────────────────────────────────────────┘

**Metody interaktywne (interactive methods)** — konkretne algorytmy realizujące interaktywne wspomaganie decyzji. W kontekście tego pytania są to: metoda loterii (wyznaczanie funkcji użyteczności U(x) przez pytania o loterie), metoda certainty equivalent (wyznaczanie ekwiwalentu pewności), AHP (porównania parami), PROMETHEE i ELECTRE (metody outranking). Każda z nich wymaga od decydenta ODPOWIEDZI na pytania — to czyni je interaktywnymi.

    Metoda            Jakie pytania zadaje decydentowi?
    ──────────────────────────────────────────────────────────────────
    Loteria           „Wolisz X na pewno, czy loterię (p: best, 1-p: worst)?"
    CE                „Ile na pewno = ta loteria?"
    AHP               „Ile razy kryterium A ważniejsze od B?" (skala 1-9)
    PROMETHEE         „Jak ważne jest każde kryterium?" (wagi)
    ELECTRE           „Jaki próg zgody/sprzeciwu?"

---

**Warunki decyzyjne** — trzy poziomy wiedzy o przyszłości, w których podejmujemy decyzje:

    Pewność (certainty)     → znamy dokładny wynik każdej decyzji
    Ryzyko (risk)           → znamy możliwe wyniki I ich prawdopodobieństwa
    Niepewność (uncertainty) → nie znamy prawdopodobieństw

Przykład ryzyka: „Z 60% szansą zysk 100 zł, z 40% strata 50 zł." Przykład niepewności: „Możemy zyskać lub stracić, ale nie wiemy ile i z jakim prawdopodobieństwem."

---

**Decydent (decision maker)** — osoba lub podmiot, który musi wybrać jedną z dostępnych alternatyw. Metody interaktywne wymagają dialogu z decydentem — pytamy go o preferencje, zamiast zakładać je z góry.

**Funkcja użyteczności U(x) (utility function)** — matematyczne przypisanie „wartości subiektywnej" do wyniku. Dla kogoś, kto boi się ryzyka, różnica między 0 a 1000 zł jest bardziej odczuwalna niż między 9000 a 10000 zł.

    U(x)
    │      ╭──────── wklęsła (risk-averse)
    │    ╱╱
    │  ╱╱
    │╱╱
    └──────────── x (pieniądze)

**Risk averse (awersja do ryzyka)** — decydent preferuje pewne wyniki nad ryzykowne loterie o tej samej wartości oczekiwanej. Funkcja U jest **wklęsła** (concave): U''(x) < 0.

    Loteria: 50% szans na 0 zł, 50% na 100 zł → E[X] = 50 zł
    Risk-averse: „Wolę 50 zł na pewno" (a nawet 40 zł na pewno!)

**Risk neutral (neutralność)** — U jest liniowa. Decydentowi jest obojętne czy dostanie E[X] na pewno, czy zagra w loterię.

**Risk seeking (skłonność do ryzyka)** — U jest **wypukła** (convex). Decydent woli ryzyko niż pewny E[X]. „Wolę zagrać niż dostać pewniaka."

---

**Loteria (lottery)** — formalizacja decyzji ryzykownej: zbiór wyników z ich prawdopodobieństwami. Notacja L = (p: best, 1-p: worst).

    L = (0.6: 100 zł,  0.4: 0 zł)
    E[L] = 0.6 × 100 + 0.4 × 0 = 60 zł

**Metoda loterii (lottery method)** — technika wyznaczania U(x) przez zadawanie pytań decydentowi. Ustalamy U(worst)=0, U(best)=1 i szukamy „indifference point" — prawdopodobieństwa p*, przy którym decydent jest obojętny między pewną kwotą a loterią.

    Pyt: „Wolisz 500 zł na pewno, czy loterię (p: 1000 zł, 1-p: 0 zł)?"
    Jeśli punkt obojętności p* = 0.7 → U(500) = 0.7
    (Risk-neutral dałby p*=0.5, bo 500/1000=0.5)

**Certainty Equivalent (CE, ekwiwalent pewności)** — pewna kwota, która jest dla decydenta równoważna danej loterii.

    Loteria: 50/50 zysk 100 zł lub 0 zł → E[X] = 50 zł
    Decydent risk-averse: CE = 35 zł (wolałby 35 zł na pewno niż grać)
    Risk premium = E[X] − CE = 50 − 35 = 15 zł

**Wartość oczekiwana E[X] (expected value)** — średni wynik loterii ważony prawdopodobieństwami.

    E[X] = Σ pᵢ × xᵢ
    Dla L = (0.3: 100, 0.7: 20): E[X] = 0.3×100 + 0.7×20 = 44

---

**AHP (Analytic Hierarchy Process)** — metoda Saaty'ego do wyboru najlepszej alternatywy gdy mamy wiele kryteriów. Rozbija problem na hierarchię: Cel → Kryteria → Alternatywy.

    Cel: Wybierz samochód
    ├── Kryterium: Cena
    │   ├── Auto A, Auto B, Auto C
    ├── Kryterium: Komfort
    │   ├── Auto A, Auto B, Auto C
    └── Kryterium: Spalanie
        ├── Auto A, Auto B, Auto C

**Porównania parami (pairwise comparisons)** — w AHP porównujemy każdą parę kryteriów/alternatyw i oceniamy na skali 1-9 Saaty'ego:

    1 = równe znaczenie
    3 = umiarkowana przewaga
    5 = silna przewaga
    7 = bardzo silna
    9 = absolutna przewaga

    Macierz 3×3 (Cena vs Komfort vs Spalanie):
           Cena  Komf  Spal
    Cena  [ 1     3     5  ]
    Komf  [ 1/3   1     2  ]
    Spal  [ 1/5   1/2   1  ]

**Eigenvalue (wartość własna)** — z macierzy porównań wyznaczamy wektor własny → wagi kryteriów. To serce AHP: macierz parami → ranking numeryczny.

**Consistency Ratio (CR)** — miara spójności ocen decydenta. Jeśli A>B i B>C, ale C>A, to niespójne. CR < 0.1 = akceptowalne. CR ≥ 0.1 → decydent powinien poprawić oceny.

---

**PROMETHEE (Preference Ranking Organization METHod for Enrichment Evaluations)** — metoda porównująca alternatywy parami per kryterium za pomocą funkcji preferencji. Wynik: przepływy (flows).

    Φ⁺(a) = outgoing flow = „o ile a jest lepsze od reszty" (siła)
    Φ⁻(a) = incoming flow = „o ile reszta jest lepsza od a" (słabość)
    Φ(a) = Φ⁺(a) − Φ⁻(a) = net flow → im wyższe, tym lepsza alternatywa

**ELECTRE (ÉLimination Et Choix Traduisant la REalité)** — metoda outranking: A przewyższa B (A S B) gdy:

1. **Concordance (zgoda):** wystarczająco dużo kryteriów popiera A nad B
2. **Discordance (sprzeciw):** żadne kryterium nie daje B drastycznej przewagi nad A

    Cecha         AHP              PROMETHEE         ELECTRE
    ──────────────────────────────────────────────────────────
    Input         parami (skala)   per-kryterium     per-kryterium
    Wynik         wagi + ranking   przepływy Φ       relacja outranking
    Typ           kompensacyjna    częściowo komp.   niekompensacyjna
    Sens          wartość globalna przepływ netto     eliminacja słabych

---

### Warunki: pewność (determinizm) → **ryzyko** (znane prawdopodobieństwa) → niepewność (brak prawdopodobieństw)

### Interaktywność = dialog z decydentem → odkrycie preferencji (funkcji użyteczności)

### Metody

**1. Metoda loterii:** Ustal U(worst)=0, U(best)=1. Pytaj: „Wolisz x_mid na pewno, czy loterię (p: best, 1-p: worst)?" Punkt obojętności p* = U(x_mid).

**2. Certainty Equivalent (CE):** CE(L) = pewna kwota równoważna loterii L.
- CE < E[X] → risk averse (wklęsła U)
- CE = E[X] → risk neutral
- CE > E[X] → risk seeking
- Risk Premium = E[X] − CE

**3. AHP (Analytic Hierarchy Process):** Hierarchia: Cel → Kryteria → Alternatywy. Porównania parami (skala 1-9) → eigenvalue → wagi. Consistency Ratio CR < 0.1.

**4. PROMETHEE:** Funkcje preferencji per kryterium; agregacja; przepływy Φ⁺, Φ⁻, Φ (net); ranking.

**5. ELECTRE:** Concordance (zgoda) + Discordance (sprzeciw) → outranking aSb.

### Etymologia

**AHP** — Thomas Saaty (U. of Pittsburgh, 1970s); Analytic Hierarchy Process. **PROMETHEE** — Preference Ranking Organization METHod for Enrichment Evaluations (Jean-Pierre Brans, 1982). **ELECTRE** — ÉLimination Et Choix Traduisant la REalité (Bernard Roy, 1965) = „Eliminacja i Wybór Odzwierciedlający Rzeczywistość". **Certainty Equivalent** — z teorii użyteczności von Neumanna-Morgensterna (1944). **Funkcja użyteczności** — Daniel Bernoulli (1738) wprowadził koncepcję; vN-M sformalizowali aksjomatycznie.

### Jak zapamiętać

- **CE = „ile dałbyś za pewniaka zamiast loterii?"** → miara awersji do ryzyka
- **AHP = „porównaj parami, policz wagi"** (macierz → eigenvalue)
- **PROMETHEE = „przepływy"** (Φ⁺ outgoing, Φ⁻ incoming)

