## PYTANIE 1: Automaty i klasy języków (AISDI)

**Porównać "siłę wyrazu" automatu skończonego, automatu ze stosem oraz maszyny Turinga. Jakie klasy języków rozpoznaje każdy z nich?**

---

### Tło pojęciowe — słowniczek

**Język (formalny)** — zbiór słów (ciągów symboli) nad ustalonym alfabetem Σ. Np. alfabet Σ = {a, b}, język L = {ab, aabb, aaabbb, ...} = {aⁿbⁿ | n ≥ 1}. Język formalny to nie język naturalny (polski, angielski) — to matematyczny zbiór napisów spełniających pewną regułę.

**Automat** — abstrakcyjny model maszyny obliczeniowej. Czyta wejście (słowo) symbol po symbolu i stwierdza, czy to słowo należy do danego języka. „Rozpoznaje" (akceptuje) język = akceptuje dokładnie te słowa, które do niego należą, i odrzuca pozostałe.

**Stan (state)** — chwilowa „konfiguracja" automatu. Automat przechodzi między stanami na podstawie odczytanego symbolu. Pomyśl o nim jak o pozycji na schemacie blokowym — automat „wie" tylko tyle, ile mówi mu aktualny stan.

**Pamięć** — dodatkowa struktura danych, którą automat może zapisywać i odczytywać poza samym stanem. FA nie ma żadnej pamięci (cała informacja to aktualny stan). PDA ma stos. TM ma taśmę.

**Stos (stack)** — struktura danych typu LIFO (Last In, First Out = ostatni włożony, pierwszy wyjęty). Jak stos talerzy: dokładasz na górę, zdejmujesz z góry. Jedyny dostęp to szczyt stosu — nie możesz zajrzeć na dno bez zdjęcia wszystkiego powyżej.

**LIFO** — Last In, First Out. Zasada działania stosu: element dodany jako ostatni jest usuwany jako pierwszy. Przeciwieństwo FIFO (First In, First Out = kolejka).

**Taśma (tape)** — nieskończona (lub ograniczona) linia komórek, z których każda przechowuje symbol. Głowica odczytująco-zapisująca (R/W) może się poruszać w lewo i prawo, odczytywać i nadpisywać symbole. To pamięć o swobodnym dostępie — w przeciwieństwie do stosu, możesz wrócić do dowolnego wcześniejszego miejsca.

**DFA i NFA** — DFA = Deterministic Finite Automaton (deterministyczny automat skończony): w każdym stanie, dla każdego symbolu, istnieje DOKŁADNIE jedno przejście — automat zawsze „wie", co robić. NFA = Nondeterministic Finite Automaton (niedeterministyczny): może mieć WIELE przejść dla jednego symbolu (lub żadne), a także przejścia ε (bez czytania symbolu). **DFA ≡ NFA** oznacza, że rozpoznają DOKŁADNIE te same języki — każdy NFA da się zamienić na równoważny DFA (konstrukcja podzbiorów, powerset construction). NFA bywa wygodniejszy do zapisu, ale nie jest „silniejszy".

**Wyrażenie regularne (regular expression, regex)** — wzorzec tekstowy opisujący zbiór ciągów znaków. Składa się z: symboli alfabetu, konkatenacji (ab), alternatywy (a|b), gwiazdki Kleene'ego (a* = zero lub więcej a). Np. `(a|b)*abb` opisuje wszystkie ciągi nad {a,b} kończące się na „abb". **Równoważne FA** = każde wyrażenie regularne opisuje język, który można rozpoznać automatem skończonym, i odwrotnie — to ten sam zbiór języków.

**Identyfikatory i podzielność (przykłady języków regularnych):**
- *Identyfikatory* — nazwy zmiennych w programowaniu, np. `[a-zA-Z_][a-zA-Z0-9_]*` (zaczyna się od litery lub _, potem litery/cyfry/_). To wyrażenie regularne → język regularny.
- *Podzielność* — np. „liczby binarne podzielne przez 3": automat z 3 stanami (reszta 0, 1, 2) śledzi resztę z dzielenia — nie potrzebuje pamięci, wystarczą stany.

**Nawiasy** — język poprawnie zagnieżdżonych nawiasów, np. `()`, `(())`, `(()())`. FA nie poradzi sobie z tym, bo musi „liczyć" głębokość zagnieżdżenia (potrzebuje pamięci) — PDA ze stosem to robi naturalnie (push na `(`, pop na `)`). To klasyczny język bezkontekstowy.

**Palindromy** — słowa czytane tak samo od przodu i od tyłu, np. `abba`, `aba`, `aabaa`. FA nie rozpoznaje palindromów, bo musiałby zapamiętać pierwszą połowę słowa. PDA rozpoznaje palindromy o nieparzystej długości (NPDA), ale nie deterministycznie — musi „zgadnąć" środek.

**DPDA i NPDA:**
- DPDA = Deterministic Pushdown Automaton — w każdej konfiguracji (stan + szczyt stosu + symbol) jest JEDNO możliwe przejście.
- NPDA = Nondeterministic Pushdown Automaton — może mieć WIELE przejść, „zgaduje" właściwą ścieżkę.
- **DPDA ⊂ NPDA** — w przeciwieństwie do FA, tutaj niedeterminizm DODAJE moc! NPDA rozpoznaje ściśle więcej języków niż DPDA. Np. palindromy nad {a,b} (wwᴿ) wymagają NPDA — DPDA nie potrafi „zgadnąć" środka słowa.

**Dlaczego aⁿbⁿ, nawiasy, wwᴿ pasują do Typu 2 (PDA), a aⁿbⁿcⁿ i ww nie:**
- **aⁿbⁿ** — stos zlicza: push a na stos, potem pop a przy każdym b. Jeśli stos pusty po przeczytaniu → akceptuj. Stos idealnie pasuje do „zliczenia jednej rzeczy, potem dopasowania drugiej".
- **Nawiasy ()** — push na `(`, pop na `)`. Stos śledzi głębokość.
- **wwᴿ** (słowo + jego odwrócenie, np. abba) — push pierwszą połowę, potem pop i porównuj z drugą. NPDA „zgaduje" środek.
- **aⁿbⁿcⁿ — NIE da się na stosie:** stos zużyje się przy dopasowaniu a↔b (push a, pop przy b), i już PUSTY przy c — nie ma czym liczyć c. Potrzeba dwóch niezależnych „liczników" jednocześnie → potrzebna taśma R/W.
- **ww (słowo powtórzone, np. abab) — NIE da się na stosie:** w przeciwieństwie do wwᴿ, druga połowa NIE jest odwrócona, więc porównanie „z góry stosu" nie działa. Stos odwraca kolejność — to pomaga przy palindromach, ale przeszkadza przy powtórzeniu.

**|w| w Typie 1** — |w| to długość słowa wejściowego w. Np. jeśli w = „aabbcc", to |w| = 6. LBA (Linear Bounded Automaton) to maszyna Turinga, której taśma jest ograniczona do co najwyżej |w| komórek (liniowo proporcjonalnie do długości wejścia). Nie może wydłużać taśmy ponad to.

**DLBA i NLBA:**
- DLBA = Deterministic Linear Bounded Automaton.
- NLBA = Nondeterministic Linear Bounded Automaton.
- **Czy DLBA = NLBA?** — to OTWARTY PROBLEM (nierozwiązany!). Nie wiemy, czy deterministyczny LBA rozpoznaje te same języki co niedeterministyczny. To jedno z wielkich otwartych pytań teorii złożoności.

**Dlaczego aⁿbⁿcⁿ i ww pasują do Typu 1 (LBA):**
- **aⁿbⁿcⁿ** — LBA z taśmą R/W może: (1) przejść przez a-ki zaznaczając jednego, (2) przejść przez b-ki zaznaczając jednego, (3) przejść przez c-ki zaznaczając jednego, (4) wrócić na początek i powtarzać. Taśma pozwala wielokrotnie przechodzić i „odznaczać" symbole — tego stos nie potrafi.
- **ww** — LBA porównuje i-ty symbol pierwszej połowy z i-tym symbolem drugiej, przeskakując po taśmie. Swobodny dostęp do taśmy umożliwia porównanie w dowolnej kolejności.

**DTM i NTM — dlaczego równoważne:**
- DTM = Deterministic Turing Machine, NTM = Nondeterministic Turing Machine.
- **DTM ≡ NTM** pod względem MOCY (rozpoznawanych języków) — DTM może symulować NTM, np. przez BFS po drzewie konfiguracji. Symulacja jest wykładniczo wolniejsza, ale DTM rozpoznaje DOKŁADNIE te same języki.
- Uwaga: czy symulacja musi być wolniejsza to osobne pytanie — to jest istota problemu P vs NP!

**Domknięcie ∩/¬ (closure under intersection and complement):**
- Klasa języków jest „domknięta" na operację, jeśli wynik tej operacji na językach z klasy ZAWSZE daje język z tej samej klasy.
- **∩ (przecięcie):** jeśli L₁ i L₂ należą do klasy, to L₁ ∩ L₂ też? Np. języki regularne: TAK (automat produktowy). Bezkontekstowe: NIE (kontrprzykład: {aⁿbⁿcᵐ} ∩ {aᵐbⁿcⁿ} = {aⁿbⁿcⁿ}, który nie jest bezkontekstowy).
- **¬ (dopełnienie/komplement):** jeśli L należy do klasy, to L̄ (wszystkie słowa NIE należące do L) też? Regularne: TAK (zamień stany akceptujące ↔ nieakceptujące). Bezkontekstowe: NIE. Rek. przeliczalne: NIE (komplement problemu stopu nie jest rek. przeliczalny).

**Zastosowania — co oznaczają:**
- **Leksery (lexers)** — pierwszy etap kompilacji: dzielą kod źródłowy na tokeny (słowa kluczowe, identyfikatory, liczby, operatory). Używają automatów skończonych / wyrażeń regularnych. Np. `if`, `123`, `"hello"`, `+` to tokeny.
- **Parsery (parsers)** — drugi etap: budują drzewo składniowe (parse tree) z tokenów, sprawdzając strukturę gramatyczną programu. Używają gramatyk bezkontekstowych / automatów ze stosem. Np. sprawdzają, czy `if (x) { y; }` ma poprawną strukturę.
- **Weryfikacja ograniczeń (constraint verification)** — sprawdzanie złożonych reguł kontekstowych, np. „zmienna musi być zadeklarowana przed użyciem", „typy muszą się zgadzać". Wykracza poza CFG, odpowiada gramatykom kontekstowym / LBA.
- **Obliczenia ogólne (general computation)** — dowolne obliczenia algorytmiczne: od sortowania, przez sztuczną inteligencję, po symulację fizyki. Maszyna Turinga modeluje KAŻDE możliwe obliczenie (teza Churcha-Turinga).

---

### Porównanie siły wyrazu

**Siła wyrazu** (expressive power) — klasa języków, które automat rozpoznaje. Im szersza klasa, tym większa siła:

    FA  ⊂  PDA  ⊂  LBA  ⊂  TM

- **FA < PDA:** FA nie rozpoznaje aⁿbⁿ (brak pamięci do liczenia), PDA tak (stos zlicza).
- **PDA < LBA:** PDA nie rozpoznaje aⁿbⁿcⁿ (stos zużyty po a/b), LBA tak (taśma ogr. R/W).
- **LBA < TM:** LBA ograniczona do |w| komórek, TM ma nieskończoną taśmę.

### Hierarchia Chomsky'ego (1956)

    Typ 0: Rek. przeliczalne (TM)
      ⊃ Typ 1: Kontekstowe (LBA)
      ⊃ Typ 2: Bezkontekstowe (PDA)
      ⊃ Typ 3: Regularne (FA)

### FA — Typ 3: Języki regularne

M = (Q, Σ, δ, q₀, F). **Pamięć:** brak — tylko stan. **DFA ≡ NFA.**
Równoważne wyrażeniom regularnym (regex).
Przykłady: identyfikatory, podzielność. Nie: aⁿbⁿ, nawiasy, palindromy.

### PDA — Typ 2: Języki bezkontekstowe

M = (Q, Σ, Γ, δ, q₀, Z₀, F). **Pamięć:** stos LIFO. **DPDA ⊂ NPDA!**
Przykłady: aⁿbⁿ, nawiasy, wwᴿ. Nie: aⁿbⁿcⁿ, ww.

### LBA — Typ 1: Języki kontekstowe

TM z taśmą ograniczoną do |w|. **DLBA =? NLBA** — problem otwarty!
Przykłady: aⁿbⁿcⁿ, ww.

### TM — Typ 0: Rekurencyjnie przeliczalne

M = (Q, Σ, Γ, δ, q₀, q_acc, q_rej). **Pamięć:** taśma ∞ R/W. **DTM ≡ NTM** (moc).
Teza Churcha-Turinga: TM modeluje każde obliczenie. Nie: komplement problemu stopu.

### Tabela porównawcza

| Cecha          | FA         | PDA            | LBA              | TM                |
|----------------|------------|----------------|------------------|-------------------|
| Pamięć         | Brak       | Stos (LIFO)    | Taśma ogr. (R/W) | Taśma ∞ (R/W)     |
| Klasa języków  | Regularne  | Bezkontekstowe | Kontekstowe      | Rek. przeliczalne |
| DET = NIEDET?  | TAK        | NIE            | Otwarte!         | TAK (moc)         |
| Domknięcie ∩/¬ | TAK/TAK    | NIE/NIE        | TAK/TAK          | TAK/NIE           |
| Zastosowanie   | Leksery    | Parsery        | Weryfikacja ogr. | Obliczenia ogólne |

### Etymologia nazw

**Automaty:** *Finite Automaton* — „skończony" = skończona liczba stanów (cała pamięć to stan). *Pushdown Automaton* — „pushdown" od spring-loaded tray dispenser (dozownik tac w stołówce: push down = zepchnij na stos). *LBA* — taśma liniowo proporcjonalna do wejścia (Myhill 1960, Kuroda 1964). *Maszyna Turinga* — Alan Turing (1936, „On Computable Numbers"), formalizacja obliczalności; odpowiedź na Entscheidungsproblem Hilberta; złamał Enigmę w WWII. *Hierarchia Chomsky'ego* — Noam Chomsky (MIT, 1956), lingwista; hierarchia gramatyk dla języków naturalnych okazała się fundamentem informatyki.

**Języki:** *Regularne* — od „regular expressions" (Kleene 1956); „regular" = podlegające stałej regule (łac. regula). *Bezkontekstowe (Context-Free)* — produkcje A → α stosowane BEZ patrzenia na kontekst wokół A; nieterminal przepisywany niezależnie od otoczenia. *Kontekstowe (Context-Sensitive)* — produkcje αAβ → αγβ: przepisanie A ZALEŻY od kontekstu α i β. *Rekurencyjnie przeliczalne (Recursively Enumerable)* — istnieje TM wyliczająca (enumerate) wszystkie słowa języka; „rekurencyjnie" = przez procedurę obliczeniową (ale może nie zatrzymać się na nie-członkach).

### Jak zapamiętać

- **„Raz Bardzo Kolorowy Rekin"** — Regularny ⊂ Bezkontekstowy ⊂ Kontekstowy ⊂ Rek.przeliczalny
- **Pamięć:** Brak → Stos → Taśma ogr. → Taśma ∞
- **Kontrprzykłady:** aⁿbⁿ łamie FA, aⁿbⁿcⁿ łamie PDA
- **Kontekst nazw:** Context-Free = A przepisywane bez kontekstu; Context-Sensitive = kontekst αAβ decyduje

\newpage

## PYTANIE 2: Algorytmy najkrótszej ścieżki (AISDI)

**Omówić i porównać algorytmy: Dijkstry, Bellmana-Forda, A*.**

---

### Tło pojęciowe — słowniczek

**Graf** — struktura danych składająca się z **wierzchołków** (vertices/nodes) połączonych **krawędziami** (edges). Np. mapa miast: miasta = wierzchołki, drogi = krawędzie.

**Wierzchołek (vertex, node)** — punkt w grafie. Oznaczany jako v, u, n, m itp. **V** = zbiór wszystkich wierzchołków; |V| = ich liczba.

**Krawędź (edge)** — połączenie między dwoma wierzchołkami. **E** = zbiór krawędzi; |E| = ich liczba. Krawędź może być skierowana (A→B ≠ B→A) lub nieskierowana (A↔B).

**Waga (weight)** — liczba przypisana do krawędzi, oznaczająca „koszt" przejścia. Np. odległość w km, czas podróży, opłata za przejazd. Graf z wagami = graf ważony.

**Koszt (cost)** — ogólne pojęcie „ceny" przejścia ścieżką. Koszt ścieżki = suma wag krawędzi na tej ścieżce. Cel algorytmów: znaleźć ścieżkę o **minimalnym koszcie**.

**SSSP (Single-Source Shortest Path)** — problem: mając JEDEN wierzchołek startowy (źródło), znajdź najkrótsze ścieżki do WSZYSTKICH pozostałych wierzchołków. Dijkstra i Bellman-Ford rozwiązują SSSP. **Single-Pair** — prostszy problem: znajdź najkrótszą ścieżkę z A do B (jednej konkretnej pary). A* rozwiązuje Single-Pair.

**d[v]** — tablica odległości. **d** = tablica (array), **v** = wierzchołek. d[v] przechowuje aktualnie najlepsze znane oszacowanie odległości od źródła do wierzchołka v. Na początku d[start] = 0, d[wszystko inne] = ∞. Algorytm stopniowo poprawia te wartości.

**Zachłanny (greedy)** — strategia algorytmiczna: w każdym kroku wybierz opcję, która TERAZ wygląda najlepiej (lokalnie optymalna), bez cofania się. Dijkstra jest zachłanny: zawsze bierze wierzchołek o najmniejszym d[v] i nigdy go nie rewiduje.

**Relaksacja krawędzi (edge relaxation)** — kluczowa operacja. Sprawdza: „czy droga do v przez u jest krótsza niż dotychczas znana?" Jeśli d[u] + waga(u,v) < d[v], to zaktualizuj d[v]. Nazwa od „rozluźniania" — górne ograniczenie na odległość się „rozluźnia" (maleje) w stronę prawdziwej wartości.

**Tablica (array)** — najprostsza struktura danych: ciągły blok pamięci. W Dijkstrze z tablicą: szukanie minimum d[v] wymaga przejrzenia WSZYSTKICH wierzchołków → O(V) na szukanie × V razy = **O(V²)**.

Przykład — graf z 4 wierzchołkami (A, B, C, D), start = A:

    Graf:  A --2-- B --3-- D
           |               |
           4               1
           |               |
           C ------5-------+

    d = [ A:0,  B:∞,  C:∞,  D:∞ ]     ← tablica na starcie
         odwiedzone = {}

    Krok 1: przeszukaj CAŁĄ tablicę d → min = A (0)
            d = [ A:0, B:2, C:4, D:∞ ]   odw = {A}
                        ↑    ↑
                    A→B=2  A→C=4  (relaksacja sąsiadów A)

    Krok 2: przeszukaj CAŁĄ tablicę d (poza odw.) → min = B (2)
            d = [ A:0, B:2, C:4, D:5 ]   odw = {A,B}
                                  ↑
                            B→D=2+3=5 (relaksacja)

    Krok 3: przeszukaj tablicę → min = C (4)
            d = [ A:0, B:2, C:4, D:5 ]   odw = {A,B,C}
                                  ↑
                            C→D=4+5=9 > 5, nie zmieniaj

    Krok 4: min = D (5). Koniec! d = [A:0, B:2, C:4, D:5]

    Każdy krok = przejrzyj V elementów → 4 kroki × 4 elementy = 16 operacji = O(V²)

**Kopiec (heap)** — drzewiasta struktura danych, w której element minimalny jest zawsze na szczycie. Wyciąganie minimum: O(log n). W Dijkstrze z kopcem: szukanie min d[v] to O(log V) zamiast O(V) → **O((V+E) log V)**.

Przykład — ten sam graf, ale z kopcem (min-heap):

    Kopiec na starcie:      (0,A)          ← min zawsze na szczycie
                                           (reszta to ∞)

    Krok 1: pop (0,A) — O(log 4)=O(2), relaksuj sąsiadów:
            push (2,B), push (4,C)

            Kopiec:    (2,B)
                      /     \
                   (4,C)   ...

    Krok 2: pop (2,B) — O(log 4), relaksuj:
            push (5,D)

            Kopiec:    (4,C)
                      /
                   (5,D)

    Krok 3: pop (4,C) — O(log 4). C→D: 9 > 5, nie zmieniaj.
    Krok 4: pop (5,D) — O(log 4). Koniec!

    Każdy pop = O(log V), każdy push = O(log V)
    V popów + E pushów = O((V+E) log V)

**Kopiec Fibonacciego** — zaawansowany kopiec, w którym operacja „zmniejsz klucz" (decrease-key) działa w zamortyzowanym O(1) zamiast O(log V). Dijkstra robi decrease-key dla każdej krawędzi → z kopcem Fib: **O(V log V + E)** — E operacji po O(1) + V wyciągnięć po O(log V).

Przykład — kluczowa różnica: decrease-key:

    Zwykły kopiec — gdy znajdziesz krótszą drogę do D:
        d[D] zmienia się z 9 na 5
        Trzeba „naprawić" kopiec: przesuwaj D w górę → O(log V)

    Kopiec Fibonacciego — ta sama sytuacja:
        d[D] zmienia się z 9 na 5
        Po prostu odetnij D od rodzica i wstaw do listy korzeni → O(1)!
        (naprawienie struktury odłożone na później — „zamortyzowane")

    Różnica ma znaczenie przy GĘSTYCH grafach (E >> V):
    - Zwykły kopiec: E × O(log V) = O(E log V) na decrease-key
    - Kopiec Fib:    E × O(1)     = O(E)       na decrease-key
    Razem: O(V log V) [pop] + O(E) [decrease-key] = O(V log V + E)

**Złożoność — dlaczego takie wartości:**
- **O(V²)** z tablicą: V razy szukaj minimum (O(V) każdy) = V × V.
- **O((V+E) log V)** z kopcem: V wyciągnięć min (O(log V)) + E relaksacji z decrease-key (O(log V)).
- **O(V log V + E)** z kopcem Fib: V wyciągnięć min (O(log V)) + E decrease-key (O(1) zamortyzowane).

**Programowanie dynamiczne (DP)** — technika rozwiązywania problemów przez rozbicie na mniejsze podproblemy i zapamiętywanie wyników (żeby nie liczyć tego samego dwa razy). Bellman-Ford jest DP: podproblem = „najkrótsza ścieżka do v używająca ≤ k krawędzi"; rozwiązuje dla k = 1, 2, ..., V−1.

**Cykl** — ścieżka w grafie, która wraca do punktu wyjścia (A → B → C → A). **Cykl ujemny** — cykl, w którym suma wag < 0. Problem: za każdym obejściem cyklu „odległość" maleje — można iść w nieskończoność → najkrótsza ścieżka nie istnieje (= −∞).

**Dlaczego O(V·E) w Bellman-Ford:** Algorytm wykonuje |V|−1 iteracji (bo najdłuższa najkrótsza ścieżka bez cykli ma co najwyżej V−1 krawędzi). W każdej iteracji relaksuje WSZYSTKIE |E| krawędzi. Razem: (V−1) × E ≈ O(V·E).

**Heurystyczny** — wykorzystujący przybliżone oszacowanie (heurystykę) zamiast dokładnych obliczeń. A* jest heurystyczny: używa funkcji h(n) do zgadywania „ile jeszcze do celu".

**f(n), g(n), h(n) — co oznacza n i każda funkcja:**
- **n** = aktualnie rozpatrywany wierzchołek.
- **g(n)** = dotychczasowy koszt dotarcia od startu do n (znany, dokładny).
- **h(n)** = heurystyka: OSZACOWANIE kosztu od n do celu (przybliżone, „zgadywane"). Np. odległość w linii prostej do celu.
- **f(n) = g(n) + h(n)** = oszacowanie CAŁKOWITEGO kosztu ścieżki przez n. A* zawsze rozwija wierzchołek o najniższym f(n).

**Dopuszczalna (admissible)** — heurystyka h jest dopuszczalna, jeśli NIGDY nie przeszacowuje: h(n) ≤ prawdziwy koszt od n do celu. Gwarantuje, że A* znajdzie optymalną ścieżkę. Np. odległość w linii prostej jest dopuszczalna (nie da się dojechać krócej niż prosto).

**Rzeczywisty koszt** — prawdziwa najkrótsza odległość (nie oszacowanie). Np. faktyczna najkrótsza droga od n do celu, uwzględniając wszystkie krawędzie.

**n → cel** — od wierzchołka n do wierzchołka docelowego (cel = destination = target).

**Spójna (consistent / monotone)** — silniejszy warunek na heurystykę: h(n) ≤ w(n,m) + h(m) dla każdej krawędzi n→m. Tu **w(n,m)** = waga krawędzi z n do m, a **m** = sąsiad n. Spójność oznacza: oszacowanie z n nie jest „dużo lepsze" niż to co uzyskasz idąc jeden krok do m. Spójna ⇒ dopuszczalna (ale nie odwrotnie).

**Dlaczego O(V) w najlepszym przypadku A*:** Jeśli heurystyka jest idealna (h(n) = prawdziwy koszt), A* idzie prosto do celu, nie eksplorując zbędnych wierzchołków — odwiedza tylko te na optymalnej ścieżce ≈ O(V) jeśli ścieżka krótka. **Najgorszy przypadek** = h(n) = 0 dla wszystkich n → A* degeneruje się do Dijkstry.

### Pseudokod (Python)

**Dijkstra:**

    import heapq
    def dijkstra(graph, start):
        d = {v: float('inf') for v in graph}
        d[start] = 0
        pq = [(0, start)]               # (odległość, wierzchołek)
        while pq:
            dist_u, u = heapq.heappop(pq)
            if dist_u > d[u]: continue   # nieaktualny wpis
            for v, w in graph[u]:        # v=sąsiad, w=waga
                if d[u] + w < d[v]:      # relaksacja
                    d[v] = d[u] + w
                    heapq.heappush(pq, (d[v], v))
        return d

**Bellman-Ford:**

    def bellman_ford(vertices, edges, start):
        d = {v: float('inf') for v in vertices}
        d[start] = 0
        for _ in range(len(vertices) - 1):  # V-1 iteracji
            for u, v, w in edges:            # każda krawędź
                if d[u] + w < d[v]:          # relaksacja
                    d[v] = d[u] + w
        # Wykrywanie cyklu ujemnego:
        for u, v, w in edges:
            if d[u] + w < d[v]:
                return None  # cykl ujemny!
        return d

**A*:**

    def a_star(graph, start, goal, h):
        d = {start: 0}
        pq = [(h(start), start)]             # f = g + h
        came_from = {}
        while pq:
            f_u, u = heapq.heappop(pq)
            if u == goal: break              # znaleziono!
            for v, w in graph[u]:
                g_new = d[u] + w
                if v not in d or g_new < d[v]:
                    d[v] = g_new
                    heapq.heappush(pq, (g_new + h(v), v))
                    came_from[v] = u
        return came_from, d.get(goal)

---

### Dijkstra — zachłanny, SSSP

**Ograniczenie:** wagi ≥ 0.
**Idea:** Relaksacja krawędzi; zawsze przetwarzaj wierzchołek o najmniejszym d[v].
**Złożoność:** O(V²) z tablicą, O((V+E) log V) z kopcem, O(V log V + E) z kopcem Fibonacciego.
**Dlaczego nie ujemne wagi?** Raz oznaczony wierzchołek nie jest rewidowany — ujemna krawędź może go poprawić.

### Bellman-Ford — programowanie dynamiczne, SSSP

**Zaleta:** obsługuje ujemne wagi + **wykrywa cykle ujemne**.
**Idea:** |V|−1 iteracji relaksacji WSZYSTKICH krawędzi. Jeśli w iteracji V nadal można poprawić → cykl ujemny.
**Złożoność:** O(V·E) — zawsze.

### A* — heurystyczny, Single-Pair

**Rozszerzenie Dijkstry:** f(n) = g(n) + h(n), gdzie h(n) to heurystyka.
**Wymóg:** h dopuszczalna (admissible): h(n) ≤ rzeczywisty koszt n→cel. Jeśli h spójna (consistent): h(n) ≤ w(n,m) + h(m) — optymalne.
**Złożoność:** zależy od h; najlepszy przypadek O(V), najgorszy jak Dijkstra.

### Porównanie

| Cecha           | Dijkstra         | Bellman-Ford    | A*                |
|-----------------|------------------|-----------------|-------------------|
| Typ             | Zachłanny        | Prog. dynamiczne| Heurystyczny      |
| Problem         | SSSP             | SSSP            | Single-pair       |
| Ujemne wagi     | NIE              | TAK             | NIE               |
| Wykrywa cykle-  | NIE              | TAK             | NIE               |
| Złożoność       | O((V+E)log V)    | O(VE)           | Zależy od h       |

### Etymologia

**Dijkstra** — Edsger W. Dijkstra (Holandia, 1959); pionier informatyki (Turing Award 1972). **Bellman-Ford** — Richard Bellman (twórca programowania dynamicznego) + Lester Ford Jr. (1956). **A*** — Hart, Nilsson, Raphael (Stanford, 1968); „A*" = ulepszona wersja algorytmu „A". **Zachłanny (Greedy)** — algorytm „chciwie" bierze lokalnie najlepszą opcję. **SSSP** — Single-Source Shortest Path. **Programowanie dynamiczne** — Bellman wybrał „dynamic" by brzmiało imponująco dla polityków (nie miało związku z dynamiką!). **Heurystyka** — grec. „heuriskein" = znajdować (to samo co „Eureka!" Archimedesa). **Relaksacja** — „rozluźnianie" górnego ograniczenia na odległość d[v].

### Jak zapamiętać

- **Dijkstra = chciwy**, bierze minimum — ale „nie patrzy wstecz" (stąd problem z ujemnymi wagami)
- **Bellman-Ford = brute force x (V−1)** — relaksuj wszystko, V−1 razy, bo najdłuższa ścieżka ma V−1 krawędzi
- **A* = Dijkstra + „GPS"** — heurystyka mówi w którą stronę jest cel

\newpage

## PYTANIE 3: Redundancja i normalizacja (BD2)

**Omówić zagadnienia redundancji i normalizacji w relacyjnej bazie danych.**

---

### Tło pojęciowe — słowniczek

**Relacja (tabela)** — w bazie danych: tabela z kolumnami (atrybutami) i wierszami (krotkami/rekordami). Np. tabela Studenci z kolumnami: StudentID, Imię, Nazwisko, WydziałID.

**Atrybut (attribute)** — kolumna w tabeli. Np. „Imię", „WydziałID", „NazwaKursu". Każdy atrybut ma nazwę i typ danych (tekst, liczba, data itp.).

**Klucz główny (primary key, PK)** — kolumna (lub zestaw kolumn), której wartość JEDNOZNACZNIE identyfikuje każdy wiersz. Np. StudentID = 12345 → dokładnie jeden student. Nie może się powtarzać, nie może być NULL.

**Klucz złożony (composite key)** — klucz główny składający się z WIĘCEJ NIŻ JEDNEJ kolumny. Np. klucz (StudentID, KursID) — jeden student na jednym kursie to unikalny zapis. Sam StudentID ani sam KursID nie wystarczą, bo student ma wiele kursów, a kurs ma wielu studentów.

**Atrybut wtórny (non-prime attribute)** — kolumna, która NIE jest częścią żadnego klucza kandydującego. Np. w tabeli z kluczem (StudentID, KursID): NazwaKursu, Ocena, NazwaWydziału — to atrybuty wtórne (nie identyfikują wiersza). **Atrybut pierwszy (prime)** — kolumna, która JEST częścią jakiegoś klucza (np. StudentID).

**Nadklucz (superkey)** — dowolny zbiór kolumn, który JEDNOZNACZNIE identyfikuje wiersz. Każdy klucz główny jest nadkluczem, ale nadklucz może mieć „nadmiarowe" kolumny. Np. {StudentID} to klucz i nadklucz; {StudentID, Imię} to nadklucz (ale nie minimalny klucz).

**Redundancja** — powtarzanie tych samych danych w wielu miejscach. Nie chodzi o kopie zapasowe — chodzi o niepotrzebne duplikowanie informacji w tabeli.

Przykład — tabela StudentKursy (ZŁEJ konstrukcji, BEZ normalizacji):

    | StudentID | Imię  | WydziałID | NazwaWydziału | KursID | NazwaKursu |
    |-----------|-------|-----------|---------------|--------|------------|
    | 1         | Anna  | W4        | EiTI          | K10    | Bazy danych|
    | 1         | Anna  | W4        | EiTI          | K20    | Algorytmy  |
    | 2         | Jan   | W4        | EiTI          | K10    | Bazy danych|
    | 3         | Ewa   | W2        | Fizyka        | K30    | Optyka     |

Problem: „Anna", „W4", „EiTI", „Bazy danych" powtórzone wielokrotnie!

**Anomalia** — niepożądany efekt uboczny operacji na redundantnych danych. Trzy typy:

**Anomalia wstawiania** — nie możesz dodać danych bez podania niepotrzebnych powiązań.
- Przykład: chcesz dodać nowy wydział W5 „Chemia" do systemu, ale nie ma jeszcze żadnego studenta na tym wydziale. W tej tabeli NIE DA SIĘ — bo StudentID (część klucza) nie może być NULL.

**Anomalia usuwania** — usuwając jeden fakt, tracisz niezwiązany inny.
- Przykład: Ewa (jedyny student Fizyki) rezygnuje → usuwasz jej wiersz → tracisz informację, że wydział W2 to „Fizyka" i istnieje kurs „Optyka". Dane o wydziale i kursie znikają razem ze studentem!

**Anomalia modyfikacji** — zmiana jednego faktu wymaga aktualizacji wielu wierszy.
- Przykład: wydział W4 zmienia nazwę z „EiTI" na „Informatyka". Trzeba zaktualizować KAŻDY wiersz, w którym jest NazwaWydziału = „EiTI" (tu: 3 wiersze). Jeśli pominiesz jeden → niespójność.

**Zależność funkcyjna (FD — Functional Dependency):** X → Y oznacza: „znając wartość X, ZAWSZE mogę jednoznacznie wyznaczyć Y". Jak funkcja matematyczna: f(x) daje dokładnie jedno y. Np. StudentID → Imię (jeden student = jedno imię), KursID → NazwaKursu (jeden kurs = jedna nazwa). **X → Y NIE oznacza Y → X!** (StudentID → WydziałID, ale WydziałID → StudentID NIE — na wydziale jest wielu studentów).

**Zależność przechodnia (transitive dependency):** A → B i B → C, więc A → C „przez pośrednika B". Np. StudentID → WydziałID → NazwaWydziału. StudentID nie określa bezpośrednio NazwaWydziału — robi to pośrednio przez WydziałID. Problem: NazwaWydziału „zależy od czegoś, co nie jest kluczem" → redundancja.

**Nietrywialna FD:** X → A, gdzie A nie jest częścią X. Np. StudentID → Imię (nietrywialna: Imię ≠ StudentID). Ale {StudentID, Imię} → StudentID jest TRYWIALNA (StudentID jest częścią lewej strony — oczywiste). W BCNF sprawdzamy tylko nietrywialne FD.

**Wielowartościowa zależność (MVD — Multi-Valued Dependency):** X →→ Y oznacza: dla jednej wartości X istnieje ZBIÓR wartości Y, niezależny od reszty. Np. Student →→ Hobby i Student →→ Kurs: hobby Ani nie zależą od jej kursów i odwrotnie, ale ich połączenie tworzy iloczyn kartezjański (niepotrzebne powtórzenia).

**Dekompozycja** — rozbicie jednej dużej tabeli na kilka mniejszych, połączonych kluczami obcymi. Cel: każda tabela przechowuje JEDEN fakt. **Normalizacja eliminuje redundancję** właśnie przez dekompozycję — informacja zamiast być powtarzana w wielu wierszach, przechowywana jest RAZ w osobnej tabeli i łączona przez JOIN.

Przykład dekompozycji powyższej tabeli:

    Studenci:                    Wydziały:              Kursy:
    | StID | Imię | WydziałID |  | WydziałID | Nazwa | | KursID | Nazwa      |
    |------|------|-----------|  |-----------|-------|  |--------|------------|
    | 1    | Anna | W4        |  | W4        | EiTI  |  | K10    | Bazy danych|
    | 2    | Jan  | W4        |  | W2        |Fizyka |  | K20    | Algorytmy  |
    | 3    | Ewa  | W2        |                         | K30    | Optyka     |

    Zapisy (StudentID, KursID):
    | StID | KursID |
    |------|--------|
    | 1    | K10    |
    | 1    | K20    |
    | 2    | K10    |
    | 3    | K30    |

    Teraz: „EiTI" zapisane RAZ (w Wydziały). Zmiana nazwy = 1 wiersz.

**Atomowe wartości (1NF)** — każda komórka zawiera JEDNĄ niepodzielną wartość. NIE listy, NIE zbiory, NIE tabele w komórce.

    ŹLE (łamie 1NF):                    DOBRZE (1NF):
    | Student | Kursy           |        | Student | Kurs        |
    |---------|-----------------|        |---------|-------------|
    | Anna    | BD, Algorytmy   |        | Anna    | BD          |
    | Jan     | BD              |        | Anna    | Algorytmy   |
                                         | Jan     | BD          |

### Przykłady postaci normalnych

**Przykład naruszenia 2NF** — klucz złożony (StudentID, KursID):

    | StudentID | KursID | NazwaKursu  | Ocena |
    |-----------|--------|-------------|-------|
    | 1         | K10    | Bazy danych | 5     |
    | 2         | K10    | Bazy danych | 4     |

    NazwaKursu zależy TYLKO od KursID, nie od pełnego klucza (StudentID, KursID).
    To „częściowa zależność" → łamie 2NF.
    Naprawa: wydziel Kursy(KursID, NazwaKursu) osobno.

**Przykład naruszenia 3NF** — klucz StudentID:

    | StudentID | Imię  | WydziałID | NazwaWydziału |
    |-----------|-------|-----------|---------------|
    | 1         | Anna  | W4        | EiTI          |
    | 2         | Jan   | W4        | EiTI          |  ← „EiTI" powtórzone!

    StudentID → WydziałID → NazwaWydziału (zależność przechodnia!).
    NazwaWydziału zależy od WydziałID, a nie bezpośrednio od klucza.
    Naprawa: wydziel Wydziały(WydziałID, NazwaWydziału).

**Przykład naruszenia BCNF:**

    Przedmioty prowadzone — klucz: (Student, Przedmiot)
    | Student | Przedmiot | Prowadzący |
    |---------|-----------|------------|
    | Anna    | BD        | Kowalski   |
    | Jan     | BD        | Kowalski   |
    | Anna    | Algo      | Nowak      |

    FD: Prowadzący → Przedmiot (jeden prowadzący = jeden przedmiot).
    Prowadzący NIE jest nadkluczem → łamie BCNF.
    (Spełnia 3NF, bo Przedmiot jest atrybutem pierwszym — wyjątek 3NF.)
    Naprawa: StudentProwadzący(Student, Prowadzący) + ProwadzącyPrzedmiot(Prowadzący, Przedmiot).

**Przykład naruszenia 4NF:**

    | Student | Hobby    | Kurs      |
    |---------|----------|-----------|
    | Anna    | Szachy   | BD        |
    | Anna    | Szachy   | Algorytmy |
    | Anna    | Bieganie | BD        |
    | Anna    | Bieganie | Algorytmy |

    Student →→ Hobby i Student →→ Kurs (niezależne wielowartościowe zależności).
    Hobby i Kursy nie mają ze sobą nic wspólnego, ale tworzą iloczyn kartezjański.
    Naprawa: StudentHobby(Student, Hobby) + StudentKurs(Student, Kurs).

---

### Redundancja — powtarzanie danych

Prowadzi do trzech **anomalii**:
1. **Wstawiania** — nie można dodać danych bez zbędnych powiązań
2. **Usuwania** — usunięcie rekordu kasuje niezwiązane informacje
3. **Modyfikacji** — zmiana jednej informacji wymaga wielu aktualizacji

### Normalizacja — eliminacja redundancji przez dekompozycję

**Zależność funkcyjna:** X → Y — wartość X jednoznacznie określa Y.

### Postacie normalne (5NF ⊂ 4NF ⊂ BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF)

**1NF:** Atomowe wartości, brak list/tablic w komórkach, istnieje klucz główny.

**2NF:** 1NF + każdy atrybut wtórny zależy od CAŁEGO klucza (dotyczy kluczy złożonych).
- Naruszenie: NazwaKursu zależy tylko od KursID, nie od (StudentID, KursID).

**3NF:** 2NF + brak zależności przechodnich (atrybut wtórny nie zależy od innego wtórnego).
- Naruszenie: StudentID → WydziałID → NazwaWydziału.

**BCNF:** Dla każdej nietrywialnej FD X→A, X jest nadkluczem. Silniejsza niż 3NF.

**4NF:** BCNF + brak wielowartościowych zależności nietrywialnych.

### Denormalizacja

Świadome wprowadzanie redundancji dla wydajności (mniej JOIN-ów). Stosowane w systemach analitycznych (OLAP), data warehousing.

### Etymologia

**Redundancja** — łac. „redundantia" = nadmiar/przelewanie się. **Normalizacja** — Edgar F. Codd (IBM, 1970, „A Relational Model of Data"); 1NF–3NF w oryginalnej pracy. **BCNF** — Raymond Boyce + Codd (1974). **Anomalia** — grec. „anomalia" = nieregularność. **„Klucz, cały klucz i tylko klucz"** — parafraza przysięgi sądowej; przypisywana Coddowi. **Zależność funkcyjna** — jak funkcja mat.: X jednoznacznie wyznacza Y.

### Jak zapamiętać

- **„Klucz, cały klucz i tylko klucz — tak mi dopomóż Codd"** — 1NF (klucz), 2NF (cały klucz), 3NF (tylko klucz)
- **3 anomalie:** Wstawianie, Usuwanie, Modyfikacja — „WUM"
- **BCNF:** jak 3NF, ale lewa strona FD zawsze nadklucz (bez wyjątku dla atrybutów pierwszych)

\newpage

## PYTANIE 4: Baza danych jako fundament systemów (BD2)

**Dlaczego baza danych stanowi dobry fundament do budowy wielu systemów informatycznych?**

---

### Tło pojęciowe — słowniczek

**System informatyczny** — oprogramowanie realizujące jakąś funkcję: sklep internetowy, system bankowy, CRM, system rezerwacji. Każdy taki system potrzebuje PRZECHOWYWAĆ dane i OPEROWAĆ na nich. Baza danych daje gotowe, sprawdzone mechanizmy do tego — nie trzeba ich pisać od zera.

**Dlaczego DB to „dobry fundament"?** — Bez bazy danych każdy system musi SAM rozwiązywać: „co jeśli prąd padnie w trakcie zapisu?", „co jeśli dwóch użytkowników edytuje to samo?", „jak chronić dane?". Baza dostarcza to wszystko „z pudełka" → programista skupia się na logice biznesowej, nie na infrastrukturze.

---

**Transakcja** — logiczna jednostka pracy: zestaw operacji, które MUSZĄ wykonać się razem jako całość. Np. przelew bankowy = (1) odejmij 100 zł od Ani + (2) dodaj 100 zł Janowi. Nie może być tak, że tylko (1) się wykona, a (2) nie — pieniądze by „zniknęły".

**ACID** — cztery właściwości, które baza gwarantuje dla każdej transakcji:

**Atomicity (Atomowość)** — „albo cała, albo nic" (all-or-nothing). Jeśli COKOLWIEK w transakcji się nie powiedzie (błąd, crash, brak pamięci), WSZYSTKIE zmiany tej transakcji są cofane (rollback). Jakby nic się nie stało. Np. przelew: jeśli krok (2) się nie uda, krok (1) jest automatycznie cofany — saldo Ani wraca do stanu sprzed przelewu.

**Jak to odpowiada na pytanie:** Bez atomowości system bankowy mógłby tracić pieniądze przy każdym crashu. Baza gwarantuje, że KAŻDA operacja jest bezpieczna → solidny fundament.

**Consistency (Spójność)** — transakcja przeprowadza bazę ze SPÓJNEGO stanu w inny SPÓJNY stan. **Stan** = aktualna zawartość wszystkich tabel w bazie (wszystkie dane w danym momencie). **Spójny stan** = stan, w którym WSZYSTKIE reguły (constraints) są spełnione. Np. „saldo ≥ 0", „każde zamówienie ma klienta", „PESEL ma 11 cyfr". **Spójny → spójny** = transakcja NIE MOŻE zostawić bazy w stanie łamiącym reguły. Np. przelew: suma pieniędzy w systemie przed = suma po (nie da się „stworzyć" pieniędzy).

**Jak to odpowiada na pytanie:** Dane w systemie ZAWSZE mają sens. Nie będzie zamówienia bez klienta, produktu z ceną −5 zł, ani studenta z oceną 7.

**Isolation (Izolacja)** — równoległe (jednoczesne) transakcje nie widzą nawzajem swoich niedokończonych zmian. Każda transakcja „myśli", że jest jedyną operacją na bazie. Np. Ania przelewa 100 zł a Jan sprawdza saldo — Jan widzi ALBO stan przed przelewem, ALBO po, NIGDY stan pośredni (np. „Ania odjęła, ale Jan jeszcze nie dostał").

**Jak to odpowiada na pytanie:** System może obsługiwać TYSIĄCE użytkowników jednocześnie bez chaosu. Każdy widzi spójne dane.

**Durability (Trwałość)** — po zatwierdzeniu transakcji (COMMIT), jej efekty przetrwają KAŻDĄ awarię: crash serwera, awaria dysku, przerwa w zasilaniu. Baza zapisuje zmiany do trwałego magazynu (dysk, WAL — Write-Ahead Log). Nawet jeśli serwer padnie 1 ms po COMMIT, dane są bezpieczne.

**Jak to odpowiada na pytanie:** System nie traci danych. Klient płaci za zamówienie → zamówienie jest zapisane NA ZAWSZE, nawet jeśli serwer zaraz potem się wyłączy.

---

**ANSI** — American National Standards Institute: amerykańska organizacja normalizacyjna (odpowiednik polskiego PKN). Ustala standardy techniczne.

**SPARC** — Standards Planning And Requirements Committee: komitet przy ANSI, który w 1975 zaproponował 3-poziomową architekturę baz danych.

**3-poziomowa architektura ANSI/SPARC:**

    Poziom zewnętrzny  — CO widzi użytkownik/aplikacja (widoki, podzbiory danych)
    Poziom konceptualny — JAKA jest struktura danych (tabele, kolumny, relacje)
    Poziom wewnętrzny  — JAK dane są fizycznie przechowywane (pliki, indeksy, bloki)

Dzięki tym 3 poziomom zmiany na jednym poziomie NIE wymuszają zmian na innych.

**Niezależność fizyczna** — zmiana SPOSOBU przechowywania (np. dodanie indeksu, zmiana partycjonowania) nie wymaga zmiany aplikacji.

**Indeks (index)** — struktura pomocnicza przyspieszająca wyszukiwanie (jak indeks w książce — nie czytasz całej książki, szukasz po indeksie). Np. indeks na kolumnie „Nazwisko" pozwala szybko znaleźć studenta po nazwisku, bez przeszukiwania milionów wierszy. Dodanie/usunięcie indeksu NIE zmienia danych ani zapytań SQL — aplikacja działa tak samo, tylko szybciej.

**Partycjonowanie (partitioning)** — podział dużej tabeli na mniejsze kawałki (partycje). Np. tabela Zamówienia podzielona na partycje wg roku: 2024, 2025, 2026. Zapytanie o 2025 przeszukuje TYLKO tę partycję. Zmiana partycjonowania jest przezroczysta dla aplikacji.

**Niezależność logiczna** — zmiana struktury tabel minimalizuje wpływ na aplikacje. Np. rozdzielasz tabelę StudentKursy na Studenci + Zapisy, ale tworzysz **widok (view)** = „wirtualna tabela" symulująca starą strukturę. Aplikacja dalej pyta o ten sam widok — dla niej nic się nie zmieniło.

**Jak to odpowiada na pytanie:** System może EWOLUOWAĆ (rosnąć, zmieniać strukturę, optymalizować) BEZ przepisywania aplikacji. Baza oddziela „co" od „jak" → elastyczny fundament.

---

**Współbieżność (concurrency)** — wielu użytkowników/procesów operuje na bazie JEDNOCZEŚNIE. Np. 1000 osób kupuje bilety w tym samym momencie. Baza musi zapewnić, że nie sprzedadzą dwóch biletów na to samo miejsce.

**Blokady (locks)** — najprostszy mechanizm: transakcja „blokuje" wiersz/tabelę, inne muszą CZEKAĆ. Np. transakcja aktualizuje saldo Ani → saldo jest zablokowane → Jan nie może go modyfikować, czeka aż Ania skończy. Typy: shared lock (wiele odczytów jednocześnie) vs exclusive lock (tylko jedna transakcja pisze).

**MVCC (Multi-Version Concurrency Control)** — zamiast blokować, baza trzyma WIELE WERSJI danych. Transakcja czyta wersję z momentu swojego startu — nie jest blokowana przez zapis. Np. Jan czyta saldo (wersja sprzed przelewu), Ania jednocześnie przelewa (tworzy nową wersję). Nikt nie czeka!

**Snapshot Isolation** — wariant MVCC: każda transakcja widzi „migawkę" (snapshot) bazy z momentu swojego startu. Nawet jeśli inne transakcje zmieniają dane, ta widzi SPÓJNY obraz z przeszłości. Eliminuje większość problemów z współbieżnym czytaniem.

**Jak to odpowiada na pytanie:** Baza automatycznie zarządza dostępem wielu użytkowników → system może obsługiwać setki/tysiące jednoczesnych połączeń bez ręcznego pisania mechanizmów synchronizacji.

---

**Integralność (integrity)** — dane w bazie ZAWSZE spełniają zdefiniowane reguły. Baza SAMA pilnuje reguł — nie trzeba ich sprawdzać w kodzie aplikacji.

**Klucze obce (foreign keys, FK)** — wiersz w tabeli MUSI odnosić się do istniejącego wiersza w innej tabeli. Np. Zamówienia.KlientID MUSI wskazywać na istniejącego klienta w tabeli Klienci. Nie możesz wstawić zamówienia dla klienta „999" jeśli nie ma klienta o ID 999. NIE możesz usunąć klienta, który ma zamówienia.

**CHECK** — ograniczenie na wartości kolumny. Np. `CHECK (wiek >= 0 AND wiek <= 150)` — baza ODRZUCI próbę wstawienia osoby z wiekiem −5 lub 200. `CHECK (status IN ('aktywny', 'nieaktywny'))` — nie wpiszesz statusu „cokolwiek".

**Trigger (wyzwalacz)** — fragment kodu uruchamiany AUTOMATYCZNIE, gdy coś się dzieje w bazie. Np. `AFTER INSERT ON Zamówienia` → automatycznie zmniejsz stan magazynowy produktu. Trigger „pilnuje" reguł, których nie da się wyrazić samym CHECK-iem.

**Procedura składowana (stored procedure)** — funkcja zapisana W BAZIE (nie w aplikacji), wywoływana z SQL. Np. `CALL przelejPieniadze(101, 102, 500)` — cała logika przelewu w jednym miejscu, współdzielona przez wszystkie aplikacje.

**Jak to odpowiada na pytanie:** Reguły biznesowe (np. „nie sprzedawaj produktu z zerowym stanem") wymuszane PRZEZ bazę, nie PRZEZ aplikację → nawet jeśli ktoś napisze błędną aplikację, baza nie pozwoli złamać reguł.

---

**Optymalizator zapytań (query optimizer)** — moduł bazy, który automatycznie wybiera NAJSZYBSZY sposób wykonania zapytania SQL. Programista pisze CO chce (`SELECT ... WHERE ...`), a optymalizator decyduje JAK to zrobić (np. użyć indeksu czy przeszukać całą tabelę, w jakiej kolejności łączyć tabele). **Plan wykonania (execution plan)** — sekwencja kroków, którą baza wykona. Np. „użyj indeksu na Nazwisko → odfiltruj wiersze → posortuj".

**Jak to odpowiada na pytanie:** Programista nie musi znać struktury fizycznej danych. Pisze prosty SQL, a baza SAMA optymalizuje → szybkość „za darmo".

---

**Bezpieczeństwo (security):**

**GRANT/REVOKE** — polecenia SQL do nadawania/odbierania uprawnień. Np. `GRANT SELECT ON Studenci TO Dziekanat` — dziekanat może CZYTAĆ studentów, ale nie modyfikować. `REVOKE INSERT ON Zamówienia FROM Praktykant` — praktykant nie może dodawać zamówień.

**Role** — grupy uprawnień. Zamiast nadawać uprawnienia każdemu użytkownikowi osobno, tworzysz rolę (np. „Kasjer") i przypisujesz ją użytkownikom. Kasjer = SELECT + INSERT na Zamówienia, ale bez dostępu do tabeli Pracownicy.

**Szyfrowanie (encryption)** — dane na dysku i w transmisji zamienione na nieczytelny ciąg, który wymaga klucza do odszyfrowania. TDE (Transparent Data Encryption) = szyfrowanie „przezroczyste" — aplikacja nie wie, że dane są szyfrowane.

**Audyt (audit)** — baza rejestruje KTO, KIEDY, CO zrobił. Np. „użytkownik Kowalski zmodyfikował saldo klienta 123 o 15:42". Niezbędne dla zgodności z prawem (RODO, SOX, PCI-DSS).

**Jak to odpowiada na pytanie:** Baza chroni dane przez kontrolę dostępu, szyfrowanie i śledzenie zmian → fundament bezpieczeństwa systemu.

---

**Skalowalność (scalability)** — zdolność systemu do ROŚNIĘCIA (więcej danych, więcej użytkowników) bez utraty wydajności.

**Replikacja (replication)** — kopia bazy na wielu serwerach. Np. master (zapis) + 3 repliki (odczyt). 80% zapytań to odczyty → rozkładasz je na repliki. Jeśli master padnie, replika przejmuje rolę.

**Sharding (fragmentacja)** — podział danych na kawałki (shardy) na RÓŻNYCH serwerach. Np. klienci A–M na serwerze 1, N–Z na serwerze 2. Każdy serwer przechowuje i obsługuje MNIEJSZY zbiór danych → szybciej.

**Klaster (cluster)** — grupa serwerów pracujących RAZEM jako jeden system. Np. klaster PostgreSQL Citus albo MySQL NDB Cluster — z zewnątrz wygląda jak jedna baza, ale fizycznie to wiele maszyn.

**Jak to odpowiada na pytanie:** System może obsłużyć od 10 do 10 000 000 użytkowników bez zmiany architektury aplikacji → baza rośnie razem z systemem.

---

**SQL (Structured Query Language)** — standardowy język zapytań do baz relacyjnych. TEN SAM SQL działa (z drobnymi różnicami) w PostgreSQL, MySQL, Oracle, SQL Server, SQLite. Programista, który zna SQL, może pracować z KAŻDĄ z tych baz.

**Jak to odpowiada na pytanie:** Jeden uniwersalny interfejs → łatwość wymiany bazy danych, łatwe znalezienie programistów, bogactwo narzędzi, ORM-ów i bibliotek. Nie trzeba uczyć się osobnego języka dla każdego systemu.

---

### 1. Transakcyjność ACID

| Właściwość | Znaczenie |
|------------|-----------|
| **A**tomicity | Transakcja — albo cała, albo nic |
| **C**onsistency | Spójny stan → spójny stan |
| **I**solation | Równoległe transakcje nie interferują |
| **D**urability | Zatwierdzone zmiany przetrwają awarię |

### 2. Niezależność danych (3-poziomowa architektura ANSI/SPARC)

- **Fizyczna:** zmiana indeksów/partycjonowania nie wpływa na aplikacje
- **Logiczna:** zmiana schematu minimalizuje wpływ na aplikacje (widoki)

### 3. Współbieżność — mechanizmy: blokady, MVCC, snapshot isolation

### 4. Integralność — klucze obce, CHECK, triggery, procedury składowane

### 5. Optymalizator zapytań — automatyczny wybór planu wykonania

### 6. Bezpieczeństwo — GRANT/REVOKE, role, szyfrowanie, audyt

### 7. Skalowalność — replikacja, sharding, klastry

### 8. Standardowy interfejs — SQL jako uniwersalny język zapytań

### Etymologia

**ACID** — akronim: Reuter & Härder (1983); celowo łatwy do zapamiętania. **ANSI/SPARC** — American National Standards Institute / Standards Planning And Requirements Committee (1975). **SQL** — oryginalnie SEQUEL (Structured English Query Language, Chamberlin & Boyce, IBM 1974); zmieniono na SQL przez konflikt znaku towarowego. **MVCC** — Multi-Version Concurrency Control. **Transakcja** — łac. „transactio" = doprowadzenie do końca.

### Jak zapamiętać

- **ACID** — zapamiętaj przelew bankowy: bez A tracisz pieniądze, bez C saldo < 0, bez I widać stan pośredni, bez D znika po crashu
- **„DB = centralne źródło prawdy"** — jedna baza vs. pliki rozproszone po systemach
- Kluczowe słowa: trwałość, współbieżność, integralność, niezależność

\newpage

## PYTANIE 5: Kategorie STL (PROI)

**Omówić główne kategorie elementów biblioteki STL.**

---

### Tło pojęciowe — słowniczek

**STL (Standard Template Library)** — część standardowej biblioteki C++ zawierająca gotowe struktury danych i algorytmy. „Template" = szablonowa: działa z DOWOLNYM typem danych (int, string, własna klasa) dzięki mechanizmowi templates (generyczność). Zamiast pisać osobno „sortuj tablicę intów" i „sortuj tablicę stringów", piszesz RAZ `sort<T>` i działa dla WSZYSTKIEGO.

**Template (szablon)** — mechanizm C++: piszesz kod raz z „placeholder-em" na typ, a kompilator generuje wersję dla każdego użytego typu. Np. `vector<int>`, `vector<string>` — ten sam kod wewnętrznie, ale dla różnych typów.

---

### Cztery filary — dlaczego akurat te cztery?

**Kontener (container)** — struktura danych przechowująca kolekcję elementów. „CO przechowujemy". Jak pudełko na dane: vector to tablica, map to słownik, set to zbiór.

**Iterator** — obiekt wskazujący na element w kontenerze, umożliwiający przechodzenie (iterowanie) po elementach. „JAK się poruszamy po danych". Jak kursor/wskaźnik, który może iść do przodu, do tyłu, lub skoczyć na dowolną pozycję (zależy od typu iteratora).

**Algorytm (algorithm)** — gotowa OPERACJA na danych: sortowanie, wyszukiwanie, kopiowanie, zliczanie itp. „CO ROBIMY z danymi". STL daje ~100 gotowych algorytmów.

**Funktor (function object)** — obiekt, który zachowuje się jak funkcja (ma operator `()`). Służy do PARAMETRYZACJI algorytmów = mówi algorytmowi JAK porównywać, JAK przekształcać. Np. `sort` domyślnie sortuje rosnąco, ale funktor `greater<int>` zmieni to na malejąco.

**Operacje i parametryzacja** — algorytmy to operacje (sort, find, copy), a funktory to parametryzacja (JAK sortować? według jakiego kryterium? jaką transformację zastosować?).

**Dlaczego właśnie te 4 to filary?** — Razem pozwalają wyrażać KAŻDĄ operację na danych:
1. Kontener = gdzie dane leżą
2. Iterator = jak się do nich dobrać
3. Algorytm = co z nimi zrobić
4. Funktor = jak dostosować algorytm

Klucz: algorytmy NIE znają kontenerów. Komunikują się TYLKO przez iteratory. Dzięki temu M kontenerów + N algorytmów wymaga M+N implementacji (nie M×N). To się nazywa **architektura ortogonalna**.

---

### Kontenery — szczegóły

**Kontenery sekwencyjne** — elementy mają POZYCJĘ (kolejność ma znaczenie). Jak tablica, lista, kolejka.

**vector (tablica dynamiczna)** — ciągły blok pamięci, jak tablica C, ale automatycznie rośnie. Dostęp do i-tego elementu: O(1) (bo pamięć ciągła). Dodawanie na końcu: zamortyzowane O(1). Wstawianie w środku: O(n) (trzeba przesunąć elementy). **Domyślny wybór** — najszybszy dzięki ciągłej pamięci (cache-friendly).

    vector<int> v = {10, 20, 30, 40};
    v[2];          // 30 — dostęp O(1)
    v.push_back(50); // dodaj na końcu O(1)
    // Pamięć: [10|20|30|40|50] — ciągły blok

**Co to jest „pamięć ciągła" (contiguous memory)?**

Elementy leżą OBOK SIEBIE w RAM, jeden za drugim, bez przerw:

    Adres:  1000  1004  1008  1012  1016
    Dane:   [10]  [20]  [30]  [40]  [50]
            ↑ baza

    Adres i-tego elementu = baza + i × rozmiar_elementu
    v[0] = adres 1000 + 0×4 = 1000 → 10
    v[2] = adres 1000 + 2×4 = 1008 → 30
    v[99]= adres 1000 + 99×4= 1396 → ???

    To JEDNO mnożenie i JEDNO dodawanie — zawsze tyle samo,
    niezależnie czy tablica ma 5 czy 5 000 000 elementów → O(1).

W liście NIE MA ciągłej pamięci — węzły rozrzucone po całym RAM:

    Adres:  1000       5040       2200
    Dane:   [10]→5040  [20]→2200  [30]→null
    Żeby znaleźć element 2: 1000→5040→2200 = 2 skoki → O(n)

Dodatkowo ciągła pamięć jest **cache-friendly**: CPU ładuje pamięć blokami (cache lines, 64B). Przy vector cały blok to przydatne dane. Przy list każdy skok to potencjalny cache miss → ~10-100× wolniej.

**deque (Double-Ended QUEue)** — kolejka dwustronna. Szybkie dodawanie/usuwanie NA OBU KOŃCACH: O(1). Wewnętrznie: tablica wskaźników do bloków pamięci (nie jeden ciągły blok). Dostęp O(1) ale nieco wolniejszy niż vector (extra pośredniość).

    deque<int> d = {10, 20, 30};
    d.push_front(5);  // O(1) — dodaj z przodu
    d.push_back(40);  // O(1) — dodaj z tyłu
    // [5|10|20|30|40]

**list (lista dwukierunkowa)** — każdy element to węzeł z wskaźnikami do POPRZEDNIEGO i NASTĘPNEGO. Wstawianie/usuwanie w dowolnym miejscu: O(1) (jeśli masz iterator na to miejsce). Brak dostępu po indeksie! Żeby dostać 5. element, musisz przejść 5 kroków od początku.

    list<int> l = {10, 20, 30};
    // 10 ↔ 20 ↔ 30  (dwukierunkowe wskaźniki)
    auto it = l.begin(); advance(it, 1); // idź na pozycję 1
    l.insert(it, 15);   // O(1): 10 ↔ 15 ↔ 20 ↔ 30

**Dlaczego wstawianie to O(1)?** Bo wystarczy „przepiąć" 2 wskaźniki:

    PRZED: ... ↔ [A|→B] ↔ [B|→C] ↔ ...
    Wstaw X między A i B:
    1. X.next = B
    2. X.prev = A
    3. A.next = X
    4. B.prev = X
    POTEM: ... ↔ [A|→X] ↔ [X|→B] ↔ [B|→C] ↔ ...
    4 operacje — zawsze tyle samo, niezależnie od rozmiaru listy → O(1).

**forward_list (lista jednokierunkowa)** — jak list, ale każdy węzeł ma wskaźnik TYLKO do NASTĘPNEGO (nie do poprzedniego). Mniej pamięci niż list, ale nie da się cofać. Iteracja tylko DO PRZODU.

    forward_list<int> fl = {10, 20, 30};
    // 10 → 20 → 30  (tylko w przód)

**array (tablica stała)** — tablica o STAŁYM rozmiarze (znanym w czasie kompilacji). Jak tablica C, ale z interfejsem STL. Rozmiar nie może się zmienić. Najszybsza — zero narzutu.

    array<int, 4> a = {10, 20, 30, 40};  // rozmiar 4, stały

---

**Kontenery asocjacyjne** — elementy przechowywane w POSORTOWANEJ kolejności. Wyszukiwanie po kluczu: O(log n). Wewnętrznie: **drzewo czerwono-czarne (R-B tree)** — zbalansowane drzewo binarne.

**Dlaczego O(log n)?** Drzewo binarne dzieli dane na pół przy każdym kroku:

    set z 1000 elementów → drzewo głębokości ~10
    Szukam 42: idę lewo/prawo 10 razy → znalezione
    set z 1 000 000 elementów → głębokość ~20
    Szukam 42: 20 kroków → znalezione
    log₂(1000)≈10, log₂(1000000)≈20 — to jest O(log n)

**set** — zbiór UNIKALNYCH wartości, posortowany. Dodanie, usunięcie, wyszukiwanie: O(log n).

    set<int> s = {30, 10, 20, 10};
    // Przechowuje: {10, 20, 30} — posortowane, bez duplikatów

**multiset** — jak set, ale POZWALA na duplikaty.

    multiset<int> ms = {30, 10, 20, 10};
    // Przechowuje: {10, 10, 20, 30} — posortowane, z duplikatami

**Po co multiset? Czym różni się od vector?**

multiset to posortowany zbiór Z duplikatami. Zastosowania:
- zliczanie wystąpień: ms.count(10) → 2 (ile razy 10 się pojawia) — O(log n)
- zakresowe zapytania: ms.lower_bound(15) → iterator na 20 — O(log n)
- mediana, percentyle: dane zawsze posortowane

Porównanie z vector:

    Operacja              vector    multiset
    ──────────────────────────────────────────
    Szukanie elementu     O(n)      O(log n)  ← vector musi przejrzec cały
    Wstawianie w porz.    O(n)      O(log n)  ← vector musi przesunąć el.
    Dostęp po indeksie    O(1)      BRAK      ← multiset nie ma []
    Pamięć                ciągła    rozrzucona ← vector jest cache-friendly
    Automatyczne sort.    NIE       TAK

Kiedy multiset: dane napływają strumieniowo, chcesz je mieć ZAWSZE posortowane i szybko szukać. Kiedy vector: potrzebujesz indeksu [] i iterujesz sekwencyjnie.

**map** — słownik: pary (klucz → wartość), klucze UNIKALNE i posortowane. Dostęp po kluczu: O(log n).

    map<string, int> m = {{"Anna", 5}, {"Jan", 4}};
    m["Anna"];   // 5 — wyszukiwanie O(log n)

**multimap** — jak map, ale jeden klucz może mieć WIELE wartości.

---

**Kontenery nieuporządkowane (hash)** — wewnętrznie: **tablica haszująca**. Funkcja haszująca zamienia klucz na indeks w tablicy → dostęp O(1) ŚREDNIO. Najgorszy przypadek (kolizje): O(n). Elementy NIE są posortowane.

**Dlaczego O(1)?** Hash to „adres kalkulowany":

    Mamy tablicę 8 kubełków [0..7]:
    hash("Anna") = 5 → idź od razu do kubełka 5 → znalezione
    hash("Jan")  = 2 → idź od razu do kubełka 2 → znalezione
    
    Nie trzeba przeszukiwać niczego — JEDNO obliczenie → JEDEN skok.
    Kolizja: hash("Ola") = 5 = ten sam co Anna → O(n) w najgorszym przypadku.

**unordered_set** — zbiór unikalnych wartości, BEZ sortowania. Szukanie O(1) średnio.

**unordered_map** — słownik, BEZ sortowania kluczy. Dostęp O(1) średnio.

    unordered_map<string, int> um = {{"Anna", 5}, {"Jan", 4}};
    um["Anna"];  // 5 — O(1) średnio (hash)

Kiedy set/map, kiedy unordered? Posortowane dane lub iteracja w kolejności → set/map (O(log n)). Szybkie wyszukiwanie bez porządku → unordered (O(1)).

---

**Adaptery kontenerów** — NIE są „prawdziwymi" kontenerami — opakowują inny kontener i ograniczają jego interfejs.

**stack (stos)** — LIFO (Last In, First Out). Dostęp TYLKO do szczytu: push (wrzuć), pop (zdejmij), top (popatrz na szczyt). Domyślnie opakowuje deque.

    stack<int> s;
    s.push(10); s.push(20); s.push(30);
    s.top();   // 30 (ostatni dodany)
    s.pop();   // usuwa 30

**queue (kolejka)** — FIFO (First In, First Out). Dodajesz z tyłu, zdejmujesz z przodu. Jak kolejka w sklepie.

    queue<int> q;
    q.push(10); q.push(20); q.push(30);
    q.front();  // 10 (pierwszy dodany)
    q.pop();    // usuwa 10

**priority_queue (kolejka priorytetowa)** — zawsze wyciąga element o NAJWYŻSZYM priorytecie (domyślnie największy). Wewnętrznie: heap (kopiec). Push/pop: O(log n).

    priority_queue<int> pq;
    pq.push(10); pq.push(30); pq.push(20);
    pq.top();   // 30 (największy)
    pq.pop();   // usuwa 30, teraz top = 20

---

### Iteratory — szczegóły

**Wskaźnik (pointer)** — zmienna przechowująca adres w pamięci. Iterator to UOGÓLNIONY wskaźnik: działa jak wskaźnik (de-referencja `*it`, inkrementacja `++it`), ale może obsługiwać dowolną strukturę danych, nie tylko tablice.

**Hierarchia iteratorów** — każdy kolejny typ DODAJE możliwości:

**Input Iterator** — jednokrotny odczyt, tylko do przodu. Jak czytanie ze strumienia: raz odczytane, nie wrócisz. Np. `istream_iterator`.

**Output Iterator** — jednokrotny zapis, tylko do przodu. Np. `ostream_iterator`.

**Forward Iterator** — odczyt/zapis, do przodu, WIELOKROTNE przejścia. Np. `forward_list::iterator`.

**Bidirectional Iterator** — jak Forward + cofanie (`--it`). Np. `list::iterator`, `set::iterator`.

**Random Access Iterator** — jak Bidirectional + skok na DOWOLNĄ pozycję (`it + 5`, `it[3]`). Np. `vector::iterator`, `deque::iterator`.

**Contiguous Iterator** (C++17) — jak Random Access + gwarantowane SĄSIEDZTWO w pamięci. Np. `vector::iterator`, `array::iterator`.

**Dlaczego vector = Random Access?** — Pamięć ciągła: adres i-tego elementu = baza + i × rozmiar. Skok na pozycję 1000 to jedno dodanie — O(1). `vec.begin() + 1000` działa natychmiast.

**Dlaczego list = Bidirectional?** — Lista dwukierunkowa: węzły połączone wskaźnikami prev/next. Możesz iść do przodu (`++it`) i do tyłu (`--it`). Ale NIE możesz „skoczyć" na pozycję 1000 — musisz przejść 1000 kroków, bo nie ma ciągłej pamięci.

**Dlaczego forward_list = Forward?** — Lista jednokierunkowa: każdy węzeł ma TYLKO wskaźnik „next". Możesz iść TYLKO do przodu (`++it`). Nie da się cofnąć (`--it`) — brak wskaźnika wstecz.

**Dlaczego hierarchia ma znaczenie?** — Algorytmy WYMAGAJĄ minimalnej kategorii iteratora:
- `find` potrzebuje Input (wystarczy jeden przebieg)
- `reverse` potrzebuje Bidirectional (musi cofać się)
- `sort` potrzebuje Random Access (musi skakać po pozycjach)

Dlatego NIE MOŻNA `sort(mylist.begin(), mylist.end())` — list daje Bidirectional, a sort wymaga Random Access. Lista ma własny `mylist.sort()`.

---

### Algorytmy — szczegóły

**Zakres [begin, end)** — algorytmy operują na PARZE iteratorów: begin = pierwszy element, end = JEDEN ZA OSTATNIM (nie sam ostatni!). Pozwala elegancko wyrażać puste zakresy i podzakresy.

**sort** — sortuje elementy. Wymaga Random Access. Złożoność: O(n log n). Domyślnie rosnąco.

**find** — szuka pierwszego elementu równego wartości. Wymaga Input. O(n).

**transform** — przekształca każdy element (jak map w Pythonie). Np. pomnóż każdy × 2.

**copy** — kopiuje elementy z jednego zakresu do drugiego.

**accumulate** — „zwijanie" zakresu do jednej wartości (jak fold/reduce). Np. suma, iloczyn.

**count_if** — zlicza elementy spełniające warunek (predykat).

**remove_if** — przenosi elementy niespełniające warunku na początek (nie usuwa fizycznie!).

    vector<int> v = {3, 1, 4, 1, 5};
    sort(v.begin(), v.end());             // {1, 1, 3, 4, 5}
    find(v.begin(), v.end(), 4);          // iterator na 4
    count_if(v.begin(), v.end(),
             [](int x){return x > 2;});  // 3 (bo: 3, 4, 5)
    accumulate(v.begin(), v.end(), 0);    // 14 (suma)

**Kluczowa cecha:** algorytmy nie wiedzą, CZY dane leżą w vector, list, deque — widzą TYLKO iteratory. Dlatego TEN SAM `find` działa na vector, na set, na deque.

---

### Funktory i lambdy — szczegóły

**Funktor (obiekt funkcyjny)** — klasa/struct z overloadowanym `operator()`. Można ją „wywoływać" jak funkcję.

    struct Podwoj {
        int operator()(int x) { return x * 2; }
    };
    Podwoj f;
    f(5);    // 10 — wygląda jak wywołanie funkcji, ale to obiekt

**Wbudowane funktory STL:**
- `less<int>` — porównuje `a < b` (domyślne sortowanie rosnące)
- `greater<int>` — porównuje `a > b` (sortowanie malejące)
- `plus<int>` — oblicza `a + b`

    sort(v.begin(), v.end(), greater<int>());  // sortuj MALEJĄCO

**Lambda (C++11)** — anonimowa (bezimienна) funkcja definiowana w miejscu użycia. Zastępuje ręczne pisanie funktorów.

    [capture](parametry) { ciało }

    sort(v.begin(), v.end(), [](int a, int b){ return a > b; });
    // To samo co greater<int>(), ale inline

**Parametryzacja** = funktor/lambda mówi algorytmowi JAK działać:
- sort + less → sortuj rosnąco
- sort + greater → sortuj malejąco
- sort + custom lambda → sortuj po dowolnym kryterium (np. długość stringa)

---

### Architektura ortogonalna — szczegóły

**Ortogonalność** — komponenty są NIEZALEŻNE. Kontenery nie wiedzą o algorytmach. Algorytmy nie wiedzą o kontenerach. Łącznikiem są iteratory.

Bez ortogonalności: M kontenerów × N algorytmów = **M×N** implementacji (sort dla vector, sort dla list, sort dla deque, find dla vector...). Z ortogonalnością: **M + N** implementacji — każdy kontener daje iteratory, każdy algorytm operuje na iteratorach.

    // TEN SAM algorytm, RÓŻNE kontenery:
    sort(vec.begin(), vec.end());        // vector
    sort(deq.begin(), deq.end());        // deque
    // (list ma własny sort, bo sort wymaga Random Access)

    // TEN SAM kontener, RÓŻNE algorytmy:
    sort(vec.begin(), vec.end());
    find(vec.begin(), vec.end(), 42);
    reverse(vec.begin(), vec.end());

---

### Etymologia

**STL** — Standard Template Library; Alexander Stepanov + Meng Lee (HP, 1994); Stepanov od lat 70. marzył o programowaniu generycznym. **Iterator** — łac. „iter" = podróż/ścieżka; ten, kto przemierza kolekcję. **Funktor** — z teorii kategorii (matematyka); obiekt zachowujący się jak funkcja. **Deque** — Double-Ended QUEue. **Vector** — łac. „vector" = nośnik; tablica dynamiczna. **Lambda** — od greckiej litery λ; Alonzo Church, rachunek lambda (1930s).

### Jak zapamiętać

- **„KIAF"** — Kontenery, Iteratory, Algorytmy, Funktory
- **Ortogonalność:** algorytmy + kontenery połączone iteratorami
- **vector** — domyślny wybór; list gdy dużo insert/erase w środku; map/set gdy potrzebne sortowanie i wyszukiwanie

\newpage

## PYTANIE 6: Reużywalność kodu w OOP (PROI)

**Omówić metody reużywalności kodu i struktur danych w obiektowych językach programowania.**

---

### Tło pojęciowe — słowniczek

**OOP (Object-Oriented Programming / Programowanie obiektowe)** — paradygmat, w którym program składa się z obiektów łączących dane (pola) i zachowanie (metody). Cztery filary: enkapsulacja, dziedziczenie, polimorfizm, abstrakcja. W kontekście pytania — to OOP wprowadza mechanizmy ponownego użycia kodu omawiane poniżej.

**Klasa (class)** — „wzorzec" (blueprint) obiektu. Definiuje pola i metody. Obiekt to konkretna instancja klasy.

    class Dog {          // klasa
        string name;
        void bark();
    };
    Dog rex;             // obiekt (instancja)

**Reużywalność kodu (code reuse)** — możliwość wykorzystania raz napisanego kodu w wielu miejscach bez kopiowania. Zmniejsza ilość duplikatów, ułatwia utrzymanie i redukuje błędy. To główny temat pytania.

---

**Dziedziczenie (inheritance)** — mechanizm, w którym klasa pochodna (child) przejmuje pola i metody klasy bazowej (parent). Relacja „jest" (is-a): Dog **jest** Animal.

    class Animal { void eat(); };
    class Dog : public Animal { void bark(); };
    // Dog ma eat() + bark()

**Klasa bazowa / pochodna (base class / derived class)** — bazowa = rodzic, pochodna = dziecko. Pochodna dziedziczy interfejs i implementację bazowej, może dodawać własne lub nadpisywać istniejące metody.

**Dziedziczenie wielokrotne (multiple inheritance)** — klasa dziedziczy po więcej niż jednym rodzicu. Dostępne w C++, ale nie w Java/C# (tam tylko interfejsy). Powoduje ryzyko konfliktu nazw i problem diamentu.

**Problem diamentu (diamond problem)** — gdy klasa D dziedziczy po B i C, a oba dziedziczą po A, D ma dwie kopie A. Pytanie: której użyć?

         A
        / \
       B   C
        \ /
         D     ← dwie kopie A!

Rozwiązanie w C++: dziedziczenie wirtualne (`class B : virtual public A`), dzięki czemu istnieje jedna kopia A.

**Polimorfizm (polymorphism)** — grec. „wiele form". Możliwość traktowania obiektów różnych klas przez wspólny interfejs. Kluczowy dla reużywalności — piszesz kod raz, działa z wieloma typami.

    Animal* a = new Dog();
    a->speak();  // woła Dog::speak(), nie Animal::speak()
    // To samo wywołanie, różne zachowanie — polimorfizm

Realizacja: funkcje wirtualne (`virtual` + `override`) — tablica vtable wskazuje na właściwą implementację.

---

**Kompozycja (composition)** — obiekt zawiera inne obiekty jako pola. Relacja „ma" (has-a). Stack **ma** wektor (nie **jest** wektorem). Silniejsza enkapsulacja niż dziedziczenie, bo wnętrze komponentu jest ukryte.

    class Engine { int hp; };
    class Car {
        Engine engine;   // kompozycja: Car "ma" Engine
    };

**„Favor composition over inheritance"** — zasada GoF: preferuj kompozycję nad dziedziczenie. Dziedziczenie tworzy silne wiązanie (zmiana bazowej łamie pochodne). Kompozycja pozwala wymieniać części w runtime.

**Agregacja (aggregation)** — słabsza forma kompozycji: obiekt „używa" innego, ale go nie posiada. Samochód ma kierowcę, ale kierowca istnieje niezależnie. W UML: pusty romb (◇).

**Enkapsulacja (encapsulation)** — ukrywanie szczegółów implementacji za interfejsem publicznym. Zapewnia, że obiekt kontroluje dostęp do swoich danych (private, protected, public).

**Luźne wiązanie (loose coupling)** — komponenty mają minimum zależności między sobą. Zmiana jednego nie wymusza zmian w drugim. Kompozycja daje luźniejsze wiązanie niż dziedziczenie.

---

**Programowanie generyczne (generic programming)** — pisanie kodu niezależnego od konkretnego typu danych. Jedna implementacja działa dla int, float, string itd.

**Template (szablon, C++)** — mechanizm generyczny w C++. Kompilator generuje osobną wersję kodu dla każdego użytego typu (monomorfizacja).

    template<typename T>
    T max(T a, T b) { return a > b ? a : b; }
    max(3, 5);       // T = int
    max(1.5, 2.7);   // T = double

**Generics (Java/C#)** — odpowiednik templates, ale z type erasure (Java) lub reifikacją (C#). `List<String>` — lista przechowująca tylko stringi; bezpieczeństwo typów bez duplikowania kodu.

**STL (Standard Template Library)** — biblioteka C++ oparta na templates: kontenery (`vector`, `map`), algorytmy (`sort`, `find`), iteratory. Przykład reużywalności: jeden `sort()` sortuje dowolny kontener.

---

**Interfejs (interface)** — kontrakt: zbiór metod bez implementacji. Klasa implementująca interfejs musi dostarczyć ciała wszystkich metod. W C++ → czysto wirtualne metody (`= 0`); w Java/C# → `interface`.

    // C++
    class Drawable {
    public:
        virtual void draw() = 0;  // pure virtual = interfejs
    };

**Klasa abstrakcyjna (abstract class)** — klasa, której nie można instancjonować; może mieć zarówno metody abstrakcyjne, jak i z implementacją. Interfejs = 100% abstrakcyjna.

**Wzorce projektowe (design patterns)** — sprawdzone, reużywalne rozwiązania typowych problemów projektowych. Opisane jako: Nazwa + Problem + Rozwiązanie + Konsekwencje.

**GoF (Gang of Four)** — Gamma, Helm, Johnson, Vlissides — autorzy książki „Design Patterns" (1994) z 23 wzorcami w trzech kategoriach: kreacyjne, strukturalne, behawioralne.

**Strategy** — wzorzec: wymień algorytm w runtime przez interfejs. Np. różne strategie sortowania.
**Observer** — wzorzec: obiekt powiadamia subskrybentów o zmianach stanu (pub/sub w OOP).
**Factory** — wzorzec: tworzenie obiektów bez określania dokładnej klasy (decyzja w runtime).
**Decorator** — wzorzec: dodaj zachowanie do obiektu dynamicznie, opakowując go.

**Biblioteka (library)** — zbiór reużywalnego kodu wywoływanego przez nasz program (my code calls library).
**Framework** — odwrotność: framework wywołuje nasz kod (Inversion of Control). Np. Unity, Django.
**Trait / Mixin** — mechanizm współdzielenia kodu między klasami bez dziedziczenia. Trait (Rust, Scala) = zbiór metod do „wmixowania". Mixin (Ruby, Python) = klasa dodająca funkcjonalność przez wielodziedziczenie.

---

### Główne metody

### 1. Dziedziczenie (Inheritance) — relacja „jest" (is-a)
- Klasa pochodna przejmuje atrybuty i metody bazowej
- Typy: pojedyncze, wielokrotne, wielopoziomowe
- Problem diamentu → dziedziczenie wirtualne w C++
- Polimorfizm (virtual, override)

### 2. Kompozycja (Composition) — relacja „zawiera" (has-a)
- **„Favor composition over inheritance"**
- Stack nie JEST wektorem → Stack ZAWIERA wektor
- Silniejsza enkapsulacja, luźne wiązanie
- Typy: kompozycja (owns), agregacja (uses), asocjacja (knows)

### 3. Programowanie generyczne (Templates/Generics)
- Kod niezależny od typu: `template<typename T> T max(T a, T b)`
- STL jest oparta na templates
- Java/C#: Generics (`List<T>`)

### 4. Interfejsy i klasy abstrakcyjne
- Kontrakt bez implementacji (pure virtual w C++, interface w Java)
- Umożliwiają multiple inheritance bez diamond problem

### 5. Wzorce projektowe (Design Patterns)
- Strategy, Observer, Factory, Decorator — reużywalne rozwiązania
- GoF (Gang of Four) — 23 wzorce

### 6. Biblioteki, frameworki, traity/mixiny

### Etymologia

**OOP** — Alan Kay (Smalltalk, 1970s), sam ukuł termin „object-oriented". **GoF** — Gang of Four: Gamma, Helm, Johnson, Vlissides (1994). **Polimorfizm** — grec. „poly" (wiele) + „morphē" (forma) = wiele postaci. **Enkapsulacja** — łac. „capsula" = pudełeczko. **Design Pattern** — z architektury: Christopher Alexander „A Pattern Language" (1977); GoF zaadaptowali do IT. **Kompozycja > Dziedziczenie** — zasada z GoF: „favor object composition over class inheritance".

### Jak zapamiętać

- **„Kompozycja > Dziedziczenie"** — najważniejsza zasada
- Dziedziczenie: silne wiązanie, krucha klasa bazowa, diamond problem
- Kompozycja: elastyczna, testowalna, preferowan
- Granica: dziedziczenie dla prawdziwego „is-a" z polimorfizmem; kompozycja dla reszty

\newpage

## PYTANIE 7: DNS i caching (SKM)

**Które serwery DNS zyskują najwięcej na cachingu? Jakie znasz rodzaje serwerów DNS?**

---

### Tło pojęciowe — słowniczek

**DNS (Domain Name System)** — rozproszony system tłumaczący nazwy domenowe (np. `google.com`) na adresy IP (np. `142.250.74.206`). Bez DNS musielibyśmy zapamiętywać ciągi liczb zamiast nazw. Struktura hierarchiczna: root → TLD → domeny → subdomeny.

    google.com.        ← końcowa kropka = root
    │      │
    │      └── TLD (.com)
    └── domena II poziomu (google)

**Serwer DNS** — komputer odpowiadający na zapytania o adresy IP. Istnieje kilka typów o różnych rolach w hierarchii (root, TLD, authoritative, recursive, stub, forwarding).

**Cache (pamięć podręczna)** — szybki bufor przechowujący niedawne odpowiedzi. Zamiast pytać hierarchię DNS od zera, resolver sprawdza cache. Trafienie w cache = odpowiedź w <1 ms zamiast ~50-200 ms podróży przez internet.

**Caching DNS** — mechanizm zapisywania odpowiedzi DNS na określony czas (TTL). Kluczowy dla wydajności — bez caching root servers byłyby przeciążone miliardami zapytań dziennie.

---

**Root server (serwer główny)** — najwyższy poziom hierarchii DNS. 13 logicznych serwerów (a.root-servers.net … m.root-servers.net), ale setki fizycznych instancji rozproszonych po świecie (anycast). Nie znają adresów konkretnych domen — odsyłają (referral) do serwerów TLD.

**TLD server (Top-Level Domain)** — serwer obsługujący domeny najwyższego poziomu: .com, .pl, .org, .net itd. Zarządzane przez rejestry (np. Verisign dla .com, NASK dla .pl). Odsyłają do serwerów authoritative konkretnych domen.

**Authoritative NS (serwer autorytatywny)** — serwer znający ostateczne odpowiedzi dla danej domeny. Primary (master) — zawiera oryginalne rekordy (edytowalny); Secondary (slave) — kopia do nadmiarowości. To „źródło prawdy" dla danej domeny.

**Recursive resolver (resolver rekurencyjny)** — serwer wykonujący pełne rozwiązywanie: pyta root → TLD → authoritative, zbiera odpowiedź i zwraca klientowi. Przykłady: Google 8.8.8.8, Cloudflare 1.1.1.1, resolver ISP. To ON głównie korzysta z cache.

**Stub resolver** — prosty klient DNS wbudowany w system operacyjny. Nie rozwiązuje sam — wysyła zapytanie do recursive resolvera i czeka na odpowiedź.

**Forwarding server** — serwer DNS, który nie rozwiązuje sam, lecz przekazuje zapytania do innego resolvera (np. firmowy DNS przekazuje do ISP).

---

**TTL (Time To Live)** — czas w sekundach, przez który odpowiedź DNS może być przechowywana w cache. Po upływie TTL wpis jest usuwany i trzeba zapytać ponownie. Root referrals mają TTL 48h–7 dni; TLD referrals 24h–48h; typowe domeny 300–3600s.

    Przykład: TTL = 3600 → resolver pamięta odpowiedź przez 1 godzinę

**Referral (odesłanie)** — odpowiedź DNS mówiąca „nie wiem, ale zapytaj tamten serwer". Root referral → „zapytaj serwer TLD .com"; TLD referral → „zapytaj NS domeny google.com".

**Anycast** — technika routingu: ten sam adres IP jest ogłaszany z wielu lokalizacji na świecie. Klient automatycznie trafia do najbliższego serwera (routing BGP kieruje do najbliższego). Root servers używają anycast — dlatego 13 adresów obsługuje cały internet.

**ISP (Internet Service Provider)** — dostawca internetu. Zwykle udostępnia własny recursive resolver, z którego korzystają klienci domyślnie.

**Dlaczego ROOT i TLD zyskują NAJWIĘCEJ na cachingu?** Root servers to tylko 13 logicznych adresów dla CAŁEGO internetu. Bez cache każde zapytanie o dowolną domenę musi przejść przez root. Z cache: resolver pyta root RAZ o .com, cachuje referral na 48h+, i przez ten czas miliardy zapytań o domeny .com omijają root. Redukcja ruchu: z ~100% do ~0.01% zapytań.

    Bez cache:     klient → resolver → ROOT → TLD → Auth (za każdym razem!)
    Z cache:       klient → resolver → cache hit! (odpowiedź w <1ms)

---

### Rodzaje serwerów DNS

1. **Root Servers** (.) — 13 logicznych (a..m.root-servers.net), setki fizycznych (anycast)
2. **TLD Servers** (.com, .pl, .org) — zarządzane przez rejestry
3. **Authoritative NS** — Primary (master, edytowalny) i Secondary (slave, kopia)
4. **Recursive Resolvers** — wykonują pełne rozwiązywanie (ISP, Google 8.8.8.8, Cloudflare 1.1.1.1)
5. **Stub Resolvers** — prosty klient w OS, wysyła do recursive
6. **Forwarding Servers** — przekazują zapytania dalej

### Proces rozwiązywania

    Klient → Recursive Resolver → Root → TLD → Authoritative → odpowiedź

### ODPOWIEDŹ: ROOT i TLD zyskują NAJWIĘCEJ na cachingu

**Dlaczego:**
- 13 root servers vs miliardy zapytań dziennie
- BEZ cache: każde zapytanie o DOWOLNĄ domenę musi przejść przez root i TLD
- Z cache: resolver pyta root RAZ o .com, cachuje referral na 48h+
- Root referrals: TTL 48h–7 dni (!); TLD referrals: TTL 24h–48h
- Redukcja ruchu do root: z ~100% do ~0.01% zapytań

### Etymologia

**DNS** — Domain Name System; Paul Mockapetris (1983, RFC 882/883). **Cache** — fr. „cacher" = ukrywać; ukryte szybkie przechowywanie. **TTL** — Time To Live. **Anycast** — ten sam IP z wielu lokalizacji; klient dostaje odpowiedź od najbliższego serwera. **Root servers** — 13 logicznych identyfikatorów (a–m); infrastruktura krytyczna internetu. **Recursive resolver** — „rekurencyjny" bo iteracyjnie pyta kolejne poziomy hierarchii aż do odpowiedzi.

### Jak zapamiętać

- **„Piramida DNS"** — root (wierzchołek, najmniej serwerów) → TLD → Auth (podstawa, miliony)
- Im mniej serwerów na poziomie, tym większy zysk z cache
- **TTL** = Time To Live — im dłuższy, tym rzadziej odświeżany cache

\newpage

## PYTANIE 8: TCP Three-Way Handshake (SKM)

**Cel, interpretacja numerów sekwencyjnych, wartość początkowa ISN.**

---

### Tło pojęciowe — słowniczek

**TCP (Transmission Control Protocol)** — protokół warstwy transportowej zapewniający niezawodne, uporządkowane dostarczanie danych. W przeciwieństwie do UDP, TCP gwarantuje: brak utraty, poprawną kolejność, brak duplikatów. Ceną jest większy narzut (handshake, potwierdzenia, retransmisje).

    Warstwa aplikacji:    HTTP, FTP, SMTP
    Warstwa transportowa: TCP / UDP       ← tu TCP
    Warstwa sieciowa:     IP
    Warstwa łącza:        Ethernet, WiFi

**Połączenie (connection)** — TCP jest protokołem połączeniowym (connection-oriented). Zanim dane popłyną, obie strony muszą ustanowić połączenie — to właśnie robi three-way handshake.

**Segment** — jednostka danych w TCP. Nagłówek TCP (20+ bajtów) + dane. Nagłówek zawiera m.in. porty, numery sekwencyjne, flagi (SYN, ACK, FIN…), window size.

---

**Handshake (uścisk dłoni)** — procedura nawiązywania połączenia. „Three-way" = trzy kroki: SYN → SYN-ACK → ACK. Metafora: „Hej!" → „Hej, słyszę!" → „OK, gadamy!". Cel: obie strony potwierdzają gotowość i synchronizują numery sekwencyjne.

**SYN (Synchronize)** — flaga w nagłówku TCP. Segment z flagą SYN inicjuje połączenie i przekazuje początkowy numer sekwencyjny (ISN) nadawcy.

**ACK (Acknowledge)** — flaga potwierdzenia. Numer ACK = numer następnego oczekiwanego bajtu. Gdy serwer wysyła SYN-ACK, jednocześnie potwierdza odbiór SYN klienta (ACK=x+1) i wysyła swój SYN (ISN serwera = y).

---

**Numer sekwencyjny (Sequence Number, SEQ)** — 32-bitowa liczba identyfikująca pozycję pierwszego bajtu danych w segmencie w strumieniu bajtów. Funkcje: zapewnia kolejność, wykrywa duplikaty i braki, umożliwia potwierdzenia.

    Klient wysyła 100 bajtów od pozycji 1000:
    SEQ = 1000, dane = bajty 1000–1099
    Następny segment: SEQ = 1100

**Numer potwierdzenia (Acknowledgment Number, ACK number)** — mówi: „odebrałem wszystko do bajtu X-1, teraz czekam na bajt X". Jest kumulatywny — jedno ACK potwierdza wszystkie dane do tej pozycji.

    Klient wysłał SEQ=1000, 100 bajtów
    Serwer odpowiada: ACK=1100 → „dostałem do 1099, czekam na 1100"

**SACK (Selective ACK)** — rozszerzenie TCP. Pozwala potwierdzać niesąsiednie bloki danych, co przyspiesza retransmisję. Bez SACK: utrata jednego segmentu wymaga retransmisji wszystkiego od niego.

---

**ISN (Initial Sequence Number)** — początkowy numer sekwencyjny wybierany przy nawiązywaniu połączenia. Każda strona wybiera swój ISN niezależnie.

**Dlaczego ISN nie zaczyna od 0?**
1. **Bezpieczeństwo** — losowy ISN utrudnia atakującemu zgadnięcie numerów i przejęcie sesji (TCP hijacking).
2. **Unikanie kolizji** — gdyby ISN=0, segmenty z poprzedniego połączenia między tymi samymi portami mogłyby zostać błędnie zaakceptowane.
3. RFC 793 (oryg.): ISN = timer inkrementowany co 4μs mod 2³².
4. RFC 6528 (współcz.): ISN = M + F(adresy, porty, secret_key) — kryptograficznie losowy.

**MSS (Maximum Segment Size)** — maksymalny rozmiar danych w jednym segmencie TCP. Uzgadniana w handshake (zwykle 1460 bajtów dla Ethernetu = MTU 1500 − 20 IP − 20 TCP).

**Window Scale** — opcja TCP negocjowana w handshake. Pozwala zwiększyć okno odbiorcze ponad 65535 bajtów (do ~1 GB), co jest konieczne dla szybkich łączy.

**RFC (Request For Comments)** — dokumenty standaryzacyjne internetu. Nazwa historyczna z ARPANET — „prośba o komentarze" — ale w praktyce to obowiązujące standardy. TCP = RFC 793 (1981).

**Bajt (byte)** — 8 bitów. TCP numeruje strumień po bajtach, nie po segmentach. Dlatego SEQ to numer bajtu, a nie numer pakietu.

---

### Cel handshake'u
1. Nawiązanie połączenia — obie strony się zgadzają
2. Synchronizacja ISN (Initial Sequence Number)
3. Uzgodnienie parametrów (MSS, Window Scale, SACK)

### Przebieg

    Klient                          Serwer
      |  (1) SYN, seq=x              |
      |-----------------------------→|
      |  (2) SYN+ACK, seq=y, ack=x+1 |
      |←-----------------------------|
      |  (3) ACK, seq=x+1, ack=y+1   |
      |-----------------------------→|
      |     [POŁĄCZENIE NAWIĄZANE]    |

### Numery sekwencyjne (SEQ)
- SEQ = numer pierwszego bajtu danych w segmencie
- Funkcje: kolejność, duplikaty, braki, potwierdzenia

### Numery potwierdzenia (ACK)
- ACK = numer **następnego oczekiwanego** bajtu (kumulatywne)
- SACK — opcja potwierdzania niesąsiednich bloków

### Wartość początkowa ISN
- **NIE zaczyna od 0** — bezpieczeństwo + unikanie kolizji z poprzednimi połączeniami
- RFC 793: ISN = timer 4μs mod 2³²
- RFC 6528: ISN = M + F(adresy, porty, secret_key) — kryptograficznie

### Etymologia

**TCP** — Transmission Control Protocol; Vint Cerf + Bob Kahn (1974, „A Protocol for Packet Network Intercommunication"). **Handshake** — metafora uścisku dłoni = wzajemna zgoda na komunikację. **SYN** — Synchronize. **ACK** — Acknowledge. **ISN** — Initial Sequence Number. **MSS** — Maximum Segment Size. **SACK** — Selective ACK. **RFC** — Request For Comments; tradycja ARPANET (1969).

### Jak zapamiętać

- **„SYN, SYN-ACK, ACK"** — 3 kroki, jak potwierdzenie rozmowy: „Hej!" „Hej, słyszę!" „OK, gadamy!"
- **SEQ = numer bajtu**, ACK = „czekam na bajt numer..."
- **ISN losowy** — bo inaczej atakujący może zgadnąć i przejąć sesję

\newpage

## PYTANIE 9: Procesy i wątki (SOI)

**Budowa, szybkość, zastosowanie. Problemy komunikacji i synchronizacji.**

---

### Tło pojęciowe — słowniczek

**Proces (process)** — program w trakcie wykonania. Każdy proces ma własną, izolowaną przestrzeń adresową. System operacyjny zarządza procesami — tworzy, planuje (scheduling), kończy. Np. przeglądarka i edytor to osobne procesy.

**Wątek (thread)** — lekka jednostka wykonania wewnątrz procesu. Wątki jednego procesu współdzielą pamięć (kod, dane, heap), ale mają własny stos i rejestry CPU. Tworzenie wątku jest ~100x szybsze niż procesu.

    Proces = mieszkanie (własny adres, izolacja)
    Wątek  = pokój w mieszkaniu (współdzielona kuchnia = heap)

    Cecha              Proces         Wątek
    ─────────────────────────────────────────
    Pamięć             własna         współdzielona
    Tworzenie          ~1-10 ms       ~10-100 μs
    Przełączanie       wolne (TLB)    szybkie (rejestry)
    Komunikacja        IPC/pipe       bezpośrednia
    Awaria             izolowana      może zabić proces

---

**Przestrzeń adresowa (address space)** — zakres adresów pamięci wirtualnej dostępnych procesowi. Każdy proces widzi swoją „prywatną" pamięć, nawet jeśli fizycznie jest mapowana gdzieś indziej.

**Segmenty pamięci procesu:**
- **TEXT** — kod maszynowy (read-only)
- **DATA** — zainicjalizowane zmienne globalne/statyczne
- **BSS** — niezainicjalizowane zmienne globalne (zerowane)
- **HEAP** — pamięć alokowana dynamicznie (malloc/new), rośnie w górę
- **STACK** — zmienne lokalne, adresy powrotu, rośnie w dół

        ┌──────────┐ wysoki adres
        │  STACK ↓ │
        │   ...    │
        │  HEAP  ↑ │
        │  BSS     │
        │  DATA    │
        │  TEXT    │
        └──────────┘ niski adres

**PCB (Process Control Block)** — struktura danych w jądrze OS opisująca proces: PID, stan, rejestry CPU, tablice stron, otwarte pliki, priorytety. Przełączenie kontekstu = zapisanie PCB starego procesu i wczytanie nowego.

**PID (Process ID)** — unikalny identyfikator procesu w systemie. Np. `PID 1` = init/systemd w Linux.

**TID (Thread ID)** — unikalny identyfikator wątku.

**Stany procesu:** NEW (tworzony) → READY (gotowy, czeka na CPU) ↔ RUNNING (wykonywany) → BLOCKED (czeka na I/O), TERMINATED (zakończony). Scheduler decyduje, który READY staje się RUNNING.

---

**Przełączanie kontekstu (context switch)** — zapisanie stanu aktualnego procesu/wątku i wczytanie stanu następnego. Dla procesów kosztowne (wymaga TLB flush = unieważnienie cache translacji adresów). Dla wątków tańsze (ta sama przestrzeń adresowa = brak TLB flush).

**TLB (Translation Lookaside Buffer)** — sprzętowy cache translacji adres wirtualny → fizyczny. Przy zmianie procesu TLB trzeba wyczyścić (flush), bo nowy proces ma inne mapowania. Koszt: ~1000 ns. Przy zmianie wątku — TLB zostaje (ten sam proces).

---

**IPC (Inter-Process Communication)** — mechanizmy komunikacji między procesami. Konieczne, bo procesy mają izolowane przestrzenie adresowe i nie mogą czytać wzajemnej pamięci bezpośrednio.

- **Pipe** — jednokierunkowy strumień bajtów (ls | grep foo). Anonimowy, tylko między spokrewnionymi procesami.
- **Named Pipe (FIFO)** — pipe z nazwą w systemie plików, mogą go używać niespokrewnione procesy.
- **Message Queue** — kolejka wiadomości w jądrze; asynchroniczna komunikacja.
- **Shared Memory** — wspólny region pamięci; najszybszy IPC (brak kopiowania), ale wymaga synchronizacji.
- **Socket** — komunikacja sieciowa lub lokalna (Unix domain socket). Uniwersalny, działa między maszynami.
- **Signal** — asynchroniczne powiadomienie (np. SIGKILL, SIGTERM). Ograniczony — przesyła tylko numer sygnału.

---

**Wyścig (race condition)** — sytuacja, gdy wynik programu zależy od kolejności wykonania operacji przez wątki. Przykład: dwa wątki zwiększają x=0 o 1 → wynik może być 1 zamiast 2, bo oba czytają 0 zanim zapiszą.

    Wątek A:  czytaj x(=0) → dodaj 1 → zapisz x(=1)
    Wątek B:  czytaj x(=0) → dodaj 1 → zapisz x(=1)
    Wynik: x = 1 zamiast oczekiwanego 2!

**Sekcja krytyczna (critical section)** — fragment kodu, który może być wykonywany przez najwyżej jeden wątek naraz. Chroni współdzielone zasoby przed race condition.

**Zakleszczenie (deadlock)** — sytuacja, w której dwa lub więcej wątków czekają na siebie nawzajem i żaden nie może kontynuować. Jak dwa samochody na skrzyżowaniu — oba czekają, nikt nie jedzie.

    Wątek A: trzyma mutex1, czeka na mutex2
    Wątek B: trzyma mutex2, czeka na mutex1
    → Zakleszczenie! Żaden nie puści swojego.

**Warunki Coffmana** — 4 warunki konieczne deadlocka (wszystkie muszą zachodzić jednocześnie):
1. **Mutual exclusion** — zasób jest wyłączny (tylko jeden wątek)
2. **Hold and wait** — trzymaj zasób, czekaj na kolejny
3. **No preemption** — nie można zabrać zasobu siłą
4. **Circular wait** — cykliczne oczekiwanie (A→B→C→A)
Złam jeden = brak deadlocka.

**Zagłodzenie (starvation)** — wątek nigdy nie dostaje zasobu, bo inni ciągle go wyprzedzają (np. nisko priorytetowy wątek przy high-priority scheduling).

---

**Mutex (MUTual EXclusion)** — zamek na sekcję krytyczną. Tylko jeden wątek może go „zamknąć" (lock); reszta czeka (sleep). Tryb: lock → sekcja krytyczna → unlock.

**Semafor (semaphore)** — uogólniony mutex z licznikiem. Semafor binarny (0/1) = mutex. Semafor zliczający (n) — pozwala n wątkom jednocześnie. P() = probeer (zmniejsz), V() = verhoog (zwiększ).

    semafor(3):  3 wątki mogą wejść naraz
    P() → counter-- (jeśli 0 → czekaj)
    V() → counter++ (obudź czekającego)

**Monitor** — wysokopoziomowy mechanizm synchronizacji. Obiekt z mutexem wbudowanym — tylko jeden wątek może wykonywać metody monitora. Java: `synchronized`.

**Condition Variable** — pozwala wątkowi czekać (wait) na spełnienie warunku i być obudzonym (signal/notify) przez inny wątek. Używane z mutexem.

**Spinlock** — zamek, w którym wątek aktywnie czeka w pętli (busy-wait) zamiast zasypiać. Szybki dla bardzo krótkich sekcji krytycznych (~ns), marnotrawny dla dłuższych.

**Read-Write Lock** — pozwala wielu czytelnikom jednocześnie LUB jednemu pisarzowi. Optymalizacja dla scenariuszy z dużo odczytów i rzadkimi zapisami.

**Barrier** — punkt synchronizacji: wszystkie wątki muszą dotrzeć do bariery, zanim którykolwiek może kontynuować. Użyteczna w obliczeniach równoległych (np. po każdej iteracji).

---

### Proces — program w trakcie wykonania

Pamięć: TEXT (kod) | DATA | BSS | HEAP | STACK — oddzielna przestrzeń adresowa.
PCB: PID, stan, rejestry CPU, tablice stron, otwarte pliki.
Stany: NEW → READY ↔ RUNNING → BLOCKED, TERMINATED.

### Wątek — lekka jednostka wykonania

**Współdzielone** z procesem: kod, dane globalne, heap, pliki.
**Prywatne:** stos, rejestry CPU, PC, TID.

### Porównanie

| Cecha           | Proces           | Wątek               |
|-----------------|------------------|----------------------|
| Przestrzeń addr | Własna, izolowana| Współdzielona        |
| Tworzenie       | ~1-10 ms         | ~10-100 μs           |
| Przełączanie    | Wolne (TLB flush)| Szybkie (rejestry)   |
| Komunikacja     | IPC (pipe, shm)  | Współdzielona pamięć |
| Izolacja        | Pełna            | Brak                 |

### Komunikacja międzyprocesowa (IPC)
Pipe, Named Pipe (FIFO), Message Queue, Shared Memory, Sockets, Signals, Memory-mapped files.

### Synchronizacja — problemy
- **Wyścig (race condition)** — wynik zależy od kolejności operacji
- **Sekcja krytyczna** — fragment kodu wymagający wyłącznego dostępu
- **Zakleszczenie (deadlock)** — wzajemne oczekiwanie (warunki Coffmana: mutual exclusion, hold & wait, no preemption, circular wait)
- **Zagłodzenie (starvation)** — wątek nigdy nie dostaje zasobu

### Mechanizmy synchronizacji
Mutex, Semaphore, Monitor, Condition Variable, Spinlock, Read-Write Lock, Barrier.

### Etymologia

**Proces** — łac. „processus" = posuwanie się naprzód. **Wątek (Thread)** — metafora nitki wykonania (jak nić Ariadny). **Mutex** — portmanteau MUTual EXclusion. **Semafor** — Dijkstra (1965); od semaforów kolejowych; P() = hol. „proberen" (próbować), V() = hol. „verhogen" (podnosić). **Coffman** — Edward Coffman Jr. et al. (1971): 4 warunki konieczne deadlocka. **Deadlock (zakleszczenie)** — jak zablokowane koła zębate. **IPC** — Inter-Process Communication.

### Jak zapamiętać

- **„Proces = mieszkanie, Wątek = pokój"** — każde mieszkanie ma adres (przestrzeń), pokoje dzielą kuchnię (heap)
- Wątki szybsze bo nie trzeba zmieniać „mieszkania" (TLB flush)
- **4 warunki Coffmana** zakleszczenia: złam jeden → brak deadlocka

\newpage

## PYTANIE 10: Zarządzanie pamięcią (SOI)

**Problemy i mechanizmy. Stronicowanie vs segmentacja.**

---

### Tło pojęciowe — słowniczek

**Pamięć operacyjna (RAM)** — szybka pamięć ulotna, z której procesor odczytuje i zapisuje dane. Ograniczona ilościowo (np. 8–64 GB). Zadanie OS: rozdzielić ją sprawiedliwie i bezpiecznie między procesy.

**Pamięć wirtualna (virtual memory)** — abstrakcja: każdy proces „widzi" własną, ciągłą przestrzeń adresową, niezależnie od fizycznego rozmieszczenia danych w RAM. OS + MMU (sprzęt) tłumaczą adresy wirtualne na fizyczne. Dzięki temu programy mogą używać więcej pamięci niż fizycznie dostępne (reszta na dysku = swap).

    Program widzi:    [0x0000 ... 0xFFFF]  ← wirtualne, ciągłe
    RAM fizyczny:     [ramka 5][ramka 12][ramka 3]  ← rozproszone

---

**Fragmentacja (fragmentation)** — marnowanie pamięci z powodu sposobu alokacji.

**Fragmentacja zewnętrzna (external)** — wolna pamięć jest rozproszona w małych kawałkach między zajętymi. Suma wolnych kawałków wystarczy, ale żaden pojedynczy nie jest wystarczająco duży.

    [ZAJĘTE][wolne 2KB][ZAJĘTE][wolne 3KB][ZAJĘTE]
    Razem 5KB wolne, ale nie zmieści się blok 4KB!

**Fragmentacja wewnętrzna (internal)** — przydzielony blok jest większy niż potrzebny. Pozostała różnica jest zmarnowana. Np. strona 4KB przydzielona dla 100 bajtów danych — 3996 bajtów zmarnowane.

**Ochrona pamięci (memory protection)** — mechanizm uniemożliwiający procesowi dostęp do pamięci innego procesu. Realizowana przez tablice stron (bity R/W/X) i MMU. Bez ochrony: crash jednego procesu mógłby zepsuć cały system.

**Relokacja (relocation)** — program musi działać pod różnymi adresami fizycznymi (nie wie z góry, gdzie zostanie załadowany). Pamięć wirtualna rozwiązuje to automatycznie — program zawsze widzi te same adresy wirtualne.

**COW (Copy-on-Write)** — optymalizacja: przy fork() (tworzenie procesu) dziecko współdzieli strony z rodzicem. Kopia fizyczna następuje dopiero gdy któryś pisze. Oszczędność: jeśli procesy tylko czytają, nie kopiujemy nic.

---

**Strona (page)** — jednostka pamięci wirtualnej o stałym rozmiarze (zwykle 4 KB). Pamięć wirtualna jest podzielona na strony.

**Ramka (frame)** — jednostka pamięci fizycznej o tym samym rozmiarze co strona. Strona wirtualna mapowana jest na ramkę fizyczną.

**Tablica stron (page table)** — struktura danych tłumacząca numer strony → numer ramki. Każdy proces ma własną tablicę stron. Wpis zawiera: numer ramki, bity present/dirty/R/W/X.

    Adres wirtualny = [numer strony | offset]
    Tablica stron:    strona 5 → ramka 12
    Adres fizyczny  = [12 | offset]

**Wielopoziomowe tablice stron** — oszczędność pamięci. Zamiast jednej ogromnej tablicy (32-bit: 4 MB per proces!), drzewo tablic. Nieużywane gałęzie nie istnieją.

    32-bit: 2-level (1024 × 1024 wpisów)
    64-bit: 4-level (x86-64: PML4 → PDPT → PD → PT)

**TLB (Translation Lookaside Buffer)** — sprzętowy cache translacji adresów. Przechowuje ostatnio używane mapowania strona→ramka. Trafienie w TLB: ~1 ns; pudło: ~10-100 ns (trzeba chodzić po tablicy stron). Hit rate: typowo >99%.

**Page fault (brak strony)** — wyjątek sprzętowy gdy strona nie jest aktualnie w RAM. OS ładuje ją z dysku (swap). Nie jest „błędem" programisty — to normalna część zarządzania pamięcią wirtualną.

    Koszt: ~1-10 ms (bo dysk!) vs ~100 ns dla dostępu do RAM
    Różnica ~10 000x — dlatego minimalizacja page faults jest krytyczna

---

**Algorytmy wymiany stron (page replacement):**
- **FIFO** — usuń najstarszą stronę. Prosty, ale anomalia Bélády'ego (więcej ramek → więcej page faults!).
- **LRU (Least Recently Used)** — usuń najdawniej używaną. Dobry, ale kosztowna implementacja (trzeba śledzić czas użycia).
- **Clock (Second Chance)** — przybliżenie LRU. Wskazówka zegara + bit odwołania. Jeśli bit=1, daj drugą szansę (zeruj i idź dalej). Jeśli bit=0, wymień.
- **Optimal** — usuń stronę, która nie będzie potrzebna najdłużej. Idealny, ale nierealizowalny (wymaga znajomości przyszłości). Benchmark dla porównania.

---

**Segmentacja (segmentation)** — podział pamięci na segmenty logiczne o zmiennych rozmiarach (kod, dane, stos). Adres = (numer segmentu, offset). Każdy segment ma bazę i limit.

    Cecha              Stronicowanie         Segmentacja
    ─────────────────────────────────────────────────────
    Jednostka          strona (stały, 4KB)   segment (zmienny)
    Fragmentacja       wewnętrzna            zewnętrzna
    Widok programisty  niewidoczne           logiczne (kod, dane)
    Współczesne OS     dominuje (x86-64)     prawie zniknęła

**Dlaczego stronicowanie wygrało?** Stałe rozmiary stron = brak fragmentacji zewnętrznej, prostsze zarządzanie, łatwiejsze w sprzęcie. Intel porzucił pełną segmentację w x86-64 (flat segments + paging).

**Swap** — przestrzeń na dysku używana gdy RAM się wyczerpie. OS przenosi rzadko używane strony na swap (swap out) i wczytuje je z powrotem gdy potrzebne (swap in). Wolne (dysk!), ale pozwala uruchamiać więcej niż RAM.

---

### Problemy
1. **Fragmentacja** — zewnętrzna (wolna pamięć rozproszona) i wewnętrzna (przydzielony blok > potrzebny)
2. **Ochrona** — procesy nie mogą czytać cudzej pamięci
3. **Relokacja** — program musi działać pod różnymi adresami
4. **Współdzielenie** — biblioteki, COW (Copy-on-Write)
5. **Ograniczona pamięć** — więcej procesów niż RAM

### Stronicowanie (Paging)

- Pamięć wirtualna → **strony** (pages, np. 4KB), fizyczna → **ramki** (frames)
- **Tablica stron** mapuje strony na ramki
- Translacja: adres = (numer strony | offset) → (numer ramki | offset)
- **Wielopoziomowe tablice** — oszczędność pamięci (32-bit: 2-level, 64-bit: 4-level)
- **TLB** (Translation Lookaside Buffer) — cache translacji
- **Page fault** — strona nie w RAM → ładuj z dysku (swap)
- **Algorytmy wymiany:** FIFO, LRU, Clock (Second Chance), Optimal

### Segmentacja (Segmentation)

- Pamięć dzielona na **segmenty logiczne** (kod, dane, stos) o różnych rozmiarach
- Adres = (numer segmentu, offset), tablica segmentów: (baza, limit)
- Ochrona per-segment (R, W, X)

### Porównanie

| Cecha             | Stronicowanie          | Segmentacja             |
|-------------------|------------------------|-------------------------|
| Jednostka         | Strona (stały rozmiar) | Segment (zmienny)       |
| Fragmentacja      | Wewnętrzna             | Zewnętrzna              |
| Widok programisty | Niewidoczne            | Widoczne (logiczne)     |
| Ochrona           | Per-strona             | Per-segment             |
| Współdzielenie    | Per-strona             | Per-segment (naturalne) |
| Współczesne OS    | Dominuje (x86-64)      | Rzadko (Intel porzucił) |

### Etymologia

**Stronicowanie (Paging)** — pamięć dzielona na „strony" jak w książce. **TLB** — Translation Lookaside Buffer; „lookaside" = sprawdź z boku (cache) zanim sięgniesz do tablicy. **Segmentacja** — łac. „segmentum" = odcięty kawałek. **COW** — Copy-on-Write: kopiuj dopiero przy modyfikacji. **LRU** — Least Recently Used. **FIFO** — First In, First Out. **Page fault** — „fault" to wyjątek sprzętowy, nie błąd programisty.

### Jak zapamiętać

- **Stronicowanie = szuflady jednakowej wielkości** (proste, mała fragmentacja wewnętrzna)
- **Segmentacja = pudełka różnej wielkości** (logiczne, ale fragmentacja zewnętrzna)
- Współcześnie: **stronicowanie wygrało** — segmentacja prawie zniknęła (x86-64 = flat segments + paging)

\newpage

## PYTANIE 11: Modelowanie procesów biznesowych (WSYZ)

**Scharakteryzować standardy i narzędzia do modelowania procesów biznesowych.**

---

### Tło pojęciowe — słowniczek

**Proces biznesowy (business process)** — uporządkowany zbiór czynności, które transformują dane wejściowe (np. zamówienie klienta) w wynik (np. dostarczony produkt). Przykład: „obsługa reklamacji" = przyjmij zgłoszenie → zweryfikuj → zatwierdź/odrzuć → poinformuj klienta. Modelowanie to graficzne przedstawienie takich procesów.

**Modelowanie procesów** — tworzenie wizualnych diagramów opisujących KTO, CO, KIEDY i W JAKIEJ KOLEJNOŚCI wykonuje w organizacji. Cel: zrozumienie, dokumentacja, optymalizacja, automatyzacja.

---

**BPMN (Business Process Model and Notation)** — najpopularniejszy standard notacji graficznej dla procesów biznesowych. Utrzymywany przez OMG (Object Management Group). Wersja 2.0 ma format XML, dzięki czemu diagramy mogą być bezpośrednio wykonywane przez silnik procesów (BPMS).

**Elementy BPMN:**
- **Zdarzenia (Events):** ○ start, ◎ pośrednie, ◉ końcowe — co wyzwala lub kończy proces.
- **Czynności (Activities):** prostokąty — praca do wykonania (task, subprocess).
- **Bramki (Gateways):** ◇ kontrola przepływu — decyzje i rozgałęzienia.

**Bramki BPMN (gateways):**
- **XOR (Exclusive):** dokładnie JEDNA ścieżka (jak if/else). Np. „Czy kwota > 1000? → Tak/Nie".
- **AND (Parallel):** WSZYSTKIE ścieżki jednocześnie. Np. „Wyślij e-mail I zaktualizuj bazę".
- **OR (Inclusive):** JEDNA LUB WIĘCEJ ścieżek. Np. „Powiadom SMS i/lub e-mail zależnie od preferencji."

    ○─→[Przyjmij zamówienie]─→◇XOR─→[Zapłata kartą]─→◉
                                  └→[Zapłata przelewem]─→◉

**Łączniki BPMN:**
- **Sequence Flow (→)** — kolejność czynności
- **Message Flow (- - →)** — komunikacja między uczestnikami (poolami)
- **Association (···→)** — powiązanie z danymi/komentarzami

**Swimlane** — element organizacyjny: **Pool** = organizacja/uczestnik, **Lane** = dział/rola w organizacji. Jak tory na basenie — każdy „pływa" na swoim torze.

---

**UML (Unified Modeling Language)** — uniwersalny język modelowania w inżynierii oprogramowania. 14 typów diagramów. W kontekście procesów używa się **Activity Diagrams** — rozszerzenie flowchartów z fork/join (współbieżność), decision nodes, object flow. Lepszy dla procesów technicznych/software niż BPMN.

**UML Activity Diagram vs BPMN:**

    Cecha          BPMN                 UML Activity
    ─────────────────────────────────────────────────
    Cel            Procesy biznesowe    Przepływ sterowania
    Odbiorcy       Biznes + IT          Głównie IT
    Komunikacja    Pools + Msg Flow     Partitions
    Automatyzacja  Tak (XML)            Ograniczona

**EPC (Event-driven Process Chain)** — notacja procesowa: naprzemienne zdarzenia i funkcje, połączone łącznikami logicznymi (AND/OR/XOR). Popularny w środowisku SAP (framework ARIS). Mniej uniwersalny niż BPMN.

**ARIS (Architecture of Integrated Information Systems)** — framework i narzędzie prof. Scheera do modelowania procesów. Bazuje na EPC. Używany głównie w dużych firmach z SAP.

---

**OMG (Object Management Group)** — organizacja standaryzacyjna odpowiedzialna za BPMN, UML, CORBA. Non-profit, członkowie to firmy IT (IBM, Oracle, SAP...).

**BPMS (Business Process Management System/Suite)** — oprogramowanie do automatyzacji procesów BPMN. Diagram BPMN 2.0 XML jest interpretowany i wykonywany przez silnik (np. Camunda, jBPM). Zmiana procesu = zmiana diagramu, nie kodu.

**IDEF0 (Integration DEFinition)** — notacja modelowania funkcji z US Air Force (1970s). Skupia się na WEJŚCIach, WYJŚCIach, mechanizmach i kontrolach. Rzadko używana współcześnie.

**VSM (Value Stream Map)** — narzędzie Lean Manufacturing. Mapuje przepływ materiałów i informacji od dostawcy do klienta, identyfikuje marnotrawstwo (waste). Stosowane w fabrykach i IT (DevOps).

**Flowchart (schemat blokowy)** — najprostszy sposób modelowania: prostokąty (czynności), romby (decyzje), strzałki (przepływ). Prekursor BPMN, ale brak standardów dla komunikacji międzyprocesowej.

---

### Główne standardy

### BPMN 2.0 (Business Process Model and Notation) — OMG
- **Uniwersalny standard** — dla analityków, architektów, programistów
- Elementy: Zdarzenia (○ start, ◎ pośrednie, ◉ końcowe), Czynności (prostokąty), Bramki (◇ XOR, ◆ AND, ○◇ OR)
- Łączniki: Sequence Flow (→), Message Flow (- - →), Association (···→)
- Swimlanes: Pool (organizacja) / Lane (dział)
- Format XML → automatyzacja (BPMS)

### UML Activity Diagrams
- Część UML 2.x — rozszerzenie flowchartów + sieci Petriego
- Elementy: akcje, decyzje (◇), fork/join (▬), pin (object flow)
- Lepsze dla procesów technicznych/software

### EPC (Event-driven Process Chain)
- Naprzemienne zdarzenia i funkcje, łączniki AND/OR/XOR
- Popularny w SAP (ARIS framework)

### Inne: IDEF0 (modelowanie funkcji), VSM (Value Stream Map, Lean), Flowcharty

### BPMN vs UML Activity

| Cecha        | BPMN               | UML Activity       |
|--------------|---------------------|---------------------|
| Cel          | Procesy biznesowe   | Przepływ sterowania |
| Odbiorcy     | Biznes + IT         | Głównie IT          |
| Komunikacja  | Pools + Message Flow| Partitions          |
| Automatyzacja| Tak (BPMN 2.0 XML) | Ograniczona         |

### Narzędzia
Bizagi Modeler, Camunda, Signavio, Lucidchart, draw.io, Enterprise Architect

### Etymologia

**BPMN** — Business Process Model and Notation; OMG (Object Management Group). **UML** — Unified Modeling Language; „Unified" bo połączył metody Boocha, Rumbaugh i Jacobsona („Three Amigos", 1990s). **EPC** — Event-driven Process Chain; August-Wilhelm Scheer (Saarland, 1990s; podstawa SAP ARIS). **Swimlane** — metafora torów na basenie: każdy uczestnik na swoim „torze". **IDEF0** — Integration DEFinition; US Air Force (1970s).

### Jak zapamiętać

- **BPMN = „standard nr 1" dla biznesu** — bramki, swimlanes, zdarzenia
- **3 typy bramek: XOR (jeden), AND (wszystkie), OR (jeden lub więcej)**
- UML Activity → programiści; BPMN → wszyscy

\newpage

## PYTANIE 12: Sieciowe modele optymalizacji (WSYZ)

**Przedstawić sieciowe modele optymalizacji stosowane w systemach zarządzania.**

---

### Tło pojęciowe — słowniczek

**Graf (graph)** — struktura: zbiór **węzłów** (vertices) połączonych **krawędziami** (edges). Podstawowa abstrakcja dla wszystkich modeli sieciowych. Krawędzie mogą mieć wagi (koszt, odległość, przepustowość) i kierunek (graf skierowany).

    A──5──B──3──C       graf ważony nieskierowany
    │           │       węzły: A,B,C,D
    2           4       krawędzie z wagami
    │           │
    D─────7─────┘

**Sieć (network)** — graf z interpretacją: węzły = lokalizacje/zadania, krawędzie = połączenia/trasy, wagi = koszty/czasy/przepustowości. Modele sieciowe rozwiązują problemy optymalizacyjne na takich grafach.

**Optymalizacja** — znalezienie najlepszego rozwiązania (minimum lub maksimum funkcji celu) przy zadanych ograniczeniach. W kontekście sieciowym: najkrótsza trasa, maksymalny przepływ, minimalny koszt itp.

---

**Najkrótsza ścieżka (shortest path)** — znajdź ścieżkę od źródła do celu o minimalnej sumie wag. Zastosowanie: GPS, routing sieciowy.

**Dijkstra** — algorytm zachłanny. Bierze najbliższy nieodwiedzony węzeł, aktualizuje odległości sąsiadów. Wymaga wag ≥ 0. Złożoność: O(E log V) z kopcem. Dla V=1000, E=5000: ~60 000 operacji.

**Bellman-Ford** — obsługuje ujemne wagi. Relaksuje wszystkie krawędzie V-1 razy. O(VE). Wykrywa cykle ujemne.

**A\*** — rozszerzenie Dijkstry z heurystyką (szacuje odległość do celu). Szybszy w praktyce, bo eksploruje w kierunku celu. Używany w nawigacji, grach.

---

**Maksymalny przepływ (max flow)** — znajdź największy przepływ od źródła (s) do ujścia (t) w sieci z ograniczonymi przepustowościami krawędzi. Zastosowanie: przepustowość linii, ruch sieciowy, planowanie.

**Ford-Fulkerson** — metoda: znajdź ścieżkę powiększającą (augmenting path) w sieci rezydualnej, powiększ przepływ, powtarzaj. Twierdzenie max-flow min-cut: max. przepływ = min. przepustowość przekroju.

**Edmonds-Karp** — implementacja Ford-Fulkerson z BFS (zamiast DFS). Gwarantuje O(VE²). Dla V=100, E=500: ~25 000 000 operacji max.

---

**Problem przydziału (assignment problem)** — przydziel n zadań do n pracowników, minimalizując łączny koszt. Każdy pracownik dostaje dokładnie jedno zadanie. Macierz kosztów n×n.

    Pracownik   Z1   Z2   Z3
    A           8    4    7
    B           5    2    3
    C           9    4    8
    Optymalne: A→Z2(4), B→Z3(3), C→Z1(9) = 16

**Algorytm węgierski (Hungarian algorithm)** — rozwiązuje problem przydziału optymalnie w O(n³). Nazwa od prac matematyków węgierskich: Kőnig i Egerváry.

---

**TSP (Travelling Salesman Problem / problem komiwojażera)** — odwiedź wszystkie miasta dokładnie raz i wróć do startu, minimalizując trasę. **NP-trudny** — nie ma znanego algorytmu wielomianowego. Dla n=20 miast: 20!/2 ≈ 1.2×10¹⁸ tras do sprawdzenia brute-force! W praktyce: heurystyki (nearest neighbor, 2-opt, simulated annealing, algorytmy genetyczne).

**NP-trudny (NP-hard)** — klasa problemów, dla których nie znamy algorytmu rozwiązującego w czasie wielomianowym. Nie oznacza „niemożliwe" — oznacza „nie da się szybko dla dużych instancji" (czas rośnie wykładniczo). Stosuje się heurystyki i przybliżenia.

---

**CPM (Critical Path Method)** — metoda harmonogramowania projektów. Wyznacza **ścieżkę krytyczną** = najdłuższą ścieżkę w grafie zadań. Opóźnienie zadania na ścieżce krytycznej opóźnia cały projekt. O(V+E). Zastosowanie: budownictwo, inżynieria.

**PERT (Program Evaluation and Review Technique)** — podobna do CPM, ale z niepewnością czasu (optymistyczny, pesymistyczny, prawdopodobny → rozkład β). Opracowana dla US Navy (program Polaris, 1958).

**MST (Minimum Spanning Tree / minimalne drzewo rozpinające)** — połącz wszystkie węzły grafu minimalnym kosztem (bez cykli). Zastosowanie: sieci telekomunikacyjne, elektryczne, wodociągowe.

**Kruskal** — sortuj krawędzie rosnąco, dodawaj najlżejszą nie tworzącą cyklu. O(E log E). Używa Union-Find.
**Prim** — startuj od węzła, dodawaj najtańszą krawędź prowadzącą na zewnątrz drzewa. O(E log V) z kopcem.

**Minimalny koszt przepływu (min-cost flow)** — połączenie max flow i najkrótszej ścieżki: przesyłaj zadany przepływ od s do t z minimalnym łącznym kosztem. Zastosowanie: transport, logistics.

---

### 1. Najkrótsza ścieżka — GPS, routing (Dijkstra, Bellman-Ford, A*)
### 2. Maksymalny przepływ — przepustowość linii, dystrybucja (Ford-Fulkerson, Edmonds-Karp)
### 3. Minimalny koszt przepływu — minimalizacja kosztów transportu przy zadanym przepływie
### 4. Problem przydziału — n zadań do n osób, minimalizacja kosztów (algorytm węgierski, O(n³))
### 5. TSP (komiwojażer) — odwiedź wszystkie miasta raz, minimalizuj trasę (NP-trudny, heurystyki)
### 6. CPM/PERT — harmonogramowanie projektów, ścieżka krytyczna
### 7. MST (drzewo rozpinające) — połącz wszystkie węzły minimalnym kosztem (Kruskal, Prim)

| Model               | Złożoność       | Zastosowanie              |
|----------------------|-----------------|---------------------------|
| Najkrótsza ścieżka  | O(E log V)      | Logistyka, routing        |
| Max Flow             | O(VE²)          | Planowanie, dystrybucja   |
| Przydział            | O(n³)           | HR, grafiki               |
| TSP                  | NP-trudny       | Trasy kurierów            |
| CPM                  | O(V+E)          | Zarządzanie projektami    |
| MST                  | O(E log V)      | Sieci infrastrukturalne   |

### Etymologia

**Ford-Fulkerson** — Lester Ford Jr. + Delbert Fulkerson (1956). **Edmonds-Karp** — Jack Edmonds + Richard Karp (1972); BFS-owa wersja Ford-Fulkerson. **TSP (komiwojażer)** — z XIX-wiecznych niemieckich podręczników dla handlowców. **CPM** — Critical Path Method (DuPont, 1957). **PERT** — Program Evaluation and Review Technique (US Navy, Polaris, 1958). **Kruskal** — Joseph Kruskal (1956). **Prim** — Robert Prim (1957; niezależnie Jarník 1930). **Algorytm węgierski** — Harold Kuhn (1955); od prac Węgrów: Kőniga i Egerváry'ego.

### Jak zapamiętać

- **6 modeli na grafach:** Ścieżka, Przepływ, Min-koszt-przepływ, Przydział, TSP, Harmonogram, MST
- Wszystko sprowadza się do: „węzły + krawędzie + wagi → optymalizuj"

\newpage

## PYTANIE 13/27: Modelowanie architektury systemów informatycznych (AIS)

**Cele i metody modelowania architektury.**

---

### Tło pojęciowe — słowniczek

**Architektura systemu informatycznego (software/system architecture)** — fundamentalne decyzje projektowe dotyczące struktury systemu: jakie komponenty, jak się komunikują, jakie technologie. Jak plan architektoniczny budynku — definiuje „kształt" systemu przed budową.

**Modelowanie architektury** — tworzenie uproszczonych reprezentacji (diagramów, opisów) systemu na różnych poziomach abstrakcji. Cele: komunikacja w zespole, dokumentacja, analiza jakości (czy system będzie wydajny? skalowalny?), planowanie rozwoju.

---

**Framework architektoniczny (architecture framework)** — ustrukturyzowane podejście do opisywania architektury. Definiuje: jakie widoki (views) tworzyć, jakie aspekty uwzględnić, w jakiej kolejności pracować.

**TOGAF (The Open Group Architecture Framework)** — najpopularniejszy framework enterprise architecture. Definiuje metodykę ADM (Architecture Development Method) — cykliczny proces tworzenia architektury. 4 domeny:
- **Business** — procesy organizacji
- **Data** — struktury danych
- **Application** — aplikacje i ich interakcje
- **Technology** — infrastruktura (serwery, sieci)

**ADM (Architecture Development Method)** — cykliczny proces TOGAF: Preliminary → Vision → Business Arch → IS Arch → Technology Arch → Opportunities → Migration → Governance. Iteracyjny — można wracać do wcześniejszych faz.

**4+1 View Model (Kruchten)** — model pięciu perspektyw architektury:
- **Logical View** — funkcjonalność (klasy, moduły)
- **Process View** — współbieżność, przepływ danych
- **Development View** — organizacja kodu (pakiety, warstwy)
- **Physical View** — wdrożenie na sprzęt (serwery, kontenery)
- **+1 Scenarios** — use cases łączące wszystkie widoki

    Dlaczego 4+1? Bo różni interesariusze patrzą na system inaczej:
    programista → Development View, admin → Physical View,
    użytkownik → Scenarios, architekt → Logical View

**Zachman Framework** — taksonomia 6×6: pytania CO/JAK/GDZIE/KTO/KIEDY/DLACZEGO × poziomy abstrakcji (kontekst → logiczny → fizyczny → ...). Nie mówi JAK modelować — mówi CO należy udokumentować. Kompletny, ale złożony.

---

**C4 Model (Simon Brown)** — pragmatyczny model: 4 poziomy zoomu diagramów:
1. **Context** — system w otoczeniu (kto go używa, z czym się integruje)
2. **Container** — kontenery techniczne (app server, DB, SPA, API)
3. **Component** — moduły wewnątrz kontenera
4. **Code** — klasy, interfejsy (opcjonalnie, np. UML)

Zaleta: prosty, zrozumiały dla nie-architektów. Zaczynasz od „big picture" i zanurzasz się głębiej.

**ArchiMate** — język modelowania The Open Group. 3 warstwy (Business, Application, Technology) × 3 aspekty (Active Structure — kto?, Behavior — co robi?, Passive Structure — na czym?). Komplementarny z TOGAF.

---

**UML (Unified Modeling Language)** — uniwersalny język modelowania. W kontekście architektury: **Component Diagram** (moduły i zależności), **Deployment Diagram** (mapowanie na sprzęt), **Sequence Diagram** (interakcje w czasie).

**ADR (Architecture Decision Records)** — lekka dokumentacja: każda kluczowa decyzja architektoniczna zapisana jako plik z: kontekstem, decyzją, konsekwencjami. Wersjonowane w repo. Format: „Zdecydowaliśmy X, bo Y. Konsekwencje: Z."

**ATAM (Architecture Tradeoff Analysis Method)** — metoda oceny architektury przez scenariusze jakościowe. Identyfikuje tradeoffs: „ta decyzja poprawia wydajność kosztem modyfikowalności". Opracowana przez SEI (Carnegie Mellon).

**Quality Attributes (atrybuty jakości, ISO 25010)** — mierzalne cechy systemu: Performance, Security, Scalability, Maintainability, Reliability, Usability, Portability, Compatibility. Architektura determinuje osiągalne atrybuty jakości.

---

### Cele: komunikacja, dokumentacja, analiza jakości, planowanie, zarządzanie złożonością

### Frameworki

**TOGAF** — metodyka ADM (Architecture Development Method), 4 domeny: Business, Data, Application, Technology.

**4+1 View Model (Kruchten):**
- Logical (funkcjonalność), Process (współbieżność), Development (organizacja kodu), Physical (wdrożenie), + Scenarios (use cases)

**Zachman Framework** — taksonomia 6×6: What/How/Where/Who/When/Why × poziomy abstrakcji.

**C4 Model (Simon Brown):**
- Level 1: System Context → Level 2: Container → Level 3: Component → Level 4: Code

**ArchiMate** — 3 warstwy: Business, Application, Technology × 3 aspekty: Active, Behavior, Passive.

### Notacje: UML (Component, Deployment, Sequence), ArchiMate, C4, ADR (Architecture Decision Records)

### Analiza: ATAM (Architecture Tradeoff Analysis Method), Quality Attributes (ISO 25010: Performance, Security, Scalability, Maintainability, Reliability)

### Etymologia

**TOGAF** — The Open Group Architecture Framework. **Zachman** — John Zachman (IBM, 1987); framework nazwany od twórcy. **C4** — 4 × C: Context, Container, Component, Code (Simon Brown, 2006). **ArchiMate** — „Architecture" + „animate" (The Open Group). **ATAM** — Architecture Tradeoff Analysis Method (SEI, Carnegie Mellon). **Kruchten** — Philippe Kruchten (Rational/IBM, 1995); 4+1 View Model. **ISO 25010** — międzynarodowy standard atrybutów jakości oprogramowania.

### Jak zapamiętać

- **TOGAF = JAK** budować architekturę; **Zachman = CO** dokumentować
- **C4 = 4 poziomy zoomu** (Context → Container → Component → Code)
- **4+1 = LDPP+S** (Logical, Development, Process, Physical + Scenarios)

\newpage

## PYTANIE 14/28: Wzorce architektoniczne (AIS)

**Czemu służą? Jak powstają? Jak są katalogowane? Przykłady.**

---

### Tło pojęciowe — słowniczek

**Wzorzec (pattern)** — udokumentowane, powtarzalne rozwiązanie typowego problemu. Format: Nazwa + Problem (kiedy stosować) + Rozwiązanie (struktura) + Konsekwencje (tradeoffs). To nie gotowy kod — to szablon myślowy, który adaptujemy do kontekstu.

**Wzorzec architektoniczny (architectural pattern)** — wzorzec definiujący CAŁKOWITĄ strukturę systemu: jak podzielić na komponenty, jak komunikują się, jak skalować. Większa skala niż wzorzec projektowy (design pattern), który dotyczy pojedynczej klasy/obiektu.

    Skala wzorców:
    Architektoniczny: Microservices, Layered, Event-Driven  (cały system)
    Projektowy:       Singleton, Observer, Factory            (klasa/obiekt)
    Idiomatyczny:     RAII, for-each                          (linia kodu)

---

**Monolith (monolit)** — cały system jako jedna aplikacja, jeden deployment. Prosty, łatwy na start. Problemy: trudne skalowanie (skalujesz wszystko albo nic), długie buildy, duże ryzyko przy zmianach.

**Layered (warstwowy)** — system podzielony na warstwy, każda zależna od niższej: Presentation → Business Logic → Data Access → Database. Separacja odpowiedzialności. Wada: każde żądanie przechodzi przez WSZYSTKIE warstwy (overhead).

    [Presentation]  ← UI, API
          ↓
    [Business Logic] ← reguły domenowe
          ↓
    [Data Access]    ← SQL, ORM
          ↓
    [Database]       ← PostgreSQL

**Microservices (mikroserwisy)** — system rozbity na małe, niezależne serwisy, każdy z własną bazą danych i deploymentem. Każdy serwis odpowiada za jedną domenę (np. zamówienia, płatności, użytkownicy). Zalety: niezależne skalowanie, niezależne deployments, różne technologie. Wady: złożoność operacyjna (sieć, monitoring, transakcje rozproszone).

**Event-Driven Architecture (EDA)** — komunikacja przez zdarzenia (events). Producer generuje event → Broker (np. Kafka) → Consumers reagują. Loose coupling — producent nie wie kto konsumuje. Eventual consistency.

---

**CQRS (Command Query Responsibility Segregation)** — osobne modele do zapisu (Command) i odczytu (Query). Command model zoptymalizowany do walidacji i zapisu, Query model zoptymalizowany do szybkiego odczytu (np. zdenormalizowane widoki). Złożony, ale potężny przy asymetrii read/write.

    Command → [Write DB] → Event → [Read DB projekcja] → Query
    Zapis i odczyt mają osobne schematy!

**Hexagonal (Ports & Adapters, Alistair Cockburn)** — rdzeń domeny (business logic) jest niezależny od frameworków, baz danych, UI. Komunikuje się przez „porty" (interfejsy). „Adaptery" implementują porty (np. adapter PostgreSQL, adapter REST). Korzyść: testowalność — możesz podmienić adapter na mock.

---

**Katalogi wzorców:**
- **POSA (Pattern-Oriented Software Architecture)** — 5-tomowa seria o wzorcach architektonicznych: Layers, Pipes & Filters, Broker, MVC, Microkernel.
- **GoF (Gang of Four)** — Gamma, Helm, Johnson, Vlissides. 23 wzorce projektowe (nie architektoniczne): kreacyjne (Factory, Singleton), strukturalne (Adapter, Decorator), behawioralne (Observer, Strategy). Książka z 1994 r.
- **EIP (Enterprise Integration Patterns)** — Hohpe & Woolf. Wzorce komunikacji między systemami: Message Channel, Content-Based Router, Aggregator.
- **PoEAA (Patterns of Enterprise Application Architecture)** — Martin Fowler. Wzorce aplikacji enterprise: Repository, Unit of Work, Domain Model, Active Record.
- **Cloud Patterns** — Microsoft Azure Architecture Center, AWS Well-Architected. Wzorce chmurowe: Circuit Breaker, Sidecar, Saga, Strangler Fig.

---

**Skalowalność (scalability)** — zdolność systemu do obsługi rosnącego obciążenia. W kontekście wzorców: monolith → skalowalność niska (scale up), microservices → wysoka (scale out per serwis).

**Loose coupling (luźne wiązanie)** — komponenty mają minimalne zależności. Zmiana jednego nie wymaga zmiany drugiego. Event-Driven i Microservices promują loose coupling.

**Separacja odpowiedzialności (separation of concerns)** — każdy komponent odpowiada za jedną rzecz. Fundamentalna zasada stojąca za wzorcami warstwowymi, hexagonal, CQRS.

**Eventual consistency (spójność ostateczna)** — dane mogą być chwilowo niespójne, ale „w końcu" się zsynchronizują. Cena za skalowalność i loose coupling w systemach rozproszonych (EDA, Microservices).

---

### Cel: reużywalne rozwiązania typowych problemów, wspólne słownictwo, dokumentacja wiedzy

### Powstawanie: Problem powtarzalny → Podobne rozwiązania → Uogólnienie → Dokumentacja → Walidacja → Katalogowanie

### Katalogi: POSA (wzorce architektoniczne), GoF (projektowe), EIP (integracja), PoEAA (Fowler), Cloud Patterns

### Przykładowe wzorce

**Layered (Warstwy):** Presentation → Business Logic → Data Access → DB. Separacja odpowiedzialności. Sztywne, boilerplate.

**Microservices:** Niezależne serwisy, osobne wdrożenia, skalowalność. Złożoność operacyjna.

**Event-Driven (EDA):** Producer → Event Broker (Kafka) → Consumers. Loose coupling, eventual consistency.

**CQRS:** Osobne modele Read/Write. Optymalizacja per-strona. Złożoność.

**Hexagonal (Ports & Adapters):** Core niezależny od frameworków. Testowalność.

| Wzorzec        | Skalowalność | Złożoność | Use Case            |
|----------------|--------------|-----------|---------------------|
| Monolith       | Niska        | Niska     | MVP, małe zespoły   |
| Layered        | Średnia      | Niska     | Enterprise CRUD     |
| Microservices  | Wysoka       | Wysoka    | Duże systemy        |
| Event-Driven   | Wysoka       | Średnia   | Real-time, IoT      |

### Etymologia

**POSA** — Pattern-Oriented Software Architecture (Buschmann et al., 1996). **GoF** — Gang of Four: Gamma, Helm, Johnson, Vlissides (1994, „Design Patterns"). **EIP** — Enterprise Integration Patterns (Hohpe & Woolf, 2003). **PoEAA** — Patterns of Enterprise Application Architecture (Martin Fowler, 2002). **Hexagonal** — Alistair Cockburn (2005); kształt sześciokąta nie ma specjalnego znaczenia. **CQRS** — Command Query Responsibility Segregation (Greg Young, ~2010); oparty na CQS Bertranda Meyera. **Microservices** — termin spopularyzowany ~2012 (James Lewis, Martin Fowler).

### Jak zapamiętać

- **„Monolith first"** — rozdzielaj gdy znasz granice domen
- **Wzorzec = Nazwa + Problem + Rozwiązanie + Konsekwencje**
- Katalogi: POSA = architektura, GoF = klasy/obiekty, EIP = messaging

\newpage

## PYTANIE 15: Agent upostaciowiony w robotyce

**Jak wykorzystuje się agenta upostaciowionego do specyfikacji sterowników robotów?**

---

### Tło pojęciowe — słowniczek

**Agent (w AI)** — autonomiczny byt, który postrzega środowisko (sensory), podejmuje decyzje (deliberacja) i wykonuje akcje (efektory). Agent ma cel i działa racjonalnie — wybiera akcje maksymalizujące osiągnięcie celu.

**Agent upostaciowiony (embodied agent)** — agent posiadający ciało fizyczne w rzeczywistym świecie. Przeciwieństwo agenta czysto softwareowego (np. chatbot). Robot = klasyczny agent upostaciowiony: ma sensory (kamery, LIDAR), ciało (ramię, koła) i działa w środowisku fizycznym. Kluczowe: musi radzić sobie z szumem sensorów, opóźnieniami, nieprzewidywalnością świata.

    Agent software:    dane → algorytm → wynik (deterministyczne)
    Agent embodied:    szum sensorów → niepewność → akcja fizyczna → efekt nieprzewidywalny

**Sterownik robota (robot controller)** — oprogramowanie decydujące co robot robi w każdej chwili. Specyfikacja sterownika = formalny opis zachowania robota. Agent upostaciowiony to model konceptualny, na którym opiera się sterownik.

---

**Cykl percepcja-deliberacja-akcja (See-Think-Act)** — podstawowy cykl działania agenta upostaciowionego:
1. **See (Percepcja)** — odczytaj dane z sensorów (obraz, odległość, pozycja)
2. **Think (Deliberacja)** — podejmij decyzję (planuj trasę, wybierz akcję)
3. **Act (Akcja)** — wyślij komendy do efektorów (silniki, chwytaki)

    Czujnik LIDAR → [Mapa otoczenia] → [Planowanie ścieżki] → [Silniki kół]
         See              Think                Think               Act

---

**3T Architecture (trójwarstwowa architektura sterownika):**
1. **Planner (deliberacja)** — planowanie symboliczne na wysokim poziomie. Czas reakcji: sekundy–minuty. Np. „zaplanuj trasę z A do B przez pokoje 1,2,3".
2. **Sequencer (wykonawca)** — koordynuje zachowania, FSM/Behavior Trees. Czas: 100ms–sekundy. Np. „Jedź do punktu → Obróć → Chwyć obiekt".
3. **Controller (reaktywny)** — bezpośrednie sterowanie sprzętem. Czas: milisekundy. Np. PID utrzymujący prędkość, unikanie kolizji.

    PLANNER       (minuty)    "Jedź do kuchni po kubek"
        ↓
    SEQUENCER     (sekundy)   "1: Jedź do drzwi → 2: Otwórz → 3: Jedź do blatu"
        ↓
    CONTROLLER    (ms)        "PID: prędkość lewego koła = 0.5 m/s"

---

**BDI (Beliefs-Desires-Intentions)** — formalny model agenta racjonalnego:
- **Beliefs** — wiedza agenta o świecie (mapa, pozycja, stan baterii). Może być niepełna/nieprecyzyjna.
- **Desires** — cele, które agent chciałby osiągnąć (np. „dotrzyj do punktu B").
- **Intentions** — aktualnie realizowany plan (podzbiór desires, do którego agent się zobowiązał).

Przykład: Robot-dostawca. Belief: „drzwi zamknięte". Desire: „dostarczyć paczkę do pokoju 5". Intention: „spróbuję drzwi boczne".

**FSM (Finite State Machine / automat skończony)** — model zachowania: skończona liczba stanów + przejścia warunkowe. Prosty, ale przy złożonych zachowaniach eksploduje liczba stanów i przejść.

    IDLE ──[wykryto cel]──→ APPROACH ──[blisko]──→ GRASP
      ↑                                              │
      └──────────────[obiekt chwycony]────────────────┘

**Behavior Tree (drzewo zachowań)** — nowoczesna alternatywa FSM. Hierarchiczna struktura: węzły wewnętrzne = logika (Selector, Sequence), liście = akcje/warunki. Modularny, reużywalny, łatwy do debugowania. Wywodzi się z AI w grach (Halo 2, ~2004).
- **Selector (?)** — wykonuj dzieci po kolei aż pierwszy sukces (jak OR)
- **Sequence (→)** — wykonuj dzieci po kolei, wstrzymaj przy porażce (jak AND)

---

**LTL (Linear Temporal Logic)** — logika temporalna do formalnej specyfikacji zachowań w czasie:
- **□ (always/globally)** — musi być prawdziwe ZAWSZE. □(¬collision) = „nigdy nie koliduj".
- **◇ (eventually)** — kiedyś musi być prawdziwe. ◇(at_goal) = „w końcu dotrzyj do celu".
- **Bezpieczeństwo (safety):** □(obstacle → ¬move_forward) — „zawsze: jeśli przeszkoda, nie jedź do przodu".
- **Żywotność (liveness):** ◇(at_goal) — „w końcu osiągnij cel".

**PID (Proportional-Integral-Derivative)** — klasyczny regulator sterowania. Minimalizuje błąd (różnicę między wartością zadaną a rzeczywistą). Trzy składniki:
- **P** — proporcjonalny: reaguje na aktualny błąd
- **I** — całkowy: eliminuje błąd stały (drift)
- **D** — różniczkowy: tłumi oscylacje

    Przykład: PID utrzymuje prędkość 1 m/s:
    Błąd = 1.0 - 0.8 = 0.2 → P zwiększa moc
    Błąd utrzymuje się? → I dodaje korektę
    Błąd maleje za szybko? → D hamuje

**ROS (Robot Operating System)** — middleware (nie OS!) do robotyki. Model pub/sub: węzły (nodes) publikują i subskrybują tematy (topics). Pozwala łączyć moduły (LIDAR, planowanie, sterowanie) w jednolity system. Open source, standard w akademii.

---

### Agent upostaciowiony = ciało fizyczne + sensory + efektory + środowisko

Cykl: **Percepcja → Deliberacja → Akcja** (See-Think-Act)

### Architektura sterownika — 3 warstwy (3T Architecture)

1. **PLANNER** (deliberacja) — planowanie symboliczne, sekundy–minuty
2. **SEQUENCER** (wykonawca) — FSM/Behavior Trees, 100ms–sekundy
3. **CONTROLLER** (reaktywny) — PID, unikanie kolizji, milisekundy

### Model formalny BDI
- **Beliefs** — mapa, pozycja, stan
- **Desires** — cel nawigacji
- **Intentions** — aktualny plan

### Specyfikacja w logice temporalnej (LTL)
- Bezpieczeństwo: □(obstacle → ¬move_forward)
- Żywotność: ◇(at_goal)

### Behavior Trees — nowoczesna specyfikacja zachowań
- Selector (?): wykonaj pierwszy sukces
- Sequence (→): wykonaj wszystkie po kolei
- Action/Condition jako liście

### ROS (Robot Operating System) — middleware pub/sub dla robotów

### Etymologia

**Agent upostaciowiony (Embodied)** — łac. „corpus" = ciało; agent posiadający ciało fizyczne w środowisku. **BDI** — Beliefs-Desires-Intentions; Michael Bratman (filozof, 1987); Rao & Georgeff (1991) przenieśli do AI. **LTL** — Linear Temporal Logic; Amir Pnueli (1977, Turing Award 1996). **PID** — Proportional-Integral-Derivative; Nicolas Minorsky (1922, sterowanie okrętami). **ROS** — Robot Operating System (Willow Garage, 2007). **Behavior Tree** — z game AI (Halo 2, ~2004); zaadaptowane w robotyce.

### Jak zapamiętać

- **„See-Think-Act"** = Percepcja → Deliberacja → Akcja
- **3T = Plan-Sequence-Control** (od abstrakcji do sprzętu)
- BDI = Beliefs, Desires, Intentions

\newpage

## PYTANIE 16: Języki programowania robotów

**Omówić specjalizowane języki. Uwypuklić klasyfikację.**

---

### Tło pojęciowe — słowniczek

**Robot** — cz. „robota" = ciężka praca; termin ukuty przez Karla Čapka (R.U.R., 1920). W przemyśle: programowalna maszyna wykonująca zadania (spawanie, paletyzacja, montaż). W kontekście pytania: głównie roboty przemysłowe (manipulatory).

**Język programowania robotów** — język do definiowania zachowania robota: ruchy, logika, I/O. Może być specjalizowany (dedykowany producenta) lub ogólny (C++, Python z bibliotekami). Klasyfikacja wg poziomu abstrakcji — od zadań po sygnały silników.

---

**Poziomy abstrakcji T-R-M-S:**

**Task-level (poziom zadania)** — najwyższy: opisujesz CO robot ma zrobić, nie JAK. „Podnieś A, połóż na B." Robot sam planuje ruchy. Przykłady: PDDL, Behavior Trees.

    // Task-level:
    pick(objectA);
    place(locationB);
    // Robot sam oblicza kinematykę, trajektorię, chwyt

**Robot-level (poziom robota)** — komendy ruchu w przestrzeni kartezjańskiej lub konfiguracyjnej: move_to(x,y,z), grasp(). Programista mówi GDZIE jechać, robot oblicza JAK (kinematyka odwrotna). Przykłady: RAPID (ABB), KRL (KUKA), Karel (FANUC).

    // RAPID (ABB):
    MoveL p1, v500, fine, tool1;  // liniowo do p1, prędkość 500 mm/s

**Motion-level (poziom ruchu)** — planowanie trajektorii: generowanie ciągu punktów od startu do celu z unikaniem kolizji. Kinematyka odwrotna, interpolacja. Przykłady: MoveIt (ROS), OMPL.

**Servo-level (poziom serwa)** — najniższy: bezpośrednie sterowanie silnikami/serwomechanizmami. Regulacja PID, sygnały PWM. Języki: C/C++, FPGA. Czas reakcji: mikro-milisekundy.

    Task:    "Zamontuj śrubę"          (sekundy)
    Robot:   MoveL do_pozycji           (100ms)
    Motion:  Trajektoria 50 pkt/s       (20ms)
    Servo:   PID: PWM silnika = 75%     (1ms)

---

**Kinematyka odwrotna (inverse kinematics, IK)** — obliczenie kątów w stawach robota, aby efektor (np. chwytak) znalazł się w zadanej pozycji. Problem odwrotny: znasz cel, szukasz konfiguracji. Może mieć 0, 1 lub wiele rozwiązań.

**Trajektoria (trajectory)** — zaplanowana ścieżka ruchu w czasie: sekwencja pozycji + prędkości + przyspieszenia. Interpolacja: liniowa (LIN), kołowa (CIRC), punkt-do-punktu (PTP).

---

**Języki producentów (vendor-specific):**
- **RAPID (ABB)** — Robotics Application Programming Interactive Dialogue. Ruchy: MoveJ (joint), MoveL (linear), MoveC (circular).
- **KRL (KUKA Robot Language)** — PTP (point-to-point), LIN (linear), CIRC (circular). Pascal-like syntax.
- **Karel (FANUC)** — od Karla Čapka. MOVE TO target. Pascal-like.
- **PDL2 (Comau)** — MOVE LINEAR TO. Proceduralne.

**Vendor lock-in** — każdy producent ma WŁASNY język. Program napisany w RAPID nie działa na robocie KUKA. To motywacja dla ROS i standardów.

**Online vs Offline programming:**
- **Online (teach-in)** — operator prowadzi robota „za rękę" (pendant/teach pendant), robot zapamiętuje punkty. Proste, ale wymaga zatrzymania produkcji.
- **Offline** — programowanie w symulacji (CAD/CAM), bez zatrzymywania robota. Transferujesz gotowy program.

---

**ROS (Robot Operating System)** — middleware (nie OS!) do robotyki. Model pub/sub: węzły publikują/subskrybują tematy. Uniwersalny — działa z robotami różnych producentów. Głównie Python/C++. Wada: nie nadaje się do hard real-time (soft real-time OK; ROS 2 poprawia).

**MoveIt** — biblioteka ROS do planowania ruchu manipulatorów. Obejmuje: IK, collision avoidance, trajectory planning. Open source.

**PDDL (Planning Domain Definition Language)** — język opisu problemów planowania. Definiujesz: stany, akcje, warunki, cel. Planner automatycznie znajduje sekwencję akcji. Task-level.

**FPGA (Field-Programmable Gate Array)** — programowalny układ logiczny. Dla servo-level: przetwarzanie sygnałów w nanosekundach. Szybszy niż mikrokontroler, ale trudniejszy w programowaniu.

---

### Klasyfikacja wg poziomu abstrakcji: **T-R-M-S**

1. **Task-level** — „Podnieś A, połóż na B" (PDDL, Behavior Trees)
2. **Robot-level** — move_to(), grasp() (RAPID, KRL, Karel, ROS)
3. **Motion-level** — trajektorie, kinematyka odwrotna (MoveIt, OMPL)
4. **Servo-level** — PID, sterowanie silnikami (C/C++, FPGA)

### Klasyfikacja wg metody: Online (teach-in, pendant) vs Offline (symulacja, CAD)

### Języki producentów

| Producent | Język | Ruchy              |
|-----------|-------|--------------------|
| ABB       | RAPID | MoveJ, MoveL, MoveC|
| KUKA      | KRL   | PTP, LIN, CIRC     |
| FANUC     | Karel | MOVE TO            |
| Comau     | PDL2  | MOVE LINEAR TO     |

### Uniwersalne: ROS + Python/C++, MoveIt (planowanie manipulatora), Orocos (real-time)

### Graficzne: RobotStudio (ABB), ROBOGUIDE (FANUC), Blockly (edukacja)

### Etymologia

**RAPID** — Robotics Application Programming Interactive Dialogue (ABB). **KRL** — KUKA Robot Language. **Karel** — od Karla Čapka, czeskiego pisarza, który ukuł słowo „robot" (cz. „robota" = ciężka/przymusowa praca) w sztuce R.U.R. (1920). **PDDL** — Planning Domain Definition Language. **MoveIt** — open source do planowania ruchu manipulatora (Willow Garage/PickNik). **Robot** — cz. „robota" = pańszczyzna; Karel Čapek, R.U.R. (1920).

### Jak zapamiętać

- **„Od zadania do serwa: T-R-M-S"**
- Każdy producent ma WŁASNY język (vendor lock-in)
- ROS próbuje ujednolicić, ale nie dla hard real-time

\newpage

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

### Notacja Grahama: **α | β | γ**

- **α** — środowisko maszynowe: 1 (jedna), Pm (m równoległych), F (flow shop), J (job shop)
- **β** — charakterystyki zadań: rⱼ (release dates), dⱼ (due dates), pmtn (preemption), prec (precedencje)
- **γ** — kryterium: Cmax (makespan), ΣCⱼ, Lmax, ΣTⱼ, ΣUⱼ

### Klasyczne reguły optymalne

| Reguła   | Problem      | Opis                          |
|----------|-------------|-------------------------------|
| **SPT**  | 1 \|\| ΣCⱼ   | Najkrótsze najpierw           |
| **EDD**  | 1 \|\| Lmax  | Najwcześniejszy termin        |
| **Johnson** | F2 \|\| Cmax | Optymalny dla 2-maszynowego flow shop |

### Przykład: 1 || ΣCⱼ z regułą SPT

Zadania: J1(5), J2(3), J3(8), J4(2), J5(6)
Posortowane SPT: J4(2), J2(3), J1(5), J5(6), J3(8)
Czasy zakończenia: 2, 5, 10, 16, 24
**ΣCⱼ = 57** (optymalne!)

**Dowód:** zamiana sąsiednich i,j gdzie pᵢ > pⱼ zawsze zwiększa ΣC.

### Złożoność: Większość problemów **NP-trudna** (Job shop, Pm||Cmax dla m≥2)

### Etymologia

**Notacja Grahama** — Ronald Graham (Bell Labs, 1966–1979); znany też z liczby Grahama. **SPT** — Shortest Processing Time. **EDD** — Earliest Due Date. **Johnson** — Selmer Johnson (RAND, 1954). **Makespan** — „make" (ukończyć) + „span" (rozpiętość); czas od startu do końca wszystkich zadań. **Flow shop** — zadania „płyną" przez maszyny w tej samej kolejności (jak taśma). **Job shop** — każde zadanie ma indywidualną trasę. **NP-trudny** — Non-deterministic Polynomial-time hard.

### Jak zapamiętać

- **α|β|γ = Maszyny|Zadania|Cel**
- **SPT = „Short first"** — krótsze pierwsze dla sumy Cⱼ
- **EDD = „Early Due Date"** — najwcześniejszy termin dla Lmax

\newpage

## PYTANIE 18: Zarządzanie zapasami w łańcuchu dostaw

**Problemy i przykładowy model.**

---

### Tło pojęciowe — słowniczek

**Łańcuch dostaw (supply chain)** — sieć organizacji od surowca do klienta końcowego: dostawcy → producenci → dystrybutorzy → detaliści → klienci. Zarządzanie zapasami na każdym ogniwie ma ogromny wpływ na koszty i poziom obsługi.

    Dostawca → [Magazyn] → Producent → [Magazyn] → Dystrybutor → [Magazyn] → Sklep → Klient
                                    zapasy na każdym etapie!

**Zapasy (inventory)** — produkty/materiały przechowywane „na wszelki wypadek" lub w oczekiwaniu na sprzedaż/produkcję. Za dużo = zamrożony kapitał, koszty magazynowania, ryzyko przeterminowania. Za mało = brak towaru (stockout), utrata klientów.

---

**Bullwhip Effect (efekt byczego bicza)** — zjawisko amplifikacji wahań popytu w górę łańcucha dostaw. Mała zmiana popytu u detalisty (np. +5%) powoduje coraz większe wahania zamówień u dystrybutorów (+10%), producentów (+20%), dostawców (+40%).

    Klient: popyt +5% → Detalista zamawia +10% → Dystrybutor +20% → Producent +40%
    Jak bicz: mały ruch ręki → ogromny ruch na końcu

Przyczyny: prognozowanie (forecasting), zamawianie partiami (batching), promocje cenowe, racjonowanie przy niedoborach.

**Stockout (brak towaru)** — sytuacja gdy produkt jest niedostępny. Koszt: utrata sprzedaży, utrata klienta, kary umowne.

**Overstock (nadmiar zapasów)** — za dużo towaru. Koszt: magazynowanie, zamrożony kapitał, obsolescence (przeterminowanie/utrata aktualności).

---

**Koszty zapasów — trzy kategorie:**

**Koszt utrzymania (holding cost, h)** — koszt przechowywania towaru per jednostka per rok. Obejmuje: magazyn, ubezpieczenie, koszt kapitału, utrata wartości. Typowo: 15-30% wartości towaru rocznie.

**Koszt zamawiania (ordering cost, K)** — stały koszt złożenia jednego zamówienia. Obejmuje: transport, administracja, kontrola jakości. Niezależny od ilości zamówionej.

**Koszt braku (shortage cost, p)** — koszt gdy nie mamy towaru: utrata sprzedaży, ekspresowe dostawy, kary.

---

**EOQ (Economic Order Quantity)** — model Harrisa-Wilsona (1913). Najstarszy model zarządzenia zapasami. Znajduje optymalną wielkość zamówienia Q* minimalizującą łączny koszt (zamawianie + utrzymanie).

**Założenia EOQ:** popyt stały i znany (D szt/rok), lead time = 0, brak braków, koszt zamówienia K, koszt utrzymania h.

**Wzór EOQ:**

    Q* = √(2KD/h)

    TC(Q) = K·D/Q    +    h·Q/2
            koszt         koszt
         zamawiania    utrzymania

**Dlaczego √?** Bo koszty zamawiania maleją z Q (mniej zamówień), a koszty utrzymania rosną z Q (więcej w magazynie). Optimum = punkt przecięcia.

**Przykład liczbowy:**

    D = 10 000 szt/rok, K = 100 PLN/zamówienie, h = 2 PLN/szt/rok
    Q* = √(2 × 100 × 10000 / 2) = √1 000 000 = 1000 szt
    Liczba zamówień = 10000/1000 = 10/rok
    TC* = √(2 × 100 × 10000 × 2) = 2000 PLN/rok

---

**Lead time (czas realizacji, L)** — czas od złożenia zamówienia do otrzymania dostawy. Np. 5 dni. Kluczowy dla punktu zamawiania.

**ROP (Reorder Point / punkt zamawiania)** — poziom zapasu, przy którym składamy nowe zamówienie:

    ROP = d × L + SS
    d = popyt dzienny, L = lead time, SS = safety stock

**Safety stock (zapas bezpieczeństwa, SS)** — dodatkowy bufor na wypadek wahań popytu lub opóźnień dostawy:

    SS = z × σ_L
    z = kwantyl rozkładu normalnego (np. 1.65 dla 95% poziomu obsługi)
    σ_L = odchylenie standardowe popytu w lead time

    Przykład: d=30 szt/dzień, L=5 dni, SS=50 szt
    ROP = 30×5 + 50 = 200 szt
    Gdy stan spada do 200 → zamawiaj!

---

**Modele zaawansowane:**
- **(s, Q)** — gdy stan spadnie do s, zamów dokładnie Q sztuk. (s = ROP, Q = EOQ)
- **(s, S)** — gdy stan spadnie do s, zamów „do poziomu S" (order-up-to). Wielkość zamówienia zmienna.
- **(R, S)** — co R dni (stały cykl) zamów „do poziomu S". Prostsze administracyjnie.
- **VMI (Vendor Managed Inventory)** — dostawca zarządza zapasami klienta (np. Walmart + P&G). Dostawca widzi dane sprzedażowe i sam decyduje kiedy dostarczyć.

---

### Problemy

- **Bullwhip Effect** — amplifikacja wahań popytu w górę łańcucha (detaliści → dystrybutorzy → producenci → dostawcy). Przyczyny: forecasting, batching, promocje.
- Stockouts vs Overstock, obsolescence, lead time variability, demand uncertainty

### Koszty: Utrzymania (h) + Zamawiania (K) + Braku (p)

### Model EOQ (Economic Order Quantity) — Harris-Wilson

**Założenia:** popyt stały D, lead time = 0, koszt zamówienia K, koszt utrzymania h.

    TC(Q) = K·D/Q + h·Q/2

    Optymalna wielkość: Q* = √(2KD/h)
    Opt. koszt: TC* = √(2KDh)

**Przykład:** D=10000, K=100, h=2 → Q*=1000, TC*=2000 PLN/rok

### Punkt zamawiania (ROP)

    ROP = d × L + SS     (popyt dzienny × lead time + safety stock)
    SS = z × σ_L          (z z tablic normalnych, np. 1.65 dla 95%)

### Modele zaawansowane: (s,Q), (s,S), (R,S), VMI (Vendor Managed Inventory)

### Etymologia

**EOQ** — Economic Order Quantity; Ford W. Harris (1913, „How Many Parts To Make At Once") — jedno z najstarszych zastosowań badań operacyjnych. **Bullwhip Effect** — Procter & Gamble (1990s) nadali nazwę; Jay Forrester (MIT, 1961) pierwszy opisał jako „demand amplification"; „bullwhip" = bicz pasterski. **ROP** — Reorder Point. **VMI** — Vendor Managed Inventory (Walmart + P&G, lata 80.). **Safety stock** — zapas bezpieczeństwa na wypadek wahań popytu/dostaw.

### Jak zapamiętać

- **EOQ = √(2KD/h)** — zapamiętaj formułę!
- **ROP = d×L + SS** — kiedy zamawiać
- **Bullwhip = bicz** — małe wahania na końcu → duże na początku łańcucha

\newpage

## PYTANIE 19/29: Model Publish-Subscribe

**Scharakteryzować model i przykładowe rozwiązania techniczne.**

---

### Tło pojęciowe — słowniczek

**Pub/Sub (Publish-Subscribe)** — wzorzec komunikacji: nadawcy (publishers) wysyłają wiadomości, NIE wiedząc kto je odbierze. Odbiorcy (subscribers) deklarują zainteresowanie i otrzymują dopasowane wiadomości. Między nimi stoi **broker** (pośrednik). Metafora: radio — nadawca nadaje, kto chce słucha.

    Publisher A ──→ ┌─────────┐ ──→ Subscriber X
    Publisher B ──→ │  BROKER │ ──→ Subscriber Y
    Publisher C ──→ └─────────┘ ──→ Subscriber Z

**Dlaczego nie bezpośrednio?** Bo publisher musiałby znać wszystkich subscriberów, zarządzać połączeniami, retransmitować. Broker rozwiązuje to centralnie.

---

**Publisher (nadawca)** — komponent wysyłający wiadomości (eventy/zdarzenia) do brokera. Nie wie, kto subskrybuje. Przykład: czujnik temperatury publikuje odczyt co 5 sekund.

**Subscriber (odbiorca)** — komponent rejestrujący się u brokera na określone tematy/typy wiadomości. Otrzymuje wiadomości pasujące do subskrypcji. Przykład: alarm subskrybuje temat „temperatura" i reaguje gdy >50°C.

**Broker (pośrednik)** — centralny komponent routujący wiadomości od publishers do subscribers. Odpowiada za: filtrowanie, dostarczanie, buforowanie, gwarancje dostarczenia.

**Luźne powiązanie (loose coupling)** — publisher i subscriber nie znają się nawzajem. Można dodać nowego subscribera bez zmiany publishera. Fundamentalna zaleta pub/sub.

---

**Typy subskrypcji:**
- **Topic-based** — subscriber subskrybuje temat (np. „orders.created"). Najprostszy i najpopularniejszy.
- **Content-based** — filtrowanie po treści wiadomości (np. „price > 100"). Bardziej elastyczny, ale wolniejszy.
- **Type-based** — filtrowanie po typie wiadomości (np. klasa OrderEvent).
- **Hierarchical (wildcards)** — wzorce tematów: `orders.*` dopasowuje `orders.created`, `orders.cancelled`.

    Topic: "sensors/temperature/room1"
    Wildcard: "sensors/temperature/#"  → dopasowuje room1, room2, ...

---

**QoS (Quality of Service)** — gwarancje dostarczenia wiadomości:
- **At-most-once** — wiadomość dostarczana 0 lub 1 raz. „Fire and forget." Najszybszy, ryzyko utraty. Użycie: logi, metryki.
- **At-least-once** — wiadomość dostarczana ≥1 raz. Mogą być duplikaty. Użycie: płatności (z idempotencją).
- **Exactly-once** — wiadomość dostarczana dokładnie 1 raz. Najtrudniejszy do zaimplementowania. Użycie: transakcje finansowe.

    At-most-once:   send → ✓ lub ✗ (nie retransmituj)
    At-least-once:  send → ack? retry → może duplikat
    Exactly-once:   send → ack + deduplikacja (najkosztowniejszy)

---

**Kafka (Apache Kafka)** — rozproszony log. Model pull: konsument sam ciągnie wiadomości ze logu. Wiadomości **przechowywane** na dysku (retention 7 dni default). Partycje + Consumer Groups = równoległy odczyt. Bardzo wysoka przepustowość (miliony msg/s). LinkedIn (2011). Exactly-once z transakcjami.

    Kafka = rozproszony, trwały LOG
    Topic: [msg1][msg2][msg3][msg4][msg5]  ← append-only
    Consumer czyta od dowolnego offsetu (może cofnąć!)

**RabbitMQ** — klasyczna kolejka wiadomości (message queue). Model push: broker dostarcza do konsumenta. Protokół AMQP. Exchange types: Direct (klucz), Topic (*, #), Fanout (broadcast), Headers. Elastyczny routing. Wiadomości konsumowane → usunięte z kolejki.

    RabbitMQ: Publisher → Exchange → Queue → Consumer
    Wiadomość skonsumowana = znika z kolejki

**MQTT (Message Queuing Telemetry Transport)** — ultralekkiprotokół pub/sub. 2-bajtowy nagłówek! Zaprojektowany dla IoT i urządzeń z ograniczonymi zasobami (sensory, mikrokontrolery). IBM (1999) do monitoringu rurociągów naftowych przez satelitę. Brokers: Mosquitto, HiveMQ.

**Redis Pub/Sub** — pub/sub wbudowany w Redis (in-memory database). Szybki, ale BEZ persistencji — jeśli subscriber był offline, wiadomość przepada. Dla real-time (chat, live updates).

    Cecha           Kafka         RabbitMQ      MQTT          Redis
    ────────────────────────────────────────────────────────────────
    Model           Pull (log)    Push (queue)  Push          Push
    Persistencja    Tak           Opcjonalna    Retained msg  Nie
    Throughput      Bardzo wysoki Wysoki        Niski-średni  Wysoki
    Use case        Streaming     Task queues   IoT           Real-time

---

**SPOF (Single Point of Failure)** — broker jako centralny punkt: jeśli padnie, cała komunikacja się zatrzymuje. Rozwiązanie: klasteryzacja brokera (Kafka cluster, RabbitMQ cluster).

**AMQP (Advanced Message Queuing Protocol)** — otwarty protokół messaging. Standard implementowany przez RabbitMQ. Definiuje: exchange, queue, binding, ack.

---

### Model Pub/Sub

Publishers → **Broker** (router/message bus) → Subscribers
- Luźne powiązanie (publisher nie zna subscriberów)
- Asynchroniczne, skalowalne (1:N, N:M)

### Typy subskrypcji: topic-based, content-based, type-based, hierarchical (wildcards)

### Gwarancje dostarczenia (QoS): At-most-once, At-least-once, Exactly-once

### Rozwiązania techniczne

| Technologia  | Model          | Persistence | Throughput    | Use Case      |
|--------------|----------------|-------------|---------------|---------------|
| **Kafka**    | Pull (log)     | Tak         | Bardzo wysoki | Event streaming|
| **RabbitMQ** | Push (queue)   | Opcjonalne  | Wysoki        | Task queues   |
| **MQTT**     | Push           | Retained    | Niski-średni  | IoT           |
| **Redis**    | Push           | Nie         | Wysoki        | Real-time     |

**Kafka:** Partycje + Consumer Groups, distributed log, exactly-once z transakcjami.
**RabbitMQ:** AMQP, Exchange types (Direct, Topic, Fanout, Headers), flexible routing.
**MQTT:** Lekki (2-byte header), idealny dla IoT/constrained devices, brokers: Mosquitto, HiveMQ.

### Zalety / Wady

Zalety: decoupling, skalowalność, asynchroniczność, broadcast.
Wady: debugging trudniejsze, ordering challenges, broker = SPOF.

### Etymologia

**Kafka** — od Franza Kafki (pisarz); Jay Kreps (LinkedIn, 2011): „system zoptymalizowany do pisania — a Kafka był pisarzem". **RabbitMQ** — „rabbit" = szybkość; AMQP = Advanced Message Queuing Protocol. **MQTT** — Message Queuing Telemetry Transport; Andy Stanford-Clark (IBM) + Arlen Nipper (1999); do monitoringu rurociągów naftowych przez satelitę. **Redis** — REmote DIctionary Server (Salvatore Sanfilippo, 2009). **Pub/Sub** — publish-subscribe; wzorzec z systemów event-driven (lata 80/90). **QoS** — Quality of Service.

### Jak zapamiętać

- **„Pub/Sub = Radio"** — nadawca nadaje, kto chce słucha
- **Kafka = Log** (przechowuje historię), **RabbitMQ = Queue** (konsumuje i kasuje)
- **MQTT = IoT** — lekki, mały overhead

\newpage

## PYTANIE 20/30: Analityka danych strumieniowych

**Rozwiązania analityczne na danych strumieniowych.**

---

### Tło pojęciowe — słowniczek

**Dane strumieniowe (streaming data)** — ciągły, potencjalnie nieskończony przepływ zdarzeń (events) przychodzących w czasie rzeczywistym. Przykłady: kliknięcia użytkowników, odczyty sensorów IoT, transakcje bankowe, logi serwerów. W odróżnieniu od danych wsadowych (batch): nie możesz „poczekać na wszystkie" — musisz analizować na bieżąco.

    Batch:      [cały zbiór] → analiza → wynik     (minuty/godziny)
    Streaming:  event → event → event → ...→ analiza ciągła    (ms/sekundy)

**Strumień (stream)** — abstrakcja: nieograniczona (unbounded) sekwencja zdarzeń, każde ze stemplem czasowym. Musisz przetwarzać „w locie" — nie mieścisz wszystkiego w pamięci.

---

**Event Time vs Processing Time:**
- **Event Time** — moment GDY zdarzenie nastąpiło (np. kliknięcie o 14:00:05)
- **Processing Time** — moment GDY system przetwarza zdarzenie (np. o 14:00:07)
- Różnica wynika z opóźnień sieciowych. Zdarzenia mogą przychodzić **out-of-order** (pozamiejscowe).

    Zdarzenie A (event time 14:00:01) → dociera o 14:00:05
    Zdarzenie B (event time 14:00:03) → dociera o 14:00:04
    B dociera PRZED A, mimo że A było wcześniej!

**Watermark** — znacznik postępu: „z dużym prawdopodobieństwem nie przyjdą już zdarzenia z event time < W". Pozwala systemowi zdecydować, kiedy zamknąć okno i wyemitować wynik. Zdarzenia po watermarku = „late data" (spóźnione).

---

**Okno czasowe (window)** — mechanizm grupowania zdarzeń w strumienia w skończone porcje do analizy:

**Tumbling window (okno przerzutne)** — stały rozmiar, rozłączne. Np. „liczba kliknięć co 5 minut".

    |---5min---|---5min---|---5min---|
    [events A] [events B] [events C]   ← 0 nakładania

**Sliding window (okno przesuwne)** — stały rozmiar + krok przesunięcia. Nakładają się. Np. „średnia z 10 min, co 1 min".

    |----10min----|
       |----10min----|
          |----10min----|              ← nakładanie

**Session window (okno sesji)** — dynamiczny rozmiar, oparte na aktywności. Nowa sesja po przerwie (gap). Np. „sesja użytkownika: od pierwszego kliknięcia do 30 min nieaktywności".

**Global window** — jedno okno na cały strumień. Trigger decyduje kiedy wyemitować wynik.

---

**True streaming vs Micro-batch:**
- **True streaming** — przetwarzanie event-by-event. Niższa latencja. Kafka Streams, Flink.
- **Micro-batch** — grupowanie zdarzeń w małe paczki (np. co 100ms) i przetwarzanie batch. Spark Streaming. Prostsza semantyka, ale wyższa latencja.

**Kafka Streams** — biblioteka (nie klaster!) do przetwarzania strumieni Kafka. Działa w procesie aplikacji Java. Niska latencja, exactly-once. Stateful processing (windows, joins).

**Apache Flink** — rozproszony silnik do true streaming. Bardzo niska latencja (<10ms). Natywne wsparcie event time, windows, stateful processing. Exactly-once. Deployment jako klaster.

**Spark Streaming** — rozszerzenie Apache Spark. Model micro-batch (~100ms+). Średnia latencja, ale korzysta z ekosystemu Spark (SQL, ML). Exactly-once.

---

**Algorytmy strumieniowe (probabilistyczne):**

**HyperLogLog** — estymacja liczby unikalnych elementów (cardinality). Zużywa O(1) pamięci (~1.5 KB) niezależnie od liczby elementów. Błąd ~2%.

    100 mln unikalnych URL-i → HyperLogLog odpowiada "~100 mln ± 2%"
    Pamięć: 1.5 KB zamiast ~800 MB (hash set)

**Count-Min Sketch** — estymacja częstości elementów. Macierz d×w z hashami. Gwarantuje overestimates (nigdy nie zaniży). O(1) per query/update.

    "Ile razy pojawił się IP 192.168.1.1?" → CMS: ~4523 (± ε·N)

**Reservoir Sampling** — równomierne próbkowanie k elementów ze strumienia o nieznanym rozmiarze n. Każdy element ma szansę k/n. O(k) pamięci.

**Late data strategies:**
- **Drop** — odrzuć spóźnione zdarzenia
- **Recompute** — przelicz okno ponownie
- **Side output** — przekieruj do osobnego strumienia do ręcznej analizy
- **Allowed lateness** — czekaj dodatkowy czas przed zamknięciem okna

---

### Charakterystyka strumieni
- Nieograniczone (unbounded), ciągłe, niska latencja wymagana
- Event Time vs Processing Time — mogą się różnić, out-of-order

### Okna czasowe (Windowing)

1. **Tumbling** — rozłączne, stały rozmiar
2. **Sliding** — nakładające się (size + slide)
3. **Session** — oparte na aktywności (gap between events)
4. **Global** — jedno okno, trigger decyduje emisję

### Platformy

| Cecha          | Kafka Streams      | Flink            | Spark Streaming  |
|----------------|--------------------|------------------|------------------|
| Model          | True streaming     | True streaming   | Micro-batch      |
| Deployment     | Library            | Cluster          | Cluster          |
| Latency        | Niska              | Bardzo niska     | Średnia (~100ms) |
| Exactly-once   | Tak                | Tak              | Tak              |

### Algorytmy strumieniowe

- **HyperLogLog** — zliczanie unikalnych, O(1) space, ~2% error
- **Count-Min Sketch** — estymacja częstości, overestimates
- **Reservoir Sampling** — równomierne próbkowanie k z n nieznanego

### Obsługa opóźnień: Watermarks + late data strategies (drop, recompute, side output, allowed lateness)

### Etymologia

**Flink** — niem. „flink" = zwinny/szybki (TU Berlin, 2014). **Spark** — „iskra"; Matei Zaharia (UC Berkeley, 2012). **HyperLogLog** — Philippe Flajolet et al. (2007); „Hyper" = ulepszenie LogLog; „LogLog" = zużywa log(log(n)) pamięci. **Count-Min Sketch** — Cormode & Muthukrishnan (2005); „sketch" = probabilistyczny skrót danych. **Reservoir Sampling** — Jeffrey Vitter (1985); „reservoir" = stały zbiornik prób. **Watermark** — znacznik postępu czasu zdarzeń w strumieniu.

### Jak zapamiętać

- **4 okna: „TSSG"** — Tumbling, Sliding, Session, Global
- **Flink = szybki (true streaming)**, Spark = safe (micro-batch)
- **HyperLogLog = „ile unikalnych?" z kilobajtem pamięci**

\newpage

## PYTANIE 21: Zegary logiczne i wektory stempli czasowych

**Koncepcja i przeznaczenie.**

---

### Tło pojęciowe — słowniczek

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

Właściwość: a → b ⟹ C(a) < C(b) (TAK). Ale: C(a) < C(b) **NIE** implikuje a → b! Nie wykrywa współbieżności.

    P1: [A:1]──msg──→[C:2]                P1 events: A(1), C(2)
    P2:          [B:1]──────[D:3]          P2 events: B(1), D(3)
    C(A)=1, C(B)=1 → Lamport nie wie czy A||B czy A→B!

---

**Zegar wektorowy (vector clock)** — każdy z N procesów utrzymuje wektor V[1..N]. V_i[j] = „ile zdarzeń procesu j jest mi znanych". Algorytm:
1. Przed własnym zdarzeniem: V_i[i]++
2. Przy wysyłaniu: dołącz cały wektor V_i
3. Przy odbieraniu (wektor T): V_i[j] = max(V_i[j], T[j]) ∀j, potem V_i[i]++

Właściwość: a → b **⟺** V(a) < V(b). Pełna charakteryzacja! Wykrywa współbieżność.

    V(a) < V(b) ⟺ ∀i: V(a)[i] ≤ V(b)[i] i ∃j: V(a)[j] < V(b)[j]
    V(a) || V(b) ⟺ ¬(V(a) ≤ V(b)) ∧ ¬(V(b) ≤ V(a))

    Przykład (2 procesy):
    P1: A=[1,0] → wysyła msg → C=[2,1]
    P2: B=[0,1] → odbiera msg → D=[2,2]
    A||B? V(A)=[1,0], V(B)=[0,1] → 1>0 ale 0<1 → TAK, współbieżne!

---

**Porównanie Lamport vs Vector:**

    Cecha                  Lamport        Vector
    ───────────────────────────────────────────────
    Rozmiar per zdarzenie  O(1) (skalar)  O(N) (wektor)
    a→b ⟹ C(a)<C(b)       TAK            TAK
    C(a)<C(b) ⟹ a→b       NIE            TAK
    Wykrywa współbieżność  NIE            TAK

**Dlaczego O(N) to problem?** W systemie z 1000 węzłów każda wiadomość niesie wektor 1000 liczb. Dla milionów wiadomości = duży overhead. W praktyce: version vectors (kompresja), Dynamo używa wektorów wersji.

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

\newpage

## PYTANIE 22: Modele spójności danych w systemach rozproszonych

**Silne i słabe modele spójności.**

---

### Tło pojęciowe — słowniczek

**Spójność danych (consistency)** — gwarancja, że wszystkie węzły systemu rozproszonego widzą te same dane w przewidywalny sposób. Pytanie: gdy zapisuję na węzeł A, co odczyta węzeł B? Odpowiedź zależy od modelu spójności.

**Replikacja (replication)** — przechowywanie kopii danych na wielu węzłach. Cel: dostępność (awaria jednego → dane na innym), wydajność (odczyt z najbliższego). Problem: aktualizujesz jedną kopię — kiedy reszta się zsynchronizuje?

    Zapis na replice A: x = 5
    Replika B: x = ? (jeszcze 3? już 5?)
    Odpowiedź zależy od modelu spójności!

---

**Linearizability (linearyzowalność)** — najsilniejszy model. Każda operacja wygląda jakby nastąpiła atomowo w jednym momencie między jej wywołaniem a odpowiedzią. System zachowuje się jak JEDNA kopia danych. Wymaga consensus (np. Paxos, Raft) — kosztowna.

    Klient A pisze x=5 o 14:00:01, dostaje OK o 14:00:02
    Klient B czyta x o 14:00:01.5 → MUSI dostać 5 (bo zapis "nastąpił" gdzieś w 14:00:01-02)

Przykład: Google Spanner (zegary atomowe TrueTime).

**Sequential consistency (spójność sekwencyjna)** — globalny porządek operacji zgodny z porządkiem programu KAŻDEGO procesu. Ale NIE musi odpowiadać czasowi rzeczywistemu. Słabsza niż linearyzowalność.

    Proces A: write(x,1), write(x,2)
    Proces B: read(x)→2, read(x)→1  ← NIE OK (B widzi operacje A w złej kolejności)
    Proces B: read(x)→1, read(x)→2  ← OK (zgodne z kolejnością A)

---

**Causal consistency (spójność przyczynowa)** — operacje przyczynowo zależne widziane w tej samej kolejności przez wszystkich. Operacje współbieżne (niezależne) mogą być widziane w różnej kolejności. Wymaga vector clocks.

    A pisze x=1 → B czyta x(=1) → B pisze y=2
    Przyczynowość: write(x,1) → write(y,2)
    Każdy musi widzieć write(x,1) PRZED write(y,2)

**Session guarantees (gwarancje sesji):**
- **Read Your Writes** — jeśli zapisałem x=5, mój następny odczyt zobaczy 5 (nie starą wartość)
- **Monotonic Reads** — odczyty nie „cofają się w czasie" (jeśli widziałem x=5, nie zobaczę x=3)
- **Monotonic Writes** — moje zapisy są stosowane w kolejności
- **Writes Follow Reads** — jeśli przeczytałem x i na tej podstawie zapisałem y, inni widzą x przed y

**Eventual consistency (spójność ostateczna)** — najsłabszy model. Jeśli przestaniesz pisać, KIEDYŚ wszystkie odczyty zwrócą tę samą wartość. Ale „kiedyś" może trwać sekundy lub minuty! Najszybszy i najskalowalniejszy. Przykłady: DNS, Cassandra.

    Zapis x=5 na replice A
    Replika B: jeszcze x=3... x=3... [replikacja]... x=5 ← w końcu!

---

**CAP Theorem (twierdzenie Brewera)** — w systemie rozproszonym przy partycji sieciowej (P) musisz wybrać między Consistency (C) a Availability (A):
- **CP** — spójny, ale niedostępny przy partycji (np. HBase, Spanner)
- **AP** — dostępny, ale niespójny przy partycji (np. Cassandra, DynamoDB)
- Bez partycji możesz mieć oba. Ale partycje SĄ nieuniknione w sieci.

    Partycja = węzły A i B nie mogą się komunikować
    CP: odmów operacji (niedostępny) → zachowaj spójność
    AP: wykonaj operację (dostępny) → ryzykuj niespójność

---

**Consensus (uzgadnianie)** — protokół, w którym rozproszone węzły zgadzają się na jedną wartość pomimo awarii. Kluczowy dla linearyzowalności. Algorytmy: Paxos (Lamport), Raft (prostszy), Zab (Zookeeper).

**Quorum** — minimalna liczba węzłów, które muszą potwierdzić operację.

    N = liczba replik, W = quorum zapisu, R = quorum odczytu
    W + R > N → gwarantuje odczyt najnowszej wartości
    Np. N=3, W=2, R=2: zawsze przynajmniej 1 wspólna replika

**CRDTs (Conflict-free Replicated Data Types)** — struktury danych, które automatycznie zbiegają do spójnego stanu bez koordynacji. Matematycznie gwarantują brak konfliktów. Przykłady: G-Counter (grow-only counter), OR-Set (observed-remove set). Idealne dla eventual consistency.

**LWW (Last-Writer-Wins)** — prosty mechanizm rozwiązywania konfliktów: wygrywa zapis z najnowszym timestampem. Problem: wymaga zsynchronizowanych zegarów i może tracić dane.

---

### Spektrum (od silnego do słabego)

    Linearizability → Sequential → Causal → Session → Eventual

### Silne modele

**Linearizability:** Każda operacja wygląda atomowo w momencie między wywołaniem a odpowiedzią. Najsilniejsza. „Globalny czas rzeczywisty." Kosztowna (consensus). Przykład: Spanner.

**Sequential Consistency:** Globalny porządek operacji zgodny z porządkiem programu każdego procesu, ale NIE z czasem rzeczywistym. Przykład: Zookeeper.

### Słabe modele

**Causal Consistency:** Operacje przyczynowo zależne widziane w tej samej kolejności. Niezależne mogą być w różnej. Wymaga vector clocks. Przykład: MongoDB.

**Session Guarantees:** Read Your Writes, Monotonic Reads, Monotonic Writes, Writes Follow Reads.

**Eventual Consistency:** Jeśli brak nowych zapisów, ostatecznie wszystkie odczyty zwrócą tę samą wartość. Najsłabszy, najszybszy. Przykład: DNS, Cassandra.

### CAP Theorem: Consistency + Availability + Partition tolerance — wybierz 2 (w obecności partycji: C lub A).

### Rozwiązywanie konfliktów: LWW (Last-Writer-Wins), Siblings (multi-value), **CRDTs** (automatycznie zbieżne struktury).

### Etymologia

**Linearizability** — Maurice Herlihy + Jeannette Wing (1990); łac. „linearis" = w linii. **Sequential consistency** — Leslie Lamport (1979). **Causal consistency** — Ahamad et al. (1995); łac. „causa" = przyczyna. **CAP** — Eric Brewer (UC Berkeley, 2000, „Brewer's conjecture"); udowniony przez Gilbert & Lynch (2002). **CRDTs** — Conflict-free Replicated Data Types (Marc Shapiro et al., 2011). **Quorum** — łac. „of whom" = minimalna liczba głosów (z prawa rzymskiego).

### Jak zapamiętać

- **Linearizable = „natychmiast, atomowo, jak 1 kopia"**
- **Eventual = „kiedyś się zsynchronizuje" (ale kiedy?)**
- **CAP = „Partition → wybierz C albo A"**
- **Quorum: W+R > N** gwarantuje odczyt najnowszej wartości

\newpage

## PYTANIE 23: Segmentacja obrazu

**Problem, strategie klasyczne i sieci neuronowe.**

---

### Tło pojęciowe — słowniczek

**Obraz cyfrowy (digital image)** — macierz pikseli. Obraz 1920×1080 = ~2 mln pikseli. Każdy piksel ma wartość (grayscale: 0-255) lub kanały RGB (3 × 0-255). Segmentacja operuje na tej macierzy.

**Piksel (pixel)** — najmniejsza jednostka obrazu. „Picture element." Segmentacja = przypisanie etykiety KAŻDEMU pikselowi.

**Segmentacja obrazu (image segmentation)** — podział obrazu na regiony, gdzie każdy piksel dostaje etykietę klasy (np. „samochód", „droga", „niebo"). Różni się od klasyfikacji (cały obraz → 1 etykieta) i detekcji (bounding box + etykieta).

---

**Typy segmentacji:**

**Semantic segmentation** — każdy piksel → klasa, ale NIE rozróżnia instancji. Wszystkie samochody = jedna klasa „samochód".

    [samochód][samochód][droga][droga][pieszo][niebo]
    Dwa samochody = ta sama etykieta "samochód"

**Instance segmentation** — rozróżnia instancje tego samego obiektu. Samochód#1 i Samochód#2 mają różne etykiety.

**Panoptic segmentation** — łączy semantic + instance. Obiekty „things" (samochody, ludzie) mają instancje; „stuff" (niebo, droga) — tylko klasy.

---

**Thresholding (progowanie)** — najprostsza metoda: piksel > próg → klasa 1, inaczej → klasa 0. Otsu: automatyczny dobór progu minimalizujący wariancję wewnątrzklasową. Działa tylko dla 2 klas i prostych scen.

    Obraz: [50][200][180][30][220][190]
    Próg=128: [ 0 ][ 1 ][ 1 ][ 0][ 1 ][ 1 ]

**Region Growing (rozrastanie regionu)** — zacznij od punktu „ziarna" (seed), dodawaj sąsiednie piksele o podobnej wartości. Wrażliwa na wybór ziarna; tendencja do over-segmentation.

**Watershed (metoda zlewiska)** — traktuje obraz jak mapę topograficzną (jasność = wysokość). „Zalewaj" od minimów; granice regionów to „granie". Over-segmentation → wymaga markers (pre-processing).

**Mean Shift** — iteracyjne przesuwanie jądra do maksimum gęstości w przestrzeni cech. Grupuje piksele zbiegające do tego samego maksimum. Wolny, O(n²).

**Normalized Cuts** — modeluje obraz jako graf (piksele = węzły, podobieństwo = wagi krawędzi). Minimalizuje cut (rozdzielenie) znormalizowany do wielkości regionów. O(n³) — kosztowny.

---

**Sieć neuronowa (neural network)** — model uczenia maszynowego złożony z warstw neuronów. W segmentacji: sieci konwolucyjne (CNN) uczą się rozpoznawać cechy obrazu automatycznie.

**CNN (Convolutional Neural Network)** — sieć ze splotowymi warstwami (convolution): filtr przesuwany po obrazie wyodrębnia cechy (krawędzie, tekstury, kształty). Hierarchia: niskie warstwy → krawędzie, wysokie → obiekty.

**Encoder-Decoder** — architektura: encoder zmniejsza rozdzielczość (downsampling), wyodrębnia cechy. Decoder zwiększa rozdzielczość (upsampling), odtwarzając przestrzenną mapę segmentacji. Typowa struktura dla sieci segmentacyjnych.

    Encoder:  [224×224] → [112] → [56] → [28] → [14]  (cechy)
    Decoder:  [14] → [28] → [56] → [112] → [224×224]  (mapa segm.)

**Skip connections** — połączenia „na skróty" łączące warstwy encodera z decodera. Przenoszą drobne detale przestrzenne, które encoder utracił. Kluczowe w U-Net i FCN.

**FCN (Fully Convolutional Network, 2015)** — pierwsza sieć w pełni konwolucyjna do segmentacji. Zastępuje warstwy fully-connected konwolucjami → wejście dowolnego rozmiaru. Decoder: upsampling + skip connections.

**U-Net (2015)** — encoder-decoder w kształcie „U" ze skip connections (concatenation). Świetna przy małych zbiorach danych (data augmentation). Dominuje w segmentacji medycznej.

    Encoder ──skip──→ Decoder
      ↓     ──skip──→   ↑
      ↓     ──skip──→   ↑
    bottleneck

**DeepLab v3+** — Google. Kluczowe: **atrous (dilated) convolutions** — konwolucje z „dziurami" (fr. à trous = z dziurami). Większe receptive field bez dodatkowych parametrów. **ASPP (Atrous Spatial Pyramid Pooling)** — wieloskalowe cechy równolegle.

    Zwykła konwolucja 3×3:   [x][x][x]
    Dilated (rate=2):        [x][ ][x][ ][x]   ← większy zasięg

**Transformer-based (SegFormer, Mask2Former)** — najnowsze podejście. Transformery (self-attention) zastępują CNN. Self-attention widzi globalne zależności (CNN widzi tylko lokalne). SOTA na benchmarkach.

---

**mIoU (mean Intersection over Union)** — standardowa metryka segmentacji. Dla każdej klasy: IoU = (piksele poprawne ∩ ground truth) / (piksele poprawne ∪ ground truth). Potem średnia z klas.

    Klasa "samochód": predykcja=100 pikseli, GT=120, wspólne=80
    IoU = 80 / (100+120-80) = 80/140 = 0.571 = 57.1%

**Dice Loss** — funkcja kosztu powiązana z IoU: 2·|A∩B| / (|A|+|B|). Popularna w segmentacji medycznej (dobrze radzi sobie z class imbalance).

**Focal Loss** — modyfikacja cross-entropy redukująca wpływ łatwych przykładów, skupiająca uczenie na trudnych. Kluczowa przy class imbalance (np. 99% tła, 1% obiekt).

**Receptive field** — ile wejścia „widzi" jeden neuron. Większe receptive field = kontekst globalny. Atrous convolutions zwiększają receptive field bez zwiększania parametrów.

---

### Definicja: Przypisać każdemu pikselowi etykietę klasy/regionu.

Typy: **Semantic** (klasa per piksel), **Instance** (rozróżnia instancje), **Panoptic** (unified)

### Metody klasyczne

| Metoda          | Idea                                      | Wada                  |
|-----------------|-------------------------------------------|-----------------------|
| Thresholding    | Próg intensywności (Otsu = automat.)      | Tylko 2 klasy         |
| Region Growing  | Rozszerzaj od seeda wg podobieństwa       | Over-segmentation     |
| Watershed       | „Zalewanie" topografii obrazu             | Over-segmentation     |
| Mean Shift      | Przesuń do max gęstości, grupuj zbieżne  | Wolny                 |
| Normalized Cuts | Graf: min-cut z normalizacją              | O(n³)                 |

### Metody deep learning

**FCN (2015):** Pierwsza sieć fully-convolutional; encoder → upsampling; skip connections.
**U-Net (2015):** Encoder-decoder w kształcie U; skip connections (concat); popularne w medycynie.
**DeepLab v3+ :** Atrous/dilated convolutions (większe receptive field bez parametrów); ASPP (multi-scale).
**SegFormer, Mask2Former:** Transformer-based; SOTA.

### Metryki: **mIoU** (mean Intersection over Union) — standard; Dice, Pixel Accuracy.
### Loss: Cross-Entropy, Dice Loss, Focal Loss (class imbalance).

### Etymologia

**Segmentacja** — łac. „segmentum" = odcięty kawałek; podział obrazu na regiony. **Otsu** — Nobuyuki Otsu (1979); automatyczny dobór progu. **Watershed** — metafora: woda spływająca z grani do dolin (z geografii). **U-Net** — Ronneberger et al. (Freiburg, 2015); „U" od kształtu architektury. **FCN** — Fully Convolutional Network (Long, Shelhamer, Darrell, 2015). **DeepLab** — Google (2015–2018); „Atrous" z fr. „à trous" = „z dziurami" (dilated convolutions). **mIoU** — mean Intersection over Union.

### Jak zapamiętać

- **U-Net = „U-shape + skip connections"** — encoder-decoder
- **DeepLab = „Atrous (dilated) convolutions + ASPP"**
- **mIoU = Intersection / Union, uśrednione per klasa**

\newpage

## PYTANIE 24: Detekcja obiektów

**Problem, metody klasyczne, deep learning. Jak zbudować detektor z klasyfikatora?**

---

### Tło pojęciowe — słowniczek

**Detekcja obiektów (object detection)** — zadanie widzenia komputerowego: zlokalizuj obiekty na obrazie (bounding box) i przypisz im klasy (samochód, pieszo, kot...). Wynik: lista (klasa, prostokąt, pewność). Trudniejsze niż klasyfikacja (→ cały obraz, 1 label), ale łatwiejsze niż segmentacja (→ per piksel).

    Klasyfikacja:  "To zdjęcie zawiera kota"
    Detekcja:      "Kot w prostokącie (50,30)-(200,180), pewność 95%"
    Segmentacja:   Maska pikseli kota

**Bounding box (prostokąt ograniczający, bbox)** — prostokąt opisujący położenie obiektu. Zwykle: (x_min, y_min, x_max, y_max) lub (x_center, y_center, width, height). Przybliżenie — obiekty rzadko są prostokątne.

**Confidence (pewność)** — wynik 0-1 mówiący jak pewny jest detektor, że wykrył obiekt danej klasy. Zwykle próg np. 0.5: detiekcje poniżej odrzucane.

---

**Klasyfikator (classifier)** — model przypisujący etykietę do wejścia. Np. CNN trenowany na ImageNet: obraz → „kot" (+ prawdopodobieństwo). SAM nie lokalizuje — mówi tylko co jest na obrazie. Pytanie brzmi: jak z takiego modelu zbudować detektor?

**Sliding window (okno przesuwane)** — najprostsza metoda budowy detektora z klasyfikatora: wytnij prostokątny fragment obrazu (wiele rozmiarów, wiele pozycji), każdy fragment sklasyfikuj. Jeśli „pozytywny" → detekcja. Ekstremalnie wolne: tysiące fragmentów × klasyfikacja per fragment.

    [okno 64×64] przesuwa się po obrazie 640×480:
    (640-64)×(480-64) ≈ ~240 000 pozycji × wiele skal = MILIONY klasyfikacji!

---

**HOG (Histogram of Oriented Gradients)** — klasyczny deskryptor cech: oblicza histogramy kierunków gradientów (krawędzi) w komórkach obrazu. Dobrze opisuje kształt obiektów (sylwetki ludzi). Dalal & Triggs (2005, detekcja pieszych).

**SVM (Support Vector Machine)** — klasyczny klasyfikator: znajduje hiperpłaszczyznę maksymalnie separującą klasy. HOG+SVM = klasyczny pipeline detekcji pieszych.

**Viola-Jones (2001)** — przełomowy detektor twarzy real-time. Kluczowe innowacje:
- **Haar features** — proste cechy prostokątne (jasne/ciemne regiony)
- **Integral Image** — obliczenie dowolnej sumy prostokąta w O(1)!
- **AdaBoost cascade** — kaskada klasyfikatorów: szybkie odrzucenie 99% okien w pierwszych etapach, szczegółowa analiza tylko obiecujących

---

**R-CNN family (two-stage detectors)** — dwuetapowe: najpierw generuj propozycje regionów, potem klasyfikuj każdy region.

**R-CNN (2014)** — Selective Search → ~2000 regionów → CNN per region → SVM. 50 sekund/obraz! Wolne, bo CNN odpalane 2000 razy.

**Fast R-CNN** — CNN raz na całym obrazie, ROI Pooling wycinająca cechy regionów. ~2 sekundy/obraz.

**Faster R-CNN** — zastępuje Selective Search siecią RPN (Region Proposal Network). RPN generuje propozycje w sieci, nie oddzielnym algorytmem. ~5 fps. Najpopularniejszy two-stage detektor.

    Faster R-CNN:
    Obraz → CNN backbone → Feature Map → RPN (proposals) → ROI Pool → Classification + BBox regression

---

**One-stage detectors** — klasyfikacja i lokalizacja w jednym przejściu (bez osobnego etapu propozycji). Szybsze, ale historycznie mniej precyzyjne.

**YOLO (You Only Look Once, 2016)** — dzieli obraz na siatkę S×S. Każda komórka predykuje B bounding boxów + C klas. Jedno przejście przez sieć → wynik. 45-155 fps! Rewolucja w real-time detection.

    Obraz [416×416] → siatka 13×13 → każda komórka: 5 bbox + 80 klas
    Jedno forward pass → wszystkie detekcje na raz

**SSD (Single Shot MultiBox Detector, 2016)** — multi-scale feature maps + anchor boxes. Łączy szybkość YOLO z multi-scale (lepszy na małych obiektach).

**Anchor box** — predefiniowany prostokąt o określonym kształcie/proporcji. Sieć przewiduje przesunięcie (offset) od anchora. Wiele anchorów → pokrycie różnych kształtów obiektów.

**Anchor-free** — nowoczesne podejście (FCOS, YOLOv8): bezpośrednia predykcja środka i wymiarów, bez predefiniowanych anchorów. Prostsza architektura.

---

**NMS (Non-Maximum Suppression)** — post-processing: detektor generuje wiele nakładających się bbox dla tego samego obiektu. NMS: weź najlepszą (max confidence), usuń wszystkie mocno nakładające się (IoU > prog), powtórz.

    Detections: [bbox1, 0.95], [bbox2, 0.90], [bbox3, 0.85]  (nakładające się)
    NMS: zachowaj bbox1 (0.95), usuń bbox2 i bbox3 (IoU > 0.5 z bbox1)

**IoU (Intersection over Union)** — miara nakładania dwóch bbox: pole przecięcia / pole sumy. IoU=1 → identyczne; IoU=0 → brak nakładania. Próg NMS typowo 0.5.

**Backbone** — sieć bazowa (np. ResNet, VGG) wyciągająca cechy z obrazu. Detection head (głowa detekcyjna) jest dodawana „na wierzch" backbone i predykuje bbox + klasy. Fine-tuning backbone na detekcję = transfer learning.

---

**Jak zbudować detektor z klasyfikatora? Trzy podejścia:**
1. **Sliding window** — wytnij, sklasyfikuj, NMS. Bardzo wolne.
2. **Region proposals + klasyfikator** — Selective Search generuje ~2000 regionów, sklasyfikuj każdy + NMS. Szybsze.
3. **Fine-tune backbone** — weź pretrained classifier (np. ResNet z ImageNet), dodaj detection head (bbox regression + cls), dotrenuj na danych detekcyjnych. **Najlepsza jakość.**

**DETR (DEtection TRansformer, 2020)** — Facebook AI. Transformer zamiast CNN, bezpośrednia predykcja zestawu obiektów (set prediction), bez NMS. Uproszczona architektura.

---

### Definicja: Lokalizacja (bounding box) + klasyfikacja obiektów. Wynik: (class, bbox, confidence).

### Metody klasyczne

**Sliding Window + HOG/SVM:** Przesuwaj okno, wyekstrahuj cechy HOG, klasyfikuj SVM. Wolne!
**Viola-Jones (2001):** Haar features + Integral Image + AdaBoost cascade. Face detection real-time.

### Deep Learning

**Two-stage (R-CNN family):**
- R-CNN: Selective Search → 2000 regionów → CNN per region → SVM. 50 sec/image.
- Fast R-CNN: CNN raz, ROI Pooling. ~2 sec.
- **Faster R-CNN:** RPN (Region Proposal Network) zamiast Selective Search. ~5 fps.

**One-stage:**
- **YOLO:** Grid S×S, każda cell predykuje B bbox + C klas. 45-155 fps! Gorszy dla małych obiektów.
- **SSD:** Multi-scale feature maps + anchors. Łączy szybkość YOLO z multi-scale.

**Nowoczesne:** YOLOv8 (anchor-free), DETR (transformer, no NMS), RT-DETR.

### Jak zbudować detektor z klasyfikatora?

1. **Sliding Window:** crop → classify → NMS. Bardzo wolne.
2. **Region Proposals + Classifier:** Selective Search → crop → classify → NMS. Szybsze.
3. **Fine-tune na detekcję:** Pretrained classifier jako backbone + detection head (bbox regression + cls). **Najlepsza jakość!**

### NMS (Non-Maximum Suppression): Sortuj po confidence; weź najlepszą; usuń overlapping (IoU > threshold); powtórz.

### Etymologia

**YOLO** — You Only Look Once (Joseph Redmon et al., 2016). **R-CNN** — Region-based CNN (Ross Girshick, 2014). **HOG** — Histogram of Oriented Gradients (Dalal & Triggs, 2005). **SVM** — Support Vector Machine (Vapnik, 1995). **Viola-Jones** — Paul Viola + Michael Jones (2001). **DETR** — DEtection TRansformer (Facebook AI, 2020). **SSD** — Single Shot MultiBox Detector (Liu et al., 2016). **NMS** — Non-Maximum Suppression; tłumienie nie-maksymalnych detekcji.

### Jak zapamiętać

- **YOLO = „You Only Look Once"** — jednoetapowy, szybki
- **Faster R-CNN = CNN + RPN + ROI Pool** — dwuetapowy, dokładny
- **Detektor z klasyfikatora:** sliding window (wolno) → proposals (lepiej) → fine-tune backbone (najlepiej)

\newpage

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

### Etymologia

**Gene Amdahl** (IBM, 1967, „Validity of the single processor approach..."); współtwórca IBM System/360. **John Gustafson** (Sandia Labs, 1988, „Reevaluating Amdahl's Law"); weak scaling vs strong scaling. **Speedup (przyspieszenie)** — stosunek czasu sekwencyjnego do równoległego. **Efektywność** — ile z dodanych procesorów jest naprawdę wykorzystane. **Lock-free** — struktury danych bez blokad (CAS — Compare-And-Swap).

### Jak zapamiętać

- **S = 1/((1-p) + p/n)** — zapamiętaj wzór!
- **„10% seq = max 10x"** — sekwencyjna część limituje WSZYSTKO
- **Gustafson = „zwiększ problem, nie procesory"** — weak scaling
- **„FLOP" = False sharing, Load imbalance, Overhead, Poor locality**

\newpage

## PYTANIE 26: Komunikacja sync/async, blokująca/nieblokująca

**Definicje. Jak uniknąć zakleszczenia w symetrycznych procesach (Jacobi)?**

---

### Tło pojęciowe — słowniczek

**Komunikacja międzyprocesowa w obliczeniach równoległych** — procesy na różnych procesorach/maszynach muszą wymieniać dane. Kluczowe pytania: czy nadawca czeka na odbiorcę? Czy funkcja blokuje wątek? Te dwa aspekty (synchroniczność i blokowanie) to osobne, ortogonalne koncepcje.

---

**Komunikacja synchroniczna (synchronous)** — nadawca czeka, aż odbiorca faktycznie odbierze wiadomość. Obie strony muszą być „zsynchronizowane" w czasie — jak rozmowa telefoniczna (mówisz, słuchacz MUSI słuchać w tym momencie).

    Nadawca: Send(data) ──────────→ Odbiorca: Recv()
                  ↑                        ↑
             czeka tu                 czeka tu
             aż odbiorca              aż nadawca
             odbierze                 wyśle

**Komunikacja asynchroniczna (asynchronous)** — nadawca wysyła wiadomość do bufora i kontynuuje pracę, nie czekając na odbiorcę. Jak SMS — wysyłasz i robisz swoje, odbiorca przeczyta kiedy chce.

    Nadawca: Send(data) → [BUFOR] → kontynuuje pracę
                                    Odbiorca: Recv() kiedy gotowy

---

**Funkcja blokująca (blocking)** — wywołanie funkcji nie wraca, dopóki operacja nie jest zakończona (lub wystarczająco zaawansowana). Wątek jest „zamrożony" w oczekiwaniu.

    MPI_Send(data, dest) ← program "stoi" tutaj aż bufor gotowy
    printf("gotowe");     ← wykona się DOPIERO po zakończeniu Send

**Funkcja nieblokująca (non-blocking)** — wywołanie wraca natychmiast, operacja odbywa się w tle. Programista sprawdza status później (wait/test). Wątek może robić inne rzeczy w międzyczasie.

    MPI_Isend(data, dest, &request) ← wraca natychmiast
    // ... rób inne obliczenia ...
    MPI_Wait(&request)              ← czekaj na zakończenie

**Kluczowe: synchroniczność ≠ blokowanie!**

    Cecha              Synchroniczna          Asynchroniczna
    ──────────────────────────────────────────────────────────
    Nadawca czeka na   odbiorcę               bufor
    Wymaga matchingu   Tak (rendezvous)       Nie
    Bufor              Nie potrzebny          Potrzebny

    Cecha              Blokująca              Nieblokująca
    ──────────────────────────────────────────────────────────
    Funkcja wraca      po zakończeniu         natychmiast
    Wątek              zamrożony              może pracować
    Sprawdzenie        automatyczne           wait()/test()

---

**MPI (Message Passing Interface)** — standard komunikacji w obliczeniach równoległych (HPC). Najbardziej popularny model programowania na klastrach. Procesy komunikują się przez przesyłanie wiadomości (send/recv). Forum MPI zdefiniowało kilka wariantów Send:

- **MPI_Send** — blokujące, synchroniczność zależna od implementacji (może buforować lub czekać na recv)
- **MPI_Ssend** — blokujące, synchroniczne (czeka aż odbiorca dopasuje recv)
- **MPI_Bsend** — blokujące, asynchroniczne (kopiuje do bufora użytkownika i wraca)
- **MPI_Isend** — nieblokujące (I = Immediate), wraca natychmiast
- **MPI_Recv** — blokujące odbieranie
- **MPI_Irecv** — nieblokujące odbieranie

---

**Zakleszczenie (deadlock) w komunikacji** — gdy oba procesy wywołują blokujące Send przed Recv, żaden nie może odebrać (bo czeka na odbiorcę):

    Proc 0: Send(to=1); Recv(from=1);   ← czeka na recv z proc 1
    Proc 1: Send(to=0); Recv(from=0);   ← czeka na recv z proc 0
    → Oba czekają, nikt nie odbiera → DEADLOCK!

**Metoda Jacobiego** — iteracyjna metoda rozwiązywania układów równań liniowych. W wersji równoległej: każdy proces oblicza swoją część i wymienia wartości graniczne z sąsiadami. Symetryczny kod (wszyscy robią to samo) → podatny na deadlock Send-Send.

**Rozwiązania deadlocka w symetrycznym kodzie:**
1. **Asymetria kolejności** — Proc 0: Send→Recv; Proc 1: Recv→Send. Działa, ale asymetrycne.
2. **Nieblokujące** — Irecv + Isend + Waitall. Oba procesy inicjują odbiór ZANIM wyślą.
3. **MPI_Sendrecv** — jedna funkcja wykonująca Send i Recv atomowo. Bezpieczna, symetryczna. Rekomendowana.
4. **Bsend** — buforowane wysyłanie: kopiuje do bufora i wraca. Recv nie musi być gotowy.

    // Rozwiązanie 2 (nieblokujące):
    MPI_Irecv(from=neighbor, &req_r);   // inicjuj odbiór
    MPI_Isend(to=neighbor, &req_s);     // inicjuj wysyłanie
    MPI_Waitall(2, [req_r, req_s]);     // czekaj na oba

    // Rozwiązanie 3 (Sendrecv):
    MPI_Sendrecv(send_buf, dest, recv_buf, source);  // jedna funkcja, 0 deadlock

---

### Definicje

**Synchroniczna:** Nadawca czeka aż odbiorca odbierze (oba zsynchronizowane).
**Asynchroniczna:** Nadawca wysyła do bufora i kontynuuje (nie czeka na odbiorcę).

**Blokująca:** Funkcja nie wraca dopóki operacja nie skończona.
**Nieblokująca:** Funkcja wraca natychmiast; operacja w tle; sprawdzaj wait()/test().

### MPI

| Funkcja    | Blok? | Sync?     |
|------------|-------|-----------|
| MPI_Send   | Blok  | Zależy    |
| MPI_Ssend  | Blok  | Sync      |
| MPI_Bsend  | Blok  | Async     |
| MPI_Isend  | Nie   | Async     |
| MPI_Recv   | Blok  | -         |
| MPI_Irecv  | Nie   | -         |

### Problem: Zakleszczenie w symetrycznym kodzie

    // DEADLOCK!
    Proc 0: Send(to=1); Recv(from=1);
    Proc 1: Send(to=0); Recv(from=0);
    // Oba czekają aż partner odbierze, nikt nie robi Recv!

### Rozwiązania

1. **Zmiana kolejności:** Proc 0: Send→Recv; Proc 1: Recv→Send (asymetria)
2. **Nieblokujące:** Irecv + Isend + Wait (oba procesy symetrycznie)
3. **MPI_Sendrecv** — jedna funkcja, automatycznie bezpieczna
4. **Bsend** — buforowane wysyłanie (kopiuje do bufora i wraca)

### Etymologia

**MPI** — Message Passing Interface (MPI Forum, 1994); standard komunikacji w obliczeniach równoległych. **Jacobi** — Carl Gustav Jacob Jacobi (1804–1851, mat. niemiecki); metoda iteracyjna rozwiązywania układów równań. **Synchroniczna** — grec. „syn" (razem) + „chronos" (czas) = w tym samym czasie. **Asynchroniczna** — grec. „a-" (nie) + synchronous = nie w tym samym czasie. **Blokująca** — funkcja „blokuje" wątek aż operacja się skończy.

### Jak zapamiętać

- **Deadlock = Send-Send** — oba czekają, nikt nie odbiera
- **Sendrecv = „safe exchange"** — jedna funkcja, zero deadlocków
- **I = Immediate = Non-blocking** (MPI_Isend, MPI_Irecv)
- **S = Synchronous** (MPI_Ssend — czeka na recv)

\newpage

## PYTANIE 31: Interaktywne wspomaganie decyzji w warunkach ryzyka

**Przedstawić metody interaktywne.**

---

### Tło pojęciowe — słowniczek

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

\newpage

## PYTANIE 32: Dominacja stochastyczna

**FSD i SSD. Jak mogą być użyte w modelach wyboru?**

---

### Tło pojęciowe — słowniczek

**Dominacja stochastyczna (stochastic dominance)** — metoda porównywania rozkładów prawdopodobieństwa (np. dwóch inwestycji) BEZ konieczności znajomości dokładnej funkcji użyteczności decydenta. Jeśli rozkład A „dominuje" B, to cała klasa racjonalnych decydentów wybierze A.

    Idea kluczowa:
    Nie wiem jaka DOKŁADNIE jest Twoja U(x),
    ale wiem, że preferujesz „więcej" (FSD)
    lub dodatkowo „mniej ryzyka" (SSD).
    To wystarczy, żeby A > B.

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
