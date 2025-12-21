// Unity API Stubs for static analysis
// These provide minimal type definitions so the analyzer can check code
// without needing actual Unity assemblies

using System;
using System.Collections;
using System.Collections.Generic;

namespace UnityEngine
{
    public class Object { 
        public string name;
        public static void Destroy(Object obj) { }
        public static void DontDestroyOnLoad(Object target) { }
        public static T FindObjectOfType<T>() where T : Object => default;
        public static T[] FindObjectsOfType<T>() where T : Object => default;
        public static T Instantiate<T>(T original) where T : Object => default;
        public static T Instantiate<T>(T original, Vector3 position, Quaternion rotation) where T : Object => default;
    }
    
    public class Component : Object { 
        public GameObject gameObject;
        public Transform transform;
        public T GetComponent<T>() => default;
        public T[] GetComponents<T>() => default;
        public T GetComponentInChildren<T>() => default;
        public T GetComponentInParent<T>() => default;
    }
    
    public class Behaviour : Component { public bool enabled; public bool isActiveAndEnabled; }
    public class MonoBehaviour : Behaviour { 
        protected void Invoke(string methodName, float time) { }
        protected void CancelInvoke() { }
        protected void CancelInvoke(string methodName) { }
        protected Coroutine StartCoroutine(IEnumerator routine) => null;
        protected Coroutine StartCoroutine(string methodName) => null;
        protected void StopCoroutine(Coroutine routine) { }
        protected void StopAllCoroutines() { }
    }
    public class ScriptableObject : Object { }
    
    public class GameObject : Object { 
        public Transform transform;
        public bool activeSelf;
        public bool activeInHierarchy;
        public GameObject() { }
        public GameObject(string name) { }
        public T GetComponent<T>() => default;
        public T AddComponent<T>() where T : Component => default;
        public void SetActive(bool value) { }
    }
    
    public class Transform : Component, IEnumerable {
        public Vector3 position;
        public Vector3 localPosition;
        public Quaternion rotation;
        public Quaternion localRotation;
        public Vector3 localScale;
        public Transform parent;
        public int childCount;
        public void SetParent(Transform parent) { }
        public Transform GetChild(int index) => default;
        public IEnumerator GetEnumerator() => null;
    }
    
    public struct Vector2 {
        public float x, y;
        public Vector2(float x, float y) { this.x = x; this.y = y; }
        public static Vector2 up => new Vector2(0, 1);
        public static Vector2 down => new Vector2(0, -1);
        public static Vector2 left => new Vector2(-1, 0);
        public static Vector2 right => new Vector2(1, 0);
        public static Vector2 zero => new Vector2(0, 0);
        public static Vector2 one => new Vector2(1, 1);
        public Vector2 normalized => this;
        public float magnitude => 0;
        public float sqrMagnitude => 0;
        public static Vector2 operator +(Vector2 a, Vector2 b) => default;
        public static Vector2 operator -(Vector2 a, Vector2 b) => default;
        public static Vector2 operator *(Vector2 a, float d) => default;
        public static Vector2 operator *(float d, Vector2 a) => default;
        public static implicit operator Vector3(Vector2 v) => default;
    }
    
    public struct Vector3 {
        public float x, y, z;
        public Vector3(float x, float y, float z) { this.x = x; this.y = y; this.z = z; }
        public static Vector3 up => new Vector3(0, 1, 0);
        public static Vector3 down => new Vector3(0, -1, 0);
        public static Vector3 forward => new Vector3(0, 0, 1);
        public static Vector3 back => new Vector3(0, 0, -1);
        public static Vector3 left => new Vector3(-1, 0, 0);
        public static Vector3 right => new Vector3(1, 0, 0);
        public static Vector3 zero => new Vector3(0, 0, 0);
        public static Vector3 one => new Vector3(1, 1, 1);
        public Vector3 normalized => this;
        public static Vector3 operator +(Vector3 a, Vector3 b) => default;
        public static Vector3 operator -(Vector3 a, Vector3 b) => default;
        public static Vector3 operator *(Vector3 a, float d) => default;
        public static Vector3 operator *(float d, Vector3 a) => default;
        public static implicit operator Vector2(Vector3 v) => default;
    }
    
    public struct Quaternion {
        public float x, y, z, w;
        public static Quaternion identity => default;
        public static Quaternion Euler(float x, float y, float z) => default;
        public static Vector3 operator *(Quaternion rotation, Vector3 point) => default;
    }
    
    public struct Color {
        public float r, g, b, a;
        public Color(float r, float g, float b, float a = 1f) { this.r = r; this.g = g; this.b = b; this.a = a; }
        public static Color white => new Color(1, 1, 1);
        public static Color black => new Color(0, 0, 0);
        public static Color red => new Color(1, 0, 0);
        public static Color green => new Color(0, 1, 0);
        public static Color blue => new Color(0, 0, 1);
    }
    
    public struct Rect { public float x, y, width, height; }
    
    public class Collider : Component { }
    public class Collider2D : Component { public new T GetComponent<T>() => default; }
    public class BoxCollider2D : Collider2D { }
    public class CircleCollider2D : Collider2D { }
    public class Rigidbody : Component { }
    public class Rigidbody2D : Component { }
    
    public class SpriteRenderer : Component { public Sprite sprite; public Color color; }
    public class Sprite : Object { }
    
    public static class Time {
        public static float time => 0;
        public static float deltaTime => 0;
        public static float fixedDeltaTime => 0;
        public static float unscaledDeltaTime => 0;
        public static float timeScale { get; set; }
    }
    
    public static class Input {
        public static float GetAxis(string axisName) => 0;
        public static float GetAxisRaw(string axisName) => 0;
        public static bool GetKey(KeyCode key) => false;
        public static bool GetKeyDown(KeyCode key) => false;
        public static bool GetKeyUp(KeyCode key) => false;
        public static bool GetMouseButton(int button) => false;
        public static bool GetMouseButtonDown(int button) => false;
        public static bool GetMouseButtonUp(int button) => false;
        public static Vector3 mousePosition => default;
    }
    
    public enum KeyCode { 
        None, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
        Alpha0, Alpha1, Alpha2, Alpha3, Alpha4, Alpha5, Alpha6, Alpha7, Alpha8, Alpha9,
        Space, Return, Escape, Tab, LeftShift, RightShift, LeftControl, RightControl,
        UpArrow, DownArrow, LeftArrow, RightArrow
    }
    
    public static class Mathf {
        public const float PI = 3.14159265f;
        public static float Abs(float f) => f < 0 ? -f : f;
        public static float Sin(float f) => 0;
        public static float Cos(float f) => 0;
        public static float Sqrt(float f) => 0;
        public static float Clamp(float value, float min, float max) => value;
        public static float Clamp01(float value) => value;
        public static int Clamp(int value, int min, int max) => value;
        public static float Max(float a, float b) => a > b ? a : b;
        public static float Min(float a, float b) => a < b ? a : b;
        public static int Max(int a, int b) => a > b ? a : b;
        public static int Min(int a, int b) => a < b ? a : b;
        public static int FloorToInt(float f) => (int)f;
        public static int RoundToInt(float f) => (int)f;
        public static float Repeat(float t, float length) => t;
    }
    
    public static class Random {
        public static float Range(float min, float max) => min;
        public static int Range(int min, int max) => min;
        public static float value => 0;
    }
    
    public static class Debug {
        public static void Log(object message) { }
        public static void LogWarning(object message) { }
        public static void LogError(object message) { }
    }
    
    public static class Resources {
        public static T Load<T>(string path) where T : Object => default;
        public static T GetBuiltinResource<T>(string path) where T : Object => default;
    }
    
    public class WaitForSeconds : YieldInstruction {
        public WaitForSeconds(float seconds) { }
    }
    public class YieldInstruction { }
    public class Coroutine : YieldInstruction { }
    
    public class AnimationCurve {
        public float Evaluate(float time) => 0;
        public static AnimationCurve Linear(float timeStart, float valueStart, float timeEnd, float valueEnd) => new AnimationCurve();
    }
    
    [AttributeUsage(AttributeTargets.Field)]
    public class SerializeField : Attribute { }
    [AttributeUsage(AttributeTargets.Field)]
    public class HideInInspector : Attribute { }
    [AttributeUsage(AttributeTargets.Field | AttributeTargets.Class)]
    public class HeaderAttribute : Attribute { public HeaderAttribute(string header) { } }
    [AttributeUsage(AttributeTargets.Field)]
    public class RangeAttribute : Attribute { public RangeAttribute(float min, float max) { } }
    [AttributeUsage(AttributeTargets.Class)]
    public class RequireComponent : Attribute { public RequireComponent(Type type) { } }
    [AttributeUsage(AttributeTargets.Method)]
    public class RuntimeInitializeOnLoadMethodAttribute : Attribute { 
        public RuntimeInitializeOnLoadMethodAttribute() { }
        public RuntimeInitializeOnLoadMethodAttribute(RuntimeInitializeLoadType loadType) { }
    }
    public enum RuntimeInitializeLoadType { AfterSceneLoad, BeforeSceneLoad, AfterAssembliesLoaded, BeforeSplashScreen, SubsystemRegistration }
    
    public class Camera : Behaviour {
        public static Camera main => null;
        public float orthographicSize;
        public float fieldOfView;
        public float aspect;
        public Vector3 ScreenToWorldPoint(Vector3 position) => default;
        public Vector3 WorldToScreenPoint(Vector3 position) => default;
        public Ray ScreenPointToRay(Vector3 pos) => default;
    }
    public struct Ray { public Vector3 origin; public Vector3 direction; }
    
    public class Canvas : Behaviour {
        public RenderMode renderMode;
    }
    public enum RenderMode { ScreenSpaceOverlay, ScreenSpaceCamera, WorldSpace }
    public class CanvasScaler : Component { }
    public class GraphicRaycaster : Component { }
    public class RectTransform : Transform {
        public Vector2 anchorMin;
        public Vector2 anchorMax;
        public Vector2 pivot;
        public Vector2 anchoredPosition;
        public Vector2 sizeDelta;
    }
    
    public class Font : Object { }
}

namespace UnityEngine.UI
{
    public class Text : UnityEngine.Behaviour {
        public string text;
        public UnityEngine.Font font;
        public int fontSize;
        public UnityEngine.Color color;
        public TextAnchor alignment;
        public HorizontalWrapMode horizontalOverflow;
    }
    public enum TextAnchor { UpperLeft, UpperCenter, UpperRight, MiddleLeft, MiddleCenter, MiddleRight, LowerLeft, LowerCenter, LowerRight }
    public enum HorizontalWrapMode { Wrap, Overflow }
    public class Image : UnityEngine.Behaviour { }
    public class Button : UnityEngine.Behaviour { }
    public class Graphic : UnityEngine.Behaviour { }
}
