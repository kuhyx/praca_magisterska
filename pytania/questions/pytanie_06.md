## PYTANIE 6: Reużywalność kodu w OOP (PROI)

**Omówić metody reużywalności kodu i struktur danych w obiektowych językach programowania.**

---

### Tło pojęciowe — słowniczek

**OOP (Object-Oriented Programming / Programowanie obiektowe)** — paradygmat, w którym program składa się z obiektów łączących dane (pola) i zachowanie (metody). Cztery filary: enkapsulacja, dziedziczenie, polimorfizm, abstrakcja. W kontekście pytania — to OOP wprowadza mechanizmy ponownego użycia kodu omawiane poniżej.

**Klasa (class)** — „wzorzec" (blueprint) obiektu. Definiuje pola i metody. Obiekt to konkretna instancja klasy.

    class Dog {          // klasa
        string name;
        void bark();
    };
    Dog rex;             // obiekt (instancja)

**Reużywalność kodu (code reuse)** — możliwość wykorzystania raz napisanego kodu w wielu miejscach bez kopiowania. Zmniejsza ilość duplikatów, ułatwia utrzymanie i redukuje błędy. To główny temat pytania.

---

### Cztery filary OOP

**1. Enkapsulacja (encapsulation)** — ukrywanie szczegółów implementacji za interfejsem publicznym. Obiekt kontroluje dostęp do swoich danych przez modyfikatory dostępu: `private` (tylko klasa), `protected` (klasa + pochodne), `public` (wszyscy).

    class BankAccount {
    private:
        double balance;          // ukryte — nikt z zewnątrz nie zmieni bezpośrednio
    public:
        void deposit(double amt) { if (amt > 0) balance += amt; }  // kontrolowany dostęp
        double getBalance() const { return balance; }
    };

**Jak enkapsulacja wspiera reużywalność?** Klasa z dobrze zdefiniowanym publicznym interfejsem jest jak „czarna skrzynka" — można ją użyć w DOWOLNYM projekcie bez znajomości implementacji. Zmiana wewnętrznej implementacji (np. zmiana struktury danych z tablicy na drzewo) NIE łamie kodu, który tej klasy używa. Dzięki temu klasa jest bezpiecznie reużywalna — użytkownik zależy od interfejsu, nie od szczegółów.

**2. Abstrakcja (abstraction)** — wyodrębnianie ISTOTNYCH cech obiektu i pomijanie szczegółów nieistotnych z perspektywy użytkownika. Abstrakcja odpowiada na pytanie „CO obiekt robi?", nie „JAK to robi?".

    // Abstrakcja: "kształt ma pole powierzchni" — szczegóły ukryte
    class Shape {
    public:
        virtual double area() = 0;  // CO: oblicz pole. JAK? — to zależy od kształtu
    };
    class Circle : public Shape {
        double r;
    public:
        double area() override { return 3.14159 * r * r; }  // JAK: π·r²
    };

**Jak abstrakcja wspiera reużywalność?** Kod operujący na abstrakcji (np. `void printArea(Shape& s)`) działa z KAŻDYM kształtem — kołem, prostokątem, trójkątem — bez modyfikacji. Nowy kształt = nowa klasa implementująca `Shape`, zero zmian w istniejącym kodzie. Abstrakcja tworzy stabilne „punkty podłączenia" (extension points), do których można dołączać nowe implementacje.

**Różnica enkapsulacja vs abstrakcja:** Enkapsulacja = UKRYWANIE wnętrza (mechanizm ochrony). Abstrakcja = UPRASZCZANIE interfejsu (mechanizm projektowania). Enkapsulacja chroni dane, abstrakcja modeluje pojęcia. Często współdziałają: klasa abstrakcyjna (abstrakcja) z polami prywatnymi (enkapsulacja).

**3. Dziedziczenie (inheritance)** — mechanizm, w którym klasa pochodna (child) przejmuje pola i metody klasy bazowej (parent). Relacja „jest" (is-a): Dog **jest** Animal.

    class Animal { void eat(); };
    class Dog : public Animal { void bark(); };
    // Dog ma eat() + bark()

**Klasa bazowa / pochodna (base class / derived class)** — bazowa = rodzic, pochodna = dziecko. Pochodna dziedziczy interfejs i implementację bazowej, może dodawać własne lub nadpisywać istniejące metody.

**Jak dziedziczenie wspiera reużywalność?** Klasa pochodna otrzymuje CAŁY kod bazowej „za darmo" — wystarczy napisać to, co się różni. Hierarchia klas pozwala współdzielić wspólną logikę w jednym miejscu zamiast kopiować ją do wielu klas.

**Dziedziczenie wielokrotne (multiple inheritance)** — klasa dziedziczy po więcej niż jednym rodzicu. Dostępne w C++, ale nie w Java/C# (tam tylko interfejsy). Powoduje ryzyko konfliktu nazw i problem diamentu.

**Problem diamentu (diamond problem)** — gdy klasa D dziedziczy po B i C, a oba dziedziczą po A, D ma dwie kopie A. Pytanie: której użyć?

         A
        / \
       B   C
        \ /
         D     ← dwie kopie A!

Rozwiązanie w C++: dziedziczenie wirtualne (`class B : virtual public A`), dzięki czemu istnieje jedna kopia A.

**4. Polimorfizm (polymorphism)** — grec. „wiele form". Możliwość traktowania obiektów różnych klas przez wspólny interfejs. Kluczowy dla reużywalności — piszesz kod raz, działa z wieloma typami.

    Animal* a = new Dog();
    a->speak();  // woła Dog::speak(), nie Animal::speak()
    // To samo wywołanie, różne zachowanie — polimorfizm

Realizacja: funkcje wirtualne (`virtual` + `override`) — tablica vtable wskazuje na właściwą implementację.

**Jak polimorfizm wspiera reużywalność?** Funkcja `void feed(Animal& a)` działa z Dog, Cat, Parrot — KAŻDĄ klasą pochodną. Nowy typ zwierzęcia NIE wymaga zmiany funkcji `feed`. Kod wywołujący jest reużywalny, bo operuje na abstrakcji (bazowa klasa/interfejs), nie na konkretnym typie.

---

**Kompozycja (composition)** — obiekt zawiera inne obiekty jako pola. Relacja „ma" (has-a). Stack **ma** wektor (nie **jest** wektorem). Silniejsza enkapsulacja niż dziedziczenie, bo wnętrze komponentu jest ukryte.

    class Engine { int hp; };
    class Car {
        Engine engine;   // kompozycja: Car "ma" Engine
    };

**„Favor composition over inheritance"** — zasada GoF: preferuj kompozycję nad dziedziczenie. Dziedziczenie tworzy silne wiązanie (zmiana bazowej łamie pochodne). Kompozycja pozwala wymieniać części w runtime.

**Agregacja (aggregation)** — słabsza forma kompozycji: obiekt „używa" innego, ale go nie posiada. Samochód ma kierowcę, ale kierowca istnieje niezależnie. W UML: pusty romb (◇).

**Luźne wiązanie (loose coupling)** — komponenty mają minimum zależności między sobą. Zmiana jednego nie wymusza zmian w drugim. Kompozycja daje luźniejsze wiązanie niż dziedziczenie.

---

**Programowanie generyczne (generic programming)** — pisanie kodu niezależnego od konkretnego typu danych. Jedna implementacja działa dla int, float, string itd.

**Template (szablon, C++)** — mechanizm generyczny w C++. Kompilator generuje osobną wersję kodu dla każdego użytego typu (monomorfizacja).

    template<typename T>
    T max(T a, T b) { return a > b ? a : b; }
    max(3, 5);       // T = int
    max(1.5, 2.7);   // T = double

**Generics (Java/C#)** — odpowiednik templates, ale z type erasure (Java) lub reifikacją (C#). `List<String>` — lista przechowująca tylko stringi; bezpieczeństwo typów bez duplikowania kodu.

**STL (Standard Template Library)** — biblioteka C++ oparta na templates: kontenery (`vector`, `map`), algorytmy (`sort`, `find`), iteratory. Przykład reużywalności: jeden `sort()` sortuje dowolny kontener.

---

**Interfejs (interface)** — kontrakt: zbiór metod bez implementacji. Klasa implementująca interfejs musi dostarczyć ciała wszystkich metod. W C++ → czysto wirtualne metody (`= 0`); w Java/C# → `interface`.

    // C++
    class Drawable {
    public:
        virtual void draw() = 0;  // pure virtual = interfejs
    };

**Klasa abstrakcyjna (abstract class)** — klasa, której nie można instancjonować; może mieć zarówno metody abstrakcyjne, jak i z implementacją. Interfejs = 100% abstrakcyjna.

**Wzorce projektowe (design patterns)** — sprawdzone, reużywalne rozwiązania typowych problemów projektowych. Opisane jako: Nazwa + Problem + Rozwiązanie + Konsekwencje.

**GoF (Gang of Four)** — Gamma, Helm, Johnson, Vlissides — autorzy książki „Design Patterns" (1994) z 23 wzorcami w trzech kategoriach: kreacyjne, strukturalne, behawioralne.

**Strategy** — wzorzec: wymień algorytm w runtime przez interfejs. Np. różne strategie sortowania.
**Observer** — wzorzec: obiekt powiadamia subskrybentów o zmianach stanu (pub/sub w OOP).
**Factory** — wzorzec: tworzenie obiektów bez określania dokładnej klasy (decyzja w runtime).
**Decorator** — wzorzec: dodaj zachowanie do obiektu dynamicznie, opakowując go.

**Biblioteka (library)** — zbiór reużywalnego kodu wywoływanego przez nasz program (my code calls library).
**Framework** — odwrotność: framework wywołuje nasz kod (Inversion of Control). Np. Unity, Django.
**Trait / Mixin** — mechanizm współdzielenia kodu między klasami bez dziedziczenia. Trait (Rust, Scala) = zbiór metod do „wmixowania". Mixin (Ruby, Python) = klasa dodająca funkcjonalność przez wielodziedziczenie.

---

### Główne metody

### 1. Dziedziczenie (Inheritance) — relacja „jest" (is-a)
- Klasa pochodna przejmuje atrybuty i metody bazowej
- Typy: pojedyncze, wielokrotne, wielopoziomowe
- Problem diamentu → dziedziczenie wirtualne w C++
- Polimorfizm (virtual, override)

### 2. Kompozycja (Composition) — relacja „zawiera" (has-a)
- **„Favor composition over inheritance"**
- Stack nie JEST wektorem → Stack ZAWIERA wektor
- Silniejsza enkapsulacja, luźne wiązanie
- Typy: kompozycja (owns), agregacja (uses), asocjacja (knows)

### 3. Programowanie generyczne (Templates/Generics)
- Kod niezależny od typu: `template<typename T> T max(T a, T b)`
- STL jest oparta na templates
- Java/C#: Generics (`List<T>`)

### 4. Interfejsy i klasy abstrakcyjne
- Kontrakt bez implementacji (pure virtual w C++, interface w Java)
- Umożliwiają multiple inheritance bez diamond problem

### 5. Wzorce projektowe (Design Patterns)
- Strategy, Observer, Factory, Decorator — reużywalne rozwiązania
- GoF (Gang of Four) — 23 wzorce

### 6. Biblioteki, frameworki, traity/mixiny

### Etymologia

**OOP** — Alan Kay (Smalltalk, 1970s), sam ukuł termin „object-oriented". **GoF** — Gang of Four: Gamma, Helm, Johnson, Vlissides (1994). **Polimorfizm** — grec. „poly" (wiele) + „morphē" (forma) = wiele postaci. **Enkapsulacja** — łac. „capsula" = pudełeczko. **Abstrakcja** — łac. „abstrahere" = odciągać, oddzielać (oddzielanie istoty od szczegółów). **Design Pattern** — z architektury: Christopher Alexander „A Pattern Language" (1977); GoF zaadaptowali do IT. **Kompozycja > Dziedziczenie** — zasada z GoF: „favor object composition over class inheritance".

### Jak zapamiętać

- **4 filary OOP:** Enkapsulacja (ukrywanie) → Abstrakcja (upraszczanie) → Dziedziczenie (przejmowanie) → Polimorfizm (wielopostaciowość)
- Enkapsulacja = czarna skrzynka → bezpieczna reużywalność. Abstrakcja = punkty rozszerzenia → otwarta reużywalność
- **„Kompozycja > Dziedziczenie"** — najważniejsza zasada
- Dziedziczenie: silne wiązanie, krucha klasa bazowa, diamond problem
- Kompozycja: elastyczna, testowalna, preferowana
- Granica: dziedziczenie dla prawdziwego „is-a" z polimorfizmem; kompozycja dla reszty

