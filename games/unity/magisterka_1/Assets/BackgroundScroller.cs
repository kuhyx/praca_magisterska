using UnityEngine;

public class BackgroundScroller : MonoBehaviour
{
    [SerializeField] private float scrollSpeed = 2f;
    [SerializeField] private float tileSizeY = 20f;
    [SerializeField] private bool randomizeOffset;

    private Vector3 startPosition;

    private void Start()
    {
        startPosition = transform.position;
        if (randomizeOffset)
        {
            float initialOffset = Random.Range(0f, tileSizeY);
            startPosition -= Vector3.up * initialOffset;
        }
    }

    private void Update()
    {
        float newPosition = Mathf.Repeat(Time.time * scrollSpeed, tileSizeY);
        transform.position = startPosition + Vector3.down * newPosition;
    }
}
