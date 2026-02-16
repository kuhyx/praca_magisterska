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

