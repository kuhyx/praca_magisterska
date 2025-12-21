# Pytanie 5: Główne kategorie elementów biblioteki STL

## Pytanie
**"Omówić główne kategorie elementów biblioteki STL. Jaka jest ich rola i wzajemne powiązania? Odpowiedź uzasadnić na przykładach."**

Przedmiot: PROI (Programowanie Obiektowe)

---

## 📚 Odpowiedź główna

### Wprowadzenie

**STL (Standard Template Library)** to część standardowej biblioteki C++ zawierająca generyczne struktury danych i algorytmy. Została zaprojektowana przez Alexandra Stepanova i weszła do standardu C++98.

### Filozofia STL
- **Generyczność** - szablony (templates) umożliwiają pracę z dowolnymi typami
- **Wydajność** - zero-overhead abstraction
- **Modularność** - komponenty są niezależne i wymienne
- **Ortogonalność** - kontenery i algorytmy są rozdzielone (przez iteratory)

---

## Cztery główne kategorie STL

```
┌─────────────────────────────────────────────────────────────────┐
│                           STL                                   │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│  KONTENERY  │  ITERATORY  │  ALGORYTMY  │  FUNKTORY           │
│  (co?)      │  (jak?)     │  (operacje) │  (parametryzacja)   │
├─────────────┼─────────────┼─────────────┼─────────────────────┤
│ vector      │ input       │ sort        │ less<T>             │
│ list        │ output      │ find        │ greater<T>          │
│ map         │ forward     │ transform   │ plus<T>             │
│ set         │ bidirect.   │ copy        │ lambdy              │
│ ...         │ random      │ ...         │ ...                 │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
```

---

## 1. Kontenery (Containers)

### Definicja
**Kontenery** to struktury danych przechowujące kolekcje obiektów. Zarządzają pamięcią automatycznie.

### Kategorie kontenerów

#### 1.1 Kontenery sekwencyjne (Sequence Containers)

Przechowują elementy w określonej kolejności.

| Kontener | Struktura | Dostęp | Wstawianie | Usuwanie |
|----------|-----------|--------|------------|----------|
| `vector` | Tablica dynamiczna | O(1) random | O(1) koniec, O(n) środek | O(1) koniec, O(n) środek |
| `deque` | Tablica tablic | O(1) random | O(1) początek/koniec | O(1) początek/koniec |
| `list` | Lista dwukierunkowa | O(n) | O(1) wszędzie* | O(1) wszędzie* |
| `forward_list` | Lista jednokierunkowa | O(n) | O(1) po elemencie | O(1) po elemencie |
| `array` | Tablica statyczna | O(1) random | N/A | N/A |

*po znalezieniu pozycji

```cpp
#include <vector>
#include <list>
#include <deque>

// vector - najczęściej używany
std::vector<int> vec = {1, 2, 3, 4, 5};
vec.push_back(6);           // O(1) amortyzowane
vec[2] = 10;                // O(1) dostęp
vec.insert(vec.begin(), 0); // O(n) - przesunięcie

// list - szybkie wstawianie/usuwanie
std::list<int> lst = {1, 2, 3};
auto it = lst.begin();
std::advance(it, 1);
lst.insert(it, 99);         // O(1) po znalezieniu miejsca

// deque - szybki dostęp do obu końców
std::deque<int> deq;
deq.push_front(1);          // O(1)
deq.push_back(2);           // O(1)
```

#### 1.2 Kontenery asocjacyjne (Associative Containers)

Przechowują pary klucz-wartość, posortowane według klucza (drzewo czerwono-czarne).

| Kontener | Klucze | Wartości | Złożoność |
|----------|--------|----------|-----------|
| `set` | Unikalne | Brak | O(log n) |
| `multiset` | Duplikaty OK | Brak | O(log n) |
| `map` | Unikalne | Tak | O(log n) |
| `multimap` | Duplikaty OK | Tak | O(log n) |

```cpp
#include <set>
#include <map>

// set - zbiór unikalnych, posortowanych elementów
std::set<int> s = {3, 1, 4, 1, 5};  // {1, 3, 4, 5} - bez duplikatów
s.insert(2);                         // O(log n)
bool exists = s.count(3) > 0;        // O(log n)

// map - słownik klucz->wartość
std::map<std::string, int> ages;
ages["Jan"] = 25;                    // O(log n)
ages["Anna"] = 30;
for (const auto& [name, age] : ages) {
    std::cout << name << ": " << age << "\n";  // Posortowane alfabetycznie
}
```

#### 1.3 Kontenery asocjacyjne nieuporządkowane (Unordered Associative)

Implementacja: tablica haszująca (hash table).

| Kontener | Klucze | Wartości | Złożoność średnia |
|----------|--------|----------|-------------------|
| `unordered_set` | Unikalne | Brak | O(1) |
| `unordered_multiset` | Duplikaty OK | Brak | O(1) |
| `unordered_map` | Unikalne | Tak | O(1) |
| `unordered_multimap` | Duplikaty OK | Tak | O(1) |

```cpp
#include <unordered_map>
#include <unordered_set>

// unordered_map - szybsza od map dla dużych zbiorów
std::unordered_map<std::string, int> umap;
umap["klucz"] = 42;        // O(1) średnio
auto it = umap.find("klucz");  // O(1) średnio

// unordered_set
std::unordered_set<int> uset = {1, 2, 3};
uset.insert(4);            // O(1) średnio
```

#### 1.4 Adaptery kontenerów (Container Adapters)

Interfejsy ograniczające funkcjonalność bazowego kontenera.

| Adapter | Domyślny kontener | Operacje |
|---------|-------------------|----------|
| `stack` | deque | push, pop, top (LIFO) |
| `queue` | deque | push, pop, front (FIFO) |
| `priority_queue` | vector | push, pop, top (max-heap) |

```cpp
#include <stack>
#include <queue>

// stack - LIFO
std::stack<int> stk;
stk.push(1);
stk.push(2);
stk.top();   // 2
stk.pop();   // usuwa 2

// queue - FIFO
std::queue<int> q;
q.push(1);
q.push(2);
q.front();  // 1
q.pop();    // usuwa 1

// priority_queue - max-heap domyślnie
std::priority_queue<int> pq;
pq.push(3);
pq.push(1);
pq.push(4);
pq.top();   // 4 (największy)
```

---

## 2. Iteratory (Iterators)

### Definicja
**Iteratory** to uogólnione wskaźniki - abstrakcja umożliwiająca jednolity dostęp do elementów kontenerów.

### Hierarchia iteratorów

```
                    Input Iterator      Output Iterator
                          ↓                   ↓
                    Forward Iterator ←────────┘
                          ↓
                  Bidirectional Iterator
                          ↓
                  Random Access Iterator
                          ↓
                  Contiguous Iterator (C++17)
```

### Kategorie iteratorów

| Kategoria | Operacje | Przykłady kontenerów |
|-----------|----------|---------------------|
| **Input** | `++`, `*`, `==`, `!=` | istream_iterator |
| **Output** | `++`, `*` (zapis) | ostream_iterator |
| **Forward** | Input + wielokrotne przejście | forward_list, unordered_* |
| **Bidirectional** | Forward + `--` | list, set, map |
| **Random Access** | Bidirectional + `+`, `-`, `[]`, `<` | vector, deque, array |
| **Contiguous** | Random + ciągła pamięć | vector, array, string |

```cpp
#include <vector>
#include <list>
#include <iterator>

std::vector<int> vec = {1, 2, 3, 4, 5};

// Random access iterator
auto it = vec.begin();
it += 3;                    // OK - random access
std::cout << *it;           // 4
std::cout << it[1];         // 5

std::list<int> lst = {1, 2, 3, 4, 5};

// Bidirectional iterator
auto lit = lst.begin();
++lit;                      // OK
--lit;                      // OK - bidirectional
// lit += 3;                // BŁĄD! - brak random access

// Pomocnicze funkcje
std::advance(lit, 3);       // Działa dla każdego iteratora
auto dist = std::distance(lst.begin(), lst.end());  // 5
```

### Iteratory specjalne

```cpp
#include <iterator>
#include <iostream>
#include <vector>

std::vector<int> vec = {1, 2, 3};

// Iteratory wstawiające
std::vector<int> dest;
std::copy(vec.begin(), vec.end(), std::back_inserter(dest));  // push_back

// Iteratory strumieni
std::copy(vec.begin(), vec.end(), 
          std::ostream_iterator<int>(std::cout, " "));  // wypisuje: 1 2 3

// Iteratory odwrotne
for (auto rit = vec.rbegin(); rit != vec.rend(); ++rit) {
    std::cout << *rit << " ";  // 3 2 1
}
```

---

## 3. Algorytmy (Algorithms)

### Definicja
**Algorytmy** to funkcje szablonowe operujące na zakresach (parach iteratorów). Są **oddzielone od kontenerów** - działają przez iteratory.

### Kategorie algorytmów

#### 3.1 Algorytmy niemodyfikujące

```cpp
#include <algorithm>
#include <vector>

std::vector<int> vec = {1, 2, 3, 4, 5, 3};

// Wyszukiwanie
auto it = std::find(vec.begin(), vec.end(), 3);     // pierwszy 3
int cnt = std::count(vec.begin(), vec.end(), 3);    // 2
bool any = std::any_of(vec.begin(), vec.end(), 
                       [](int x) { return x > 4; }); // true

// Porównywanie
std::vector<int> vec2 = {1, 2, 3, 4, 5, 3};
bool eq = std::equal(vec.begin(), vec.end(), vec2.begin());  // true

// Zliczanie
auto [min_it, max_it] = std::minmax_element(vec.begin(), vec.end());
```

#### 3.2 Algorytmy modyfikujące

```cpp
std::vector<int> vec = {3, 1, 4, 1, 5, 9};

// Sortowanie
std::sort(vec.begin(), vec.end());                    // {1, 1, 3, 4, 5, 9}
std::sort(vec.begin(), vec.end(), std::greater<>());  // malejąco

// Przekształcanie
std::transform(vec.begin(), vec.end(), vec.begin(),
               [](int x) { return x * 2; });          // podwojenie

// Usuwanie (erase-remove idiom)
vec.erase(std::remove(vec.begin(), vec.end(), 1), vec.end());

// Wypełnianie
std::fill(vec.begin(), vec.end(), 0);
std::iota(vec.begin(), vec.end(), 1);  // {1, 2, 3, ...}

// Kopiowanie
std::vector<int> dest(vec.size());
std::copy(vec.begin(), vec.end(), dest.begin());
```

#### 3.3 Algorytmy partycjonujące i sortujące

```cpp
std::vector<int> vec = {3, 1, 4, 1, 5, 9, 2, 6};

// Partycjonowanie
auto pivot = std::partition(vec.begin(), vec.end(),
                            [](int x) { return x < 5; });
// Teraz: elementy < 5 | pivot | elementy >= 5

// Częściowe sortowanie
std::partial_sort(vec.begin(), vec.begin() + 3, vec.end());
// Pierwsze 3 elementy posortowane, reszta nieokreślona

// N-ty element
std::nth_element(vec.begin(), vec.begin() + 4, vec.end());
// Element na pozycji 4 jest taki jak po pełnym sortowaniu

// Sortowanie stabilne
std::stable_sort(vec.begin(), vec.end());  // zachowuje kolejność równych
```

#### 3.4 Algorytmy na zbiorach (posortowanych!)

```cpp
std::vector<int> a = {1, 2, 3, 4, 5};
std::vector<int> b = {3, 4, 5, 6, 7};
std::vector<int> result;

// Suma zbiorów
std::set_union(a.begin(), a.end(), b.begin(), b.end(),
               std::back_inserter(result));  // {1,2,3,4,5,6,7}

// Przecięcie
result.clear();
std::set_intersection(a.begin(), a.end(), b.begin(), b.end(),
                      std::back_inserter(result));  // {3,4,5}

// Różnica
result.clear();
std::set_difference(a.begin(), a.end(), b.begin(), b.end(),
                    std::back_inserter(result));  // {1,2}
```

#### 3.5 Algorytmy numeryczne (`<numeric>`)

```cpp
#include <numeric>

std::vector<int> vec = {1, 2, 3, 4, 5};

int sum = std::accumulate(vec.begin(), vec.end(), 0);           // 15
int product = std::accumulate(vec.begin(), vec.end(), 1,
                              std::multiplies<>());             // 120

// Iloczyn skalarny
std::vector<int> a = {1, 2, 3};
std::vector<int> b = {4, 5, 6};
int dot = std::inner_product(a.begin(), a.end(), b.begin(), 0); // 32

// Sumy częściowe
std::vector<int> prefix(vec.size());
std::partial_sum(vec.begin(), vec.end(), prefix.begin());       // {1,3,6,10,15}
```

---

## 4. Funktory (Function Objects / Functors)

### Definicja
**Funktory** to obiekty, które można wywołać jak funkcje (mają operator `()`). Służą do parametryzacji algorytmów.

### Rodzaje funktorów

#### 4.1 Predefiniowane funktory (`<functional>`)

```cpp
#include <functional>
#include <algorithm>

std::vector<int> vec = {3, 1, 4, 1, 5};

// Funktory arytmetyczne
std::plus<int> add;
int result = add(2, 3);  // 5

// Funktory porównania
std::sort(vec.begin(), vec.end(), std::greater<int>());  // malejąco
std::sort(vec.begin(), vec.end(), std::less<int>());     // rosnąco

// Funktory logiczne
std::logical_and<bool> land;
bool b = land(true, false);  // false
```

#### 4.2 Wyrażenia lambda (C++11)

```cpp
std::vector<int> vec = {3, 1, 4, 1, 5, 9, 2, 6};

// Lambda jako predykat
auto it = std::find_if(vec.begin(), vec.end(),
                       [](int x) { return x > 5; });

// Lambda z przechwytywaniem
int threshold = 4;
int count = std::count_if(vec.begin(), vec.end(),
                          [threshold](int x) { return x > threshold; });

// Lambda modyfikująca (mutable)
int counter = 0;
std::for_each(vec.begin(), vec.end(),
              [&counter](int x) { counter += x; });

// Generic lambda (C++14)
auto generic = [](auto x, auto y) { return x + y; };
```

#### 4.3 std::function i std::bind

```cpp
#include <functional>

// std::function - uniwersalny wrapper na callable
std::function<int(int, int)> func = [](int a, int b) { return a + b; };
func = std::plus<int>();
func = &free_function;

// std::bind - częściowa aplikacja funkcji
auto add5 = std::bind(std::plus<int>(), std::placeholders::_1, 5);
int result = add5(10);  // 15

// std::bind z referencją
void modify(int& x) { x *= 2; }
int n = 5;
auto bound = std::bind(modify, std::ref(n));
bound();  // n == 10
```

---

## 📊 Wzajemne powiązania

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│     KONTENERY ←──── ITERATORY ────→ ALGORYTMY ←──── FUNKTORY     │
│         │              │                 │              │         │
│    przechowują    abstrakcja        operują na     parametryzują  │
│      dane         dostępu           zakresach       algorytmy     │
│         │              │                 │              │         │
│    vector<T>     begin()/end()      sort()        less<T>        │
│    map<K,V>      ++, *, ==          find()        lambdy         │
│    set<T>        random/bidir       transform()   std::function  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### Kluczowa zasada: Ortogonalność

**M kontenerów × N algorytmów = M + N implementacji** (nie M × N!)

Dzięki iteratorom:
- Algorytm `sort` działa z `vector`, `deque`, `array`
- Każdy nowy kontener automatycznie współpracuje z istniejącymi algorytmami
- Każdy nowy algorytm automatycznie współpracuje z istniejącymi kontenerami

---

## 🧠 Mnemoniki

### "KIAF" dla kategorii STL:
- **K**ontenery - CO przechowujemy
- **I**teratory - JAK się poruszamy
- **A**lgorytmy - CO robimy z danymi
- **F**unktory - JAK parametryzujemy operacje

### "VLDA" dla kontenerów sekwencyjnych:
- **V**ector - domyślny wybór, tablica dynamiczna
- **L**ist - szybkie wstawianie w środku
- **D**eque - szybki dostęp do obu końców
- **A**rray - stały rozmiar, na stosie

### "SM-UM" dla asocjacyjnych:
- **S**et/**M**ap - posortowane (drzewo), O(log n)
- **U**nordered_**M**ap/set - hash, O(1)

### "SQP" dla adapterów:
- **S**tack - LIFO (stos talerzy)
- **Q**ueue - FIFO (kolejka do kasy)
- **P**riority_queue - VIP (najważniejsi pierwsi)

### "IOFBRC" dla iteratorów (od najsłabszego):
- **I**nput - tylko czytanie, jedno przejście
- **O**utput - tylko pisanie, jedno przejście
- **F**orward - wielokrotne przejście do przodu
- **B**idirectional - do przodu i do tyłu
- **R**andom - skok do dowolnego miejsca
- **C**ontiguous - ciągła pamięć

---

## ❓ Możliwe pytania dodatkowe (follow-up)

### Q1: "Kiedy użyć vector, a kiedy list?"

**Odpowiedź:**

| Kryterium | vector | list |
|-----------|--------|------|
| Dostęp losowy | O(1) ✓ | O(n) ✗ |
| Wstawianie na końcu | O(1) ✓ | O(1) ✓ |
| Wstawianie w środku | O(n) ✗ | O(1) ✓* |
| Cache-friendly | TAK ✓ | NIE ✗ |
| Pamięć | Mniej | Więcej (wskaźniki) |

*po znalezieniu pozycji

**Praktyczna zasada:** Używaj `vector` domyślnie. `list` tylko gdy:
- Bardzo częste wstawianie/usuwanie w środku
- Iteratory muszą pozostać ważne po modyfikacji
- Nigdy nie potrzebujesz dostępu losowego

---

### Q2: "Czym się różni map od unordered_map?"

**Odpowiedź:**

| Cecha | map | unordered_map |
|-------|-----|---------------|
| Struktura | Drzewo RB | Hash table |
| Złożoność | O(log n) | O(1) średnio |
| Najgorszy przypadek | O(log n) | O(n) |
| Wymagania dla klucza | `operator<` | `hash`, `operator==` |
| Kolejność iteracji | Posortowana | Nieokreślona |
| Stabilność | Iteratory stabilne | Rehashing może unieważnić |

**Kiedy co:**
- `map`: Potrzebujesz kolejności, mały zbiór, klucze trudne do hashowania
- `unordered_map`: Duży zbiór, najważniejsza szybkość, kolejność nieistotna

---

### Q3: "Co to jest iterator invalidation?"

**Odpowiedź:**

**Iterator invalidation** = iterator przestaje wskazywać na ważny element po modyfikacji kontenera.

| Kontener | push_back | insert | erase |
|----------|-----------|--------|-------|
| vector | Może (realloc) | Tak | Tak (od miejsca) |
| deque | Tak | Tak | Tak |
| list | Nie | Nie | Tylko usunięty |
| map/set | Nie | Nie | Tylko usunięty |
| unordered_* | Może (rehash) | Może (rehash) | Tylko usunięty |

```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};
auto it = vec.begin() + 2;

vec.push_back(6);  // it może być INVALID!
vec.insert(vec.begin(), 0);  // it jest INVALID!

// Bezpieczny sposób usuwania
for (auto it = vec.begin(); it != vec.end(); ) {
    if (*it % 2 == 0)
        it = vec.erase(it);  // erase zwraca następny ważny iterator
    else
        ++it;
}
```

---

### Q4: "Jak działa erase-remove idiom?"

**Odpowiedź:**

`std::remove` **nie usuwa** elementów - tylko przesuwa "dobre" na początek i zwraca iterator do "końca" dobrych.

```cpp
std::vector<int> vec = {1, 2, 3, 2, 4, 2, 5};

// BEZ idiomu
// std::remove zwraca iterator do nowego "końca"
auto new_end = std::remove(vec.begin(), vec.end(), 2);
// vec = {1, 3, 4, 5, ?, ?, ?} - stary rozmiar!
//                    ^new_end

// Z idiomem
vec.erase(new_end, vec.end());  // usuń "śmieci"
// vec = {1, 3, 4, 5}

// Jednolinijkowo
vec.erase(std::remove(vec.begin(), vec.end(), 2), vec.end());

// C++20: std::erase (wreszcie!)
std::erase(vec, 2);
```

---

### Q5: "Co to są zakresy (ranges) w C++20?"

**Odpowiedź:**

**Ranges** to ewolucja STL - algorytmy przyjmują kontener zamiast pary iteratorów.

```cpp
#include <ranges>
#include <algorithm>
#include <vector>

std::vector<int> vec = {5, 3, 1, 4, 2};

// C++17 (klasyczne)
std::sort(vec.begin(), vec.end());

// C++20 (ranges)
std::ranges::sort(vec);

// Widoki (views) - leniwe, kompozowalne
auto result = vec 
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * 2; })
    | std::views::take(3);

// Pipeline - nie kopiuje, leniwe obliczenia
for (int x : result) {
    std::cout << x << " ";
}
```

---

### Q6: "Jaka jest złożoność pamięciowa kontenerów?"

**Odpowiedź:**

| Kontener | Pamięć na element | Narzut całkowity |
|----------|-------------------|------------------|
| `array<T,N>` | sizeof(T) | 0 |
| `vector<T>` | sizeof(T) | 3 wskaźniki + capacity |
| `list<T>` | sizeof(T) + 2 wskaźniki | 1 wskaźnik (head) |
| `forward_list<T>` | sizeof(T) + 1 wskaźnik | 1 wskaźnik |
| `deque<T>` | sizeof(T) | Mapa bloków |
| `set<T>` | sizeof(T) + 3 wsk. + kolor | Root + size |
| `unordered_set<T>` | sizeof(T) + wskaźnik | Bucket array |

**Praktyka:** `vector` jest najbardziej cache-friendly (ciągła pamięć).

---

## 🎯 Kluczowe punkty do zapamiętania

1. **4 kategorie:** Kontenery, Iteratory, Algorytmy, Funktory
2. **Ortogonalność:** M kontenerów + N algorytmów = M + N implementacji
3. **vector domyślnie:** Najlepszy cache, wystarczający dla 90% przypadków
4. **Iteratory łączą:** Abstrakcja między kontenerami a algorytmami
5. **Lambda > funktory:** Czytelniejsze, nowocześniejsze
6. **Ranges (C++20):** Przyszłość STL - leniwe, kompozowalne

---

## 📖 Źródła do pogłębienia

1. Josuttis - "The C++ Standard Library"
2. Meyers - "Effective STL"
3. cppreference.com - dokumentacja STL
4. Stepanov - "Elements of Programming"
