# Pytanie 35: Modelowanie układów cyber-fizycznych

## Pytanie
**"Na czym polega specyfika modelowania matematycznego układów cyber-fizycznych? Podać przykłady współpracy agentów w sieci i problemów w osiąganiu pożądanego zachowania układu."**

Przedmiot: SIU (Systemy Inteligentne i Uczące się)

---

## 📚 Odpowiedź główna

### 1. Definicja układów cyber-fizycznych (CPS)

```
┌─────────────────────────────────────────────────────────────────┐
│              CYBER-PHYSICAL SYSTEM (CPS)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌──────────────────┐         ┌──────────────────┐           │
│    │  CYBER           │ ←────→  │  PHYSICAL        │           │
│    │  (computation,   │         │  (dynamics,      │           │
│    │   communication, │         │   physics,       │           │
│    │   control)       │         │   environment)   │           │
│    └──────────────────┘         └──────────────────┘           │
│             ↑                            ↑                      │
│             │         SENSORS            │                      │
│             └────────────────────────────┘                      │
│                       ACTUATORS                                 │
│                                                                 │
│  Przykłady: Autonomiczne pojazdy, smart grid, robotyka,        │
│             drony, systemy medyczne, Industry 4.0              │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Specyfika modelowania CPS

#### Hybrid Systems (systemy hybrydowe)

```
┌─────────────────────────────────────────────────────────────────┐
│ DYNAMIKA CIĄGŁA + DYSKRETNA                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Ciągła (fizyka):        ẋ = f(x, u)     (równania różniczkowe) │
│ Dyskretna (logika):     Automat stanów   (przełączanie trybów) │
│                                                                 │
│ Przykład - termostat:                                           │
│                                                                 │
│   Mode: OFF                    Mode: ON                         │
│   ┌─────────────┐             ┌─────────────┐                  │
│   │ Ṫ = -α(T-Tₑ)│ ──T<Tₗ───→ │ Ṫ = β - α(T-Tₑ)│              │
│   │             │ ←──T>Tₕ─── │              │                  │
│   └─────────────┘             └─────────────┘                  │
│                                                                 │
│ T = temperatura, Tₑ = zewnętrzna, Tₗ/Tₕ = progi               │
└─────────────────────────────────────────────────────────────────┘
```

#### Modelowanie matematyczne

| Aspekt | Model | Opis |
|--------|-------|------|
| **Dynamika ciągła** | ODE/PDE | ẋ = f(x,u,t) |
| **Stany dyskretne** | Automaty hybrydowe | Przejścia między trybami |
| **Komunikacja** | Grafy, delay | Topologia sieci, opóźnienia |
| **Niepewność** | Stochastyczne ODE | Szum, zakłócenia |
| **Ograniczenia** | Nierówności | Fizyczne limity |

---

### 3. Współpraca agentów w sieci

#### Consensus (uzgadnianie)

```
Problem: Agenty mają osiągnąć wspólną wartość

Protokół consensus:
  ẋᵢ = Σⱼ∈Nᵢ aᵢⱼ(xⱼ - xᵢ)

gdzie:
- xᵢ = stan agenta i
- Nᵢ = sąsiedzi agenta i
- aᵢⱼ = waga połączenia

Forma macierzowa:
  ẋ = -L·x

L = Laplacian grafu komunikacji

┌─────────────────────────────────────────────────────────────────┐
│ Przykład: 4 agenty, różne wartości początkowe                  │
│                                                                 │
│   x(t)                                                          │
│    ↑                                                            │
│  5 │  ●                                                         │
│  4 │    ●───────────────────────────●  consensus               │
│  3 │        ●───────────────────────●  value                   │
│  2 │            ●───────────────────●                          │
│  1 │  ●─────────────────────────────●                          │
│    └─────────────────────────────────→ t                       │
│                                                                 │
│ Wszystkie wartości zbiegają do średniej                        │
└─────────────────────────────────────────────────────────────────┘
```

#### Formation Control (formacje)

```
Problem: Utrzymanie geometrycznej formacji

Agent i:
  ẋᵢ = Σⱼ∈Nᵢ aᵢⱼ[(xⱼ - xᵢ) - (dⱼ* - dᵢ*)]

gdzie dᵢ* = pozycja docelowa agenta i w formacji

Przykład - formacja trójkąta:

  Start:           Cel:
    ●  ●             ●
   ●    ●           / \
    ●              ●───●
```

#### Flocking (stado)

```
Trzy zasady Reynoldsa:

1. SEPARATION: Unikaj kolizji z sąsiadami
   Fₛₑₚ = -Σ (xⱼ - xᵢ)/||xⱼ - xᵢ||²

2. ALIGNMENT: Dopasuj prędkość do sąsiadów  
   Fₐₗᵢₘ = Σ (vⱼ - vᵢ)

3. COHESION: Dąż do centrum grupy
   Fₖₒₕ = (x̄ - xᵢ)

┌─────────────────────────────────────────────────────────────────┐
│                    ●→                                           │
│        ●→         ●→        ●→                                 │
│              ●→          ●→                                    │
│         ●→     ●→    ●→                                        │
│    ●→            ●→                                             │
│                                                                 │
│    Ptaki/ryby poruszają się jako zorganizowana grupa           │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. Problemy w osiąganiu pożądanego zachowania

#### 4.1 Problemy komunikacyjne

```
┌─────────────────────────────────────────────────────────────────┐
│ OPÓŹNIENIA (Delays):                                            │
│                                                                 │
│   ẋᵢ(t) = Σⱼ aᵢⱼ[xⱼ(t - τᵢⱼ) - xᵢ(t)]                        │
│                                                                 │
│   Duże τ → niestabilność, oscylacje                            │
│                                                                 │
│ UTRATA PAKIETÓW:                                                │
│                                                                 │
│   Agent nie otrzymuje informacji od sąsiada                    │
│   → Stale dane, błędne decyzje                                 │
│                                                                 │
│ OGRANICZONA PRZEPUSTOWOŚĆ:                                      │
│                                                                 │
│   Kwantyzacja informacji                                       │
│   → Błędy zaokrągleń, limit cykli                             │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2 Problemy topologii

| Problem | Opis | Skutek |
|---------|------|--------|
| **Słaba łączność** | Graf niespójny | Brak consensus |
| **Zmiana topologii** | Agenty się przemieszczają | Niestabilność |
| **Single point of failure** | Kluczowy węzeł pada | Rozpad sieci |
| **Partycjonowanie** | Sieć dzieli się | Lokalne consensus |

```
Graf spójny:            Graf niespójny:
  ●───●                   ●───●   ●───●
  │   │                   │       │
  ●───●                   ●       ●
  
Consensus: TAK           Consensus: NIE
                         (dwa osobne clustry)
```

#### 4.3 Problemy dynamiczne

```
┌─────────────────────────────────────────────────────────────────┐
│ HETEROGENICZNOŚĆ:                                               │
│   Agenty mają różne dynamiki (szybkie vs wolne)                │
│   → Różne szybkości zbieżności                                 │
│                                                                 │
│ SATURACJA AKTUATORÓW:                                          │
│   |uᵢ| ≤ uₘₐₓ (fizyczne ograniczenia)                         │
│   → Wolniejsza zbieżność, możliwy brak zbieżności             │
│                                                                 │
│ ZAKŁÓCENIA:                                                     │
│   ẋᵢ = f(x) + wᵢ(t)  gdzie wᵢ = szum                          │
│   → Błąd steady-state, oscylacje wokół celu                   │
│                                                                 │
│ ADVERSARIAL AGENTS:                                            │
│   Złośliwy agent wysyła fałszywe dane                         │
│   → Consensus na błędnej wartości                              │
│   Rozwiązanie: Byzantine fault tolerance                       │
└─────────────────────────────────────────────────────────────────┘
```

---

### 5. Warunki zbieżności consensus

```
Twierdzenie: Protokół consensus ẋ = -Lx zbiega do consensus ⟺
             Graf komunikacji jest (słabo) spójny

Szybkość zbieżności ~ λ₂(L) (algebraic connectivity)

Większe λ₂ → szybsza zbieżność

Dla grafów skierowanych:
- Potrzebny spanning tree
- Wartość consensus = ważona średnia
```

---

### 6. Przykłady zastosowań

| Zastosowanie | Agenty | Współpraca |
|--------------|--------|------------|
| **Swarm robotics** | Roboty | Eksploracja, transport |
| **Vehicular platoon** | Pojazdy | Jazda w kolumnie |
| **Smart grid** | Generatory | Balansowanie mocy |
| **Sensor networks** | Sensory | Distributed estimation |
| **UAV coordination** | Drony | Surveillance, delivery |

---

## 🧠 Mnemoniki

### "CPS = Cyber + Physical + Sensors":
Trzy elementy systemu cyber-fizycznego

### "Consensus = Laplacian = -Lx":
Protokół consensus używa Laplacianu grafu

### "SAC = Separation, Alignment, Cohesion":
Trzy zasady flockingu Reynoldsa

---

## ❓ Pytania dodatkowe

### Q1: "Jak modelować opóźnienia w komunikacji?"
**Odpowiedź:** Delay differential equations (DDE): ẋ(t) = f(x(t), x(t-τ)). Analiza stabilności: metody Lyapunova-Krasovskiego, analiza wartości własnych z delay. Kompensacja: predyktory Smitha, robust control.

### Q2: "Co to jest algebraic connectivity?"
**Odpowiedź:** Druga najmniejsza wartość własna Laplacianu grafu (λ₂). Mierzy jak dobrze graf jest połączony. λ₂ > 0 ⟺ graf spójny. Większe λ₂ = szybsza zbieżność consensus.

### Q3: "Jak zapewnić odporność na złośliwe agenty?"
**Odpowiedź:** Byzantine fault tolerance: F-local / F-total model, W-MSR algorithm (Weighted Mean-Subsequence-Reduced), redundancja informacji, reputation systems.

---

## 🎯 Kluczowe punkty

1. **CPS:** Hybrid systems (ciągła + dyskretna dynamika)
2. **Consensus:** ẋ = -Lx, zbieżność do wspólnej wartości
3. **Flocking:** Separation, Alignment, Cohesion
4. **Problemy:** Delays, packet loss, topology changes
5. **Warunek:** Graf spójny dla consensus

---

## 📖 Źródła

1. Olfati-Saber, Murray - "Consensus Problems in Networks of Agents"
2. Mesbahi, Egerstedt - "Graph Theoretic Methods in Multiagent Networks"
3. Bullo - "Lectures on Network Systems"
