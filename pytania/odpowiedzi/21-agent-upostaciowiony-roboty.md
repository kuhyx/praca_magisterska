# Pytanie 21: Agent upostaciowiony w specyfikacji sterowników robotów

## Pytanie
**"Jak wykorzystuje się agenta upostaciowionego do specyfikacji sterowników robotów?"**

Przedmiot: ERPM (Elementy Robotyki i Projektowania Mechatronicznego)

---

## 📚 Odpowiedź główna

### 1. Agent upostaciowiony (Embodied Agent)

#### Definicja

**Agent upostaciowiony** = agent posiadający fizyczne ciało, osadzony w rzeczywistym środowisku, zdolny do:
- **Percepcji** poprzez sensory
- **Działania** poprzez efektory
- **Interakcji** ze środowiskiem

```
┌─────────────────────────────────────────────────────────────────┐
│                    ŚRODOWISKO FIZYCZNE                          │
│                                                                 │
│    ┌───────────────────────────────────────────────┐           │
│    │           ROBOT (Agent upostaciowiony)        │           │
│    │                                               │           │
│    │   Sensory          Sterownik        Efektory  │           │
│    │   ┌─────┐         ┌─────────┐      ┌─────┐   │           │
│    │   │Kamera│───────→│ Agent   │─────→│Motor│   │           │
│    │   │LIDAR │        │ Logic   │      │Grip │   │           │
│    │   │IMU   │        │ (BDI)   │      │Servo│   │           │
│    │   └─────┘         └─────────┘      └─────┘   │           │
│    │       ↑                                ↓      │           │
│    │       └────────────────────────────────┘      │           │
│    │              Sprzężenie zwrotne               │           │
│    └───────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Specyfikacja sterownika robota

#### Architektura agentowa sterownika

```
┌─────────────────────────────────────────────────────────────────┐
│  WARSTWA DELIBERACYJNA (Agent BDI)                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Beliefs: mapa, pozycja, stan zadania                   │   │
│  │  Desires: cel nawigacji, zadanie manipulacji            │   │
│  │  Intentions: aktualny plan działania                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  WARSTWA WYKONAWCZA (Reactive behaviors)                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Unikanie kolizji, śledzenie ścieżki, chwytanie        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  WARSTWA SPRZĘTOWA (HAL)                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Sterowniki silników, protokoły sensorów               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3. Formalny model agenta

#### Cykl percepcja-akcja

```
Agent: Environment → Action
Agent: Percept* → Action  (historia percepcji)

Formalnie:
  see: E → P           (funkcja percepcji)
  action: P* → A       (funkcja decyzyjna)
  next: E × A → E      (funkcja przejścia środowiska)
```

#### Specyfikacja w logice temporalnej

```
Przykład specyfikacji bezpieczeństwa:
□(obstacle_detected → ¬move_forward)
"Zawsze gdy wykryto przeszkodę, nie jedź do przodu"

Specyfikacja żywotności:
◇(at_goal)
"Kiedyś robot dotrze do celu"

Specyfikacja reaktywności:
□(request_pickup → ◇holding_object)
"Zawsze gdy jest żądanie podniesienia, kiedyś obiekt będzie trzymany"
```

---

### 4. Zastosowanie w ROS (Robot Operating System)

#### Agent jako węzeł ROS

```
┌─────────────────────────────────────────────────────────────────┐
│  ROS Architecture                                               │
│                                                                 │
│  /sensor_node ──topic──→ /agent_node ──topic──→ /motor_node    │
│       ↓                       ↓                      ↓         │
│  [Publikuje]            [Subskrybuje &         [Wykonuje]      │
│  /scan                   Publikuje]             /cmd_vel       │
│  /camera                 /plan                                  │
│  /odom                   /status                                │
│                                                                 │
│  Agent node implementuje:                                       │
│  - Pętlę kontrolną (control loop)                              │
│  - Stan wewnętrzny (beliefs)                                   │
│  - Planowanie (intentions)                                      │
└─────────────────────────────────────────────────────────────────┘
```

#### Behavior Trees (BT)

```
Nowoczesna specyfikacja zachowań robota:

        [Selector ?]
        /    |     \
       /     |      \
    [Seq→] [Seq→]  [Idle]
    /    \    |
   /      \   |
[Check] [Pick] [Navigate]

Węzły:
- Sequence (→): wykonaj wszystkie po kolei
- Selector (?): wykonaj pierwszy sukces
- Action: atomowa akcja
- Condition: sprawdzenie warunku
```

---

### 5. Hybrydowa architektura 3T

```
┌─────────────────────────────────────────────────────────────────┐
│  THREE-TIER (3T) Architecture                                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PLANNER (deliberation)                                 │   │
│  │  - Długoterminowe planowanie                           │   │
│  │  - Rozumowanie symboliczne                             │   │
│  │  Czas: sekundy - minuty                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓↑                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  SEQUENCER (executive)                                  │   │
│  │  - Wybór zachowań, nadzór wykonania                    │   │
│  │  - Finite State Machine / Behavior Tree                │   │
│  │  Czas: 100ms - sekundy                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓↑                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  CONTROLLER (reactive)                                  │   │
│  │  - Pętle PID, unikanie kolizji                         │   │
│  │  - Bezpośrednia reakcja sensor → motor                 │   │
│  │  Czas: ms                                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6. Korzyści podejścia agentowego

| Korzyść | Opis |
|---------|------|
| **Modularność** | Rozdzielenie percepcji, decyzji, akcji |
| **Abstrakcja** | Ukrycie szczegółów sprzętu |
| **Autonomia** | Robot sam decyduje o działaniach |
| **Reużywalność** | Zachowania przenośne między platformami |
| **Weryfikowalność** | Formalna specyfikacja → model checking |

---

## 🧠 Mnemoniki

### "Agent = See-Think-Act":
Percepcja → Deliberacja → Akcja

### "3T = Plan-Sequence-Control":
Trzy warstwy od abstrakcji do sprzętu

### "BDI w robocie":
- **B**eliefs = mapa, pozycja
- **D**esires = cel nawigacji
- **I**ntentions = plan ruchu

---

## ❓ Pytania dodatkowe

### Q1: "Czym różni się agent reaktywny od deliberatywnego?"
**Odpowiedź:** Reaktywny: bezpośrednia reakcja sensor→akcja (np. unikanie kolizji), bez planowania. Deliberatywny: model świata, planowanie, cel. Hybryda łączy oba.

### Q2: "Co to jest subsumption architecture?"
**Odpowiedź:** Architektura Brooksa - warstwy zachowań, wyższe mogą "nadpisać" niższe. Bez centralnego modelu świata. Skuteczna dla prostych robotów mobilnych.

### Q3: "Jak weryfikować poprawność sterownika agentowego?"
**Odpowiedź:** Model checking (SPIN, NuSMV), symulacja (Gazebo), formalna specyfikacja (LTL, CTL), testy jednostkowe zachowań, testy integracyjne w symulacji przed wdrożeniem na sprzęt.

---

## 🎯 Kluczowe punkty

1. **Agent upostaciowiony** = ciało + sensory + efektory + środowisko
2. **BDI** dla deliberacji, reaktywność dla bezpieczeństwa
3. **3T Architecture:** Planner → Sequencer → Controller
4. **Behavior Trees** nowoczesna specyfikacja zachowań➜ utils (main) ✗ git commit -m "feat: more aggressive android script"
Running auto-fixers and shell_check before committing...
Auto-fixing 3 shell file(s)...
  → Running shfmt...
  ✓ Auto-fixes applied and staged
Running shell_check validation...

In scripts/utils/android_guardian/post-fs-data.sh line 5:
MODULE_DIR="/data/adb/modules/android_guardian"
^--------^ SC2034 (warning): MODULE_DIR appears unused. Verify use (or export if used externally).

For more information:
  https://www.shellcheck.net/wiki/SC2034 -- MODULE_DIR appears unused. Verify...

Commit aborted: shellcheck found issues.
Fix the remaining problems and retry the commit.
5. **Korzyści:** modularność, abstrakcja, weryfikowalność

---

## 📖 Źródła

1. Wooldridge - "Introduction to MultiAgent Systems"
2. Siciliano, Khatib - "Springer Handbook of Robotics"
3. Gat - "Three-Layer Architectures"
4. ROS Documentation - ros.org
