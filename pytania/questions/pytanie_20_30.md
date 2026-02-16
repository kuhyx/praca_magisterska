## PYTANIE 20/30: Analityka danych strumieniowych

**Rozwiązania analityczne na danych strumieniowych.**

---

### Tło pojęciowe — słowniczek

**Dane strumieniowe (streaming data)** — ciągły, potencjalnie nieskończony przepływ zdarzeń (events) przychodzących w czasie rzeczywistym. Przykłady: kliknięcia użytkowników, odczyty sensorów IoT, transakcje bankowe, logi serwerów. W odróżnieniu od danych wsadowych (batch): nie możesz „poczekać na wszystkie" — musisz analizować na bieżąco.

    Batch:      [cały zbiór] → analiza → wynik     (minuty/godziny)
    Streaming:  event → event → event → ...→ analiza ciągła    (ms/sekundy)

**Strumień (stream)** — abstrakcja: nieograniczona (unbounded) sekwencja zdarzeń, każde ze stemplem czasowym. Musisz przetwarzać „w locie" — nie mieścisz wszystkiego w pamięci.

---

**Event Time vs Processing Time:**
- **Event Time** — moment GDY zdarzenie nastąpiło (np. kliknięcie o 14:00:05)
- **Processing Time** — moment GDY system przetwarza zdarzenie (np. o 14:00:07)
- Różnica wynika z opóźnień sieciowych. Zdarzenia mogą przychodzić **out-of-order** (pozamiejscowe).

    Zdarzenie A (event time 14:00:01) → dociera o 14:00:05
    Zdarzenie B (event time 14:00:03) → dociera o 14:00:04
    B dociera PRZED A, mimo że A było wcześniej!

**Watermark** — znacznik postępu: „z dużym prawdopodobieństwem nie przyjdą już zdarzenia z event time < W". Pozwala systemowi zdecydować, kiedy zamknąć okno i wyemitować wynik. Zdarzenia po watermarku = „late data" (spóźnione).

---

**Okno czasowe (window)** — mechanizm grupowania zdarzeń w strumienia w skończone porcje do analizy:

**Tumbling window (okno przerzutne)** — stały rozmiar, rozłączne. Np. „liczba kliknięć co 5 minut".

    |---5min---|---5min---|---5min---|
    [events A] [events B] [events C]   ← 0 nakładania

**Sliding window (okno przesuwne)** — stały rozmiar + krok przesunięcia. Nakładają się. Np. „średnia z 10 min, co 1 min".

    |----10min----|
       |----10min----|
          |----10min----|              ← nakładanie

**Session window (okno sesji)** — dynamiczny rozmiar, oparte na aktywności. Nowa sesja po przerwie (gap). Np. „sesja użytkownika: od pierwszego kliknięcia do 30 min nieaktywności".

**Global window** — jedno okno na cały strumień. Trigger decyduje kiedy wyemitować wynik.

---

**True streaming vs Micro-batch:**
- **True streaming** — przetwarzanie event-by-event. Niższa latencja. Kafka Streams, Flink.
- **Micro-batch** — grupowanie zdarzeń w małe paczki (np. co 100ms) i przetwarzanie batch. Spark Streaming. Prostsza semantyka, ale wyższa latencja.

**Kafka Streams** — biblioteka (nie klaster!) do przetwarzania strumieni Kafka. Działa w procesie aplikacji Java. Niska latencja, exactly-once. Stateful processing (windows, joins).

**Apache Flink** — rozproszony silnik do true streaming. Bardzo niska latencja (<10ms). Natywne wsparcie event time, windows, stateful processing. Exactly-once. Deployment jako klaster.

**Spark Streaming** — rozszerzenie Apache Spark. Model micro-batch (~100ms+). Średnia latencja, ale korzysta z ekosystemu Spark (SQL, ML). Exactly-once.

---

**Algorytmy strumieniowe (probabilistyczne):**

**HyperLogLog** — estymacja liczby unikalnych elementów (cardinality). Zużywa O(1) pamięci (~1.5 KB) niezależnie od liczby elementów. Błąd ~2%.

    100 mln unikalnych URL-i → HyperLogLog odpowiada "~100 mln ± 2%"
    Pamięć: 1.5 KB zamiast ~800 MB (hash set)

**Count-Min Sketch** — estymacja częstości elementów. Macierz d×w z hashami. Gwarantuje overestimates (nigdy nie zaniży). O(1) per query/update.

    "Ile razy pojawił się IP 192.168.1.1?" → CMS: ~4523 (± ε·N)

**Reservoir Sampling** — równomierne próbkowanie k elementów ze strumienia o nieznanym rozmiarze n. Każdy element ma szansę k/n. O(k) pamięci.

**Late data strategies:**
- **Drop** — odrzuć spóźnione zdarzenia
- **Recompute** — przelicz okno ponownie
- **Side output** — przekieruj do osobnego strumienia do ręcznej analizy
- **Allowed lateness** — czekaj dodatkowy czas przed zamknięciem okna

---

### Rozwiązania analityczne — przegląd

Rozwiązanie analityczne na strumieniu = odpowiedź na pytanie biznesowe w czasie rzeczywistym, gdy dane przychodzą ciągle i nie można ich wszystkich zapamiętać. Trzy filary: **windowing** (jak grupować), **platformy** (gdzie przetwarzać), **algorytmy probabilistyczne** (jak liczyć w O(1) pamięci).

---

### Rozwiązanie 1 — Analityka okienna (Windowing)

Problem: strumień jest nieskończony, a analiza wymaga skończonej porcji danych. Okno wyodrębnia fragment strumienia do obliczenia agregatu (count, sum, avg, max).

**4 typy okien:**

| Okno | Rozmiar | Nakładanie | Kiedy użyć |
|------|---------|------------|------------|
| **Tumbling** | stały | rozłączne | raporty okresowe: „kliknięcia co 5 min" |
| **Sliding** | stały + krok | nakładające | średnie kroczące: „avg(10 min) co 1 min" |
| **Session** | dynamiczny (gap) | rozłączne per klucz | sesje użytkowników: „aktywność do 30 min przerwy" |
| **Global** | cały strumień | — | trigger-based: „emituj po N zdarzeniach" |

**Przykład — Tumbling window (fraud detection):**

    Strumień transakcji bankowych, okno = 1 minuta:
    [14:00–14:01] → 3 transakcje z karty X → OK
    [14:01–14:02] → 47 transakcji z karty X → ALERT! (>10 = podejrzane)

**Przykład — Sliding window (monitoring SLA):**

    Okno = 5 min, krok = 1 min (nakładanie):
    t=14:05 → avg latency [14:00–14:05] = 120ms ✓
    t=14:06 → avg latency [14:01–14:06] = 340ms ✗ → alert

**Event Time vs Processing Time:**
- Okna na **event time** = poprawne biznesowo (kiedy zdarzenie faktycznie nastąpiło)
- Okna na **processing time** = prostsze, ale podatne na out-of-order delivery
- **Watermark** rozwiązuje problem: „z prawdopodobieństwem ~100% nie przyjdą zdarzenia z event time < W"

---

### Rozwiązanie 2 — Platformy przetwarzania strumieniowego

| Cecha | Kafka Streams | Apache Flink | Spark Streaming |
|-------|---------------|--------------|-----------------|
| **Model** | event-by-event | event-by-event | micro-batch (~100ms) |
| **Deployment** | library (w JVM) | klaster | klaster |
| **Latencja** | ~1–10 ms | < 10 ms | 100 ms – sekundy |
| **Exactly-once** | tak (Kafka TXN) | tak (checkpointing) | tak (WAL) |
| **State management** | RocksDB local | RocksDB + checkpoints | in-memory/external |
| **Okna** | tumbling, sliding, session | wszystkie + custom | tumbling, sliding |
| **Use case** | transformacja Kafka → Kafka | złożona analityka real-time | ETL z ekosystemem Spark |

**True streaming vs Micro-batch — co wybrać?**

    True streaming (Flink, Kafka Streams):
      Latencja:  < 10 ms    ← trade fraud, click tracking
      Semantyka: event-by-event
      Złożoność: wyższa (watermarks, state, exactly-once)

    Micro-batch (Spark Streaming):
      Latencja:  ~100 ms – sekundy
      Semantyka: mini-batch (prostsza, batch-like API)
      Ekosystem: Spark SQL, MLlib → łatwa integracja z ML

**Architektura Lambda vs Kappa:**

    Lambda: [batch layer (Spark)] + [speed layer (Flink)] → merge
            Dwa systemy, dwa kody — skomplikowane ale pewne

    Kappa:  [streaming only (Flink/Kafka)] → replay z Kafka
            Jeden system — prostsze, ale replay = I/O koszt

---

### Rozwiązanie 3 — Algorytmy probabilistyczne (Sketches)

Problem: na strumieniu nie zmieścisz WSZYSTKICH danych w pamięci. Algorytmy probabilistyczne dają przybliżone odpowiedzi w **O(1) pamięci** z gwarantowanym błędem.

| Algorytm | Pytanie | Pamięć | Błąd | Przykład |
|----------|---------|--------|------|----------|
| **HyperLogLog** | „Ile unikalnych?" | ~1.5 KB | ~2% | unique visitors na stronie |
| **Count-Min Sketch** | „Ile razy element X?" | d×w counters | ε·N (overestimate) | częstość IP w logach |
| **Bloom Filter** | „Czy element X był?" | m bitów | false positives, 0 false neg | cache: „czy URL widziany?" |
| **Reservoir Sampling** | „Losowa próbka k z n?" | O(k) | dokładna (nie przybliżona) | próbka logów do debugowania |
| **T-Digest** | „Jaki percentyl?" | O(δ) | <1% na ogonach | p99 latency monitorowanie |

**Dlaczego HyperLogLog zużywa O(1)?**

    Idea: hashuj każdy element, licz pozycję pierwszego bitu 1.
    Jeśli widzisz dużo zer na początku → prawdopodobnie dużo unikalnych.

    100 mln unikalnych URL-i:
    - HashSet: ~800 MB pamięci (8 bajtów × 10⁸)
    - HyperLogLog: 1.5 KB pamięci, odpowiedź ~100 mln ± 2%
    - Oszczędność: 500 000× mniej pamięci!

**Count-Min Sketch — jak działa:**

    Macierz d wierszy × w kolumn (np. 5 × 2048), d funkcji hashowych.
    Insert("X"): dla każdego hash h_i, zwiększ cell[i][h_i("X")]++
    Query("X"):  min over i of cell[i][h_i("X")]
    Gwarancja: nigdy nie ZANIŻY (overestimate, no underestimate)

---

### Rozwiązanie 4 — Obsługa opóźnień i spójność

**Problem late data:** zdarzenie z event time 14:00:01 przychodzi o 14:00:30, gdy okno [14:00–14:05] już zamknięte.

| Strategia | Opis | Trade-off |
|-----------|------|-----------|
| **Drop** | odrzuć spóźnione | proste, ale utrata danych |
| **Allowed lateness** | czekaj dodatkowy czas (np. +5 min) | wyższe zużycie pamięci |
| **Recompute** | przelicz okno z nowym zdarzeniem | poprawne ale kosztowne |
| **Side output** | przekieruj late events do osobnego strumienia | elastyczne, ręczna analiza |

**Exactly-once semantics** — gwarancja, że każde zdarzenie wpływa na wynik dokładnie raz, mimo awarii:
- **At-most-once** — mogą zginąć (szybkie, proste)
- **At-least-once** — mogą się zduplikować (retry)
- **Exactly-once** — żadnych duplikatów ani strat (checkpoint + transakcje, kosztowne)

    Flink: distributed snapshots (algorytm Chandy-Lamport) → checkpoint co N ms
    Kafka Streams: transakcje Kafka (idempotent producer + TX coordinator)
    Spark: WAL (Write-Ahead Log) + idempotent sinks

---

### Rozwiązanie 5 — CEP (Complex Event Processing)

Wykrywanie złożonych wzorców w strumieniach zdarzeń. Reguły definiowane deklaratywnie.

    Pattern: "Jeśli 3 nieudane logowania z tego samego IP w ciągu 5 minut,
             a potem udane logowanie z INNEGO IP → alert: konto przejęte"

    Flink CEP:
    Pattern.<LoginEvent>begin("fails")
        .where(event -> !event.isSuccess())
        .times(3).within(Time.minutes(5))
        .next("success")
        .where(event -> event.isSuccess())

Zastosowania: fraud detection, cybersecurity, monitoring IoT, trading algorytmiczny.

### Etymologia

**Flink** — niem. „flink" = zwinny/szybki (TU Berlin, 2014). **Spark** — „iskra"; Matei Zaharia (UC Berkeley, 2012). **HyperLogLog** — Philippe Flajolet et al. (2007); „Hyper" = ulepszenie LogLog; „LogLog" = zużywa log(log(n)) pamięci. **Count-Min Sketch** — Cormode & Muthukrishnan (2005); „sketch" = probabilistyczny skrót danych. **Reservoir Sampling** — Jeffrey Vitter (1985); „reservoir" = stały zbiornik prób. **Watermark** — znacznik postępu czasu zdarzeń w strumieniu.

### Jak zapamiętać

- **4 okna: „TSSG"** — Tumbling, Sliding, Session, Global
- **Flink = szybki (true streaming)**, Spark = safe (micro-batch)
- **HyperLogLog = „ile unikalnych?" z kilobajtem pamięci**

