using UnityEngine;

public class Bullet : MonoBehaviour
{
    public float speed = 10f;

    void Update()
    {
        transform.Translate(Vector3.up * speed * Time.deltaTime);
        if (transform.position.y > 10) Destroy(gameObject); // Out of bounds
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        Debug.Log($"Bullet hit: {other.name} with tag: {other.tag}");
        if (other.gameObject.GetComponent<Enemy>() != null)
        {
            Debug.Log("Enemy destroyed!");
            Destroy(other.gameObject);
            Destroy(gameObject);
        }
    }   
}
