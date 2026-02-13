# Plan nauki — Obrona magisterska (1 marca 2026)

> **Start:** 14 lutego (sobota) | **Obrona:** 1 marca (niedziela)
> **Dni nauki:** 15 (Feb 14–28) | **Pytań:** 28
> **Szacowany całkowity czas nauki:** ~63h

---

## Harmonogram tygodnia i dostępny czas

| Dzień        | Tryb pracy   | Czas na naukę                                     |
|--------------|-------------|----------------------------------------------------|
| **Poniedziałek** | Zdalnie  | ~3h wieczorem po pracy                             |
| **Wtorek**       | Biuro    | 2h dojazd (transport publiczny → Anki/czytanie) + 1.5h wieczór |
| **Środa**        | Biuro    | 2h dojazd + 1.5h wieczór                          |
| **Czwartek**     | Zdalnie  | ~3h wieczorem po pracy                             |
| **Piątek**       | Biuro    | 2h dojazd + 1.5h wieczór                          |
| **Sob/Niedz**    | Wolne    | ~6h solidnej nauki                                 |

---

## Budżet czasu

| Typ dnia           | Dni  | h/dzień | Suma  |
|--------------------|------|---------|-------|
| Weekend            | 5    | 6h      | 30h   |
| Praca zdalna       | 4    | 3h      | 12h   |
| Praca biuro        | 6    | 3.5h    | 21h   |
| **RAZEM**          | **15** |       | **63h** |

Podział: ~40h na 1. przejście (nauka) + ~17h na powtórkę + ~6h na mock defense.

---

## Rozkład pytań wg trudności

### Ciężkie (200+ linii, dużo teorii)
- **Q5** STL categories (325 linii) — najdłuższe pytanie
- **Q2** Shortest paths (225 linii) — trzy algorytmy + pseudokod

### Średnio-ciężkie (140-180 linii)
- Q3 Normalizacja (176), Q4 Bazy danych (162), Q9 Procesy/wątki (160)
- Q6 OOP reuse (151), Q31 Decyzje pod ryzykiem (146), Q32 Dominacja stochastyczna (168)
- Q1 Automaty (138), Q26 Sync/async (135)

### Średnie (100-130 linii)
- Q8 TCP (103), Q10 Pamięć (127), Q11 Procesy biznesowe (111), Q12 Optymalizacja (99)
- Q14/28 Wzorce (102), Q15 Robotyka (119), Q16 Języki robotów (103), Q17 Szeregowanie (112)
- Q18 Zapasy (127), Q19/29 Pub-Sub (120), Q20/30 Streaming (122)
- Q21 Zegary logiczne (128), Q22 Spójność (112), Q23 Segmentacja (122)
- Q24 Detekcja (128), Q25 Amdahl (123)

### Lekkie (<100 linii)
- **Q7** DNS & caching (88) — najkrótsze
- **Q13/27** Arch. systemów (93), **Q12** Optymalizacja sieciowa (99)

---

## FAZA 1: Pierwsze przejście — nauka i zrozumienie (Feb 14–22)

Cel: przeczytać i zrozumieć każde pytanie, zanotować kluczowe koncepty.

### Dzień 1 — Sobota 14.02 (6h) 🏠
**Temat: Algorytmy i Teoria (AISDI)**

| Czas | Pytanie | Co zrobić |
|------|---------|-----------|
| 09:00–11:00 (2h) | **Q1** Automaty i klasy języków | Hierarchia Chomsky'ego, tabela FA/PDA/LBA/TM, kontrprzykłady |
| 11:15–13:45 (2.5h) | **Q2** Algorytmy najkrótszej ścieżki | Dijkstra/BF/A* — pseudokod, złożoności, tabela porównawcza |
| 14:30–16:00 (1.5h) | **Q5** (część 1) Kategorie STL | Kontenery sekwencyjne i asocjacyjne (połowa pytania) |

**Metoda:** Czytaj aktywnie — po każdej sekcji zamknij oczy i opowiedz sobie kluczowe punkty.

---

### Dzień 2 — Niedziela 15.02 (6h) 🏠
**Temat: Programowanie + Bazy danych (PROI + BD2)**

| Czas | Pytanie | Co zrobić |
|------|---------|-----------|
| 09:00–10:30 (1.5h) | **Q5** (część 2) Kategorie STL | Adaptery, iteratory, algorytmy, funktory |
| 10:45–12:15 (1.5h) | **Q6** Reużywalność kodu OOP | Dziedziczenie vs kompozycja, wzorce, SOLID |
| 13:00–14:30 (1.5h) | **Q3** Redundancja i normalizacja | 1NF→BCNF, anomalie, zależności funkcyjne |
| 14:45–16:15 (1.5h) | **Q4** Baza danych jako fundament | ACID, transakcje, indeksy, architektura |

**Wieczór:** 20 min — szybkie powtórzenie głównych tabel z Q1-Q6.

---

### Dzień 3 — Poniedziałek 16.02 (3h) 💻 zdalnie
**Temat: Sieci + Systemy operacyjne (SKM + SOI)**

| Czas | Pytanie | Co zrobić |
|------|---------|-----------|
| 19:00–19:50 (50min) | **Q7** DNS i caching | Hierarchia DNS, typy rekordów, cache TTL |
| 20:00–20:50 (50min) | **Q8** TCP Three-Way Handshake | SYN/SYN-ACK/ACK, stany połączenia, flagi |
| 21:00–22:00 (1h) | **Q9** Procesy i wątki | Stany procesów, różnice procesu vs wątek, synchronizacja |

---

### Dzień 4 — Wtorek 17.02 (3.5h) 🏢 biuro
**Temat: Systemy operacyjne + Zarządzanie (SOI + WSYZ)**

| Kiedy | Pytanie | Co zrobić |
|-------|---------|-----------|
| 🚌 Dojazd tam (1h) | Powtórka Q1–Q4 | Czytaj podsumowania i tabele na telefonie |
| 🚌 Dojazd powrót (1h) | Powtórka Q5–Q9 | Anki flashcards + kluczowe schematy |
| 🌙 Wieczór (1.5h) | **Q10** Zarządzanie pamięcią | Stronicowanie, segmentacja, pamięć wirtualna, TLB |

---

### Dzień 5 — Środa 18.02 (3.5h) 🏢 biuro
**Temat: Zarządzanie + Architektura (WSYZ + AIS)**

| Kiedy | Pytanie | Co zrobić |
|-------|---------|-----------|
| 🚌 Dojazd (2h) | Powtórka Q7–Q10 | Skupienie na słabszych punktach z wczoraj |
| 🌙 Wieczór (1.5h) | **Q11** Modelowanie procesów biznesowych + **Q12** Optymalizacja sieciowa | BPMN elementy, problem transportowy, simpleks |

---

### Dzień 6 — Czwartek 19.02 (3h) 💻 zdalnie
**Temat: Architektura + Robotyka (AIS + Robotyka)**

| Czas | Pytanie | Co zrobić |
|------|---------|-----------|
| 19:00–19:50 (50min) | **Q13/27** Modelowanie architektury SI | UML, 4+1, diagramy komponentów/wdrożeń |
| 20:00–20:50 (50min) | **Q14/28** Wzorce architektoniczne | MVC, mikrousługi, CQRS, event-driven |
| 21:00–22:00 (1h) | **Q15** Agent upostaciowiony | Sense-plan-act, zachowania reaktywne, robotyka kognitywna |

---

### Dzień 7 — Piątek 20.02 (3.5h) 🏢 biuro
**Temat: Robotyka + Scheduling**

| Kiedy | Pytanie | Co zrobić |
|-------|---------|-----------|
| 🚌 Dojazd (2h) | Powtórka Q10–Q15 | Anki + szybkie streszczenia na telefonie |
| 🌙 Wieczór (1.5h) | **Q16** Języki programowania robotów + **Q17** Szeregowanie zadań | ROS, C++/Python w robotyce; EDF, RM, Gantt |

---

### Dzień 8 — Sobota 21.02 (6h) 🏠
**Temat: Supply chain + Messaging + Systemy rozproszone**

| Czas | Pytanie | Co zrobić |
|------|---------|-----------|
| 09:00–10:15 (1.25h) | **Q18** Zarządzanie zapasami | EOQ, punkt zamawiania, model newsvendor |
| 10:30–11:30 (1h) | **Q19/29** Model Publish-Subscribe | Broker, topic vs content-based, przykłady (Kafka/MQTT) |
| 11:45–12:45 (1h) | **Q20/30** Analityka strumieniowa | Okna czasowe, CEP, Storm/Flink/Spark Streaming |
| 13:30–14:45 (1.25h) | **Q21** Zegary logiczne | Lamport, zegary wektorowe, happened-before |
| 15:00–16:15 (1.25h) | **Q22** Modele spójności danych | Silna/eventual/causal consistency, CAP theorem |

**Wieczór:** 15 min podsumowanie — narysuj mapę myśli łączącą Q18-Q22.

---

### Dzień 9 — Niedziela 22.02 (6h) 🏠
**Temat: Wizja komputerowa + Równoległość + Decyzje (KOŃCZYMY FAZĘ 1!)**

| Czas | Pytanie | Co zrobić |
|------|---------|-----------|
| 09:00–10:00 (1h) | **Q23** Segmentacja obrazu | Progowanie, region growing, k-means, watershed |
| 10:15–11:15 (1h) | **Q24** Detekcja obiektów | YOLO, R-CNN, SSD, mAP, IoU |
| 11:30–12:30 (1h) | **Q25** Prawo Amdahla | Wzór, ograniczenia części sekwencyjnej, strong/weak scaling |
| 13:15–14:15 (1h) | **Q26** Komunikacja sync/async | Blokująca/nieblokująca, MPI, async/await |
| 14:30–15:30 (1h) | **Q31** Wspomaganie decyzji | Drzewa decyzyjne, macierz wypłat, EMV, EVPI |
| 15:45–16:45 (1h) | **Q32** Dominacja stochastyczna | FSD, SSD, wykres CDF, porównanie z E[X] |

**✅ Koniec Fazy 1 — wszystkie 28 pytań przeczytane i zrozumiane!**

---

## FAZA 2: Aktywne powtarzanie i utrwalanie (Feb 23–27)

Cel: przejść od biernego czytania do aktywnego wydobywania z pamięci. **Metoda Feynmana** — wytłumacz każde pytanie jak 5-latkowi (po polsku, na głos).

### Dzień 10 — Poniedziałek 23.02 (3h) 💻 zdalnie
**Powtórka: AISDI + BD2 + PROI (Q1–Q6)**

| Czas | Aktywność |
|------|-----------|
| 19:00–20:00 | Q1+Q2: Narysuj od zera hierarchię Chomsky'ego + tabelę Dijkstra/BF/A* z pamięci |
| 20:15–21:15 | Q3+Q4: Przeprowadź normalizację przykładowej tabeli na kartce; wypisz ACID |
| 21:15–22:00 | Q5+Q6: Wymień kategorie STL + po 2 przykłady; narysuj diagram dziedziczenie vs kompozycja |

**Samoocena:** Oceń każde pytanie 🟢 (umiem) / 🟡 (częściowo) / 🔴 (słabo). Zanotuj 🔴.

---

### Dzień 11 — Wtorek 24.02 (3.5h) 🏢 biuro
**Powtórka: SKM + SOI + WSYZ (Q7–Q12)**

| Kiedy | Aktywność |
|-------|-----------|
| 🚌 Dojazd (2h) | Anki flashcards — pula Q1-Q12. Skup się na 🔴 z wczoraj |
| 🌙 Wieczór (1.5h) | Q7–Q12 aktywne powtórzenie: bez notatek opowiedz TCP handshake, narysuj stany procesów, wymień formy normalne |

---

### Dzień 12 — Środa 25.02 (3.5h) 🏢 biuro
**Powtórka: AIS + Robotyka + Scheduling (Q13–Q18)**

| Kiedy | Aktywność |
|-------|-----------|
| 🚌 Dojazd (2h) | Anki — pula Q7-Q18. Ćwicz kluczowe tabele, wzory, schematy |
| 🌙 Wieczór (1.5h) | Q13–Q18 aktywne: Narysuj diagram UML 4+1, wypisz wzorce architektoniczne, EOQ wzór z pamięci |

---

### Dzień 13 — Czwartek 26.02 (3h) 💻 zdalnie
**Powtórka: Messaging + Rozproszone + Wizja (Q19–Q26)**

| Czas | Aktywność |
|------|-----------|
| 19:00–20:00 | Q19–Q22: Pub-Sub diagram z pamięci, CEP przykład, zegar Lamporta step-by-step, CAP theorem |
| 20:15–21:15 | Q23–Q26: Wymień metody segmentacji, narysuj pipeline YOLO, zapisz wzór Amdahla i oblicz przykład |
| 21:15–22:00 | Przejrzyj WSZYSTKIE notatki 🔴 ze wcześniejszych dni. Skoncentruj się na słabych punktach |

---

### Dzień 14 — Piątek 27.02 (3.5h) 🏢 biuro
**Powtórka: Decyzje + NAJTRUDNIEJSZE pytania**

| Kiedy | Aktywność |
|-------|-----------|
| 🚌 Dojazd (2h) | Anki — PEŁNA PULA wszystkie 28 pytań. Ostatni dojazd — skup się na tym, co wciąż trudne |
| 🌙 Wieczór (1.5h) | Q31+Q32 aktywne + **ponowna powtórka 5 najtrudniejszych pytań** (na podstawie samooceny 🔴/🟡) |

---

## FAZA 3: Symulacja obrony (Feb 28)

### Dzień 15 — Sobota 28.02 (6h) 🏠
**MOCK DEFENSE + ostatnie szlify**

| Czas | Aktywność |
|------|-----------|
| 09:00–10:30 (1.5h) | **Mock #1:** Wylosuj 3 pytania (np. dice online). Odpowiedz na głos, max 5 min/pytanie. Nagraj się telefonem |
| 10:45–11:45 (1h) | Odsłuchaj nagranie. Zanotuj: co było niejasne? co pominąłeś? |
| 12:30–14:00 (1.5h) | **Mock #2:** Wylosuj kolejne 3 pytania. Spróbuj odpowiedzieć BEZ notatek |
| 14:15–15:15 (1h) | Przeczytaj odpowiedzi do pytań, z którymi miałeś problem. Uzupełnij luki |
| 15:30–16:30 (1h) | **Speed round:** Przejdź przez WSZYSTKIE 28 pytań — 2 min na pytanie, powiedz esencję (kluczowe 3 punkty) |

**Wieczór:** ODPOCZYNEK. Żadnej nauki po 18:00. Dobry sen.

---

## Niedziela 1.03 — DZIEŃ OBRONY 🎓

- Rano: lekkie przeglądnięcie tabel porównawczych (15 min max)
- **NIE** ucz się niczego nowego
- Zjedz dobry posiłek, przyjdź wcześniej

---

## Techniki nauki — podsumowanie

| Technika | Kiedy | Jak |
|----------|-------|-----|
| **Aktywne czytanie** | Faza 1 | Po każdej sekcji: zamknij dokument, opowiedz kluczowe punkty |
| **Anki flashcards** | Dojazdy + codziennie | Użyj istniejących plików `anki_*.txt` z katalogu `pytania/` |
| **Metoda Feynmana** | Faza 2 | Wytłumacz pytanie prostymi słowami, na głos |
| **Samoocena 🟢🟡🔴** | Po każdej sesji | Zaznacz co umiesz, wróć do 🔴 następnego dnia |
| **Mock defense** | Faza 3 | Losuj pytania, odpowiadaj na czas, nagrywaj się |
| **Spaced repetition** | Cały czas | Wracaj do wcześniejszych pytań w dojazdach |

---

## Materiały dodatkowe w repozytorium

- `pytania/anki_atomic.txt` — fiszki Anki (atomowe)
- `pytania/anki_egzamin_magisterski.txt` — fiszki z zakresu egzaminu
- `pytania/OBRONA_SKRYPT_MOWIONY.md` — skrypt do przećwiczenia mówienia
- `pytania/odpowiedzi/` — dodatkowe materiały

---

## Quick reference — grupowanie tematyczne

| # | Pytanie | Przedmiot | Para |
|---|---------|-----------|------|
| 1 | Automaty i klasy języków | AISDI | 1+2 |
| 2 | Algorytmy najkrótszej ścieżki | AISDI | 1+2 |
| 3 | Redundancja i normalizacja | BD2 | 3+4 |
| 4 | Baza danych jako fundament | BD2 | 3+4 |
| 5 | Kategorie STL | PROI | 5+6 |
| 6 | Reużywalność kodu OOP | PROI | 5+6 |
| 7 | DNS i caching | SKM | 7+8 |
| 8 | TCP Three-Way Handshake | SKM | 7+8 |
| 9 | Procesy i wątki | SOI | 9+10 |
| 10 | Zarządzanie pamięcią | SOI | 9+10 |
| 11 | Modelowanie procesów biznesowych | WSYZ | 11+12 |
| 12 | Sieciowe modele optymalizacji | WSYZ | 11+12 |
| 13/27 | Modelowanie architektury SI | AIS | 13+14 |
| 14/28 | Wzorce architektoniczne | AIS | 13+14 |
| 15 | Agent upostaciowiony | Robotyka | 15+16 |
| 16 | Języki programowania robotów | Robotyka | 15+16 |
| 17 | Szeregowanie zadań | Scheduling | 17+18 |
| 18 | Zarządzanie zapasami | Supply chain | 17+18 |
| 19/29 | Model Publish-Subscribe | Messaging | 19+20 |
| 20/30 | Analityka strumieniowa | Streaming | 19+20 |
| 21 | Zegary logiczne | Rozproszone | 21+22 |
| 22 | Modele spójności danych | Rozproszone | 21+22 |
| 23 | Segmentacja obrazu | Wizja | 23+24 |
| 24 | Detekcja obiektów | Wizja | 23+24 |
| 25 | Prawo Amdahla | Równoległość | 25+26 |
| 26 | Komunikacja sync/async | Komunikacja | 25+26 |
| 31 | Wspomaganie decyzji pod ryzykiem | Decyzje | 31+32 |
| 32 | Dominacja stochastyczna | Decyzje | 31+32 |

---

## Tracker codzienny

Kopiuj do notatnika i zaznaczaj codziennie:

```
[ ] Feb 14 (Sob) — Q1, Q2, Q5(1/2)
[ ] Feb 15 (Nie) — Q5(2/2), Q6, Q3, Q4
[ ] Feb 16 (Pon) — Q7, Q8, Q9
[ ] Feb 17 (Wto) — powtórka dojazd + Q10
[ ] Feb 18 (Śro) — powtórka dojazd + Q11, Q12
[ ] Feb 19 (Czw) — Q13/27, Q14/28, Q15
[ ] Feb 20 (Pią) — powtórka dojazd + Q16, Q17
[ ] Feb 21 (Sob) — Q18, Q19/29, Q20/30, Q21, Q22
[ ] Feb 22 (Nie) — Q23, Q24, Q25, Q26, Q31, Q32 ✅ FAZA 1 DONE
[ ] Feb 23 (Pon) — recall Q1-Q6
[ ] Feb 24 (Wto) — recall Q7-Q12
[ ] Feb 25 (Śro) — recall Q13-Q18
[ ] Feb 26 (Czw) — recall Q19-Q26
[ ] Feb 27 (Pią) — recall Q31-Q32 + 5 najtrudniejszych
[ ] Feb 28 (Sob) — MOCK DEFENSE x2 + speed round
--- Mar 1 (Nie) — 🎓 OBRONA ---
```
