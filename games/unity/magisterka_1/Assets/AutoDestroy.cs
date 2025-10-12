using UnityEngine;

public class AutoDestroy : MonoBehaviour
{
    [SerializeField] private float lifetime = 1.5f;

    private void OnEnable()
    {
        Invoke(nameof(DestroySelf), lifetime);
    }

    private void OnDisable()
    {
        CancelInvoke();
    }

    private void DestroySelf()
    {
        Destroy(gameObject);
    }
}
