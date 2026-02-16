## PYTANIE 4: Baza danych jako fundament systemów (BD2)

**Dlaczego baza danych stanowi dobry fundament do budowy wielu systemów informatycznych?**

---

### Tło pojęciowe — słowniczek

**System informatyczny** — oprogramowanie realizujące jakąś funkcję: sklep internetowy, system bankowy, CRM, system rezerwacji. Każdy taki system potrzebuje PRZECHOWYWAĆ dane i OPEROWAĆ na nich. Baza danych daje gotowe, sprawdzone mechanizmy do tego — nie trzeba ich pisać od zera.

**Dlaczego DB to „dobry fundament"?** — Bez bazy danych każdy system musi SAM rozwiązywać: „co jeśli prąd padnie w trakcie zapisu?", „co jeśli dwóch użytkowników edytuje to samo?", „jak chronić dane?". Baza dostarcza to wszystko „z pudełka" → programista skupia się na logice biznesowej, nie na infrastrukturze.

---

**Transakcja** — logiczna jednostka pracy: zestaw operacji, które MUSZĄ wykonać się razem jako całość. Np. przelew bankowy = (1) odejmij 100 zł od Ani + (2) dodaj 100 zł Janowi. Nie może być tak, że tylko (1) się wykona, a (2) nie — pieniądze by „zniknęły".

**ACID** — cztery właściwości, które baza gwarantuje dla każdej transakcji:

**Atomicity (Atomowość)** — „albo cała, albo nic" (all-or-nothing). Jeśli COKOLWIEK w transakcji się nie powiedzie (błąd, crash, brak pamięci), WSZYSTKIE zmiany tej transakcji są cofane (rollback). Jakby nic się nie stało. Np. przelew: jeśli krok (2) się nie uda, krok (1) jest automatycznie cofany — saldo Ani wraca do stanu sprzed przelewu.

**Jak to odpowiada na pytanie:** Bez atomowości system bankowy mógłby tracić pieniądze przy każdym crashu. Baza gwarantuje, że KAŻDA operacja jest bezpieczna → solidny fundament.

**Consistency (Spójność)** — transakcja przeprowadza bazę ze SPÓJNEGO stanu w inny SPÓJNY stan. **Stan** = aktualna zawartość wszystkich tabel w bazie (wszystkie dane w danym momencie). **Spójny stan** = stan, w którym WSZYSTKIE reguły (constraints) są spełnione. Np. „saldo ≥ 0", „każde zamówienie ma klienta", „PESEL ma 11 cyfr". **Spójny → spójny** = transakcja NIE MOŻE zostawić bazy w stanie łamiącym reguły. Np. przelew: suma pieniędzy w systemie przed = suma po (nie da się „stworzyć" pieniędzy).

**Jak to odpowiada na pytanie:** Dane w systemie ZAWSZE mają sens. Nie będzie zamówienia bez klienta, produktu z ceną −5 zł, ani studenta z oceną 7.

**Isolation (Izolacja)** — równoległe (jednoczesne) transakcje nie widzą nawzajem swoich niedokończonych zmian. Każda transakcja „myśli", że jest jedyną operacją na bazie. Np. Ania przelewa 100 zł a Jan sprawdza saldo — Jan widzi ALBO stan przed przelewem, ALBO po, NIGDY stan pośredni (np. „Ania odjęła, ale Jan jeszcze nie dostał").

**Jak to odpowiada na pytanie:** System może obsługiwać TYSIĄCE użytkowników jednocześnie bez chaosu. Każdy widzi spójne dane.

**Durability (Trwałość)** — po zatwierdzeniu transakcji (COMMIT), jej efekty przetrwają KAŻDĄ awarię: crash serwera, awaria dysku, przerwa w zasilaniu. Baza zapisuje zmiany do trwałego magazynu (dysk, WAL — Write-Ahead Log). Nawet jeśli serwer padnie 1 ms po COMMIT, dane są bezpieczne.

**Jak to odpowiada na pytanie:** System nie traci danych. Klient płaci za zamówienie → zamówienie jest zapisane NA ZAWSZE, nawet jeśli serwer zaraz potem się wyłączy.

---

**ANSI** — American National Standards Institute: amerykańska organizacja normalizacyjna (odpowiednik polskiego PKN). Ustala standardy techniczne.

**SPARC** — Standards Planning And Requirements Committee: komitet przy ANSI, który w 1975 zaproponował 3-poziomową architekturę baz danych.

**3-poziomowa architektura ANSI/SPARC:**

    Poziom zewnętrzny  — CO widzi użytkownik/aplikacja (widoki, podzbiory danych)
    Poziom konceptualny — JAKA jest struktura danych (tabele, kolumny, relacje)
    Poziom wewnętrzny  — JAK dane są fizycznie przechowywane (pliki, indeksy, bloki)

Dzięki tym 3 poziomom zmiany na jednym poziomie NIE wymuszają zmian na innych.

**Niezależność fizyczna** — zmiana SPOSOBU przechowywania (np. dodanie indeksu, zmiana partycjonowania) nie wymaga zmiany aplikacji.

**Indeks (index)** — struktura pomocnicza przyspieszająca wyszukiwanie (jak indeks w książce — nie czytasz całej książki, szukasz po indeksie). Np. indeks na kolumnie „Nazwisko" pozwala szybko znaleźć studenta po nazwisku, bez przeszukiwania milionów wierszy. Dodanie/usunięcie indeksu NIE zmienia danych ani zapytań SQL — aplikacja działa tak samo, tylko szybciej.

**Partycjonowanie (partitioning)** — podział dużej tabeli na mniejsze kawałki (partycje). Np. tabela Zamówienia podzielona na partycje wg roku: 2024, 2025, 2026. Zapytanie o 2025 przeszukuje TYLKO tę partycję. Zmiana partycjonowania jest przezroczysta dla aplikacji.

**Niezależność logiczna** — zmiana struktury tabel minimalizuje wpływ na aplikacje. Np. rozdzielasz tabelę StudentKursy na Studenci + Zapisy, ale tworzysz **widok (view)** = „wirtualna tabela" symulująca starą strukturę. Aplikacja dalej pyta o ten sam widok — dla niej nic się nie zmieniło.

**Jak to odpowiada na pytanie:** System może EWOLUOWAĆ (rosnąć, zmieniać strukturę, optymalizować) BEZ przepisywania aplikacji. Baza oddziela „co" od „jak" → elastyczny fundament.

---

**Współbieżność (concurrency)** — wielu użytkowników/procesów operuje na bazie JEDNOCZEŚNIE. Np. 1000 osób kupuje bilety w tym samym momencie. Baza musi zapewnić, że nie sprzedadzą dwóch biletów na to samo miejsce.

**Blokady (locks)** — najprostszy mechanizm: transakcja „blokuje" wiersz/tabelę, inne muszą CZEKAĆ. Np. transakcja aktualizuje saldo Ani → saldo jest zablokowane → Jan nie może go modyfikować, czeka aż Ania skończy. Typy: shared lock (wiele odczytów jednocześnie) vs exclusive lock (tylko jedna transakcja pisze).

**MVCC (Multi-Version Concurrency Control)** — zamiast blokować, baza trzyma WIELE WERSJI danych. Transakcja czyta wersję z momentu swojego startu — nie jest blokowana przez zapis. Np. Jan czyta saldo (wersja sprzed przelewu), Ania jednocześnie przelewa (tworzy nową wersję). Nikt nie czeka!

**Snapshot Isolation** — wariant MVCC: każda transakcja widzi „migawkę" (snapshot) bazy z momentu swojego startu. Nawet jeśli inne transakcje zmieniają dane, ta widzi SPÓJNY obraz z przeszłości. Eliminuje większość problemów z współbieżnym czytaniem.

**Jak to odpowiada na pytanie:** Baza automatycznie zarządza dostępem wielu użytkowników → system może obsługiwać setki/tysiące jednoczesnych połączeń bez ręcznego pisania mechanizmów synchronizacji.

---

**Integralność (integrity)** — dane w bazie ZAWSZE spełniają zdefiniowane reguły. Baza SAMA pilnuje reguł — nie trzeba ich sprawdzać w kodzie aplikacji.

**Klucze obce (foreign keys, FK)** — wiersz w tabeli MUSI odnosić się do istniejącego wiersza w innej tabeli. Np. Zamówienia.KlientID MUSI wskazywać na istniejącego klienta w tabeli Klienci. Nie możesz wstawić zamówienia dla klienta „999" jeśli nie ma klienta o ID 999. NIE możesz usunąć klienta, który ma zamówienia.

**CHECK** — ograniczenie na wartości kolumny. Np. `CHECK (wiek >= 0 AND wiek <= 150)` — baza ODRZUCI próbę wstawienia osoby z wiekiem −5 lub 200. `CHECK (status IN ('aktywny', 'nieaktywny'))` — nie wpiszesz statusu „cokolwiek".

**Trigger (wyzwalacz)** — fragment kodu uruchamiany AUTOMATYCZNIE, gdy coś się dzieje w bazie. Np. `AFTER INSERT ON Zamówienia` → automatycznie zmniejsz stan magazynowy produktu. Trigger „pilnuje" reguł, których nie da się wyrazić samym CHECK-iem.

**Procedura składowana (stored procedure)** — funkcja zapisana W BAZIE (nie w aplikacji), wywoływana z SQL. Np. `CALL przelejPieniadze(101, 102, 500)` — cała logika przelewu w jednym miejscu, współdzielona przez wszystkie aplikacje.

**Jak to odpowiada na pytanie:** Reguły biznesowe (np. „nie sprzedawaj produktu z zerowym stanem") wymuszane PRZEZ bazę, nie PRZEZ aplikację → nawet jeśli ktoś napisze błędną aplikację, baza nie pozwoli złamać reguł.

---

**Optymalizator zapytań (query optimizer)** — moduł bazy, który automatycznie wybiera NAJSZYBSZY sposób wykonania zapytania SQL. Programista pisze CO chce (`SELECT ... WHERE ...`), a optymalizator decyduje JAK to zrobić (np. użyć indeksu czy przeszukać całą tabelę, w jakiej kolejności łączyć tabele). **Plan wykonania (execution plan)** — sekwencja kroków, którą baza wykona. Np. „użyj indeksu na Nazwisko → odfiltruj wiersze → posortuj".

**Jak to odpowiada na pytanie:** Programista nie musi znać struktury fizycznej danych. Pisze prosty SQL, a baza SAMA optymalizuje → szybkość „za darmo".

---

**Bezpieczeństwo (security):**

**GRANT/REVOKE** — polecenia SQL do nadawania/odbierania uprawnień. Np. `GRANT SELECT ON Studenci TO Dziekanat` — dziekanat może CZYTAĆ studentów, ale nie modyfikować. `REVOKE INSERT ON Zamówienia FROM Praktykant` — praktykant nie może dodawać zamówień.

**Role** — grupy uprawnień. Zamiast nadawać uprawnienia każdemu użytkownikowi osobno, tworzysz rolę (np. „Kasjer") i przypisujesz ją użytkownikom. Kasjer = SELECT + INSERT na Zamówienia, ale bez dostępu do tabeli Pracownicy.

**Szyfrowanie (encryption)** — dane na dysku i w transmisji zamienione na nieczytelny ciąg, który wymaga klucza do odszyfrowania. TDE (Transparent Data Encryption) = szyfrowanie „przezroczyste" — aplikacja nie wie, że dane są szyfrowane.

**Audyt (audit)** — baza rejestruje KTO, KIEDY, CO zrobił. Np. „użytkownik Kowalski zmodyfikował saldo klienta 123 o 15:42". Niezbędne dla zgodności z prawem (RODO, SOX, PCI-DSS).

**Jak to odpowiada na pytanie:** Baza chroni dane przez kontrolę dostępu, szyfrowanie i śledzenie zmian → fundament bezpieczeństwa systemu.

---

**Skalowalność (scalability)** — zdolność systemu do ROŚNIĘCIA (więcej danych, więcej użytkowników) bez utraty wydajności.

**Replikacja (replication)** — kopia bazy na wielu serwerach. Np. master (zapis) + 3 repliki (odczyt). 80% zapytań to odczyty → rozkładasz je na repliki. Jeśli master padnie, replika przejmuje rolę.

**Sharding (fragmentacja)** — podział danych na kawałki (shardy) na RÓŻNYCH serwerach. Np. klienci A–M na serwerze 1, N–Z na serwerze 2. Każdy serwer przechowuje i obsługuje MNIEJSZY zbiór danych → szybciej.

**Klaster (cluster)** — grupa serwerów pracujących RAZEM jako jeden system. Np. klaster PostgreSQL Citus albo MySQL NDB Cluster — z zewnątrz wygląda jak jedna baza, ale fizycznie to wiele maszyn.

**Jak to odpowiada na pytanie:** System może obsłużyć od 10 do 10 000 000 użytkowników bez zmiany architektury aplikacji → baza rośnie razem z systemem.

---

**SQL (Structured Query Language)** — standardowy język zapytań do baz relacyjnych. TEN SAM SQL działa (z drobnymi różnicami) w PostgreSQL, MySQL, Oracle, SQL Server, SQLite. Programista, który zna SQL, może pracować z KAŻDĄ z tych baz.

**Jak to odpowiada na pytanie:** Jeden uniwersalny interfejs → łatwość wymiany bazy danych, łatwe znalezienie programistów, bogactwo narzędzi, ORM-ów i bibliotek. Nie trzeba uczyć się osobnego języka dla każdego systemu.

---

### 1. Transakcyjność ACID

| Właściwość | Znaczenie |
|------------|-----------|
| **A**tomicity | Transakcja — albo cała, albo nic |
| **C**onsistency | Spójny stan → spójny stan |
| **I**solation | Równoległe transakcje nie interferują |
| **D**urability | Zatwierdzone zmiany przetrwają awarię |

### 2. Niezależność danych (3-poziomowa architektura ANSI/SPARC)

- **Fizyczna:** zmiana indeksów/partycjonowania nie wpływa na aplikacje
- **Logiczna:** zmiana schematu minimalizuje wpływ na aplikacje (widoki)

### 3. Współbieżność — mechanizmy: blokady, MVCC, snapshot isolation

### 4. Integralność — klucze obce, CHECK, triggery, procedury składowane

### 5. Optymalizator zapytań — automatyczny wybór planu wykonania

### 6. Bezpieczeństwo — GRANT/REVOKE, role, szyfrowanie, audyt

### 7. Skalowalność — replikacja, sharding, klastry

### 8. Standardowy interfejs — SQL jako uniwersalny język zapytań

### Etymologia

**ACID** — akronim: Reuter & Härder (1983); celowo łatwy do zapamiętania. **ANSI/SPARC** — American National Standards Institute / Standards Planning And Requirements Committee (1975). **SQL** — oryginalnie SEQUEL (Structured English Query Language, Chamberlin & Boyce, IBM 1974); zmieniono na SQL przez konflikt znaku towarowego. **MVCC** — Multi-Version Concurrency Control. **Transakcja** — łac. „transactio" = doprowadzenie do końca.

### Jak zapamiętać

- **ACID** — zapamiętaj przelew bankowy: bez A tracisz pieniądze, bez C saldo < 0, bez I widać stan pośredni, bez D znika po crashu
- **„DB = centralne źródło prawdy"** — jedna baza vs. pliki rozproszone po systemach
- Kluczowe słowa: trwałość, współbieżność, integralność, niezależność

