## PYTANIE 10: Zarządzanie pamięcią (SOI)

**Problemy i mechanizmy. Stronicowanie vs segmentacja.**

---

### Tło pojęciowe — słowniczek

**Pamięć operacyjna (RAM)** — szybka pamięć ulotna, z której procesor odczytuje i zapisuje dane. Ograniczona ilościowo (np. 8–64 GB). Zadanie OS: rozdzielić ją sprawiedliwie i bezpiecznie między procesy.

**Pamięć wirtualna (virtual memory)** — abstrakcja: każdy proces „widzi" własną, ciągłą przestrzeń adresową, niezależnie od fizycznego rozmieszczenia danych w RAM. OS + MMU (sprzęt) tłumaczą adresy wirtualne na fizyczne. Dzięki temu programy mogą używać więcej pamięci niż fizycznie dostępne (reszta na dysku = swap).

    Program widzi:    [0x0000 ... 0xFFFF]  ← wirtualne, ciągłe
    RAM fizyczny:     [ramka 5][ramka 12][ramka 3]  ← rozproszone

**MMU (Memory Management Unit)** — dedykowany układ sprzętowy (część procesora) odpowiedzialny za translację adresów wirtualnych na fizyczne. Każdy dostęp do pamięci przechodzi przez MMU — program podaje adres wirtualny, MMU sprawdza tablicę stron (lub TLB) i przekształca go na adres fizyczny.

    CPU: "chcę bajt pod adresem wirtualnym 0x1234"
      ↓
    MMU: sprawdza tablicę stron → strona 1 → ramka 7
      ↓
    Magistrala: odczyt z adresu fizycznego 0x7234

MMU sprawdza też uprawnienia (bity R/W/X) — jeśli proces próbuje pisać do strony read-only, MMU generuje wyjątek (page fault / segmentation fault). Bez MMU nie ma pamięci wirtualnej — każdy program musiałby zarządzać fizycznymi adresami ręcznie (tak było w MS-DOS).

---

**Fragmentacja (fragmentation)** — marnowanie pamięci z powodu sposobu alokacji.

**Fragmentacja zewnętrzna (external)** — wolna pamięć jest rozproszona w małych kawałkach między zajętymi. Suma wolnych kawałków wystarczy, ale żaden pojedynczy nie jest wystarczająco duży.

    [ZAJĘTE][wolne 2KB][ZAJĘTE][wolne 3KB][ZAJĘTE]
    Razem 5KB wolne, ale nie zmieści się blok 4KB!

**Fragmentacja wewnętrzna (internal)** — przydzielony blok jest większy niż potrzebny. Pozostała różnica jest zmarnowana. Np. strona 4KB przydzielona dla 100 bajtów danych — 3996 bajtów zmarnowane.

**Ochrona pamięci (memory protection)** — mechanizm uniemożliwiający procesowi dostęp do pamięci innego procesu. Realizowana przez tablice stron (bity R/W/X) i MMU. Bez ochrony: crash jednego procesu mógłby zepsuć cały system.

**Dlaczego crash bez ochrony zabija cały system?** Bez ochrony pamięci wszystkie procesy widzą tę samą, płaską przestrzeń fizyczną. Wadliwy program może nadpisać dowolny adres — w tym:
- **Kod jądra OS** — nadpisanie instrukcji jądra = kernel crash = restart.
- **Dane innego procesu** — np. baza danych traci spójność.
- **Tablice systemowe** — np. tablica przerwań (IDT) — procesor nie wie, co robić przy przerwaniu → zawieszenie.

    Bez ochrony (MS-DOS, lata 80.):
    [jądro OS | program A | program B | wolne]
    0x0000     0x1000      0x5000      0x8000

    Program A ma bug → pisze pod adres 0x0500 (pamięć jądra!)
    → nadpisuje tablicę przerwań → system się zawiesza

    Z ochroną (Windows/Linux):
    Program A widzi:  [0x0000 ... 0xFFFF]  ← wirtualne
    Program B widzi:  [0x0000 ... 0xFFFF]  ← wirtualne, ALE inne ramki!
    Program A pisze pod 0x0500 → trafia do SWOJEJ ramki, nie jądra.
    Próba dostępu do cudzej pamięci → MMU: Segmentation Fault → OS zabija TYLKO ten proces.

**Bity R/W/X (Read / Write / eXecute)** — flagi ochrony w każdym wpisie tablicy stron, określające co wolno robić ze stroną:
- **R (Read)** — można czytać dane ze strony.
- **W (Write)** — można zapisywać dane na stronę. Bez W próba zapisu → page fault.
- **X (eXecute)** — procesor może wykonywać kod ze strony. Bez X próba skoku → fault.

Przykłady zastosowań:

    Rodzaj pamięci    R  W  X   Wyjaśnienie
    ──────────────────────────────────────────
    Kod programu      ✓  ✗  ✓   czytaj i wykonuj, nie modyfikuj
    Dane globalne     ✓  ✓  ✗   czytaj/pisz, nie wykonuj (DEP)
    Stos              ✓  ✓  ✗   zmienne lokalne, brak wykonania
    Stałe (const)     ✓  ✗  ✗   tylko do odczytu
    Guard page        ✗  ✗  ✗   brak dostępu → wykrywanie przepełnienia stosu

**DEP (Data Execution Prevention)** — mechanizm bezpieczeństwa: strony z danymi nie mają bitu X. Atakujący wstrzykuje kod do bufora (dane), ale procesor odmawia wykonania → ochrona przed atakami buffer overflow.

**Relokacja (relocation)** — program musi działać pod różnymi adresami fizycznymi (nie wie z góry, gdzie zostanie załadowany). Pamięć wirtualna rozwiązuje to automatycznie — program zawsze widzi te same adresy wirtualne.

**Dlaczego program nie wie, pod jakim adresem fizycznym będzie?** Przy uruchamianiu OS decyduje, które ramki RAM są wolne. To zależy od tego, co innego aktualnie działa.

    Scenariusz 1: uruchom program A jako jedyny
    RAM: [jądro][....A....][wolne...........]
    Program A fizycznie pod adresem 0x1000

    Scenariusz 2: uruchom A gdy B i C już działają
    RAM: [jądro][..B..][..C..][..A..][wolne]
    Program A fizycznie pod adresem 0x5000

    Problem: program ma instrukcję "skocz do adresu 0x2000" (swojej funkcji)
    W scenariuszu 1: 0x2000 to poprawne miejsce w A
    W scenariuszu 2: 0x2000 to fragment B → CRASH!

    Rozwiązanie — pamięć wirtualna:
    A ZAWSZE widzi siebie pod adresami 0x0000–0xFFFF (wirtualne)
    MMU tłumaczy: wirtualne 0x2000 → fizyczne 0x6000 (scenariusz 2)
    Program nie musi wiedzieć, gdzie fizycznie leży — abstrahuje od tego.

**COW (Copy-on-Write)** — optymalizacja: przy fork() (tworzenie procesu) dziecko współdzieli strony z rodzicem. Kopia fizyczna następuje dopiero gdy któryś pisze. Oszczędność: jeśli procesy tylko czytają, nie kopiujemy nic.

    fork()
    Rodzic: strona 7 → ramka 42 [R-only]  ─┐
                                             ├─ ta sama ramka fizyczna!
    Dziecko: strona 7 → ramka 42 [R-only] ─┘

    Dziecko pisze do strony 7:
    → page fault (ochrona zapisu) → OS kopiuje ramkę 42 → nowa ramka 58
    Rodzic: strona 7 → ramka 42 [R/W]
    Dziecko: strona 7 → ramka 58 [R/W]   ← kopia powstała dopiero teraz

Zysk w praktyce: `fork()` + `exec()` (typowy wzorzec Unix) — dziecko natychmiast zastępuje obraz procesu, więc żadna strona nie jest kopiowana. Bez COW: fork() kopiowałby setki MB niepotrzebnie.

---

**Współdzielenie pamięci (memory sharing)** — mechanizm pozwalający wielu procesom korzystać z tych samych ramek fizycznych. To jeden z kluczowych problemów zarządzania pamięcią — bez współdzielenia każdy proces musiałby mieć własną kopię wszystkiego, co drastycznie zwiększyłoby zużycie RAM.

**Formy współdzielenia:**

1. **Biblioteki współdzielone (shared libraries / .so / .dll)** — kod biblioteki (np. libc) jest ładowany do RAM raz i mapowany do przestrzeni adresowej wielu procesów. Każdy proces widzi tę samą ramkę fizyczną z kodem, ale pod własnym adresem wirtualnym.

        RAM fizyczny:
        [ramka 100: kod libc] ← załadowana RAZ

        Proces A: strona 50 → ramka 100 (read-only)
        Proces B: strona 80 → ramka 100 (read-only)
        Proces C: strona 30 → ramka 100 (read-only)

        Bez współdzielenia: 3 kopie × 2 MB = 6 MB
        Ze współdzieleniem: 1 kopia × 2 MB = 2 MB
        Przy 100 procesach: 200 MB vs 2 MB — oszczędność 99%!

    Sekcje biblioteki: TEXT (kod, read-only) — współdzielona; DATA (zmienne globalne) — każdy proces ma własną kopię (COW).

2. **COW (Copy-on-Write)** — opisany wyżej. Współdzielenie stron po fork() do momentu zapisu.

3. **Shared Memory (pamięć współdzielona IPC)** — region RAM jawnie współdzielony między procesami (np. `shmget()`/`shmat()` w POSIX, `mmap()` z `MAP_SHARED`). Najszybszy mechanizm IPC — brak kopiowania, bezpośredni dostęp. Wymaga synchronizacji (semafory, muteksy).

        Proces A                 Proces B
        strona 20 ──┐       ┌── strona 45
                     ↓       ↓
                  [ramka 200: wspólne dane]
        A pisze „hello" → B natychmiast widzi „hello"

4. **Memory-mapped files (pliki mapowane w pamięci)** — plik z dysku mapowany do przestrzeni adresowej procesu (`mmap()`). Wiele procesów może mapować ten sam plik — zmiany jednego są widoczne dla innych.

**Realizacja sprzętowa:** Współdzielenie działa dzięki tablicom stron — wiele procesów ma wpisy wskazujące na tę samą ramkę fizyczną. Bity ochrony (R/W/X) kontrolują, kto może czytać, pisać, wykonywać.

    Tablica stron procesu A:  strona 50 → ramka 100 [R--]
    Tablica stron procesu B:  strona 80 → ramka 100 [R--]
    Tablica stron procesu C:  strona 30 → ramka 100 [R--]
    → 3 procesy, 1 ramka fizyczna, różne adresy wirtualne

**Dlaczego to ważne dla zarządzania pamięcią?** Typowy system Linux ma dziesiątki procesów korzystających z tych samych bibliotek (libc, libpthread, libm…). Bez współdzielenia zapotrzebowanie na RAM byłoby wielokrotnie większe. Współdzielenie to kluczowa optymalizacja pozwalająca uruchamiać wiele procesów jednocześnie.

**Czy ochrona pamięci i współdzielenie nie są sprzeczne?** Nie — one współpracują dzięki tablicom stron. Ochrona to **domyślna odmowa** — tablica stron procesu A po prostu nie zawiera wpisów wskazujących na ramki procesu B, więc A nie może nawet zaadresować pamięci B (MMU blokuje). Współdzielenie to **jawny, kontrolowany wyjątek** — OS celowo mapuje tę samą ramkę fizyczną w tablicach stron obu procesów, ustawiając bity ochrony (R/W/X) niezależnie dla każdego.

    Bez współdzielenia (domyślnie — ochrona):
    Proces A: strona 5 → ramka 10 [R/W]
    Proces B: strona 5 → ramka 77 [R/W]   ← inna ramka, A nie widzi B

    Ze współdzieleniem (jawna decyzja OS):
    Proces A: strona 5 → ramka 10 [R]     ← ta sama ramka!
    Proces B: strona 8 → ramka 10 [R]     ← ale może read-only

Kluczowy punkt: tylko jądro OS może modyfikować tablice stron. Proces nie może sam sobie dodać mapowania do cudzej ramki. Dlatego:
- **libc**: OS mapuje tę samą ramkę z kodem jako read-only do 50 procesów. Bezpieczne, bo nikt nie pisze.
- **shmget/mmap**: proces prosi OS „daj mi i procesowi B wspólny region." OS tworzy mapowanie. To opt-in, nie luka.
- **COW**: OS mapuje strony rodzica do dziecka jako read-only. Przy zapisie → page fault → OS kopiuje → dopiero wtedy zapis.

Analogia: blok mieszkalny z ochroną — każde mieszkanie ma własny zamek (ochrona), ale dwóch lokatorów może wybrać współdzielenie sali konferencyjnej (współdzielenie) — administrator budynku (OS) daje im obu klucz. To nie znaczy, że mogą wchodzić do swoich mieszkań nawzajem.

---

**Strona (page)** — jednostka pamięci wirtualnej o stałym rozmiarze (zwykle 4 KB). Pamięć wirtualna jest podzielona na strony.

**Ramka (frame)** — jednostka pamięci fizycznej o tym samym rozmiarze co strona. Strona wirtualna mapowana jest na ramkę fizyczną.

**Tablica stron (page table)** — struktura danych tłumacząca numer strony → numer ramki. Każdy proces ma własną tablicę stron.

    Adres wirtualny = [numer strony | offset]
    Tablica stron:    strona 5 → ramka 12
    Adres fizyczny  = [12 | offset]

**Wpis tablicy stron (page table entry, PTE)** — każdy wpis opisuje jedną stronę i zawiera:
- **Numer ramki (frame number)** — wskazuje, w której ramce fizycznej leży ta strona.
- **Bit Present (P)** — czy strona jest aktualnie w RAM? P=1 → w RAM, P=0 → na dysku (swap) lub nieprzydzielona. Dostęp do strony z P=0 → page fault → OS ładuje stronę z dysku.
- **Bit Dirty (D)** — czy strona była modyfikowana od załadowania? D=1 → przy wymianie trzeba zapisać ją na dysk (bo dane się zmieniły). D=0 → można po prostu wyrzucić (kopia na dysku jest aktualna). Oszczędza czas I/O.
- **Bit R (Read)** — pozwala na odczyt strony.
- **Bit W (Write)** — pozwala na zapis. W=0 → strona read-only (próba zapisu = fault). Używane przez COW i ochronę kodu.
- **Bit X (eXecute)** — pozwala na wykonanie kodu ze strony (NX bit). X=0 → strona z danymi, próba wykonania = fault (DEP).
- **Bit User/Supervisor (U/S)** — U=1 → dostępna dla kodu użytkownika; U=0 → tylko jądro OS.

Przykład wpisu:

    Strona 5: [ramka=12 | P=1 | D=0 | R=1 | W=0 | X=1 | U=1]
    → strona w RAM, nienaruszona, read+execute, dostępna dla usera
    → to wygląda jak segment TEXT (kod programu)

    Strona 8: [ramka=-- | P=0 | D=- | R=- | W=- | X=- | U=-]
    → strona NIE w RAM (P=0), dostęp = page fault

**Wielopoziomowe tablice stron** — oszczędność pamięci. Zamiast jednej ogromnej tablicy, drzewo tablic. Nieużywane gałęzie nie istnieją.

**Problem jednopoziomowej tablicy:** W 32-bitowym systemie z 4KB stronami: 2³² / 4096 = 1 048 576 wpisów × 4 bajty = **4 MB tablicy per proces**. Przy 100 procesach = 400 MB samych tablic! A większość stron jest nieużywana (typowy proces używa ułamek przestrzeni adresowej).

**Rozwiązanie — drzewo tablic:** Dzielimy tablicę na poziomy. Tylko gałęzie odpowiadające faktycznie używanym stronom muszą istnieć w pamięci.

**32-bit: 2 poziomy (x86)**

    Adres wirtualny (32 bity):
    [10 bitów: nr w Page Directory | 10 bitów: nr w Page Table | 12 bitów: offset]

    Page Directory (1024 wpisy) → każdy wskazuje na Page Table (1024 wpisy) → ramka

    Jeśli proces używa tylko 4 MB pamięci (1024 stron):
    - 1 Page Directory = 4 KB
    - 1 Page Table = 4 KB
    - Razem: 8 KB zamiast 4 MB! (oszczędność 500x)
    Pozostałe 1023 wpisy Page Directory = NULL (Page Table nie istnieje)

**64-bit: 4 poziomy (x86-64)** — każdy poziom to tablica 512 wpisów:

    PML4 → PDPT → PD → PT → ramka fizyczna

- **PML4 (Page Map Level 4)** — najwyższy poziom, 512 wpisów. Każdy wpis wskazuje na jedną tablicę PDPT. Pokrywa 512 × 512 GB = 256 TB przestrzeni.
- **PDPT (Page Directory Pointer Table)** — 512 wpisów, każdy wskazuje na PD. Jeden wpis PDPT pokrywa 1 GB.
- **PD (Page Directory)** — 512 wpisów, każdy wskazuje na PT. Jeden wpis PD pokrywa 2 MB.
- **PT (Page Table)** — 512 wpisów, każdy wskazuje na ramkę fizyczną 4 KB.

Schemat:

    Adres wirtualny (48 bitów używanych z 64):
    [9b PML4 | 9b PDPT | 9b PD | 9b PT | 12b offset]

    Translacja: CPU bierze adres wirtualny i „schodzi" po 4 tablicach:
    rejestr CR3 → PML4[idx1] → PDPT[idx2] → PD[idx3] → PT[idx4] → ramka

**Dlaczego nieużywane gałęzie nie istnieją?** W drzewie wielopoziomowym tablicę niższego poziomu tworzymy TYLKO gdy proces faktycznie odwołuje się do adresów z tego zakresu. Jeśli wpis w PML4 ma P=0 (present=0), to odpowiadające mu PDPT, PD i PT w ogóle nie zajmują pamięci.

    Typowy proces 64-bit (100 MB kodu + danych):
    - 1 PML4                          = 4 KB
    - 1-2 PDPT (max 2 GB zakresy)     = 4-8 KB
    - ~50 PD                          = ~200 KB
    - ~25600 PT (100 MB / 4 KB)       = ~100 KB
    Razem: ~310 KB zamiast pełnych tablic pokrywających 256 TB

    Puste regiony (np. 99.99% przestrzeni 256 TB):
    PML4[5] = NULL → żadna PDPT, PD ani PT nie istnieje
    → 0 bajtów kosztu za nieużywany region 512 GB!

---

**Cache (pamięć podręczna)** — mała, bardzo szybka pamięć przechowująca kopie często używanych danych z wolniejszej pamięci. Zasada: jeśli dane są w cache (hit), odczyt jest szybki; jeśli nie (miss), trzeba sięgnąć do wolniejszej pamięci i skopiować dane do cache na przyszłość.

**Hierarchia pamięci i czasy dostępu:**

    Poziom         Rozmiar     Czas dostępu    Przykład
    ──────────────────────────────────────────────────────
    Rejestry CPU   ~1 KB       ~0.3 ns         RAX, RBX
    L1 cache       32-64 KB    ~1 ns           per rdzeń
    L2 cache       256 KB-1MB  ~3-5 ns         per rdzeń
    L3 cache       8-64 MB     ~10-20 ns       współdzielony
    RAM            8-64 GB     ~50-100 ns      DDR4/DDR5
    SSD            256GB-4TB   ~50-100 μs      NVMe
    HDD            1-16 TB     ~5-10 ms        mechaniczny

    Różnica RAM vs HDD: ~100 000x wolniej!
    Dlatego swap (pamięć wirtualna na dysku) jest ostatecznością.

**Cache translacji adresów = TLB.** Translacja adresu wirtualnego wymaga przejścia 4 poziomów tablic stron (4 odczyty RAM × 100 ns = 400 ns). TLB przechowuje wynik translacji (strona→ramka) — trafienie w TLB skraca to do ~1 ns. Bez TLB każdy dostęp do pamięci byłby 4-5x wolniejszy.

**TLB (Translation Lookaside Buffer)** — sprzętowy cache translacji adresów. Przechowuje ostatnio używane mapowania strona→ramka. Trafienie w TLB: ~1 ns; pudło: ~10-100 ns (trzeba chodzić po tablicy stron). Hit rate: typowo >99%.

    Dostęp do pamięci wirtualnej adres 0x12345:
    1. CPU pyta TLB: "masz stronę 0x12?"
       → TLB hit: od razu ramka 42, koszt ~1 ns
       → TLB miss: przejdź PML4→PDPT→PD→PT, koszt ~400 ns
    2. Wynik miss zapisywany w TLB na przyszłość

    TLB ma ~64-1024 wpisów (mały, ale wystarczający)
    99% trafień × 1 ns + 1% pudło × 400 ns = śr. ~5 ns
    Bez TLB: zawsze 400 ns = 80x wolniej!

**Page fault (brak strony)** — wyjątek sprzętowy gdy strona nie jest aktualnie w RAM. OS ładuje ją z dysku (swap). Nie jest „błędem" programisty — to normalna część zarządzania pamięcią wirtualną.

    Koszt: ~1-10 ms (bo dysk!) vs ~100 ns dla dostępu do RAM
    Różnica ~10 000x — dlatego minimalizacja page faults jest krytyczna

---

**Algorytmy wymiany stron (page replacement):**
- **FIFO** — usuń najstarszą stronę (tę, która weszła do RAM jako pierwsza). Prosty, ale podatny na anomalię Bélády'ego.
- **LRU (Least Recently Used)** — usuń najdawniej używaną. Dobry, ale kosztowna implementacja (trzeba śledzić czas użycia każdej strony).
- **Clock (Second Chance)** — przybliżenie LRU. Wskazówka zegara + bit odwołania. Jeśli bit=1, daj drugą szansę (zeruj bit i idź dalej). Jeśli bit=0, wymień.
- **Optimal** — usuń stronę, która nie będzie potrzebna najdłużej. Idealny, ale nierealizowalny (wymaga znajomości przyszłości). Benchmark do porównań.

**Anomalia Bélády'ego** — paradoks specyficzny dla FIFO: zwiększenie liczby ramek (więcej pamięci!) może ZWIĘKSZYĆ liczbę page faults. Jest to kontraintuicyjne — więcej pamięci powinno pomóc, ale FIFO nie bierze pod uwagę tego, jak często strona jest używana.

Klasyczny przykład (ciąg odwołań: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5):

    3 ramki → 9 page faults:
    Odw.: 1  2  3  4  1  2  5  1  2  3  4  5
    R1:   1  1  1  4  4  4  5  5  5  5  5  5
    R2:   -  2  2  2  1  1  1  1  1  3  3  3
    R3:   -  -  3  3  3  2  2  2  2  2  4  4
    Fault: F  F  F  F  F  F  F  -  -  F  F  -  = 9 faults

    4 ramki → 10 page faults (WIĘCEJ!):
    Odw.: 1  2  3  4  1  2  5  1  2  3  4  5
    R1:   1  1  1  1  1  1  5  5  5  5  4  4
    R2:   -  2  2  2  2  2  2  1  1  1  1  5
    R3:   -  -  3  3  3  3  3  3  2  2  2  2
    R4:   -  -  -  4  4  4  4  4  4  3  3  3
    Fault: F  F  F  F  -  -  F  F  F  F  F  F  = 10 faults

    3 ramki: 9 faults
    4 ramki: 10 faults ← ANOMALIA! więcej pamięci = gorzej!

**Dlaczego FIFO to powoduje?** FIFO wybiera ofiarę wyłącznie na podstawie czasu wejścia do RAM, ignorując czy strona jest wciąż potrzebna. Dodanie ramki zmienia kolejność wyrzucania tak nieszczęśliwie, że strony potrzebne w przyszłości są wyrzucane wcześniej niż przy mniejszej liczbie ramek.

**LRU i Optimal NIE mają tej anomalii** — należą do tzw. algorytmów stosowych (stack algorithms): zbiór stron w pamięci przy n ramkach jest ZAWSZE podzbiorem stron przy n+1 ramkach. FIFO nie ma tej własności.

---

**Segment logiczny (logical segment)** — fragment programu o spójnym, logicznym znaczeniu. Programista (i kompilator) myśli o programie jako o kilku częściach, z których każda ma inną rolę i inne reguły dostępu.

**Typowe segmenty programu:**

- **Segment kodu (TEXT / Code Segment)** — skompilowane instrukcje maszynowe programu. Read-only + Execute. Współdzielony między procesami uruchamiającymi ten sam program (po co trzymać 10 kopii tego samego kodu?).

        int main() { return add(2, 3); }  // ← po kompilacji to segment TEXT
        Rozmiar: zależy od programu (np. 50 KB prosty, 100+ MB gra)
        Ochrona: R-X (czytaj + wykonuj, NIE pisz)

- **Segment danych (DATA Segment)** — zainicjalizowane zmienne globalne i statyczne. Read + Write.

        int counter = 42;          // ← DATA (zainicjalizowana)
        static char name[] = "Jan"; // ← DATA
        Ochrona: RW- (czytaj + pisz, NIE wykonuj)

- **Segment BSS (Block Started by Symbol)** — niezainicjalizowane zmienne globalne. OS zeruje ten segment przy starcie. Nie zajmuje miejsca w pliku wykonywalnym (wiadomo, że będą same zera).

        int table[10000];  // ← BSS, 40 KB, ale w pliku .exe: 0 bajtów
        // OS alokuje 40 KB i zeruje przy starcie

- **Segment stosu (Stack Segment)** — zmienne lokalne, adresy powrotu z funkcji, parametry. Rośnie w dół (od wysokich adresów). Każdy wątek ma własny stos.

        void foo() {
            int x = 5;    // ← na stosie
            int arr[100];  // ← na stosie (400 bajtów)
        }  // ← po powrocie z funkcji: zwolnione automatycznie
        Typowy rozmiar: 1-8 MB per wątek

- **Segment sterty (Heap Segment)** — pamięć alokowana dynamicznie (malloc/new). Rośnie w górę. Programista zarządza ręcznie (lub garbage collector).

        int* p = malloc(1000);  // ← na stercie
        free(p);                // ← ręczne zwolnienie

Układ w pamięci:

    Wysoki adres
    ┌──────────┐
    │  STOS ↓  │ zmienne lokalne, rośnie w dół
    │    ...   │
    │  HEAP ↑  │ malloc/new, rośnie w górę
    │   BSS    │ niezainicjalizowane globalne (zerowane)
    │   DATA   │ zainicjalizowane globalne
    │   TEXT   │ kod maszynowy (read-only)
    └──────────┘
    Niski adres

---

**Segmentacja (segmentation)** — model zarządzania pamięcią, w którym przestrzeń adresowa procesu jest podzielona na segmenty logiczne o **zmiennych** rozmiarach. Każdy segment odpowiada jednej logicznej części programu (kod, dane, stos).

**Adresowanie w segmentacji:** Adres = (numer segmentu, offset). CPU szuka wpisu w **tablicy segmentów** i sprawdza bazę + limit.

**Baza (base)** — adres fizyczny początku segmentu w RAM. Mówi: „ten segment zaczyna się pod adresem fizycznym X".

**Limit** — maksymalny offset (rozmiar segmentu). Mówi: „ten segment ma Y bajtów". Jeśli offset ≥ limit → wyjątek (Segmentation Fault) → próba wyjścia poza segment.

    Tablica segmentów:
    Segment   Baza      Limit     Ochrona
    ──────────────────────────────────────
    0 (TEXT)  0x4000    8 KB      R-X
    1 (DATA)  0x6000    4 KB      RW-
    2 (STOS)  0xA000    2 KB      RW-

    Adres logiczny: (segment=1, offset=500)
    Sprawdź: 500 < limit(4096)? TAK
    Adres fizyczny: baza(0x6000) + offset(500) = 0x61F4

    Adres logiczny: (segment=1, offset=5000)
    Sprawdź: 5000 < limit(4096)? NIE → Segmentation Fault!

    Cecha              Stronicowanie         Segmentacja
    ─────────────────────────────────────────────────────
    Jednostka          strona (stały, 4KB)   segment (zmienny)
    Fragmentacja       wewnętrzna            zewnętrzna
    Widok programisty  niewidoczne           logiczne (kod, dane)
    Adresowanie        (strona, offset)      (segment, offset)
    Co definiuje rozmiar  sprzęt (4KB)       program (dowolny)
    Współczesne OS     dominuje (x86-64)     prawie zniknęła

**Dlaczego stronicowanie wygrało?** Stałe rozmiary stron = brak fragmentacji zewnętrznej, prostsze zarządzanie, łatwiejsze w sprzęcie. Zmienne rozmiary segmentów powodują fragmentację zewnętrzną (trzeba kompaktować pamięć, co jest kosztowne). Intel porzucił pełną segmentację w x86-64 (flat segments + paging).

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

---

### 🎮 Mostek do pracy magisterskiej — pamięć w silnikach gier

> Praca magisterska porównuje Unity (C#, Garbage Collector) z Unreal (C++, manual memory management). Zarządzanie pamięcią to **centralny temat** różnicy wydajnościowej.

![GC vs Manual Memory — porównanie Unity i Unreal](img/q10_gc_vs_manual_memory.png)

#### Garbage Collector w Unity — jak to działa i dlaczego boli

**Boehm GC** (Unity < 2021) / **Incremental GC** (Unity 2019+):
1. Allokacja: `new Bullet()` → managed heap
2. Gdy heap pełny → **Stop-the-world GC pause** (mark & sweep)
3. Wszystkie wątki **zamrożone** na czas GC → frame spike!

    Frame time [ms]:
    Normal:  █████████ 8ms
    GC hit:  █████████████████████████████ 28ms  ← SPIKE!
    Target:  ████████████████ 16.67ms (60 FPS)

**Rozwiązanie #1 — Object Pooling:**

![Object Pooling — eliminacja alokacji w runtime](img/q10_object_pooling.png)

**Rozwiązanie #2 — Unity DOTS (ECS + Burst):**
- NativeArray<T> → **unmanaged memory** (nie skanowana przez GC)
- Burst Compiler → kompilacja C# do natywnego SIMD
- Efekt: wydajność zbliżona do C++

#### Unreal Engine — pamięć w C++

| Mechanizm | Opis | Analogia z pytania |
|-----------|------|---------------------|
| `TSharedPtr<T>` | Reference counting (jak GC, ale deterministyczny) | Smart pointer = automatyczna relokacja |
| `TUniquePtr<T>` | Exclusive ownership, zero overhead | Segment z private access |
| `FMemory::Malloc` | Custom allocator z pool per size class | Jak system buddy allocation |
| UObject GC | Reflection-based GC **tylko** dla UObject | Mark-sweep, ale kontrolowany timing |

#### Tabela porównawcza z pracy magisterskiej

| Metryka (Nsight) | Unity (bez pool) | Unity (z pool) | Unreal |
|-------------------|-------------------|----------------|--------|
| Alloc/frame | ~800 | ~0 | ~5 (deterministic) |
| GC pause max | 25ms | 3ms | 0ms |
| Heap fragmentation | Wysoka | Niska | Brak (custom alloc) |
| Frame time sigma | 4.2ms | 0.8ms | 0.3ms |

#### Mnemonik — „GAP" = GC → Alloc → Pool

- **G**arbage Collector → problem (spikes)
- **A**llocation → przyczyna (new w Update)
- **P**ooling → rozwiązanie (pre-alloc + reuse)

Kiedy na obronie padnie pytanie o pamięć → powiedz:
*„W mojej pracy kluczowa różnica to: Unity managed heap z GC (Boehm/Incremental) vs Unreal custom allocators + smart pointers. Object Pooling w Unity niweluje tę różnicę — mierzę to Nsight-em."*

---

### Etymologia

**Stronicowanie (Paging)** — pamięć dzielona na „strony" jak w książce. **TLB** — Translation Lookaside Buffer; „lookaside" = sprawdź z boku (cache) zanim sięgniesz do tablicy. **Segmentacja** — łac. „segmentum" = odcięty kawałek. **COW** — Copy-on-Write: kopiuj dopiero przy modyfikacji. **LRU** — Least Recently Used. **FIFO** — First In, First Out. **Page fault** — „fault" to wyjątek sprzętowy, nie błąd programisty.

### Jak zapamiętać

- **Stronicowanie = szuflady jednakowej wielkości** (proste, mała fragmentacja wewnętrzna)
- **Segmentacja = pudełka różnej wielkości** (logiczne, ale fragmentacja zewnętrzna)
- Współcześnie: **stronicowanie wygrało** — segmentacja prawie zniknęła (x86-64 = flat segments + paging)

**Mnemonik na 5 segmentów — „Tadek Będzie Dobry Student Harcerz":**

    T — TEXT   (kod programu, R-X)
    B — BSS    (niezainicjalizowane globalne, zerowane)
    D — DATA   (zainicjalizowane globalne, RW-)
    S — STOS   (zmienne lokalne, rośnie ↓)
    H — HEAP   (malloc/new, rośnie ↑)

    Kolejność w pamięci (od niskich adresów):
    TEXT → DATA → BSS → HEAP ↑ ... ↓ STOS

    Alternatywny mnemonik — od dołu pamięci w górę:
    „Tekst Daje Bezpieczeństwo, Hasła Stoją"
    TEXT → DATA → BSS → HEAP → STOS

**Mnemonik na fragmentację — „FOWZE":**

    Fragmentacja:
      O (stały rOzmiar) → W (Wewnętrzna)  — stronicowanie
      Z (Zmienny rozmiar) → E (Zewnętrzna) — segmentacja

    Skojarzenie wizualne:
    Stronicowanie: szuflada 4KB, wkładasz 100B → reszta zmarnowana WEWNĄTRZ szuflady
    Segmentacja:   pudełka różnej wielkości → dziury ZEWNĄTRZ między pudełkami

    Krótka reguła: „Stały → Wewnętrzna, Zmienny → Zewnętrzna"

**Jak zapamiętać, żeby W OGÓLE wspomnieć o fragmentacji w odpowiedzi?**

Fragmentacja to PIERWSZY problem zarządzania pamięcią — wymień go jako punkt nr 1 listy problemów. Mnemonik na 5 problemów pamięci — **„FORWOW"**:

    1. F — Fragmentacja (zewnętrzna + wewnętrzna)
    2. O — Ochrona (procesy nie widzą nawzajem pamięci)
    3. R — Relokacja (program pod różnymi adresami)
    4. W — Współdzielenie (biblioteki, COW)
    5. O — Ograniczona pamięć (więcej procesów niż RAM)
    (W — Wydajność — TLB, cache, minimalizacja page faults)

    Kiedy mówisz o stronicowaniu → powiedz: „eliminuje fragmentację ZEWNĘTRZNĄ,
    ale wprowadza WEWNĘTRZNĄ" (to pokazuje, że pamiętasz!)
    Kiedy mówisz o segmentacji → powiedz: „brak wewnętrznej,
    ale fragmentacja ZEWNĘTRZNA — dlatego przegrała"

