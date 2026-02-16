## PYTANIE 19/29: Model Publish-Subscribe

**Scharakteryzować model i przykładowe rozwiązania techniczne.**

---

### Tło pojęciowe — słowniczek

**Pub/Sub (Publish-Subscribe)** — wzorzec komunikacji: nadawcy (publishers) wysyłają wiadomości, NIE wiedząc kto je odbierze. Odbiorcy (subscribers) deklarują zainteresowanie i otrzymują dopasowane wiadomości. Między nimi stoi **broker** (pośrednik). Metafora: radio — nadawca nadaje, kto chce słucha.

    Publisher A ──→ ┌─────────┐ ──→ Subscriber X
    Publisher B ──→ │  BROKER │ ──→ Subscriber Y
    Publisher C ──→ └─────────┘ ──→ Subscriber Z

**Dlaczego nie bezpośrednio?** Bo publisher musiałby znać wszystkich subscriberów, zarządzać połączeniami, retransmitować. Broker rozwiązuje to centralnie.

---

**Publisher (nadawca)** — komponent wysyłający wiadomości (eventy/zdarzenia) do brokera. Nie wie, kto subskrybuje. Przykład: czujnik temperatury publikuje odczyt co 5 sekund.

**Subscriber (odbiorca)** — komponent rejestrujący się u brokera na określone tematy/typy wiadomości. Otrzymuje wiadomości pasujące do subskrypcji. Przykład: alarm subskrybuje temat „temperatura" i reaguje gdy >50°C.

**Broker (pośrednik)** — centralny komponent routujący wiadomości od publishers do subscribers. Odpowiada za: filtrowanie, dostarczanie, buforowanie, gwarancje dostarczenia.

**Luźne powiązanie (loose coupling)** — publisher i subscriber nie znają się nawzajem. Można dodać nowego subscribera bez zmiany publishera. Fundamentalna zaleta pub/sub.

---

**Typy subskrypcji:**
- **Topic-based** — subscriber subskrybuje temat (np. „orders.created"). Najprostszy i najpopularniejszy.
- **Content-based** — filtrowanie po treści wiadomości (np. „price > 100"). Bardziej elastyczny, ale wolniejszy.
- **Type-based** — filtrowanie po typie wiadomości (np. klasa OrderEvent).
- **Hierarchical (wildcards)** — wzorce tematów: `orders.*` dopasowuje `orders.created`, `orders.cancelled`.

    Topic: "sensors/temperature/room1"
    Wildcard: "sensors/temperature/#"  → dopasowuje room1, room2, ...

---

**QoS (Quality of Service)** — gwarancje dostarczenia wiadomości:
- **At-most-once** — wiadomość dostarczana 0 lub 1 raz. „Fire and forget." Najszybszy, ryzyko utraty. Użycie: logi, metryki.
- **At-least-once** — wiadomość dostarczana ≥1 raz. Mogą być duplikaty. Użycie: płatności (z idempotencją).
- **Exactly-once** — wiadomość dostarczana dokładnie 1 raz. Najtrudniejszy do zaimplementowania. Użycie: transakcje finansowe.

    At-most-once:   send → ✓ lub ✗ (nie retransmituj)
    At-least-once:  send → ack? retry → może duplikat
    Exactly-once:   send → ack + deduplikacja (najkosztowniejszy)

---

**Kafka (Apache Kafka)** — rozproszony log. Model pull: konsument sam ciągnie wiadomości ze logu. Wiadomości **przechowywane** na dysku (retention 7 dni default). Partycje + Consumer Groups = równoległy odczyt. Bardzo wysoka przepustowość (miliony msg/s). LinkedIn (2011). Exactly-once z transakcjami.

    Kafka = rozproszony, trwały LOG
    Topic: [msg1][msg2][msg3][msg4][msg5]  ← append-only
    Consumer czyta od dowolnego offsetu (może cofnąć!)

**RabbitMQ** — klasyczna kolejka wiadomości (message queue). Model push: broker dostarcza do konsumenta. Protokół AMQP. Exchange types: Direct (klucz), Topic (*, #), Fanout (broadcast), Headers. Elastyczny routing. Wiadomości konsumowane → usunięte z kolejki.

    RabbitMQ: Publisher → Exchange → Queue → Consumer
    Wiadomość skonsumowana = znika z kolejki

**MQTT (Message Queuing Telemetry Transport)** — ultralekkiprotokół pub/sub. 2-bajtowy nagłówek! Zaprojektowany dla IoT i urządzeń z ograniczonymi zasobami (sensory, mikrokontrolery). IBM (1999) do monitoringu rurociągów naftowych przez satelitę. Brokers: Mosquitto, HiveMQ.

**Redis Pub/Sub** — pub/sub wbudowany w Redis (in-memory database). Szybki, ale BEZ persistencji — jeśli subscriber był offline, wiadomość przepada. Dla real-time (chat, live updates).

    Cecha           Kafka         RabbitMQ      MQTT          Redis
    ────────────────────────────────────────────────────────────────
    Model           Pull (log)    Push (queue)  Push          Push
    Persistencja    Tak           Opcjonalna    Retained msg  Nie
    Throughput      Bardzo wysoki Wysoki        Niski-średni  Wysoki
    Use case        Streaming     Task queues   IoT           Real-time

---

**SPOF (Single Point of Failure)** — broker jako centralny punkt: jeśli padnie, cała komunikacja się zatrzymuje. Rozwiązanie: klasteryzacja brokera (Kafka cluster, RabbitMQ cluster).

**AMQP (Advanced Message Queuing Protocol)** — otwarty protokół messaging. Standard implementowany przez RabbitMQ. Definiuje: exchange, queue, binding, ack.

---

### Model Pub/Sub

Publishers → **Broker** (router/message bus) → Subscribers
- Luźne powiązanie (publisher nie zna subscriberów)
- Asynchroniczne, skalowalne (1:N, N:M)

### Typy subskrypcji: topic-based, content-based, type-based, hierarchical (wildcards)

### Gwarancje dostarczenia (QoS): At-most-once, At-least-once, Exactly-once

### Rozwiązania techniczne

| Technologia  | Model          | Persistence | Throughput    | Use Case      |
|--------------|----------------|-------------|---------------|---------------|
| **Kafka**    | Pull (log)     | Tak         | Bardzo wysoki | Event streaming|
| **RabbitMQ** | Push (queue)   | Opcjonalne  | Wysoki        | Task queues   |
| **MQTT**     | Push           | Retained    | Niski-średni  | IoT           |
| **Redis**    | Push           | Nie         | Wysoki        | Real-time     |

**Kafka:** Partycje + Consumer Groups, distributed log, exactly-once z transakcjami.
**RabbitMQ:** AMQP, Exchange types (Direct, Topic, Fanout, Headers), flexible routing.
**MQTT:** Lekki (2-byte header), idealny dla IoT/constrained devices, brokers: Mosquitto, HiveMQ.

### Zalety / Wady

Zalety: decoupling, skalowalność, asynchroniczność, broadcast.
Wady: debugging trudniejsze, ordering challenges, broker = SPOF.

### Etymologia

**Kafka** — od Franza Kafki (pisarz); Jay Kreps (LinkedIn, 2011): „system zoptymalizowany do pisania — a Kafka był pisarzem". **RabbitMQ** — „rabbit" = szybkość; AMQP = Advanced Message Queuing Protocol. **MQTT** — Message Queuing Telemetry Transport; Andy Stanford-Clark (IBM) + Arlen Nipper (1999); do monitoringu rurociągów naftowych przez satelitę. **Redis** — REmote DIctionary Server (Salvatore Sanfilippo, 2009). **Pub/Sub** — publish-subscribe; wzorzec z systemów event-driven (lata 80/90). **QoS** — Quality of Service.

### Jak zapamiętać

- **„Pub/Sub = Radio"** — nadawca nadaje, kto chce słucha
- **Kafka = Log** (przechowuje historię), **RabbitMQ = Queue** (konsumuje i kasuje)
- **MQTT = IoT** — lekki, mały overhead

