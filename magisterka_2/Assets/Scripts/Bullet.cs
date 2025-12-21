using System.Collections.Generic;
using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Handles individual bullet lifetime, movement, and collision dispatching.
    /// </summary>
    [RequireComponent(typeof(SpriteRenderer))]
    public class Bullet : MonoBehaviour
    {
        private static readonly Dictionary<Color, Sprite> SpriteCache = new Dictionary<Color, Sprite>();

        [SerializeField] private float radius = 0.22f;
        [SerializeField] private float despawnBounds = 14f;

        private SpriteRenderer _spriteRenderer;
        private CircleCollider2D _collider;
        private Rigidbody2D _body;
        private BulletPool _ownerPool;
        private Vector2 _direction;
        private float _speed;
        private float _damage;
        private Faction _ownerFaction;

        public bool BelongsToEnemy => _ownerFaction == Faction.Enemy;
        public BulletPool OwnerPool => _ownerPool;

        public static Bullet Create(BulletPool pool, Color tint, Faction faction)
        {
            var go = new GameObject("Bullet" + faction, typeof(SpriteRenderer));
            var bullet = go.AddComponent<Bullet>();
            bullet.Initialize(pool, tint, faction);
            return bullet;
        }

        private void Initialize(BulletPool pool, Color tint, Faction faction)
        {
            _ownerPool = pool;
            _ownerFaction = faction;
            _spriteRenderer = GetComponent<SpriteRenderer>();
            _spriteRenderer.sprite = GetOrCreateSprite(tint);
            _spriteRenderer.color = tint;

            _body = gameObject.AddComponent<Rigidbody2D>();
            _body.gravityScale = 0f;
            _body.bodyType = RigidbodyType2D.Kinematic;
            _body.interpolation = RigidbodyInterpolation2D.Interpolate;

            _collider = gameObject.AddComponent<CircleCollider2D>();
            _collider.isTrigger = true;
            _collider.radius = radius;

            gameObject.layer = LayerMask.NameToLayer("Default");
            gameObject.SetActive(false);
        }

        public void Configure(Vector2 direction, float speed, float damage, Faction faction)
        {
            _direction = direction.normalized;
            _speed = speed;
            _damage = damage;
            _ownerFaction = faction;
        }

        private void Update()
        {
            transform.position += (Vector3)(_direction * (_speed * Time.deltaTime));

            if (Mathf.Abs(transform.position.x) > despawnBounds || Mathf.Abs(transform.position.y) > despawnBounds)
            {
                Despawn();
            }
        }

        private void OnTriggerEnter2D(Collider2D other)
        {
            if (other.TryGetComponent(out Bullet otherBullet))
            {
                if (otherBullet == this || otherBullet._ownerFaction == _ownerFaction)
                {
                    return;
                }

                if (otherBullet.gameObject.activeInHierarchy)
                {
                    otherBullet.Despawn();
                }

                Despawn();
                return;
            }

            if (!other.TryGetComponent(out Health health))
            {
                return;
            }

            if (health.Faction == _ownerFaction)
            {
                return;
            }

            if (health.Faction == Faction.Player && PlayerController.Instance != null && PlayerController.Instance.IsInvulnerable())
            {
                return;
            }

            health.ApplyDamage(_damage, transform.position);
            Despawn();
        }

        public void Despawn()
        {
            if (_ownerPool != null)
            {
                _ownerPool.Return(this);
            }
        }

        private static Sprite GetOrCreateSprite(Color tint)
        {
            if (SpriteCache.TryGetValue(tint, out var sprite))
            {
                return sprite;
            }

            const int size = 16;
            var texture = new Texture2D(size, size, TextureFormat.RGBA32, false) { filterMode = FilterMode.Point };
            var pixels = new Color[size * size];
            for (int i = 0; i < pixels.Length; i++)
            {
                pixels[i] = tint;
            }

            texture.SetPixels(pixels);
            texture.Apply();

            sprite = Sprite.Create(texture, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 100f);
            SpriteCache[tint] = sprite;
            return sprite;
        }
    }
}
