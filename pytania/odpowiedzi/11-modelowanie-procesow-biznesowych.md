# Pytanie 11: Standardy i narzędzia do modelowania procesów biznesowych

## Pytanie
**"Scharakteryzować standardy i narzędzia do modelowania procesów biznesowych."**

Przedmiot: WSYZ (Wstęp do Systemów Zarządzania)

---

## 📚 Odpowiedź główna

### Wprowadzenie

**Modelowanie procesów biznesowych** to graficzne przedstawienie przepływu pracy, działań i decyzji w organizacji. Służy do:
- Dokumentowania procesów
- Analizy i optymalizacji
- Automatyzacji (workflow, BPM)
- Komunikacji między działami

---

## 1. Główne standardy modelowania

### Przegląd standardów

```
┌─────────────────────────────────────────────────────────────────┐
│                 STANDARDY MODELOWANIA PROCESÓW                  │
├─────────────────┬─────────────────┬─────────────────────────────┤
│      BPMN       │      UML        │        EPC                  │
│  Business       │  Activity       │  Event-driven               │
│  Process Model  │  Diagrams       │  Process Chain              │
│  and Notation   │                 │                             │
├─────────────────┼─────────────────┼─────────────────────────────┤
│     IDEF0       │   Flowcharts    │   Value Stream Map          │
│  Function       │  (Schematy      │   (Lean Manufacturing)      │
│  Modeling       │   blokowe)      │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

---

## 2. BPMN (Business Process Model and Notation)

### Charakterystyka

- **Standard:** OMG (Object Management Group)
- **Wersja aktualna:** BPMN 2.0 (2011)
- **Cel:** Uniwersalny język dla analityków, architektów i programistów
- **Format:** Graficzny + XML (dla automatyzacji)

### Podstawowe elementy BPMN

#### Flow Objects (Obiekty przepływu)

```
┌─────────────────────────────────────────────────────────────────┐
│ ZDARZENIA (Events)                                              │
│                                                                 │
│   ○    Zdarzenie startowe (Start Event)                        │
│                                                                 │
│   ◎    Zdarzenie pośrednie (Intermediate Event)                │
│                                                                 │
│   ◉    Zdarzenie końcowe (End Event)                           │
│                                                                 │
│ Modyfikatory: Timer ⏱, Message ✉, Error ⚡, Signal 📶          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ CZYNNOŚCI (Activities)                                          │
│                                                                 │
│   ┌─────────┐                                                   │
│   │         │    Zadanie (Task) - atomowa czynność             │
│   └─────────┘                                                   │
│                                                                 │
│   ┌─────────┐                                                   │
│   │ [+]     │    Podproces (Sub-Process) - zagnieżdżony        │
│   └─────────┘                                                   │
│                                                                 │
│ Typy zadań: User, Service, Script, Manual, Send, Receive       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ BRAMKI (Gateways)                                               │
│                                                                 │
│   ◇     Exclusive (XOR) - jeden z wielu ścieżek               │
│                                                                 │
│   ◆     Parallel (AND) - wszystkie ścieżki równolegle         │
│                                                                 │
│   ○◇    Inclusive (OR) - jedna lub więcej ścieżek             │
│                                                                 │
│   ⊕     Event-based - wybór na podstawie zdarzenia            │
└─────────────────────────────────────────────────────────────────┘
```

#### Connecting Objects (Łączniki)

| Symbol | Nazwa | Użycie |
|--------|-------|--------|
| ────→ | Sequence Flow | Kolejność czynności |
| - - -→ | Message Flow | Komunikacja między uczestnikami |
| · · ·→ | Association | Powiązanie z artefaktem |

#### Swimlanes (Tory)

```
┌─────────────────────────────────────────────────────────────────┐
│ Pool: Firma XYZ                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Lane: Dział Sprzedaży                                           │
│   ○────→[Przyjmij zamówienie]────→◇────→[Potwierdź]           │
├─────────────────────────────────────────────────────────────────┤
│ Lane: Magazyn                                                   │
│                                    └──→[Skompletuj]────→◉      │
└─────────────────────────────────────────────────────────────────┘
```

#### Artefakty

| Symbol | Nazwa | Użycie |
|--------|-------|--------|
| 📄 | Data Object | Dane wejściowe/wyjściowe |
| 📁 | Data Store | Baza danych, repozytorium |
| 📝 | Annotation | Komentarz |
| [ ] | Group | Grupowanie elementów |

### Przykład procesu BPMN

```
┌─────────────────────────────────────────────────────────────────┐
│ Proces: Obsługa reklamacji                                      │
│                                                                 │
│  ○────→[Przyjmij      ]────→◇────→[Weryfikuj    ]────→◇       │
│        [reklamację    ]      │     [produkt     ]      │       │
│                              │                         │       │
│                        [Brak danych]            [OK]   │[NOK]  │
│                              │                   │     │       │
│                              ↓                   │     ↓       │
│                        [Poproś o    ]            │  [Odrzuć   ]│
│                        [uzupełnienie]            │  [reklamację]│
│                              │                   │     │       │
│                              └─────────────────→◆←────┘       │
│                                                  │              │
│                                                  ↓              │
│                                           [Wyślij      ]       │
│                                           [odpowiedź   ]       │
│                                                  │              │
│                                                  ↓              │
│                                                  ◉              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. UML Activity Diagrams

### Charakterystyka

- **Standard:** OMG (część UML 2.x)
- **Cel:** Modelowanie przepływu sterowania i danych
- **Pochodzenie:** Rozszerzenie flowcharts + Petri nets

### Elementy Activity Diagrams

```
┌─────────────────────────────────────────────────────────────────┐
│ WĘZŁY AKCJI                                                     │
│                                                                 │
│   ╭─────────╮                                                   │
│   │ Akcja   │    Action Node - pojedyncza czynność             │
│   ╰─────────╯                                                   │
│                                                                 │
│   ╭──[warunek]──╮                                               │
│   │   Akcja     │    z Guard - akcja warunkowa                 │
│   ╰─────────────╯                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WĘZŁY STERUJĄCE                                                 │
│                                                                 │
│   ●     Initial Node (początek)                                │
│   ◉     Activity Final (koniec całości)                        │
│   ⊗     Flow Final (koniec przepływu)                          │
│                                                                 │
│   ◇     Decision/Merge Node                                    │
│   ▬     Fork/Join Node (równoległość)                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PRZEPŁYW OBIEKTÓW                                               │
│                                                                 │
│   [Zamówienie]    Object Node                                  │
│                                                                 │
│   ▭▭▭▭▭▭▭▭▭▭     Datastore                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Porównanie BPMN vs UML Activity

| Cecha | BPMN | UML Activity |
|-------|------|--------------|
| **Cel** | Procesy biznesowe | Logika oprogramowania |
| **Odbiorcy** | Analitycy, biznes | Programiści, architekci |
| **Swimlanes** | Pool/Lane | Partition |
| **Zdarzenia** | Bogate (timer, message...) | Ograniczone |
| **Automatyzacja** | BPEL, silniki BPM | Generowanie kodu |

---

## 4. EPC (Event-driven Process Chain)

### Charakterystyka

- **Pochodzenie:** ARIS (Architecture of Integrated Information Systems)
- **Twórca:** Prof. August-Wilhelm Scheer (1992)
- **Zastosowanie:** SAP, modelowanie procesów ERP

### Elementy EPC

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ⬡     Zdarzenie (Event) - pasywne, opisuje stan             │
│         np. "Zamówienie otrzymane"                              │
│                                                                 │
│   ▭     Funkcja (Function) - aktywna, opisuje działanie       │
│         np. "Sprawdź dostępność"                                │
│                                                                 │
│   ∧     AND - wszystkie ścieżki                                │
│   ∨     OR - jedna lub więcej                                  │
│   XOR   XOR - dokładnie jedna                                  │
│                                                                 │
│   ○     Organizational Unit                                    │
│   □     Information Object                                     │
│   ◇     IT System                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Reguły EPC

1. **Start i koniec:** Zdarzenie
2. **Naprzemienność:** Zdarzenie → Funkcja → Zdarzenie
3. **Łączniki:** Między zdarzeniami a funkcjami

```
EPC: Proces zamówienia

   ⬡ Zamówienie otrzymane
          │
          ↓
   ▭ Sprawdź dostępność
          │
          ↓
        XOR
       /   \
      ↓     ↓
⬡ Produkt   ⬡ Produkt
  dostępny    niedostępny
      │          │
      ↓          ↓
▭ Przygotuj  ▭ Złóż 
  wysyłkę      zamówienie
      │        u dostawcy
      ↓          │
⬡ Wysyłka      ↓
  gotowa     ⬡ Zamówienie
               złożone
```

---

## 5. IDEF (Integration DEFinition)

### Rodzina IDEF

| Standard | Nazwa | Zastosowanie |
|----------|-------|--------------|
| **IDEF0** | Function Modeling | Hierarchia funkcji |
| **IDEF1** | Information Modeling | Struktura danych |
| **IDEF1X** | Data Modeling | Bazy danych (ERD) |
| **IDEF3** | Process Description | Przepływ procesów |
| **IDEF4** | Object-Oriented Design | Projektowanie OO |
| **IDEF5** | Ontology Description | Ontologie |

### IDEF0 - Modelowanie funkcji

```
┌─────────────────────────────────────────────────────────────────┐
│                        KONTROLA (C)                             │
│                             │                                   │
│                             ↓                                   │
│   WEJŚCIE (I) ────→  ┌───────────┐  ────→ WYJŚCIE (O)          │
│                      │  FUNKCJA  │                              │
│                      └───────────┘                              │
│                             ↑                                   │
│                             │                                   │
│                       MECHANIZM (M)                             │
│                                                                 │
│   I = Input (co jest przetwarzane)                             │
│   C = Control (reguły, ograniczenia)                           │
│   O = Output (rezultat)                                         │
│   M = Mechanism (kto/co wykonuje)                              │
└─────────────────────────────────────────────────────────────────┘
```

### Dekompozycja IDEF0

```
Poziom 0: A0 - Całość procesu
    │
    ├── A1 - Podfunkcja 1
    │    ├── A11
    │    ├── A12
    │    └── A13
    │
    ├── A2 - Podfunkcja 2
    │
    └── A3 - Podfunkcja 3
```

---

## 6. Inne notacje i podejścia

### Flowcharts (Schematy blokowe)

```
┌─────────────────────────────────────────────────────────────────┐
│ Symbole:                                                        │
│                                                                 │
│   ⬭     Terminal (Start/End)                                   │
│   ▭     Process (Operacja)                                     │
│   ◇     Decision (Decyzja)                                     │
│   ▱     I/O (Wejście/Wyjście)                                  │
│   ─→    Flow (Przepływ)                                        │
└─────────────────────────────────────────────────────────────────┘
```

**Zalety:** Proste, uniwersalne, znane
**Wady:** Brak standaryzacji, niewystarczające dla złożonych procesów

### Value Stream Map (VSM)

```
┌─────────────────────────────────────────────────────────────────┐
│ Lean Manufacturing                                              │
│                                                                 │
│ Supplier ──→ [Magazyn] ──→ [Produkcja] ──→ [QC] ──→ Customer   │
│              Inv: 5d        PT: 2h         PT: 30min           │
│                             CT: 45s                             │
│                                                                 │
│ PT = Processing Time (czas przetwarzania)                      │
│ CT = Cycle Time (czas cyklu)                                   │
│ Inv = Inventory (zapas)                                        │
│                                                                 │
│ Cel: Identyfikacja MUDA (marnotrawstwo)                        │
└─────────────────────────────────────────────────────────────────┘
```

### Petri Nets (Sieci Petriego)

```
┌─────────────────────────────────────────────────────────────────┐
│ Formalizm matematyczny dla współbieżności                       │
│                                                                 │
│   ○     Place (Miejsce) - stan                                 │
│   ▭     Transition (Przejście) - akcja                         │
│   ●     Token (Żeton) - znacznik                               │
│                                                                 │
│   ●○────→▭────→○                                               │
│                                                                 │
│ Zastosowanie: Analiza deadlocków, weryfikacja formalna         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Narzędzia do modelowania

### Przegląd narzędzi

| Narzędzie | Standardy | Typ | Cena |
|-----------|-----------|-----|------|
| **Bizagi Modeler** | BPMN | Dedykowane | Free/Paid |
| **Camunda Modeler** | BPMN, DMN | Open Source | Free |
| **Signavio** | BPMN, EPC | Cloud | Paid |
| **ARIS** | EPC, BPMN | Enterprise | Paid |
| **Enterprise Architect** | UML, BPMN | Uniwersalne | Paid |
| **Lucidchart** | Wszystkie | Cloud | Free/Paid |
| **draw.io** | Wszystkie | Free | Free |
| **Visio** | Flowcharts, BPMN | Desktop | Paid |
| **ProcessMaker** | BPMN | BPM Suite | Paid |
| **Bonita** | BPMN | Open Source | Free/Paid |

### Funkcjonalności narzędzi

| Funkcja | Podstawowe | Zaawansowane |
|---------|------------|--------------|
| Modelowanie graficzne | ✓ | ✓ |
| Walidacja modelu | ✗ | ✓ |
| Symulacja | ✗ | ✓ |
| Wykonywanie (engine) | ✗ | ✓ |
| Eksport (XML, PDF) | ✓ | ✓ |
| Współpraca | ✗/Cloud | ✓ |
| Integracja z IT | ✗ | ✓ |

---

## 📊 Porównanie standardów

| Cecha | BPMN | UML Activity | EPC | IDEF0 |
|-------|------|--------------|-----|-------|
| **Cel główny** | Procesy biznesowe | Logika systemu | Procesy ERP | Funkcje |
| **Złożoność** | Średnia-wysoka | Średnia | Średnia | Niska |
| **Automatyzacja** | Tak (BPEL) | Częściowo | Tak (SAP) | Nie |
| **Popularność** | Bardzo wysoka | Wysoka | Średnia (SAP) | Niska |
| **Krzywa uczenia** | Stroma | Średnia | Płaska | Płaska |
| **Standaryzacja** | OMG (ISO) | OMG | ARIS | NIST |

---

## 🧠 Mnemoniki

### "BPMN = Business Process Modeling Notation":
- **B**iznesowe procesy
- **P**ule i tory (swimlanes)
- **M**odele graficzne + XML
- **N**otacja standardowa (OMG)

### "EPC = Event → Process → Control":
- **E**vent startuje i kończy
- **P**roces (funkcja) działa
- **C**ontrol przez XOR/AND/OR

### "ICOM" dla IDEF0:
- **I**nput - co wchodzi
- **C**ontrol - co kontroluje
- **O**utput - co wychodzi
- **M**echanism - kto/co wykonuje

### "Bramki BPMN - X AND OR":
- **X** (XOR) - wyłącznie jedna ścieżka
- **AND** (+) - wszystkie ścieżki
- **OR** (○) - jedna lub więcej

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Jakie są poziomy dojrzałości modelowania procesów?"

**Odpowiedź:**

**CMMI-like dla BPM:**

| Poziom | Nazwa | Charakterystyka |
|--------|-------|-----------------|
| 1 | **Initial** | Ad-hoc, brak dokumentacji |
| 2 | **Repeatable** | Podstawowa dokumentacja |
| 3 | **Defined** | Procesy zdefiniowane, BPMN |
| 4 | **Managed** | Mierzone KPI, optymalizacja |
| 5 | **Optimizing** | Ciągłe doskonalenie, automatyzacja |

---

### Q2: "Co to jest BPEL i jak się ma do BPMN?"

**Odpowiedź:**

**BPEL (Business Process Execution Language)** = język XML do wykonywania procesów przez silniki workflow.

```
BPMN (graficzny) → eksport → BPEL (XML) → silnik BPM → wykonanie
```

| Cecha | BPMN | BPEL |
|-------|------|------|
| Format | Graficzny | XML |
| Cel | Modelowanie | Wykonanie |
| Odbiorcy | Analitycy | Systemy IT |
| Czytelność | Wysoka | Niska |

---

### Q3: "Jakie metryki procesów można monitorować?"

**Odpowiedź:**

**KPI procesów biznesowych:**

| Metryka | Opis | Przykład |
|---------|------|----------|
| **Cycle Time** | Czas od początku do końca | 5 dni na zamówienie |
| **Throughput** | Liczba zakończonych instancji | 100 zamówień/dzień |
| **Cost per Transaction** | Koszt pojedynczej instancji | 50 PLN/zamówienie |
| **Error Rate** | Procent błędów/odrzuceń | 2% reklamacji |
| **SLA Compliance** | Zgodność z umową | 95% w terminie |
| **Resource Utilization** | Wykorzystanie zasobów | 80% czasu pracy |

---

### Q4: "Czym różni się proces od procedury?"

**Odpowiedź:**

| Aspekt | Proces | Procedura |
|--------|--------|-----------|
| **Definicja** | CO robimy (flow) | JAK robimy (instrukcja) |
| **Zakres** | End-to-end | Pojedyncza czynność |
| **Format** | Diagram (BPMN) | Tekst, checklist |
| **Cel** | Optymalizacja, automatyzacja | Standaryzacja, jakość |
| **Przykład** | Proces reklamacji | Procedura weryfikacji produktu |

---

### Q5: "Co to jest DMN i jak współpracuje z BPMN?"

**Odpowiedź:**

**DMN (Decision Model and Notation)** = standard OMG do modelowania decyzji.

```
BPMN: [Oceń ryzyko kredytowe] ←── połączenie ──→ DMN: Tabela decyzyjna
                                                      ┌─────────────┐
                                                      │Dochód │Wynik│
                                                      │>10k   │ OK  │
                                                      │<10k   │ NOK │
                                                      └─────────────┘
```

**Zalety:**
- Oddzielenie logiki decyzji od przepływu
- Łatwiejsze utrzymanie reguł biznesowych
- Zrozumiałe dla biznesu (tabele decyzyjne)

---

### Q6: "Jakie są zasady poprawnego modelowania BPMN?"

**Odpowiedź:**

**Dobre praktyki:**

1. **Jeden start, jeden koniec** (per proces)
2. **Nazwy = czasownik + rzeczownik** ("Sprawdź zamówienie")
3. **Bramki w parach** (split → merge)
4. **Unikaj krzyżowania linii**
5. **Swimlanes = role, nie osoby**
6. **Poziom szczegółowości = cel modelu**
7. **Happy path główny, wyjątki osobno**

**Błędy częste:**
- Brak bramki po decyzji
- Mieszanie XOR i AND bez merge
- Zbyt szczegółowe lub zbyt ogólne

---

## 🎯 Kluczowe punkty do zapamiętania

1. **BPMN** = standard przemysłowy, OMG, automatyzacja
2. **UML Activity** = dla programistów, część UML
3. **EPC** = SAP, zdarzenia-funkcje-łączniki
4. **IDEF0** = hierarchia funkcji, ICOM
5. **Narzędzia:** Bizagi, Camunda, draw.io, Visio
6. **Cel:** Dokumentacja → Analiza → Optymalizacja → Automatyzacja

---

## 📖 Źródła do pogłębienia

1. OMG - "Business Process Model and Notation (BPMN) 2.0"
2. Weske, M. - "Business Process Management"
3. Dumas, M. et al. - "Fundamentals of Business Process Management"
4. Scheer, A.-W. - "ARIS - Business Process Modeling"
