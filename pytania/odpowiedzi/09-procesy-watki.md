# Pytanie 9: Procesy i wątki w systemie operacyjnym

## Pytanie
**"Procesy i wątki w systemie operacyjnym. Omówić budowę, szybkość działania i zakres zastosowania. Przedstawić problemy i możliwości komunikacji i synchronizacji."**

Przedmiot: SOI (Systemy Operacyjne)

---

## 📚 Odpowiedź główna

### Wprowadzenie

**Proces** i **wątek** to podstawowe jednostki wykonania w systemach operacyjnych. Różnią się poziomem izolacji i kosztami przełączania.

---

## 1. Proces (Process)

### Definicja
**Proces** = program w trakcie wykonania + jego kontekst (zasoby, stan).

### Budowa procesu

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRZESTRZEŃ ADRESOWA PROCESU                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                                            │
│  │      STOS       │  ← zmienne lokalne, adresy powrotu        │
│  │    (Stack)      │    rośnie w dół ↓                         │
│  ├─────────────────┤                                            │
│  │        ↓        │                                            │
│  │                 │  ← wolna przestrzeń                        │
│  │        ↑        │                                            │
│  ├─────────────────┤                                            │
│  │     STERTA      │  ← pamięć dynamiczna (malloc/new)         │
│  │     (Heap)      │    rośnie w górę ↑                        │
│  ├─────────────────┤                                            │
│  │      BSS       │  ← zmienne globalne niezainicjowane        │
│  ├─────────────────┤                                            │
│  │      DATA       │  ← zmienne globalne zainicjowane          │
│  ├─────────────────┤                                            │
│  │      TEXT       │  ← kod programu (read-only)               │
│  │     (Code)      │                                            │
│  └─────────────────┘                                            │
└─────────────────────────────────────────────────────────────────┘
```

### PCB (Process Control Block)

Struktura w jądrze przechowująca informacje o procesie:

| Pole | Opis |
|------|------|
| **PID** | Identyfikator procesu |
| **Stan** | Running, Ready, Blocked, etc. |
| **Rejestry CPU** | PC, SP, flagi, rejestry ogólne |
| **Informacje o pamięci** | Tablice stron, limity |
| **Informacje I/O** | Otwarte pliki, urządzenia |
| **Informacje rozliczeniowe** | Czas CPU, limity |
| **Priorytet** | Szeregowanie |
| **Wskaźniki** | Rodzic, dzieci, kolejki |

### Stany procesu

```
                    ┌──────────────────┐
       (utworzenie) │                  │ (zakończenie)
            ↓       │                  │      ↓
      ┌─────────┐   │   ┌──────────┐   │  ┌──────────┐
      │   NEW   │───┼──→│  READY   │←──┼──│TERMINATED│
      └─────────┘   │   └──────────┘   │  └──────────┘
                    │        ↑↓        │
                    │   (scheduler)    │
                    │        ↓↑        │
                    │   ┌──────────┐   │
                    │   │ RUNNING  │   │
                    │   └──────────┘   │
                    │        │         │
                    │   (I/O, wait)    │
                    │        ↓         │
                    │   ┌──────────┐   │
                    └───│ BLOCKED  │───┘
                        └──────────┘
```

---

## 2. Wątek (Thread)

### Definicja
**Wątek** = lekka jednostka wykonania współdzieląca przestrzeń adresową procesu.

### Budowa wątku

```
┌─────────────────────────────────────────────────────────────────┐
│                         PROCES                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   WSPÓŁDZIELONE:              PRYWATNE (per wątek):            │
│   ┌─────────────────┐         ┌───────┐ ┌───────┐ ┌───────┐    │
│   │ Przestrzeń      │         │ Stos  │ │ Stos  │ │ Stos  │    │
│   │ adresowa        │         │ W1    │ │ W2    │ │ W3    │    │
│   ├─────────────────┤         ├───────┤ ├───────┤ ├───────┤    │
│   │ Kod (TEXT)      │         │Rejestry│ │Rejestry│ │Rejestry│   │
│   ├─────────────────┤         │ CPU   │ │ CPU   │ │ CPU   │    │
│   │ Dane globalne   │         ├───────┤ ├───────┤ ├───────┤    │
│   ├─────────────────┤         │  PC   │ │  PC   │ │  PC   │    │
│   │ Sterta (Heap)   │         ├───────┤ ├───────┤ ├───────┤    │
│   ├─────────────────┤         │  TID  │ │  TID  │ │  TID  │    │
│   │ Otwarte pliki   │         └───────┘ └───────┘ └───────┘    │
│   │ Sygnały         │         Wątek 1   Wątek 2   Wątek 3      │
│   └─────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### TCB (Thread Control Block)

| Pole | Opis |
|------|------|
| **TID** | Identyfikator wątku |
| **Stan** | Running, Ready, Blocked |
| **Rejestry** | PC, SP, rejestry ogólne |
| **Stos** | Wskaźnik do prywatnego stosu |
| **Priorytet** | Szeregowanie |
| **Wskaźnik do PCB** | Proces macierzysty |

---

## 3. Porównanie: Proces vs Wątek

### Tabela porównawcza

| Cecha | Proces | Wątek |
|-------|--------|-------|
| **Przestrzeń adresowa** | Własna, izolowana | Współdzielona z procesem |
| **Tworzenie** | Wolne (~ms) | Szybkie (~μs) |
| **Przełączanie kontekstu** | Wolne (TLB flush) | Szybkie (tylko rejestry) |
| **Komunikacja** | IPC (pipe, socket, shm) | Bezpośrednia (współdzielona pamięć) |
| **Izolacja** | Pełna | Brak (awaria = awaria procesu) |
| **Zasoby** | Własne | Współdzielone |
| **Wieloprocesorowość** | Naturalna | Wymaga synchronizacji |

### Koszty czasowe (typowe)

| Operacja | Czas |
|----------|------|
| Tworzenie procesu | 1-10 ms |
| Tworzenie wątku | 10-100 μs |
| Przełączanie procesu | 1-10 μs |
| Przełączanie wątku | 0.1-1 μs |
| Komunikacja IPC | 1-100 μs |
| Współdzielona pamięć | 10-100 ns |

---

## 4. Typy wątków

### Wątki użytkownika (User-level Threads)

```
┌─────────────────────────────────────────┐
│           PRZESTRZEŃ UŻYTKOWNIKA        │
│  ┌─────────────────────────────────┐    │
│  │   Biblioteka wątków (pthread)   │    │
│  │   ┌─────┐ ┌─────┐ ┌─────┐      │    │
│  │   │ W1  │ │ W2  │ │ W3  │      │    │
│  │   └─────┘ └─────┘ └─────┘      │    │
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│            JĄDRO                        │
│   Widzi tylko JEDEN wątek (proces)      │
└─────────────────────────────────────────┘
```

**Zalety:** Szybkie przełączanie, przenośność
**Wady:** Blokujące wywołanie blokuje wszystkie wątki, brak prawdziwej równoległości

### Wątki jądra (Kernel-level Threads)

```
┌─────────────────────────────────────────┐
│           PRZESTRZEŃ UŻYTKOWNIKA        │
│      ┌─────┐ ┌─────┐ ┌─────┐           │
│      │ W1  │ │ W2  │ │ W3  │           │
│      └──┬──┘ └──┬──┘ └──┬──┘           │
├─────────┼───────┼───────┼───────────────┤
│         ↓       ↓       ↓               │
│   ┌─────────────────────────────┐       │
│   │     JĄDRO (scheduler)       │       │
│   │  Zarządza wszystkimi wątkami│       │
│   └─────────────────────────────┘       │
└─────────────────────────────────────────┘
```

**Zalety:** Prawdziwa równoległość, blokada jednego nie blokuje innych
**Wady:** Wolniejsze operacje (wywołanie systemowe)

### Modele mapowania

| Model | Opis | Przykłady |
|-------|------|-----------|
| **1:1** | 1 wątek user = 1 wątek kernel | Linux, Windows |
| **N:1** | N wątków user = 1 wątek kernel | Green threads |
| **M:N** | M wątków user = N wątków kernel | Solaris, Go goroutines |

---

## 5. Komunikacja między procesami (IPC)

### Mechanizmy IPC

```
┌─────────────────────────────────────────────────────────────────┐
│                    MECHANIZMY IPC                               │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   SYGNAŁY       │      POTOKI     │      PAMIĘĆ WSPÓŁDZIELONA   │
│   (Signals)     │     (Pipes)     │      (Shared Memory)        │
├─────────────────┼─────────────────┼─────────────────────────────┤
│   KOLEJKI       │     GNIAZDA     │      PLIKI MAPOWANE         │
│  KOMUNIKATÓW    │    (Sockets)    │      (Memory-mapped)        │
│  (Msg Queues)   │                 │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

### Szczegóły mechanizmów

#### Potoki (Pipes)

```c
// Potok nienazwany (anonimowy)
int fd[2];
pipe(fd);
// fd[0] - odczyt, fd[1] - zapis

// Potok nazwany (FIFO)
mkfifo("/tmp/myfifo", 0666);
```

**Cechy:** Jednokierunkowe, FIFO, między powiązanymi procesami (anonimowe)

#### Pamięć współdzielona (Shared Memory)

```c
// POSIX shared memory
int fd = shm_open("/my_shm", O_CREAT | O_RDWR, 0666);
ftruncate(fd, SIZE);
void* ptr = mmap(NULL, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

// Użycie
strcpy(ptr, "Hello from process A");
// Proces B może odczytać przez ten sam shm_open
```

**Cechy:** Najszybszy IPC, wymaga synchronizacji!

#### Gniazda (Sockets)

```c
// Unix domain socket (lokalne)
int sock = socket(AF_UNIX, SOCK_STREAM, 0);

// Network socket (sieciowe)
int sock = socket(AF_INET, SOCK_STREAM, 0);
```

**Cechy:** Uniwersalne, lokalne i sieciowe, dwukierunkowe

#### Kolejki komunikatów (Message Queues)

```c
// POSIX message queue
mqd_t mq = mq_open("/my_queue", O_CREAT | O_RDWR, 0666, &attr);
mq_send(mq, message, strlen(message), priority);
mq_receive(mq, buffer, MAX_SIZE, &priority);
```

**Cechy:** Asynchroniczne, z priorytetami, zachowują granice wiadomości

---

## 6. Synchronizacja

### Problemy współbieżności

#### 1. Wyścig (Race Condition)

```c
// Dwa wątki wykonują:
counter++;  // NIE ATOMOWE!

// W asemblerze:
// LOAD counter → reg
// ADD 1 → reg  
// STORE reg → counter

// Możliwy przebieg:
// Wątek A: LOAD (counter=5)
// Wątek B: LOAD (counter=5)
// Wątek A: ADD (reg=6)
// Wątek B: ADD (reg=6)
// Wątek A: STORE (counter=6)
// Wątek B: STORE (counter=6)
// Wynik: 6 zamiast 7!
```

#### 2. Zakleszczenie (Deadlock)

```
Wątek A: lock(mutex1) → czeka na mutex2
Wątek B: lock(mutex2) → czeka na mutex1

→ DEADLOCK! (wzajemne oczekiwanie)
```

**Warunki Coffmana (wszystkie muszą być spełnione):**
1. **Mutual exclusion** - zasób może mieć tylko jeden właściciel
2. **Hold and wait** - trzymaj i czekaj na więcej
3. **No preemption** - nie można odebrać zasobu
4. **Circular wait** - cykliczne oczekiwanie

#### 3. Głodzenie (Starvation)

Proces nigdy nie dostaje zasobu, bo inni mają wyższy priorytet.

#### 4. Inwersja priorytetów (Priority Inversion)

Proces o niskim priorytecie blokuje proces o wysokim priorytecie (przez mutex).

---

### Mechanizmy synchronizacji

#### Mutex (Mutual Exclusion)

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_lock(&mutex);
// Sekcja krytyczna
counter++;
pthread_mutex_unlock(&mutex);
```

#### Semafor (Semaphore)

```c
sem_t sem;
sem_init(&sem, 0, 3);  // Wartość początkowa 3

sem_wait(&sem);  // P() - dekrementuj, blokuj jeśli 0
// Sekcja krytyczna
sem_post(&sem);  // V() - inkrementuj
```

**Typy:**
- **Binarny** (0/1) - jak mutex
- **Licznikowy** - ogranicza liczbę wątków (np. pula połączeń)

#### Zmienna warunkowa (Condition Variable)

```c
pthread_mutex_t mutex;
pthread_cond_t cond;

// Producent
pthread_mutex_lock(&mutex);
buffer[in] = item;
pthread_cond_signal(&cond);  // Obudź czekającego
pthread_mutex_unlock(&mutex);

// Konsument
pthread_mutex_lock(&mutex);
while (buffer_empty) {
    pthread_cond_wait(&cond, &mutex);  // Zwalnia mutex i czeka
}
item = buffer[out];
pthread_mutex_unlock(&mutex);
```

#### Bariera (Barrier)

```c
pthread_barrier_t barrier;
pthread_barrier_init(&barrier, NULL, NUM_THREADS);

// W każdym wątku:
// ... obliczenia ...
pthread_barrier_wait(&barrier);  // Czekaj na wszystkich
// ... dalsze obliczenia ...
```

#### Read-Write Lock

```c
pthread_rwlock_t rwlock;

// Czytelnik
pthread_rwlock_rdlock(&rwlock);  // Wielu może czytać
// ... czytanie ...
pthread_rwlock_unlock(&rwlock);

// Pisarz
pthread_rwlock_wrlock(&rwlock);  // Wyłączny dostęp
// ... pisanie ...
pthread_rwlock_unlock(&rwlock);
```

---

## 📊 Porównanie mechanizmów synchronizacji

| Mechanizm | Blokujący | Użycie | Koszt |
|-----------|-----------|--------|-------|
| **Mutex** | Tak | Sekcja krytyczna | Niski |
| **Spinlock** | Tak (aktywne) | Krótkie sekcje, SMP | Bardzo niski* |
| **Semafor** | Tak | Ograniczanie zasobów | Niski |
| **Cond. var.** | Tak | Oczekiwanie na warunek | Niski |
| **Bariera** | Tak | Synchronizacja fazowa | Średni |
| **RW Lock** | Tak | Wielu czytelników | Średni |
| **Atomics** | Nie | Proste operacje | Najniższy |

*jeśli sekcja krytyczna krótka

---

## 7. Zastosowania

### Kiedy procesy?

- **Izolacja** - awaria jednego nie wpływa na inne
- **Bezpieczeństwo** - różne uprawnienia
- **Różne języki/technologie** - mikrousługi
- **Niezawodność** - restart bez wpływu na system

**Przykłady:** Serwery WWW (fork), przeglądarki (proces per tab), bazy danych

### Kiedy wątki?

- **Współdzielenie danych** - bez kopiowania
- **Responsywność** - UI thread + worker threads
- **Równoległość CPU** - obliczenia na wielu rdzeniach
- **I/O asynchroniczne** - czekanie nie blokuje wszystkiego

**Przykłady:** Gry, serwery aplikacji, przetwarzanie obrazu/wideo

---

## 🧠 Mnemoniki

### "PEST" dla różnic Proces-wątek:
- **P**amięć - proces ma własną, wątek współdzieli
- **E**fektywność - wątek szybszy
- **S**ynchronizacja - wątki wymagają więcej
- **T**worzenie - proces wolniejsze

### "SPIN WAIT SLEEP" dla oczekiwania:
- **Spinlock** - aktywne czekanie (pętla)
- **Mutex** - uśpienie, wybudzenie przez scheduler

### "COFFMAN" dla warunków deadlocka:
- **C**ircular wait - cykliczne oczekiwanie
- **O**nly one - mutual exclusion
- **F**orever hold - hold and wait
- **F**orced release - no preemption (brak)

### "PV" dla semafora:
- **P** = Proberen (testuj) = wait = down = dekrementuj
- **V** = Verhogen (zwiększ) = signal = up = inkrementuj

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Jak unikać deadlocka?"

**Odpowiedź:**

1. **Zapobieganie** - złam jeden z warunków Coffmana:
   - Zamawianie zasobów (zawsze lock A przed B)
   - Żądaj wszystkich zasobów naraz
   - Timeout na blokady

2. **Unikanie** - algorytm bankiera (sprawdź czy bezpieczne)

3. **Wykrywanie i naprawianie** - graf oczekiwania, zabij proces

```c
// Zapobieganie przez porządek
// Zawsze: mutex1 przed mutex2
pthread_mutex_lock(&mutex1);
pthread_mutex_lock(&mutex2);
// ...
pthread_mutex_unlock(&mutex2);
pthread_mutex_unlock(&mutex1);
```

---

### Q2: "Czym różni się fork() od pthread_create()?"

**Odpowiedź:**

| fork() | pthread_create() |
|--------|------------------|
| Tworzy nowy proces | Tworzy nowy wątek |
| Kopiuje przestrzeń adresową (COW) | Współdzieli przestrzeń |
| Nowy PID | Ten sam PID, nowy TID |
| Komunikacja przez IPC | Komunikacja przez pamięć |
| Wolne (~ms) | Szybkie (~μs) |

```c
// fork()
pid_t pid = fork();
if (pid == 0) {
    // Proces potomny
} else {
    // Proces rodzic
}

// pthread_create()
pthread_t thread;
pthread_create(&thread, NULL, thread_function, arg);
pthread_join(thread, NULL);
```

---

### Q3: "Co to jest Copy-on-Write (COW)?"

**Odpowiedź:**

**COW** = optymalizacja fork() - strony pamięci są współdzielone dopóki nie zostaną zmodyfikowane.

```
Przed fork():
Proces A: [strona 1] [strona 2] [strona 3]

Po fork() (bez COW):
Proces A: [strona 1] [strona 2] [strona 3]  ← kopia
Proces B: [strona 1] [strona 2] [strona 3]  ← kopia
          (kopiowanie całej pamięci - WOLNE!)

Po fork() (z COW):
Proces A: [strona 1 (shared, RO)]
                    ↑
Proces B: [strona 1 (shared, RO)]
          (współdzielenie - SZYBKIE!)

Po modyfikacji przez A:
Proces A: [strona 1 (kopia, RW)]  ← kopia dopiero teraz!
Proces B: [strona 1 (shared, RO)]
```

---

### Q4: "Wyjaśnij problem producent-konsument"

**Odpowiedź:**

**Problem:** Producent wytwarza dane, konsument je pobiera. Bufor ograniczony.

```c
#define BUFFER_SIZE 10
int buffer[BUFFER_SIZE];
int count = 0;

sem_t empty, full;
pthread_mutex_t mutex;

// Inicjalizacja
sem_init(&empty, 0, BUFFER_SIZE);  // Wolne miejsca
sem_init(&full, 0, 0);              // Zajęte miejsca

void* producer(void* arg) {
    while (1) {
        int item = produce();
        
        sem_wait(&empty);           // Czekaj na wolne miejsce
        pthread_mutex_lock(&mutex);
        buffer[in] = item;
        in = (in + 1) % BUFFER_SIZE;
        pthread_mutex_unlock(&mutex);
        sem_post(&full);            // Sygnalizuj dane
    }
}

void* consumer(void* arg) {
    while (1) {
        sem_wait(&full);            // Czekaj na dane
        pthread_mutex_lock(&mutex);
        int item = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        pthread_mutex_unlock(&mutex);
        sem_post(&empty);           // Sygnalizuj wolne miejsce
        
        consume(item);
    }
}
```

---

### Q5: "Co to są coroutines/goroutines?"

**Odpowiedź:**

**Coroutines** = współprogramy - lekkie "wątki" zarządzane w przestrzeni użytkownika.

| Cecha | Wątki | Coroutines |
|-------|-------|------------|
| Scheduling | Preemptive (OS) | Cooperative (yield) |
| Stos | ~1-8 MB | ~2-8 KB |
| Tworzenie | ~10-100 μs | ~100 ns |
| Liczba | Setki-tysiące | Miliony |

**Goroutines (Go):**
```go
go func() {
    fmt.Println("Hello from goroutine")
}()
```

**Async/await (Python, C#, JavaScript):**
```python
async def fetch_data():
    data = await http_client.get(url)
    return data
```

---

### Q6: "Jak działa scheduler wątków?"

**Odpowiedź:**

**Algorytmy schedulingu:**

| Algorytm | Opis | Użycie |
|----------|------|--------|
| **FIFO** | Pierwszy przyszedł, pierwszy obsłużony | Prosty, batch |
| **Round Robin** | Kwant czasu, rotacja | Interaktywne |
| **Priority** | Wyższy priorytet pierwszy | Real-time |
| **CFS** | Completely Fair Scheduler | Linux |
| **Multi-level Feedback** | Priorytety + promocja/degradacja | Windows |

**CFS (Linux):**
- Wirtualny czas wykonania (vruntime)
- Czerwono-czarne drzewo
- Sprawiedliwy podział CPU

---

## 🎯 Kluczowe punkty do zapamiętania

1. **Proces** = izolacja, własna pamięć, wolne tworzenie
2. **Wątek** = współdzielenie, szybkie, wymaga synchronizacji
3. **IPC:** Pipes, shared memory, sockets, message queues
4. **Synchronizacja:** Mutex, semafor, cond var, bariera
5. **Deadlock:** 4 warunki Coffmana, zapobiegaj przez porządek
6. **Race condition:** Atomowe operacje lub blokady

---

## 📖 Źródła do pogłębienia

1. Silberschatz, Galvin - "Operating System Concepts"
2. Tanenbaum - "Modern Operating Systems"
3. Love, R. - "Linux Kernel Development"
4. Butenhof - "Programming with POSIX Threads"
