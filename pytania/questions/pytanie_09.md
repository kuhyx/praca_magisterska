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

### Budowa procesu

Proces = program w trakcie wykonania + cały jego kontekst. Składa się z:

**Pamięć (oddzielna przestrzeń adresowa):**

    ┌──────────┐ wysoki adres
    │  STACK ↓ │  zmienne lokalne, adresy powrotu (każdy wątek ma WŁASNY)
    │   ...    │
    │  HEAP  ↑ │  malloc/new — dynamiczna alokacja (współdzielony między wątkami)
    │  BSS     │  zmienne globalne niezainicjalizowane (zerowane)
    │  DATA    │  zmienne globalne zainicjalizowane
    │  TEXT    │  kod maszynowy (read-only, współdzielony)
    └──────────┘ niski adres

**PCB (Process Control Block)** — struktura w jądrze OS opisująca proces:

    PCB = { PID, stan (READY/RUNNING/BLOCKED), rejestry CPU,
            tablice stron, otwarte pliki, priorytety, statystyki }

Przełączenie kontekstu = zapisanie PCB starego procesu → wczytanie PCB nowego.

**Stany procesu:** NEW → READY ↔ RUNNING → BLOCKED → TERMINATED.
Scheduler decyduje, który READY staje się RUNNING.

### Budowa wątku

Wątek = lekka jednostka wykonania WEWNĄTRZ procesu.

**Współdzielone** z innymi wątkami procesu: TEXT, DATA, BSS, HEAP, otwarte pliki, PID.
**Prywatne** (każdy wątek ma własne): stos (stack), rejestry CPU, program counter (PC), TID.

    Proces P (PID=42)
    ┌────────────────────────────────────────┐
    │  TEXT  │  DATA  │  BSS  │  HEAP        │  ← współdzielone
    ├────────┴────────┴───────┴──────────────┤
    │  Wątek 1: [stos₁] [rejestry₁] [PC₁]   │  ← prywatne
    │  Wątek 2: [stos₂] [rejestry₂] [PC₂]   │
    │  Wątek 3: [stos₃] [rejestry₃] [PC₃]   │
    └────────────────────────────────────────┘

Kluczowa różnica: proces ma CAŁĄ przestrzeń adresową, wątek to tylko kontekst wykonania (stos + rejestry) w ramach tej przestrzeni.

### Szybkość — porównanie ilościowe

| Operacja          | Proces           | Wątek              | Dlaczego różnica?                    |
|-------------------|------------------|---------------------|--------------------------------------|
| Tworzenie         | ~1–10 ms         | ~10–100 μs (100x)  | Proces: nowa przestrzeń adresowa, tablice stron, kopiowanie struktur jądra. Wątek: tylko nowy stos + wpis w schedulerze. |
| Przełączanie      | ~1000–5000 ns    | ~100–500 ns (10x)  | Proces: TLB flush (unieważnienie cache adresów). Wątek: te same tablice stron, TLB zostaje. |
| Komunikacja       | ~μs (IPC)        | ~ns (pamięć)        | Proces: kopiowanie przez jądro (pipe/socket). Wątek: bezpośredni zapis/odczyt heapu. |
| Zakończenie       | wolne            | szybkie             | Proces: zwolnienie przestrzeni adresowej, zamknięcie plików. Wątek: zwolnienie stosu. |

Konkretny przykład tworzenia (Linux):

    fork() (nowy proces):   ~1-5 ms  → kopiowanie tablic stron (copy-on-write)
    pthread_create() (wątek): ~50 μs → alokacja stosu (~8 MB) + wpis w schedulerze

Przełączanie kontekstu (benchmarki):

    Proces → Proces:  ~3000 ns (TLB flush + cache cold)
    Wątek  → Wątek:   ~300 ns  (TLB ciepły, ta sama pamięć)
    Zysk: ~10x szybciej

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

**Typowe scenariusze w praktyce:**

    Scenariusz                    Proces czy wątek?    Dlaczego?
    ──────────────────────────────────────────────────────────────
    Serwer WWW (Apache pre-fork)  Proces               izolacja klientów
    Serwer WWW (nginx)            Wątek/async           szybkość, cooperacja
    Przeglądarka (karty)          Proces               crash isolation
    Przeglądarka (JS + rendering) Wątek                współdzielony DOM
    Gra (fizyka + rendering)      Wątek                współdzielony świat
    Kompilacja wieloplikowa       Proces (make -j8)    izolacja, prostota
    Baza danych (zapytania)       Wątek                współdzielony cache
    Microservices                 Proces (kontener)    izolacja, deployment

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

**Pipe (potok anonimowy)** — jednokierunkowy strumień bajtów w pamięci jądra. Tylko między procesem-rodzicem a potomkiem (fork). Klasyczny przykład Unix:

    $ ls -la | grep ".txt" | wc -l

    Jak to działa wewnętrznie:
    ┌────────┐  write()  ┌─────────────┐  read()  ┌────────┐
    │  ls    │──────────→│ bufor jądra │──────────→│  grep  │
    │ stdout │  fd[1]    │  (4 KB)     │  fd[0]    │ stdin  │
    └────────┘           └─────────────┘           └────────┘
    Proces A pisze do fd[1], Proces B czyta z fd[0].
    Jądro buforuje dane. Gdy bufor pełny → write() blokuje.

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

    ┌───────────┐           ┌───────────┐
    │ Proces A  │           │ Proces B  │
    │           │           │           │
    │ strona 7 ─┼──→ RAM ←─┼─ strona 3 │  ← ta sama ramka fizyczna!
    │           │  ramka 42 │           │
    └───────────┘           └───────────┘
    Bez kopiowania — A pisze, B widzi od razu.

    Kod C (POSIX):
    int fd = shm_open("/my_shm", O_CREAT|O_RDWR, 0666);
    ftruncate(fd, 4096);
    char *ptr = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    sprintf(ptr, "dane z procesu A"); // Proces A pisze
    // Proces B: shm_open + mmap → czyta ptr → "dane z procesu A"

**Message Queue (kolejka wiadomości)** — strukturalne wiadomości w jądrze. Asynchroniczna: nadawca wrzuca, odbiorca pobiera z kolejki kiedy chce. Typ wiadomości pozwala filtrować.

    Proces A: msgsnd(qid, &msg, size, 0)    // wyślij wiadomość
    Proces B: msgrcv(qid, &msg, size, typ, 0) // odbierz (filtruj typ)

    Przewaga nad pipe: wiele nadawców/odbiorców, filtrowanie typów,
    wiadomość ma granice (pipe to surowy strumień bajtów).

**Socket** — dwukierunkowa komunikacja, działa lokalnie (Unix domain) i przez sieć (TCP/UDP). Najbardziej uniwersalny mechanizm IPC.

    ┌──────────┐  TCP/IP  ┌──────────┐
    │ Klient   │←────────→│ Serwer   │    sieciowy (różne maszyny)
    └──────────┘          └──────────┘

    ┌──────────┐  Unix    ┌──────────┐
    │ Proces A │←────────→│ Proces B │    lokalny (ten sam host)
    └──────────┘  socket  └──────────┘    /tmp/app.sock

**Signal (sygnał)** — asynchroniczne powiadomienie od jądra/procesu. Przesyła TYLKO numer (nie dane). Użycie: obsługa Ctrl+C (SIGINT), zabijanie procesów (SIGKILL), powiadomienie o zdarzeniu.

    kill(pid, SIGUSR1);    // wyślij sygnał SIGUSR1 do procesu
    $ kill -9 1234         // wyślij SIGKILL (nie do przechwycenia)
    signal(SIGINT, handler); // zarejestruj handler dla Ctrl+C

#### Porównanie mechanizmów IPC

    Mechanizm        Kierunek     Szybkość       Zastosowanie
    ──────────────────────────────────────────────────────────
    Pipe             jednokier.   średnia        ls | grep
    Named Pipe       jednokier.   średnia        demon → klient
    Shared Memory    dwukier.     najszybsza     video, bazy danych
    Message Queue    dwukier.     średnia        wieloproducentowe
    Socket           dwukier.     wolna (sieć)   klient-serwer
    Signal           jednokier.   natychmiast.   powiadomienia

---

### Problemy synchronizacji

Gdy wątki (lub procesy z shared memory) współdzielą dane, pojawiają się 4 fundamentalne problemy:

![Ilustracja zakleszczenia — cykl oczekiwania](img/deadlock_illustration.png)

#### Problem 1 — Wyścig (Race Condition)

Wynik programu zależy od losowej kolejności operacji wątków. Źródło: operacja „czytaj-modyfikuj-zapisz" nie jest atomowa.

    Przykład: konto bankowe, saldo = 1000 zł
    Wątek A: wpłata 500 zł          Wątek B: wypłata 200 zł

    BEZ synchronizacji (błąd!):
    ─────────────────────────────────────────────────────────
    Czas  Wątek A                   Wątek B
    ─────────────────────────────────────────────────────────
    t1    czytaj saldo → 1000
    t2                              czytaj saldo → 1000
    t3    saldo = 1000 + 500 = 1500
    t4                              saldo = 1000 - 200 = 800
    t5    zapisz saldo ← 1500
    t6                              zapisz saldo ← 800
    ─────────────────────────────────────────────────────────
    Wynik: 800 zł (powinno być 1300!)  ← wypłata nadpisała wpłatę!

    Poprawka — mutex:
    lock(mutex);
    saldo = saldo + kwota;  // sekcja krytyczna
    unlock(mutex);

    Z mutex: A blokuje → czyta 1000 → pisze 1500 → B blokuje → czyta 1500 → pisze 1300. ✓

#### Problem 2 — Zakleszczenie (Deadlock)

Dwa lub więcej wątków czekają na siebie nawzajem — żaden nie może kontynuować. System „zamiera".

    Klasyczny scenariusz: 2 wątki, 2 mutexy
    ─────────────────────────────────────────────────────────
    Wątek A:                      Wątek B:
      lock(mutex1) ✓  ←trzyma       lock(mutex2) ✓  ←trzyma
      lock(mutex2) ⏳ ←czeka!       lock(mutex1) ⏳ ←czeka!
    ─────────────────────────────────────────────────────────
    A czeka na mutex2 (B go trzyma), B czeka na mutex1 (A go trzyma).
    → DEADLOCK — żaden nie odpuści!

    Diagram cyklu:
          ┌──────────┐  czeka na  ┌──────────┐
          │ Wątek A  │───────────→│ Mutex 2  │
          │ trzyma   │            │ trzyma   │
          │ Mutex 1  │←───────────│ Wątek B  │
          └──────────┘  czeka na  └──────────┘

**Warunki Coffmana** — 4 warunki konieczne deadlocka (WSZYSTKIE muszą zachodzić):

    1. Mutual Exclusion  — zasób wyłączny (tylko 1 wątek)
    2. Hold and Wait     — trzymaj zasób, czekaj na kolejny
    3. No Preemption     — nie można zabrać zasobu siłą
    4. Circular Wait     — cykliczne oczekiwanie (A→B→...→A)

    Strategie zapobiegania (złam jeden warunek):
    ────────────────────────────────────────────────────
    Warunek            Jak złamać                  Przykład
    ────────────────────────────────────────────────────
    Mutual Exclusion   Zrób zasób współdzielony    Read-write lock
    Hold and Wait      Bierz WSZYSTKIE naraz       lock(m1, m2) atomowo
    No Preemption      Pozwól na timeout/trylock   pthread_mutex_trylock()
    Circular Wait      Porządek liniowy zamków     Zawsze m1 przed m2
    ────────────────────────────────────────────────────

    Najczęstsza strategia: PORZĄDEK LINIOWY (Circular Wait).
    Zasada: numeruj mutexy, zawsze blokuj w rosnącej kolejności.
    Jeśli mutex1 < mutex2 → ZAWSZE lock(mutex1) przed lock(mutex2).

#### Problem 3 — Zagłodzenie (Starvation)

Wątek nigdy nie dostaje zasobu, bo inni ciągle go wyprzedzają. Nie jest deadlockiem (inni się wykonują). Przykład: 10 wątków, wątek niskopriorytetowy nigdy nie dostaje CPU bo wysoko priorytetowe ciągle dominują.

    Rozwiązanie: aging (starzenie) — priorytet rośnie z czasem oczekiwania.
    Po 100 ms bez CPU: priorytet +1, po 200 ms: +2, itd.
    W końcu nawet najniższy wątek dostanie CPU.

#### Problem 4 — Inwersja priorytetów (Priority Inversion)

Wątek wysokopriorytetowy (H) czeka na mutex trzymany przez niskopriorytetowy (L), a średniopriorytetowy (M) blokuje L. Efekt: H czeka na M (mimo wyższego priorytetu!).

    Priorytet: H > M > L
    ─────────────────────────────────────────────────
    Czas   L             M           H
    ─────────────────────────────────────────────────
    t1     lock(mutex)
    t2                   (gotowy, wypycha L!)
    t3                   pracuje...     (czeka na mutex!)
    t4                   pracuje...     (CZEKA — bo M blokuje L)
    t5                   gotowy
    t6     unlock(mutex)                (wreszcie!)
    ─────────────────────────────────────────────────
    H czekał, dopóki M nie skończył, mimo że H > M!

    Rozwiązanie: Priority Inheritance Protocol.
    L dziedziczy priorytet H (tymczasowo L=H), więc M nie może wypchać L.
    Mars Pathfinder (1997) — klasyczny bug priority inversion w kosmosie!

---

### Klasyczne problemy synchronizacji

![Producent-konsument z buforem cyklicznym](img/producer_consumer.png)

#### Producent-Konsument (Bounded Buffer)

n producentów wrzuca elementy do bufora o ograniczonej pojemności, m konsumentów pobiera. Bufor pełny → producent czeka. Bufor pusty → konsument czeka.

    Rozwiązanie z semaforami:
    ─────────────────────────────────────────────────
    semaphore mutex = 1;       // wyłączny dostęp do bufora
    semaphore empty = N;       // ile wolnych slotów (początkowo N)
    semaphore full  = 0;       // ile pełnych slotów (początkowo 0)

    Producent:                  Konsument:
      P(empty)  // czekaj na   P(full)   // czekaj na
                // wolny slot            // pełny slot
      P(mutex)  // wejdź do    P(mutex)  // wejdź do
                // sek. kryt.            // sek. kryt.
      wstaw(elem)              elem = pobierz()
      V(mutex)  // wyjdź       V(mutex)  // wyjdź
      V(full)   // +1 pełny    V(empty)  // +1 wolny
    ─────────────────────────────────────────────────

    Bufor (N=4):
    ┌────┬────┬────┬────┐
    │ A  │ B  │    │    │  ← full=2, empty=2
    └────┴────┴────┴────┘
      ↑                 ↑
    konsument        producent

    BŁĄD jeśli zamienimy kolejność P(empty) i P(mutex) w producencie:
    Producent: P(mutex) → P(empty) ← bufor pełny → czeka z mutexem!
    Konsument: P(full) → P(mutex) ← mutex zajęty → DEADLOCK!

#### Czytelnicy-Pisarze (Readers-Writers)

Wielu czytelników może czytać jednocześnie. Pisarz wymaga wyłącznego dostępu (ani czytelnicy, ani inni pisarze).

    Rozwiązanie (first readers-writers):
    ─────────────────────────────────────────────────
    int readers = 0;
    mutex rw_mutex;    // pisarz LUB pierwszy/ostatni czytelnik
    mutex count_mutex; // ochrona zmiennej readers

    Czytelnik:                    Pisarz:
      lock(count_mutex)             lock(rw_mutex)
      readers++                     // PISZ (wyłączny)
      if (readers == 1)             unlock(rw_mutex)
        lock(rw_mutex)  // 1. czytelnik blokuje pisarzy
      unlock(count_mutex)
      // CZYTAJ (wielu jednocześnie!)
      lock(count_mutex)
      readers--
      if (readers == 0)
        unlock(rw_mutex) // ostatni odblokowuje pisarzy
      unlock(count_mutex)
    ─────────────────────────────────────────────────

    Problem: pisarze mogą głodować (readers=0 nigdy nie zachodzi).
    Rozwiązanie: fairness — kolejka FIFO czytelników i pisarzy.

#### Ucztujący filozofowie (Dining Philosophers)

5 filozofów siedzi przy okrągłym stole, między każdą parą 1 widelec. Filozofowie myślą lub jedzą. Jedzenie wymaga 2 widelców (lewego i prawego). Naiwne rozwiązanie: każdy bierze lewy → prawy → deadlock (wszyscy trzymają lewy, czekają na prawy).

    Rozwiązanie — złamanie cyklu:
    Filozofowie 0-3: bierz lewy, potem prawy.
    Filozof 4: bierz PRAWY, potem lewy. ← łamie circular wait!

    Alternatywa: semafor(4) — max 4 filozofów próbuje jeść naraz
    → jeden widelec zawsze wolny → brak deadlocka.

---

### Mechanizmy synchronizacji — porównanie

    Mechanizm         Opis                           Kiedy używać
    ──────────────────────────────────────────────────────────────────
    Mutex             Zamek: 1 wątek w sekcji        Sekcja krytyczna
    Semafor(n)        Licznik: max n wątków          Ograniczone zasoby
    Monitor           Obiekt z wbudowanym mutex      Java synchronized
    Cond. Variable    wait()/signal() na warunek     Producent-konsument
    Spinlock          Aktywne czekanie (busy-wait)   Bardzo krótkie sekcje
    RW Lock           Wielu czytelników LUB 1 pisarz Bazy danych, cache
    Barrier           Czekaj aż wszyscy dotrą        Obliczenia równoległe

    Mutex vs Semafor:
    ┌────────────────────────────────────────────────────────────┐
    │  Mutex = klucz do łazienki (1 osoba)                      │
    │  Semafor(3) = parking na 3 miejsca (3 samochody naraz)    │
    │  Semafor(1) = mutex (szczególny przypadek)                │
    └────────────────────────────────────────────────────────────┘

    Mutex vs Spinlock:
    ┌────────────────────────────────────────────────────────────┐
    │  Mutex: wątek ZASYPIA gdy czeka → OS go obudzi (koszt ~μs)│
    │  Spinlock: wątek KRĘCI się w pętli → marnuje CPU          │
    │  Spinlock lepszy gdy sekcja < 1 μs (koszt uśpienia > spin)│
    │  Mutex lepszy gdy sekcja > 1 μs (nie marnuje CPU)         │
    └────────────────────────────────────────────────────────────┘

### Etymologia

**Proces** — łac. „processus" = posuwanie się naprzód. **Wątek (Thread)** — metafora nitki wykonania (jak nić Ariadny). **Mutex** — portmanteau MUTual EXclusion. **Semafor** — Dijkstra (1965); od semaforów kolejowych; P() = hol. „proberen" (próbować), V() = hol. „verhogen" (podnosić). **Coffman** — Edward Coffman Jr. et al. (1971): 4 warunki konieczne deadlocka. **Deadlock (zakleszczenie)** — jak zablokowane koła zębate. **IPC** — Inter-Process Communication.

### Jak zapamiętać

- **„Proces = mieszkanie, Wątek = pokój"** — każde mieszkanie ma adres (przestrzeń), pokoje dzielą kuchnię (heap)
- Wątki szybsze bo nie trzeba zmieniać „mieszkania" (TLB flush)
- **4 warunki Coffmana** zakleszczenia: złam jeden → brak deadlocka

