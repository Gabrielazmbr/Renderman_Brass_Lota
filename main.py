import math
import os
import random
import sys

RMANTREE = os.environ.get("RMANTREE", "/Applications/Pixar/RenderManProServer-27.2")
sys.path.insert(0, os.path.join(RMANTREE, "bin"))

import prman

# ── Scene constants ────────────────────────────────────────────────────────────
GROUND_Y = -2.5

# Real-world half-dimensions (cm, 1 unit = 1cm)
ALMOND_LEN = 1.10
ALMOND_WID = 1.65
ALMOND_HGT = 0.40

PSEED_LEN = 0.50
PSEED_WID = 0.30
PSEED_HGT = 0.10

HAZEL_BASE_R = 0.58
HAZEL_HEIGHT = 1.50

CHOC_R = 0.90
CHOC_FLAT = 0.78

CASHEW_ARC_R = 0.80
CASHEW_BEAD_R = 0.32


# ── Shared displacement setup ──────────────────────────────────────────────────


def displacement_setup(ri, shader_name, bound=0.10):
    ri.Attribute(
        "displacementbound",
        {"float sphere": [bound], "string coordinatesystem": ["object"]},
    )
    ri.Pattern(shader_name, "disp_out", {})
    ri.Displace(
        "PxrDisplace",
        "displace",
        {
            "float dispAmount": [1.0],
            "reference vector dispVector": ["disp_out:dPdisp"],
        },
    )


# ── Almond ────────────────────────────────────────────────────────────────────


def make_almond(ri, x, y, z, rx, ry, rz, scale=1.0, color_var=None):
    if color_var is None:
        color_var = (0.0, 0.0, 0.0)
    base_r = max(0.01, min(1.0, 0.58 + color_var[0]))
    base_g = max(0.01, min(1.0, 0.36 + color_var[1]))
    base_b = max(0.01, min(1.0, 0.16 + color_var[2]))

    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Rotate(rz, 0, 0, 1)
    ri.Rotate(ry, 0, 1, 0)
    ri.Rotate(rx, 1, 0, 0)

    ri.ShadingRate(0.25)
    ri.Bxdf(
        "PxrSurface",
        "almond_surface",
        {
            "color diffuseColor": [base_r, base_g, base_b],
            "float diffuseGain": [1.0],
            "float diffuseRoughness": [0.75],
            "color specularFaceColor": [0.03, 0.02, 0.01],
            "color specularEdgeColor": [0.10, 0.07, 0.03],
            "float specularRoughness": [0.55],
            "color specularIor": [1.45, 1.45, 1.45],
            "int specularFresnelMode": [0],
        },
    )
    displacement_setup(ri, "almond_skin", bound=0.12)

    # Main body
    ri.TransformBegin()
    ri.Scale(scale * ALMOND_LEN, scale * ALMOND_HGT, scale * ALMOND_WID)
    ri.Sphere(1, -1, 1, 360)
    ri.TransformEnd()

    # Tip sphere offset along +X
    ri.TransformBegin()
    ri.Translate(scale * ALMOND_LEN * 0.65, 0, 0)
    ri.Scale(
        scale * ALMOND_LEN * 0.45, scale * ALMOND_HGT * 0.55, scale * ALMOND_WID * 0.55
    )
    ri.Sphere(1, -1, 1, 360)
    ri.TransformEnd()

    ri.AttributeEnd()


# ── Pumpkin seed ───────────────────────────────────────────────────────────────


def make_pumpkin_seed(ri, x, y, z, rx, ry, rz, scale=1.0, color_var=None):
    if color_var is None:
        color_var = (0.0, 0.0, 0.0)
    base_r = max(0.01, min(1.0, 0.62 + color_var[0]))
    base_g = max(0.01, min(1.0, 0.65 + color_var[1]))
    base_b = max(0.01, min(1.0, 0.38 + color_var[2]))

    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Rotate(rz, 0, 0, 1)
    ri.Rotate(ry, 0, 1, 0)
    ri.Rotate(rx, 1, 0, 0)

    ri.ShadingRate(0.25)
    ri.Bxdf(
        "PxrSurface",
        "pseed_surface",
        {
            "color diffuseColor": [base_r, base_g, base_b],
            "float diffuseGain": [1.0],
            "float diffuseRoughness": [0.45],
            "color specularFaceColor": [0.05, 0.06, 0.04],
            "color specularEdgeColor": [0.18, 0.20, 0.12],
            "float specularRoughness": [0.25],
            "color specularIor": [1.45, 1.45, 1.45],
            "int specularFresnelMode": [0],
        },
    )
    displacement_setup(ri, "pseed_skin", bound=0.05)

    ri.Scale(scale * PSEED_LEN, scale * PSEED_HGT, scale * PSEED_WID)
    ri.Sphere(1, -1, 1, 360)
    ri.AttributeEnd()


# ── Hazelnut  ───────────────────────────────────


def make_hazelnut(ri, x, y, z, rx, ry, rz, scale=1.0, color_var=None):

    if color_var is None:
        color_var = (0.0, 0.0, 0.0)
    base_r = max(0.01, min(1.0, 0.48 + color_var[0]))
    base_g = max(0.01, min(1.0, 0.28 + color_var[1]))
    base_b = max(0.01, min(1.0, 0.10 + color_var[2]))

    # Profile: (radius, height) from base to tip
    profile = [
        (0.55, 0.00),  # base edge
        (0.68, 0.35),  # lower body
        (0.62, 0.55),  # mid body
        (0.50, 0.88),  # upper body
        (0.30, 1.18),  # shoulder
        (0.10, 1.42),  # near tip
        (0.01, 1.50),  # tip (tiny radius, not zero, avoids degenerate)
    ]

    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Rotate(rz, 0, 0, 1)
    ri.Rotate(ry, 0, 1, 0)
    ri.Rotate(rx, 1, 0, 0)
    ri.Scale(scale, scale, scale)

    ri.ShadingRate(0.25)
    ri.Bxdf(
        "PxrSurface",
        "hazel_surface",
        {
            "color diffuseColor": [base_r, base_g, base_b],
            "float diffuseGain": [1.0],
            "float diffuseRoughness": [0.65],
            "color specularFaceColor": [0.04, 0.025, 0.01],
            "color specularEdgeColor": [0.15, 0.10, 0.04],
            "float specularRoughness": [0.40],
            "color specularIor": [1.50, 1.50, 1.50],
            "int specularFresnelMode": [0],
        },
    )
    displacement_setup(ri, "hazel_skin", bound=0.10)

    # Stacked Hyperboloid segments — each sweeps between two profile points
    for i in range(len(profile) - 1):
        r1, y1 = profile[i]
        r2, y2 = profile[i + 1]
        ri.TransformBegin()
        ri.Translate(0, y1, 0)
        ri.Rotate(-90, 1, 0, 0)  # Y-up to Z-up for Hyperboloid
        ri.Hyperboloid([r1, 0, 0], [r2, 0, y2 - y1], 360)
        ri.TransformEnd()

    # Base disk
    ri.TransformBegin()
    ri.Rotate(90, 1, 0, 0)
    ri.Disk(0, profile[0][0], 360)
    ri.TransformEnd()

    ri.AttributeEnd()


# ── Chocolate pebble ───────────────────────────────────────────────────────────


def make_chocolate(ri, x, y, z, rx, ry, rz, scale=1.0, color_var=None):
    if color_var is None:
        color_var = (0.0, 0.0, 0.0)
    base_r = max(0.01, min(1.0, 0.13 + color_var[0]))
    base_g = max(0.01, min(1.0, 0.06 + color_var[1]))
    base_b = max(0.01, min(1.0, 0.03 + color_var[2]))

    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Rotate(rz, 0, 0, 1)
    ri.Rotate(ry, 0, 1, 0)
    ri.Rotate(rx, 1, 0, 0)
    ri.Scale(scale * CHOC_R, scale * CHOC_R * CHOC_FLAT, scale * CHOC_R)

    ri.ShadingRate(0.2)
    ri.Bxdf(
        "PxrSurface",
        "choc_surface",
        {
            "color diffuseColor": [base_r, base_g, base_b],
            "float diffuseGain": [1.0],
            "float diffuseRoughness": [0.10],
            "color specularFaceColor": [0.06, 0.04, 0.02],
            "color specularEdgeColor": [0.35, 0.25, 0.15],
            "float specularRoughness": [0.10],
            "color specularIor": [1.55, 1.55, 1.55],
            "int specularFresnelMode": [0],
        },
    )
    ri.Sphere(1, -1, 1, 360)
    ri.AttributeEnd()


# ── Cashew (bead chain along a C-curve arc) ────────────────────────────────────


def make_cashew(ri, x, y, z, rx, ry, rz, scale=1.0, color_var=None):
    """
    Cashew: overlapping ellipsoid beads positioned along a 280-degree arc.
    Beads taper at both ends giving natural cashew tip shape.
    Lying flat in XZ plane, C-curve faces +Z (toward camera).
    """
    if color_var is None:
        color_var = (0.0, 0.0, 0.0)
    base_r = max(0.01, min(1.0, 0.82 + color_var[0]))
    base_g = max(0.01, min(1.0, 0.68 + color_var[1]))
    base_b = max(0.01, min(1.0, 0.38 + color_var[2]))

    sweep = 280.0
    n_beads = 16
    arc_r = CASHEW_ARC_R

    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Rotate(rz, 0, 0, 1)
    ri.Rotate(ry, 0, 1, 0)
    ri.Rotate(rx, 1, 0, 0)
    ri.Scale(scale, scale, scale)

    ri.ShadingRate(0.3)
    ri.Bxdf(
        "PxrSurface",
        "cashew_surface",
        {
            "color diffuseColor": [base_r, base_g, base_b],
            "float diffuseGain": [1.0],
            "float diffuseRoughness": [0.55],
            "color specularFaceColor": [0.04, 0.03, 0.01],
            "color specularEdgeColor": [0.14, 0.11, 0.05],
            "float specularRoughness": [0.35],
            "color specularIor": [1.45, 1.45, 1.45],
            "int specularFresnelMode": [0],
        },
    )
    displacement_setup(ri, "cashew_skin", bound=0.06)

    for i in range(n_beads):
        t = i / (n_beads - 1)
        angle = math.radians(-sweep / 2.0 + t * sweep)

        # Position on arc in XZ plane (lying flat)
        bx = arc_r * math.cos(angle)
        bz = arc_r * math.sin(angle)

        # Taper: beads at tips are smaller
        taper = math.sin(t * math.pi)  # 0 at tips, 1 at centre
        bead_scale = CASHEW_BEAD_R * (0.45 + 0.55 * taper)

        # Orient bead along the arc tangent
        tangent_deg = math.degrees(angle) + 90.0

        ri.TransformBegin()
        ri.Translate(bx, 0, bz)
        ri.Rotate(tangent_deg, 0, 1, 0)
        ri.Scale(
            bead_scale * 1.3,  # along arc tangent
            bead_scale * 0.70,  # flattened height
            bead_scale,
        )  # cross-section
        ri.Sphere(1, -1, 1, 360)
        ri.TransformEnd()

    ri.AttributeEnd()


# ── Ground plane ───────────────────────────────────────────────────────────────


def make_ground_plane(ri):
    ri.AttributeBegin()
    ri.Bxdf("PxrDiffuse", "ground_material", {"color diffuseColor": [0.45, 0.28, 0.12]})
    ri.Patch(
        "bilinear",
        {
            "P": [
                -30,
                GROUND_Y,
                -30,
                30,
                GROUND_Y,
                -30,
                -30,
                GROUND_Y,
                30,
                30,
                GROUND_Y,
                30,
            ]
        },
    )
    ri.AttributeEnd()


# ── Showcase placement ─────────────────────────────────────────────────────────


def place_showcase(ri):
    random.seed(42)

    def cv():
        return (
            random.uniform(-0.04, 0.04),
            random.uniform(-0.03, 0.03),
            random.uniform(-0.02, 0.02),
        )

    g = GROUND_Y

    make_almond(
        ri, x=-6.0, y=g + ALMOND_HGT, z=0, rx=0, ry=15, rz=0, scale=1.0, color_var=cv()
    )

    make_pumpkin_seed(
        ri, x=-3.0, y=g + PSEED_HGT, z=0, rx=5, ry=20, rz=0, scale=1.0, color_var=cv()
    )

    make_hazelnut(ri, x=0.0, y=g, z=0, rx=0, ry=25, rz=0, scale=1.0, color_var=cv())

    make_chocolate(
        ri,
        x=3.0,
        y=g + CHOC_R * CHOC_FLAT,
        z=0,
        rx=0,
        ry=30,
        rz=0,
        scale=1.0,
        color_var=cv(),
    )

    make_cashew(
        ri,
        x=6.5,
        y=g + CASHEW_BEAD_R * 0.70,
        z=0,
        rx=0,
        ry=0,
        rz=0,
        scale=2.0,
        color_var=cv(),
    )


# ── Main render ────────────────────────────────────────────────────────────────

ri = prman.Ri()
ri.Begin("output/main.rib")

shader_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shaders")
ri.Option("searchpath", {"string shader": [f"{shader_path}:@"]})

ri.Display("output/render.exr", "openexr", "rgba")
ri.Format(1400, 600, 1)

ri.Integrator("PxrPathTracer", "integrator", {"int maxIndirectBounces": [8]})
ri.Option("Ri", {"int Pixelsamples": [32]})

ri.Projection("perspective", {"fov": 45})
ri.Translate(0, 0, 14)
ri.Rotate(-18, 1, 0, 0)
ri.Rotate(0, 0, 1, 0)

ri.WorldBegin()

ri.Light(
    "PxrDomeLight",
    "domeLight",
    {
        "float intensity": [0.6],
        "color lightColor": [1.0, 0.95, 0.85],
    },
)

ri.AttributeBegin()
ri.Translate(-8, 10, 6)
ri.Rotate(-40, 1, 0, 0)
ri.Light(
    "PxrRectLight",
    "keyLight",
    {
        "float intensity": [15.0],
        "color lightColor": [1.0, 0.97, 0.90],
    },
)
ri.AttributeEnd()

ri.AttributeBegin()
ri.Translate(8, 5, -2)
ri.Rotate(-20, 1, 0, 0)
ri.Light(
    "PxrRectLight",
    "fillLight",
    {
        "float intensity": [4.0],
        "color lightColor": [0.85, 0.90, 1.0],
    },
)
ri.AttributeEnd()

make_ground_plane(ri)
place_showcase(ri)

ri.WorldEnd()
ri.End()

print("RIB generated successfully!")
