using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 7.5f;
    [SerializeField] private Vector2 boundsMin = new Vector2(-8.5f, -4.5f);
    [SerializeField] private Vector2 boundsMax = new Vector2(8.5f, 4.5f);

    [Header("Primary Fire")]
    [SerializeField] private Bullet playerBulletPrefab;
    [SerializeField] private Transform[] firePoints;
    [SerializeField, Range(0.02f, 0.5f)] private float fireInterval = 0.08f;
    [SerializeField, Range(1, 9)] private int volleySize = 3;
    [SerializeField, Range(0f, 45f)] private float volleySpread = 12f;
    [SerializeField] private float playerBulletSpeed = 22f;
    [SerializeField] private float playerBulletLifetime = 3f;
    [SerializeField] private bool allowMouseFire = true;

    [Header("Special Ability")]
    [SerializeField] private KeyCode specialKey = KeyCode.X;
    [SerializeField] private GameObject specialEffectPrefab;

    [Header("Durability")]
    [SerializeField] private int maxLives = 3;
    [SerializeField] private GameObject hitEffectPrefab;
    [SerializeField] private GameObject deathEffectPrefab;

    private float fireTimer;
    private int currentLives;
    private bool specialUsed;

    public int MaxLives => maxLives;
    public int CurrentLives => currentLives;

    private void Awake()
    {
        currentLives = Mathf.Max(1, maxLives);
    }

    private void Update()
    {
        HandleMovement();
        HandlePrimaryFire();
        HandleSpecial();
    }

    private void HandleMovement()
    {
        Vector2 input = new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical"));
        Vector3 velocity = input.normalized * moveSpeed * Time.deltaTime;
        Vector3 candidate = transform.position + velocity;
        candidate.x = Mathf.Clamp(candidate.x, boundsMin.x, boundsMax.x);
        candidate.y = Mathf.Clamp(candidate.y, boundsMin.y, boundsMax.y);
        transform.position = candidate;
    }

    private void HandlePrimaryFire()
    {
        bool wantsToFire = Input.GetKey(KeyCode.Z) || (allowMouseFire && Input.GetMouseButton(0));
        if (!wantsToFire || playerBulletPrefab == null || firePoints == null || firePoints.Length == 0)
        {
            fireTimer = Mathf.Max(0f, fireTimer - Time.deltaTime);
            return;
        }

        fireTimer -= Time.deltaTime;
        if (fireTimer > 0f) return;

        fireTimer = Mathf.Max(0.02f, fireInterval);
        foreach (Transform firePoint in firePoints)
        {
            EmitVolleyFrom(firePoint.position);
        }
    }

    private void EmitVolleyFrom(Vector3 origin)
    {
        int burstCount = Mathf.Max(1, volleySize);
        if (burstCount == 1)
        {
            SpawnPlayerBullet(origin, Vector2.up);
            return;
        }

        float spreadTotal = volleySpread * (burstCount - 1);
        float startAngle = -spreadTotal * 0.5f;
        for (int i = 0; i < burstCount; i++)
        {
            float angle = startAngle + i * volleySpread;
            Vector2 direction = Quaternion.Euler(0f, 0f, angle) * Vector2.up;
            SpawnPlayerBullet(origin, direction.normalized);
        }
    }

    private void SpawnPlayerBullet(Vector3 position, Vector2 direction)
    {
        Bullet bulletInstance = Instantiate(playerBulletPrefab, position, Quaternion.identity);
        bulletInstance.Initialize(direction, playerBulletSpeed, false, playerBulletLifetime);
    }

    private void HandleSpecial()
    {
        if (specialUsed) return;

        bool activated = Input.GetKeyDown(specialKey) || Input.GetMouseButtonDown(1);
        if (!activated) return;

        specialUsed = true;
        if (specialEffectPrefab != null)
        {
            Instantiate(specialEffectPrefab, transform.position, Quaternion.identity);
        }

        Bullet.ClearEnemyProjectilesWithEffect();
        Enemy.DestroyAllEnemies();
        ScoreManager.Instance?.RegisterBombUse();
    }

    public void TakeHit(int damage, Vector3 hitWorldPosition)
    {
        currentLives -= Mathf.Max(1, damage);
        currentLives = Mathf.Max(0, currentLives);

        if (hitEffectPrefab != null)
        {
            Instantiate(hitEffectPrefab, hitWorldPosition, Quaternion.identity);
        }

        ScoreManager.Instance?.SetLives(currentLives);

        if (currentLives <= 0)
        {
            HandleDeath();
        }
    }

    private void OnEnable()
    {
        ScoreManager.Instance?.SetLives(currentLives);
    }

    private void HandleDeath()
    {
        if (deathEffectPrefab != null)
        {
            Instantiate(deathEffectPrefab, transform.position, Quaternion.identity);
        }

        gameObject.SetActive(false);
        GameDirector.Instance?.HandlePlayerDeath();
    }
}