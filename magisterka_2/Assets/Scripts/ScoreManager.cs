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
        private int _score;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
        }

        public void Initialize(Text scoreText)
        {
            _scoreText = scoreText;
            ResetScore();
        }

        public void AddScore(int value)
        {
            _score += value;
            UpdateLabel();
        }

        public void ResetScore()
        {
            _score = 0;
            UpdateLabel();
        }

        private void UpdateLabel()
        {
            if (_scoreText == null)
            {
                return;
            }

            _scoreText.text = $"Score: {_score:N0}";
        }
    }
}
