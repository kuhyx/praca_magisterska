# Pytanie 32: Komunikacja synchroniczna/asynchroniczna, blokująca/nieblokująca

## Pytanie
**"Podać definicję komunikacji synchronicznej i asynchronicznej oraz blokującej i nieblokującej. Jak uniknąć zakleszczenia, gdy dwa symetryczne procesy (np. realizujące algorytm iteracyjny Jacobiego) mają w kodzie następujące po sobie wywołania funkcji wysyłającej komunikat do partnera i odbierającej komunikat wysłany przez niego?"**

Przedmiot: PORR (Programowanie Równoległe i Rozproszone)

---

## 📚 Odpowiedź główna

### 1. Definicje podstawowe

#### Synchroniczna vs Asynchroniczna

```
KOMUNIKACJA SYNCHRONICZNA:
┌─────────────────────────────────────────────────────────────────┐
│ Nadawca i odbiorca synchronizują się w momencie przekazania    │
│                                                                 │
│ Proces A                        Proces B                        │
│    │                               │                            │
│    │ send() ──────────────────> recv()                         │
│    │ [czeka aż B odbierze]       [odbiera]                     │
│    │ [kontynuuje]                 │                            │
│                                                                 │
│ Gwarancja: Po powrocie z send() wiadomość została odebrana     │
└─────────────────────────────────────────────────────────────────┘

KOMUNIKACJA ASYNCHRONICZNA:
┌─────────────────────────────────────────────────────────────────┐
│ Nadawca nie czeka na odbiorcę                                   │
│                                                                 │
│ Proces A                        Proces B                        │
│    │                               │                            │
│    │ send() ─────────> [bufor] ───> recv()                     │
│    │ [kontynuuje                    │ (później)                │
│    │  natychmiast]                  │                          │
│                                                                 │
│ Gwarancja: Wiadomość trafiła do bufora (nie do odbiorcy!)      │
└─────────────────────────────────────────────────────────────────┘
```

#### Blokująca vs Nieblokująca

```
OPERACJA BLOKUJĄCA:
┌─────────────────────────────────────────────────────────────────┐
│ Wywołanie nie zwraca kontroli do wołającego dopóki operacja    │
│ nie zostanie zakończona (lub warunek spełniony)                │
│                                                                 │
│ Proces:   send()                                                │
│           ├─────────────────────┤                               │
│           │     BLOKADA         │                               │
│           │  (czeka na coś)     │                               │
│           └─────────────────────┘                               │
│                              return                             │
└─────────────────────────────────────────────────────────────────┘

OPERACJA NIEBLOKUJĄCA:
┌─────────────────────────────────────────────────────────────────┐
│ Wywołanie zwraca natychmiast, operacja wykonuje się w tle      │
│                                                                 │
│ Proces:   isend() → return immediately                         │
│           │                                                     │
│           │ (inne obliczenia)                                   │
│           │                                                     │
│           wait() lub test()  ← sprawdź czy zakończone          │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Kombinacje w MPI

| Funkcja MPI | Blokująca? | Synchroniczna? | Opis |
|-------------|------------|----------------|------|
| `MPI_Send` | Blokująca | Zależne od impl. | Standard send |
| `MPI_Ssend` | Blokująca | Synchroniczna | Czeka na recv |
| `MPI_Bsend` | Blokująca | Asynchroniczna | Buforowana |
| `MPI_Rsend` | Blokująca | - | Ready (recv musi czekać) |
| `MPI_Isend` | Nieblokująca | Asynchroniczna | Immediate |
| `MPI_Recv` | Blokująca | - | Standard recv |
| `MPI_Irecv` | Nieblokująca | - | Immediate recv |

---

### 3. Problem zakleszczenia (Deadlock)

#### Scenariusz: Algorytm Jacobiego

```c
// DEADLOCK! - oba procesy czekają na siebie nawzajem

// Proces 0:                    // Proces 1:
MPI_Send(to=1, data);           MPI_Send(to=0, data);
MPI_Recv(from=1, data);         MPI_Recv(from=0, data);

Przebieg:
┌──────────────────┬──────────────────┐
│    PROCES 0      │    PROCES 1      │
├──────────────────┼──────────────────┤
│ Send(to=1)       │ Send(to=0)       │
│ [BLOKUJE - czeka │ [BLOKUJE - czeka │
│  aż 1 odbierze]  │  aż 0 odbierze]  │
│        ↓         │        ↓         │
│   DEADLOCK!      │   DEADLOCK!      │
│ (nikt nie robi   │ (nikt nie robi   │
│  Recv)           │  Recv)           │
└──────────────────┴──────────────────┘
```

---

### 4. Rozwiązania problemu zakleszczenia

#### 4.1 Zmiana kolejności operacji

```c
// Proces 0:                    // Proces 1:
MPI_Send(to=1, data);           MPI_Recv(from=0, data);  // ← zmiana!
MPI_Recv(from=1, data);         MPI_Send(to=0, data);

Przebieg:
┌──────────────────┬──────────────────┐
│    PROCES 0      │    PROCES 1      │
├──────────────────┼──────────────────┤
│ Send(to=1) ──────│──→ Recv(from=0)  │
│ [zakończone]     │ [zakończone]     │
│ Recv(from=1) ←───│─── Send(to=0)    │
│ [zakończone]     │ [zakończone]     │
└──────────────────┴──────────────────┘
✓ Brak deadlocka!
```

#### 4.2 Nieblokujące operacje

```c
// Oba procesy:
MPI_Request req_send, req_recv;

MPI_Irecv(from=partner, data_in, &req_recv);  // Nieblokujące recv
MPI_Isend(to=partner, data_out, &req_send);   // Nieblokujące send
MPI_Wait(&req_recv, &status);                  // Czekaj na recv
MPI_Wait(&req_send, &status);                  // Czekaj na send

Przebieg:
┌──────────────────┬──────────────────┐
│    PROCES 0      │    PROCES 1      │
├──────────────────┼──────────────────┤
│ Irecv (posted)   │ Irecv (posted)   │
│ Isend (posted)   │ Isend (posted)   │
│     ↓ ↓          │     ↓ ↓          │
│ [operacje w tle] │ [operacje w tle] │
│ Wait (recv done) │ Wait (recv done) │
│ Wait (send done) │ Wait (send done) │
└──────────────────┴──────────────────┘
✓ Brak deadlocka!
```

#### 4.3 MPI_Sendrecv

```c
// Oba procesy (najczystsze rozwiązanie):
MPI_Sendrecv(
    send_buf, send_count, type, dest, send_tag,
    recv_buf, recv_count, type, source, recv_tag,
    comm, &status
);

// Wewnętrznie implementuje bezpieczną wymianę
// Unika deadlocka automatycznie
```

#### 4.4 Buforowane wysyłanie

```c
// Attach buffer
char buffer[BUFFER_SIZE];
MPI_Buffer_attach(buffer, BUFFER_SIZE);

// Oba procesy:
MPI_Bsend(to=partner, data);  // Kopiuje do bufora i wraca
MPI_Recv(from=partner, data); // Teraz może odebrać

MPI_Buffer_detach(&buffer, &size);

// Działa gdy bufor wystarczająco duży
```

---

### 5. Porównanie rozwiązań

| Rozwiązanie | Zalety | Wady |
|-------------|--------|------|
| **Zmiana kolejności** | Proste, brak overhead | Wymaga asymetrii kodu |
| **Isend/Irecv** | Elastyczne, overlap | Złożoność kodu |
| **Sendrecv** | Proste, bezpieczne | Mniej elastyczne |
| **Bsend** | Podobne do standardowego | Wymaga bufora, memory |

---

### 6. Algorytm Jacobiego - pełny przykład

```c
// Iteracyjne rozwiązanie równania Laplace'a
// Grid podzielony między procesy

for (int iter = 0; iter < MAX_ITER; iter++) {
    // Wymiana granic z sąsiadami
    
    // Bezpieczna wymiana z lewym sąsiadem
    if (rank > 0) {
        MPI_Sendrecv(
            &u[1], 1, MPI_DOUBLE, rank-1, 0,      // wyślij lewą granicę
            &u[0], 1, MPI_DOUBLE, rank-1, 0,      // odbierz od lewego
            MPI_COMM_WORLD, &status
        );
    }
    
    // Bezpieczna wymiana z prawym sąsiadem
    if (rank < size-1) {
        MPI_Sendrecv(
            &u[n-2], 1, MPI_DOUBLE, rank+1, 0,    // wyślij prawą granicę
            &u[n-1], 1, MPI_DOUBLE, rank+1, 0,    // odbierz od prawego
            MPI_COMM_WORLD, &status
        );
    }
    
    // Obliczenia Jacobiego
    for (int i = 1; i < n-1; i++) {
        u_new[i] = 0.5 * (u[i-1] + u[i+1]);
    }
    
    swap(&u, &u_new);
}
```

---

### 7. Wzorce komunikacji

```
┌─────────────────────────────────────────────────────────────────┐
│ RING (pierścień) - każdy z sąsiadami:                          │
│                                                                 │
│     ┌───→ P0 ───→ P1 ───→ P2 ───→ P3 ───┐                      │
│     └──────────────────────────────────────┘                    │
│                                                                 │
│ Bezpieczne: Sendrecv w jednym kierunku                         │
├─────────────────────────────────────────────────────────────────┤
│ ALL-TO-ALL - każdy z każdym:                                   │
│                                                                 │
│     P0 ←→ P1                                                    │
│     P0 ←→ P2                                                    │
│     P1 ←→ P2                                                    │
│     ...                                                         │
│                                                                 │
│ Rozwiązanie: MPI_Alltoall lub ordered pairwise exchange        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mnemoniki

### "S-B Matrix":
| | Sync | Async |
|---|---|---|
| **Block** | Ssend | Send/Bsend |
| **Non-block** | - | Isend |

### "I = Immediate = Non-blocking":
MPI_Isend, MPI_Irecv - nieblokujące (I na początku)

### "Sendrecv = Safe exchange":
Jedna funkcja, zero deadlocków

---

## ❓ Pytania dodatkowe

### Q1: "Czy MPI_Send jest synchroniczne?"
**Odpowiedź:** Zależy od implementacji i rozmiaru! Małe wiadomości często buforowane (async), duże mogą być sync. MPI_Ssend zawsze sync, MPI_Bsend zawsze async (buforowane).

### Q2: "Jak wykryć potencjalny deadlock?"
**Odpowiedź:** Analiza statyczna grafu zależności send/recv. Narzędzia: MUST, Marmot. Runtime: timeouty, watchdog. Zasada: unikaj cykli w grafie oczekiwań.

### Q3: "Co to jest eager vs rendezvous protocol?"
**Odpowiedź:** Eager: małe msg kopiowane do bufora natychmiast (async). Rendezvous: duże msg - handshake send/recv przed transferem (sync). Threshold zależy od implementacji MPI.

---

## 🎯 Kluczowe punkty

1. **Synchroniczna:** Nadawca czeka na odbiorcę
2. **Blokująca:** Funkcja nie wraca do zakończenia
3. **Deadlock:** Cykliczne oczekiwanie (Send-Send)
4. **Rozwiązania:** Sendrecv, Isend/Irecv, zmiana kolejności
5. **MPI_I*** = nieblokujące (Immediate)

---

## 📖 Źródła

1. MPI Standard (mpi-forum.org)
2. Gropp et al. - "Using MPI"
3. Pacheco - "Parallel Programming with MPI"
