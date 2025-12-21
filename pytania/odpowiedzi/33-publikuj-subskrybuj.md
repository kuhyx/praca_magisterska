# Pytanie 33: Model publikuj-subskrybuj (Pub/Sub)

## Pytanie
**"Scharakteryzować model przesyłania komunikatów publikuj-subskrybuj oraz przykładowe rozwiązania techniczne wykorzystujące ten model."**

Przedmiot: PSD (Przetwarzanie Strumieniowe Danych)

---

## 📚 Odpowiedź główna

### 1. Definicja modelu Pub/Sub

```
┌─────────────────────────────────────────────────────────────────┐
│                      MODEL PUBLISH-SUBSCRIBE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PUBLISHERS              BROKER              SUBSCRIBERS        │
│  (nadawcy)               (pośrednik)         (odbiorcy)        │
│                                                                 │
│  ┌─────┐                ┌─────────┐           ┌─────┐          │
│  │ P1  │ ──publish──→   │         │  ──────→  │ S1  │          │
│  └─────┘      topic:A   │         │  topic:A  └─────┘          │
│                         │  MESSAGE │                            │
│  ┌─────┐                │  BROKER  │           ┌─────┐          │
│  │ P2  │ ──publish──→   │         │  ──────→  │ S2  │          │
│  └─────┘      topic:B   │  (router)│  topic:A  └─────┘          │
│                         │         │  topic:B                   │
│  ┌─────┐                │         │           ┌─────┐          │
│  │ P3  │ ──publish──→   │         │  ──────→  │ S3  │          │
│  └─────┘      topic:A   └─────────┘  topic:B  └─────┘          │
│                                                                 │
│  Cechy:                                                         │
│  • Luźne powiązanie (publisher nie zna subscriberów)           │
│  • Asynchroniczność                                             │
│  • Skalowalność (1:N, N:M)                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Typy subskrypcji

| Typ | Opis | Przykład |
|-----|------|----------|
| **Topic-based** | Subskrypcja na nazwany temat | `subscribe("orders")` |
| **Content-based** | Filtrowanie po zawartości | `price > 100 AND category = "electronics"` |
| **Type-based** | Na podstawie typu wiadomości | `subscribe(OrderEvent.class)` |
| **Hierarchical** | Tematy zagnieżdżone | `sport/football/+` (wildcard) |

### Wildcardy (MQTT)

```
Hierarchia tematów:
  home/living-room/temperature
  home/living-room/humidity
  home/bedroom/temperature
  home/kitchen/temperature

Subskrypcje:
  home/living-room/#     → wszystko z living-room
  home/+/temperature     → temperatura ze wszystkich pomieszczeń
  home/#                 → wszystko z home
```

---

### 3. Gwarancje dostarczenia

```
┌─────────────────────────────────────────────────────────────────┐
│ QoS (Quality of Service) levels:                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ QoS 0: AT MOST ONCE (fire and forget)                          │
│   Publisher ──msg──→ Broker ──msg──→ Subscriber                │
│   • Brak potwierdzenia                                          │
│   • Możliwa utrata                                              │
│   • Najszybsze                                                  │
│                                                                 │
│ QoS 1: AT LEAST ONCE                                           │
│   Publisher ──msg──→ Broker ──ack──→ Publisher                 │
│   • Potwierdzenie dostarczenia                                  │
│   • Możliwe duplikaty                                           │
│                                                                 │
│ QoS 2: EXACTLY ONCE                                            │
│   Publisher ←──handshake──→ Broker                             │
│   • 4-way handshake                                             │
│   • Brak duplikatów, brak utraty                               │
│   • Najwolniejsze                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. Rozwiązania techniczne

#### 4.1 Apache Kafka

```
┌─────────────────────────────────────────────────────────────────┐
│                        APACHE KAFKA                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Topic: "orders"                                                 │
│ ┌─────────────────────────────────────────────────┐            │
│ │ Partition 0: [msg1][msg2][msg3][msg4]...       │            │
│ │ Partition 1: [msg5][msg6][msg7]...             │            │
│ │ Partition 2: [msg8][msg9]...                   │            │
│ └─────────────────────────────────────────────────┘            │
│                                                                 │
│ Consumer Groups:                                                │
│   Group A: Consumer1 → Part0, Consumer2 → Part1,2              │
│   Group B: Consumer3 → Part0,1,2 (wszystkie)                   │
│                                                                 │
│ Cechy:                                                          │
│ • Distributed, fault-tolerant                                  │
│ • Persisted log (retention)                                    │
│ • High throughput (millions msg/s)                             │
│ • Pull model (consumer kontroluje tempo)                       │
│ • Exactly-once semantics (transactions)                        │
└─────────────────────────────────────────────────────────────────┘

// Producer
producer.send(new ProducerRecord<>("orders", key, value));

// Consumer
consumer.subscribe(Arrays.asList("orders"));
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        process(record);
    }
}
```

#### 4.2 RabbitMQ

```
┌─────────────────────────────────────────────────────────────────┐
│                        RABBITMQ                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Publisher → Exchange → Queue → Consumer                        │
│                                                                 │
│ Exchange types:                                                 │
│ • Direct:  routing_key exact match                             │
│ • Topic:   routing_key pattern (*.error, logs.#)              │
│ • Fanout:  broadcast to all queues                             │
│ • Headers: match on headers                                    │
│                                                                 │
│     [P] ─→ [Exchange] ─┬─→ [Queue1] ─→ [C1]                   │
│              (topic)   │                                       │
│                        └─→ [Queue2] ─→ [C2]                   │
│                                                                 │
│ Cechy:                                                          │
│ • AMQP protocol                                                │
│ • Flexible routing                                              │
│ • Push model (broker wysyła do consumera)                      │
│ • Acknowledgments, dead letter queues                          │
└─────────────────────────────────────────────────────────────────┘

// Python - pika
channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.basic_publish(exchange='logs', routing_key='', body=message)

channel.queue_bind(exchange='logs', queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
```

#### 4.3 MQTT (Message Queuing Telemetry Transport)

```
┌─────────────────────────────────────────────────────────────────┐
│                          MQTT                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Lightweight protocol for IoT                                   │
│                                                                 │
│ [Sensor] ──publish──→ [Broker] ──deliver──→ [Dashboard]       │
│           topic:                  (Mosquitto,                  │
│           "home/temp"             HiveMQ)                      │
│                                                                 │
│ Cechy:                                                          │
│ • Minimal overhead (2 byte header)                             │
│ • QoS 0, 1, 2                                                  │
│ • Retained messages                                            │
│ • Last Will and Testament (LWT)                                │
│ • Ideal for constrained devices                                │
│                                                                 │
│ Brokers: Mosquitto, HiveMQ, EMQ X, AWS IoT Core               │
└─────────────────────────────────────────────────────────────────┘

// Python - paho-mqtt
client.publish("home/temperature", payload="22.5")
client.subscribe("home/#")
```

#### 4.4 Redis Pub/Sub

```
┌─────────────────────────────────────────────────────────────────┐
│                      REDIS PUB/SUB                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Prosty pub/sub w Redis                                         │
│                                                                 │
│ PUBLISH channel message                                         │
│ SUBSCRIBE channel                                               │
│ PSUBSCRIBE pattern (np. news.*)                                │
│                                                                 │
│ Cechy:                                                          │
│ • Fire-and-forget (brak persistence)                           │
│ • Very fast                                                    │
│ • Brak consumer groups (podstawowy)                            │
│                                                                 │
│ Redis Streams (nowsze):                                        │
│ • Persistent log (jak Kafka)                                   │
│ • Consumer groups                                               │
│ • XADD, XREAD, XGROUP                                          │
└─────────────────────────────────────────────────────────────────┘

# Publisher
redis-cli PUBLISH news "Breaking: ..."

# Subscriber
redis-cli SUBSCRIBE news
```

---

### 5. Porównanie rozwiązań

| Cecha | Kafka | RabbitMQ | MQTT | Redis Pub/Sub |
|-------|-------|----------|------|---------------|
| **Model** | Pull (log) | Push (queue) | Push | Push |
| **Persistence** | Tak (log) | Opcjonalne | Retained only | Nie (Streams: tak) |
| **Throughput** | Bardzo wysoki | Wysoki | Niski-średni | Wysoki |
| **Routing** | Topic/partition | Flexible | Topic hierarchy | Channel/pattern |
| **Use case** | Event streaming | Task queues | IoT | Real-time simple |
| **Protocol** | Własny | AMQP | MQTT | RESP |

---

### 6. Zalety i wady Pub/Sub

```
┌─────────────────────────────────────────────────────────────────┐
│ ZALETY:                                                         │
│ ✓ Luźne powiązanie (decoupling)                                │
│ ✓ Skalowalność (dodawanie subskrybentów bez zmian publishera) │
│ ✓ Asynchroniczność (brak blokowania)                           │
│ ✓ Broadcast (1:N)                                              │
│ ✓ Filtrowanie (content-based, topics)                          │
├─────────────────────────────────────────────────────────────────┤
│ WADY:                                                           │
│ ✗ Brak gwarancji dostarczenia (zależy od QoS)                 │
│ ✗ Ordering challenges (zwłaszcza z partycjami)                │
│ ✗ Debugging trudniejsze (brak bezpośredniego połączenia)      │
│ ✗ Broker = single point of failure (wymaga HA)                │
│ ✗ Message loss jeśli subscriber offline (bez persistence)     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7. Wzorce użycia

```
1. EVENT SOURCING:
   [Service] ─publish─→ [Kafka] ←─consume─ [Projections]
   Wszystkie zmiany jako events, rebuild state z log

2. CQRS (Command Query Responsibility Segregation):
   [Write Model] ─events─→ [Event Bus] ─→ [Read Model]
   Oddzielne modele do zapisu i odczytu

3. MICROSERVICES COMMUNICATION:
   [Order Service] ─"OrderCreated"─→ [Message Broker]
                                           │
                      ┌────────────────────┼────────────────────┐
                      ↓                    ↓                    ↓
               [Inventory]          [Shipping]           [Notification]

4. IoT DATA COLLECTION:
   [Sensors] ─MQTT─→ [Broker] ─→ [Data Pipeline] ─→ [Analytics]
```

---

## 🧠 Mnemoniki

### "Pub/Sub = Radio broadcast":
Publisher nadaje, kto chce słucha (subscribe)

### "Kafka = Log, RabbitMQ = Queue":
Kafka przechowuje log, RabbitMQ to klasyczna kolejka

### "QoS 0-1-2 = Fire-AtLeast-Exactly":
0 = fire&forget, 1 = at least once, 2 = exactly once

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy Kafka a kiedy RabbitMQ?"
**Odpowiedź:** Kafka: event streaming, log retention, replay, high throughput, analytics. RabbitMQ: task queues, complex routing, request-reply, legacy AMQP integration.

### Q2: "Co to jest consumer group w Kafce?"
**Odpowiedź:** Grupa consumerów gdzie każda partycja jest przypisana do jednego consumera w grupie. Umożliwia parallel processing i load balancing. Różne grupy otrzymują wszystkie wiadomości niezależnie.

### Q3: "Jak zapewnić ordering w pub/sub?"
**Odpowiedź:** Kafka: ordering per partition (użyj tego samego klucza). RabbitMQ: single queue, single consumer. MQTT: QoS 2 dla pojedynczego topicu. Globalny ordering wymaga single partition/queue.

---

## 🎯 Kluczowe punkty

1. **Pub/Sub:** Luźne powiązanie, asynchroniczność, 1:N
2. **Kafka:** Distributed log, high throughput, persistence
3. **RabbitMQ:** AMQP, flexible routing, push model
4. **MQTT:** IoT, lightweight, QoS levels
5. **Gwarancje:** At most/least/exactly once

---

## 📖 Źródła

1. Kafka Documentation - kafka.apache.org
2. RabbitMQ Tutorials - rabbitmq.com
3. MQTT Specification - mqtt.org
4. Kleppmann - "Designing Data-Intensive Applications"
