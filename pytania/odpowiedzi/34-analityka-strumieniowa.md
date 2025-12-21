# Pytanie 34: Analityka danych strumieniowych

## Pytanie
**"Scharakteryzować rozwiązania analityczne działające na danych o charakterze strumieniowym."**

Przedmiot: PSD (Przetwarzanie Strumieniowe Danych)

---

## 📚 Odpowiedź główna

### 1. Charakterystyka danych strumieniowych

```
┌─────────────────────────────────────────────────────────────────┐
│              DANE STRUMIENIOWE vs BATCH                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ BATCH:                                                          │
│ ┌─────────────────────────┐                                    │
│ │  Dane statyczne         │ → Przetwarzanie → Wynik            │
│ │  (cały zbiór)           │    (jednorazowe)                   │
│ └─────────────────────────┘                                    │
│                                                                 │
│ STREAMING:                                                      │
│ ─────●────●──●─────●──●────●───────→ (nieskończony strumień)   │
│      │    │  │     │  │    │                                    │
│      ↓    ↓  ↓     ↓  ↓    ↓                                    │
│   [Przetwarzanie ciągłe] → Wyniki w czasie rzeczywistym        │
│                                                                 │
│ Cechy strumieni:                                                │
│ • Nieograniczone (unbounded)                                   │
│ • Ciągłe napływanie                                            │
│ • Brak możliwości przechowania wszystkiego                     │
│ • Wymagana niska latencja                                      │
│ • Dane mogą być nieuporządkowane (out-of-order)               │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Modele przetwarzania

#### Event Time vs Processing Time

```
Event Time:     Kiedy zdarzenie faktycznie nastąpiło
Processing Time: Kiedy zdarzenie dotarło do systemu

Timeline:
Event time:     ─●─────●───●─────────●───→
                 E1    E2  E3        E4

Processing:     ───●───────●──●──●───────→
                   E1      E3 E2 E4 (różna kolejność!)

Watermark: znacznik postępu event time
  "Wszystkie zdarzenia do czasu T już dotarły"
```

#### Windowing (okna czasowe)

```
┌─────────────────────────────────────────────────────────────────┐
│ TUMBLING WINDOW (rozłączne):                                    │
│ ├────────┤├────────┤├────────┤├────────┤                       │
│ │ Window1││ Window2││ Window3││ Window4│                       │
│                                                                 │
│ SLIDING WINDOW (nakładające się):                              │
│ ├────────────┤                                                  │
│     ├────────────┤                                              │
│         ├────────────┤                                          │
│             ├────────────┤                                      │
│                                                                 │
│ SESSION WINDOW (oparte na aktywności):                         │
│ ├────┤    ├──────────┤  ├───┤     ├─────┤                      │
│ session1    session2    s3       session4                      │
│        gap         gap      gap                                 │
│                                                                 │
│ GLOBAL WINDOW:                                                  │
│ ├─────────────────────────────────────────────────────→        │
│ (jedno okno, trigger decyduje kiedy emitować)                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3. Platformy Stream Processing

#### Apache Kafka Streams

```java
StreamsBuilder builder = new StreamsBuilder();

KStream<String, String> source = builder.stream("input-topic");

KTable<Windowed<String>, Long> counts = source
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count();

counts.toStream().to("output-topic");

// Cechy:
// • Library (nie cluster)
// • Exactly-once semantics
// • Stateful processing z RocksDB
// • Integracja z Kafka ecosystem
```

#### Apache Flink

```java
DataStream<Event> stream = env.addSource(new FlinkKafkaConsumer<>(...));

DataStream<Result> result = stream
    .keyBy(event -> event.getKey())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new MyAggregateFunction())
    .process(new MyProcessFunction());

// Cechy:
// • True streaming (nie micro-batch)
// • Event time processing
// • Exactly-once state
// • Savepoints & checkpoints
// • Complex Event Processing (CEP)
```

#### Apache Spark Structured Streaming

```python
df = spark.readStream \
    .format("kafka") \
    .option("subscribe", "events") \
    .load()

result = df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window("timestamp", "5 minutes"),
        "userId"
    ) \
    .count()

query = result.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Cechy:
# • Micro-batch (domyślnie) lub Continuous
# • Unified batch + streaming API
# • Catalyst optimizer
# • Integracja z Spark ecosystem
```

---

### 4. Porównanie platform

| Cecha | Kafka Streams | Flink | Spark Streaming |
|-------|---------------|-------|-----------------|
| **Model** | True streaming | True streaming | Micro-batch |
| **Deployment** | Library | Cluster | Cluster |
| **Latency** | Niska | Bardzo niska | Średnia (~100ms) |
| **State** | RocksDB | RocksDB/heap | In-memory/external |
| **Exactly-once** | Tak | Tak | Tak |
| **SQL** | KSQL | Flink SQL | Spark SQL |
| **CEP** | Ograniczone | Tak (FlinkCEP) | Nie natywnie |

---

### 5. Algorytmy strumieniowe

#### Approximate counting - HyperLogLog

```
Problem: Zlicz unikalne elementy w strumieniu
         (bez przechowywania wszystkich)

HyperLogLog:
• O(1) space (kilka KB)
• ~2% error dla 12-bit registers
• Używa hash → trailing zeros

Przykład: Redis PFADD, PFCOUNT
```

#### Frequency estimation - Count-Min Sketch

```
Problem: Estymuj częstość elementów

Count-Min Sketch:
┌─────────────────────────────────┐
│ h1: [3][0][2][5][1][0][4][2]   │
│ h2: [1][2][0][3][4][1][0][2]   │
│ h3: [2][1][3][0][2][1][3][0]   │
└─────────────────────────────────┘

Query(x): min(h1[hash1(x)], h2[hash2(x)], h3[hash3(x)])

• Overestimates (never underestimates)
• Tunable accuracy vs space
```

#### Sampling - Reservoir Sampling

```
Problem: Równomiernie próbkuj k elementów
         ze strumienia o nieznanej długości

Algorithm:
1. Zachowaj pierwsze k elementów
2. Dla i-tego elementu (i > k):
   - Z prawdopodobieństwem k/i zamień
     losowy element w reservoir

Gwarancja: Każdy element ma szansę k/n
```

---

### 6. Obsługa opóźnień i Out-of-Order

```
┌─────────────────────────────────────────────────────────────────┐
│ WATERMARKS + LATE DATA                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Stream:    ─●(t=1)──●(t=5)──●(t=3)──●(t=8)──●(t=2)───→         │
│                       ↑                       ↑                 │
│                    out-of-order           late data            │
│                                                                 │
│ Watermark: "Prawdopodobnie wszystkie events do t=X dotarły"    │
│                                                                 │
│ Strategie dla late data:                                        │
│ 1. DROP: Ignoruj spóźnione (najprostsze)                       │
│ 2. RECOMPUTE: Przelicz okno (kosztowne)                        │
│ 3. SIDE OUTPUT: Zapisz do osobnego strumienia                  │
│ 4. ALLOWED LATENESS: Czekaj dodatkowo N czasu                  │
│                                                                 │
│ Flink:                                                          │
│   .allowedLateness(Time.minutes(5))                            │
│   .sideOutputLateData(lateOutputTag)                           │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7. Exactly-Once Semantics

```
┌─────────────────────────────────────────────────────────────────┐
│ GWARANCJE PRZETWARZANIA:                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ AT-MOST-ONCE:                                                   │
│   Fire-and-forget, możliwa utrata danych                       │
│                                                                 │
│ AT-LEAST-ONCE:                                                  │
│   Retry przy failure, możliwe duplikaty                        │
│                                                                 │
│ EXACTLY-ONCE:                                                   │
│   Każde zdarzenie przetworzone dokładnie raz                   │
│                                                                 │
│ Implementacja (Flink/Kafka):                                    │
│ • Checkpointing (periodic snapshots)                           │
│ • Transactional sinks (Kafka transactions)                     │
│ • Barrier alignment                                             │
│ • Idempotent operations                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

### 8. Use Cases

| Use Case | Technologia | Opis |
|----------|-------------|------|
| **Fraud detection** | Flink CEP | Pattern matching w czasie rzeczywistym |
| **IoT analytics** | Kafka Streams | Agregacja danych z sensorów |
| **Real-time dashboards** | Spark + Druid | Metryki biznesowe |
| **Log analysis** | ELK + Kafka | Centralizacja logów |
| **Recommendations** | Flink | Real-time personalizacja |

---

## 🧠 Mnemoniki

### "TWSS = Tumbling, Window, Sliding, Session":
Cztery typy okien czasowych

### "Flink = Fast, Spark = Safe":
Flink najszybszy (true streaming), Spark bezpieczny (micro-batch)

### "HLL = Hash, Leading zeros, Log":
HyperLogLog do zliczania unikalnych

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy micro-batch a kiedy true streaming?"
**Odpowiedź:** True streaming (Flink): ultra-low latency, CEP, event-time critical. Micro-batch (Spark): wyższa przepustowość, łatwiejsza integracja z batch, mniej wrażliwe na anomalie.

### Q2: "Jak obsłużyć skoki danych (spikes)?"
**Odpowiedź:** Backpressure (Flink automatycznie), buffering, auto-scaling (Kubernetes), rate limiting na źródle, spillage to disk.

### Q3: "Co to jest checkpointing?"
**Odpowiedź:** Periodic snapshots stanu (Flink). Przy failure - restart od ostatniego checkpoointu. Barrier synchronizuje snapshot między operatorami. Incremental checkpoints dla dużych stanów.

---

## 🎯 Kluczowe punkty

1. **Streaming:** Unbounded, continuous, low latency
2. **Windowing:** Tumbling, Sliding, Session, Global
3. **Event time vs Processing time:** Watermarks
4. **Platforms:** Flink (true), Spark (micro-batch), Kafka Streams (library)
5. **Exactly-once:** Checkpointing + transactions

---

## 📖 Źródła

1. Kleppmann - "Designing Data-Intensive Applications"
2. Apache Flink Documentation
3. Spark Structured Streaming Guide
4. Kafka Streams Documentation
