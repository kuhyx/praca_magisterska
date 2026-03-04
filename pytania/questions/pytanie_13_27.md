## PYTANIE 13/27: Modelowanie architektury systemów informatycznych (AIS)

**Cele i metody modelowania architektury.**

---

### Tło pojęciowe — słowniczek

**Architektura systemu informatycznego (software/system architecture)** — fundamentalne decyzje projektowe dotyczące struktury systemu: jakie komponenty, jak się komunikują, jakie technologie. Jak plan architektoniczny budynku — definiuje „kształt" systemu przed budową.

**Modelowanie architektury** — tworzenie uproszczonych reprezentacji (diagramów, opisów) systemu na różnych poziomach abstrakcji. Cele: komunikacja w zespole, dokumentacja, analiza jakości (czy system będzie wydajny? skalowalny?), planowanie rozwoju.

---

**Framework architektoniczny (architecture framework)** — ustrukturyzowane podejście do opisywania architektury. Definiuje: jakie widoki (views) tworzyć, jakie aspekty uwzględnić, w jakiej kolejności pracować.

**TOGAF (The Open Group Architecture Framework)** — najpopularniejszy framework enterprise architecture. Definiuje metodykę ADM (Architecture Development Method) — cykliczny proces tworzenia architektury. 4 domeny:
- **Business** — procesy organizacji
- **Data** — struktury danych
- **Application** — aplikacje i ich interakcje
- **Technology** — infrastruktura (serwery, sieci)

**ADM (Architecture Development Method)** — cykliczny proces TOGAF: Preliminary → Vision → Business Arch → IS Arch → Technology Arch → Opportunities → Migration → Governance. Iteracyjny — można wracać do wcześniejszych faz.

**4+1 View Model (Kruchten)** — model pięciu perspektyw architektury:
- **Logical View** — funkcjonalność (klasy, moduły)
- **Process View** — współbieżność, przepływ danych
- **Development View** — organizacja kodu (pakiety, warstwy)
- **Physical View** — wdrożenie na sprzęt (serwery, kontenery)
- **+1 Scenarios** — use cases łączące wszystkie widoki

    Dlaczego 4+1? Bo różni interesariusze patrzą na system inaczej:
    programista → Development View, admin → Physical View,
    użytkownik → Scenarios, architekt → Logical View

**Zachman Framework** — taksonomia 6×6: pytania CO/JAK/GDZIE/KTO/KIEDY/DLACZEGO × poziomy abstrakcji (kontekst → logiczny → fizyczny → ...). Nie mówi JAK modelować — mówi CO należy udokumentować. Kompletny, ale złożony.

---

**C4 Model (Simon Brown)** — pragmatyczny model: 4 poziomy zoomu diagramów:
1. **Context** — system w otoczeniu (kto go używa, z czym się integruje)
2. **Container** — kontenery techniczne (app server, DB, SPA, API)
3. **Component** — moduły wewnątrz kontenera
4. **Code** — klasy, interfejsy (opcjonalnie, np. UML)

Zaleta: prosty, zrozumiały dla nie-architektów. Zaczynasz od „big picture" i zanurzasz się głębiej.

**ArchiMate** — język modelowania The Open Group. 3 warstwy (Business, Application, Technology) × 3 aspekty (Active Structure — kto?, Behavior — co robi?, Passive Structure — na czym?). Komplementarny z TOGAF.

---

**UML (Unified Modeling Language)** — uniwersalny język modelowania. W kontekście architektury: **Component Diagram** (moduły i zależności), **Deployment Diagram** (mapowanie na sprzęt), **Sequence Diagram** (interakcje w czasie).

**ADR (Architecture Decision Records)** — lekka dokumentacja: każda kluczowa decyzja architektoniczna zapisana jako plik z: kontekstem, decyzją, konsekwencjami. Wersjonowane w repo. Format: „Zdecydowaliśmy X, bo Y. Konsekwencje: Z."

**ATAM (Architecture Tradeoff Analysis Method)** — metoda oceny architektury przez scenariusze jakościowe. Identyfikuje tradeoffs: „ta decyzja poprawia wydajność kosztem modyfikowalności". Opracowana przez SEI (Carnegie Mellon).

**Quality Attributes (atrybuty jakości, ISO 25010)** — mierzalne cechy systemu: Performance, Security, Scalability, Maintainability, Reliability, Usability, Portability, Compatibility. Architektura determinuje osiągalne atrybuty jakości.

---

### Diagramy — wizualizacja modeli architektonicznych

Poniższe diagramy ilustrują kluczowe frameworki i modele omówione w pytaniu. Wszystkie modelują architekturę systemu, ale z różnych perspektyw i na różnych poziomach abstrakcji.

**TOGAF ADM — cykl iteracyjny:**

![TOGAF ADM — cykl Architecture Development Method](img/togaf_adm.png)

**4+1 View Model (Kruchten) — 5 perspektyw:**

![4+1 View Model — 4 widoki + Scenarios](img/4plus1_view_model.png)

**C4 Model — 4 poziomy zoomu (Context → Container → Component → Code):**

![C4 Model — 4 poziomy zoomu](img/c4_model.png)

**Zachman Framework — taksonomia 6×6 (pytania × perspektywy):**

![Zachman Framework — siatka taksonomii](img/zachman_framework.png)

**ArchiMate — 3 warstwy × 3 aspekty:**

![ArchiMate — warstwy i aspekty](img/archimate_layers.png)

---

### Cele: komunikacja, dokumentacja, analiza jakości, planowanie, zarządzanie złożonością

### Frameworki

**TOGAF** — metodyka ADM (Architecture Development Method), 4 domeny: Business, Data, Application, Technology.

**4+1 View Model (Kruchten):**
- Logical (funkcjonalność), Process (współbieżność), Development (organizacja kodu), Physical (wdrożenie), + Scenarios (use cases)

**Zachman Framework** — taksonomia 6×6: What/How/Where/Who/When/Why × poziomy abstrakcji.

**C4 Model (Simon Brown):**
- Level 1: System Context → Level 2: Container → Level 3: Component → Level 4: Code

**ArchiMate** — 3 warstwy: Business, Application, Technology × 3 aspekty: Active, Behavior, Passive.

### Notacje: UML (Component, Deployment, Sequence), ArchiMate, C4, ADR (Architecture Decision Records)

### Analiza: ATAM (Architecture Tradeoff Analysis Method), Quality Attributes (ISO 25010: Performance, Security, Scalability, Maintainability, Reliability)

### Etymologia

**TOGAF** — The Open Group Architecture Framework. **Zachman** — John Zachman (IBM, 1987); framework nazwany od twórcy. **C4** — 4 × C: Context, Container, Component, Code (Simon Brown, 2006). **ArchiMate** — „Architecture" + „animate" (The Open Group). **ATAM** — Architecture Tradeoff Analysis Method (SEI, Carnegie Mellon). **Kruchten** — Philippe Kruchten (Rational/IBM, 1995); 4+1 View Model. **ISO 25010** — międzynarodowy standard atrybutów jakości oprogramowania.

### Jak zapamiętać

---

#### 0. LISTA WSZYSTKICH 5 FRAMEWORKÓW

TOGAF, Zachman, C4, 4+1, ArchiMate

Mnemonic: **„Tomek Zachował Cztery Ciastka Archimedesowi"**

    T  → TOGAF          (metodyka — JAK budować)
    Z  → Zachman        (taksonomia — CO dokumentować)
    C4 → C4 Model       (4 poziomy zoomu diagramów)
    C  → Cztery+1 (4+1) (5 perspektyw Kruchtena)
    A  → ArchiMate      (język/notacja modelowania)

Podział ról — kto robi co:

    TOGAF    = PROCES (jak budować architekturę krok po kroku)
    Zachman  = TAKSONOMIA (co dokumentować — siatka pytań)
    4+1      = PERSPEKTYWY (kto patrzy na system — 5 widoków)
    C4       = ZOOM (jak głęboko patrzysz — 4 poziomy)
    ArchiMate = JĘZYK (jakim językiem rysujesz diagramy)

Mnemonic ról: **„PTZJZ"** — **„Proces, Taksonomia, Zoom, Jakby-pięć-oczu, Żargon"**

---

#### 1. TOGAF — 4 domeny: Business, Data, Application, Technology

Mnemonic: **„BDAT"** → **„Buduj Domy Ale Tanio"**

    B → Business    (procesy organizacji — CO firma robi)
    D → Data        (struktury danych — JAKIE dane)
    A → Application (aplikacje — CZYM realizujemy)
    T → Technology  (infrastruktura — NA CZYM to stoi)

Kolejność = od abstrakcji do konkretu:
firma → dane → apki → serwery

---

#### 2. TOGAF ADM — 8 faz cyklu

Preliminary → Vision → Business → IS → Technology → Opportunities → Migration → Governance

Mnemonic: **„PVB-IT-OMG!"**

    P → Preliminary      (przygotowanie)
    V → Vision           (wizja architektury)
    B → Business Arch    (architektura biznesowa)
    I → IS Arch          (Information Systems — dane + aplikacje)
    T → Technology Arch  (infrastruktura)
    O → Opportunities    (szanse i rozwiązania)
    M → Migration        (plan migracji)
    G → Governance       (nadzór/zarządzanie)

Wyobraź sobie: Planujesz wizję biznesu, IT daje możliwości, migrujesz i zarządzasz — **„PVB-IT-OMG!"** (jakbyś krzyknął „OMG!" na koniec projektu)

---

#### 3. 4+1 View Model (Kruchten) — 5 widoków

Logical, Development, Process, Physical + Scenarios

Mnemonic: **„LoDeProFi + Scenariusz"** albo **„LDPP+S"**

    L → Logical     (klasy, moduły — CO system robi)
    D → Development (pakiety, warstwy — JAK kod zorganizowany)
    P → Process     (współbieżność — JAK przepływają dane)
    P → Physical    (serwery, kontenery — GDZIE wdrożony)
    S → Scenarios   (+1 — use cases łączące wszystko)

Mnemonic-historia: **„Logik Deweloper Procesuje Fizycznie Scenę"**

Kto patrzy na który widok — mnemonic par:

    Architekt   → Logical     „Architekt LOGICZNIE myśli"
    Programista → Development „Programista DEVELOPUJE"
    Integrator  → Process     „Integrator scala PROCESY"
    Admin       → Physical    „Admin zarządza FIZYCZNYMI serwerami"
    Użytkownik  → Scenarios   „Użytkownik ma SCENARIUSZ użycia"

---

#### 4. Zachman — 6 pytań

What, How, Where, Who, When, Why

Mnemonic: **„Co Jak Gdzie Kto Kiedy Dlaczego"** → **„CJGKKD"**

→ **„Co Jan Gotuje? Kurczaka, Kiełbasę i Dynię"**

    Co      → What  (dane, encje)
    Jak     → How   (procesy, funkcje)
    Gdzie   → Where (lokalizacje, sieci)
    Kto     → Who   (ludzie, role)
    Kiedy   → When  (zdarzenia, cykl)
    Dlaczego → Why  (cele, motywacje)

Zachman vs TOGAF — klucz: **„Zachman = MAPA (co dokumentować), TOGAF = GPS (jak dojść)"**

---

#### 5. C4 Model — 4 poziomy zoomu

Context → Container → Component → Code

Mnemonic: **„4 × C = Coraz Ciekawsze Części Codu"**

    C1 → Context    (cały system z lotu ptaka — KTO go używa)
    C2 → Container  (zoom: kontenery techniczne — API, DB, SPA)
    C3 → Component  (zoom: moduły wewnątrz kontenera)
    C4 → Code       (zoom: klasy, interfejsy — opcjonalny)

Wyobraź sobie Google Maps:

    Context   = widok kontynentu (cały system w otoczeniu)
    Container = widok miasta (budynki = kontenery techniczne)
    Component = widok ulicy (pokoje wewnątrz budynku)
    Code      = widok mebli (detale — klasy, metody)

---

#### 6. ArchiMate — 3 warstwy × 3 aspekty

Warstwy: Business, Application, Technology → **BAT** → **„BATman jest architektem"**

    B → Business     (procesy biznesowe)
    A → Application  (aplikacje)
    T → Technology   (infrastruktura)

Aspekty: Active Structure, Behavior, Passive Structure → **ABP** → **„Aktor Biega Pasywnie"**

    A → Active Structure   (KTO działa — aktorzy, komponenty)
    B → Behavior           (CO robi — procesy, usługi)
    P → Passive Structure  (NA CZYM — obiekty danych, artefakty)

Siatka 3×3 — wyobraź sobie tabelkę:

    Aspekt →     Active (KTO)    Behavior (CO)    Passive (NA CZYM)
    ───────────────────────────────────────────────────────────────
    Business     aktor bizn.     proces bizn.     obiekt bizn.
    Application  komponent       usługa           obiekt danych
    Technology   węzeł/serwer    infrastruktura   artefakt

---

#### 7. UML — 3 diagramy architektoniczne

Component, Deployment, Sequence → **CDS** → **„Co Dzień Sekwencja"**

    C → Component   (moduły i zależności między nimi)
    D → Deployment   (mapowanie modułów → serwery/sprzęt)
    S → Sequence     (kto do kogo wysyła komunikaty w czasie)

Mnemonic-historia: **„Komponent Deploy'ujesz i Sekwencyjnie testujesz"**

---

#### 8. Quality Attributes (ISO 25010) — 8 atrybutów

Performance, Security, Scalability, Maintainability, Reliability, Usability, Portability, Compatibility

Mnemonic: **„PS SM RUPC"** → **„Pan Stefan Spotkał Małą Rudą Uczącą Polskiego Codziennie"**

    P → Performance      (wydajność — jak szybko)
    S → Security         (bezpieczeństwo — jak chroniony)
    S → Scalability      (skalowalność — jak rośnie)
    M → Maintainability  (utrzymywalność — jak łatwo zmienić)
    R → Reliability      (niezawodność — jak rzadko pada)
    U → Usability        (użyteczność — jak łatwy w użyciu)
    P → Portability      (przenośność — jak łatwo przenieść)
    C → Compatibility    (kompatybilność — jak współpracuje)

Alternatywny podział na pary:

    „Szybki i Bezpieczny" → Performance + Security
    „Rośnie i Zmienia się" → Scalability + Maintainability
    „Niezawodny i Łatwy"  → Reliability + Usability
    „Przenośny i Zgodny"  → Portability + Compatibility

---

#### 9. Cele modelowania — 5 celów

Komunikacja, Dokumentacja, Analiza jakości, Planowanie, Zarządzanie złożonością

Mnemonic: **„KDAPZ"** → **„Każdy Dobry Architekt Planuje Złożoność"**

    K → Komunikacja            (zespół się rozumie)
    D → Dokumentacja           (wiedza nie ginie)
    A → Analiza jakości        (czy będzie wydajne?)
    P → Planowanie             (co budować dalej)
    Z → Zarządzanie złożonością (okiełznać chaos)

---

#### 10. ADR — struktura

Kontekst → Decyzja → Konsekwencje → **KDK**

Mnemonic: **„Kanapka: Kromka – Dżem – Kromka"**

    K → Kontekst       (DLACZEGO decydujemy — sytuacja)
    D → Decyzja        (CO zdecydowaliśmy)
    K → Konsekwencje   (CO z tego wynika — plusy i minusy)

---

#### 11. ATAM — co robi

**„ATAM = ATakuj Architekturę Metodycznie"**

→ Szukasz tradeoffs: „ta decyzja poprawia X kosztem Y"
→ Metoda scenariuszowa: wymyślasz scenariusze jakościowe i sprawdzasz, jak architektura sobie z nimi radzi

---

#### 12. MASTER MNEMONIC — cały pytanie w jednym zdaniu

**„Tomek (TOGAF) Zachował (Zachman) Cztery Ciastka (C4) i 4+1 Archimedesowi (ArchiMate), rysując UML-em ADR-y, a ATAM sprawdził jakość ISO."**

Rozbicie:

    Tomek         → TOGAF (proces ADM: PVB-IT-OMG!, domeny BDAT)
    Zachował      → Zachman (siatka 6×6: CJGKKD × abstrakcje)
    Cztery Ciastka → C4 (4×C: Context→Container→Component→Code)
    4+1           → Kruchten (LDPP+S: Logical, Dev, Process, Physical + Scenarios)
    Archimedesowi → ArchiMate (BAT × ABP)
    UML           → 3 diagramy: CDS (Component, Deployment, Sequence)
    ADR           → KDK (Kontekst, Decyzja, Konsekwencje)
    ATAM          → ATakuj Architekturę Metodycznie
    ISO 25010     → 8 atrybutów: PS SM RUPC

---

### 🎮 Mostek do pracy magisterskiej — architektura silników gier

> Moja praca porównuje architekturę Unity i Unreal Engine — to gotowy case study dla modelowania C4, 4+1, ADR.

![C4 Model — architektura silnika gry](img/q13_engine_c4_architecture.png)

#### C4 Model zastosowany do silnika gry

| Poziom C4 | Unity | Unreal Engine |
|-----------|-------|---------------|
| **Context** | Gracz → Gra ← Twórca (edytor) | Gracz → Gra ← Twórca (edytor) |
| **Container** | Mono Runtime + IL2CPP, URP/HDRP Renderer, PhysX, FMOD | Unreal Runtime (C++), Nanite/Lumen Renderer, Chaos Physics, MetaSounds |
| **Component** | `MonoBehaviour`, `ScriptableObject`, Job System | `UActorComponent`, `USubsystem`, TaskGraph |
| **Code** | C# klasy: `BulletPool.cs`, `GameDirector.cs` | C++ klasy: `ABullet`, `AGameMode` |

#### 4+1 Kruchten — mapowanie na silnik

| Widok Kruchtena | Silnik gry |
|----------------|------------|
| Logiczny | Component Pattern, ECS, Scene Graph |
| Procesowy | Game Loop (Update→Physics→Render), wątki |
| Fizyczny | PC / PS5 / Xbox / Switch — deployment |
| Rozwojowy | Edytor Unity/UE, pakiety, pluginy |
| +1 Scenariusze | Gameplay: gracz strzela → bullet spawn → collision → damage |

#### ADR (Architecture Decision Records) z mojej pracy

Przykładowe decyzje architektoniczne, które mogę opisać językiem ADR:

1. **ADR-001**: Wybór Object Pooling zamiast Instantiate/Destroy  
   *Kontekst*: 500 pocisków/sekundę powoduje GC spikes  
   *Decyzja*: Pre-alokacja puli 500 obiektów  
   *Konsekwencja*: Frame time σ z 8ms → 2ms

2. **ADR-002**: Singleton GameDirector zamiast static class  
   *Kontekst*: Potrzeba globalnego stanu gry z lifecycle  
   *Decyzja*: MonoBehaviour Singleton z `DontDestroyOnLoad`  
   *Konsekwencja*: Testowalne, ale tight coupling

3. **ADR-003**: Unity URP zamiast Built-in RP  
   *Kontekst*: SRP Batcher zmniejsza draw calls o ~40%  
   *Decyzja*: Universal Render Pipeline  
   *Konsekwencja*: Lepszy batching, ale ograniczenie custom shaderów

#### Mnemonik — „SPRM" = Silnik Porównuję Rysując Modele

- **S**cena jako Context (C4 Level 1)
- **P**odsystemy jako Containers (Renderer, Physics, Audio)
- **R**ejestr decyzji ADR (dlaczego Pool, Singleton, URP)
- **M**oduły jako Components (MonoBehaviour, UActorComponent)

Na obronie: *„W mojej pracy porównuję architekturę Unity i Unreal — to idealny case study dla modelowania C4. Na poziomie Container widzimy fundamentalne różnice: Unity opiera się na Mono/.NET runtime z GC, a Unreal na natywnym C++ z ręcznym zarządzaniem pamięcią. Decyzje architektoniczne (ADR) w mojej implementacji — jak wybór Object Pooling — bezpośrednio odnoszą się do ADR rationales z publikacji Borowej."*

---

### 📚 Odniesienia do publikacji z Katedry

> Poniższe notatki pochodzą z publikacji promotorów/recenzentów i mogą być przydatne jako dodatkowy kontekst na obronie.

**Borowa, Zalewski, Kijas — „What rationales drive architectural decisions? An empirical inquiry" (ECSA 2023):**
- Badanie empiryczne (46 uczestników) identyfikujące TOP rationales stojące za decyzjami architektonicznymi
- Najczęstsze uzasadnienia decyzji: **łatwość użycia dla programisty**, **utrzymywalność (maintainability)**, **wydajność (performance)**, **wcześniejsza wiedza/doświadczenie**, **ograniczenia czasowe/deadlines**
- Wniosek: decyzje architektoniczne są silnie napędzane czynnikami ludzkimi (doświadczenie, presja czasu), nie tylko technicznymi

**Borowa — „Cognitive Biases in Architectural Decision-Making: Impact and Debiasing Strategies" (rozprawa doktorska, PW 2024):**
- Zidentyfikowano **11 błędów poznawczych (cognitive biases)** wpływających na ADM: efekt ramowania (framing), potwierdzenia (confirmation bias), efekt IKEA, prawo trywialności Parkinsona, zakotwiczenie (anchoring), klątwa wiedzy, pro-innovation bias, planistyczny optymizm, efekt owczego pędu (bandwagon), irracjonalna eskalacja, prawo instrumentu, optymizm
- **„Wicked Triad"** — zakotwiczenie → potwierdzenie → optymizm: łańcuchowa reakcja prowadząca do źle uzasadnionych decyzji architektonicznych
- Podstawa teoretyczna: **Dual Process Theory (Kahneman)** — System 1 (szybki, intuicyjny) vs System 2 (wolny, analityczny); biasy wynikają z nadmiernego polegania na System 1
- ADR-y (Architecture Decision Records) mogą częściowo łagodzić biasy, wymuszając jawne zapisanie kontekstu i konsekwencji
- Debiasing: **interwencja C-level Fischhoffa** — 3 techniki: (1) rozważ wiele opcji, (2) wypisz wady wybranego rozwiązania, (3) wypisz ryzyka
- Eksperyment z 18 praktykami (Polska, Niemcy, Brazylia): statystycznie istotny wzrost kontrargumentów nie-biasowych (p=0.0449)

**Borowa, Zalewski — „The influence of cognitive biases on architectural technical debt" (ICSA 2021):**
- Zakotwiczenie + optymizm → **„Architectural Lock-in"** (zamknięcie się w architekturze)
- Confirmation bias → **„Re-inventing the wheel"** (wymyślanie koła na nowo zamiast reuse)
- Biasy poznawcze są bezpośrednią przyczyną powstawania architektonicznego długu technicznego (ATD)

**Szlenk — „Formal Semantics of Architectural Decision Models":**
- Formalizacja semantyki modeli decyzji architektonicznych — umożliwia formalne rozumowanie o poprawności i spójności decyzji
- Związek z ADR: formalne podejście do walidacji decyzji architektonicznych

**Szlenk — „Modelling architectural decisions under changing requirements":**
- Jak zmieniające się wymagania wpływają na decyzje architektoniczne
- Metoda śledzenia wpływu zmian wymagań na podjęte wcześniej decyzje (traceability)

