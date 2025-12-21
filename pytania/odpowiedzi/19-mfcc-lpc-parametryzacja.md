# Pytanie 19: MFCC i LPC - parametryzacja sygnału mowy

## Pytanie
**"Przedstawić metody wyznaczania cech (parametryzacji) sygnału mowy: MFCC (cechy mel-cepstralne) i LPC (cechy według liniowej predykcji)."**

Przedmiot: EASAR (Elementy Automatycznego Sterowania i Rozpoznawania)

---

## 📚 Odpowiedź główna

### 1. Cel parametryzacji mowy

- **Redukcja wymiarowości:** 16kHz × 16bit → ~13-40 cech/ramkę
- **Ekstrakcja informacji fonetycznej**
- **Usunięcie informacji mówcy** (częściowo)
- **Reprezentacja kompaktowa** dla modeli (HMM, DNN)

---

### 2. MFCC (Mel-Frequency Cepstral Coefficients)

#### Pipeline MFCC

```
┌─────────────────────────────────────────────────────────────────┐
│  Sygnał mowy                                                    │
│      ↓                                                          │
│  [Pre-emphasis] ──→ y[n] = x[n] - α·x[n-1], α ≈ 0.97           │
│      ↓                                                          │
│  [Ramkowanie] ──→ 20-30ms ramki, 10ms przesunięcie             │
│      ↓                                                          │
│  [Okienkowanie] ──→ Hamming: w[n] = 0.54 - 0.46cos(2πn/N)      │
│      ↓                                                          │
│  [FFT] ──→ Widmo mocy |X(k)|²                                  │
│      ↓                                                          │
│  [Filtracja Mel] ──→ Bank filtrów trójkątnych (26-40)          │
│      ↓                                                          │
│  [Log] ──→ log(energia w pasmach)                              │
│      ↓                                                          │
│  [DCT] ──→ Discrete Cosine Transform                           │
│      ↓                                                          │
│  MFCC (12-13 współczynników)                                   │
└─────────────────────────────────────────────────────────────────┘
```

#### Skala Mel

```
Percepcja częstotliwości przez człowieka jest nieliniowa:

mel(f) = 2595 · log₁₀(1 + f/700)

Hz:    0    500   1000  2000  4000  8000
Mel:   0    607   1000  1500  2146  2840

      Bank filtrów Mel:
      ╱╲   ╱╲   ╱╲   ╱╲   ╱╲   ╱╲
     ╱  ╲ ╱  ╲ ╱  ╲ ╱  ╲ ╱  ╲ ╱  ╲
    ╱    ╳    ╳    ╳    ╳    ╳    ╲
   ──────────────────────────────────→ f
   0                              8000 Hz
   
   Filtry gęściej w niskich częstotliwościach
```

#### Cechy dynamiczne (Delta, Delta-Delta)

```
Δ MFCC (velocity):
Δc[t] = Σ_{n=1}^{N} n·(c[t+n] - c[t-n]) / (2·Σ n²)

ΔΔ MFCC (acceleration):
ΔΔc[t] = Δ(Δc[t])

Typowy wektor: 13 MFCC + 13 Δ + 13 ΔΔ = 39 cech
```

---

### 3. LPC (Linear Predictive Coding)

#### Idea

Model mowy jako filtr pobudzany:
- **Dźwięczne:** pobudzenie okresowe (struny głosowe)
- **Bezdźwięczne:** pobudzenie szumowe

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Pobudzenie e[n]     Filtr H(z)        Sygnał mowy s[n]       │
│        ┌───┐         ┌─────────┐                               │
│   ──→  │ G │ ──────→ │ 1/A(z)  │ ──────→                       │
│        └───┘         └─────────┘                               │
│                                                                 │
│   gdzie A(z) = 1 - Σ_{k=1}^{p} a_k z^{-k}                      │
│                                                                 │
│   Predykcja: ŝ[n] = Σ_{k=1}^{p} a_k s[n-k]                     │
│   Błąd:      e[n] = s[n] - ŝ[n]                                │
└─────────────────────────────────────────────────────────────────┘
```

#### Wyznaczanie współczynników LPC

**Metoda autokorelacji (Levinson-Durbin):**

```
1. Oblicz autokorelację: R[k] = Σ s[n]·s[n+k]

2. Algorytm Levinsona-Durbina:
   E₀ = R[0]
   for i = 1 to p:
       k_i = (R[i] - Σ_{j=1}^{i-1} a_{i-1,j}·R[i-j]) / E_{i-1}
       a_{i,i} = k_i
       for j = 1 to i-1:
           a_{i,j} = a_{i-1,j} - k_i·a_{i-1,i-j}
       E_i = (1 - k_i²)·E_{i-1}

3. Wynik: współczynniki a₁, a₂, ..., a_p
```

**Typowo:** p = 10-16 dla mowy (8kHz), p = 16-20 (16kHz)

#### Parametry pochodne LPC

| Parametr | Opis |
|----------|------|
| **Współczynniki LPC** | a₁, ..., a_p |
| **PARCOR (k)** | Współczynniki odbicia |
| **LSF/LSP** | Line Spectral Frequencies |
| **Cepstrum LPC** | Transformacja współczynników |

---

### 4. Porównanie MFCC vs LPC

| Cecha | MFCC | LPC |
|-------|------|-----|
| **Podstawa** | Percepcja słuchowa | Model produkcji mowy |
| **Filtracja** | Bank filtrów Mel | Model all-pole |
| **Wymiarowość** | 12-13 + delty | 10-20 |
| **Zastosowanie** | Rozpoznawanie mowy | Kodowanie, synteza |
| **Korelacja** | Niska (DCT dekoreluje) | Wysoka |
| **Interpolacja** | Trudna | Łatwa (LSF) |

---

### 5. Rozszerzenia

#### PLP (Perceptual Linear Prediction)
Łączy LPC z percepcją słuchową:
- Filtracja w skali Bark
- Krzywa równej głośności
- Kompresja intensity-loudness

#### Filter Banks (dla DNN)
Nowoczesne podejście:
- Log Mel filterbanks (bez DCT)
- 40-80 filtrów
- DNN uczy się własnych cech

---

## 🧠 Mnemoniki

### "MFCC = Mel + FFT + Cepstrum":
Skala Mel → FFT → Log → DCT

### "LPC = Linear Prediction Coefficients":
Przewiduj próbkę z p poprzednich

### "39 = 13 + 13 + 13":
MFCC + Delta + Delta-Delta

---

## ❓ Pytania dodatkowe

### Q1: "Dlaczego używamy skali Mel?"
**Odpowiedź:** Percepcja częstotliwości przez człowieka jest logarytmiczna. Różnica 100-200Hz jest bardziej słyszalna niż 4000-4100Hz. Mel modeluje tę nieliniowość.

### Q2: "Co to jest cepstrum?"
**Odpowiedź:** "Widmo widma" - IFFT(log(|FFT(x)|)). Rozdziela pobudzenie (pitch) od filtra (formantów). MFCC używa DCT zamiast IFFT dla lepszych właściwości.

### Q3: "Dlaczego LPC jest używane w kodowaniu mowy (CELP)?"
**Odpowiedź:** Kompaktowa reprezentacja (~10 współczynników). Łatwa interpolacja (LSF). Efektywna synteza (filtr IIR). Standard w GSM, VoIP.

---

## 🎯 Kluczowe punkty

1. **MFCC:** Pre-emphasis → Ramki → FFT → Mel → Log → DCT
2. **LPC:** Model all-pole, predykcja liniowa, Levinson-Durbin
3. **Wymiary:** MFCC ~39, LPC ~10-20
4. **MFCC** dla rozpoznawania, **LPC** dla kodowania/syntezy

---

## 📖 Źródła

1. Rabiner, Schafer - "Digital Processing of Speech Signals"
2. Huang et al. - "Spoken Language Processing"
3. HTK Book - Feature extraction
