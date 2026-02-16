## PYTANIE 16: Języki programowania robotów

**Omówić specjalizowane języki. Uwypuklić klasyfikację.**

---

### Tło pojęciowe — słowniczek

**Robot** — cz. „robota" = ciężka praca; termin ukuty przez Karla Čapka (R.U.R., 1920). W przemyśle: programowalna maszyna wykonująca zadania (spawanie, paletyzacja, montaż). W kontekście pytania: głównie roboty przemysłowe (manipulatory).

**Język programowania robotów** — język do definiowania zachowania robota: ruchy, logika, I/O. Może być specjalizowany (dedykowany producenta) lub ogólny (C++, Python z bibliotekami). Klasyfikacja wg poziomu abstrakcji — od zadań po sygnały silników.

---

**Poziomy abstrakcji T-R-M-S:**

**Task-level (poziom zadania)** — najwyższy: opisujesz CO robot ma zrobić, nie JAK. „Podnieś A, połóż na B." Robot sam planuje ruchy. Przykłady: PDDL, Behavior Trees.

    // Task-level:
    pick(objectA);
    place(locationB);
    // Robot sam oblicza kinematykę, trajektorię, chwyt

**Robot-level (poziom robota)** — komendy ruchu w przestrzeni kartezjańskiej lub konfiguracyjnej: move_to(x,y,z), grasp(). Programista mówi GDZIE jechać, robot oblicza JAK (kinematyka odwrotna). Przykłady: RAPID (ABB), KRL (KUKA), Karel (FANUC).

    // RAPID (ABB):
    MoveL p1, v500, fine, tool1;  // liniowo do p1, prędkość 500 mm/s

**Motion-level (poziom ruchu)** — planowanie trajektorii: generowanie ciągu punktów od startu do celu z unikaniem kolizji. Kinematyka odwrotna, interpolacja. Przykłady: MoveIt (ROS), OMPL.

**Servo-level (poziom serwa)** — najniższy: bezpośrednie sterowanie silnikami/serwomechanizmami. Regulacja PID, sygnały PWM. Języki: C/C++, FPGA. Czas reakcji: mikro-milisekundy.

    Task:    "Zamontuj śrubę"          (sekundy)
    Robot:   MoveL do_pozycji           (100ms)
    Motion:  Trajektoria 50 pkt/s       (20ms)
    Servo:   PID: PWM silnika = 75%     (1ms)

---

**Kinematyka odwrotna (inverse kinematics, IK)** — obliczenie kątów w stawach robota, aby efektor (np. chwytak) znalazł się w zadanej pozycji. Problem odwrotny: znasz cel, szukasz konfiguracji. Może mieć 0, 1 lub wiele rozwiązań.

**Trajektoria (trajectory)** — zaplanowana ścieżka ruchu w czasie: sekwencja pozycji + prędkości + przyspieszenia. Interpolacja: liniowa (LIN), kołowa (CIRC), punkt-do-punktu (PTP).

---

**Języki producentów (vendor-specific):**
- **RAPID (ABB)** — Robotics Application Programming Interactive Dialogue. Ruchy: MoveJ (joint), MoveL (linear), MoveC (circular).
- **KRL (KUKA Robot Language)** — PTP (point-to-point), LIN (linear), CIRC (circular). Pascal-like syntax.
- **Karel (FANUC)** — od Karla Čapka. MOVE TO target. Pascal-like.
- **PDL2 (Comau)** — MOVE LINEAR TO. Proceduralne.

**Vendor lock-in** — każdy producent ma WŁASNY język. Program napisany w RAPID nie działa na robocie KUKA. To motywacja dla ROS i standardów.

**Online vs Offline programming:**
- **Online (teach-in)** — operator prowadzi robota „za rękę" (pendant/teach pendant), robot zapamiętuje punkty. Proste, ale wymaga zatrzymania produkcji.
- **Offline** — programowanie w symulacji (CAD/CAM), bez zatrzymywania robota. Transferujesz gotowy program.

---

**ROS (Robot Operating System)** — middleware (nie OS!) do robotyki. Model pub/sub: węzły publikują/subskrybują tematy. Uniwersalny — działa z robotami różnych producentów. Głównie Python/C++. Wada: nie nadaje się do hard real-time (soft real-time OK; ROS 2 poprawia).

**MoveIt** — biblioteka ROS do planowania ruchu manipulatorów. Obejmuje: IK, collision avoidance, trajectory planning. Open source.

**PDDL (Planning Domain Definition Language)** — język opisu problemów planowania. Definiujesz: stany, akcje, warunki, cel. Planner automatycznie znajduje sekwencję akcji. Task-level.

**FPGA (Field-Programmable Gate Array)** — programowalny układ logiczny. Dla servo-level: przetwarzanie sygnałów w nanosekundach. Szybszy niż mikrokontroler, ale trudniejszy w programowaniu.

---

### Klasyfikacja wg poziomu abstrakcji: **T-R-M-S**

1. **Task-level** — „Podnieś A, połóż na B" (PDDL, Behavior Trees)
2. **Robot-level** — move_to(), grasp() (RAPID, KRL, Karel, ROS)
3. **Motion-level** — trajektorie, kinematyka odwrotna (MoveIt, OMPL)
4. **Servo-level** — PID, sterowanie silnikami (C/C++, FPGA)

### Klasyfikacja wg metody: Online (teach-in, pendant) vs Offline (symulacja, CAD)

### Języki producentów

| Producent | Język | Ruchy              |
|-----------|-------|--------------------|
| ABB       | RAPID | MoveJ, MoveL, MoveC|
| KUKA      | KRL   | PTP, LIN, CIRC     |
| FANUC     | Karel | MOVE TO            |
| Comau     | PDL2  | MOVE LINEAR TO     |

### Uniwersalne: ROS + Python/C++, MoveIt (planowanie manipulatora), Orocos (real-time)

### Graficzne: RobotStudio (ABB), ROBOGUIDE (FANUC), Blockly (edukacja)

### Etymologia

**RAPID** — Robotics Application Programming Interactive Dialogue (ABB). **KRL** — KUKA Robot Language. **Karel** — od Karla Čapka, czeskiego pisarza, który ukuł słowo „robot" (cz. „robota" = ciężka/przymusowa praca) w sztuce R.U.R. (1920). **PDDL** — Planning Domain Definition Language. **MoveIt** — open source do planowania ruchu manipulatora (Willow Garage/PickNik). **Robot** — cz. „robota" = pańszczyzna; Karel Čapek, R.U.R. (1920).

### Jak zapamiętać

- **„Od zadania do serwa: T-R-M-S"**
- Każdy producent ma WŁASNY język (vendor lock-in)
- ROS próbuje ujednolicić, ale nie dla hard real-time

