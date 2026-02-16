## PYTANIE 8: TCP Three-Way Handshake (SKM)

**Cel, interpretacja numerów sekwencyjnych, wartość początkowa ISN.**

---

### Tło pojęciowe — słowniczek

**TCP (Transmission Control Protocol)** — protokół warstwy transportowej zapewniający niezawodne, uporządkowane dostarczanie danych. W przeciwieństwie do UDP, TCP gwarantuje: brak utraty, poprawną kolejność, brak duplikatów. Ceną jest większy narzut (handshake, potwierdzenia, retransmisje).

    Warstwa aplikacji:    HTTP, FTP, SMTP
    Warstwa transportowa: TCP / UDP       ← tu TCP
    Warstwa sieciowa:     IP
    Warstwa łącza:        Ethernet, WiFi

**Połączenie (connection)** — TCP jest protokołem połączeniowym (connection-oriented). Zanim dane popłyną, obie strony muszą ustanowić połączenie — to właśnie robi three-way handshake.

**Segment** — jednostka danych w TCP. Nagłówek TCP (20+ bajtów) + dane. Nagłówek zawiera m.in. porty, numery sekwencyjne, flagi (SYN, ACK, FIN…), window size.

---

**Handshake (uścisk dłoni)** — procedura nawiązywania połączenia. „Three-way" = trzy kroki: SYN → SYN-ACK → ACK. Metafora: „Hej!" → „Hej, słyszę!" → „OK, gadamy!". Cel: obie strony potwierdzają gotowość i synchronizują numery sekwencyjne.

**SYN (Synchronize)** — flaga w nagłówku TCP. Segment z flagą SYN inicjuje połączenie i przekazuje początkowy numer sekwencyjny (ISN) nadawcy.

**ACK (Acknowledge)** — flaga potwierdzenia. Numer ACK = numer następnego oczekiwanego bajtu. Gdy serwer wysyła SYN-ACK, jednocześnie potwierdza odbiór SYN klienta (ACK=x+1) i wysyła swój SYN (ISN serwera = y).

---

**Numer sekwencyjny (Sequence Number, SEQ)** — 32-bitowa liczba identyfikująca pozycję pierwszego bajtu danych w segmencie w strumieniu bajtów. Funkcje: zapewnia kolejność, wykrywa duplikaty i braki, umożliwia potwierdzenia.

    Klient wysyła 100 bajtów od pozycji 1000:
    SEQ = 1000, dane = bajty 1000–1099
    Następny segment: SEQ = 1100

**Numer potwierdzenia (Acknowledgment Number, ACK number)** — mówi: „odebrałem wszystko do bajtu X-1, teraz czekam na bajt X". Jest kumulatywny — jedno ACK potwierdza wszystkie dane do tej pozycji.

    Klient wysłał SEQ=1000, 100 bajtów
    Serwer odpowiada: ACK=1100 → „dostałem do 1099, czekam na 1100"

**SACK (Selective ACK)** — rozszerzenie TCP. Pozwala potwierdzać niesąsiednie bloki danych, co przyspiesza retransmisję. Bez SACK: utrata jednego segmentu wymaga retransmisji wszystkiego od niego.

---

**ISN (Initial Sequence Number)** — początkowy numer sekwencyjny wybierany przy nawiązywaniu połączenia. Każda strona wybiera swój ISN niezależnie.

**Dlaczego ISN nie zaczyna od 0?**
1. **Bezpieczeństwo** — losowy ISN utrudnia atakującemu zgadnięcie numerów i przejęcie sesji (TCP hijacking).
2. **Unikanie kolizji** — gdyby ISN=0, segmenty z poprzedniego połączenia między tymi samymi portami mogłyby zostać błędnie zaakceptowane.
3. RFC 793 (oryg.): ISN = timer inkrementowany co 4μs mod 2³².
4. RFC 6528 (współcz.): ISN = M + F(adresy, porty, secret_key) — kryptograficznie losowy.

**Rozbicie formuły RFC 6528:**

    ISN = M + F(srcIP, dstIP, srcPort, dstPort, secret_key)

- **M** — globalny timer (zegar). Licznik inkrementowany co ~4 μs przez jądro OS, niezależnie od połączeń. Zapewnia, że ISN „płyną do przodu" w czasie — dwa połączenia otwarte w odstępie 1 sekundy dostaną M różniące się o ~250 000.
- **F** — funkcja kryptograficzna (np. MD5, SHA-256, SipHash). Bierze dane połączenia i zwraca pseudolosowy offset. Atakujący nie może odgadnąć wyniku F, bo nie zna klucza.
- **srcIP, dstIP (adresy)** — adres IP źródłowy i docelowy (np. 192.168.1.5, 93.184.216.34). Dzięki nim ISN jest różny DLA KAŻDEJ PARY hostów.
- **srcPort, dstPort (porty)** — port źródłowy i docelowy (np. 49152, 443). Ten sam klient łączący się z tym samym serwerem, ale na inny port, dostanie inny ISN.
- **secret_key** — losowy klucz znany TYLKO jądru OS. Generowany przy starcie systemu, nigdy nie ujawniony na zewnątrz. Bez niego atakujący musi zgadywać F — co przy 2³² możliwych wartości jest praktycznie niemożliwe.

Przykład liczbowy:

    M = 1 000 000 (wartość timera w danej chwili)
    F(192.168.1.5, 93.184.216.34, 49152, 443, 0xDEAD...) = 2 738 491 203
    ISN = 1 000 000 + 2 738 491 203 = 2 739 491 203

    Inna para (srcIP, dstIP) → F daje zupełnie inną wartość → inny ISN

**Dlaczego to bezpieczne?** Atakujący widzi ISN (bo jest w nagłówku SYN), ale nie może z niego wyliczyć secret_key ani przewidzieć ISN innego połączenia, bo F jest jednokierunkowa (one-way function).

**MSS (Maximum Segment Size)** — maksymalny rozmiar danych w jednym segmencie TCP. Uzgadniana w handshake (zwykle 1460 bajtów dla Ethernetu = MTU 1500 − 20 IP − 20 TCP).

**Window Scale** — opcja TCP negocjowana w handshake. Pozwala zwiększyć okno odbiorcze ponad 65535 bajtów (do ~1 GB), co jest konieczne dla szybkich łączy.

**RFC (Request For Comments)** — dokumenty standaryzacyjne internetu. Nazwa historyczna z ARPANET — „prośba o komentarze" — ale w praktyce to obowiązujące standardy. TCP = RFC 793 (1981).

**Bajt (byte)** — 8 bitów. TCP numeruje strumień po bajtach, nie po segmentach. Dlatego SEQ to numer bajtu, a nie numer pakietu.

---

### Cel handshake'u
1. Nawiązanie połączenia — obie strony się zgadzają
2. Synchronizacja ISN (Initial Sequence Number)
3. Uzgodnienie parametrów (MSS, Window Scale, SACK)

### Przebieg

    Klient                          Serwer
      |  (1) SYN, seq=x              |
      |-----------------------------→|
      |  (2) SYN+ACK, seq=y, ack=x+1 |
      |←-----------------------------|
      |  (3) ACK, seq=x+1, ack=y+1   |
      |-----------------------------→|
      |     [POŁĄCZENIE NAWIĄZANE]    |

### Numery sekwencyjne (SEQ)
- SEQ = numer pierwszego bajtu danych w segmencie
- Funkcje: kolejność, duplikaty, braki, potwierdzenia

### Numery potwierdzenia (ACK)
- ACK = numer **następnego oczekiwanego** bajtu (kumulatywne)
- SACK — opcja potwierdzania niesąsiednich bloków

### Wartość początkowa ISN
- **NIE zaczyna od 0** — bezpieczeństwo + unikanie kolizji z poprzednimi połączeniami
- RFC 793: ISN = timer 4μs mod 2³²
- RFC 6528: ISN = M + F(adresy, porty, secret_key) — kryptograficznie

### Etymologia

**TCP** — Transmission Control Protocol; Vint Cerf + Bob Kahn (1974, „A Protocol for Packet Network Intercommunication"). **Handshake** — metafora uścisku dłoni = wzajemna zgoda na komunikację. **SYN** — Synchronize. **ACK** — Acknowledge. **ISN** — Initial Sequence Number. **MSS** — Maximum Segment Size. **SACK** — Selective ACK. **RFC** — Request For Comments; tradycja ARPANET (1969).

### Jak zapamiętać

- **„SYN, SYN-ACK, ACK"** — 3 kroki, jak potwierdzenie rozmowy: „Hej!" „Hej, słyszę!" „OK, gadamy!"
- **SEQ = numer bajtu**, ACK = „czekam na bajt numer..."
- **ISN losowy** — bo inaczej atakujący może zgadnąć i przejąć sesję

