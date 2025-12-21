# Pytanie 7: Serwery DNS i buforowanie zapytań

## Pytanie
**"Które serwery DNS najwięcej zyskują dzięki buforowaniu zapytań (caching) w serwerach rekursywnych? Jakie znasz rodzaje serwerów DNS?"**

Przedmiot: SKM (Sieci Komputerowe)

---

## 📚 Odpowiedź główna

### Wprowadzenie do DNS

**DNS (Domain Name System)** to hierarchiczny, rozproszony system tłumaczenia nazw domenowych na adresy IP (i odwrotnie).

```
www.example.com → 93.184.216.34
```

### Hierarchia DNS

```
                         . (root)
                        /|\
                       / | \
                     com org pl
                    /|\      |
                   / | \     |
              google amazon  pw
                 |            |
                www          elka
```

---

## 1. Rodzaje serwerów DNS

### 1.1 Serwery autorytatywne (Authoritative)

**Definicja:** Przechowują oryginalne rekordy DNS dla danej domeny. Są "źródłem prawdy".

```
┌─────────────────────────────────────────────────────────────────┐
│                    SERWERY AUTORYTATYWNE                        │
├─────────────────────────────────────────────────────────────────┤
│  ROOT SERVERS (.) - 13 klastrów (a.root-servers.net ... m.)    │
│       ↓                                                         │
│  TLD SERVERS (.com, .org, .pl) - zarządzane przez rejestry     │
│       ↓                                                         │
│  AUTHORITATIVE NS - serwery konkretnych domen (ns1.example.com)│
└─────────────────────────────────────────────────────────────────┘
```

#### Root Servers (Serwery główne)
- **13 logicznych serwerów:** a.root-servers.net do m.root-servers.net
- **Fizycznie:** Setki serwerów (anycast)
- **Funkcja:** Wskazują serwery TLD

#### TLD Servers (Top-Level Domain)
- **gTLD:** .com, .org, .net (generic)
- **ccTLD:** .pl, .de, .uk (country code)
- **Nowe gTLD:** .shop, .app, .xyz
- **Funkcja:** Wskazują autoryzacyjne NS domen

#### Authoritative Name Servers
- **Primary (Master):** Oryginalne rekordy, edytowalne
- **Secondary (Slave):** Kopie przez transfer stref (AXFR/IXFR)
- **Funkcja:** Odpowiadają na zapytania o konkretną domenę

### 1.2 Serwery rekursywne (Recursive Resolvers)

**Definicja:** Wykonują pełne rozwiązywanie nazw w imieniu klienta, pytając kolejno serwery autorytatywne.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SERWERY REKURSYWNE                           │
├─────────────────────────────────────────────────────────────────┤
│  ISP Resolvers - dostarczane przez dostawcę Internetu          │
│  Public Resolvers - Google (8.8.8.8), Cloudflare (1.1.1.1)     │
│  Enterprise Resolvers - wewnętrzne serwery firmowe             │
│  Local Resolvers - np. router domowy, Pi-hole                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Stub Resolvers (Resolwery klienckie)

**Definicja:** Prosty klient DNS w systemie operacyjnym. Wysyła zapytanie do rekursywnego resolvera i czeka na odpowiedź.

- Windows: usługa DNS Client
- Linux: libc resolver (nsswitch.conf, resolv.conf)
- Nie wykonuje rekurencji sam

### 1.4 Forwarding Servers (Przekazujące)

**Definicja:** Przyjmują zapytania i przekazują je do innego resolvera zamiast samodzielnie rozwiązywać.

```
Klient → Forwarder → Recursive Resolver → Authoritative
```

---

## 2. Proces rozwiązywania DNS (Resolution)

### Zapytanie rekursywne vs iteracyjne

```
ZAPYTANIE REKURSYWNE (klient → resolver):
"Daj mi odpowiedź na www.example.com"
→ Resolver musi zwrócić ostateczną odpowiedź lub błąd

ZAPYTANIE ITERACYJNE (resolver → authoritative):
"Co wiesz o www.example.com?"
→ Serwer zwraca odpowiedź lub odesłanie (referral)
```

### Pełny proces rozwiązywania

```
Klient                  Recursive           Root      .com TLD    example.com
  │                     Resolver             │           │            │
  │──(1) www.example.com?──→│                │           │            │
  │                         │──(2) query?───→│           │            │
  │                         │←─(3) refer .com┘           │            │
  │                         │──(4) query?────────────────→│            │
  │                         │←─(5) refer example.com─────┘            │
  │                         │──(6) query?─────────────────────────────→│
  │                         │←─(7) 93.184.216.34──────────────────────┘
  │←─(8) 93.184.216.34─────┘                 
  │                         │                
  │       [CACHE zapisuje wszystkie odpowiedzi]
```

---

## 3. Buforowanie (Caching) w DNS

### Jak działa caching?

1. **Resolver otrzymuje odpowiedź** z serwera autorytatywnego
2. **Zapisuje w cache** wraz z TTL (Time To Live)
3. **Przy kolejnym zapytaniu** o tę samą nazwę - zwraca z cache
4. **Po wygaśnięciu TTL** - pyta ponownie serwer autorytatywny

### TTL (Time To Live)

```
; Fragment strefy DNS
www.example.com.    300    IN    A    93.184.216.34
                    ↑
                TTL = 300 sekund (5 minut)
```

| Typowe TTL | Zastosowanie |
|------------|--------------|
| 60-300 s | Dynamiczne usługi, failover |
| 3600 s (1h) | Standardowe strony |
| 86400 s (24h) | Stabilne serwisy |
| 604800 s (7d) | Rzadko zmieniane |

---

## 4. Które serwery zyskują najwięcej na cachingu?

### 🏆 Odpowiedź: **ROOT SERVERS i TLD SERVERS**

### Dlaczego root servers zyskują najwięcej?

```
BEZ CACHINGU:
┌────────────────────────────────────────────────────────────────┐
│ Każde zapytanie DNS → najpierw pytanie do root server         │
│ Miliardy zapytań dziennie → root servers byłyby przeciążone!  │
└────────────────────────────────────────────────────────────────┘

Z CACHINGIEM:
┌────────────────────────────────────────────────────────────────┐
│ Resolver pyta root server RAZ o serwery .com                  │
│ Cache przechowuje referral przez długi czas (np. 48h)         │
│ Kolejne tysiące zapytań o .com → z cache, bez root            │
└────────────────────────────────────────────────────────────────┘
```

### Analiza ilościowa

| Poziom | Liczba domen | Zapytania bez cache | Z cache |
|--------|--------------|---------------------|---------|
| **Root** | 1 (.) | ~100% zapytań | ~0.01% |
| **TLD** | ~1500 | ~100% zapytań | ~0.1% |
| **Authoritative** | Miliony | Proporcjonalnie | Zależne od TTL |

### Dlaczego ROOT i TLD zyskują więcej niż authoritative?

1. **Mniejsza liczba = więcej zapytań na serwer:**
   - 13 root servers vs miliony domen
   - Każde zapytanie o DOWOLNĄ domenę musi przejść przez root i TLD

2. **Długie TTL referrali:**
   - Root NS referrals: TTL 48h - 7 dni
   - TLD NS referrals: TTL 24h - 48h
   - Authoritative records: często krótsze (minuty-godziny)

3. **Hierarchiczna struktura:**
   ```
   Zapytanie o www.google.com:
   - Root: "Oto serwery .com"          → cached
   - TLD:  "Oto serwery google.com"    → cached
   - Auth: "Oto IP www.google.com"     → cached (ale krótszy TTL)
   
   Zapytanie o www.facebook.com:
   - Root: z cache! ✓
   - TLD:  z cache! ✓ (ten sam .com)
   - Auth: trzeba pytać (inna domena)
   ```

### Podsumowanie zysków z cachingu

```
REDUKCJA RUCHU DZIĘKI CACHINGOWI:

Root Servers:     ████████████████████████████░░  ~99.9% redukcja
TLD Servers:      ██████████████████████████░░░░  ~99% redukcja  
Authoritative:    ████████████░░░░░░░░░░░░░░░░░░  ~50-90% redukcja*

*zależy od TTL i popularności domeny
```

---

## 5. Typy rekordów DNS

| Rekord | Przeznaczenie | Przykład |
|--------|---------------|----------|
| **A** | IPv4 address | www → 93.184.216.34 |
| **AAAA** | IPv6 address | www → 2606:2800:220:1:... |
| **CNAME** | Alias (canonical name) | blog → www.example.com |
| **MX** | Mail server | @ → 10 mail.example.com |
| **NS** | Name server | @ → ns1.example.com |
| **TXT** | Tekst (SPF, DKIM) | @ → "v=spf1 ..." |
| **SOA** | Start of Authority | Metadata strefy |
| **PTR** | Reverse DNS | IP → nazwa |
| **SRV** | Service location | _sip._tcp → server:5060 |

---

## 📊 Tabela porównawcza serwerów DNS

| Typ serwera | Funkcja | Cache | Autorytatywny |
|-------------|---------|-------|---------------|
| **Root** | Wskazuje TLD | Nie | Tak (dla .) |
| **TLD** | Wskazuje NS domen | Nie | Tak (dla TLD) |
| **Authoritative** | Przechowuje rekordy | Nie | Tak |
| **Recursive** | Rozwiązuje dla klientów | **TAK** | Nie |
| **Forwarder** | Przekazuje zapytania | Może | Nie |
| **Stub** | Klient systemu | Minimalny | Nie |

---

## 🧠 Mnemoniki

### "RATS" dla hierarchii DNS:
- **R**oot - korzeń drzewa
- **A**uthoritative TLD - .com, .pl...
- **T**arget NS - ns1.example.com
- **S**tub resolver - klient

### "ROOT COOL" dla zysków z cache:
- **ROOT** = **C**ache **O**ffers **O**verwhelming **L**oad reduction
- Root servers byłyby przeciążone bez cache w resolverach

### "TRIP" dla procesu rozwiązywania:
- **T**ranslate - tłumaczenie nazwy na IP
- **R**ecursive - resolver robi pracę
- **I**terative - serwery autorytatywne odpowiadają lub odsyłają
- **P**ersist - cache przechowuje wynik

### "A-QUAD" dla popularnych rekordów:
- **A** - Address (IPv4)
- **AAAA** - Address (IPv6) - 4×A
- **D**NS - NS record

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Jak działa anycast w kontekście root servers?"

**Odpowiedź:**

**Anycast** = ten sam adres IP na wielu serwerach geograficznie rozproszonych.

```
Użytkownik w Polsce     → najbliższy serwer a.root-servers.net (Frankfurt)
Użytkownik w USA        → najbliższy serwer a.root-servers.net (Virginia)
Użytkownik w Japonii    → najbliższy serwer a.root-servers.net (Tokyo)

Wszystkie mają ten sam adres IP!
Routing BGP kieruje do najbliższego.
```

**Korzyści:**
- Niższe opóźnienia (latency)
- Odporność na DDoS
- Load balancing geograficzny

---

### Q2: "Co to jest DNS poisoning/spoofing?"

**Odpowiedź:**

**DNS Cache Poisoning** = atak polegający na wstrzyknięciu fałszywych rekordów do cache resolvera.

```
Atakujący → fałszywa odpowiedź "google.com = 1.2.3.4"
               ↓
Resolver zapisuje w cache
               ↓
Użytkownicy kierowani na serwer atakującego
```

**Zabezpieczenia:**
- **DNSSEC** - podpisy kryptograficzne rekordów
- **Randomizacja portów źródłowych**
- **0x20 encoding** - randomizacja wielkości liter
- **DNS over HTTPS (DoH)** / **DNS over TLS (DoT)**

---

### Q3: "Co to jest DNSSEC?"

**Odpowiedź:**

**DNSSEC (DNS Security Extensions)** = rozszerzenie dodające kryptograficzne podpisy do rekordów DNS.

**Nowe typy rekordów:**
- **RRSIG** - podpis rekordu
- **DNSKEY** - klucz publiczny
- **DS** - delegacja bezpieczeństwa (u rodzica)
- **NSEC/NSEC3** - dowód nieistnienia

**Łańcuch zaufania:**
```
Root (.) → podpisuje DS dla .com
.com     → podpisuje DS dla example.com  
example.com → podpisuje A dla www
```

---

### Q4: "Czym różni się DNS over HTTPS od DNS over TLS?"

**Odpowiedź:**

| Cecha | DoT (DNS over TLS) | DoH (DNS over HTTPS) |
|-------|-------------------|---------------------|
| Port | 853 (dedykowany) | 443 (jak HTTPS) |
| Protokół | TLS | HTTPS |
| Widoczność | Łatwy do zablokowania | Trudny do odróżnienia |
| Format | Wire format DNS | Wire lub JSON |
| Klient | Systemowy resolver | Przeglądarka/aplikacja |

**DoH** jest trudniejszy do blokowania/monitorowania - wygląda jak normalny ruch HTTPS.

---

### Q5: "Co się stanie, jeśli wszystkie root servers przestaną działać?"

**Odpowiedź:**

**Krótkoterminowo (godziny):** Większość działa dzięki cache
- Resolwery mają w cache adresy TLD servers
- TTL root referrals: ~48h

**Średnioterminowo (dni):** Stopniowa degradacja
- Cache wygasa
- Nowe domeny nierozwiązywalne
- Istniejące z długim TTL jeszcze działają

**W praktyce:** Niemożliwe do osiągnięcia
- 13 klastrów anycast
- Setki fizycznych serwerów
- Geograficzne rozproszenie
- Różni operatorzy

---

### Q6: "Jak działa Negative Caching?"

**Odpowiedź:**

**Negative caching** = cache'owanie odpowiedzi "nie istnieje" (NXDOMAIN).

```
Zapytanie: nieistniejaca.example.com
Odpowiedź: NXDOMAIN (SOA z TTL dla negative cache)
Cache: "nieistniejaca.example.com = NXDOMAIN" przez TTL
```

**Korzyści:**
- Redukcja ruchu przy literówkach
- Szybsza odpowiedź dla nieistniejących domen
- Ochrona przed niektórymi atakami

**RFC 2308** definiuje negative caching.

---

## 🎯 Kluczowe punkty do zapamiętania

1. **ROOT i TLD zyskują NAJWIĘCEJ** na cachingu w resolverach
2. **Recursive resolver** = wykonuje pełne rozwiązywanie + cache
3. **Authoritative** = źródło prawdy, nie cache'uje
4. **Hierarchia:** Root → TLD → Authoritative NS
5. **TTL** określa czas życia rekordu w cache
6. **Anycast** pozwala 13 root serwerom obsługiwać cały Internet

---

## 📖 Źródła do pogłębienia

1. RFC 1034, 1035 - DNS specification
2. RFC 2308 - Negative caching
3. RFC 4033-4035 - DNSSEC
4. Cricket Liu - "DNS and BIND"
5. root-servers.org - informacje o root servers
