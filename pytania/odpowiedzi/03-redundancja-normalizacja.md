# Pytanie 3: Redundancja i normalizacja w relacyjnej bazie danych

## Pytanie
**"Omówić zagadnienia redundancji i normalizacji w relacyjnej bazie danych oraz wynikające z tego wymagania."**

Przedmiot: BD2 (Bazy Danych 2)

---

## 📚 Odpowiedź główna

### Wprowadzenie

**Redundancja** (nadmiarowość) i **normalizacja** to dwa fundamentalne, przeciwstawne pojęcia w projektowaniu relacyjnych baz danych:

- **Redundancja** = niepożądane powtarzanie danych
- **Normalizacja** = proces eliminacji redundancji poprzez dekompozycję relacji

---

## 1. Redundancja danych

### Definicja
**Redundancja** występuje, gdy ta sama informacja jest przechowywana w wielu miejscach bazy danych, co prowadzi do:
- Marnowania pamięci
- Niespójności danych (anomalii)
- Trudności w utrzymaniu

### Anomalie wynikające z redundancji

#### Przykład - tabela z redundancją:

| StudentID | Imię | Nazwisko | KursID | NazwaKursu | Prowadzący |
|-----------|------|----------|--------|------------|------------|
| 1 | Jan | Kowalski | BD1 | Bazy Danych | Dr Nowak |
| 1 | Jan | Kowalski | AISDI | Algorytmy | Prof. Wiśniewski |
| 2 | Anna | Nowak | BD1 | Bazy Danych | Dr Nowak |
| 2 | Anna | Nowak | BD1 | Bazy Danych | Dr Nowak |

**Problemy:**
- "Bazy Danych" i "Dr Nowak" powtórzono 3 razy
- "Jan Kowalski" powtórzono 2 razy

### Trzy typy anomalii

#### 1. Anomalia wstawiania (Insertion Anomaly)
**Problem:** Nie można dodać danych bez dodania innych, niepotrzebnych danych.

**Przykład:** Nie możemy dodać nowego kursu "Sieci komputerowe" bez przypisania do niego studenta.

#### 2. Anomalia usuwania (Deletion Anomaly)
**Problem:** Usunięcie danych powoduje niezamierzoną utratę innych informacji.

**Przykład:** Jeśli Anna Nowak zrezygnuje ze studiów, tracimy informację, że kurs BD1 prowadzi Dr Nowak (jeśli była jedynym studentem tego kursu).

#### 3. Anomalia modyfikacji (Update Anomaly)
**Problem:** Zmiana jednej informacji wymaga modyfikacji wielu wierszy.

**Przykład:** Jeśli Dr Nowak zmieni nazwisko, musimy zaktualizować wszystkie wiersze z kursem BD1.

---

## 2. Normalizacja

### Definicja
**Normalizacja** to proces organizowania danych w bazie w celu:
- Eliminacji redundancji
- Zapewnienia integralności danych
- Ułatwienia utrzymania i modyfikacji

### Podstawowe pojęcia

#### Zależność funkcyjna (Functional Dependency - FD)
**X → Y** oznacza: wartość X jednoznacznie określa wartość Y

**Przykład:** StudentID → (Imię, Nazwisko)
- Znając StudentID, możemy jednoznacznie określić imię i nazwisko

#### Klucz główny (Primary Key)
Minimalny zbiór atrybutów, który jednoznacznie identyfikuje krotkę (wiersz).

#### Klucz kandydujący (Candidate Key)
Każdy minimalny zbiór atrybutów, który mógłby być kluczem głównym.

#### Atrybut pierwszy (Prime Attribute)
Atrybut należący do jakiegokolwiek klucza kandydującego.

#### Atrybut wtórny (Non-prime Attribute)
Atrybut nienależący do żadnego klucza kandydującego.

---

## 3. Postacie normalne

### Hierarchia postaci normalnych

```
5NF ⊂ 4NF ⊂ BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF
```

Każda wyższa postać implikuje niższą.

---

### 1NF - Pierwsza Postać Normalna

#### Wymagania:
1. **Atomowość wartości** - każda komórka zawiera jedną, niepodzielną wartość
2. **Brak powtarzających się grup** - brak tablic/list w komórkach
3. **Istnieje klucz główny**

#### ❌ Naruszenie 1NF:

| StudentID | Imię | Telefony |
|-----------|------|----------|
| 1 | Jan | 123456, 789012 |

#### ✅ Po normalizacji do 1NF:

**Studenci:**
| StudentID | Imię |
|-----------|------|
| 1 | Jan |

**Telefony:**
| StudentID | Telefon |
|-----------|---------|
| 1 | 123456 |
| 1 | 789012 |

---

### 2NF - Druga Postać Normalna

#### Wymagania:
1. Spełnia 1NF
2. **Każdy atrybut wtórny jest w pełni funkcyjnie zależny od całego klucza głównego** (nie od jego części)

Dotyczy tylko tabel z **kluczem złożonym** (wielokolumnowym).

#### ❌ Naruszenie 2NF:

| StudentID | KursID | NazwaKursu | Ocena |
|-----------|--------|------------|-------|
| 1 | BD1 | Bazy Danych | 5 |
| 2 | BD1 | Bazy Danych | 4 |

Klucz: (StudentID, KursID)
- NazwaKursu zależy tylko od KursID, nie od całego klucza!
- KursID → NazwaKursu (częściowa zależność)

#### ✅ Po normalizacji do 2NF:

**Oceny:**
| StudentID | KursID | Ocena |
|-----------|--------|-------|
| 1 | BD1 | 5 |
| 2 | BD1 | 4 |

**Kursy:**
| KursID | NazwaKursu |
|--------|------------|
| BD1 | Bazy Danych |

---

### 3NF - Trzecia Postać Normalna

#### Wymagania:
1. Spełnia 2NF
2. **Brak przechodnich zależności funkcyjnych** - atrybuty wtórne nie zależą od innych atrybutów wtórnych

**Formalnie:** Dla każdej nietrywialnej FD X → A:
- X jest nadkluczem, LUB
- A jest atrybutem pierwszym (należy do klucza)

#### ❌ Naruszenie 3NF:

| StudentID | Imię | WydziałID | NazwaWydziału |
|-----------|------|-----------|---------------|
| 1 | Jan | W4 | Elektroniki |

Klucz: StudentID
- StudentID → WydziałID → NazwaWydziału (przechodnia zależność!)

#### ✅ Po normalizacji do 3NF:

**Studenci:**
| StudentID | Imię | WydziałID |
|-----------|------|-----------|
| 1 | Jan | W4 |

**Wydziały:**
| WydziałID | NazwaWydziału |
|-----------|---------------|
| W4 | Elektroniki |

---

### BCNF - Postać Normalna Boyce'a-Codda

#### Wymagania:
1. Spełnia 3NF
2. **Dla każdej nietrywialnej FD X → Y, X jest nadkluczem**

BCNF jest silniejsza niż 3NF - eliminuje przypadki, gdy atrybut pierwszy zależy od atrybutu niebędącego nadkluczem.

#### ❌ Naruszenie BCNF (ale spełnia 3NF):

| Student | Przedmiot | Prowadzący |
|---------|-----------|------------|
| Jan | Bazy Danych | Dr Nowak |
| Jan | Algorytmy | Dr Nowak |
| Anna | Bazy Danych | Dr Kowalski |

Klucze kandydujące: {Student, Przedmiot}, {Student, Prowadzący}
- Prowadzący → Przedmiot (jeden prowadzący = jeden przedmiot)
- Ale Prowadzący nie jest nadkluczem!

#### ✅ Po normalizacji do BCNF:

**Zapisy:**
| Student | Prowadzący |
|---------|------------|
| Jan | Dr Nowak |
| Anna | Dr Kowalski |

**Prowadzący:**
| Prowadzący | Przedmiot |
|------------|-----------|
| Dr Nowak | Bazy Danych |
| Dr Kowalski | Bazy Danych |

---

### 4NF - Czwarta Postać Normalna

#### Wymagania:
1. Spełnia BCNF
2. **Brak nietrywialnych zależności wielowartościowych** (MVD - Multivalued Dependencies)

**Zależność wielowartościowa X ↠ Y:** Dla danego X istnieje zbiór wartości Y niezależny od innych atrybutów.

#### ❌ Naruszenie 4NF:

| Pracownik | Umiejętność | Język |
|-----------|-------------|-------|
| Jan | Java | Angielski |
| Jan | Java | Niemiecki |
| Jan | Python | Angielski |
| Jan | Python | Niemiecki |

Pracownik ↠ Umiejętność i Pracownik ↠ Język (niezależne!)

#### ✅ Po normalizacji do 4NF:

**PracownikUmiejętności:**
| Pracownik | Umiejętność |
|-----------|-------------|
| Jan | Java |
| Jan | Python |

**PracownikJęzyki:**
| Pracownik | Język |
|-----------|-------|
| Jan | Angielski |
| Jan | Niemiecki |

---

### 5NF - Piąta Postać Normalna (PJNF)

#### Wymagania:
1. Spełnia 4NF
2. **Brak zależności połączeniowych** (Join Dependencies)
3. Dekompozycja bez strat tylko na podstawie kluczy kandydujących

5NF eliminuje redundancję wynikającą z niemożliwości odtworzenia oryginalnej relacji przez złączenie jej projekcji.

---

## 📊 Tabela porównawcza postaci normalnych

| Postać | Eliminuje | Wymaga |
|--------|-----------|--------|
| **1NF** | Wielowartościowe atrybuty | Atomowość, klucz główny |
| **2NF** | Częściowe zależności | Pełna zależność od klucza |
| **3NF** | Przechodnie zależności | Brak X → A gdzie X nie jest nadkluczem i A nie jest pierwszym |
| **BCNF** | Zależności od nie-nadkluczy | Każdy determinant jest nadkluczem |
| **4NF** | Wielowartościowe zależności | Brak nietrywialnych MVD |
| **5NF** | Zależności połączeniowe | Dekompozycja tylko przez klucze |

---

## 4. Proces normalizacji

### Algorytm dekompozycji do 3NF

1. **Znajdź pokrycie kanoniczne** zbioru zależności funkcyjnych
2. **Dla każdej FD X → A** utwórz relację R(X, A)
3. **Jeśli żadna relacja nie zawiera klucza kandydującego**, dodaj relację z atrybutami klucza
4. **Usuń relacje zawarte w innych relacjach**

### Własności dobrej dekompozycji

#### 1. Bezstratność (Lossless Join)
Po dekompozycji można odtworzyć oryginalną relację przez złączenie naturalne.

**Twierdzenie:** Dekompozycja R na R₁ i R₂ jest bezstratna wtw gdy:
- R₁ ∩ R₂ → R₁, lub
- R₁ ∩ R₂ → R₂

#### 2. Zachowanie zależności (Dependency Preservation)
Wszystkie oryginalne FD można zweryfikować w pojedynczych tabelach wynikowych (bez złączeń).

---

## 5. Denormalizacja

### Kiedy stosować?
- **Optymalizacja wydajności** - złączenia są kosztowne
- **Systemy OLAP/hurtownie danych** - dane głównie odczytywane
- **Raportowanie** - predefiniowane zapytania

### Techniki denormalizacji:
1. **Dodanie redundantnych kolumn** - unikanie złączeń
2. **Tabele podsumowujące** - agregaty
3. **Tabele historyczne** - snapshoty
4. **Materializowane widoki** - cache wyników

### Kompromis:
```
NORMALIZACJA ←————————————→ DENORMALIZACJA
Integralność                 Wydajność odczytu
Mniej redundancji           Więcej redundancji
Wolniejsze odczyty          Szybsze odczyty
Szybsze zapisy              Wolniejsze zapisy
```

---

## 🧠 Mnemoniki

### "1-2-3-BC" dla postaci normalnych:
- **1**NF = **1** wartość w komórce (atomowość)
- **2**NF = **2** słowa: "pełna zależność" (od całego klucza)
- **3**NF = **3** słowa: "brak przechodniości" (A→B→C eliminowane)
- **BC**NF = **B**ardzo **C**isty (każdy determinant = nadklucz)

### "AIU" dla anomalii:
- **A**nomalia wstawiania (**A**dding) - nie można dodać
- **I**nsercja usuwania (**I**nterrupts) - traci dane przy DELETE
- **U**pdate modyfikacji - trzeba zmieniać wiele wierszy

### "KAP" dla kluczy:
- **K**lucz główny - wybrany unikalny identyfikator
- **A**lternatywny (kandydujący) - mógłby być głównym
- **P**ierwszy atrybut - należy do jakiegoś klucza

### Wzór na 3NF:
> "Każdy atrybut zależy od **klucza**, **całego klucza** i **tylko od klucza**."
> (The key, the whole key, and nothing but the key - so help me Codd!)

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Podaj przykład dekompozycji do 3NF z zachowaniem bezstratności"

**Odpowiedź:**

**Relacja:** R(A, B, C, D)
**FD:** A → B, B → C, C → D

**Klucz:** A

**Dekompozycja:**
1. R₁(A, B) - z FD A → B
2. R₂(B, C) - z FD B → C
3. R₃(C, D) - z FD C → D

**Sprawdzenie bezstratności:**
- R₁ ∩ R₂ = {B}, B → C (B jest kluczem R₂) ✓
- R₂ ∩ R₃ = {C}, C → D (C jest kluczem R₃) ✓

---

### Q2: "Czym się różni 3NF od BCNF?"

**Odpowiedź:**

| Cecha | 3NF | BCNF |
|-------|-----|------|
| **Warunek** | X nadklucz LUB A pierwszy | X zawsze nadklucz |
| **Siła** | Słabsza | Silniejsza |
| **Dekompozycja** | Zachowuje zależności | Może nie zachować |
| **Redundancja** | Możliwa minimalna | Brak |

**Przykład różnicy:**

R(Student, Przedmiot, Prowadzący)
- Klucze: {Student, Przedmiot}, {Student, Prowadzący}
- FD: Prowadzący → Przedmiot

**3NF:** ✅ spełniona (Przedmiot jest atrybutem pierwszym)
**BCNF:** ❌ naruszona (Prowadzący nie jest nadkluczem)

---

### Q3: "Jak sprawdzić, czy relacja jest w 3NF?"

**Odpowiedź:**

**Algorytm:**
1. Znajdź wszystkie nietrywialne FD
2. Dla każdej FD X → A sprawdź:
   - Czy X jest nadkluczem? → OK
   - Czy A jest atrybutem pierwszym? → OK
   - Jeśli żadne → NIE jest w 3NF

**Przykład:**
R(A, B, C), FD: {A → B, B → C}

Klucz: A
- A → B: A jest nadkluczem ✓
- B → C: B nie jest nadkluczem, C nie jest pierwszy ✗

**Wniosek:** R NIE jest w 3NF

---

### Q4: "Kiedy normalizacja może zaszkodzić?"

**Odpowiedź:**

1. **Systemy OLAP/raportowe:**
   - Złączenia wielu tabel są kosztowne
   - Dane głównie odczytywane, rzadko modyfikowane
   - Lepiej: denormalizacja, schematy gwiazdy/płatka śniegu

2. **Aplikacje o wysokiej wydajności:**
   - Każde złączenie to koszt
   - Cache'owanie i replikacja danych może być szybsze

3. **Systemy czasu rzeczywistego:**
   - Determinizm ważniejszy niż oszczędność miejsca
   - Redundancja może przyspieszyć dostęp

**Zasada:** Normalizuj dla OLTP, denormalizuj dla OLAP

---

### Q5: "Co to jest zależność wielowartościowa (MVD)?"

**Odpowiedź:**

**Zależność wielowartościowa X ↠ Y:**
Dla każdej wartości X istnieje zbiór wartości Y, który jest niezależny od innych atrybutów relacji.

**Formalnie:** X ↠ Y w R(X, Y, Z) gdy:
Dla każdych dwóch krotek t₁, t₂ takich że t₁[X] = t₂[X]:
istnieje krotka t₃ gdzie:
- t₃[X] = t₁[X] = t₂[X]
- t₃[Y] = t₁[Y]
- t₃[Z] = t₂[Z]

**Intuicja:** Y i Z są "niezależne" przy danym X.

**Przykład:**
Pracownik ↠ Umiejętność (niezależne od języka)
Pracownik ↠ Język (niezależne od umiejętności)

---

### Q6: "Wyjaśnij pojęcie pokrycia kanonicznego"

**Odpowiedź:**

**Pokrycie kanoniczne** to minimalny zbiór FD równoważny oryginalnemu.

**Właściwości:**
1. Prawa strona każdej FD ma jeden atrybut
2. Lewa strona jest minimalna (brak nadmiarowych atrybutów)
3. Brak redundantnych FD

**Algorytm:**
1. Rozłóż prawe strony: A → BC na A → B, A → C
2. Usuń nadmiarowe atrybuty z lewych stron
3. Usuń redundantne FD (te wynikające z innych)

**Przykład:**
F = {A → BC, B → C, A → B, AB → C}

Pokrycie kanoniczne:
Fc = {A → B, B → C}

---

## 🎯 Kluczowe punkty do zapamiętania

1. **Redundancja** = powtarzanie danych → anomalie AIU
2. **Normalizacja** = dekompozycja eliminująca redundancję
3. **3NF** = standard praktyczny (zachowuje zależności)
4. **BCNF** = silniejsza, ale może gubić zależności
5. **Wzór 3NF:** "klucz, cały klucz, tylko klucz"
6. **Kompromis:** normalizacja vs wydajność

---

## 📖 Źródła do pogłębienia

1. Date, C.J. - "An Introduction to Database Systems"
2. Elmasri, Navathe - "Fundamentals of Database Systems"
3. Codd, E.F. - "A Relational Model of Data for Large Shared Data Banks" (1970)
4. Garcia-Molina, Ullman, Widom - "Database Systems: The Complete Book"
