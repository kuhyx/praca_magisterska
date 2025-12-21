# Pytanie 20: Rozpoznawanie mowy - HMM vs Deep Learning

## Pytanie
**"Przedstawić klasyczną metodę rozpoznawania mowy opartą o HMM (Ukryte Modele Markowa). Porównać ją z metodami korzystającymi z głębokich sieci neuronowych."**

Przedmiot: EASAR (Elementy Automatycznego Sterowania i Rozpoznawania)

---

## 📚 Odpowiedź główna

### 1. System rozpoznawania mowy - architektura

```
┌─────────────────────────────────────────────────────────────────┐
│  Sygnał audio                                                   │
│      ↓                                                          │
│  [Ekstrakcja cech] ──→ MFCC/Filterbanks                        │
│      ↓                                                          │
│  [Model akustyczny] ──→ HMM / DNN / Hybrid                     │
│      ↓                                                          │
│  [Model językowy] ──→ N-gram / RNN-LM                          │
│      ↓                                                          │
│  [Dekoder] ──→ Wyszukiwanie najlepszej hipotezy                │
│      ↓                                                          │
│  Tekst                                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. HMM (Hidden Markov Model) - klasyczne podejście

#### Struktura HMM dla fonemu

```
      a₁₂         a₂₃         a₃₄
  ┌────────→ ┌────────→ ┌────────→
  │          │          │
┌─┴─┐      ┌─┴─┐      ┌─┴─┐      ┌───┐
│ 1 │      │ 2 │      │ 3 │      │ 4 │
│   │      │   │      │   │      │END│
└─┬─┘      └─┬─┘      └─┬─┘      └───┘
  │          │          │
  └──────────┴──────────┘
     a₁₁        a₂₂        a₃₃ (self-loops)

Każdy stan emituje obserwacje (MFCC) według rozkładu GMM:
b_j(o) = Σ_m c_{jm} N(o; μ_{jm}, Σ_{jm})
```

#### Parametry HMM

| Symbol | Opis |
|--------|------|
| **A** | Macierz przejść (a_ij) |
| **B** | Rozkłady emisji (GMM) |
| **π** | Rozkład początkowy |

#### Trzy problemy HMM

| Problem | Algorytm | Zastosowanie |
|---------|----------|--------------|
| **Ewaluacja:** P(O\|λ) | Forward-Backward | Scoring |
| **Dekodowanie:** argmax P(Q\|O) | Viterbi | Rozpoznawanie |
| **Uczenie:** argmax P(O\|λ) | Baum-Welch (EM) | Trening |

#### Algorytm Viterbi

```
Znajdź najbardziej prawdopodobną sekwencję stanów:

α_t(j) = max_{i} [α_{t-1}(i) · a_{ij}] · b_j(o_t)

Backtrace: ψ_t(j) = argmax_{i} [α_{t-1}(i) · a_{ij}]

      t=1    t=2    t=3    t=4
s=1   ●──────●──────●──────●
      │╲     │╲     │╲     │
s=2   ●──────●──────●──────●
      │╲     │╲     │╲     │
s=3   ●──────●──────●──────●
              Viterbi trellis
```

---

### 3. Deep Learning w rozpoznawaniu mowy

#### DNN-HMM Hybrid (2012+)

```
┌─────────────────────────────────────────────────────────────────┐
│  Klasyczne GMM-HMM:                                             │
│  Cechy MFCC → GMM → P(o|stan) → HMM → dekodowanie              │
│                                                                 │
│  Hybrid DNN-HMM:                                                │
│  Cechy → DNN → P(stan|o) → P(o|stan) = P(stan|o)/P(stan)       │
│                    ↓                                            │
│                   HMM → dekodowanie                             │
│                                                                 │
│  DNN zastępuje GMM jako model emisji!                          │
└─────────────────────────────────────────────────────────────────┘
```

#### End-to-End Models (2014+)

```
CTC (Connectionist Temporal Classification):
┌──────────────────────────────────────────────────────────────┐
│  Audio → [LSTM/Transformer] → P(y_t|x) → CTC Loss → Tekst    │
│                                                               │
│  CTC pozwala na różne wyrównania:                            │
│  "h-e-l-l-o" = "hh-ee-ll-lo" = "-h-e-l-l-o-"                │
│  (blank = '-')                                                │
└──────────────────────────────────────────────────────────────┘

Attention-based (Seq2Seq):
┌──────────────────────────────────────────────────────────────┐
│  Audio → [Encoder] → [Attention] → [Decoder] → Tekst         │
│                         ↓                                     │
│                   Wyrównanie uczone                          │
│                                                               │
│  Modele: LAS (Listen Attend Spell), Transformer ASR          │
└──────────────────────────────────────────────────────────────┘
```

#### Transformer ASR (2020+)

```
Whisper, Wav2Vec 2.0, Conformer:

Audio waveform
     ↓
[CNN Feature Encoder]
     ↓
[Transformer Encoder] × N
     ↓
[CTC / Attention Decoder]
     ↓
Tekst

Pre-training: Self-supervised na dużych danych
Fine-tuning: Supervised na labeled data
```

---

### 4. Porównanie HMM vs DNN

| Aspekt | GMM-HMM | DNN-HMM | End-to-End |
|--------|---------|---------|------------|
| **Model akustyczny** | GMM | DNN | DNN |
| **Model czasowy** | HMM | HMM | CTC/Attention |
| **Wyrównanie** | Viterbi | Viterbi | Uczone/CTC |
| **Trening** | EM (Baum-Welch) | Backprop | Backprop |
| **Interpretowalność** | Wysoka | Średnia | Niska |
| **Dane treningowe** | Małe | Średnie | Duże |
| **WER (Word Error Rate)** | ~15-20% | ~8-12% | ~3-5% |
| **Latencja** | Niska | Średnia | Zmienna |

---

### 5. Ewolucja wydajności

```
WER na Switchboard (telefon):

Rok     Model              WER
2010    GMM-HMM           ~18%
2012    DNN-HMM           ~12%
2015    LSTM-HMM          ~8%
2017    LAS (Seq2Seq)     ~6%
2020    Conformer         ~4%
2023    Whisper Large     ~3%
        Poziom ludzki     ~4%
```

---

## 🧠 Mnemoniki

### "HMM = Hidden states + Markov + Model":
Ukryte stany, przejścia markowskie, emisje obserwacji

### "Viterbi = Find best path":
Dynamiczne programowanie dla najlepszej ścieżki

### "CTC = Collapse The Characters":
Usuwa powtórzenia i blanki → tekst

---

## ❓ Pytania dodatkowe

### Q1: "Co to jest forced alignment?"
**Odpowiedź:** Viterbi z ograniczeniem do znanej transkrypcji. Wyznacza granice czasowe fonemów/słów. Używane do tworzenia danych treningowych i TTS.

### Q2: "Dlaczego DNN jest lepszy od GMM?"
**Odpowiedź:** DNN może modelować złożone, nieliniowe zależności. GMM zakłada mieszaninę Gaussianów (często niewystarczające). DNN korzysta z kontekstu (wiele ramek na wejściu).

### Q3: "Co to jest language model fusion?"
**Odpowiedź:** Łączenie modelu akustycznego z językowym: P(W|O) ∝ P(O|W)·P(W)^α. Shallow fusion (podczas dekodowania) lub deep fusion (wspólny trening).

---

## 🎯 Kluczowe punkty

1. **HMM:** Stany ukryte, GMM emisje, Viterbi dekodowanie
2. **DNN-HMM Hybrid:** DNN zastępuje GMM, HMM dla czasu
3. **End-to-End:** CTC lub Attention, bez HMM
4. **Trend:** Większe modele, więcej danych, mniej inżynierii cech

---

## 📖 Źródła

1. Rabiner - "A Tutorial on HMM"
2. Hinton et al. - "Deep Neural Networks for Acoustic Modeling" (2012)
3. Graves et al. - "CTC" (2006)
4. Chan et al. - "LAS" (2016)
