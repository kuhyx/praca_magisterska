## PYTANIE 22: Modele spójności danych w systemach rozproszonych

**Silne i słabe modele spójności.**

---

### Tło pojęciowe — słowniczek

**Model (w informatyce)** — uproszczony, formalny opis zachowania systemu. Model definiuje REGUŁY: co system gwarantuje, a czego nie. Jak umowa/kontrakt — mówi programiście „na to możesz liczyć". W kontekście spójności: model opisuje jakie wyniki odczytów są dopuszczalne po zapisie.

    Model = kontrakt:
    "Jeśli zapiszesz x=5, to odczyt zwróci..."
    ...5 natychmiast?  (silny model)
    ...5 kiedyś?       (słaby model)
    ...3 albo 5?       (bardzo słaby model)

**Model spójności (consistency model)** — kontrakt między systemem rozproszonym a programistą, definiujący jakie GWARANCJE daje system dotyczące kolejności i widoczności operacji na danych. Każdy model odpowiada na pytanie: „Gdy węzeł A zapisze x=5, co i kiedy zobaczy węzeł B?"

Modele tworzą **spektrum** od silnych do słabych:

    Silne ←───────────────────────────────→ Słabe
    Linearizability → Sequential → Causal → Eventual

**Silny model spójności (strong consistency)** — system zachowuje się tak, jakby istniała JEDNA kopia danych. Każdy odczyt po zapisie zwraca najnowszą wartość. Gwarancja: programista nie musi myśleć o replikacji. Cena: wysoka latencja (węzły muszą się komunikować/uzgadniać przed odpowiedzią), niska dostępność przy partycjach sieciowych.

    Silny model:
    Klient A pisze x=5  →  [consensus: 3 węzły potwierdzają]  → OK
    Klient B czyta x    →  GWARANTOWANE: x=5 (natychmiast!)
    Koszt: ~10-100ms latencji na zapis (czeka na consensus)

**Słaby model spójności (weak consistency)** — system NIE gwarantuje, że odczyt po zapisie zwróci najnowszą wartość. Repliki mogą być chwilowo rozbieżne (stale data). Zaleta: niska latencja (odpowiedź natychmiast z lokalnej repliki), wysoka dostępność. Programista musi obsłużyć niespójności.

    Słaby model:
    Klient A pisze x=5  →  [zapis lokalny]  → OK (natychmiast!)
    Klient B czyta x    →  x=3 (stara wartość! replika nie zdążyła)
    ...po kilku sekundach...
    Klient B czyta x    →  x=5 (w końcu zsynchronizowane)
    Koszt: programista musi tolerować stale data

**Trade-off silny vs słaby:**

    Cecha              Silny (Linearizable)     Słaby (Eventual)
    ─────────────────────────────────────────────────────────────
    Latencja zapisu    wysoka (~10-100ms)        niska (~1ms)
    Latencja odczytu   wysoka (quorum read)      niska (lokalna replika)
    Dostępność         niska (wymaga quorum)     wysoka (lokalna odpowiedź)
    Poprawność         gwarantowana              programista musi obsłużyć
    Skalowanie         trudne (consensus)        łatwe (dodaj repliki)
    Przykłady          Spanner, Zookeeper        Cassandra, DNS, DynamoDB

---

**Spójność danych (consistency)** — gwarancja, że wszystkie węzły systemu rozproszonego widzą te same dane w przewidywalny sposób. Pytanie: gdy zapisuję na węzeł A, co odczyta węzeł B? Odpowiedź zależy od modelu spójności.

**Replikacja (replication)** — przechowywanie kopii danych na wielu węzłach. Cel: dostępność (awaria jednego → dane na innym), wydajność (odczyt z najbliższego). Problem: aktualizujesz jedną kopię — kiedy reszta się zsynchronizuje?

    Zapis na replice A: x = 5
    Replika B: x = ? (jeszcze 3? już 5?)
    Odpowiedź zależy od modelu spójności!

---

**Linearizability (linearyzowalność)** — najsilniejszy model. Każda operacja wygląda jakby nastąpiła atomowo w jednym momencie między jej wywołaniem a odpowiedzią. System zachowuje się jak JEDNA kopia danych. Wymaga consensus (np. Paxos, Raft) — kosztowna.

    Klient A pisze x=5 o 14:00:01, dostaje OK o 14:00:02
    Klient B czyta x o 14:00:01.5 → MUSI dostać 5 (bo zapis "nastąpił" gdzieś w 14:00:01-02)

Przykład: Google Spanner (zegary atomowe TrueTime).

**Sequential consistency (spójność sekwencyjna)** — globalny porządek operacji zgodny z porządkiem programu KAŻDEGO procesu. Ale NIE musi odpowiadać czasowi rzeczywistemu. Słabsza niż linearyzowalność.

    Proces A: write(x,1), write(x,2)
    Proces B: read(x)→2, read(x)→1  ← NIE OK (B widzi operacje A w złej kolejności)
    Proces B: read(x)→1, read(x)→2  ← OK (zgodne z kolejnością A)

---

![Linearizability vs Sequential Consistency](img/linearizability_vs_sequential.png)

**KLUCZOWA RÓŻNICA: Linearizability vs Sequential Consistency — przykład:**

Wyobraź sobie rejestr x, dwa klienty A i B, i oś REALNEGO CZASU:

    Czas:     t₁────t₂────t₃────t₄────t₅────t₆
    Klient A: [──write(x,1)──]                     (start t₁, OK t₃)
    Klient B:            [──read(x)──]              (start t₂, odpowiedź t₄)
    Klient A:                          [──write(x,2)──]  (start t₅, OK t₆)

**Linearizability mówi:** Operacja read(x) klienta B ZACZĘŁA SIĘ (t₂) PO ROZPOCZĘCIU write(x,1) klienta A (t₁), i SKOŃCZYŁA SIĘ (t₄) PO ZAKOŃCZENIU write(x,1) (t₃). Więc operacje NIE nakładają się — read musi OBOWIĄZKOWO zwrócić x=1. Gdyby zwróciła coś innego (np. starą wartość x=0), naruszałoby to linearizability, bo w czasie rzeczywistym zapis już się zakończył.

**Sequential consistency mówi:** Musi istnieć JAKIŚ globalny porządek operacji, który jest zgodny z kolejnością programu klienta A (write(x,1) przed write(x,2)) i klienta B (read(x) w jego kolejności). ALE ten porządek NIE MUSI odpowiadać temu, co dzieje się w czasie rzeczywistym.

    Linearizability: read(x) o t₂-t₄ MUSI zobaczyć wynik write z t₁-t₃ → x=1 ✓
    Sequential:      system MOŻE ułożyć operacje jako: read(x)→0, write(x,1), write(x,2)
                     → read(x) zwraca 0 (starą wartość) → DOPUSZCZALNE!
                     Bo ten porządek jest „sekwencyjnie spójny" — po prostu read
                     jest w globalnej kolejności PRZED write, mimo że w zegarku ściennym
                     nakładały się czasowo.

**Jeszcze prościej — analogia kina:**
- **Linearizability** = film NA ŻYWO: jeśli gol padł o 14:00, to widzowie w tym momencie MUSZĄ go zobaczyć.
- **Sequential consistency** = film NAGRANY i emitowany z opóźnieniem: kolejność scen jest zachowana, ale nie odpowiada czasowi rzeczywistemu. Widzisz gol, potem korner — w poprawnej kolejności, ale nie wiesz KIEDY naprawdę się wydarzyły.

---

**Causal consistency (spójność przyczynowa)** — operacje przyczynowo zależne widziane w tej samej kolejności przez wszystkich. Operacje współbieżne (niezależne) mogą być widziane w różnej kolejności. Wymaga vector clocks.

    A pisze x=1 → B czyta x(=1) → B pisze y=2
    Przyczynowość: write(x,1) → write(y,2)
    Każdy musi widzieć write(x,1) PRZED write(y,2)

**Session guarantees (gwarancje sesji):**
- **Read Your Writes** — jeśli zapisałem x=5, mój następny odczyt zobaczy 5 (nie starą wartość)
- **Monotonic Reads** — odczyty nie „cofają się w czasie" (jeśli widziałem x=5, nie zobaczę x=3)
- **Monotonic Writes** — moje zapisy są stosowane w kolejności
- **Writes Follow Reads** — jeśli przeczytałem x i na tej podstawie zapisałem y, inni widzą x przed y

**Eventual consistency (spójność ostateczna)** — najsłabszy model. Jeśli przestaniesz pisać, KIEDYŚ wszystkie odczyty zwrócą tę samą wartość. Ale „kiedyś" może trwać sekundy lub minuty! Najszybszy i najskalowalniejszy. Przykłady: DNS, Cassandra.

    Zapis x=5 na replice A
    Replika B: jeszcze x=3... x=3... [replikacja]... x=5 ← w końcu!

**Dlaczego DNS to przykład eventual consistency?**

DNS (Domain Name System) tłumaczy nazwy domen (np. google.com) na adresy IP. Jest MASYWNIE rozproszony — tysiące serwerów DNS na świecie, każdy z własną kopią (cache). Gdy zmienisz rekord DNS (np. google.com → nowy IP), co się dzieje:

    Krok 1: Admin zmienia rekord na AUTHORITATIVE server: google.com → 142.250.80.46
    Krok 2: Authoritative server ma nową wartość NATYCHMIAST
    Krok 3: Ale tysiące serwerów DNS na świecie mają STARY cache!
            → ISP DNS w Warszawie: google.com → 142.250.80.14 (stary, z cache)
            → ISP DNS w Tokio: google.com → 142.250.80.14 (stary)
            → Google Public DNS: google.com → 142.250.80.14 (stary)
    Krok 4: Cache ma TTL (Time To Live), np. 300 sekund = 5 minut
            Po upływie TTL, serwer DNS pyta authoritative → dostaje nowy IP
    Krok 5: STOPNIOWO, jeden po drugim, serwery DNS aktualizują cache
            Po ~24-48h → WSZYSTKIE serwery mają nową wartość

    To jest EVENTUAL CONSISTENCY:
    - Brak silnej gwarancji: w t=0 różni klienci widzą RÓŻNE IP
    - „Kiedyś" się zsynchronizuje: po TTL + propagacja
    - Kompromis: SZYBKOŚĆ (cache, brak czekania na consensus) vs NIESPÓJNOŚĆ (stale data)
    - Gdyby DNS był linearizable, każde zapytanie DNS musiałoby pytać
      authoritative server → 100-300ms latencji zamiast <1ms z cache → internet byłby WOLNY

---

**CAP Theorem (twierdzenie Brewera)** — w systemie rozproszonym przy partycji sieciowej (P) musisz wybrać między Consistency (C) a Availability (A):
- **CP** — spójny, ale niedostępny przy partycji (np. HBase, Spanner)
- **AP** — dostępny, ale niespójny przy partycji (np. Cassandra, DynamoDB)
- Bez partycji możesz mieć oba. Ale partycje SĄ nieuniknione w sieci.

    Partycja = węzły A i B nie mogą się komunikować
    CP: odmów operacji (niedostępny) → zachowaj spójność
    AP: wykonaj operację (dostępny) → ryzykuj niespójność

---

**Consensus (uzgadnianie)** — protokół, w którym rozproszone węzły zgadzają się na jedną wartość pomimo awarii. Kluczowy dla linearyzowalności. Algorytmy: Paxos (Lamport), Raft (prostszy), Zab (Zookeeper).

![Paxos — uproszczony przebieg](img/paxos_flow.png)

**Jak działa Paxos — uproszczony walkthrough (dlaczego daje linearyzowalność):**

Paxos ma 3 role: **Proposer** (proponuje wartość), **Acceptor** (głosuje), **Learner** (dowiaduje się wyniku). Typowo 3-5 acceptorów (nieparzyste). Protokół ma 2 fazy:

    FAZA 1: PREPARE — „Czy mogę zaproponować?"
    Proposer → wysyła Prepare(n) do WSZYSTKICH acceptorów (n = numer propozycji, rosnący)
    Acceptor → jeśli n > każdy wcześniejszy n, odpowiada Promise(n) + ewentualnie wcześniej
               zaakceptowaną wartość. Jeśli n mniejszy — ignoruje.

    FAZA 2: ACCEPT — „Zaakceptujcie tę wartość!"
    Proposer → jeśli dostał Promise od MAJORITY (np. 2 z 3), wysyła Accept(n, wartość)
    Acceptor → jeśli nie obiecał wyższego n, akceptuje → wartość UZGODNIONA

    Przykład: 3 acceptory (A₁, A₂, A₃), proposer chce zapisać x=5

    Proposer  ──Prepare(1)──→  A₁: Promise(1) ✓
                               A₂: Promise(1) ✓  ← majority (2/3)!
                               A₃: (wolny, nie odpowiedział)

    Proposer  ──Accept(1, x=5)──→  A₁: Accepted ✓
                                    A₂: Accepted ✓  ← majority!
    → x=5 jest UZGODNIONE. Każdy przyszły odczyt MUSI zwrócić 5.

**Dlaczego to daje linearyzowalność?** Bo zapis x=5 jest „zacommitowany" dopiero gdy MAJORITY potwierdzi. Odczyt też musi odpytać majority → co najmniej 1 acceptor wie o x=5 (bo majority zapisu i majority odczytu OVERLAPują się — kworum). Dlatego odczyt ZAWSZE widzi najnowszą wartość.

    W + R > N → overlap gwarantowany
    W=2, R=2, N=3: zapis potwierdza 2, odczyt pyta 2 → min. 1 wspólny acceptor

**Quorum** — minimalna liczba węzłów, które muszą potwierdzić operację.

    N = liczba replik, W = quorum zapisu, R = quorum odczytu
    W + R > N → gwarantuje odczyt najnowszej wartości
    Np. N=3, W=2, R=2: zawsze przynajmniej 1 wspólna replika

**CRDTs (Conflict-free Replicated Data Types)** — struktury danych, które automatycznie zbiegają do spójnego stanu bez koordynacji. Matematycznie gwarantują brak konfliktów. Przykłady: G-Counter (grow-only counter), OR-Set (observed-remove set). Idealne dla eventual consistency.

**LWW (Last-Writer-Wins)** — prosty mechanizm rozwiązywania konfliktów: wygrywa zapis z najnowszym timestampem. Problem: wymaga zsynchronizowanych zegarów i może tracić dane.

---

### Spektrum (od silnego do słabego)

    Linearizability → Sequential → Causal → Session → Eventual

### Silne modele

**Linearizability:** Każda operacja wygląda atomowo w momencie między wywołaniem a odpowiedzią. Najsilniejsza. „Globalny czas rzeczywisty." Kosztowna (consensus). Przykład: Spanner.

**Sequential Consistency:** Globalny porządek operacji zgodny z porządkiem programu każdego procesu, ale NIE z czasem rzeczywistym. Przykład: Zookeeper.

### Słabe modele

**Causal Consistency:** Operacje przyczynowo zależne widziane w tej samej kolejności. Niezależne mogą być w różnej. Wymaga vector clocks. Przykład: MongoDB.

**Session Guarantees:** Read Your Writes, Monotonic Reads, Monotonic Writes, Writes Follow Reads.

**Eventual Consistency:** Jeśli brak nowych zapisów, ostatecznie wszystkie odczyty zwrócą tę samą wartość. Najsłabszy, najszybszy. Przykład: DNS, Cassandra.

### CAP Theorem: Consistency + Availability + Partition tolerance — wybierz 2 (w obecności partycji: C lub A).

### Rozwiązywanie konfliktów: LWW (Last-Writer-Wins), Siblings (multi-value), **CRDTs** (automatycznie zbieżne struktury).

### Etymologia

**Linearizability** — Maurice Herlihy + Jeannette Wing (1990); łac. „linearis" = w linii. **Sequential consistency** — Leslie Lamport (1979). **Causal consistency** — Ahamad et al. (1995); łac. „causa" = przyczyna. **CAP** — Eric Brewer (UC Berkeley, 2000, „Brewer's conjecture"); udowniony przez Gilbert & Lynch (2002). **CRDTs** — Conflict-free Replicated Data Types (Marc Shapiro et al., 2011). **Quorum** — łac. „of whom" = minimalna liczba głosów (z prawa rzymskiego).

### Jak zapamiętać

- **Linearizable = „natychmiast, atomowo, jak 1 kopia"**
- **Eventual = „kiedyś się zsynchronizuje" (ale kiedy?)**
- **CAP = „Partition → wybierz C albo A"**
- **Quorum: W+R > N** gwarantuje odczyt najnowszej wartości

