# Pytanie 27: Jakość modelu danych w projekcie informatycznym

## Pytanie
**"Dlaczego jakość modelu danych jest krytycznie ważnym czynnikiem jakości projektu informatycznego?"**

Przedmiot: MODA (Modelowanie Danych)

---

## 📚 Odpowiedź główna

### 1. Model danych jako fundament systemu

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITEKTURA SYSTEMU                         │
│                                                                 │
│    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐        │
│    │     UI      │   │   Logika    │   │  Integracje │        │
│    │             │   │  biznesowa  │   │             │        │
│    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘        │
│           │                 │                 │                │
│           └────────────┬────┴────────────────┘                │
│                        │                                       │
│                        ↓                                       │
│           ╔════════════════════════════════╗                  │
│           ║       MODEL DANYCH             ║ ← FUNDAMENT      │
│           ║   (schemat bazy, encje,        ║                  │
│           ║    relacje, ograniczenia)      ║                  │
│           ╚════════════════════════════════╝                  │
│                                                                │
│   Zmiana modelu danych → kaskadowe zmiany w całym systemie!   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Konsekwencje złego modelu danych

| Problem | Konsekwencje |
|---------|--------------|
| **Redundancja** | Anomalie (insert, update, delete), niespójność |
| **Brak normalizacji** | Duplikacja, trudna aktualizacja |
| **Nadmierna normalizacja** | Wolne zapytania (wiele JOIN) |
| **Złe typy danych** | Błędy konwersji, utrata precyzji |
| **Brak ograniczeń** | Nieprawidłowe dane w bazie |
| **Słaba dokumentacja** | Niezrozumiały schemat |

### Przykład: Anomalie przy braku normalizacji

```
Tabela nienormalizowana (zamówienia):
┌────────┬─────────┬─────────────┬───────────┬─────────┐
│OrderID │Customer │CustomerAddr │ Product   │ Price   │
├────────┼─────────┼─────────────┼───────────┼─────────┤
│ 1      │ Jan     │ Warszawa    │ Laptop    │ 3000    │
│ 2      │ Jan     │ Warszawa    │ Mysz      │ 50      │
│ 3      │ Anna    │ Kraków      │ Laptop    │ 3000    │
└────────┴─────────┴─────────────┴───────────┴─────────┘

Problemy:
❌ UPDATE: Jan zmienia adres → aktualizuj wiele wierszy
❌ DELETE: Usunięcie zamówienia 3 → tracimy info o Annie
❌ INSERT: Nowy klient bez zamówienia → nie można dodać
```

---

### 3. Wpływ na różne aspekty projektu

#### Wydajność

```
Zły model:
SELECT * FROM orders 
JOIN customers ON orders.customer_name = customers.name  -- string comparison!
JOIN products ON orders.product_name = products.name
WHERE customers.city = 'Warszawa';
→ Full table scans, wolne JOIN na stringach

Dobry model:
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id  -- integer FK
JOIN products p ON o.product_id = p.id
WHERE c.city_id = 1;  -- indexed lookup
→ Index scans, szybkie JOIN na integer PK/FK
```

#### Skalowalność

| Model | Skalowalność |
|-------|--------------|
| **Denormalizowany (złe)** | Ogromne tabele, trudne sharding |
| **Nadmiernie znormalizowany** | Wiele JOIN, complex queries |
| **Zbalansowany** | Optymalne partycjonowanie, cache-friendly |

#### Utrzymywalność

```
Zły model:
- Pole "data" typu VARCHAR przechowuje JSON, XML, CSV...
- Brak dokumentacji co oznaczają kody (status=1,2,3?)
- Nazwy kolumn: col1, col2, temp_field, test123

Dobry model:
- Dedykowane tabele i kolumny z opisowymi nazwami
- ENUM lub tabela słownikowa dla statusów
- Komentarze w schemacie, dokumentacja ERD
```

---

### 4. Koszty naprawy złego modelu

```
Koszt zmiany modelu danych w czasie:

Koszt
  ↑
  │                                    ████
  │                              ████████████
  │                        ████████████████████
  │                  ████████████████████████████
  │            ████████████████████████████████████
  │      ████████████████████████████████████████████
  │████████████████████████████████████████████████████
  └────────────────────────────────────────────────────→ Czas
   Projekt  Dev   Test   Prod   2 lata  5 lat
   
Migracja w produkcji: downtime, ryzyko utraty danych,
koordynacja z aplikacjami, rollback plan
```

**Reguła 1:10:100:**
- Naprawa w fazie projektowania: 1x
- Naprawa w fazie developmentu: 10x
- Naprawa w produkcji: 100x

---

### 5. Cechy dobrego modelu danych

| Cecha | Opis |
|-------|------|
| **Poprawność** | Odzwierciedla dziedzinę biznesową |
| **Kompletność** | Wszystkie wymagane dane |
| **Spójność** | Brak sprzeczności, integralność |
| **Minimalizm** | Brak zbędnej redundancji |
| **Elastyczność** | Możliwość rozszerzenia |
| **Wydajność** | Odpowiednia denormalizacja gdzie potrzeba |
| **Dokumentacja** | ERD, słownik danych |

---

### 6. Wpływ na jakość danych (GIGO)

```
Garbage In, Garbage Out:

┌──────────────────┐
│ Złe dane wejść.  │ → Zły model → Złe decyzje biznesowe
│ (brak walidacji) │
└──────────────────┘

Dobry model wymusza jakość:
- NOT NULL gdzie wymagane
- CHECK constraints (age > 0)
- FOREIGN KEY (referential integrity)
- UNIQUE (brak duplikatów)
- Trigger dla złożonej walidacji
```

---

### 7. Model danych a architektura aplikacji

```
┌─────────────────────────────────────────────────────────────────┐
│ Model danych wpływa na:                                         │
│                                                                 │
│ • ORM mapping (Entity classes)                                 │
│ • API endpoints (REST resources)                               │
│ • UI forms (pola formularzy)                                   │
│ • Validation rules                                             │
│ • Business logic                                               │
│ • Reports & Analytics                                          │
│ • Data warehouse schema                                        │
│ • Integration contracts                                        │
│                                                                 │
│ Zmiana w modelu → propagacja do WSZYSTKICH warstw!             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mnemoniki

### "Model = Fundament domu":
Zły fundament → dom się zawali (kosztowna przebudowa)

### "GIGO = Garbage In, Garbage Out":
Zły model → złe dane → złe decyzje

### "1:10:100 = Koszt naprawy rośnie":
Im później naprawa, tym drożej

---

## ❓ Pytania dodatkowe

### Q1: "Jak mierzyć jakość modelu danych?"
**Odpowiedź:** Metryki: liczba anomalii, poziom normalizacji, pokrycie constraints, liczba orphan records, czas wykonania typowych zapytań, coupling między tabelami, dokumentacja coverage.

### Q2: "Kiedy denormalizacja jest uzasadniona?"
**Odpowiedź:** Read-heavy systemy (raportowanie), krytyczne zapytania wymagające wielu JOIN, cache/materialized views, data warehouse (star schema), gdy koszt UPDATE < koszt JOIN.

### Q3: "Jak ewoluować model w produkcji?"
**Odpowiedź:** Migracje (Flyway, Liquibase), blue-green deployment, feature flags, backward compatible changes (add column, nie remove), expand-contract pattern.

---

## 🎯 Kluczowe punkty

1. **Fundament:** Model danych = podstawa całego systemu
2. **Kaskada:** Zmiana modelu → zmiany wszędzie
3. **Koszt:** 1:10:100 - wczesne poprawki tańsze
4. **Jakość:** Constraints wymuszają poprawność danych
5. **Dokumentacja:** ERD, słownik danych niezbędne

---

## 📖 Źródła

1. Date - "An Introduction to Database Systems"
2. Fowler - "Patterns of Enterprise Application Architecture"
3. Ambler - "Agile Database Techniques"
