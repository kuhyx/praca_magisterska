## PYTANIE 17: Szeregowanie zadań

**Cechy klasyfikacji. Przykładowa metoda.**

---

### Tło pojęciowe — słowniczek

**Szeregowanie zadań (scheduling)** — przydzielanie zadań do maszyn (procesorów, linii produkcyjnych) w czasie, tak aby zoptymalizować wybrane kryterium (np. minimalizacja czasu ukończenia, minimalizacja opóźnień). Fundamentalny problem badań operacyjnych i systemów operacyjnych.

    Mam 5 zadań i 2 maszyny. Które zadanie na którą maszynę? W jakiej kolejności?
    Cel: ukończyć wszystko najszybciej.

---

**Notacja Grahama (α | β | γ)** — standardowy sposób opisu problemu szeregowania w trzech polach:

**α — środowisko maszynowe:** ile i jakie maszyny?
- **1** — jedna maszyna
- **Pm** — m identycznych maszyn równoległych
- **F** (flow shop) — zadania „płyną" przez maszyny w tej samej kolejności (jak taśma montażowa)
- **J** (job shop) — każde zadanie ma indywidualną trasę przez maszyny (elastyczniejsze, trudniejsze)

**β — charakterystyki zadań:** jakie ograniczenia?
- **rⱼ** (release dates) — zadanie j dostępne dopiero w czasie rⱼ
- **dⱼ** (due dates) — termin, do którego zadanie j powinno być ukończone
- **pmtn** (preemption) — można przerwać zadanie i wrócić później
- **prec** (precedencje) — zadanie A musi skończyć się przed B

**γ — kryterium optymalizacji:** co minimalizujemy?
- **Cmax (makespan)** — czas ukończenia OSTATNIEGO zadania. Minimalizacja → najszybsze „zrobienie wszystkiego".
- **ΣCⱼ** — suma czasów ukończenia. Minimalizacja → minimalizacja średniego czasu.
- **Lmax** — maksymalne opóźnienie (max(Cⱼ - dⱼ)). Minimalizacja → żadne zadanie nie jest „bardzo" spóźnione.
- **ΣTⱼ** — suma spóźnień (Tⱼ = max(0, Cⱼ - dⱼ)).
- **ΣUⱼ** — liczba spóźnionych zadań (Uⱼ = 1 jeśli Cⱼ > dⱼ, 0 w.p.p.).

    Przykład zapisu: 1 || ΣCⱼ
    Znaczenie: 1 maszyna, brak ograniczeń, minimalizuj sumę czasów ukończenia

---

**SPT (Shortest Processing Time)** — reguła: wykonuj najkrótsze zadanie najpierw. Optymalna dla problemu 1 || ΣCⱼ.

    Dlaczego SPT jest optymalne? Bo krótkie zadania „nie blokują" długich.
    Zadania: 5, 3, 8, 2, 6
    SPT → 2, 3, 5, 6, 8
    Czasy ukończenia: 2, 5, 10, 16, 24
    ΣCⱼ = 57

    Gdyby odwrotnie (LPT): 8, 6, 5, 3, 2
    Czasy ukończenia: 8, 14, 19, 22, 24
    ΣCⱼ = 87 (gorsze!)

**EDD (Earliest Due Date)** — reguła: wykonuj najpierw zadanie z najwcześniejszym terminem (deadline). Optymalna dla 1 || Lmax.

**Algorytm Johnsona** — optymalny dla flow shopu z 2 maszynami (F2 || Cmax). Algorytm:
1. Jeśli min czas jest na maszynie 1 → zadanie na początek
2. Jeśli min czas jest na maszynie 2 → zadanie na koniec

---

**Makespan (Cmax)** — czas od startu do zakończenia OSTATNIEGO zadania. „Jak długo trwa cały projekt?"

**Flow shop** — każde zadanie przechodzi przez te same maszyny w tej samej kolejności (M1 → M2 → M3). Jak linia montażowa w fabryce: każdy samochód przechodzi spawanie → malowanie → montaż.

**Job shop** — każde zadanie ma indywidualną trasę (J1: M2→M1→M3; J2: M1→M3→M2). Bardziej elastyczny, ale problem szeregowania jest znacznie trudniejszy (NP-trudny już dla 3 maszyn!).

**Preemption (wywłaszczanie)** — możliwość przerwania zadania w trakcie i dokończenia go później. Bez preemption (non-preemptive): raz rozpoczęte zadanie musi się skończyć.

**Precedencje (precedence constraints)** — ograniczenia kolejności: zadanie A musi skończyć się zanim B może się zacząć. Modelowane jako DAG (Directed Acyclic Graph).

**NP-trudny** — klasa problemów bez znanego algorytmu wielomianowego. Job shop scheduling jest NP-trudny nawet dla 3 maszyn. Pm||Cmax jest NP-trudny dla m≥2. W praktyce: heurystyki, metaheurystyki (genetic algorithms, simulated annealing), programming math.

---

### Część 1 — Cechy klasyfikacji problemów szeregowania

Problemy szeregowania klasyfikuje się za pomocą **notacji Grahama α | β | γ** (trzy pola opisujące problem) oraz ortogonalnych cech dodatkowych.

#### Notacja Grahama: **α | β | γ**

**α — środowisko maszynowe** (ile i jakie maszyny):

| Symbol | Nazwa | Opis |
|--------|-------|------|
| **1** | jedna maszyna | najprostsze problemy |
| **Pm** | identyczne równoległe | m maszyn, ten sam czas pⱼ na każdej |
| **Qm** | jednorodne (uniform) | maszyna i ma prędkość sᵢ; czas = pⱼ/sᵢ |
| **Rm** | niespokrewnione (unrelated) | czas pᵢⱼ zależy od pary (zadanie, maszyna) |
| **Fm** | flow shop | wszystkie zadania w tej samej kolejności maszyn |
| **Jm** | job shop | każde zadanie ma indywidualną trasę |
| **Om** | open shop | kolejność maszyn dowolna per zadanie |

    Flow shop: każde zadanie → M1 → M2 → M3  (ta sama kolejność)
    Job shop:  J1 → M2→M1→M3;  J2 → M1→M3→M2  (indywidualne trasy)
    Open shop: dowolna permutacja maszyn per zadanie

**β — charakterystyki zadań** (ograniczenia i cechy):

| Symbol | Nazwa | Znaczenie |
|--------|-------|-----------|
| **rⱼ** | release dates | zadanie j dostępne od czasu rⱼ |
| **dⱼ** | due dates | termin ukończenia (soft — opóźnienie jest kosztem) |
| **d̄ⱼ** | deadlines | termin bezwzględny (hard — musi być dotrzymany) |
| **pmtn** | preemption | można przerwać i wznowić zadanie |
| **prec** | precedencje | DAG zależności: A musi się skończyć przed B |
| **pⱼ=1** | unit processing | wszystkie zadania mają czas = 1 |
| **sⱼₖ** | setup times | czas przezbrojenia między zadaniami j i k |

**γ — kryterium optymalizacji** (co minimalizujemy):

| Kryterium | Wzór | Interpretacja |
|-----------|------|---------------|
| **Cmax** | max(Cⱼ) | makespan — czas ukończenia WSZYSTKIEGO |
| **ΣCⱼ** | Σ Cⱼ | suma czasów ukończenia (~ średni czas) |
| **ΣwⱼCⱼ** | Σ wⱼCⱼ | ważona suma (priorytety zadań) |
| **Lmax** | max(Cⱼ - dⱼ) | maksymalne opóźnienie |
| **ΣTⱼ** | Σ max(0, Cⱼ-dⱼ) | suma spóźnień |
| **ΣUⱼ** | Σ 𝟙(Cⱼ>dⱼ) | liczba spóźnionych zadań |

    Przykład zapisu: F2 || Cmax
    Znaczenie: flow shop, 2 maszyny, brak ograniczeń na zadania, minimalizuj makespan

#### Cechy dodatkowe (ortogonalne do α|β|γ)

| Cecha | Warianty | Wpływ |
|-------|----------|-------|
| **Determinizm** | deterministyczne vs stochastyczne | czy czasy pⱼ są znane z góry czy losowe? |
| **Dynamika** | statyczne vs dynamiczne | czy wszystkie zadania znane na starcie? |
| **Wywłaszczanie** | preemptive vs non-preemptive | czy można przerwać zadanie? |
| **Online/offline** | online vs offline | czy decyzje podejmowane bez wiedzy o przyszłości? |

#### Złożoność obliczeniowa

| Problem | Złożoność | Metoda rozwiązania |
|---------|-----------|-------------------|
| 1 \|\| ΣCⱼ | **O(n log n)** | SPT — sortowanie |
| 1 \|\| Lmax | **O(n log n)** | EDD — sortowanie |
| F2 \|\| Cmax | **O(n log n)** | Algorytm Johnsona |
| Pm \|\| Cmax (m≥2) | **NP-trudny** | heurystyki (LPT), metaheurystyki |
| Jm \|\| Cmax (m≥3) | **silnie NP-trudny** | branch & bound, GA, symulowane wyżarzanie |

---

### Część 2 — Przykładowa metoda: Algorytm Johnsona (F2 || Cmax)

#### Problem

Flow shop z **2 maszynami** (M1, M2), **n zadań**. Każde zadanie musi najpierw przejść przez M1 (czas aⱼ), potem M2 (czas bⱼ). Kolejność zadań na obu maszynach **taka sama** (permutacyjny flow shop). Cel: minimalizacja **Cmax** (makespanu).

#### Algorytm (Selmer Johnson, 1954)

1. Dla każdego zadania j wyznacz min(aⱼ, bⱼ).
2. Jeśli minimum jest na M1 (aⱼ ≤ bⱼ) → zadanie na **POCZĄTEK** kolejki (od lewej).
3. Jeśli minimum jest na M2 (bⱼ < aⱼ) → zadanie na **KONIEC** kolejki (od prawej).
4. W obrębie grupy „na początek" — rosnąco wg aⱼ; „na koniec" — malejąco wg bⱼ.

#### Przykład liczbowy

5 zadań z czasami:

    Zadanie:  J1   J2   J3   J4   J5
    M1 (aⱼ):  4    2    6    1    3
    M2 (bⱼ):  5    3    2    7    4

**Krok 1 — Znajdź minima i przydziel:**

    J1: min(4,5) = 4 na M1 → POCZĄTEK
    J2: min(2,3) = 2 na M1 → POCZĄTEK
    J3: min(6,2) = 2 na M2 → KONIEC
    J4: min(1,7) = 1 na M1 → POCZĄTEK
    J5: min(3,4) = 3 na M1 → POCZĄTEK

**Krok 2 — Posortuj w grupach:**

    POCZĄTEK (rosnąco wg aⱼ): J4(1), J2(2), J5(3), J1(4)
    KONIEC (malejąco wg bⱼ):  J3(2)

**Optymalna kolejność: J4 → J2 → J5 → J1 → J3**

**Krok 3 — Oblicz czasy (diagram Gantta):**

    M1: |J4:1|J2:2 |J5:3  |J1:4   |J3:6       |
    t:  0   1    3     6      10       16

    M2:      |J4:7      |J2:3|J5:4   |J1:5      |J3:2|
    t:  0   1          8   11     15       20   22

    Szczegółowe obliczenie:
    J4: M1=[0,1],   M2=[1,8]     (start M2 = max(1, 0) = 1)
    J2: M1=[1,3],   M2=[8,11]    (start M2 = max(3, 8) = 8)
    J5: M1=[3,6],   M2=[11,15]   (start M2 = max(6, 11) = 11)
    J1: M1=[6,10],  M2=[15,20]   (start M2 = max(10, 15) = 15)
    J3: M1=[10,16], M2=[20,22]   (start M2 = max(16, 20) = 20)

    Cmax = 22

**Dlaczego optymalny?** Johnson udowodnił (1954), że zamiana dowolnych dwóch sąsiednich zadań w tej kolejności nie zmniejszy Cmax. Algorytm minimalizuje „idle time" na M2 — krótkie zadania na M1 na początku szybko „karmią" M2, a krótkie na M2 na końcu kończą się szybko po M1.

#### Klasyczne reguły optymalne (inne metody)

| Reguła | Problem | Opis | Złożoność |
|--------|---------|------|-----------|
| **SPT** | 1 \|\| ΣCⱼ | najkrótsze najpierw | O(n log n) |
| **WSPT** | 1 \|\| ΣwⱼCⱼ | sortuj wg pⱼ/wⱼ rosnąco | O(n log n) |
| **EDD** | 1 \|\| Lmax | najwcześniejszy termin | O(n log n) |
| **Johnson** | F2 \|\| Cmax | algorytm powyżej | O(n log n) |

#### Przykład SPT: 1 || ΣCⱼ

    Zadania: J1(5), J2(3), J3(8), J4(2), J5(6)
    SPT → J4(2), J2(3), J1(5), J5(6), J3(8)
    Czasy ukończenia:  2,  5,  10,  16,  24
    ΣCⱼ = 2+5+10+16+24 = 57  ← OPTYMALNE

    Gdyby LPT (odwrotnie): J3(8), J5(6), J1(5), J2(3), J4(2)
    Czasy ukończenia:         8,  14,  19,  22,  24
    ΣCⱼ = 8+14+19+22+24 = 87  ← 53% gorsze!

    Dowód optymalności SPT: zamiana sąsiednich i,j gdzie pᵢ > pⱼ
    zwiększa ΣCⱼ o (n-k)(pᵢ - pⱼ) > 0. Więc SPT = minimum.

### Etymologia

**Notacja Grahama** — Ronald Graham (Bell Labs, 1966–1979); znany też z liczby Grahama. **SPT** — Shortest Processing Time. **EDD** — Earliest Due Date. **Johnson** — Selmer Johnson (RAND, 1954). **Makespan** — „make" (ukończyć) + „span" (rozpiętość); czas od startu do końca wszystkich zadań. **Flow shop** — zadania „płyną" przez maszyny w tej samej kolejności (jak taśma). **Job shop** — każde zadanie ma indywidualną trasę. **NP-trudny** — Non-deterministic Polynomial-time hard.

### Diagramy — wizualizacja

**Notacja Grahama α|β|γ — mapa mnemoniczna z wszystkimi parametrami:**

![Notacja Grahama α|β|γ — mapa mnemoniczna](img/scheduling_graham_notation.png)

**Flow shop vs Job shop — wizualne porównanie:**

![Flow shop vs Job shop — porównanie](img/scheduling_flow_vs_job.png)

**Algorytm Johnsona — tabela decyzyjna + diagram Gantta:**

![Algorytm Johnsona — Gantt](img/scheduling_johnson_gantt.png)

**SPT vs LPT — porównanie na przykładzie 1 || ΣCⱼ:**

![SPT vs LPT porównanie](img/scheduling_spt_comparison.png)

**EDD — przykład 1 || Lmax z terminami:**

![EDD — Earliest Due Date przykład](img/scheduling_edd_example.png)

**Złożoność problemów szeregowania — od łatwych do NP-trudnych:**

![Złożoność problemów szeregowania](img/scheduling_complexity_map.png)

---

### Przykład EDD: 1 || Lmax (krok po kroku)

    Zadania: J1(p=4,d=10), J2(p=2,d=6), J3(p=6,d=15), J4(p=3,d=8), J5(p=5,d=18)
    EDD → sortuj wg due date (dⱼ): J2(d=6), J4(d=8), J1(d=10), J3(d=15), J5(d=18)

    Kolejność: J2 → J4 → J1 → J3 → J5
    J2: C₂ = 2,  L₂ = 2-6  = -4  (wcześniej = OK)
    J4: C₄ = 5,  L₄ = 5-8  = -3  (wcześniej = OK)
    J1: C₁ = 9,  L₁ = 9-10 = -1  (wcześniej = OK)
    J3: C₃ = 15, L₃ = 15-15 = 0  (na czas = OK)
    J5: C₅ = 20, L₅ = 20-18 = +2 (spóźniony!)

    Lmax = max(-4, -3, -1, 0, 2) = 2  ← OPTYMALNE

    Gdyby inna kolejność (np. J1→J2→J3→J4→J5):
    C₁=4(L=-6), C₂=6(L=0), C₃=12(L=-3), C₄=15(L=+7), C₅=20(L=+2)
    Lmax = 7 — GORSZE! (3.5× gorsze)

### Przykład WSPT: 1 || ΣwⱼCⱼ (ważona suma)

    Zadania z wagami (priorytetami):
    J1(p=6, w=3), J2(p=2, w=5), J3(p=8, w=1), J4(p=4, w=4)

    WSPT: sortuj wg pⱼ/wⱼ ROSNĄCO (im niższy stosunek, tym ważniejszy):
    J2: 2/5 = 0.4  ← pierwszy!
    J4: 4/4 = 1.0
    J1: 6/3 = 2.0
    J3: 8/1 = 8.0  ← ostatni

    Kolejność: J2 → J4 → J1 → J3
    C₂=2, C₄=6, C₁=12, C₃=20
    ΣwⱼCⱼ = 5·2 + 4·6 + 3·12 + 1·20 = 10+24+36+20 = 90 ← OPTYMALNE

    Intuicja: „wysoki priorytet + krótkie = rób NATYCHMIAST"

---

### Jak zapamiętać

#### MEGA-MNEMONIK: „α|β|γ = MASZYNY | OGRANICZENIA | CEL"

    Pytanie kluczowe:
    α → „ILE maszyn i JAKIE?"
    β → „CO ogranicza zadania?"
    γ → „CO chcę zminimalizować?"

#### α — Maszyny: „Jeden Prawdziwy Quasi-Rycerz Forsuje Jaskinię Orków"

    1  = Jedna maszyna (najprostsze)
    Pm = Prawdziwy parallel (identyczne)
    Qm = Quasi-uniform (różne prędkości)
    Rm = Rycerz Random/unRelated (każda para ma inny czas)
    Fm = Forsuje Flow shop (ta sama kolejność — taśma montażowa)
    Jm = Jaskinię Job shop (indywidualne trasy — labirynt)
    Om = Orków Open shop (dowolna kolejność)

    Mnemotechnika wzrokowa:
    1 = jeden samotny wojownik
    P = Pluton identycznych żołnierzy
    Q = Quasi — różne prędkości jak różne klasy postaci
    R = Random — losowe powiązania
    F = Fabryka — taśma montażowa, każdy przez te same stacje
    J = Jaskinia — każdy szuka własnej drogi
    O = Open world — idź gdzie chcesz

#### β — Ograniczenia: „Robak Daje Deadline'y: Przerwy Poprzedzają Pojedyncze Setup'y"

    rⱼ  = Release dates — Robak: zadanie j NIE ISTNIEJE przed czasem rⱼ
    dⱼ  = Due dates — Daje: miękki termin (kara za spóźnienie, ale można się spóźnić)
    d̄ⱼ  = Deadlines — Deadline: TWARDY termin (nie wolno przekroczyć!)
    pmtn = Preemption — Przerwy: można PRZERWAĆ zadanie (jak pauza w grze)
    prec = Precedencje — Poprzedzają: A→B, trzeba skończyć A przed B (DAG)
    pⱼ=1 = Unit time — Pojedyncze: wszystkie zadania trwają dokładnie 1
    sⱼₖ  = Setup times — Setup'y: przezbrojenie maszyny MIĘDZY zadaniami

    Dwa "d" — łatwo pomylić:
    dⱼ  = Due date = miękki termin → KARA za spóźnienie (ale życie trwa)
    d̄ⱼ  = Deadline z kreską = ABSOLUTNY termin → NIE WOLNO przekroczyć

#### γ — Kryterium: „Ciężki Sum Ważony Lata, Tardiness Uderza"

    Cmax   = Ciężki makespan — „jak długo trwa WSZYSTKO?" max(Cⱼ)
    ΣCⱼ    = Sum ukończeń — „średni czas oczekiwania" → SPT
    ΣwⱼCⱼ  = Ważony sum — „z priorytetami" → WSPT (pⱼ/wⱼ rosnąco)
    Lmax   = Lata max opóźnienie — „najgorszy delikwent" → EDD
    ΣTⱼ    = Tardiness sum — „łączne spóźnienia" (liczy się tylko > 0)
    ΣUⱼ    = Uderza count — „ile zadań spóźnionych?" (0 lub 1 per zadanie)

    Różnica T vs L:
    Lⱼ = Cⱼ - dⱼ  (może być ujemne = wcześniej)
    Tⱼ = max(0, Lⱼ) (obcięte — liczy się TYLKO spóźnienie)

#### Metody — „SPT EDD Johnson WSPT"

    SPT  = „Short People To the front" → 1 || ΣCⱼ
           Krótkie najpierw, jak niskie osoby w zdjęciu klasowym
           Bo krótkie zadania NIE BLOKUJĄ długich

    EDD  = „Early Due? Do it first!" → 1 || Lmax
           Najpilniejszy termin idzie pierwszy

    WSPT = „Wealthy Short People first" → 1 || ΣwⱼCⱼ
           Sortuj wg pⱼ/wⱼ rosnąco (ważne+krótkie pierwsze)

    Johnson = „Krótki na M1 → START, Krótki na M2 → STOP" → F2 || Cmax
              M1 minimum → na Początek (M1 = Pierwszy!)
              M2 minimum → na Koniec (M2 = End!)
              Intuicja: szybkie starty karmią M2, szybkie końce zamykają robotę

#### Złożoność — „Jedna maszyna = łatwo, dodaj drugą = katastrofa"

    1 maszyna → prawie zawsze wielomianowe (sortuj!)
    ≥2 maszyny równoległe → NP-trudne (Pm||Cmax)
    Flow shop 2 maszyny → Johnson O(n log n) (wyjątek!)
    Flow shop ≥3 maszyny → NP-trudne
    Job shop ≥3 maszyny → silnie NP-trudne

    Mnemonik: „1 = sortuj, 2+ = cierp"

#### Quick-fire pytanie → odpowiedź

    „Minimalizuj średni czas?" → γ = ΣCⱼ, metoda SPT
    „Minimalizuj max opóźnienie?" → γ = Lmax, metoda EDD
    „Flow shop 2 maszyny?" → Johnson
    „Z priorytetami?" → WSPT (pⱼ/wⱼ rosnąco)
    „Ile spóźnionych zadań?" → γ = ΣUⱼ (zliczanie, NP-trudne!)

