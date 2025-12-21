# Pytanie 44: Zarządzanie zapasami w łańcuchu dostaw

## Pytanie
**"Jakie problemy wiążą się z zarządzaniem zapasami w łańcuchu dostaw? Omówić przykładowy model zarządzania zapasami w łańcuchu dostaw."**

Przedmiot: ZBOP (Zarządzanie i Badania Operacyjne w Produkcji)

---

## 📚 Odpowiedź główna

### 1. Łańcuch dostaw - struktura

```
┌─────────────────────────────────────────────────────────────────┐
│                    ŁAŃCUCH DOSTAW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Dostawcy → Producent → Dystrybutor → Detalista → Klient       │
│     │          │            │            │                      │
│     └──────────┴────────────┴────────────┘                      │
│              Przepływ informacji (zamówienia)                   │
│     ┌──────────┬────────────┬────────────┐                      │
│     │          │            │            │                      │
│  Dostawcy ← Producent ← Dystrybutor ← Detalista                │
│              Przepływ produktów                                 │
│                                                                 │
│  Na każdym etapie: ZAPASY (inventory)                          │
│  • Surowce (raw materials)                                     │
│  • Produkcja w toku (WIP)                                      │
│  • Wyroby gotowe (finished goods)                              │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Problemy zarządzania zapasami

#### 2.1 Bullwhip Effect (Efekt byczego bicza)

```
┌─────────────────────────────────────────────────────────────────┐
│ BULLWHIP EFFECT                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Popyt klienta:    ───────────────────────────                  │
│                   (stabilny)                                    │
│                                                                 │
│ Zamówienia        ┌┐  ┌┐                                       │
│ detalisty:     ───┘└──┘└─────────────────                      │
│                   (małe wahania)                                │
│                                                                 │
│ Zamówienia      ┌──┐    ┌──┐                                   │
│ dystrybutora: ──┘  └────┘  └─────────                          │
│                   (większe wahania)                             │
│                                                                 │
│ Zamówienia    ┌────┐        ┌────┐                             │
│ producenta: ──┘    └────────┘    └───                          │
│                   (jeszcze większe)                             │
│                                                                 │
│ Zamówienia  ┌──────┐              ┌──────┐                     │
│ dostawcy: ──┘      └──────────────┘                            │
│                   (AMPLIFIKACJA!)                               │
│                                                                 │
│ Przyczyny:                                                      │
│ • Prognozowanie popytu (forecasting)                           │
│ • Batching zamówień                                            │
│ • Wahania cen (promocje)                                       │
│ • Rationing/shortage gaming                                    │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.2 Kluczowe problemy

| Problem | Opis |
|---------|------|
| **Bullwhip effect** | Amplifikacja wahań w górę łańcucha |
| **Stockouts** | Brak towaru, utrata sprzedaży |
| **Overstock** | Nadmiar zapasów, koszty magazynowania |
| **Obsolescence** | Przestarzałe/przeterminowane produkty |
| **Lead time variability** | Zmienność czasu dostawy |
| **Demand uncertainty** | Niepewność popytu |
| **Koordynacja** | Brak współpracy między ogniwami |
| **Visibility** | Brak widoczności zapasów w łańcuchu |

---

### 3. Koszty zapasów

```
┌─────────────────────────────────────────────────────────────────┐
│ STRUKTURA KOSZTÓW                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. KOSZTY UTRZYMANIA (Holding costs) - h                       │
│    • Koszt kapitału zamrożonego                                │
│    • Magazynowanie, ubezpieczenie                              │
│    • Zużycie, przestarzałość                                   │
│    Typowo: 15-30% wartości rocznie                             │
│                                                                 │
│ 2. KOSZTY ZAMAWIANIA (Ordering costs) - K                      │
│    • Stałe koszty zamówienia                                   │
│    • Transport, obsługa                                        │
│    • Przezbrojenia (setup)                                     │
│                                                                 │
│ 3. KOSZTY BRAKU (Shortage costs) - p                           │
│    • Utrata sprzedaży                                          │
│    • Kary umowne                                               │
│    • Utrata reputacji                                          │
│                                                                 │
│ CEL: Minimalizuj TC = Holding + Ordering + Shortage            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. Model EOQ (Economic Order Quantity)

#### Założenia

```
┌─────────────────────────────────────────────────────────────────┐
│ MODEL EOQ - Klasyczny model Harrisa-Wilsona                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Założenia:                                                      │
│ • Popyt deterministyczny, stały: D jednostek/rok               │
│ • Lead time = 0 (natychmiastowa dostawa)                       │
│ • Brak braków (no stockouts)                                   │
│ • Stały koszt zamówienia: K                                    │
│ • Stały koszt utrzymania: h na jednostkę/rok                  │
│                                                                 │
│ Poziom zapasu:                                                  │
│   Q │╲                                                          │
│     │  ╲                                                        │
│     │    ╲                                                      │
│     │      ╲      ╱╲                                           │
│     │        ╲  ╱    ╲                                         │
│     │          ╲        ╲                                      │
│   0 └──────────────────────────────→ t                         │
│     │←── T ──→│←── T ──→│                                      │
│                                                                 │
│ Q = wielkość zamówienia                                        │
│ T = Q/D = cykl zamawiania                                      │
└─────────────────────────────────────────────────────────────────┘
```

#### Formuła EOQ

```
Koszty roczne:

Ordering cost = K × (D/Q)        (D/Q zamówień rocznie)
Holding cost = h × (Q/2)         (średni zapas = Q/2)

TC(Q) = K·D/Q + h·Q/2

Minimalizacja: dTC/dQ = 0

-K·D/Q² + h/2 = 0

         ┌──────────┐
    Q* = │ 2·K·D   │
         │ ──────  │
         │   h     │
         └──────────┘

Optymalna wielkość zamówienia!
```

#### Przykład numeryczny

```
Dane:
  D = 10,000 jednostek/rok
  K = 100 PLN/zamówienie
  h = 2 PLN/jednostkę/rok

EOQ:
  Q* = √(2 × 100 × 10,000 / 2) = √1,000,000 = 1,000 jednostek

Cykl zamawiania:
  T* = Q*/D = 1,000/10,000 = 0.1 roku ≈ 5 tygodni

Liczba zamówień:
  D/Q* = 10,000/1,000 = 10 zamówień/rok

Koszt całkowity:
  TC* = √(2·K·D·h) = √(2×100×10,000×2) = 2,000 PLN/rok
  
  (lub: TC = 100×10 + 2×500 = 1,000 + 1,000 = 2,000 PLN)
```

---

### 5. Model z punktem zamawiania (ROP)

```
┌─────────────────────────────────────────────────────────────────┐
│ REORDER POINT (ROP) - uwzględnienie lead time                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Poziom zapasu:                                                  │
│     │╲                      ╱╲                                 │
│     │  ╲                  ╱    ╲                               │
│     │    ╲              ╱        ╲                             │
│ ROP │──────╲──────────╲────────────╲──                        │
│     │        ╲      ╱  ╲          ╱  ╲                        │
│   SS│──────────╲──╱──────╲──────╱──────                       │
│   0 └────────────────────────────────→ t                       │
│              │←L→│                                              │
│          zamówienie  dostawa                                   │
│                                                                 │
│ ROP = d × L + SS                                               │
│                                                                 │
│ gdzie:                                                          │
│   d = średni popyt dzienny                                     │
│   L = lead time (czas dostawy)                                 │
│   SS = safety stock (zapas bezpieczeństwa)                    │
│                                                                 │
│ SS = z × σ_L                                                   │
│   z = współczynnik (z tablic normalnych, np. 1.65 dla 95%)    │
│   σ_L = odchylenie std popytu w czasie L                      │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6. Model (s, S) / (R, Q)

| Model | Opis |
|-------|------|
| **(s, Q)** | Zamów Q gdy poziom spadnie do s |
| **(s, S)** | Zamów do poziomu S gdy spadnie do s |
| **(R, S)** | Co R okresów uzupełnij do S |
| **(R, s, S)** | Co R okresów: jeśli ≤ s, uzupełnij do S |

```
Model (s, S):
  Poziom zapasu:
      S │╲
        │  ╲
        │    ╲
      s │──────╲──────────────╲──
        │        ╲          ╱  ╲
        │          ╲      ╱      ╲
      0 └────────────────────────→ t
               zamów    dostawa
               S-poziom

  Polityka: Gdy poziom ≤ s, zamów aby osiągnąć S
```

---

### 7. Vendor Managed Inventory (VMI)

```
┌─────────────────────────────────────────────────────────────────┐
│ VMI - Dostawca zarządza zapasami klienta                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Tradycyjnie:                                                    │
│   Klient → zamówienie → Dostawca → dostawa                     │
│                                                                 │
│ VMI:                                                            │
│   Klient → dane o zapasach/sprzedaży → Dostawca               │
│   Dostawca → decyzja o uzupełnieniu → Klient                  │
│                                                                 │
│ Korzyści:                                                       │
│ • Redukcja bullwhip effect                                     │
│ • Lepsza widoczność popytu                                     │
│ • Optymalizacja transportu                                      │
│ • Redukcja stockouts                                           │
│                                                                 │
│ Przykłady: Walmart-P&G, 7-Eleven-dostawcy                     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 8. Wskaźniki efektywności

| Wskaźnik | Formuła | Cel |
|----------|---------|-----|
| **Inventory Turnover** | COGS / Avg Inventory | Wyższy = lepszy |
| **Days of Inventory** | 365 / Turnover | Niższy = lepszy |
| **Fill Rate** | Zamówienia zrealizowane / Wszystkie | Wyższy |
| **Service Level** | P(brak stockout) | 95-99% |
| **GMROI** | Gross Margin / Avg Inventory | Wyższy |

---

## 🧠 Mnemoniki

### "EOQ = √(2KD/h)":
Economic Order Quantity - kwadrat z 2KD/h

### "ROP = d×L + SS":
Reorder Point = popyt w lead time + safety stock

### "Bullwhip = Bigger upstream":
Wahania rosną w górę łańcucha

---

## ❓ Pytania dodatkowe

### Q1: "Jak zredukować bullwhip effect?"
**Odpowiedź:** Współdzielenie informacji (POS data), VMI, CPFR (Collaborative Planning), redukcja lead times, stabilne ceny (EDLP), mniejsze partie (smaller batches), centralizacja decyzji.

### Q2: "EOQ vs JIT?"
**Odpowiedź:** EOQ: optymalizuje koszty przy danych K, h. JIT (Just-In-Time): redukuje K (częste małe dostawy), redukuje zapasy (Q→0). JIT wymaga: niskich setup costs, niezawodnych dostawców, stabilnego popytu.

### Q3: "Jak ustalić poziom zapasu bezpieczeństwa?"
**Odpowiedź:** SS = z × σ_L, gdzie z zależy od wymaganego service level (z=1.65 dla 95%, z=2.33 dla 99%). σ_L = σ_d × √L dla niezależnego popytu. Trade-off: wyższy SS = mniej stockouts, ale wyższe koszty.

---

## 🎯 Kluczowe punkty

1. **Bullwhip effect:** Amplifikacja wahań w łańcuchu
2. **Koszty:** Holding (h), Ordering (K), Shortage (p)
3. **EOQ:** Q* = √(2KD/h)
4. **ROP:** d×L + SS (uwzględnia lead time)
5. **VMI:** Dostawca zarządza zapasami klienta

---

## 📖 Źródła

1. Silver, Pyke, Peterson - "Inventory Management and Production Planning"
2. Chopra, Meindl - "Supply Chain Management"
3. Simchi-Levi - "Designing and Managing the Supply Chain"
