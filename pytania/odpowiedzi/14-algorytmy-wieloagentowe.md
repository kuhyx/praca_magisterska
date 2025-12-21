# Pytanie 14: Algorytmy i metody w systemach wieloagentowych i aktorowych

## Pytanie
**"Wymienić i szczegółowo opisać wybrane algorytmy i metody wykorzystywane w systemach wieloagentowych i aktorowych."**

Przedmiot: AASD (Agentowe i Aktorowe Systemy Decyzyjne)

---

## 📚 Odpowiedź główna

### 1. Algorytmy negocjacji i aukcji

#### Contract Net Protocol (CNP)

```
Fazy:
1. ANNOUNCEMENT - Manager ogłasza zadanie (cfp)
2. BIDDING - Wykonawcy składają oferty (propose)
3. AWARDING - Manager wybiera najlepszą (accept/reject)
4. EXECUTION - Wybrany wykonuje zadanie (inform)

        Manager                    Contractors
           │                      ┌───┬───┬───┐
           │────── cfp ──────────→│ A │ B │ C │
           │                      └───┴───┴───┘
           │←───── propose ───────    │   │
           │←───── propose ────────────   │
           │←───── propose ─────────────────
           │
           │── accept-proposal ──→ B (winner)
           │── reject-proposal ──→ A, C
           │
           │←───── inform ─────── B (result)
```

**Zastosowania:** Przydział zadań, zarządzanie zasobami, e-commerce

#### Aukcje wieloagentowe

| Typ aukcji | Mechanizm | Właściwości |
|------------|-----------|-------------|
| **English** | Rosnące stawki | Otwarta, winner's curse |
| **Dutch** | Malejące stawki | Szybka, ryzykowna |
| **First-price sealed** | Zapieczętowane | Strategiczne zaniżanie |
| **Vickrey** | Second-price sealed | Truthful (incentive compatible) |

---

### 2. Algorytmy konsensusu

#### Raft (dla systemów aktorowych)

```
Stany węzłów: FOLLOWER → CANDIDATE → LEADER

Leader Election:
1. Follower timeout → staje się Candidate
2. Candidate wysyła RequestVote do wszystkich
3. Większość głosów → nowy Leader
4. Leader wysyła heartbeats

Log Replication:
1. Client → Leader (command)
2. Leader → Followers (AppendEntries)
3. Większość potwierdza → commit
4. Leader → Client (success)
```

#### PBFT (Practical Byzantine Fault Tolerance)

```
Toleruje f błędnych węzłów przy n ≥ 3f + 1

Fazy:
PRE-PREPARE → PREPARE → COMMIT → REPLY

Client ──request──→ Primary
                      │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      Replica1   Replica2   Replica3
          └──────────┼──────────┘
                     ↓
                   Reply
```

---

### 3. Algorytmy koordynacji

#### Distributed Mutual Exclusion

**Algorytm Ricarta-Agrawali:**
```
Wejście do sekcji krytycznej:
1. Wyślij REQUEST(timestamp) do wszystkich
2. Czekaj na REPLY od wszystkich
3. Wejdź do sekcji krytycznej

Odbiór REQUEST:
- Jeśli nie chcę CS lub mój timestamp > nadawcy → wyślij REPLY
- W przeciwnym razie → kolejkuj REQUEST
```

**Złożoność:** 2(N-1) wiadomości na wejście do CS

#### Token Ring
```
     ┌───→ A ───→ B ───┐
     │                 ↓
     │    [TOKEN]      │
     │                 │
     └─── D ←─── C ←───┘

Kto ma token → może wejść do CS
Złożoność: 0 do N-1 wiadomości (średnio N/2)
```

---

### 4. Algorytmy uczenia wieloagentowego

#### Q-Learning (Independent Learners)

```
Każdy agent uczy się niezależnie:

Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]

Problem: Środowisko niestacjonarne (inni agenci się zmieniają)
```

#### Nash Q-Learning

```
Uwzględnia akcje innych agentów:

Q_i(s, a₁, a₂, ..., aₙ) - wartość dla agenta i

Aktualizacja używa równowagi Nasha:
Q_i ← Q_i + α[r_i + γ Nash(Q_i(s')) - Q_i]
```

#### Fictitious Play
```
1. Obserwuj akcje przeciwników
2. Buduj rozkład empiryczny ich strategii
3. Graj best response wobec tego rozkładu
4. Powtarzaj

Zbieżność do Nasha w grach z właściwością FP
```

---

### 5. Algorytmy dla aktorów

#### Supervision Strategies (Akka)

```scala
// One-for-One: restart tylko tego aktora
override val supervisorStrategy =
  OneForOneStrategy() {
    case _: ArithmeticException => Resume
    case _: NullPointerException => Restart
    case _: Exception => Stop
  }

// All-for-One: restart wszystkich dzieci
override val supervisorStrategy =
  AllForOneStrategy() {
    case _: Exception => Restart
  }
```

#### Routing Strategies

| Strategia | Opis |
|-----------|------|
| **Round Robin** | Po kolei do każdego |
| **Random** | Losowo |
| **Smallest Mailbox** | Do najmniej obciążonego |
| **Broadcast** | Do wszystkich |
| **Consistent Hashing** | Wg klucza (locality) |

---

### 6. Algorytmy planowania (BDI)

#### Means-Ends Reasoning

```
Goal: be_at(destination)

Plans:
  plan1: walk(X,Y) :- distance(X,Y) < 1km
  plan2: drive(X,Y) :- have(car), distance(X,Y) >= 1km
  plan3: take_bus(X,Y) :- bus_available(X,Y)

Wybór planu na podstawie:
- Kontekstu (beliefs)
- Preferencji
- Kosztu
```

#### Partial Order Planning (POP)

```
Cel: have(coffee) ∧ have(report)

       Start
         │
    ┌────┴────┐
    ↓         ↓
 buy(coffee) write(report)
    │         │
    └────┬────┘
         ↓
        Goal

Ordering constraints: flexible (równoległość gdy możliwa)
```

---

### 7. Algorytmy formowania koalicji

#### Shapley Value

```
Sprawiedliwy podział zysków w koalicji:

φᵢ = Σ [|S|!(n-|S|-1)!/n!] × [v(S∪{i}) - v(S)]

Gdzie:
- S = podzbiór agentów bez i
- v(S) = wartość koalicji S
- n = liczba agentów

Właściwości: efektywność, symetria, addytywność
```

---

## 📊 Podsumowanie algorytmów

| Kategoria | Algorytm | Zastosowanie |
|-----------|----------|--------------|
| Negocjacje | Contract Net | Przydział zadań |
| Aukcje | Vickrey | Truthful bidding |
| Konsensus | Raft, PBFT | Systemy rozproszone |
| Koordynacja | Ricart-Agrawala | Mutual exclusion |
| Uczenie | Nash Q-Learning | Gry wieloagentowe |
| Aktorzy | Supervision | Fault tolerance |
| Planowanie | Means-Ends | BDI agenty |
| Koalicje | Shapley Value | Podział zysków |

---

## 🧠 Mnemoniki

### "CNP = Call, Propose, Award, Execute":
Fazy Contract Net Protocol

### "RAFT = Replicated And Fault Tolerant":
Leader election + log replication

### "Vickrey = Second price = Truthful":
Płacisz drugą cenę → opłaca się licytować prawdziwie

---

## ❓ Pytania dodatkowe

### Q1: "Dlaczego aukcja Vickreya jest truthful?"
**Odpowiedź:** Płacisz drugą najwyższą cenę, nie swoją. Licytowanie poniżej wartości = ryzyko przegranej. Licytowanie powyżej = ryzyko przepłacenia. Optymalna strategia = licytuj prawdziwą wartość.

### Q2: "Jak Raft radzi sobie z partycją sieci?"
**Odpowiedź:** Tylko partycja z większością węzłów może wybrać lidera i commitować. Mniejszość jest zablokowana (read-only lub niedostępna). Po naprawie partycji - synchronizacja logów.

### Q3: "Czym różni się One-for-One od All-for-One supervision?"
**Odpowiedź:** One-for-One: restart tylko wadliwego aktora (izolacja błędu). All-for-One: restart wszystkich dzieci (gdy stan jest współdzielony/zależny). Wybór zależy od zależności między aktorami.

---

## 🎯 Kluczowe punkty

1. **Contract Net** = aukcja zadań między agentami
2. **Raft/PBFT** = konsensus w systemach rozproszonych
3. **Nash Q-Learning** = uczenie z uwzględnieniem innych
4. **Supervision** = "let it crash" + automatic recovery
5. **Shapley Value** = sprawiedliwy podział koalicji

---

## 📖 Źródła

1. Shoham, Leyton-Brown - "Multiagent Systems"
2. Ongaro, Ousterhout - "In Search of an Understandable Consensus Algorithm" (Raft)
3. Akka Documentation - Supervision
4. Sandholm - "Distributed Rational Decision Making"
