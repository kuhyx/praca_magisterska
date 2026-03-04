## PYTANIE 9: Procesy i wątki (SOI)

**Budowa, szybkość, zastosowanie. Problemy komunikacji i synchronizacji.**

---

### Tło pojęciowe — słowniczek

**Proces (process)** — program w trakcie wykonania. Każdy proces ma własną, izolowaną przestrzeń adresową. System operacyjny zarządza procesami — tworzy, planuje (scheduling), kończy. Np. przeglądarka i edytor to osobne procesy.

**Wątek (thread)** — lekka jednostka wykonania wewnątrz procesu. Wątki jednego procesu współdzielą pamięć (kod, dane, heap), ale mają własny stos i rejestry CPU. Tworzenie wątku jest ~100× szybsze niż procesu.

![Proces vs Wątek — porównanie](img/q9_process_vs_thread.png)

---

**Przestrzeń adresowa (address space)** — zakres adresów pamięci wirtualnej dostępnych procesowi. Każdy proces widzi swoją „prywatną" pamięć, nawet jeśli fizycznie jest mapowana gdzieś indziej.

**Segmenty pamięci procesu:**
- **TEXT** — kod maszynowy (read-only)
- **DATA** — zainicjalizowane zmienne globalne/statyczne
- **BSS** — niezainicjalizowane zmienne globalne (zerowane)
- **HEAP** — pamięć alokowana dynamicznie (malloc/new), rośnie w górę
- **STACK** — zmienne lokalne, adresy powrotu, rośnie w dół

![Segmenty pamięci procesu](img/q9_memory_layout.png)

**PCB (Process Control Block)** — struktura danych w jądrze OS opisująca proces: PID, stan, rejestry CPU, tablice stron, otwarte pliki, priorytety. Przełączenie kontekstu = zapisanie PCB starego procesu i wczytanie nowego.

![PCB — Process Control Block](img/q9_pcb_structure.png)

**PID (Process ID)** — unikalny identyfikator procesu w systemie. Np. `PID 1` = init/systemd w Linux.

**TID (Thread ID)** — unikalny identyfikator wątku.

**Stany procesu:** NEW (tworzony) → READY (gotowy, czeka na CPU) ↔ RUNNING (wykonywany) → BLOCKED (czeka na I/O), TERMINATED (zakończony). Scheduler decyduje, który READY staje się RUNNING.

![Stany procesu — diagram przejść](img/q9_process_states.png)

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

![Wyścig — race condition](img/q9_race_condition.png)

**Sekcja krytyczna (critical section)** — fragment kodu, który może być wykonywany przez najwyżej jeden wątek naraz. Chroni współdzielone zasoby przed race condition.

**Zakleszczenie (deadlock)** — sytuacja, w której dwa lub więcej wątków czekają na siebie nawzajem i żaden nie może kontynuować. Jak dwa samochody na skrzyżowaniu — oba czekają, nikt nie jedzie.

![Zakleszczenie — deadlock](img/q9_deadlock_scenario.png)

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

![Semafor — koncepcja](img/q9_semaphore_concept.png)

**Monitor** — wysokopoziomowy mechanizm synchronizacji. Obiekt z mutexem wbudowanym — tylko jeden wątek może wykonywać metody monitora. Java: `synchronized`.

**Condition Variable** — pozwala wątkowi czekać (wait) na spełnienie warunku i być obudzonym (signal/notify) przez inny wątek. Używane z mutexem.

**Spinlock** — zamek, w którym wątek aktywnie czeka w pętli (busy-wait) zamiast zasypiać. Szybki dla bardzo krótkich sekcji krytycznych (~ns), marnotrawny dla dłuższych.

**Read-Write Lock** — pozwala wielu czytelnikom jednocześnie LUB jednemu pisarzowi. Optymalizacja dla scenariuszy z dużo odczytów i rzadkimi zapisami.

**Barrier** — punkt synchronizacji: wszystkie wątki muszą dotrzeć do bariery, zanim którykolwiek może kontynuować. Użyteczna w obliczeniach równoległych (np. po każdej iteracji).

---

### Budowa procesu

Proces = program w trakcie wykonania + cały jego kontekst. Składa się z **3 filarów**: pamięć, PCB, stany.

**Filar 1 — Pamięć (oddzielna przestrzeń adresowa):**

Każdy proces dostaje własną, izolowaną przestrzeń adresową. Inne procesy NIE widzą tej pamięci. Składa się z 5 segmentów (od niskich do wysokich adresów): TEXT → DATA → BSS → HEAP → STACK.

![Segmenty pamięci procesu — szczegóły](img/q9_memory_layout.png)

Konkretny przykład — mapowanie kodu C na segmenty pamięci:

![Mapowanie kodu C na segmenty pamięci](img/q9_memory_c_annotated.png)

**Filar 2 — PCB (Process Control Block):**

PCB to „dowód osobisty" procesu w jądrze OS. Zawiera WSZYSTKO co OS musi wiedzieć: PID, stan, rejestry CPU, tablice stron, otwarte pliki, priorytety, statystyki.

![PCB — struktura z konkretnymi wartościami](img/q9_pcb_detailed.png)

Przełączenie kontekstu = zapisanie PCB starego procesu → wczytanie PCB nowego.

**Filar 3 — Stany procesu:**

![Stany procesu — diagram przejść z opisami](img/q9_process_states_labeled.png)

Scheduler decyduje, który READY staje się RUNNING.

> **Mnemonik BUDOWY PROCESU — „3 filary: MPS":**
> **M**ieszkanie, **P**aszport, **S**tatus = **M**emory (5 segmentów), **P**CB (dowód), **S**tany (5 stanów).
>
> Segmenty od dołu — **„TDBHS"**: **T**ata **D**aje **B**abci **H**erbatę ze **S**mietanką = TEXT → DATA → BSS → HEAP → STACK.
>
> Stany — **„NRRBT"**: **N**igdy **R**ano **R**ybki **B**iegać nie **T**rafią = NEW → READY → RUNNING → BLOCKED → TERMINATED.
>
> PCB = paszport procesu — bez niego OS nie wie kim jest proces.

### Budowa wątku

Wątek = lekka jednostka wykonania WEWNĄTRZ procesu.

Kluczowa idea: wątek to NIE osobny byt — to dodatkowa „ścieżka wykonania" w istniejącym procesie. Proces z 3 wątkami ma 1 przestrzeń adresową, ale 3 niezależne ciągi instrukcji.

![Wątki wewnątrz procesu — współdzielone vs prywatne](img/q9_thread_shared_private.png)

**Co WSPÓŁDZIELONE**: TEXT, DATA, BSS, HEAP, otwarte pliki, PID — wszystkie wątki widzą to samo.

**Co PRYWATNE** (każdy wątek ma własne):
- **Stos (stack)** — zmienne lokalne TEGO wątku, ramki wywołań
- **Rejestry CPU** — stan procesora TEGO wątku (EAX, EBX, ESP...)
- **Program Counter (PC)** — KTÓRA instrukcja jest teraz wykonywana
- **TID** — unikalny identyfikator wątku

Konkretny przykład — dlaczego współdzielenie to siła i zagrożenie:

    // Wątek 1 i Wątek 2 widzą TEN SAM obiekt:
    int shared_counter = 0;  // HEAP — współdzielone!

    // Wątek 1:                    // Wątek 2:
    shared_counter++;              shared_counter++;
    // Oba czytają 0, oba piszą 1 → wynik 1 zamiast 2!
    // → race condition (potrzebny mutex)

Kluczowa różnica od procesu: proces ma CAŁĄ przestrzeń adresową (jak całe mieszkanie), wątek to tylko kontekst wykonania — stos + rejestry + PC (jak osoba w mieszkaniu ze swoim telefonem i pozycją w książce).

> **Mnemonik BUDOWY WĄTKU — „Wspólna kuchnia, własny pokój":**
> Współdzielone = KOD + DANE + HEAP + PLIKI (kuchnia, salon, łazienka — wszyscy korzystają).
> Prywatne = STOS + REJESTRY + PC (twój pokój, twój telefon, twoja pozycja w książce).
>
> Skrót: **„SRP"** — **S**tos, **R**ejestry, **P**C = to co PRYWATNE.
> Skrót odwrotny: **„KDHP"** — **K**od, **D**ane, **H**eap, **P**liki = to co WSPÓŁDZIELONE.
>
> Test: „Czy dwa wątki widzą tę samą zmienną globalną?" → TAK (współdzielone DATA).
> „Czy dwa wątki widzą tę samą zmienną lokalną?" → NIE (osobne stosy).

### Szybkość — porównanie ilościowe

| Operacja          | Proces           | Wątek              | Dlaczego różnica?                    |
|-------------------|------------------|---------------------|--------------------------------------|
| Tworzenie         | ~1–10 ms         | ~10–100 μs (100×)  | Proces: nowa przestrzeń adresowa, tablice stron, kopiowanie struktur jądra. Wątek: tylko nowy stos + wpis w schedulerze. |
| Przełączanie      | ~1000–5000 ns    | ~100–500 ns (10×)  | Proces: TLB flush (unieważnienie cache adresów). Wątek: te same tablice stron, TLB zostaje. |
| Komunikacja       | ~μs (IPC)        | ~ns (pamięć)        | Proces: kopiowanie przez jądro (pipe/socket). Wątek: bezpośredni zapis/odczyt heapu. |
| Zakończenie       | wolne            | szybkie             | Proces: zwolnienie przestrzeni adresowej, zamknięcie plików. Wątek: zwolnienie stosu. |

![Szybkość — benchmarki Linux](img/q9_speed_comparison.png)

> **Mnemonik SZYBKOŚCI — „100, 10, 1000":**
> Tworzenie wątku **100×** szybsze, przełączanie **10×** szybsze, komunikacja **1000×** szybsza.
> Dlaczego? **„TLB zostaje"** — wątek nie zmienia mieszkania (przestrzeni adresowej), więc cache adresów (TLB) nie trzeba czyścić.
> Zapamiętaj: **fork() = przeprowadzka**, **pthread_create() = nowy pokój w tym samym mieszkaniu**.

### Zastosowanie — kiedy proces, kiedy wątek?

**Procesy — stosuj gdy:**

- **Izolacja jest krytyczna** — awaria jednego nie zabija reszty
    - Przeglądarka Chrome: każda karta = osobny proces. Crash Flash w jednej karcie nie zabija reszty.
    - Serwer: każde połączenie = fork() → klient nie może uszkodzić serwera (Apache pre-fork MPM)
- **Bezpieczeństwo** — procesy nie widzą nawzajem pamięci
    - Sandboxing: proces renderujący PDFa nie ma dostępu do pamięci procesu z hasłami
- **Wieloprogramowość** — różne programy (edytor + kompilator + przeglądarka)
- **Fork-exec** — klasyczny model Unix: fork() + exec() → nowy program

**Wątki — stosuj gdy:**

- **Współdzielenie danych** — wątki czytają/piszą ten sam heap bez kopiowania
    - Serwer WWW: wątki obsługujące requesty współdzielą cache w pamięci (nginx worker threads)
    - Gra: wątek renderujący i wątek fizyki czytają ten sam świat gry
- **Szybkość tworzenia/przełączania** — potrzeba wielu lekkich zadań
    - Thread pool: 8 wątków obsługuje tysiące zadań (zamiast tysiąca procesów)
- **Obliczenia równoległe** — podział pracy na rdzenie CPU
    - Mnożenie macierzy: każdy wątek liczy fragment wyniku
    - Rendering: każdy wątek renderuje część klatki
- **Responsywność UI** — wątek główny obsługuje interfejs, wątek tła liczy/pobiera dane

![Kiedy proces, kiedy wątek? — scenariusze](img/q9_scenario_table.png)

> **Mnemonik ZASTOSOWANIA — „MURY vs OKNA":**
> **Proces jak MURY** = izolacja, bezpieczeństwo, crash isolation (Chrome karty, Apache, sandboxing).
> **Wątek jak OKNA** = szybki dostęp do wspólnych danych, lekki, wydajny (gry, thread pool, UI).
> Pytanie-test: „Czy awaria jednego ma zabić resztę?" → TAK = wątek OK, NIE = proces.
> Regułka: **„IBW → P, WSO → W"** = **I**zolacja/**B**ezpieczeństwo/**W**ieloprogramowość → **P**roces. **W**spółdzielenie/**S**zybkość/**O**bliczenia → **W**ątek.

### Porównanie zbiorcze

| Cecha           | Proces           | Wątek               |
|-----------------|------------------|----------------------|
| Przestrzeń addr | Własna, izolowana| Współdzielona        |
| Tworzenie       | ~1-10 ms         | ~10-100 μs           |
| Przełączanie    | Wolne (TLB flush)| Szybkie (rejestry)   |
| Komunikacja     | IPC (pipe, shm)  | Współdzielona pamięć |
| Izolacja        | Pełna            | Brak                 |
| Awaria          | Nie zabija innych | Może zabić cały proces|
| Zastosowanie    | Izolacja, bezpieczeństwo | Wydajność, współdzielenie |

### Problemy komunikacji

Procesy mają **izolowane** przestrzenie adresowe — nie mogą bezpośrednio czytać/pisać wzajemnej pamięci. Komunikacja wymaga pośrednictwa jądra OS (IPC). Wątki mają odwrotny problem: współdzielą pamięć, więc komunikacja jest trywialna, ale wymaga synchronizacji.

![Mechanizmy IPC — porównanie wizualny](img/ipc_mechanisms.png)

**Problem 1 — Overhead kopiowania (procesy).** Większość mechanizmów IPC wymaga kopiowania danych: proces A → jądro → proces B (2 kopie!). Przy dużych danych (np. klatki wideo 4K = 24 MB) to kosztowne.

**Problem 2 — Synchronizacja dostępu (wątki).** Wątki komunikują się przez wspólny heap, ale muszą pilnować, by nie pisać jednocześnie w to samo miejsce (race condition).

**Problem 3 — Blokowanie.** IPC może być synchroniczne (blokujące — nadawca czeka aż odbiorca przeczyta) lub asynchroniczne (nieblokujące — nadawca idzie dalej). Wybór wpływa na wydajność i złożoność kodu.

#### Mechanizmy IPC z przykładami

![Mechanizmy IPC — szczegóły: Pipe, Shared Memory, Socket](img/q9_ipc_details.png)

**Pipe (potok anonimowy)** — jednokierunkowy strumień bajtów w pamięci jądra. Tylko między procesem-rodzicem a potomkiem (fork). Klasyczny przykład Unix:

    $ ls -la | grep ".txt" | wc -l

    Kod C:
    int fd[2];
    pipe(fd);               // tworzy potok: fd[0]=read, fd[1]=write
    if (fork() == 0) {      // potomek
        close(fd[1]);        // zamknij pisanie
        read(fd[0], buf, n); // czytaj od rodzica
    } else {                // rodzic
        close(fd[0]);        // zamknij czytanie
        write(fd[1], "hello", 5); // pisz do potomka
    }

**Named Pipe (FIFO)** — jak pipe, ale ma nazwę w systemie plików. Niespokrewnione procesy mogą go używać:

    $ mkfifo /tmp/moj_potok                   # stwórz FIFO
    $ echo "dane" > /tmp/moj_potok &          # proces A pisze
    $ cat /tmp/moj_potok                       # proces B czyta → "dane"

**Shared Memory (pamięć współdzielona)** — najszybszy IPC. OS mapuje ten sam region pamięci fizycznej do obu procesów. Zero kopiowania — oba procesy czytają/piszą bezpośrednio. ALE: wymaga synchronizacji (semafor/mutex).

    Kod C (POSIX):
    int fd = shm_open("/my_shm", O_CREAT|O_RDWR, 0666);
    ftruncate(fd, 4096);
    char *ptr = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    sprintf(ptr, "dane z procesu A"); // Proces A pisze
    // Proces B: shm_open + mmap → czyta ptr → "dane z procesu A"

**Message Queue (kolejka wiadomości)** — strukturalne wiadomości w jądrze. Asynchroniczna: nadawca wrzuca, odbiorca pobiera z kolejki kiedy chce. Typ wiadomości pozwala filtrować.

    Kod C:
    Proces A: msgsnd(qid, &msg, size, 0)    // wyślij wiadomość
    Proces B: msgrcv(qid, &msg, size, typ, 0) // odbierz (filtruj typ)
    Przewaga nad pipe: wiele nadawców/odbiorców, filtrowanie typów,
    wiadomość ma granice (pipe to surowy strumień bajtów).

**Socket** — dwukierunkowa komunikacja, działa lokalnie (Unix domain) i przez sieć (TCP/UDP). Najbardziej uniwersalny mechanizm IPC.

**Signal (sygnał)** — asynchroniczne powiadomienie od jądra/procesu. Przesyła TYLKO numer (nie dane). Użycie: obsługa Ctrl+C (SIGINT), zabijanie procesów (SIGKILL), powiadomienie o zdarzeniu.

    kill(pid, SIGUSR1);    // wyślij sygnał SIGUSR1 do procesu
    $ kill -9 1234         // wyślij SIGKILL (nie do przechwycenia)
    signal(SIGINT, handler); // zarejestruj handler dla Ctrl+C

#### Porównanie mechanizmów IPC

![Porównanie mechanizmów IPC — tabela](img/q9_ipc_table.png)

> **Mnemonik KOMUNIKACJI — „PNMSSS" (6 mechanizmów IPC):**
> **P**iotrek **N**ie **M**a **S**iedmiu **S**tarych **S**karpet = **P**ipe, **N**amed pipe, **M**essage queue, **S**hared memory, **S**ocket, **S**ignal.
> Szybkość: **Shared Memory > Pipe ≈ MsgQueue > Socket** (sieciowy najwolniejszy).
> Zapamiętaj: **„Shared = zero kopii"** — najszybszy bo oba procesy piszą do tej samej ramki RAM.
> **Pipe = rura z wodą** (jednokierunkowa), **Socket = telefon** (dwukierunkowy, też przez sieć).

---

### Problemy synchronizacji

Gdy wątki (lub procesy z shared memory) współdzielą dane, pojawiają się 4 fundamentalne problemy:

![Ilustracja zakleszczenia — cykl oczekiwania](img/deadlock_illustration.png)

#### Problem 1 — Wyścig (Race Condition)

Wynik programu zależy od losowej kolejności operacji wątków. Źródło: operacja „czytaj-modyfikuj-zapisz" nie jest atomowa.

![Wyścig — dwa przykłady](img/q9_race_condition.png)

    Poprawka — mutex:
    lock(mutex);
    saldo = saldo + kwota;  // sekcja krytyczna
    unlock(mutex);

#### Problem 2 — Zakleszczenie (Deadlock)

Dwa lub więcej wątków czekają na siebie nawzajem — żaden nie może kontynuować. System „zamiera".

![Zakleszczenie — scenariusz i cykl oczekiwania](img/q9_deadlock_scenario.png)

**Warunki Coffmana** — 4 warunki konieczne deadlocka (WSZYSTKIE muszą zachodzić):

![Warunki Coffmana — strategie zapobiegania](img/q9_coffman_strategies.png)

#### Problem 3 — Zagłodzenie (Starvation)

Wątek nigdy nie dostaje zasobu, bo inni ciągle go wyprzedzają. Nie jest deadlockiem (inni się wykonują). Przykład: 10 wątków, wątek niskopriorytetowy nigdy nie dostaje CPU bo wysoko priorytetowe ciągle dominują.

#### Problem 4 — Inwersja priorytetów (Priority Inversion)

Wątek wysokopriorytetowy (H) czeka na mutex trzymany przez niskopriorytetowy (L), a średniopriorytetowy (M) blokuje L. Efekt: H czeka na M (mimo wyższego priorytetu!).

![Zagłodzenie i inwersja priorytetów](img/q9_starvation_priority.png)

> **Mnemonik SYNCHRONIZACJI — „WZZI" (4 problemy):**
> **W**szystkie **Z**egarki **Z**atrzymały się **I**naczej = **W**yścig, **Z**akleszczenie, **Z**agłodzenie, **I**nwersja priorytetów.
> Coffman — **„MHNC"**: **M**uszę **H**amować, **N**ie **C**ofam = **M**utual exclusion, **H**old-and-wait, **N**o preemption, **C**ircular wait. Złam JEDEN = brak deadlocka.
> Najłatwiej złamać **Circular Wait** → numeruj mutexy, blokuj ROSNĄCO.
> Wyścig → **mutex**. Zakleszczenie → **porządek zamków**. Zagłodzenie → **aging**. Inwersja → **priority inheritance**.

---

### Klasyczne problemy synchronizacji

![Klasyczne problemy synchronizacji — 3 panele](img/q9_classic_problems.png)

#### Producent-Konsument (Bounded Buffer)

n producentów wrzuca elementy do bufora o ograniczonej pojemności, m konsumentów pobiera. Bufor pełny → producent czeka. Bufor pusty → konsument czeka.

![Producent-konsument z buforem cyklicznym](img/producer_consumer.png)

    Rozwiązanie z semaforami:
    semaphore mutex = 1;       // wyłączny dostęp do bufora
    semaphore empty = N;       // ile wolnych slotów (początkowo N)
    semaphore full  = 0;       // ile pełnych slotów (początkowo 0)

    Producent:                  Konsument:
      P(empty)                    P(full)
      P(mutex)                    P(mutex)
      wstaw(elem)                 elem = pobierz()
      V(mutex)                    V(mutex)
      V(full)                     V(empty)

    UWAGA: kolejność P(empty/full) PRZED P(mutex)!
    Odwrotnie (P(mutex) → P(empty)) = DEADLOCK!

#### Czytelnicy-Pisarze (Readers-Writers)

Wielu czytelników może czytać jednocześnie. Pisarz wymaga wyłącznego dostępu (ani czytelnicy, ani inni pisarze).

    Rozwiązanie (first readers-writers):
    int readers = 0;
    mutex rw_mutex;    // pisarz LUB pierwszy/ostatni czytelnik
    mutex count_mutex; // ochrona zmiennej readers

    Czytelnik:                    Pisarz:
      lock(count_mutex)             lock(rw_mutex)
      readers++                     // PISZ (wyłączny)
      if (readers == 1)             unlock(rw_mutex)
        lock(rw_mutex)
      unlock(count_mutex)
      // CZYTAJ (wielu jednocześnie!)
      lock(count_mutex)
      readers--
      if (readers == 0)
        unlock(rw_mutex)
      unlock(count_mutex)

    Problem: pisarze mogą głodować (readers=0 nigdy nie zachodzi).
    Rozwiązanie: fairness — kolejka FIFO czytelników i pisarzy.

#### Ucztujący filozofowie (Dining Philosophers)

5 filozofów siedzi przy okrągłym stole, między każdą parą 1 widelec. Filozofowie myślą lub jedzą. Jedzenie wymaga 2 widelców (lewego i prawego). Naiwne rozwiązanie: każdy bierze lewy → prawy → deadlock (wszyscy trzymają lewy, czekają na prawy).

    Rozwiązanie — złamanie cyklu:
    Filozofowie 0-3: bierz lewy, potem prawy.
    Filozof 4: bierz PRAWY, potem lewy. ← łamie circular wait!

    Alternatywa: semafor(4) — max 4 filozofów próbuje jeść naraz
    → jeden widelec zawsze wolny → brak deadlocka.

> **Mnemonik KLASYCZNYCH PROBLEMÓW — „PCF":**
> **P**yszne **C**iastka **F**ilozofów = **P**roducent-konsument, **C**zytelnicy-pisarze, **F**ilozofowie.
> Producent-konsument: „P(empty) PRZED P(mutex)" — inaczej deadlock!
> Czytelnicy-pisarze: „wielu czyta, jeden pisze" — pisarze mogą głodować.
> Filozofowie: „jeden bierze odwrotnie" — łamie circular wait.

---

### Mechanizmy synchronizacji — porównanie

![Mechanizmy synchronizacji — porównanie i mutex vs semafor vs spinlock](img/q9_sync_comparison.png)

> **Mnemonik MECHANIZMÓW — „MSMCSBR":**
> **M**ała **S**owa **M**oże **C**zasem **S**pinać na **B**ardzo **R**ówno = **M**utex, **S**emafor, **M**onitor, **C**ond.Variable, **S**pinlock, **B**arrier, **R**W Lock.
> Reguła kciuka: sekcja **> 1 μs → MUTEX** (wątek zasypia). Sekcja **< 1 μs → SPINLOCK** (kręci się). **n wątków naraz → SEMAFOR(n)**.
> Mutex = klucz do łazienki (1 osoba). Semafor(3) = parking na 3 miejsca. Spinlock = obrotowe drzwi.

---

### 🎮 Mostek do pracy magisterskiej — wątki w silnikach gier

> Praca magisterska: „Porównanie wydajności i możliwości współczesnych silników gier komputerowych" — Unity vs Unreal Engine. Temat wątków jest **kluczowy** dla game engine performance.

![Wątki w silniku gier — Game Loop Architecture](img/q9_game_engine_threads.png)

#### Game Loop = główny wątek silnika

Każdy silnik gier to **pętla główna (game loop)** działająca w jednym procesie z wieloma wątkami:

    while (gameIsRunning) {
        ProcessInput();      // ← Main Thread (sekwencyjne)
        UpdateGameLogic();   // ← Main Thread
        PhysicsStep();       // ← Physics Thread (równoległe)
        RenderFrame();       // ← Render Thread (równoległe)
        PresentFrame();      // ← GPU sync (blokujące!)
    }

#### Unity vs Unreal — porównanie wielowątkowości

| Aspekt | Unity | Unreal Engine |
|--------|-------|---------------|
| Język | C# (managed) | C++ (native) |
| Main thread | MonoBehaviour.Update() | AActor::Tick() |
| Physics thread | PhysX (osobny) | PhysX (osobny) |
| Render thread | Ukryty, submit GPU cmd | RenderThread (jawny) |
| Worker pool | Job System (DOTS/Burst) | TaskGraph |
| Problem | **GC pauses** zamrażają main thread! | Brak GC — deterministyczny timing |
| Object pooling | BulletPool.cs eliminuje GC spikes | FPooledObject |

#### Przykład z pracy — BulletPool (Object Pooling)

W grze bullet-hell (1000+ pocisków) **bez poolingu**:
- `Instantiate()` → alokacja na managed heap → GC musi zbierać → **spike w frame time**
- Nsight Graphics pokazuje: frame time skacze z 8ms na 25ms podczas GC sweep

**Z poolingiem** (`BulletPool.cs`):
- Pre-alokacja 2000 obiektów na starcie
- `pool.Get()` / `pool.Return()` → **zero alokacji w runtime**
- Frame time stabilny: 8ms ± 0.5ms

#### Problemy synchronizacji w silnikach gier — konkretne przykłady

| Problem (z pytania) | Jak występuje w game engine |
|---------------------|------------------------------|
| **Race condition** | Dwa wątki modyfikują pozycję tego samego obiektu (AI + Physics) |
| **Deadlock** | Render Thread czeka na dane z Main Thread, który czeka na GPU fence |
| **Zagłodzenie** | Render Thread ma wyższy priorytet → Audio Thread nie dostaje CPU |
| **Inwersja priorytetów** | Low-pri asset loading blokuje mutex potrzebny High-pri render |

#### Mnemonik — „GRAJ WĄTKAMI"

**G**ame Loop (main thread) → **R**ender Thread → **A**udio Thread → **J**ob System (workers)
Każda litera = osobny wątek. Game Loop orkiestruje resztę.

Kiedy na obronie padnie pytanie o wątki → od razu powiedz:
*„W mojej pracy porównuję Unity Job System (C#/Burst) z Unreal TaskGraph (C++). Kluczowa różnica: Unity GC może zatrzymać main thread, Unreal ma deterministyczne czasy."*

---

### Etymologia

**Proces** — łac. „processus" = posuwanie się naprzód. **Wątek (Thread)** — metafora nitki wykonania (jak nić Ariadny). **Mutex** — portmanteau MUTual EXclusion. **Semafor** — Dijkstra (1965); od semaforów kolejowych; P() = hol. „proberen" (próbować), V() = hol. „verhogen" (podnosić). **Coffman** — Edward Coffman Jr. et al. (1971): 4 warunki konieczne deadlocka. **Deadlock (zakleszczenie)** — jak zablokowane koła zębate. **IPC** — Inter-Process Communication.

### Jak zapamiętać

- **„Proces = mieszkanie, Wątek = pokój"** — każde mieszkanie ma adres (przestrzeń), pokoje dzielą kuchnię (heap)
- Wątki szybsze bo nie trzeba zmieniać „mieszkania" (TLB flush)
- **4 warunki Coffmana** zakleszczenia: złam jeden → brak deadlocka
- **„100, 10, 1000"** — tworzenie 100× szybsze, przełączanie 10×, komunikacja 1000×
- **PNMSSS** — 6 mechanizmów IPC (Pipe, Named pipe, Msg queue, Shared mem, Socket, Signal)
- **WZZI** — 4 problemy synchronizacji (Wyścig, Zakleszczenie, Zagłodzenie, Inwersja)
- **MHNC** — 4 warunki Coffmana (Mutual excl., Hold&wait, No preemption, Circular wait)
- **PCF** — 3 klasyczne problemy (Producent-konsument, Czytelnicy-pisarze, Filozofowie)
- **SRP** — prywatne części wątku (Stos, Rejestry, PC)
- **IBW → Proces, WSO → Wątek** — kiedy co stosować

\newpage
