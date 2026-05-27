# Renderman Brass Lota

Procedural modelling and rendering of a brass lota (traditional Indian water vessel) using the RenderMan 27.2 Python API. No external DCC tools (Maya/Houdini) are used for geometry import as all geometry is generated programmatically.

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

A brass lota approximately 8cm tall. The profile was traced in Houdini from a photograph of the real object, exported as 234 points, and reconstructed in RenderMan as a stack of `Hyperboloid` segments, a surface of revolution technique requiring no external geometry import.

---

## Zone System

The vase surface is divided into 6 zones by profile point index, each with its own shader:

| Zone | Points | Description | Status |
|------|--------|-------------|--------|
| 1 | 0–2 | Base foot | Plain brass |
| 2 | 2–64 | Lower belly | 24 vertical ridges (OSL displacement) |
| 3 | 64–68 | Goldish ring | Shinier brass, horizontal grooves planned |
| 4 | 68–103 | Art pattern band | Texture mapped (roughness variation) |
| 5 | 103–167 | Neck | Anisotropic scratch noise planned |
| 6 | 167–233 | Inner rim | Similar to zone 5 planned but darker and more pronounced |

---

## Shaders

### Brass Material (PxrSurface)
All zones share a base brass BRDF near-zero diffuse, warm gold specular. Metals in physically based rendering carry almost no diffuse response; the colour lives entirely in the specular.

Per-zone variations in `specularRoughness` simulate different surface treatments:
- Zone 3 (ring): roughness 0.20 — polished
- Zone 2 (belly): roughness 0.45 — worn
- Zone 4 (art band): roughness driven by texture — engraved surface

### Zone 2 — Vertical Ridges (zone2_skin.osl)
Sine wave displacement along the circumferential U direction. 24 complete cycles = 24 evenly spaced panels matching the real object. Displacement is scoped per segment using `AttributeBegin/AttributeEnd` to prevent zone bleeding.

### Zone 4 — Art Band (zone4_skin.osl)
Texture coordinates computed from world-space position:
- U: `atan2(-Pw[0], Pw[2])` — angle around Y axis
- V: `Pw[1]` — height along vase

Texture drives `specularRoughness` variation: light areas of the engraving = smoother/shinier, dark recessed areas = rougher. Diffuse colour remains a dark brass constant. The texture is a greyscale albedo map of engraved figurative symbols.

---

## Lighting

Single `PxrDomeLight` with an HDRI environment map (`INT_AMB_WARM_001`). No additional rect lights for now. the HDRI provides sufficient warm indoor lighting and gives the brass surface a rich environment to reflect.

```python
ri.AttributeBegin()
ri.Rotate(90, 0, 1, 0)
ri.Light("PxrDomeLight", "domeLight", {
    "float intensity": [1.0],
    "string lightColorMap": [absolute_path],
})
ri.AttributeEnd()
```

---

## Texture Conversion

All textures must be converted to RenderMan's `.tex` format before use:

```bash
# Standard texture (colour/albedo)
arch -x86_64 /Applications/Pixar/RenderManProServer-27.2/bin/txmake \
    -mode periodic -format openexr \
    textures/input.png textures/output.tex

# HDRI environment map
arch -x86_64 /Applications/Pixar/RenderManProServer-27.2/bin/txmake \
    hdri/input.exr hdri/output.tex
```

---

## Render Settings

```python
ri.Format(1400, 800, 1)
ri.Integrator("PxrPathTracer", "integrator", {"int maxIndirectBounces": [8]})
ri.Option("Ri", {"int Pixelsamples": [32]})   # lower to 4 for test renders
ri.ShadingRate(0.25)                            # raise to 2.0 for test renders
```
