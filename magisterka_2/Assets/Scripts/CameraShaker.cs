using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Quick camera shake helper for impactful effects.
    /// </summary>
    public class CameraShaker : MonoBehaviour
    {
        private Vector3 _originalPos;
        private float _shakeTime;
        private float _shakeStrength;

        private void Awake()
        {
            _originalPos = transform.localPosition;
        }

        private void Update()
        {
            if (_shakeTime <= 0f)
            {
                transform.localPosition = Vector3.Lerp(transform.localPosition, _originalPos, 6f * Time.deltaTime);
                return;
            }

            _shakeTime -= Time.deltaTime;
            var offset = Random.insideUnitCircle * _shakeStrength;
            transform.localPosition = _originalPos + new Vector3(offset.x, offset.y, 0f);
            _shakeStrength = Mathf.Lerp(_shakeStrength, 0f, 3f * Time.deltaTime);
        }

        public void Shake(float duration, float strength)
        {
            _shakeTime = Mathf.Max(_shakeTime, duration);
            _shakeStrength = Mathf.Max(_shakeStrength, strength);
        }
    }
}
