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

**Metody interaktywne (interactive methods)** — konkretne algorytmy realizujące interaktywne wspomaganie decyzji. W kontekście tego pytania są to KRYTERIA DECYZYJNE stosowane gdy decydent nie zna prawdopodobieństw stanów natury (lub je zakłada). Interaktywność polega na tym, że decydent WYBIERA kryterium (a w przypadku Hurwicza — także parametr α), co wymaga dialogu o jego postawie wobec ryzyka.

    Kryterium         Pytanie do decydenta / założenie
    ──────────────────────────────────────────────────────────────────
    Wart. oczekiwana  „Znasz prawdopodobieństwa stanów?" (potrzebne p)
    Laplace'a         „Każdy stan natury równie prawdopodobny" (założenie)
    Optymistyczne     „Zawsze liczysz na najlepszy scenariusz?" (postawa)
    Pesymistyczne     „Chcesz zabezpieczyć się przed najgorszym?" (postawa)
    Hurwicza          „Podaj swój współczynnik optymizmu α ∈ [0,1]" (parametr)
    Savage'a          „Chcesz minimalizować żal z podjętej decyzji?" (postawa)

---

**Warunki decyzyjne** — trzy poziomy wiedzy o przyszłości, w których podejmujemy decyzje:

    Pewność (certainty)     → znamy dokładny wynik każdej decyzji
    Ryzyko (risk)           → znamy możliwe wyniki I ich prawdopodobieństwa
    Niepewność (uncertainty) → nie znamy prawdopodobieństw

Przykład ryzyka: „Z 60% szansą zysk 100 zł, z 40% strata 50 zł." Przykład niepewności: „Możemy zyskać lub stracić, ale nie wiemy ile i z jakim prawdopodobieństwem."

![Warunki decyzyjne — spektrum wiedzy decydenta](img/q31_conditions_spectrum.png)

---

**Decydent (decision maker)** — osoba lub podmiot, który musi wybrać jedną z dostępnych alternatyw. Metody interaktywne wymagają dialogu z decydentem — pytamy go o postawę wobec ryzyka (optymista? pesymista?) i ew. parametry (α Hurwicza).

**Stan natury (state of nature)** — scenariusz/sytuacja zewnętrzna, na którą decydent NIE ma wpływu. Np. pogoda, koniunktura gospodarcza, zachowanie konkurencji. Oznaczamy S₁, S₂, …, Sₙ.

    Stany natury: S₁ = „dobra koniunktura", S₂ = „zła koniunktura"
    Decydent NIE wybiera stanu — stan „się zdarza".

**Macierz wypłat (payoff matrix)** — tabela, w której wiersze = alternatywy (decyzje), kolumny = stany natury, a komórki = wyniki (wypłaty). To podstawowa struktura danych dla WSZYSTKICH kryteriów decyzyjnych.

    Przykład — macierz wypłat (zyski w tys. zł):
                  S₁ (dobra)    S₂ (średnia)   S₃ (zła)
    ─────────────────────────────────────────────────────
    A₁ (fabryka)     200           50            −100
    A₂ (sklep)        80           70              40
    A₃ (obligacje)    30           30              30

    A₁ może dać 200k, ale też stratę 100k.
    A₃ daje 30k niezależnie od stanu → decyzja bezpieczna.

**Wartość oczekiwana E[X] (expected value)** — średni wynik ważony prawdopodobieństwami stanów natury. Używana w kryterium wartości oczekiwanej (gdy znamy prawdopodobieństwa) i w kryterium Laplace'a (z równymi prawdopodobieństwami).

    E[X] = Σ pᵢ × xᵢ

    Przykład z PRAWDZIWYMI prawdopodobieństwami (p₁=0.5, p₂=0.3, p₃=0.2):
    E[A₁] = 0.5×200 + 0.3×50 + 0.2×(−100) = 100 + 15 − 20 = 95  ← MAX
    E[A₂] = 0.5×80  + 0.3×70 + 0.2×40     = 40 + 21 + 8   = 69
    E[A₃] = 0.5×30  + 0.3×30 + 0.2×30     = 15 + 9 + 6    = 30

    Dla Laplace'a (równe prawdopodobieństwa, p₁ = p₂ = p₃ = 1/3):
    E[A₁] = (200 + 50 + (−100)) / 3 = 150/3 = 50
    E[A₂] = (80 + 70 + 40) / 3 = 190/3 ≈ 63.3  ← najlepsza wg Laplace'a
    E[A₃] = (30 + 30 + 30) / 3 = 30

**Kryterium wartości oczekiwanej (expected value criterion)** — NAJPROSTSZA metoda decyzyjna W WARUNKACH RYZYKA (gdy znamy prawdopodobieństwa). Oblicz E[Aᵢ] = Σⱼ pⱼ × aᵢⱼ dla każdej alternatywy i wybierz tę z NAJWYŻSZĄ wartością oczekiwaną.

    Formuła: V(Aᵢ) = Σⱼ pⱼ × aᵢⱼ    →    wybierz Aᵢ z max V(Aᵢ)

    Przykład (p₁=0.5, p₂=0.3, p₃=0.2):
    V(A₁) = 0.5×200 + 0.3×50 + 0.2×(−100) = 95  ← MAX → wybieramy A₁
    V(A₂) = 0.5×80  + 0.3×70 + 0.2×40     = 69
    V(A₃) = 0.5×30  + 0.3×30 + 0.2×30     = 30

    Kluczowa różnica od Laplace'a:
    - Laplace: ZAKŁADA p = 1/n (bo nie znamy prawdopodobieństw)
    - Wart. oczekiwana: UŻYWA PRAWDZIWYCH p (bo je znamy!)

    Przykład życiowy: firma rozważa inwestycję
    - Analityk oszacował: P(boom) = 50%, P(stabilna) = 30%, P(kryzys) = 20%
    - Fabryka wygrywa (E=95k), bo wysoki zysk w boomie (200k) × duże p (50%)
      przeważa nad stratą w kryzysie (−100k) × małe p (20%)

    Ograniczenie: E[X] ignoruje ROZRZUT wyników! A₁ ma E=95k, ale może
    dać −100k. Decydent z awersją do ryzyka może wolę A₂ (E=69k, ale
    minimum 40k). Dlatego sam E[X] nie wystarczy — potrzeba też analizy
    ryzyka (np. wariancji, worst-case).

    Mnemonik: „Średnia ważona — jak średnia ocen"
    Wynik × prawdopodobieństwo = waga.
    Sumuj wagi → E[X]. Jak w dzienniku: 5×0.3 + 4×0.5 + 2×0.2 = 3.9

![Kryterium wartości oczekiwanej — rozkład wyników](img/q31_expected_value.png)

---

**Kryterium decyzyjne (decision criterion)** — reguła/algorytm, który z macierzy wypłat wyznacza „najlepszą" alternatywę. Każde kryterium odzwierciedla INNĄ postawę decydenta wobec ryzyka. Dlatego to samo zadanie może dać INNE odpowiedzi zależnie od wybranego kryterium — i to jest OK.

    Te same dane, różne kryteria → różne „najlepsze" decyzje:
    Kryterium          Wygrywa     Dlaczego?
    ─────────────────────────────────────────────────────
    Wart. oczekiwana   A₁ (95)     najwyższa E[X] z prawdziwymi p
    Laplace            A₂ (≈63)    najwyższa średnia (równe p)
    Optymistyczne      A₁ (200)    najwyższy max
    Pesymistyczne      A₂ (40)     najwyższy min (bezpieczne)
    Hurwicz (α=0.6)    A₁ (80)     kompromis
    Savage             A₂ (120)    najniższy max żalu

![Porównanie kryteriów — macierz wypłat i wykresy](img/q31_criteria_comparison.png)

**Kryterium Laplace'a (Laplace criterion / principle of insufficient reason)** — zakładamy, że WSZYSTKIE stany natury są RÓWNIE PRAWDOPODOBNE (bo nie mamy powodu faworyzować żadnego). Obliczamy średnią arytmetyczną wypłat dla każdej alternatywy i wybieramy najwyższą.

    Formuła: V(Aᵢ) = (1/n) × Σⱼ aᵢⱼ    (n = liczba stanów natury)

    Przykład z macierzy powyżej (n=3):
    V(A₁) = (200 + 50 + (−100)) / 3 = 50.0
    V(A₂) = (80 + 70 + 40) / 3       = 63.3  ← MAX → wybieramy A₂
    V(A₃) = (30 + 30 + 30) / 3       = 30.0

    Interaktywność: decydent musi zaakceptować założenie równych
    prawdopodobieństw — „Czy zgadzasz się, że każdy scenariusz
    jest tak samo możliwy?"

    Przykład życiowy: wybieram restaurację w nieznanym mieście.
    Nie wiem, która dobra — traktuję je „po równo" i porównuję
    średnią ocen z 3 portali (każdy portal = stan natury z p=1/3).

    Mnemonik: „Laplace = Loteria — Losowe, ALE Po równo"

**Kryterium optymistyczne (maximax / optimistic criterion)** — decydent-OPTYMISTA: dla każdej alternatywy bierzemy NAJLEPSZY możliwy wynik (max w wierszu), potem wybieramy alternatywę z najwyższym z tych maksimów.

    Formuła: V(Aᵢ) = maxⱼ aᵢⱼ    →    wybierz Aᵢ z max V(Aᵢ)

    max(A₁) = max(200, 50, −100) = 200  ← MAX → wybieramy A₁
    max(A₂) = max(80, 70, 40)    = 80
    max(A₃) = max(30, 30, 30)    = 30

    A₁ wygrywa — optymista liczy na najlepszy scenariusz (200k).
    Ryzyko: jeśli S₃, to strata −100k!

    Przykład życiowy: gracz w pokera, który zawsze idzie all-in,
    bo „może trafię straight flush". Patrzy TYLKO na najlepsze
    możliwe rozdanie. Ignoruje szansę przegranej.

    Mnemonik: „Maximax = Marzyciel — Max z Max, bo MARZĘ o najlepszym"

**Kryterium pesymistyczne (maximin / Wald criterion)** — decydent-PESYMISTA: dla każdej alternatywy bierzemy NAJGORSZY możliwy wynik (min w wierszu), potem wybieramy alternatywę z najwyższym z tych minimów. Zabezpieczamy się przed najgorszym scenariuszem.

    Formuła: V(Aᵢ) = minⱼ aᵢⱼ    →    wybierz Aᵢ z max V(Aᵢ)

    min(A₁) = min(200, 50, −100) = −100
    min(A₂) = min(80, 70, 40)    = 40
    min(A₃) = min(30, 30, 30)    = 30

    max{−100, 40, 30} = 40 → wybieramy A₂
    Pesymista: „Nawet w najgorszym razie dostanę 40k" (A₂ jest bezpieczna).

    Przykład życiowy: jadąc na wakacje, pesymista wybiera hotel z gwarancją
    zwrotu, bo „a jeśli będzie brzydka pogoda?". Woli gwarantowany minimum
    komfort niż ryzykować. Ubezpieczenia działają na tej zasadzie.

    Mnemonik: „Maximin = Mur obronny — buduję MUR pod MINimum, bo zawsze
    zakładam NAJGORSZE (Wald = Wall = Mur)"

**Kryterium Hurwicza (Hurwicz criterion)** — kompromis między optymizmem a pesymizmem. Decydent podaje współczynnik optymizmu α ∈ [0, 1], gdzie α = 1 to pełny optymista, α = 0 to pełny pesymista.

    Formuła: V(Aᵢ) = α × maxⱼ aᵢⱼ + (1−α) × minⱼ aᵢⱼ

    Dla α = 0.6:
    V(A₁) = 0.6×200 + 0.4×(−100) = 120 − 40 = 80
    V(A₂) = 0.6×80  + 0.4×40     = 48 + 16  = 64
    V(A₃) = 0.6×30  + 0.4×30     = 18 + 12  = 30

    max{80, 64, 30} = 80 → A₁ wygrywa dla α=0.6.

    Dla α = 0.3 (bardziej pesymistyczny):
    V(A₁) = 0.3×200 + 0.7×(−100) = 60 − 70 = −10
    V(A₂) = 0.3×80  + 0.7×40     = 24 + 28 = 52  ← teraz A₂!
    V(A₃) = 0.3×30  + 0.7×30     = 9 + 21  = 30

    → Zmiana α zmienia wynik! Dlatego TO kryterium jest najbardziej
      interaktywne — decydent MUSI podać swoje α w dialogu.

    Przypadki specjalne:
    α = 1 → kryterium optymistyczne (maximax)
    α = 0 → kryterium pesymistyczne (maximin)

    Przykład życiowy: kupujesz akcje. Z α=0.8 (optymista) patrzysz głównie
    na potencjalny zysk. Z α=0.2 (pesymista) prawie tylko na potencjalną
    stratę. α to „pokrętło optymizmu" — kręcisz i widzisz jak zmienia
    się rekomendacja.

    Mnemonik: „Hurwicz = Huśtawka — huśtasz się między max a min,
    α mówi jak daleko w stronę max się wychylasz"

![Kryterium Hurwicza — wpływ α na wybór](img/q31_hurwicz_alpha.png)

**Współczynnik optymizmu α (optimism coefficient)** — parametr Hurwicza z przedziału [0, 1]. Wyraża postawę decydenta: α bliskie 1 = optymista (wierzy w dobre scenariusze), α bliskie 0 = pesymista.

    α = 1.0 → patrzę tylko na max → maximax
    α = 0.5 → równa waga max i min
    α = 0.0 → patrzę tylko na min → maximin

---

**Macierz żalu / macierz strat (regret matrix)** — tabela, w której każda komórka zawiera ŻALE (regret) = ile TRACĘ wybierając daną alternatywę zamiast najlepszej w danym stanie natury.

    Obliczanie: rᵢⱼ = maxₖ aₖⱼ − aᵢⱼ  (max w kolumnie minus wartość w komórce)

    Macierz wypłat:              Macierz żalu:
              S₁    S₂    S₃              S₁    S₂    S₃    max żalu
    A₁       200    50   −100    A₁        0     20    140     140
    A₂        80    70     40    A₂      120      0      0     120  ← MIN
    A₃        30    30     30    A₃      170     40     10     170

    maxₖ aₖ₁ = 200, maxₖ aₖ₂ = 70, maxₖ aₖ₃ = 40
    r₁₁ = 200−200 = 0,   r₁₂ = 70−50 = 20,  r₁₃ = 40−(−100) = 140
    r₂₁ = 200−80 = 120,  r₂₂ = 70−70 = 0,   r₂₃ = 40−40 = 0
    r₃₁ = 200−30 = 170,  r₃₂ = 70−30 = 40,  r₃₃ = 40−30 = 10

**Kryterium Savage'a (minimax regret / Savage criterion)** — minimalizacja MAKSYMALNEGO ŻALU. Dla każdej alternatywy znajdujemy największy żal (max w wierszu macierzy żalu), potem wybieramy alternatywę z NAJMNIEJSZYM max żalem.

    Formuła: V(Aᵢ) = maxⱼ rᵢⱼ    →    wybierz Aᵢ z min V(Aᵢ)

    max żalu(A₁) = max(0, 20, 140)  = 140
    max żalu(A₂) = max(120, 0, 0)   = 120  ← MIN → wybieramy A₂
    max żalu(A₃) = max(170, 40, 10) = 170

    Interpretacja: „Niezależnie co się zdarzy, mój żal nie przekroczy 120k"
    (gdybym wybrał A₁, mógłbym żałować aż 140k; A₃ → aż 170k).

    Przykład życiowy: wybieram studia. Po 5 latach zobaczę, jaki zawód
    najlepiej zarabia. Żal = „ile bym zarobił na najlepszych studiach
    minus ile zarabiam". Savage minimalizuje ten maksymalny żal —
    wybieram studia, po których NIGDY nie będę żałować za bardzo.

    Mnemonik: „Savage = Szał żalu — Savage to dziki (savage) żal,
    więc go minimalizuję. Min z max żalu = trzymam żal na smyczy."

![Kryterium Savage'a — budowa macierzy żalu](img/q31_regret_matrix.png)

---

**Porównanie kryteriów — tabela zbiorcza:**

    Kryterium       Postawa         Formuła               Wymaga od decydenta
    ──────────────────────────────────────────────────────────────────────────────
    Wart. oczekiw.  racjonalna      Σ pⱼ·aᵢⱼ              podanie prawdopodobieństw
    Laplace         neutralna       średnia wypłat         akceptacja równych p
    Optymistyczne   optymista       max z max              nic (automatyczne)
    Pesymistyczne   pesymista       max z min              nic (automatyczne)
    Hurwicza        kompromis       α·max + (1−α)·min      podanie α ∈ [0,1]
    Savage'a        minimalizacja   min z max żalu          nic (automatyczne)
                    żalu

![Mapa mnemoniczna — wszystkie kryteria](img/q31_criteria_mnemonic.png)

---

### Warunki: pewność (determinizm) → **ryzyko** (znane prawdopodobieństwa) → niepewność (brak prawdopodobieństw)

### Interaktywność = dialog z decydentem → odkrycie preferencji (funkcji użyteczności)

### Metody (kryteria decyzyjne)

**0. Kryterium wartości oczekiwanej (E[X]):** WYMAGA prawdopodobieństw stanów (warunki RYZYKA). Oblicz E[Aᵢ] = Σⱼ pⱼ·aᵢⱼ. Wybierz max. Ograniczenie: ignoruje rozrzut/ryzyko.

**1. Kryterium Laplace'a:** Załóż równe prawdopodobieństwa stanów (warunki NIEPEWNOŚCI). Oblicz średnią wypłat per alternatywa. Wybierz max średniej. Formuła: V(Aᵢ) = (1/n) × Σⱼ aᵢⱼ.

**2. Kryterium optymistyczne (maximax):** Dla każdej alternatywy weź max wypłatę. Wybierz alternatywę z max z tych max. Formuła: max maxⱼ aᵢⱼ.

**3. Kryterium pesymistyczne (maximin / Walda):** Dla każdej alternatywy weź min wypłatę. Wybierz alternatywę z max z tych min. Formuła: max minⱼ aᵢⱼ.

**4. Kryterium Hurwicza:** Kompromis: V(Aᵢ) = α × maxⱼ aᵢⱼ + (1−α) × minⱼ aᵢⱼ. Decydent podaje α ∈ [0,1]. α=1 → maximax, α=0 → maximin.

**5. Kryterium Savage'a (minimax regret):** Zbuduj macierz żalu (rᵢⱼ = maxₖ aₖⱼ − aᵢⱼ). Dla każdej alternatywy weź max żal. Wybierz alternatywę z min max żalu.

### Etymologia

**Wartość oczekiwana** — pojęcie z XVII w., Blaise Pascal i Pierre de Fermat (1654), formalizacja hazardu; „ile przeciętnie wygrasz?". **Laplace** — Pierre-Simon de Laplace (1749–1827), francuski matematyk; zasada niedostatecznej racji (principle of insufficient reason) — jeśli nie mamy powodu faworyzować żadnego stanu, traktujemy je jako równie prawdopodobne. **Wald** — Abraham Wald (1902–1950), matematyk z Wiednia; kryterium maximin = strategia minimax z teorii gier. **Hurwicz** — Leonid Hurwicz (1917–2008), laureat Nobla z ekonomii 2007 (z Myersonem i Maskinem, za mechanism design); zaproponował kompromis z parametrem α. **Savage** — Leonard Jimmie Savage (1917–1971), amerykański statystyk; kryterium minimax regret — minimalizacja żalu (1951, „The Foundations of Statistics").

### Jak zapamiętać

- **E[X] = „średnia ważona prawdopodobieństwami"** → jak średnia ocen w dzienniku, ale wagi to szanse
- **Laplace = „wszystko po równo"** → średnia arytmetyczna wypłat (Loteria — ALE Po równo)
- **Maximax = „marzyciel → max z max"** → najlepszy z najlepszych, ignoruje ryzyko
- **Maximin = „mur obronny → max z min"** → najlepszy z najgorszych (Wald = Wall = Mur)
- **Hurwicz = „huśtawka — α pomiędzy"** → α·max + (1−α)·min, kręcisz pokrętłem optymizmu
- **Savage = „szał żalu → min max żalu"** → macierz żalu → minimalizuj maksymalny żal (trzymaj żal na smyczy)

