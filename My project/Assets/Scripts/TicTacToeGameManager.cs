using System.Collections.Generic;
using UnityEngine;

namespace TicTacToe3D
{
    public class TicTacToeGameManager : MonoBehaviour
    {
        public enum Player
        {
            None = 0,
            X,
            O
        }

        [Header("Board Layout")]
        [SerializeField] private int gridSize = 3;
        [SerializeField] private float tileSize = 1.0f;
        [SerializeField] private float tileHeight = 0.15f;
        [SerializeField] private float tileSpacing = 1.1f;
        [SerializeField] private Transform boardRoot;

        [Header("Visuals")]
        [SerializeField] private Color boardBaseColor = new Color(0.18f, 0.22f, 0.26f, 1f);
        [SerializeField] private Color boardHoverColor = new Color(0.28f, 0.75f, 0.69f, 1f);
        [SerializeField] private Color boardWinColor = new Color(0.94f, 0.77f, 0.38f, 1f);
        [SerializeField] private Color xMarkerColor = new Color(0.89f, 0.22f, 0.22f, 1f);
        [SerializeField] private Color oMarkerColor = new Color(0.22f, 0.35f, 0.89f, 1f);

        [Header("Gameplay")]
        [SerializeField] private float markerHeight = 0.55f;
        [SerializeField] private bool allowDiagonalWin = true;

        private readonly List<Tile> tiles = new List<Tile>();
        private Player[,] boardState;
        private Player currentPlayer = Player.X;
        private bool isGameOver;
        private readonly List<Tile> winningTiles = new List<Tile>();

        public Color BaseColor => boardBaseColor;
        public Color HoverColor => boardHoverColor;
        public Color WinColor => boardWinColor;
        public Color XColor => xMarkerColor;
        public Color OColor => oMarkerColor;
        public float MarkerHeight => markerHeight;

        private void Awake()
        {            
            if (gridSize < 3)
            {
                gridSize = 3;
            }

            if (boardRoot == null)
            {
                boardRoot = transform;
            }

            boardState = new Player[gridSize, gridSize];
            BuildBoard();
            UpdateStatusMessage();
        }

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.R))
            {
                ResetGame();
            }
        }

        private void OnGUI()
        {
            var style = new GUIStyle(GUI.skin.box)
            {
                fontSize = 24,
                alignment = TextAnchor.MiddleCenter,
                wordWrap = true
            };

            GUILayout.BeginArea(new Rect(20f, 20f, 280f, 120f));
            GUILayout.Box(GetStatusMessage(), style);
            GUILayout.EndArea();
        }

        public bool CanInteract(Vector2Int coordinates)
        {
            return !isGameOver && boardState[coordinates.x, coordinates.y] == Player.None;
        }

        public void TryPlay(Vector2Int coordinates, Tile tile)
        {
            if (!CanInteract(coordinates))
            {
                return;
            }

            boardState[coordinates.x, coordinates.y] = currentPlayer;
            tile.AttachMarker(CreateMarker(currentPlayer, tile.transform));

            if (DidPlayerWin(currentPlayer))
            {
                isGameOver = true;
                HighlightWinningTiles();
                UpdateStatusMessage();
                return;
            }

            if (IsBoardFull())
            {
                isGameOver = true;
                UpdateStatusMessage();
                return;
            }

            currentPlayer = currentPlayer == Player.X ? Player.O : Player.X;
            UpdateStatusMessage();
        }

        public void NotifyHoverEnter(Tile tile)
        {
            if (!isGameOver && CanInteract(tile.Coordinates))
            {
                tile.SetColor(boardHoverColor);
            }
        }

        public void NotifyHoverExit(Tile tile)
        {
            if (isGameOver && winningTiles.Contains(tile))
            {
                tile.SetColor(boardWinColor);
            }
            else
            {
                tile.SetColor(boardBaseColor);
            }
        }

        private void BuildBoard()
        {
            foreach (var tile in tiles)
            {
                if (tile != null)
                {
                    Destroy(tile.gameObject);
                }
            }

            tiles.Clear();
            boardState = new Player[gridSize, gridSize];

            for (int x = 0; x < gridSize; x++)
            {
                for (int y = 0; y < gridSize; y++)
                {
                    var tileObject = GameObject.CreatePrimitive(PrimitiveType.Cube);
                    tileObject.name = $"Tile_{x}_{y}";
                    tileObject.transform.SetParent(boardRoot, false);
                    tileObject.transform.localScale = new Vector3(tileSize, tileHeight, tileSize);
                    tileObject.transform.localPosition = new Vector3(
                        (x - (gridSize - 1) * 0.5f) * tileSpacing,
                        tileHeight * 0.5f,
                        (y - (gridSize - 1) * 0.5f) * tileSpacing
                    );

                    var tile = tileObject.AddComponent<Tile>();
                    tile.Initialize(this, new Vector2Int(x, y), boardBaseColor);
                    tiles.Add(tile);
                }
            }
        }

        private GameObject CreateMarker(Player player, Transform parent)
        {
            var markerRoot = new GameObject(player.ToString());
            markerRoot.transform.SetParent(parent, false);
            markerRoot.transform.localPosition = Vector3.up * markerHeight;

            if (player == Player.X)
            {
                BuildCross(markerRoot.transform, xMarkerColor);
            }
            else
            {
                BuildSphere(markerRoot.transform, oMarkerColor);
            }

            return markerRoot;
        }

        private void BuildCross(Transform parent, Color color)
        {
            CreateBar(parent, Quaternion.Euler(0f, 0f, 45f), color);
            CreateBar(parent, Quaternion.Euler(0f, 0f, -45f), color);
        }

        private void BuildSphere(Transform parent, Color color)
        {
            var sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            sphere.transform.SetParent(parent, false);
            sphere.transform.localScale = new Vector3(0.6f, 0.25f, 0.6f);

            var renderer = sphere.GetComponent<Renderer>();
            renderer.sharedMaterial = new Material(renderer.sharedMaterial)
            {
                color = color
            };

            var collider = sphere.GetComponent<Collider>();
            if (collider != null)
            {
                Destroy(collider);
            }
        }

        private void CreateBar(Transform parent, Quaternion rotation, Color color)
        {
            var bar = GameObject.CreatePrimitive(PrimitiveType.Cube);
            bar.transform.SetParent(parent, false);
            bar.transform.localRotation = rotation;
            bar.transform.localScale = new Vector3(0.15f, 0.15f, 0.9f);

            var renderer = bar.GetComponent<Renderer>();
            renderer.sharedMaterial = new Material(renderer.sharedMaterial)
            {
                color = color
            };

            var collider = bar.GetComponent<Collider>();
            if (collider != null)
            {
                Destroy(collider);
            }
        }

        private bool DidPlayerWin(Player player)
        {
            winningTiles.Clear();

            // Rows and columns
            for (int i = 0; i < gridSize; i++)
            {
                if (IsFullLine(player, true, i))
                {
                    return true;
                }

                if (IsFullLine(player, false, i))
                {
                    return true;
                }
            }

            if (allowDiagonalWin)
            {
                if (IsFullDiagonal(player, true))
                {
                    return true;
                }

                if (IsFullDiagonal(player, false))
                {
                    return true;
                }
            }

            winningTiles.Clear();
            return false;
        }

        private bool IsFullLine(Player player, bool horizontal, int index)
        {
            var temp = new List<Tile>();

            for (int i = 0; i < gridSize; i++)
            {
                int x = horizontal ? i : index;
                int y = horizontal ? index : i;

                if (boardState[x, y] != player)
                {
                    return false;
                }

                temp.Add(GetTile(x, y));
            }

            winningTiles.Clear();
            winningTiles.AddRange(temp);
            return true;
        }

        private bool IsFullDiagonal(Player player, bool mainDiagonal)
        {
            var temp = new List<Tile>();

            for (int i = 0; i < gridSize; i++)
            {
                int x = mainDiagonal ? i : i;
                int y = mainDiagonal ? i : (gridSize - 1) - i;

                if (boardState[x, y] != player)
                {
                    return false;
                }

                temp.Add(GetTile(x, y));
            }

            winningTiles.Clear();
            winningTiles.AddRange(temp);
            return true;
        }

        private Tile GetTile(int x, int y)
        {
            return tiles[y + x * gridSize];
        }

        private bool IsBoardFull()
        {
            for (int x = 0; x < gridSize; x++)
            {
                for (int y = 0; y < gridSize; y++)
                {
                    if (boardState[x, y] == Player.None)
                    {
                        return false;
                    }
                }
            }

            return true;
        }

        private void HighlightWinningTiles()
        {
            foreach (var tile in winningTiles)
            {
                tile.SetColor(boardWinColor);
            }
        }

        private void ResetGame()
        {
            for (int x = 0; x < gridSize; x++)
            {
                for (int y = 0; y < gridSize; y++)
                {
                    boardState[x, y] = Player.None;
                }
            }

            foreach (var tile in tiles)
            {
                tile.ResetTile(boardBaseColor);
            }

            winningTiles.Clear();
            isGameOver = false;
            currentPlayer = Player.X;
            UpdateStatusMessage();
        }

        private string GetStatusMessage()
        {
            if (!isGameOver)
            {
                return $"Current Player: {currentPlayer}\nClick a tile to place a marker.\nPress R to reset.";
            }

            if (winningTiles.Count > 0)
            {
                return $"Player {currentPlayer} wins!\nPress R to play again.";
            }

            return "It's a draw!\nPress R to play again.";
        }

        private void UpdateStatusMessage()
        {
            // Intentionally left blank; OnGUI queries status message when needed.
        }
    }
}
