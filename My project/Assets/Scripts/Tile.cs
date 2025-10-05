using UnityEngine;

namespace TicTacToe3D
{
    [RequireComponent(typeof(Renderer))]
    [RequireComponent(typeof(Collider))]
    public class Tile : MonoBehaviour
    {
        private TicTacToeGameManager manager;
        private Vector2Int coordinates;
        private Material runtimeMaterial;
        private GameObject currentMarker;
        private Color baseColor;

        public Vector2Int Coordinates => coordinates;

        public void Initialize(TicTacToeGameManager manager, Vector2Int coordinates, Color tileColor)
        {
            this.manager = manager;
            this.coordinates = coordinates;
            baseColor = tileColor;

            var renderer = GetComponent<Renderer>();
            runtimeMaterial = new Material(renderer.sharedMaterial)
            {
                color = tileColor
            };
            renderer.material = runtimeMaterial;

            var collider = GetComponent<Collider>();
            if (collider != null)
            {
                collider.isTrigger = false;
            }
        }

        public void AttachMarker(GameObject marker)
        {
            if (currentMarker != null)
            {
                Destroy(currentMarker);
            }

            currentMarker = marker;
            RemoveColliders(marker);
        }

        public void SetColor(Color color)
        {
            if (runtimeMaterial != null)
            {
                runtimeMaterial.color = color;
            }
        }

        public void ResetTile(Color color)
        {
            baseColor = color;
            SetColor(baseColor);

            if (currentMarker != null)
            {
                Destroy(currentMarker);
                currentMarker = null;
            }
        }

        private void RemoveColliders(GameObject root)
        {
            foreach (var collider in root.GetComponentsInChildren<Collider>())
            {
                Destroy(collider);
            }
        }

        private void OnMouseEnter()
        {
            manager?.NotifyHoverEnter(this);
        }

        private void OnMouseExit()
        {
            manager?.NotifyHoverExit(this);
        }

        private void OnMouseDown()
        {
            manager?.TryPlay(coordinates, this);
        }
    }
}
