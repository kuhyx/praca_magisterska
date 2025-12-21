# Pytanie 4: Baza danych jako fundament systemów informatycznych

## Pytanie
**"Dlaczego baza danych stanowi dobry fundament do budowy wielu systemów informatycznych?"**

Przedmiot: BD2 (Bazy Danych 2)

---

## 📚 Odpowiedź główna

### Wprowadzenie

Baza danych to **centralny komponent** większości systemów informatycznych, ponieważ zapewnia:
- Trwałe przechowywanie danych
- Współbieżny dostęp
- Integralność i spójność
- Niezależność danych od aplikacji

---

## 1. Kluczowe właściwości baz danych (ACID)

### Transakcyjność - gwarancje ACID

| Właściwość | Opis | Znaczenie |
|------------|------|-----------|
| **A**tomicity (Atomowość) | Transakcja wykonuje się w całości lub wcale | Brak częściowych zmian |
| **C**onsistency (Spójność) | Dane przechodzą z jednego spójnego stanu w drugi | Reguły biznesowe zawsze spełnione |
| **I**solation (Izolacja) | Równoległe transakcje nie widzą swoich zmian | Brak efektów ubocznych |
| **D**urability (Trwałość) | Zatwierdzone zmiany przetrwają awarie | Bezpieczeństwo danych |

### Przykład znaczenia ACID

**Przelew bankowy:**
```sql
BEGIN TRANSACTION;
    UPDATE Konta SET saldo = saldo - 1000 WHERE id = 1;  -- Odejmij
    UPDATE Konta SET saldo = saldo + 1000 WHERE id = 2;  -- Dodaj
COMMIT;
```

Bez ACID:
- Awaria po pierwszym UPDATE = utrata pieniędzy (brak atomowości)
- Saldo < 0 mimo ograniczenia (brak spójności)
- Inna transakcja widzi stan pośredni (brak izolacji)
- Po zatwierdzeniu dane giną (brak trwałości)

---

## 2. Niezależność danych

### Trójpoziomowa architektura ANSI/SPARC

```
┌─────────────────────────────────────────┐
│     Poziom zewnętrzny (widoki)          │  ← Aplikacje widzą różne "okna"
├─────────────────────────────────────────┤
│     Poziom konceptualny (logiczny)      │  ← Struktura logiczna danych
├─────────────────────────────────────────┤
│     Poziom wewnętrzny (fizyczny)        │  ← Sposób przechowywania
└─────────────────────────────────────────┘
```

### Rodzaje niezależności

#### 1. Niezależność fizyczna
Zmiana sposobu przechowywania (indeksy, partycjonowanie, kompresja) **nie wpływa** na aplikacje.

**Przykład:** Dodanie indeksu przyspiesza zapytania bez zmiany kodu aplikacji.

#### 2. Niezależność logiczna
Zmiana struktury logicznej (dodanie kolumn, widoków) **minimalizuje** wpływ na aplikacje.

**Przykład:** Podział tabeli na dwie + widok łączący = stare aplikacje działają bez zmian.

---

## 3. Współbieżność i wielodostęp

### Problem współbieżności

Wiele aplikacji/użytkowników **jednocześnie** korzysta z tych samych danych.

### Mechanizmy kontroli współbieżności

| Mechanizm | Opis | Zastosowanie |
|-----------|------|--------------|
| **Blokady (Locks)** | Pesymistyczne - blokuj przed dostępem | Wysokie konflikty |
| **MVCC** | Optymistyczne - wersjonowanie | Dużo odczytów |
| **Timestamp Ordering** | Szeregowanie po czasie | Systemy rozproszone |
| **Snapshot Isolation** | Izolacja migawkowa | Analityka |

### Poziomy izolacji (SQL Standard)

| Poziom | Dirty Read | Non-repeatable Read | Phantom Read |
|--------|------------|---------------------|--------------|
| READ UNCOMMITTED | Możliwy | Możliwy | Możliwy |
| READ COMMITTED | Niemożliwy | Możliwy | Możliwy |
| REPEATABLE READ | Niemożliwy | Niemożliwy | Możliwy |
| SERIALIZABLE | Niemożliwy | Niemożliwy | Niemożliwy |

---

## 4. Integralność danych

### Mechanizmy wymuszania integralności

#### 1. Ograniczenia deklaratywne
```sql
CREATE TABLE Zamowienia (
    id INT PRIMARY KEY,                          -- Klucz główny
    klient_id INT NOT NULL,                      -- NOT NULL
    data DATE DEFAULT CURRENT_DATE,              -- Wartość domyślna
    kwota DECIMAL(10,2) CHECK (kwota > 0),       -- Warunek CHECK
    FOREIGN KEY (klient_id) REFERENCES Klienci(id)  -- Klucz obcy
);
```

#### 2. Wyzwalacze (Triggers)
```sql
CREATE TRIGGER sprawdz_saldo
BEFORE UPDATE ON Konta
FOR EACH ROW
BEGIN
    IF NEW.saldo < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Brak środków';
    END IF;
END;
```

#### 3. Procedury składowane
Logika biznesowa w bazie = jednolite reguły dla wszystkich aplikacji.

---

## 5. Wydajność i optymalizacja

### Optymalizator zapytań

SZBD automatycznie:
1. **Analizuje zapytanie** (parsing)
2. **Generuje plany wykonania** (alternatywy)
3. **Szacuje koszty** (statystyki)
4. **Wybiera najlepszy plan** (optymalizacja)

### Mechanizmy wydajności

| Mechanizm | Funkcja |
|-----------|---------|
| **Indeksy** | Szybkie wyszukiwanie (B-tree, Hash, GiST) |
| **Buforowanie** | Cache często używanych danych |
| **Partycjonowanie** | Podział dużych tabel |
| **Materializowane widoki** | Prekompilowane złączenia |
| **Query cache** | Cache wyników zapytań |

---

## 6. Bezpieczeństwo

### Wielopoziomowe zabezpieczenia

```
┌─────────────────────────────────────────┐
│  Autoryzacja (GRANT/REVOKE)             │
├─────────────────────────────────────────┤
│  Autentykacja (użytkownicy, role)       │
├─────────────────────────────────────────┤
│  Szyfrowanie (TDE, SSL/TLS)             │
├─────────────────────────────────────────┤
│  Audyt (logi, śledzenie zmian)          │
└─────────────────────────────────────────┘
```

### Kontrola dostępu
```sql
-- Tworzenie roli
CREATE ROLE analityk;
GRANT SELECT ON Sprzedaz TO analityk;

-- Przypisanie użytkownika
GRANT analityk TO jan_kowalski;

-- Widok ograniczający dane
CREATE VIEW MojeZamowienia AS
    SELECT * FROM Zamowienia WHERE sprzedawca = CURRENT_USER;
```

---

## 7. Skalowalność i dostępność

### Skalowanie pionowe (Scale-up)
- Więcej RAM, szybsze CPU, dyski SSD
- Proste, ale ograniczone

### Skalowanie poziome (Scale-out)
- **Replikacja** - kopie do odczytu
- **Sharding** - podział danych między serwery
- **Klastry** - wysoka dostępność

### Wysoka dostępność (HA)

| Rozwiązanie | Opis |
|-------------|------|
| **Replikacja Master-Slave** | Odczyty z replik |
| **Replikacja Master-Master** | Zapisy na wielu węzłach |
| **Failover automatyczny** | Przełączanie przy awarii |
| **Backup/Recovery** | Odtwarzanie po katastrofie |

---

## 8. Standaryzacja i ekosystem

### SQL jako lingua franca
- **Standardowy język** - SQL:2016, SQL:2023
- **Przenośność** - kod działa na różnych SZBD
- **Narzędzia** - uniwersalne IDE, ORM, ETL

### Bogaty ekosystem
- **ORM** (Hibernate, Entity Framework, SQLAlchemy)
- **Narzędzia migracji** (Flyway, Liquibase)
- **Monitorowanie** (Grafana, Datadog)
- **Backup** (pg_dump, mysqldump, RMAN)

---

## 9. Różnorodność modeli danych

### Jeden fundament, wiele modeli

| Model | SZBD | Zastosowanie |
|-------|------|--------------|
| **Relacyjny** | PostgreSQL, MySQL, Oracle | OLTP, dane strukturalne |
| **Dokumentowy** | MongoDB, CouchDB | JSON, elastyczne schematy |
| **Klucz-wartość** | Redis, DynamoDB | Cache, sesje |
| **Grafowy** | Neo4j, Amazon Neptune | Relacje, sieci społeczne |
| **Kolumnowy** | Cassandra, ClickHouse | Analityka, time-series |
| **Czasowy** | TimescaleDB, InfluxDB | IoT, metryki |

### Polyglot Persistence
Nowoczesne systemy często używają **wielu baz** - każda do swojego celu.

---

## 📊 Porównanie: z bazą vs bez bazy

| Aspekt | Bez bazy (pliki) | Z bazą danych |
|--------|------------------|---------------|
| **Współbieżność** | Ręczne blokady | Automatyczna |
| **Integralność** | W kodzie aplikacji | Deklaratywna |
| **Zapytania** | Parsowanie plików | SQL/indeksy |
| **Backup** | Kopiowanie plików | Spójne snapshoty |
| **Skalowanie** | Trudne | Replikacja/sharding |
| **Bezpieczeństwo** | OS-level | Granularne uprawnienia |

---

## 🧠 Mnemoniki

### "ACID" - już sam w sobie mnemonik:
- **A**tomowość - **A**ll or nothing
- **C**onsistency - **C**orrect always
- **I**solation - **I**ndependent transactions
- **D**urability - **D**ata survives

### "BDSM" dla korzyści bazy danych:
- **B**ezpieczeństwo (autoryzacja, audyt)
- **D**ane niezależne (od aplikacji)
- **S**kalowalność (replikacja, sharding)
- **M**echanizmy integralności (FK, CHECK)

### "CIA" dla bezpieczeństwa:
- **C**onfidentiality - kto może czytać
- **I**ntegrity - kto może zmieniać
- **A**vailability - dostępność usługi

### "CRUD = baza umie wszystko":
- **C**reate - INSERT
- **R**ead - SELECT
- **U**pdate - UPDATE
- **D**elete - DELETE

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Wyjaśnij różnicę między blokadami pesymistycznymi a optymistycznymi"

**Odpowiedź:**

| Cecha | Pesymistyczne | Optymistyczne |
|-------|---------------|---------------|
| **Założenie** | Konflikty są częste | Konflikty są rzadkie |
| **Działanie** | Blokuj przed dostępem | Sprawdź przy zatwierdzeniu |
| **Implementacja** | Locki (S, X, IS, IX) | Wersjonowanie (MVCC) |
| **Zaleta** | Gwarancja sukcesu | Brak blokowania |
| **Wada** | Deadlocki możliwe | Rollback przy konflikcie |
| **Zastosowanie** | Dużo zapisów | Dużo odczytów |

**MVCC (Multi-Version Concurrency Control):**
- Każdy zapis tworzy nową wersję wiersza
- Odczyt widzi "migawkę" z początku transakcji
- Brak blokowania między odczytem a zapisem

---

### Q2: "Co to jest CAP theorem i jak wpływa na projektowanie?"

**Odpowiedź:**

**Twierdzenie CAP** (Brewer, 2000):
W systemie rozproszonym można mieć **co najwyżej 2 z 3** właściwości:

- **C**onsistency - wszystkie węzły widzą te same dane
- **A**vailability - każde żądanie otrzymuje odpowiedź
- **P**artition tolerance - system działa mimo podziału sieci

**Konsekwencje:**

| Wybór | Poświęca | Przykład |
|-------|----------|----------|
| **CA** | Partition tolerance | Tradycyjne RDBMS (single node) |
| **CP** | Availability | MongoDB, HBase |
| **AP** | Consistency | Cassandra, DynamoDB |

**Praktyka:** Systemy rozproszone MUSZĄ być P (partycje się zdarzają), więc wybór to C vs A.

---

### Q3: "Kiedy baza relacyjna, a kiedy NoSQL?"

**Odpowiedź:**

| Kryteria | Relacyjna (SQL) | NoSQL |
|----------|-----------------|-------|
| **Struktura danych** | Stała, dobrze zdefiniowana | Zmienna, elastyczna |
| **Transakcje** | ACID wymagane | BASE akceptowalne |
| **Relacje** | Złożone złączenia | Proste lub brak |
| **Skala** | Pionowa (scale-up) | Pozioma (scale-out) |
| **Przykłady** | Finanse, ERP, CRM | Social media, IoT, gaming |

**BASE** (dla NoSQL):
- **B**asically **A**vailable - zazwyczaj dostępny
- **S**oft state - stan może być nieaktualny
- **E**ventually consistent - ostatecznie spójny

---

### Q4: "Jak baza danych wspiera architekturę mikroserwisów?"

**Odpowiedź:**

**Wzorzec: Database per Service**
- Każdy mikroserwis ma **własną bazę**
- Brak bezpośredniego dostępu do cudzych danych
- Komunikacja przez API/eventy

**Wyzwania:**
1. **Rozproszone transakcje** → Saga pattern
2. **Spójność danych** → Event sourcing, CQRS
3. **Złączenia** → Denormalizacja, API composition

**Rozwiązania:**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Zamówienia │     │   Klienci   │     │  Produkty   │
│  (MongoDB)  │     │ (PostgreSQL)│     │   (Redis)   │
└─────────────┘     └─────────────┘     └─────────────┘
       ↓                  ↓                   ↓
       └──────── Message Broker (Kafka) ─────┘
```

---

### Q5: "Co to jest indeks i jakie są rodzaje?"

**Odpowiedź:**

**Indeks** = struktura danych przyspieszająca wyszukiwanie.

| Typ | Struktura | Zastosowanie |
|-----|-----------|--------------|
| **B-tree** | Zbalansowane drzewo | Ogólne, zakresy, sortowanie |
| **Hash** | Tablica mieszająca | Równość (=), bardzo szybki |
| **GiST** | Drzewo uogólnione | Geodane, full-text |
| **GIN** | Inverted index | Tablice, JSONB, full-text |
| **BRIN** | Block Range Index | Duże tabele, dane posortowane |

**Kompromis:**
- Indeks **przyspiesza** SELECT
- Indeks **spowalnia** INSERT/UPDATE/DELETE
- Indeks **zajmuje** miejsce na dysku

---

### Q6: "Wyjaśnij pojęcie normalizacji vs denormalizacji w kontekście wydajności"

**Odpowiedź:**

| Aspekt | Normalizacja | Denormalizacja |
|--------|--------------|----------------|
| **Redundancja** | Minimalna | Celowa |
| **Złączenia** | Wymagane | Minimalne |
| **Zapisy** | Szybkie | Wolniejsze |
| **Odczyty** | Wolniejsze | Szybsze |
| **Spójność** | Łatwa | Trudniejsza |
| **Zastosowanie** | OLTP | OLAP, cache |

**Praktyka:**
- **OLTP** (transakcje) → 3NF/BCNF
- **OLAP** (analityka) → Star/Snowflake schema
- **Cache** → Pełna denormalizacja (Redis)

---

## 🎯 Kluczowe punkty do zapamiętania

1. **ACID** = gwarancje transakcyjne fundamentem niezawodności
2. **Niezależność danych** = zmiany struktury nie psują aplikacji
3. **Współbieżność** = tysiące użytkowników jednocześnie
4. **Integralność** = reguły biznesowe wymuszone w bazie
5. **Optymalizator** = automatyczne przyspieszanie zapytań
6. **Bezpieczeństwo** = wielopoziomowa kontrola dostępu
7. **Skalowalność** = od jednego serwera do klastra globalnego

---

## 📖 Źródła do pogłębienia

1. Date, C.J. - "An Introduction to Database Systems"
2. Kleppmann, M. - "Designing Data-Intensive Applications"
3. Garcia-Molina, Ullman, Widom - "Database Systems: The Complete Book"
4. Hellerstein, Stonebraker - "Readings in Database Systems" (Red Book)
