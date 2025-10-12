using System.Collections;
using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    [SerializeField] private GameObject enemyPrefab;
    [SerializeField] private Transform[] spawnPoints;
    [SerializeField] private float spawnAreaHalfWidth = 9f;
    [SerializeField] private float gameDuration = 300f;
    [SerializeField] private AnimationCurve spawnPerSecond = AnimationCurve.Linear(0f, 0.4f, 1f, 4.5f);
    [SerializeField] private int maxSimultaneousEnemies = 120;

    private bool spawningActive;

    private void Start()
    {
        spawningActive = true;
        StartCoroutine(SpawnLoop());
    }

    private IEnumerator SpawnLoop()
    {
        if (enemyPrefab == null)
        {
            yield break;
        }

        float elapsed = 0f;

        while (spawningActive && elapsed < gameDuration)
        {
            float normalized = gameDuration > 0f ? Mathf.Clamp01(elapsed / gameDuration) : 1f;
            float spawnsPerSecond = Mathf.Max(0.05f, spawnPerSecond.Evaluate(normalized));
            float waitTime = 1f / spawnsPerSecond;

            if (Enemy.ActiveEnemies.Count < maxSimultaneousEnemies)
            {
                SpawnWave(normalized);
            }

            elapsed += waitTime;
            yield return new WaitForSeconds(waitTime);
        }
    }

    private void SpawnWave(float normalizedTime)
    {
        int baseCount = Mathf.Clamp(Mathf.RoundToInt(1f + normalizedTime * 6f), 1, 8);
        int burstSize = Mathf.Clamp(baseCount + Random.Range(0, 3), 1, 12);

        for (int i = 0; i < burstSize; i++)
        {
            SpawnEnemy();
        }
    }

    private void SpawnEnemy()
    {
        Vector3 spawnPosition = transform.position;

        if (spawnPoints != null && spawnPoints.Length > 0)
        {
            Transform pick = spawnPoints[Random.Range(0, spawnPoints.Length)];
            spawnPosition = pick.position;
        }
        else
        {
            spawnPosition.x = Random.Range(-spawnAreaHalfWidth, spawnAreaHalfWidth);
        }

        Instantiate(enemyPrefab, spawnPosition, Quaternion.identity);
    }

    public void StopSpawning()
    {
        spawningActive = false;
        StopAllCoroutines();
    }
}