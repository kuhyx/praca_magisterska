# Pytanie 16: Wzorce architektoniczne

## Pytanie
**"Czemu służą wzorce architektoniczne? Jak powstają? Jak są katalogowane? Omówić przykładowe wzorce architektoniczne."**

Przedmiot: AIS (Architektura i Integracja Systemów)

---

## 📚 Odpowiedź główna

### 1. Cel wzorców architektonicznych

| Cel | Opis |
|-----|------|
| **Reużywalność** | Sprawdzone rozwiązania typowych problemów |
| **Komunikacja** | Wspólne słownictwo ("używamy MVC") |
| **Dokumentacja** | Zapis wiedzy architektonicznej |
| **Jakość** | Adresowanie atrybutów jakościowych |
| **Edukacja** | Nauka z doświadczeń innych |

---

### 2. Jak powstają wzorce

```
┌─────────────────────────────────────────────────────────────────┐
│  1. PROBLEM pojawia się wielokrotnie                           │
│                    ↓                                            │
│  2. Różni architekci znajdują PODOBNE ROZWIĄZANIA              │
│                    ↓                                            │
│  3. UOGÓLNIENIE - wyodrębnienie wspólnych elementów            │
│                    ↓                                            │
│  4. DOKUMENTACJA w formie wzorca                               │
│                    ↓                                            │
│  5. WALIDACJA przez społeczność (peer review)                  │
│                    ↓                                            │
│  6. KATALOGOWANIE w książkach/repozytoriach                    │
└─────────────────────────────────────────────────────────────────┘
```

**Format opisu wzorca:**
- **Nazwa** - identyfikator
- **Kontekst** - kiedy stosować
- **Problem** - co rozwiązuje
- **Rozwiązanie** - struktura i zachowanie
- **Konsekwencje** - trade-offs
- **Znane zastosowania** - przykłady

---

### 3. Katalogowanie wzorców

| Katalog | Zakres | Przykłady |
|---------|--------|-----------|
| **POSA** (Pattern-Oriented Software Architecture) | Architektura | Layers, Pipes&Filters |
| **GoF** (Gang of Four) | Projektowe | Factory, Observer |
| **EIP** (Enterprise Integration Patterns) | Integracja | Message Router, Aggregator |
| **PoEAA** (Fowler) | Enterprise | Repository, Unit of Work |
| **Cloud Patterns** | Chmura | Circuit Breaker, Sidecar |

---

### 4. Przykładowe wzorce architektoniczne

#### Layered Architecture (Warstwy)

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │  UI, Controllers
├─────────────────────────────────────────┤
│         Business Logic Layer            │  Services, Domain
├─────────────────────────────────────────┤
│         Data Access Layer               │  Repositories, ORM
├─────────────────────────────────────────┤
│         Database                        │  SQL, NoSQL
└─────────────────────────────────────────┘

Zasada: Warstwa zna tylko warstwę bezpośrednio niższą
+ Separacja odpowiedzialności
- Sztywność, boilerplate
```

#### Microservices

```
┌─────┐   ┌─────┐   ┌─────┐
│User │   │Order│   │Inv- │
│Svc  │   │Svc  │   │entory│
└──┬──┘   └──┬──┘   └──┬──┘
   │         │         │
   └────┬────┴────┬────┘
        │         │
   ┌────┴────┐    │
   │API Gate │────┘
   │  way    │
   └─────────┘

+ Niezależne wdrożenia, skalowalność
- Złożoność operacyjna, komunikacja
```

#### Event-Driven Architecture (EDA)

```
┌──────────┐     event     ┌──────────┐
│ Producer │ ───────────→  │  Event   │
└──────────┘               │  Broker  │
                           │(Kafka)   │
┌──────────┐     event     └────┬─────┘
│ Consumer │ ←─────────────────┘
│    A     │
└──────────┘
┌──────────┐     event
│ Consumer │ ←─────────────────┘
│    B     │
└──────────┘

+ Loose coupling, skalowalność
- Eventual consistency, debugging
```

#### CQRS (Command Query Responsibility Segregation)

```
          Commands                    Queries
              │                          │
              ↓                          ↓
       ┌──────────┐              ┌──────────┐
       │  Write   │              │   Read   │
       │  Model   │              │  Model   │
       └────┬─────┘              └────┬─────┘
            │                         │
            ↓                         ↓
       ┌──────────┐   sync      ┌──────────┐
       │  Write   │ ─────────→  │   Read   │
       │   DB     │             │   DB     │
       └──────────┘             └──────────┘

+ Optymalizacja read/write osobno
- Złożoność, eventual consistency
```

#### Hexagonal Architecture (Ports & Adapters)

```
           ┌─────────────────────────────────────┐
           │         Application Core            │
           │  ┌───────────────────────────────┐  │
  Adapter  │  │                               │  │  Adapter
  (REST) ──┼──│►  Port     Domain     Port  ◄├──┼── (DB)
           │  │   (in)     Logic      (out)   │  │
           │  └───────────────────────────────┘  │
           └─────────────────────────────────────┘

+ Testowalność, niezależność od frameworków
- Więcej kodu (adaptery)
```

#### Saga Pattern (dla transakcji rozproszonych)

```
Orchestration:
┌─────────┐    cmd    ┌─────────┐    cmd    ┌─────────┐
│  Saga   │ ───────→  │ Service │ ───────→  │ Service │
│Orchestr.│ ←─reply── │    A    │ ←─reply── │    B    │
└─────────┘           └─────────┘           └─────────┘
     │
     │ compensation (rollback) jeśli błąd
     ↓

Choreography:
Service A ──event──→ Service B ──event──→ Service C
     ↑                                        │
     └────────── compensation event ──────────┘
```

---

### 5. Porównanie wzorców

| Wzorzec | Skalowalność | Złożoność | Use Case |
|---------|--------------|-----------|----------|
| **Monolith** | Niska | Niska | MVP, małe zespoły |
| **Layered** | Średnia | Niska | Enterprise CRUD |
| **Microservices** | Wysoka | Wysoka | Duże systemy |
| **Event-Driven** | Wysoka | Średnia | Real-time, IoT |
| **CQRS** | Wysoka | Wysoka | Read-heavy systems |

---

## 🧠 Mnemoniki

### "LAMP = Layers, API Gateway, Microservices, Pub/Sub":
Ewolucja architektur

### "CQRS = Commands mutate, Queries read":
Rozdzielenie zapisu od odczytu

### "Hexagonal = Inside-Out testing":
Core nie zna zewnętrznych szczegółów

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy wybrać monolith zamiast microservices?"
**Odpowiedź:** Mały zespół (<10), MVP, niejasne granice domen, brak DevOps maturity. "Monolith first" - rozdzielaj gdy wiesz gdzie granice.

### Q2: "Jak CQRS współpracuje z Event Sourcing?"
**Odpowiedź:** Event Sourcing zapisuje zdarzenia (nie stan), CQRS buduje read model z eventów. Razem: audit trail, time-travel, ale złożoność.

### Q3: "Co to jest Strangler Fig Pattern?"
**Odpowiedź:** Migracja z monolitu do microservices. Nowe funkcje jako mikroserwisy, stare stopniowo zastępowane. Routing przez facade. Nazwa od figi dusiciela.

---

## 🎯 Kluczowe punkty

1. **Wzorce** = sprawdzone rozwiązania typowych problemów
2. **Katalogi:** POSA, GoF, EIP, PoEAA
3. **Layered** = separacja, proste, sztywne
4. **Microservices** = niezależność, złożoność ops
5. **Event-Driven** = loose coupling, eventual consistency
6. **CQRS** = osobne modele read/write

---

## 📖 Źródła

1. Buschmann et al. - "POSA Vol. 1"
2. Fowler - "Patterns of Enterprise Application Architecture"
3. Hohpe, Woolf - "Enterprise Integration Patterns"
4. Richardson - "Microservices Patterns"
