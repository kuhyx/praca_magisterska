## PYTANIE 16: Języki programowania robotów

**Omówić specjalizowane języki. Uwypuklić klasyfikację.**

---

### Tło pojęciowe — słowniczek

**Robot** — cz. „robota" = ciężka praca; termin ukuty przez Karla Čapka (R.U.R., 1920). W przemyśle: programowalna maszyna wykonująca zadania (spawanie, paletyzacja, montaż). W kontekście pytania: głównie roboty przemysłowe (manipulatory) — ramiona z 4–7 osiami obrotu, sterowane komputerowo.

**Język programowania robotów** — język do definiowania zachowania robota: ruchy, logika, I/O. Może być specjalizowany (dedykowany producenta) lub ogólny (C++, Python z bibliotekami). Klasyfikacja wg poziomu abstrakcji — od zadań po sygnały silników.

---

**Poziomy abstrakcji T-R-M-S:**

**Task-level (poziom zadania)** — najwyższy: opisujesz CO robot ma zrobić, nie JAK. „Podnieś A, połóż na B." Robot sam planuje ruchy. Przykłady: PDDL, Behavior Trees.

    // Task-level (pseudokod):
    pick(objectA);
    place(locationB);
    // Robot sam oblicza kinematykę, trajektorię, chwyt

**Robot-level (poziom robota)** — komendy ruchu w przestrzeni kartezjańskiej lub konfiguracyjnej: move_to(x,y,z), grasp(). Programista mówi GDZIE jechać, robot oblicza JAK (kinematyka odwrotna). Tu działają języki producentów: RAPID (ABB), KRL (KUKA), Karel (FANUC), PDL2 (Comau), URScript (Universal Robots).

**Motion-level (poziom ruchu)** — planowanie trajektorii: generowanie ciągu punktów od startu do celu z unikaniem kolizji. Kinematyka odwrotna, interpolacja. Przykłady: MoveIt (ROS), OMPL.

**Servo-level (poziom serwa)** — najniższy: bezpośrednie sterowanie silnikami/serwomechanizmami. Regulacja PID, sygnały PWM. Języki: C/C++, FPGA/VHDL. Czas reakcji: mikro-milisekundy.

    Przykład czasu reakcji na każdym poziomie:
    Task:    "Zamontuj śrubę"          (sekundy)
    Robot:   MoveL do_pozycji           (100 ms)
    Motion:  Trajektoria 50 pkt/s       (20 ms)
    Servo:   PID: PWM silnika = 75%     (1 ms)

![Piramida T-R-M-S](img/robot_trms_pyramid.png)

---

**Kinematyka odwrotna (inverse kinematics, IK)** — obliczenie kątów w stawach robota, aby efektor (np. chwytak) znalazł się w zadanej pozycji. Problem odwrotny: znasz cel (x,y,z + orientacja), szukasz konfiguracji (kąty q₁…qₙ). Może mieć 0, 1 lub wiele rozwiązań. Robot 6-osiowy: zazwyczaj do 8 rozwiązań dla jednej pozycji.

    Przykład (robot 2-osiowy, ramiona L₁=L₂=1m, cel: x=1.0, y=1.0):
    q₂ = arccos((x²+y²−L₁²−L₂²) / (2·L₁·L₂))
       = arccos((1+1−1−1)/2) = arccos(0) = 90°
    Dwa rozwiązania: „łokieć do góry" i „łokieć na dół"

**Trajektoria (trajectory)** — zaplanowana ścieżka ruchu w czasie: sekwencja pozycji + prędkości + przyspieszenia. Trzy typy interpolacji:
- **PTP (Point-to-Point)** — najszybsza, ale ścieżka w przestrzeni kartezjańskiej nieprzewidywalna (interpolacja w przestrzeni stawów)
- **LIN (Linear)** — prosta linia TCP (Tool Center Point); wymaga obliczenia IK w każdym punkcie
- **CIRC (Circular)** — łuk kołowy przez 3 punkty (start, pkt pomocniczy, cel)

![Typy ruchu robota](img/robot_movement_types.png)

---

**Vendor lock-in** — każdy producent ma WŁASNY język. Program napisany w RAPID nie działa na robocie KUKA. To motywacja dla ROS i standardów. Porównanie języków:

![Porównanie języków producentów](img/robot_vendor_comparison.png)

---

**TCP (Tool Center Point)** — punkt centralny narzędzia zamontowanego na końcu ramienia (np. czubek spawarki, środek chwytaka). Wszystkie komendy ruchu LIN i CIRC odnoszą się do TCP — robot steruje tak, żeby ten punkt poruszał się po żądanej ścieżce.

    Definiowanie TCP w RAPID:
    PERS tooldata tGripper := [TRUE, [[0,0,150],[1,0,0,0]],
                                [2,[0,0,75],[1,0,0,0],0,0,0]];
    // TCP jest 150mm nad kołnierzem, masa narzędzia 2kg

**Strefa zbliżenia (zone)** — parametr określający, jak blisko celu robot musi dojechać zanim zacznie ruch do kolejnego punktu. `fine` = dojazd dokładnie do punktu (zatrzymanie), `z10` = robot zaczyna skręcać w stronę następnego punktu gdy jest 10mm od celu (ruch „na okrągło", płynniejszy i szybszy).

    MoveL p1, v500, fine, tool1;   // zatrzymaj się dokładnie w p1
    MoveL p1, v500, z50, tool1;    // zacznij skręcać 50mm przed p1
    // z50 → szybszy cykl, ale mniejsza precyzja w punkcie

---

### Klasyfikacja wg poziomu abstrakcji: **T-R-M-S**

1. **Task-level** — „Podnieś A, połóż na B" (PDDL, Behavior Trees)
2. **Robot-level** — move_to(), grasp() (RAPID, KRL, Karel, URScript)
3. **Motion-level** — trajektorie, kinematyka odwrotna (MoveIt, OMPL)
4. **Servo-level** — PID, sterowanie silnikami (C/C++, FPGA)

### Klasyfikacja wg metody programowania

![Online vs Offline](img/robot_online_offline.png)

- **Online (teach-in)** — operator z teach pendantem prowadzi robota i zapisuje punkty. Proste, intuicyjne, ale wymaga wyłączenia produkcji.
- **Offline** — programowanie w symulatorze 3D (RobotStudio, KUKA.Sim, ROBOGUIDE), bez zatrzymywania robota. Wymaga kalibracji po transferze.
- **Hybrid** — w praktyce łączy się oba podejścia: offline do wstępnego programu, online do korekcji punktów.

### Języki producentów — szczegółowo

#### RAPID (ABB)

**Producent:** ABB. **Rozwinięcie:** Robotics Application Programming Interactive Dialogue. **Składnia:** własny typ, strukturalna, wielozadaniowa (RAPID obsługuje wielowątkowość). **Symulator:** RobotStudio (darmowa wersja edukacyjna).

**Kluczowe cechy:**
- Typy danych: `num` (liczba), `string`, `bool`, `robtarget` (pozycja kartezjańska + orientacja + konfiguracja), `jointtarget` (kąty stawów), `tooldata`, `wobjdata` (układ współrzędnych obiektu)
- Ruchy: `MoveJ` (joint — PTP), `MoveL` (linear), `MoveC` (circular), `MoveAbsJ` (absolutne kąty)
- I/O: `SetDO` (digital output), `WaitDI` (czekaj na digital input), `SetAO` (analog out)
- Kontrola przepływu: `IF/ELSEIF/ELSE/ENDIF`, `WHILE/ENDWHILE`, `FOR/ENDFOR`, `TEST/CASE/DEFAULT/ENDTEST`
- Obsługa błędów: `TRAP` (przerwania), `ERROR` handler
- Wielozadaniowość: wiele tasków wykonywanych równolegle — np. jeden task steruje ruchem, drugi monitoruje czujniki

**Przykładowy program pick & place:**

    MODULE MainModule
        ! --- Dane ---
        CONST robtarget pHome  := [[500,0,600],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
        CONST robtarget pPick  := [[400,200,100],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
        CONST robtarget pPlace := [[400,-200,100],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
        VAR num nCycles := 0;

        ! --- Procedura główna ---
        PROC main()
            MoveJ pHome, v1000, z50, tGripper;     ! jedź do pozycji bazowej (joint)
            WHILE TRUE DO
                PickPart;
                PlacePart;
                Incr nCycles;
                TPWrite "Cykl nr: " + ValToStr(nCycles);
            ENDWHILE
        ENDPROC

        ! --- Podnoszenie ---
        PROC PickPart()
            MoveL Offs(pPick,0,0,50), v500, z10, tGripper;   ! 50mm nad celem
            MoveL pPick, v100, fine, tGripper;                 ! precyzyjnie na cel
            SetDO doGripper, 1;                                ! zamknij chwytak
            WaitTime 0.3;                                      ! czekaj na zamknięcie
            MoveL Offs(pPick,0,0,50), v500, z10, tGripper;   ! podnieś 50mm
        ENDPROC

        ! --- Odkładanie ---
        PROC PlacePart()
            MoveL Offs(pPlace,0,0,50), v500, z10, tGripper;  ! 50mm nad miejscem
            MoveL pPlace, v100, fine, tGripper;                ! precyzyjnie na cel
            SetDO doGripper, 0;                                ! otwórz chwytak
            WaitTime 0.3;
            MoveL Offs(pPlace,0,0,50), v500, z10, tGripper;  ! podnieś 50mm
        ENDPROC
    ENDMODULE

**Objaśnienie parametrów MoveL:**

    MoveL  pPick,  v500,   z10,    tGripper;
    │      │       │       │       └── narzędzie (tooldata) — definiuje TCP
    │      │       │       └── strefa zbliżenia: 10mm (nie zatrzymuj się, skręcaj)
    │      │       └── prędkość TCP: 500 mm/s
    │      └── cel: robtarget (pozycja + orientacja + konfiguracja)
    └── typ ruchu: ruch liniowy (TCP jedzie po prostej)

![Struktura programu RAPID](img/robot_rapid_example.png)

---

#### KRL (KUKA Robot Language)

**Producent:** KUKA. **Rozwinięcie:** KUKA Robot Language. **Składnia:** Pascal-like (BEGIN/END, deklaracje na początku). **Symulator:** KUKA.Sim Pro, WorkVisual.

**Kluczowe cechy:**
- Program = dwa pliki: `.src` (kod) + `.dat` (dane punktów)
- Typy: `INT`, `REAL`, `BOOL`, `CHAR`, `POS` (x,y,z,a,b,c), `E6POS` (+ osie dodatkowe), `AXIS` (kąty stawów)
- Ruchy: `PTP` (point-to-point = joint), `LIN` (linear), `CIRC` (circular)
- Approximation (odpowiednik zone w RAPID): `C_DIS` — robot nie zatrzymuje się w punkcie
- Kontrola przepływu: `IF/ENDIF`, `WHILE/ENDWHILE`, `FOR/ENDFOR`, `SWITCH/CASE/ENDSWITCH`

**Przykładowy program:**

    DEF PickAndPlace()
        ; --- Deklaracje ---
        DECL E6POS XHome, XPick, XPlace
        DECL INT nLoop

        ; --- Inicjalizacja ---
        BAS (#INITMOV, 0)         ; inicjalizacja ruchów
        $VEL.CP = 0.5             ; prędkość kartezjańska 0.5 m/s
        $APO.CDIS = 10            ; approximacja: 10mm

        ; --- Ruch do domu ---
        PTP XHome                 ; point-to-point (joint space)

        FOR nLoop = 1 TO 100
            ; Podjedź nad punkt pobrania
            LIN XPick              ; ruch liniowy do punktu
            ; Zamknij chwytak
            OUT 1 TRUE             ; digital output 1 = ON
            WAIT SEC 0.3
            ; Jedź do miejsca odkładania
            LIN XPlace
            OUT 1 FALSE            ; otwórz chwytak
            WAIT SEC 0.3
        ENDFOR
    END

**KRL vs RAPID — kluczowe różnice:**
- KRL rozdziela kod (`.src`) od danych (`.dat`); RAPID trzyma wszystko w MODULE
- KRL: `$VEL.CP = 0.5` (zmienna systemowa); RAPID: `v500` (nazwany speeddata)
- KRL: `C_DIS` approximation; RAPID: `z10` zone
- KRL: `OUT 1 TRUE`; RAPID: `SetDO doGripper, 1`

---

#### Karel (FANUC)

**Producent:** FANUC. **Nazwa:** od Karla Čapka. **Składnia:** Pascal-like (PROGRAM/BEGIN/END, VAR). **Symulator:** ROBOGUIDE.

**Kluczowe cechy:**
- Dwa tryby: Karel (tekstowy, pełny język) i TP (Teach Pendant — uproszczony, listowy)
- Karel: kompilowany, typowany, procedury/funkcje
- Typy: `INTEGER`, `REAL`, `BOOLEAN`, `STRING`, `POSITION`, `XYZWPR`
- TP program jest częściej używany w praktyce (prostszy, operatorzy go rozumieją)

**Przykład Karel:**

    PROGRAM pick_place
    VAR
        home_pos : POSITION
        pick_pos : POSITION
        place_pos : POSITION
        cycle_count : INTEGER
    BEGIN
        cycle_count = 0
        -- Jedź do domu
        MOVE TO home_pos
        WHILE cycle_count < 100 DO
            -- Podnoszenie
            MOVE TO pick_pos
            DOUT[1] = ON           -- zamknij chwytak
            DELAY 300              -- czekaj 300ms
            -- Odkładanie
            MOVE TO place_pos
            DOUT[1] = OFF          -- otwórz chwytak
            DELAY 300
            cycle_count = cycle_count + 1
        ENDWHILE
    END pick_place

**Przykład TP (Teach Pendant) — to widzi operator:**

       1: J P[1] 100% FINE          ; joint move do Home, 100% speed
       2: L P[2] 500mm/sec FINE     ; linear do Pick
       3: DO[1]=ON                  ; chwytak zamknij
       4: WAIT 0.30(sec)
       5: L P[3] 500mm/sec FINE     ; linear do Place
       6: DO[1]=OFF                 ; chwytak otwórz
       7: WAIT 0.30(sec)
       8: JMP LBL[1]               ; skocz do linii 1

**Uwaga:** W praktyce fabrycznej TP jest dominujący — operatorzy uczą się numerowanych linii, nie pełnego Karela.

---

#### URScript (Universal Robots)

**Producent:** Universal Robots (coboty — collaborative robots). **Składnia:** Python-like (brak nawiasów klamrowych, wcięcia nie mają znaczenia, ale styl jest skryptowy). **Symulator:** URSim (darmowy, oparty na VM).

**Kluczowe cechy:**
- Skryptowy i prosty — niski próg wejścia (coboty = roboty współpracujące z ludźmi)
- Wbudowane funkcje force control (sterowanie siłą) — unikalne dla cobotów
- Typy: brak deklaracji typów (dynamiczne), `pose` = [x,y,z,rx,ry,rz]
- Polyscope — graficzny interfejs do programowania (drag & drop + URScript)

**Przykład URScript:**

    def pick_and_place():
        # Pozycje jako pose: [x, y, z, rx, ry, rz] w metrach i radianach
        home  = p[0.5, 0.0, 0.4, 3.14, 0.0, 0.0]
        pick  = p[0.4, 0.2, 0.1, 3.14, 0.0, 0.0]
        place = p[0.4, -0.2, 0.1, 3.14, 0.0, 0.0]

        movej(home, a=1.2, v=0.5)          # joint move, acc=1.2 rad/s², vel=0.5 rad/s

        i = 0
        while i < 100:
            # Podnoszenie
            movel(pick, a=0.5, v=0.3)      # linear move
            set_digital_out(0, True)        # zamknij chwytak
            sleep(0.3)

            # Odkładanie
            movel(place, a=0.5, v=0.3)
            set_digital_out(0, False)       # otwórz chwytak
            sleep(0.3)

            i = i + 1
        end
    end

**URScript — unikalne cechy cobotów:**

    # Force mode — wkładanie kołka w otwór z kontrolą siły:
    force_mode(p[0,0,0,0,0,0], [0,0,1,0,0,0], [0,0,-10,0,0,0], 2, [0.1,0.1,0.05,1,1,1])
    # Robot naciska z siłą 10N w dół (oś Z), reszt osi blokuje

    # Freedrive — operator prowadzi robota ręcznie:
    freedrive_mode()
    sleep(10)   # 10 sekund swobodnego prowadzenia
    end_freedrive_mode()

---

#### PDL2 (Comau)

**Producent:** Comau (Fiat/Stellantis). **Składnia:** proceduralna, C-like. **Symulator:** RoboSim.

**Przykład:**

    PROGRAM pick_place
    VAR home_pos, pick_pos, place_pos : POSITION
    BEGIN
        MOVE TO home_pos
        CYCLE
            MOVE LINEAR TO pick_pos
            $DOUT[1] := TRUE          -- chwytak
            DELAY 300
            MOVE LINEAR TO place_pos
            $DOUT[1] := FALSE
            DELAY 300
        END CYCLE
    END pick_place

---

### Porównanie składni — ten sam ruch w 5 językach

    Zadanie: ruch liniowy do punktu pPick z prędkością ~500mm/s

    RAPID (ABB):    MoveL pPick, v500, fine, tGripper;
    KRL (KUKA):     LIN XPick
    Karel (FANUC):  MOVE TO pick_pos                      ; z opcją LINEAR
    TP (FANUC):     L P[2] 500mm/sec FINE
    URScript (UR):  movel(pick, a=0.5, v=0.5)
    PDL2 (Comau):   MOVE LINEAR TO pick_pos

### Języki uniwersalne i middleware

#### ROS / ROS 2 (Robot Operating System)

**ROS** to middleware (NIE system operacyjny!) — warstwa komunikacji między modułami (węzłami). Programuje się w Python lub C++. Architektura publish/subscribe: węzły publikują wiadomości na tematy (topics), inne węzły subskrybują.

![Architektura ROS](img/robot_ros_architecture.png)

**ROS 1 vs ROS 2:**
- ROS 1: roscore (centralny master), brak real-time, Python 2/3 + C++
- ROS 2: DDS (bez centralnego mastera, peer-to-peer), real-time friendly, Python 3 + C++17
- ROS 2 dodaje: lifecycle nodes, QoS (Quality of Service), lepsze multi-robot

**Przykład ROS 2 (Python) — publisher prędkości:**

    import rclpy
    from geometry_msgs.msg import Twist

    def main():
        rclpy.init()
        node = rclpy.create_node('velocity_publisher')
        pub = node.create_publisher(Twist, '/cmd_vel', 10)

        msg = Twist()
        msg.linear.x = 0.5    # 0.5 m/s do przodu
        msg.angular.z = 0.1   # obrót 0.1 rad/s

        timer = node.create_timer(0.1, lambda: pub.publish(msg))  # co 100ms
        rclpy.spin(node)

**MoveIt** — biblioteka ROS do planowania ruchu manipulatorów. Obejmuje: IK, collision avoidance, trajectory planning. Wspiera roboty wielu producentów — klucz do przełamania vendor lock-in.

    # MoveIt — planowanie ruchu w Pythonie:
    move_group = MoveGroupCommander("arm")
    move_group.set_pose_target(target_pose)     # cel w kartezjańskiej
    plan = move_group.plan()                     # automatyczny plan trajektorii
    move_group.execute(plan)                     # wykonaj

#### Orocos (Open Robot Control Software)

Framework C++ do **hard real-time** sterowania robotów. Tam gdzie ROS nie wystarczy (pętle regulacji < 1ms), Orocos wypełnia lukę. Często łączony z ROS: ROS do komunikacji + Orocos do sterowania.

---

### Task-level: PDDL i Behavior Trees

#### PDDL (Planning Domain Definition Language)

Język opisu problemów planowania. Definiujesz: stany, akcje z warunkami i efektami, cel. Planner (np. Fast Downward) automatycznie znajduje sekwencję akcji.

    ; PDDL — domena: robot pick & place
    (define (domain robot-world)
        (:predicates
            (on-table ?obj)
            (holding ?obj)
            (arm-empty))
        (:action pick
            :parameters (?obj)
            :precondition (and (on-table ?obj) (arm-empty))
            :effect (and (holding ?obj) (not (on-table ?obj)) (not (arm-empty))))
        (:action place
            :parameters (?obj)
            :precondition (holding ?obj)
            :effect (and (on-table ?obj) (arm-empty) (not (holding ?obj)))))

    ; Problem: weź obiektA ze stołu
    (define (problem pick-a)
        (:domain robot-world)
        (:init (on-table objectA) (arm-empty))
        (:goal (holding objectA)))

    ; Planner automatycznie znajdzie: pick(objectA)

#### Behavior Trees (drzewa zachowań)

Alternatywa dla maszyn stanów w sterowaniu robotów i postaci w grach. Drzewo składa się z:
- **Sequence** (→) — wykonuj dzieci po kolei, przerwij jeśli któreś zawiedzie
- **Selector** (?) — próbuj dzieci po kolei, przerwij po pierwszym sukcesie
- **Action** — liść: wykonaj akcję
- **Condition** — liść: sprawdź warunek

    Behavior Tree: „Pick and Place"
    [→ Sequence]
        ├── [? Selector: FindObject]
        │     ├── [Condition: ObjectVisible?]
        │     └── [Action: SearchForObject]
        ├── [Action: MoveToObject]
        ├── [Action: Grasp]
        ├── [Action: MoveToTarget]
        └── [Action: Release]

---

### Środowiska graficzne

| Narzędzie    | Producent | Typ                    | Koszt            |
|-------------|-----------|------------------------|------------------|
| RobotStudio | ABB       | Offline + symulacja 3D | Licencja / edu   |
| KUKA.Sim    | KUKA      | Offline + symulacja 3D | Licencja         |
| ROBOGUIDE   | FANUC     | Offline + symulacja 3D | Licencja         |
| URSim       | UR        | Symulator kontrolera   | Darmowy          |
| Polyscope   | UR        | GUI na teach pendancie | Wbudowany        |
| Blockly     | Różni     | Graficzne (edukacja)   | Open source      |
| Gazebo      | ROS/OSRF  | Symulacja fizyczna 3D  | Open source      |

### Podsumowanie klasyfikacji

| Kryterium           | Kategorie                                                |
|--------------------|----------------------------------------------------------|
| **Poziom abstrakcji** | Task → Robot → Motion → Servo (T-R-M-S)              |
| **Metoda**           | Online (teach-in) vs Offline (symulacja) vs Hybrid    |
| **Zakres**           | Vendor-specific (RAPID, KRL, Karel) vs Universal (ROS)|
| **Interfejs**        | Tekstowy (RAPID, KRL) vs Graficzny (Polyscope, Blockly)|
| **Real-time**        | Hard RT (Orocos, C/FPGA) vs Soft RT (ROS 2)          |

### Etymologia

**RAPID** — Robotics Application Programming Interactive Dialogue (ABB, 1994). **KRL** — KUKA Robot Language (KUKA, Augsburg). **Karel** — od Karla Čapka, czeskiego pisarza, który ukuł słowo „robot" (cz. „robota" = ciężka/przymusowa praca) w sztuce R.U.R. (Rossum's Universal Robots, 1920). **PDL2** — Programming and Data Language 2 (Comau). **URScript** — Universal Robots Script. **PDDL** — Planning Domain Definition Language (Drew McDermott et al., 1998). **MoveIt** — open source, Willow Garage → PickNik Robotics. **ROS** — Robot Operating System (Willow Garage, 2007 → Open Robotics). **Orocos** — Open Robot Control Software (KU Leuven, Belgia). **TCP** — Tool Center Point (nie mylić z Transmission Control Protocol!). **OMPL** — Open Motion Planning Library. **Cobot** — collaborative robot (termin 1996, Northwestern University).

### Jak zapamiętać

- **„Tomek Robi Mechaniczne Serwa" → T-R-M-S** (Task → Robot → Motion → Servo, od abstrakcji do sprzętu)
- **„ABB RAPID jak rapier (szybki miecz)" → MoveL, MoveJ, MoveC** — trzy podstawowe ruchy
- **„KUKA KRL = Pascal na sterydach"** — PTP, LIN, CIRC; dwa pliki (.src + .dat)
- **„FANUC Karel = Čapek" → MOVE TO** — najprostszy składniowo
- **„UR = Python robota" → movel(), movej()** — małe litery, skryptowy, coboty
- **„ROS = WhatsApp robotów"** — węzły wysyłają wiadomości na tematy (topics), ale to NIE system operacyjny
- **Vendor lock-in → „Program w RAPID na KUKA = jak wtyczka EU w gniazdku UK"** — nie pasuje
- **Online = „trzymaj robota za rękę", Offline = „rysuj w symulatorze"**
- **MoveIt = „GPS dla ramienia robota"** — planuje trasę z unikaniem przeszkód
- **Zone/Approximation = „hamowanie przed zakrętem"** — fine = stop, z50 = przejeżdżaj płynnie

