<!-- SKRYPT MÓWIONY — obrona magisterska. Drukuj: pandoc → PDF, A4, 10pt, marginesy 2cm. Każde pytanie = osobny moduł. -->
<!-- Konwencja: [TABLICA: ...] = narysuj/napisz na tablicy. [GEST: ...] = wskazanie/ruch. [PAUZA] = weź oddech. -->
<!-- Styl: mówiony polski, nie literacki. Krótkie zdania. Naturalny tok. -->

---

# SKRYPT MÓWIONY — Obrona Magisterska

---

\newpage

## PYTANIE 1 · Automaty i klasy języków (AISDI)

**Pytanie:** *Porównać „siłę wyrazu" automatu skończonego, automatu ze stosem oraz maszyny Turinga. Jakie klasy języków rozpoznaje każdy z nich?*

---

### Co mówię

Dobrze, tutaj chodzi o hierarchię Chomsky'ego, czyli o to, jak kolejne automaty mają coraz większą moc obliczeniową dzięki temu, że mają coraz lepszą pamięć.

[TABLICA: rysuj „schodki" albo kółka zagnieżdżone — od najmniejszego do największego]

Zaczynam od najsłabszego. **Automat skończony** — on nie ma żadnej pamięci poza swoim stanem. Może rozpoznawać języki regularne, czyli takie, które da się opisać wyrażeniem regularnym. Przykład — sprawdzanie czy identyfikator w kodzie jest poprawny. Ale nie poradzi sobie z czymś, co wymaga zliczania — na przykład z językiem a^n b^n, bo nie ma jak zapamiętać ile było tych „a".

[TABLICA: napisz FA → Regularne, pamięć: brak]

Następny krok — **automat ze stosem**. Tutaj dodajemy stos, i to wystarczy, żeby obsłużyć nawiasy, rekurencję w gramatykach. Rozpoznaje języki bezkontekstowe — to jest ten poziom, na którym działają parsery języków programowania. Poradzi sobie z a^n b^n, bo na stos odkłada „a" i zdejmuje przy „b". Ale nie da rady z a^n b^n c^n, bo stos zostaje zużyty po dwóch pierwszych grupach.

[TABLICA: dopisz PDA → Bezkontekstowe, pamięć: stos LIFO]

Na końcu — **maszyna Turinga**. Ma nieskończoną taśmę z odczytem i zapisem. Może się cofać, może pisać w dowolnym miejscu. Rozpoznaje języki rekurencyjnie przeliczalne, czyli — zgodnie z tezą Churcha-Turinga — wszystko to, co w ogóle da się obliczyć.

[TABLICA: dopisz TM → Rek. przeliczalne, pamięć: taśma ∞ R/W]

Więc mamy taką hierarchię inkluzji: regularne ⊂ bezkontekstowe ⊂ kontekstowe ⊂ rekurencyjnie przeliczalne. Każdy następny automat rozpoznaje ściśle więcej.

Warto wspomnieć, że jest jeszcze **LBA** — automat z ograniczoną taśmą — między PDA a TM. On rozpoznaje języki kontekstowe, takie jak a^n b^n c^n. Ale nie jest wprost wymieniony w pytaniu.

### Jeśli mam jeszcze czas / pytają dalej

Ciekawa różnica: dla automatów skończonych — determinizm i niedeterminizm dają tę samą moc. Każdy NFA da się przekształcić na DFA. Dla PDA — nie: niedeterministyczny PDA rozpoznaje więcej niż deterministyczny. A dla maszyn Turinga — znowu równoważne, pod względem mocy, choć nie szybkości.

### Spodziewane pytania dodatkowe

**„Podaj kontrprzykład — co łamie FA?"** → a^n b^n — trzeba liczyć, FA nie ma pamięci, nie da rady.

**„Czym się różni DFA od NFA?"** → NFA może być w wielu stanach naraz, ale każdy NFA da się zamienić na DFA — kosztem wykładniczej liczby stanów.

**„Co to jest teza Churcha-Turinga?"** → Że maszyna Turinga opisuje wszystko, co intuicyjnie rozumiemy jako „obliczanie". Nie jest to twierdzenie matematyczne — to teza filozoficzna.

---

\newpage

## PYTANIE 2 · Algorytmy najkrótszej ścieżki (AISDI)

**Pytanie:** *Omówić i porównać algorytmy: Dijkstry, Bellmana-Forda, A\*.*

---

### Co mówię

Trzy algorytmy, każdy rozwiązuje problem najkrótszej ścieżki, ale w innych warunkach i innym podejściem.

[TABLICA: narysuj prosty graf ważony — 5 wierzchołków, parę krawędzi z wagami]

**Dijkstra** — algorytm zachłanny. Startujemy z jednego źródła, trzymamy kolejkę priorytetową wierzchołków po aktualnej odległości i zawsze przetwarzamy ten o najmniejszej. Relaksujemy jego krawędzie. Kluczowy warunek — **wagi muszą być nieujemne**, bo raz przetworzony wierzchołek już nie jest odwiedzany ponownie. Złożoność z kopcem — O((V+E) log V).

**Bellman-Ford** — podejście z programowania dynamicznego. Robimy V−1 iteracji, w każdej relaksujemy wszystkie krawędzie. Dlaczego V−1? Bo najdłuższa ścieżka prosta ma V−1 krawędzi. Główna zaleta — **obsługuje ujemne wagi** i potrafi **wykryć cykl ujemny**: jeśli po V−1 iteracjach dalej da się poprawić jakąś odległość, to jest cykl. Złożoność — O(V·E), wolniejszy od Dijkstry.

**A\*** — to w zasadzie Dijkstra z heurystyką. Zamiast przetwarzać wierzchołek o najmniejszej odległości g(n), bierze ten o najmniejszym f(n) = g(n) + h(n), gdzie h to oszacowanie ile jeszcze zostało do celu. Jeśli heurystyka jest dopuszczalna — czyli nie przeszacowuje — to A\* jest optymalny. Typowe zastosowanie — nawigacja, gry.

[TABLICA: napisz krótką tabelkę]

| Algo | Podejście | Ujemne wagi | Złożoność |
|------|-----------|-----------|-----------|
| Dijkstra | Zachłanny | NIE | O((V+E)log V) |
| Bellman-Ford | DP | TAK | O(VE) |
| A* | Heuryst. | NIE | Zależy od h |

### Spodziewane pytania dodatkowe

**„Dlaczego Dijkstra nie działa z ujemnymi wagami?"** → Bo po przetworzeniu wierzchołka zakładamy, że mamy już najkrótszą ścieżkę do niego. Ujemna waga może później dać lepszą trasę — ale algorytm już tego nie sprawdzi.

**„Co to znaczy, że heurystyka jest dopuszczalna?"** → Że h(n) ≤ faktyczny koszt z n do celu. Nigdy nie przeszacowuje. Przykład — odległość po linii prostej na mapie.

**„Który jest najszybszy w praktyce?"** → A\* z dobrą heurystyką, bo eksploruje mniej wierzchołków. Dijkstra exploruje we wszystkich kierunkach, A\* kieruje się ku celowi.

---

\newpage

## PYTANIE 3 · Redundancja i normalizacja (BD2)

**Pytanie:** *Omówić zagadnienia redundancji i normalizacji w relacyjnej bazie danych.*

---

### Co mówię

Redundancja to powtarzanie tych samych danych w wielu miejscach. Problem nie jest sam fakt powtórzenia, tylko **anomalie**, jakie powoduje.

Są trzy rodzaje anomalii. **Wstawiania** — nie mogę dodać danych bez podania niepotrzebnych powiązań. **Usuwania** — kasuję rekord i tracę informację, która nie powinna zniknąć. **Modyfikacji** — zmieniam jedno pole, ale muszę to zrobić w dziesięciu miejscach, bo dane są powielone.

[TABLICA: przykład — tabela Student-Kurs-Wydział, gdzie NazwaWydziału się powtarza]

Rozwiązaniem jest **normalizacja** — rozbijamy tabelę na mniejsze, eliminując zależności, które powodują redundancję.

Postacie normalne idą tak: 1NF → 2NF → 3NF → BCNF → dalej.

Jest taka mnemotechnika: **„Klucz, cały klucz i tylko klucz — tak mi dopomóż Codd."**

- **1NF** — wartości atomowe, istnieje klucz. Czyli żadnych list w komórkach.
- **2NF** — każdy atrybut wtórny zależy od **całego** klucza, nie od jego części. To dotyczy kluczy złożonych.
- **3NF** — brak zależności przechodnich. Jeśli A → B → C, to C nie powinno być w tej samej tabeli co A.
- **BCNF** — dla każdej zależności funkcyjnej lewa strona musi być nadkluczem. Silniejsza niż 3NF.

W praktyce — 3NF albo BCNF to taki „standard" w systemach transakcyjnych. Dalsze postacie — 4NF, 5NF — dotyczą zależności wielowartościowych i łączeniowych, ale stosuje się je rzadko.

Jest też **denormalizacja** — świadome dodawanie redundancji dla wydajności, żeby uniknąć kosztownych JOIN-ów. Typowe w hurtowniach danych, OLAP.

### Spodziewane pytania dodatkowe

**„Podaj przykład naruszenia 2NF."** → Tabela (StudentID, KursID, NazwaKursu): NazwaKursu zależy tylko od KursID, nie od całego klucza złożonego.

**„Jaka jest różnica między 3NF a BCNF?"** → 3NF pozwala na zależności, gdzie lewa strona nie jest nadkluczem, jeśli prawa strona jest atrybutem pierwszym. BCNF tego nie akceptuje.

**„Kiedy denormalizować?"** → Gdy zapytania analityczne wymagają wielu JOIN-ów i opóźnienie jest nieakceptowalne. Obniżamy normalizację na rzecz wydajności odczytu.

---

\newpage

## PYTANIE 4 · Baza danych jako fundament systemów (BD2)

**Pytanie:** *Dlaczego baza danych stanowi dobry fundament do budowy wielu systemów informatycznych?*

---

### Co mówię

To pytanie jest trochę bardziej koncepcyjne. Chodzi o to, dlaczego baza danych jest tak dobrym fundamentem — w porównaniu z alternatywami typu pliki, pamięć operacyjna, własne rozwiązania.

Powodów jest kilka i pójdę po kolei.

Po pierwsze — **transakcyjność ACID**. Atomowość gwarantuje, że operacja się wykona w całości albo wcale. Spójność — że baza przechodzi ze spójnego stanu w spójny. Izolacja — równoległe operacje sobie nie przeszkadzają. Trwałość — raz zapisane dane przetrwają awarię. To jest fundament — bez tego każdy system musiałby sam implementować te gwarancje.

Po drugie — **niezależność danych**. Architektura ANSI/SPARC wyróżnia trzy poziomy: fizyczny, logiczny, zewnętrzny. Zmiana indeksów czy partycjonowania nie wpływa na logikę aplikacji. To pozwala na niezależną ewolucję systemu.

Po trzecie — **współbieżność**. Baza ma wbudowane mechanizmy — blokady, MVCC — żeby wielu użytkowników mogło pracować jednocześnie. Bez bazy — musielibyśmy to implementować sami.

Po czwarte — **integralność**. Klucze obce, CHECK-i, triggery — baza sama pilnuje reguł biznesowych na poziomie danych.

Po piąte — **optymalizator zapytań**. Piszę CO chcę, a baza sama decyduje JAK to zrealizować — wybiera indeksy, plany wykonania. To ogromna oszczędność pracy.

Jeszcze bezpieczeństwo — GRANT/REVOKE, role, szyfrowanie. Skalowalność — replikacja, sharding. I SQL jako standardowy interfejs — nie wymyślam protokołu od zera.

Podsumowując — baza danych daje zestaw rozwiązanych problemów, które każdy system potrzebuje. Zamiast budować od zera, korzystamy z dojrzałego narzędzia.

### Spodziewane pytania dodatkowe

**„Co to MVCC?"** → Multi-Version Concurrency Control. Zamiast blokować, baza trzyma wiele wersji wiersza. Czytający widzi starszą wersję, piszący tworzy nową. Nie blokują się nawzajem.

**„A kiedy baza NIE jest dobrym fundamentem?"** → Kiedy mamy dane niestrukturalne, wymagania ultra-niskiej latencji, albo dane w grafie — wtedy rozwiązania specjalizowane (timeseries DB, document stores, graph DB) mogą być lepsze.

---

\newpage

## PYTANIE 5 · Kategorie STL (PROI)

**Pytanie:** *Omówić główne kategorie elementów biblioteki STL.*

---

### Co mówię

STL ma cztery główne filary — i kluczowe jest to, jak one ze sobą współpracują.

[TABLICA: narysuj schemat]

    KONTENERY  ←→  ITERATORY  ←→  ALGORYTMY
                                    ↑
                                  FUNKTORY

**Kontenery** — przechowują dane. Mamy sekwencyjne — vector, list, deque. Asocjacyjne oparte na drzewach R-B — set, map — z O(log n). Nieuporządkowane oparte na hashach — unordered_set, unordered_map — z O(1) średnio. I adaptery — stack, queue, priority_queue — ograniczony interfejs.

**Iteratory** — to uogólnione wskaźniki. Są w hierarchii: od Input/Output, przez Forward, Bidirectional, po Random Access. Vector daje Random Access, list — Bidirectional, forward_list — Forward. Iterator mówi algorytmowi JAK przechodzić po kontenerze.

**Algorytmy** — sort, find, transform, copy, accumulate. Kluczowa cecha — **operują na iteratorach, nie na kontenerach**. Nie obchodzi ich, czy to vector, list czy deque.

**Funktory** — obiekty funkcyjne, które parametryzują algorytmy. Klasyczne: less, greater. W C++11 — lambdy.

I to jest ta genialna architektura STL — jest **ortogonalna**. Mam M kontenerów i N algorytmów — potrzebuję M+N komponentów, nie M×N. Bo kontenery i algorytmy komunikują się przez iteratory. Ten sam sort działa na vectorze i na deque — wystarczy że mają Random Access iterator.

[TABLICA: sort(v.begin(), v.end()) — ten sam algorytm, różne kontenery]

### Spodziewane pytania dodatkowe

**„Kiedy wybrać vector, a kiedy list?"** → Vector domyślnie — contiguous memory, cache-friendly, Random Access. List — gdy dużo wstawiania/usuwania w środku, bo to O(1) z iteratorem, ale cache-unfriendly. W praktyce — vector wygrywa prawie zawsze.

**„Co to jest ortogonalność w kontekście STL?"** → To, że kontener i algorytm nie muszą o sobie wiedzieć. Łączy je iterator — wspólny interfejs. Dodanie nowego kontenera nie wymaga zmian w algorytmach.

**„Czym się różni funktor od lambdy?"** → Funktor to klasa z operatorem(), lambda to skrócona składnia, która pod spodem generuje analogiczną klasę. W C++11+ — praktycznie to samo.

---

\newpage

## PYTANIE 6 · Reużywalność kodu w OOP (PROI)

**Pytanie:** *Omówić metody reużywalności kodu i struktur danych w obiektowych językach programowania.*

---

### Co mówię

Mamy kilka głównych mechanizmów, ale zacznę od dwóch najważniejszych — i od tego, jak się je porównuje.

**Dziedziczenie** — relacja „jest" (is-a). Klasa pochodna przejmuje interfejs i implementację bazowej. Pozwala na polimorfizm — virtual, override. Wada — silne wiązanie, krucha klasa bazowa, i diamond problem przy wielodziedziczeniu.

**Kompozycja** — relacja „zawiera" (has-a). Zamiast dziedziczyć, obiekt ma pole innego typu. Stack nie JEST wektorem — Stack ZAWIERA wektor. Luźniejsze wiązanie, lepsza enkapsulacja, łatwiejsze testowanie.

I tutaj zasada z GoF-a, którą trzeba znać: **„Favor composition over inheritance"**. Kompozycja jest preferowana. Dziedziczenie — tylko gdy mam rzeczywiście relację is-a i potrzebuję polimorfizmu.

**Programowanie generyczne** — szablony w C++, generics w Javie. Piszę kod raz, działa dla wielu typów. Przykład — cała STL jest oparta na templates. To jest reużywalność na poziomie algorytmów i struktur.

**Interfejsy i klasy abstrakcyjne** — kontrakt bez implementacji. W Javie `interface`, w C++ czysta klasa wirtualna. Pozwala na strategy pattern, dependency injection, testowanie przez mocki.

**Wzorce projektowe** — reużywalne rozwiązania problemów. GoF opisał 23 wzorce. Strategy, Observer, Factory, Decorator — to nie jest kod do kopiowania, ale sprawdzone schematy.

No i oczywiście **biblioteki i frameworki** — najoczywistsza forma reużywalności na większą skalę.

### Spodziewane pytania dodatkowe

**„Co to problem diamentu?"** → Gdy klasa dziedziczy po dwóch klasach, które mają wspólną bazę. W C++ — rozwiązanie przez `virtual inheritance`. W Javie — nie ma wielodziedziczenia klas, są interfejsy.

**„Podaj przykład, kiedy dziedziczenie jest lepsze od kompozycji?"** → Gdy potrzebuję polimorfizmu — np. mam kolekcję Shape* i wywołuję draw() — list, circle, rectangle. Każdy rysuje się inaczej, ale interfejs jest wspólny.

**„Czym jest dependency injection?"** → Przekazuję zależności z zewnątrz zamiast tworzyć je wewnątrz klasy. To ułatwia testowanie i wymianę implementacji.

---

\newpage

## PYTANIE 7 · DNS i caching (SKM)

**Pytanie:** *Które serwery DNS zyskują najwięcej na cachingu? Jakie znasz rodzaje serwerów DNS?*

---

### Co mówię

Zacznę od tego, jakie są rodzaje serwerów DNS, bo to kontekst do odpowiedzi na główne pytanie.

[TABLICA: rysuj piramidę DNS]

Na samej górze — **Root Servers**. Jest ich 13 logicznych — od A do M — ale fizycznie setki, rozproszonych przez anycast. Poniżej — **serwery TLD** — odpowiedzialne za .com, .pl, .org. Dalej — **Authoritative** — mają faktyczne rekordy konkretnych domen. Mam primary, który jest edytowalny, i secondary, który jest kopią.

Po stronie klienta mamy **recursive resolver** — to jest ten, który wykonuje pełne rozwiązywanie nazw. ISP-owski resolver, Google 8.8.8.8, Cloudflare 1.1.1.1. I na samym końcu — **stub resolver** w systemie operacyjnym, który po prostu pyta recursive resolver.

[TABLICA: narysuj strzałki: Klient → Recursive → Root → TLD → Authoritative]

Teraz — **które serwery zyskują najwięcej na cachingu?**

Odpowiedź: **root i TLD** — i to zdecydowanie.

Dlaczego? Rozmiar piramidy. Jest tylko 13 logicznych root serwerów, a zapytań o DNS są miliardy dziennie. **Bez cache** — każde zapytanie o cokolwiek musiałoby przejść przez root, potem TLD. Z cache — resolver pyta root RAZ o .com, cachuje ten referral na 48 godzin albo dłużej, i przez ten czas wszystkie zapytania o .com idą bezpośrednio do TLD bez angażowania roota.

TTL-e rootów to 48 godzin do 7 dni! TLD — 24 do 48 godzin. Dzięki temu redukcja ruchu do root serwerów to z prawie 100% do ułamka procenta. Gdyby nie caching, infrastruktura roota nie wytrzymałaby obciążenia.

### Spodziewane pytania dodatkowe

**„Co to anycast?"** → Jeden adres IP rozgłaszany z wielu lokalizacji. Klient łączy się z najbliższą instancją — na podstawie routingu BGP. Wszystkie root servery używają anycast.

**„Co to TTL?"** → Time To Live — ile sekund rekord DNS może być trzymany w cache. Po upłynięciu trzeba odpytać ponownie.

**„Co się stanie jak wyłączysz cache w resolverze?"** → Ogromny wzrost ruchu do root i TLD serwerów. Każde zapytanie zaczyna od góry piramidy. W skali — to zatopiłoby infrastrukturę.

---

\newpage

## PYTANIE 8 · TCP Three-Way Handshake (SKM)

**Pytanie:** *Cel, interpretacja numerów sekwencyjnych, wartość początkowa ISN.*

---

### Co mówię

TCP Three-Way Handshake to mechanizm nawiązywania połączenia. Trzy kroki.

[TABLICA: rysuj diagram]

    Klient              Serwer
      |--- SYN, seq=x ---→|
      |←- SYN+ACK, seq=y, ack=x+1 -|
      |--- ACK, seq=x+1, ack=y+1 →|

Krok pierwszy — klient wysyła **SYN** z losowym numerem sekwencyjnym x. Krok drugi — serwer odpowiada **SYN+ACK**: swoim numerem y i potwierdzeniem x+1. Krok trzeci — klient potwierdza: ACK z ack=y+1.

**Cel?** Trzy rzeczy. Nawiązanie obustronne — obie strony się zgadzają na komunikację. Synchronizacja numerów ISN — obie strony znają początkowy numer drugiej. I uzgodnienie parametrów — w opcjach TCP lecą MSS, Window Scale, SACK.

Teraz — **numery sekwencyjne**. SEQ to numer pierwszego bajtu danych w segmencie. Nie numerujemy segmentów, numerujemy bajty! Jeśli sending seq=100 i 50 bajtów danych, to następny segment zacznie od 150.

**Numery potwierdzenia** — ACK to numer **następnego oczekiwanego bajtu**. Jest kumulatywny — potwierdza wszystko do tego numeru. Jest też SACK — selective ACK — pozwala potwierdzać niesąsiednie bloki.

**ISN** — wartość początkowa. Nie zaczyna od zera! Dwa powody. Po pierwsze — **bezpieczeństwo**: gdyby ISN był zero albo przewidywalny, atakujący mógłby zgadnąć numer sekwencyjny i przejąć sesję. Po drugie — unikanie kolizji z pakietami z poprzednich połączeń. Oryginalny RFC 793 mówił o timerze co 4 mikrosekundy. Nowszy RFC 6528 — ISN jest generowany kryptograficznie z adresów, portów i tajnego klucza.

### Spodziewane pytania dodatkowe

**„Dlaczego trzy kroki, a nie dwa?"** → Bo obie strony muszą potwierdzić swój ISN. W dwóch krokach serwer nie wie, czy klient odebrał jego ISN.

**„Co to SYN flood?"** → Atak DoS — wysyłam tysiące SYN-ów bez dokończenia handshake'u. Serwer trzyma pół-otwarte połączenia, aż wyczerpie zasoby. Obrona — SYN cookies.

---

\newpage

## PYTANIE 9 · Procesy i wątki (SOI)

**Pytanie:** *Budowa, szybkość, zastosowanie. Problemy komunikacji i synchronizacji.*

---

### Co mówię

**Proces** to program w trakcie wykonania. Ma własną przestrzeń adresową — oddzielny kod, dane, stos, heap. Procesy są od siebie **izolowane**. Jeden spadnie — drugi dalej działa.

**Wątek** to lekka jednostka wykonania **wewnątrz** procesu. Współdzieli z procesem kod, dane globalne, heap, otwarte pliki. Ma **prywatny** stos i rejestry.

[TABLICA: narysuj — dwa prostokąty-procesy, w jednym dwa mniejsze prostokąty-wątki z własnymi stosami, ale wspólnym heapem]

Główna różnica praktyczna — **szybkość**. Tworzenie procesu to milisekundy — trzeba kopiować tablicę stron, deskryptory. Tworzenie wątku — mikrosekundy. Przełączanie kontekstu procesu — kosztowne, bo wymaga TLB flush. Przełączanie wątku — znacznie szybsze, bo nie zmienia się przestrzeni adresowej.

**Komunikacja** — i tu jest różnica. Między procesami — IPC: pipe, shared memory, message queue, sockety. Między wątkami — po prostu współdzielona pamięć. Ale ta prostota ma cenę.

**Problemy synchronizacji:**

**Race condition** — dwa wątki modyfikują tę samą zmienną, wynik zależy od kolejności — niedeterminizm.

**Deadlock** — zakleszczenie. Wątek A trzyma zasób 1 i czeka na 2, wątek B trzyma 2 i czeka na 1. Cztery warunki Coffmana: mutual exclusion, hold and wait, no preemption, circular wait. Złam jeden — deadlocka nie ma.

**Starvation** — zagłodzenie, wątek nigdy nie dostaje zasobu.

Mechanizmy rozwiązań: mutex, semafor, monitor, condition variable, spinlock, barrier.

Lubię tę analogię: proces to mieszkanie — ma adres, własne ściany. Wątek to pokój — współdzieli kuchnię i łazienkę z innymi pokojami.

### Spodziewane pytania dodatkowe

**„Czym jest mutex a czym semafor?"** → Mutex — binarny zamek, tylko jeden wątek wchodzi do sekcji krytycznej. Semafor — licznik: pozwala na N jednoczesnych dostępów. Mutex to w zasadzie semafor z N=1, ale semantycznie — mutex ma właściciela.

**„Co to jest TLB?"** → Translation Lookaside Buffer — cache translacji adresów wirtualnych na fizyczne. Przy zmianie procesu — trzeba go wyczyścić, bo nowy proces ma inną tablicę stron.

---

\newpage

## PYTANIE 10 · Zarządzanie pamięcią (SOI)

**Pytanie:** *Problemy i mechanizmy. Stronicowanie vs segmentacja.*

---

### Co mówię

Zarządzanie pamięcią musi rozwiązać kilka problemów. **Fragmentacja** — zewnętrzna, gdy wolna pamięć jest porozrzucana, i wewnętrzna, gdy przydzielony blok jest większy niż potrzeba. **Ochrona** — proces nie może czytać pamięci innego procesu. **Relokacja** — program musi działać pod różnymi adresami. **Współdzielenie** — biblioteki współdzielone, copy-on-write.

Dwa podejścia — stronicowanie i segmentacja.

[TABLICA: stronicowanie — rysuj kratki jednakowej wielkości po obu stronach (strony i ramki)]

**Stronicowanie** — dzielę pamięć wirtualną na **strony** stałego rozmiaru, najczęściej 4KB. Pamięć fizyczna to **ramki** tego samego rozmiaru. Tablica stron mapuje strony na ramki. Adres = numer strony + offset, translacja zamienia numer strony na numer ramki.

Zalety — **brak fragmentacji zewnętrznej**, bo wszystko jest tego samego rozmiaru. Wada — fragmentacja wewnętrzna, ale mała — średnio pół strony.

TLB — cache translacji — bo sięganie do tablicy stron na każdy dostęp byłoby za wolne. Page fault — gdy strona nie jest w RAM-ie, ładujemy z dysku-swap. Algorytmy wymiany: FIFO, LRU, Clock.

[TABLICA: segmentacja — rysuj bloki różnej wielkości etykietowane: KOD, DANE, STOS]

**Segmentacja** — dzielę pamięć na logiczne **segmenty** o różnych rozmiarach — segment kodu, danych, stosu. Naturalnie odpowiada strukturze programu. Ochrona jest naturalna — per segment mogę ustawić prawa R/W/X.

Wada — **fragmentacja zewnętrzna**, bo segmenty są różnej wielkości.

W praktyce — **stronicowanie wygrało**. x86-64 ma flat segmentation — segmenty obejmują całą przestrzeń, a faktyczna translacja idzie przez stronicowanie wielopoziomowe. Intel praktycznie porzucił segmentację.

### Spodziewane pytania dodatkowe

**„Co to copy-on-write?"** → Przy fork() dziecko dostaje tę samą pamięć co rodzic — ale strony są oznaczone jako read-only. Dopiero przy pierwszym zapisie robimy kopię. Oszczędność — bo często dziecko robi exec() i zmienia cały obraz.

**„Dlaczego wielopoziomowe tablice stron?"** → Bo dla 64-bit jednopoziomowa tablica byłaby gigantyczna. Wielopoziomowa — alokujemy tylko te fragmenty tablicy, które naprawdę pokrywają używaną pamięć.

---

\newpage

## PYTANIE 11 · Modelowanie procesów biznesowych (WSYZ)

**Pytanie:** *Scharakteryzować standardy i narzędzia do modelowania procesów biznesowych.*

---

### Co mówię

Standard numer jeden to **BPMN 2.0**. To jest to, co się pojawia wszędzie, gdzie biznes spotyka IT.

BPMN ma trzy typy elementów. **Zdarzenia** — koła: start, pośrednie, końcowe. **Czynności** — prostokąty z zaokrąglonymi rogami: taski i podprocesy. **Bramki** — romby: XOR — jeden z wielu, AND — wszystkie ścieżki, OR — jeden lub więcej.

[TABLICA: narysuj prosty proces BPMN — koło start → task → bramka XOR → dwa taski → koło end]

Do tego — **swimlanes**: pool to organizacja, lane to dział wewnątrz. Pozwalają pokazać kto za co odpowiada.

BPMN 2.0 ma format XML — to znaczy, że diagram nie jest tylko rysunkiem, może być wykonywany w silniku procesowym jak Camunda.

Drugi standard — **diagramy aktywności UML**. Podobne do BPMN, ale bardziej zorientowane na IT. Mają fork/join dla współbieżności, pin-y dla przepływu obiektów. Lepsze do modelowania procesów technicznych, gorsze dla osób biznesowych.

Trzeci — **EPC** (Event-driven Process Chain). Naprzemienne zdarzenia i funkcje, łączniki AND/OR/XOR. Popularny w ekosystemie SAP, framework ARIS.

Porównanie: BPMN jest uniwersalny — łączy biznes z IT. UML Activity — głównie dla programistów. EPC — głównie SAP.

Narzędzia: Bizagi Modeler, Camunda, Signavio, Lucidchart, draw.io, Enterprise Architect.

### Spodziewane pytania dodatkowe

**„Jaka jest różnica między bramką XOR a OR?"** → XOR — dokładnie jedna ścieżka. OR — jedna LUB więcej. AND — wszystkie. W praktyce XOR jest najczęstsza.

**„Czy BPMN może być wykonywany automatycznie?"** → Tak, BPMN 2.0 ma format XML, który silniki procesowe — Camunda, jBPM — mogą interpretować i wykonywać.

---

\newpage

## PYTANIE 12 · Sieciowe modele optymalizacji (WSYZ)

**Pytanie:** *Przedstawić sieciowe modele optymalizacji stosowane w systemach zarządzania.*

---

### Co mówię

Tutaj chodzi o problemy optymalizacyjne, które modelujemy na grafach. Wymienię kilka najważniejszych.

[TABLICA: narysuj prosty graf z wagami]

**Najkrótsza ścieżka** — klasyka. Dijkstra, Bellman-Ford, A\*. Zastosowanie — GPS, routing w sieciach. Omawialiśmy już wcześniej.

**Maksymalny przepływ** — mam sieć z pojemnościami na krawędziach, chcę przepchnąć jak najwięcej ze źródła do ujścia. Algorytm Ford-Fulkersona, Edmonds-Karp. Zastosowanie — przepustowość sieci, planowanie produkcji.

**Minimalny koszt przepływu** — jak max flow, ale oprócz pojemności każda krawędź ma koszt. Chcę przepchnąć wymaganą ilość po minimalnym koszcie. Transport, logistyka.

**Problem przydziału** — n zadań do n pracowników, macierz kosztów, minimalizuj sumę. Algorytm węgierski, O(n³). HR, grafiki zmianowe.

**TSP — problem komiwojażera** — odwiedź wszystkie miasta dokładnie raz, wróć do startu, minimalizuj trasę. NP-trudny — dokładne rozwiązanie nie skaluje się. W praktyce — heurystyki, metaheurystyki. Trasy kurierów.

**CPM/PERT** — harmonogramowanie projektów. Wierzchołki to zadania, krawędzie to zależności. Ścieżka krytyczna — najdłuższa ścieżka w grafie — wyznacza minimalny czas projektu.

**MST — minimalne drzewo rozpinające** — połącz wszystkie wierzchołki minimalnym kosztem. Kruskal, Prim. Sieci infrastrukturalne — kablowanie, wodociągi.

Wspólny mianownik — to wszystko to grafy z wagami i pytanie „jak optymalnie wykorzystać tę sieć?"

### Spodziewane pytania dodatkowe

**„Jaka jest różnica między CPM a PERT?"** → CPM — deterministyczne czasy zadań. PERT — probabilistyczne, z trzema oszacowaniami (optymistyczny, pesymistyczny, prawdopodobny).

**„Dlaczego TSP jest NP-trudny?"** → Nie znamy algorytmu wielomianowego. Brute force to O(n!) — nie skaluje się. Heurystyki dają przybliżone rozwiązania w rozsądnym czasie.

---

\newpage

## PYTANIE 13/27 · Modelowanie architektury systemów informatycznych (AIS)

**Pytanie:** *Cele i metody modelowania architektury.*

---

### Co mówię

Modelowanie architektury to sposób na zarządzanie złożonością systemu. Cele — komunikacja między zespołami, dokumentacja decyzji, analiza atrybutów jakości, planowanie ewolucji.

Kilka frameworków.

**C4 Model** — bo jest najprostszy i najpopularniejszy. Simon Brown. Cztery poziomy zoomu:
Level 1 — Context: system w otoczeniu, kto z niego korzysta.
Level 2 — Container: główne komponenty — web app, baza danych, API.
Level 3 — Component: wewnątrz kontenera.
Level 4 — Code: klasy, kluczowe fragmenty. Zazwyczaj ten poziom to za dużo.

[TABLICA: narysuj cztery kwadraciki, coraz bardziej szczegółowe — „zoom"]

**4+1 View Model** Kruchtena. Pięć perspektyw: Logical — funkcjonalność, Process — współbieżność, Development — organizacja kodu, Physical — wdrożenie i sprzęt. I Scenarios — use-case'y, które to wszystko łączą.

**TOGAF** — metodyka korporacyjna. ADM — Architecture Development Method. Cztery domeny: Business, Data, Application, Technology. Duży, formalny, enterprise.

**Zachman Framework** — taksonomia. Tabela 6×6: What/How/Where/Who/When/Why na jednej osi, a poziomy abstrakcji na drugiej. Nie mówi JAK modelować, mówi CO trzeba opisać.

**ArchiMate** — notacja graficzna dla architektury enterprise. Trzy warstwy: Business, Application, Technology.

Do analizy — **ATAM**: ocena kompromisów architektonicznych, np. performance vs security. Atrybuty jakości z ISO 25010.

### Spodziewane pytania dodatkowe

**„Co to ADR?"** → Architecture Decision Record. Dokument opisujący jedną decyzję architektoniczną: kontekst, decyzja, konsekwencje. Lekka forma dokumentacji.

**„Kiedy użyć C4 vs TOGAF?"** → C4 — projekty software'owe, dokumentacja techniczna. TOGAF — architektura korporacyjna, strategic planning, duże organizacje.

---

\newpage

## PYTANIE 14/28 · Wzorce architektoniczne (AIS)

**Pytanie:** *Czemu służą? Jak powstają? Jak są katalogowane? Przykłady.*

---

### Co mówię

Wzorzec architektoniczny to sprawdzone rozwiązanie powtarzalnego problemu. Służą jako **wspólne słownictwo** — mówię „microservices" i każdy wie o co chodzi — oraz jako **przenoszenie wiedzy** między projektami.

**Jak powstają?** Ktoś rozwiązuje problem. Inni rozwiązują podobne problemy podobnie. Ktoś to zauważa, uogólnia i **dokumentuje**. Struktura: Nazwa + Problem + Rozwiązanie + Konsekwencje.

**Katalogi:**
- **GoF** — 23 wzorce projektowe, poziom klas i obiektów.
- **POSA** — wzorce architektoniczne, większa skala — Layers, Pipes and Filters, Broker.
- **PoEAA** Fowlera — wzorce dla aplikacji enterprise: Repository, Unit of Work, Active Record.
- **EIP** — Enterprise Integration Patterns — messaging.
- **Cloud Patterns** — Circuit Breaker, Saga, Sidecar.

Przykłady wzorców architektonicznych:

**Layered** — warstwy: prezentacja → logika → dostęp do danych → baza. Prosta separacja odpowiedzialności, ale sztywna i boilerplate.

**Microservices** — niezależne serwisy, osobne wdrożenia, skalowanie per-serwis. Ogromna złożoność operacyjna.

**Event-Driven** — zdarzenia przez broker (np. Kafka). Luźne powiązanie, eventual consistency.

**Hexagonal / Ports & Adapters** — rdzeń logiki biznesowej niezależny od frameworków i baz danych. Porty to interfejsy, adaptery to implementacje. Świetna testowalność.

Złota zasada — **„Monolith first."** Zacznij od monolitu, rozdzielaj gdy poznasz granice domen.

### Spodziewane pytania dodatkowe

**„Jaka jest różnica między wzorcem architektonicznym a projektowym?"** → Skala. Architektoniczny — struktura całego systemu (Layers, Microservices). Projektowy — struktura kodu (Strategy, Observer). Architektoniczny wpływa na deployment, zespoły, skalowanie.

**„Co to CQRS?"** → Command Query Responsibility Segregation — osobne modele do odczytu i zapisu. Optymalizuję każdą stronę niezależnie. Przydatne gdy read i write mają bardzo różne wymagania.

---

\newpage

## PYTANIE 15 · Agent upostaciowiony w robotyce

**Pytanie:** *Jak wykorzystuje się agenta upostaciowionego do specyfikacji sterowników robotów?*

---

### Co mówię

Agent upostaciowiony to agent, który ma ciało fizyczne — sensory, efektory — i działa w rzeczywistym środowisku. W odróżnieniu od agenta software'owego, musi radzić sobie z szumem sensorycznym, opóźnieniami i niepewnością.

Cykl działania to: **Percepcja → Deliberacja → Akcja**. See-Think-Act.

Do specyfikacji sterowników używa się architektury warstwowej — klasycznie trzy warstwy.

[TABLICA: narysuj trzy prostokąty jeden nad drugim]

Na dole — **Controller** — warstwa reaktywna. PID, unikanie kolizji, sterowanie silnikami. Działa w milisekundach. Nie „myśli", reaguje.

W środku — **Sequencer** — zarządza sekwencją zachowań. FSM albo Behavior Tree. Decyduje: teraz jedziemy do punktu A, potem chwytamy, potem wracamy. Skala: setki milisekund.

Na górze — **Planner** — planowanie symboliczne. Zna mapę, zna cel, tworzy plan. Skala: sekundy do minut.

Do formalnej specyfikacji celów i bezpieczeństwa używa się **logiki temporalnej LTL**. Mogę zapisać: „zawsze, gdy jest przeszkoda, nie jedź do przodu" — □(obstacle → ¬move_forward). Albo „ostatecznie dotrzesz do celu" — ◇(at_goal). Te formuły mogą być formalnie weryfikowane.

Nowocześnie — **Behavior Trees** stały się popularnym narzędziem specyfikacji. Selector — wykonaj pierwszy sukces. Sequence — wykonaj wszystkie po kolei. Czytelne, modularne, łatwe do wizualizacji. Wywodzą się z game AI — Halo 2 — ale zaadaptowano je w robotyce.

Model formalny agenta — BDI: Beliefs — co wiem o świecie, Desires — czego chcę, Intentions — co aktualnie realizuję.

### Spodziewane pytania dodatkowe

**„Co to PID?"** → Regulator proporcjonalno-całkująco-różniczkujący. Trzy składniki: P — proporcjonalny do błędu, I — kumulowany błąd, D — szybkość zmiany błędu. Klasyka sterowania.

**„Czym jest ROS?"** → Robot Operating System — middleware pub/sub do komunikacji między modułami robota. Nie jest OS-em w sensie jądra, ale daje abstrakcję komunikacji.

---

\newpage

## PYTANIE 16 · Języki programowania robotów

**Pytanie:** *Omówić specjalizowane języki. Uwypuklić klasyfikację.*

---

### Co mówię

Klasyfikuję języki robotów po **poziomie abstrakcji** — od najwyższego do najniższego.

[TABLICA: napisz piramidkę — T-R-M-S]

**Task-level** — najwyższy. Mówię „podnieś A, połóż na B" — system sam planuje ruchy. PDDL, Behavior Trees. Planowanie zadań.

**Robot-level** — komendy ruchu robota: move_to, grasp, release. Każdy producent ma swój język. ABB — RAPID (MoveJ, MoveL, MoveC). KUKA — KRL (PTP, LIN, CIRC). FANUC — Karel. To jest podejście imperatywne — mówię robotowi co ma robić ruch po ruchu.

**Motion-level** — planowanie trajektorii, kinematyka odwrotna. Biblioteka MoveIt w ROS. Tutaj programista operuje na poziomie „dojedź z pozycji A do B bez kolizji", ale system musi obliczyć konkretną trajektorię.

**Servo-level** — najniższy, sterowanie silnikami. PID, regulacja prądu, pozycji. C/C++, FPGA. Czas rzeczywisty.

Jest też podział na **online vs offline**. Online — uczę robota przy konsoli (teach pendant), prowadzę go ręcznie. Offline — programuję w symulatorze na komputerze, potem wgrywam.

Problem branży — **vendor lock-in**. Każdy producent ma swój język — RAPID, KRL, Karel, PDL2. Nie są kompatybilne. ROS próbuje to ujednolicić jako warstwa abstrakcji, ale ma problem z hard real-time.

Programowanie graficzne — RobotStudio dla ABB, ROBOGUIDE dla FANUC. I Blockly w edukacji.

Ciekawostka etymologiczna: język Karel nazwano od Karla Čapka, czeskiego pisarza, który wymyślił słowo „robot" — od czeskiego „robota" — pańszczyzna.

### Spodziewane pytania dodatkowe

**„Czym się różni PTP od LIN w KUKA?"** → PTP — Point-to-Point — robot jedzie najszybszą drogą, nie kontroluję trajektorii. LIN — ruch liniowy — efektor jedzie po linii prostej. CIRC — ruch kołowy.

**„Czy ROS rozwiązuje problem vendor lock-in?"** → Częściowo. ROS daje wspólną warstwę komunikacji i planowania, ale sterownik nisko poziomowy nadal jest producenta. Oraz ROS nie jest hard real-time w standardowym wydaniu (ROS 2 poprawia to z DDS).

---

\newpage

## PYTANIE 17 · Szeregowanie zadań

**Pytanie:** *Cechy klasyfikacji. Przykładowa metoda.*

---

### Co mówię

Problemy szeregowania klasyfikuje się przez **notację Grahama**: alfa | beta | gamma.

[TABLICA: napisz α | β | γ]

**α** — środowisko maszynowe. 1 — jedna maszyna. Pm — m maszyn równoległych. F — flow shop, wszyscy przechodzą przez maszyny w tej samej kolejności. J — job shop, każde zadanie ma własną trasę.

**β** — cechy zadań. rⱼ — release dates, dⱼ — due dates, pmtn — preemption dozwolona, prec — precedencje.

**γ** — kryterium optymalizacji. Cmax — makespan, czas zakończenia ostatniego. ΣCⱼ — suma czasów zakończenia. Lmax — maksymalne opóźnienie.

Pokażę na przykładzie.

[TABLICA: problem 1 || ΣCⱼ]

Mam jedną maszynę, pięć zadań z czasami: J1(5), J2(3), J3(8), J4(2), J5(6). Chcę zminimalizować sumę czasów zakończenia.

Reguła **SPT** — Shortest Processing Time — uszereguj od najkrótszego.

Sortujemy: J4(2), J2(3), J1(5), J5(6), J3(8).
Czasy zakończenia: 2, 5, 10, 16, 24.
ΣCⱼ = 2+5+10+16+24 = 57. To jest optymalne!

[TABLICA: narysuj oś czasu z zadaniami]

Dlaczego to działa? Intuicja — krótkie zadania kończą się wcześnie i „nie czekają" na długie. Formalnie — zamiana sąsiednich zadań, gdzie krótsze jest za długim, zawsze zwiększa sumę.

Inne reguły: **EDD** — Earliest Due Date — dla Lmax. **Johnson** — optymalny dla dwumaszynowego flow shop.

Większość problemów szeregowania jest **NP-trudna** — job shop, Pm||Cmax dla m≥2.

### Spodziewane pytania dodatkowe

**„Co to makespan?"** → Czas od startu pierwszego zadania do zakończenia ostatniego. Mierzy „jak długo trwa cała produkcja".

**„Czym się różni flow shop od job shop?"** → Flow shop — wszystkie zadania przechodzą przez maszyny w tej samej kolejności, jak taśma produkcyjna. Job shop — każde zadanie ma indywidualną trasę, jak warsztat naprawczy.

---

\newpage

## PYTANIE 18 · Zarządzanie zapasami w łańcuchu dostaw

**Pytanie:** *Problemy i przykładowy model.*

---

### Co mówię

Główny problem — znalezienie równowagi. Za dużo zapasów — koszty magazynowania, pieniądze zamrożone, ryzyko przeterminowania. Za mało — brak towaru, utracona sprzedaż.

Klasyczny problem — **efekt byczego bicza** (bullwhip effect). Małe wahania popytu u detalistów narastają w górę łańcucha — dystrybutor zamawia więcej, producent jeszcze więcej, dostawca surowców widzi gigantyczne wahania. Przyczyny — prognozowanie, zamówienia partiami, promocje.

[TABLICA: narysuj sinusoidę, która się amplifikuje — detalista → dystrybutor → producent]

Podstawowy model — **EOQ** — Economic Order Quantity. Harrisowsko-Wilsonowski.

[TABLICA: napisz wzór]

TC(Q) = K·D/Q + h·Q/2

K — koszt zamówienia, D — popyt roczny, h — koszt utrzymania jednostki na rok, Q — wielkość zamówienia.

Optymalna wielkość: **Q\* = √(2KD/h)**

Przykład: D=10000, K=100, h=2. Q\* = √(2·100·10000/2) = √(1000000) = 1000 sztuk. Koszt optymalny — 2000 PLN/rok.

Jest jeszcze **punkt ponownego zamawiania** — ROP = d × L + SS. Popyt dzienny razy lead time plus safety stock. Safety stock zależy od poziomu obsługi — na 95% bierzemy z=1.65, mnożymy przez odchylenie popytu w czasie dostawy.

Modele zaawansowane: (s,Q) — zamawiaj Q gdy stan spadnie do s. (s,S) — zamawiaj do poziomu S. VMI — dostawca sam zarządza zapasem u klienta.

### Spodziewane pytania dodatkowe

**„Jakie są założenia EOQ?"** → Popyt stały i znany, lead time zero lub stały, brak rabatów ilościowych, dostawy jednorazowe. Bardzo uproszczony model, ale daje dobre intuicje.

**„Jak ograniczyć bullwhip effect?"** → Dzielenie danych o popycie w czasie rzeczywistym (POS data), VMI, mniejsze partie zamówień, stabilne ceny bez promocji.

---

\newpage

## PYTANIE 19/29 · Model Publish-Subscribe

**Pytanie:** *Scharakteryzować model i przykładowe rozwiązania techniczne.*

---

### Co mówię

Pub/Sub to wzorzec komunikacji, w którym nadawcy nie wysyłają wiadomości bezpośrednio do odbiorców. Między nimi jest **broker**.

[TABLICA: narysuj]

    Publishers → [Broker] → Subscribers

Publisher mówi „oto zdarzenie", a broker dostarcza je wszystkim zainteresowanym subskrybentom. Kluczowa cecha — **luźne powiązanie**: publisher nie wie kto słucha, subscriber nie wie kto wysyła. Jak stacja radiowa — nadaje, kto chce słucha.

Typy subskrypcji: **topic-based** — subskrybuję temat, np. „orders.created". **Content-based** — filtracja po zawartości wiadomości. Hierarchiczne tematy z wildcardami — np. „orders.#" łapie wszystko z prefiksem.

Gwarancje dostarczenia — QoS. At-most-once — mogę stracić wiadomość. At-least-once — mogą być duplikaty. Exactly-once — najdroższa gwarancja, ale najtrudniejsza do osiągnięcia.

Teraz konkretne technologie.

**Kafka** — model oparty na logu. Producer pisze do partycji, consumer czyta z offsetu. Pull model — consumer sam decyduje kiedy czyta. Persistence domyślnie — mogę odtworzyć strumień. Very high throughput. Consumer groups — load balancing. LinkedIn, potem Apache.

**RabbitMQ** — AMQP, push model. Exchange types: Direct, Topic, Fanout, Headers. Bardziej elastyczny routing, ale wiadomości znikają po konsumpcji. Tradycyjny message broker.

**MQTT** — lekki, 2-bajtowy header. Idealny dla IoT, urządzenia z ograniczonymi zasobami. Trzy poziomy QoS.

**Redis Pub/Sub** — prosty, szybki, ale fire-and-forget — brak persistence. Dobre do real-time notyfikacji.

### Spodziewane pytania dodatkowe

**„Kafka vs RabbitMQ — kiedy co?"** → Kafka — event streaming, duże wolumeny, replay, analityka. RabbitMQ — task queues, złożony routing, tradycyjny messaging. Kafka to log, RabbitMQ to kolejka.

**„Co jeśli broker padnie?"** → Broker to Single Point of Failure. Rozwiązanie — replication, clustering. Kafka ma replication factor, RabbitMQ ma mirrored queues.

---

\newpage

## PYTANIE 20/30 · Analityka danych strumieniowych

**Pytanie:** *Rozwiązania analityczne na danych strumieniowych.*

---

### Co mówię

Strumień danych to dane, które płyną ciągle, potencjalnie w nieskończoność. Nie mogę zebrać wszystkiego i przetworzyć — muszę analizować na bieżąco.

Kluczowy koncept — **okna czasowe** (windowing).

[TABLICA: narysuj oś czasu z oknami]

**Tumbling** — rozłączne okna stałego rozmiaru. Każde zdarzenie należy do dokładnie jednego okna. Np. liczba zdarzeń co minutę.

**Sliding** — nakładające się okna. Rozmiar 10 minut, przesunięcie co 1 minutę. Zdarzenie może być w wielu oknach.

**Session** — definiowane aktywnością. Okno trwa dopóki są zdarzenia, zamyka się po przerwie (gap).

**Global** — jedno wielkie okno, trigger decyduje kiedy emitować wynik.

Platformy:

**Apache Flink** — true streaming, przetwarza zdarzenie po zdarzeniu. Bardzo niska latencja, exactly-once guarantees. SOTA do stream processingu. Nazwa — z niemieckiego „flink" = szybki.

**Spark Streaming** — micro-batch. Zbiera zdarzenia w małe paczki i przetwarza. Latencja ~100ms. Prostszy model programowania, łatwo przejść z batcha.

**Kafka Streams** — biblioteka, nie klaster. Wbudowana w Kafkę. Lekka, nie wymaga osobnej infrastruktury.

Problem czasu — **Event Time vs Processing Time**. Zdarzenie powstaje o 12:00, dociera o 12:05 — który czas liczymy? Watermarki mówią systemowi „do tego momentu powinny dotrzeć wszystkie zdarzenia". Spóźnione dane — drop, przeliczymy, boczny output.

Algorytmy strumieniowe — gdy nie ma pamięci na wszystko. **HyperLogLog** — zlicz unikalne elementy z kilobajtem pamięci, ~2% błąd. **Count-Min Sketch** — estymacja częstości. **Reservoir Sampling** — losowa próbka z nieznanego strumienia.

### Spodziewane pytania dodatkowe

**„Czym jest watermark?"** → Znacznik postępu event time. Mówi: „wszystkie zdarzenia z czasem mniejszym niż W już dotarły." Spóźnione — traktujemy wg strategii: ignoruj, przelicz, side output.

**„Micro-batch vs true streaming?"** → Micro-batch zbiera dane w małe paczki i przetwarza periodycznie — prostsza semantyka, ale wyższe latencje. True streaming — przetwarza per wydarzenie — niższa latencja, ale bardziej skomplikowana obsługa stanu i exactly-once.

---

\newpage

## PYTANIE 21 · Zegary logiczne i wektory stempli czasowych

**Pytanie:** *Koncepcja i przeznaczenie.*

---

### Co mówię

W systemach rozproszonych nie ma globalnego zegara. Każdy węzeł ma swój zegar i one się rozjeżdżają — drift, opóźnienia sieciowe. Nie możemy powiedzieć „to zdarzenie było pierwsze" patrząc na czas ścienny.

Lamport w 1978 roku zaproponował rozwiązanie — **relacja happened-before**. Zapisuję ją jako →.

Reguły: jeśli a jest przed b w tym samym procesie — a → b. Jeśli a to wysłanie wiadomości, a b to jej odbiór — a → b. I przechodniość. Jeśli nie mogę ustalić porządku — zdarzenia są **współbieżne**, a || b.

**Zegar Lamporta** — skalarny. Każdy proces ma licznik C. Przed zdarzeniem — inkrementuję. Wysyłając — dołączam C do wiadomości. Odbierając — biorę max ze swojego C i odebranego, i inkrementuję.

[TABLICA: narysuj trzy procesy, strzałki wiadomości, dopisz wartości zegara]

Problem — zegar Lamporta gwarantuje: jeśli a → b, to C(a) < C(b). Ale **nie odwrotnie**! Jeśli C(a) < C(b), nie wiem czy a → b, czy są współbieżne. Nie wykrywa współbieżności.

**Zegary wektorowe** rozwiązują ten problem. Każdy z N procesów trzyma wektor V[1..N]. Przed zdarzeniem — V[i]++. Wysyłając — dołączam cały wektor. Odbierając — V[j] = max(V[j], T[j]) dla wszystkich j, potem V[i]++.

Kluczowa właściwość: **a → b ⟺ V(a) < V(b)**. Równoważność! Jeśli wektory są nieporównywalne — zdarzenia są współbieżne.

Porównanie wektorów: V ≤ W wtedy gdy V[i] ≤ W[i] dla każdego i. Współbieżne — gdy ani V ≤ W, ani W ≤ V.

Cena — wektor ma rozmiar O(N). Lamport — O(1). Dla małych systemów nieistotne, dla tysięcy procesów — problematyczne.

Zastosowania — wykrywanie konfliktów w replikacji (Amazon Dynamo), causal broadcast, debugowanie rozproszone.

### Spodziewane pytania dodatkowe

**„Co to version vectors w Dynamo?"** → Wariant zegarów wektorowych do śledzenia wersji obiektów w replikowanej bazie. Pozwalają wykryć konflikty — jeśli wektory nieporównywalne, to dwa węzły pisały niezależnie.

**„Czy da się coś między Lamportem a vector clock?"** → Tak — np. dotted version vectors, albo Bloom clocks — hybrydowe podejścia, które oszczędzają pamięć przy zachowaniu wykrywania współbieżności.

---

\newpage

## PYTANIE 22 · Modele spójności danych w systemach rozproszonych

**Pytanie:** *Silne i słabe modele spójności.*

---

### Co mówię

To pytanie o kompromis — im silniejsza spójność, tym wolniejszy system. Im słabsza — tym szybszy, ale trudniejszy do programowania.

[TABLICA: narysuj spektrum od lewej do prawej]

    Linearizability → Sequential → Causal → Session → Eventual

**Linearizability** — najsilniejsza. Każda operacja wygląda tak, jakby wykonała się atomowo w jednym momencie między wywołaniem a odpowiedzią. Globalny czas rzeczywisty. Kosztowna — wymaga konsensusu. Przykład — Google Spanner, który synchronizuje atomowe zegary.

**Sequential consistency** — jest globalny porządek operacji, zgodny z porządkiem programu każdego procesu, ale NIE musi zgadzać się z czasem rzeczywistym. Przykład — ZooKeeper.

**Causal consistency** — operacje przyczynowo zależne widziane w tej samej kolejności przez wszystkich. Niezależne — mogą być w różnej kolejności. Wymaga vector clocks.

**Session guarantees** — słabsze: Read Your Writes — widzę to co napisałem. Monotonic Reads — nie cofam się w czasie.

**Eventual consistency** — najsłabsza. Jeśli przestanę pisać, to kiedyś wszystkie repliki się zsynchronizują. Ale nie wiadomo kiedy. DNS, Cassandra, DynamoDB.

**CAP Theorem** — w obliczu partycji sieciowej muszę wybrać: Consistency albo Availability. Nie mogę mieć obu. CP — np. Spanner, silna spójność, ale niedostępny przy partycji. AP — np. Cassandra, zawsze dostępna, ale eventual.

Konflikty w modelu eventual rozwiązuję przez: Last-Writer-Wins, porównanie wersji, albo **CRDTs** — struktury, które matematycznie gwarantują, że po zsynchronizowaniu dają ten sam wynik niezależnie od kolejności.

### Spodziewane pytania dodatkowe

**„Czy CAP to wybór 2 z 3?"** → W praktyce — partycja się zdarzy, więc to nie „wybierz 2 z 3", tylko „przy partycji: C czy A?" Normaltynie system ma C i A, problem pojawia się przy awarii sieci.

**„Co to quorum?"** → W replikacji — W+R > N gwarantuje, że odczyt trafi na co najmniej jedną replikę z najnowszą wersją. Np. N=3, W=2, R=2.

---

\newpage

## PYTANIE 23 · Segmentacja obrazu

**Pytanie:** *Problem, strategie klasyczne i sieci neuronowe.*

---

### Co mówię

Segmentacja to przypisanie **każdemu pikselowi** etykiety klasy lub regionu. W odróżnieniu od klasyfikacji — która mówi „co jest na zdjęciu" — segmentacja mówi **gdzie** dokładnie.

Typy: **Semantic** — klasa per piksel, wszystkie samochody to „samochód". **Instance** — rozróżnia poszczególne instancje, ten samochód od tamtego. **Panoptic** — łączy oba.

Metody klasyczne:

**Thresholding** — próg intensywności. Piksele powyżej progu — obiekt, poniżej — tło. Otsu automatycznie dobiera próg. Proste, ale ograniczone do dwóch klas.

**Region growing** — zaczynam od punktu seed, dodaję sąsiednie piksele spełniające kryterium podobieństwa. Tendencja do over-segmentation.

**Watershed** — traktujemy obraz jako teren topograficzny i „zalewamy wodą". Granice — tam, gdzie woda z różnych źródeł się spotyka.

Deep learning — tu nastąpił przełom:

**U-Net** — encoder-decoder w kształcie U. Encoder kompresuje obraz, decoder odtwarza rozdzielczość. Kluczowe — **skip connections** — łączą warstwy o tej samej rozdzielczości z encodera do decodera. Popularne w medycynie — mało danych, ale skip connections pomagają zachować detale.

**DeepLab** — atrous (dilated) convolutions — powiększają receptive field bez dodatkowych parametrów. ASPP — multi-scale processing.

**Metryka** — mIoU: intersection over union, uśrednione po klasach. Standard w benchmarkach.

[TABLICA: narysuj kształt litery U z prostokątów — encoder po lewej, decoder po prawej, strzałki skip]

### Spodziewane pytania dodatkowe

**„Co to dilated convolution?"** → Normalna konwolucja ma filtr 3×3 pokrywający 3×3 pikseli. Dilated — filtr 3×3, ale z przerwami — widzi np. 5×5 lub 7×7 pikseli. Większe receptive field przy tych samych parametrach.

**„Dlaczego U-Net jest popularne w medycynie?"** → Bo wymaga mało danych treningowych — skip connections zachowują informacje przestrzenne. Obrazy medyczne są drogie do annotacji, więc data efficiency jest kluczowa.

---

\newpage

## PYTANIE 24 · Detekcja obiektów

**Pytanie:** *Problem, metody klasyczne, deep learning. Jak zbudować detektor z klasyfikatora?*

---

### Co mówię

Detekcja obiektów to jednoczesna **lokalizacja** (bounding box) i **klasyfikacja**. Wynik: klasa, współrzędne ramki, pewność.

Podejścia dzielę na dwa etapy — two-stage i one-stage.

**Two-stage — rodzina R-CNN:**

R-CNN — generuję ~2000 regionów przez Selective Search, każdy region przepuszczam przez CNN, klasyfikuję SVM-em. Bardzo wolne — 50 sekund na obraz.

Fast R-CNN — CNN raz na cały obraz, potem ROI Pooling — wycinam cechy regionu z mapy cech. ~2 sekundy.

**Faster R-CNN** — kluczowy krok — Region Proposal Network. Zamiast Selective Search — sieć sama proponuje regiony. End-to-end. ~5 fps.

[TABLICA: obraz → CNN → RPN → ROI Pool → klasyfikacja + bbox regression]

**One-stage — YOLO, SSD:**

**YOLO** — You Only Look Once. Dzielę obraz na siatkę S×S, każda komórka predykuje bounding boxy i klasy naraz, w jednym przebiegu sieci. 45-155 fps! Rewolucja w szybkości. Gorszy dla małych obiektów, ale kolejne wersje to poprawiaj.

Po detekcji — **NMS** — Non-Maximum Suppression. Mam wiele nakładających się detekcji tego samego obiektu. Sortuję po confidence, biorę najlepszą, usuwam te, które się z nią mocno nakładają (IoU > próg), powtarzam.

Teraz — **jak zbudować detektor z klasyfikatora?**

Trzy sposoby, coraz lepsze:
1. **Sliding window** — przesuwam okno, każdy patch klasyfikuję. Ekstremalnie wolne.
2. **Region proposals + klasyfikator** — Selective Search wysiewa kandydatów, klasyfikuję każdego. Szybsze, ale wciąż oddzielne kroki.
3. **Fine-tune** — biorę pretrained klasyfikator jako backbone, doczepiam głowicę detekcyjną — bbox regression + klasyfikacja. End-to-end. Najlepsza jakość.

### Spodziewane pytania dodatkowe

**„YOLO vs Faster R-CNN — kiedy co?"** → YOLO — gdy zależy na szybkości — real-time, wideo, edge computing. Faster R-CNN — gdy zależy na dokładności, zwłaszcza dla małych obiektów.

**„Co to anchor boxes?"** → Predefiniowane kształty ramek o różnych proporcjach. Sieć nie predykuje ramki od zera — predykuje offset od najbliższego anchora. Anchor-free (np. YOLOv8) — bez tego, predykuje punkt centralny i wymiary.

---

\newpage

## PYTANIE 25 · Prawo Amdahla — przyspieszenie równoległe

**Pytanie:** *Oszacować przyspieszenie. Co osłabia ograniczenie?*

---

### Co mówię

Prawo Amdahla mówi, ile zyskam dodając procesory.

[TABLICA: napisz wzór]

    S(n) = 1 / ((1−p) + p/n)

p — część kodu, która może być zrównolegloona. n — liczba procesorów. 1−p — część sekwencyjna.

Kluczowe — przy n dążącym do nieskończoności:

    S_max = 1 / (1−p)

Jeśli 10% kodu jest sekwencyjne — maksymalne przyspieszenie to 10x. Nawet z milionem procesorów. Sekwencyjna część jest limitem.

[TABLICA: szybka tabelka]

| p    | n=4  | n=16 | n→∞  |
|------|------|------|------|
| 90%  | 3.08 | 5.93 | 10   |
| 95%  | 3.48 | 9.52 | 20   |
| 99%  | 3.88 |13.91 | 100  |

To jest dość pesymistyczna perspektywa. **Co osłabia to ograniczenie?**

**Prawo Gustafsona** — zmień perspektywę. Amdahl mówi: stały problem, więcej procesorów. Gustafson mówi: stały czas, **większy problem**. S = 1 − p + p·n. Dla p=90%, n=100 → S=90.1. Bo w praktyce — gdy mam więcej procesów, daję im więcej danych do przetwarzania, a nie ten sam mały problem.

Techniki zmniejszania sekwencyjnej części: algorytmy równoległe (zamiast sekwencyjnych), lock-free structures (zamiast mutexów), pipelining, ukrywanie latencji — async I/O, prefetching.

Ale w praktyce przyspieszenie jest jeszcze gorsze niż Amdahl przewiduje — overhead synchronizacji, komunikacja, load imbalance, efekty cache (false sharing).

### Spodziewane pytania dodatkowe

**„Jaka jest różnica między strong scaling a weak scaling?"** → Strong — stały problem, dodaję procesory. Amdahl. Weak — zwiększam problem proporcjonalnie do procesorów. Gustafson. W HPC — weak scaling jest bardziej realistyczny.

**„Co to false sharing?"** → Dwa wątki piszą do różnych zmiennych, ale tych samych cache lines. CPU unieważnia cache lines nawzajem — ogromne spowolnienie, mimo braku logicznego konfliktu.

---

\newpage

## PYTANIE 26 · Komunikacja synchroniczna/asynchroniczna, blokująca/nieblokująca

**Pytanie:** *Definicje. Jak uniknąć zakleszczenia w symetrycznych procesach (Jacobi)?*

---

### Co mówię

Dwa wymiary — i ludzie je często mylą.

**Synchroniczna vs asynchroniczna** — dotyczy tego, czy nadawca czeka na odbiorcę. Synchroniczna — nadawca czeka aż odbiorca przyjmie wiadomość. Asynchroniczna — nadawca wrzuca do bufora i jedzie dalej.

**Blokująca vs nieblokująca** — dotyczy tego, czy funkcja wraca od razu. Blokująca — nie wraca dopóki operacja nie skończona. Nieblokująca — wraca natychmiast, operacja w tle, sprawdzam wynik później.

W MPI: MPI_Send — blokująca, synchroniczność zależy od implementacji. MPI_Ssend — blokująca synchroniczna. MPI_Isend — nieblokująca. „I" od Immediate.

Teraz — **problem zakleszczenia w symetrycznym kodzie**.

[TABLICA: narysuj dwa procesy i strzałki]

    Proc 0: Send(to=1);   Recv(from=1);
    Proc 1: Send(to=0);   Recv(from=0);

Oba robią Send jako pierwsze. Oba czekają aż partner odbierze. Nikt nie robi Recv. **Deadlock.**

**Rozwiązania:**

Pierwsze — **asymetria**. Proc 0: Send → Recv. Proc 1: Recv → Send. Jeden wysyła pierwszy, drugi odbiera pierwszy. Prosty, działa.

Drugie — **nieblokujące**. Oba robią Irecv + Isend + Wait. Isend i Irecv wracają natychmiast, inicjują operacje w tle, Wait czeka na zakończenie obu. Symetryczny kod, zero deadlocków.

Trzecie — **MPI_Sendrecv** — jedna funkcja, która jednocześnie wysyła i odbiera. Implementacja dba żeby nie było zakleszczenia. Najprostsze rozwiązanie.

Czwarte — **Bsend** — buforowane. Kopiuje dane do bufora i wraca. Nie czeka na odbiorcę.

### Spodziewane pytania dodatkowe

**„Co to metoda Jacobiego i dlaczego ma ten problem?"** → Metoda iteracyjna rozwiązywania układów równań. W wersji równoległej — każdy proces liczy swoją część i wymienia wyniki z sąsiadami. Symetryczny wzorzec — wszyscy robią to samo — stąd ryzyko Send-Send deadlocka.

**„Kiedy użyć Isend vs Ssend?"** → Isend — gdy chcę nakładać komunikację z obliczeniami. Ssend — gdy potrzebuję pewności, że odbiorca odebrał (np. protokół synchroniczny).

---

\newpage

## PYTANIE 31 · Interaktywne wspomaganie decyzji w warunkach ryzyka

**Pytanie:** *Przedstawić metody interaktywne.*

---

### Co mówię

„Warunki ryzyka" — znamy prawdopodobieństwa wyników, ale nie wiemy na pewno co się stanie. W odróżnieniu od pewności — gdzie wiem dokładnie — i niepewności — gdzie nie znam nawet prawdopodobieństw.

„Interaktywne" — kluczowe słowo. Nie narzucamy decydentowi wyniku. Prowadzamy **dialog** — odkrywamy jego preferencje, funkcję użyteczności — i na tej podstawie rekomendujemy.

**Metoda loterii** — najprostsza. Ustalam U(worst)=0, U(best)=1. Pytam: „wolisz x na pewno, czy loterię — z prawdopodobieństwem p najlepszy wynik, z 1−p najgorszy?" Punkt obojętności p\* = U(x). Powtarzam dla kilku wartości x — otrzymuję kształt funkcji użyteczności.

**Certainty Equivalent** — CE loterii to pewna kwota, której wartość dla decydenta jest taka sama jak loterii. Jeśli CE < wartość oczekiwana — decydent jest **risk-averse**, ma wklęsłą funkcję użyteczności. CE > E[X] — risk-seeking.

**AHP** — Analytic Hierarchy Process Saaty'ego. Strukturyzuję problem jako hierarchię: cel na górze, kryteria w środku, alternatywy na dole. Porównuję parami w skali 1–9. Z macierzy porównań wyciągam wagi — eigenvalue. Sprawdzam spójność — CR < 0.1.

[TABLICA: narysuj hierarchię — Cel → Kryteria → Alternatywy]

**PROMETHEE** — definiuję funkcje preferencji per kryterium. Obliczam przepływy: Φ⁺ — ile razy alternatywa dominuje inne, Φ⁻ — ile razy jest dominowana. Φ net = Φ⁺ − Φ⁻. Ranking.

**ELECTRE** — concordance (na ile kryteriów A jest lepsza od B) plus discordance (jak bardzo B jest lepsza w najgorszym kryterium). Outranking: A S B.

### Spodziewane pytania dodatkowe

**„Czym jest risk premium?"** → E[X] − CE. Ile decydent „zapłaci" za pozbycie się ryzyka. Risk-averse → premium > 0.

**„Kiedy AHP a kiedy PROMETHEE?"** → AHP — gdy mogę porównać parami, niewielu kryteriów i alternatyw. PROMETHEE — gdy mam więcej danych ilościowych i chcę ranking z przepływami.

---

\newpage

## PYTANIE 32 · Dominacja stochastyczna

**Pytanie:** *FSD i SSD. Jak mogą być użyte w modelach wyboru?*

---

### Co mówię

Dominacja stochastyczna pozwala porównać dwie inwestycje — dwa rozkłady wyników — **bez znajomości dokładnej funkcji użyteczności**. Jeśli A dominuje B, to każdy racjonalny decydent z danej klasy wybierze A.

**FSD — First-order Stochastic Dominance.**

[TABLICA: narysuj dwie dystrybuanty, F_A zawsze poniżej F_B]

A dominuje B w sensie FSD wtedy gdy dystrybuanta A nie jest wyższa od B w żadnym punkcie: F_A(x) ≤ F_B(x) dla każdego x.

Interpretacja — A daje **zawsze nie mniejsze prawdopodobieństwo** przekroczenia dowolnego progu. Potrzebuję tylko jednego założenia o U: U' ≥ 0, czyli „więcej = lepiej". Klasa: wszyscy racjonalni, nienasyceni.

FSD jest **rzadka** w praktyce — dystrybuanty nie mogą się przecinać.

**SSD — Second-order Stochastic Dominance.**

A dominuje B wtedy gdy **całka** z dystrybuanty A nie przekracza całki z B — dla każdego x. Dystrybuanty **mogą się przecinać**, ale skumulowane pole pod F_A musi być nie większe.

Wymaganie na U: U' ≥ 0 i U'' ≤ 0 — monotoniczne i wklęsłe. Klasa: decydenci z **awersją do ryzyka.**

SSD jest znacznie **częstsza** niż FSD.

Relacja: FSD implikuje SSD, ale nie odwrotnie.

**Zastosowania w modelach wyboru:**

Selekcja portfeli — mogę wyeliminować zdominowane portfele bez pytania o U. Jeśli A SSD-dominuje B, to żaden risk-averse decydent nie wybierze B. Redukuję zbiór rozwiązań.

Ubezpieczenia — fair ubezpieczenie SSD-dominuje brak ubezpieczenia dla risk-averse. Mean-preserving spread — B = A + szum o zerowej wartości oczekiwanej → A SSD B.

Evaluacja inwestycji — A ma wyższy zwrot i mniejsze ryzyko niż B → A SSD B.

### Spodziewane pytania dodatkowe

**„Co to mean-preserving spread?"** → Dodaję losowy szum o średniej zero do rozkładu — zachowuję średnią, ale zwiększam rozproszenie. Dla risk-averse — to gorsze. Stąd rozkład bez szumu SSD-dominuje ten z szumem.

**„Czy FSD/SSD daje pełne uporządkowanie?"** → Nie — to porządek częściowy. Wiele par alternatyw jest nieporównywalnych. To nie jest ranking — to filtr eliminacyjny.

---

<!-- Na druku sprawdź: A4, 10pt, marginesy 2cm, każde pytanie zaczyna nową stronę -->
