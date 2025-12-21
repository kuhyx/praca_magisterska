# Pytanie 23: Zegary logiczne i wektory stempli czasowych

## Pytanie
**"Przedstawić koncepcję i przeznaczenie zegarów logicznych i wektorów stempli czasowych."**

Przedmiot: ERSMS (Elementy Rozproszonych Systemów i Middleware'u Sieciowego)

---

## 📚 Odpowiedź główna

### 1. Problem czasu w systemach rozproszonych

```
┌─────────────────────────────────────────────────────────────────┐
│ Brak globalnego zegara:                                         │
│                                                                 │
│ Node A:  ──●────────●────────●──→ czas lokalny A               │
│            e1      e2       e3                                  │
│                    │↘                                           │
│                    │  ↘ msg                                     │
│                    │    ↘                                       │
│ Node B:  ────●─────────────●───→ czas lokalny B                │
│              e4           e5                                    │
│                                                                 │
│ Pytanie: Czy e2 było przed e5, czy po?                         │
│ Zegary fizyczne: drift, synchronizacja niedokładna             │
└─────────────────────────────────────────────────────────────────┘
```

**Problem:** Nie możemy polegać na zegarach fizycznych - drift, opóźnienia sieciowe, brak atomowej synchronizacji.

---

### 2. Relacja "happened-before" (Lamport)

#### Definicja (→)

Zdarzenie **a** happened-before **b** (a → b) jeśli:
1. **a** i **b** są w tym samym procesie i **a** występuje przed **b**
2. **a** to wysłanie wiadomości, **b** to jej odbiór
3. Przechodniość: a → c ∧ c → b ⟹ a → b

```
P1:  ─●─────●─────────●───→
      a     b         d
            │↘
            │  ↘ m1
            │    ↘
P2:  ───────────●─────●───→
                c     e

a → b (ten sam proces)
b → c (wysłanie → odbiór)
a → c (przechodniość)
c → e (ten sam proces)
```

#### Zdarzenia współbieżne

Jeśli ¬(a → b) ∧ ¬(b → a), to **a || b** (współbieżne).

---

### 3. Zegar Lamporta (Scalar Clock)

#### Algorytm

```
Każdy proces P_i ma licznik C_i:

1. Przed każdym zdarzeniem lokalnym:
   C_i := C_i + 1

2. Wysyłając wiadomość m:
   C_i := C_i + 1
   Dołącz timestamp(m) = C_i

3. Odbierając wiadomość m z timestamp t:
   C_i := max(C_i, t) + 1
```

#### Przykład

```
P1: C=0  ──●(1)────●(2)─────────●(5)──→
           a       b             d
                   │↘
                   │  ↘ m(2)
                   │    ↘
P2: C=0  ────●(1)───────●(3)────●(4)──→
             x           c       e

Zdarzenia: a=1, b=2, x=1, c=3, e=4, d=5
```

#### Właściwości

| Właściwość | Zegar Lamporta |
|------------|----------------|
| a → b ⟹ C(a) < C(b) | ✅ TAK |
| C(a) < C(b) ⟹ a → b | ❌ NIE |

**Ograniczenie:** C(a) < C(b) nie oznacza, że a → b (mogą być współbieżne).

---

### 4. Zegary wektorowe (Vector Clocks)

#### Algorytm

```
Każdy z N procesów ma wektor V[1..N]:

1. Przed każdym zdarzeniem lokalnym:
   V_i[i] := V_i[i] + 1

2. Wysyłając wiadomość m:
   V_i[i] := V_i[i] + 1
   Dołącz timestamp(m) = V_i

3. Odbierając wiadomość m z timestamp T:
   V_i[j] := max(V_i[j], T[j]) dla każdego j
   V_i[i] := V_i[i] + 1
```

#### Przykład

```
P1: [0,0,0] ──●[1,0,0]────●[2,0,0]─────────●[3,2,0]──→
              a            b                 d
                           │↘
                           │  ↘ m[2,0,0]
                           │    ↘
P2: [0,0,0] ────●[0,1,0]─────────●[2,2,0]────●[2,3,0]──→
                x                 c            e
```

#### Porównanie wektorów

```
V ≤ W  ⟺  ∀i: V[i] ≤ W[i]
V < W  ⟺  V ≤ W ∧ V ≠ W
V || W ⟺  ¬(V ≤ W) ∧ ¬(W ≤ V)

Przykład:
[2,3,1] < [2,4,1]  (happened-before)
[2,3,1] || [1,4,2] (współbieżne)
```

#### Właściwości

| Właściwość | Zegar wektorowy |
|------------|-----------------|
| a → b ⟺ V(a) < V(b) | ✅ TAK |
| Wykrycie współbieżności | ✅ TAK |

**Zegary wektorowe charakteryzują dokładnie relację happened-before!**

---

### 5. Porównanie

| Cecha | Lamport | Vector Clock |
|-------|---------|--------------|
| **Rozmiar** | O(1) | O(N) |
| **a → b ⟹ C(a) < C(b)** | ✅ | ✅ |
| **C(a) < C(b) ⟹ a → b** | ❌ | ✅ |
| **Wykrycie współbieżności** | ❌ | ✅ |
| **Zastosowanie** | Uporządkowanie | Wykrywanie konfliktów |

---

### 6. Zastosowania

| Zastosowanie | Typ zegara | Cel |
|--------------|------------|-----|
| **Mutual exclusion** | Lamport | Uporządkowanie żądań |
| **Causal broadcast** | Vector | Dostarczanie w kolejności przyczynowej |
| **Conflict detection** | Vector | Wykrycie współbieżnych zapisów |
| **Distributed debugging** | Vector | Odtworzenie kolejności zdarzeń |
| **Version vectors (Dynamo)** | Vector | Wykrycie konfliktów w replikacji |

#### Przykład: Dynamo/Riak

```
Put(key, value) z vector clock:

Client → Server A: put("x", "v1", [A:1])
Client → Server B: put("x", "v2", [B:1])

Konflikt wykryty: [A:1] || [B:1]
Oba wartości przechowane, klient rozwiązuje
```

---

### 7. Warianty i rozszerzenia

| Wariant | Opis |
|---------|------|
| **Interval Tree Clocks** | Dynamiczna liczba procesów |
| **Bloom Clocks** | Probabilistyczne, kompaktowe |
| **Hybrid Logical Clocks** | Lamport + czas fizyczny |
| **Matrix Clocks** | Wiedza o wiedzy innych |

---

## 🧠 Mnemoniki

### "Lamport = Licznik skalarny":
Jedna liczba, nie wykrywa współbieżności

### "Vector = Każdy wie o każdym":
V[i] = ile zdarzeń widział proces i

### "< oznacza →, || oznacza współbieżność":
Porównanie wektorów = relacja przyczynowa

---

## ❓ Pytania dodatkowe

### Q1: "Dlaczego nie używać NTP zamiast zegarów logicznych?"
**Odpowiedź:** NTP ma błąd ~ms (LAN) do ~100ms (WAN). Dla zdarzeń szybszych niż błąd synchronizacji, kolejność fizyczna jest nieznana. Zegary logiczne dają gwarancje przyczynowe bez względu na drift.

### Q2: "Co to jest causal consistency?"
**Odpowiedź:** Model spójności gdzie zapisy przyczynowo zależne są widziane w tej samej kolejności przez wszystkich. Wymaga vector clocks. Słabszy niż sequential consistency, silniejszy niż eventual.

### Q3: "Problem skalowalności vector clocks?"
**Odpowiedź:** O(N) rozmiar dla N procesów. Rozwiązania: przycinanie (Dynamo), Interval Tree Clocks (dynamiczne ID), Bloom clocks (probabilistyczne).

---

## 🎯 Kluczowe punkty

1. **Problem:** Brak globalnego zegara w systemach rozproszonych
2. **Lamport:** Skalarny, a → b ⟹ C(a) < C(b), nie odwrotnie
3. **Vector:** a → b ⟺ V(a) < V(b), wykrywa współbieżność
4. **Zastosowania:** Replikacja, debugging, causal broadcast

---

## 📖 Źródła

1. Lamport - "Time, Clocks, and the Ordering of Events" (1978)
2. Fidge, Mattern - "Vector Clocks" (1988)
3. DeCandia et al. - "Dynamo" (Amazon, 2007)
