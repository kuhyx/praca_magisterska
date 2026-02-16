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

**Definicja formalna:** M = (Q, Σ, δ, q₀, F)

| Symbol | Nazwa | Znaczenie | Przykład |
|--------|-------|-----------|----------|
| **Q** | Zbiór stanów (States) | Skończony zbiór wszystkich stanów automatu — „pozycji" w schemacie | Q = {q₀, q₁, q₂} — trzy stany |
| **Σ** | Alfabet wejściowy (Sigma) | Skończony zbiór symboli, które automat czyta | Σ = {a, b} — alfabet dwuliterowy |
| **δ** | Funkcja przejścia (Delta) | Reguła: „w stanie q, czytając symbol a, przejdź do stanu q'" — δ: Q × Σ → Q (DFA) | δ(q₀, a) = q₁ — z q₀ po 'a' idź do q₁ |
| **q₀** | Stan początkowy | Stan, w którym automat zaczyna pracę | q₀ — zawsze startujemy tu |
| **F** | Stany akceptujące (Final) | Podzbiór Q — jeśli automat skończy w stanie z F, słowo jest AKCEPTOWANE | F = {q₂} — tylko q₂ akceptuje |

**Pamięć:** brak — cała informacja to aktualny stan. **DFA ≡ NFA.**
Równoważne wyrażeniom regularnym (regex).
Przykłady: identyfikatory, podzielność. Nie: aⁿbⁿ, nawiasy, palindromy.

**Przykład krok po kroku — FA rozpoznaje język L = {słowa nad {a,b} kończące się na "ab"}:**

Automat DFA: Q = {q₀, q₁, q₂}, Σ = {a, b}, F = {q₂}

    Tabela przejść:
    ┌───────┬───────┬───────┐
    │ Stan  │  a    │  b    │
    ├───────┼───────┼───────┤
    │  q₀   │  q₁   │  q₀   │   (q₀ = „nie widziałem 'a' na końcu")
    │  q₁   │  q₁   │  q₂   │   (q₁ = „ostatni symbol to 'a'")
    │  q₂*  │  q₁   │  q₀   │   (q₂ = „ostatnie dwa to 'ab'" ← AKCEPTUJ)
    └───────┴───────┴───────┘

    Wejście: w = "baab"

    Krok 1: stan = q₀, czytam 'b' → δ(q₀, b) = q₀     stan: q₀
    Krok 2: stan = q₀, czytam 'a' → δ(q₀, a) = q₁     stan: q₁
    Krok 3: stan = q₁, czytam 'a' → δ(q₁, a) = q₁     stan: q₁
    Krok 4: stan = q₁, czytam 'b' → δ(q₁, b) = q₂     stan: q₂ ✓

    Końcowy stan q₂ ∈ F → słowo "baab" AKCEPTOWANE ✓

    Wejście: w = "ba"

    Krok 1: stan = q₀, czytam 'b' → δ(q₀, b) = q₀     stan: q₀
    Krok 2: stan = q₀, czytam 'a' → δ(q₀, a) = q₁     stan: q₁

    Końcowy stan q₁ ∉ F → słowo "ba" ODRZUCONE ✗

![Diagram FA rozpoznającego język kończący się na "ab"](img/fa_recognition_example.png)

### PDA — Typ 2: Języki bezkontekstowe

**Definicja formalna:** M = (Q, Σ, Γ, δ, q₀, Z₀, F)

| Symbol | Nazwa | Znaczenie | Przykład |
|--------|-------|-----------|----------|
| **Q** | Zbiór stanów | Jak w FA — skończony zbiór stanów | Q = {q₀, q₁, q₂} |
| **Σ** | Alfabet wejściowy | Symbole czytane z wejścia | Σ = {a, b} |
| **Γ** | Alfabet stosowy (Gamma) | Symbole, które mogą być na stosie — INNE niż alfabet wejściowy! | Γ = {Z₀, A} — Z₀ = dno stosu, A = znacznik |
| **δ** | Funkcja przejścia | Teraz zależy od TRZECH rzeczy: stan + symbol wejściowy + szczyt stosu → nowy stan + operacja na stosie | δ(q₀, a, Z₀) = (q₀, AZ₀) — „push A" |
| **q₀** | Stan początkowy | Jak w FA | q₀ |
| **Z₀** | Symbol dna stosu | Początkowy symbol na stosie — pozwala wykryć, że stos jest „pusty" | Z₀ — stos zaczyna z jednym Z₀ |
| **F** | Stany akceptujące | Jak w FA (alternatywnie: akceptacja przez pusty stos) | F = {q₂} |

**Pamięć:** stos LIFO — ostatni włożony, pierwszy wyjęty. **DPDA ⊂ NPDA!**
Przykłady: aⁿbⁿ, nawiasy, wwᴿ. Nie: aⁿbⁿcⁿ, ww.

**Przykład krok po kroku — PDA rozpoznaje język L = {aⁿbⁿ | n ≥ 1}:**

Automat PDA: Q = {q₀, q₁, q₂}, Σ = {a, b}, Γ = {Z₀, A}, F = {q₂}

    Reguły przejścia:
    δ(q₀, a, Z₀) = (q₀, AZ₀)    ← czytam 'a', stos pusty → push A
    δ(q₀, a, A)  = (q₀, AA)      ← czytam 'a', na stosie A → push jeszcze A
    δ(q₀, b, A)  = (q₁, ε)       ← czytam 'b', na stosie A → pop A, przejdź do q₁
    δ(q₁, b, A)  = (q₁, ε)       ← czytam 'b', na stosie A → pop A
    δ(q₁, ε, Z₀) = (q₂, Z₀)     ← brak wejścia, stos = Z₀ → akceptuj!

    Wejście: w = "aabb" (a²b², n=2)

    Krok 1: stan=q₀, czytam 'a', stos=[Z₀]
            δ(q₀, a, Z₀) = (q₀, AZ₀) → push A
            stan=q₀, stos=[A, Z₀]

    Krok 2: stan=q₀, czytam 'a', stos=[A, Z₀]
            δ(q₀, a, A) = (q₀, AA) → push A
            stan=q₀, stos=[A, A, Z₀]

    Krok 3: stan=q₀, czytam 'b', stos=[A, A, Z₀]
            δ(q₀, b, A) = (q₁, ε) → pop A
            stan=q₁, stos=[A, Z₀]

    Krok 4: stan=q₁, czytam 'b', stos=[A, Z₀]
            δ(q₁, b, A) = (q₁, ε) → pop A
            stan=q₁, stos=[Z₀]

    Krok 5: stan=q₁, brak wejścia, stos=[Z₀]
            δ(q₁, ε, Z₀) = (q₂, Z₀) → akceptuj!
            stan=q₂ ∈ F → "aabb" AKCEPTOWANE ✓

    Intuicja: Push A za każde 'a', pop A za każde 'b'.
    Jeśli stos pusty po przeczytaniu → równo a i b → akceptuj!

![Diagram PDA rozpoznającego język aⁿbⁿ](img/pda_recognition_example.png)

### LBA — Typ 1: Języki kontekstowe

**Definicja formalna:** M = (Q, Σ, Γ, δ, q₀, q_acc, q_rej) — jak TM, ale z ograniczeniem taśmy

| Symbol | Nazwa | Znaczenie | Przykład |
|--------|-------|-----------|----------|
| **Q** | Zbiór stanów | Skończony zbiór stanów — może być większy niż w FA/PDA | Q = {q₀, q₁, q₂, q₃, q₄, q_acc, q_rej} |
| **Σ** | Alfabet wejściowy | Symbole na taśmie na początku (BEZ markera pustego) | Σ = {a, b, c} |
| **Γ** | Alfabet taśmowy (Gamma) | Wszystkie symbole dozwolone na taśmie, Σ ⊂ Γ, zawiera marker pusty ⊔ | Γ = {a, b, c, X, Y, Z, ⊔} — X,Y,Z = zaznaczone |
| **δ** | Funkcja przejścia | δ(stan, symbol_na_taśmie) = (nowy_stan, symbol_do_zapisania, kierunek_głowicy) | δ(q₀, a) = (q₁, X, R) — zaznacz 'a' jako X, idź w prawo |
| **q₀** | Stan początkowy | Głowica na pierwszym symbolu taśmy | q₀ |
| **q_acc** | Stan akceptujący | Akceptacja — automat się ZATRZYMUJE | q_acc |
| **q_rej** | Stan odrzucający | Odrzucenie — automat się ZATRZYMUJE | q_rej |

**Ograniczenie LBA:** Głowica NIE może wyjść poza |w| komórek (długość wejścia). To jedyna różnica od TM!
**DLBA =? NLBA** — problem otwarty!
Przykłady: aⁿbⁿcⁿ, ww.

**Przykład krok po kroku — LBA rozpoznaje język L = {aⁿbⁿcⁿ | n ≥ 1}:**

Strategia: wielokrotnie przejdź taśmę, za każdym razem zaznacz jedno 'a', jedno 'b', jedno 'c'.

    Wejście: w = "aabbcc" (n=2), taśma = [a, a, b, b, c, c]

    === Runda 1: zaznacz po jednym z każdego ===
    Krok 1: stan=q₀, głowica→'a', zaznacz a→X, idź w prawo
            taśma = [X, a, b, b, c, c]  głowica na 'a'

    Krok 2: stan=q₁, przeskocz pozostałe 'a' (idź prawo)
            głowica na 'b'

    Krok 3: zaznacz b→Y, idź w prawo
            taśma = [X, a, Y, b, c, c]  głowica na 'b'

    Krok 4: stan=q₂, przeskocz pozostałe 'b' (idź prawo)
            głowica na 'c'

    Krok 5: zaznacz c→Z, wróć na początek
            taśma = [X, a, Y, b, Z, c]

    === Runda 2: zaznacz kolejne ===
    Krok 6: od początku, znajdź pierwsze niezaznaczone 'a' → zaznacz X
            taśma = [X, X, Y, b, Z, c]

    Krok 7: znajdź pierwsze niezaznaczone 'b' → zaznacz Y
            taśma = [X, X, Y, Y, Z, c]

    Krok 8: znajdź pierwsze niezaznaczone 'c' → zaznacz Z
            taśma = [X, X, Y, Y, Z, Z]

    === Sprawdzenie: nie ma niezaznaczonych symboli → AKCEPTUJ ✓ ===

    Gdyby "aabcc" (2a, 1b, 2c): po zaznaczeniu a,b,c w rundzie 1
    w rundzie 2 zaznaczamy drugie 'a', ale NIE MA drugiego 'b' → ODRZUĆ ✗

![Diagram LBA rozpoznającego język aⁿbⁿcⁿ](img/lba_recognition_example.png)

### TM — Typ 0: Rekurencyjnie przeliczalne

**Definicja formalna:** M = (Q, Σ, Γ, δ, q₀, q_acc, q_rej)

| Symbol | Nazwa | Znaczenie | Przykład |
|--------|-------|-----------|----------|
| **Q** | Zbiór stanów | Skończony zbiór stanów — jak LBA | Q = {q₀, q₁, q₂, q₃, q_acc, q_rej} |
| **Σ** | Alfabet wejściowy | Symbole wejścia (nie zawiera ⊔) | Σ = {0, 1} |
| **Γ** | Alfabet taśmowy | Σ ⊂ Γ, zawiera marker pusty ⊔ (blank) | Γ = {0, 1, X, ⊔} |
| **δ** | Funkcja przejścia | Identyczna forma jak LBA: δ(q, a) = (q', b, L/R) | δ(q₀, 0) = (q₁, X, R) |
| **q₀** | Stan początkowy | Głowica na pierwszym symbolu | q₀ |
| **q_acc** | Stan akceptujący | Wejście do q_acc → słowo AKCEPTOWANE, stop | q_acc |
| **q_rej** | Stan odrzucający | Wejście do q_rej → słowo ODRZUCONE, stop | q_rej |

**Kluczowa różnica od LBA:** Taśma jest **nieskończona** w prawo — głowica może wyjść poza wejście i pisać na pustych komórkach. To daje NIEOGRANICZONĄ pamięć roboczą.

**Pamięć:** taśma ∞ R/W. **DTM ≡ NTM** (równoważne pod względem mocy).
Teza Churcha-Turinga: TM modeluje każde obliczenie. Nie: komplement problemu stopu.

**Przykład krok po kroku — TM rozpoznaje język L = {0ⁿ1ⁿ | n ≥ 1} (jak aⁿbⁿ, ale z 0 i 1):**

Strategia: zaznacz jedno '0' i jedno '1' w każdej rundzie, powtarzaj aż do wyczerpania.

    Wejście: w = "0011", taśma = [0, 0, 1, 1, ⊔, ⊔, ⊔, ...]
                                                    ↑ nieskończona!

    === Runda 1 ===
    Krok 1: stan=q₀, głowica→'0', zaznacz 0→X, idź w prawo
            taśma = [X, 0, 1, 1, ⊔, ...]  stan=q₁

    Krok 2: stan=q₁, przeskocz '0' w prawo, znajdź '1'
            głowica na pierwszym '1'

    Krok 3: zaznacz 1→Y, wróć na początek (idź w lewo do X)
            taśma = [X, 0, Y, 1, ⊔, ...]  stan=q₃

    === Runda 2 ===
    Krok 4: znajdź pierwsze niezaznaczone '0' → zaznacz X
            taśma = [X, X, Y, 1, ⊔, ...]

    Krok 5: znajdź pierwsze niezaznaczone '1' → zaznacz Y
            taśma = [X, X, Y, Y, ⊔, ...]

    === Sprawdzenie ===
    Krok 6: od początku szukam niezaznaczonych — nie ma → q_acc
            "0011" AKCEPTOWANE ✓

    TM może też WYJŚĆ poza wejście (czego LBA nie może):
    Np. "011" — po zaznaczeniu 0↔1, zostaje '1' bez pary → q_rej ✗

![Diagram TM rozpoznającego język 0ⁿ1ⁿ](img/tm_recognition_example.png)

### Porównanie definicji formalnych

| Element | FA | PDA | LBA | TM |
|---------|----|----|-----|-----|
| **Stany Q** | ✓ mało | ✓ mało | ✓ więcej | ✓ więcej |
| **Alfabet Σ** | ✓ | ✓ | ✓ | ✓ |
| **Alfabet stosu/taśmy Γ** | ✗ brak | ✓ stosowy | ✓ taśmowy | ✓ taśmowy |
| **Przejście δ** | q × Σ → q | q × (Σ∪ε) × Γ → q × Γ* | q × Γ → q × Γ × {L,R} | q × Γ → q × Γ × {L,R} |
| **Dodatkowa pamięć** | brak | stos (LIFO) | taśma ogr. do \|w\| | taśma ∞ |
| **Akceptacja** | stan ∈ F | stan ∈ F lub pusty stos | stan = q_acc | stan = q_acc |
| **Może się zapętlić?** | NIE (skończone) | TAK (ε-przejścia) | TAK | TAK (problem stopu!) |

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

