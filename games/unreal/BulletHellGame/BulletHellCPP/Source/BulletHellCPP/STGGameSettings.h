#pragma once

/**
 * STGGameSettings.h - Centralized game configuration
 * 
 * All game constants are defined here. Change values in ONE place
 * and they propagate to all systems automatically.
 * 
 * Usage: #include "STGGameSettings.h"
 *        float speed = STG::Default::PlayerMoveSpeed;
 */

namespace STG
{
    // ===== PLAY AREA =====
    namespace PlayArea
    {
        // Play area boundaries (centered at origin)
        constexpr float MinX = -850.0f;
        constexpr float MaxX = 850.0f;
        constexpr float MinY = -450.0f;
        constexpr float MaxY = 450.0f;
        
        // Derived values
        constexpr float Width = MaxX - MinX;      // 1700
        constexpr float Height = MaxY - MinY;     // 900
        constexpr float HalfWidth = Width / 2.0f;
        constexpr float HalfHeight = Height / 2.0f;
        
        // Spawn/despawn margins (beyond play area)
        constexpr float SpawnMarginX = 10.0f;     // Spawn just above visible edge
        constexpr float DespawnMarginX = 50.0f;   // How far below play area before despawn
    }

    // ===== GAME TIMING =====
    namespace Game
    {
        constexpr float DefaultDuration = 60.0f;  // 1 minute game
        constexpr float DebugQuickDuration = 10.0f;
    }

    // ===== PLAYER DEFAULTS =====
    namespace Player
    {
        constexpr float MoveSpeed = 750.0f;
        constexpr float BulletSpeed = 2200.0f;
        constexpr int32 MaxLives = 3;
        
        // Starting stats (weak!)
        constexpr float StartFireInterval = 0.5f;   // Slow firing at start
        constexpr int32 StartVolleySize = 1;        // Single bullet at start
        constexpr float StartVolleySpread = 0.0f;   // No spread with 1 bullet
        
        // Max stats (after all upgrades)
        constexpr float MaxFireInterval = 0.08f;    // Very fast
        constexpr int32 MaxVolleySize = 5;          // 5-bullet spread
        constexpr float MaxVolleySpread = 20.0f;    // Wide spread
        
        // Upgrade thresholds (score needed)
        constexpr int32 UpgradeScore1 = 100;   // 2 bullets, 0.35s
        constexpr int32 UpgradeScore2 = 300;   // 3 bullets, 0.20s
        constexpr int32 UpgradeScore3 = 600;   // 4 bullets, 0.12s
        constexpr int32 UpgradeScore4 = 1000;  // 5 bullets, 0.08s (max)
        
        // Bullet visuals
        constexpr float BulletScale = 0.06f;
        constexpr float BulletEmissive = 2.0f;
    }

    // ===== ENEMY DEFAULTS =====
    // Difficulty progression: Fodder → Runner → Turret → Tank
    namespace Enemy
    {
        // FODDER - Easiest: Very slow, NO bullets, dies in 1 hit
        // Shape: Tiny circle (small sphere)
        // Color: Green (easy target)
        namespace Fodder
        {
            constexpr int32 Health = 1;
            constexpr int32 ScoreValue = 10;
            constexpr float VerticalSpeed = 80.0f;     // Very slow
            constexpr float HorizontalAmplitude = 100.0f;
            constexpr float HorizontalFrequency = 0.5f;
            constexpr float FireInterval = 0.0f;       // NO shooting
            constexpr int32 BulletsPerBurst = 0;       // NO bullets
            constexpr float BurstSpread = 0.0f;
            constexpr float BulletSpeed = 0.0f;
        }
        
        // RUNNER - Fast but harmless: Quick, NO bullets, low HP
        // Shape: Small diamond (rotated square)
        // Color: Cyan (zippy)
        namespace Runner
        {
            constexpr int32 Health = 3;
            constexpr int32 ScoreValue = 25;
            constexpr float VerticalSpeed = 90.0f;     // Fast but manageable
            constexpr float HorizontalAmplitude = 300.0f;
            constexpr float HorizontalFrequency = 2.5f;
            constexpr float FireInterval = 0.0f;       // NO shooting
            constexpr int32 BulletsPerBurst = 0;       // NO bullets
            constexpr float BurstSpread = 0.0f;
            constexpr float BulletSpeed = 0.0f;
        }
        
        // TURRET - First shooter: Slow, shoots FEW bullets, medium tanky
        // Shape: Square (cube)
        // Color: Orange (warning)
        namespace Turret
        {
            constexpr int32 Health = 15;
            constexpr int32 ScoreValue = 75;
            constexpr float VerticalSpeed = 60.0f;     // Very slow
            constexpr float HorizontalAmplitude = 80.0f;
            constexpr float HorizontalFrequency = 0.4f;
            constexpr float FireInterval = 1.2f;       // Shoots slowly (gentle intro)
            constexpr int32 BulletsPerBurst = 4;       // Few bullets (first shooter!)
            constexpr float BurstSpread = 360.0f;      // 360° burst
            constexpr float BulletSpeed = 200.0f;      // Very slow bullets
        }
        
        // TANK - Hardest: Slow, bullet hell, very tanky
        // Shape: Large rectangle
        // Color: Red (danger!)
        namespace Tank
        {
            constexpr int32 Health = 50;
            constexpr int32 ScoreValue = 200;
            constexpr float VerticalSpeed = 40.0f;     // Crawling
            constexpr float HorizontalAmplitude = 50.0f;
            constexpr float HorizontalFrequency = 0.3f;
            constexpr float FireInterval = 0.3f;       // Rapid fire
            constexpr int32 BulletsPerBurst = 20;      // Many bullets
            constexpr float BurstSpread = 360.0f;      // Full spread
            constexpr float BulletSpeed = 175.0f;      // Slow bullets (halved again)
        }
        
        // Common enemy settings
        constexpr float BulletLifetime = 10.0f;        // Longer lifetime for slower bullets
        constexpr float DespawnY = PlayArea::MinX - 100.0f;  // Below play area
        
        // Bullet visuals (enemy) - BIG visually but SMALL hitbox for "grazing"
        constexpr float BulletVisualScale = 0.25f;     // Large visual (easy to see)
        constexpr float BulletCollisionRadius = 3.0f;  // Tiny hitbox (can "touch" without dying)
        constexpr float BulletEmissive = 8.0f;
    }

    // ===== SPAWNER SETTINGS =====
    namespace Spawner
    {
        constexpr float BaseSpawnInterval = 1.2f;     // Start slow
        constexpr float MinSpawnInterval = 0.08f;     // Very fast at end
        constexpr float FinalRushInterval = 0.03f;    // Insane for last 5 seconds
        constexpr float FinalRushDuration = 5.0f;     // Last 5 seconds = chaos
        constexpr int32 MaxSimultaneousEnemies = 200; // Allow more enemies
        constexpr float SpawnAreaHalfWidth = 200.0f;
        
        // X position where enemies spawn (above play area)
        constexpr float SpawnX = PlayArea::MaxX + PlayArea::SpawnMarginX;
    }

    // ===== CAMERA SETTINGS =====
    namespace Camera
    {
        constexpr float DefaultFOV = 60.0f;
        constexpr float DefaultHeight = 1500.0f;  // Fallback if auto-fit fails
        constexpr float DefaultMargin = 0.0f;     // No margin - show exactly play area
        constexpr float OrthoWidth = 2000.0f;
    }

    // ===== VFX SETTINGS =====
    namespace VFX
    {
        constexpr int32 DeathParticleCount = 500;
    }
}
