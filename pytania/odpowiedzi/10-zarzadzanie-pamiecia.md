# Pytanie 10: Zarządzanie pamięcią - stronicowanie i segmentacja

## Pytanie
**"Scharakteryzować problemy i mechanizmy zarządzania pamięcią. Porównać cechy i przeznaczenie mechanizmów stronicowania i segmentacji."**

Przedmiot: SOI (Systemy Operacyjne)

---

## 📚 Odpowiedź główna

### Wprowadzenie

**Zarządzanie pamięcią** to jeden z kluczowych zadań systemu operacyjnego:
- Przydzielanie pamięci procesom
- Ochrona pamięci między procesami
- Efektywne wykorzystanie ograniczonego zasobu
- Abstrakcja (programista nie musi znać fizycznych adresów)

---

## 1. Problemy zarządzania pamięcią

### 1.1 Fragmentacja

#### Fragmentacja zewnętrzna (External Fragmentation)

```
┌─────────────────────────────────────────────────────────────────┐
│ Pamięć fizyczna:                                                │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐              │
│ │PROC│ │FREE│ │PROC│ │FREE│ │PROC│ │FREE│ │PROC│              │
│ │ A  │ │ 2K │ │ B  │ │ 3K │ │ C  │ │ 1K │ │ D  │              │
│ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘              │
│                                                                 │
│ Suma wolnej pamięci: 6K                                         │
│ Ale nie można przydzielić bloku 5K! (fragmentacja)              │
└─────────────────────────────────────────────────────────────────┘
```

**Problem:** Wolna pamięć jest rozproszona w małych, nieciągłych blokach.

#### Fragmentacja wewnętrzna (Internal Fragmentation)

```
┌─────────────────────────────────────────────────────────────────┐
│ Przydzielono blok 4KB, proces potrzebuje 3.5KB:                 │
│ ┌────────────────────────────────────────┐                      │
│ │ WYKORZYSTANE (3.5KB) │ ZMARNOWANE (0.5KB) │                   │
│ └────────────────────────────────────────┘                      │
│                          ↑                                       │
│              Fragmentacja wewnętrzna                             │
└─────────────────────────────────────────────────────────────────┘
```

**Problem:** Przydzielony blok jest większy niż potrzeba.

### 1.2 Ochrona pamięci

- Proces A nie może czytać/pisać pamięci procesu B
- Jądro chronione przed aplikacjami użytkownika
- Mechanizmy: rejestry bazowy/graniczny, bity ochrony, ringi

### 1.3 Relokacja

**Problem:** Program kompilowany z założeniem konkretnych adresów musi działać pod różnymi adresami.

**Rozwiązania:**
- Relokacja statyczna (loader)
- Relokacja dynamiczna (MMU - Memory Management Unit)

### 1.4 Współdzielenie

- Biblioteki współdzielone (DLL, .so)
- Pamięć współdzielona między procesami
- Copy-on-Write (COW)

### 1.5 Ograniczona pamięć fizyczna

- Więcej procesów niż RAM
- Rozwiązanie: pamięć wirtualna + swap

---

## 2. Mechanizmy zarządzania pamięcią

### 2.1 Partycjonowanie stałe (Fixed Partitioning)

```
┌────────────────────────────────────────────────────────────────┐
│ Pamięć podzielona na stałe partycje:                           │
│ ┌──────────┬──────────┬──────────┬──────────┐                  │
│ │ Partycja │ Partycja │ Partycja │ Partycja │                  │
│ │   1MB    │   2MB    │   4MB    │   8MB    │                  │
│ └──────────┴──────────┴──────────┴──────────┘                  │
│                                                                 │
│ Zalety: Proste, brak fragmentacji zewnętrznej                  │
│ Wady: Fragmentacja wewnętrzna, maks. rozmiar procesu ograniczony│
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Partycjonowanie dynamiczne (Dynamic Partitioning)

```
┌────────────────────────────────────────────────────────────────┐
│ Partycje tworzone według potrzeb:                              │
│ ┌─────┬───────────┬────────┬─────────────────────────────┐     │
│ │ P1  │    P2     │   P3   │         WOLNA               │     │
│ │ 3MB │    5MB    │  2MB   │          10MB               │     │
│ └─────┴───────────┴────────┴─────────────────────────────┘     │
│                                                                 │
│ Zalety: Brak fragmentacji wewnętrznej, elastyczność            │
│ Wady: Fragmentacja zewnętrzna!                                 │
└────────────────────────────────────────────────────────────────┘
```

**Algorytmy przydziału:**

| Algorytm | Opis | Zalety | Wady |
|----------|------|--------|------|
| **First Fit** | Pierwszy wystarczający blok | Szybki | Fragmentacja na początku |
| **Best Fit** | Najmniejszy wystarczający | Oszczędza duże bloki | Wiele małych fragmentów |
| **Worst Fit** | Największy blok | Pozostawia użyteczne resztki | Niszczy duże bloki |
| **Next Fit** | First Fit od ostatniego miejsca | Rozproszenie | Fragmentacja |

---

## 3. Stronicowanie (Paging)

### Idea

Dzielimy pamięć na **równe bloki** (strony/ramki):
- **Strona (Page)** - blok pamięci wirtualnej (4KB typowo)
- **Ramka (Frame)** - blok pamięci fizycznej (ten sam rozmiar)

```
┌─────────────────────────────────────────────────────────────────┐
│  PAMIĘĆ WIRTUALNA                    PAMIĘĆ FIZYCZNA           │
│  (przestrzeń adresowa)               (RAM)                      │
│                                                                 │
│  ┌─────────┐                         ┌─────────┐               │
│  │ Strona 0│─────────────────────────│ Ramka 5 │               │
│  ├─────────┤                         ├─────────┤               │
│  │ Strona 1│──────────┐              │ Ramka 1 │               │
│  ├─────────┤          │              ├─────────┤               │
│  │ Strona 2│────┐     │              │ Ramka 2 │←──────────┐   │
│  ├─────────┤    │     │              ├─────────┤           │   │
│  │ Strona 3│    │     └─────────────→│ Ramka 3 │           │   │
│  └─────────┘    │                    ├─────────┤           │   │
│                 │                    │ Ramka 4 │           │   │
│                 │                    ├─────────┤           │   │
│                 └───────────────────→│ Ramka 7 │           │   │
│                                      └─────────┘           │   │
│                                                            │   │
│  TABLICA STRON (Page Table)          Strona 2 → Ramka 7────┘   │
│  ┌──────────────────────┐                                      │
│  │ Strona │ Ramka │Flagi│                                      │
│  │   0    │   5   │ RW  │                                      │
│  │   1    │   3   │ R   │                                      │
│  │   2    │   7   │ RW  │                                      │
│  │   3    │   -   │ INV │ ← Strona nie w pamięci (page fault)  │
│  └──────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Translacja adresu

```
Adres wirtualny (32-bit, strony 4KB):
┌────────────────────────┬──────────────┐
│   Numer strony (20b)   │ Offset (12b) │
└────────────────────────┴──────────────┘
         │                      │
         ↓                      │
    Tablica stron               │
         │                      │
         ↓                      │
┌────────────────────────┬──────────────┐
│   Numer ramki (20b)    │ Offset (12b) │
└────────────────────────┴──────────────┘
         Adres fizyczny
```

### Wielopoziomowe tablice stron

**Problem:** Tablica stron dla 32-bit przestrzeni z 4KB stronami = 2²⁰ wpisów × 4B = **4MB per proces!**

**Rozwiązanie:** Hierarchiczna tablica stron

```
Adres wirtualny (32-bit, 2 poziomy):
┌────────────┬────────────┬──────────────┐
│ Katalog(10)│ Tabela(10) │ Offset (12)  │
└────────────┴────────────┴──────────────┘
      │             │             │
      ↓             ↓             │
┌──────────┐  ┌──────────┐        │
│ Page     │  │ Page     │        │
│Directory │→ │ Table    │→ Ramka + Offset
└──────────┘  └──────────┘
```

**64-bit (x86-64):** 4 poziomy (PML4 → PDPT → PD → PT)

### TLB (Translation Lookaside Buffer)

**Problem:** Każdy dostęp do pamięci wymaga 2+ odczytów (tablica + dane).

**Rozwiązanie:** Cache translacji adresów

```
┌─────────────────────────────────────────────────────────────────┐
│                          TLB                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Strona wirtualna │ Ramka fizyczna │ Flagi │ ASID          │  │
│  │     0x12345      │     0x789AB    │  RW   │  42           │  │
│  │     0x12346      │     0x789AC    │  R    │  42           │  │
│  │       ...        │       ...      │  ...  │ ...           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  TLB hit:  ~1 cykl                                              │
│  TLB miss: ~100+ cykli (page walk)                              │
│  Hit rate: >99% typowo                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Zalety i wady stronicowania

| Zalety | Wady |
|--------|------|
| Brak fragmentacji zewnętrznej | Fragmentacja wewnętrzna (ostatnia strona) |
| Prosta alokacja (bitmapa ramek) | Narzut tablicy stron |
| Łatwe współdzielenie (COW) | TLB miss kosztowny |
| Pamięć wirtualna naturalna | Nie odpowiada strukturze programu |

---

## 4. Segmentacja (Segmentation)

### Idea

Dzielimy pamięć na **logiczne segmenty** odpowiadające strukturze programu:
- Segment kodu
- Segment danych
- Segment stosu
- Segment bibliotek

```
┌─────────────────────────────────────────────────────────────────┐
│  PRZESTRZEŃ LOGICZNA                 PAMIĘĆ FIZYCZNA           │
│                                                                 │
│  ┌─────────────────┐                 ┌─────────────────────┐   │
│  │  Segment 0      │                 │                     │   │
│  │  (Kod)          │─────────────────│→ 0x1000 - 0x3FFF    │   │
│  │  Rozmiar: 12KB  │                 │                     │   │
│  └─────────────────┘                 ├─────────────────────┤   │
│  ┌─────────────────┐                 │                     │   │
│  │  Segment 1      │─────────────────│→ 0x8000 - 0xBFFF    │   │
│  │  (Dane)         │                 │                     │   │
│  │  Rozmiar: 16KB  │                 ├─────────────────────┤   │
│  └─────────────────┘                 │                     │   │
│  ┌─────────────────┐                 │                     │   │
│  │  Segment 2      │─────────────────│→ 0xF000 - 0xF7FF    │   │
│  │  (Stos)         │                 │                     │   │
│  │  Rozmiar: 2KB   │                 └─────────────────────┘   │
│  └─────────────────┘                                           │
│                                                                 │
│  TABLICA SEGMENTÓW                                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Segment │  Baza   │ Limit  │ Prawa │                      │ │
│  │    0    │ 0x1000  │ 12KB   │  RX   │ (kod - execute)      │ │
│  │    1    │ 0x8000  │ 16KB   │  RW   │ (dane - read/write)  │ │
│  │    2    │ 0xF000  │  2KB   │  RW   │ (stos)               │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Translacja adresu

```
Adres logiczny:
┌────────────────────┬──────────────────────┐
│ Numer segmentu (s) │    Offset (d)        │
└────────────────────┴──────────────────────┘
         │                     │
         ↓                     │
    Tablica segmentów          │
    ┌──────┬───────┐           │
    │ Baza │ Limit │           │
    └──────┴───────┘           │
         │         │           │
         │   Sprawdź: d < Limit?
         │         │           │
         ↓         ↓           │
    Adres fizyczny = Baza + Offset
```

### Ochrona w segmentacji

Każdy segment ma **prawa dostępu:**
- **R** (Read) - odczyt dozwolony
- **W** (Write) - zapis dozwolony
- **X** (Execute) - wykonanie dozwolone

```
Segment kodu:    RX  (wykonaj, nie modyfikuj)
Segment danych:  RW  (czytaj/pisz, nie wykonuj)
Segment stosu:   RW  (bez wykonywania - ochrona przed exploitami)
```

### Zalety i wady segmentacji

| Zalety | Wady |
|--------|------|
| Odpowiada strukturze programu | Fragmentacja zewnętrzna |
| Naturalna ochrona (per segment) | Segmenty o zmiennej wielkości |
| Łatwe współdzielenie (cały segment) | Kompaktowanie potrzebne |
| Dynamiczny wzrost segmentów | Skomplikowana alokacja |

---

## 5. Porównanie: Stronicowanie vs Segmentacja

| Cecha | Stronicowanie | Segmentacja |
|-------|---------------|-------------|
| **Jednostka** | Strona (stały rozmiar) | Segment (zmienny rozmiar) |
| **Widoczność dla programisty** | Niewidoczna | Widoczna (logiczne jednostki) |
| **Fragmentacja zewnętrzna** | ❌ Brak | ✅ Występuje |
| **Fragmentacja wewnętrzna** | ✅ Występuje | ❌ Brak |
| **Tablica** | Tablica stron (duża) | Tablica segmentów (mała) |
| **Ochrona** | Per strona (mniej naturalna) | Per segment (naturalna) |
| **Współdzielenie** | Per strona | Per segment (całe moduły) |
| **Pamięć wirtualna** | Łatwa (strony na dysk) | Trudniejsza |

---

## 6. Segmentacja ze stronicowaniem (Hybrid)

### Intel x86 (tryb chroniony)

Kombinacja obu mechanizmów:

```
Adres logiczny (Selector:Offset)
         │
         ↓
    SEGMENTACJA
    (Segment → Adres liniowy)
         │
         ↓
    Adres liniowy
         │
         ↓
    STRONICOWANIE
    (Strona → Ramka)
         │
         ↓
    Adres fizyczny
```

**Praktyka:** Współczesne OS (Linux, Windows) używają **flat memory model** - wszystkie segmenty pokrywają całą przestrzeń adresową, efektywnie wyłączając segmentację.

### Zalety hybrydowego podejścia

1. **Ochrona** z segmentacji (kod vs dane vs stos)
2. **Brak fragmentacji zewnętrznej** ze stronicowania
3. **Pamięć wirtualna** ze stronicowania

---

## 7. Pamięć wirtualna (Virtual Memory)

### Idea

Nie wszystkie strony muszą być w RAM - część może być na dysku (swap).

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  PAMIĘĆ WIRTUALNA          RAM              DYSK (Swap)        │
│  ┌─────────────┐      ┌──────────┐       ┌──────────────┐      │
│  │   Strona 0  │ ────→│ Ramka 2  │       │              │      │
│  │   Strona 1  │      │          │       │   Strona 3   │      │
│  │   Strona 2  │ ────→│ Ramka 5  │       │   Strona 5   │      │
│  │   Strona 3  │ ─────────────────────→  │              │      │
│  │   Strona 4  │ ────→│ Ramka 1  │       │              │      │
│  │   Strona 5  │ ─────────────────────→  │              │      │
│  └─────────────┘      └──────────┘       └──────────────┘      │
│                                                                 │
│  Page fault: Strona 3 → załaduj z dysku do RAM                 │
└─────────────────────────────────────────────────────────────────┘
```

### Algorytmy zastępowania stron

| Algorytm | Opis | Właściwości |
|----------|------|-------------|
| **FIFO** | Najstarsza strona | Prosty, anomalia Bélády'ego |
| **LRU** | Najdawniej używana | Optymalny offline, kosztowny |
| **LRU Approximation** | Clock, Second Chance | Praktyczny kompromis |
| **LFU** | Najrzadziej używana | Dobre dla hot data |
| **OPT** | Najdalej używana | Teoretycznie optymalny, niemożliwy |

### Algorytm Clock (Second Chance)

```
       ┌───┐
   ┌──→│ 1 │──┐       Bit referencji:
   │   └───┘  │       1 = używana ostatnio
   │          ↓       0 = kandydat do usunięcia
┌───┐      ┌───┐
│ 0 │      │ 1 │      Wskazówka zegara:
└───┘      └───┘      - Jeśli bit=1: zeruj, idź dalej
   ↑          │       - Jeśli bit=0: zastąp tę stronę
   │   ┌───┐  │
   └───│ 0 │←─┘
       └───┘
         ↑
      wskazówka
```

---

## 🧠 Mnemoniki

### "STRONY RÓWNE, SEGMENTY LOGICZNE":
- **Strony** = wszystkie takie same (4KB)
- **Segmenty** = różne rozmiary, logiczny podział

### "PAGE = Physical Allocation Generates Equality":
- Fizyczne ramki równej wielkości
- Brak fragmentacji zewnętrznej

### "SEGMENT = Software Entity with Guarded Memory, ENforcing Type safety":
- Logiczne jednostki programu
- Ochrona per segment

### "TLB = Translation Lightning-fast Buffer":
- Cache dla translacji adresów
- Hit = 1 cykl, Miss = 100+ cykli

### "LRU = Last Recently Used → pierwszy do usunięcia":
- Najdawniej używana = najlepsza do wyrzucenia

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Co to jest Page Fault i jak jest obsługiwany?"

**Odpowiedź:**

**Page Fault** = wyjątek gdy strona nie jest w RAM (bit valid=0 w tablicy stron).

```
1. Proces odwołuje się do adresu w stronie 5
2. MMU sprawdza tablicę stron: strona 5 invalid
3. Page Fault exception
4. OS:
   a) Znajdź stronę na dysku (swap)
   b) Znajdź wolną ramkę (lub zwolnij przez algorytm zastępowania)
   c) Załaduj stronę z dysku do RAM
   d) Zaktualizuj tablicę stron (valid=1, ramka=X)
   e) Wznów instrukcję
5. Proces kontynuuje (nie wie, że był page fault)
```

---

### Q2: "Wyjaśnij anomalię Bélády'ego"

**Odpowiedź:**

**Anomalia Bélády'ego** = więcej ramek → więcej page faults (dla FIFO)!

```
Sekwencja odwołań: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5

3 ramki (FIFO): 9 page faults
4 ramki (FIFO): 10 page faults (!!)

Wniosek: FIFO nie jest "stack algorithm" - nie ma tej właściwości:
"Strony w pamięci z N ramkami ⊆ strony z N+1 ramkami"

LRU nie ma tej anomalii (jest stack algorithm).
```

---

### Q3: "Co to jest thrashing?"

**Odpowiedź:**

**Thrashing** = system spędza więcej czasu na page faults niż na wykonywaniu kodu.

```
Przyczyna: Zbyt mało RAM dla working set procesów

Working set = zbiór stron aktywnie używanych przez proces

Symptomy:
- CPU utilization spada
- Dysk ciągle pracuje (swap in/out)
- System "zamiera"

Rozwiązania:
- Zwiększ RAM
- Zmniejsz multiprogramming
- Working set model (przydziel RAM proporcjonalnie)
- Swap na SSD
```

---

### Q4: "Jak działa Copy-on-Write?"

**Odpowiedź:**

**COW** = odroczenie kopiowania do momentu modyfikacji.

```
fork() bez COW:
Rodzic: [Strona A] [Strona B] [Strona C]
                ↓ kopiowanie
Dziecko: [Strona A'] [Strona B'] [Strona C']
→ Kosztowne!

fork() z COW:
Rodzic:  [Strona A (RO)] [Strona B (RO)] [Strona C (RO)]
              ↓ shared     ↓ shared       ↓ shared
Dziecko: [Strona A (RO)] [Strona B (RO)] [Strona C (RO)]
→ Szybkie! (tylko tablice stron)

Dziecko pisze do Strony B:
1. Page fault (strona RO)
2. OS kopiuje Stronę B → B'
3. Dziecko dostaje B' (RW), rodzic zachowuje B (RW)
```

---

### Q5: "Jaki jest typowy rozmiar strony i dlaczego?"

**Odpowiedź:**

| Rozmiar | Zalety | Wady |
|---------|--------|------|
| **Mały (1KB)** | Mała fragmentacja wewnętrzna | Duża tablica stron |
| **Duży (64KB)** | Mała tablica stron | Duża fragmentacja wewnętrzna |
| **4KB (typowy)** | Kompromis | Kompromis |

**Dlaczego 4KB?**
- Rozmiar bloku dysku (sektor 512B × 8 lub 4K native)
- Rozsądna fragmentacja (~2KB średnio)
- Rozsądna tablica stron
- Historyczne (VAX, Unix)

**Huge Pages (2MB, 1GB):**
- Dla dużych aplikacji (bazy danych)
- Mniej wpisów TLB
- Mniej page faults

---

### Q6: "Jak segmentacja jest używana w x86-64?"

**Odpowiedź:**

**x86-64 praktycznie nie używa segmentacji:**

```
CS, DS, ES, SS → Baza = 0, Limit = maksymalny
               → Efektywnie "flat model"

Wyjątki:
- FS, GS → używane dla Thread Local Storage (TLS)
- CS → poziom uprzywilejowania (ring 0/3)
```

**Powód:** Segmentacja komplikuje pamięć wirtualną i nie jest potrzebna z ochroną per-strona (NX bit, SMEP, SMAP).

---

## 🎯 Kluczowe punkty do zapamiętania

1. **Stronicowanie** = równe strony/ramki, brak fragmentacji zewnętrznej
2. **Segmentacja** = logiczne jednostki, fragmentacja zewnętrzna
3. **Współczesne OS** = stronicowanie (segmentacja wyłączona)
4. **TLB** = cache translacji, kluczowy dla wydajności
5. **Page fault** = strona nie w RAM, załaduj z dysku
6. **Thrashing** = za mało RAM, ciągłe page faults

---

## 📖 Źródła do pogłębienia

1. Silberschatz, Galvin - "Operating System Concepts"
2. Tanenbaum - "Modern Operating Systems"
3. Intel Manual Vol. 3 - System Programming Guide
4. Linux kernel documentation - Memory Management
