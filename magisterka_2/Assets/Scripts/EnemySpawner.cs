using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Spawns continuously escalating enemy waves for roughly five minutes.
    /// </summary>
    public class EnemySpawner : MonoBehaviour
    {
        public static EnemySpawner Instance { get; private set; }

        [SerializeField] private float totalDuration = 300f;
        [SerializeField] private float spawnDelayStart = 1.2f;
        [SerializeField] private float spawnDelayEnd = 0.18f;
        [SerializeField] private float spawnHeight = 10f;
        [SerializeField] private float horizontalPadding = 1.2f;

        private readonly List<EnemyController> _liveEnemies = new List<EnemyController>();

        private BulletPool _enemyBulletPool;
        private Camera _camera;
        private Sprite _enemySprite;
        private float _elapsed;
        private Vector2 _worldBounds;

        private PlayerController _player;

        public void Initialize(Camera camera, BulletPool enemyPool, PlayerController player, Vector2 worldBounds)
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;

            _camera = camera;
            _enemyBulletPool = enemyPool;
            _player = player;
            _worldBounds = worldBounds;
            _enemySprite = BuildEnemySprite();

            StartCoroutine(SpawnRoutine());
        }

        public void NotifyEnemyKilled(EnemyController enemy)
        {
            _liveEnemies.Remove(enemy);
        }

        public void DespawnEnemy(EnemyController enemy)
        {
            if (enemy == null)
            {
                return;
            }

            _liveEnemies.Remove(enemy);
            Destroy(enemy.gameObject);
        }

        public void ClearScreen()
        {
            foreach (var enemy in _liveEnemies.ToArray())
            {
                if (enemy != null && enemy.TryGetComponent(out Health health))
                {
                    health.Kill();
                }
            }

            _enemyBulletPool?.ClearLiveBullets();
        }

        private IEnumerator SpawnRoutine()
        {
            yield return new WaitForSeconds(1.5f);

            while (_elapsed < totalDuration)
            {
                SpawnWave();

                float progress = Mathf.Clamp01(_elapsed / totalDuration);
                float delay = Mathf.Lerp(spawnDelayStart, spawnDelayEnd, progress);
                delay = Mathf.Max(0.08f, delay);
                yield return new WaitForSeconds(delay);
                _elapsed += delay;
            }
        }

        private void SpawnWave()
        {
            int targetCount = Mathf.Clamp(Mathf.RoundToInt(3 + _elapsed * 0.12f), 4, 18);
            float difficulty = Mathf.Clamp01(_elapsed / totalDuration) * 8f;

            for (int i = 0; i < targetCount; i++)
            {
                Vector2 spawnPos = PickSpawnPosition(i, targetCount);
                SpawnEnemy(spawnPos, difficulty);
            }
        }

        private Vector2 PickSpawnPosition(int index, int total)
        {
            float camWidth = _worldBounds.x;
            float step = (camWidth * 2f - horizontalPadding * 2f) / Mathf.Max(1, total - 1);
            float x = -camWidth + horizontalPadding + step * index + Random.Range(-0.6f, 0.6f);
            float y = _camera.orthographicSize + spawnHeight;
            return new Vector2(x, y);
        }

        private void SpawnEnemy(Vector2 position, float difficulty)
        {
            var enemyGO = new GameObject("Enemy");
            enemyGO.transform.SetParent(transform, false);
            enemyGO.transform.position = position;
            enemyGO.transform.localScale = Vector3.one * 1.6f;

            var renderer = enemyGO.AddComponent<SpriteRenderer>();
            renderer.sprite = _enemySprite;
            renderer.sortingOrder = 10;
            renderer.color = Color.Lerp(new Color(1f, 0.6f, 0.3f, 1f), new Color(1f, 0.1f, 0.2f, 1f), Mathf.Clamp01(difficulty / 8f));

            var collider = enemyGO.AddComponent<CircleCollider2D>();
            collider.isTrigger = true;
            collider.radius = 0.7f;

            var health = enemyGO.AddComponent<Health>();

            var controller = enemyGO.AddComponent<EnemyController>();
            controller.Initialize(this, _enemyBulletPool, _player, difficulty, 30f + difficulty * 20f);

            _liveEnemies.Add(controller);
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                Instance = null;
            }
        }

        private Sprite BuildEnemySprite()
        {
            const int size = 64;
            var texture = new Texture2D(size, size, TextureFormat.RGBA32, false)
            {
                filterMode = FilterMode.Point
            };

            var center = new Vector2(size / 2f, size / 2f);
            var pixels = new Color[size * size];
            var body = new Color(1f, 0.35f, 0.35f, 1f);

            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    int index = x + y * size;
                    float dist = Vector2.Distance(center, new Vector2(x, y));
                    float threshold = size * 0.35f + Mathf.Sin(y * 0.2f) * 2f;
                    pixels[index] = dist <= threshold ? body : new Color(0f, 0f, 0f, 0f);
                }
            }

            texture.SetPixels(pixels);
            texture.Apply();

            return Sprite.Create(texture, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 64f);
        }
    }
}
