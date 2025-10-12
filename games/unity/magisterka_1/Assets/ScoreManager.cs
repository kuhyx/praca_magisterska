using UnityEngine;
using UnityEngine.UI;

public class ScoreManager : MonoBehaviour
{
    public static ScoreManager Instance { get; private set; }

    [SerializeField] private Text scoreText;
    [SerializeField] private Text livesText;
    [SerializeField] private Text timerText;

    private int score;
    private int currentLives;
    private float cachedDuration;

    private float bombMessageTimer;
    private const float BombMessageDuration = 2.5f;

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }

        Instance = this;
        DontDestroyOnLoad(gameObject);
        EnsureUiReferences();
        RefreshLabels();
    }

    private void Update()
    {
        if (bombMessageTimer <= 0f || timerText == null) return;

        bombMessageTimer -= Time.deltaTime;
        if (bombMessageTimer <= 0f)
        {
            timerText.text = FormatTime(cachedDuration);
        }
    }

    public void RegisterGameStart(int initialLives, float duration)
    {
        currentLives = Mathf.Max(0, initialLives);
        cachedDuration = Mathf.Max(0f, duration);
        score = 0;
        bombMessageTimer = 0f;
        RefreshLabels();
    }

    public void AddScore(int amount)
    {
        score += Mathf.Max(0, amount);
        UpdateScoreLabel();
    }

    public void SetLives(int lives)
    {
        currentLives = Mathf.Max(0, lives);
        UpdateLivesLabel();
    }

    public void UpdateTimer(float timeRemaining)
    {
        cachedDuration = Mathf.Max(0f, timeRemaining);
        if (bombMessageTimer > 0f) return;
        if (timerText == null) return;

        timerText.text = FormatTime(timeRemaining);
    }

    public void HandleGameOver()
    {
        if (timerText != null)
        {
            timerText.text = "Game Over";
        }
    }

    public void HandleGameClear()
    {
        if (timerText != null)
        {
            timerText.text = "Mission Complete";
        }
    }

    public void RegisterBombUse()
    {
        if (timerText == null) return;

        timerText.text = "Screen Clear Deployed";
        bombMessageTimer = BombMessageDuration;
    }

    private void EnsureUiReferences()
    {
        if (scoreText != null && livesText != null && timerText != null) return;

        Canvas canvas = FindObjectOfType<Canvas>();
        if (canvas == null)
        {
            canvas = BuildRuntimeCanvas();
        }

        if (scoreText == null)
        {
            scoreText = CreateLabel(canvas.transform, "ScoreText", new Vector2(20f, -20f));
        }

        if (livesText == null)
        {
            livesText = CreateLabel(canvas.transform, "LivesText", new Vector2(20f, -60f));
        }

        if (timerText == null)
        {
            timerText = CreateLabel(canvas.transform, "TimerText", new Vector2(20f, -100f));
        }
    }

    private Canvas BuildRuntimeCanvas()
    {
        GameObject canvasObject = new GameObject("HUDCanvas");
        DontDestroyOnLoad(canvasObject);

        Canvas canvas = canvasObject.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvasObject.AddComponent<CanvasScaler>();
        canvasObject.AddComponent<GraphicRaycaster>();
        return canvas;
    }

    private Text CreateLabel(Transform parent, string name, Vector2 anchoredOffset)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(parent);

        RectTransform rectTransform = go.AddComponent<RectTransform>();
        rectTransform.anchorMin = new Vector2(0f, 1f);
        rectTransform.anchorMax = new Vector2(0f, 1f);
        rectTransform.pivot = new Vector2(0f, 1f);
        rectTransform.anchoredPosition = anchoredOffset;
        rectTransform.sizeDelta = new Vector2(320f, 36f);

        Text label = go.AddComponent<Text>();
        label.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        label.fontSize = 24;
        label.color = Color.white;
        label.alignment = TextAnchor.UpperLeft;
        label.horizontalOverflow = HorizontalWrapMode.Overflow;
        return label;
    }

    private void RefreshLabels()
    {
        UpdateScoreLabel();
        UpdateLivesLabel();
        if (timerText != null)
        {
            timerText.text = FormatTime(cachedDuration);
        }
    }

    private void UpdateScoreLabel()
    {
        if (scoreText != null)
        {
            scoreText.text = $"Score: {score}";
        }
    }

    private void UpdateLivesLabel()
    {
        if (livesText != null)
        {
            livesText.text = $"Lives: {currentLives}";
        }
    }

    private static string FormatTime(float seconds)
    {
        seconds = Mathf.Max(0f, seconds);
        int minutes = Mathf.FloorToInt(seconds / 60f);
        int secs = Mathf.FloorToInt(seconds % 60f);
        return $"Time: {minutes:00}:{secs:00}";
    }
}
