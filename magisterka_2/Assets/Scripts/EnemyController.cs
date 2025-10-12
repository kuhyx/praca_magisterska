using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Controls enemy motion, firing patterns, and death rewards.
    /// </summary>
    [RequireComponent(typeof(Health))]
    public class EnemyController : MonoBehaviour
    {
    [SerializeField] private float despawnPadding = 2f;

        private EnemySpawner _spawner;
        private BulletPool _bulletPool;
        private PlayerController _player;
        private EnemyBlueprint _config;
        private Health _health;
        private float _difficulty;
        private float _moveTime;
        private float _phaseSeed;
        private float _fireTimer;
    private float _baseX;
    private Vector2 _worldBounds;

        public void Initialize(EnemySpawner spawner, BulletPool bulletPool, PlayerController player, EnemyBlueprint blueprint, float difficultyScale, Vector2 worldBounds)
        {
            _spawner = spawner;
            _bulletPool = bulletPool;
            _player = player;
            _config = blueprint;
            _difficulty = difficultyScale;
            _health = GetComponent<Health>();
            _worldBounds = worldBounds;
            _health.Configure(Faction.Enemy, blueprint.Health + difficultyScale * 12f);
            _health.Died += HandleDeath;

            var collider = GetComponent<CircleCollider2D>();
            if (collider != null)
            {
                collider.radius = 0.4f * blueprint.Scale;
            }

            _phaseSeed = Random.Range(0f, Mathf.PI * 2f);
            _baseX = transform.position.x;
            _moveTime = 0f;
            _fireTimer = GetFireDelay(true);
        }

        private void Update()
        {
            AdvanceMovement();
            HandleFiring();

            float bottomLimit = -_worldBounds.y - despawnPadding;
            if (transform.position.y < bottomLimit)
            {
                _spawner?.DespawnEnemy(this);
            }
        }

        private void AdvanceMovement()
        {
            _moveTime += Time.deltaTime;
            var pos = transform.position;
            float speed = _config.MoveSpeed + _difficulty * 0.2f;

            switch (_config.Movement)
            {
                case EnemyMovementStyle.ZigZag:
                    pos += Vector3.down * (speed * Time.deltaTime);
                    pos.x += Mathf.Sin((_moveTime + _phaseSeed) * (1.4f + _config.HorizontalFrequency)) * (_config.HorizontalAmplitude * Time.deltaTime);
                    break;
                case EnemyMovementStyle.Straight:
                    pos += Vector3.down * (speed * Time.deltaTime);
                    break;
                case EnemyMovementStyle.Sine:
                    pos += Vector3.down * (speed * Time.deltaTime);
                    pos.x = _baseX + Mathf.Sin((_moveTime + _phaseSeed) * (1f + _config.HorizontalFrequency)) * _config.HorizontalAmplitude;
                    break;
                case EnemyMovementStyle.Orbit:
                    float orbitSpeed = _config.HorizontalFrequency + 0.8f + _difficulty * 0.05f;
                    pos += Vector3.down * (speed * 0.6f * Time.deltaTime);
                    pos.x = _baseX + Mathf.Cos((_moveTime + _phaseSeed) * orbitSpeed) * _config.OrbitRadius;
                    pos.y += Mathf.Sin((_moveTime + _phaseSeed) * orbitSpeed) * (_config.OrbitRadius * 0.25f) * Time.deltaTime;
                    break;
            }

            if (_config.CenteringBias > 0f)
            {
                float lerpFactor = Mathf.Clamp01(_config.CenteringBias * Time.deltaTime);
                pos.x = Mathf.Lerp(pos.x, 0f, lerpFactor);
            }

            ClampWithinBounds(ref pos);
            transform.position = pos;
        }

        private void HandleFiring()
        {
            if (_config.Fire == EnemyFireStyle.None)
            {
                return;
            }

            _fireTimer -= Time.deltaTime;
            if (_fireTimer > 0f)
            {
                return;
            }

            FirePattern();
            _fireTimer = GetFireDelay(false);
        }

        private void FirePattern()
        {
            switch (_config.Fire)
            {
                case EnemyFireStyle.Radial:
                    FireRadial();
                    break;
                case EnemyFireStyle.Stream:
                    FireStream();
                    break;
                case EnemyFireStyle.Burst:
                    FireBurst();
                    break;
            }
        }

        private void FireRadial()
        {
            int bullets = Mathf.Clamp(_config.BulletsPerVolley + Mathf.RoundToInt(_difficulty), 6, 24);
            float angleStep = 360f / bullets;
            float offset = (_moveTime + _phaseSeed) * 60f;

            for (int i = 0; i < bullets; i++)
            {
                float angle = (angleStep * i + offset) * Mathf.Deg2Rad;
                var dir = new Vector2(Mathf.Cos(angle), Mathf.Sin(angle));
                _bulletPool.Spawn(transform.position, dir, _config.BulletSpeed * 0.2f, _config.BulletDamage);
            }
        }

        private void FireStream()
        {
            var forward = Vector2.down;
            int count = Mathf.Clamp(_config.BulletsPerVolley, 2, 6);

            for (int i = 0; i < count; i++)
            {
                float spread = (i - (count - 1) * 0.5f) * 7f;
                var dir = Quaternion.Euler(0f, 0f, spread) * forward;
                _bulletPool.Spawn(transform.position, dir, _config.BulletSpeed * 0.2f, _config.BulletDamage);
            }

            if (_player != null && _player.isActiveAndEnabled)
            {
                var toPlayer = ((Vector2)_player.transform.position - (Vector2)transform.position).normalized;
                _bulletPool.Spawn(transform.position, toPlayer, _config.BulletSpeed * 0.22f, _config.BulletDamage);
            }
        }

        private void FireBurst()
        {
            int volleys = Mathf.Clamp(_config.BulletsPerVolley, 1, 3);
            var baseDir = Vector2.down;

            for (int v = 0; v < volleys; v++)
            {
                float spread = 12f + v * 4f;
                for (int i = -1; i <= 1; i++)
                {
                    var dir = Quaternion.Euler(0f, 0f, i * spread) * baseDir;
                    _bulletPool.Spawn(transform.position, dir, _config.BulletSpeed * (0.18f + v * 0.02f), _config.BulletDamage);
                }
            }
        }

        private float GetFireDelay(bool first)
        {
            if (_config.Fire == EnemyFireStyle.None)
            {
                return float.MaxValue;
            }

            float baseDelay = Mathf.Max(0.3f, _config.FireInterval - _difficulty * 0.04f);
            return first ? Random.Range(0.2f, baseDelay) : baseDelay;
        }

        private void HandleDeath(Health _)
        {
            EffectManager.Instance?.SpawnExplosion(transform.position, Faction.Enemy, 2.6f + _difficulty * 0.2f);
            ScoreManager.Instance?.AddScore(_config.Score + Mathf.RoundToInt(_difficulty * 20f));
            _spawner?.NotifyEnemyKilled(this);
            Destroy(gameObject);
        }

        private void OnTriggerEnter2D(Collider2D other)
        {
            if (!other.TryGetComponent(out PlayerController player))
            {
                return;
            }

            player.ApplyDamage(Mathf.Max(10f, _config.ContactDamage));
            EffectManager.Instance?.SpawnHitEffect(player.transform.position, Faction.Player, 0.9f);
            _health?.Kill();
        }

        private void OnDestroy()
        {
            if (_health != null)
            {
                _health.Died -= HandleDeath;
            }
        }

        private void ClampWithinBounds(ref Vector3 position)
        {
            if (_worldBounds == Vector2.zero)
            {
                return;
            }

            position.x = Mathf.Clamp(position.x, -_worldBounds.x + 0.6f, _worldBounds.x - 0.6f);
            float upperLimit = _worldBounds.y + 4f;
            position.y = Mathf.Min(position.y, upperLimit);
        }
    }
}
