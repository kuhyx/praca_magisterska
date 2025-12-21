# Pytanie 1: Porównanie automatów i rozpoznawanych klas języków

## Pytanie
**"Porównać 'siłę wyrazu' automatu skończonego, automatu ze stosem oraz maszyny Turinga. Jakie klasy języków rozpoznaje każdy z nich?"**

Przedmiot: AISDI (Algorytmy i Struktury Danych)

---

## 📚 Odpowiedź główna

### Hierarchia Chomsky'ego - fundament teoretyczny

Noam Chomsky w 1956 roku zaproponował hierarchię czterech klas języków formalnych, gdzie każda kolejna klasa zawiera poprzednią:

```
Typ 0: Języki rekurencyjnie przeliczalne (Recursively Enumerable)
   ⊃
Typ 1: Języki kontekstowe (Context-Sensitive)
   ⊃
Typ 2: Języki bezkontekstowe (Context-Free)
   ⊃
Typ 3: Języki regularne (Regular)
```

### 1. Automat Skończony (Finite Automaton - FA)

#### Definicja formalna
Automat skończony to piątka: **M = (Q, Σ, δ, q₀, F)**
- **Q** - skończony zbiór stanów
- **Σ** - alfabet wejściowy (skończony zbiór symboli)
- **δ** - funkcja przejścia: Q × Σ → Q (DFA) lub Q × Σ → P(Q) (NFA)
- **q₀** - stan początkowy (q₀ ∈ Q)
- **F** - zbiór stanów akceptujących (F ⊆ Q)

#### Rozpoznawana klasa języków
**Języki regularne (Typ 3)** - najsłabsza klasa w hierarchii Chomsky'ego

#### Charakterystyka
- **Pamięć**: Brak pamięci pomocniczej - tylko aktualny stan
- **Moc obliczeniowa**: Nie potrafi "liczyć" (porównywać ilości)
- **Równoważne formalizmy**:
  - Wyrażenia regularne (regex)
  - Gramatyki regularne (prawo- lub lewostronnie liniowe)
  - DFA ≡ NFA ≡ ε-NFA (równoważne pod względem mocy)

#### Przykłady języków rozpoznawalnych
- L = {w ∈ {a,b}* : w zawiera podciąg "ab"}
- L = {w ∈ {0,1}* : w jest podzielne przez 3 (interpretowane binarnie)}
- Identyfikatory w językach programowania: `[a-zA-Z_][a-zA-Z0-9_]*`

#### Przykłady języków NIEROZPOZNAWALNYCH
- L = {aⁿbⁿ : n ≥ 0} - wymaga liczenia
- L = {ww : w ∈ {a,b}*} - wymaga zapamiętania w
- Poprawnie zagnieżdżone nawiasy

#### Lemat o pompowaniu (Pumping Lemma) dla języków regularnych
Dla każdego języka regularnego L istnieje stała p (długość pompowania), taka że:
każde słowo w ∈ L, gdzie |w| ≥ p, można podzielić na w = xyz, gdzie:
1. |y| > 0
2. |xy| ≤ p
3. ∀i ≥ 0: xyⁱz ∈ L

---

### 2. Automat ze Stosem (Pushdown Automaton - PDA)

#### Definicja formalna
Automat ze stosem to siódemka: **M = (Q, Σ, Γ, δ, q₀, Z₀, F)**
- **Q** - skończony zbiór stanów
- **Σ** - alfabet wejściowy
- **Γ** - alfabet stosowy
- **δ** - funkcja przejścia: Q × (Σ ∪ {ε}) × Γ → P(Q × Γ*)
- **q₀** - stan początkowy
- **Z₀** - początkowy symbol na stosie
- **F** - zbiór stanów akceptujących

#### Rozpoznawana klasa języków
**Języki bezkontekstowe (Typ 2)** - Context-Free Languages (CFL)

#### Charakterystyka
- **Pamięć**: Stos (LIFO) - pamięć potencjalnie nieskończona, ale z ograniczonym dostępem
- **Moc obliczeniowa**: Potrafi "liczyć" (porównywać pary ilości)
- **DPDA ⊂ NPDA**: Deterministyczne PDA są SŁABSZE niż niedeterministyczne!
- **Równoważne formalizmy**: Gramatyki bezkontekstowe (CFG)

#### Dwa tryby akceptacji
1. **Przez stan końcowy**: automat jest w stanie z F po przeczytaniu całego słowa
2. **Przez pusty stos**: stos jest pusty po przeczytaniu całego słowa

Oba tryby są równoważne pod względem mocy.

#### Przykłady języków rozpoznawalnych
- L = {aⁿbⁿ : n ≥ 0} - klasyczny przykład
- L = {w ∈ {a,b}* : #a(w) = #b(w)} - równa liczba a i b
- Poprawnie zagnieżdżone nawiasy: (), (()), (()()), ...
- Palindromy: L = {wwᴿ : w ∈ {a,b}*}

#### Przykłady języków NIEROZPOZNAWALNYCH
- L = {aⁿbⁿcⁿ : n ≥ 0} - wymaga liczenia trzech rzeczy
- L = {ww : w ∈ {a,b}*} - kopiowanie (nie odwracanie!)
- L = {aⁱbʲcᵏ : i = j lub j = k} - to jest CFL! (suma dwóch CFL)

#### DPDA vs NPDA
**Deterministyczne PDA** rozpoznają **właściwy podzbiór** języków bezkontekstowych:
- DPDA: L = {aⁿbⁿ : n ≥ 0} ✓
- NPDA only: L = {wwᴿ : w ∈ {a,b}*} - palindromy parzyste

---

### 3. Maszyna Turinga (Turing Machine - TM)

#### Definicja formalna
Maszyna Turinga to siódemka: **M = (Q, Σ, Γ, δ, q₀, qaccept, qreject)**
- **Q** - skończony zbiór stanów
- **Σ** - alfabet wejściowy (nie zawiera symbolu pustego ␣)
- **Γ** - alfabet taśmowy (Σ ⊂ Γ, ␣ ∈ Γ)
- **δ** - funkcja przejścia: Q × Γ → Q × Γ × {L, R}
- **q₀** - stan początkowy
- **qaccept** - stan akceptujący
- **qreject** - stan odrzucający

#### Rozpoznawana klasa języków
**Języki rekurencyjnie przeliczalne (Typ 0)** - Recursively Enumerable (RE)

Podklasa: **Języki rekurencyjne (rozstrzygalne)** - TM zawsze się zatrzymuje

#### Charakterystyka
- **Pamięć**: Taśma nieskończona z dostępem swobodnym (R/W)
- **Moc obliczeniowa**: Maksymalna możliwa (teza Churcha-Turinga)
- **DTM ≡ NTM**: Deterministyczne i niedeterministyczne TM są RÓWNOWAŻNE pod względem mocy (ale różnią się złożonością czasową)

#### Warianty równoważne
- Wielotaśmowa TM
- Niedeterministyczna TM
- RAM (Random Access Machine)
- Języki programowania (Turing-complete)

#### Przykłady języków rozpoznawalnych
- L = {aⁿbⁿcⁿ : n ≥ 0}
- L = {ww : w ∈ {a,b}*}
- Wszystkie języki bezkontekstowe
- Wszystkie języki kontekstowe
- Problem stopu (HP) - ale TM może się nie zatrzymać!

#### Przykłady języków NIEROZPOZNAWALNYCH
- Komplement problemu stopu: L = {⟨M,w⟩ : M nie zatrzymuje się na w}
- Problem odpowiedniości Posta (PCP)

---

## 📊 Tabela porównawcza

| Cecha | FA | PDA | TM |
|-------|-----|-----|-----|
| **Pamięć** | Brak (tylko stan) | Stos (LIFO) | Taśma (R/W swobodny) |
| **Klasa języków** | Regularne (Typ 3) | Bezkontekstowe (Typ 2) | Rek. przeliczalne (Typ 0) |
| **Gramatyka** | Regularna | Bezkontekstowa (CFG) | Nieograniczona |
| **DET = NIEDET?** | TAK | NIE | TAK (moc), NIE (złożoność) |
| **Domknięcie ∪** | TAK | TAK | TAK |
| **Domknięcie ∩** | TAK | NIE | TAK |
| **Domknięcie ¬** | TAK | NIE | NIE (RE), TAK (rekurencyjne) |
| **Rozstrzygalność pustości** | TAK | TAK | NIE |
| **Zastosowanie** | Leksery, regex | Parsery, kompilatory | Obliczenia ogólne |

---

## 🔄 Relacje między klasami

```
┌─────────────────────────────────────────────────────────────┐
│                    Typ 0: Rekurencyjnie przeliczalne (TM)   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Rekurencyjne (TM zatrzymująca się)       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │           Typ 1: Kontekstowe (LBA)              │  │  │
│  │  │  ┌───────────────────────────────────────────┐  │  │  │
│  │  │  │      Typ 2: Bezkontekstowe (PDA)          │  │  │  │
│  │  │  │  ┌─────────────────────────────────────┐  │  │  │  │
│  │  │  │  │   Deterministyczne CFL (DPDA)       │  │  │  │  │
│  │  │  │  │  ┌───────────────────────────────┐  │  │  │  │  │
│  │  │  │  │  │   Typ 3: Regularne (FA)       │  │  │  │  │  │
│  │  │  │  │  └───────────────────────────────┘  │  │  │  │  │
│  │  │  │  └─────────────────────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mnemoniki

### "STOS LIFO"
- **S**kończony automat - **S**tan tylko (bez pamięci)
- **T**ylko regex - języki regularne
- **O**graniczony PDA - **O**dnosi się do stosu
- **S**tos = bezkontekstowe

### "TuRing = Total Random access"
- **T**aśma nieskończona
- **R**andom access (czytanie i pisanie)
- **Total** - wszystko może obliczyć (co jest obliczalne)

### "3-2-1 START"
- **3** = Typ 3 = FA = regex (najsłabszy)
- **2** = Typ 2 = PDA = CFG (parser)
- **1** = Typ 1 = kontekstowe (LBA)
- **0** = Typ 0 = TM = wszystko (START od zera = najpotężniejszy)

### "FA NIC nie pamięta, PDA pamięta ALE odwraca, TM pamięta WSZYSTKO"
- FA: nie liczy
- PDA: liczy ale LIFO (stąd aⁿbⁿ tak, aⁿbⁿcⁿ nie)
- TM: liczy wszystko

### Akronim "CHOMSKY" dla hierarchii:
- **C**omputable all (Typ 0 - TM)
- **H**ard context-sensitive (Typ 1)
- **O**K with stack (Typ 2 - PDA)
- **M**inimal - regex only (Typ 3 - FA)
- **S**trict inclusion (każda klasa zawiera niższą)
- **K**ey for compilers (zastosowania)
- **Y**ears of theory (od 1956)

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Udowodnij, że język L = {aⁿbⁿ} nie jest regularny"

**Odpowiedź:**
Stosujemy lemat o pompowaniu. Załóżmy, że L jest regularny z długością pompowania p.

Weźmy w = aᵖbᵖ ∈ L, |w| = 2p ≥ p

Według lematu: w = xyz, gdzie |xy| ≤ p, |y| > 0

Ponieważ |xy| ≤ p, to xy składa się tylko z 'a' (pierwsze p znaków to same 'a').
Zatem y = aᵏ dla pewnego k > 0.

Pompujemy: xy²z = aᵖ⁺ᵏbᵖ

Ale p + k ≠ p, więc xy²z ∉ L. **Sprzeczność!** ∎

---

### Q2: "Dlaczego DPDA ⊂ NPDA, ale DFA = NFA?"

**Odpowiedź:**

**DFA = NFA:**
- Można przekształcić NFA w DFA przez konstrukcję potęgową (subset construction)
- Każdy stan DFA odpowiada podzbiorowi stanów NFA
- Wykładniczy wzrost stanów, ale ta sama moc

**DPDA ⊂ NPDA:**
- PDA ma stos - niedeterminizm pozwala "zgadywać" środek palindromu
- DPDA nie może rozpoznać {wwᴿ} bo nie wie, kiedy kończy się w
- DPDA rozpoznaje języki z własnością prefiksową
- Niedeterminizm w PDA NIE daje się wyeliminować (brak konstrukcji analogicznej do potęgowej dla stosów)

---

### Q3: "Co to jest LBA i gdzie się mieści w hierarchii?"

**Odpowiedź:**
**Linear Bounded Automaton (LBA)** - maszyna Turinga z ograniczoną taśmą:
- Taśma ograniczona do długości liniowej względem wejścia: O(n)
- Rozpoznaje języki kontekstowe (Typ 1)
- NLBA > DLBA? - otwarty problem!
- Przykład: L = {aⁿbⁿcⁿ} - kontekstowy, ale nie bezkontekstowy

---

### Q4: "Jakie są praktyczne zastosowania każdego typu automatu?"

**Odpowiedź:**

| Automat | Zastosowania praktyczne |
|---------|------------------------|
| **FA/DFA** | Leksery (tokenizacja), walidacja regex, kontrolery stanów w grach, protokoły sieciowe, automaty w VHDL/Verilog |
| **PDA** | Parsery (analiza składniowa), kompilatory (CFG), walidacja XML/JSON, sprawdzanie nawiasów |
| **TM** | Model teoretyczny obliczeń, dowody nierozstrzygalności, złożoność obliczeniowa (P vs NP) |

---

### Q5: "Co to jest teza Churcha-Turinga?"

**Odpowiedź:**
**Teza Churcha-Turinga** (nieformalnie):
> "Każda funkcja, która może być obliczona przez jakikolwiek algorytm, może być obliczona przez maszynę Turinga."

**Równoważne formalizmy:**
- Maszyna Turinga
- Rachunek lambda (Church)
- Funkcje rekurencyjne (Gödel)
- Maszyna RAM
- Języki Turing-complete (C, Python, Java...)

**To jest TEZA, nie twierdzenie** - nie można jej udowodnić, bo "algorytm" nie ma formalnej definicji.

---

### Q6: "Czy istnieje język, który nie jest rekurencyjnie przeliczalny?"

**Odpowiedź:**
TAK! Argument przekątniowy (diagonalizacja):

**L_d** = {⟨M⟩ : M nie akceptuje ⟨M⟩}

Ten język nie jest RE (rekurencyjnie przeliczalny).

**Dowód:**
Załóżmy, że TM M_d rozpoznaje L_d.
- Czy M_d akceptuje ⟨M_d⟩?
- Jeśli TAK → ⟨M_d⟩ ∉ L_d → M_d nie powinno akceptować (sprzeczność)
- Jeśli NIE → ⟨M_d⟩ ∈ L_d → M_d powinno akceptować (sprzeczność)

Zatem M_d nie istnieje, więc L_d ∉ RE. ∎

---

## 🎯 Kluczowe punkty do zapamiętania

1. **Hierarchia jest ścisła**: Reg ⊂ CFL ⊂ CSL ⊂ RE
2. **Pamięć = moc**: brak < stos < taśma
3. **FA: DET = NIEDET**, PDA: DET < NIEDET, TM: DET = NIEDET (moc)
4. **Domknięcie na dopełnienie**: FA tak, CFL nie, RE nie
5. **Praktyka**: FA = regex/lexer, PDA = parser, TM = teoria

---

## 📖 Źródła do pogłębienia

1. Hopcroft, Motwani, Ullman - "Introduction to Automata Theory, Languages, and Computation"
2. Sipser - "Introduction to the Theory of Computation"
3. Kozen - "Automata and Computability"
