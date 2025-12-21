# Pytanie 6: Metody reużywalności kodu w językach obiektowych

## Pytanie
**"Omówić metody reużywalności kodu i struktur danych w obiektowych językach programowania."**

Przedmiot: PROI (Programowanie Obiektowe)

---

## 📚 Odpowiedź główna

### Wprowadzenie

**Reużywalność kodu (code reuse)** to fundamentalna zasada inżynierii oprogramowania - "nie wynajduj koła na nowo". W programowaniu obiektowym mamy kilka mechanizmów umożliwiających wielokrotne wykorzystanie kodu.

### Główne metody reużywalności

```
┌─────────────────────────────────────────────────────────────────┐
│                    METODY REUŻYWALNOŚCI                         │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   DZIEDZICZENIE │    KOMPOZYCJA   │      PROGRAMOWANIE          │
│   (Inheritance) │   (Composition) │      GENERYCZNE             │
├─────────────────┼─────────────────┼─────────────────────────────┤
│   INTERFEJSY    │   DELEGACJA     │      BIBLIOTEKI             │
│   (Interfaces)  │   (Delegation)  │      (Libraries)            │
├─────────────────┼─────────────────┼─────────────────────────────┤
│     MIXINY      │    TRAITY       │   WZORCE PROJEKTOWE         │
│    (Mixins)     │   (Traits)      │   (Design Patterns)         │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

---

## 1. Dziedziczenie (Inheritance)

### Definicja
**Dziedziczenie** to mechanizm, w którym klasa pochodna (child) przejmuje atrybuty i metody klasy bazowej (parent).

### Typy dziedziczenia

| Typ | Opis | Języki |
|-----|------|--------|
| **Pojedyncze** | Jedna klasa bazowa | Java, C# |
| **Wielokrotne** | Wiele klas bazowych | C++, Python |
| **Wielopoziomowe** | A → B → C | Wszystkie |
| **Hierarchiczne** | A → B, A → C | Wszystkie |

### Przykład (C++)

```cpp
// Klasa bazowa
class Pojazd {
protected:
    std::string marka;
    int predkosc;
    
public:
    Pojazd(const std::string& m) : marka(m), predkosc(0) {}
    
    virtual void jedz() {
        std::cout << marka << " jedzie " << predkosc << " km/h\n";
    }
    
    virtual ~Pojazd() = default;
};

// Klasa pochodna - dziedziczy i rozszerza
class Samochod : public Pojazd {
private:
    int liczbaDrzwi;
    
public:
    Samochod(const std::string& m, int drzwi) 
        : Pojazd(m), liczbaDrzwi(drzwi) {}
    
    void jedz() override {
        predkosc = 120;
        Pojazd::jedz();  // wywołanie metody bazowej
        std::cout << "Drzwi: " << liczbaDrzwi << "\n";
    }
    
    void parkuj() { /* nowa metoda */ }
};

// Użycie
Samochod auto1("BMW", 4);
auto1.jedz();  // Polimorfizm - wywołuje Samochod::jedz()
```

### Zalety i wady dziedziczenia

| Zalety | Wady |
|--------|------|
| Naturalne modelowanie hierarchii | Silne wiązanie (tight coupling) |
| Polimorfizm | Problem kruchej klasy bazowej |
| Łatwe rozszerzanie | Problemy z wielodziedziczeniem (diamond) |
| Współdzielenie implementacji | Narusza enkapsulację |

### Problem diamentu (Diamond Problem)

```
       A
      / \
     B   C
      \ /
       D
```

```cpp
class A { public: void metoda() {} };
class B : public A {};
class C : public A {};
class D : public B, public C {};  // Która A::metoda()?

D d;
// d.metoda();  // BŁĄD: niejednoznaczne!
d.B::metoda();  // OK - jawne wskazanie
```

**Rozwiązanie w C++:** Dziedziczenie wirtualne
```cpp
class B : virtual public A {};
class C : virtual public A {};
class D : public B, public C {};  // Jedna kopia A
```

---

## 2. Kompozycja (Composition)

### Definicja
**Kompozycja** to budowanie złożonych obiektów z prostszych komponentów. Relacja "zawiera" (has-a) zamiast "jest" (is-a).

### Zasada: "Favor composition over inheritance"

```cpp
// ZŁE - dziedziczenie
class Stack : public std::vector<int> {
    // Stack NIE JEST wektorem!
    // Użytkownik może wywołać insert(), erase()...
};

// DOBRE - kompozycja
class Stack {
private:
    std::vector<int> elements;  // Stack ZAWIERA wektor
    
public:
    void push(int x) { elements.push_back(x); }
    int pop() { 
        int top = elements.back();
        elements.pop_back();
        return top;
    }
    bool empty() const { return elements.empty(); }
    // Tylko te metody, które mają sens dla stosu
};
```

### Typy relacji obiektowych

| Relacja | Siła | Cykl życia | Przykład |
|---------|------|------------|----------|
| **Kompozycja** | Silna | Zależny (owns) | Samochód → Silnik |
| **Agregacja** | Słaba | Niezależny (uses) | Uniwersytet → Student |
| **Asocjacja** | Luźna | Niezależny | Klient ↔ Zamówienie |

```cpp
// Kompozycja - silnik "umiera" z samochodem
class Samochod {
private:
    Silnik silnik;  // Obiekt wewnętrzny
public:
    Samochod() : silnik() {}  // Tworzy silnik
    // ~Samochod() niszczy silnik automatycznie
};

// Agregacja - student istnieje niezależnie od uniwersytetu
class Uniwersytet {
private:
    std::vector<Student*> studenci;  // Wskaźniki/referencje
public:
    void dodajStudenta(Student* s) { studenci.push_back(s); }
    // ~Uniwersytet() NIE niszczy studentów
};
```

---

## 3. Programowanie generyczne (Generic Programming)

### Definicja
**Programowanie generyczne** to pisanie kodu niezależnego od konkretnych typów danych, używając szablonów (templates) lub generyków.

### Szablony w C++

```cpp
// Szablon funkcji
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

// Użycie - kompilator generuje wersje dla każdego typu
int m1 = maximum(3, 5);           // int
double m2 = maximum(3.14, 2.71);  // double
std::string m3 = maximum("abc", "xyz");  // string

// Szablon klasy
template<typename T, size_t N>
class Array {
private:
    T data[N];
public:
    T& operator[](size_t i) { return data[i]; }
    constexpr size_t size() const { return N; }
};

Array<int, 10> arr;     // Tablica 10 intów
Array<double, 5> darr;  // Tablica 5 double'i
```

### Generyki w Java/C#

```java
// Java
public class Box<T> {
    private T value;
    
    public void set(T value) { this.value = value; }
    public T get() { return value; }
}

// Ograniczenia typów (bounded type parameters)
public <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}
```

```csharp
// C#
public class Repository<T> where T : class, IEntity, new() {
    public T Create() => new T();
    public void Save(T entity) { /* ... */ }
}
```

### Zalety programowania generycznego

| Zaleta | Opis |
|--------|------|
| **Type safety** | Błędy wykrywane w czasie kompilacji |
| **Brak duplikacji** | Jeden kod dla wielu typów |
| **Wydajność** | C++: specjalizacja w kompilacji, brak rzutowania |
| **Czytelność** | Jawne wymagania typów |

---

## 4. Interfejsy (Interfaces)

### Definicja
**Interfejs** definiuje kontrakt (zestaw metod), który klasa musi zaimplementować. Oddziela "co" od "jak".

### Przykład

```java
// Java - interfejs
public interface Drawable {
    void draw();
    default void clear() { /* domyślna implementacja */ }
}

public interface Resizable {
    void resize(int width, int height);
}

// Klasa implementuje wiele interfejsów
public class Rectangle implements Drawable, Resizable {
    @Override
    public void draw() { /* implementacja */ }
    
    @Override
    public void resize(int w, int h) { /* implementacja */ }
}
```

```cpp
// C++ - klasa abstrakcyjna jako interfejs
class IDrawable {
public:
    virtual void draw() = 0;  // Pure virtual
    virtual ~IDrawable() = default;
};

class IResizable {
public:
    virtual void resize(int w, int h) = 0;
    virtual ~IResizable() = default;
};

class Rectangle : public IDrawable, public IResizable {
public:
    void draw() override { /* ... */ }
    void resize(int w, int h) override { /* ... */ }
};
```

### Interfejsy vs Klasy abstrakcyjne

| Cecha | Interfejs | Klasa abstrakcyjna |
|-------|-----------|-------------------|
| Wielodziedziczenie | TAK | NIE (Java/C#) |
| Pola | NIE (do Java 8) | TAK |
| Konstruktor | NIE | TAK |
| Implementacja metod | default (Java 8+) | TAK |
| Cel | Definiuje kontrakt | Współdzieli implementację |

---

## 5. Delegacja (Delegation)

### Definicja
**Delegacja** to przekazywanie odpowiedzialności za wykonanie operacji do innego obiektu.

```cpp
// Bez delegacji - dziedziczenie
class LoggingList : public std::list<int> {
public:
    void push_back(int x) {
        log("Adding: " + std::to_string(x));
        std::list<int>::push_back(x);
    }
};

// Z delegacją - kompozycja
class LoggingList {
private:
    std::list<int> delegate;  // Delegat
    
public:
    void push_back(int x) {
        log("Adding: " + std::to_string(x));
        delegate.push_back(x);  // Delegacja
    }
    
    size_t size() const { 
        return delegate.size();  // Delegacja
    }
};
```

### Wzorzec strategii (Strategy Pattern)

```cpp
// Interfejs strategii
class SortStrategy {
public:
    virtual void sort(std::vector<int>& data) = 0;
    virtual ~SortStrategy() = default;
};

class QuickSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override { /* quicksort */ }
};

class MergeSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override { /* mergesort */ }
};

// Kontekst deleguje sortowanie do strategii
class Sorter {
private:
    std::unique_ptr<SortStrategy> strategy;
    
public:
    void setStrategy(std::unique_ptr<SortStrategy> s) {
        strategy = std::move(s);
    }
    
    void performSort(std::vector<int>& data) {
        strategy->sort(data);  // Delegacja
    }
};
```

---

## 6. Mixiny i Traity

### Mixiny (Mixins)
Klasy dostarczające funkcjonalność do "wmieszania" do innych klas.

```python
# Python - mixiny przez wielodziedziczenie
class JSONSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class XMLSerializableMixin:
    def to_xml(self):
        # implementacja...
        pass

class User(JSONSerializableMixin, XMLSerializableMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email

user = User("Jan", "jan@example.com")
print(user.to_json())  # {"name": "Jan", "email": "jan@example.com"}
```

### Traity (Traits)

```rust
// Rust - traits
trait Drawable {
    fn draw(&self);
}

trait Movable {
    fn move_to(&mut self, x: i32, y: i32);
}

struct Circle {
    x: i32,
    y: i32,
    radius: i32,
}

impl Drawable for Circle {
    fn draw(&self) { /* ... */ }
}

impl Movable for Circle {
    fn move_to(&mut self, x: i32, y: i32) {
        self.x = x;
        self.y = y;
    }
}
```

```php
// PHP - traits
trait Timestampable {
    public $createdAt;
    public $updatedAt;
    
    public function touch() {
        $this->updatedAt = new DateTime();
    }
}

trait SoftDeletable {
    public $deletedAt;
    
    public function softDelete() {
        $this->deletedAt = new DateTime();
    }
}

class Article {
    use Timestampable, SoftDeletable;
    
    public $title;
}
```

---

## 7. Biblioteki i frameworki

### Poziomy reużywalności

```
┌─────────────────────────────────────────────────────┐
│                    FRAMEWORK                         │
│    (IoC, definiuje architekturę aplikacji)          │
├─────────────────────────────────────────────────────┤
│                    BIBLIOTEKA                        │
│    (kolekcja klas/funkcji, wywołujesz Ty)           │
├─────────────────────────────────────────────────────┤
│                    MODUŁ/PAKIET                      │
│    (logicznie powiązane klasy)                      │
├─────────────────────────────────────────────────────┤
│                    KLASA                             │
│    (jednostka enkapsulacji)                         │
├─────────────────────────────────────────────────────┤
│                    FUNKCJA                           │
│    (najmniejsza jednostka reużywalna)               │
└─────────────────────────────────────────────────────┘
```

### Przykłady

| Poziom | Przykłady |
|--------|-----------|
| Framework | Spring, .NET, Unity, Django |
| Biblioteka | STL, Boost, jQuery, NumPy |
| Moduł | java.util, System.IO |
| Klasa | ArrayList, HttpClient |

---

## 8. Wzorce projektowe (Design Patterns)

### Wzorce wspierające reużywalność

| Wzorzec | Typ | Cel |
|---------|-----|-----|
| **Factory Method** | Kreacyjny | Delegacja tworzenia obiektów |
| **Abstract Factory** | Kreacyjny | Rodziny powiązanych obiektów |
| **Prototype** | Kreacyjny | Klonowanie obiektów |
| **Adapter** | Strukturalny | Dopasowanie interfejsów |
| **Decorator** | Strukturalny | Dynamiczne rozszerzanie |
| **Strategy** | Behawioralny | Wymienne algorytmy |
| **Template Method** | Behawioralny | Szkielet algorytmu z krokami |

### Przykład: Template Method

```cpp
// Szkielet algorytmu w klasie bazowej
class DataParser {
public:
    // Template method - definiuje szkielet
    void parse(const std::string& data) {
        openFile();
        readHeader();
        processData(data);  // Krok abstrakcyjny
        closeFile();
    }
    
protected:
    virtual void openFile() { /* domyślna impl */ }
    virtual void readHeader() { /* domyślna impl */ }
    virtual void processData(const std::string& data) = 0;  // PURE
    virtual void closeFile() { /* domyślna impl */ }
};

// Konkretne implementacje
class JSONParser : public DataParser {
protected:
    void processData(const std::string& data) override {
        // Parsowanie JSON
    }
};

class XMLParser : public DataParser {
protected:
    void processData(const std::string& data) override {
        // Parsowanie XML
    }
};
```

---

## 📊 Porównanie metod reużywalności

| Metoda | Wiązanie | Elastyczność | Złożoność |
|--------|----------|--------------|-----------|
| Dziedziczenie | Statyczne | Niska | Średnia |
| Kompozycja | Dynamiczne | Wysoka | Niska |
| Interfejsy | Statyczne* | Wysoka | Niska |
| Generyki | Statyczne | Wysoka | Średnia |
| Delegacja | Dynamiczne | Wysoka | Średnia |
| Mixiny/Traity | Statyczne | Średnia | Średnia |

*ale implementacja może być dynamiczna (polimorfizm)

---

## 🧠 Mnemoniki

### "SOLID" - zasady dobrego OOP:
- **S**ingle Responsibility - jedna odpowiedzialność
- **O**pen/Closed - otwarte na rozszerzenia, zamknięte na modyfikacje
- **L**iskov Substitution - podtyp zastępuje typ bazowy
- **I**nterface Segregation - wiele małych interfejsów > jeden duży
- **D**ependency Inversion - zależność od abstrakcji, nie konkretu

### "HAS-A przed IS-A":
- **HAS-A** = kompozycja (Samochód HAS-A Silnik)
- **IS-A** = dziedziczenie (Samochód IS-A Pojazd)
- Preferuj HAS-A!

### "DRIED" dla reużywalności:
- **D**on't **R**epeat - nie powtarzaj kodu
- **I**nterfaces - definiuj kontrakty
- **E**ncapsulate - ukrywaj szczegóły
- **D**elegate - przekazuj odpowiedzialność

### "GIT" dla generyków:
- **G**eneric - niezależne od typu
- **I**nvariant - sprawdzane w kompilacji
- **T**ype-safe - bezpieczne typowanie

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Kiedy dziedziczenie, a kiedy kompozycja?"

**Odpowiedź:**

| Użyj dziedziczenia gdy: | Użyj kompozycji gdy: |
|------------------------|---------------------|
| Relacja "jest" (is-a) | Relacja "zawiera" (has-a) |
| Potrzebujesz polimorfizmu | Potrzebujesz elastyczności |
| Klasa pochodna JEST typem bazowym | Chcesz zmieniać zachowanie w runtime |
| Zasada Liskov jest spełniona | Chcesz uniknąć problemów z hierarchią |

**Przykład decyzji:**
- Ptak IS-A Zwierzę → dziedziczenie OK
- Samochód HAS-A Silnik → kompozycja!
- Stack IS-A Vector? → NIE! Kompozycja.

---

### Q2: "Co to jest zasada substytucji Liskov?"

**Odpowiedź:**

> "Obiekty klasy bazowej powinny być zastępowalne obiektami klas pochodnych bez zmiany poprawności programu."

**Naruszenie LSP:**
```cpp
class Rectangle {
public:
    virtual void setWidth(int w) { width = w; }
    virtual void setHeight(int h) { height = h; }
    int area() { return width * height; }
protected:
    int width, height;
};

class Square : public Rectangle {  // PROBLEM!
public:
    void setWidth(int w) override { width = height = w; }
    void setHeight(int h) override { width = height = h; }
};

// Kod klienta
void resize(Rectangle& r) {
    r.setWidth(5);
    r.setHeight(10);
    assert(r.area() == 50);  // FAIL dla Square!
}
```

**Rozwiązanie:** Kwadrat nie powinien dziedziczyć po prostokącie (matematycznie IS-A, programistycznie NIE).

---

### Q3: "Czym różnią się szablony C++ od generyków Java?"

**Odpowiedź:**

| Cecha | C++ Templates | Java Generics |
|-------|---------------|---------------|
| Implementacja | Kompilacja (code generation) | Type erasure (runtime) |
| Specjalizacja | TAK | NIE |
| Prymitywy | TAK (int, double...) | NIE (tylko obiekty) |
| Sprawdzanie typu | W czasie instancjacji | W czasie kompilacji |
| Ograniczenia | Concepts (C++20) | Bounded types |
| Wydajność | Optymalna | Rzutowanie w runtime |

```cpp
// C++ - specjalizacja szablonu
template<typename T>
class Container { /* ogólna implementacja */ };

template<>
class Container<bool> { /* specjalna dla bool - bitset */ };
```

---

### Q4: "Co to jest Dependency Injection?"

**Odpowiedź:**

**Dependency Injection (DI)** = wzorzec przekazywania zależności z zewnątrz zamiast tworzenia ich wewnątrz.

```cpp
// BEZ DI - silne wiązanie
class OrderService {
private:
    MySQLDatabase db;  // Zależność "zahardkodowana"
public:
    OrderService() : db() {}
};

// Z DI - luźne wiązanie
class OrderService {
private:
    IDatabase& db;  // Zależność od abstrakcji
public:
    OrderService(IDatabase& database) : db(database) {}  // Injection
};

// Użycie
MySQLDatabase mysql;
PostgresDatabase postgres;

OrderService service1(mysql);    // Możemy łatwo zmienić
OrderService service2(postgres);  // implementację
```

**Typy DI:**
1. Constructor Injection (preferowany)
2. Setter Injection
3. Interface Injection

---

### Q5: "Jak wzorce projektowe wspierają reużywalność?"

**Odpowiedź:**

| Wzorzec | Mechanizm reużywalności |
|---------|------------------------|
| **Factory** | Oddziela tworzenie od użycia |
| **Strategy** | Wymienna rodzina algorytmów |
| **Decorator** | Dynamiczne dodawanie funkcji |
| **Adapter** | Reużycie niekompatybilnych klas |
| **Template Method** | Reużycie szkieletu algorytmu |
| **Composite** | Jednolite traktowanie obiektów i kolekcji |

---

### Q6: "Wyjaśnij różnicę między agregacją a kompozycją"

**Odpowiedź:**

| Cecha | Kompozycja | Agregacja |
|-------|------------|-----------|
| Siła związku | Silna ("owns") | Słaba ("uses") |
| Cykl życia | Zależny | Niezależny |
| UML | Wypełniony romb ◆ | Pusty romb ◇ |
| Przykład | Samochód → Silnik | Firma → Pracownik |

```cpp
// Kompozycja - silnik jest częścią samochodu
class Car {
    Engine engine;  // Engine tworzony z Car, niszczony z Car
};

// Agregacja - pracownik może istnieć bez firmy
class Company {
    std::vector<Employee*> employees;  // Wskaźniki - nie "posiada"
};
```

---

## 🎯 Kluczowe punkty do zapamiętania

1. **Kompozycja > Dziedziczenie** - elastyczność, luźne wiązanie
2. **Interfejsy oddzielają** kontrakt od implementacji
3. **Generyki eliminują** duplikację kodu dla różnych typów
4. **SOLID** - 5 zasad dobrego OOP
5. **Delegacja** - przekazuj odpowiedzialność
6. **Wzorce projektowe** - sprawdzone rozwiązania typowych problemów

---

## 📖 Źródła do pogłębienia

1. Gamma et al. - "Design Patterns: Elements of Reusable OO Software" (GoF)
2. Martin, R. - "Clean Code" i "Clean Architecture"
3. Meyers, S. - "Effective C++"
4. Bloch, J. - "Effective Java"
