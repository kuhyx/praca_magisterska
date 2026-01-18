#!/bin/bash
#
# Unity Project Static Code Analyzer
# Uses Microsoft.Unity.Analyzers for Unity-specific checks
#
# Usage: ./analyze_unity_project.sh [path_to_unity_project]
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="${1:-$SCRIPT_DIR/magisterka_1}"
ANALYZER_VERSION="1.19.0"
TOOLS_DIR="$SCRIPT_DIR/.unity-analyzers"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Unity Project Static Code Analyzer${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# ============================================
# Step 1: Check prerequisites
# ============================================
echo -e "${YELLOW}[1/5] Checking prerequisites...${NC}"

# Check if .NET SDK is installed
if ! command -v dotnet &> /dev/null; then
    echo -e "${RED}ERROR: .NET SDK is not installed.${NC}"
    echo ""
    echo "Install .NET SDK using one of these methods:"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    sudo apt-get update && sudo apt-get install -y dotnet-sdk-8.0"
    echo ""
    echo "  Fedora:"
    echo "    sudo dnf install dotnet-sdk-8.0"
    echo ""
    echo "  Arch Linux:"
    echo "    sudo pacman -S dotnet-sdk"
    echo ""
    echo "  Or download from: https://dotnet.microsoft.com/download"
    exit 1
fi

DOTNET_VERSION=$(dotnet --version)
echo -e "  ${GREEN}✓${NC} .NET SDK found: $DOTNET_VERSION"

# Check if project path exists
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}ERROR: Unity project not found at: $PROJECT_PATH${NC}"
    echo "Usage: $0 [path_to_unity_project]"
    exit 1
fi

# Check if it's a Unity project (has Assets folder)
if [ ! -d "$PROJECT_PATH/Assets" ]; then
    echo -e "${RED}ERROR: Not a valid Unity project (no Assets folder found)${NC}"
    exit 1
fi

# Get absolute path
PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)
echo -e "  ${GREEN}✓${NC} Unity project found: $PROJECT_PATH"

# ============================================
# Step 2: Create analyzer project with Unity stubs
# ============================================
echo ""
echo -e "${YELLOW}[2/5] Setting up analyzer environment...${NC}"

mkdir -p "$TOOLS_DIR"

# Create Unity stub file that provides minimal definitions for compilation
cat > "$TOOLS_DIR/UnityStubs.cs" << 'STUBEOF'
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
STUBEOF

echo -e "  ${GREEN}✓${NC} Unity stubs created"

# ============================================
# Step 3: Collect C# source files
# ============================================
echo ""
echo -e "${YELLOW}[3/5] Collecting C# source files...${NC}"

# Find all .cs files in Assets folder (excluding generated/editor scripts if needed)
CS_FILES=$(find "$PROJECT_PATH/Assets" -name "*.cs" -type f ! -path "*/Editor/*" 2>/dev/null)
CS_COUNT=$(echo "$CS_FILES" | grep -c "\.cs$" || echo "0")

if [ "$CS_COUNT" -eq 0 ]; then
    echo -e "${RED}ERROR: No C# files found in $PROJECT_PATH/Assets${NC}"
    exit 1
fi

echo -e "  ${GREEN}✓${NC} Found $CS_COUNT C# files"

# List the files being analyzed
echo -e "  Files to analyze:"
echo "$CS_FILES" | while read -r file; do
    echo -e "    - $(basename "$file")"
done

# Create project file with source files
cat > "$TOOLS_DIR/UnityAnalyzer.csproj" << EOF
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.1</TargetFramework>
    <LangVersion>9.0</LangVersion>
    <Nullable>disable</Nullable>
    <TreatWarningsAsErrors>false</TreatWarningsAsErrors>
    <!-- Suppress common Unity-related warnings that aren't real issues -->
    <NoWarn>CS0649;CS0414;CS0169;CS0067;CS8618;CS0626;CS0108</NoWarn>
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
    <!-- Output analysis results in SARIF format -->
    <ErrorLog>$TOOLS_DIR/analysis-results.sarif,version=2.1</ErrorLog>
  </PropertyGroup>

  <!-- Unity Analyzers - the main tool -->
  <ItemGroup>
    <PackageReference Include="Microsoft.Unity.Analyzers" Version="$ANALYZER_VERSION">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
  </ItemGroup>

  <!-- Unity stubs (local file providing type definitions) -->
  <ItemGroup>
    <Compile Include="UnityStubs.cs" />
  </ItemGroup>

  <!-- Source files from Unity project -->
  <ItemGroup>
EOF

echo "$CS_FILES" | while read -r file; do
    if [ -n "$file" ]; then
        echo "    <Compile Include=\"$file\" />" >> "$TOOLS_DIR/UnityAnalyzer.csproj"
    fi
done

cat >> "$TOOLS_DIR/UnityAnalyzer.csproj" << 'EOF'
  </ItemGroup>
</Project>
EOF

# ============================================
# Step 4: Restore packages and run analysis
# ============================================
echo ""
echo -e "${YELLOW}[4/5] Running static analysis...${NC}"
echo -e "  (This may take a moment on first run while downloading packages)"
echo ""

cd "$TOOLS_DIR"

# Restore packages
dotnet restore --verbosity quiet 2>/dev/null || true

# Run build (which triggers analyzers)
BUILD_OUTPUT="$TOOLS_DIR/build-output.txt"
dotnet build --no-restore /p:TreatWarningsAsErrors=false 2>&1 | tee "$BUILD_OUTPUT"

# ============================================
# Step 5: Parse and display results
# ============================================
echo ""
echo -e "${YELLOW}[5/5] Analysis Results${NC}"
echo -e "${BLUE}========================================${NC}"

# Count different types of diagnostics
UNITY_WARNINGS=$(grep -oE "UNT[0-9]{4}" "$BUILD_OUTPUT" | wc -l || echo "0")
CS_WARNINGS=$(grep -E "warning CS[0-9]{4}" "$BUILD_OUTPUT" | wc -l || echo "0")
CS_ERRORS=$(grep -E "error CS[0-9]{4}" "$BUILD_OUTPUT" | wc -l || echo "0")

echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  Unity-specific issues (UNT*): ${YELLOW}$UNITY_WARNINGS${NC}"
echo -e "  C# warnings (CS*):            ${YELLOW}$CS_WARNINGS${NC}"
echo -e "  C# errors (CS*):              ${RED}$CS_ERRORS${NC}"
echo ""

# Show Unity-specific diagnostics in detail
if [ "$UNITY_WARNINGS" -gt 0 ]; then
    echo -e "${BLUE}Unity-Specific Diagnostics Found:${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
    grep -E "UNT[0-9]{4}" "$BUILD_OUTPUT" | sort -u | while read -r line; do
        echo -e "  ${YELLOW}→${NC} $line"
    done
    echo ""
fi

# Show any real C# errors (not from stubs)
if grep -q "error CS" "$BUILD_OUTPUT"; then
    REAL_ERRORS=$(grep "error CS" "$BUILD_OUTPUT" | grep -v "UnityStubs.cs" || true)
    if [ -n "$REAL_ERRORS" ]; then
        echo -e "${RED}C# Errors Found:${NC}"
        echo "$REAL_ERRORS" | head -20
        echo ""
    fi
fi

# Common Unity Analyzer diagnostic codes reference
echo -e "${BLUE}Common Unity Analyzer Codes Reference:${NC}"
echo "  UNT0001: Empty Unity message (Update, Start, etc.)"
echo "  UNT0002: Inefficient tag comparison"
echo "  UNT0003: Incorrect usage of GetComponent"
echo "  UNT0004: Time.fixedDeltaTime used in Update"
echo "  UNT0005: Time.deltaTime used in FixedUpdate"
echo "  UNT0006: Incorrect message signature"
echo "  UNT0007: Null propagation on Unity objects"
echo "  UNT0008: Null coalescing on Unity objects"
echo "  UNT0009: Missing static constructor for InitializeOnLoad"
echo "  UNT0010: Component instance creation (use AddComponent)"
echo "  UNT0011: ScriptableObject instance creation (use CreateInstance)"
echo "  UNT0012: Unused coroutine return value"
echo "  UNT0013: Invalid SerializeField attribute"
echo "  UNT0014: GetComponent with non-Component type"
echo "  UNT0015: Incorrect method signature with ContextMenu"
echo "  UNT0016: Unsafe way to get position/rotation"
echo "  UNT0017: SetPixels invocation"
echo "  UNT0018: System.Reflection features"
echo "  UNT0019: Indirect calling of SendMessage"
echo "  UNT0020: MenuItem with invalid static method"
echo "  UNT0021: OnGUI allocation"
echo "  UNT0022: Inefficient position/rotation multiplication"
echo "  UNT0023: Coalescing assignment on Unity objects"
echo "  UNT0024: Obsolete Unity methods"
echo "  UNT0025: Input.GetKey in MonoBehaviour FixedUpdate"
echo "  UNT0026: GetComponent always allocates"
echo ""

# Output file locations
echo -e "${GREEN}Analysis complete!${NC}"
echo ""
echo "Output files:"
echo "  Build log:    $BUILD_OUTPUT"
if [ -f "$TOOLS_DIR/analysis-results.sarif" ]; then
    echo "  SARIF report: $TOOLS_DIR/analysis-results.sarif"
fi
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Tip: For IDE integration in Unity:${NC}"
echo "  1. Open Unity project, then open any .cs file in VS/Rider"
echo "  2. Analyzers auto-run via com.unity.ide.visualstudio package"
echo "  3. Or manually add Microsoft.Unity.Analyzers NuGet to .csproj"
echo -e "${BLUE}========================================${NC}"
