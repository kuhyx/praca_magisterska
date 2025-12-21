# Pytanie 8: TCP Three-Way Handshake

## Pytanie
**"Jaki jest cel uzgadniania trójetapowego (three way handshake) w protokole TCP? Jaka jest interpretacja numerów sekwencyjnych i potwierdzenia? Jaka jest wartość początkowa numeru sekwencyjnego?"**

Przedmiot: SKM (Sieci Komputerowe)

---

## 📚 Odpowiedź główna

### Wprowadzenie do TCP

**TCP (Transmission Control Protocol)** to protokół warstwy transportowej zapewniający:
- Niezawodne dostarczanie danych
- Kontrolę przepływu
- Kontrolę przeciążenia
- Połączeniowość (connection-oriented)

---

## 1. Three-Way Handshake - cel i przebieg

### Cele uzgadniania trójetapowego

1. **Nawiązanie połączenia** - obie strony zgadzają się na komunikację
2. **Synchronizacja numerów sekwencyjnych** - ISN (Initial Sequence Number)
3. **Uzgodnienie parametrów** - MSS, Window Scale, SACK, Timestamps
4. **Weryfikacja dostępności** - obie strony są aktywne i gotowe

### Przebieg (diagram)

```
    Klient                                      Serwer
      │                                           │
      │  (1) SYN, seq=x                           │
      │──────────────────────────────────────────→│
      │                                           │
      │  (2) SYN+ACK, seq=y, ack=x+1              │
      │←──────────────────────────────────────────│
      │                                           │
      │  (3) ACK, seq=x+1, ack=y+1                │
      │──────────────────────────────────────────→│
      │                                           │
      │         [POŁĄCZENIE NAWIĄZANE]            │
      │                                           │
```

### Szczegółowy opis kroków

#### Krok 1: SYN (Synchronize)
```
Klient → Serwer:
┌────────────────────────────────────────┐
│ Flaga: SYN = 1                         │
│ Sequence Number: x (ISN klienta)       │
│ Acknowledgment Number: 0 (nieistotny)  │
│ Opcje: MSS, Window Scale, SACK, etc.   │
└────────────────────────────────────────┘
```
- Klient inicjuje połączenie
- Wysyła swój ISN (Initial Sequence Number)
- Stan klienta: SYN_SENT

#### Krok 2: SYN-ACK (Synchronize-Acknowledge)
```
Serwer → Klient:
┌────────────────────────────────────────┐
│ Flagi: SYN = 1, ACK = 1                │
│ Sequence Number: y (ISN serwera)       │
│ Acknowledgment Number: x + 1           │
│ Opcje: MSS, Window Scale, etc.         │
└────────────────────────────────────────┘
```
- Serwer potwierdza otrzymanie SYN (ACK = x+1)
- Serwer wysyła swój ISN
- Stan serwera: SYN_RECEIVED

#### Krok 3: ACK (Acknowledge)
```
Klient → Serwer:
┌────────────────────────────────────────┐
│ Flaga: ACK = 1                         │
│ Sequence Number: x + 1                 │
│ Acknowledgment Number: y + 1           │
└────────────────────────────────────────┘
```
- Klient potwierdza otrzymanie SYN serwera
- Połączenie nawiązane (ESTABLISHED)
- Może zawierać już dane (TCP Fast Open)

---

## 2. Numery sekwencyjne (Sequence Numbers)

### Interpretacja

**Sequence Number (SEQ)** = numer pierwszego bajtu danych w segmencie

```
Strumień danych:
Bajty: [0][1][2][3][4][5][6][7][8][9][10][11][12]...

Segment 1: SEQ=0,  dane = bajty 0-4    (5 bajtów)
Segment 2: SEQ=5,  dane = bajty 5-9    (5 bajtów)  
Segment 3: SEQ=10, dane = bajty 10-12  (3 bajty)
```

### Funkcje numerów sekwencyjnych

| Funkcja | Opis |
|---------|------|
| **Kolejność** | Odbiorca składa segmenty we właściwej kolejności |
| **Wykrywanie duplikatów** | Ten sam SEQ = duplikat |
| **Wykrywanie braków** | Luka w SEQ = brakujący segment |
| **Potwierdzanie** | ACK wskazuje oczekiwany następny SEQ |

### Przykład transmisji

```
Klient (ISN=1000)                    Serwer (ISN=5000)
    │                                     │
    │  SEQ=1000, "Hello" (5 bytes)        │
    │────────────────────────────────────→│
    │                                     │
    │  SEQ=5000, ACK=1005, "Hi" (2 bytes) │
    │←────────────────────────────────────│
    │                                     │
    │  SEQ=1005, ACK=5002, "World" (5 b)  │
    │────────────────────────────────────→│
    │                                     │
```

---

## 3. Numery potwierdzenia (Acknowledgment Numbers)

### Interpretacja

**Acknowledgment Number (ACK)** = numer **następnego oczekiwanego** bajtu

```
ACK = ostatni_otrzymany_SEQ + liczba_otrzymanych_bajtów
```

### Kumulatywne potwierdzenia

TCP używa **cumulative ACK** - potwierdza wszystkie bajty do danego numeru:

```
Otrzymano: SEQ=100 (10 bajtów), SEQ=110 (10 bajtów)
ACK = 120 (potwierdza bajty 100-119)

Otrzymano: SEQ=100 (10 bajtów), BRAK SEQ=110, SEQ=120 (10 bajtów)
ACK = 110 (nie można potwierdzić 120, bo brakuje 110-119!)
```

### Selective ACK (SACK)

Opcja TCP pozwalająca potwierdzać niesąsiednie bloki:

```
Otrzymano: SEQ=100, BRAK SEQ=110, SEQ=120
ACK = 110
SACK: [120-130]  ← "mam też te bajty"
```

---

## 4. Wartość początkowa numeru sekwencyjnego (ISN)

### Dlaczego ISN nie zaczyna od 0?

1. **Bezpieczeństwo** - przewidywalny ISN umożliwia ataki (TCP hijacking)
2. **Unikanie kolizji** - stare segmenty z poprzednich połączeń nie będą mylone z nowymi

### Generowanie ISN

#### Historycznie (RFC 793):
```
ISN = (4 mikrosekundy timer) mod 2^32
```
Zwiększany o 1 co 4μs → pełny cykl co ~4.55 godziny

#### Współcześnie (RFC 6528):
```
ISN = M + F(localhost, localport, remotehost, remoteport, secretkey)
```
Gdzie:
- **M** = timer (jak wyżej)
- **F** = funkcja kryptograficzna (MD5/SHA)
- **secretkey** = tajny klucz serwera

### Właściwości dobrego ISN

| Właściwość | Powód |
|------------|-------|
| **Losowy** | Utrudnia ataki typu sequence prediction |
| **Unikalny** | Różny dla każdego połączenia |
| **Monotonicznie rosnący** | Unikanie kolizji z poprzednimi połączeniami |

### Zakres numerów sekwencyjnych

```
SEQ: 32 bity → zakres 0 do 4,294,967,295 (2^32 - 1)

Przy szybkości 1 Gbps:
- 125 MB/s danych
- Przepełnienie (wrap-around) co ~34 sekundy!

Rozwiązanie: PAWS (Protection Against Wrapped Sequences)
- Używa opcji Timestamp do rozróżniania "starych" i "nowych" numerów
```

---

## 5. Stany połączenia TCP

```
                              ┌─────────────┐
                    ┌────────→│   CLOSED    │←────────┐
                    │         └─────────────┘         │
                    │               │                 │
               (timeout)      (passive open)     (active open)
                    │               ↓                 │
                    │         ┌─────────────┐        │
                    │         │   LISTEN    │        │
                    │         └─────────────┘        │
                    │               │                 │
                    │          (recv SYN)        (send SYN)
                    │               ↓                 ↓
              ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
              │  TIME_WAIT  │  │ SYN_RECEIVED│  │  SYN_SENT   │
              └─────────────┘  └─────────────┘  └─────────────┘
                    ↑               │                 │
               (recv FIN+ACK)  (send SYN+ACK)    (recv SYN+ACK)
                    │               ↓                 ↓
              ┌─────────────┐  ┌─────────────────────────────┐
              │  FIN_WAIT_2 │  │        ESTABLISHED          │
              └─────────────┘  └─────────────────────────────┘
```

---

## 6. Zamykanie połączenia (Four-Way Handshake)

```
    Klient                                      Serwer
      │                                           │
      │  (1) FIN, seq=u                           │
      │──────────────────────────────────────────→│
      │                                           │
      │  (2) ACK, ack=u+1                         │
      │←──────────────────────────────────────────│
      │                                           │
      │  (serwer może jeszcze wysyłać dane)       │
      │                                           │
      │  (3) FIN, seq=v                           │
      │←──────────────────────────────────────────│
      │                                           │
      │  (4) ACK, ack=v+1                         │
      │──────────────────────────────────────────→│
      │                                           │
      │  [TIME_WAIT: 2×MSL]                       │
      │                                           │
```

**MSL (Maximum Segment Lifetime)** = maksymalny czas życia segmentu (~2 minuty)
**TIME_WAIT = 2×MSL** = ~4 minuty (oczekiwanie na zagubione segmenty)

---

## 📊 Podsumowanie Three-Way Handshake

| Krok | Kierunek | Flagi | SEQ | ACK | Cel |
|------|----------|-------|-----|-----|-----|
| 1 | C→S | SYN | x | - | Inicjacja, ISN klienta |
| 2 | S→C | SYN+ACK | y | x+1 | Akceptacja, ISN serwera |
| 3 | C→S | ACK | x+1 | y+1 | Potwierdzenie, połączenie gotowe |

---

## 🧠 Mnemoniki

### "SYN-SYN/ACK-ACK" - trzy kroki:
- **SYN** - "Chcę rozmawiać" (klient)
- **SYN/ACK** - "OK, ja też" (serwer)
- **ACK** - "Super, zaczynamy" (klient)

### "SEQ = Sent, ACK = Expected":
- **SEQ**uence = numer wysyłanego bajtu
- **ACK**nowledgment = numer oczekiwanego bajtu

### "ISN = Initial Secret Number":
- **I**nitial - początkowy
- **S**ecret - losowy dla bezpieczeństwa
- **N**umber - 32-bitowa liczba

### "ESTABLISHED po trzech krokach":
- 1: SYN_SENT
- 2: SYN_RECEIVED  
- 3: **ESTABLISHED** (obie strony)

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Dlaczego trzy kroki, nie dwa?"

**Odpowiedź:**

Dwa kroki nie wystarczą do synchronizacji **obu** ISN:

```
Dwa kroki (hipotetycznie):
Klient: SYN, seq=x          → Serwer zna ISN klienta
Serwer: SYN+ACK, seq=y      → Klient zna ISN serwera
                            → Ale serwer NIE WIE, czy klient otrzymał y!

Trzy kroki:
Klient: SYN, seq=x          → Serwer zna ISN klienta
Serwer: SYN+ACK, seq=y      → Klient zna ISN serwera
Klient: ACK, ack=y+1        → Serwer WIE, że klient otrzymał y ✓
```

---

### Q2: "Co to jest SYN flood attack?"

**Odpowiedź:**

**SYN flood** = atak DoS wysyłający masę SYN bez dokończenia handshake'a.

```
Atakujący: SYN, SYN, SYN, SYN... (tysiące)
Serwer: SYN+ACK, SYN+ACK...     (czeka na ACK)
        → Kolejka half-open connections pełna
        → Serwer nie może przyjąć nowych połączeń
```

**Obrona:**
- **SYN cookies** - serwer nie przechowuje stanu, koduje go w ISN
- **Zwiększenie kolejki SYN**
- **Zmniejszenie timeout SYN_RECEIVED**
- **Firewall/IDS**

---

### Q3: "Co to jest TCP Fast Open (TFO)?"

**Odpowiedź:**

**TFO** pozwala wysyłać dane już w pierwszym SYN (0-RTT):

```
Standardowo:         TFO:
SYN         →        SYN + dane     →
     ← SYN+ACK            ← SYN+ACK + dane
ACK + dane  →        ACK            →

3 RTT do danych      1 RTT do danych!
```

**Wymaga:** Cookie TFO z poprzedniego połączenia (uzyskany przy pierwszym handshake).

---

### Q4: "Jak działa retransmisja w TCP?"

**Odpowiedź:**

1. **Timeout (RTO):** Brak ACK w określonym czasie → retransmisja
2. **Fast Retransmit:** 3 duplikaty ACK → retransmisja bez czekania na timeout

```
Wysłano: SEQ=100, SEQ=200, SEQ=300
Zgubiono: SEQ=200

Odbiorca: ACK=200, ACK=200, ACK=200 (3× duplikat)
Nadawca: "Ah, brakuje 200!" → retransmisja SEQ=200
```

---

### Q5: "Co oznacza flaga RST?"

**Odpowiedź:**

**RST (Reset)** = natychmiastowe przerwanie połączenia.

**Kiedy wysyłane:**
- Segment do zamkniętego portu
- Segment do nieistniejącego połączenia
- Połączenie w nieprawidłowym stanie
- Aplikacja chce natychmiast zamknąć (bez FIN handshake)

```
RST nie wymaga potwierdzenia - połączenie natychmiast zamknięte.
```

---

### Q6: "Wyjaśnij opcje negocjowane podczas handshake"

**Odpowiedź:**

| Opcja | Opis | Wartość typowa |
|-------|------|----------------|
| **MSS** | Maximum Segment Size | 1460 (Ethernet) |
| **Window Scale** | Mnożnik okna (>65535) | 0-14 (×2^n) |
| **SACK Permitted** | Selective ACK dozwolone | tak/nie |
| **Timestamp** | Pomiar RTT, PAWS | 32-bit timer |
| **NOP** | Padding | - |

---

## 🎯 Kluczowe punkty do zapamiętania

1. **3 kroki:** SYN → SYN+ACK → ACK
2. **SEQ** = numer pierwszego bajtu w segmencie
3. **ACK** = numer **następnego oczekiwanego** bajtu
4. **ISN** = losowy, dla bezpieczeństwa i unikania kolizji
5. **Zamknięcie:** 4 kroki (FIN → ACK → FIN → ACK) + TIME_WAIT
6. **SYN flood** - atak DoS, obrona: SYN cookies

---

## 📖 Źródła do pogłębienia

1. RFC 793 - TCP Specification
2. RFC 6528 - Defending Against Sequence Number Attacks
3. RFC 7413 - TCP Fast Open
4. Stevens - "TCP/IP Illustrated, Volume 1"
