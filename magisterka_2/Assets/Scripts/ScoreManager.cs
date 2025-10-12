using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Handles score accumulation and HUD updates.
    /// </summary>
    public class ScoreManager : MonoBehaviour
    {
        public static ScoreManager Instance { get; private set; }

        private Text _scoreText;
        private Image[] _lifeIcons;
        private Text _statusText;
        private Image _damageOverlay;
        private int _score;
        private int _queuedLives = -1;
        private string _queuedStatus;
        private Color _queuedStatusColor = Color.white;
        private Coroutine _damageFlashRoutine;

        public event Action<int> ScoreChanged;

        public int CurrentScore => _score;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
        }

        public void Initialize(Text scoreText, Image[] lifeIcons, Text statusText, Image damageOverlay)
        {
            _scoreText = scoreText;
            _lifeIcons = lifeIcons;
            _statusText = statusText;
            _damageOverlay = damageOverlay;
            HideStatus();

            ResetScore();

            if (_queuedLives >= 0)
            {
                ApplyLives(_queuedLives);
                _queuedLives = -1;
            }

            if (!string.IsNullOrEmpty(_queuedStatus))
            {
                ShowStatus(_queuedStatus, _queuedStatusColor);
                _queuedStatus = null;
            }

            if (_damageOverlay != null)
            {
                var color = _damageOverlay.color;
                color.a = 0f;
                _damageOverlay.color = color;
            }

            ScoreChanged?.Invoke(_score);
        }

        public void AddScore(int value)
        {
            _score += value;
            UpdateLabel();
            ScoreChanged?.Invoke(_score);
        }

        public void ResetScore()
        {
            _score = 0;
            UpdateLabel();
            HideStatus();
            ScoreChanged?.Invoke(_score);
        }

        public void SetLives(int lives)
        {
            if (_lifeIcons == null || _lifeIcons.Length == 0)
            {
                _queuedLives = lives;
                return;
            }

            ApplyLives(lives);
        }

        public void ShowGameOver()
        {
            ShowStatus("GAME OVER", new Color(1f, 0.5f, 0.5f, 1f));
        }

        public void ShowVictory()
        {
            ShowStatus("YOU WIN", new Color(0.6f, 1f, 0.6f, 1f));
        }

        public void TriggerDamageFlash(float strength)
        {
            if (_damageOverlay == null)
            {
                return;
            }

            strength = Mathf.Clamp01(strength);

            if (_damageFlashRoutine != null)
            {
                StopCoroutine(_damageFlashRoutine);
            }

            _damageFlashRoutine = StartCoroutine(DamageFlashRoutine(strength));
        }

        public void HideStatus()
        {
            if (_statusText == null)
            {
                return;
            }

            _statusText.enabled = false;
        }

        private void UpdateLabel()
        {
            if (_scoreText == null)
            {
                return;
            }

            _scoreText.text = $"Score: {_score:N0}";
        }

        private void ApplyLives(int lives)
        {
            if (_lifeIcons == null)
            {
                return;
            }

            for (int i = 0; i < _lifeIcons.Length; i++)
            {
                if (_lifeIcons[i] != null)
                {
                    _lifeIcons[i].enabled = i < lives;
                }
            }
        }

        private void ShowStatus(string message, Color color)
        {
            if (_statusText == null)
            {
                _queuedStatus = message;
                _queuedStatusColor = color;
                return;
            }

            _statusText.text = message;
            _statusText.color = color;
            _statusText.enabled = true;
        }

        private IEnumerator DamageFlashRoutine(float strength)
        {
            float peakAlpha = Mathf.Lerp(0.35f, 0.75f, strength);
            float duration = 0.45f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime;
                float normalized = Mathf.Clamp01(elapsed / duration);
                float alpha = Mathf.Sin(normalized * Mathf.PI) * peakAlpha;
                var color = _damageOverlay.color;
                color.a = alpha;
                _damageOverlay.color = color;
                yield return null;
            }

            var reset = _damageOverlay.color;
            reset.a = 0f;
            _damageOverlay.color = reset;
            _damageFlashRoutine = null;
        }
    }
}
