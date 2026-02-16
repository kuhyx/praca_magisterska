## PYTANIE 32: Dominacja stochastyczna

**FSD i SSD. Jak mogą być użyte w modelach wyboru?**

---

### Tło pojęciowe — słowniczek

**Rozkład (distribution)** — opis WSZYSTKICH możliwych wartości, jakie może przyjąć zmienna losowa, wraz z informacją jak prawdopodobne jest każda z nich. To „mapa" losowości — mówi nam: „co może się zdarzyć i z jakim prawdopodobieństwem".

    Rzut kostką — rozkład dyskretny:
    Wartość:          1     2     3     4     5     6
    Prawdopodobieństwo: 1/6   1/6   1/6   1/6   1/6   1/6

    Wzrost ludzi — rozkład ciągły (normalny):
    Średnia μ = 175 cm, odchylenie σ = 7 cm
    → większość ludzi 168–182 cm, mało kto >195 cm

**Prawdopodobieństwo (probability)** — liczba z przedziału [0, 1] wyrażająca szansę zajścia zdarzenia. P=0 → niemożliwe, P=1 → pewne, P=0.5 → „rzut monetą".

    P(orzeł) = 0.5 = 50%
    P(6 na kostce) = 1/6 ≈ 0.167 = 16.7%
    P(deszcz jutro) = 0.3 = 30%   ← subiektywne, ale nadal p ∈ [0,1]

**Rozkład prawdopodobieństwa (probability distribution)** — kompletny opis zmiennej losowej: jakie wartości może przyjąć + jakie jest prawdopodobieństwo każdej z nich. Dwa sposoby opisu:

    1. PDF (gęstość) — dla rozkładów ciągłych: f(x), pole pod krzywą = prawdopodobieństwo
    2. CDF (dystrybuanta) — F(x) = P(X ≤ x), rośnie od 0 do 1

    Przykład: inwestycja A ma rozkład zwrotów:
    -10% z p=0.2,  +5% z p=0.5,  +15% z p=0.3
    → To jest rozkład prawdopodobieństwa inwestycji A

---

**Decydent (decision maker)** — osoba lub podmiot, który MUSI wybrać jedną z dostępnych alternatyw. W praktyce: inwestor wybierający portfel, menedżer wybierający projekt, pacjent wybierający leczenie. Kluczowe: decydent ma PREFERENCJE (np. boi się ryzyka lub je lubi), których my nie znamy dokładnie.

**Funkcja użyteczności U(x) (utility function)** — matematyczna funkcja przypisująca każdemu wynikowi $x$ (np. kwocie pieniędzy) liczbę $U(x)$ odzwierciedlającą SUBIEKTYWNĄ wartość tego wyniku dla decydenta. Wyższa U(x) = lepiej. Kluczowe: kształt U(x) koduje stosunek do ryzyka.

    U(x) = √x  (typowa risk-averse):
    U(0) = 0,  U(100) = 10,  U(400) = 20,  U(900) = 30

    Osoba A (risk-averse):  U(x) = √x    → wklęsła ∩
    Osoba B (risk-neutral): U(x) = x     → liniowa /
    Osoba C (risk-seeking): U(x) = x²    → wypukła ∪

    U(x)
    │    ╭── risk-averse (√x) — wolni wzrost, „nasycenie"
    │  ╱─── risk-neutral (x)  — stały wzrost
    │╱ ╱─── risk-seeking (x²) — przyspieszający wzrost
    └──────── x

**Dokładna funkcja użyteczności decydenta** — w idealnym świecie znalibyśmy DOKŁADNY wzór U(x) konkretnego decydenta (np. U(x) = ln(x+1) z parametrami). Wtedy wystarczy policzyć E[U(A)] i E[U(B)] i wybrać wyższe. Problem: w praktyce NIGDY nie znamy dokładnej U(x) — ludzie nie potrafią podać precyzyjnego wzoru swoich preferencji. Dlatego dominacja stochastyczna jest tak cenna — działa BEZ znajomości dokładnej U!

---

**Metoda (method)** — sformalizowany algorytm prowadzący od danych do wyniku. W tym kontekście: algorytm porównywania dwóch alternatyw (inwestycji, portfeli, decyzji).

**Metoda porównywania rozkładów (method of comparing distributions)** — sposób na odpowiedź „czy rozkład A jest lepszy od B?". Proste metody porównują JEDNĄ liczbę (np. średnią E[X] lub wariancję Var[X]) — ale to za mało, bo gubią informację o kształcie rozkładu. Dominacja stochastyczna porównuje CAŁY kształt dystrybuanty — dlatego daje silniejsze wnioski.

    Porównanie po średniej: E[A]=10%, E[B]=8% → A lepsza? Ale może A ma ogromny rozrzut!
    Porównanie po wariancji: Var[A]<Var[B] → A bezpieczniejsza? Ale może E[A] ≪ E[B]!
    Dominacja stochastyczna: porównuje CAŁY rozkład → wniosek jest uniwersalny

---

**Dominacja (dominance)** — relacja „A jest co najmniej tak dobre jak B" (a w pewnych aspektach lepsze). Pochodzi od łac. „dominari" = panować. Gdy A dominuje B, to A „panuje" nad B — nie ma powodu, żeby wybrać B. W teorii decyzji dominacja oznacza: ŻADEN racjonalny decydent (z danej klasy) nie wybrałby B, skoro A jest dostępne.

**Stochastyczna (stochastic)** — znaczy „losowa, probabilistyczna" (grec. „stochastos" = zdolny do celowania/zgadywania). Mówmy „stochastyczna" zamiast „losowa" w kontekście formalnym. Dominacja stochastyczna = dominacja między rozkładami losowymi (a nie między pojedynczymi liczbami).

    Dominacja „zwykła" (deterministyczna): A=100, B=80 → A > B (oczywiste)
    Dominacja stochastyczna: A ~ N(10%, 15%), B ~ N(8%, 20%) → A > B?
    → Nie jest oczywiste! Trzeba porównać CAŁE rozkłady, nie tylko średnie.

**Co znaczy „rozkład A dominuje rozkład B"?** — że dla KAŻDEGO racjonalnego decydenta (z odpowiedniej klasy) oczekiwana użyteczność z A jest ≥ niż z B:

    A ≥ B  ⟺  E[U(A)] ≥ E[U(B)]  dla KAŻDEGO U z danej klasy

    Nie muszę znać Twojej dokładnej U(x).
    Wystarczy, że wiem DO JAKIEJ KLASY należysz:
    - FSD: klasa U' ≥ 0 (preferujesz więcej) → WSZYSCY racjonalni
    - SSD: klasa U' ≥ 0, U'' ≤ 0 (więcej + mniej ryzyka) → risk-averse

---

**Klasa decydentów (class of decision makers)** — zbiór WSZYSTKICH decydentów, których funkcje użyteczności spełniają pewne warunki. To nie jest grupa konkretnych osób — to matematyczny zbiór WSZYSTKICH MOŻLIWYCH funkcji U(x) z danymi własnościami.

**Racjonalny decydent (rational decision maker)** — decydent, którego preferencje są SPÓJNE (np. jeśli woli A od B i B od C, to woli A od C) i który preferuje więcej niż mniej ($U'(x) \geq 0$ — monotoniczność). To minimalne założenie — prawie każdy człowiek je spełnia.

**Klasa racjonalnych decydentów** — zbiór WSZYSTKICH funkcji U(x) takich, że $U'(x) \geq 0$. Jest ich NIESKOŃCZENIE wiele (√x, ln(x), x, x², 2x+7, ...). FSD mówi: jeśli A dominuje B, to DLA KAŻDEJ z tych nieskończenie wielu funkcji E[U(A)] ≥ E[U(B)]. Dlatego dominacja jest tak silnym twierdzeniem!

**Dlaczego cała klasa wybierze A?** — Twierdzenie (Hardy-Littlewood-Polya): A ≥_FSD B ⟺ E[U(A)] ≥ E[U(B)] dla KAŻDEGO monotonicznie rosnącego U. To nie jest opinia — to dowiedzione matematyczne twierdzenie. Jeśli dystrybuanta A leży pod B, to nie istnieje żadna rosnąca funkcja U, dla której B byłoby lepsze.

---

**U(x) — notacja** — $U$ to nazwa funkcji (od ang. „utility" = użyteczność), $x$ to argument (wynik, np. kwota pieniędzy). $U(x)$ to wartość użyteczności wyniku $x$ dla danego decydenta.

    U(x) = √x
    U(100) = √100 = 10   ← „100 zł daje mi 10 jednostek użyteczności"
    U(400) = √400 = 20   ← „400 zł daje 20 — tylko 2× więcej, choć to 4× pieniędzy"

**Dlaczego „preferujesz więcej" = FSD?** — FSD wymaga TYLKO $U'(x) \geq 0$, czyli że funkcja użyteczności jest niemalejąca. To jedyne założenie: „wolisz 101 zł niż 100 zł". Nie mówi NIC o ryzyku — to mogą być osoby kochające ryzyko, neutralne, czy z awersją. Dlatego FSD to najszersza klasa: WSZYSCY, którzy wolą „więcej".

**Dlaczego „mniej ryzyka" = SSD?** — SSD dodaje warunek $U''(x) \leq 0$ (wklęsłość). To oznacza malejącą użyteczność krańcową: „każda kolejna złotówka daje mi coraz mniej radości". Konsekwencja: taki decydent PREFERUJE pewność od loterii o tej samej średniej → jest risk-averse. Dlatego SSD obejmuje węższą klasę: tylko tych, co preferują więcej I mniej ryzyka.

    FSD: U'≥0              → „więcej = lepiej" (szeroka klasa, wszyscy racjonalni)
    SSD: U'≥0 i U''≤0      → „więcej = lepiej" + „ryzyko = złe" (węższa, risk-averse)

    FSD: {√x, ln(x), x, x², 2x+7, ...}     ← KAŻDA rosnąca U
    SSD: {√x, ln(x), ...}                    ← tylko wklęsłe rosnące U (bez x²!)

**Co znaczy A > B (A dominuje B)?** — formalnie: „A jest co najmniej tak dobre jak B dla KAŻDEGO decydenta z danej klasy, i ŚCIŚLE lepsze dla co najmniej jednego". Praktyczne znaczenie: jeśli masz do wyboru A i B, i A dominuje B, to B jest IRRACJONALNE — nie ma żadnego powodu, by je wybrać. Można je bezpiecznie wyeliminować z rozważań.

    A ≥_FSD B znaczy:
    ∀ U : U'≥0 → E[U(A)] ≥ E[U(B)]
    „Każdy kto woli więcej, wybierze A (lub jest mu obojętnie)"

    A ≥_SSD B znaczy:
    ∀ U : U'≥0, U''≤0 → E[U(A)] ≥ E[U(B)]
    „Każdy risk-averse wybierze A (lub jest mu obojętnie)"

---

**Dystrybuanta F(x) (CDF — Cumulative Distribution Function)** — prawdopodobieństwo, że zmienna losowa X przyjmie wartość ≤ x. F(x) = P(X ≤ x). Rośnie od 0 do 1.

    Przykład: rzut kostką
    F(1) = 1/6,  F(2) = 2/6,  F(3) = 3/6,  F(4) = 4/6,  F(5) = 5/6,  F(6) = 1

    Graficznie (ciągły rozkład):
    F(x)
    1 ┤            ──────────
      │          ╱
      │        ╱
      │      ╱
    0 ┤────╱
      └─────────────────── x

**Dlaczego dystrybuanta?** Dominacja stochastyczna porównuje KSZTAŁT dystrybuant, nie pojedyncze liczby jak średnia czy wariancja. To daje silniejsze wnioski.

---

**FSD (First-order Stochastic Dominance, dominacja stochastyczna I rzędu)** — A dominuje B w sensie FSD, gdy dystrybuanta A leży ZAWSZE poniżej (lub jest równa) dystrybuancie B:

    F_A(x) ≤ F_B(x)  dla każdego x

Intuicja: „Dla DOWOLNEGO progu x, szansa, że A daje wynik ≤ x jest mniejsza lub równa niż dla B." A daje zawsze co najmniej tyle samo „dobrych wyników".

    F(x)
    1 ┤         ╱── B (gorsza — wyższa CDF)
      │       ╱╱── A (lepsza — niższa CDF)
      │     ╱╱
      │   ╱╱
    0 ┤──╱╱
      └──────────── x
    A ≥_FSD B: F_A zawsze pod F_B

**Warunek na klasę U:** U'(x) ≥ 0 — monotoniczność, czyli „więcej = lepiej". WSZYSCY racjonalni (nienasyceni) decydenci wybiorą A.

Przykład liczbowy:

    Inwestycja A: wynik = {20, 30, 40} każdy z p=1/3
    Inwestycja B: wynik = {10, 30, 40} każdy z p=1/3

    F_A(10)=0, F_B(10)=1/3 → F_A ≤ F_B ✓
    F_A(20)=1/3, F_B(20)=1/3 → F_A ≤ F_B ✓
    F_A(30)=2/3, F_B(30)=2/3 → F_A ≤ F_B ✓
    A ≥_FSD B → każdy racjonalny wybierze A

**FSD jest rzadka w praktyce** — wystarczy JEDEN punkt, w którym F_A(x) > F_B(x), i dominacja nie zachodzi.

---

**SSD (Second-order Stochastic Dominance, dominacja II rzędu)** — A dominuje B w sensie SSD, gdy skumulowana całka z dystrybuanty A jest ≤ niż z B:

    ∫_{-∞}^{x} F_A(t)dt  ≤  ∫_{-∞}^{x} F_B(t)dt   dla każdego x

Dystrybuanty MOGĄ się przecinać (A nie musi być wszędzie lepsza), ale „pole pod F_A" jest zawsze mniejsze lub równe.

**Warunek na klasę U:** U'(x) ≥ 0 i U''(x) ≤ 0 — monotoniczność + wklęsłość = **risk-averse** decydenci.

    F(x)                    ∫F(x)dx
    1 ┤    ╱B               │     ╱B (większe pole)
      │  ╱X╱                │   ╱╱
      │╱╱A                  │  ╱╱A (mniejsze pole)
    0 ┤                     │╱
      └───── x              └───── x
    CDF mogą się krzyżować! Ale skumulowane pole A ≤ B → A ≥_SSD B

---

**Relacja między FSD a SSD:**

    FSD ⟹ SSD ⟹ TSD ⟹ ...  (ale NIE odwrotnie!)

Jeśli A dominuje B w sensie FSD, to automatycznie dominuje w SSD. Ale SSD może zachodzić nawet gdy FSD nie — bo SSD „przebacza" chwilowe przekroczenia F_A nad F_B, jeśli kompensowane gdzie indziej.

---

**Mean-Preserving Spread (MPS)** — operacja, która zwiększa rozrzut (wariancję) rozkładu, zachowując tę samą średnią. B = A + ε, gdzie E[ε|A]=0.

    A: zawsze 50 zł                    → E[A] = 50, Var = 0
    B: 50% szans na 20 zł, 50% na 80 zł → E[B] = 50, Var = 900
    B jest MPS wobec A: ta sama średnia, większy rozrzut
    → A ≥_SSD B (risk-averse wolą A!)

**Kluczowe twierdzenie Rothschilda-Stiglitza:** A SSD-dominuje B ⟺ B jest mean-preserving spread A (przy jednakowej średniej).

---

**Funkcja wklęsła (concave)** — „krzywa w dół", U''(x) ≤ 0. Każdy dodatkowy złotówka daje coraz mniej użyteczności (malejąca użyteczność krańcowa). Modeluje risk aversion.

    U(x) = √x → U(0)=0, U(100)=10, U(400)=20
    Różnica 0→100: +10 użyteczności
    Różnica 100→400: +10 użyteczności  (mimo 3× więcej pieniędzy!)

**Funkcja wypukła (convex)** — „krzywa w górę", U''(x) ≥ 0. Modeluje risk seeking.

---

**Portfolio selection (wybór portfela)** — zastosowanie dominacji: porównaj rozkłady zwrotów portfeli. Eliminuj zdominowane stochastycznie portfele BEZ znania dokładnej U inwestora.

    Portfel A: N(10%, 15%)  (średnia 10%, odch. std. 15%)
    Portfel B: N(8%, 20%)   (średnia 8%, odch. std. 20%)
    E[A] > E[B] i σ[A] < σ[B] → A SSD B
    Każdy risk-averse inwestor wybierze A.

---

### Idea: Porównaj rozkłady BEZ znajomości dokładnej U. Jeśli A dominuje B → KAŻDY (z danej klasy) wybierze A.

![FSD i SSD — porównanie dystrybuant](img/fsd_ssd_comparison.png)

### FSD (First-order Stochastic Dominance)

    A ≥_FSD B  ⟺  F_A(x) ≤ F_B(x) ∀x

- Warunek na U: U'(x) ≥ 0 (monotoniczność — „więcej = lepiej")
- Klasa: WSZYSCY racjonalni (nienasyceni)
- Interpretacja: A ma zawsze ≥ prawdopodobieństwo przekroczenia dowolnego progu
- **Rzadka** w praktyce

### SSD (Second-order Stochastic Dominance)

    A ≥_SSD B  ⟺  ∫_{-∞}^{x} F_A(t)dt ≤ ∫_{-∞}^{x} F_B(t)dt ∀x

- Warunek na U: U' ≥ 0 i U'' ≤ 0 (monotoniczne + wklęsłe)
- Klasa: **Risk-averse** (awersja do ryzyka)
- Dystrybuanty mogą się przecinać, ale skumulowane pole nie
- **Częstsza** niż FSD
- Mean-Preserving Spread: B = A + ε (E[ε|A]=0) → A SSD B

### Relacja: FSD ⟹ SSD ⟹ TSD... (ale nie odwrotnie)

### Jak FSD i SSD mogą być użyte w modelach wyboru?

**Odpowiedź abstrakcyjna:** Dominacja stochastyczna służy jako **kryterium eliminacji** — pozwala odrzucić zdominowane alternatywy z puli rozważanych opcji, BEZ konieczności znania dokładnej funkcji użyteczności decydenta. Zamiast pytać „jaki jest Twój dokładny wzór preferencji?", wystarczy wiedzieć, czy decydent jest racjonalny (FSD) lub ma awersję do ryzyka (SSD).

**Trzy sposoby użycia w modelach wyboru:**

**1. Filtracja zbioru efektywnego (Efficient Set Screening)**

W modelu wyboru portfela inwestor ma N portfeli. Zamiast analizować wszystkie N, eliminuj te zdominowane stochastycznie. TYLKO niezdominowane trafiają do dalszej analizy (np. optymalizacji Markowitza). To redukuje przestrzeń decyzyjną.

    Portfele: {A, B, C, D, E, F}
    FSD screening:  A ≥_FSD C,  D ≥_FSD F
    → Eliminuj C i F → Efficient set = {A, B, D, E}
    SSD screening:  A ≥_SSD B
    → Eliminuj B → Efficient set = {A, D, E}
    Inwestor wybiera spośród 3 zamiast 6 portfeli

**2. Ranking alternatyw bez znajomości U(x)**

Gdy znasz rozkłady zwrotów kilku inwestycji, możesz je CZĘŚCIOWO uszeregować:

    Inwestycja A: N(12%, 10%)   (średnia 12%, odch. std. 10%)
    Inwestycja B: N(12%, 15%)   (ta sama średnia, WIĘKSZY rozrzut)
    Inwestycja C: N(8%, 10%)    (niższa średnia, ten sam rozrzut)

    A ≥_SSD B:  Ta sama średnia, ale B to mean-preserving spread A
                → Każdy risk-averse woli A (mniej ryzyka, ten sam zwrot)
    A ≥_FSD C:  F_A(x) ≤ F_C(x) ∀x (bo A ma wyższą średnią, ten sam kształt)
                → KAŻDY racjonalny woli A (więcej w każdym scenariuszu)
    B vs C:     B ma wyższą średnię (12% vs 8%), ale większy rozrzut (15% vs 10%)
                → SSD może NIE zachodzić → zależy od konkretnej U(x) decydenta

    Ranking: A > B i A > C (pewne), ale B vs C → ZALEŻY OD DECYDENTA

**3. Kryterium fair ubezpieczenia (insurance decision)**

    Sytuacja: masz majątek 100 000 zł.
    Ryzyko: 10% szans na stratę 80 000 zł.
    Fair ubezpieczenie: składka = oczekiwana strata = 0.10 × 80 000 = 8 000 zł/rok

    BEZ ubezpieczenia: {100 000 z p=0.9,  20 000 z p=0.1}  → E=92 000
    Z ubezpieczeniem:  {92 000 z p=1.0}                      → E=92 000

    Ta sama średnia (92k), ale ubezpieczenie = PEWNOŚĆ.
    „Bez ubezpieczenia" to mean-preserving spread „z ubezpieczeniem"
    → „Z ubezpieczeniem" ≥_SSD „bez ubezpieczenia"
    → KAŻDY risk-averse kupi fair ubezpieczenie (nie musisz znać jego U!)

**Konkretny przykład obliczeniowy — FSD w wyborze portfela:**

    Portfel A: zwroty = {-5%, +10%, +15%} z prawdopodobieństwami {0.2, 0.5, 0.3}
    Portfel B: zwroty = {-10%, +10%, +15%} z prawdopodobieństwami {0.2, 0.5, 0.3}

    Dystrybuanty (CDF):
    x       F_A(x)    F_B(x)    F_A ≤ F_B?
    -10%    0.0       0.2       0.0 ≤ 0.2 ✓
    -5%     0.2       0.2       0.2 ≤ 0.2 ✓ (równe)
    +10%    0.7       0.7       0.7 ≤ 0.7 ✓ (równe)
    +15%    1.0       1.0       1.0 ≤ 1.0 ✓ (równe)

    F_A(x) ≤ F_B(x) ∀x, i F_A(-10%) < F_B(-10%) → A ≥_FSD B
    → Portfel A dominuje B w sensie FSD
    → ŻADEN racjonalny inwestor nie wybierze B, bo A jest ściśle lepszy w najgorszym scenariuszu
    → Eliminuj B z dalszej analizy portfelowej

### Zastosowania

- **Portfolio selection:** eliminuj zdominowane portfele bez znajomości U
- **Ubezpieczenia:** fair ubezpieczenie SSD-dominuje brak ubezpieczenia (dla risk-averse)
- **Ocena inwestycji:** A: N(10%,15%), B: N(8%,20%) → E[A]>E[B], σ[A]<σ[B] → A SSD B

| Cecha      | FSD                    | SSD                          |
|------------|------------------------|------------------------------|
| Warunek    | F_A(x) ≤ F_B(x) ∀x    | ∫F_A ≤ ∫F_B ∀x              |
| Na U       | U' ≥ 0                | U' ≥ 0, U'' ≤ 0             |
| Decydenci  | Wszyscy racjonalni     | Risk-averse                  |
| Częstość   | Rzadka                 | Częstsza                     |

### Etymologia

**Stochastyczna** — grec. „stochastos" = zdolny do celowania, od „stochazein" = mierzyć; w probabilistyce: losowy. **FSD/SSD** — Hadar & Russell (1969); Rothschild & Stiglitz (1970) niezależnie. **Mean-Preserving Spread** — Rothschild & Stiglitz: ten sam średni wynik, ale większy rozrzut = gorsze dla risk-averse. **Dominacja** — łac. „dominari" = panować; A dominuje B gdy jest zawsze co najmniej tak dobre.

### Jak zapamiętać

- **FSD = „F always below"** — dystrybuanta A zawsze ≤ B
- **SSD = „Second = Sum (integral)"** — całka z F_A ≤ całka z F_B
- **FSD → wszyscy; SSD → risk-averse**
- FSD implikuje SSD, ale nie odwrotnie

