## PYTANIE 20/30: Analityka danych strumieniowych

**Rozwiązania analityczne na danych strumieniowych.**

---

### Tło pojęciowe — słowniczek

**Dane strumieniowe (streaming data)** — ciągły, potencjalnie nieskończony przepływ zdarzeń (events) przychodzących w czasie rzeczywistym. Przykłady: kliknięcia użytkowników, odczyty sensorów IoT, transakcje bankowe, logi serwerów. W odróżnieniu od danych wsadowych (batch): nie możesz „poczekać na wszystkie" — musisz analizować na bieżąco.

![Batch vs Streaming](img/q20_batch_vs_streaming.png)

**Strumień (stream)** — abstrakcja: nieograniczona (unbounded) sekwencja zdarzeń, każde ze stemplem czasowym. Musisz przetwarzać „w locie" — nie mieścisz wszystkiego w pamięci.

---

**Event Time vs Processing Time:**
- **Event Time** — moment GDY zdarzenie nastąpiło (np. kliknięcie o 14:00:05)
- **Processing Time** — moment GDY system przetwarza zdarzenie (np. o 14:00:07)
- Różnica wynika z opóźnień sieciowych. Zdarzenia mogą przychodzić **out-of-order** (pozamiejscowe).

**Watermark** — znacznik postępu: „z dużym prawdopodobieństwem nie przyjdą już zdarzenia z event time < W". Pozwala systemowi zdecydować, kiedy zamknąć okno i wyemitować wynik. Zdarzenia po watermarku = „late data" (spóźnione).

---

**Okno czasowe (window)** — mechanizm grupowania zdarzeń w strumienia w skończone porcje do analizy:

**Tumbling window (okno przerzutne)** — stały rozmiar, rozłączne. Np. „liczba kliknięć co 5 minut".

**Sliding window (okno przesuwne)** — stały rozmiar + krok przesunięcia. Nakładają się. Np. „średnia z 10 min, co 1 min".

**Session window (okno sesji)** — dynamiczny rozmiar, oparte na aktywności. Nowa sesja po przerwie (gap). Np. „sesja użytkownika: od pierwszego kliknięcia do 30 min nieaktywności".

**Global window** — jedno okno na cały strumień. Trigger decyduje kiedy wyemitować wynik.

![4 typy okien](img/q20_window_types.png)

---

**True streaming vs Micro-batch:**
- **True streaming** — przetwarzanie event-by-event. Niższa latencja. Kafka Streams, Flink.
- **Micro-batch** — grupowanie zdarzeń w małe paczki (np. co 100ms) i przetwarzanie batch. Spark Streaming. Prostsza semantyka, ale wyższa latencja.

**Kafka Streams** — biblioteka (nie klaster!) do przetwarzania strumieni Kafka. Działa w procesie aplikacji Java. Niska latencja, exactly-once. Stateful processing (windows, joins).

**Apache Flink** — rozproszony silnik do true streaming. Bardzo niska latencja (<10ms). Natywne wsparcie event time, windows, stateful processing. Exactly-once. Deployment jako klaster.

**Spark Streaming** — rozszerzenie Apache Spark. Model micro-batch (~100ms+). Średnia latencja, ale korzysta z ekosystemu Spark (SQL, ML). Exactly-once.

---

**Algorytmy strumieniowe (probabilistyczne):**

**HyperLogLog** — estymacja liczby unikalnych elementów (cardinality). Zużywa O(1) pamięci (~1.5 KB) niezależnie od liczby elementów. Błąd ~2%. Np. 100 mln unikalnych URL-i → HyperLogLog: ~100 mln ± 2%, pamięć: 1.5 KB zamiast ~800 MB (hash set).

**Count-Min Sketch** — estymacja częstości elementów. Macierz d×w z hashami. Gwarantuje overestimates (nigdy nie zaniży). O(1) per query/update.

**Reservoir Sampling** — równomierne próbkowanie k elementów ze strumienia o nieznanym rozmiarze n. Każdy element ma szansę k/n. O(k) pamięci.

**Late data strategies:**
- **Drop** — odrzuć spóźnione zdarzenia
- **Recompute** — przelicz okno ponownie
- **Side output** — przekieruj do osobnego strumienia do ręcznej analizy
- **Allowed lateness** — czekaj dodatkowy czas przed zamknięciem okna

---

### Rozwiązania analityczne — przegląd

Rozwiązanie analityczne na strumieniu = odpowiedź na pytanie biznesowe w czasie rzeczywistym, gdy dane przychodzą ciągle i nie można ich wszystkich zapamiętać. Dwa filary: **windowing** (jak grupować zdarzenia w skończone porcje) i **platformy** (gdzie i jak przetwarzać strumień).

---

### Rozwiązanie 1 — Analityka okienna (Windowing)

Problem: strumień jest nieskończony, a analiza wymaga skończonej porcji danych. Okno wyodrębnia fragment strumienia do obliczenia agregatu (count, sum, avg, max).

**Analogia:** Strumień to rzeka. Nie możesz zmierzyć „wszystkiej wody w rzece", ale możesz nabierać wiadra (okna) i mierzyć każde z nich.

**4 typy okien — TSSG (Tumbling, Sliding, Session, Global):**

| Okno | Rozmiar | Nakładanie | Kiedy użyć |
|------|---------|------------|------------|
| **Tumbling** | stały | rozłączne | raporty okresowe: „kliknięcia co 5 min" |
| **Sliding** | stały + krok | nakładające | średnie kroczące: „avg(10 min) co 1 min" |
| **Session** | dynamiczny (gap) | rozłączne per klucz | sesje użytkowników: „aktywność do 30 min przerwy" |
| **Global** | cały strumień | — | trigger-based: „emituj po N zdarzeniach" |

---

**Tumbling Window — szczegółowo:**

Stały rozmiar, zero nakładania. Każde zdarzenie trafia do DOKŁADNIE jednego okna.

**Przykład — fraud detection (tumbling 1 min):**

![Tumbling window — fraud detection](img/q20_tumbling_fraud.png)

**Przykład — raporty sprzedaży (tumbling 1h):**

Sklep internetowy, okno = 1 godzina: [10:00-11:00] zamówienia: 142, suma: 28 400 zł | [11:00-12:00] zamówienia: 89, suma: 17 800 zł | [12:00-13:00] zamówienia: 201, suma: 40 200 zł (szczyt). Dashboard aktualizuje się CO GODZINĘ.

---

**Sliding Window — szczegółowo:**

Stały rozmiar + krok przesunięcia. Okna NAKŁADAJĄ SIĘ → jedno zdarzenie trafia do WIELU okien.

**Dlaczego nakładanie jest przydatne?** Tumbling 5 min: nagły skok dokładnie na granicę okien → podzielony na dwa okna, żaden nie pokaże pełnego obrazu. Sliding 5 min / 1 min: okna co minutę → skok ZAWSZE widoczny w co najmniej jednym pełnym oknie.

**Przykład — monitoring SLA (sliding 5 min, krok 1 min):**

![Sliding window — monitoring SLA](img/q20_sliding_sla.png)

---

**Session Window — szczegółowo:**

Rozmiar DYNAMICZNY, zależy od aktywności. Gap (przerwa) definiuje koniec sesji.

![Session window — sesje użytkowników](img/q20_session_users.png)

**Przykład — analiza zachowań użytkowników (e-commerce, gap = 30 min):**
- Sesja Anny: strona główna → kategoria → produkt → koszyk → ZAKUP (22 min, 5 stron, konwersja: TAK)
- Sesja Boba: strona główna → kategoria → wychodzi (3 min, 2 strony, konwersja: NIE)
- Metryka: avg session duration, pages/session, conversion rate

---

**Global Window:**

Jedno okno na cały strumień. Potrzebujesz **triggera** aby wyemitować wynik (np. „emituj po każdych 1000 zdarzeń" lub „emituj co 1 minutę" → de facto tumbling na processing time).

---

**Event Time vs Processing Time + Watermark:**

![Event Time vs Processing Time + Watermark](img/q20_event_vs_processing_time.png)

- Okna na **event time** = poprawne biznesowo (kiedy zdarzenie faktycznie nastąpiło)
- Okna na **processing time** = prostsze, ale podatne na out-of-order delivery
- **Watermark** rozwiązuje problem: „z prawdopodobieństwem ~100% nie przyjdą zdarzenia z event time < W"

**Watermark krok po kroku:** e1 (event=14:00:01, arrives=14:00:02) → watermark=14:00:01. e2 (event=14:00:03, arrives=14:00:03) → watermark=14:00:03. e3 (event=14:00:02, arrives=14:00:04) → LATE! (event < watermark). Okno [14:00:00-14:00:05]: watermark przeszedł 14:00:05 → okno ZAMKNIĘTE. Strategia: allowed lateness +2s → jeszcze przyjmij, albo drop/side output.

**Mnemonik okien — „TSSG jak Termometr/Suwak/Sesja/Glob":** T = Tumbling = Termometr (stały odczyt co X minut, ZERO nakładania). S = Sliding = Suwak (przesuwasz suwak = nakładanie). S = Session = Sesja (zależy od aktywności użytkownika). G = Global = Glob (jedna wielka kula = cały strumień). Albo: „TeSt SG" — Testujesz Strumieniowe Grupowanie.

---

**Late data — 4 strategie (mnemonik „DRAS"):**

![Late data — 4 strategie DRAS](img/q20_late_data_strategies.png)

---

### Rozwiązanie 2 — Platformy przetwarzania strumieniowego

**Analogia:** Masz fabrykę (dane strumieniowe). Potrzebujesz maszyny do ich przetwarzania. Trzy główne maszyny na rynku — każda z inną filozofią.

![Ekosystem streamingu](img/q20_streaming_ecosystem.png)

| Cecha | Kafka Streams | Apache Flink | Spark Streaming |
|-------|---------------|--------------|-----------------|
| **Model** | event-by-event | event-by-event | micro-batch (~100ms) |
| **Deployment** | library (w JVM) | klaster | klaster |
| **Latencja** | ~1–10 ms | < 10 ms | 100 ms – sekundy |
| **Exactly-once** | tak (Kafka TXN) | tak (checkpointing) | tak (WAL) |
| **State management** | RocksDB local | RocksDB + checkpoints | in-memory/external |
| **Okna** | tumbling, sliding, session | wszystkie + custom | tumbling, sliding |
| **Skalowalność** | liczba partycji Kafka | auto-scaling klaster | klaster Spark |
| **Use case** | transformacja Kafka → Kafka | złożona analityka real-time | ETL z ekosystemem Spark |

---

**True streaming vs Micro-batch — wizualnie:**

![True Streaming vs Micro-batch](img/q20_true_vs_microbatch.png)

**Kiedy co wybrać? (drzewo decyzyjne)**

![Drzewo decyzyjne wyboru platformy](img/q20_decision_tree.png)

---

**Kafka Streams — architektura (library, nie klaster!):**

![Kafka Streams — architektura](img/q20_kafka_streams_arch.png)
    
    Kluczowe: NIE potrzebujesz osobnego klastra!
    Skalujesz = dodajesz instancje swojej aplikacji.
    Partycje Kafki automatycznie rozdzielane między instancje.

**Przykład — Kafka Streams (zliczanie kliknięć co 5 min):**

    StreamsBuilder builder = new StreamsBuilder();
    
    builder.stream("clicks")                       // input topic
        .groupByKey()                              // grupuj po user_id
        .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))  // tumbling 5 min
        .count()                                   // zlicz
        .toStream()
        .to("click-counts");                       // output topic
    
    // Deploy = uruchom JAR. Skalujesz = uruchom więcej JARów.

---

**Apache Flink — architektura (klaster):**

![Apache Flink — architektura](img/q20_flink_arch.png)

**Exactly-once w Flinku (algorytm Chandy-Lamport):**

Exactly-once w Flinku działa algorytmem Chandy-Lamport: Job Manager co N ms wysyła „barrier" przez graf przetwarzania. Gdy operator otrzyma barrier → zapisuje stan do checkpointu (HDFS/S3). Po awarii → odtworzenie z ostatniego checkpointu.

**Przykład — Flink (średnia temperatura sensorów co 10s):**

    DataStream<SensorReading> readings = env.addSource(kafkaConsumer);
    
    readings
        .keyBy(r -> r.sensorId)                // grupuj po sensorze
        .window(TumblingEventTimeWindows.of(Time.seconds(10)))
        .aggregate(new AvgTemperature())       // średnia w oknie
        .addSink(new AlertSink());             // sink: alert jeśli > 50°C
    
    // Flink obsługuje event time natywnie → poprawne wyniki
    // mimo out-of-order zdarzeń z sensorów

---

**Spark Streaming — architektura (micro-batch):**

![Spark Streaming — architektura](img/q20_spark_streaming_arch.png)

ZALETA: ten sam kod co batch Spark → łatwa migracja. WADA: latencja = rozmiar micro-batcha (min ~100ms).

---

**Architektura Lambda vs Kappa — wizualnie:**

![Lambda vs Kappa — architektura](img/q20_lambda_vs_kappa.png)

Lambda: 2 systemy, 2 bazy kodu, 2× utrzymanie. Kappa: 1 system, 1 kod. Potrzebujesz przeliczyć historię? → Replay z Kafka od początku. WADA: replay = dużo I/O, Kafka musi trzymać historię.

**Porównanie Lambda vs Kappa:**

![Lambda vs Kappa — porównanie](img/q20_lambda_kappa_table.png)

---

**Exactly-once — porównanie mechanizmów:**

![Exactly-Once — mechanizmy](img/q20_exactly_once.png)

**Mnemonik platform — „KFS: Kawa, Filiżanka, Szklanka":** K = Kafka Streams = Kawa (szybka, w filiżance = w Twojej JVM), F = Flink = Filiżanka (elegancka, pełna = true streaming + state), S = Spark = Szklanka (duża, paczka = micro-batch). Albo: „Kafka = lekki (library), Flink = fastest, Spark = safest (batch-like)".

---

### Etymologia

**Flink** — niem. „flink" = zwinny/szybki (TU Berlin, 2014). **Spark** — „iskra"; Matei Zaharia (UC Berkeley, 2012). **Kafka** — Franz Kafka; Jay Kreps (LinkedIn, 2011) — „system zoptymalizowany do pisania" (jak Kafka pisarz). **Watermark** — „znak wodny" — znacznik postępu czasu zdarzeń w strumieniu, analogicznie do znaku wodnego na papierze: niewidoczny, ale wyznacza granicę. **Tumbling** — ang. „koziołkowanie" — okna „przewracają się" jedno po drugim bez przerwy. **Sliding** — ang. „przesuwanie" — okno przesuwa się po osi czasu. **Lambda/Kappa** — litery greckie; Lambda = dwie ścieżki (λ ma dwie nóżki), Kappa = jedna ścieżka (κ prostsza).

### Jak zapamiętać

- **4 okna: „TSSG"** — Tumbling (stały, rozłączne), Sliding (stały+krok, nakładające), Session (gap), Global (trigger)
- **TSSG = „TeSt SG — Testujesz Strumieniowe Grupowanie"**
- **Tumbling = Termometr** (odczyt co X, zero nakładania), **Sliding = Suwak** (przesuwasz = nakładanie)
- **Late data: „DRAS"** — Drop, Recompute, Allowed lateness, Side output
- **Platformy: „KFS"** — Kafka Streams (library, lekki), Flink (fastest, true streaming), Spark (safest, micro-batch)
- **Lambda = λ = 2 nóżki = 2 ścieżki** (batch + speed), **Kappa = κ = 1 ścieżka** (streaming only)
- **Event time vs processing time** — „kiedy NAPRAWDĘ się stało" vs „kiedy system to ZOBACZYŁ"
- **Watermark** — „linia w piasku" = poniżej niej = już na pewno dotarło

