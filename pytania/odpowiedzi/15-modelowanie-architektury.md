# Pytanie 15: Metody modelowania architektury systemów informatycznych

## Pytanie
**"Omówić metody modelowania architektury systemów informatycznych. Przedstawić cele i metody modelowania architektury."**

Przedmiot: AIS (Architektura i Integracja Systemów)

---

## 📚 Odpowiedź główna

### 1. Cele modelowania architektury

| Cel | Opis |
|-----|------|
| **Komunikacja** | Wspólny język dla stakeholderów |
| **Dokumentacja** | Zapis decyzji architektonicznych |
| **Analiza** | Weryfikacja atrybutów jakościowych |
| **Planowanie** | Roadmapa rozwoju systemu |
| **Zarządzanie złożonością** | Abstrakcja, dekompozycja |

---

### 2. Frameworki architektoniczne

#### TOGAF (The Open Group Architecture Framework)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADM (Architecture Development Method)         │
│                                                                 │
│                         Preliminary                             │
│                             ↓                                   │
│              ┌─── A. Architecture Vision ───┐                   │
│              ↓                              ↓                   │
│    H. Architecture    ←───────────→    B. Business            │
│    Change Mgmt                         Architecture            │
│              ↑                              ↓                   │
│    G. Implementation  ←── Requirements ── C. Information       │
│    Governance              Management      Systems Arch        │
│              ↑                              ↓                   │
│    F. Migration       ←───────────→    D. Technology          │
│    Planning                            Architecture            │
│              ↑                              ↓                   │
│              └─── E. Opportunities & Solutions ───┘            │
└─────────────────────────────────────────────────────────────────┘
```

**Domeny TOGAF:**
- Business Architecture
- Data Architecture  
- Application Architecture
- Technology Architecture

#### Zachman Framework

```
         │ What    │ How     │ Where   │ Who     │ When    │ Why
─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────
Planner  │ Data    │ Function│ Network │ People  │ Time    │ Motivation
Owner    │ Entity  │ Process │ Location│ Org     │ Schedule│ Goals
Designer │ Model   │ System  │ Distrib │ Role    │ Workflow│ Rules
Builder  │ Schema  │ Program │ Infra   │ UI      │ Control │ Logic
         │         │         │         │         │         │
```

#### 4+1 View Model (Kruchten)

```
                    ┌─────────────────┐
                    │   Scenarios     │
                    │   (Use Cases)   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Logical     │   │   Process     │   │  Development  │
│   View        │   │   View        │   │   View        │
│ (funkcjonalna)│   │ (współbieżn.) │   │ (organizacja) │
└───────────────┘   └───────────────┘   └───────────────┘
                             │
                    ┌────────┴────────┐
                    │   Physical      │
                    │   View          │
                    │ (wdrożenie)     │
                    └─────────────────┘
```

---

### 3. Notacje i języki modelowania

#### UML (Unified Modeling Language)

| Diagram | Zastosowanie |
|---------|--------------|
| **Component** | Struktura modułów |
| **Deployment** | Fizyczne rozmieszczenie |
| **Package** | Organizacja logiczna |
| **Sequence** | Interakcje czasowe |

#### ArchiMate

```
┌─────────────────────────────────────────────────────────────────┐
│ Warstwy ArchiMate:                                              │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ Business Layer    │ Actor, Role, Process, Service, Event   ││
│ ├─────────────────────────────────────────────────────────────┤│
│ │ Application Layer │ Component, Interface, Function, Service ││
│ ├─────────────────────────────────────────────────────────────┤│
│ │ Technology Layer  │ Node, Device, Network, Artifact         ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ Aspekty: Passive (data), Behavior (process), Active (actor)    │
└─────────────────────────────────────────────────────────────────┘
```

#### C4 Model (Simon Brown)

```
Level 1: System Context    - System w kontekście użytkowników
Level 2: Container         - Aplikacje, bazy, serwisy
Level 3: Component         - Wewnętrzna struktura kontenera
Level 4: Code              - Klasy, interfejsy (opcjonalnie)

Zasada: Zoom in/out między poziomami
```

---

### 4. ADR (Architecture Decision Records)

```markdown
# ADR-001: Wybór bazy danych

## Status: Accepted

## Context
System wymaga przechowywania danych użytkowników...

## Decision
Wybieramy PostgreSQL

## Consequences
+ Dojrzały, stabilny
+ Wsparcie JSON
- Wymaga DBA
```

---

### 5. Metody analizy architektury

#### ATAM (Architecture Tradeoff Analysis Method)

```
Fazy:
1. Present architecture
2. Identify quality attribute scenarios
3. Generate quality attribute utility tree
4. Analyze architectural approaches
5. Identify sensitivity & tradeoff points
6. Generate risks & non-risks
```

#### Quality Attributes (ISO 25010)

| Atrybut | Opis |
|---------|------|
| **Performance** | Czas odpowiedzi, throughput |
| **Security** | CIA (Confidentiality, Integrity, Availability) |
| **Scalability** | Horizontal/Vertical scaling |
| **Maintainability** | Modyfikowalność, testowalność |
| **Reliability** | MTBF, MTTR |

---

## 🧠 Mnemoniki

### "TOGAF ADM = A-H cycle":
A-Vision, B-Business, C-IS, D-Tech, E-Opportunities, F-Migration, G-Governance, H-Change

### "C4 = Context, Container, Component, Code":
4 poziomy zoomu architektury

### "4+1 = LDPP + Scenarios":
Logical, Development, Process, Physical + Scenarios

---

## ❓ Pytania dodatkowe

### Q1: "Jaka jest różnica między TOGAF a Zachman?"
**Odpowiedź:** TOGAF to metodyka (proces ADM), Zachman to taksonomia (klasyfikacja artefaktów). TOGAF mówi JAK tworzyć architekturę, Zachman CO dokumentować.

### Q2: "Kiedy używać C4 vs ArchiMate?"
**Odpowiedź:** C4 dla programistów (proste, 4 poziomy), ArchiMate dla enterprise architects (formalne, warstwy biznes-aplikacja-technologia).

---

## 🎯 Kluczowe punkty

1. **TOGAF** = metodyka ADM + 4 domeny
2. **4+1** = 5 widoków (Logical, Process, Development, Physical, Scenarios)
3. **C4** = 4 poziomy zoomu
4. **ArchiMate** = 3 warstwy (Business, Application, Technology)
5. **ADR** = dokumentacja decyzji

---

## 📖 Źródła

1. TOGAF 9.2 Standard - The Open Group
2. Kruchten - "4+1 View Model"
3. Simon Brown - "C4 Model" (c4model.com)
4. ArchiMate 3.1 Specification
