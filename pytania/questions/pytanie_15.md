## PYTANIE 15: Agent upostaciowiony w robotyce

**Jak wykorzystuje się agenta upostaciowionego do specyfikacji sterowników robotów?**

---

### Tło pojęciowe — słowniczek

**Agent (w AI)** — autonomiczny byt, który postrzega środowisko (sensory), podejmuje decyzje (deliberacja) i wykonuje akcje (efektory). Agent ma cel i działa racjonalnie — wybiera akcje maksymalizujące osiągnięcie celu.

**Agent upostaciowiony (embodied agent)** — agent posiadający ciało fizyczne w rzeczywistym świecie. Przeciwieństwo agenta czysto softwareowego (np. chatbot). Robot = klasyczny agent upostaciowiony: ma sensory (kamery, LIDAR), ciało (ramię, koła) i działa w środowisku fizycznym. Kluczowe: musi radzić sobie z szumem sensorów, opóźnieniami, nieprzewidywalnością świata.

    Agent software:    dane → algorytm → wynik (deterministyczne)
    Agent embodied:    szum sensorów → niepewność → akcja fizyczna → efekt nieprzewidywalny

**Sterownik robota (robot controller)** — oprogramowanie decydujące co robot robi w każdej chwili. Specyfikacja sterownika = formalny opis zachowania robota. Agent upostaciowiony to model konceptualny, na którym opiera się sterownik.

---

**Cykl percepcja-deliberacja-akcja (See-Think-Act)** — podstawowy cykl działania agenta upostaciowionego:
1. **See (Percepcja)** — odczytaj dane z sensorów (obraz, odległość, pozycja)
2. **Think (Deliberacja)** — podejmij decyzję (planuj trasę, wybierz akcję)
3. **Act (Akcja)** — wyślij komendy do efektorów (silniki, chwytaki)

    Czujnik LIDAR → [Mapa otoczenia] → [Planowanie ścieżki] → [Silniki kół]
         See              Think                Think               Act

---

**3T Architecture (trójwarstwowa architektura sterownika):**
1. **Planner (deliberacja)** — planowanie symboliczne na wysokim poziomie. Czas reakcji: sekundy–minuty. Np. „zaplanuj trasę z A do B przez pokoje 1,2,3".
2. **Sequencer (wykonawca)** — koordynuje zachowania, FSM/Behavior Trees. Czas: 100ms–sekundy. Np. „Jedź do punktu → Obróć → Chwyć obiekt".
3. **Controller (reaktywny)** — bezpośrednie sterowanie sprzętem. Czas: milisekundy. Np. PID utrzymujący prędkość, unikanie kolizji.

    PLANNER       (minuty)    "Jedź do kuchni po kubek"
        ↓
    SEQUENCER     (sekundy)   "1: Jedź do drzwi → 2: Otwórz → 3: Jedź do blatu"
        ↓
    CONTROLLER    (ms)        "PID: prędkość lewego koła = 0.5 m/s"

---

**BDI (Beliefs-Desires-Intentions)** — formalny model agenta racjonalnego:
- **Beliefs** — wiedza agenta o świecie (mapa, pozycja, stan baterii). Może być niepełna/nieprecyzyjna.
- **Desires** — cele, które agent chciałby osiągnąć (np. „dotrzyj do punktu B").
- **Intentions** — aktualnie realizowany plan (podzbiór desires, do którego agent się zobowiązał).

Przykład: Robot-dostawca. Belief: „drzwi zamknięte". Desire: „dostarczyć paczkę do pokoju 5". Intention: „spróbuję drzwi boczne".

**FSM (Finite State Machine / automat skończony)** — model zachowania: skończona liczba stanów + przejścia warunkowe. Prosty, ale przy złożonych zachowaniach eksploduje liczba stanów i przejść.

    IDLE ──[wykryto cel]──→ APPROACH ──[blisko]──→ GRASP
      ↑                                              │
      └──────────────[obiekt chwycony]────────────────┘

**Behavior Tree (drzewo zachowań)** — nowoczesna alternatywa FSM. Hierarchiczna struktura: węzły wewnętrzne = logika (Selector, Sequence), liście = akcje/warunki. Modularny, reużywalny, łatwy do debugowania. Wywodzi się z AI w grach (Halo 2, ~2004).
- **Selector (?)** — wykonuj dzieci po kolei aż pierwszy sukces (jak OR)
- **Sequence (→)** — wykonuj dzieci po kolei, wstrzymaj przy porażce (jak AND)

---

**LTL (Linear Temporal Logic)** — logika temporalna do formalnej specyfikacji zachowań w czasie:
- **□ (always/globally)** — musi być prawdziwe ZAWSZE. □(¬collision) = „nigdy nie koliduj".
- **◇ (eventually)** — kiedyś musi być prawdziwe. ◇(at_goal) = „w końcu dotrzyj do celu".
- **Bezpieczeństwo (safety):** □(obstacle → ¬move_forward) — „zawsze: jeśli przeszkoda, nie jedź do przodu".
- **Żywotność (liveness):** ◇(at_goal) — „w końcu osiągnij cel".

**PID (Proportional-Integral-Derivative)** — klasyczny regulator sterowania. Minimalizuje błąd (różnicę między wartością zadaną a rzeczywistą). Trzy składniki:
- **P** — proporcjonalny: reaguje na aktualny błąd
- **I** — całkowy: eliminuje błąd stały (drift)
- **D** — różniczkowy: tłumi oscylacje

    Przykład: PID utrzymuje prędkość 1 m/s:
    Błąd = 1.0 - 0.8 = 0.2 → P zwiększa moc
    Błąd utrzymuje się? → I dodaje korektę
    Błąd maleje za szybko? → D hamuje

**ROS (Robot Operating System)** — middleware (nie OS!) do robotyki. Model pub/sub: węzły (nodes) publikują i subskrybują tematy (topics). Pozwala łączyć moduły (LIDAR, planowanie, sterowanie) w jednolity system. Open source, standard w akademii.

---

### Odpowiedź wprost: jak agent upostaciowiony specyfikuje sterownik robota

**Definicja:** Agent upostaciowiony (embodied agent) to formalny model konceptualny robota — bytu posiadającego ciało fizyczne, sensory i efektory, działającego w rzeczywistym środowisku. Wykorzystanie tego modelu do specyfikacji sterowników polega na tym, że **architektura sterownika robota jest bezpośrednim odwzorowaniem struktury agenta**: cykl percepcja–deliberacja–akcja staje się pętlą sterowania, a formalne modele agenta (BDI, LTL) stają się specyfikacją wymagań dla oprogramowania robota.

**Krótko: model agenta → architektura sterownika → implementacja na robocie.**

#### Krok 1: Model agenta definiuje CO robot ma robić

Robot traktujemy jako agenta upostaciowionego. To oznacza, że specyfikujemy:
- **Sensory** — jakie dane wejściowe robot otrzymuje (LIDAR, kamera, IMU)
- **Efektory** — jakie akcje fizyczne może wykonać (jedź, chwyć, obróć)
- **Cel** — co agent ma osiągnąć (dostarczyć paczkę, unikać kolizji)
- **Środowisko** — w jakim świecie działa (magazyn, szpital, droga)

#### Krok 2: Cykl See-Think-Act definiuje JAK działa pętla sterowania

Każdy sterownik robota realizuje wariant cyklu agenta:
1. **See** — odczytaj sensory → zbuduj wewnętrzny model świata (np. mapę)
2. **Think** — na podstawie modelu i celu wybierz akcję (planowanie)
3. **Act** — wyślij komendy do silników/chwytaków

Ten cykl powtarza się w pętli z częstotliwością zależną od warstwy (ms → min).

![Cykl See-Think-Act agenta upostaciowionego](img/agent_see_think_act.png)

#### Krok 3: Architektura 3T dzieli sterownik na warstwy odpowiedzialności

Praktyczna realizacja agenta upostaciowionego to **architektura trójwarstwowa (3T)**:

| Warstwa | Rola | Czas reakcji | Przykład |
|---------|------|-------------|----------|
| **Planner** | planowanie symboliczne (CEL → PLAN) | sekundy–minuty | "Jedź trasą A→B→C" |
| **Sequencer** | koordynacja zachowań (PLAN → SEKWENCJA) | 100 ms–sekundy | FSM: IDLE→APPROACH→GRASP |
| **Controller** | sterowanie sprzętem (SEKWENCJA → SYGNAŁY) | milisekundy | PID: prędkość = 0.5 m/s |

Każda warstwa odpowiada innemu aspektowi agenta:
- Planner = deliberacja (myślenie długoterminowe)
- Sequencer = koordynacja intencji (BDI: Intentions)
- Controller = reaktywność (natychmiastowe bezpieczeństwo)

![Architektura 3T sterownika robota](img/agent_3t_architecture.png)

#### Krok 4: Formalne modele agenta specyfikują wymagania

**Model BDI** pozwala formalnie opisać stan wewnętrzny agenta i na tej podstawie generować/weryfikować sterownik:
- Beliefs = wiedza robota → baza danych sensorycznych
- Desires = cele → warunki sukcesu
- Intentions = aktualny plan → sekwencer

![Model BDI agenta](img/agent_bdi_model.png)

**Logika temporalna LTL** pozwala specyfikować wymagania bezpieczeństwa i żywotności:
- **Bezpieczeństwo:** □(obstacle → ¬move_forward) — "ZAWSZE: jeśli przeszkoda, NIE jedź naprzód"
- **Żywotność:** ◇(at_goal) — "KIEDYŚ dotrzyj do celu"

Formalna specyfikacja LTL → automatyczna synteza/weryfikacja sterownika (model checking).

#### Krok 5: Behavior Trees implementują specyfikację zachowań

Nowoczesna metoda implementacji warstwy Sequencer. Modularność, reużywalność, łatwe debugowanie:

![Behavior Tree — robot przenoszący obiekt](img/agent_behavior_tree.png)

#### Konkretny przykład: robot-dostawca w szpitalu

1. **Model agenta:** sensory = LIDAR + kamera; efektory = koła + chwytak; cel = dostarcz lek do pokoju 5
2. **BDI:** Belief = "drzwi pokoju 5 zamknięte"; Desire = "dostarczyć lek"; Intention = "jedź do drzwi bocznych"
3. **LTL:** □(¬collision) ∧ ◇(at_room5) — "nigdy nie koliduj I w końcu dotrzyj do pokoju 5"
4. **3T:**
   - Planner: A* wyznacza trasę korytarz → winda → piętro 3 → pokój 5
   - Sequencer: BT: [Jedź do windy → Wjedź → Jedź do pokoju → Otwórz drzwi → Podaj lek]
   - Controller: PID utrzymuje prędkość 0.3 m/s, emergency stop przy przeszkodzie < 30 cm
5. **ROS:** node `/lidar_scan` → topic → node `/path_planner` → topic → node `/motor_driver`

---

### Agent upostaciowiony = ciało fizyczne + sensory + efektory + środowisko

Cykl: **Percepcja → Deliberacja → Akcja** (See-Think-Act)

### Architektura sterownika — 3 warstwy (3T Architecture)

1. **PLANNER** (deliberacja) — planowanie symboliczne, sekundy–minuty
2. **SEQUENCER** (wykonawca) — FSM/Behavior Trees, 100ms–sekundy
3. **CONTROLLER** (reaktywny) — PID, unikanie kolizji, milisekundy

### Model formalny BDI
- **Beliefs** — mapa, pozycja, stan
- **Desires** — cel nawigacji
- **Intentions** — aktualny plan

### Specyfikacja w logice temporalnej (LTL)
- Bezpieczeństwo: □(obstacle → ¬move_forward)
- Żywotność: ◇(at_goal)

### Behavior Trees — nowoczesna specyfikacja zachowań
- Selector (?): wykonaj pierwszy sukces
- Sequence (→): wykonaj wszystkie po kolei
- Action/Condition jako liście

### ROS (Robot Operating System) — middleware pub/sub dla robotów

### Etymologia

**Agent upostaciowiony (Embodied)** — łac. „corpus" = ciało; agent posiadający ciało fizyczne w środowisku. **BDI** — Beliefs-Desires-Intentions; Michael Bratman (filozof, 1987); Rao & Georgeff (1991) przenieśli do AI. **LTL** — Linear Temporal Logic; Amir Pnueli (1977, Turing Award 1996). **PID** — Proportional-Integral-Derivative; Nicolas Minorsky (1922, sterowanie okrętami). **ROS** — Robot Operating System (Willow Garage, 2007). **Behavior Tree** — z game AI (Halo 2, ~2004); zaadaptowane w robotyce.

### Jak zapamiętać

- **"STA"** = **S**ee → **T**hink → **A**ct (jak STA-bilność — stabilny cykl sterowania)
- **3T = "Plan-Seq-Con"** = od abstrakcji do sprzętu, jak w armii: generał (Plan) → oficer (Seq) → żołnierz (Con)
- **BDI = "Wiem–Chcę–Robię"**: Beliefs = co Wiem, Desires = co Chcę, Intentions = co Robię
- **LTL: □ = "zawsze" (kwadrat = solidny, niezmienny), ◇ = "kiedyś" (diament = cenny cel do zdobycia)**
- **Agent→Sterownik w 5 krokach:** CO (model agenta) → JAK (STA) → WARSTWY (3T) → WYMAGANIA (BDI+LTL) → IMPLEMENTACJA (BT+ROS)
- **Akronim SPECYFIKACJA:** **S**ensory → **P**ercepcja → **E**fekty → **C**ykl → **I**ntencje → **F**ormalność → **I**mplementacja → **K**ontroler → **A**kcja → **C**el → **J**akość → **A**rchitektura

