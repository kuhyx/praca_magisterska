## PYTANIE 24: Detekcja obiektów

**Problem, metody klasyczne, deep learning. Jak zbudować detektor z klasyfikatora?**

---

### Tło pojęciowe — słowniczek

**Detekcja obiektów (object detection)** — zadanie widzenia komputerowego: zlokalizuj obiekty na obrazie (bounding box) i przypisz im klasy (samochód, pieszo, kot...). Wynik: lista (klasa, prostokąt, pewność). Trudniejsze niż klasyfikacja (→ cały obraz, 1 label), ale łatwiejsze niż segmentacja (→ per piksel).

    Klasyfikacja:  "To zdjęcie zawiera kota"
    Detekcja:      "Kot w prostokącie (50,30)-(200,180), pewność 95%"
    Segmentacja:   Maska pikseli kota

**Bounding box (prostokąt ograniczający, bbox)** — prostokąt opisujący położenie obiektu. Zwykle: (x_min, y_min, x_max, y_max) lub (x_center, y_center, width, height). Przybliżenie — obiekty rzadko są prostokątne.

**Confidence (pewność)** — wynik 0-1 mówiący jak pewny jest detektor, że wykrył obiekt danej klasy. Zwykle próg np. 0.5: detiekcje poniżej odrzucane.

---

**Klasyfikator (classifier)** — model przypisujący etykietę do wejścia. Np. CNN trenowany na ImageNet: obraz → „kot" (+ prawdopodobieństwo). SAM nie lokalizuje — mówi tylko co jest na obrazie. Pytanie brzmi: jak z takiego modelu zbudować detektor?

**Sliding window (okno przesuwane)** — najprostsza metoda budowy detektora z klasyfikatora: wytnij prostokątny fragment obrazu (wiele rozmiarów, wiele pozycji), każdy fragment sklasyfikuj. Jeśli „pozytywny" → detekcja. Ekstremalnie wolne: tysiące fragmentów × klasyfikacja per fragment.

    [okno 64×64] przesuwa się po obrazie 640×480:
    (640-64)×(480-64) ≈ ~240 000 pozycji × wiele skal = MILIONY klasyfikacji!

---

**HOG (Histogram of Oriented Gradients)** — klasyczny deskryptor cech wizualnych. Rozbijmy nazwę:

- **Gradient** — w kontekście obrazu to „kierunek i siła zmiany jasności" w danym pikselu. Oblicza się go jako różnicę jasności sąsiednich pikseli. Gradient wskazuje KRAWĘDZIE — tam, gdzie jasność zmienia się szybko.

      Piksel:           [50] [50] [200]       ← nagły skok jasności
      Gradient w x:      0    150              ← duży gradient = KRAWĘDŹ!
      Gradient w y:      obliczany analogicznie (góra/dół)
      Kierunek krawędzi: arctan(gy/gx) ← np. 0° = pionowa, 90° = pozioma

- **Orientacja (Oriented)** — kierunek gradientu. Gradient ma KĄTP (0°–180°): krawędź pionowa = ~0°, pozioma = ~90°, ukośna = ~45°.

- **Histogram** — zliczenie „ile pikseli ma gradient w danym kierunku". Dla komórki 8×8 pikseli liczymy histogram 9 binów (co 20°: 0°, 20°, 40°, ..., 160°).

- **HOG pipeline krok po kroku:**

      Krok 1: Oblicz gradient KAŻDEGO piksela (Gx, Gy → magnitude + direction)
                Gx = pixel[x+1] - pixel[x-1]
                Gy = pixel[y+1] - pixel[y-1]
                magnitude = √(Gx² + Gy²)
                direction = arctan(Gy / Gx)

      Krok 2: Podziel obraz na komórki (cells) 8×8 pikseli
                Okno 64×128 → 8×16 komórek

      Krok 3: Dla każdej komórki stwórz histogram 9 binów (0°-180°, co 20°)
                Każdy piksel w komórce „głosuje" na bin odpowiadający jego kierunkowi
                z wagą = magnitude (silniejsze krawędzie głosują mocniej)

      Krok 4: Normalizuj histogramy w blokach 2×2 komórek (16×16 px)
                → odporność na zmiany oświetlenia

      Krok 5: Połącz wszystkie histogramy w jeden wektor cech
                Okno 64×128: (8-1)×(16-1) = 7×15 = 105 bloków × 4 komórki × 9 binów = 3780 cech

      Wynik: wektor 3780 liczb = „odcisk palca" kształtu w oknie
      Sylwetka człowieka → charakterystyczny wzorzec kierunków krawędzi

**Pseudokod HOG:**

      def compute_hog(window_64x128):
          gradients = compute_gradients(window)     # Gx, Gy per pixel
          magnitudes = sqrt(Gx**2 + Gy**2)
          directions = arctan2(Gy, Gx) * 180 / pi   # kąt w stopniach

          hog_vector = []
          for block in sliding_blocks_2x2(cells_8x8):
              block_hist = []
              for cell in block.four_cells():
                  hist = zeros(9)                    # 9 binów
                  for pixel in cell.pixels():
                      bin_idx = int(directions[pixel] / 20)
                      hist[bin_idx] += magnitudes[pixel]
                  block_hist.append(hist)
              block_hist = normalize(concatenate(block_hist))  # L2-norm
              hog_vector.extend(block_hist)

          return hog_vector   # 3780-dim vector

**SVM (Support Vector Machine)** — klasyczny klasyfikator binarny (2 klasy: „tak/nie", „pieszy/nie-pieszy"). Pomysł:

- Dane treningowe to punkty w przestrzeni wielowymiarowej (np. wektory HOG 3780-dim)
- Każdy punkt ma etykietę: +1 (pozytywna klasa) lub -1 (negatywna)
- SVM szuka **hiperpłaszczyzny** (w 2D to linia, w 3D to płaszczyzna) najlepiej SEPARUJĄCEJ dwie klasy

**Czym jest hiperpłaszczyzna?** W 2D: linia dzieląca punkty na dwie grupy. W 3D: płaszczyzna. W N wymiarach: (N-1)-wymiarowa „ściana".

**Margines (margin)** — odległość od hiperpłaszczyzny do najbliższego punktu danych. SVM MAKSYMALIZUJE margines → najlepsza generalizacja.

**Support Vectors** — punkty danych NAJBLIŻSZE hiperpłaszczyźnie. To one „podpierają" (support) margines i definiują pozycję hiperpłaszczyzny. Reszta punktów jest nieistotna! Nazwa: „wektory nośne" — bo to wektory cech, które „niosą" decyzję.

      Przestrzeń 2D:          O = klasa "pie szy"   X = klasa "nie-pieszy"
                              O     O
                               O   O
      hiperpłaszczyzna →  ─ ─ ─ ─ ─ ─ ─ ─  ← margines ↕
                              X    X
                               X  X    X

      Support vectors: O i X najbliższe linii (zaznaczone pogrubione)
      SVM: przesuń linię tak, żeby margines ↕ był MAKSYMALNY

**HOG+SVM — klasyczny pipeline detekcji pieszych:**

![HOG + SVM pipeline detekcji pieszych](img/hog_svm_pipeline.png)

      1. Sliding window (okno 64×128) przesuwa się po obrazie
      2. Dla każdej pozycji okna:
         a) Oblicz HOG → wektor 3780 cech
         b) SVM klasyfikuje: „pieszy" (+1) lub „nie-pieszy" (-1)
      3. NMS (Non-Maximum Suppression) → usuń duplikaty
      4. Wynik: lista bounding boxów z detekcjami pieszych

**Viola-Jones (2001)** — przełomowy detektor twarzy real-time. Kluczowe innowacje:
- **Haar features** — proste cechy prostokątne (jasne/ciemne regiony)
- **Integral Image** — obliczenie dowolnej sumy prostokąta w O(1)!
- **AdaBoost cascade** — kaskada klasyfikatorów: szybkie odrzucenie 99% okien w pierwszych etapach, szczegółowa analiza tylko obiecujących

---

![Ewolucja detektorów: R-CNN → Faster R-CNN → YOLO](img/rcnn_evolution.png)

**R-CNN family (two-stage detectors)** — dwuetapowe: najpierw generuj propozycje regionów, potem klasyfikuj każdy region.

**Czym jest „region proposal" (propozycja regionu)?** — prostokąt, w którym MOŻE BYĆ obiekt. Zamiast sprawdzać miliony pozycji okna (sliding window), algorytm propozycji generuje ~2000 „obiecujących" prostokątów. Jak? Metoda Selective Search analizuje kolory, tekstury i rozmiary → łączy podobne regiony → generuje kandydatów.

**R-CNN (2014, Ross Girshick)** — pierwszy detektor oparty na CNN. Pipeline:

    Krok 1: Selective Search → ~2000 regionów-kandydatów (prostokątów)
    Krok 2: Dla KAŻDEGO z 2000 regionów:
            a) Wytnij prostokąt z obrazu, przeskaluj do 224×224
            b) Przepuść przez CNN (np. AlexNet) → wektor cech 4096-dim
            c) SVM klasyfikuje: „samochód? kot? tło?"
    Krok 3: Bbox regression — doprecyzuj pozycję prostokąta
    Krok 4: NMS — usuń duplikaty

    Problem: 2000 × CNN forward pass = 50 SEKUND na obraz! (2000 razy odpalasz CNN)
    Dlaczego tak wolno? Bo CNN liczy cechy na KAŻDYM wyciętym regionie OSOBNO,
    choć regiony się częściowo nakładają → redundantne obliczenia

**Fast R-CNN (2015)** — kluczowa optymalizacja: przepuść cały obraz przez CNN RAZ, uzyskaj „mapę cech" (feature map). Potem wytnij cechy regionów z tej mapy (ROI Pooling), zamiast odpalać CNN 2000 razy.

    Dlaczego „ROI Pooling"? ROI = Region of Interest. Regiony mają RÓŻNE rozmiary,
    ale warstwa FC wymaga stałego. ROI Pooling dzieli region na siatkę np. 7×7
    i w każdej komórce bierze MAX → stały rozmiar wyjścia niezależnie od wejścia.

    CNN raz na obraz → feature map → ROI Pool 2000 regionów → FC → klasy + bbox
    Przyspieszenie: ~2 sec/obraz (vs 50 sec w R-CNN)

**Faster R-CNN (2015)** — ostatni krok: zastąp Selective Search (osobny algorytm) siecią neuronową! **RPN (Region Proposal Network)** — mała sieć przesuwana po feature mapie, która w KAŻDEJ pozycji predykuje: „czy tu jest obiekt?" + proponuje bbox. Wszystko w jednej sieci, end-to-end.

    Obraz → CNN backbone (np. ResNet) → Feature Map → RPN (proposals) → ROI Pool → FC → klasy + bbox

    RPN szczegóły:
    - W każdym punkcie feature mapy rozważ k=9 „anchor boxes" (3 rozmiary × 3 proporcje)
    - Dla każdego anchora: P(obiekt) + przesunięcie bbox (Δx, Δy, Δw, Δh)
    - Zachowaj ~300 propozycji z najwyższym P(obiekt) → do ROI Pool

    Faster R-CNN: ~5 fps (~0.2 sec/obraz) — 250× szybciej niż R-CNN!

---

**One-stage detectors** — klasyfikacja i lokalizacja w jednym przejściu (bez osobnego etapu propozycji). Szybsze, ale historycznie mniej precyzyjne.

**YOLO (You Only Look Once, 2016)** — rewolucyjny pomysł: „po co robić 2 etapy, skoro można w JEDNYM?" Obraz dzielony jest na siatkę S×S (np. 13×13 = 169 komórek). Każda komórka odpowiada za wykrycie obiektu, którego ŚRODEK wpada w tę komórkę. Każda komórka predykuje:
- B bounding boxów × (x, y, w, h, confidence) = lokalizacja + „pewność, że tu jest obiekt"
- C prawdopodobieństw klas = „jaki to obiekt?"
Jedno przejście przez sieć → WSZYSTKIE detekcje naraz. 45-155 fps!

    Jak to działa wizualnie (S=7, B=2, C=20 klas jak w Pascal VOC):

    Obraz [448×448] → CNN (24 warstwy konwolucyjne + 2 FC) → tensor 7×7×30
                                                                ↑
                                                    30 = 2×(4+1) + 20
                                                    2 bbox × (x,y,w,h,conf) + 20 klas

    Komórka (3,4) predykuje: bbox1=(0.3, 0.7, 0.4, 0.6, 0.92), klasa="samochód" (p=0.88)
    → „środek samochodu jest w komórce (3,4), bbox ma takie wymiary, pewność 92%"

    Potem NMS: usuwa duplikaty (wiele komórek może wykryć ten sam obiekt)

**SSD (Single Shot MultiBox Detector, 2016)** — ulepsza YOLO przez multi-scale feature maps: predykcje z WIELU warstw CNN, każda o innej rozdzielczości. Wczesne warstwy (wysoka rozdzielczość) wykrywają MAŁE obiekty; późne warstwy (niska rozdzielczość) wykrywają DUŻE. Anchor boxes predefiniowane na każdej skali.

**Anchor box (kotwica)** — predefiniowany prostokąt o określonym kształcie/proporcji (np. 1:1, 1:2, 2:1). Sieć NIE predykuje bbox od zera — predykuje PRZESUNIĘCIE (offset) od najbliższego anchora. Łatwiejsze zadanie! Wiele anchorów → pokrycie różnych kształtów obiektów (osoby = wysoki prostokąt, samochód = szeroki).

**Anchor-free** — nowoczesne podejście (FCOS, YOLOv8): bezpośrednia predykcja środka i wymiarów, bez predefiniowanych anchorów. Prostsza architektura, mniej hyperparametrów.

**DETR (DEtection TRansformer, 2020)** — Facebook AI. Zamiast CNN + anchor + NMS, używa **transformera** z mechanizmem self-attention. Predykuje bezpośrednio ZESTAW obiektów (set prediction, nie grid). NIE potrzebuje NMS (unik duplikatów rozwiązany przez Hungarian matching w treningu). Najprostsza architektura w detekcji, ale wolniejsza w treningu.

---

**NMS (Non-Maximum Suppression)** — post-processing: detektor generuje wiele nakładających się bbox dla tego samego obiektu. NMS: weź najlepszą (max confidence), usuń wszystkie mocno nakładające się (IoU > prog), powtórz.

    Detections: [bbox1, 0.95], [bbox2, 0.90], [bbox3, 0.85]  (nakładające się)
    NMS: zachowaj bbox1 (0.95), usuń bbox2 i bbox3 (IoU > 0.5 z bbox1)

**IoU (Intersection over Union)** — miara nakładania dwóch bbox: pole przecięcia / pole sumy. IoU=1 → identyczne; IoU=0 → brak nakładania. Próg NMS typowo 0.5.

**Backbone** — sieć bazowa (np. ResNet, VGG) wyciągająca cechy z obrazu. Detection head (głowa detekcyjna) jest dodawana „na wierzch" backbone i predykuje bbox + klasy. Fine-tuning backbone na detekcję = transfer learning.

---

**Jak zbudować detektor z klasyfikatora? Trzy podejścia:**
1. **Sliding window** — wytnij, sklasyfikuj, NMS. Bardzo wolne.
2. **Region proposals + klasyfikator** — Selective Search generuje ~2000 regionów, sklasyfikuj każdy + NMS. Szybsze.
3. **Fine-tune backbone** — weź pretrained classifier (np. ResNet z ImageNet), dodaj detection head (bbox regression + cls), dotrenuj na danych detekcyjnych. **Najlepsza jakość.**

**DETR (DEtection TRansformer, 2020)** — Facebook AI. Transformer zamiast CNN, bezpośrednia predykcja zestawu obiektów (set prediction), bez NMS. Uproszczona architektura.

---

### Problem: czym jest detekcja obiektów?

Detekcja obiektów to **lokalizacja** (gdzie?) i **klasyfikacja** (co?) obiektów na obrazie. Wynik: lista krotek **(klasa, bounding box, confidence)**.

    Wejście:   zdjęcie ulicy
    Wynik:     [("samochód", [50,30,200,180], 0.95),
                ("pieszy",   [300,100,350,250], 0.88),
                ("rower",    [400,150,480,300], 0.72)]

**Porównanie z innymi zadaniami:**

    Zadanie           Wynik                        Przykład
    ─────────────────────────────────────────────────────────
    Klasyfikacja      "kot" (1 etykieta)           cały obraz → 1 klasa
    Detekcja          bbox + klasa (N obiektów)    prostokąty wokół obiektów
    Segmentacja       etykieta per piksel          maska pikseli

---

### Metody klasyczne

Metody sprzed deep learningu — ręcznie projektowane cechy (features) + klasyczny klasyfikator.

| Metoda | Rok | Cechy | Klasyfikator | Szybkość | Use case |
|--------|-----|-------|-------------|----------|----------|
| **HOG + SVM** | 2005 | Histogram of Oriented Gradients | SVM | wolna (~1 fps) | detekcja pieszych |
| **Viola-Jones** | 2001 | Haar features + Integral Image | AdaBoost cascade | real-time (30+ fps) | detekcja twarzy |

**HOG + SVM (Dalal & Triggs, 2005):**

    Pipeline:  Obraz → Sliding window → HOG (histogramy gradientów) → SVM → detekcja/brak
    HOG: dzieli okno na komórki (8×8 px), liczy histogramy kierunków krawędzi
    SVM: "czy ten wzorzec krawędzi to człowiek?"
    Wada: ręczne cechy, wolny sliding window, działa dobrze TYLKO na pieszych

**Viola-Jones (2001) — 3 innowacje:**

    1. Haar features:    [ jasne | ciemne ]  → prosta różnica intensywności
    2. Integral Image:   suma prostokąta w O(1), niezależnie od rozmiaru!
    3. Cascade:          Etap 1 (2 cechy): odrzuca 50% okien w 1 μs
                         Etap 2 (10 cech): odrzuca 80% reszty
                         ...Etap 25 (200 cech): szczegółowa analiza TYLKO 0.01% okien
    Efekt: ~95% detections = szybkie odrzucenia → real-time!

---

### Deep learning

**Two-stage detectors (dwuetapowe)** — najpierw generuj propozycje regionów, potem klasyfikuj.

| Model | Rok | Propozycje | Szybkość | Innowacja |
|-------|-----|-----------|----------|----------|
| **R-CNN** | 2014 | Selective Search (~2000) | 50 sec/img (!) | CNN per region |
| **Fast R-CNN** | 2015 | Selective Search | ~2 sec/img | CNN raz + ROI Pooling |
| **Faster R-CNN** | 2015 | RPN (w sieci!) | ~5 fps | Region Proposal Network |

    Ewolucja R-CNN:
    R-CNN:       [Selective Search] → 2000 × [CNN] → 2000 × [SVM]    = 50s WOLNE!
    Fast R-CNN:  [CNN raz] → [ROI Pool 2000 regionów] → [FC]          = 2s lepiej
    Faster R-CNN:[CNN] → [RPN generuje propozycje] → [ROI Pool] → [FC] = 0.2s!

**One-stage detectors (jednoetapowe)** — klasyfikacja i lokalizacja w JEDNYM przejściu.

| Model | Rok | Szybkość | Innowacja |
|-------|-----|----------|----------|
| **YOLO** | 2016 | 45-155 fps | siatka S×S, jedno przejście |
| **SSD** | 2016 | 46-59 fps | multi-scale feature maps |
| **YOLOv8** | 2023 | 100+ fps | anchor-free, SOTA |
| **DETR** | 2020 | ~40 fps | transformer, bez NMS |

    YOLO:
    Obraz [416×416] → siatka 13×13 → każda komórka predykuje:
      - B bounding boxów (pozycja + rozmiar + confidence)
      - C klas (prawdopodobieństwa)
    Jedno forward pass → WSZYSTKIE detekcje naraz → NMS → wynik

**Two-stage vs One-stage:**

    Cecha              Two-stage (Faster R-CNN)    One-stage (YOLO)
    ─────────────────────────────────────────────────────────────────
    Szybkość           ~5 fps                      45-155 fps
    Dokładność (mAP)   wyższa (historycznie)        dorównuje (YOLOv8)
    Małe obiekty       lepszy                       gorszy (ale SSD/FPN pomaga)
    Architektura       2 etapy + NMS                1 etap + NMS (DETR: bez NMS)
    Real-time?         nie                          TAK

---

### Jak zbudować detektor z klasyfikatora?

Masz wytrenowany klasyfikator (np. ResNet na ImageNet: obraz → „kot"). Jak go użyć do **lokalizacji** obiektów?

**Podejście 1 — Sliding Window (najwolniejsze):**

    Wytnij okno → klasyfikuj → przesuń → powtórz → NMS
    Obraz 640×480, okno 64×64, krok 8px, 5 skal:
    ~240 000 pozycji × 5 skal = ~1 200 000 klasyfikacji!
    Przy 100 cls/sec → 3.3 godziny na 1 obraz → NIEPRAKTYCZNE

**Podejście 2 — Region Proposals + Klasyfikator (szybsze):**

    Selective Search → ~2000 regionów (zamiast milionów)
    Każdy region → resize → klasyfikator → wynik + NMS
    Przy 100 cls/sec → 20 sec/obraz → lepiej, ale wciąż wolno
    To jest dokładnie R-CNN (2014)

**Podejście 3 — Fine-tune backbone + detection head (najlepsze):**

    Pretrained classifier (ResNet):  obraz → cechy → FC → "kot"
    Zamień FC na detection head:
      obraz → cechy (backbone) → [cls head: P(klasa)]
                                → [bbox head: Δx, Δy, Δw, Δh]
    Dotrenuj na danych z bounding boxami (COCO, VOC)
    = Transfer learning → NAJLEPSZA jakość + szybkość
    To jest Faster R-CNN, YOLO, SSD — wszystkie używają pretrained backbone!

    Podsumowanie:
    Sliding Window:    ~milion klasyfikacji → NIEPRAKTYCZNE
    Region Proposals:  ~2000 klasyfikacji  → wolne ale działa (R-CNN)
    Fine-tune:         1 przejście sieci   → szybkie i dokładne (Faster R-CNN, YOLO)

---

### NMS (Non-Maximum Suppression) — post-processing

    Detektor generuje WIELE nakładających się bbox dla jednego obiektu:
    [bbox1, 0.95], [bbox2, 0.90], [bbox3, 0.85] — wszystkie na tym samym kocie

    Algorytm NMS:
    1. Sortuj po confidence: [0.95, 0.90, 0.85]
    2. Weź najlepszą (0.95) → ZACHOWAJ
    3. Oblicz IoU z resztą: IoU(bbox1,bbox2)=0.82, IoU(bbox1,bbox3)=0.75
    4. Usuń te z IoU > próg (0.5): usuń bbox2 i bbox3
    5. Powtórz dla następnej najlepszej
    Wynik: 1 bbox per obiekt

### Etymologia

**YOLO** — You Only Look Once (Joseph Redmon et al., 2016). **R-CNN** — Region-based CNN (Ross Girshick, 2014). **HOG** — Histogram of Oriented Gradients (Dalal & Triggs, 2005). **SVM** — Support Vector Machine (Vapnik, 1995). **Viola-Jones** — Paul Viola + Michael Jones (2001). **DETR** — DEtection TRansformer (Facebook AI, 2020). **SSD** — Single Shot MultiBox Detector (Liu et al., 2016). **NMS** — Non-Maximum Suppression; tłumienie nie-maksymalnych detekcji.

### Jak zapamiętać

- **YOLO = „You Only Look Once"** — jednoetapowy, szybki
- **Faster R-CNN = CNN + RPN + ROI Pool** — dwuetapowy, dokładny
- **Detektor z klasyfikatora:** sliding window (wolno) → proposals (lepiej) → fine-tune backbone (najlepiej)

