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

            var scoreManager = new GameObject("ScoreManager").AddComponent<ScoreManager>();
            var scoreText = CreateScoreUI();
            scoreManager.Initialize(scoreText);

            var pools = new GameObject("BulletPools").transform;
            pools.SetParent(root, false);

            var playerPool = BulletPool.Create(pools, "PlayerBullets", new Color(0.35f, 0.9f, 1f, 1f), Faction.Player, 600);
            var enemyPool = BulletPool.Create(pools, "EnemyBullets", new Color(1f, 0.4f, 0.2f, 1f), Faction.Enemy, 1200);

            var player = PlayerController.CreatePlayer(root, playerPool, bounds);

            var spawnerGO = new GameObject("EnemySpawner");
            spawnerGO.transform.SetParent(root, false);
            var spawner = spawnerGO.AddComponent<EnemySpawner>();
            spawner.Initialize(cam, enemyPool, player, bounds);
        }

        private Text CreateScoreUI()
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
            label.fontSize = 32;
            label.alignment = TextAnchor.UpperLeft;
            label.color = Color.white;
            label.text = "Score: 0";

            var rect = label.rectTransform;
            rect.anchorMin = new Vector2(0f, 1f);
            rect.anchorMax = new Vector2(0f, 1f);
            rect.pivot = new Vector2(0f, 1f);
            rect.anchoredPosition = new Vector2(20f, -20f);

            canvasGO.transform.SetParent(transform, false);
            return label;
        }
    }
}
