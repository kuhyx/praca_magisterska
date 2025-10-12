using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Builds a procedural starfield and scrolls it endlessly.
    /// </summary>
    public class BackgroundScroller : MonoBehaviour
    {
        [SerializeField] private float scrollSpeed = 2f;
        [SerializeField] private float parallaxFactor = 0.6f;
        [SerializeField] private float tileHeight = 30f;

        private Transform _tileA;
        private Transform _tileB;
        private float _resetY;
        private float _cameraWidth;

        public static BackgroundScroller Create(Camera targetCamera, Transform parent)
        {
            var go = new GameObject("BackgroundScroller");
            go.transform.SetParent(parent, false);
            var scroller = go.AddComponent<BackgroundScroller>();
            scroller.Build(targetCamera);
            return scroller;
        }

        private void Build(Camera cam)
        {
            if (cam == null)
            {
                cam = Camera.main;
            }

            float height = cam.orthographicSize * 2f;
            _cameraWidth = height * cam.aspect;
            _resetY = -tileHeight;

            var sprite = GenerateStarSprite((int)(_cameraWidth * 16f), (int)(tileHeight * 16f));

            _tileA = CreateTile("Starfield_A", sprite, 0f);
            _tileB = CreateTile("Starfield_B", sprite, tileHeight);
        }

        private Transform CreateTile(string name, Sprite sprite, float yOffset)
        {
            var tile = new GameObject(name);
            tile.transform.SetParent(transform, false);
            tile.transform.position = new Vector3(0f, yOffset, 10f);
            var renderer = tile.AddComponent<SpriteRenderer>();
            renderer.sprite = sprite;
            renderer.sortingOrder = -100;
            renderer.color = new Color(0.7f, 0.7f, 0.7f, 0.8f);
            float scaleX = (_cameraWidth + 6f) / sprite.bounds.size.x;
            float scaleY = tileHeight / sprite.bounds.size.y;
            tile.transform.localScale = new Vector3(scaleX, scaleY, 1f);
            return tile.transform;
        }

        private void Update()
        {
            float delta = scrollSpeed * Time.deltaTime;
            ScrollTile(_tileA, delta);
            ScrollTile(_tileB, delta * parallaxFactor);

            Recycle(_tileA);
            Recycle(_tileB);
        }

        private void ScrollTile(Transform tile, float delta)
        {
            if (tile == null)
            {
                return;
            }

            tile.Translate(Vector3.down * delta, Space.World);
        }

        private void Recycle(Transform tile)
        {
            if (tile == null)
            {
                return;
            }

            if (tile.position.y <= _resetY)
            {
                tile.Translate(Vector3.up * (tileHeight * 2f), Space.World);
            }
        }

        private static Sprite GenerateStarSprite(int width, int height)
        {
            width = Mathf.Clamp(width, 128, 2048);
            height = Mathf.Clamp(height, 128, 4096);

            var texture = new Texture2D(width, height, TextureFormat.RGBA32, false)
            {
                filterMode = FilterMode.Bilinear,
                wrapMode = TextureWrapMode.Repeat
            };

            var pixels = new Color[width * height];
            var background = new Color(0.03f, 0.04f, 0.08f, 1f);

            for (int i = 0; i < pixels.Length; i++)
            {
                pixels[i] = background;
            }

            int starCount = (width * height) / 45;
            for (int i = 0; i < starCount; i++)
            {
                int x = Random.Range(0, width);
                int y = Random.Range(0, height);
                float intensity = Random.Range(0.6f, 1.2f);
                var color = new Color(intensity, intensity, intensity, 1f);
                pixels[x + y * width] = color;
            }

            texture.SetPixels(pixels);
            texture.Apply();

            return Sprite.Create(texture, new Rect(0, 0, width, height), new Vector2(0.5f, 0.5f), 64f);
        }
    }
}
