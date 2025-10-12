using System.Collections.Generic;
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public static readonly List<Enemy> ActiveEnemies = new List<Enemy>();

    [Header("Durability")]
    [SerializeField] private int maxHealth = 12;
    [SerializeField] private int scoreValue = 50;

    [Header("Movement")]
    [SerializeField] private float verticalSpeed = 2.2f;
    [SerializeField] private float horizontalAmplitude = 2.5f;
    [SerializeField] private float horizontalFrequency = 1.8f;
    [SerializeField] private float despawnY = -7.5f;
    [SerializeField] private float despawnX = 14f;

    [Header("Weaponry")]
    [SerializeField] private Bullet enemyBulletPrefab;
    [SerializeField] private Transform[] muzzlePoints;
    [SerializeField] private float fireInterval = 0.35f;
    [SerializeField] private int bulletsPerBurst = 20;
    [SerializeField] private float burstSpread = 360f;
    [SerializeField] private float enemyBulletSpeed = 10f;
    [SerializeField] private float enemyBulletLifetime = 6f;

    [Header("VFX")]
    [SerializeField] private GameObject hitEffectPrefab;
    [SerializeField] private GameObject deathEffectPrefab;

    private int currentHealth;
    private float baseX;
    private float waveSeed;
    private float fireTimer;
    private bool isDying;

    private void OnEnable()
    {
        currentHealth = Mathf.Max(1, maxHealth);
        baseX = transform.position.x;
        waveSeed = Random.Range(0f, Mathf.PI * 2f);
        fireTimer = Random.Range(0f, fireInterval);
        isDying = false;

        if (!ActiveEnemies.Contains(this))
        {
            ActiveEnemies.Add(this);
        }
    }

    private void OnDisable()
    {
        ActiveEnemies.Remove(this);
    }

    private void Update()
    {
        AdvanceMovement();
        HandleFiring();
        CheckBounds();
    }

    private void AdvanceMovement()
    {
        Vector3 position = transform.position;
        position.y -= verticalSpeed * Time.deltaTime;
        position.x = baseX + Mathf.Sin((Time.time + waveSeed) * horizontalFrequency) * horizontalAmplitude;
        transform.position = position;
    }

    private void HandleFiring()
    {
        if (enemyBulletPrefab == null) return;

        fireTimer -= Time.deltaTime;
        if (fireTimer > 0f) return;

        fireTimer = Mathf.Max(0.05f, fireInterval);

        if (muzzlePoints != null && muzzlePoints.Length > 0)
        {
            for (int i = 0; i < muzzlePoints.Length; i++)
            {
                EmitBurst(muzzlePoints[i].position);
            }
        }
        else
        {
            EmitBurst(transform.position);
        }
    }

    private void EmitBurst(Vector3 worldPosition)
    {
        int count = Mathf.Max(1, bulletsPerBurst);
        float angleStep = burstSpread >= 360f ? 360f / count : burstSpread / Mathf.Max(1, count - 1);
        float startAngle = burstSpread >= 360f ? 0f : -burstSpread * 0.5f;

        for (int i = 0; i < count; i++)
        {
            float degrees = startAngle + i * angleStep;
            Vector2 direction = Quaternion.Euler(0f, 0f, degrees) * Vector2.down;
            Bullet projectile = Instantiate(enemyBulletPrefab, worldPosition, Quaternion.identity);
            projectile.Initialize(direction, enemyBulletSpeed, true, enemyBulletLifetime);
        }
    }

    private void CheckBounds()
    {
        Vector3 position = transform.position;
        if (position.y < despawnY || Mathf.Abs(position.x) > despawnX)
        {
            Destroy(gameObject);
        }
    }

    public void ApplyDamage(int amount)
    {
        currentHealth -= Mathf.Max(1, amount);
        if (hitEffectPrefab != null)
        {
            Instantiate(hitEffectPrefab, transform.position, Quaternion.identity);
        }

        if (currentHealth <= 0 && !isDying)
        {
            HandleDeath();
        }
    }

    private void HandleDeath()
    {
        if (isDying) return;
        isDying = true;

        ScoreManager.Instance?.AddScore(scoreValue);

        if (deathEffectPrefab != null)
        {
            Instantiate(deathEffectPrefab, transform.position, Quaternion.identity);
        }

        Destroy(gameObject);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        PlayerController player = other.GetComponent<PlayerController>();
        if (player == null) return;

        player.TakeHit(1, transform.position);
        HandleDeath();
    }

    public static void DestroyAllEnemies()
    {
        if (ActiveEnemies.Count == 0) return;

        Enemy[] snapshot = ActiveEnemies.ToArray();
        for (int i = 0; i < snapshot.Length; i++)
        {
            Enemy enemy = snapshot[i];
            if (enemy == null) continue;
            enemy.HandleDeath();
        }
    }
}