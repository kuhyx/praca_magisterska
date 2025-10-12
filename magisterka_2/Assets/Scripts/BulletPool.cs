using System;
using System.Collections.Generic;
using Magisterka.BulletHell;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Runtime pool that keeps huge bullet counts without constant allocations.
    /// </summary>
    public class BulletPool : MonoBehaviour
    {
        [SerializeField] private Color bulletColor = Color.white;
        [SerializeField] private Faction faction = Faction.Player;
        [SerializeField] private int warmCapacity = 64;

        private readonly Queue<Bullet> _pool = new Queue<Bullet>();
        private readonly HashSet<Bullet> _liveBullets = new HashSet<Bullet>();

        private Transform _poolRoot;

        public Color BulletColor => bulletColor;
        public Faction OwnerFaction => faction;

        public static BulletPool Create(Transform parent, string poolName, Color color, Faction ownerFaction, int warmCount)
        {
            if (parent == null) throw new ArgumentNullException(nameof(parent));

            var go = new GameObject(poolName);
            go.transform.SetParent(parent, false);
            var pool = go.AddComponent<BulletPool>();
            pool.Initialize(color, ownerFaction, warmCount);
            return pool;
        }

        private void Initialize(Color color, Faction ownerFaction, int warmCount)
        {
            bulletColor = color;
            faction = ownerFaction;
            warmCapacity = Mathf.Max(0, warmCount);
            _poolRoot = new GameObject("Inactive" + name).transform;
            _poolRoot.SetParent(transform, false);

            for (int i = 0; i < warmCapacity; i++)
            {
                var bullet = Bullet.Create(this, bulletColor, faction);
                Return(bullet);
            }
        }

        public Bullet Spawn(Vector2 position, Vector2 direction, float speed, float damage)
        {
            Bullet bullet = _pool.Count > 0 ? _pool.Dequeue() : Bullet.Create(this, bulletColor, faction);
            _liveBullets.Add(bullet);
            bullet.transform.SetParent(null, false);
            bullet.gameObject.SetActive(true);
            bullet.transform.position = position;
            bullet.Configure(direction, speed, damage, faction);
            return bullet;
        }

        public void Return(Bullet bullet)
        {
            if (bullet == null) return;

            bullet.gameObject.SetActive(false);
            bullet.transform.SetParent(_poolRoot, false);
            _pool.Enqueue(bullet);
            _liveBullets.Remove(bullet);
        }

        public void ClearLiveBullets()
        {
            if (_liveBullets.Count == 0) return;

            foreach (var bullet in _liveBullets)
            {
                if (bullet != null)
                {
                    bullet.gameObject.SetActive(false);
                    bullet.transform.SetParent(_poolRoot, false);
                    _pool.Enqueue(bullet);
                }
            }

            _liveBullets.Clear();
        }
    }
}
