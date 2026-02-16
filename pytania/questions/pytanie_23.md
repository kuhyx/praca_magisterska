## PYTANIE 23: Segmentacja obrazu

**Problem, strategie klasyczne i sieci neuronowe.**

---

### Tło pojęciowe — słowniczek

**Obraz cyfrowy (digital image)** — macierz pikseli. Obraz 1920×1080 = ~2 mln pikseli. Każdy piksel ma wartość (grayscale: 0-255) lub kanały RGB (3 × 0-255). Segmentacja operuje na tej macierzy.

**Piksel (pixel)** — najmniejsza jednostka obrazu. „Picture element." Segmentacja = przypisanie etykiety KAŻDEMU pikselowi.

**Segmentacja obrazu (image segmentation)** — podział obrazu na regiony, gdzie każdy piksel dostaje etykietę klasy (np. „samochód", „droga", „niebo"). Różni się od klasyfikacji (cały obraz → 1 etykieta) i detekcji (bounding box + etykieta).

**Czy naprawdę KAŻDY piksel?** Tak, w semantic segmentation wynik to mapa o IDENTYCZNYM rozmiarze jak obraz wejściowy. Obraz 640×480 → mapa 640×480, w której KAŻDY z 307 200 pikseli ma etykietę klasy. Żaden piksel nie jest pominięty. Nawet piksele „tła" dostają etykietę (np. klasa „background" lub „void"). W instance segmentation dodatkowo piksele tego samego obiektu dostają ten sam ID instancji.

    Obraz wejściowy:        640 × 480 pikseli (RGB, 3 kanały)
    Mapa segmentacji:       640 × 480 pikseli (1 kanał — numer klasy)
    Piksel (100, 200):      RGB=(134, 178, 210) → klasa 3 ("niebo")
    Piksel (320, 400):      RGB=(82, 79, 73)    → klasa 7 ("droga")
    KAŻDY piksel ma etykietę — nawet ten "nudny" fragment tła.

---

**Over-segmentation (nad-segmentacja)** — sytuacja, gdy algorytm segmentacji generuje ZBYT WIELE regionów — więcej niż jest obiektów/klas na obrazie. Jeden obiekt zostaje podzielony na kilka-kilkadziesiąt fragmentów. Problem typowy dla metod klasycznych (watershed, region growing).

    Obraz: jeden kubek na stole
    Idealna segmentacja: 2 regiony (kubek, tło)
    Over-segmentation:  47 regionów! (kubek podzielony na 12 kawałków,
                        stół na 20, tło na 15)

    Dlaczego to się dzieje?
    - Watershed: każde lokalne minimum jasności → osobny region → setki regionów
    - Region Growing: drobne różnice w intensywności → osobne regiony
    - Szum (noise) w obrazie → fałszywe granice

    Jak sobie z tym radzić?
    - **Markers/seeds:** zamiast automatycznych minimów → podaj ręczne punkty startowe
    - **Superpixels:** celowa nad-segmentacja na ~100-500 jednorodnych "superpikseli"
      (np. SLIC), potem GRUPOWANIE superpikseli w klasy → szybsze i stabilniejsze
    - **Hierarchiczne:** wielopoziomowa segmentacja → scalanie regionów bottom-up
    - **Deep learning:** sieci neuronowe uczą się "co jest obiektem" z danych → nie mają
      problemu z over-segmentation (bo wiedzą, że kubek to jeden obiekt)

**Under-segmentation (pod-segmentacja)** — przeciwieństwo: zbyt mało regionów, różne obiekty zlane w jeden region. Mniej typowy problem.

---

**Typy segmentacji:**

**Semantic segmentation** — każdy piksel → klasa, ale NIE rozróżnia instancji. Wszystkie samochody = jedna klasa „samochód".

    [samochód][samochód][droga][droga][pieszo][niebo]
    Dwa samochody = ta sama etykieta "samochód"

**Instance segmentation** — rozróżnia instancje tego samego obiektu. Samochód#1 i Samochód#2 mają różne etykiety.

**Panoptic segmentation** — łączy semantic + instance. Obiekty „things" (samochody, ludzie) mają instancje; „stuff" (niebo, droga) — tylko klasy.

---

**Thresholding (progowanie)** — najprostsza metoda segmentacji. Pomysł: każdy piksel ma wartość jasności (0=czarny, 255=biały). Wybierz PRÓG T: piksel > T → klasa 1 (obiekt), piksel ≤ T → klasa 0 (tło). Działa lepiej niż się wydaje na prostych obrazach (tekst na kartce, RTG, dokumenty).

    Obraz (jasność pikseli): [50][200][180][30][220][190]
    Próg T=128:
    50 ≤ 128 → 0 (tło)
    200 > 128 → 1 (obiekt)
    180 > 128 → 1
    30 ≤ 128 → 0
    Wynik:                   [ 0 ][ 1 ][ 1 ][ 0][ 1 ][ 1 ]

    Problem: JAK wybrać T? Ręcznie → subiektywne. Rozwiązanie → Otsu.

**Otsu** — automatyczny dobór progu. Algorytm: przetestuj WSZYSTKIE progi T=0..255, dla każdego oblicz wariancję wewnątrzklasową (jak „różnorodne" są piksele w klasie 0 i klasie 1). Wybierz T minimalizujące tę wariancję = klasy jak najbardziej jednorodne. Złożoność: O(n·L) gdzie n=piksele, L=poziomy jasności (256). Ograniczenie: działa TYLKO dla 2 klas i zakłada bimodalny histogram jasności (dwa „garby").

**Region Growing (rozrastanie regionu)** — zaczynasz od jednego piksela „ziarna" (seed) wybranego ręcznie lub automatycznie. Sprawdzasz sąsiadów: jeśli sąsiad jest PODOBNY (np. |jasność_sąsiada - jasność_regionu| < próg), dodaj go do regionu. Powtarzaj aż nie ma więcej podobnych sąsiadów. Następnie nowy seed → nowy region.

    Seed piksel (100,100) ma jasność 150
    Sąsiad (101,100) ma jasność 153 → |153-150|=3 < próg 10 → DODAJ
    Sąsiad (100,101) ma jasność 200 → |200-150|=50 > próg 10 → ODRZUĆ (granica!)
    Region rośnie jak „plama" od seeda

    Pseudokod:
    region = {seed}
    queue = [seed]
    while queue not empty:
        pixel = queue.pop()
        for neighbor in pixel.neighbors():  # 4 lub 8 sąsiadów
            if neighbor not visited AND similar(neighbor, region):
                region.add(neighbor)
                queue.append(neighbor)

    Problem: over-segmentation — drobne szumy → małe regiony

**Watershed (metoda zlewiska)** — traktuje obraz jak mapę topograficzną: wartość jasności piksela = wysokość terenu. Ciemne piksele = doliny, jasne = szczyty. Algorytm „zalewa" mapę wodą od najniższych punktów (minimów). Gdy woda z dwóch dolin się spotyka — tam jest GRANICA segmentu (grań).

    Obraz jako mapa wysokości:
        ████████
       ██      ██          ← jasne piksele = szczyty (granice)
      █   dolina  █
     █   (obiekt)  █
      █            █
       ██  dolina ██        ← kolejna dolina (inny segment)
        ████████

    Algorytm: zalewamy od dołu → woda spotyka się na graniach → SEGMENTY

    Problem: MASYWNA over-segmentation — każde lokalne minimum (nawet szum) → osobna dolina
    Rozwiązanie: marker-controlled watershed — ręcznie podaj „ziarna" (markers)
    zamiast zalewać od KAŻDEGO minimum

**Mean Shift** — iteracyjne przesuwanie okna (jądra) do punktu o najwyższej gęstości pikseli w przestrzeni cech. Cechy to np. (jasność, x, y) lub (R, G, B, x, y). Piksele, które zbiegają do tego samego maksimum gęstości, tworzą jeden segment. Wolny: O(n²), ale nie wymaga podania liczby segmentów.

    Wyobraź sobie rozsypane kulki na stole (= piksele w przestrzeni cech)
    Każda kulka „toczy się" w kierunku najbliższej „góry kulek" (max gęstości)
    Kulki, które dotoczyły się do tej samej góry → jeden segment

**Normalized Cuts** — modeluje obraz jako graf: piksele = węzły, krawędzie łączą sąsiednie piksele z wagą = PODOBIEŃSTWO (im bardziej podobne, tym wyższa waga). Szukamy CIĘCIA grafu (podział na grupy) minimalizującego stosunek ciętych krawędzi do rozmiaru grup. „Znormalizowane" → unika tworzenia malutkich segmentów. O(n³) — bardzo kosztowny: obraz 100×100 = 10 000 węzłów → 10¹² operacji!

---

**Sieć neuronowa (neural network)** — model uczenia maszynowego inspirowany biologicznymi neuronami. Składa się z warstw „neuronów" — każdy neuron oblicza ważoną sumę wejść + bias, przepuszcza przez funkcję aktywacji (np. ReLU = max(0,x)), i przekazuje wynik dalej. Sieć uczy się automatycznie z danych: dostaje pary (obraz, poprawna mapa segmentacji), dostosowuje wagi by minimalizować błąd.

    Neuron: output = ReLU(w₁·x₁ + w₂·x₂ + ... + wₙ·xₙ + bias)
    ReLU(x) = max(0, x)  — prosta, ale bardzo skuteczna funkcja aktywacji
    Uczenie: porównaj predykcję sieci z poprawną mapą (label) → oblicz błąd (loss)
             → backpropagation → aktualizuj wagi → powtórz miliony razy

**CNN (Convolutional Neural Network)** — sieć, której kluczowym elementem jest warstwa konwolucyjna (splotowa). Zamiast łączyć KAŻDY piksel z KAŻDYM neuronem (co byłoby niewykonalne — obraz 640×480 = 307 200 neuronów wejściowych!), CNN przesuwany mały filtr (np. 3×3 pikseli) po obrazie, obliczając w każdym miejscu iloczyn skalarny filtra z fragmentem obrazu.

    Co robi konwolucja? Filtr 3×3 „jedzie" po obrazie jak wycieraczka:

    Filtr (edge detector):    Fragment obrazu:    Wynik konwolucji:
    [-1  0  1]                [50  50 200]        (-1·50 + 0·50 + 1·200 +
    [-1  0  1]      *         [50  50 200]    =    -1·50 + 0·50 + 1·200 +
    [-1  0  1]                [50  50 200]         -1·50 + 0·50 + 1·200) = 450

    Duża wartość → tu jest KRAWĘDŹ (przejście ciemne→jasne)

    Hierarchia cech w CNN (wyuczona automatycznie!):
    Warstwa 1: krawędzie (|, —, /, \)
    Warstwa 2: tekstury (paski, siatki, plamy)
    Warstwa 3: części (koła, oczy, krawędź dachu)
    Warstwa 4+: obiekty (twarz, samochód, drzewo)

**Encoder-Decoder** — architektura segmentacji: encoder ZMNIEJSZA rozdzielczość obrazu (downsampling — pooling), wydobywając coraz bardziej abstrakcyjne cechy (krawędzie → tekstury → obiekty). Decoder ZWIĘKSZA rozdzielczość (upsampling — dekonwolucja lub interpolacja), odtwarzając mapę segmentacji o pełnej rozdzielczości.

    Encoder (zmniejsza):  [224×224] →pool→ [112×112] →pool→ [56×56] →pool→ [28×28] →pool→ [14×14]
    Decoder (zwiększa):   [14×14] →up→ [28×28] →up→ [56×56] →up→ [112×112] →up→ [224×224]

    Dlaczego nie sklasyfikować od razu KAŻDEGO piksela osobno?
    Bo pojedynczy piksel nie ma kontekstu — nie wiesz, czy piksel o wartości 150
    to fragment nieba czy samochodu. Encoder-decoder widzi KONTEKST (cały obiekt)
    i jednocześnie tworzy wynik o PEŁNEJ ROZDZIELCZOŚCI.

**Skip connections (połączenia skrótowe)** — połączenia „na skróty" łączące warstwy encodera z odpowiadającymi warstwami decodera. Problem: encoder traci detale przestrzenne (GDZIE dokładnie jest krawędź) podczas poolingu. Skip connections PRZENOSZĄ te detale z encodera wprost do decodera, umożliwiając precyzyjne granice segmentów.

    Bez skip connections: decoder „wie" ŻE tu jest samochód, ale granice są rozmyte
    Ze skip connections: decoder „wie" ŻE tu jest samochód AND DOKŁADNIE GDZIE jest krawędź

**FCN (Fully Convolutional Network, 2015)** — pierwsza sieć w pełni konwolucyjna do segmentacji. Kluczowa innowacja: **zastąpienie warstw fully-connected** (FC → stały rozmiar wejścia) **konwolucjami** (→ dowolny rozmiar wejścia). Klasyczny CNN (np. VGG, AlexNet) kończy się warstwami FC, które wymagają stałego rozmiaru (np. 224×224). FCN zamienia FC na Conv 1×1, co pozwala przetwarzać obraz o DOWOLNYM rozmiarze i zwracać mapę segmentacji.

    Klasyczny CNN:  Conv → Conv → Pool → ... → FC(4096) → FC(1000) → "kot"
    FCN:            Conv → Conv → Pool → ... → Conv1×1   → Upsample → mapa [H×W×C]
                                                  ↑ skip connections z encodera

**U-Net (2015)** — encoder-decoder w kształcie litery „U" ze skip connections realizowanymi przez **concatenation** (złączenie) — cechy z encodera są DOKLEJANE do cech decodera w odpowiedniej warstwie. Zaprojektowany dla segmentacji medycznej, gdzie zbiory danych są MAŁE (np. 30 zdjęć RTG), więc U-Net intensywnie używa data augmentation (obroty, odbicia, elastyczne deformacje).

    Encoder ──skip (concat)──→ Decoder
      ↓       ──skip (concat)──→   ↑
      ↓       ──skip (concat)──→   ↑
    bottleneck (najgłębsza warstwa)

    Dlaczego „U"? Bo wizualnie encoder schodzi w dół (↓), bottleneck na dole,
    decoder wraca do góry (↑) — tworząc kształt litery U.
    Dlaczego concat a nie dodawanie? Więcej informacji — encoder features + decoder features
    → sieć sama decyduje, które informacje wykorzystać.

**DeepLab v3+** — Google. Kluczowe innowacje:

**Atrous (dilated) convolutions** — konwolucje z „dziurami" (fr. à trous = z dziurami). Standardowy filtr 3×3 patrzy na 3×3 = 9 sąsiednich pikseli. Atrous convolution z rate=2 patrzy na piksele z odstępem 2 — efektywnie widzi 5×5 obszar, ALE używa TYCH SAMYCH 9 parametrów (wag). Większe receptive field (pole widzenia) za darmo!

    Zwykła konwolucja 3×3:   [x][x][x]         receptive field = 3×3
    Dilated (rate=2):        [x][ ][x][ ][x]   receptive field = 5×5, 9 parametrów!
    Dilated (rate=3):        [x][ ][ ][x][ ][ ][x]  receptive field = 7×7, 9 parametrów!

    Dlaczego to ważne? Segmentacja wymaga KONTEKSTU — żeby wiedzieć, że piksel to
    „droga", musisz zobaczyć otaczające budynki i niebo. Większe receptive field = więcej kontekstu.

**ASPP (Atrous Spatial Pyramid Pooling)** — równoległe zastosowanie atrous convolutions z WIELOMA rate (np. 6, 12, 18) + global average pooling, potem połączenie wyników. Każdy rate widzi kontekst w INNEJ skali → multi-scale features.

**Transformer-based (SegFormer, Mask2Former)** — najnowsze podejście zastępujące CNN transformerami. Kluczowy mechanizm: **self-attention** — każdy piksel „pyta" WSZYSTKIE inne piksele: „jak bardzo jesteś ze mną powiązany?" CNN widzi tylko lokalne okno (3×3, 5×5), a self-attention widzi CAŁY obraz naraz → lepsze rozumienie globalnych zależności (np. „ten piksel jest częścią tego samego samochodu co piksel 500 pikseli dalej"). Cena: O(n²) pamięci (n = liczba pikseli), ale jakość SOTA na benchmarkach.

---

**mIoU (mean Intersection over Union)** — standardowa metryka segmentacji. Dla każdej klasy: IoU = (piksele poprawne ∩ ground truth) / (piksele poprawne ∪ ground truth). Potem średnia z klas.

    Klasa "samochód": predykcja=100 pikseli, GT=120, wspólne=80
    IoU = 80 / (100+120-80) = 80/140 = 0.571 = 57.1%

**Dice Loss** — funkcja kosztu powiązana z IoU: 2·|A∩B| / (|A|+|B|). Popularna w segmentacji medycznej (dobrze radzi sobie z class imbalance).

**Focal Loss** — modyfikacja cross-entropy redukująca wpływ łatwych przykładów, skupiająca uczenie na trudnych. Kluczowa przy class imbalance (np. 99% tła, 1% obiekt).

**Receptive field** — ile wejścia „widzi" jeden neuron. Większe receptive field = kontekst globalny. Atrous convolutions zwiększają receptive field bez zwiększania parametrów.

---

### Problem: czym jest segmentacja obrazu?

Segmentacja obrazu to **przypisanie etykiety klasy KAŻDEMU pikselowi** obrazu. Wynik: mapa segmentacji o tym samym rozmiarze co obraz wejściowy, gdzie każdy piksel ma etykietę (np. „samochód", „droga", „niebo").

    Wejście:   obraz 640×480 (RGB)                    = 307 200 pikseli
    Wynik:     mapa 640×480, każdy piksel → etykieta   = 307 200 etykiet

    Obraz:           [niebo niebo niebo niebo]
                     [niebo drzewo drzewo niebo]
                     [droga droga samochód droga]
                     [droga droga droga   droga]

**Czym segmentacja NIE jest:**

    Zadanie              Wynik                          Granulacja
    ──────────────────────────────────────────────────────────────
    Klasyfikacja         1 etykieta na cały obraz       obraz
    Detekcja             bounding box + klasa            prostokąt
    Segmentacja          etykieta per piksel             piksel

**3 warianty segmentacji:**

![Typy segmentacji obrazu](img/segmentation_types.png)

| Wariant | Co robi | Przykład |
|---------|---------|----------|
| **Semantic** | klasa per piksel, bez rozróżniania instancji | wszystkie samochody = „samochód" |
| **Instance** | rozróżnia instancje tego samego obiektu | samochód#1, samochód#2 |
| **Panoptic** | semantic + instance razem | „stuff" (niebo) + „things" (samochód#1, #2) |

---

### Strategie klasyczne

Metody niewymagające uczenia maszynowego — oparte na ręcznie zdefiniowanych regułach (próg, podobieństwo, struktura grafu).

| Metoda | Idea | Wada | Złożoność |
|--------|------|------|-----------|
| **Thresholding** | piksel > T → klasa 1, else → klasa 0 | tylko 2 klasy, proste sceny | O(n) |
| **Otsu** | automatyczny próg (min wariancja wewnątrzklasowa) | j.w. ale dobiera T sam | O(n·L) |
| **Region Growing** | dodawaj sąsiednie piksele o podobnej wartości | over-segmentation, zależy od seeda | O(n) |
| **Watershed** | obraz = mapa wysokości, granice = granie gór | over-segmentation | O(n log n) |
| **Mean Shift** | iteracyjnie przesuwaj jądro do max gęstości | wolny | O(n²) |
| **Normalized Cuts** | piksele = węzły grafu, minimalizuj znormalizowane cięcie | bardzo wolny | O(n³) |

**Przykład — Thresholding (Otsu):**

    Obraz grayscale: [30][200][180][45][210][190]
    Otsu automatycznie dobiera próg T=128:
    Wynik:           [ 0 ][ 1 ][ 1 ][ 0][ 1 ][ 1 ]
    Zastosowanie: oddzielenie tekstu od tła (OCR), analiza zdjęć RTG

**Przykład — Watershed:**

    Obraz traktowany jako mapa topograficzna:
    Jasne piksele = szczyty,  ciemne = doliny
    "Zalewamy" od minimów → woda spotyka się na graniach → GRANICE segmentów
    Problem: za wiele minimów → over-segmentation → potrzeba markers

**Wspólna wada klasycznych metod:** wymagają ręcznego doboru parametrów (próg, seed, kernel), nie uczą się cech z danych, słabe na złożonych obrazach naturalnych.

---

### Sieci neuronowe (deep learning)

Metody uczące się automatycznie rozpoznawać cechy z danych treningowych. Wszystkie oparte na architekturze **encoder-decoder** z wariacjami.

**Wspólna idea encoder-decoder:**

    Encoder: obraz [224×224] → [112] → [56] → [28] → [14]   (wyciąga CECHY)
    Decoder: cechy [14] → [28] → [56] → [112] → [224×224]   (odtwarza MAPĘ)
                                   bottleneck

| Sieć | Rok | Kluczowa innowacja | Use case |
|------|-----|-------------------|----------|
| **FCN** | 2015 | w pełni konwolucyjna + skip connections | pierwsza end-to-end |
| **U-Net** | 2015 | U-shape + skip concat + data augmentation | segmentacja medyczna |
| **DeepLab v3+** | 2018 | atrous (dilated) conv + ASPP | general-purpose |
| **SegFormer** | 2021 | transformer encoder (self-attention) | SOTA lightweight |
| **Mask2Former** | 2022 | masked attention + unified architecture | SOTA universal |

**FCN (Fully Convolutional Network):**

    Zwykły CNN:  Conv → Conv → Pool → ... → FC → FC → "kot"
    FCN:         Conv → Conv → Pool → ... → Conv → Upsample → mapa pikseli
    Innowacja: zamiana FC na Conv → wejście dowolnego rozmiaru
    Skip connections: łączą cechy z encodera → zachowują detale przestrzenne

**U-Net:**

    Encoder (↓)         Decoder (↑)
    [64]────skip────→[64]        ← skip connections = concatenation
    [128]───skip───→[128]           (przenosi detale z encodera do decodera)
    [256]──skip──→[256]
    [512]─skip─→[512]
         [1024]                  ← bottleneck
    Dlaczego medycyna? Działa dobrze z MAŁYMI zbiorami danych (data augmentation)

**DeepLab v3+:**

    Zwykła konwolucja 3×3:   [x][x][x]         receptive field = 3
    Dilated (rate=2):        [x][ ][x][ ][x]   receptive field = 5, te same parametry!
    ASPP: równolegle rate=6,12,18 → multi-scale features → łączenie
    Efekt: widzi kontekst globalny BEZ zwiększania parametrów

**Transformery (SegFormer, Mask2Former):**

    CNN: filtr 3×3 widzi LOKALNY kontekst (sąsiadów)
    Transformer: self-attention widzi CAŁY obraz naraz
    Cena: O(n²) pamięci (n = piksele), ale lepsze wyniki

---

### Metryki i funkcje kosztu

| Metryka/Loss | Wzór | Kiedy użyć |
|-------------|------|------------|
| **mIoU** | mean(IoU per klasa) | standardowy benchmark |
| **Pixel Accuracy** | poprawne / wszystkie | prosta, ale zła przy class imbalance |
| **Dice Loss** | 1 - 2·\|A∩B\| / (\|A\|+\|B\|) | segmentacja medyczna |
| **Focal Loss** | -α(1-p)^γ · log(p) | class imbalance (99% tła) |

### Etymologia

**Segmentacja** — łac. „segmentum" = odcięty kawałek; podział obrazu na regiony. **Otsu** — Nobuyuki Otsu (1979); automatyczny dobór progu. **Watershed** — metafora: woda spływająca z grani do dolin (z geografii). **U-Net** — Ronneberger et al. (Freiburg, 2015); „U" od kształtu architektury. **FCN** — Fully Convolutional Network (Long, Shelhamer, Darrell, 2015). **DeepLab** — Google (2015–2018); „Atrous" z fr. „à trous" = „z dziurami" (dilated convolutions). **mIoU** — mean Intersection over Union.

### Jak zapamiętać

- **U-Net = „U-shape + skip connections"** — encoder-decoder
- **DeepLab = „Atrous (dilated) convolutions + ASPP"**
- **mIoU = Intersection / Union, uśrednione per klasa**

