# Skrypt do prezentacji (~10 minut)

## Slajd 1 — Strona tytułowa
Dzień dobry, nazywam się Krzysztof Rudnicki. Tematem mojej pracy magisterskiej jest porównanie wydajności i możliwości współczesnych silników gier komputerowych. Promotorem pracy jest doktor inżynier Michał Chwesiuk.

## Slajd 2 — Plan prezentacji
Prezentacja składa się z siedmiu części: omówię cel pracy, metodologię badań, implementację gier testowych, narzędzie profilowania, wyniki testów wydajności, wnioski z wywiadów z deweloperami i podsumowanie.

## Slajd 3 — Motywacja
Rynek gier komputerowych jest zdominowany przez dwa silniki. Unity ma prawie 25 tysięcy gier na platformie Steam, a Unreal Engine ponad 7500. Pomimo tej dominacji, brakuje systematycznych badań porównawczych, które w sposób obiektywny zestawiałyby te dwa silniki pod kątem wydajności i możliwości.

## Slajd 4 — Cel pracy
Praca realizuje cztery cele: po pierwsze — testy wydajności z użyciem narzędzia NVIDIA Nsight Systems. Po drugie — implementację identycznej gry w obu silnikach. Po trzecie — analizę porównawczą ich funkcjonalności. I po czwarte — wywiady z ośmioma deweloperami gier, żeby uzyskać perspektywę praktyczną.

## Slajd 5 — Hipoteza
Hipoteza badawcza brzmi: Unity osiągnie lepszą wydajność w grze 2D bullet hell dzięki natywnemu wsparciu dla grafiki dwuwymiarowej.

## Slajd 6 — Bullet hell (obraz Touhou)
Jako gatunek testowy wybrałem bullet hell. To gry, w których na ekranie pojawiają się setki, a nawet tysiące pocisków jednocześnie. Taki gatunek doskonale testuje zarządzanie pamięcią — czyli garbage collector w Unity kontra ręczne zarządzanie w C++ — a także wydajność wykrywania kolizji i ogólną skalowalność silnika przy rosnącym obciążeniu. Dodatkową zaletą jest prosta koncepcja rozgrywki, co pozwala skupić się wyłącznie na aspekcie wydajnościowym.

## Slajd 7 — Parametry gry testowej
Gra testowa trwa 90 sekund. Występują trzy typy przeciwników z różnymi wzorcami strzelania. Trudność eskaluje w trzech fazach — od niskiej, przez średnią, po wysoką, z maksymalną liczbą 200 jednoczesnych przeciwników. Interwał pojawiania się wrogów zmniejsza się z 0,25 do 0,08 sekundy.

## Slajd 8 — Środowisko testowe
Testy przeprowadzono na komputerze z procesorem AMD Ryzen 9 7900X3D, kartą graficzną NVIDIA RTX 3090 i 32 gigabajtami pamięci RAM, pod kontrolą systemu Arch Linux. Użyto Unity w wersji 6.0 LTS oraz Unreal Engine 5.5.3. Profilerem był NVIDIA Nsight Systems.

## Slajd 9 — Implementacja Unity (tekst)
Implementacja w Unity wykorzystuje język C# i natywny tryb 2D silnika. Do fizyki użyto komponentów Rigidbody2D i Collider2D. Object pooling zrealizowano prostą metodą SetActive — włączamy i wyłączamy obiekty zamiast je niszczyć i tworzyć od nowa. Unity oferuje też hot reload, co przyspiesza iterację. Instalacja silnika zajęła około 30 minut.

## Slajd 10 — Implementacja Unity (zrzut ekranu)
Tutaj widzimy zrzut z gry w Unity — widoczni są przeciwnicy, pociski i gracz na ekranie.

## Slajd 11 — Implementacja Unreal (tekst)
W Unreal Engine implementacja wymagała C++ i Blueprintów. Ponieważ Unreal nie ma natywnego trybu 2D, zastosowałem tak zwane fałszywe 2D — gra działa w środowisku trójwymiarowym z kamerą ustawioną prostopadle. Object pooling był bardziej złożony i wymagał trzech oddzielnych wywołań: ukrycie aktora, wyłączenie kolizji i wyłączenie logiki tick. Instalacja na Linuksie zajęła od dwóch do czterech godzin.

## Slajd 12 — Implementacja Unreal (zrzut ekranu)
A tutaj analogiczny widok gry w Unreal Engine.

## Slajd 13 — Porównanie implementacji (tabela)
Zestawienie doświadczeń implementacyjnych pokazuje wyraźne różnice. Unity ma niższy próg wejścia, szybszą kompilację, prostszy object pooling i pełny hot reload. Unreal wymaga więcej czasu na instalację i konfigurację, ale oferuje dostęp do kodu źródłowego silnika.

## Slajd 14 — Dlaczego Nsight?
Dlaczego zastosowałem zewnętrzne narzędzie, a nie wbudowane profilery silników? Wbudowane profilery używają różnych definicji metryk, mają różny narzut profilowania i generują nieporównywalne formaty wyjściowe. NVIDIA Nsight Systems to niezależne narzędzie, które analizuje obie aplikacje na tym samym poziomie — wywołań Vulkan API — z minimalnym narzutem na poziomie sterownika i spójnym formatem danych.

## Slajd 15 — Nsight (zrzut ekranu)
Na ekranie widzimy interfejs Nsight Systems z oś czasu wywołań GPU i CPU, który pozwala na szczegółową analizę każdej klatki.

## Slajd 16 — Unity: wydajność klatek
Przejdźmy do wyników. Unity wyrenderowało prawie 13 i pół tysiąca klatek w 94 sekundach, co daje średnio 144 klatki na sekundę — czyli dokładnie tyle, ile wynosi V-Sync na monitorze testowym. Mediana czasu klatki to 6,94 milisekundy, a 99. percentyl — 7,58 milisekundy. Prawie 98 i ćwierć procenta klatek mieściło się w przedziale 5 do 10 milisekund. Rozstęp międzykwartylowy wynosi zaledwie 0,08 milisekundy, co świadczy o bardzo wysokiej stabilności.

## Slajd 17 — Unity: architektura renderowania
Unity stosuje prosty potok renderowania — zaledwie 2 wywołania vkQueueSubmit na klatkę. Funkcja vkWaitForFences zajmowała ponad 95% czasu Vulkan API, co oznacza, że CPU czekał na GPU, a nie odwrotnie — klasyczny scenariusz GPU-bound. W całym teście Unity użyło tylko 3 potoków graficznych i około 219 tysięcy wywołań Vulkan API. Wykorzystanie GPU wynosiło jedynie 23%, bo V-Sync ograniczał liczbę klatek.

## Slajd 18 — Unreal: wydajność klatek
Unreal Engine działał bez V-Sync, więc osiągał 332 do 339 klatek w fazach pierwszej i drugiej. W wymagającej fazie trzeciej wydajność spadła do 162 FPS — czyli spadek o ponad połowę. Wykorzystanie GPU sięgało 91% w lekkich fazach i spadało do 50% w ciężkiej fazie. Warto zwrócić uwagę, że liczba submitów na klatkę jest stała — 16,2 — niezależnie od obciążenia.

## Slajd 19 — Unreal: architektura renderowania
Unreal ma znacznie bardziej złożony potok — 16 wywołań submit na klatkę, podczas gdy Unity ma tylko 2. Tworzenie potoków graficznych pochłaniało od 47 do 72% czasu Vulkan API. Unreal tworzył około tysiąc potoków na fazę, w porównaniu do zaledwie trzech w Unity. Łącznie Unreal wykonał 32 miliony wywołań Vulkan API i 9 milionów wywołań synchronizacji na poziomie systemu operacyjnego. Intensywnie korzysta też z compute shaderów do operacji takich jak culling i post-processing.

## Slajd 20 — Porównanie kluczowych wyników
Tabela zestawia najważniejsze metryki. Unreal generuje 64-krotnie więcej wywołań Vulkan API, ponad 300-krotnie więcej wywołań synchronizacji OS i 800-krotnie więcej potoków graficznych. To odzwierciedla fundamentalną różnicę w architekturze — Unreal ma potok zaprojektowany pod gry 3D AAA, który w kontekście prostej gry 2D generuje znaczący narzut.

## Slajd 21 — Interpretacja: Unity
Podsumowując wyniki Unity: prosty dwuetapowy potok okazał się bardzo wydajny dla gier 2D. Czasy klatek były niezwykle stabilne. Jednocześnie GPU było wykorzystane jedynie w 23 procentach, co sugeruje duży zapas wydajności.

## Slajd 22 — Interpretacja: Unreal
Z kolei Unreal Engine cechuje złożony, wieloetapowy potok, który w przypadku prostych scen 2D generuje zbędny narzut. Silnik ciągle rekompiluje potoki graficzne w ramach dynamicznej optymalizacji. Wykorzystanie GPU sięgało 91%, ale przy dużym obciążeniu wydajność spadała o ponad połowę.

## Slajd 23 — Wywiady (1/2)
W ramach pracy przeprowadziłem wywiady z ośmioma deweloperami o doświadczeniu od roku do dziesięciu lat. Respondenci potwierdzili, że próg wejścia do Unity jest niższy. Dokumentacja Unity jest lepsza dzięki konkretnym przykładom kodu, podczas gdy dokumentacja Unreala bywa określana jako szkieletowa. Blueprinty ułatwiają współpracę z osobami nietechnicznymi, ale powodują problemy z kontrolą wersji w Gicie.

## Slajd 24 — Wywiady (2/2)
Dalsze wnioski: architektura Unreala wymusza pewien porządek w kodzie, podczas gdy Unity daje większą elastyczność. C# jest postrzegany jako łatwiejszy język, a C++ w Unrealu jest opisywany jako niestandardowy z powodu makr i systemu refleksji. Jeśli chodzi o dostępność materiałów edukacyjnych, Unity ma przewagę ilościową.

## Slajd 25 — Weryfikacja hipotezy
Wracając do hipotezy — wyniki wskazują, że Unity ma prostszą architekturę renderowania, stabilniejsze czasy klatek, łatwiejszy i szybszy proces implementacji oraz natywne wsparcie dla grafiki 2D.

## Slajd 26 — Rekomendacje
Na podstawie wyników przygotowałem macierz rekomendacji. Unity jest lepszym wyborem dla gier 2D indie, gier mobilnych i szybkiego prototypowania. Unreal sprawdzi się lepiej w grach 3D AAA dzięki technologiom Nanite i Lumen, w projektach VR high-end i w zespołach mieszanych, gdzie Blueprinty ułatwiają współpracę.

## Slajd 27 — Wkład pracy
Wkład tej pracy obejmuje: zunifikowaną metodykę pomiaru z użyciem Nsight Systems, szczegółową analizę na poziomie Vulkan API, triangulację metod badawczych łączącą testy, wywiady i implementację, oraz praktyczne rekomendacje w postaci macierzy wyboru silnika.

## Slajd 28 — Ograniczenia
Praca ma swoje ograniczenia: badanie dotyczy jednego gatunku gry, przeprowadzono je na jednej, wydajnej konfiguracji sprzętowej, a wywiady objęły ośmiu respondentów, co kwalifikuje je jako badanie eksploracyjne.

## Slajd 29 — Dalsze badania
W przyszłości warto przeprowadzić testy dla innych gatunków, takich jak RPG, RTS czy gry logiczne. Przydatne byłoby też zbadanie wydajności na różnych platformach — mobile, konsolach, słabszych komputerach. Można też stworzyć automatyczny framework benchmarkowy i powtarzać badanie co kilka lat, śledząc rozwój silników.

## Slajd 30 — Dziękuję za uwagę
Dziękuję za uwagę. Jestem gotowy na pytania.
