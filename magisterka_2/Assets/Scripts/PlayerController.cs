using System.Collections;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Handles user input, shooting, screen-clearing bomb, and respawn logic.
    /// </summary>
    [RequireComponent(typeof(Health))]
    public class PlayerController : MonoBehaviour
    {
        public static PlayerController Instance { get; private set; }

        [Header("Movement")]
        [SerializeField] private float moveSpeed = 12f;
        [SerializeField] private float focusSpeedMultiplier = 0.6f;

        [Header("Offense")]
        [SerializeField] private float fireRate = 0.08f;
        [SerializeField] private float bulletSpeed = 26f;
        [SerializeField] private float bulletDamage = 16f;
        [SerializeField] private int volleyWidth = 6;

        [Header("Survivability")]
        [SerializeField] private int maxLives = 5;
        [SerializeField] private float respawnDelay = 1.4f;
        [SerializeField] private float invulnerabilityDuration = 2f;

        [Header("Controls")]
        [SerializeField] private KeyCode fireKey = KeyCode.Z;
        [SerializeField] private KeyCode modifierKey = KeyCode.LeftShift;
        [SerializeField] private KeyCode bombKey = KeyCode.X;

        private BulletPool _playerBulletPool;
        private Health _health;
        private SpriteRenderer _renderer;
        private Vector2 _bounds = new Vector2(8f, 4.5f);
        private float _fireCooldown;
        private bool _bombAvailable = true;
        private int _remainingLives;
        private bool _isInvulnerable;
        private Color _baseColor;

        public void Initialize(BulletPool bulletPool, Vector2 movementBounds)
        {
            Instance = this;
            _playerBulletPool = bulletPool;
            _bounds = movementBounds;
            _health = GetComponent<Health>();
            _health.Configure(Faction.Player, 60f);
            _health.Died += HandleDeath;

            _renderer = GetComponent<SpriteRenderer>();
            _baseColor = _renderer != null ? _renderer.color : Color.cyan;

            _remainingLives = Mathf.Max(0, maxLives - 1);
            transform.position = new Vector3(0f, -_bounds.y + 1.5f, 0f);
        }

        public static PlayerController CreatePlayer(Transform parent, BulletPool playerBulletPool, Vector2 movementBounds)
        {
            var playerGO = new GameObject("Player");
            playerGO.transform.SetParent(parent, false);

            var renderer = playerGO.AddComponent<SpriteRenderer>();
            renderer.sprite = BuildPlayerSprite();
            renderer.sortingOrder = 20;
            renderer.color = new Color(0.25f, 0.85f, 1f, 1f);

            var collider = playerGO.AddComponent<CircleCollider2D>();
            collider.radius = 0.55f;
            collider.isTrigger = true;

            var health = playerGO.AddComponent<Health>();

            var controller = playerGO.AddComponent<PlayerController>();
            controller.Initialize(playerBulletPool, movementBounds);
            return controller;
        }

        private void Update()
        {
            HandleMovement();
            HandleShooting();
            HandleBomb();

            if (_fireCooldown > 0f)
            {
                _fireCooldown -= Time.deltaTime;
            }
        }

        private void HandleMovement()
        {
            float x = 0f;
            float y = 0f;

            if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow)) x -= 1f;
            if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow)) x += 1f;
            if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow)) y += 1f;
            if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow)) y -= 1f;

            var direction = new Vector2(x, y).normalized;
            float speed = moveSpeed * (Input.GetKey(modifierKey) ? focusSpeedMultiplier : 1f);
            var delta = direction * (speed * Time.deltaTime);
            var next = transform.position + (Vector3)delta;
            next.x = Mathf.Clamp(next.x, -_bounds.x + 0.5f, _bounds.x - 0.5f);
            next.y = Mathf.Clamp(next.y, -_bounds.y + 0.5f, _bounds.y - 0.5f);
            transform.position = next;
        }

        private void HandleShooting()
        {
            bool wantsFire = Input.GetKey(fireKey) || Input.GetMouseButton(0);
            if (!wantsFire || _fireCooldown > 0f)
            {
                return;
            }

            FireVolley();
            _fireCooldown = fireRate;
        }

        private void FireVolley()
        {
            var origin = transform.position + Vector3.up * 0.4f;
            int half = volleyWidth / 2;

            for (int i = -half; i <= half; i++)
            {
                float spread = i * 6f;
                var direction = Quaternion.Euler(0f, 0f, spread) * Vector2.up;
                var offset = direction * 0.25f * Mathf.Abs(i);
                _playerBulletPool.Spawn(origin + (Vector3)offset, direction, bulletSpeed, bulletDamage);
            }

            EffectManager.Instance?.SpawnHitEffect(origin + Vector3.up * 0.2f, Faction.Player, 0.6f);
        }

        private void HandleBomb()
        {
            if (!_bombAvailable)
            {
                return;
            }

            bool trigger = Input.GetKeyDown(bombKey) || Input.GetKeyDown(KeyCode.Space) || Input.GetMouseButtonDown(1);
            if (!trigger)
            {
                return;
            }

            _bombAvailable = false;
            StartCoroutine(PerformBomb());
        }

        private IEnumerator PerformBomb()
        {
            _isInvulnerable = true;
            _renderer.color = Color.white;
            EffectManager.Instance?.SpawnScreenClear(transform.position, 18f);
            EnemySpawner.Instance?.ClearScreen();

            // Hyper dash upwards and back for dramatic flair.
            Vector3 start = transform.position;
            Vector3 apex = new Vector3(0f, Mathf.Min(_bounds.y - 0.6f, start.y + 4.5f), 0f);
            float travel = 0.4f;
            float elapsed = 0f;

            while (elapsed < travel)
            {
                elapsed += Time.deltaTime;
                float t = elapsed / travel;
                transform.position = Vector3.Lerp(start, apex, t);
                yield return null;
            }

            elapsed = 0f;
            while (elapsed < travel)
            {
                elapsed += Time.deltaTime;
                float t = elapsed / travel;
                transform.position = Vector3.Lerp(apex, start, t);
                yield return null;
            }

            _isInvulnerable = false;
            _renderer.color = _baseColor;
        }

        private void HandleDeath(Health _)
        {
            StartCoroutine(RespawnRoutine());
        }

        private IEnumerator RespawnRoutine()
        {
            EffectManager.Instance?.SpawnExplosion(transform.position, Faction.Player, 4f);
            _renderer.enabled = false;
            _isInvulnerable = true;

            if (_remainingLives < 0)
            {
                gameObject.SetActive(false);
                yield break;
            }

            yield return new WaitForSeconds(respawnDelay);
            transform.position = new Vector3(0f, -_bounds.y + 1.5f, 0f);
            _renderer.enabled = true;
            _health.RestoreFull();

            float timer = invulnerabilityDuration;
            while (timer > 0f)
            {
                timer -= Time.deltaTime;
                float pulse = Mathf.PingPong(Time.time * 10f, 1f);
                if (_renderer != null)
                {
                    _renderer.color = Color.Lerp(_baseColor, Color.white, pulse);
                }

                yield return null;
            }

            if (_renderer != null)
            {
                _renderer.color = _baseColor;
            }

            _isInvulnerable = false;
            _remainingLives--;
        }

        private void OnDestroy()
        {
            if (_health != null)
            {
                _health.Died -= HandleDeath;
            }

            if (Instance == this)
            {
                Instance = null;
            }
        }

        public bool IsInvulnerable() => _isInvulnerable;

        public void ApplyDamage(float value)
        {
            if (_isInvulnerable)
            {
                return;
            }

            _health.ApplyDamage(value, transform.position);
        }

        private static Sprite BuildPlayerSprite()
        {
            const int size = 64;
            var texture = new Texture2D(size, size, TextureFormat.RGBA32, false)
            {
                filterMode = FilterMode.Point
            };

            var center = new Vector2(size / 2f, size / 5f * 4f);
            var pixels = new Color[size * size];
            var body = new Color(0.2f, 0.8f, 1f, 1f);

            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    int index = x + y * size;
                    float dist = Vector2.Distance(center, new Vector2(x, y * 0.9f));
                    pixels[index] = dist < size * 0.35f ? body : new Color(0f, 0f, 0f, 0f);
                }
            }

            texture.SetPixels(pixels);
            texture.Apply();

            return Sprite.Create(texture, new Rect(0, 0, size, size), new Vector2(0.5f, 0.2f), 64f);
        }
    }
}
