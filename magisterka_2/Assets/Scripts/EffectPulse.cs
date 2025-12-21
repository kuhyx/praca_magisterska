using System;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Simple animated sprite burst that scales and fades over a short lifetime.
    /// </summary>
    [RequireComponent(typeof(SpriteRenderer))]
    public class EffectPulse : MonoBehaviour
    {
        private SpriteRenderer _renderer;
        private Action<EffectPulse> _onComplete;
        private Vector3 _startScale;
        private Vector3 _endScale;
        private float _duration;
        private float _elapsed;
        private Color _baseColor;
        private bool _isActive;

        private void Awake()
        {
            _renderer = GetComponent<SpriteRenderer>();
            _renderer.sprite = BuildPulseSprite();
            _renderer.sortingOrder = 50;
            _renderer.color = Color.white;
        }

        public void Play(Vector2 position, Color color, float startSize, float endSize, float duration, Action<EffectPulse> onComplete)
        {
            transform.position = position;
            _startScale = Vector3.one * Mathf.Max(0.01f, startSize);
            _endScale = Vector3.one * Mathf.Max(0.02f, endSize);
            _duration = Mathf.Max(0.05f, duration);
            _elapsed = 0f;
            _baseColor = color;
            _renderer.color = color;
            _onComplete = onComplete;
            _isActive = true;
            gameObject.SetActive(true);
        }

        private void Update()
        {
            if (!_isActive)
            {
                return;
            }

            _elapsed += Time.deltaTime;
            float t = Mathf.Clamp01(_elapsed / _duration);
            transform.localScale = Vector3.Lerp(_startScale, _endScale, t);

            var color = _baseColor;
            color.a = Mathf.Lerp(1f, 0f, t);
            _renderer.color = color;

            if (_elapsed >= _duration)
            {
                Stop();
            }
        }

        public void Stop()
        {
            if (!_isActive)
            {
                return;
            }

            _isActive = false;
            gameObject.SetActive(false);
            if (_onComplete != null)
            {
                _onComplete.Invoke(this);
            }
        }

        private static Sprite BuildPulseSprite()
        {
            const int size = 32;
            var texture = new Texture2D(size, size, TextureFormat.RGBA32, false);
            texture.filterMode = FilterMode.Bilinear;

            var center = new Vector2(size - 1, size - 1) * 0.5f;
            var pixels = new Color[size * size];

            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    var index = x + y * size;
                    float dst = Vector2.Distance(center, new Vector2(x, y)) / (size * 0.5f);
                    float alpha = Mathf.Clamp01(1f - dst);
                    pixels[index] = new Color(1f, 1f, 1f, alpha * alpha);
                }
            }

            texture.SetPixels(pixels);
            texture.Apply();

            return Sprite.Create(texture, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 64f);
        }
    }
}
