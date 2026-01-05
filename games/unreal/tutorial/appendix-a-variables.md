# Appendix A: Complete Variable Reference

[← Part 9: Final Setup](part-9-final-setup.md) | [Back to Index](README.md) | [Appendix B: Troubleshooting →](appendix-b-troubleshooting.md)

---

## BP_Player Variables

| Variable Name  | Type      | Default Value |
| -------------- | --------- | ------------- |
| `MoveSpeed`    | Float     | 750.0         |
| `BoundsMin`    | Vector 2D | (-850, -450)  |
| `BoundsMax`    | Vector 2D | (850, 450)    |
| `FireInterval` | Float     | 0.08          |
| `FireTimer`    | Float     | 0.0           |
| `BulletSpeed`  | Float     | 2200.0        |
| `MaxLives`     | Integer   | 3             |
| `CurrentLives` | Integer   | 3             |
| `VolleySize`   | Integer   | 3             |
| `VolleySpread` | Float     | 12.0          |
| `SpecialUsed`  | Boolean   | false         |
| `BulletClass`  | Class Ref | BP_Bullet     |

---

## BP_Bullet Variables

| Variable Name       | Type    | Default Value |
| ------------------- | ------- | ------------- |
| `TravelDirection`   | Vector  | (0, 1, 0)     |
| `TravelSpeed`       | Float   | 1200.0        |
| `RemainingLifetime` | Float   | 4.0           |
| `IsEnemyProjectile` | Boolean | false         |
| `Damage`            | Integer | 1             |

---

## BP_Enemy Variables

| Variable Name         | Type      | Default Value |
| --------------------- | --------- | ------------- |
| `MaxHealth`           | Integer   | 12            |
| `CurrentHealth`       | Integer   | 12            |
| `ScoreValue`          | Integer   | 50            |
| `VerticalSpeed`       | Float     | 220.0         |
| `HorizontalAmplitude` | Float     | 250.0         |
| `HorizontalFrequency` | Float     | 1.8           |
| `DespawnY`            | Float     | -750.0        |
| `FireInterval`        | Float     | 0.35          |
| `BulletsPerBurst`     | Integer   | 20            |
| `BurstSpread`         | Float     | 360.0         |
| `EnemyBulletSpeed`    | Float     | 1000.0        |
| `EnemyBulletLifetime` | Float     | 6.0           |
| `BaseX`               | Float     | 0.0           |
| `WaveSeed`            | Float     | 0.0           |
| `FireTimer`           | Float     | 0.0           |
| `BulletClass`         | Class Ref | BP_Bullet     |

---

## BP_EnemySpawner Variables

| Variable Name            | Type        | Default Value        |
| ------------------------ | ----------- | -------------------- |
| `EnemyClass`             | Class Ref   | BP_Enemy             |
| `SpawnAreaHalfWidth`     | Float       | 900.0                |
| `GameDuration`           | Float       | 300.0                |
| `MaxSimultaneousEnemies` | Integer     | 120                  |
| `ElapsedTime`            | Float       | 0.0                  |
| `SpawnTimer`             | Float       | 0.0                  |
| `SpawningActive`         | Boolean     | true                 |
| `SpawnCurve`             | Curve Float | SpawnRateCurve asset |

---

## BP_GameDirector Variables

| Variable Name      | Type       | Default Value    |
| ------------------ | ---------- | ---------------- |
| `PlayerReference`  | Object Ref | (set at runtime) |
| `SpawnerReference` | Object Ref | (set at runtime) |
| `GameDuration`     | Float      | 300.0            |
| `ElapsedTime`      | Float      | 0.0              |
| `GameActive`       | Boolean    | true             |

---

## BP_ScoreManager Variables

| Variable Name    | Type       | Default Value    |
| ---------------- | ---------- | ---------------- |
| `Score`          | Integer    | 0                |
| `CurrentLives`   | Integer    | 3                |
| `HUDWidget`      | Object Ref | (set at runtime) |
| `HUDWidgetClass` | Class Ref  | WBP_HUD          |

---

[← Part 9: Final Setup](part-9-final-setup.md) | [Back to Index](README.md) | [Appendix B: Troubleshooting →](appendix-b-troubleshooting.md)
