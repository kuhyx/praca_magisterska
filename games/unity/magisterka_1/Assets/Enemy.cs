using UnityEngine;

public class Enemy : MonoBehaviour
{
    public float speed = 2f;

    void Update()
    {
        transform.Translate(Vector3.down * speed * Time.deltaTime);
        if (transform.position.y < -10) Destroy(gameObject); // Out of bounds
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        Debug.Log($"Enemy hit: {other.name} with tag: {other.tag}");
        if (other.gameObject.GetComponent<Player>() != null)
        {
            Destroy(other.gameObject);
        }
    }
}