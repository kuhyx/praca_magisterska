# Pytanie 38: Projekcje grafów dwudzielnych

## Pytanie
**"Porównać metody projekcji grafów dwudzielnych. Przedstawić ich użyteczność w grupowaniu dokumentów tekstowych."**

Przedmiot: TASS (Technologie i Algorytmy dla Sieci Społecznościowych)

---

## 📚 Odpowiedź główna

### 1. Grafy dwudzielne (Bipartite Graphs)

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRAF DWUDZIELNY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    Zbiór U (np. dokumenty)     Zbiór V (np. słowa)             │
│                                                                 │
│         D1 ●────────────────● word1                            │
│            │ ╲              │                                   │
│         D2 ●──╲─────────────● word2                            │
│            │   ╲            │                                   │
│         D3 ●────╲───────────● word3                            │
│                  ╲          │                                   │
│         D4 ●──────╲─────────● word4                            │
│                                                                 │
│    Krawędzie tylko między U i V (nigdy wewnątrz zbioru)        │
│                                                                 │
│ Przykłady:                                                      │
│ • Dokumenty - Słowa                                             │
│ • Użytkownicy - Produkty                                        │
│ • Autorzy - Artykuły                                            │
│ • Aktorzy - Filmy                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Projekcja grafu dwudzielnego

```
┌─────────────────────────────────────────────────────────────────┐
│ PROJEKCJA = przekształcenie grafu dwudzielnego na jednomodowy  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Graf dwudzielny:           Projekcja na U (dokumenty):         │
│                                                                 │
│    D1 ●───────● w1              D1 ●─────● D2                  │
│       │╲      │                    │╲   ╱│                     │
│    D2 ●─╲─────● w2                 │ ╲ ╱ │                     │
│       │  ╲    │                    │  ╳  │                     │
│    D3 ●───╲───● w3                 │ ╱ ╲ │                     │
│              ╲                     │╱   ╲│                     │
│    D4 ●───────● w4              D3 ●─────● D4                  │
│                                                                 │
│ Dwa dokumenty połączone ⟺ mają wspólne słowo                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3. Metody projekcji

#### 3.1 Projekcja binarna (Simple/Unweighted)

```
Macierz sąsiedztwa projekcji:

P = B · Bᵀ  (dla projekcji na U)
P = Bᵀ · B  (dla projekcji na V)

gdzie B = macierz incydencji grafu dwudzielnego

Pᵢⱼ > 0 ⟹ węzły i, j połączone w projekcji

Wady:
❌ Utrata informacji o sile powiązania
❌ Wszystkie wspólni sąsiedzi traktowani równo
```

#### 3.2 Projekcja ważona (Weighted)

| Metoda | Waga krawędzi (i,j) | Opis |
|--------|---------------------|------|
| **Simple count** | w_ij = \|N(i) ∩ N(j)\| | Liczba wspólnych sąsiadów |
| **Jaccard** | w_ij = \|N(i) ∩ N(j)\| / \|N(i) ∪ N(j)\| | Normalizacja przez sumę |
| **Cosine** | w_ij = (B_i · B_j) / (\|\|B_i\|\| · \|\|B_j\|\|) | Podobieństwo wektorów |
| **Hyperbolic** | w_ij = Σ_k 1/(k_k - 1) | Rzadkie słowa ważniejsze |
| **Resource allocation** | w_ij = Σ_k 1/k_k | Jak hyperbolic |

```
Przykład - Jaccard:

D1 = {w1, w2, w3}
D2 = {w2, w3, w4}

Wspólne: {w2, w3} → |∩| = 2
Suma: {w1, w2, w3, w4} → |∪| = 4

w(D1, D2) = 2/4 = 0.5
```

#### 3.3 Projekcja TF-IDF (dla dokumentów)

```
┌─────────────────────────────────────────────────────────────────┐
│ TF-IDF weighted projection                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ TF(t,d) = częstość słowa t w dokumencie d                      │
│ IDF(t) = log(N / df(t))   gdzie df(t) = liczba dok. z t       │
│                                                                 │
│ TF-IDF(t,d) = TF(t,d) × IDF(t)                                 │
│                                                                 │
│ Podobieństwo dokumentów:                                        │
│ sim(d1, d2) = cos(TF-IDF(d1), TF-IDF(d2))                      │
│                                                                 │
│ Rzadkie słowa mają większą wagę (IDF)!                         │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. Porównanie metod

| Metoda | Zalety | Wady |
|--------|--------|------|
| **Binarna** | Prosta, szybka | Brak wag, utrata info |
| **Simple count** | Intuicyjna | Bias ku popularnym węzłom |
| **Jaccard** | Normalizowana | Ignoruje rozmiar zbiorów |
| **Cosine** | Standard w IR | Wymaga wektorów |
| **Hyperbolic** | Rzadkie elementy ważne | Bardziej złożona |
| **TF-IDF** | Standard dla tekstów | Specyficzna dla dokumentów |

---

### 5. Zastosowanie w grupowaniu dokumentów

```
┌─────────────────────────────────────────────────────────────────┐
│         PIPELINE GRUPOWANIA DOKUMENTÓW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. PREPROCESSING                                                │
│    Dokumenty → tokenizacja → stemming → usunięcie stop words   │
│                                                                 │
│ 2. BUDOWA GRAFU DWUDZIELNEGO                                   │
│    G = (Documents, Terms, Edges)                               │
│    Krawędź (d, t) jeśli term t występuje w dokumencie d       │
│                                                                 │
│ 3. PROJEKCJA                                                    │
│    P = projekcja ważona (TF-IDF/Cosine) na dokumenty           │
│                                                                 │
│ 4. GRUPOWANIE                                                   │
│    Na grafie projekcji:                                         │
│    • Community detection (Louvain, Label Propagation)          │
│    • Spectral clustering                                        │
│    • K-means na wektorach podobieństwa                         │
│                                                                 │
│ 5. WYNIK                                                        │
│    Grupy tematycznie podobnych dokumentów                      │
└─────────────────────────────────────────────────────────────────┘
```

#### Przykład

```
Dokumenty:
D1: "machine learning algorithms"
D2: "deep learning neural networks"  
D3: "neural network architecture"
D4: "database query optimization"
D5: "SQL query performance"

Graf dwudzielny projekcja (cosine similarity):

D1 ──0.3── D2 ──0.6── D3     Klaster 1: ML/DL
                              {D1, D2, D3}

D4 ──0.5── D5                 Klaster 2: Databases
                              {D4, D5}

Grupowanie znajdzie te dwa klastry!
```

---

### 6. Algorytmy grupowania na projekcji

```
┌─────────────────────────────────────────────────────────────────┐
│ LOUVAIN (Community Detection):                                  │
│ • Optymalizuje modularność Q                                   │
│ • Iteracyjne przenoszenie węzłów między grupami               │
│ • O(n log n) - szybki                                          │
├─────────────────────────────────────────────────────────────────┤
│ SPECTRAL CLUSTERING:                                            │
│ • Eigendecomposition Laplacianu                                │
│ • K-means na wektorach własnych                                │
│ • Znajduje struktury niekonweksowe                             │
├─────────────────────────────────────────────────────────────────┤
│ LABEL PROPAGATION:                                              │
│ • Propagacja etykiet po krawędziach                            │
│ • Bardzo szybki O(m)                                           │
│ • Niedeterministyczny                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7. Problemy i rozwiązania

| Problem | Opis | Rozwiązanie |
|---------|------|-------------|
| **Gęstość** | Projekcja tworzy gęste grafy | Threshold na wagi |
| **Huby** | Popularne słowa łączą wszystko | TF-IDF, filtering |
| **Skalowalność** | O(n²) krawędzi | Sparse representation, LSH |
| **Utrata info** | Projekcja traci strukturę | Zachowaj oryginalny graf |

---

## 🧠 Mnemoniki

### "B×Bᵀ = Projekcja":
Mnożenie macierzy incydencji daje projekcję

### "TF-IDF = Term Frequency × Inverse Document Frequency":
Rzadkie słowa ważniejsze

### "Jaccard = Intersection over Union":
IoU dla zbiorów

---

## ❓ Pytania dodatkowe

### Q1: "Dlaczego projekcja binarna jest problematyczna?"
**Odpowiedź:** Traci informację o sile powiązania. Dokument z 1 wspólnym słowem ma taką samą krawędź jak z 100 wspólnymi. Popularne słowa (stop words) tworzą fałszywe powiązania.

### Q2: "Jak skalować dla dużych zbiorów?"
**Odpowiedź:** MinHash/LSH dla approximate similarity, sparse matrix operations, sampling, dimension reduction (LSA/SVD), distributed computing (Spark GraphX).

### Q3: "Alternatywy dla projekcji?"
**Odpowiedź:** Bezpośrednie algorytmy na grafach dwudzielnych (bipartite community detection), tensor decomposition, embedding methods (node2vec), GNN na grafach heterogenicznych.

---

## 🎯 Kluczowe punkty

1. **Projekcja:** Graf dwudzielny → jednomodowy (P = B·Bᵀ)
2. **Metody:** Binarna, Jaccard, Cosine, TF-IDF
3. **TF-IDF:** Rzadkie słowa ważniejsze (IDF)
4. **Grupowanie:** Louvain, Spectral, Label Propagation
5. **Problem:** Gęstość, popularne węzły → filtering, thresholding

---

## 📖 Źródła

1. Newman - "Networks: An Introduction"
2. Zhou et al. - "Bipartite Network Projection and Personal Recommendation"
3. Manning - "Introduction to Information Retrieval"
