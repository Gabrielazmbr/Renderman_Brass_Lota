import sys
import os
import random
import math

RMANTREE = os.environ.get("RMANTREE", "/Applications/Pixar/RenderManProServer-27.2")
sys.path.insert(0, os.path.join(RMANTREE, "bin"))

import prman

# ── Scene constants ────────────────────────────────────────────────────────────
GROUND_Y     = -2.5

JAR_BOTTOM_Y = GROUND_Y
JAR_HEIGHT   =  4.3
JAR_TOP_Y    = JAR_BOTTOM_Y + JAR_HEIGHT

JAR_R_TOP    = 1.90    # rim radius (narrower than widest point)
JAR_R_BOTTOM = 1.80
JAR_WALL     = 0.30
JAR_INNER_R  = 2.15 - JAR_WALL

BEAN_LEN = 0.50   # half-length → full bean = 1.0cm = 10mm ✓
BEAN_WID = 0.35   # half-width  → full bean = 0.7cm = 7mm  ✓
BEAN_HGT = 0.25   # half-height → full bean = 0.5cm = 5mm  ✓

# ── Collision ──────────────────────────────────────────────────────────────────

def beans_overlap(ax, ay, az, a_scale, bx, by, bz, b_scale, pad=0.76):  # was 0.82
    rx = (BEAN_LEN * a_scale + BEAN_LEN * b_scale) * pad
    ry = (BEAN_HGT * a_scale + BEAN_HGT * b_scale) * pad
    rz = (BEAN_WID * a_scale + BEAN_WID * b_scale) * pad
    dx = (ax - bx) / rx
    dy = (ay - by) / ry
    dz = (az - bz) / rz
    return (dx*dx + dy*dy + dz*dz) < 1.0


def inside_jar(x, z, scale, margin=0.05):
    r = math.sqrt(x*x + z*z)
    return r < (JAR_INNER_R - BEAN_LEN * 0.5 * scale - margin)


# ── Geometry helpers ───────────────────────────────────────────────────────────

def hex_points(cx, cz, r, n=6, angle_offset=0):
    """Return 2D (x, z) vertices of a regular hexagon."""
    pts = []
    for i in range(n):
        a = math.radians(angle_offset + 60 * i)
        pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return pts


def make_jar(ri):
    """
    Bonne Maman mini jar — revolved profile built from stacked Hyperboloid
    segments. Each segment sweeps between two (radius, height) control points.
    Profile derived from reference photographs.
    All units in cm. Jar sits with base at JAR_BOTTOM_Y.
    """
    ri.AttributeBegin()
    ri.Attribute("identifier", {"string name": ["jar"]})

    ri.Bxdf("PxrSurface", "glass_placeholder", {
        "color diffuseColor":    [0.0, 0.0, 0.0],
        "float diffuseGain":     [0.0],
        "color refractionColor": [0.82, 0.93, 0.85],
        "float refractionGain":  [1.0],
        "float glassRoughness":  [0.02],
        "float glassIor":        [1.52],
    })

    W = JAR_WALL

    # Profile control points: (radius, y_offset_from_base)
    # Outer profile — matches the barrel shape in photos
    outer = [
        (1.80, 0.00),   # base edge
        (2.00, 0.50),   # lower body widens
        (2.15, 1.40),   # widest point (mid body)
        (2.15, 2.20),   # still wide through middle
        (2.05, 3.00),   # shoulder begins tapering
        (1.85, 3.60),   # neck narrows
        (1.90, 3.90),   # slight flare at rim lip
        (1.90, 4.30),   # top of rim
    ]

    # Inner profile — wall thickness offset inward
    inner = [(max(0.1, r - W), y) for (r, y) in outer]
    # Thicker base — inner starts higher
    inner[0] = (outer[0][0] - W, 0.38)   # thick glass base

    def hyperboloid_segment(ri, p1, p2, y_base):
        """Emit one Hyperboloid segment between two profile points."""
        r1, y1 = p1
        r2, y2 = p2
        # RenderMan Hyperboloid sweeps a line in the XZ plane around Z axis
        # We work in Y-up so we rotate -90 around X after translating
        mid_y = y_base + (y1 + y2) / 2
        half  = (y2 - y1) / 2
        ri.TransformBegin()
        ri.Translate(0, y_base + y1, 0)
        ri.Rotate(-90, 1, 0, 0)
        ri.Hyperboloid([r1, 0, 0], [r2, 0, y2 - y1], 360)
        ri.TransformEnd()

    yb = JAR_BOTTOM_Y

    # Outer wall segments
    for i in range(len(outer) - 1):
        hyperboloid_segment(ri, outer[i], outer[i+1], yb)

    # Inner wall segments
    for i in range(len(inner) - 1):
        hyperboloid_segment(ri, inner[i], inner[i+1], yb)

    # Outer base disk
    ri.TransformBegin()
    ri.Translate(0, yb, 0)
    ri.Rotate(90, 1, 0, 0)
    ri.Disk(0, outer[0][0], 360)
    ri.TransformEnd()

    # Inner base disk (top of thick glass floor)
    ri.TransformBegin()
    ri.Translate(0, yb + 0.38, 0)
    ri.Rotate(-90, 1, 0, 0)
    ri.Disk(0, inner[0][0], 360)
    ri.TransformEnd()

    # Top rim annulus — flat glass lip at very top
    ri.TransformBegin()
    ri.Translate(0, yb + outer[-1][1], 0)
    ri.Rotate(-90, 1, 0, 0)
    ri.Disk(0, outer[-1][0], 360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(0, yb + outer[-1][1], 0)
    ri.Rotate(90, 1, 0, 0)
    ri.Disk(0, inner[-1][0], 360)
    ri.TransformEnd()

    ri.AttributeEnd()


# ── Bean placement ─────────────────────────────────────────────────────────────


def make_bean(ri, x, y, z, rx, ry, rz, scale=1.0):
    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Rotate(rz, 0, 0, 1)
    ri.Rotate(ry, 0, 1, 0)
    ri.Rotate(rx, 1, 0, 0)
    ri.Scale(scale * BEAN_LEN, scale * BEAN_HGT, scale * BEAN_WID)
    ri.Bxdf("PxrDiffuse", "bean_material", {
        "color diffuseColor": [0.18, 0.09, 0.04]
    })
    ri.Sphere(1, -1, 1, 360)
    ri.AttributeEnd()

def scatter_beans_in_jar(ri, target=200, seed=42):
    random.seed(seed)
    placed = []

    layer_step_y   = BEAN_HGT * 2 * 0.80
    grid_spacing_x = BEAN_LEN * 2 * 0.82
    grid_spacing_z = BEAN_WID * 2 * 0.82

    floor_y  = JAR_BOTTOM_Y + 0.38 + BEAN_HGT
    overflow = JAR_TOP_Y + 0.3
    layer = 0
    while len(placed) < target:
        y_centre = floor_y + layer * layer_step_y

        if y_centre > overflow:
            break

        is_overflow = y_centre > JAR_TOP_Y

        offset_x = (grid_spacing_x * 0.5) if layer % 2 == 1 else 0.0
        offset_z = (grid_spacing_z * 0.5) if layer % 2 == 1 else 0.0
        n_cells  = int((JAR_INNER_R * 2) / grid_spacing_x) + 2

        for ix in range(-n_cells, n_cells + 1):
            for iz in range(-n_cells, n_cells + 1):
                if len(placed) >= target:
                    break

                gx = ix * grid_spacing_x + offset_x
                gz = iz * grid_spacing_z + offset_z

                jitter_scale = 0.25
                jx = gx + random.uniform(-BEAN_LEN * jitter_scale,
                                          BEAN_LEN * jitter_scale)
                jz = gz + random.uniform(-BEAN_WID * jitter_scale,
                                          BEAN_WID * jitter_scale)
                scale = random.uniform(0.90, 1.08)

                if not inside_jar(jx, jz, scale):
                    continue

                # jx and jz are now defined — safe to use in overflow block
                if is_overflow:
                    dist_from_centre = math.sqrt(jx*jx + jz*jz)
                    dome_offset = max(0, 0.3 * (1.0 - dist_from_centre / JAR_INNER_R))
                    local_top = JAR_TOP_Y
                    for (bx, by, bz, bs) in placed:
                        dx = jx - bx
                        dz = jz - bz
                        if math.sqrt(dx*dx + dz*dz) < BEAN_LEN * 2.0:
                            candidate = by + BEAN_HGT * bs + BEAN_HGT * scale
                            if candidate > local_top:
                                local_top = candidate
                    jy = local_top + dome_offset + random.uniform(
                        -BEAN_HGT * 0.1, BEAN_HGT * 0.3)
                    rot_x = random.uniform(-50, 50)
                    rot_y = random.uniform(0, 360)
                    rot_z = random.uniform(-40, 40)
                else:
                    jy = y_centre + random.uniform(-BEAN_HGT * 0.15,
                                                    BEAN_HGT * 0.15)
                    rot_x = random.uniform(-35, 35)
                    rot_y = random.uniform(0, 360)
                    rot_z = random.uniform(-25, 25)

                overlap = any(beans_overlap(jx, jy, jz, scale,
                                            bx, by, bz, bs)
                              for (bx, by, bz, bs) in placed)
                if overlap:
                    continue

                placed.append((jx, jy, jz, scale))
                make_bean(ri, jx, jy, jz, rot_x, rot_y, rot_z, scale)

        layer += 1

    print(f"  Jar beans: {len(placed)} placed across {layer} layers")
    return placed



def scatter_floor_beans(ri, count=8, seed=99, placed_jar=None):
    """A few beans scattered casually on the ground around the jar."""
    random.seed(seed)
    placed = list(placed_jar) if placed_jar else []

    # Offset floor beans away from jar
    floor_offsets = []
    attempts = 0
    while len(floor_offsets) < count and attempts < 2000:
        attempts += 1
        angle  = random.uniform(0, 2 * math.pi)
        radius = random.uniform(JAR_R_TOP + 1.0, JAR_R_TOP + 4.5)
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius
        scale = random.uniform(0.90, 1.05)

        y = GROUND_Y + BEAN_HGT * scale + random.uniform(0, 0.08)

        overlap = any(beans_overlap(x, y, z, scale, bx, by, bz, bs)
                      for (bx, by, bz, bs) in placed)
        if overlap:
            continue

        rot_x = random.uniform(-15, 15)   # mostly flat on ground
        rot_y = random.uniform(0, 360)
        rot_z = random.uniform(-10, 10)

        placed.append((x, y, z, scale))
        floor_offsets.append((x, y, z, scale))
        make_bean(ri, x, y, z, rot_x, rot_y, rot_z, scale)

    print(f"  Floor beans: {len(floor_offsets)} placed")


def make_ground_plane(ri):
    ri.AttributeBegin()
    ri.Bxdf("PxrDiffuse", "ground_material", {
        "color diffuseColor": [0.45, 0.28, 0.12]
    })
    ri.Patch("bilinear", {"P": [
        -20, GROUND_Y, -20,
         20, GROUND_Y, -20,
        -20, GROUND_Y,  20,
         20, GROUND_Y,  20,
    ]})
    ri.AttributeEnd()


# ── Main render ────────────────────────────────────────────────────────────────

ri = prman.Ri()
ri.Begin("output/main.rib")

ri.Display("output/render.exr", "openexr", "rgba")
ri.Format(800, 600, 1)

ri.Integrator("PxrPathTracer", "integrator", {
    "int maxIndirectBounces": [12]
})
ri.Option("Ri", {"int[2] Pixelsamples": [8, 8]})

# Camera — three-quarter view, slightly elevated
ri.Projection("perspective", {"fov": 38})
ri.Translate(0, 0, 18)
ri.Rotate(-25, 1, 0, 0)
ri.Rotate(20,  0, 1, 0)

ri.WorldBegin()

# Dome — warm ambient
ri.Light("PxrDomeLight", "domeLight", {
    "float intensity":  [0.8],
    "color lightColor": [1.0, 0.95, 0.85],
})

# Key light — upper left, window-like
ri.AttributeBegin()
ri.Translate(-6, 8, 4)
ri.Rotate(-40, 1, 0, 0)
ri.Light("PxrRectLight", "keyLight", {
    "float intensity":    [12.0],
    "float sceneUnits":   [1.0],
    "color lightColor":   [1.0, 0.97, 0.90],
})
ri.AttributeEnd()

# Fill light — opposite side, softer
ri.AttributeBegin()
ri.Translate(5, 4, -3)
ri.Rotate(-20, 1, 0, 0)
ri.Light("PxrRectLight", "fillLight", {
    "float intensity":  [3.0],
    "float[2] sides":   [3.0, 3.0],
    "color lightColor": [0.85, 0.90, 1.0],
})
ri.AttributeEnd()

make_ground_plane(ri)
make_jar(ri)
jar_beans = scatter_beans_in_jar(ri, target=200)
scatter_floor_beans(ri, count=8, seed=99, placed_jar=jar_beans)

ri.WorldEnd()
ri.End()

print("RIB generated successfully!")
