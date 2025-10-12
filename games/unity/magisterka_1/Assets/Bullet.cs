using System.Collections.Generic;
using UnityEngine;

public class Bullet : MonoBehaviour
{
    public static readonly List<Bullet> ActiveEnemyProjectiles = new List<Bullet>();

    [SerializeField] private float defaultSpeed = 12f;
    [SerializeField] private float defaultLifetime = 4f;
    [SerializeField] private int defaultDamage = 1;
    [SerializeField] private GameObject impactEffectPrefab;

    private Vector2 travelDirection = Vector2.up;
    private float travelSpeed;
    private float remainingLifetime;
    private bool isEnemyProjectile;
    private int damage;

    private void OnEnable()
    {
        remainingLifetime = Mathf.Max(0.1f, defaultLifetime);
        travelSpeed = Mathf.Max(1f, defaultSpeed);
        damage = Mathf.Max(1, defaultDamage);
    }

    private void Update()
    {
        float step = travelSpeed * Time.deltaTime;
        transform.position += (Vector3)(travelDirection * step);

        remainingLifetime -= Time.deltaTime;
        if (remainingLifetime <= 0f)
        {
            Recycle();
        }
    }

    public void Initialize(Vector2 direction, float speed, bool enemyProjectile, float lifetime, int damageValue = 1)
    {
        travelDirection = direction.sqrMagnitude > 0f ? direction.normalized : Vector2.up;
        travelSpeed = speed > 0f ? speed : defaultSpeed;
        remainingLifetime = lifetime > 0f ? lifetime : defaultLifetime;
        damage = Mathf.Max(1, damageValue);

        if (isEnemyProjectile && !enemyProjectile)
        {
            ActiveEnemyProjectiles.Remove(this);
        }

        isEnemyProjectile = enemyProjectile;

        if (isEnemyProjectile && !ActiveEnemyProjectiles.Contains(this))
        {
            ActiveEnemyProjectiles.Add(this);
        }
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (isEnemyProjectile)
        {
            PlayerController player = collision.GetComponent<PlayerController>();
            if (player != null)
            {
                SpawnImpact();
                player.TakeHit(damage, transform.position);
                Recycle();
            }
        }
        else
        {
            Enemy enemy = collision.GetComponent<Enemy>();
            if (enemy != null)
            {
                SpawnImpact();
                enemy.ApplyDamage(damage);
                Recycle();
            }
        }
    }

    private void SpawnImpact()
    {
        if (impactEffectPrefab != null)
        {
            Instantiate(impactEffectPrefab, transform.position, Quaternion.identity);
        }
    }

    private void OnDestroy()
    {
        if (isEnemyProjectile)
        {
            ActiveEnemyProjectiles.Remove(this);
        }
    }

    private void Recycle()
    {
        if (isEnemyProjectile)
        {
            ActiveEnemyProjectiles.Remove(this);
        }

        Destroy(gameObject);
    }

    public static void ClearEnemyProjectilesWithEffect()
    {
        if (ActiveEnemyProjectiles.Count == 0) return;

        Bullet[] snapshot = ActiveEnemyProjectiles.ToArray();
        ActiveEnemyProjectiles.Clear();

        for (int i = 0; i < snapshot.Length; i++)
        {
            Bullet projectile = snapshot[i];
            if (projectile == null) continue;
            projectile.SpawnImpact();
            Destroy(projectile.gameObject);
        }
    }
}
