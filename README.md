# Renderman Brass Lota

Procedural modelling and rendering of a brass lota (traditional Indian water vessel) using the RenderMan 27.2 Python API. All geometry is generated programmatically — no external DCC tools or mesh imports are used.

---

## Technical Requirements

| Component | Details |
|-----------|---------|
| OS | macOS (Apple Silicon, runs under Rosetta 2) |
| RenderMan | 27.2 at `/Applications/Pixar/RenderManProServer-27.2` |
| Python | 3.11 at `/usr/local/bin/python3.11` (x86 Homebrew) |
| Architecture | All commands run under `arch -x86_64` |

---

## Project Structure

```
Renderman_Brass_Lota/
├── main.py           ← camera, lights, render settings
├── geometry.py       ← all geometry, zone shaders, scene placement
├── Makefile
├── shaders/          ← OSL source (.osl) and compiled (.oso) files
├── textures/         ← .tex files converted with txmake
├── hdri/             ← HDRI environment map
└── output/           ← generated .rib and rendered .exr files
```

---

## Usage

```bash
# Compile shaders, generate RIB, and render
make both

# Steps individually
make compile_shaders
make generate
make render

# View output
make view

# Clean outputs
make clean
```

---

## Object

A brass lota approximately 8cm tall. The profile was traced from a reference photograph using a 2D graph of radius against height, producing 234 coordinate pairs. These were reconstructed in RenderMan as a stack of `Hyperboloid` segments — a surface-of-revolution technique requiring no external geometry import.

---

## Zone System

The vase surface is divided into 6 zones by profile point index, each with its own OSL shader:

| Zone | Points | Description | Shader |
|------|--------|-------------|--------|
| 1 | 0–1 | Base foot | Hash stains, fine grain, border darkening |
| 2 | 2–63 | Lower belly | 24 vertical ridges (sine displacement), directional scratches, vertical streaks |
| 3 | 64–67 | Lathe ring | Horizontal sine grooves (displacement), oxidation stains |
| 4 | 68–102 | Art pattern band | Texture-mapped roughness + displacement from photo-sourced greyscale maps |
| 5 | 103–166 | Neck | Gaussian line displacement, hash stains, perlin stains |
| 6 | 167–233 | Inner rim | Hash stains, fine grain |

---

## Shaders

### Brass Material (PxrSurface)
All zones use PxrSurface with near-zero diffuse and a warm gold specular. Metals in physically based rendering carry almost no diffuse response; colour lives entirely in the specular lobe. Per-zone variations in roughness and specularFaceColor simulate different surface treatments:

- Zone 1 (base): roughness 0.30 — plain worn brass
- Zone 2 (belly): roughness 0.45 — worn, directional scratches
- Zone 3 (ring): roughness 0.40 — lathe-polished
- Zone 4 (art band): roughness 0.60–0.95, texture-driven — engraved surface
- Zone 5 (neck): roughness 0.60 — anisotropic scratches and horizontal lines
- Zone 6 (rim): roughness 0.40 — darker inner brass

### Zone 2 — Vertical Ridges (zone2_skin.osl)
Sine wave displacement along the circumferential U direction. 24 complete cycles produce 24 evenly spaced ridges matching the real object. Hash stains and vertical streak darkening near the zone's upper border simulate dirt accumulation.

### Zone 3 — Lathe Ring (zone3_skin.osl)
Superposed sine waves in world-space height simulate horizontal lathe grooves. Displacement scoped per segment using `AttributeBegin/AttributeEnd`.

### Zone 4 — Art Band (zone4_skin.osl)
Texture coordinates computed from world-space position:
- U: `atan2(-Pw[0], Pw[2])` — angle around Y axis
- V: `Pw[1]` — height along vase

Both the roughness driver and displacement map were produced from close-up photographs of the real object's engraved band, processed in Photoshop to separate raised brass surfaces (light) from recessed engraving (dark). The texture drives `resultRough = 0.60 + (1.0 - grey) * 0.35`.

### Zone 5 — Neck (zone5_skin.osl)
Eight horizontal lines defined by Gaussian falloff functions produce subtle ring marks. Multi-scale hash stains and Perlin noise stains add oxidation variation.

### Wear System (all zones)
All zone shaders share a common wear approach:
- Fine grain: two octaves of Perlin noise at frequencies 40 and 100
- Hash stains: three-scale hash noise in cylindrical coordinates at large, medium and small scales, modulated by a Perlin vary factor
- Border effects: height-based masks with noise modulation at zone transitions

---

## Lighting

Four light sources in the final scene:

| Light | Type | Position | Purpose |
|-------|------|----------|---------|
| Dome | PxrDomeLight | — | Warm HDRI ambient (`INT_AMB_WARM_002.tex`), intensity 0.6 |
| Key | PxrRectLight | −20, 25, 15 | Primary warm directional, aimed at vase centre |
| Fill | PxrRectLight | −40, 100, 30 | High-angle top specular contribution |
| Kick | PxrRectLight | −30, 2, −20 | Left side rim, separates vase from background |
| Wall | PxrRectLight | −20, 5, −5 | Warm patch on back wall for compositional depth |

All rect lights use `AimZ()` (yaw/pitch decomposition helper in `geometry.py`) to point at a target coordinate.

---

## Camera

Two cameras defined in `main.py`:

**Cam 01** — Front view, straight on  
**Cam 02** — Three-quarter view, 35° orbit

```python
ri.Projection("perspective", {
    "fov": 45,
    "float fStop": [4.0],
    "float focalLength": [1.0],
    "float focalDistance": [20.0],
})
ri.Translate(0, -2.5, 20)
ri.Rotate(-15, 1, 0, 0)
ri.Rotate(35, 0, 1, 0)
```
---

## Texture Conversion

All textures must be converted to RenderMan's `.tex` format before use:

```bash
# Standard texture (colour/albedo or greyscale)
arch -x86_64 /Applications/Pixar/RenderManProServer-27.2/bin/txmake \
    -mode periodic -format openexr \
    textures/input.png textures/output.tex

# HDRI environment map
arch -x86_64 /Applications/Pixar/RenderManProServer-27.2/bin/txmake \
    hdri/input.exr hdri/output.tex
```

---

## Render Settings

### Final quality
```python
ri.Format(1512, 2016, 1)
ri.Integrator("PxrPathTracer", "integrator", {
    "int maxIndirectBounces": [16],
    "int numLightSamples": [4],
    "int numBxdfSamples": [4],
})
ri.Option("Ri", {"int pixelsamples": [256]})
ri.ShadingRate(0.2)  # set in make_vase()
```

### Fast test
```python
ri.Format(800, 600, 1)
ri.Integrator("PxrDirectLighting", "integrator")
ri.Option("Ri", {"int pixelsamples": [8]})
ri.ShadingRate(2.5)
# comment out all ri.Displace() calls
# set PxrDomeLight intensity to 0
```

---
