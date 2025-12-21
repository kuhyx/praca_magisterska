# Pytanie 24: Modele spójności danych w systemach rozproszonych

## Pytanie
**"Omówić silne i słabe modele spójności danych w środowisku rozproszonym."**

Przedmiot: ERSMS (Elementy Rozproszonych Systemów i Middleware'u Sieciowego)

---

## 📚 Odpowiedź główna

### 1. Problem spójności w systemach rozproszonych

```
┌─────────────────────────────────────────────────────────────────┐
│ Repliki danych:                                                 │
│                                                                 │
│    Client A           Client B                                  │
│        │ write(x=1)       │ read(x)=?                          │
│        ↓                  ↓                                     │
│    ┌───────┐          ┌───────┐                                │
│    │Replica│──sync?──→│Replica│                                │
│    │   1   │          │   2   │                                │
│    │ x=1   │          │ x=0?  │                                │
│    └───────┘          └───────┘                                │
│                                                                 │
│ Pytanie: Co zwróci read(x)?                                    │
│ Odpowiedź zależy od modelu spójności!                          │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Spektrum modeli spójności

```
Silne ←─────────────────────────────────────────→ Słabe
                                                   
Linearizability                              Eventual
    │                                        Consistency
    ↓                                             ↑
Sequential                               Causal
Consistency                              Consistency
    │                                         ↑
    ↓                                    Session
Causal+                                  Guarantees
    │
    ↓
PRAM
```

---

### 3. Silne modele spójności

#### Linearizability (Linearyzacja)

```
Definicja: Każda operacja wygląda jakby wykonała się atomowo
w pewnym momencie między wywołaniem a odpowiedzią.

Timeline:
Client A: ─────[write(x=1)]─────────────────────→
Client B: ───────────[read(x)]──────────────────→
                        ↓
                     Musi zwrócić 1!

Właściwości:
- Najsilniejsza gwarancja
- "Globalny porządek rzeczywisty"
- Kosztowna (wymaga koordynacji)
```

**Implementacja:** Consensus (Paxos, Raft), single leader

#### Sequential Consistency

```
Definicja: Istnieje globalny porządek operacji zgodny
z porządkiem programu każdego procesu.

Client A: write(x=1) ──────────────────→
Client B: ──────────── write(x=2) ─────→
Client C: read(x)=? ── read(x)=? ──────→

Dozwolone: C widzi [1,2] lub [2,1]
           (byle konsystentnie z innymi)

Różnica od linearyzacji:
- Nie wymaga zgodności z czasem rzeczywistym
- Wystarczy spójny porządek
```

---

### 4. Słabe modele spójności

#### Eventual Consistency

```
Definicja: Jeśli nie ma nowych zapisów, ostatecznie
wszystkie odczyty zwrócą tę samą wartość.

Timeline:
write(x=1) @ Replica A
           ↓ (propagacja)
           ↓
           ↓ ... czas ...
           ↓
read(x)=1 @ Replica B (eventually)

Gwarancje:
✅ Dostępność (AP w CAP)
✅ Niska latencja
❌ Stare dane przez jakiś czas
❌ Możliwe konflikty
```

**Implementacja:** DNS, Dynamo, Cassandra

#### Causal Consistency

```
Definicja: Operacje przyczynowo zależne widziane
w tej samej kolejności przez wszystkich.

P1: write(x=1) ─────────────────────────→
                  ↓ (read x)
P2: ──────────── write(y=2) ────────────→

P3 widzi: x=1 przed y=2 (zawsze!)
          (bo y=2 zależy przyczynowo od x=1)

Niezależne zapisy mogą być widziane w różnej kolejności.
```

**Implementacja:** Vector clocks, COPS

#### Session Guarantees

| Gwarancja | Opis |
|-----------|------|
| **Read Your Writes** | Odczyt widzi własne wcześniejsze zapisy |
| **Monotonic Reads** | Raz widziana wartość nie "cofa się" |
| **Monotonic Writes** | Zapisy aplikowane w kolejności sesji |
| **Writes Follow Reads** | Zapis po odczycie widzi ten odczyt |

```
Read Your Writes:
Session: write(x=5) ──── read(x)=? ────→
                         Musi być 5!

Monotonic Reads:
Session: read(x)=5 ──── read(x)=? ────→
                        Musi być ≥ 5!
```

---

### 5. CAP Theorem

```
┌─────────────────────────────────────────────────────────────────┐
│                      CAP Theorem                                │
│                                                                 │
│                    Consistency (C)                              │
│                         /\                                      │
│                        /  \                                     │
│                       /    \                                    │
│                      / CA   \                                   │
│                     /        \                                  │
│                    /    CP    \                                 │
│   Availability (A) ──────────── Partition Tolerance (P)        │
│                         AP                                      │
│                                                                 │
│ W obecności partycji sieci (P): wybierz C lub A                │
│                                                                 │
│ CP: Spójne, ale niedostępne (Zookeeper, etcd)                 │
│ AP: Dostępne, ale niespójne (Dynamo, Cassandra)               │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6. Porównanie modeli

| Model | Gwarancje | Wydajność | Przykłady |
|-------|-----------|-----------|-----------|
| **Linearizable** | Najsilniejsze | Niska | Spanner, CockroachDB |
| **Sequential** | Silne | Średnia | Zookeeper |
| **Causal** | Przyczynowe | Dobra | COPS, MongoDB |
| **Session** | Per-sesja | Dobra | Dynamo sessions |
| **Eventual** | Najsłabsze | Najwyższa | DNS, Cassandra |

---

### 7. Strategie rozwiązywania konfliktów

#### Last-Writer-Wins (LWW)
```
Konflikt: write(x=1) || write(x=2)
Rozwiązanie: Większy timestamp wygrywa
Problem: Utrata danych!
```

#### Multi-Value (Siblings)
```
Konflikt: write(x=1) || write(x=2)
Rozwiązanie: Przechowaj oba: x=[1,2]
Klient rozwiązuje przy odczycie (Riak)
```

#### CRDTs (Conflict-free Replicated Data Types)
```
Struktury automatycznie łączące się:
- G-Counter (grow-only counter)
- OR-Set (observed-remove set)
- LWW-Register

Merge jest łączny, przemienny, idempotentny
→ Zawsze zbieżność!
```

---

## 🧠 Mnemoniki

### "Linearizable = Real-time + Atomic":
Widoczne natychmiast, atomowo

### "Eventual = Eventually, trust me":
Kiedyś będzie spójne (bez gwarancji kiedy)

### "CAP = Choose 2 of 3":
Partition → wybierz Consistency lub Availability

### "CRDT = Conflict-free":
Matematyczna gwarancja zbieżności

---

## ❓ Pytania dodatkowe

### Q1: "Czym różni się linearizability od serializability?"
**Odpowiedź:** Linearizability = dla pojedynczych operacji, real-time ordering. Serializability = dla transakcji, jakiś serial order. Strict serializability = oba razem.

### Q2: "Kiedy wybrać eventual consistency?"
**Odpowiedź:** Wysoka dostępność ważniejsza niż spójność, tolerancja na stale reads, możliwość rozwiązania konfliktów (shopping cart, likes counter, DNS).

### Q3: "Co to jest Quorum?"
**Odpowiedź:** W = write quorum, R = read quorum, N = repliki. W + R > N gwarantuje odczyt najnowszej wartości. Dynamo: N=3, W=2, R=2.

---

## 🎯 Kluczowe punkty

1. **Linearizable:** Najsilniejszy, atomowy, kosztowny
2. **Sequential:** Globalny porządek, bez real-time
3. **Causal:** Przyczynowo zależne w kolejności
4. **Eventual:** Ostatecznie spójne, najszybszy
5. **CAP:** Partition → C xor A
6. **CRDTs:** Automatyczne rozwiązywanie konfliktów

---

## 📖 Źródła

1. Herlihy, Wing - "Linearizability" (1990)
2. Vogels - "Eventually Consistent" (Amazon CTO)
3. Gilbert, Lynch - "CAP Theorem" (2002)
4. Shapiro et al. - "CRDTs" (2011)
