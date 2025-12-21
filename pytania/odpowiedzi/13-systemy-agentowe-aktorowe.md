# Pytanie 13: Systemy agentowe i aktorowe - teorie, standardy, narzędzia

## Pytanie
**"Omówić szczegółowo teorie, definicje, standardy i narzędzia wykorzystywane przy projektowaniu i implementacji systemów opartych na koncepcji agenta i aktora."**

Przedmiot: AASD (Agentowe i Aktorowe Systemy Decyzyjne)

---

## 📚 Odpowiedź główna

### 1. Definicje fundamentalne

#### Agent (wg Wooldridge & Jennings)
**Agent** = system komputerowy umieszczony w środowisku, zdolny do **autonomicznego działania** w celu realizacji celów.

```
┌─────────────────────────────────────────────────────────────────┐
│                      ŚRODOWISKO                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │    Percepcja          ┌─────────┐         Akcja        │   │
│  │   ─────────────────→  │  AGENT  │  ─────────────────→  │   │
│  │      (sensory)        │         │       (effectors)    │   │
│  │                       │ Cele    │                       │   │
│  │                       │ Wiedza  │                       │   │
│  │                       │ Plany   │                       │   │
│  │                       └─────────┘                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

#### Właściwości agenta (AARC)

| Właściwość | Opis |
|------------|------|
| **Autonomiczność** | Działa bez bezpośredniej interwencji |
| **Reaktywność** | Reaguje na zmiany środowiska |
| **Proaktywność** | Inicjuje działania do realizacji celów |
| **Społeczność** | Komunikuje się z innymi agentami |

#### Aktor (model Hewitta, 1973)
**Aktor** = fundamentalna jednostka obliczeń, która:
- Ma **prywatny stan**
- Komunikuje się wyłącznie przez **wiadomości**
- Może tworzyć nowych aktorów
- Przetwarza jedną wiadomość naraz

```
┌────────────────────────────────────────────────────────────────┐
│  AKTOR                                                         │
│  ┌──────────────────┐                                         │
│  │   Mailbox        │  ← wiadomości (kolejka)                 │
│  │   ┌─┬─┬─┬─┐     │                                         │
│  │   │m│m│m│m│     │                                         │
│  │   └─┴─┴─┴─┘     │                                         │
│  │        ↓         │                                         │
│  │   Behavior       │  → przetwarzanie sekwencyjne            │
│  │   (zachowanie)   │                                         │
│  │        ↓         │                                         │
│  │   Stan prywatny  │  → izolowany, niemutowalny z zewnątrz   │
│  └──────────────────┘                                         │
│                                                                │
│  Reakcje na wiadomość:                                        │
│  1. Wyślij wiadomości do innych aktorów                       │
│  2. Utwórz nowych aktorów                                     │
│  3. Zmień własne zachowanie (become)                          │
└────────────────────────────────────────────────────────────────┘
```

---

### 2. Agent vs Aktor

| Cecha | Agent | Aktor |
|-------|-------|-------|
| **Cel** | Inteligentne zachowanie | Współbieżność |
| **Stan** | Beliefs, Goals, Intentions | Prywatny, izolowany |
| **Komunikacja** | ACL (semantyka) | Wiadomości (asynchroniczne) |
| **Autonomia** | Wysoka (decyzje) | Średnia (reaktywność) |
| **Pochodzenie** | AI, systemy rozproszone | Teoria obliczeń |

---

### 3. Architektury agentów

#### BDI (Belief-Desire-Intention)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITEKTURA BDI                             │
│                                                                 │
│   Percepcja → BELIEFS (przekonania o świecie)                  │
│                    ↓                                            │
│              DESIRES (cele do osiągnięcia)                     │
│                    ↓                                            │
│              INTENTIONS (wybrane plany)                        │
│                    ↓                                            │
│                  Akcja                                          │
│                                                                 │
│   Przykład:                                                     │
│   B: "Jest czerwone światło"                                   │
│   D: "Chcę dojechać do celu"                                   │
│   I: "Zatrzymam się i poczekam"                                │
└─────────────────────────────────────────────────────────────────┘
```

#### Subsumption Architecture (Brooks)

```
Warstwa 3: [Eksploruj]     → najwyższy priorytet
              ↓ suppress
Warstwa 2: [Unikaj przeszkód]
              ↓ suppress
Warstwa 1: [Idź przed siebie]
              ↓
           Effektory

Zachowania niskopoziomowe mogą być "nadpisane" przez wyższe.
```

---

### 4. Standardy komunikacji agentów

#### FIPA (Foundation for Intelligent Physical Agents)

**FIPA-ACL** (Agent Communication Language):

```
(inform
  :sender    agent1
  :receiver  agent2
  :content   (price item1 100)
  :language  FIPA-SL
  :ontology  trading-ontology
)
```

**Performatywy FIPA:**

| Performatyw | Znaczenie |
|-------------|-----------|
| `inform` | Informuje o fakcie |
| `request` | Prosi o wykonanie akcji |
| `query-if` | Pyta czy coś jest prawdą |
| `propose` | Proponuje transakcję |
| `accept-proposal` | Akceptuje propozycję |
| `reject-proposal` | Odrzuca propozycję |
| `cfp` | Call for Proposals |

#### KQML (Knowledge Query and Manipulation Language)
Starszy standard, podobny do FIPA-ACL.

---

### 5. Narzędzia i frameworki

#### Systemy agentowe

| Narzędzie | Język | Opis |
|-----------|-------|------|
| **JADE** | Java | FIPA-compliant, najpopularniejszy |
| **Jason** | AgentSpeak | BDI, deklaratywny |
| **SPADE** | Python | Asynchroniczny, XMPP |
| **NetLogo** | Logo | Symulacje, edukacja |
| **MASON** | Java | Symulacje wieloagentowe |

#### Systemy aktorowe

| Narzędzie | Język | Opis |
|-----------|-------|------|
| **Akka** | Scala/Java | Produkcyjny, dojrzały |
| **Erlang/OTP** | Erlang | Telekomunikacja, fault-tolerant |
| **Orleans** | C# | Microsoft, Virtual Actors |
| **Pony** | Pony | Capabilities, bezpieczny |
| **Ray** | Python | ML, distributed computing |

---

### 6. Protokoły interakcji

#### Contract Net Protocol

```
┌─────────┐        cfp         ┌─────────┐
│ Manager │───────────────────→│ Bidder1 │
│         │←──────propose──────│         │
│         │        cfp         ├─────────┤
│         │───────────────────→│ Bidder2 │
│         │←──────propose──────│         │
│         │                    ├─────────┤
│         │───accept-proposal─→│ Winner  │
│         │←─────inform────────│         │
└─────────┘                    └─────────┘
```

---

## 🧠 Mnemoniki

### "BDI = Believe, Desire, Intend":
- **B**eliefs = co wiem o świecie
- **D**esires = czego chcę
- **I**ntentions = co zamierzam zrobić

### "ARPS" - właściwości agenta:
- **A**utonomiczność
- **R**eaktywność
- **P**roaktywność
- **S**połeczność

### "Aktor = Mailbox + Behavior + State":
- Kolejka wiadomości
- Logika przetwarzania
- Izolowany stan

---

## ❓ Pytania dodatkowe

### Q1: "Czym różni się JADE od Akka?"
**Odpowiedź:** JADE to framework agentowy (FIPA, ACL, inteligentne zachowania), Akka to framework aktorowy (współbieżność, fault-tolerance, reactive streams). JADE dla AI/MAS, Akka dla systemów rozproszonych.

### Q2: "Co to jest Yellow Pages w systemach agentowych?"
**Odpowiedź:** Usługa katalogowa (Directory Facilitator w FIPA) gdzie agenty rejestrują swoje usługi. Inne agenty mogą wyszukiwać agenty oferujące konkretne usługi. Analogia do książki telefonicznej.

### Q3: "Jak Akka zapewnia fault-tolerance?"
**Odpowiedź:** Supervision trees - każdy aktor ma supervisora, który decyduje o reakcji na błąd (restart, stop, eskaluj). "Let it crash" philosophy - izolacja błędów.

---

## 🎯 Kluczowe punkty

1. **Agent** = autonomiczny, reaktywny, proaktywny, społeczny
2. **Aktor** = mailbox + behavior + isolated state
3. **BDI** = Beliefs-Desires-Intentions (architektura)
4. **FIPA-ACL** = standard komunikacji agentów
5. **JADE** = agenty (Java), **Akka** = aktorzy (Scala)

---

## 📖 Źródła

1. Wooldridge - "An Introduction to MultiAgent Systems"
2. Hewitt - "A Universal Modular Actor Formalism for AI"
3. FIPA Specifications - fipa.org
4. Akka Documentation - akka.io
