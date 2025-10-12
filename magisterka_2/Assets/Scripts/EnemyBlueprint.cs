using UnityEngine;

namespace Magisterka.BulletHell
{
    public enum EnemyMovementStyle
    {
        ZigZag,
        Straight,
        Sine,
        Orbit
    }

    public enum EnemyFireStyle
    {
        None,
        Radial,
        Stream,
        Burst
    }

    /// <summary>
    /// Runtime configuration for enemy archetypes.
    /// </summary>
    public sealed class EnemyBlueprint
    {
        public EnemyBlueprint(
            string name,
            Color color,
            float scale,
            EnemyMovementStyle movement,
            EnemyFireStyle fire,
            float moveSpeed,
            float horizontalAmplitude,
            float horizontalFrequency,
            float fireInterval,
            int bulletsPerVolley,
            int aimedShots,
            float bulletSpeed,
            float bulletDamage,
            float contactDamage,
            float health,
            int score,
            float orbitRadius,
            Sprite sprite,
            float centeringBias)
        {
            Name = name;
            Color = color;
            Scale = scale;
            Movement = movement;
            Fire = fire;
            MoveSpeed = moveSpeed;
            HorizontalAmplitude = horizontalAmplitude;
            HorizontalFrequency = horizontalFrequency;
            FireInterval = fireInterval;
            BulletsPerVolley = bulletsPerVolley;
            AimedShots = aimedShots;
            BulletSpeed = bulletSpeed;
            BulletDamage = bulletDamage;
            ContactDamage = contactDamage;
            Health = health;
            Score = score;
            OrbitRadius = orbitRadius;
            Sprite = sprite;
            CenteringBias = centeringBias;
        }

        public string Name { get; }
        public Color Color { get; }
        public float Scale { get; }
        public EnemyMovementStyle Movement { get; }
        public EnemyFireStyle Fire { get; }
        public float MoveSpeed { get; }
        public float HorizontalAmplitude { get; }
        public float HorizontalFrequency { get; }
        public float FireInterval { get; }
        public int BulletsPerVolley { get; }
        public int AimedShots { get; }
        public float BulletSpeed { get; }
        public float BulletDamage { get; }
        public float ContactDamage { get; }
        public float Health { get; }
        public int Score { get; }
        public float OrbitRadius { get; }
        public Sprite Sprite { get; }
        public float CenteringBias { get; }
    }
}
