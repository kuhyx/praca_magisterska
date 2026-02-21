## PYTANIE 24: Detekcja obiektów

**Problem, metody klasyczne, deep learning. Jak zbudować detektor z klasyfikatora?**

---

### Tło pojęciowe — słowniczek

**Detekcja obiektów (object detection)** — zadanie widzenia komputerowego: zlokalizuj obiekty na obrazie (bounding box) i przypisz im klasy (samochód, pieszo, kot...). Wynik: lista (klasa, prostokąt, pewność). Trudniejsze niż klasyfikacja (→ cały obraz, 1 label), ale łatwiejsze niż segmentacja (→ per piksel).

    Klasyfikacja:  "To zdjęcie zawiera kota"
    Detekcja:      "Kot w prostokącie (50,30)-(200,180), pewność 95%"
    Segmentacja:   Maska pikseli kota

**Bounding box (prostokąt ograniczający, bbox)** — prostokąt opisujący położenie obiektu. Zwykle: (x_min, y_min, x_max, y_max) lub (x_center, y_center, width, height). Przybliżenie — obiekty rzadko są prostokątne.

**Confidence (pewność)** — wynik 0-1 mówiący jak pewny jest detektor, że wykrył obiekt danej klasy. Zwykle próg np. 0.5: detekcje poniżej odrzucane.

---

**CNN (Convolutional Neural Network, konwolucyjna sieć neuronowa)** — typ sieci neuronowej zaprojektowany specjalnie do przetwarzania OBRAZÓW. Używany w KAŻDYM nowoczesnym detektorze (R-CNN, YOLO, SSD, DETR). Kluczowa idea: zamiast łączyć KAŻDY piksel z KAŻDYM neuronem (→ miliardy parametrów), CNN używa MAŁYCH filtrów (np. 3×3 piksele) przesuwanych po obrazie. Dzięki temu:
1. Mało parametrów (filtr 3×3 = 9 wag, niezależnie od rozmiaru obrazu)
2. Wykrywa lokalne wzorce (krawędzie, rogi, tekstury)
3. Inwariantność na przesunięcie (kot w lewym rogu = kot w prawym rogu)

    Dlaczego CNN a nie zwykła sieć neuronowa?
    Obraz 224×224×3 = 150 528 pikseli.
    Zwykła sieć (FC): 150 528 × 4096 neuronów = 616 MILIONÓW wag w 1 warstwie!
    CNN: filtr 3×3×3 = 27 wag, przesuwany po CAŁYM obrazie → 27 wag zamiast 616M!

    Mnemonik: CNN = „Czytaj Nie Naraz" — nie bierzesz całego obrazu naraz,
    tylko małe fragmenty (filtry 3×3), krok po kroku.

**Konwolucja (convolution)** — podstawowa operacja CNN: mały filtr (macierz np. 3×3) przesuwa się po obrazie, w każdej pozycji mnoży element-po-elemencie z fragmentem obrazu i sumuje → jedna liczba na wyjściu. Wynik = „feature mapa" — mapa pokazująca GDZIE na obrazie dany wzorzec jest obecny.

    Przykład liczbowy:
    Fragment obrazu 3×3:     Filtr 3×3:             Wynik (1 piksel feature mapy):
    [1  2  3]                [-1  0  1]
    [4  5  6]       ×        [-1  0  1]    = 1(-1)+2(0)+3(1)+4(-1)+5(0)+6(1)+7(-1)+8(0)+9(1)
    [7  8  9]                [-1  0  1]    = (-1+0+3) + (-4+0+6) + (-7+0+9) = 6

    Ten filtr wykrywa PIONOWE KRAWĘDZIE (liczy różnicę prawa-lewa strona).
    Duży wynik (6) = silna krawędź. Wynik ≈ 0 = brak krawędzi.
    Filtr przesuwa się po CAŁYM obrazie → cała mapa cech.

    Pseudokod konwolucji:
    def convolve(image, filter_3x3):
        output = zeros(image.height - 2, image.width - 2)
        for y in range(1, image.height - 1):
            for x in range(1, image.width - 1):
                patch = image[y-1:y+2, x-1:x+2]        # wycinek 3×3
                output[y-1][x-1] = sum(patch * filter)   # iloczyn + suma
        return output

**Filtr / Kernel** — mała macierz wag (np. 3×3, 5×5) uczona AUTOMATYCZNIE podczas treningu. CNN ma WIELE filtrów — każdy uczy się wykrywać INNY wzorzec. 64 filtry w jednej warstwie → 64 map cech.

    KLUCZOWA RÓŻNICA: w HOG cechy projektuje CZŁOWIEK.
    W CNN filtry uczy się SIEĆ SAMA — to główna przewaga deep learning!

    Warstwa conv z 64 filtrami 3×3:
    Filtr 1: nauczył się wykrywać pionowe krawędzie
    Filtr 2: nauczył się wykrywać poziome krawędzie
    Filtr 3: nauczył się wykrywać rogi
    ...
    Filtr 64: jakiś inny wzorzec pomocny w rozpoznawaniu

**Feature map (mapa cech)** — wynik zastosowania JEDNEGO filtra do obrazu. Jasne piksele = „tu jest ten wzorzec". 64 filtry → 64 map cech → tensor [H × W × 64]. Feature mapy to WEWNĘTRZNA REPREZENTACJA tego, co sieć „widzi" na obrazie.

    Hierarchia cech w CNN (każda warstwa coraz bardziej abstrakcyjna):
    Warstwa 1:  krawędzie, gradienty         (jak HOG!)
    Warstwa 2:  rogi, proste tekstury
    Warstwa 3:  fragmenty obiektów (oko, koło, ucho)
    Warstwa 4+: całe obiekty (twarz = oczy+nos+usta, samochód = koła+okna+dach)

    Mnemonik: „K-R-F-O" = „Każdy Rycerz Znajduje Obiekt"
    (Krawędzie → Rogi → Fragmenty → Obiekty)

**Pooling (łączenie / podpróbkowanie)** — warstwa ZMNIEJSZAJĄCA rozmiar feature mapy. Najczęstsza: **max pooling 2×2** — z każdego bloku 2×2 pikseli zachowaj MAKSIMUM. Wynik: mapa 2× mniejsza w każdym wymiarze (= 4× mniej pikseli), ale zachowuje najsilniejsze cechy.

    Feature map 4×4:           Po Max Pool 2×2:
    [1  3 | 2  1]              [3  2]    ← max(1,3,0,3)=3   max(2,1,1,2)=2
    [0  3 | 1  2]              [4  3]    ← max(0,4,1,2)=4   max(1,0,3,1)=3
    ─────────────
    [0  4 | 1  0]              Rozmiar: 4×4 → 2×2 (4× mniej danych!)
    [1  2 | 3  1]              Zachowane: najsilniejsze cechy z każdego bloku

    Dlaczego max pooling?
    1. Mniej pikseli = mniej obliczeń w następnych warstwach
    2. Większe „pole widzenia" (receptive field) — warstwa „widzi" większy fragment
    3. Odporność na małe przesunięcia: obiekt ±1px → ten sam max

**Stride (krok)** — o ile pikseli filtr przesuwa się za jednym krokiem. Stride=1: co 1 piksel (wyjście duże). Stride=2: co 2 piksele (wyjście 2× mniejsze). Max pool 2×2 ze stride 2 = typowy pooling.

**FC (Fully Connected layer, warstwa w pełni połączona)** — warstwa, w której KAŻDY neuron jest połączony z KAŻDYM wyjściem poprzedniej warstwy. W CNN zwykle na KOŃCU sieci: feature mapy (3D) → spłaszczone do wektora 1D → FC klasyfikuje.

    CNN: Conv → Pool → Conv → Pool → [Flatten] → FC(4096) → FC(1000) → "kot"
                                         ↑                       ↑
                                  spłaszcz 3D→1D         1000 klas (ImageNet)

    FC = „warstwa decyzyjna" — łączy cechy z CAŁEGO obrazu w jedną decyzję.
    Mnemonik: FC = „Full Connection" — każdy z każdym, jak klasa każdy-z-każdym.
    Problem FC: DUŻO parametrów (np. 25088 × 4096 = 102M wag w VGG-16!)

**Forward pass (przejście w przód)** — JEDNO przetworzenie danych przez sieć od wejścia do wyjścia. Obraz wchodzi → przechodzi przez Conv, Pool, FC → wychodzi predykcja. Nie aktualizuje wag (to backward pass / backpropagation = uczenie).

    Forward pass CNN (czasy na GPU):
    Jeden obraz przez ResNet-50: ~5ms
    R-CNN:      2000 regionów × 5ms = 10 SEKUND (dlatego był wolny!)
    Fast R-CNN: 1 forward pass cały obraz + ROI Pool = ~200ms (50× szybciej!)

**ReLU (Rectified Linear Unit)** — funkcja aktywacji: f(x) = max(0, x). Przepuszcza wartości dodatnie, zeruje ujemne. Standard w CNN — stosowana PO KAŻDEJ warstwie konwolucyjnej.

    Wejście:  [-3, 5, -1, 2, 0, -7, 4]
    ReLU:     [ 0, 5,  0, 2, 0,  0, 4]

    Dlaczego potrzebna? Bez ReLU sieć = seria mnożeń macierzy = JEDNA liniowa
    transformacja → nie potrafi uchwycić złożonych wzorców.
    ReLU dodaje NIELINIOWOŚĆ → sieć aproksymuje DOWOLNĄ funkcję.

**Softmax** — funkcja na WYJŚCIU klasyfikatora: zamienia surowe wyniki (logits) na prawdopodobieństwa sumujące się do 1.

    Logits:     [2.0,  1.0,  0.1]
    Softmax:    [0.66, 0.24, 0.10]   ← e^2.0 / (e^2.0 + e^1.0 + e^0.1) ≈ 0.66
    Klasy:      ["kot", "pies", "ryba"]
    → „66% szans, że to kot"

**Tensor** — wielowymiarowa tablica liczb. Uogólnienie wektora i macierzy.

    Skalar = 0D tensor:     5
    Wektor = 1D:            [1, 2, 3]
    Macierz = 2D:           [[1,2],[3,4]]
    Obraz RGB = 3D:         [224 × 224 × 3]        ← wysokość × szerokość × kanały
    Batch obrazów = 4D:     [32 × 224 × 224 × 3]   ← 32 obrazy naraz
    Wyjście YOLO = 3D:      [7 × 7 × 30]           ← siatka × predykcje

**Architektura CNN — pełny przykład (AlexNet, wygrał ImageNet 2012):**

![CNN — od obrazu do predykcji](img/q24_cnn_architecture.png)

    ROZMIARY MALEJĄ:  224 → 55 → 27 → 13 → 6  (kompresja przestrzenna)
    KANAŁY ROSNĄ:     3 → 96 → 256 → 384 → 256 (coraz więcej wyuczonych cech)

---

**Backbone (kręgosłup / sieć bazowa)** — duża, pretrenowana sieć CNN (np. ResNet-50, VGG-16) używana jako „ekstraktor cech". Backbone przetwarza obraz → feature mapa. Na wierzch dodaje się GŁOWICĘ (head) specyficzną dla zadania.

    Analogia: backbone = SILNIK samochodu, head = KAROSERIA.
    Ten sam silnik (ResNet) w różnych karoseriach:
        Sedan  → klasyfikacja: FC head → "kot"
        SUV    → detekcja: RPN + ROI Pool head → bbox + klasa
        Pickup → segmentacja: dekoder head → maska pikseli

    Backbone PRETRENOWANY na ImageNet (miliony obrazów).
    Head TRENOWANY od zera na konkretnym zadaniu (detekcja, segmentacja).

**Detection head (głowa detekcyjna)** — warstwy dodane NA WIERZCH backbone'u. Predykują klasy obiektów + pozycje bbox. W Faster R-CNN: RPN + ROI Pool + FC. W YOLO: warstwy conv + wyjście S×S×(B×5+C).

**ResNet, VGG, AlexNet — popularne backbone'y:**

    Sieć       Rok   Warstw   Parametrów   Top-5 ImageNet   Innowacja
    ─────────────────────────────────────────────────────────────────────
    AlexNet    2012   8        60M          84.7%             Pierwsza głęboka CNN
    VGG-16     2014   16       138M         92.7%             Małe filtry 3×3
    ResNet-50  2015   50       25M          96.4%             Skip connections

    Mnemonik: A → V → R = „Architektura Bardzo Rezylientna" (2012 → 2014 → 2015)

    Skip connection (ResNet): y = F(x) + x
    Wejście bloku DODAWANE do wyjścia → gradient nie zanika
    → można trenować 50-152 warstw (bez skip: >20 warstw = DEGRADACJA!)

**ImageNet** — ogromny zbiór danych: 14M obrazów, 1000 klas (pies, samolot, gitara...). Standard pretrenowania w computer vision. ILSVRC (coroczne zawody) — AlexNet wygrał 2012 → rewolucja deep learning.

**Transfer learning (uczenie transferowe)** — weź sieć pretrenowaną na dużym zbiorze (ImageNet), użyj do INNEGO zadania (detekcja, segmentacja). Backbone „wie" jak wyglądają krawędzie i kształty — trzeba tylko nauczyć nowej głowicy.

    Krok po kroku:
    1. ResNet-50 pretrenowany na ImageNet (1000 klas, miliony obrazów)
    2. Odtnij warstwę FC (klasyfikujse 1000 klas ImageNet) ← WYRZUĆ
    3. Dodaj nową głowicę detekcji (bbox + 80 klas COCO)  ← NOWA
    4. Trenuj głowicę na danych detekcyjnych (COCO/VOC)
    5. Opcjonalnie: fine-tune = odmroź backbone, ucz z MAŁYM learning rate

    Dlaczego działa? Cechy niskiego poziomu (krawędzie, tekstury) SĄ UNIWERSALNE.
    Kot, samochód, twarz — wszystko ma krawędzie i tekstury!

**Fine-tuning (dostrajanie)** — forma transfer learning: odmrażasz backbone i uczysz CAŁĄ sieć z MAŁYM learning rate, żeby subtelnie dopasować cechy do nowego zadania.

**COCO (Common Objects in Context)** — benchmark detekcji: 330K obrazów, 80 klas (samochód, osoba, pies...), 1.5M bboxów. Standard oceny detektorów.

**Pascal VOC (Visual Object Classes)** — starszy benchmark: 20 klas. Używany w oryginalnym YOLO i R-CNN.

**mAP (mean Average Precision)** — główna metryka jakości detekcji. Łączy trafność klasy z trafnością lokalizacji.

    mAP@0.5:      detekcja „trafna" jeśli IoU ≥ 0.5 (≥50% pokrycia z prawdą)
    mAP@0.5:0.95: średnia po progach 0.5, 0.55, ..., 0.95 (dużo surowsza)

    Faster R-CNN (COCO): mAP ≈ 42%
    YOLOv8-X (COCO):     mAP ≈ 53%

**End-to-end (od końca do końca)** — cała sieć trenowana jako JEDNOŚĆ, jeden loss, jeden trening. Przeciwieństwo: R-CNN miał ODDZIELNIE Selective Search + CNN + SVM = 3 osobne kroki. Faster R-CNN = end-to-end → komponenty uczą się WSPÓŁPRACOWAĆ → lepsze wyniki.

**FPN (Feature Pyramid Network)** — technika łączenia feature map z RÓŻNYCH warstw backbone'u. Wczesne warstwy (wysoka rozdzielczość) → małe obiekty. Późne warstwy (niska rozdzielczość) → duże obiekty. FPN łączy obie → wykrywa obiekty WSZYSTKICH rozmiarów.

![FPN (Feature Pyramid Network)](img/q24_fpn.png)

---

**Klasyfikator (classifier)** — model przypisujący etykietę do wejścia. Np. CNN trenowany na ImageNet: obraz → „kot" (+ prawdopodobieństwo). Klasyfikator nie mówi GDZIE jest obiekt — mówi tylko CO jest na obrazie. Pytanie brzmi: jak z takiego modelu zbudować detektor?

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

![SVM — hiperpłaszczyzna i margines](img/q24_svm_hyperplane.png)

**HOG+SVM — klasyczny pipeline detekcji pieszych:**

![HOG + SVM pipeline detekcji pieszych](img/hog_svm_pipeline.png)

      1. Sliding window (okno 64×128) przesuwa się po obrazie
      2. Dla każdej pozycji okna:
         a) Oblicz HOG → wektor 3780 cech
         b) SVM klasyfikuje: „pieszy" (+1) lub „nie-pieszy" (-1)
      3. NMS (Non-Maximum Suppression) → usuń duplikaty
      4. Wynik: lista bounding boxów z detekcjami pieszych

**Viola-Jones (2001)** — przełomowy detektor twarzy w CZASIE RZECZYWISTYM. Trzy kluczowe innowacje wyjasnione szczegółowo:

**Haar features (cechy Haarowe)** — najprostsze cechy obrazowe: prostokąty podzielone na jasną i ciemną część. Wartość cechy = (suma pikseli jasnych) − (suma pikseli ciemnych). Proste, ale skuteczne — wykrywają kontrasty typowe dla twarzy.

![Cechy Haar — typy i zastosowanie na twarzy](img/q24_haar_features.png)

    Dlaczego działa na TWARZACH?
    - Oczy CIEMNIEJSZE niż czoło → cecha "krawędź pozioma" daje dużą wartość
    - Nos JAŚNIEJSZY niż policzki → cecha "linia pionowa" daje dużą wartość
    - Twarz = charakterystyczna KOMBINACJA takich kontrastów!

    Ile cech? W oknie 24×24 pikseli: ponad 160 000 możliwych cech Haar
    (różne rozmiary × różne pozycje). AdaBoost wybiera ~200 NAJLEPSZYCH.

**Integral Image (obraz całkowy)** — precomputed tabela pozwalająca obliczyć sumę pikseli w DOWOLNYM prostokącie w O(1) — stały czas, niezależnie od rozmiaru! To dlatego Haar features liczą się tak szybko.

    Jak? Integral Image[x,y] = suma WSZYSTKICH pikseli od (0,0) do (x,y).

![Integral Image — suma prostokąta w O(1)](img/q24_integral_image.png)

    Zawsze 4 odczyty z tabeli → O(1)!
    Czy prostokąt ma 4 piksele czy 4 MILIONY — czas TEN SAM!
    Bez Integral Image: O(w×h) — suma 1000×1000 = milion operacji.
    Z Integral Image: O(1) — 4 operacje. ZAWSZE.

    Pseudokod:
    def integral_image(img):
        II = zeros_like(img)
        for y in range(H):
            for x in range(W):
                II[y][x] = img[y][x] + II[y-1][x] + II[y][x-1] - II[y-1][x-1]
        return II

    def rect_sum(II, x1, y1, x2, y2):   # O(1) zawsze!
        return II[y2][x2] - II[y1-1][x2] - II[y2][x1-1] + II[y1-1][x1-1]

**AdaBoost (Adaptive Boosting)** — algorytm uczenia maszynowego łączący wiele SŁABYCH klasyfikatorów w jeden SILNY. Słaby = niewiele lepszy od losowego (>50% trafień). AdaBoost iteracyjnie:
1. Trenuj słaby klasyfikator (np. 1 cecha Haar + próg: "czy wartość > 1200?")
2. Sprawdź, które przykłady ŹLE sklasyfikował
3. Nadaj źle sklasyfikowanym WIĘKSZĄ wagę → następny klasyfikator SKUPI się na nich
4. Powtórz 200× → suma ważona 200 słabych klasyfikatorów ≈ silny klasyfikator

    Intuicja: jak PANEL EKSPERTÓW, z których każdy zna się na JEDNEJ rzeczy.
    Ekspert 1: "czy okolice oczu ciemne?"        (trafność 55%)
    Ekspert 2: "czy nos jaśniejszy niż policzki?" (trafność 60%)
    Ekspert 3: "czy brwi ciemne?"                 (trafność 53%)
    ...
    200 ekspertów razem → trafność >95%!
    Mnemonik: AdaBoost = "ADAptacyjnie BOOSTuj" słabe modele do silnego.

**Cascade (kaskada klasyfikatorów)** — genialna optymalizacja szybkości: zamiast sprawdzać WSZYSTKIE 200 cech na każdym oknie, użyj KASKADY etapów. Każdy etap = prosty klasyfikator, który szybko ODRZUCA "na pewno nie-twarz".

![Viola-Jones — kaskada klasyfikatorów (SITO)](img/q24_viola_jones_cascade.png)

    Mnemonik: kaskada = "SITO" — coraz drobniejsze oczka,
    na początku odpada piach, na końcu zostaje ZŁOTO (twarz).

    Pseudokod kaskady:
    def cascade_classify(window):
        for stage in cascade_stages:           # etap 1, 2, ..., 25
            score = stage.evaluate(window)     # oblicz kilka cech Haar
            if score < stage.threshold:        # za niski wynik
                return "NIE-TWARZ"             # SZYBKIE odrzucenie!
        return "TWARZ"                         # przeszło WSZYSTKIE etapy

---

![Ewolucja detektorów: R-CNN → Faster R-CNN → YOLO](img/q24_rcnn_evolution.png)

**R-CNN family (two-stage detectors)** — dwuetapowe: najpierw generuj propozycje regionów, potem klasyfikuj każdy region. Nazwa: Region-based CNN.

**Selective Search (wyszukiwanie selektywne)** — klasyczny algorytm (NIE sieć neuronowa!) generowania propozycji regionów. Zamiast MILIONÓW pozycji okna (sliding window), inteligentnie łączy podobne fragmenty obrazu i proponuje ~2000 prostokątów, w których MOGĄ być obiekty.

    Algorytm krok po kroku:
    1. Over-segmentation: podziel obraz na ~1000 małych regionów (superpixele)
       (na podstawie koloru i tekstury — algorytm Felzenszwalb)
    2. Powtarzaj aż zostanie 1 region:
       a) Znajdź 2 najbardziej PODOBNE sąsiednie regiony:
          - podobny kolor? (histogram kolorów)
          - podobna tekstura? (histogram gradientów)
          - pasujący rozmiar? (preferuj łączenie MAŁYCH regionów)
       b) Połącz je w jeden → zapamiętaj bounding box nowego regionu
    3. Zebrane bbox-y ze WSZYSTKICH kroków → ~2000 propozycji

    Sliding window:    ~500 000 okien → 99.9% to "tło" → marnujesz czas
    Selective Search:  ~2 000 regionów → ~50% zawiera coś → 250× wydajniej
    RPN (Faster R-CNN): ~300 propozycji → sieć neuronowa (najszybciej!)

**Czym jest "region proposal" (propozycja regionu)?** — prostokąt, w którym MOŻE być obiekt. Dużo mniej niż sliding window (2000 zamiast milionów), ale każda propozycja ma WYSOKIE prawdopodobieństwo trafienia obiektu.

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

**Fast R-CNN (2015)** — kluczowa optymalizacja: przepuść cały obraz przez CNN RAZ, uzyskaj "mapę cech" (feature map). Potem wytnij cechy regionów z tej mapy (ROI Pooling), zamiast odpalać CNN 2000 razy.

**ROI (Region of Interest, region zainteresowania)** — prostokątny fragment feature mapy odpowiadający propozycji regionu na oryginalnym obrazie. Np. Selective Search zaproponował bbox (100,50)-(200,150) na obrazie 800×600 → odpowiadający ROI na feature mapie (po redukcji 16× przez pooling) to mniej więcej (6,3)-(12,9).

**ROI Pooling (pooling regionu zainteresowania)** — operacja zamieniająca ROI o DOWOLNYM rozmiarze na tensor o STAŁYM rozmiarze (np. 7×7). Konieczne, bo warstwa FC wymaga stałego rozmiaru wejścia!

    Problem: region 1 = 14×10 na feature mapie,  region 2 = 8×6  → RÓŻNE!
             Warstwa FC wymaga np. 7×7 → STAŁY rozmiar.

    Rozwiązanie — ROI Pooling:
    1. Weź ROI (np. 14×10) z feature mapy
    2. Podziel go na siatkę 7×7 (= 7 wierszy × 7 kolumn)
       Każda komórka obejmuje ok. 2×1.4 pikseli feature mapy
    3. W każdej komórce weź MAX (jak max pooling)
    4. Wynik: tensor 7×7 — STAŁY rozmiar niezależnie od oryginalnego ROI!

![ROI Pooling](img/q24_roi_pooling.png)

    Kluczowa sztuczka Fast R-CNN:
    CNN raz na CAŁY obraz → JEDNA feature mapa → ROI Pool 2000 regionów z TEJ SAMEJ mapy
    (zamiast 2000× odpalać CNN jak w R-CNN!)
    Przyspieszenie: ~2 sec/obraz (vs 50 sec) → 25× szybciej!

    Pseudokod ROI Pooling:
    def roi_pool(feature_map, roi_bbox, output_size=7):
        roi = feature_map[roi_bbox]              # wycinek z feature mapy
        h, w = roi.shape
        cell_h, cell_w = h // output_size, w // output_size
        output = zeros(output_size, output_size)
        for i in range(output_size):
            for j in range(output_size):
                cell = roi[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
                output[i][j] = max(cell)         # max pooling w komórce
        return output   # stały rozmiar 7×7!

    CNN raz → feature map → ROI Pool 2000 regionów → FC → klasy + bbox

**Bbox regression (regresja prostokąta ograniczającego)** — sieć predykuje nie bezpośrednie współrzędne bbox, ale PRZESUNIĘCIA (offsets) od propozycji: Δx, Δy (przesunięcie środka), Δw, Δh (zmiana szerokości/wysokości).

    Propozycja (z RPN/Selective Search): (x=100, y=80,  w=60,  h=90)  ← przybliżone
    Predykcja regresji:                  (Δx=+5, Δy=-3, Δw=+10, Δh=+5)
    Ostateczny bbox:                     (x=105, y=77,  w=70,  h=95)  ← dokładniejsze!

    Dlaczego offsets a nie współrzędne bezpośrednio?
    Łatwiejsze zadanie! Sieć poprawia przybliżony prostokąt O TROCHĘ,
    zamiast zgadywać lokalizację od zera.
    Mnemonik: bbox regression = "GPS korekta" — masz przybliżoną pozycję,
    poprawiasz o parę metrów w prawo i w górę.

**Faster R-CNN (2015)** — ostatni krok ewolucji: zastąp Selective Search (osobny algorytm) siecią neuronową! **RPN (Region Proposal Network)** — mała sieć przesuwana po feature mapie, która w KAŻDEJ pozycji predykuje: "czy tu jest obiekt?" + proponuje bbox. Wszystko w jednej sieci, end-to-end.

    Pipeline Faster R-CNN:
    Obraz → CNN backbone (np. ResNet) → Feature Map → RPN (proposals) → ROI Pool → FC → klasy + bbox

    RPN krok po kroku:
    Feature mapa [40×60×256] ← z backbone
      ↓ Filtr 3×3 przesuwa się po feature mapie
      ↓ W KAŻDEJ pozycji (x,y) rozważ k=9 "anchor boxes":

        9 anchorów = 3 rozmiary × 3 proporcje:
        ┌───┐  ┌─────┐  ┌───────┐   ← 128×128, 256×256, 512×512
        │   │  │     │  │       │      × proporcje 1:1, 1:2, 2:1
        └───┘  └─────┘  └───────┘

      ↓ Dla KAŻDEGO z 9 anchorów sieć predykuje:
        - P(obiekt) = prawdopodobieństwo, że tu jest obiekt
        - (Δx, Δy, Δw, Δh) = przesunięcie bbox względem anchora

    40×60 = 2400 pozycji × 9 anchorów = 21 600 potencjalnych propozycji!
    → Weź ~300 z najwyższym P(obiekt) → ROI Pool → FC → klasy + bbox

    Faster R-CNN: ~5 fps (~0.2 sec/obraz) — 250× szybciej niż R-CNN!

    Mnemonik ewolucji R-CNN: "CORAZ MNIEJ MARNOWANIA"
    R-CNN:       Selective Search + 2000×CNN          = 50s  → WOLNE
    Fast R-CNN:  Selective Search + 1×CNN + ROI Pool   = 2s   → lepiej
    Faster R-CNN: RPN (w sieci!) + 1×CNN + ROI Pool   = 0.2s → 250× szybciej!

---

**One-stage detectors** — klasyfikacja i lokalizacja w jednym przejściu (bez osobnego etapu propozycji). Szybsze, ale historycznie mniej precyzyjne.

**YOLO (You Only Look Once, 2016)** — rewolucyjny pomysł: „po co robić 2 etapy, skoro można w JEDNYM?" Obraz dzielony jest na siatkę S×S (np. 13×13 = 169 komórek). Każda komórka odpowiada za wykrycie obiektu, którego ŚRODEK wpada w tę komórkę. Każda komórka predykuje:
- B bounding boxów × (x, y, w, h, confidence) = lokalizacja + „pewność, że tu jest obiekt"
- C prawdopodobieństw klas = „jaki to obiekt?"
Jedno przejście przez sieć → WSZYSTKIE detekcje naraz. 45-155 fps!

![YOLO — detekcja jednoetapowa (siatka S×S)](img/q24_yolo_grid.png)

**SSD (Single Shot MultiBox Detector, 2016)** — ulepsza YOLO przez multi-scale feature maps: predykcje z WIELU warstw CNN, każda o innej rozdzielczości. Wczesne warstwy (wysoka rozdzielczość) wykrywają MAŁE obiekty; późne warstwy (niska rozdzielczość) wykrywają DUŻE. Anchor boxes predefiniowane na każdej skali.

**Anchor box (kotwica)** — predefiniowany prostokąt o określonym kształcie/proporcji (np. 1:1, 1:2, 2:1). Sieć NIE predykuje bbox od zera — predykuje PRZESUNIĘCIE (offset) od najbliższego anchora. Łatwiejsze zadanie! Wiele anchorów → pokrycie różnych kształtów obiektów (osoby = wysoki prostokąt, samochód = szeroki).

![Anchor boxes — predefiniowane kształty](img/q24_anchor_boxes.png)

**Anchor-free** — nowoczesne podejście (FCOS, YOLOv8): bezpośrednia predykcja środka i wymiarów, bez predefiniowanych anchorów. Prostsza architektura, mniej hyperparametrów.

**Transformer** — architektura sieci neuronowej pierwotnie z NLP (2017, "Attention is All You Need"), ale skutecznie zaadaptowana do wizji komputerowej (ViT, DETR). Kluczowy mechanizm: **self-attention** — każdy element wejścia "patrzy" na WSZYSTKIE inne elementy i decyduje, które są dla niego ważne.

    W tekście: słowo "bank" patrzy na "rzeka" i "pieniądze" →
    attention decyduje: "w tym zdaniu chodzi o brzeg RZEKI, nie bank pieniędzy"

    W obrazie (DETR): fragment obrazu "patrzy" na inne fragmenty →
    attention: "ta łapa jest częścią TEGO kota, a nie tamtego psa"

**Self-attention (samo-uwaga)** — mechanizm: dla każdego elementu oblicz "uwagę" do KAŻDEGO innego elementu. Matematycznie: Query × Key → wagi attention → ważona suma Values.

    Uproszczony pseudokod:
    def self_attention(features):         # features = N elementów
        Q = features × W_query            # Query: "czego szukam?"
        K = features × W_key              # Key: "co oferuję?"
        V = features × W_value            # Value: "jaką informację niosę?"

        attention = softmax(Q × K^T / sqrt(d))  # macierz N×N: "kto ważny dla kogo"
        output = attention × V                   # ważona kombinacja wartości
        return output

    Złożoność: O(n^2) — każdy element z każdym → wolne dla dużych obrazów.
    Dlatego DETR wolniej się TRENUJE niż YOLO (ale architektura jest PROSTSZA).

**DETR (DEtection TRansformer, 2020)** — model Facebooka stosujący Transformer do detekcji. Radykalnie prostszy pipeline: BRAK anchorów, BRAK NMS! Sieć predykuje bezpośrednio ZESTAW N obiektów (np. N=100).

![DETR — Transformer do detekcji](img/q24_detr_pipeline.png)

    "Object queries" = 100 wyuczonych wektorów, każdy "szuka" jednego obiektu.
    Obraz z 5 obiektami → 5 queries dopasuje się do obiektów,
    95 queries zwróci klasę "brak obiektu" (empty set).

    Pseudokod DETR:
    def detr_forward(image):
        features = backbone(image)                # ResNet → feature mapa
        encoded = transformer_encoder(features)   # self-attention na feat. mapie
        queries = learnable_queries(100)           # 100 wyuczonych zapytań
        decoded = transformer_decoder(queries, encoded)  # cross-attention
        predictions = []
        for q in decoded:
            cls = classify(q)      # "samochód" / "pies" / "brak"
            box = regress(q)       # (x, y, w, h)
            predictions.append((cls, box))
        return predictions         # 100 predykcji (większość = brak)

    Mnemonik DETR: "Detekcja Eliminująca Trikowe Redundancje"
    → bez NMS, bez anchorów, prosty pipeline.

**Hungarian matching (dopasowanie węgierskie)** — algorytm używany podczas TRENINGU DETR. Problem: sieć daje 100 predykcji, na obrazie jest 5 obiektów — która predykcja odpowiada któremu obiektowi? Algorytm węgierski znajduje OPTYMALNE dopasowanie 1:1 minimalizując łączny koszt (błąd klasy + błąd bbox).

    Predykcje DETR:           Ground truth:
    pred_1: "samochód"        gt_1: "samochód" (bbox A)
    pred_2: "pies"            gt_2: "pies" (bbox B)
    pred_3: "brak"
    ...                       Hungarian matching:
    pred_100: "brak"          pred_1 ↔ gt_1 (najlepsze dopasowanie!)
                              pred_2 ↔ gt_2
                              reszta ↔ "brak obiektu"

    Efekt: BRAK DUPLIKATÓW → BRAK NMS!
    (Każdy obiekt dopasowany do DOKŁADNIE jednej predykcji)

---

**NMS (Non-Maximum Suppression, tłumienie nie-maksymalnych)** — algorytm post-processingu usuwający ZDUPLIKOWANE detekcje. Problem: detektor generuje WIELE nakładających się bbox dla tego samego obiektu. NMS zachowuje NAJLEPSZĄ i usuwa resztę. Jedyny detektor BEZ NMS = DETR.

    Algorytm NMS krok po kroku:
    Wejście: detekcje posortowane malejąco po confidence
    [bbox_1 conf=0.95], [bbox_2 conf=0.90], [bbox_3 conf=0.85], [bbox_4 conf=0.40]

    Pseudokod NMS:
    def nms(detections, iou_threshold=0.5):
        detections.sort(by=confidence, descending=True)
        keep = []
        while detections:
            best = detections.pop(0)        # weź najlepszą
            keep.append(best)               # ZACHOWAJ ją
            detections = [d for d in detections
                          if iou(best, d) < iou_threshold]  # usuń nakładające
        return keep

    Krok 1: Weź bbox_1 (0.95) → ZACHOWAJ
    Krok 2: IoU(bbox_1, bbox_2) = 0.82 > 0.5 → USUŃ (duplikat tego samego kota!)
            IoU(bbox_1, bbox_3) = 0.75 > 0.5 → USUŃ (duplikat!)
            IoU(bbox_1, bbox_4) = 0.10 < 0.5 → ZACHOWAJ (INNY obiekt!)
    Krok 3: Wynik: [bbox_1, bbox_4] — 2 unikalne obiekty

    Mnemonik: NMS = "Najlepszy Ma Się dobrze" — zachowaj najlepszą, usuń resztę.

**IoU (Intersection over Union)** — miara nakładania dwóch prostokątów. IoU = pole przecięcia / pole sumy. Wartości: 0.0 (nie nakładają się) do 1.0 (identyczne).

![IoU (Intersection over Union)](img/q24_iou_diagram.png)

    IoU = pole(∩) / pole(A ∪ B)
        = pole(∩) / (pole(A) + pole(B) − pole(∩))

    Przykład liczbowy:
    A = [0, 0, 100, 100]    → pole = 10 000
    B = [50, 50, 150, 150]  → pole = 10 000
    ∩ = [50, 50, 100, 100]  → pole = 2 500
    IoU = 2500 / (10000 + 10000 − 2500) = 2500 / 17500 ≈ 0.14

    IoU > 0.5 w NMS → "to TEN SAM obiekt" → usuń słabszą detekcję
    IoU > 0.5 w mAP → "detekcja TRAFNA" → poprawna lokalizacja

---

**Jak zbudować detektor z klasyfikatora? Trzy podejścia (+ bonus):**
1. **Sliding window** — wytnij, sklasyfikuj, NMS. Bardzo wolne (miliony klasyfikacji).
2. **Region proposals + klasyfikator** — Selective Search → ~2000 regionów → klasyfikuj + NMS. Wolne ale działa (= R-CNN).
3. **Fine-tune backbone** — weź pretrained classifier (ResNet z ImageNet), dodaj detection head (bbox regression + cls), dotrenuj na danych detekcyjnych. **Najlepsza jakość** (= Faster R-CNN, YOLO, SSD).
4. **Transformer (DETR)** — bez anchorów, bez NMS, predykcja zestawu obiektów end-to-end.

---

### Problem: czym jest detekcja obiektów?

Detekcja obiektów to **lokalizacja** (gdzie?) i **klasyfikacja** (co?) obiektów na obrazie. Wynik: lista krotek **(klasa, bounding box, confidence)**.

    Wejście:   zdjęcie ulicy
    Wynik:     [("samochód", [50,30,200,180], 0.95),
                ("pieszy",   [300,100,350,250], 0.88),
                ("rower",    [400,150,480,300], 0.72)]

**Porównanie z innymi zadaniami:**

![Klasyfikacja vs Detekcja vs Segmentacja](img/q24_detection_tasks.png)

---

### Metody klasyczne

Metody sprzed deep learningu — ręcznie projektowane cechy (features) + klasyczny klasyfikator.

| Metoda | Rok | Cechy | Klasyfikator | Szybkość | Use case |
|--------|-----|-------|-------------|----------|----------|
| **HOG + SVM** | 2005 | Histogram of Oriented Gradients | SVM | wolna (~1 fps) | detekcja pieszych |
| **Viola-Jones** | 2001 | Haar features + Integral Image | AdaBoost cascade | real-time (30+ fps) | detekcja twarzy |

#### HOG + SVM (Dalal & Triggs, 2005) — krok po kroku

**Mnemonik kroków HOG: „GÓRA KOCHA BOGATYCH NARCIARZY" → Gradienty → Orientacja → Komórki → Bloki → Normalizacja**

![HOG + SVM pipeline detekcji pieszych](img/q24_hog_svm_pipeline.png)

**Krok 1 — Gradienty (G jak GÓRA):** Oblicz gradient KAŻDEGO piksela. Gradient = „siła i kierunek zmiany jasności". Tam, gdzie jasność skacze (np. 50→200), jest krawędź.

    Przykład liczbowy:
    Piksele w wierszu: [50, 50, 200]
    Gx = pixel[x+1] − pixel[x−1] = 200 − 50 = 150  ← silna krawędź pionowa!
    Gy = analogicznie w pionie
    Siła: magnitude = √(Gx² + Gy²) = √(150² + 0²) = 150
    Kierunek: direction = arctan(Gy/Gx) = arctan(0/150) = 0° (krawędź pionowa)

**Krok 2 — Orientacja (O jak KOCHA):** Każdy piksel głosuje na kierunek swojej krawędzi. 9 „koszyków" (binów) co 20°: 0°, 20°, 40°, …, 160°. Głos ważony SIŁĄ gradientu (silniejsza krawędź = mocniejszy głos).

    Piksel z magnitude=150, direction=10°:
    Głosuje na bin 0° (z wagą proporcjonalną do bliskości) i bin 20°
    Piksel z magnitude=30, direction=85°:
    Głosuje na bin 80° i bin 100° (słabsza krawędź = słabszy głos)

**Krok 3 — Komórki (K jak BOGATYCH):** Podziel okno (64×128 px) na komórki 8×8 pikseli = 8×16 = 128 komórek. Dla KAŻDEJ komórki stwórz histogram 9 binów — to jej „odcisk palca kierunkowości krawędzi".

![HOG — kroki obliczania cech](img/q24_hog_gradient_steps.png)

**Krok 4 — Bloki (B jak NARCIARZY):** Grupuj komórki w bloki 2×2 (= 16×16 px). Przesuwaj blok z krokiem 1 komórki. Okno 64×128 → (8−1)×(16−1) = 7×15 = 105 bloków.

**Krok 5 — Normalizacja (N):** Dla KAŻDEGO bloku (4 komórki × 9 binów = 36 wartości) wykonaj normalizację L2 → odporność na zmiany oświetlenia. 105 bloków × 36 = **3780 cech** → wektor HOG.

    Pseudokod:
    def compute_hog(window_64x128):
        Gx = pixel[x+1] - pixel[x-1]          # gradient poziomy
        Gy = pixel[y+1] - pixel[y-1]          # gradient pionowy
        mag = sqrt(Gx**2 + Gy**2)             # siła
        dir = arctan2(Gy, Gx) * 180 / pi     # kierunek 0°-180°

        hog = []
        for block_2x2 in sliding_blocks(cells_8x8):
            block_hist = []
            for cell in block_2x2:                 # 4 komórki
                hist = [0]*9                       # 9 binów
                for px in cell.pixels:             # 64 piksele
                    bin = int(dir[px] / 20)        # który bin?
                    hist[bin] += mag[px]           # ważone głosowanie
                block_hist += hist
            block_hist = L2_normalize(block_hist)  # normalizacja!
            hog += block_hist
        return hog  # wektor 3780 cech → do SVM

**Krok 6 — SVM klasyfikuje:** Wektor 3780 cech → SVM odpowiada: „pieszy" (+1) lub „tło" (−1).

![SVM — hiperpłaszczyzna i margines](img/q24_svm_hyperplane.png)

    Mnemonik SVM: „LINIA MAKSYMALNEGO ODDECHU"
    SVM = linia (hiperpłaszczyzna) z MAKSYMALNYM marginesem.
    Jak MOST nad rzeką — im szerszy, tym bezpieczniejszy (lepiej generalizuje).

**Krok 7 — NMS:** Usuń duplikaty (wiele okien wykryło tego samego pieszego → zachowaj najlepsze).

    Mnemonik PEŁNEGO pipeline'u HOG+SVM: „GOKBN-SN"
    → Gradienty → Orientacja → Komórki → Bloki → Normalizacja → SVM → NMS
    = „Grasz Ostro, Kumplu? Bądź Naturalny, Szybko Nabierz (wprawy)!"

---

#### Viola-Jones (2001) — krok po kroku

**Mnemonik 3 innowacji: „HIC" → Haar + Integral Image + Cascade**

**Innowacja 1 — Haar features (H):** Prostokąty dzielone na jasną i ciemną część. Wartość = Σ(jasna) − Σ(ciemna). Proste, ale wykrywają kontrasty typowe dla twarzy.

![Cechy Haar — typy i zastosowanie na twarzy](img/q24_haar_features.png)

    Pseudokod cechy Haar:
    def haar_edge_vertical(img, x, y, w, h):
        left_sum  = sum_pixels(img, x, y, x+w//2, y+h)    # jasna połówka
        right_sum = sum_pixels(img, x+w//2, y, x+w, y+h)  # ciemna połówka
        return left_sum - right_sum   # duża wartość = silna krawędź

    Mnemonik: Haar = „Hej, A tu jest Różnica?"
    Cechy Haar pytają: „Czy lewa strona JAŚNIEJSZA niż prawa?"

**Innowacja 2 — Integral Image (I):** Precomputed tabela: suma DOWOLNEGO prostokąta w O(1) — 4 odczyty z tabeli, niezależnie od rozmiaru!

![Integral Image — suma prostokąta w O(1)](img/q24_integral_image.png)

    Pseudokod:
    def build_integral_image(img):
        II = zeros(H, W)
        for y in range(H):
            for x in range(W):
                II[y][x] = img[y][x] + II[y-1][x] + II[y][x-1] - II[y-1][x-1]
        return II

    def rect_sum(II, x1, y1, x2, y2):    # ZAWSZE O(1)!
        return II[y2][x2] - II[y1-1][x2] - II[y2][x1-1] + II[y1-1][x1-1]

    Mnemonik: Integral Image = „4 Odczyty I Gotowe!" = 4OIG
    Jak czytanie z gotowej tabeli: nie liczymy, tylko odczytujemy!

**Innowacja 3 — Cascade (C):** Kaskada etapów — szybkie odrzucanie „na pewno nie-twarz".

![Viola-Jones — kaskada klasyfikatorów (SITO)](img/q24_viola_jones_cascade.png)

    Pseudokod:
    def cascade_classify(window):
        for stage in [stage_1, stage_2, ..., stage_25]:
            score = sum(stage.weights[i] * haar_feature[i](window)
                        for i in stage.features)
            if score < stage.threshold:
                return "NIE-TWARZ"      # szybkie odrzucenie!
        return "TWARZ"                  # przeszło WSZYSTKIE etapy

    Mnemonik: Cascade = „SITO z coraz drobniejszymi oczkami"
    Etap 1: sito o dużych oczkach → odpada piach (oczywiste nie-twarze)
    Etap 25: sito najdrobniejsze → zostaje ZŁOTO (twarz)
    99% okien odpada w pierwszych 3 etapach → REAL-TIME!

**Pełny pipeline Viola-Jones:**

    1. Sliding window (24×24) po obrazie w wielu skalach
    2. Integral Image (preprocessing, O(n) — raz)
    3. Dla każdego okna: kaskada (Haar + AdaBoost, najczęściej odrzuci w 1-3 etapie)
    4. NMS na detekcjach → wynik

    Mnemonik pipeline'u: „SIKN" = Sliding → Integral → Kaskada → NMS
    = „Szybko Identyfikuj Kształty Niezwykłe!"

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

![Ewolucja detektorów: R-CNN → Faster R-CNN](img/q24_rcnn_evolution.png)

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

![Two-stage vs One-stage — porównanie](img/q24_two_vs_one_stage.png)

---

### Jak zbudować detektor z klasyfikatora?

Masz wytrenowany klasyfikator (np. ResNet na ImageNet: obraz → „kot"). Jak go użyć do **lokalizacji** obiektów?

**Mnemonik 3 podejść: „SRF" = „Sliding → Region → Fine-tune" = „Szukaj Ręcznie, Finalnie optymalizuj!"**

![Jak zbudować detektor z klasyfikatora? — 3 podejścia](img/q24_detector_from_classifier.png)

---

#### Podejście 1 — Sliding Window (najprostsze, NAJWOLNIEJSZE)

**Idea:** Wycinaj prostokątne fragmenty obrazu, KAŻDY pokaż klasyfikatorowi, zbierz pozytywne.

**Mnemonik: „WYCINAJ i PYTAJ" — jak wycinanie ciasteczek: koło po kole, aż cały obraz pokryty.**

![Sliding Window — najprostsze podejście](img/q24_sliding_window.png)

    Pseudokod:
    def sliding_window_detect(image, classifier, window_size=64, step=8):
        detections = []
        for scale in [0.5, 0.75, 1.0, 1.5, 2.0]:        # 5 skal
            resized = resize(image, scale)
            for y in range(0, resized.height - window_size, step):
                for x in range(0, resized.width - window_size, step):
                    window = resized[y:y+window_size, x:x+window_size]
                    label, confidence = classifier.predict(window)
                    if label != "tło" and confidence > 0.5:
                        # przelicz współrzędne na oryginał
                        bbox = (x/scale, y/scale,
                                (x+window_size)/scale, (y+window_size)/scale)
                        detections.append((label, bbox, confidence))
        return nms(detections)   # usuń duplikaty

**Dlaczego wiele skal?** Obiekty mają różne rozmiary — kot blisko = duży, kot daleko = mały. Okno 64×64 nie złapie kota 200×200.

    Obliczenia dla obrazu 640×480:
    Pozycje na skali 1.0: (640-64)/8 × (480-64)/8 = 72 × 52 = 3 744
    × 5 skal = 18 720 okien
    × klasyfikacja ResNet (~10ms/obraz na GPU) = ~3 minuty
    × na CPU (~100ms/obraz) = ~30 minut na 1 obraz!
    ⚠ NIEPRAKTYCZNE dla zastosowań real-time

**Wady:** (1) Ekstremalnie wolne. (2) Stały kształt okna — obiekty nie są kwadratowe. (3) ~99.9% okien to „tło" → marnowanie czasu.

---

#### Podejście 2 — Region Proposals + Klasyfikator (= R-CNN)

**Idea:** Zamiast milionów okien, inteligentnie zaproponuj ~2000 regionów, w których MOGĄ być obiekty, i tylko te sklasyfikuj.

**Mnemonik: „INTELIGENTNE CIĘCIE" — zamiast kroić cały tort na milion kawałków, wytnij tylko tam, gdzie widzisz wiśnie (obiekty).**

    Pseudokod (= R-CNN):
    def region_proposal_detect(image, classifier):
        # Krok 1: Selective Search — inteligentnie generuj regiony
        proposals = selective_search(image)    # ~2000 prostokątów
        detections = []

        # Krok 2: Dla KAŻDEGO regionu — clasificuj
        for bbox in proposals:                 # ~2000 iteracji (nie milion!)
            crop = image[bbox]                 # wytnij region
            crop = resize(crop, 224, 224)      # rozmiar wymagany przez CNN
            features = cnn_backbone(crop)      # ResNet → wektor 2048 cech
            label, conf = svm_classify(features)  # SVM: "samochód? kot? tło?"
            if label != "tło" and conf > 0.5:
                detections.append((label, bbox, conf))

        # Krok 3: bbox regression — doprecyzuj pozycje
        for det in detections:
            det.bbox += bbox_regressor(det.features)  # Δx, Δy, Δw, Δh

        return nms(detections)   # Krok 4: usuń duplikaty

**Dlaczego 2000 a nie milion?** Selective Search łączy podobne fragmenty obrazu (kolor, tekstura) bottom-up. Wynik: ~2000 „mądrych" propozycji, z których ~50% zawiera coś (vs 0.1% w sliding window).

    Porównanie z sliding window:
    Sliding Window: ~18 000 okien × 10ms = ~3 min
    Proposals:      ~2 000 regionów × 10ms = ~20 sec ← 9× szybciej
    ALE wciąż 2000 × forward pass CNN → dlatego powstał Fast R-CNN!

**Wady:** (1) Selective Search jest osobnym algorytmem (nie end-to-end). (2) 2000 × forward pass CNN = wciąż wolno. (3) SVM trenowany OSOBNO od CNN.

---

#### Podejście 3 — Fine-tune backbone + detection head (NAJLEPSZE)

**Idea:** Weź pretrenowany klasyfikator, ODETNIJ głowicę klasyfikacyjną (FC 1000 klas), zastąp ją DWOMA nowymi głowicami: (1) głowica klasyfikacji → klasa obiektu, (2) głowica regresji → pozycja bbox.

**Mnemonik: „PRZESZCZEP GŁOWY" — ten sam silnik (backbone), nowa głowa (detection head).**

    Pseudokod (= Faster R-CNN / YOLO w uproszczeniu):
    # KROK 1: Weź pretrenowany klasyfikator
    resnet = load_pretrained("resnet50_imagenet")  # 1000 klas ImageNet

    # KROK 2: Odetnij starą głowicę klasyfikacji
    backbone = resnet.layers[:-2]    # ZACHOWAJ: Conv1...Conv5 (ekstraktor cech)
    # WYRZUĆ: FC(1000) + Softmax

    # KROK 3: Dodaj nowe głowice detekcji
    class DetectionHead:
        def __init__(self):
            self.cls_head = Linear(2048, num_classes)    # "samochód? kot? tło?"
            self.bbox_head = Linear(2048, 4)             # Δx, Δy, Δw, Δh

        def forward(self, features):
            cls = softmax(self.cls_head(features))       # P(klasa)
            bbox = self.bbox_head(features)              # przesunięcie bbox
            return cls, bbox

    # KROK 4: Zamroź backbone, trenuj głowice na danych detekcyjnych
    for image, gt_boxes, gt_labels in coco_dataset:
        features = backbone(image)          # pretrenowane cechy (zamrożone)
        cls, bbox = detection_head(features)
        loss = cls_loss(cls, gt_labels) + bbox_loss(bbox, gt_boxes)
        loss.backward()                     # aktualizuj TYLKO detection_head

    # KROK 5 (opcja): Fine-tune — odmroź backbone z MAŁYM learning rate
    backbone.unfreeze()
    optimizer = SGD(lr=0.0001)    # 10× mniejszy niż dla głowicy!
    # trenuj jak w kroku 4, ale teraz backbone też się uczy

**Dlaczego to działa?** Pretrenowany backbone na ImageNet „wie", jak wyglądają krawędzie, tekstury, kształty. Te cechy są UNIWERSALNE — przydają się zarówno do klasyfikacji „złota rybka vs samolot" jak i do detekcji „samochód na zdjęciu z drona".

    Transfer learning w liczbach:
    Trenowanie od zera na COCO (330K obrazów):     ~12h na 8×V100 GPU
    Fine-tune pretrained ResNet-50:                ~4h na 8×V100 GPU ← 3× szybciej!
    Fine-tune osiąga mAP ~42%, od zera ~38%        ← lepsze wyniki!

**Pełny przykład w PyTorch (Faster R-CNN z pretrained backbone):**

    import torchvision
    from torchvision.models.detection import fasterrcnn_resnet50_fpn

    # Gotowy detektor z pretrained backbone!
    model = fasterrcnn_resnet50_fpn(pretrained=True)

    # Custom: zmiana na 5 klas (zamiast 91 COCO)
    num_classes = 5  # 4 obiekty + tło
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # Trening:
    model.train()
    for images, targets in dataloader:
        loss_dict = model(images, targets)  # cls_loss + bbox_loss
        total_loss = sum(loss_dict.values())
        total_loss.backward()
        optimizer.step()

    # Inferencja:
    model.eval()
    predictions = model([test_image])
    # predictions = [{'boxes': tensor, 'labels': tensor, 'scores': tensor}]
    # boxes = [[x1,y1,x2,y2], ...], labels = [1, 3, ...], scores = [0.95, 0.88, ...]

---

#### Podsumowanie — porządek od NAJGORSZEGO do NAJLEPSZEGO:

    Podejście          Okien      Czas/obraz    Jakość     Rok     Przykład
    ──────────────────────────────────────────────────────────────────────────
    Sliding Window     ~milion    ~30 min       niska      -       (teoria)
    Region Proposals   ~2000     ~20-50 sec     średnia    2014    R-CNN
    Fine-tune + RPN    ~300      ~0.2 sec       wysoka     2015    Faster R-CNN
    One-stage          1×siatka  ~7-22 ms       wysoka     2016+   YOLO, SSD
    Transformer        N queries  ~25 ms        wysoka     2020    DETR

    Mnemonik porządku: „SRFTD" = „Sliding → Region → Fine-tune → Transformer → (Done!)"
    = „Szukaj Ręcznie, Finalnie Transformer (Detekuje!)"

---

### NMS (Non-Maximum Suppression) — post-processing

![NMS — usuwanie duplikatów](img/q24_nms_steps.png)

    Detektor generuje WIELE nakładających się bbox dla jednego obiektu:
    [bbox1, 0.95], [bbox2, 0.90], [bbox3, 0.85] — wszystkie na tym samym kocie

    Pseudokod NMS:
    def nms(detections, iou_threshold=0.5):
        detections.sort(by=confidence, descending=True)
        keep = []
        while detections:
            best = detections.pop(0)        # weź najlepszą
            keep.append(best)               # ZACHOWAJ
            detections = [d for d in detections
                          if iou(best, d) < iou_threshold]  # usuń nakładające
        return keep

    Krok po kroku (przykład):
    1. Sortuj: [0.95, 0.90, 0.85, 0.40]
    2. Weź bbox₁ (0.95) → ZACHOWAJ
    3. IoU(bbox₁, bbox₂) = 0.82 > 0.5 → USUŃ (duplikat!)
       IoU(bbox₁, bbox₃) = 0.75 > 0.5 → USUŃ (duplikat!)
       IoU(bbox₁, bbox₄) = 0.10 < 0.5 → ZACHOWAJ (INNY obiekt!)
    4. Wynik: [bbox₁, bbox₄] — 2 unikalne obiekty

![IoU (Intersection over Union)](img/q24_iou_diagram.png)

    Mnemonik NMS: „Najlepszy Ma Się dobrze" — zachowaj najlepszą, resztę wyrzuć
    Mnemonik IoU: „Ile pokrycia Ustalono?" — pole(∩) / pole(A∪B)

### Etymologia

**CNN** — Convolutional Neural Network (sieć z konwolucjami). **YOLO** — You Only Look Once (Joseph Redmon et al., 2016). **R-CNN** — Region-based CNN (Ross Girshick, 2014). **HOG** — Histogram of Oriented Gradients (Dalal & Triggs, 2005). **SVM** — Support Vector Machine (Vapnik, 1995). **Viola-Jones** — Paul Viola + Michael Jones (2001). **DETR** — DEtection TRansformer (Facebook AI, 2020). **SSD** — Single Shot MultiBox Detector (Liu et al., 2016). **NMS** — Non-Maximum Suppression; tłumienie nie-maksymalnych detekcji. **ROI** — Region of Interest (region zainteresowania). **RPN** — Region Proposal Network (sieć propozycji regionów). **FPN** — Feature Pyramid Network (piramida cech). **IoU** — Intersection over Union (przecięcie przez sumę). **FC** — Fully Connected (w pełni połączona). **ReLU** — Rectified Linear Unit (wyprostowana jednostka liniowa). **mAP** — mean Average Precision (średnia precyzja).

### Jak zapamiętać

- **CNN = „Czytaj Nie Naraz"** — małe filtry 3×3 przesuwane po obrazie, nie cały obraz naraz
- **Hierarchia CNN: „K-R-F-O" = „Każdy Rycerz Znajduje Obiekt"** — Krawędzie → Rogi → Fragmenty → Obiekty
- **FC = „Full Connection"** — każdy z każdym, warstwa decyzyjna na końcu CNN
- **Backbone = SILNIK samochodu** — ten sam silnik (ResNet), różne karoserie (klasyfikacja/detekcja/segmentacja)
- **Backbone'y: A→V→R = „Architektura Bardzo Rezylientna"** — AlexNet (2012) → VGG (2014) → ResNet (2015)
- **Transfer learning = „PRZESZCZEP GŁOWY"** — nie ucz się od zera, przenieś wiedzę z ImageNet, zmień głowicę
- **HOG kroki: „GOKBN" = „Grasz Ostro, Kumplu? Bądź Naturalny"** — Gradienty → Orientacja → Komórki → Bloki → Normalizacja
- **SVM = „LINIA MAKSYMALNEGO ODDECHU"** — margines jak most: im szerszy, tym bezpieczniej
- **Viola-Jones: „HIC" = Haar + Integral Image + Cascade**
- **Haar = „Hej, A tu jest Różnica?"** — porównuje jasne i ciemne prostokąty
- **Integral Image = „4 Odczyty I Gotowe" (4OIG)** — suma dowolnego prostokąta O(1)
- **Kaskada = „SITO"** — piach odpada wcześnie, złoto (twarz) zostaje na końcu
- **Viola-Jones pipeline: „SIKN" = „Szybko Identyfikuj Kształty Niezwykłe"** — Sliding → Integral → Kaskada → NMS
- **AdaBoost = „ADAptacyjnie BOOSTuj"** — słabe modele razem = silny
- **Selective Search** — inteligentne łączenie regionów zamiast milionów okien
- **ROI Pooling** — dowolny rozmiar → stały rozmiar (siatkowanie + max)
- **Bbox regression = „GPS korekta"** — popraw przybliżoną pozycję o Δx, Δy, Δw, Δh
- **Ewolucja R-CNN: „CORAZ MNIEJ MARNOWANIA"** — R-CNN (50s) → Fast (2s) → Faster (0.2s)
- **YOLO = „You Only Look Once"** — jednoetapowy, szybki, siatka S×S
- **Faster R-CNN = CNN + RPN + ROI Pool** — dwuetapowy, dokładny
- **NMS = „Najlepszy Ma Się dobrze"** — zachowaj najlepszą detekcję, usuń duplikaty
- **IoU = „Ile pokrycia Ustalono?"** — pole(∩) / pole(A∪B)
- **DETR = „Detekcja Eliminująca Trikowe Redundancje"** — bez NMS, bez anchorów, transformer
- **Detektor z klasyfikatora: „SRF" = „Szukaj Ręcznie, Finalnie optymalizuj!"** — Sliding Window (wolno) → Region Proposals (lepiej) → Fine-tune backbone (najlepiej)

