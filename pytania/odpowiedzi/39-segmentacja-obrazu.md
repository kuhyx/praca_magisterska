# Pytanie 39: Segmentacja obrazu

## Pytanie
**"Scharakteryzować problem segmentacji obrazu. Przedstawić podstawowe strategie i algorytmy segmentacji przy użyciu metod klasycznych oraz sieci neuronowych."**

Przedmiot: TWM (Techniki Wizji Maszynowej)

---

## 📚 Odpowiedź główna

### 1. Definicja problemu segmentacji

```
┌─────────────────────────────────────────────────────────────────┐
│                SEGMENTACJA OBRAZU                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Obraz wejściowy:              Maska segmentacji:              │
│  ┌────────────────┐            ┌────────────────┐              │
│  │  ░░████░░░░░░  │            │  ░░1111░░░░░░  │              │
│  │  ░████████░░░  │     →      │  ░11111111░░░  │              │
│  │  ░░████████░░  │            │  ░░11111111░░  │              │
│  │  ░░░░████░░░░  │            │  ░░░░1111░░░░  │              │
│  └────────────────┘            └────────────────┘              │
│                                                                 │
│  Cel: Przypisać każdemu pikselowi etykietę klasy/regionu       │
│                                                                 │
│  Typy segmentacji:                                              │
│  • Semantic: klasa dla każdego piksela (person, car, sky)      │
│  • Instance: rozróżnia instancje tej samej klasy               │
│  • Panoptic: semantic + instance (unified)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Metody klasyczne

#### 2.1 Thresholding (progowanie)

```
Globalne:
  pixel_out = 255 if pixel_in > T else 0

Otsu (automatyczny próg):
  - Maksymalizuje wariancję między klasami
  - σ²_between = w₀w₁(μ₀ - μ₁)²

Adaptacyjne:
  - Lokalny próg dla każdego regionu
  - T(x,y) = mean(neighborhood) - C

┌──────────────────┐    Threshold    ┌──────────────────┐
│░▒▓█░▒▓█░▒▓█░▒▓█  │ ────────────→  │░░██░░██░░██░░██  │
│▒▓█░▒▓█░▒▓█░▒▓█░  │       T        │░███░███░███░███░  │
└──────────────────┘                 └──────────────────┘
```

#### 2.2 Region Growing

```
Algorytm:
1. Wybierz punkt startowy (seed)
2. Badaj sąsiadów
3. Jeśli podobny (|I(neighbor) - I(region)| < threshold)
   → dodaj do regionu
4. Powtarzaj aż brak nowych pikseli

  Seed    Krok 1    Krok 2    Wynik
   ●        ●●       ●●●      ●●●●
            ●        ●●●      ●●●●
                     ●●       ●●●●
```

#### 2.3 Watershed

```
Obraz jako topografia:
- Intensywność = wysokość
- "Zalewanie" od minimów lokalnych
- Granice gdzie woda z różnych źródeł się spotyka

      ╱╲      ╱╲
     ╱  ╲    ╱  ╲
    ╱    ╲__╱    ╲
   ╱      ↑       ╲
  ↑    granica     ↑
 min1  (watershed) min2
```

#### 2.4 Mean Shift

```
Iteracyjne przesuwanie okna do maksimum gęstości:

1. Dla każdego piksela:
   m(x) = Σ K(x - xᵢ) × xᵢ / Σ K(x - xᵢ)
   
2. x ← m(x) (shift)
3. Powtarzaj do zbieżności
4. Piksele zbiegające do tego samego punktu → jeden segment
```

#### 2.5 Graph-based (Normalized Cuts)

```
Obraz jako graf:
- Wierzchołki = piksele
- Krawędzie = podobieństwo między pikselami
- w(i,j) = exp(-||I(i) - I(j)||² / σ²)

Normalized Cut:
  Ncut(A,B) = cut(A,B)/assoc(A,V) + cut(A,B)/assoc(B,V)

Minimalizacja Ncut → eigendecomposition Laplacianu
```

---

### 3. Porównanie metod klasycznych

| Metoda | Zalety | Wady |
|--------|--------|------|
| **Thresholding** | Szybki, prosty | Tylko 2 klasy, wrażliwy na oświetlenie |
| **Region Growing** | Intuicyjny | Wymaga seedów, over-segmentation |
| **Watershed** | Dobre krawędzie | Over-segmentation |
| **Mean Shift** | Brak k | Wolny, parametr bandwidth |
| **Graph Cut** | Globalnie optymalne | O(n³), wymaga unary terms |

---

### 4. Metody deep learning

#### 4.1 FCN (Fully Convolutional Network)

```
┌─────────────────────────────────────────────────────────────────┐
│ FCN - pierwsza architektura deep dla segmentacji (2015)        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Input     Encoder (VGG)      Decoder                   Output  │
│ H×W×3  →  Conv+Pool×5  →  Upsampling (deconv)  →  H×W×C       │
│                                                                 │
│ ┌────┐   ┌──┐   ┌──┐                    ┌────┐                 │
│ │    │ → │  │ → │  │ → ··· → upsample → │    │                 │
│ │    │   │  │   │  │          ×32       │    │                 │
│ └────┘   └──┘   └──┘                    └────┘                 │
│  input   conv   conv                    output                 │
│                                                                 │
│ Skip connections: FCN-32s, FCN-16s, FCN-8s                     │
│ Coarser + finer features → sharper boundaries                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2 U-Net

```
┌─────────────────────────────────────────────────────────────────┐
│ U-NET - encoder-decoder ze skip connections (2015)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│     Encoder              Decoder                               │
│       │                    ↑                                    │
│    ┌──┴──┐  ─ copy ─→  ┌──┴──┐                                │
│    │64×64│              │64×64│                                │
│    └──┬──┘              └──┬──┘                                │
│       ↓                    ↑                                    │
│    ┌──┴──┐  ─ copy ─→  ┌──┴──┐                                │
│    │32×32│              │32×32│                                │
│    └──┬──┘              └──┬──┘                                │
│       ↓                    ↑                                    │
│    ┌──┴──┐  ─ copy ─→  ┌──┴──┐                                │
│    │16×16│              │16×16│                                │
│    └──┬──┘              └──┬──┘                                │
│       ↓                    ↑                                    │
│       └───── bottleneck ───┘                                   │
│                                                                 │
│ Concat skip connections (nie add jak w ResNet)                 │
│ Popularne w medycynie (małe datasety)                          │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.3 DeepLab (v1-v3+)

```
┌─────────────────────────────────────────────────────────────────┐
│ DEEPLAB - Atrous/Dilated Convolutions + CRF                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Atrous Convolution (dilated):                                   │
│                                                                 │
│ Standard 3×3:        Atrous 3×3, rate=2:                       │
│ ● ● ●                ●   ●   ●                                 │
│ ● ● ●                              (większe receptive field    │
│ ● ● ●                ●   ●   ●      bez więcej parametrów)     │
│                                                                 │
│                      ●   ●   ●                                 │
│                                                                 │
│ ASPP (Atrous Spatial Pyramid Pooling):                         │
│ Parallel atrous conv z różnymi rates (6, 12, 18)              │
│ → multi-scale context                                          │
│                                                                 │
│ DeepLabv3+:                                                     │
│ Encoder-decoder + ASPP + depthwise separable conv              │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.4 Transformer-based (SegFormer, Mask2Former)

```
┌─────────────────────────────────────────────────────────────────┐
│ SEGFORMER (2021)                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Mix-Transformer encoder:                                       │
│ • Hierarchical features (1/4, 1/8, 1/16, 1/32)               │
│ • Efficient self-attention                                     │
│ • No positional encoding                                       │
│                                                                 │
│ MLP decoder:                                                    │
│ • Simple MLP combines multi-scale features                     │
│ • Lightweight                                                   │
│                                                                 │
│ MASK2FORMER (2022):                                            │
│ • Universal: semantic, instance, panoptic                      │
│ • Masked attention (per-segment)                               │
│ • Deformable attention                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

### 5. Porównanie architektur DL

| Architektura | mIoU (ADE20K) | Parametry | Cechy |
|--------------|---------------|-----------|-------|
| **FCN** | ~30% | ~135M | Pierwsze DL dla segmentacji |
| **U-Net** | - | ~31M | Medical, skip connections |
| **DeepLabv3+** | ~45% | ~60M | ASPP, dilated conv |
| **SegFormer-B5** | ~51% | ~85M | Transformer, efficient |
| **Mask2Former** | ~57% | ~200M | Universal, SOTA |

---

### 6. Loss functions

```
Cross-Entropy Loss:
  L = -Σᵢ Σc yᵢc log(pᵢc)
  
  Problem: class imbalance (dużo tła, mało obiektów)

Dice Loss:
  L = 1 - 2|X ∩ Y| / (|X| + |Y|)
  
  Bezpośrednio optymalizuje IoU-like metric

Focal Loss:
  L = -αₜ(1 - pₜ)^γ log(pₜ)
  
  γ > 0 → hard examples ważniejsze

Combined:
  L = λ₁ · CE + λ₂ · Dice
```

---

### 7. Metryki

| Metryka | Formuła | Opis |
|---------|---------|------|
| **Pixel Accuracy** | TP / (TP+FP+FN+TN) | % poprawnych pikseli |
| **IoU (Jaccard)** | TP / (TP+FP+FN) | Intersection over Union |
| **mIoU** | mean IoU per class | Standard dla segmentacji |
| **Dice** | 2TP / (2TP+FP+FN) | F1 dla segmentacji |

---

## 🧠 Mnemoniki

### "U-Net = U-shaped skip":
Kształt U z skip connections

### "ASPP = Atrous at Multiple Scales":
DeepLab's Atrous Spatial Pyramid Pooling

### "IoU = Intersection / Union":
Podstawowa metryka segmentacji

---

## ❓ Pytania dodatkowe

### Q1: "Jak radzić sobie z class imbalance?"
**Odpowiedź:** Weighted cross-entropy, Focal Loss, oversampling małych klas, Dice Loss (ignoruje dominację dużych klas), OHEM (Online Hard Example Mining).

### Q2: "U-Net vs DeepLab?"
**Odpowiedź:** U-Net: encoder-decoder z concat skip, dobre dla małych datasetów (medical). DeepLab: dilated conv zachowuje resolution, ASPP dla multi-scale, lepsze dla dużych datasetów.

### Q3: "Co to jest panoptic segmentation?"
**Odpowiedź:** Unified semantic + instance. Dzieli na "stuff" (nieczęściowe: sky, road) i "things" (policzalne: person, car). Każdy piksel ma class ID + instance ID.

---

## 🎯 Kluczowe punkty

1. **Klasyczne:** Thresholding, Region Growing, Watershed, Graph Cut
2. **FCN:** Pierwszy fully convolutional dla segmentacji
3. **U-Net:** Encoder-decoder + skip connections
4. **DeepLab:** Dilated/Atrous conv, ASPP
5. **Metryka:** mIoU (mean Intersection over Union)

---

## 📖 Źródła

1. Long et al. - "Fully Convolutional Networks" (2015)
2. Ronneberger et al. - "U-Net" (2015)
3. Chen et al. - "DeepLab" series (2014-2018)
4. Xie et al. - "SegFormer" (2021)
