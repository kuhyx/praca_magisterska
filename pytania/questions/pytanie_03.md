## PYTANIE 3: Redundancja i normalizacja (BD2)

**Omówić zagadnienia redundancji i normalizacji w relacyjnej bazie danych.**

---

### Tło pojęciowe — słowniczek

**Relacja (tabela)** — w bazie danych: tabela z kolumnami (atrybutami) i wierszami (krotkami/rekordami). Np. tabela Studenci z kolumnami: StudentID, Imię, Nazwisko, WydziałID.

**Atrybut (attribute)** — kolumna w tabeli. Np. „Imię", „WydziałID", „NazwaKursu". Każdy atrybut ma nazwę i typ danych (tekst, liczba, data itp.).

**Klucz główny (primary key, PK)** — kolumna (lub zestaw kolumn), której wartość JEDNOZNACZNIE identyfikuje każdy wiersz. Np. StudentID = 12345 → dokładnie jeden student. Nie może się powtarzać, nie może być NULL.

**Klucz złożony (composite key)** — klucz główny składający się z WIĘCEJ NIŻ JEDNEJ kolumny. Np. klucz (StudentID, KursID) — jeden student na jednym kursie to unikalny zapis. Sam StudentID ani sam KursID nie wystarczą, bo student ma wiele kursów, a kurs ma wielu studentów.

**Atrybut wtórny (non-prime attribute)** — kolumna, która NIE jest częścią żadnego klucza kandydującego. Np. w tabeli z kluczem (StudentID, KursID): NazwaKursu, Ocena, NazwaWydziału — to atrybuty wtórne (nie identyfikują wiersza). **Atrybut pierwszy (prime)** — kolumna, która JEST częścią jakiegoś klucza (np. StudentID).

**Nadklucz (superkey)** — dowolny zbiór kolumn, który JEDNOZNACZNIE identyfikuje wiersz. Każdy klucz główny jest nadkluczem, ale nadklucz może mieć „nadmiarowe" kolumny. Np. {StudentID} to klucz i nadklucz; {StudentID, Imię} to nadklucz (ale nie minimalny klucz).

**Redundancja** — powtarzanie tych samych danych w wielu miejscach. Nie chodzi o kopie zapasowe — chodzi o niepotrzebne duplikowanie informacji w tabeli.

Przykład — tabela „Rejestr" (ZŁEJ konstrukcji, BEZ normalizacji) — ta sama tabela będzie normalizowana krok po kroku od 0NF do 5NF w dalszej części:

![Tabela 0NF — forma nienormalna z listami w komórkach](img/nf_0nf_table.png)

Problem: „Anna", „W4", „EiTI", „Bazy danych" powtórzone wielokrotnie! Kolumna „Telefony" zawiera listy (nieatomowe wartości).

**Anomalia** — niepożądany efekt uboczny operacji na redundantnych danych. Trzy typy:

**Anomalia wstawiania** — nie możesz dodać danych bez podania niepotrzebnych powiązań.
- Przykład: chcesz dodać nowy wydział W5 „Chemia" do systemu, ale nie ma jeszcze żadnego studenta na tym wydziale. W tej tabeli NIE DA SIĘ — bo StudentID (część klucza) nie może być NULL.

**Anomalia usuwania** — usuwając jeden fakt, tracisz niezwiązany inny.
- Przykład: Ewa (jedyny student Fizyki) rezygnuje → usuwasz jej wiersz → tracisz informację, że wydział W2 to „Fizyka" i istnieje kurs „Optyka". Dane o wydziale i kursie znikają razem ze studentem!

**Anomalia modyfikacji** — zmiana jednego faktu wymaga aktualizacji wielu wierszy.
- Przykład: wydział W4 zmienia nazwę z „EiTI" na „Informatyka". Trzeba zaktualizować KAŻDY wiersz, w którym jest NazwaWydziału = „EiTI" (tu: 3 wiersze). Jeśli pominiesz jeden → niespójność.

**Zależność funkcyjna (FD — Functional Dependency):** X → Y oznacza: „znając wartość X, ZAWSZE mogę jednoznacznie wyznaczyć Y". Jak funkcja matematyczna: f(x) daje dokładnie jedno y. Np. StudentID → Imię (jeden student = jedno imię), KursID → NazwaKursu (jeden kurs = jedna nazwa). **X → Y NIE oznacza Y → X!** (StudentID → WydziałID, ale WydziałID → StudentID NIE — na wydziale jest wielu studentów).

**Zależność przechodnia (transitive dependency):** A → B i B → C, więc A → C „przez pośrednika B". Np. StudentID → WydziałID → NazwaWydziału. StudentID nie określa bezpośrednio NazwaWydziału — robi to pośrednio przez WydziałID. Problem: NazwaWydziału „zależy od czegoś, co nie jest kluczem" → redundancja.

**Nietrywialna FD:** X → A, gdzie A nie jest częścią X. Np. StudentID → Imię (nietrywialna: Imię ≠ StudentID). Ale {StudentID, Imię} → StudentID jest TRYWIALNA (StudentID jest częścią lewej strony — oczywiste). W BCNF sprawdzamy tylko nietrywialne FD.
P
**Wielowartościowa zależność (MVD — Multi-Valued Dependency):** X →→ Y oznacza: dla jednej wartości X istnieje ZBIÓR wartości Y, niezależny od reszty. Np. Student →→ Hobby i Student →→ Kurs: hobby Ani nie zależą od jej kursów i odwrotnie, ale ich połączenie tworzy iloczyn kartezjański (niepotrzebne powtórzenia).

**Dekompozycja** — rozbicie jednej dużej tabeli na kilka mniejszych, połączonych kluczami obcymi. Cel: każda tabela przechowuje JEDEN fakt. **Normalizacja eliminuje redundancję** właśnie przez dekompozycję — informacja zamiast być powtarzana w wielu wierszach, przechowywana jest RAZ w osobnej tabeli i łączona przez JOIN.

**Atomowe wartości (1NF)** — każda komórka zawiera JEDNĄ niepodzielną wartość. NIE listy, NIE zbiory, NIE tabele w komórce.

**Zależność złączenia (JD — Join Dependency):** Tabela R spełnia JD *{R₁, R₂, ..., Rₙ} jeśli R = R₁ ⨝ R₂ ⨝ ... ⨝ Rₙ (bezstratna dekompozycja na n projekcji). Każda MVD implikuje JD, ale JD jest OGÓLNIEJSZA — obejmuje dekompozycje na 3+ tabele, których MVD nie wyraża. 5NF eliminuje takie „ukryte" redundancje.

### Pełny przykład: od 0NF do 5NF krok po kroku

Używamy JEDNEJ tabeli „Rejestr" i normalizujemy ją przez WSZYSTKIE postacie normalne. W każdym kroku pokazujemy: (1) jaki problem istnieje, (2) jaką regułę łamie, (3) jak go naprawić dekompozycją.

**Zależności funkcyjne w tabeli Rejestr:**
- StID → Imię, WydziałID (jeden student = jedno imię, jeden wydział)
- WydziałID → NazwaWydziału (jeden wydział = jedna nazwa)
- KursID → NazwaKursu (jeden kurs = jedna nazwa)
- (StID, KursID) → Prowadzący (student na kursie ma jednego prowadzącego)
- Prowadzący → KursID (jeden prowadzący uczy dokładnie jednego kursu)
- StID →→ Telefon (wielowartościowa — student ma ZBIÓR telefonów)

---

### KROK 1: 0NF → 1NF (atomowość wartości)

**Problem:** Kolumna „Telefony" zawiera listy wartości (np. „111-222, 333-444") — to NIE jest atomowe.

**Reguła 1NF:** Każda komórka = JEDNA niepodzielna wartość + istnieje klucz główny.

**Naprawa:** Wydziel wielowartościowy atrybut do osobnej tabeli.

![Tabele po normalizacji do 1NF](img/nf_1nf_tables.png)

**Wynik:** Dwie tabele — Rejestr1NF (klucz: StID, KursID) i Telefony (klucz: StID, Telefon). Wszystkie komórki atomowe ✓.

---

### KROK 2: 1NF → 2NF (pełna zależność od klucza)

**Problem:** Klucz złożony (StID, KursID), ale wiele atrybutów zależy tylko od CZĘŚCI klucza:
- StID → Imię, WydziałID, NazwaWydziału — zależy TYLKO od StID (częściowa zależność!)
- KursID → NazwaKursu — zależy TYLKO od KursID (częściowa zależność!)
- (StID, KursID) → Prowadzący — zależy od PEŁNEGO klucza ✓

**Reguła 2NF:** Każdy atrybut wtórny (non-prime) zależy od CAŁEGO klucza, nie od jego części.

**Naprawa:** Wydziel atrybuty częściowo zależne do osobnych tabel.

![Tabele po normalizacji do 2NF](img/nf_2nf_tables.png)

**Wynik:** Studenci (StID → Imię, WydziałID, NazwaWydziału), Kursy (KursID → NazwaKursu), Zapisy (StID, KursID → Prowadzący), Telefony.

**Dlaczego to ważne:** Bez 2NF: dodanie nowego kursu wymaga podania studenta. Z 2NF: dodajesz kurs do tabeli Kursy niezależnie.

---

### KROK 3: 2NF → 3NF (brak zależności przechodnich)

**Problem w tabeli Studenci:** StID → WydziałID → NazwaWydziału — zależność PRZECHODNIA!
- NazwaWydziału nie zależy bezpośrednio od klucza (StID) — zależy od WydziałID, który sam zależy od StID.
- WydziałID NIE jest kluczem tabeli Studenci → NazwaWydziału zależy od nie-klucza → redundancja „EiTI" powtórzone.

**Reguła 3NF:** 2NF + żaden atrybut wtórny nie zależy od innego atrybutu wtórnego (brak zależności przechodnich). Formalnie: dla każdej nietrywialnej FD X → A, albo X jest nadkluczem, ALBO A jest atrybutem pierwszym (prime).

**Naprawa:** Wydziel WydziałID → NazwaWydziału do osobnej tabeli Wydziały.

![Tabele po normalizacji do 3NF](img/nf_3nf_tables.png)

**Wynik:** Studenci (StID → Imię, WydziałID), Wydziały (WydziałID → NazwaWydziału), Kursy, Zapisy, Telefony.

**Dlaczego to ważne:** Bez 3NF: zmiana nazwy wydziału wymaga aktualizacji WIELU wierszy w Studenci. Z 3NF: zmiana nazwy = 1 wiersz w tabeli Wydziały.

---

### KROK 4: 3NF → BCNF (każdy determinant = nadklucz)

**Problem w tabeli Zapisy(StID, KursID, Prowadzący):**
- Klucz: (StID, KursID)
- FD: Prowadzący → KursID (jeden prowadzący uczy jednego kursu)
- Prowadzący NIE jest nadkluczem tabeli Zapisy → **NARUSZENIE BCNF!**
- ALE: KursID JEST atrybutem pierwszym (prime — część klucza) → wyjątek 3NF → **3NF jest spełnione!**

**Reguła 3NF vs BCNF — kluczowa różnica:**
- **3NF:** Dla FD X → A: X jest nadkluczem **LUB** A jest prime. (Wyjątek dla atrybutów pierwszych!)
- **BCNF:** Dla FD X → A: X **MUSI** być nadkluczem. Kropka. (Bez wyjątków!)
- Dlatego BCNF jest SILNIEJSZA — eliminuje anomalie, które 3NF dopuszcza.

**Kiedy 3NF ≠ BCNF?** Dokładnie wtedy, gdy istnieje nietrywialna FD, w której lewa strona nie jest nadkluczem, ale prawa strona jest atrybutem pierwszym. To się zdarza tylko przy kluczach złożonych z nakładającymi się zależnościami.

**Naprawa:** Rozbij Zapisy na dwie tabele wg FD Prowadzący → KursID.

![Tabele po normalizacji do BCNF](img/nf_bcnf_tables.png)

**Wynik:** ProwadzącyKurs (Prowadzący → KursID), StudentProwadzący (StID, Prowadzący).

**Rekonstrukcja:** StudentProwadzący ⨝ ProwadzącyKurs ON Prowadzący = oryginalne Zapisy (bezstratnie!).

**Uwaga:** Dekompozycja BCNF może utracić pewne FD (tu: (StID, KursID) → Prowadzący nie jest wymuszona przez żadną z dwóch tabel z osobna). To cena za eliminację anomalii — czasem 3NF jest „wystarczająco dobra" w praktyce.

---

### KROK 5: BCNF → 4NF (brak wielowartościowych zależności)

**Nowy scenariusz:** Chcemy przechowywać hobby i umiejętności studentów. Tworzymy tabelę:
StudentAktywności(StID, Hobby, Umiejętność) — klucz: (StID, Hobby, Umiejętność).

**Problem:** Student 1 (Anna) ma 2 hobby (Szachy, Bieganie) i 2 umiejętności (Python, SQL). Te zbiory są NIEZALEŻNE od siebie, ale w jednej tabeli tworzą **iloczyn kartezjański** → 2 × 2 = 4 wiersze!

**MVD:** StID →→ Hobby i StID →→ Umiejętność — dwie niezależne wielowartościowe zależności.

**Reguła 4NF:** BCNF + dla każdej nietrywialnej MVD X →→ Y, X jest nadkluczem. Niezależne zbiory wartości nie mogą być w jednej tabeli.

**Naprawa:** Rozdziel do: StudentHobby(StID, Hobby) + StudentUmiejętność(StID, Umiejętność).

![Przykład naruszenia i naprawy 4NF](img/nf_4nf_example.png)

**Dlaczego to ważne:** Bez 4NF: dodanie nowego hobby Anny wymaga dodania TYLE wierszy, ile ma umiejętności (i odwrotnie). Z 4NF: dodanie hobby = 1 wiersz.

**Jak rozpoznać naruszenie 4NF:**
1. Czy tabela ma klucz złożony z 3+ kolumn? (StID, Hobby, Umiejętność)
2. Czy istnieją dwa niezależne zbiory wartości dla tego samego klucza? (Hobby niezależne od Umiejętności)
3. Czy widać „iloczyn kartezjański" w danych? (każde hobby × każda umiejętność)
→ Jeśli TAK na wszystkie → naruszenie 4NF.

---

### KROK 6: 4NF → 5NF (brak zależności złączenia)

**Nowy scenariusz:** Tabela Dostawy(Dostawca, Część, Projekt) — rejestr kto dostarcza co do którego projektu. Klucz: (Dostawca, Część, Projekt) — cała krotka.

**Problem:** Tabela jest w 4NF (brak nietrywialnych MVD), ale może zawierać ukrytą redundancję wynikającą z **zależności złączenia** (JD — Join Dependency).

**Reguła cykliczna:** Jeśli zachodzi ograniczenie biznesowe:
- Dostawca dostarcza Część, I
- Dostawca dostarcza do Projektu, I
- Część jest używana w Projekcie
- → TO Dostawca dostarcza tę Część do tego Projektu

...to tabela Dostawy jest redundantna — można ją bezstratnie rozłożyć na TRZY tabele binarne.

**Reguła 5NF (PJNF — Project-Join Normal Form):** Każda zależność złączenia jest implikowana przez klucze kandydujące. Innymi słowy: tabela NIE DA SIĘ dalej rozłożyć bezstratnie (bez utraty informacji) na mniejsze tabele.

**Naprawa:** Dekomponuj na trzy tabele: DostawcaCzęść, DostawcaProjekt, CzęśćProjekt.

![Przykład naruszenia i naprawy 5NF](img/nf_5nf_example.png)

**Rekonstrukcja:** DostawcaCzęść ⨝ DostawcaProjekt ⨝ CzęśćProjekt = oryginalna tabela Dostawy.

**UWAGA:** Dekompozycja 5NF jest poprawna TYLKO jeśli reguła cykliczna rzeczywiście zachodzi w domenie biznesowej! Jeśli nie zachodzi, JOIN wygeneruje fałszywe krotki (spurious tuples).

**Kiedy 5NF ma znaczenie praktyczne?**
- Rzadko w typowych aplikacjach (większość zatrzymuje się na 3NF/BCNF)
- Głównie w złożonych relacjach ternary/n-ary z ograniczeniami cyklicznymi
- Np. systemy logistyczne, harmonogramowanie, konfiguracje produktów

**Jak rozpoznać naruszenie 5NF:**
1. Tabela ma klucz = cała krotka (brak atrybutów nie-kluczowych)
2. Tabela jest w 4NF (brak MVD)
3. ALE da się ją rozłożyć na 3+ mniejszych tabel i bezstratnie złożyć JOINem
4. To rozkładalność wynika z ograniczenia biznesowego (reguły cyklicznej), nie z MVD

---

### Podsumowanie normalizacji 0NF → 5NF

![Schemat postaci normalnych — przejście od 0NF do 5NF](img/nf_summary_flow.png)

| Postać | Co eliminuje | Kluczowa reguła | Typ zależności |
|--------|-------------|-----------------|----------------|
| **1NF** | Nieatomowe wartości | Każda komórka = 1 wartość, jest klucz | — |
| **2NF** | Częściowe zależności | Atrybut wtórny zależy od CAŁEGO klucza | FD częściowa |
| **3NF** | Zależności przechodnie | Atrybut wtórny nie zależy od nie-klucza (z wyjątkiem prime) | FD przechodnia |
| **BCNF** | Determinanty nie-nadkluczowe | Lewa strona KAŻDEJ FD = nadklucz (bez wyjątków) | FD nietrywialna |
| **4NF** | Wielowartościowe zależności | Lewa strona każdej MVD = nadklucz | MVD |
| **5NF** | Zależności złączenia | Każda JD implikowana przez klucze | JD |

### Denormalizacja

Świadome wprowadzanie redundancji dla wydajności (mniej JOIN-ów). Stosowane w systemach analitycznych (OLAP), data warehousing.

### Etymologia

**Redundancja** — łac. „redundantia" = nadmiar/przelewanie się. **Normalizacja** — Edgar F. Codd (IBM, 1970, „A Relational Model of Data"); 1NF–3NF w oryginalnej pracy. **BCNF** — Raymond Boyce + Codd (1974). **4NF** — Ronald Fagin (1977). **5NF (PJNF)** — Ronald Fagin (1979); PJNF = Project-Join Normal Form. **Anomalia** — grec. „anomalia" = nieregularność. **„Klucz, cały klucz i tylko klucz"** — parafraza przysięgi sądowej; przypisywana Coddowi. **Zależność funkcyjna** — jak funkcja mat.: X jednoznacznie wyznacza Y. **MVD** — Multi-Valued Dependency; Fagin udowodnił, że 4NF eliminuje redundancje z MVD. **JD** — Join Dependency; Fagin udowodnił, że 5NF jest „ostateczną" postacią normalną dla relacyjnych baz danych.

### Jak zapamiętać

- **„Klucz, cały klucz i tylko klucz — tak mi dopomóż Codd"** — 1NF (klucz), 2NF (cały klucz), 3NF (tylko klucz)
- **3 anomalie:** Wstawianie, Usuwanie, Modyfikacja — „WUM"
- **3NF vs BCNF — jedno słowo różnicy: WYJĄTEK:**

    Obie reguły sprawdzają to samo — dla każdej nietrywialnej FD X → A:

    3NF:  X jest nadkluczem? → ✅  |  A jest prime? → ✅ (WYJĄTEK!)  |  żadne? → ❌
    BCNF: X jest nadkluczem? → ✅  |  nie jest?     → ❌ (BEZ wyjątków, kropka.)

    3NF  = „łagodny sędzia" — odpuści, jeśli zależny jest częścią klucza
    BCNF = „surowy sędzia" — lewa strona MUSI być nadkluczem, bez dyskusji

    Kiedy się RÓŻNIĄ? Tylko przy kluczach ZŁOŻONYCH z nakładającymi się FD:
    Zapisy(StID, KursID, Prowadzący) — klucz: (StID, KursID)
    FD: Prowadzący → KursID
    • Prowadzący to nadklucz? NIE → BCNF mówi ❌
    • KursID to prime (część klucza)? TAK → 3NF mówi ✅ (wyjątek!)
    → Tabela jest 3NF, ale NIE BCNF.

    Przy prostych (jednokolumnowych) kluczach 3NF = BCNF zawsze.
- **4NF:** Czy widzisz iloczyn kartezjański? Niezależne zbiory w jednej tabeli? → rozdziel!
- **5NF:** Czy tabela „rozpadalna" na 3+ części bezstratnie? Reguła cykliczna? → dekomponuj!
- **Hierarchia typów zależności:** FD (jedna wartość) → MVD (zbiór wartości) → JD (złączenie n tabel)
- **Praktyka:** 90% systemów normalizuje do 3NF/BCNF. 4NF/5NF = egzotyka, ale egzamin wymaga

