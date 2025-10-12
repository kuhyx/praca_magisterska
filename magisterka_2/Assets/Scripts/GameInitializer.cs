using Magisterka.BulletHell;
using UnityEngine;
using UnityEngine.UI;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Bootstraps the benchmark bullet hell scene entirely at runtime.
    /// </summary>
    public class GameInitializer : MonoBehaviour
    {
        [SerializeField] private float cameraSize = 6.5f;

        private struct HudElements
        {
            public Text Score;
            public Image[] Lives;
            public Text Status;
            public Text Timer;
            public Image DamageOverlay;
        }

        private void Awake()
        {
            BuildCamera();
            BuildGame();
        }

        private void BuildCamera()
        {
            var cam = Camera.main;
            if (cam == null)
            {
                cam = new GameObject("Main Camera").AddComponent<Camera>();
            }

            cam.tag = "MainCamera";
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = Color.black;
            cam.orthographic = true;
            cam.orthographicSize = cameraSize;
            cam.transform.position = new Vector3(0f, 0f, -10f);
        }

        private void BuildGame()
        {
            Application.targetFrameRate = 240;
            Cursor.visible = false;

            var cam = Camera.main;
            var bounds = new Vector2(cam.orthographicSize * cam.aspect, cam.orthographicSize);

            var root = new GameObject("GameRoot").transform;
            root.SetParent(transform, false);

            BackgroundScroller.Create(cam, root);

            var effectManager = new GameObject("EffectManager").AddComponent<EffectManager>();
            effectManager.Initialize(root);

            var scoreManagerGO = new GameObject("ScoreManager");
            scoreManagerGO.transform.SetParent(root, false);
            var scoreManager = scoreManagerGO.AddComponent<ScoreManager>();

            var pools = new GameObject("BulletPools").transform;
            pools.SetParent(root, false);

            var playerPool = BulletPool.Create(pools, "PlayerBullets", new Color(0.35f, 0.9f, 1f, 1f), Faction.Player, 400);
            var enemyPool = BulletPool.Create(pools, "EnemyBullets", new Color(1f, 0.4f, 0.2f, 1f), Faction.Enemy, 900);

            var player = PlayerController.CreatePlayer(root, playerPool, bounds);

            var hud = CreateHud(player.MaxLives);
            scoreManager.Initialize(hud.Score, hud.Lives, hud.Status, hud.DamageOverlay);
            scoreManager.SetLives(player.CurrentLives);

            var spawnerGO = new GameObject("EnemySpawner");
            spawnerGO.transform.SetParent(root, false);
            var spawner = spawnerGO.AddComponent<EnemySpawner>();
            spawner.Initialize(cam, enemyPool, player, bounds);

            var directorGO = new GameObject("GameDirector");
            directorGO.transform.SetParent(root, false);
            var director = directorGO.AddComponent<GameDirector>();
            director.Initialize(spawner, player, scoreManager, hud.Timer, 90f);
        }

        private HudElements CreateHud(int lives)
        {
            var canvasGO = new GameObject("Canvas");
            var canvas = canvasGO.AddComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvasGO.AddComponent<CanvasScaler>().uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            canvasGO.AddComponent<GraphicRaycaster>();

            var textGO = new GameObject("ScoreLabel");
            textGO.transform.SetParent(canvasGO.transform, false);
            var label = textGO.AddComponent<Text>();
            label.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            if (label.font == null)
            {
                label.font = Font.CreateDynamicFontFromOSFont("Arial", 32);
            }
            label.fontSize = 24;
            label.alignment = TextAnchor.UpperLeft;
            label.color = Color.white;
            label.text = "Score: 0";

            var rect = label.rectTransform;
            rect.anchorMin = new Vector2(0f, 1f);
            rect.anchorMax = new Vector2(0f, 1f);
            rect.pivot = new Vector2(0f, 1f);
            rect.anchoredPosition = new Vector2(12f, -12f);

            var livesGO = new GameObject("Lives");
            livesGO.transform.SetParent(canvasGO.transform, false);
            var livesRect = livesGO.AddComponent<RectTransform>();
            livesRect.anchorMin = new Vector2(0f, 1f);
            livesRect.anchorMax = new Vector2(0f, 1f);
            livesRect.pivot = new Vector2(0f, 1f);
            livesRect.anchoredPosition = new Vector2(12f, -40f);

            var lifeSprite = BuildLifeSprite();
            var lifeIcons = new Image[Mathf.Max(1, lives)];

            for (int i = 0; i < lifeIcons.Length; i++)
            {
                var iconGO = new GameObject($"Life_{i}");
                iconGO.transform.SetParent(livesGO.transform, false);
                var icon = iconGO.AddComponent<Image>();
                icon.sprite = lifeSprite;
                icon.color = new Color(0.3f + i * 0.05f, 0.85f, 1f, 0.9f);
                var iconRect = icon.rectTransform;
                iconRect.anchorMin = new Vector2(0f, 1f);
                iconRect.anchorMax = new Vector2(0f, 1f);
                iconRect.pivot = new Vector2(0f, 1f);
                iconRect.anchoredPosition = new Vector2(i * 26f, 0f);
                iconRect.sizeDelta = new Vector2(22f, 22f);
                lifeIcons[i] = icon;
            }

            var gameOverGO = new GameObject("GameOverLabel");
            gameOverGO.transform.SetParent(canvasGO.transform, false);
            var gameOver = gameOverGO.AddComponent<Text>();
            gameOver.font = label.font;
            gameOver.fontSize = 48;
            gameOver.alignment = TextAnchor.MiddleCenter;
            gameOver.color = new Color(1f, 0.55f, 0.55f, 1f);
            gameOver.text = "GAME OVER";
            gameOver.enabled = false;

            var goRect = gameOver.rectTransform;
            goRect.anchorMin = new Vector2(0.5f, 0.5f);
            goRect.anchorMax = new Vector2(0.5f, 0.5f);
            goRect.pivot = new Vector2(0.5f, 0.5f);
            goRect.anchoredPosition = Vector2.zero;

            var timerGO = new GameObject("TimerLabel");
            timerGO.transform.SetParent(canvasGO.transform, false);
            var timer = timerGO.AddComponent<Text>();
            timer.font = label.font;
            timer.fontSize = 24;
            timer.alignment = TextAnchor.UpperRight;
            timer.color = Color.white;
            timer.text = "05:00";

            var timerRect = timer.rectTransform;
            timerRect.anchorMin = new Vector2(1f, 1f);
            timerRect.anchorMax = new Vector2(1f, 1f);
            timerRect.pivot = new Vector2(1f, 1f);
            timerRect.anchoredPosition = new Vector2(-12f, -12f);

            var overlayGO = new GameObject("DamageOverlay");
            overlayGO.transform.SetParent(canvasGO.transform, false);
            var overlay = overlayGO.AddComponent<Image>();
            overlay.raycastTarget = false;
            overlay.color = new Color(1f, 0.2f, 0.2f, 0f);
            var overlayRect = overlay.rectTransform;
            overlayRect.anchorMin = Vector2.zero;
            overlayRect.anchorMax = Vector2.one;
            overlayRect.pivot = new Vector2(0.5f, 0.5f);
            overlayRect.offsetMin = Vector2.zero;
            overlayRect.offsetMax = Vector2.zero;

            overlayGO.transform.SetAsLastSibling();

            canvasGO.transform.SetParent(transform, false);
            return new HudElements
            {
                Score = label,
                Lives = lifeIcons,
                Status = gameOver,
                Timer = timer,
                DamageOverlay = overlay
            };
        }

        private static Sprite BuildLifeSprite()
        {
            const int size = 32;
            var texture = new Texture2D(size, size, TextureFormat.RGBA32, false)
            {
                filterMode = FilterMode.Bilinear
            };

            var center = new Vector2(size / 2f, size / 2f);
            var pixels = new Color[size * size];

            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    int index = x + y * size;
                    float dist = Vector2.Distance(center, new Vector2(x, y));
                    pixels[index] = dist <= size * 0.42f ? Color.white : new Color(0f, 0f, 0f, 0f);
                }
            }

            texture.SetPixels(pixels);
            texture.Apply();

            return Sprite.Create(texture, new Rect(0, 0, size, size), new Vector2(0.5f, 0.5f), 64f);
        }
    }
}
