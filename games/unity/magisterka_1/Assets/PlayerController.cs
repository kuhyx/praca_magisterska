using UnityEngine;


public class PlayerController : MonoBehaviour
{
    public GameObject bulletPrefab;
    public Transform shootPoint;
    public float speed = 5f;

    void Update()
    {
        float moveX = Input.GetAxis("Horizontal");
        float moveY = Input.GetAxis("Vertical");
        transform.position += new Vector3(moveX, moveY, 0) * speed * Time.deltaTime;
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Instantiate(bulletPrefab, shootPoint.position, Quaternion.identity);
        }
    }
}