using System.Collections;
using System.Collections.Generic;
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
    [SerializeField] private float fireRate = 0.12f;
    [SerializeField] private float bulletSpeed = 22f;
    [SerializeField] private float bulletDamage = 14f;
    [SerializeField] private int volleyWidth = 5;

    [Header("Survivability")]
    [SerializeField] private int maxLives = 1;
    [SerializeField] private float respawnDelay = 0.7f;
        [SerializeField] private float invulnerabilityDuration = 2f;

    [Header("Progression")]
    [SerializeField] private int baseLevelThreshold = 1500;

        [Header("Controls")]
        [SerializeField] private KeyCode fireKey = KeyCode.Z;
        [SerializeField] private KeyCode modifierKey = KeyCode.LeftShift;
        [SerializeField] private KeyCode bombKey = KeyCode.X;

    private const int MaxLevel = 12;

    private BulletPool _playerBulletPool;
        private Health _health;
        private SpriteRenderer _renderer;
        private Vector2 _bounds = new Vector2(8f, 4.5f);
        private float _fireCooldown;
        private bool _bombAvailable = true;
        private int _lives;
        private bool _canControl = true;
        private bool _isAlive = true;
        private bool _isInvulnerable;
        private bool _victoryAchieved;
        private Color _baseColor;
        private Coroutine _hitFlashRoutine;
    private Coroutine _levelFlashRoutine;
    private int _level;
    private float _baseBulletSpeed;
    private int _baseVolleyWidth;

        public void Initialize(BulletPool bulletPool, Vector2 movementBounds)
        {
            Instance = this;
            _playerBulletPool = bulletPool;
            _bounds = movementBounds;
            _health = GetComponent<Health>();
            _health.Configure(Faction.Player, 60f);
            _health.Died += HandleDeath;
            _health.Damaged += HandleDamageTaken;

            _renderer = GetComponent<SpriteRenderer>();
            _baseColor = _renderer != null ? _renderer.color : Color.cyan;

            _baseBulletSpeed = bulletSpeed;
            _baseVolleyWidth = volleyWidth;
            _level = 0;

            _lives = Mathf.Max(0, maxLives);
            ScoreManager.Instance?.SetLives(_lives);
            transform.position = new Vector3(0f, -_bounds.y + 1.5f, 0f);
            _isAlive = true;
            _canControl = true;
            _bombAvailable = true;
            _fireCooldown = 0f;
            _victoryAchieved = false;

            if (ScoreManager.Instance != null)
            {
                ScoreManager.Instance.ScoreChanged += HandleScoreChanged;
                HandleScoreChanged(ScoreManager.Instance.CurrentScore);
            }
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
            collider.radius = 1f / 64f;
            collider.isTrigger = true;

            playerGO.AddComponent<Health>();

            var controller = playerGO.AddComponent<PlayerController>();
            controller.Initialize(playerBulletPool, movementBounds);
            return controller;
        }

    public int MaxLives => Mathf.Max(1, maxLives);
    public int CurrentLives => Mathf.Max(0, _lives);

        private void Update()
        {
            if (_victoryAchieved)
            {
                return;
            }

            if (_fireCooldown > 0f)
            {
                _fireCooldown -= Time.deltaTime;
            }

            if (!_canControl)
            {
                return;
            }

            HandleMovement();
            HandleShooting();
            HandleBomb();
        }

        private void HandleMovement()
        {
            if (!_canControl)
            {
                return;
            }

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
            if (!_canControl || !_isAlive)
            {
                return;
            }

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
            var origin = transform.position + Vector3.up * 0.35f;
            float speed = GetLevelAdjustedBulletSpeed();
            int count = Mathf.Clamp(_baseVolleyWidth + Mathf.Max(0, _level), 1, 17);
            float mid = (count - 1) * 0.5f;
            float spreadStep = Mathf.Lerp(5f, 8f, Mathf.Clamp01(_level / 12f));

            for (int i = 0; i < count; i++)
            {
                float offsetIndex = i - mid;
                float spread = offsetIndex * spreadStep;
                var direction = Quaternion.Euler(0f, 0f, spread) * Vector2.up;
                var offset = new Vector3(offsetIndex * 0.18f, 0f, 0f);
                _playerBulletPool.Spawn(origin + offset, direction, speed, bulletDamage);
            }

            foreach (var extra in GetExtraDirectionsForLevel())
            {
                var dir = extra.normalized;
                var spawnPos = transform.position + (Vector3)(dir * 0.4f);
                _playerBulletPool.Spawn(spawnPos, dir, speed, bulletDamage);
            }

            EffectManager.Instance?.SpawnHitEffect(origin + Vector3.up * 0.1f, Faction.Player, 0.4f + _level * 0.05f);
        }

        private void HandleBomb()
        {
            if (!_bombAvailable || !_canControl || !_isAlive)
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
            _canControl = false;
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
            _canControl = true;
        }

        private void HandleDeath(Health _)
        {
            if (!_isAlive)
            {
                return;
            }

            _isAlive = false;
            _canControl = false;
            _bombAvailable = false;
            if (_hitFlashRoutine != null)
            {
                StopCoroutine(_hitFlashRoutine);
                _renderer.color = _baseColor;
                _hitFlashRoutine = null;
            }
            _lives -= 1;
            ScoreManager.Instance?.SetLives(Mathf.Max(0, _lives));
            StartCoroutine(RespawnRoutine());
        }

        private IEnumerator RespawnRoutine()
        {
            EffectManager.Instance?.SpawnExplosion(transform.position, Faction.Player, 4f);
            _renderer.enabled = false;
            _isInvulnerable = true;

            if (_lives < 0)
            {
                yield return new WaitForSeconds(1f);
                ScoreManager.Instance?.ShowGameOver();
                EnemySpawner.Instance?.StopAndClear();
                GameDirector.Instance?.OnPlayerGameOver();
                gameObject.SetActive(false);
                yield break;
            }

            yield return new WaitForSeconds(respawnDelay);
            EnemySpawner.Instance?.ClearScreen();
            transform.position = new Vector3(0f, -_bounds.y + 1.5f, 0f);
            _renderer.enabled = true;
            _health.RestoreFull();
            _fireCooldown = fireRate;
            _canControl = true;

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
            _renderer.color = _baseColor;
            _isAlive = true;
            _canControl = true;
        }

        private void OnDestroy()
        {
            if (_health != null)
            {
                _health.Died -= HandleDeath;
                _health.Damaged -= HandleDamageTaken;
            }

            if (ScoreManager.Instance != null)
            {
                ScoreManager.Instance.ScoreChanged -= HandleScoreChanged;
            }

            if (Instance == this)
            {
                Instance = null;
            }
        }

        public bool IsInvulnerable() => _isInvulnerable;

        public void ApplyDamage(float value)
        {
            if (_isInvulnerable || !_isAlive || _victoryAchieved)
            {
                return;
            }

            _health.ApplyDamage(value, transform.position);
        }

        public void HandleVictory()
        {
            _victoryAchieved = true;
            _canControl = false;
            _isInvulnerable = true;
            if (_renderer != null)
            {
                _renderer.color = Color.white;
            }
        }

        private void HandleDamageTaken(float damage, Vector2 hitPoint)
        {
            if (_renderer == null || _isInvulnerable || !_isAlive)
            {
                return;
            }

            if (_hitFlashRoutine != null)
            {
                StopCoroutine(_hitFlashRoutine);
                _renderer.color = _baseColor;
            }

            _hitFlashRoutine = StartCoroutine(HitFlashRoutine());
            float strength = Mathf.Clamp01(damage / Mathf.Max(1f, _health.MaxHealth * 0.4f));
            ScoreManager.Instance?.TriggerDamageFlash(strength);
            EffectManager.Instance?.ShakeCamera(0.22f, 0.65f);
        }

        private IEnumerator HitFlashRoutine()
        {
            const float duration = 0.35f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime;
                float t = Mathf.PingPong(elapsed * 18f, 1f);
                _renderer.color = Color.Lerp(_baseColor, Color.white, t);
                yield return null;
            }

            _renderer.color = _baseColor;
            _hitFlashRoutine = null;
        }

        private float GetLevelAdjustedBulletSpeed()
        {
            return _baseBulletSpeed;
        }

        private IEnumerable<Vector2> GetExtraDirectionsForLevel()
        {
            if (_level <= 0)
            {
                yield break;
            }

            if (_level >= 2)
            {
                yield return Vector2.left;
                yield return Vector2.right;
            }

            if (_level >= 4)
            {
                yield return (Vector2.left + Vector2.up).normalized;
                yield return (Vector2.right + Vector2.up).normalized;
            }

            if (_level >= 6)
            {
                yield return Vector2.down;
            }

            if (_level >= 8)
            {
                yield return (Vector2.left + Vector2.down * 0.7f).normalized;
                yield return (Vector2.right + Vector2.down * 0.7f).normalized;
            }
        }

        private void HandleScoreChanged(int score)
        {
            int newLevel = CalculateLevelFromScore(score);

            if (newLevel > _level)
            {
                for (int next = _level + 1; next <= newLevel; next++)
                {
                    _level = next;
                    HandleLevelUpFeedback();
                }
            }
            else if (newLevel < _level)
            {
                _level = newLevel;
            }
        }

        private int CalculateLevelFromScore(int score)
        {
            if (baseLevelThreshold <= 0)
            {
                return 0;
            }

            int level = 0;
            int increment = baseLevelThreshold;
            int threshold = baseLevelThreshold;

            while (level < MaxLevel && score >= threshold)
            {
                level++;
                increment *= 2;
                threshold += increment;
            }

            return level;
        }

        private void HandleLevelUpFeedback()
        {
            EffectManager.Instance?.SpawnExplosion(transform.position, Faction.Player, 2f + _level * 0.2f);
            EffectManager.Instance?.ShakeCamera(0.18f, 0.4f + _level * 0.05f);

            if (_hitFlashRoutine != null)
            {
                StopCoroutine(_hitFlashRoutine);
                _hitFlashRoutine = null;
            }

            if (_renderer != null)
            {
                _renderer.color = _baseColor;
            }

            if (_levelFlashRoutine != null)
            {
                StopCoroutine(_levelFlashRoutine);
            }

            _levelFlashRoutine = StartCoroutine(LevelUpFlashRoutine());
        }

        private IEnumerator LevelUpFlashRoutine()
        {
            float duration = 0.6f;
            float elapsed = 0f;
            var glowColor = Color.Lerp(_baseColor, new Color(1f, 0.95f, 0.35f, 1f), 0.85f);

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime;
                float t = Mathf.PingPong(elapsed * 6f, 1f);
                if (_renderer != null)
                {
                    _renderer.color = Color.Lerp(glowColor, _baseColor, t);
                }

                yield return null;
            }

            if (_renderer != null)
            {
                _renderer.color = _baseColor;
            }

            _levelFlashRoutine = null;
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
