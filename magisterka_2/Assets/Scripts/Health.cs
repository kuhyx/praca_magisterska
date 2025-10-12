using System;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Tracks hit points and dispatches simple death callbacks.
    /// </summary>
    public class Health : MonoBehaviour
    {
        [SerializeField] private Faction faction = Faction.Enemy;
        [SerializeField] private float maxHealth = 10f;

        private float _current;

        public event Action<Health> Died;
        public event Action<float, Vector2> Damaged;

        public Faction Faction => faction;
        public float MaxHealth => maxHealth;
        public float Current => _current;

        private void Awake()
        {
            _current = maxHealth;
        }

        public void Configure(Faction targetFaction, float health)
        {
            faction = targetFaction;
            maxHealth = Mathf.Max(1f, health);
            _current = maxHealth;
        }

        public void ApplyDamage(float damage, Vector2 hitPoint)
        {
            if (_current <= 0f)
            {
                return;
            }

            _current -= damage;
            EffectManager.Instance?.SpawnHitEffect(hitPoint, faction, Mathf.Clamp01(damage / maxHealth));
            Damaged?.Invoke(damage, hitPoint);

            if (_current <= 0f)
            {
                Die();
            }
        }

        public void RestoreFull()
        {
            _current = maxHealth;
        }

        public void Kill()
        {
            if (_current <= 0f)
            {
                return;
            }

            _current = 0f;
            Damaged?.Invoke(maxHealth, transform.position);
            Die();
        }

        private void Die()
        {
            Died?.Invoke(this);
        }
    }
}
