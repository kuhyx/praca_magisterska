using UnityEngine;

namespace Magisterka.BulletHell
{
    /// <summary>
    /// Ensures the runtime bootstrapper exists even if the scene is empty.
    /// </summary>
    public static class GameBootstrap
    {
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void EnsureInitializer()
        {
            if (Object.FindFirstObjectByType<GameInitializer>() != null)
            {
                return;
            }

            var go = new GameObject("GameInitializer");
            go.AddComponent<GameInitializer>();
            Object.DontDestroyOnLoad(go);
        }
    }
}
