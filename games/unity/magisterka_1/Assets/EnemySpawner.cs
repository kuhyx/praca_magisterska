using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    public GameObject enemyPrefab;
    public float spawnInterval = 1f;
    public float xRange = 8f;

    void Start()
    {
        InvokeRepeating("SpawnEnemy", 1f, spawnInterval);
    }

    void SpawnEnemy()
    {
        float xPos = Random.Range(-xRange, xRange);
        Instantiate(enemyPrefab, new Vector3(xPos, 6, 0), Quaternion.identity);
    }
}