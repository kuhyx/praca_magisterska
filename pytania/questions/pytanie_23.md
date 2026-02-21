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

#### Pojęcia kluczowe dla progowania i Otsu

**Wariancja (variance, σ²)** — miara tego, jak bardzo wartości RÓŻNIĄ SIĘ od swojej średniej. Im większa wariancja, tym bardziej „rozrzucone" są dane. Wzór: σ² = Σ(xᵢ - μ)² / n, gdzie μ to średnia.

    Przykład 1 — MAŁA wariancja (dane skupione):
    wartości: [48, 50, 52, 49, 51]     średnia μ = 50
    σ² = ((48-50)² + (50-50)² + (52-50)² + (49-50)² + (51-50)²) / 5
       = (4 + 0 + 4 + 1 + 1) / 5 = 2.0

    Przykład 2 — DUŻA wariancja (dane rozrzucone):
    wartości: [10, 90, 30, 80, 50]     średnia μ = 52
    σ² = ((10-52)² + (90-52)² + (30-52)² + (80-52)² + (50-52)²) / 5
       = (1764 + 1444 + 484 + 784 + 4) / 5 = 896.0

    Mała σ² = punkty blisko średniej = dane JEDNORODNE
    Duża σ² = punkty daleko od średniej = dane RÓŻNORODNE

**Wewnątrzklasowa (within-class)** — „wewnątrz klasy" oznacza, że mierzymy wariancję OSOBNO dla każdej grupy (klasy), a potem ważymy wynik proporcją pikseli w grupie. Jeśli klasa 0 ma piksele [30, 50, 45] a klasa 1 ma piksele [180, 200, 190], to σ²_wewnątrz = (udział_kl0 × σ²_kl0) + (udział_kl1 × σ²_kl1).

**Wariancja wewnątrzklasowa (within-class variance)** — obliczasz wariancję KAŻDEJ klasy osobno, ważysz przez udział pikseli w tej klasie, sumujesz. Jeśli σ²_wewnątrz jest MAŁA → klasy są „jednorodne" (piksele w klasie 0 mają podobne jasności, piksele w klasie 1 też).

**Co to znaczy „klasy jednorodne"?** — jednorodna klasa to taka, w której WSZYSTKIE piksele mają podobne wartości. Np. klasa „tło" ma jasności [195, 200, 198, 205] → jednorodna (σ² mała). Klasa mieszająca tło i obiekt [30, 200, 50, 190] → niejednorodna (σ² duża). Otsu szuka progu T, który daje NAJBARDZIEJ jednorodne klasy.

**Histogram bimodalny (bimodal histogram)** — histogram z DWOMA wyraźnymi „garbami" (pikami). „Bi" = dwa, „modal" = moda (najczęstsza wartość). Typowy dla obrazów z jednym obiektem na tle — garb 1 odpowiada ciemnym pikselom (obiekt), garb 2 jasnym (tło). Otsu działa TYLKO gdy histogram jest bimodalny — bo szuka progu MIĘDZY garbami.

    Garb 1 (ciemne~60): piksele obiektu
    Garb 2 (jasne~190): piksele tła
    Dolina między garbami → tu Otsu stawia próg T!

    Gdyby histogram miał JEDEN garb (unimodalny) → brak naturalnego
    podziału → Otsu wybierze losowy próg → słaby wynik.

![Histogram bimodalny, wariancja wewnątrzklasowa i jednorodność klas — Otsu](img/q23_otsu_bimodal.png)

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

    Mnemonik: „PRÓG na bramce" — jak bramkarz, przepuszcza piksele jaśniejsze od T,
    blokuje ciemniejsze.

**Otsu** — automatyczny dobór progu. Algorytm: przetestuj WSZYSTKIE progi T=0..255, dla każdego oblicz wariancję wewnątrzklasową (jak „różnorodne" są piksele w klasie 0 i klasie 1). Wybierz T minimalizujące tę wariancję = klasy jak najbardziej jednorodne. Złożoność: O(n·L) gdzie n=piksele, L=poziomy jasności (256). Ograniczenie: działa TYLKO dla 2 klas i zakłada bimodalny histogram jasności (dwa „garby"). Patrz diagram powyżej.

    Pseudokod Otsu:
    best_T = 0
    min_var = ∞
    for T in 0..255:
        c0 = piksele z jasność ≤ T
        c1 = piksele z jasność > T
        w0 = len(c0) / len(all_pixels)
        w1 = len(c1) / len(all_pixels)
        var = w0 * variance(c0) + w1 * variance(c1)
        if var < min_var:
            min_var = var
            best_T = T
    return best_T

    Mnemonik: „AUTO-bramkarz Otsu" — sam sprawdza 256 progów i wybiera najlepszy.

---

#### Pojęcia kluczowe dla Region Growing

**Region Growing (rozrastanie regionu)** — zaczynasz od jednego piksela „ziarna" (seed) wybranego ręcznie lub automatycznie. Sprawdzasz sąsiadów: jeśli sąsiad jest PODOBNY (np. |jasność_sąsiada - jasność_regionu| < próg), dodaj go do regionu. Powtarzaj aż nie ma więcej podobnych sąsiadów. Następnie nowy seed → nowy region.

**Dlaczego seed „ręcznie LUB automatycznie"?** — to dwa różne scenariusze użycia:

    RĘCZNY seed:
    - Użytkownik klika myszką na obraz: „tu jest obiekt"
    - Użycie: segmentacja interaktywna (Photoshop „magic wand",
      narzędzia medyczne do zaznaczania guzów na RTG)
    - Zaleta: precyzyjny, użytkownik wie co chce segmentować
    - Wada: wymaga człowieka → nie skaluje się do 10 000 obrazów

    AUTOMATYCZNY seed — metody:
    1. Siatka (grid): seed co N pikseli (np. co 50 px na obrazie 500×500 → 100 seedów)
    2. Lokalne ekstrema histogramu: znajdź najczęstszą jasność → seed tam
    3. Losowanie: wylosuj K punktów jako seedy
    4. Analiza gradientu: piksele w „płaskich" regionach (brak krawędzi) → dobre seedy

    Dlaczego OR a nie AND?
    Bo to ALTERNATYWNE podejścia — albo człowiek wybiera (mało i precyzyjnie),
    albo algorytm wybiera (dużo i szybko, ale mniej precyzyjnie).

![Region Growing: seed ręczny vs automatyczny, krok po kroku, fale BFS](img/q23_region_growing.png)

    Pseudokod Region Growing:
    region = {seed}
    queue = [seed]
    while queue not empty:
        pixel = queue.pop()
        for neighbor in pixel.neighbors():  # 4 lub 8 sąsiadów
            if neighbor not visited AND similar(neighbor, region):
                region.add(neighbor)
                queue.append(neighbor)

    Mnemonik: „PLAMA atramentu" — seed to kropla atramentu na papierze,
    rozlewa się na podobne (jasne) miejsca, zatrzymuje się na granicach.

---

#### Pojęcia kluczowe dla Watershed

**Watershed (metoda zlewiska)** — traktuje obraz jak mapę topograficzną: wartość jasności piksela = wysokość terenu. Ciemne piksele = doliny, jasne = szczyty. Algorytm „zalewa" mapę wodą od najniższych punktów (minimów). Gdy woda z dwóch dolin się spotyka — tam jest GRANICA segmentu (grań).

![Watershed: obraz jako mapa topograficzna, zalewanie, over-segmentation i marker-controlled watershed](img/q23_watershed.png)

    Algorytm:
    1. Zamień obraz na „mapę wysokości" (jasność = wysokość)
    2. Znajdź wszystkie lokalne minima (najciemniejsze punkty)
    3. „Zalewaj" od minimów — woda rośnie równomiernie
    4. Gdy woda z dwóch dolin się spotyka → postaw TAMĘ (granicę segmentu)
    5. Kontynuuj aż cały obraz zalany

    Problem: MASYWNA over-segmentation — każde lokalne minimum (nawet szum!) → osobna dolina
    Rozwiązanie: marker-controlled watershed — użytkownik podaje markery (seedy),
    zalewamy TYLKO od tych markerów

    Mnemonik: „ZALEWANIE terenu" — wyobraź sobie model terenu z plasteliny w wannie.
    Powoli nalewasz wodę → doliny się wypełniają → granie gór = granice segmentów.

---

#### Pojęcia kluczowe dla Mean Shift

**Okno (window) / jądro (kernel)** — w kontekście Mean Shift to koło (lub kula w wielowymiarowej przestrzeni) o ustalonej szerokości (bandwidth = promień h) wokół aktualnego punktu. Wewnątrz okna algorytm oblicza „średnią ważoną" pozycji pikseli. Okno = jądro — to synonim. Nazwa „jądro" pochodzi od estymacji jądrowej gęstości (kernel density estimation, KDE).

    Okno o promieniu h = 30 wokół punktu (100, 150):
    Bierze WSZYSTKIE piksele, których cechy (jasność, x, y)
    są w odległości ≤ 30 od (100, 150).
    Oblicza ich średnią → przesuwa okno NA TĘ ŚREDNIĄ.
    Powtarza aż okno się „zatrzyma" (przesunięcie < ε).

**Najwyższa gęstość (density peak)** — punkt w przestrzeni cech, gdzie jest NAJWIĘKSZE skupisko pikseli. Jak najwyższy szczyt góry w 3D. Mean Shift = „przesuń w kierunku średniej" → iteracyjnie zbliża się do szczytu gęstości.

**Przestrzeń cech (feature space)** — każdy piksel jest opisany nie tylko pozycją (x, y) ale też cechami koloru (jasność, R, G, B). Przestrzeń cech to przestrzeń wielowymiarowa, np. (R, G, B, x, y) = 5 wymiarów. Piksele o podobnych kolorach i blisko siebie będą blisko w przestrzeni cech → tworzą klastry (skupiska).

    Piksel A: (x=100, y=200, R=30, G=25, B=35)  → punkt w 5D
    Piksel B: (x=102, y=201, R=32, G=27, B=33)  → BLISKO A w 5D
    Piksel C: (x=105, y=198, R=200, G=210, B=220)  → DALEKO od A w 5D (inny kolor!)
    → A i B w jednym segmencie, C w innym

**Dlaczego Mean Shift NIE wymaga podania liczby segmentów?** — W K-means musisz podać K=3 (trzy klastry) ZANIM uruchomisz algorytm. Mean Shift działa inaczej: każdy piksel startuje i „toczy się" do najbliższego szczytu gęstości. Ile jest szczytów = tyle segmentów. Algorytm sam ODKRYWA liczbę klastrów. Parametrem jest tylko bandwidth (szerokość okna h): duże h → mało szczytów → mało segmentów; małe h → dużo szczytów → dużo segmentów.

![Mean Shift: przestrzeń cech, jądro przesuwane do max gęstości, dlaczego bez K](img/q23_mean_shift.png)

    Pseudokod Mean Shift:
    for each pixel p:
        x = p.features  # np. (R, G, B, pos_x, pos_y)
        repeat:
            window = all pixels within distance h from x
            x_new = weighted_mean(window)
            if |x_new - x| < epsilon:
                break
            x = x_new
        p.cluster = x  # zbieżny punkt = ID klastra

    Mnemonik: „KULKI toczą się do dołków" — rozsyp kulki na nierównym stole,
    każda toczy się do najbliższego zagłębienia. Ile dołków = tyle segmentów.

---

#### Pojęcia kluczowe dla Normalized Cuts

**Cięcie grafu (graph cut)** — graf to zbiór węzłów (pikseli) połączonych krawędziami (z wagami = podobieństwo). „Ciąć graf" to znaleźć LINIĘ dzielącą węzły na grupy, tak aby krawędzie „przecięte" tą linią miały niską wagę (= łączyły niepodobne piksele), a krawędzie wewnątrz grup miały wysoką wagę (= łączyły podobne piksele).

**Jak szukamy cięcia?** — Naiwnie: sprawdź WSZYSTKIE możliwe podziały → wykładnicza złożoność. Normalized Cuts zamienia problem na rozwiązanie „problemu wartości własnych" (eigenvalue problem) macierzy Laplacianu grafu. Drugi najmniejszy wektor własny wskazuje, które piksele należą do grupy A (wartości dodatnie) a które do B (wartości ujemne).

**Dlaczego „znormalizowane" (normalized)?** — Zwykłe cięcie (min-cut) ma wadę: preferuje odcinanie MALUTKICH grup (1 piksel odcięty = małe cięcie). Normalizowanie dzieli koszt cięcia przez rozmiar grup → duże, zrównoważone segmenty.

![Normalized Cuts: obraz jako graf, cięcie, algorytm krok po kroku](img/q23_normalized_cuts.png)

    Pseudokod Normalized Cuts (uproszczony):
    # 1. Zbuduj macierz podobieństwa W
    for each pair of pixels (i, j):
        W[i,j] = exp(-|color_i - color_j|^2 / sigma^2)  # jeśli sąsiedzi
        W[i,j] = 0                                        # jeśli odlegli

    # 2. Macierz stopni D
    D = diag(sum(W, axis=1))  # D[i,i] = suma wiersza i

    # 3. Rozwiąż problem wartości własnych
    (D - W) * y = lambda * D * y
    # Weź DRUGI najm. wektor własny y (pierwszy = trywialny)

    # 4. Podziel piksele
    segment_A = {i : y[i] > 0}
    segment_B = {i : y[i] <= 0}

    Mnemonik: „CIĘCIE sznurków" — piksele połączone sznurkami (mocne = podobne).
    Tnij SŁABE sznurki → dwie grupy. Normalizacja = nie odcinaj samotnych pikseli.

---

#### Pojęcia kluczowe dla sieci neuronowych

**ReLU (Rectified Linear Unit)** — najpopularniejsza funkcja aktywacji w sieciach neuronowych. Wzór: ReLU(x) = max(0, x). Jeśli wejście jest ujemne → wynik = 0 (neuron „milczy"). Jeśli wejście jest dodatnie → wynik = x (neuron „przepuszcza" sygnał bez zmiany). Prosta, ale bardzo skuteczna — szybsza od starszych funkcji (sigmoid, tanh), bo nie wymaga obliczania exp().

    ReLU(-3) = max(0, -3) = 0    ← neuron „wyłączony"
    ReLU(0)  = max(0, 0)  = 0    ← na granicy
    ReLU(2.5) = max(0, 2.5) = 2.5 ← neuron „włączony", przekazuje 2.5

    Dlaczego nie po prostu f(x) = x (bez progu)?
    Bo liniowość → cała sieć = jedna warstwa liniowa (tracisz głębokość).
    ReLU jest NIELINIOWA (ma „zakręt" w 0) → pozwala sieci uczyć się
    skomplikowanych wzorców.

![ReLU: wykres funkcji, dlaczego ReLU, przykład numeryczny](img/q23_relu.png)

**Iloczyn skalarny (dot product)** — operacja na dwóch wektorach (listach liczb) dająca JEDNĄ liczbę. Mnożysz odpowiednie elementy parami i sumujesz wyniki. W CNN konwolucja = iloczyn skalarny filtra × fragment obrazu. Duży wynik = wektory „podobne" (filtr pasuje do fragmentu).

    a = [1, 3, -2]     b = [4, -1, 5]
    a · b = 1·4 + 3·(-1) + (-2)·5 = 4 - 3 - 10 = -9

    W konwolucji:
    filtr = [-1, 0, 1, -1, 0, 1, -1, 0, 1]  (spłaszczony 3×3)
    fragment = [50, 50, 200, 50, 50, 200, 50, 50, 200]
    dot = (-1)·50 + 0·50 + 1·200 + ... = 450 → duży = krawędź!

![Iloczyn skalarny: definicja, geometryczna interpretacja, użycie w konwolucji](img/q23_dot_product.png)

---

**Warstwa Fully Connected (FC, gęsta, dense)** — warstwa, w której KAŻDY neuron jest połączony z KAŻDYM wejściem. Obraz 7×7×512 (po konwolucjach) = 25 088 wartości. FC z 4096 neuronami = 25 088 × 4 096 = **~103 miliony wag**. Wady: (1) wymaga STAŁEGO rozmiaru wejścia (zawsze 7×7×512), (2) traci informację GDZIE coś jest (spłaszcza przestrzeń na wektor 1D).

**Konwolucja (convolution)** — operacja przesuwania małego filtra (np. 3×3) po obrazie. W każdej pozycji oblicza iloczyn skalarny filtra × fragment obrazu → jedną liczbę. TE SAME wagi filtra użyte w KAŻDEJ pozycji → dzielenie parametrów. Zachowuje informację przestrzenną (GDZIE coś jest).

**Conv 1×1 (konwolucja punktowa)** — filtr o rozmiarze 1×1 pikseli. „Patrzy" na JEDEN piksel, ale WSZYSTKIE kanały (np. 512). Działa jak FC, ale OSOBNO dla KAŻDEGO piksela → zachowuje mapę H×W. FCN zamienia FC na Conv 1×1: zamiast spłaszczyć 7×7×512 → 25 088 → FC, robi Conv1×1 na KAŻDYM z 7×7 pikseli × 512 kanałów → mapa 7×7×C (C = liczba klas).

**Jak FCN zamienia FC na Conv 1×1?** — Klasyczny CNN: ostatnia mapa cech 7×7×512 → FLATTEN → wektor 25 088 → FC → 1000 klas → „to jest kot". FCN: ostatnia mapa cech H×W×512 → Conv1×1(512→C) → mapa H×W×C → upsample do pełnej rozdzielczości. Kluczowa różnica: NIE spłaszczamy → możemy przetwarzać obraz o DOWOLNYM rozmiarze.

**Skip connections z encodera** — w encoder-decoder encoder zmniejsza obraz (pooling): 224→112→56→28→14. W tym procesie traci DETALE przestrzenne (dokładne krawędzie). Skip connections = „drogi na skróty" — cechy z wczesnych warstw encodera (pełne detali) są przekazywane WPROST do odpowiednich warstw decodera. Decoder wie CO i GDZIE.

![FCN: warstwa FC vs Conv 1×1, konwolucja, skip connections](img/q23_fc_vs_conv1x1.png)

---

**U-Net — dlaczego kształt „U"?** — Narysuj architekturę: encoder zmniejsza rozdzielczość (bloki idą w DÓŁ po lewej stronie), bottleneck jest na dole, decoder zwiększa rozdzielczość (bloki idą W GÓRĘ po prawej stronie). Wizualnie tworzy literę „U". „Encoder schodzi w dół" = każda warstwa encodera ma MNIEJSZĄ rozdzielczość (224→112→56→28), wizualizowane jako bloki o malejącym rozmiarze ułożone jeden pod drugim.

**Concatenation (konkatenacja, złączenie)** — operacja „sklejania" dwóch tensorów wzdłuż osi kanałów. Jeśli encoder na poziomie 2 daje mapę 128×128×64 kanałów, a decoder na poziomie 2 daje mapę 128×128×64 kanałów, to concatenation = 128×128×**128** kanałów (64+64). Różni się od DODAWANIA (addition), które daje 128×128×64 (element-wise sum). Concatenation zachowuje WIĘCEJ informacji — sieć sama wybiera, które kanały wykorzystać.

    Dodawanie (ResNet-style):
    encoder [a, b, c] + decoder [x, y, z] = [a+x, b+y, c+z]  → 3 kanały

    Concatenation (U-Net-style):
    encoder [a, b, c] ++ decoder [x, y, z] = [a, b, c, x, y, z]  → 6 kanałów!
    → więcej informacji, sieć sama zdecyduje co ważne

![U-Net: architektura w kształcie U, skip connections z concatenation, encoder ↓ decoder ↑](img/q23_unet_arch.png)

    Mnemonik U-Net: „Litera U — w dół i w górę" — encoder schodzi ↓ (zmniejsza),
    decoder wraca ↑ (zwiększa), między nimi mosty (skip = concat).

---

**Receptive field (pole widzenia, pole recepcyjne)** — ile pikseli WEJŚCIOWYCH wpływa na JEDEN piksel wyjściowy. Konwolucja 3×3 → RF = 3×3. Dwie konwolucje 3×3 pod rząd → RF = 5×5 (druga widzi 3×3 fragmenty, z których każdy widział 3×3 → efektywnie 5×5). Większe RF = neuron widzi większy kontekst = lepiej rozumie co to za piksel.

**Dlaczego większe RF jest lepsze?** — Pojedynczy piksel o jasności 150 może być fragmentem nieba LUB samochodu. Patrząc na otoczenie 3×3 → nadal nie wiesz. Patrząc na otoczenie 50×50 → widzisz budynki obok → „to droga!". Segmentacja wymaga KONTEKSTU globalnego.

**Rate (współczynnik dylatacji)** — parametr atrous (dilated) convolution. Rate=1 = zwykła konwolucja (filtr dotyka sąsiadów). Rate=2 = filtr próbkuje co DRUGI piksel → RF rośnie z 3×3 do 5×5 przy TYCH SAMYCH 9 wagach. Rate=3 → RF = 7×7. Większy kontekst za darmo (bez dodatkowych parametrów).

**Global Average Pooling (GAP)** — operacja redukcji: mapa cech H×W×C → 1×1×C. Dla KAŻDEGO kanału oblicza ŚREDNIĄ ze wszystkich H×W pikseli. Wynik: jeden wektor o wymiarze C, reprezentujący „średnią informację" z całego obrazu. RF = nieskończone (cały obraz). Używane w ASPP DeepLab jako jedna z równoległych gałęzi.

    Mapa cech 7×7×512:
    Kanał 0: macierz 7×7 wartości → średnia → jedna liczba
    Kanał 1: macierz 7×7 wartości → średnia → jedna liczba
    ...
    Kanał 511: macierz 7×7 wartości → średnia → jedna liczba
    Wynik: wektor [avg₀, avg₁, ..., avg₅₁₁] → 1×1×512

![Receptive field: zwykła vs dilated konwolucja, rate, global average pooling](img/q23_receptive_field.png)

---

**Transformer** — architektura sieci neuronowej zaproponowana w 2017 (Vaswani et al., „Attention Is All You Need"). Oryginalnie dla NLP (tłumaczenie), od 2020 (ViT — Vision Transformer) stosowana w wizji komputerowej. Kluczowy mechanizm: **self-attention** — każdy element (piksel/token) „pyta" WSZYSTKIE inne elementy: „jak bardzo jesteś ze mną powiązany?". Każdy element tworzy trzy wektory: Q (Query — czego szukam?), K (Key — co oferuję), V (Value — moja wartość). Attention = softmax(Q·Kᵀ / √d) · V. Koszt: O(n²) pamięci (n = liczba elementów).

**SOTA (State Of The Art)** — najlepszy znany wynik na danym benchmarku (zbiorze testowym) w danym momencie. Np. „Mask2Former osiąga mIoU 57.8% na ADE20K — to aktualny SOTA". SOTA ciągle się zmienia — każdy nowy paper może pobić poprzedni rekord.

![Transformer: CNN lokalny vs Transformer globalny, self-attention Q/K/V, SOTA](img/q23_transformer_attention.png)

---

**mIoU (mean Intersection over Union)** — standardowa metryka segmentacji. Dla każdej klasy: IoU = (piksele poprawne ∩ ground truth) / (piksele poprawne ∪ ground truth). Potem średnia z klas.

    Klasa "samochód": predykcja=100 pikseli, GT=120, wspólne=80
    IoU = 80 / (100+120-80) = 80/140 = 0.571 = 57.1%

**Dice Loss** — funkcja kosztu powiązana z IoU: 2·|A∩B| / (|A|+|B|). Popularna w segmentacji medycznej (dobrze radzi sobie z class imbalance).

**Focal Loss** — modyfikacja cross-entropy redukująca wpływ łatwych przykładów, skupiająca uczenie na trudnych. Kluczowa przy class imbalance (np. 99% tła, 1% obiekt).

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

| Metoda | Idea | Wada | Złożoność | Mnemonik |
|--------|------|------|-----------|----------|
| **Thresholding** | piksel > T → klasa 1, else → klasa 0 | tylko 2 klasy, proste sceny | O(n) | „PRÓG na bramce" |
| **Otsu** | automatyczny próg (min wariancja wewnątrzklasowa) | j.w. ale dobiera T sam | O(n·L) | „AUTO-bramkarz" |
| **Region Growing** | dodawaj sąsiednie piksele o podobnej wartości | over-segmentation, zależy od seeda | O(n) | „PLAMA atramentu" |
| **Watershed** | obraz = mapa wysokości, granice = granie gór | over-segmentation | O(n log n) | „ZALEWANIE terenu" |
| **Mean Shift** | iteracyjnie przesuwaj jądro do max gęstości | wolny | O(n²) | „KULKI toczą się" |
| **Normalized Cuts** | piksele = węzły grafu, minimalizuj znormalizowane cięcie | bardzo wolny | O(n³) | „CIĘCIE sznurków" |

#### DIY Przykład — Thresholding (Otsu) krok po kroku

Poniższy diagram pokazuje CAŁY pipeline progowania Otsu od obrazu wejściowego do wyniku. Obraz syntetyczny 64×64 z ciemnym kołem na jasnym tle — typowy przypadek bimodalny.

![DIY Thresholding + Otsu: obraz → histogram bimodalny → progowanie → szukanie min σ² → pseudokod → wynik](img/q23_diy_thresholding.png)

    Pseudokod Otsu (Python-style):
    best_T, min_var = 0, float('inf')
    for T in range(256):
        c0 = pixels[pixels <= T]      # piksele ciemne
        c1 = pixels[pixels > T]       # piksele jasne
        if len(c0) == 0 or len(c1) == 0:
            continue
        w0 = len(c0) / len(pixels)    # udział klasy 0
        w1 = len(c1) / len(pixels)    # udział klasy 1
        var = w0 * variance(c0) + w1 * variance(c1)  # σ² wewnątrzklasowa
        if var < min_var:
            min_var = var
            best_T = T
    # best_T = optymalny próg (np. 128)
    result = (pixels > best_T).astype(int)  # binaryzacja

**Wspólna wada klasycznych metod:** wymagają ręcznego doboru parametrów (próg, seed, kernel), nie uczą się cech z danych, słabe na złożonych obrazach naturalnych.

---

### Sieci neuronowe (deep learning)

Metody uczące się automatycznie rozpoznawać cechy z danych treningowych. Wszystkie oparte na architekturze **encoder-decoder** z wariacjami.

**Wspólna idea encoder-decoder:**

    Encoder: obraz [224×224] → [112] → [56] → [28] → [14]   (wyciąga CECHY)
    Decoder: cechy [14] → [28] → [56] → [112] → [224×224]   (odtwarza MAPĘ)
                                   bottleneck

| Sieć | Rok | Kluczowa innowacja | Use case | Mnemonik |
|------|-----|-------------------|----------|----------|
| **FCN** | 2015 | w pełni konwolucyjna + skip connections | pierwsza end-to-end | „FC → Conv 1×1" |
| **U-Net** | 2015 | U-shape + skip concat + data augmentation | segmentacja medyczna | „Litera U + mosty" |
| **DeepLab v3+** | 2018 | atrous (dilated) conv + ASPP | general-purpose | „DZIURY w filtrze" |
| **SegFormer** | 2021 | transformer encoder (self-attention) | SOTA lightweight | „WSZYSCY ze WSZYSTKIMI" |
| **Mask2Former** | 2022 | masked attention + unified architecture | SOTA universal | „WSZYSCY ze WSZYSTKIMI" |

**FCN (Fully Convolutional Network):**

    Mnemonik: „FC → Conv 1×1 = otwieramy bramkę dla DOWOLNEGO rozmiaru"
    Zwykły CNN:  Conv → Conv → Pool → ... → FC → FC → "kot"
    FCN:         Conv → Conv → Pool → ... → Conv1×1 → Upsample → mapa pikseli
    Innowacja: zamiana FC na Conv1×1 → wejście dowolnego rozmiaru
    Skip connections: łączą cechy z encodera → zachowują detale przestrzenne

**U-Net:**

    Mnemonik: „Litera U + mosty" — schodzisz w dół, wracasz w górę,
    po drodze mosty (skip connections z concat) przenoszą detale.
    Encoder (↓)         Decoder (↑)
    [64]────skip────→[64]        ← skip connections = concatenation
    [128]───skip───→[128]           (przenosi detale z encodera do decodera)
    [256]──skip──→[256]
    [512]─skip─→[512]
         [1024]                  ← bottleneck
    Dlaczego medycyna? Działa dobrze z MAŁYMI zbiorami danych (data augmentation)

**DeepLab v3+:**

    Mnemonik: „DZIURY w filtrze" — filtr dosłownie ma dziury (à trous),
    przez co widzi dalej bez dodatkowych parametrów.
    Zwykła konwolucja 3×3:   [x][x][x]         receptive field = 3
    Dilated (rate=2):        [x][ ][x][ ][x]   receptive field = 5, te same parametry!
    ASPP: równolegle rate=6,12,18 → multi-scale features → łączenie
    Efekt: widzi kontekst globalny BEZ zwiększania parametrów

**Transformery (SegFormer, Mask2Former):**

    Mnemonik: „WSZYSCY ze WSZYSTKIMI" — każdy piksel rozmawia z KAŻDYM innym.
    CNN: filtr 3×3 widzi LOKALNY kontekst (sąsiadów)
    Transformer: self-attention widzi CAŁY obraz naraz
    Cena: O(n²) pamięci (n = piksele), ale lepsze wyniki

#### DIY Przykład — U-Net krok po kroku

Poniższy diagram pokazuje CAŁY pipeline U-Net od obrazu wejściowego do mapy segmentacji. Obraz syntetyczny 64×64 z dwoma obiektami (koła) na jasnym tle.

![DIY U-Net: obraz → encoder zmniejsza → bottleneck → decoder zwiększa + skip → mapa segmentacji → pseudokod](img/q23_diy_unet.png)

    Pseudokod U-Net (PyTorch-style):
    # ENCODER — zmniejsza rozdzielczość, wyciąga cechy
    e1 = conv_block(input, filters=64)      # [64×64×64]
    e2 = conv_block(maxpool(e1), filters=128)  # [32×32×128]
    e3 = conv_block(maxpool(e2), filters=256)  # [16×16×256]

    # BOTTLENECK — najgłębsza warstwa
    b = conv_block(maxpool(e3), filters=512)   # [8×8×512]

    # DECODER — zwiększa rozdzielczość + skip connections (concat!)
    d3 = conv_block(concat(upconv(b), e3), filters=256)    # [16×16×256]
    d2 = conv_block(concat(upconv(d3), e2), filters=128)   # [32×32×128]
    d1 = conv_block(concat(upconv(d2), e1), filters=64)    # [64×64×64]

    # WYNIK — Conv 1×1 → mapa klas
    output = conv_1x1(d1, n_classes=3)  # [64×64×3] → argmax → [64×64] etykiety

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

**Super-mnemonik na kolejność algorytmów:**

    „Turyści Oglądają Rzekę, Wodospad, Morze, Nurt — Fotografują Uroczy Dwór Tajemnic"

    Klasyczne: Thresholding → Otsu → Region growing → Watershed → Mean shift → Normalized cuts
    Neuronowe: FCN → U-Net → DeepLab → Transformer

![Mnemoniki: karty z algorytmami segmentacji i ich skojarzeniami](img/q23_mnemonics.png)

**Mnemoniki per algorytm — STRATEGIE KLASYCZNE:**

| Algorytm | Mnemonik | Skojarzenie |
|----------|----------|-------------|
| **Thresholding** | „PRÓG na bramce" | Bramkarz przepuszcza piksele > T, blokuje ≤ T |
| **Otsu** | „AUTO-bramkarz" | Sam sprawdza 256 progów, wybiera najlepszy (min σ²) |
| **Region Growing** | „PLAMA atramentu" | Kropla atramentu rozlewa się na podobne piksele (BFS) |
| **Watershed** | „ZALEWANIE terenu" | Woda zalewa doliny, granie gór = granice segmentów |
| **Mean Shift** | „KULKI toczą się do dołków" | Każda kulka → max gęstości, ile dołków = tyle segmentów |
| **Normalized Cuts** | „CIĘCIE sznurków" | Tnij słabe sznurki (krawędzie grafu), zachowaj silne |

**Mnemoniki per algorytm — SIECI NEURONOWE:**

| Sieć | Mnemonik | Skojarzenie |
|------|----------|-------------|
| **FCN** | „FC → Conv 1×1" | Otwiera bramkę dla dowolnego rozmiaru wejścia |
| **U-Net** | „Litera U + mosty" | Schodzisz ↓, wracasz ↑, mosty (skip concat) przenoszą detale |
| **DeepLab** | „DZIURY w filtrze" | Filtr ma dziury (à trous) → widzi dalej bez dodatkowych wag |
| **Transformer** | „WSZYSCY ze WSZYSTKIMI" | Każdy piksel pyta każdy inny (self-attention, O(n²)) |

**Mnemoniki per metrykę:**

- **mIoU** = „Nakładka / Suma" → intersection / union, uśrednione per klasa
- **Dice** = „Dwie nakładki / Razem" → 2·|A∩B| / (|A|+|B|)
- **Focal** = „Fokus na TRUDNYCH" → trudne piksele ważą więcej

