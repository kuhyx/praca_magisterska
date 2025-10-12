using System.Collections.Generic;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Lightweight visual feedback hub for hits, explosions, and screen-clears.
    /// </summary>
    public class EffectManager : MonoBehaviour
    {
        public static EffectManager Instance { get; private set; }

        [SerializeField] private int warmCount = 64;
        [SerializeField] private Color playerColor = new Color(0.35f, 0.85f, 1f, 1f);
        [SerializeField] private Color enemyColor = new Color(1f, 0.45f, 0.25f, 1f);

        private readonly Queue<EffectPulse> _pool = new Queue<EffectPulse>();
        private Transform _poolRoot;
        private CameraShaker _cameraShaker;

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

        public void Initialize(Transform parent)
        {
            if (parent != null)
            {
                transform.SetParent(parent, false);
            }

            _cameraShaker = FindFirstObjectByType<CameraShaker>();
            if (_cameraShaker == null && Camera.main != null)
            {
                _cameraShaker = Camera.main.gameObject.AddComponent<CameraShaker>();
            }

            _poolRoot = new GameObject("FX_Pool").transform;
            _poolRoot.SetParent(transform, false);

            Warmup(warmCount);
        }

        public void SpawnHitEffect(Vector2 position, Faction hitFaction, float intensity)
        {
            var color = hitFaction == Faction.Player ? playerColor : enemyColor;
            var endSize = Mathf.Lerp(0.6f, 1.8f, Mathf.Clamp01(intensity + 0.2f));
            PlayPulse(position, color, 0.25f, endSize, 0.18f);
        }

        public void SpawnExplosion(Vector2 position, Faction faction, float size = 2.5f)
        {
            var color = faction == Faction.Player ? playerColor : enemyColor;
            for (int i = 0; i < 4; i++)
            {
                float start = 0.4f + i * 0.1f;
                float end = size + i * 0.35f;
                float duration = 0.22f + i * 0.06f;
                PlayPulse(position, color, start, end, duration);
            }

            _cameraShaker?.Shake(0.18f, 0.45f * size);
        }

        public void SpawnScreenClear(Vector2 position, float radius)
        {
            for (int i = 0; i < 6; i++)
            {
                float start = 0.8f + i * 0.5f;
                float end = radius + i * 1.2f;
                float duration = 0.35f + i * 0.12f;
                var blend = Mathf.Clamp01(i / 5f);
                var color = Color.Lerp(playerColor, enemyColor, blend);
                PlayPulse(position, color, start, end, duration);
            }

            _cameraShaker?.Shake(0.4f, 1.2f * radius);
        }

        private void Warmup(int count)
        {
            for (int i = 0; i < count; i++)
            {
                _pool.Enqueue(CreatePulse());
            }
        }

        private EffectPulse CreatePulse()
        {
            var go = new GameObject("EffectPulse");
            go.transform.SetParent(_poolRoot, false);
            var pulse = go.AddComponent<EffectPulse>();
            go.SetActive(false);
            return pulse;
        }

        private void PlayPulse(Vector2 position, Color color, float startSize, float endSize, float duration)
        {
            var pulse = _pool.Count > 0 ? _pool.Dequeue() : CreatePulse();
            pulse.transform.SetParent(null, false);
            pulse.Play(position, color, startSize, endSize, duration, Recycle);
        }

        private void Recycle(EffectPulse pulse)
        {
            if (pulse == null)
            {
                return;
            }

            pulse.transform.SetParent(_poolRoot, false);
            _pool.Enqueue(pulse);
        }
    }
}
