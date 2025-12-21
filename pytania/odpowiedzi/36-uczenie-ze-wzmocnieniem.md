# Pytanie 36: Uczenie się ze wzmocnieniem (Reinforcement Learning)

## Pytanie
**"Omówić ogólny algorytm, elementy składowe oraz własności uczenia się ze wzmocnieniem."**

Przedmiot: SIU (Systemy Inteligentne i Uczące się)

---

## 📚 Odpowiedź główna

### 1. Model uczenia ze wzmocnieniem

```
┌─────────────────────────────────────────────────────────────────┐
│              REINFORCEMENT LEARNING LOOP                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ┌─────────────┐                            │
│          action aₜ  │             │  reward rₜ                 │
│         ──────────→ │ ENVIRONMENT │ ──────────→                │
│         │           │             │           │                │
│         │           └─────────────┘           │                │
│         │                 │                   │                │
│         │          state sₜ₊₁                 │                │
│         │                 │                   │                │
│         │                 ↓                   ↓                │
│         │           ┌─────────────┐                            │
│         └────────── │    AGENT    │ ←─────────┘                │
│                     │  (policy π) │                            │
│                     └─────────────┘                            │
│                                                                 │
│  Cel: Maksymalizacja skumulowanej nagrody E[Σ γᵗrₜ]            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Elementy składowe

| Element | Symbol | Opis |
|---------|--------|------|
| **State** | s ∈ S | Obserwacja środowiska |
| **Action** | a ∈ A | Decyzja agenta |
| **Reward** | r ∈ ℝ | Sygnał zwrotny |
| **Policy** | π(a\|s) | Strategia wyboru akcji |
| **Value function** | V(s), Q(s,a) | Oczekiwana nagroda |
| **Discount factor** | γ ∈ [0,1] | Ważność przyszłych nagród |
| **Transition** | P(s'\|s,a) | Dynamika środowiska |

### Markov Decision Process (MDP)

```
MDP = (S, A, P, R, γ)

S: Zbiór stanów
A: Zbiór akcji
P: P(s'|s,a) - prawdopodobieństwa przejść
R: R(s,a,s') - funkcja nagrody
γ: Współczynnik dyskontowania

Właściwość Markowa:
  P(sₜ₊₁|s₀,a₀,...,sₜ,aₜ) = P(sₜ₊₁|sₜ,aₜ)
  
  Przyszłość zależy tylko od obecnego stanu!
```

---

### 3. Funkcje wartości

#### State Value Function V(s)

$$V^\pi(s) = \mathbb{E}_\pi \left[ \sum_{t=0}^{\infty} \gamma^t r_t \mid s_0 = s \right]$$

#### Action Value Function Q(s,a)

$$Q^\pi(s,a) = \mathbb{E}_\pi \left[ \sum_{t=0}^{\infty} \gamma^t r_t \mid s_0 = s, a_0 = a \right]$$

#### Równania Bellmana

```
V*(s) = max_a [R(s,a) + γ Σ_s' P(s'|s,a) V*(s')]

Q*(s,a) = R(s,a) + γ Σ_s' P(s'|s,a) max_a' Q*(s',a')

Rekurencyjne równania - podstawa algorytmów DP
```

---

### 4. Algorytmy

#### 4.1 Value-based methods

```
┌─────────────────────────────────────────────────────────────────┐
│ Q-LEARNING (off-policy, model-free)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]           │
│                    └────────────────────────────────┘           │
│                           TD target                             │
│                                                                 │
│ Algorytm:                                                       │
│ 1. Obserwuj stan s                                             │
│ 2. Wybierz akcję a (ε-greedy)                                  │
│ 3. Wykonaj a, obserwuj r, s'                                   │
│ 4. Zaktualizuj Q(s,a)                                          │
│ 5. s ← s', goto 1                                              │
│                                                                 │
│ ε-greedy:                                                       │
│   Z prawdop. ε: losowa akcja (exploration)                     │
│   Z prawdop. 1-ε: argmax Q(s,a) (exploitation)                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SARSA (on-policy)                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]                  │
│                              ↑                                  │
│                    Rzeczywista następna akcja (nie max!)       │
│                                                                 │
│ Różnica od Q-learning:                                          │
│ - Używa akcji faktycznie wybranej przez policy                 │
│ - Bardziej "ostrożny" (uwzględnia exploration)                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2 Deep Q-Network (DQN)

```
┌─────────────────────────────────────────────────────────────────┐
│ DQN - Q-learning z siecią neuronową                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ State s → [Neural Network] → Q(s,a₁), Q(s,a₂), ..., Q(s,aₙ)   │
│                                                                 │
│ Innowacje:                                                      │
│ 1. Experience Replay: bufor (s,a,r,s'), losowe próbkowanie    │
│ 2. Target Network: osobna sieć do obliczania targetów         │
│    (aktualizowana co N kroków)                                 │
│                                                                 │
│ Loss: L = (r + γ max Q_target(s',a') - Q(s,a))²               │
│                                                                 │
│ Przełom: Atari games (2015)                                    │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.3 Policy-based methods

```
┌─────────────────────────────────────────────────────────────────┐
│ POLICY GRADIENT                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Bezpośrednia optymalizacja parametrów θ policy π_θ(a|s)        │
│                                                                 │
│ Gradient:                                                       │
│ ∇_θ J(θ) = E_π [∇_θ log π_θ(a|s) · Q(s,a)]                    │
│                                                                 │
│ REINFORCE algorithm:                                            │
│ 1. Generuj trajektorię τ = (s₀,a₀,r₀,s₁,...)                  │
│ 2. Oblicz return: Gₜ = Σ_{k=0}^{T-t} γᵏ r_{t+k}               │
│ 3. Update: θ ← θ + α ∇_θ log π_θ(aₜ|sₜ) · Gₜ                  │
│                                                                 │
│ Zalety: ciągłe akcje, stochastic policies                     │
│ Wady: wysoka wariancja, wolna zbieżność                        │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.4 Actor-Critic

```
┌─────────────────────────────────────────────────────────────────┐
│ ACTOR-CRITIC - łączy value-based i policy-based               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│     ┌─────────┐        ┌─────────┐                             │
│     │  ACTOR  │ ←───── │  CRITIC │                             │
│     │ π_θ(a|s)│        │  V_w(s) │                             │
│     └────┬────┘        └────┬────┘                             │
│          │                  │                                   │
│          ↓                  │                                   │
│       action           value estimate                          │
│                                                                 │
│ Actor: wybiera akcje (policy)                                  │
│ Critic: ocenia jak dobre są akcje (value function)            │
│                                                                 │
│ Advantage: A(s,a) = Q(s,a) - V(s)                             │
│ Actor update: θ ← θ + α ∇_θ log π_θ(a|s) · A(s,a)             │
│ Critic update: minimize (r + γV(s') - V(s))²                  │
│                                                                 │
│ Algorytmy: A2C, A3C, PPO, SAC                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 5. Klasyfikacja algorytmów

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│               ┌── Model-based (zna/uczy się P, R)              │
│   RL Methods ─┤                                                 │
│               └── Model-free (nie zna środowiska)              │
│                        │                                        │
│                        ├── Value-based (Q-learning, DQN)       │
│                        ├── Policy-based (REINFORCE)            │
│                        └── Actor-Critic (A2C, PPO, SAC)        │
│                                                                 │
│               ┌── On-policy (SARSA, A2C) - używa obecnej π     │
│   RL Methods ─┤                                                 │
│               └── Off-policy (Q-learning, DQN) - używa innej π │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6. Exploration vs Exploitation

| Strategia | Opis |
|-----------|------|
| **ε-greedy** | Z prawdop. ε losowa akcja |
| **Softmax/Boltzmann** | P(a) ∝ exp(Q(s,a)/τ) |
| **UCB** | a = argmax[Q(s,a) + c√(ln N / n(a))] |
| **Thompson Sampling** | Próbkowanie z posterior |
| **Curiosity-driven** | Bonus za nowość |

---

### 7. Własności i wyzwania

```
┌─────────────────────────────────────────────────────────────────┐
│ WŁASNOŚCI:                                                      │
│ ✓ Uczenie przez interakcję (nie supervised)                    │
│ ✓ Delayed rewards (kredyt za sekwencję akcji)                 │
│ ✓ Generalizacja (do nowych stanów)                            │
│ ✓ Online learning (ciągłe doskonalenie)                       │
│                                                                 │
│ WYZWANIA:                                                       │
│ ✗ Sample inefficiency (wymaga wielu interakcji)               │
│ ✗ Credit assignment (która akcja odpowiada za reward?)        │
│ ✗ Exploration-exploitation tradeoff                           │
│ ✗ Partial observability (POMDP)                               │
│ ✗ Non-stationarity (środowisko się zmienia)                  │
│ ✗ Reward shaping (sparse rewards problem)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mnemoniki

### "SARSA = State Action Reward State Action":
Sekwencja w algorytmie SARSA

### "Q = Quality of action":
Q(s,a) mierzy jakość akcji a w stanie s

### "Actor-Critic = Action + Advice":
Actor wybiera akcje, Critic doradza (ocenia)

---

## ❓ Pytania dodatkowe

### Q1: "Jaka jest różnica między Q-learning a SARSA?"
**Odpowiedź:** Q-learning (off-policy): używa max Q(s',a') - optymistyczne. SARSA (on-policy): używa Q(s',a') gdzie a' to rzeczywista następna akcja - bardziej ostrożne, uwzględnia policy exploration.

### Q2: "Po co Experience Replay w DQN?"
**Odpowiedź:** Łamie korelację między kolejnymi próbkami (iid requirement), efektywniejsze wykorzystanie danych (wielokrotne uczenie z jednej próbki), stabilizuje trening.

### Q3: "Kiedy model-based jest lepszy?"
**Odpowiedź:** Gdy środowisko jest przewidywalne, samples są drogie (robotyka), potrzebne planowanie. Model-free lepszy gdy środowisko złożone, trudne do modelowania, dużo samples dostępnych.

---

## 🎯 Kluczowe punkty

1. **MDP:** (S, A, P, R, γ) - formalizacja problemu
2. **Bellman:** V*(s) = max[R + γ·ΣP·V*]
3. **Q-learning:** off-policy, max Q update
4. **Policy Gradient:** ∇J = E[∇log π · Q]
5. **Actor-Critic:** policy + value function

---

## 📖 Źródła

1. Sutton, Barto - "Reinforcement Learning: An Introduction"
2. Silver - DeepMind RL lectures
3. Mnih et al. - "Playing Atari with Deep RL" (2015)
