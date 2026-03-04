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

Pytanie „JAK są katalogowane?" = jaką METODĘ stosujemy, żeby z setek wzorców zrobić przeszukiwalny, porównywalny, kompozytowalny system wiedzy. Odpowiedź: trzy filary, razem tworzące kompletną metodologię.

![Trzy filary katalogowania wzorców](img/q14_three_pillars.png)

**1. Ustandaryzowany szablon opisu (pattern template)** — każdy wzorzec opisany wg tego samego formatu, dzięki czemu można je porównywać „pole po polu". Mnemonik: **NaPSiRoKo**.

| Pole | Skrót | Co zawiera | Przykład (Observer, GoF) |
|------|-------|------------|--------------------------|
| **Nazwa** | **Na** | jedno słowo/fraza | Observer |
| **Problem** | **P** | kiedy stosować? | Obiekt zmienia stan → wielu zależnych musi zareagować, ale nie chcemy ich hard-codować |
| **Siły** | **Si** | konkurencyjne wymagania | loose coupling vs koszt powiadomień (100 obserwatorów = 100 wywołań) |
| **Rozwiązanie** | **Ro** | struktura + zachowanie | Subject trzyma listę Observer; przy zmianie woła notify() na każdym |
| **Konsekwencje** | **Ko** | tradeoffs +/− | (+) luźne wiązanie, (−) kaskada powiadomień, memory leaks jeśli nie odrejestrujemy |
| Powiązane | — | wzorce pokrewne | Mediator (centralizuje), Pub/Sub (rozproszony wariant) |
| Znane zastosowania | — | real-world | Java Swing listeners, C# events, React useState → re-render |

![Wypełniona karta wzorca Observer](img/q14_observer_card_filled.png)

**2. Klasyfikacja wieloosiowa** — wzorce organizowane wzdłuż kilku osi jednocześnie, jak książki w bibliotece (dział + półka + autor).

Osie klasyfikacji:
- **Skala**: architektoniczny (cały system) → projektowy (klasa) → idiomatyczny (linia kodu)
- **Domena problemu**: kreacyjne / strukturalne / behawioralne (GoF) albo warstwy / komunikacja / dekompozycja (POSA)
- **Atrybut jakościowy**: wydajność, skalowalność, testowalność, dostępność

Konkretny przykład — jak GoF klasyfikuje 23 wzorce na dwóch osiach:

| | Kreacyjne (5) | Strukturalne (7) | Behawioralne (11) |
|---|---|---|---|
| **Klasa** | Factory Method | Adapter (class) | Interpreter, Template Method |
| **Obiekt** | Abstract Factory, Builder, Prototype, Singleton | Adapter (obj), Bridge, Composite, Decorator, Facade, Flyweight, Proxy | Chain of Resp., Command, Iterator, Mediator, Memento, **Observer**, State, Strategy, Visitor |

Observer jest w komórce: **behawioralny × obiekt**. Wiedzieć GDZIE wzorzec leży = szybsze przypomnienie i porównanie z sąsiadami (Mediator, State, Strategy — też behawioralne obiektowe).

![Mapa katalogów wzorców](img/q14_catalog_map.png)

**3. Język wzorców (pattern language)** — wzorce referują się wzajemnie, tworząc nawigacyjny graf „zobacz też". Sens: masz problem → stosujesz wzorzec A → A rodzi nowy problem → wzorzec B go rozwiązuje.

Konkretna nawigacja w praktyce:

    Problem: „monolith nie skaluje się"
        ↓
    Wzorzec: Microservices
        ↓ wymaga
    Problem: „jak routować żądania do serwisów?"
        ↓
    Wzorzec: API Gateway
        ↓ rodzi problem
    Problem: „co gdy serwis nie odpowiada?"
        ↓
    Wzorzec: Circuit Breaker
        ↓ rodzi problem
    Problem: „jak zachować spójność transakcji?"
        ↓
    Wzorzec: Saga

Każdy wzorzec w katalogu ma pole „Powiązane wzorce" — to linki w tym grafie.

![Nawigacja w języku wzorców](img/q14_pattern_language_navigation.png)

**Konkretne katalogi** (5 głównych — mnemonik **PGEP+C** = „Paweł Grał Efektownie Pod Chmurami"):

| Katalog | Rok | Autorzy | Skala | Domena | Przykładowe wzorce |
|---------|-----|---------|-------|--------|--------------------|
| **POSA** | 1996 | Buschmann et al. | architektoniczny | systemy | Layers, Pipes & Filters, Broker, MVC, Microkernel |
| **GoF** | 1994 | Gamma, Helm, Johnson, Vlissides | projektowy | obiekty | Factory, Singleton, Observer, Strategy (23 łącznie) |
| **EIP** | 2003 | Hohpe & Woolf | integracyjny | komunikacja między-systemowa | Message Channel, Router, Aggregator |
| **PoEAA** | 2002 | Martin Fowler | projektowy/arch. | enterprise | Repository, Unit of Work, Domain Model, Active Record |
| **Cloud** | ~2015 | Microsoft/AWS | architektoniczny | chmura | Circuit Breaker, Sidecar, Saga, Strangler Fig |

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

**Mnemonik 1 — szablon wzorca „NaPSiRoKo":**
- **Na**zwa → **P**roblem → **Si**ły → **Ro**związanie → **Ko**nsekwencje
- Historyjka: „**Na**pisałem **P**roblem na kartce, **Si**ły mnie ciągnęły w dwie strony, **Ro**związałem go, a **Ko**nsekwencje spisałem na odwrocie"
- Wyobraź sobie kartonowe pudełko: etykieta (Nazwa) → co nie działa (Problem) → wagi na szalce (Siły) → instrukcja montażu (Rozwiązanie) → lista „+" i „−" na boku (Konsekwencje)

**Mnemonik 2 — katalogi „PGEP+C" = „Paweł Grał Efektownie Pod Chmurami":**

    P = POSA     (1996, systemy)        „Paweł"
    G = GoF      (1994, obiekty)        „Grał"
    E = EIP      (2003, integracja)     „Efektownie"
    P = PoEAA    (2002, enterprise)     „Pod"
    C = Cloud    (~2015, chmura)        „Chmurami"

- Chronologicznie: GoF '94 → POSA '96 → PoEAA '02 → EIP '03 → Cloud ~'15
- Skala rośnie: GoF (obiekty) → PoEAA (aplikacja) → POSA/EIP (system) → Cloud (infrastruktura)

**Mnemonik 3 — trzy filary katalogowania „SzKlaJ" = „Szklany Jar":**
- **Sz**ablon opisu (NaPSiRoKo) — każde hasło w tym samym formacie
- **Kla**syfikacja wieloosiowa — hasła posortowane w kategorie (jak dział w bibliotece)
- **J**ęzyk wzorców — hasła mają „zobacz też" (graf nawigacyjny)
- Analogia: encyklopedia. Każde hasło ma ten sam format (**Sz**ablon), jest w kategorii z innymi hasłami tego typu (**Kla**syfikacja), i ma „zobacz też" (**J**ęzyk wzorców)

**Mnemonik 4 — GoF 3 kategorie „KSB" = „Kto Stworzył Budynek?":**
- **K**reacyjne (5) — JAK tworzyć obiekty? (Factory, Singleton, Builder, Prototype, Abstract Factory)
- **S**trukturalne (7) — JAK składać obiekty? (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy)
- **B**ehawioralne (11) — JAK obiekty komunikują? (Observer, Strategy, Command, State, Iterator...)
- Zapamiętaj liczby: 5 + 7 + 11 = 23

**Szybka ściąga — wzorzec na obronie:**
- Wzorzec = Nazwa + Problem + Rozwiązanie + Konsekwencje (minimum do zapamiętania z dowolnego katalogu)
- „Monolith first" — rozdzielaj gdy znasz granice domen
- Katalogi wg skali: POSA = systemy, GoF = obiekty, EIP = komunikacja międzysystemowa

→ Diagramy do druku:
- `pytania/img/q14_pattern_template.png` — szablon NaPSiRoKo
- `pytania/img/q14_catalog_map.png` — mapa katalogów PGEP+C
- `pytania/img/q14_three_pillars.png` — trzy filary katalogowania
- `pytania/img/q14_observer_card_filled.png` — wypełniona karta wzorca Observer
- `pytania/img/q14_pattern_language_navigation.png` — nawigacja w języku wzorców

---

### 🎮 Mostek do pracy magisterskiej — wzorce w silnikach gier

> Silniki gier to największe repozytorium wzorców architektonicznych i projektowych w praktyce. Moja praca verwendet 6 kluczowych wzorców.

![Wzorce w silnikach gier — mapa](img/q14_engine_patterns_map.png)

#### 6 wzorców użytych w mojej pracy

| # | Wzorzec | Gdzie w Unity (C#) | Gdzie w Unreal (C++) | Kategoria GoF/POSA |
|---|---------|---------------------|----------------------|---------------------|
| 1 | **Component** | `MonoBehaviour` + `GetComponent<T>()` | `UActorComponent` + `CreateDefaultSubobject<T>()` | Strukturalny (GoF: Strategy wariant) |
| 2 | **Object Pool** | `BulletPool.cs` — `Queue<Bullet>` | `TPooledObject<ABullet>` | Kreacyjny (gamedev-specific) |
| 3 | **Observer** | `event Action OnEnemyDeath` | `DECLARE_DYNAMIC_MULTICAST_DELEGATE()` | Behawioralny (GoF) |
| 4 | **Game Loop** | `Update()` / `FixedUpdate()` / `LateUpdate()` | `Tick()` / `TickComponent()` | Architektoniczny (gamedev-specific) |
| 5 | **Singleton** | `GameDirector.Instance` (MonoBehaviour) | `UGameInstance` / Subsystem | Kreacyjny (GoF) — kontrowersyjny! |
| 6 | **ECS** | Unity DOTS: `IComponentData` + `SystemBase` | Unreal Mass Entity: `FMassEntityManager` | Architektoniczny (data-oriented) |

#### Katalogi wzorców gamedev

| Katalog | Autor | Ile wzorców | Kluczowe dla mojej pracy |
|---------|-------|-------------|--------------------------|
| „Game Programming Patterns" | Robert Nystrom | 19 | Component, Object Pool, Game Loop, Observer |
| GoF (Design Patterns, 1994) | Gamma et al. | 23 | Observer, Singleton, Strategy, State |
| POSA (Pattern-Oriented SA) | Buschmann et al. | 25+ | Layers, Pipes-and-Filters, Broker |

#### Mnemonik — „KOGLES" = Komponent Observer Game-Loop ECS Singleton

- **K**omponent (Component Pattern — fundamentalny)
- **O**bserver (event-driven gameplay)
- **G**ame Loop (Update/Tick — serce silnika)
- **L**ayers (Renderer → Physics → Logic → Audio → Input)
- **E**CS (Entity Component System — data-oriented design)
- **S**ingleton (GameDirector.Instance — globalny stan)

Na obronie: *„W mojej implementacji bullet-hell zidentyfikowałem 6 wzorców architektonicznych. Najważniejszy to Component Pattern — Unity i Unreal oparły na nim całą architekturę. Object Pool eliminuje alokacje (GC spikes), a Observer zapewnia loose coupling między podsystemami. Wzorce te odpowiadają katalogowi Nystroma 'Game Programming Patterns' i GoF."*

---

### 📚 Odniesienia do publikacji z Katedry

> Poniższe notatki pochodzą z publikacji promotorów/recenzentów i mogą być przydatne jako dodatkowy kontekst na obronie.

**Borowa, Zalewski, Kijas — „What rationales drive architectural decisions? An empirical inquiry" (ECSA 2023):**
- Uzasadnienia (rationale) za wyborem wzorca architektonicznego to najczęściej: łatwość użycia dla dev, maintainability, performance, wcześniejsza wiedza i ograniczenia czasowe
- Implikacja: wybór wzorca (np. Microservices vs Monolith) jest często napędzany doświadczeniem zespołu i deadlinem, nie tylko analizą tradeoffs
- Wzorce powinny mieć udokumentowane rationale (→ ADR), bo decyzje bez jawnego uzasadnienia mogą wynikać z biasów

**Borowa, Zalewski — „The influence of cognitive biases on architectural technical debt" (ICSA 2021):**
- **Błędy poznawcze prowadzą do złych wyborów wzorców:**
  - Zakotwiczenie (anchoring) + optymizm → „Architectural Lock-in" — zespół trzyma się wybranego wzorca mimo rosnących problemów
  - Confirmation bias → „Re-inventing the wheel" — budowanie od zera zamiast użycia istniejącego wzorca/frameworka
  - Bandwagon effect → wybór Microservices „bo wszyscy tak robią", bez analizy czy skala projektu to uzasadnia
- Wzorce architektoniczne jako **narzędzie debiasujące**: katalogowane rozwiązania wymuszają rozważenie alternatyw i tradeoffs, co przeciwdziała zakotwiczeniu

**Borowa — „The technical debt gamble: A case study on TD in a large-scale industrial microservice architecture" (ScienceDirect 2025):**
- Case study dużego systemu mikroserwisowego — dług techniczny narasta gdy decyzje o wzorcach są podejmowane pod presją czasu
- Wzorce jak Microservices wymagają świadomego zarządzania TD, bo złożoność operacyjna generuje dług

**Borowa et al. — „Reframing Technical Debt — Dagstuhl Perspectives Workshop 24452":**
- 5 values, 5 beliefs, 9 principles zarządzania TD
- Architektura jako kluczowy wymiar TD — nieodpowiednie wzorce architektoniczne to główne źródło długu technicznego
- Zasada: „TD jest nieunikniony, ale ZARZĄDZALNY" — świadomy wybór wzorca + dokumentacja (ADR) + regularny przegląd

