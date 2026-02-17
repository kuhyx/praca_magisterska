## PYTANIE 14/28: Wzorce architektoniczne (AIS)

**Czemu służą? Jak powstają? Jak są katalogowane? Przykłady.**

---

### Tło pojęciowe — słowniczek

**Wzorzec (pattern)** — udokumentowane, powtarzalne rozwiązanie typowego problemu. Format: Nazwa + Problem (kiedy stosować) + Rozwiązanie (struktura) + Konsekwencje (tradeoffs). To nie gotowy kod — to szablon myślowy, który adaptujemy do kontekstu.

**Wzorzec architektoniczny (architectural pattern)** — wzorzec definiujący CAŁKOWITĄ strukturę systemu: jak podzielić na komponenty, jak komunikują się, jak skalować. Większa skala niż wzorzec projektowy (design pattern), który dotyczy pojedynczej klasy/obiektu.

    Skala wzorców:
    Architektoniczny: Microservices, Layered, Event-Driven  (cały system)
    Projektowy:       Singleton, Observer, Factory            (klasa/obiekt)
    Idiomatyczny:     RAII, for-each                          (linia kodu)

---

**Monolith (monolit)** — cały system jako jedna aplikacja, jeden deployment. Prosty, łatwy na start. Problemy: trudne skalowanie (skalujesz wszystko albo nic), długie buildy, duże ryzyko przy zmianach.

**Layered (warstwowy)** — system podzielony na warstwy, każda zależna od niższej: Presentation → Business Logic → Data Access → Database. Separacja odpowiedzialności. Wada: każde żądanie przechodzi przez WSZYSTKIE warstwy (overhead).

    [Presentation]  ← UI, API
          ↓
    [Business Logic] ← reguły domenowe
          ↓
    [Data Access]    ← SQL, ORM
          ↓
    [Database]       ← PostgreSQL

**Microservices (mikroserwisy)** — system rozbity na małe, niezależne serwisy, każdy z własną bazą danych i deploymentem. Każdy serwis odpowiada za jedną domenę (np. zamówienia, płatności, użytkownicy). Zalety: niezależne skalowanie, niezależne deployments, różne technologie. Wady: złożoność operacyjna (sieć, monitoring, transakcje rozproszone).

**Event-Driven Architecture (EDA)** — komunikacja przez zdarzenia (events). Producer generuje event → Broker (np. Kafka) → Consumers reagują. Loose coupling — producent nie wie kto konsumuje. Eventual consistency.

---

**CQRS (Command Query Responsibility Segregation)** — osobne modele do zapisu (Command) i odczytu (Query). Command model zoptymalizowany do walidacji i zapisu, Query model zoptymalizowany do szybkiego odczytu (np. zdenormalizowane widoki). Złożony, ale potężny przy asymetrii read/write.

    Command → [Write DB] → Event → [Read DB projekcja] → Query
    Zapis i odczyt mają osobne schematy!

**Hexagonal (Ports & Adapters, Alistair Cockburn)** — rdzeń domeny (business logic) jest niezależny od frameworków, baz danych, UI. Komunikuje się przez „porty" (interfejsy). „Adaptery" implementują porty (np. adapter PostgreSQL, adapter REST). Korzyść: testowalność — możesz podmienić adapter na mock.

---

**Katalogi wzorców:**
- **POSA (Pattern-Oriented Software Architecture)** — 5-tomowa seria o wzorcach architektonicznych: Layers, Pipes & Filters, Broker, MVC, Microkernel.
- **GoF (Gang of Four)** — Gamma, Helm, Johnson, Vlissides. 23 wzorce projektowe (nie architektoniczne): kreacyjne (Factory, Singleton), strukturalne (Adapter, Decorator), behawioralne (Observer, Strategy). Książka z 1994 r.
- **EIP (Enterprise Integration Patterns)** — Hohpe & Woolf. Wzorce komunikacji między systemami: Message Channel, Content-Based Router, Aggregator.
- **PoEAA (Patterns of Enterprise Application Architecture)** — Martin Fowler. Wzorce aplikacji enterprise: Repository, Unit of Work, Domain Model, Active Record.
- **Cloud Patterns** — Microsoft Azure Architecture Center, AWS Well-Architected. Wzorce chmurowe: Circuit Breaker, Sidecar, Saga, Strangler Fig.

---

**Skalowalność (scalability)** — zdolność systemu do obsługi rosnącego obciążenia. W kontekście wzorców: monolith → skalowalność niska (scale up), microservices → wysoka (scale out per serwis).

**Loose coupling (luźne wiązanie)** — komponenty mają minimalne zależności. Zmiana jednego nie wymaga zmiany drugiego. Event-Driven i Microservices promują loose coupling.

**Separacja odpowiedzialności (separation of concerns)** — każdy komponent odpowiada za jedną rzecz. Fundamentalna zasada stojąca za wzorcami warstwowymi, hexagonal, CQRS.

**Eventual consistency (spójność ostateczna)** — dane mogą być chwilowo niespójne, ale „w końcu" się zsynchronizują. Cena za skalowalność i loose coupling w systemach rozproszonych (EDA, Microservices).

---

**Christopher Alexander** — architekt budynków (nie programista!), ojciec idei wzorców w inżynierii. W książce „A Pattern Language" (1977) opisał 253 wzorców architektonicznych — budowlanych. GoF zaadaptowali jego format do oprogramowania. Kluczowa idea: wzorzec to nie luźna rada, ale skodyfikowane rozwiązanie z ustandaryzowanym opisem.

**Forma opisu wzorca (pattern template)** — standardowy szablon, w jakim kataloguje się każdy wzorzec. To serce odpowiedzi na „JAK są katalogowane?" — każdy wzorzec opisany jest według ustalonej struktury, dzięki czemu można je porównywać, przeszukiwać i komponować. Pola szablonu: Nazwa → Kontekst/Problem → Siły (forces) → Rozwiązanie → Konsekwencje → Powiązane wzorce → Znane zastosowania. Różne katalogi mają różne warianty szablonu (GoF ma 13 pól, forma Aleksandryjska jest bardziej narracyjna), ale rdzeń jest wspólny.

**Siły (forces)** — konkurencyjne wymagania, które wzorzec próbuje pogodzić. Np. wzorzec Layered godzi testowalność vs wydajność: warstwy ułatwiają testowanie, ale dodają overhead. Siły to serce wzorca — wyjaśniają DLACZEGO dane rozwiązanie jest kompromisem, a nie „idealnym rozwiązaniem na wszystko".

**Klasyfikacja wzorców (pattern classification)** — sposób organizacji wzorców wewnątrz katalogu. Główne osie klasyfikacji:
- **Skala/zasięg**: architektoniczny (cały system) → projektowy (klasa/obiekt) → idiomatyczny (linia kodu)
- **Domena problemu**: np. GoF dzieli 23 wzorce na kreacyjne (5), strukturalne (7), behawioralne (11)
- **Atrybut jakościowy**: wydajność, skalowalność, dostępność, testowalność
- **Domena zastosowania**: enterprise, chmura, integracja, embedded

**Język wzorców (pattern language)** — zbiór wzorców, które wzajemnie się referują, tworząc nawigacyjną sieć. Wzorzec „Microservices" referuje „API Gateway", „Service Discovery", „Circuit Breaker". Można „czytać" język wzorców jak przepis: „zacznij od X → jeśli problem Y → zastosuj Z". To trzeci filar katalogowania obok szablonu opisu i klasyfikacji.

---

### Cel: reużywalne rozwiązania typowych problemów, wspólne słownictwo, dokumentacja wiedzy

### Powstawanie: Problem powtarzalny → Podobne rozwiązania → Uogólnienie → Dokumentacja → Walidacja → Katalogowanie

### Katalogowanie — trzy filary metodologii

**1. Ustandaryzowany szablon opisu** — każdy wzorzec opisany wg tego samego formatu:
- **Nazwa** — jedno słowo/fraza: „Layered", „Observer"
- **Problem/Kontekst** — kiedy stosować
- **Siły (forces)** — konkurencyjne wymagania do pogodzenia
- **Rozwiązanie** — struktura, diagram, zachowanie
- **Konsekwencje** — tradeoffs: co zyskujemy, co tracimy
- **Powiązane wzorce** — jakie wzorce współgrają lub konkurują
- **Znane zastosowania** — real-world examples

**2. Klasyfikacja wieloosiowa** — wzorce organizowane wzdłuż kilku osi jednocześnie:
- **Skala**: architektoniczny (cały system) → projektowy (klasa) → idiomatyczny (linia kodu)
- **Domena problemu**: kreacyjne / strukturalne / behawioralne (GoF) albo warstwy / komunikacja / dekompozycja (POSA)
- **Atrybut jakościowy**: wydajność, skalowalność, testowalność, dostępność

**3. Język wzorców (pattern language)** — wzorce referują się wzajemnie, tworząc graf:
- Microservices → wymaga → API Gateway, Service Discovery, Circuit Breaker
- Observer → wariant architektoniczny → Event-Driven Architecture
- Nawigacja: „mam problem X → wzorzec A → prowadzi do problemu Y → wzorzec B"

**Konkretne katalogi:**
- **POSA** (1996) — wzorce architektoniczne: Layers, Pipes & Filters, Broker, MVC, Microkernel
- **GoF** (1994) — 23 wzorce projektowe: kreacyjne (5), strukturalne (7), behawioralne (11)
- **EIP** (2003) — wzorce integracji: Message Channel, Router, Aggregator
- **PoEAA** (2002) — enterprise: Repository, Unit of Work, Domain Model, Active Record
- **Cloud Patterns** (~2015) — chmurowe: Circuit Breaker, Sidecar, Saga, Strangler Fig

### Przykładowe wzorce

**Layered (Warstwy):** Presentation → Business Logic → Data Access → DB. Separacja odpowiedzialności. Sztywne, boilerplate.

**Microservices:** Niezależne serwisy, osobne wdrożenia, skalowalność. Złożoność operacyjna.

**Event-Driven (EDA):** Producer → Event Broker (Kafka) → Consumers. Loose coupling, eventual consistency.

**CQRS:** Osobne modele Read/Write. Optymalizacja per-strona. Złożoność.

**Hexagonal (Ports & Adapters):** Core niezależny od frameworków. Testowalność.

| Wzorzec        | Skalowalność | Złożoność | Use Case            |
|----------------|--------------|-----------|---------------------|
| Monolith       | Niska        | Niska     | MVP, małe zespoły   |
| Layered        | Średnia      | Niska     | Enterprise CRUD     |
| Microservices  | Wysoka       | Wysoka    | Duże systemy        |
| Event-Driven   | Wysoka       | Średnia   | Real-time, IoT      |

### Etymologia

**POSA** — Pattern-Oriented Software Architecture (Buschmann et al., 1996). **GoF** — Gang of Four: Gamma, Helm, Johnson, Vlissides (1994, „Design Patterns"). **EIP** — Enterprise Integration Patterns (Hohpe & Woolf, 2003). **PoEAA** — Patterns of Enterprise Application Architecture (Martin Fowler, 2002). **Hexagonal** — Alistair Cockburn (2005); kształt sześciokąta nie ma specjalnego znaczenia. **CQRS** — Command Query Responsibility Segregation (Greg Young, ~2010); oparty na CQS Bertranda Meyera. **Microservices** — termin spopularyzowany ~2012 (James Lewis, Martin Fowler).

### Jak zapamiętać

- **Mnemonik katalogów „PGEP+C"**: **P**OSA → **G**oF → **E**IP → **P**oEAA + **C**loud
  - Historia: „**P**aweł **G**rał **E**fektownie **P**od **C**hmurami"
  - Chronologicznie: GoF '94 → POSA '96 → PoEAA '02 → EIP '03 → Cloud ~'15
- **Szablon wzorca „NaPSiRoKo"**: **Na**zwa, **P**roblem, **Si**ły, **Ro**związanie, **Ko**nsekwencje
  - Wyobraź sobie kartonowe pudełko: etykieta (Nazwa) → co nie działa (Problem) → wagi na szalce (Siły) → instrukcja montażu (Rozwiązanie) → lista „+" i „−" na boku (Konsekwencje)
- **3 filary katalogowania**: Szablon + Klasyfikacja + Język wzorców
  - Analogia do encyklopedii: każde hasło ma ten sam format (szablon), jest w kategorii z innymi hasłami tego typu (klasyfikacja), i ma „zobacz też" (język wzorców)
- **„Monolith first"** — rozdzielaj gdy znasz granice domen
- **Wzorzec = Nazwa + Problem + Rozwiązanie + Konsekwencje** (minimum do zapamiętania z dowolnego katalogu)
- Katalogi wg skali: POSA = systemy, GoF = obiekty, EIP = komunikacja międzysystemowa

→ Diagramy do druku: `pytania/img/q14_pattern_template.png`, `pytania/img/q14_catalog_map.png`

