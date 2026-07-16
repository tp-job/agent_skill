---
name: threejs-3d
description: >
  Build high-performance, production-grade Three.js and 3D web experiences. ALWAYS use this skill when the user mentions: Three.js, WebGL, WebGPU, 3D scene, 3D model, GLTF, GLB, OBJ, FBX, STL, shader, GLSL, TSL, vertex shader, fragment shader, particle system, procedural geometry, 3D animation, skeletal animation, morph target, animation mixer, environment map, HDRI, PBR material, physically based rendering, shadow, ambient occlusion, instanced mesh, raycasting, picking, interaction in 3D, camera rig, orbit controls, postprocessing, bloom, depth of field, FXAA, SMAA, tone mapping, color grading, 3D product viewer, configurator, 3D background, WebGL demo, spinning cube, Three Fiber, R3F, Drei, canvas 3D, point cloud, terrain generation, procedural mesh, GPU particles, compute shader, or anything involving rendering 3D graphics in the browser. Also trigger for: "make it look cinematic", "add glow", "add reflections", "realistic materials", "game-like graphics", "3D interactive experience". Produces modern r182+ code with correct memory management, delta-time animation, import maps, and professional visual quality.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Three.js r182 documentation & best practices (compiled 2026)
---

# Three.js & 3D Web — Professional Skill

Version: Three.js **r182** | Maintainer: Senior Leadership (FE + Design + QA + PM)

---

## 📋 PM — Scope & Acceptance Criteria

Every output from this skill MUST satisfy:

|#|Criterion|Owner|
|---|---|---|
|1|Uses import maps (never old CDN `<script src>`)|Frontend|
|2|Uses `renderer.setAnimationLoop()`, not manual RAF|Frontend|
|3|All motion driven by `clock.getDelta()` (frame-rate independent)|Frontend|
|4|Pixel ratio capped at `Math.min(devicePixelRatio, 2)`|Frontend|
|5|Every created GPU object has an explicit `.dispose()` path|QA|
|6|No heap allocations inside the render loop|QA|
|7|Tone mapping + output color space set on renderer|Design|
|8|Mobile fallback: antialias off + reduced pixel ratio if needed|QA|
|9|Resize handler attached on window|Frontend|
|10|Code is self-contained and runs with no build step (HTML artifact)|PM|

---

## 🗺️ Reference Map — Read the Right File First

| File | Covers |
|---|---|
| [[setup-and-renderer]] | ALWAYS read for new scenes |
| [[geometry-and-instancing]] | BufferGeometry, InstancedMesh, LOD, particles |
| [[materials-and-textures]] | PBR, texture config, KTX2, environment maps |
| [[lighting-and-shadows]] | Lights, shadow maps, CSM, baked lighting |
| [[animation]] | Keyframes, skeletal, morph targets, mixers |
| [[loaders]] | GLTF/DRACO, OBJ, FBX, HDR, async patterns |
| [[shaders-and-tsl]] | Custom GLSL, onBeforeCompile, TSL/WebGPU |
| [[postprocessing]] | Bloom, DOF, FXAA, EffectComposer, tone mapping |
| [[preformance]] | Profiling, draw calls, mobile, frustum culling |
| [[interaction]] | Raycasting, picking, drag, pointer events |
| [[three-fiber]] | React Three Fiber, Drei, Vue integration |
| [[memory-and-disposal]] | GPU resource cleanup, `.dispose()` patterns |
| [[three/refer/api|api]] | API surface reference |

---

## 🔀 Decision Tree — Which Files to Read

- New 3D scene from scratch → ALWAYS: [[setup-and-renderer]] + [[memory-and-disposal]]
- Geometry / mesh / procedural shape / particles → [[geometry-and-instancing]]
- Load model (GLTF / OBJ / FBX / STL) → [[loaders]] [+ [[animation]] if model has animations]
- Materials / textures / PBR / looks realistic → [[materials-and-textures]] + [[lighting-and-shadows]]
- Lighting / shadows / environment / HDRI → [[lighting-and-shadows]] + [[materials-and-textures]] (env maps)
- Animate objects / play GLTF animations / morph / blend → [[animation]]
- Custom shader / GLSL / TSL / vertex displacement → [[shaders-and-tsl]]
- Postprocessing / glow / bloom / cinematic → [[postprocessing]] + [[lighting-and-shadows]]
- Click / hover / pick / drag objects in 3D → [[interaction]]
- React / Next.js / Vue / R3F / Drei → [[three-fiber]]
- Performance / FPS drops / mobile / too slow → [[preformance]] + [[geometry-and-instancing]]
- Debug / memory leak / renderer info / visual artifacts → [[memory-and-disposal]]

---

## ⚡ Scene Bootstrap — Canonical Modern Pattern

Always start new scenes from this template. Read [[setup-and-renderer]] for full options.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Three.js Scene</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { overflow: hidden; background: #000; }
    canvas { display: block; width: 100vw; height: 100vh; }
  </style>
</head>
<body>
<script type="importmap">
{
  "imports": {
    "three":          "https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.module.js",
    "three/addons/":  "https://cdn.jsdelivr.net/npm/three@0.182.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

/* ── Scene ─────────────────────────────────────────────── */
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.FogExp2(0x0a0a0f, 0.02);

/* ── Camera ─────────────────────────────────────────────── */
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 500);
camera.position.set(0, 2, 8);

/* ── Renderer ───────────────────────────────────────────── */
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;  // ← cinematic look
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

/* ── Controls ───────────────────────────────────────────── */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 1;
controls.maxDistance = 200;

/* ── Lighting ───────────────────────────────────────────── */
const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);

const sun = new THREE.DirectionalLight(0xfff0dd, 3);
sun.position.set(5, 10, 5);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 50;
sun.shadow.camera.left = sun.shadow.camera.bottom = -10;
sun.shadow.camera.right = sun.shadow.camera.top = 10;
sun.shadow.bias = -0.001;
scene.add(sun);

/* ── Resize ─────────────────────────────────────────────── */
window.addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
});

/* ── Render loop (delta-time driven) ───────────────────── */
const clock = new THREE.Clock();
renderer.setAnimationLoop(() => {
  const delta = clock.getDelta();
  controls.update();
  // ← put your per-frame updates here, always using delta
  renderer.render(scene, camera);
});
</script>
</body>
</html>
```

---

## 🚫 Non-Negotiable Rules

|Rule|Wrong|Right|
|---|---|---|
|Imports|`<script src="cdn.../three.min.js">`|import maps + `type="module"`|
|Loop|`requestAnimationFrame(animate)`|`renderer.setAnimationLoop(fn)`|
|Motion speed|`mesh.rotation.y += 0.01`|`mesh.rotation.y += speed * delta`|
|Pixel ratio|`setPixelRatio(devicePixelRatio)`|`setPixelRatio(Math.min(dpr, 2))`|
|Many objects|1000 individual `Mesh`|`InstancedMesh`|
|Loop alloc|`new Vector3()` inside animate|pre-allocate outside loop|
|Remove mesh|`scene.remove(mesh)` only|`.dispose()` geometry + material|
|Texture dims|600×800 (non-POT)|512×1024 (power-of-two)|
|Color maps|no colorSpace set|`tex.colorSpace = SRGBColorSpace`|
|Renderer|no tone mapping|`ACESFilmicToneMapping` + `SRGBColorSpace`|

---

## 🎨 Design Quality Standards

When creating any 3D scene, apply these by default:

```js
// Cinematic tone mapping (always)
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;

// Soft shadows (always when shadows are needed)
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Environment-based reflections (for any metallic/glossy surface)
// → see materials-and-textures.md: PMREMGenerator

// Hemisphere light for natural sky/ground ambient
const hemi = new THREE.HemisphereLight(0xc8e0ff, 0x553311, 0.6);
scene.add(hemi);
```

Visual quality checklist before delivery:

- [ ] Tone mapping applied (no blown-out whites)
- [ ] PBR materials use correct color space on albedo maps
- [ ] Shadows have appropriate bias (no acne, no peter-panning)
- [ ] Scene has 3-point lighting or HDRI environment
- [ ] Fog or background set (no default grey void)
- [ ] Camera FOV appropriate to use case (50–75° typical)