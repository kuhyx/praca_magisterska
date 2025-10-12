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

        public float TotalDuration => totalDuration;
        public bool HasActiveEnemies => _liveEnemies.Count > 0;

    [SerializeField] private float totalDuration = 90f;
        [SerializeField] private float spawnDelayStart = 1.6f;
        [SerializeField] private float spawnDelayEnd = 0.45f;
    [SerializeField] private float spawnInset = 0.3f;
        [SerializeField] private float horizontalPadding = 1.2f;

        private readonly List<EnemyController> _liveEnemies = new List<EnemyController>();

        private BulletPool _enemyBulletPool;
        private Camera _camera;
        private PlayerController _player;
        private Vector2 _worldBounds;
        private EnemyBlueprint[] _blueprints;
    private Coroutine _spawnRoutine;
    private float _elapsed;
    private bool _spawningActive;
    private int _introIndex;

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
            _blueprints = BuildBlueprints();

            _spawningActive = true;
            _elapsed = 0f;
            _introIndex = 0;
            _spawnRoutine = StartCoroutine(SpawnRoutine());
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
            for (int i = _liveEnemies.Count - 1; i >= 0; i--)
            {
                var enemy = _liveEnemies[i];
                if (enemy != null && enemy.TryGetComponent(out Health health))
                {
                    health.Kill();
                }
            }

            _enemyBulletPool?.ClearLiveBullets();
        }

        public void StopSpawning()
        {
            _spawningActive = false;

            if (_spawnRoutine != null)
            {
                StopCoroutine(_spawnRoutine);
                _spawnRoutine = null;
            }
        }

        public void StopAndClear()
        {
            StopSpawning();
            ClearScreen();
        }

        private IEnumerator SpawnRoutine()
        {
            yield return new WaitForSeconds(1.5f);

            while (_spawningActive && _elapsed < totalDuration)
            {
                SpawnWave();

                float progress = Mathf.Clamp01(_elapsed / totalDuration);
                float delay = Mathf.Lerp(spawnDelayStart, spawnDelayEnd, progress);
                delay = Mathf.Max(0.4f, delay);
                yield return new WaitForSeconds(delay);
                _elapsed += delay;
            }
        }

        private void SpawnWave()
        {
            float progression = Mathf.Clamp01(_elapsed / totalDuration);

            if (_introIndex < _blueprints.Length)
            {
                var introBlueprint = _blueprints[_introIndex];
                _introIndex++;
                float topEdge = _camera.transform.position.y + _camera.orthographicSize;
                Vector2 spawnPos = new Vector2(0f, topEdge - Mathf.Max(0.02f, spawnInset));
                SpawnEnemy(spawnPos, introBlueprint, Mathf.Lerp(0.5f, 2.5f, progression));
                return;
            }

            int available = Mathf.Clamp(_introIndex, 1, _blueprints.Length);
            int targetCount = Mathf.Clamp(Mathf.RoundToInt(1 + _elapsed * 0.05f), 2, 10);
            float difficulty = Mathf.Lerp(1.2f, 6f, progression);

            for (int i = 0; i < targetCount; i++)
            {
                var blueprint = _blueprints[Random.Range(0, available)];
                Vector2 spawnPos = PickSpawnPosition(i, targetCount, blueprint.CenteringBias);
                SpawnEnemy(spawnPos, blueprint, difficulty);
            }
        }

        private Vector2 PickSpawnPosition(int index, int total, float centeringBias)
        {
            float camWidth = _worldBounds.x;
            float step = (camWidth * 2f - horizontalPadding * 2f) / Mathf.Max(1, total - 1);
            float x = -camWidth + horizontalPadding + step * index + Random.Range(-0.6f, 0.6f);
            if (centeringBias > 0f)
            {
                float bias = Mathf.Clamp01(centeringBias * 0.15f);
                x = Mathf.Lerp(x, 0f, bias);
            }
            float top = _camera.transform.position.y + _camera.orthographicSize;
            float y = top - Mathf.Max(0.02f, spawnInset);
            return new Vector2(x, y);
        }

        private void SpawnEnemy(Vector2 position, EnemyBlueprint blueprint, float difficulty)
        {
            var enemyGO = new GameObject($"Enemy_{blueprint.Name}");
            enemyGO.transform.SetParent(transform, false);
            enemyGO.transform.position = position;
            enemyGO.transform.localScale = Vector3.one * blueprint.Scale;

            var renderer = enemyGO.AddComponent<SpriteRenderer>();
            renderer.sprite = blueprint.Sprite;
            renderer.sortingOrder = 10;
            renderer.color = blueprint.Color;

            var collider = enemyGO.AddComponent<CircleCollider2D>();
            collider.isTrigger = true;
            collider.radius = 0.45f * blueprint.Scale;

            enemyGO.AddComponent<Health>();

            var controller = enemyGO.AddComponent<EnemyController>();
            controller.Initialize(this, _enemyBulletPool, _player, blueprint, difficulty, _worldBounds);

            _liveEnemies.Add(controller);
        }

        private EnemyBlueprint[] BuildBlueprints()
        {
            var blazeColor = new Color(1f, 0.55f, 0.25f, 1f);
            var strikerColor = new Color(0.55f, 0.45f, 1f, 1f);
            var cascadeColor = new Color(0.35f, 1f, 0.65f, 1f);
            var interceptorColor = new Color(1f, 0.9f, 0.3f, 1f);

            return new[]
            {
                new EnemyBlueprint(
                    "Blazer",
                    blazeColor,
                    1.6f,
                    EnemyMovementStyle.ZigZag,
                    EnemyFireStyle.Radial,
                    2.8f,
                    2.8f,
                    1.1f,
                    1.3f,
                    12,
                    3,
                    13f,
                    7f,
                    25f,
                    55f,
                    140,
                    0f,
                    GenerateSprite(EnemyShape.Diamond, blazeColor),
                    1.2f),
                new EnemyBlueprint(
                    "Striker",
                    strikerColor,
                    1.4f,
                    EnemyMovementStyle.Straight,
                    EnemyFireStyle.Stream,
                    3.3f,
                    0f,
                    0f,
                    1f,
                    4,
                    2,
                    18f,
                    9f,
                    30f,
                    65f,
                    160,
                    0f,
                    GenerateSprite(EnemyShape.Triangle, strikerColor),
                    1.5f),
                new EnemyBlueprint(
                    "Cascade",
                    cascadeColor,
                    1.7f,
                    EnemyMovementStyle.Sine,
                    EnemyFireStyle.Burst,
                    2.5f,
                    3.2f,
                    1.2f,
                    1.8f,
                    2,
                    0,
                    12f,
                    10f,
                    35f,
                    80f,
                    200,
                    0f,
                    GenerateSprite(EnemyShape.Disc, cascadeColor),
                    1.1f),
                new EnemyBlueprint(
                    "Interceptor",
                    interceptorColor,
                    1.3f,
                    EnemyMovementStyle.Orbit,
                    EnemyFireStyle.None,
                    5.2f,
                    0f,
                    1.6f,
                    0f,
                    0,
                    0,
                    0f,
                    0f,
                    45f,
                    50f,
                    180,
                    1.9f,
                    GenerateSprite(EnemyShape.Arrow, interceptorColor),
                    1.8f)
            };
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                Instance = null;
            }
        }

        private Sprite GenerateSprite(EnemyShape shape, Color color)
        {
            const int size = 64;
            var texture = new Texture2D(size, size, TextureFormat.RGBA32, false)
            {
                filterMode = FilterMode.Point
            };

            var pixels = new Color[size * size];
            var center = new Vector2(size * 0.5f, size * 0.5f);

            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    int index = x + y * size;
                    bool fill = false;
                    switch (shape)
                    {
                        case EnemyShape.Disc:
                            fill = Vector2.Distance(center, new Vector2(x, y)) <= size * 0.32f;
                            break;
                        case EnemyShape.Triangle:
                            {
                                float ny = 1f - (y / (float)(size - 1));
                                float halfWidth = ny * size * 0.35f;
                                fill = Mathf.Abs(x - center.x) <= halfWidth && ny > 0.1f;
                                break;
                            }
                        case EnemyShape.Diamond:
                            fill = Mathf.Abs(x - center.x) + Mathf.Abs(y - center.y) <= size * 0.32f;
                            break;
                        case EnemyShape.Arrow:
                            {
                                float ny = y / (float)(size - 1);
                                float half = Mathf.Lerp(size * 0.1f, size * 0.35f, ny);
                                bool head = ny > 0.55f && Mathf.Abs(x - center.x) <= Mathf.Lerp(size * 0.05f, size * 0.4f, Mathf.Clamp01((ny - 0.55f) / 0.45f));
                                bool body = ny <= 0.55f && Mathf.Abs(x - center.x) <= half;
                                fill = head || body;
                                break;
                            }
                    }

                    pixels[index] = fill ? color : new Color(0f, 0f, 0f, 0f);
                }
            }

            texture.SetPixels(pixels);
            texture.Apply();

            return Sprite.Create(texture, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 64f);
        }

        private enum EnemyShape
        {
            Disc,
            Triangle,
            Diamond,
            Arrow
        }
    }
}
