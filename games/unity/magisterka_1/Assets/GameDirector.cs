using UnityEngine;

public class GameDirector : MonoBehaviour
{
    public static GameDirector Instance { get; private set; }

    [SerializeField] private EnemySpawner enemySpawner;
    [SerializeField] private PlayerController player;
    [SerializeField] private float gameDuration = 300f;

    private float elapsedTime;
    private bool gameActive;

    public float GameDuration => gameDuration;

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }

        Instance = this;
        gameActive = true;
    }

    private void Start()
    {
        elapsedTime = 0f;
        if (enemySpawner == null)
        {
            enemySpawner = FindObjectOfType<EnemySpawner>();
        }
        if (player == null)
        {
            player = FindObjectOfType<PlayerController>();
        }

        ScoreManager.Instance?.RegisterGameStart(player != null ? player.CurrentLives : 0, gameDuration);
    }

    private void Update()
    {
        if (!gameActive) return;

        elapsedTime += Time.deltaTime;
        float remaining = Mathf.Max(0f, gameDuration - elapsedTime);
        ScoreManager.Instance?.UpdateTimer(remaining);

        if (elapsedTime >= gameDuration)
        {
            gameActive = false;
            enemySpawner?.StopSpawning();
            ScoreManager.Instance?.HandleGameClear();
        }
    }

    public void HandlePlayerDeath()
    {
        if (!gameActive) return;

        gameActive = false;
        enemySpawner?.StopSpawning();
        ScoreManager.Instance?.HandleGameOver();
    }
}
