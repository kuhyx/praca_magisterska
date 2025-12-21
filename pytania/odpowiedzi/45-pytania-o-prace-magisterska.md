# Pytania egzaminacyjne o pracę magisterską

## Temat pracy
**"Porównanie wydajności i możliwości współczesnych silników gier komputerowych"**

---

## 🎯 Pytanie 1: Cel i motywacja pracy

### Pytanie
**"Jaki jest cel Pana pracy magisterskiej i dlaczego wybrano akurat temat porównania silników gier?"**

### Odpowiedź wzorcowa

Celem pracy jest **kompleksowe porównanie wydajności i możliwości współczesnych silników gier** (Unity i Unreal Engine), ze szczególnym uwzględnieniem ich wpływu na proces tworzenia gier oraz końcową jakość produktu.

**Motywacja:**
1. **Praktyczna potrzeba** - wybór silnika to kluczowa decyzja wpływająca na cały cykl życia projektu
2. **Brak obiektywnych porównań** - większość istniejących materiałów ma charakter subiektywny lub marketingowy
3. **Dominacja rynkowa** - Unity i Unreal wspólnie obsługują >70% globalnego rynku gier
4. **Reprezentatywność architektur** - silniki reprezentują fundamentalnie różne podejścia (C# z GC vs C++ z ręcznym zarządzaniem pamięcią)

**Praktyczne znaczenie:**
- Pomoc deweloperom w świadomym wyborze narzędzi
- Dostarczenie obiektywnych danych wydajnościowych
- Analiza praktycznych aspektów pracy z silnikami

---

## 🎯 Pytanie 2: Metodologia badawcza

### Pytanie
**"Jaką metodologię badawczą zastosowano w pracy? Dlaczego wybrano takie podejście?"**

### Odpowiedź wzorcowa

Zastosowano **metodologię mieszaną** łączącą podejście ilościowe i jakościowe:

```
┌────────────────────────────────────────────────────────────────┐
│                    METODOLOGIA BADAWCZA                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ILOŚCIOWA (Quantitative):                                    │
│  ├── Testy wydajnościowe z NVIDIA Nsight Graphics            │
│  ├── Pomiary FPS, CPU, GPU, pamięci RAM/VRAM                 │
│  └── Obiektywne metryki porównawcze                          │
│                                                                │
│  JAKOŚCIOWA (Qualitative):                                    │
│  ├── 8 wywiadów pogłębionych z deweloperami                  │
│  ├── Analiza dokumentacji i materiałów edukacyjnych          │
│  └── Doświadczenia z implementacji porównawczej              │
│                                                                │
│  TRIANGULACJA ŹRÓDEŁ:                                         │
│  └── Weryfikacja wniosków z wielu perspektyw                 │
└────────────────────────────────────────────────────────────────┘
```

**Uzasadnienie podejścia mieszanego:**
1. **Obiektywność** - testy wydajnościowe eliminują subiektywizm
2. **Kontekst praktyczny** - wywiady dostarczają perspektywy użytkowników
3. **Kompletność** - sama wydajność nie determinuje jakości narzędzia
4. **Wiarygodność** - triangulacja zwiększa pewność wniosków

---

## 🎯 Pytanie 3: Wybór gry testowej

### Pytanie
**"Dlaczego do testów wybrano gatunek bullet hell? Jakie to ma znaczenie dla wyników?"**

### Odpowiedź wzorcowa

**Gatunek bullet hell (danmaku)** to strzelanka, w której gracz mierzy się z setkami/tysiącami pocisków tworzących skomplikowane wzory.

**Uzasadnienie wyboru:**

| Aspekt | Dlaczego bullet hell? |
|--------|----------------------|
| **Intensywność** | Setki obiektów na ekranie → obciążenie renderingu |
| **Pamięć** | Ciągłe tworzenie/niszczenie pocisków → test GC vs ręczne |
| **Fizyka** | Kolizje gracz↔pociski → obciążenie systemu fizyki |
| **Skalowalność** | Łatwa kontrola obciążenia przez liczbę pocisków |
| **Prostota** | Prosta logika → fokus na wydajność, nie złożoność |
| **Reprezentatywność** | Typowa gra 2D indie → duży segment rynku |

**Parametry gry testowej:**
- Czas rozgrywki: 90 sekund
- Maksymalnie ~500 jednoczesnych pocisków
- 3 typy przeciwników z różnymi wzorami
- Object pooling dla eliminacji alokacji runtime

**Znaczenie dla wyników:**
Gatunek wymusza stosowanie technik optymalizacyjnych (object pooling, spatial partitioning), których efektywność może różnić się między silnikami, co pozwala na rzeczywiste porównanie.

---

## 🎯 Pytanie 4: Różnice architektoniczne silników

### Pytanie
**"Jakie są fundamentalne różnice architektoniczne między Unity a Unreal Engine?"**

### Odpowiedź wzorcowa

```
┌─────────────────────────────────────────────────────────────────┐
│         PORÓWNANIE ARCHITEKTONICZNE UNITY vs UNREAL            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  UNITY:                          UNREAL ENGINE:                │
│  ├─ Język: C#                    ├─ Język: C++ / Blueprints   │
│  ├─ Pamięć: Garbage Collector    ├─ Pamięć: Ręczne/Smart ptr  │
│  ├─ Architektura: GameObject     ├─ Architektura: Actor       │
│  │   └─ Component                │   └─ Component             │
│  ├─ Natywne 2D: TAK              ├─ Natywne 2D: NIE           │
│  ├─ Kod źródłowy: częściowo     ├─ Kod źródłowy: pełny       │
│  └─ Rozmiar projektu: ~100 MB   └─ Rozmiar projektu: ~1-2 GB │
│                                                                 │
│  FILOZOFIA:                                                     │
│  Unity: Prostota, dostępność    Unreal: Moc, kontrola          │
│         Mobile, indie                   AAA, fotorealizm       │
└─────────────────────────────────────────────────────────────────┘
```

**Kluczowe implikacje:**

1. **C# z GC vs C++:**
   - Unity: szybszy rozwój, możliwe GC spikes
   - Unreal: maksymalna wydajność, większa złożoność

2. **Krzywa uczenia:**
   - Unity: łagodna, przyjazna początkującym
   - Unreal: stroma, wymaga znajomości C++

3. **Specjalizacja:**
   - Unity: elastyczne, dobre dla różnych typów gier
   - Unreal: zoptymalizowane pod FPS/AAA

---

## 🎯 Pytanie 5: Hipotezy badawcze

### Pytanie
**"Jakie hipotezy badawcze postawiono w pracy? Czy zostały potwierdzone?"**

### Odpowiedź wzorcowa

**Hipotezy badawcze:**

1. **H1:** "Silniki komercyjne oferują lepszą wydajność niż rozwiązania open source"
   - *Status:* Nie dotyczy bezpośrednio (oba badane silniki są komercyjne z darmowymi wersjami)

2. **H2:** "Kompleksowość funkcjonalności wpływa negatywnie na wydajność"
   - *Status:* Częściowo potwierdzona - Unreal z większą liczbą wbudowanych mechanizmów wymaga większych zasobów (rozmiar projektu, RAM), ale kompensuje to optymalizacjami niskopoziomowymi

3. **H3:** "Łatwość użycia jest odwrotnie proporcjonalna do możliwości konfiguracji"
   - *Status:* Potwierdzona - Unity z łagodniejszą krzywą uczenia oferuje mniejszą kontrolę nad niskopoziomowymi aspektami; Unreal wymaga większego wysiłku, ale daje pełny dostęp do kodu źródłowego

**Wnioski z hipotez:**
- Trade-off między dostępnością a kontrolą jest realny
- Nie ma "lepszego" silnika - wybór zależy od kontekstu projektu

---

## 🎯 Pytanie 6: Wyniki wywiadów z deweloperami

### Pytanie
**"Jakie główne wnioski płyną z wywiadów z deweloperami gier?"**

### Odpowiedź wzorcowa

Przeprowadzono **8 wywiadów pogłębionych** z deweloperami o zróżnicowanym doświadczeniu (1-10+ lat).

**Kluczowe wnioski:**

```
┌────────────────────────────────────────────────────────────────┐
│                    WNIOSKI Z WYWIADÓW                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ 1. DOKUMENTACJA:                                               │
│    Unity: "dogłębna, szczegółowa, z przykładami"              │
│    Unreal: "szkieletowa, praktycznie nieistniejąca"           │
│                                                                │
│ 2. MATERIAŁY EDUKACYJNE:                                       │
│    Unity: więcej, lepszej jakości (Brackeys)                  │
│    Unreal: mniej, często nieaktualne, skupione na Blueprints │
│                                                                │
│ 3. PRÓG WEJŚCIA:                                               │
│    Unity: łagodniejszy, C# jako język wysokopoziomowy         │
│    Unreal: wyższy, C++ rozszerzony o makra silnika           │
│                                                                │
│ 4. SPECJALIZACJA:                                              │
│    Unity: uniwersalne narzędzie                                │
│    Unreal: zoptymalizowane pod FPS/gry akcji                  │
│                                                                │
│ 5. KOMPILACJA:                                                 │
│    Unity: problemy z czasem przy dużych projektach            │
│    Rozwiązanie: Assembly Definitions                           │
└────────────────────────────────────────────────────────────────┘
```

**Wspólne problemy:**
- Poradniki skupiają się na pojedynczych mechanikach, nie na architekturze
- Brak holistycznego podejścia do nauczania

---

## 🎯 Pytanie 7: Narzędzia profilowania

### Pytanie
**"Jakie narzędzia wykorzystano do testów wydajnościowych? Dlaczego akurat te?"**

### Odpowiedź wzorcowa

**Główne narzędzie: NVIDIA Nsight Graphics**

**Uzasadnienie wyboru:**
1. **Niezależność** - zewnętrzne narzędzie, nie faworyzuje żadnego silnika
2. **Precyzja** - niskopoziomowe metryki GPU
3. **Porównywalność** - te same metryki dla obu silników
4. **Kompleksowość** - analiza całego pipeline'u renderowania

**Mierzone metryki:**

| Kategoria | Metryki |
|-----------|---------|
| **Rendering** | FPS, frame time, draw calls |
| **GPU** | Obciążenie, pamięć VRAM, shader performance |
| **CPU** | Obciążenie, czas na frame |
| **Pamięć** | RAM allocation, GC events (Unity) |

**Dodatkowe narzędzia:**
- Wbudowane profilery Unity i Unreal (dla kontekstu wewnętrznego)
- Monitoring systemu operacyjnego

---

## 🎯 Pytanie 8: Ograniczenia badań

### Pytanie
**"Jakie są ograniczenia przeprowadzonych badań? Co można by ulepszyć?"**

### Odpowiedź wzorcowa

**Ograniczenia:**

1. **Zakres testów:**
   - Tylko jeden gatunek gry (bullet hell 2D)
   - Brak testów 3D, VR, mobile

2. **Środowisko:**
   - Jedna konfiguracja sprzętowa
   - Brak testów na różnych platformach

3. **Wersje silników:**
   - Wyniki specyficzne dla konkretnych wersji
   - Silniki szybko się rozwijają

4. **Próba wywiadów:**
   - 8 respondentów (ograniczona reprezentatywność)
   - Głównie rynek polski

5. **Subiektywność implementacji:**
   - Implementacja w obu silnikach przez jedną osobę
   - Możliwa nieświadoma preferencja

**Propozycje ulepszeń:**
- Testy na większej liczbie gatunków gier
- Badanie na różnych platformach (mobile, konsole)
- Większa próba do badań jakościowych
- Współpraca z ekspertami od każdego silnika

---

## 🎯 Pytanie 9: Praktyczne rekomendacje

### Pytanie
**"Jakie praktyczne rekomendacje dla deweloperów wynikają z pracy?"**

### Odpowiedź wzorcowa

```
┌────────────────────────────────────────────────────────────────┐
│              REKOMENDACJE WYBORU SILNIKA                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ WYBIERZ UNITY gdy:                                             │
│ ✓ Tworzysz grę 2D lub mobilną                                 │
│ ✓ Jesteś początkującym deweloperem                            │
│ ✓ Masz ograniczony budżet/zespół (indie)                      │
│ ✓ Znasz C# lub języki podobne                                 │
│ ✓ Priorytetem jest szybkość prototypowania                    │
│                                                                │
│ WYBIERZ UNREAL gdy:                                            │
│ ✓ Tworzysz grę AAA lub fotorealistyczną                       │
│ ✓ Potrzebujesz maksymalnej wydajności                         │
│ ✓ Robisz grę FPS/akcji z widokiem pierwszej osoby            │
│ ✓ Masz doświadczenie w C++                                    │
│ ✓ Potrzebujesz zaawansowanych narzędzi cinematycznych         │
│                                                                │
│ UWAGI OGÓLNE:                                                  │
│ • Oba silniki są profesjonalne i dojrzałe                     │
│ • Wybór zależy od kontekstu projektu, nie "lepszości"         │
│ • Warto znać oba dla elastyczności kariery                    │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Pytanie 10: Wkład naukowy pracy

### Pytanie
**"Jaki jest wkład naukowy Pana pracy? Co wnosi do dziedziny?"**

### Odpowiedź wzorcowa

**Wkład naukowy:**

1. **Metodologia porównawcza:**
   - Zaproponowano systematyczne podejście do porównywania silników gier
   - Połączenie metod ilościowych (benchmarki) i jakościowych (wywiady)

2. **Obiektywne dane:**
   - Dostarczono konkretnych wyników wydajnościowych zamiast subiektywnych opinii
   - Dane z kontrolowanych warunków testowych

3. **Perspektywa praktyka:**
   - Wywiady z deweloperami dostarczają realnego kontekstu użytkowania
   - Uzupełnienie luki między marketingiem a rzeczywistością

4. **Dokumentacja różnic:**
   - Szczegółowe opisanie różnic architektonicznych
   - Praktyczne implikacje dla procesu deweloperskiego

**Znaczenie dla branży:**
- Pomoc w świadomych decyzjach technologicznych
- Redukcja ryzyka błędnego wyboru narzędzi
- Materiał edukacyjny dla początkujących deweloperów

---

## 🎯 Pytanie 11: Object pooling

### Pytanie
**"Czym jest object pooling i dlaczego był kluczowy w pracy?"**

### Odpowiedź wzorcowa

**Object pooling** to technika optymalizacyjna polegająca na **ponownym wykorzystywaniu obiektów** zamiast ciągłego tworzenia i niszczenia.

```
┌────────────────────────────────────────────────────────────────┐
│                     OBJECT POOLING                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  BEZ POOLINGU:                    Z POOLINGIEM:               │
│  ┌─────┐                          ┌─────┐                     │
│  │spawn│→ new Bullet()            │spawn│→ pool.Get()         │
│  └─────┘                          └─────┘                     │
│     ↓                                ↓                         │
│  [gameplay]                       [gameplay]                   │
│     ↓                                ↓                         │
│  ┌─────┐                          ┌─────┐                     │
│  │die  │→ destroy + GC            │die  │→ pool.Return()      │
│  └─────┘                          └─────┘                     │
│                                                                │
│  Problemy:                        Korzyści:                    │
│  • Alokacje każdą klatkę         • Zero alokacji runtime     │
│  • GC spikes (Unity)             • Brak GC spikes            │
│  • Fragmentacja pamięci          • Stały koszt pamięci       │
└────────────────────────────────────────────────────────────────┘
```

**Znaczenie dla pracy:**
- Bullet hell generuje setki pocisków/sekundę
- Bez poolingu → ciągłe alokacje → GC spikes w Unity
- Pooling pozwala na **uczciwe porównanie** silników (eliminuje narzut GC)
- Technika stosowana w obu implementacjach

---

## 🎯 Pytanie 12: Różnice w zarządzaniu pamięcią

### Pytanie
**"Jak różni się zarządzanie pamięcią w Unity i Unreal Engine? Jakie to ma konsekwencje?"**

### Odpowiedź wzorcowa

```
┌────────────────────────────────────────────────────────────────┐
│            ZARZĄDZANIE PAMIĘCIĄ: UNITY vs UNREAL               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  UNITY (C# / .NET):                                           │
│  ├─ Garbage Collector (GC) - automatyczne zwalnianie          │
│  ├─ Zalety:                                                   │
│  │   • Brak memory leaks z definicji                         │
│  │   • Prostsze programowanie                                 │
│  │   • Bezpieczeństwo typów                                  │
│  ├─ Wady:                                                     │
│  │   • GC spikes (nieprzewidywalne pauzy)                    │
│  │   • Mniejsza kontrola nad alokacją                        │
│  │   • Boxing/unboxing overhead                               │
│  └─ Mitygacja: object pooling, struct zamiast class          │
│                                                                │
│  UNREAL (C++):                                                │
│  ├─ Ręczne zarządzanie + smart pointers                       │
│  ├─ Zalety:                                                   │
│  │   • Pełna kontrola nad pamięcią                           │
│  │   • Przewidywalna wydajność                                │
│  │   • Brak GC spikes                                         │
│  ├─ Wady:                                                     │
│  │   • Ryzyko memory leaks                                    │
│  │   • Dangling pointers                                      │
│  │   • Większa złożoność kodu                                 │
│  └─ Mechanizmy UE: TSharedPtr, TWeakPtr, garbage collection  │
│     dla UObject                                                │
└────────────────────────────────────────────────────────────────┘
```

**Konsekwencje praktyczne:**
- Unity: łatwiejsze dla początkujących, ale wymaga uwagi przy wydajności
- Unreal: wymaga doświadczenia, ale daje przewidywalność

---

## 🎯 Pytanie 13: Kryteria porównania

### Pytanie
**"Według jakich kryteriów porównywano silniki?"**

### Odpowiedź wzorcowa

**Trzy główne kategorie kryteriów:**

### 1. Wydajność
- Szybkość renderowania (FPS)
- Zużycie pamięci RAM
- Obciążenie procesora
- Zużycie pamięci karty graficznej
- Czas ładowania scen

### 2. Funkcjonalność
- Wsparcie dla różnych typów renderingu
- Systemy fizyki
- Systemy audio
- Wsparcie dla VR/AR
- Możliwości skryptowania

### 3. Użyteczność
- Intuicyjność interfejsu
- Jakość dokumentacji
- Dostępność tutoriali
- Wsparcie społeczności
- Czas potrzebny na naukę (krzywa uczenia)

**Dlaczego te kryteria:**
- Pokrywają wszystkie aspekty istotne dla deweloperów
- Możliwe do zmierzenia (ilościowe) lub oceny (jakościowe)
- Odpowiadają realnym potrzebom przy wyborze silnika

---

## 🎯 Pytanie 14: Przyszłość badań

### Pytanie
**"Jakie kierunki dalszych badań Pan proponuje?"**

### Odpowiedź wzorcowa

**Propozycje dalszych badań:**

1. **Rozszerzenie zakresu testów:**
   - Testy na grach 3D (różne gatunki)
   - Porównanie wydajności VR/AR
   - Testy na platformach mobilnych i konsolach

2. **Uwzględnienie innych silników:**
   - Godot (open source, rosnąca popularność)
   - CryEngine, Amazon Lumberyard
   - Własne silniki studiów AAA

3. **Badania longitudinalne:**
   - Śledzenie rozwoju silników w czasie
   - Porównanie wersji (Unity 2020 vs 2025)

4. **Pogłębienie badań jakościowych:**
   - Większa próba deweloperów
   - Badania w różnych krajach/regionach
   - Studium przypadków konkretnych produkcji

5. **Aspekty ekonomiczne:**
   - Koszty licencji i royalties
   - ROI przy wyborze silnika
   - Czas rozwoju projektu

---

## 🎯 Pytanie 15: Blueprints vs C++ w Unreal

### Pytanie
**"Jakie są różnice między programowaniem w Blueprints a C++ w Unreal Engine?"**

### Odpowiedź wzorcowa

```
┌────────────────────────────────────────────────────────────────┐
│              BLUEPRINTS vs C++ w UNREAL ENGINE                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  BLUEPRINTS:                      C++:                        │
│  ├─ Wizualne programowanie        ├─ Tradycyjny kod          │
│  ├─ Drag & drop węzłów           ├─ Tekstowe pisanie        │
│  ├─ Szybkie prototypowanie        ├─ Maksymalna wydajność    │
│  ├─ Dla designerów/artystów       ├─ Dla programistów        │
│  ├─ Wolniejsze wykonanie          ├─ Kompilacja do natywnego │
│  └─ Trudniejsze przy złożoności   └─ Pełna kontrola          │
│                                                                │
│  TYPOWE ZASTOSOWANIE:                                          │
│  Blueprints: UI, proste mechaniki, prototypy                  │
│  C++: core gameplay, AI, systemy krytyczne wydajnościowo      │
│                                                                │
│  BEST PRACTICE: Hybrydowe podejście                           │
│  └─ Implementacja w C++, ekspozycja do Blueprints             │
└────────────────────────────────────────────────────────────────┘
```

**Wnioski z wywiadów:**
- Poradniki często skupiają się na Blueprints
- Profesjonalne produkcje głównie C++
- Blueprints dobre do nauki konceptów silnika

---

## 📋 Lista wszystkich pytań (podsumowanie)

1. Cel i motywacja pracy
2. Metodologia badawcza
3. Wybór gry testowej (bullet hell)
4. Różnice architektoniczne silników
5. Hipotezy badawcze
6. Wyniki wywiadów z deweloperami
7. Narzędzia profilowania
8. Ograniczenia badań
9. Praktyczne rekomendacje
10. Wkład naukowy pracy
11. Object pooling
12. Różnice w zarządzaniu pamięcią
13. Kryteria porównania
14. Przyszłość badań
15. Blueprints vs C++ w Unreal

---

## 🧠 Mnemoniki dla obrony

### "MWUK" - Metodologia:
**M**ieszana, **W**ywiady, **U**nity vs Unreal, **K**ryterium porównania

### "BH = Benchmark Heaven":
**B**ullet **H**ell = idealny test (dużo obiektów, kolizji, alokacji)

### "Unity = Easy, Unreal = Elite":
Unity: łatwiejsze, Unreal: dla zaawansowanych

### "C# GC, C++ MC":
C# = Garbage Collection, C++ = Manual Control
