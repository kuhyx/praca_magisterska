using System.Collections;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Controls enemy motion, firing patterns, and death rewards.
    /// </summary>
    [RequireComponent(typeof(Health))]
    public class EnemyController : MonoBehaviour
    {
        [SerializeField] private float moveSpeed = 3f;
        [SerializeField] private float bulletSpeed = 12f;
        [SerializeField] private float bulletDamage = 8f;
        [SerializeField] private float fireInterval = 0.6f;
        [SerializeField] private int scoreValue = 100;

        private EnemySpawner _spawner;
    private BulletPool _bulletPool;
    private PlayerController _player;
        private Health _health;
        private float _phaseSeed;
        private float _zigzagWidth = 2.8f;
        private float _difficulty;
        private Coroutine _fireRoutine;

        public void Initialize(EnemySpawner spawner, BulletPool bulletPool, PlayerController player, float difficultyScale, float healthValue)
        {
            _spawner = spawner;
            _bulletPool = bulletPool;
            _player = player;
            _difficulty = difficultyScale;
            _health = GetComponent<Health>();
            _health.Configure(Faction.Enemy, healthValue);
            _health.Died += HandleDeath;
            _phaseSeed = Random.Range(0f, 360f);

            moveSpeed += difficultyScale * 0.8f;
            fireInterval = Mathf.Max(0.22f, fireInterval - difficultyScale * 0.08f);
            bulletSpeed += difficultyScale * 1.4f;
            bulletDamage += difficultyScale * 0.6f;
            scoreValue += Mathf.RoundToInt(40f * difficultyScale);

            if (_fireRoutine != null)
            {
                StopCoroutine(_fireRoutine);
            }

            _fireRoutine = StartCoroutine(FireRoutine());
        }

        private void Update()
        {
            var pos = transform.position;
            pos += Vector3.down * (moveSpeed * Time.deltaTime);
            pos.x += Mathf.Sin(Time.time * (2f + _difficulty) + _phaseSeed) * (_zigzagWidth * Time.deltaTime);
            transform.position = pos;

            if (transform.position.y < -12f)
            {
                _spawner?.DespawnEnemy(this);
            }
        }

        private IEnumerator FireRoutine()
        {
            yield return new WaitForSeconds(Random.Range(0.15f, fireInterval));

            while (true)
            {
                FirePattern();
                yield return new WaitForSeconds(fireInterval);
            }
        }

        private void FirePattern()
        {
            int radialBullets = Mathf.Clamp(Mathf.RoundToInt(16 + _difficulty * 14f), 12, 48);
            float angleStep = 360f / radialBullets;
            float angleOffset = Time.time * 60f + _phaseSeed;

            for (int i = 0; i < radialBullets; i++)
            {
                float angle = (angleStep * i + angleOffset) * Mathf.Deg2Rad;
                var dir = new Vector2(Mathf.Cos(angle), Mathf.Sin(angle));
                _bulletPool.Spawn(transform.position, dir, bulletSpeed, bulletDamage);
            }

            // Additional forward stream for dense barrages.
            var forward = Vector2.down;
            for (int i = -2; i <= 2; i++)
            {
                var spreadDir = Quaternion.Euler(0f, 0f, i * 8f) * forward;
                _bulletPool.Spawn(transform.position, spreadDir, bulletSpeed * 1.2f, bulletDamage * 0.8f);
            }

            if (_player != null && _player.isActiveAndEnabled)
            {
                var toPlayer = ((Vector2)_player.transform.position - (Vector2)transform.position).normalized;
                int aimedShots = Mathf.Clamp(3 + Mathf.RoundToInt(_difficulty), 3, 8);
                for (int i = 0; i < aimedShots; i++)
                {
                    float sway = (i - (aimedShots - 1) * 0.5f) * 4f;
                    var dir = Quaternion.Euler(0f, 0f, sway) * toPlayer;
                    _bulletPool.Spawn(transform.position, dir, bulletSpeed * 1.4f, bulletDamage * 0.9f);
                }
            }
        }

        private void HandleDeath(Health _)
        {
            EffectManager.Instance?.SpawnExplosion(transform.position, Faction.Enemy, 3f + _difficulty);
            ScoreManager.Instance?.AddScore(scoreValue);
            _spawner?.NotifyEnemyKilled(this);
            Destroy(gameObject);
        }

        private void OnDestroy()
        {
            if (_health != null)
            {
                _health.Died -= HandleDeath;
            }
        }
    }
}
