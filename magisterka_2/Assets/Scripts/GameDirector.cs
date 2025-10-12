using UnityEngine;
using UnityEngine.UI;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Oversees overall game flow: timer, victory detection, and difficulty pacing hooks.
    /// </summary>
    public class GameDirector : MonoBehaviour
    {
        public static GameDirector Instance { get; private set; }

    [SerializeField] private float totalDuration = 90f;

        private EnemySpawner _spawner;
        private PlayerController _player;
        private ScoreManager _scoreManager;
        private Text _timerText;

        private float _timeRemaining;
        private bool _timerRunning;
        private bool _timerExpired;
    private bool _victoryTriggered;

        public float TotalDuration => totalDuration;

        public void Initialize(EnemySpawner spawner, PlayerController player, ScoreManager scoreManager, Text timerText, float duration)
        {
            _spawner = spawner;
            _player = player;
            _scoreManager = scoreManager;
            _timerText = timerText;
            totalDuration = duration > 0f ? duration : totalDuration;
            _timeRemaining = totalDuration;
            _timerRunning = true;
            _timerExpired = false;
            _victoryTriggered = false;
            UpdateTimerLabel();
        }

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
        }

        private void Update()
        {
            if (_timerRunning && !_timerExpired)
            {
                _timeRemaining -= Time.deltaTime;
                if (_timeRemaining <= 0f)
                {
                    _timeRemaining = 0f;
                    _timerExpired = true;
                    _timerRunning = false;
                    _spawner?.StopSpawning();
                }

                UpdateTimerLabel();
            }

            if (_timerExpired && !_victoryTriggered)
            {
                bool enemiesRemain = _spawner != null && _spawner.HasActiveEnemies;
                if (!enemiesRemain)
                {
                    TriggerVictory();
                }
            }
        }

        public void OnPlayerGameOver()
        {
            _timerRunning = false;
        }

        private void TriggerVictory()
        {
            _victoryTriggered = true;
            _scoreManager?.ShowVictory();
            _player?.HandleVictory();
        }

        private void UpdateTimerLabel()
        {
            if (_timerText == null)
            {
                return;
            }

            int seconds = Mathf.CeilToInt(_timeRemaining);
            int minutes = seconds / 60;
            seconds %= 60;
            _timerText.text = $"{minutes:00}:{seconds:00}";
        }
    }
}
