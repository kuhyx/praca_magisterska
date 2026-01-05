# Appendix C: Unity to Unreal Conversion Notes

[← Appendix B: Troubleshooting](appendix-b-troubleshooting.md) | [Back to Index](README.md)

---

## Scale Conversion

| Unity | Unreal | Notes |
|-------|--------|-------|
| 1 unit = 1 meter | 1 unit = 1 centimeter | Multiply Unity values by 100 |

**Example:**
- Unity speed: `7.5` → Unreal speed: `750`
- Unity position: `(5, 10, 0)` → Unreal position: `(500, 1000, 0)`

---

## Coordinate System

| Axis | Unity | Unreal |
|------|-------|--------|
| Up | Y | Z |
| Forward | Z | X |
| Right | X | Y |

**For 2D top-down games:**
- Both use X for horizontal
- Y/Z swap for vertical

---

## Common Operations Comparison

### Input

**Unity:**
```csharp
float h = Input.GetAxisRaw("Horizontal");
float v = Input.GetAxisRaw("Vertical");
```

**Unreal (Enhanced Input):**
1. Create Input Action (IA_Move) with Axis2D type
2. Create Input Mapping Context with key bindings
3. Add Mapping Context in BeginPlay
4. Use "Get Action Value" node to read input

---

### Instantiate / Spawn

**Unity:**
```csharp
Instantiate(prefab, position, rotation);
```

**Unreal:**
```
Spawn Actor from Class
├── Class: YourBlueprintClass
├── Spawn Transform Location: position
└── Spawn Transform Rotation: rotation
```

---

### Destroy

**Unity:**
```csharp
Destroy(gameObject);
```

**Unreal:**
```
Destroy Actor
└── Target: Self (or reference)
```

---

### Delta Time

**Unity:**
```csharp
Time.deltaTime
```

**Unreal:**
```
Get World Delta Seconds
```

---

### Find Objects

**Unity:**
```csharp
FindObjectOfType<PlayerController>();
FindObjectsOfType<Enemy>();
```

**Unreal:**
```
Get All Actors of Class
├── Actor Class: BP_Player
└── Out Actors: (array)

Then: Get (a ref) → index 0
```

---

### Singleton Pattern

**Unity:**
```csharp
public static GameManager Instance { get; private set; }

void Awake() {
    Instance = this;
}
```

**Unreal Options:**
1. **Game Instance** - Persists across levels
2. **Subsystem** - Engine-managed singleton
3. **Get All Actors of Class** - Find at runtime

---

### Coroutines vs Timers

**Unity:**
```csharp
StartCoroutine(DelayedAction());

IEnumerator DelayedAction() {
    yield return new WaitForSeconds(2.0f);
    DoSomething();
}
```

**Unreal:**
```
Set Timer by Function Name
├── Function Name: "DelayedAction"
├── Time: 2.0
└── Looping: false
```

Or use **Delay** node in blueprints.

---

### Physics Layers vs Collision Channels

**Unity:**
- Layer-based collision matrix
- `Physics.IgnoreLayerCollision()`

**Unreal:**
- Collision Channels (Object Types)
- Collision Presets
- Per-component collision settings

---

### Tags

**Unity:**
```csharp
if (other.CompareTag("Enemy")) { }
```

**Unreal:**
```
Actor Has Tag
├── Target: Other Actor
└── Tag: "Enemy"
```

Or use **Cast To** for type checking (preferred).

---

### Vector Math

| Operation | Unity | Unreal |
|-----------|-------|--------|
| Normalize | `vector.normalized` | `Normalize` node |
| Magnitude | `vector.magnitude` | `Vector Length` node |
| Dot Product | `Vector3.Dot(a, b)` | `Dot Product` node |
| Cross Product | `Vector3.Cross(a, b)` | `Cross Product` node |

---

### Random

**Unity:**
```csharp
Random.Range(0f, 1f);
Random.Range(0, 10); // int, exclusive max
```

**Unreal:**
```
Random Float in Range
├── Min: 0.0
└── Max: 1.0

Random Integer in Range
├── Min: 0
└── Max: 9  // inclusive!
```

> ⚠️ **Note:** Unreal's integer range is INCLUSIVE on both ends!

---

### Debug

**Unity:**
```csharp
Debug.Log("Message");
Debug.DrawLine(start, end, Color.red);
```

**Unreal:**
```
Print String
└── In String: "Message"

Draw Debug Line
├── Line Start: start
├── Line End: end
└── Line Color: Red
```

---

## Quick Reference Table

| Concept | Unity | Unreal |
|---------|-------|--------|
| Script | C# MonoBehaviour | Blueprint / C++ Actor |
| Prefab | .prefab asset | Blueprint Class |
| Scene | .unity scene | Level (.umap) |
| Inspector | Inspector window | Details panel |
| Hierarchy | Hierarchy window | Outliner |
| Project | Project window | Content Browser |
| Console | Console window | Output Log |
| Play | Play button | Play (Alt+P) |

---

[← Appendix B: Troubleshooting](appendix-b-troubleshooting.md) | [Back to Index](README.md)
