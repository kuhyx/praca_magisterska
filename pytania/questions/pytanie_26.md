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

**Prefiks „I" w MPI_Isend / MPI_Irecv** — oznacza **Immediate** (natychmiastowy). Funkcja wraca natychmiast, bez czekania na zakończenie operacji. Konwencja nazewnicza MPI: prefiks „I" = wersja nieblokująca danej operacji (np. MPI_Send → MPI_**I**send, MPI_Recv → MPI_**I**recv). Analogicznie „S" = Synchronous (MPI_**S**send), „B" = Buffered (MPI_**B**send).

**Dlaczego Isend/Irecv mogą wrócić natychmiast, skoro dane nie zostały jeszcze przesłane?** — Bo te funkcje NIE wykonują transferu danych. One jedynie **rejestrują żądanie** w bibliotece MPI i wracają. Konkretnie:

- **MPI_Isend** mówi bibliotece MPI: „chcę wysłać te dane z tego adresu pamięci". MPI zapisuje sobie wskaźnik na bufor, rozmiar, odbiorcę i tag w wewnętrznej strukturze (request object). Transfer nastąpi PÓŹNIEJ — w tle (np. przez osobny wątek komunikacyjny, DMA, lub sprzęt sieciowy RDMA), albo dopiero gdy programista wywoła MPI_Wait/MPI_Test.
- **MPI_Irecv** mówi bibliotece MPI: „przygotuj miejsce — gdy dane nadejdą, wpisz je pod ten adres". MPI rejestruje „oczekiwanie na wiadomość" i wraca. Dane mogą jeszcze nie istnieć — to nie problem, bo odbiór nastąpi gdy nadawca faktycznie wyśle.

Analogia: Isend/Irecv to jak złożenie zamówienia w restauracji — kelner zapisuje zamówienie (wraca natychmiast), ale jedzenie pojawi się dopiero później. MPI_Wait to moment, gdy czekasz na talerz.

    MPI_Isend(buf, n, type, dest, tag, comm, &req)
        ↓
    [Wewnątrz MPI: zapisz {buf, n, type, dest, tag} w req]
        ↓
    return;  ← NATYCHMIAST — żaden bajt nie został jeszcze wysłany!
        ↓
    ... aplikacja robi obliczenia ...
        ↓
    MPI_Wait(&req)
        ↓
    [MPI teraz FAKTYCZNIE przesyła dane / czeka na zakończenie transferu]
        ↓
    return;  ← TERAZ dane są bezpiecznie wysłane, bufor można ponownie użyć

**UWAGA:** Między Isend a Wait programista NIE MOŻE modyfikować bufora wysyłkowego (buf) — MPI może w dowolnym momencie rozpocząć kopiowanie z tego adresu. Między Irecv a Wait programista NIE MOŻE czytać bufora odbiorczego — dane mogą być jeszcze niekompletne.

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

**Metoda Jacobiego (Jacobi iteration)** — iteracyjna metoda rozwiązywania układów równań liniowych $Ax = b$. W każdej iteracji nowa wartość $x_i$ jest obliczana WYŁĄCZNIE na podstawie wartości z poprzedniej iteracji (w przeciwieństwie do metody Gaussa-Seidla, która używa już obliczonych nowych wartości).

Konkretny przykład — układ 3 równań:

    10x₁ + 2x₂ + x₃  = 27        Przekształcenie:
     x₁ + 5x₂ + x₃   = 14.5      x₁ = (27  - 2x₂ - x₃) / 10
     2x₁ + 3x₂ + 10x₃ = 29       x₂ = (14.5 - x₁ - x₃) / 5
                                    x₃ = (29  - 2x₁ - 3x₂) / 10

    Start: x = [0, 0, 0]
    Iter 1: x₁ = (27 - 0 - 0)/10 = 2.70
            x₂ = (14.5 - 0 - 0)/5 = 2.90
            x₃ = (29 - 0 - 0)/10 = 2.90
    Iter 2: x₁ = (27 - 2·2.90 - 2.90)/10 = 1.83
            x₂ = (14.5 - 2.70 - 2.90)/5 = 1.78
            x₃ = (29 - 2·2.70 - 3·2.90)/10 = 1.49
    ... → zbieżność do x = [2, 1.5, 2]

**Wersja równoległa metody Jacobiego** — w obliczeniach naukowych (np. symulacja ciepła, dynamika płynów) macierz $A$ jest ogromna (miliony zmiennych). Dzielimy wektor $x$ na bloki — każdy proces MPI oblicza swój fragment. Ale na granicy bloków proces potrzebuje wartości od sąsiada → wymiana komunikatami Send/Recv.

    Domena 1D podzielona na 4 procesy:
    Proc 0         Proc 1         Proc 2         Proc 3
    [x₀ x₁ x₂]   [x₃ x₄ x₅]   [x₆ x₇ x₈]   [x₉ x₁₀ x₁₁]
              ↑↓             ↑↓             ↑↓
         wymiana x₂↔x₃  wymiana x₅↔x₆  wymiana x₈↔x₉

    Każdy proces potrzebuje "ghost cells" (komórek-duchów) od sąsiada,
    by obliczyć nowe wartości na swojej granicy.

**Kod SPMD (Single Program, Multiple Data)** — model programowania, gdzie WSZYSTKIE procesy uruchamiają TEN SAM program. Każdy rozróżnia się tylko numerem (rankiem). To jest właśnie „symetryczny kod" — i tu leży problem z deadlockiem.

**Dlaczego Jacobi jest podatny na deadlock?** — Symetryczny kod oznacza, że każdy proces wykonuje identyczną sekwencję: najpierw Send do sąsiada, potem Recv od sąsiada. Przy blokującym, synchronicznym Send (np. MPI_Ssend) KAŻDY proces czeka, aż sąsiad wywoła Recv. Ale sąsiad też jest w Send i też czeka!

    // Deadlock w symetrycznym Jacobi — KAŻDY proces uruchamia ten sam kod:
    for (iter = 0; iter < max_iter; iter++) {
        oblicz_nowe_wartości(x_local);
        MPI_Ssend(x_boundary, neighbor);  ← BLOKUJE, czeka na Recv sąsiada
        MPI_Recv(ghost_cells, neighbor);  ← nigdy nie dotrze tutaj!
    }

    Proc 0: Ssend(to=1) → czeka na Recv(from=0) w Proc 1
    Proc 1: Ssend(to=0) → czeka na Recv(from=0) w Proc 0
    → OBA CZEKAJĄ → DEADLOCK!

---

**Rozwiązania deadlocka w symetrycznym kodzie** — istnieją 4 główne strategie. Każda ma inne kompromisy między prostotą kodu, wydajnością i bezpieczeństwem.

**1. Asymetria kolejności (odd-even trick)** — łamiemy symetrię ręcznie: procesy o parzystym ranku robią Send→Recv, a o nieparzystym Recv→Send. Wymaga ręcznego podziału logiki (kod staje się mniej czytelny), ale gwarantuje brak deadlocka, bo zawsze jest para Send↔Recv gotowa do dopasowania.

    // Proc 0 (parzysty):       // Proc 1 (nieparzysty):
    Send(to=1);                  Recv(from=0);
    Recv(from=1);                Send(to=0);

    Proc 0: Send(to=1) ──→ Proc 1: Recv(from=0)  ✓ dopasowanie!
    Proc 0: Recv(from=1) ←── Proc 1: Send(to=0)  ✓ dopasowanie!

    Wada: asymetryczny kod — trzeba pisać if (rank % 2 == 0) {...} else {...}
    Zaleta: zero buforowania, pełna kontrola, brak dodatkowej pamięci.

**2. Komunikacja nieblokująca (Irecv + Isend + Waitall)** — każdy proces NAJPIERW inicjuje odbiór (Irecv — non-blocking), POTEM inicjuje wysłanie (Isend — non-blocking), a na końcu czeka na zakończenie obu (Waitall). Ponieważ Irecv/Isend wracają natychmiast, nie ma momentu, w którym oba procesy blokowałyby się nawzajem.

    // Identyczny kod na KAŻDYM procesie (symetryczny!):
    MPI_Request reqs[2];
    MPI_Irecv(ghost_cells, neighbor, &reqs[0]);  // inicjuj odbiór — wraca natychmiast
    MPI_Isend(x_boundary, neighbor, &reqs[1]);   // inicjuj wysyłanie — wraca natychmiast
    // tutaj można robić obliczenia wewnętrzne (overlap computation & communication)
    MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE);   // czekaj na zakończenie obu

    Zalety: symetryczny kod, możliwość overlappingu obliczeń z komunikacją.
    Wady: trzeba zarządzać obiektami MPI_Request, nieco bardziej złożony kod.

**3. MPI_Sendrecv — jedna funkcja, zero deadlocków** — MPI dostarcza funkcję, która JEDNOCZEŚNIE wysyła do jednego procesu i odbiera od innego. Implementacja MPI wewnętrznie dba o brak deadlocka (np. przez buforowanie lub asynchroniczny transport). To najbezpieczniejsze i najczystsze rozwiązanie.

    // Identyczny kod na KAŻDYM procesie:
    MPI_Sendrecv(
        x_boundary, count, MPI_DOUBLE, neighbor, tag_send,  // co wysyłam i komu
        ghost_cells, count, MPI_DOUBLE, neighbor, tag_recv,  // co odbieram i od kogo
        MPI_COMM_WORLD, &status
    );

    Zalety: najprostszy kod, symetryczny, gwarantuje brak deadlocka.
    Wady: brak overlappingu (blokujące — wraca dopiero po zakończeniu obu operacji).
    → REKOMENDOWANE rozwiązanie w większości zastosowań Jacobi.

**4. Buforowane wysyłanie (MPI_Bsend)** — nadawca kopiuje dane do bufora użytkownika i wraca natychmiast (nie czeka na Recv odbiorcy). Bufor musi być wcześniej zaalokowany przez MPI_Buffer_attach. Recv nie musi być gotowy — dane czekają w buforze.

    // Przygotowanie bufora:
    char buffer[BUF_SIZE];
    MPI_Buffer_attach(buffer, BUF_SIZE);

    // Identyczny kod na KAŻDYM procesie:
    MPI_Bsend(x_boundary, count, MPI_DOUBLE, neighbor, tag);  // kopiuje do bufora → wraca
    MPI_Recv(ghost_cells, count, MPI_DOUBLE, neighbor, tag, ...);  // normalny Recv

    Zalety: symetryczny kod, Send nie blokuje.
    Wady: wymaga zarządzania buforem (alokacja, rozmiar), dodatkowa pamięć.
    Ryzyko: jeśli bufor się przepełni → MPI_ERR_BUFFER → crash.

**Porównanie rozwiązań:**

    Rozwiązanie       Symetryczny?  Overlap?   Dodatkowa pamięć?  Prostota
    ─────────────────────────────────────────────────────────────────────────
    Odd-even           Nie          Nie        Nie                Średnia
    Irecv+Isend+Wait   Tak          Tak        MPI_Request        Średnia
    MPI_Sendrecv       Tak          Nie        Nie                Najlepsza
    Bsend              Tak          Nie        Bufor użytkownika  Średnia

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

### Problem: Zakleszczenie w symetrycznym kodzie (Jacobi)

**Kontekst — równoległy Jacobi:** Rozpatrzmy symulację ciepła w 1D (równanie Poissona). Domena podzielona na $P$ procesów. W każdej iteracji:
1. Oblicz nowe wartości wewnętrznych punktów na podstawie starego $x$
2. Wyślij wartość graniczną sąsiadowi (Send)
3. Odbierz wartość graniczną od sąsiada (Recv)
4. Powtórz

Ponieważ używamy modelu SPMD (Single Program, Multiple Data), KAŻDY proces uruchamia IDENTYCZNY kod:

    // Symetryczny kod Jacobi — DEADLOCK!
    for (iter = 0; iter < 1000; iter++) {
        // Oblicz nowe wartości wewnętrzne
        for (i = 1; i < local_n-1; i++)
            x_new[i] = 0.5 * (x[i-1] + x[i+1]);

        // Wymiana granic z sąsiadami — TU JEST PROBLEM:
        MPI_Ssend(&x_new[local_n-1], 1, MPI_DOUBLE, right, tag, comm);  // ← BLOKUJE
        MPI_Ssend(&x_new[0],         1, MPI_DOUBLE, left,  tag, comm);  // ← BLOKUJE
        MPI_Recv(&ghost_right, 1, MPI_DOUBLE, right, tag, comm, &st);   // nigdy tu nie dotrze
        MPI_Recv(&ghost_left,  1, MPI_DOUBLE, left,  tag, comm, &st);   // nigdy tu nie dotrze
    }

**Dlaczego deadlock?** Każdy z $P$ procesów wisi na pierwszym Ssend, czekając aż sąsiad wywoła Recv. Ale sąsiad TEŻ wisi na swoim Ssend. Nikt nigdy nie dochodzi do Recv → klasyczny cykliczny deadlock.

    Proc 0: Ssend(to=1) ──CZEKA──→ potrzebuje Recv(from=0) w Proc 1
    Proc 1: Ssend(to=0) ──CZEKA──→ potrzebuje Recv(from=0) w Proc 0
    Proc 1: Ssend(to=2) ──CZEKA──→ potrzebuje Recv(from=1) w Proc 2
    Proc 2: Ssend(to=1) ──CZEKA──→ potrzebuje Recv(from=2) w Proc 1
    → CYKL ZALEŻNOŚCI → DEADLOCK dla WSZYSTKICH procesów!

### Rozwiązania zakleszczenia — szczegółowo

#### 1. Asymetria kolejności (odd-even trick)

Łamiemy symetrię ręcznie: procesy o **parzystym** ranku wykonują Send→Recv, a o **nieparzystym** Recv→Send. Gwarantuje to, że w każdym momencie istnieje dopasowana para Send↔Recv.

    // Pełny kod Jacobi z odd-even:
    for (iter = 0; iter < 1000; iter++) {
        oblicz_wnetrze(x, x_new, local_n);

        if (rank % 2 == 0) {
            // PARZYSTY: najpierw wyślij w prawo, potem odbierz z prawa
            MPI_Send(&x_new[local_n-1], 1, MPI_DOUBLE, right, 0, comm);
            MPI_Recv(&ghost_right,      1, MPI_DOUBLE, right, 0, comm, &st);
            // potem wyślij w lewo, odbierz z lewa
            MPI_Send(&x_new[0],         1, MPI_DOUBLE, left,  0, comm);
            MPI_Recv(&ghost_left,       1, MPI_DOUBLE, left,  0, comm, &st);
        } else {
            // NIEPARZYSTY: najpierw odbierz z lewa, potem wyślij w lewo
            MPI_Recv(&ghost_left,       1, MPI_DOUBLE, left,  0, comm, &st);
            MPI_Send(&x_new[0],         1, MPI_DOUBLE, left,  0, comm);
            // potem odbierz z prawa, wyślij w prawo
            MPI_Recv(&ghost_right,      1, MPI_DOUBLE, right, 0, comm, &st);
            MPI_Send(&x_new[local_n-1], 1, MPI_DOUBLE, right, 0, comm);
        }
    }

    Proc 0 (parzysty): Send(→1) ──→ Proc 1 (nieparzysty): Recv(←0)  ✓
    Proc 1 (nieparzysty): Send(→0) ──→ Proc 0 (parzysty): Recv(←1)  ✓

**Zalety:** brak dodatkowej pamięci, pełna kontrola nad kolejnością, brak narzutu buforowania.
**Wady:** kod asymetryczny (if/else), łatwo o błąd, trudniejszy w utrzymaniu.

#### 2. Komunikacja nieblokująca (Irecv + Isend + Waitall)

Każdy proces NAJPIERW inicjuje odbiór (Irecv), POTEM inicjuje wysłanie (Isend), a na końcu czeka na zakończenie obu (Waitall). Kluczowa zasada: **zawsze inicjuj Irecv PRZED Isend** — wtedy gdy dane dotrą, odbiór jest już gotowy na nie.

    // Pełny kod Jacobi z non-blocking — symetryczny!
    MPI_Request reqs[4];
    for (iter = 0; iter < 1000; iter++) {
        // 1. Inicjuj odbiory (wraca natychmiast)
        MPI_Irecv(&ghost_right, 1, MPI_DOUBLE, right, 0, comm, &reqs[0]);
        MPI_Irecv(&ghost_left,  1, MPI_DOUBLE, left,  0, comm, &reqs[1]);

        // 2. Inicjuj wysyłanie (wraca natychmiast)
        MPI_Isend(&x_new[local_n-1], 1, MPI_DOUBLE, right, 0, comm, &reqs[2]);
        MPI_Isend(&x_new[0],         1, MPI_DOUBLE, left,  0, comm, &reqs[3]);

        // 3. W MIĘDZYCZASIE: oblicz wartości wewnętrzne (overlap!)
        oblicz_wnetrze(x, x_new, local_n);

        // 4. Czekaj na zakończenie WSZYSTKICH komunikacji
        MPI_Waitall(4, reqs, MPI_STATUSES_IGNORE);

        // 5. Teraz ghost_left i ghost_right są gotowe — oblicz granice
        oblicz_granice(x, x_new, ghost_left, ghost_right);
    }

**Zalety:** kod symetryczny (identyczny na każdym procesie), możliwość **overlappingu** — obliczenia wewnętrznych punktów odbywają się RÓWNOCZEŚNIE z komunikacją, co może znacznie przyspieszyć program.
**Wady:** trzeba zarządzać tablicą MPI_Request, nieco bardziej złożony kod, obliczenia muszą być podzielone na „wewnętrzne" (bez ghost cells) i „graniczne" (z ghost cells).

#### 3. MPI_Sendrecv — atomowa wymiana (REKOMENDOWANE)

MPI dostarcza funkcję, która JEDNOCZEŚNIE wysyła i odbiera. Implementacja MPI wewnętrznie gwarantuje brak deadlocka (np. przez wewnętrzne buforowanie lub scheduling). Najbezpieczniejsze i najczystsze rozwiązanie.

    // Pełny kod Jacobi z Sendrecv — symetryczny, prosty, bezpieczny!
    for (iter = 0; iter < 1000; iter++) {
        oblicz_wnetrze(x, x_new, local_n);

        // Wymiana z prawym sąsiadem (wysyłam swoją prawą granicę, odbieram jego lewą):
        MPI_Sendrecv(
            &x_new[local_n-1], 1, MPI_DOUBLE, right, 0,   // wysyłam
            &ghost_right,      1, MPI_DOUBLE, right, 0,   // odbieram
            comm, &status
        );

        // Wymiana z lewym sąsiadem:
        MPI_Sendrecv(
            &x_new[0],    1, MPI_DOUBLE, left,  0,        // wysyłam
            &ghost_left,  1, MPI_DOUBLE, left,  0,        // odbieram
            comm, &status
        );

        oblicz_granice(x, x_new, ghost_left, ghost_right);
    }

**Zalety:** najprostszy kod, symetryczny, zero ryzyka deadlocka, brak zarządzania Request/Buffer.
**Wady:** blokujące — wraca dopiero po zakończeniu obu operacji, więc NIE pozwala na overlapping obliczeń z komunikacją. Dla większości zastosowań Jacobi to **nie problem**, bo komunikacja jest krótka.

#### 4. Buforowane wysyłanie (MPI_Bsend)

Nadawca kopiuje dane do wcześniej zaalokowanego bufora i wraca natychmiast. Recv nie musi być jeszcze wywołany — dane czekają w buforze. Wymaga ręcznego zarządzania buforem.

    // Pełny kod Jacobi z Bsend:
    // SETUP (jednorazowo):
    int buf_size = 2 * (sizeof(double) + MPI_BSEND_OVERHEAD);
    char* buffer = malloc(buf_size);
    MPI_Buffer_attach(buffer, buf_size);

    for (iter = 0; iter < 1000; iter++) {
        oblicz_wnetrze(x, x_new, local_n);

        // Bsend kopiuje do bufora i WRACA NATYCHMIAST:
        MPI_Bsend(&x_new[local_n-1], 1, MPI_DOUBLE, right, 0, comm);
        MPI_Bsend(&x_new[0],         1, MPI_DOUBLE, left,  0, comm);

        // Recv normalnie blokuje, ale dane już czekają w buforze sąsiada:
        MPI_Recv(&ghost_right, 1, MPI_DOUBLE, right, 0, comm, &st);
        MPI_Recv(&ghost_left,  1, MPI_DOUBLE, left,  0, comm, &st);

        oblicz_granice(x, x_new, ghost_left, ghost_right);
    }

    // CLEANUP:
    MPI_Buffer_detach(&buffer, &buf_size);
    free(buffer);

**Zalety:** kod symetryczny, Send nie blokuje, proste użycie.
**Wady:** wymaga zarządzania buforem (alokacja, rozmiar MPI_BSEND_OVERHEAD), dodatkowa pamięć. Jeśli bufor się przepełni (np. wiele Bsend bez matchujących Recv) → **MPI_ERR_BUFFER** → crash programu.

#### Porównanie wszystkich rozwiązań

    Rozwiązanie       Symetryczny?  Overlap?   Ekstra pamięć?     Prostota
    ─────────────────────────────────────────────────────────────────────────
    Odd-even           Nie          Nie        Nie                Średnia
    Irecv+Isend+Wait   Tak          TAK        MPI_Request        Średnia
    MPI_Sendrecv       Tak          Nie        Nie                ★ Najlepsza
    Bsend              Tak          Nie        Bufor użytkownika  Średnia

### Etymologia

**MPI** — Message Passing Interface (MPI Forum, 1994); standard komunikacji w obliczeniach równoległych. **Jacobi** — Carl Gustav Jacob Jacobi (1804–1851, mat. niemiecki); metoda iteracyjna rozwiązywania układów równań. **Synchroniczna** — grec. „syn" (razem) + „chronos" (czas) = w tym samym czasie. **Asynchroniczna** — grec. „a-" (nie) + synchronous = nie w tym samym czasie. **Blokująca** — funkcja „blokuje" wątek aż operacja się skończy.

### Jak zapamiętać

- **Deadlock = Send-Send** — oba czekają, nikt nie odbiera
- **Sendrecv = „safe exchange"** — jedna funkcja, zero deadlocków
- **I = Immediate = Non-blocking** (MPI_Isend, MPI_Irecv)
- **S = Synchronous** (MPI_Ssend — czeka na recv)

