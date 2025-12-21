# Pytanie 28: Fazy ewolucji modelu danych

## Pytanie
**"Omówić typowe fazy ewolucji modelu danych i pożądane cechy modelu w każdej z faz."**

Przedmiot: MODA (Modelowanie Danych)

---

## 📚 Odpowiedź główna

### 1. Przegląd faz ewolucji

```
┌─────────────────────────────────────────────────────────────────┐
│                   FAZY EWOLUCJI MODELU DANYCH                   │
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │  KONCEPTUALNY │ → │   LOGICZNY   │ → │   FIZYCZNY   │       │
│  │    (CDM)      │   │    (LDM)     │   │    (PDM)     │       │
│  └──────────────┘   └──────────────┘   └──────────────┘       │
│         │                  │                  │                │
│         ↓                  ↓                  ↓                │
│    CO przechowujemy   JAK strukturyzujemy  JAK implementujemy │
│    (biznes)           (logika)            (technologia)       │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Model konceptualny (Conceptual Data Model)

#### Cel
- Zrozumienie dziedziny biznesowej
- Komunikacja z interesariuszami (nietechnicznymi)
- Identyfikacja głównych encji i relacji

#### Cechy pożądane

| Cecha | Opis |
|-------|------|
| **Prostota** | Zrozumiały dla biznesu |
| **Abstrakcja** | Brak szczegółów technicznych |
| **Kompletność** | Wszystkie koncepcje biznesowe |
| **Poprawność** | Zgodność z rzeczywistością biznesową |

#### Notacja i narzędzia

```
Diagram ERD (Entity-Relationship) - uproszczony:

    ┌──────────┐         ┌──────────┐
    │ KLIENT   │ składa  │ZAMÓWIENIE│
    │          │ 1────M  │          │
    └──────────┘         └──────────┘
                              │
                              │ zawiera
                              │ M
                              │
                         ┌──────────┐
                         │ PRODUKT  │
                         │          │
                         └──────────┘

Brak typów danych, kluczy, atrybutów szczegółowych!
Tylko encje i relacje (z krotnością).
```

#### Przykład

```
Model konceptualny dla e-commerce:

Encje: Klient, Zamówienie, Produkt, Kategoria, Dostawca, Płatność

Relacje:
- Klient składa Zamówienia (1:N)
- Zamówienie zawiera Produkty (M:N)
- Produkt należy do Kategorii (N:1)
- Dostawca dostarcza Produkty (M:N)
- Zamówienie ma Płatność (1:1)
```

---

### 3. Model logiczny (Logical Data Model)

#### Cel
- Szczegółowa struktura danych
- Normalizacja
- Definicja atrybutów i kluczy
- Niezależność od DBMS

#### Cechy pożądane

| Cecha | Opis |
|-------|------|
| **Normalizacja** | Minimum 3NF, często BCNF |
| **Integralność** | PK, FK, constraints |
| **Kompletność atrybutów** | Wszystkie pola z typami logicznymi |
| **Dokumentacja** | Słownik danych |
| **Niezależność** | Bez szczegółów implementacji |

#### Notacja

```
ERD szczegółowy (np. Crow's Foot):

┌────────────────────────┐       ┌────────────────────────┐
│ KLIENT                 │       │ ZAMÓWIENIE             │
├────────────────────────┤       ├────────────────────────┤
│ PK klient_id           │───┐   │ PK zamowienie_id       │
│    imie                │   │   │ FK klient_id           │──┐
│    nazwisko            │   └──<│    data_zamowienia     │  │
│    email (UNIQUE)      │       │    status              │  │
│    data_rejestracji    │       │    suma                │  │
└────────────────────────┘       └────────────────────────┘  │
                                          │                   │
                                          │ 1                 │
                                          │                   │
                                 ┌────────────────────────┐  │
                                 │ POZYCJA_ZAMOWIENIA     │  │
                                 ├────────────────────────┤  │
                                 │ PK pozycja_id          │  │
                                 │ FK zamowienie_id       │──┘
                                 │ FK produkt_id          │
                                 │    ilosc               │
                                 │    cena_jednostkowa    │
                                 └────────────────────────┘
```

#### Normalizacja

```
1NF: Atomowe wartości, brak powtarzających się grup
2NF: 1NF + brak częściowych zależności od PK
3NF: 2NF + brak zależności przechodnich
BCNF: Każdy determinant jest kluczem kandydującym
```

---

### 4. Model fizyczny (Physical Data Model)

#### Cel
- Implementacja w konkretnym DBMS
- Optymalizacja wydajności
- Definicja indeksów, partycji, storage

#### Cechy pożądane

| Cecha | Opis |
|-------|------|
| **Wydajność** | Indeksy, denormalizacja gdzie potrzeba |
| **Specyfika DBMS** | Typy danych, funkcje specyficzne |
| **Skalowalność** | Partycjonowanie, sharding |
| **Bezpieczeństwo** | Uprawnienia, szyfrowanie |
| **Backup/Recovery** | Strategia archiwizacji |

#### Przykład DDL (PostgreSQL)

```sql
CREATE TABLE klient (
    klient_id SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_rejestracji TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status klient_status DEFAULT 'aktywny'
);

CREATE INDEX idx_klient_email ON klient(email);
CREATE INDEX idx_klient_nazwisko ON klient(nazwisko);

CREATE TABLE zamowienie (
    zamowienie_id SERIAL PRIMARY KEY,
    klient_id INTEGER NOT NULL REFERENCES klient(klient_id),
    data_zamowienia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status zamowienie_status DEFAULT 'nowe',
    suma DECIMAL(10,2) NOT NULL CHECK (suma >= 0)
) PARTITION BY RANGE (data_zamowienia);

CREATE TABLE zamowienie_2024 PARTITION OF zamowienie
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

#### Optymalizacje fizyczne

| Technika | Zastosowanie |
|----------|--------------|
| **Indeksy** | B-tree, Hash, GIN, GiST |
| **Partycjonowanie** | Range, List, Hash |
| **Denormalizacja** | Materialized views, redundancja |
| **Kompresja** | Kolumnowe storage |
| **Clustering** | Fizyczne uporządkowanie |

---

### 5. Porównanie faz

| Aspekt | Konceptualny | Logiczny | Fizyczny |
|--------|--------------|----------|----------|
| **Odbiorcy** | Biznes | Analitycy, projektanci | DBA, developerzy |
| **Abstrakcja** | Wysoka | Średnia | Niska |
| **DBMS** | Niezależny | Niezależny | Specyficzny |
| **Typy danych** | Brak | Logiczne | Natywne DBMS |
| **Indeksy** | Brak | Brak | Tak |
| **Normalizacja** | Nie | Tak (3NF+) | Może być denorm. |

---

### 6. Transformacje między fazami

```
┌──────────────────────────────────────────────────────────────────┐
│ Konceptualny → Logiczny:                                         │
│ • Encje → Tabele                                                 │
│ • Atrybuty → Kolumny                                             │
│ • Relacje M:N → Tabele asocjacyjne                              │
│ • Generalizacja → Opcje: single table, class table, concrete    │
│ • Normalizacja do 3NF/BCNF                                       │
├──────────────────────────────────────────────────────────────────┤
│ Logiczny → Fizyczny:                                             │
│ • Typy logiczne → Typy DBMS (VARCHAR, INTEGER, TIMESTAMP...)    │
│ • Dodanie indeksów (na FK, WHERE, ORDER BY)                     │
│ • Partycjonowanie dużych tabel                                   │
│ • Kontrolowana denormalizacja (wydajność)                        │
│ • Tablespace, storage parameters                                 │
└──────────────────────────────────────────────────────────────────┘
```

---

### 7. Ewolucja w czasie (produkcja)

```
Wersja 1.0 → 1.1 → 2.0 → ...

Narzędzia migracji:
- Flyway
- Liquibase
- Django migrations
- Alembic (SQLAlchemy)

Zasady:
✓ Backward compatible (add, nie remove)
✓ Expand-Contract pattern
✓ Zero-downtime migrations
✓ Rollback plan
```

---

## 🧠 Mnemoniki

### "C-L-F = Concept, Logic, Physical":
Trzy fazy ewolucji modelu

### "Konceptualny = CO, Logiczny = JAK, Fizyczny = GDZIE":
- CO przechowujemy (biznes)
- JAK strukturyzujemy (normalizacja)
- GDZIE i jak wydajnie (DBMS)

### "3NF w logicznym, denorm w fizycznym":
Normalizuj w logicznym, optymalizuj w fizycznym

---

## ❓ Pytania dodatkowe

### Q1: "Kiedy pominąć fazę konceptualną?"
**Odpowiedź:** Małe projekty, proste dziedziny, doświadczony zespół znający domenę. Ale ryzyko: brak wspólnego zrozumienia z biznesem, pominięte wymagania.

### Q2: "Jak dokumentować model danych?"
**Odpowiedź:** ERD (draw.io, Lucidchart, dbdiagram.io), słownik danych (Data Dictionary), komentarze w DDL, wiki z opisem biznesowym, generowana dokumentacja (SchemaSpy).

### Q3: "Co to jest reverse engineering modelu?"
**Odpowiedź:** Generowanie modelu logicznego/konceptualnego z istniejącej bazy (fizycznej). Narzędzia: ERwin, PowerDesigner, DBeaver. Przydatne dla legacy systems.

---

## 🎯 Kluczowe punkty

1. **Konceptualny:** Biznes, encje, relacje, bez technologii
2. **Logiczny:** Normalizacja, PK/FK, typy logiczne
3. **Fizyczny:** DBMS-specific, indeksy, partycje
4. **Transformacja:** Konceptualny → Logiczny → Fizyczny
5. **Ewolucja:** Migracje, backward compatibility

---

## 📖 Źródła

1. Teorey et al. - "Database Modeling and Design"
2. Silberschatz - "Database System Concepts"
3. Ambler - "Agile Database Techniques"
