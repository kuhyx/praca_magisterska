# Pytanie 22: Języki programowania robotów

## Pytanie
**"Omówić specjalizowane języki programowania robotów. Uwypuklić ich klasyfikację."**

Przedmiot: ERPM (Elementy Robotyki i Projektowania Mechatronicznego)

---

## 📚 Odpowiedź główna

### 1. Klasyfikacja języków programowania robotów

```
┌─────────────────────────────────────────────────────────────────┐
│               JĘZYKI PROGRAMOWANIA ROBOTÓW                      │
├─────────────────────────────────────────────────────────────────┤
│  POZIOM ABSTRAKCJI:                                             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ TASK-LEVEL (Zadaniowy)                                  │   │
│  │ "Podnieś obiekt A i połóż na B"                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ROBOT-LEVEL (Obiektowy)                                 │   │
│  │ move_to(position), grasp(), release()                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ MOTION-LEVEL (Ruchowy)                                  │   │
│  │ Trajektorie, interpolacja, kinematyka                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ SERVO-LEVEL (Napędowy)                                  │   │
│  │ Sterowanie silnikami, PID, momenty                     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. Klasyfikacja wg metody programowania

| Metoda | Opis | Przykłady |
|--------|------|-----------|
| **Online (Teach-in)** | Programowanie przez demonstrację | Pendant, prowadzenie ręczne |
| **Offline** | Programowanie bez robota | Symulacja, CAD/CAM |
| **Tekstowe** | Kod źródłowy | RAPID, KRL, Karel |
| **Graficzne** | Bloki, flowcharty | Blockly, ROBOGUIDE |

---

### 3. Języki producentów robotów przemysłowych

#### RAPID (ABB)

```rapid
MODULE MainModule
  PROC main()
    MoveJ pHome, v1000, z50, tool1;
    MoveL pPick, v500, fine, tool1;
    GripClose;
    MoveL pPlace, v500, fine, tool1;
    GripOpen;
  ENDPROC
ENDMODULE

! MoveJ = ruch w przestrzeni złączy (Joint)
! MoveL = ruch liniowy (Linear)
! v500 = prędkość 500 mm/s
! fine/z50 = dokładność (fine = dokładnie)
```

#### KRL - KUKA Robot Language

```krl
DEF Pick_and_Place()
  PTP HOME
  LIN pPick
  GripperClose()
  LIN pPlace
  GripperOpen()
  PTP HOME
END

; PTP = Point-to-Point (ruch złączowy)
; LIN = ruch liniowy
; CIRC = ruch kołowy
```

#### Karel (FANUC)

```karel
PROGRAM pick_place
BEGIN
  MOVE TO home_pos
  MOVE TO pick_pos
  CLOSE HAND 1
  MOVE TO place_pos
  OPEN HAND 1
END pick_place
```

#### PDL2 (Comau)
```pdl2
PROGRAM main
BEGIN
  MOVE TO home_jnt
  MOVE LINEAR TO pick_point
  $DOUT[1] := ON   -- gripper
  MOVE LINEAR TO place_point
  $DOUT[1] := OFF
END main
```

---

### 4. Porównanie języków producentów

| Cecha | RAPID (ABB) | KRL (KUKA) | Karel (FANUC) |
|-------|-------------|------------|---------------|
| **Paradygmat** | Proceduralny | Proceduralny | Proceduralny |
| **Typy ruchów** | MoveJ, MoveL, MoveC | PTP, LIN, CIRC | MOVE TO |
| **Zmienne** | VAR, PERS, CONST | DECL | VAR |
| **I/O** | SetDO, WaitDI | $OUT[], $IN[] | DOUT[], DIN[] |
| **Wielozadaniowość** | Tak (TASK) | Tak (SUBMIT) | Tak (TASK) |

---

### 5. Języki uniwersalne i frameworki

#### ROS (Robot Operating System)

```python
# Python + rospy
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('robot_controller')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

twist = Twist()
twist.linear.x = 0.5
twist.angular.z = 0.1
pub.publish(twist)
```

#### MoveIt (ROS)

```python
# Planowanie ruchu manipulatora
import moveit_commander

move_group = moveit_commander.MoveGroupCommander("arm")
move_group.set_pose_target(target_pose)
plan = move_group.go(wait=True)
```

#### Orocos / RTT

```cpp
// Real-Time Toolkit - C++
class MyComponent : public RTT::TaskContext {
  void updateHook() {
    // Pętla sterowania (deterministyczna)
  }
};
```

---

### 6. Języki graficzne

| Narzędzie | Producent | Opis |
|-----------|-----------|------|
| **RobotStudio** | ABB | RAPID + symulacja 3D |
| **KUKA.Sim** | KUKA | KRL + symulacja |
| **ROBOGUIDE** | FANUC | Karel + symulacja |
| **Blockly** | Google | Programowanie wizualne (edukacja) |
| **Scratch for Robots** | MIT | Edukacja, LEGO, mBot |

---

### 7. Klasyfikacja wg poziomu abstrakcji

```
┌─────────────────────────────────────────────────────────────────┐
│ Task-Level:                                                     │
│   "Złóż produkt X z części A, B, C"                            │
│   → Planowanie automatyczne, AI                                │
│   Przykłady: STRIPS, PDDL, Behavior Trees                      │
├─────────────────────────────────────────────────────────────────┤
│ Robot-Level:                                                    │
│   move_to(), pick(), place(), wait()                           │
│   → RAPID, KRL, Karel, Python+ROS                              │
├─────────────────────────────────────────────────────────────────┤
│ Motion-Level:                                                   │
│   Trajektorie, splajny, kinematyka odwrotna                    │
│   → MoveIt, OMPL, IKFast                                       │
├─────────────────────────────────────────────────────────────────┤
│ Servo-Level:                                                    │
│   PID, sterowanie momentem, prądem                             │
│   → C/C++, FPGA, PLC (Ladder, ST)                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mnemoniki

### "RAPID = Robot Application Programming in Data":
Język ABB - MoveJ, MoveL, MoveC

### "KRL = KUKA Robot Language":
PTP, LIN, CIRC

### "ROS = Robot Operating System":
Middleware - topics, services, actions

### "Od zadania do serwa: T-R-M-S":
Task → Robot → Motion → Servo

---

## ❓ Pytania dodatkowe

### Q1: "Czym różni się ruch PTP od LIN?"
**Odpowiedź:** PTP (Point-to-Point) = ruch w przestrzeni złączy, najszybszy ale trajektoria TCP nieprzewidywalna. LIN (Linear) = ruch liniowy TCP, wolniejszy ale precyzyjna ścieżka. LIN wymaga rozwiązania kinematyki odwrotnej w każdym punkcie.

### Q2: "Dlaczego każdy producent ma własny język?"
**Odpowiedź:** Historyczne (lata 80-90), integracja ze sterownikiem, optymalizacja dla konkretnego sprzętu, vendor lock-in. ROS próbuje to ujednolicić, ale nie dla real-time.

### Q3: "Co to jest Teach Pendant?"
**Odpowiedź:** Przenośny panel do programowania online. Przyciski ruchu (jog), zapis punktów, edycja programu. Tryb manualny (bezpieczny) vs automatyczny.

---

## 🎯 Kluczowe punkty

1. **Klasyfikacja:** Online/Offline, Task/Robot/Motion/Servo level
2. **Producenci:** RAPID (ABB), KRL (KUKA), Karel (FANUC)
3. **Uniwersalne:** ROS + Python/C++, MoveIt
4. **Graficzne:** RobotStudio, ROBOGUIDE, Blockly

---

## 📖 Źródła

1. Siciliano, Khatib - "Springer Handbook of Robotics"
2. ABB RAPID Reference Manual
3. KUKA KRL Documentation
4. ROS Wiki - ros.org
