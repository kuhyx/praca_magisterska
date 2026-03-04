**24\. Opisać problem detekcji obiektów w obrazach. Przedstawić podstawowe strategie i algorytmy detekcji przy użyciu metod klasycznych oraz sieci neuronowych. Jak skonstruować detektor obiektów dysponując istniejącym klasyfikatorem tych obiektów? TWM**

Detekcja jest trudniejsze niż klasyfikacja, ponieważ oprócz określenia klas do których należy obiekt trzeba też określić lokalizację, przez co detekcja jest o wiele bardziej czasochłonna.  
 Wyjściem detektora może być klasa i prostokąt w którym znajduje się obiekt, ale niektóre detektory zwracają też maskę obiektu.

Metoda okna przesuwnego – wzdłuż obrazu przesuwane jest okno o określonych rozmiarach.  
 Dla każdego okna określa się wektor cech obrazu i używa się klasyfikator cech i określenie wiarygodności klasyfikacji.  
 Wyniki klasyfikacji podlegają dalszemu filtrowaniu.  
 Klasyfikator musi również znać również klasę Tło

W celu przyspieszenia metody okna przesuwnego można zastosować klasyfikator kaskadowy- na szybko odrzucamy tło i potem analizujemy to co nie odrzuciliśmy.  
 Można też użyć AdaBoost dla którego cały klasyfikator stanowi sumę wyników klasyfikatorów prostszych.

Dopasowanie za pomocą punktów charakterystycznych – ekstrakcja punktów charakterystycznych i potem dopasowanie punktów charakterystycznych obiektu i obrazu

R-CNN  
         	propozycje regionów (odnalezienie prawdopodobnej lokalizacji i rozmiaru obiektu znanych klas)  
         	klasyfikacja regionu i uściślenie pozycji i rozmiaru obiektu

Region-Based Fully Convolutional Network  
         	propozycja regionów  
         	wiele map wyjściowych – każda określa odrębne przekonanie, że obiekt jest w pewnej relacji przestrzennej od danej pozycji (np. w lewo-dół)  
         	Pooling selektywny – wykorzystywane są tylko wybrane mapy wyjściowe