## PYTANIE 11: Modelowanie procesów biznesowych (WSYZ)

**Scharakteryzować standardy i narzędzia do modelowania procesów biznesowych.**

---

### Tło pojęciowe — słowniczek

**Proces biznesowy (business process)** — uporządkowany zbiór czynności, które transformują dane wejściowe (np. zamówienie klienta) w wynik (np. dostarczony produkt). Przykład: „obsługa reklamacji" = przyjmij zgłoszenie → zweryfikuj → zatwierdź/odrzuć → poinformuj klienta. Modelowanie to graficzne przedstawienie takich procesów.

**Modelowanie procesów** — tworzenie wizualnych diagramów opisujących KTO, CO, KIEDY i W JAKIEJ KOLEJNOŚCI wykonuje w organizacji. Cel: zrozumienie, dokumentacja, optymalizacja, automatyzacja.

---

**BPMN (Business Process Model and Notation)** — najpopularniejszy standard notacji graficznej dla procesów biznesowych. Utrzymywany przez OMG (Object Management Group). Wersja 2.0 ma format XML, dzięki czemu diagramy mogą być bezpośrednio wykonywane przez silnik procesów (BPMS).

**Elementy BPMN:**
- **Zdarzenia (Events):** ○ start, ◎ pośrednie, ◉ końcowe — co wyzwala lub kończy proces.
- **Czynności (Activities):** prostokąty — praca do wykonania (task, subprocess).
- **Bramki (Gateways):** ◇ kontrola przepływu — decyzje i rozgałęzienia.

**Bramki BPMN (gateways):**
- **XOR (Exclusive):** dokładnie JEDNA ścieżka (jak if/else). Np. „Czy kwota > 1000? → Tak/Nie".
- **AND (Parallel):** WSZYSTKIE ścieżki jednocześnie. Np. „Wyślij e-mail I zaktualizuj bazę".
- **OR (Inclusive):** JEDNA LUB WIĘCEJ ścieżek. Np. „Powiadom SMS i/lub e-mail zależnie od preferencji."

    ○─→[Przyjmij zamówienie]─→◇XOR─→[Zapłata kartą]─→◉
                                  └→[Zapłata przelewem]─→◉

**Łączniki BPMN:**
- **Sequence Flow (→)** — kolejność czynności
- **Message Flow (- - →)** — komunikacja między uczestnikami (poolami)
- **Association (···→)** — powiązanie z danymi/komentarzami

**Swimlane** — element organizacyjny: **Pool** = organizacja/uczestnik, **Lane** = dział/rola w organizacji. Jak tory na basenie — każdy „pływa" na swoim torze.

---

**UML (Unified Modeling Language)** — uniwersalny język modelowania w inżynierii oprogramowania. 14 typów diagramów. W kontekście procesów używa się **Activity Diagrams** — rozszerzenie flowchartów z fork/join (współbieżność), decision nodes, object flow. Lepszy dla procesów technicznych/software niż BPMN.

**UML Activity Diagram vs BPMN:**

    Cecha          BPMN                 UML Activity
    ─────────────────────────────────────────────────
    Cel            Procesy biznesowe    Przepływ sterowania
    Odbiorcy       Biznes + IT          Głównie IT
    Komunikacja    Pools + Msg Flow     Partitions
    Automatyzacja  Tak (XML)            Ograniczona

**EPC (Event-driven Process Chain)** — notacja procesowa: naprzemienne zdarzenia i funkcje, połączone łącznikami logicznymi (AND/OR/XOR). Popularny w środowisku SAP (framework ARIS). Mniej uniwersalny niż BPMN.

**ARIS (Architecture of Integrated Information Systems)** — framework i narzędzie prof. Scheera do modelowania procesów. Bazuje na EPC. Używany głównie w dużych firmach z SAP.

---

**OMG (Object Management Group)** — organizacja standaryzacyjna odpowiedzialna za BPMN, UML, CORBA. Non-profit, członkowie to firmy IT (IBM, Oracle, SAP...).

**BPMS (Business Process Management System/Suite)** — oprogramowanie do automatyzacji procesów BPMN. Diagram BPMN 2.0 XML jest interpretowany i wykonywany przez silnik (np. Camunda, jBPM). Zmiana procesu = zmiana diagramu, nie kodu.

**IDEF0 (Integration DEFinition)** — notacja modelowania funkcji z US Air Force (1970s). Skupia się na WEJŚCIach, WYJŚCIach, mechanizmach i kontrolach. Rzadko używana współcześnie.

**VSM (Value Stream Map)** — narzędzie Lean Manufacturing. Mapuje przepływ materiałów i informacji od dostawcy do klienta, identyfikuje marnotrawstwo (waste). Stosowane w fabrykach i IT (DevOps).

**Flowchart (schemat blokowy)** — najprostszy sposób modelowania: prostokąty (czynności), romby (decyzje), strzałki (przepływ). Prekursor BPMN, ale brak standardów dla komunikacji międzyprocesowej.

---

### Porównanie notacji — diagramy tego samego procesu

Poniżej ten sam proces „Obsługa reklamacji" zamodelowany w 4 różnych notacjach. Wszystkie diagramy znajdują się w katalogu `pytania/img/`.

**BPMN 2.0** — z poolem, lane'ami (BOK, Jakość, Magazyn), bramkami XOR, zdarzeniami start/end:

![BPMN 2.0 — Obsługa reklamacji](img/bpmn_reklamacja.png)

**UML Activity Diagram** — z węzłami decyzji, merge, initial/final nodes:

![UML Activity Diagram — Obsługa reklamacji](img/uml_activity_reklamacja.png)

**EPC (Event-driven Process Chain)** — naprzemienne zdarzenia (szare) i funkcje (białe), łączniki XOR:

![EPC — Obsługa reklamacji](img/epc_reklamacja.png)

**Schemat blokowy (Flowchart)** — prostokąty (procesy), romby (decyzje), równoległoboki (we/wy):

![Flowchart — Obsługa reklamacji](img/flowchart_reklamacja.png)

---

### Główne standardy

### BPMN 2.0 (Business Process Model and Notation) — OMG
- **Uniwersalny standard** — dla analityków, architektów, programistów
- Elementy: Zdarzenia (○ start, ◎ pośrednie, ◉ końcowe), Czynności (prostokąty), Bramki (◇ XOR, ◆ AND, ○◇ OR)
- Łączniki: Sequence Flow (→), Message Flow (- - →), Association (···→)
- Swimlanes: Pool (organizacja) / Lane (dział)
- Format XML → automatyzacja (BPMS)

### UML Activity Diagrams
- Część UML 2.x — rozszerzenie flowchartów + sieci Petriego
- Elementy: akcje, decyzje (◇), fork/join (▬), pin (object flow)
- Lepsze dla procesów technicznych/software

### EPC (Event-driven Process Chain)
- Naprzemienne zdarzenia i funkcje, łączniki AND/OR/XOR
- Popularny w SAP (ARIS framework)

### Inne: IDEF0 (modelowanie funkcji), VSM (Value Stream Map, Lean), Flowcharty

### BPMN vs UML Activity

| Cecha        | BPMN               | UML Activity       |
|--------------|---------------------|---------------------|
| Cel          | Procesy biznesowe   | Przepływ sterowania |
| Odbiorcy     | Biznes + IT         | Głównie IT          |
| Komunikacja  | Pools + Message Flow| Partitions          |
| Automatyzacja| Tak (BPMN 2.0 XML) | Ograniczona         |

### Narzędzia do modelowania procesów biznesowych

**Bizagi Modeler** — darmowe narzędzie desktopowe (Windows) do modelowania BPMN 2.0. Intuicyjny interfejs drag-and-drop, walidacja poprawności diagramów, eksport do PDF/Word/PNG. Wersja płatna (Bizagi Automation Server) pozwala na automatyzację i wykonywanie procesów. Popularny w edukacji i małych firmach — zerowa bariera wejścia.

**Camunda** — platforma open-source do automatyzacji procesów BPMN 2.0 i DMN (Decision Model and Notation). Składa się z:
- **Camunda Modeler** — desktopowy edytor diagramów BPMN/DMN
- **Camunda Engine** — silnik wykonawczy (Java) — interpretuje XML BPMN i realizuje proces krok po kroku
- **Camunda Cockpit** — panel monitoringu uruchomionych instancji procesów
Stosowany w bankach, ubezpieczeniach, e-commerce. Unikalna cecha: diagram BPMN = kod wykonywalny (nie tylko dokumentacja).

**Signavio (SAP Signavio)** — chmurowe narzędzie do modelowania i analizy procesów. Przejęte przez SAP w 2021. Obsługuje BPMN 2.0, EPC, DMN. Wyróżnik: **Process Intelligence** — automatyczne odkrywanie procesów z logów systemów IT (process mining). Integracja z SAP ERP. Stosowane w dużych korporacjach.

**ARIS (Software AG)** — zaawansowany framework i narzędzie do modelowania architektury przedsiębiorstwa. Bazuje na EPC, ale obsługuje też BPMN 2.0. Pięć widoków architektury (organizacja, dane, funkcje, procesy, produkty/usługi). Dominuje w środowiskach SAP. Główni odbiorcy: duże organizacje z rozbudowanymi strukturami.

**Enterprise Architect (Sparx Systems)** — komercyjne narzędzie do modelowania UML, BPMN, ArchiMate, SysML i wielu innych notacji. Jednolite środowisko dla architektów IT i analityków. Silne wsparcie dla generowania kodu z modeli i inżynierii odwrotnej (reverse engineering). Stosowane głównie w projektach software'owych.

**Lucidchart** — chmurowe narzędzie do tworzenia diagramów (BPMN, UML, flowcharty, ERD). Współpraca w czasie rzeczywistym (jak Google Docs). Prostsze niż Camunda/ARIS — raczej do dokumentacji i komunikacji niż automatyzacji. Integracje z Google Workspace, Atlassian, Microsoft.

**draw.io (diagrams.net)** — w pełni darmowe narzędzie open-source do diagramów. Działa w przeglądarce lub jako aplikacja desktopowa. Obsługuje szablony BPMN, UML, flowcharty. Brak automatyzacji procesów — wyłącznie modelowanie wizualne. Popularny wśród indywidualnych użytkowników i małych zespołów.

**jBPM (Red Hat)** — open-source silnik procesów BPMN 2.0 w ekosystemie Java/Red Hat. Podobny do Camundy — wykonuje procesy z diagramów BPMN. Część platformy Red Hat Process Automation Manager.

**Microsoft Visio** — klasyczne narzędzie desktopowe Microsoftu do diagramów biznesowych. Obsługuje szablony BPMN, flowcharty, organigramy. Integracja z ekosystemem Microsoft 365. Brak silnika wykonawczego — tylko modelowanie.

### Porównanie narzędzi

| Narzędzie         | Typ              | Notacje          | Automatyzacja | Koszt         |
|-------------------|------------------|------------------|---------------|---------------|
| Bizagi Modeler    | Desktop          | BPMN 2.0         | Płatna wersja | Darmowy       |
| Camunda           | Platforma        | BPMN, DMN        | Tak (silnik)  | Open-source   |
| Signavio (SAP)    | Chmura           | BPMN, EPC, DMN   | Process mining| Komercyjny    |
| ARIS              | Desktop/Chmura   | EPC, BPMN        | Symulacja     | Komercyjny    |
| Enterprise Arch.  | Desktop          | UML, BPMN, inne  | Code-gen      | Komercyjny    |
| Lucidchart        | Chmura           | BPMN, UML, inne  | Nie           | Freemium      |
| draw.io           | Przeglądarka     | BPMN, UML, inne  | Nie           | Darmowy       |
| jBPM              | Platforma        | BPMN 2.0         | Tak (silnik)  | Open-source   |
| MS Visio          | Desktop          | BPMN, flowcharty | Nie           | Komercyjny    |

**Podział funkcjonalny:**
- **Tylko modelowanie (dokumentacja):** draw.io, Lucidchart, Visio, Bizagi (free)
- **Modelowanie + automatyzacja (BPMS):** Camunda, jBPM, Bizagi (płatna), Signavio
- **Modelowanie + architektura przedsiębiorstwa:** ARIS, Enterprise Architect

### Etymologia

**BPMN** — Business Process Model and Notation; OMG (Object Management Group). **UML** — Unified Modeling Language; „Unified" bo połączył metody Boocha, Rumbaugh i Jacobsona („Three Amigos", 1990s). **EPC** — Event-driven Process Chain; August-Wilhelm Scheer (Saarland, 1990s; podstawa SAP ARIS). **Swimlane** — metafora torów na basenie: każdy uczestnik na swoim „torze". **IDEF0** — Integration DEFinition; US Air Force (1970s).

### Jak zapamiętać

- **BPMN = „standard nr 1" dla biznesu** — bramki, swimlanes, zdarzenia
- **3 typy bramek: XOR (jeden), AND (wszystkie), OR (jeden lub więcej)**
- UML Activity → programiści; BPMN → wszyscy

---

### 📚 Odniesienia do publikacji z Katedry

> Poniższe notatki pochodzą z publikacji promotorów/recenzentów i mogą być przydatne jako dodatkowy kontekst na obronie.

**Szlenk, Zalewski, Borowa — „An evolution process for service-oriented systems" (DepCoS/Springer):**
- Zaproponowano **4-fazowy proces modyfikacji systemów SOA** oparty o BPMN:
  1. Identyfikacja wpływu zmiany na usługi
  2. Przeprojektowanie usług dotkniętych zmianą
  3. Implementacja i testowanie
  4. Wdrożenie i monitoring
- Proces jest zgodny z **ISO 20000 / ITIL** — łączy modelowanie procesów biznesowych z zarządzaniem usługami IT
- BPMN użyty do formalnego opisu procesu ewolucji — każda faza ma diagram BPMN z bramkami decyzyjnymi i swimlane'ami
- Walidacja: pilotaż z **11 firmami** — proces okazał się praktyczny i skalowalny
- **Traceability** — śledzenie powiązań między procesami biznesowymi a usługami technicznymi, dzięki czemu zmiana w procesie BPMN automatycznie wskazuje usługi do modyfikacji

**Szlenk — „Extraction of UML class diagrams from natural language specifications":**
- Automatyczne wyodrębnianie diagramów klas UML ze specyfikacji w języku naturalnym
- Związek z BPMN: uzupełnienie modelowania procesów o modelowanie struktury danych (UML) na podstawie tych samych wymagań tekstowych

**Szlenk — „UML static models in formal approach" / „System model semantics of class diagrams":**
- Formalizacja semantyki diagramów UML — umożliwia formalne sprawdzanie poprawności modeli
- Przydatne gdy BPMN (procesy) i UML (struktura) muszą być spójne — formalizacja pozwala weryfikować tę spójność

