import math
import os
import random
import sys

RMANTREE = os.environ.get("RMANTREE", "/Applications/Pixar/RenderManProServer-27.2")
sys.path.insert(0, os.path.join(RMANTREE, "bin"))

import prman

# ── Scene constants
GROUND_Y = -2.5


# ── Geometry


def make_vase(ri, x, y, z, scale=1.0):
    S = 5.305 * scale  # scale factor: maps Houdini units to 8cm real size

    # Profile points from Houdini: (radius, height)
    profile = [
        (0.0, 0.0),
        (0.4, 0.0),
        (0.400371, 0.127306),
        (0.536637, 0.215298),
        (0.638399, 0.309673),
        (0.706514, 0.399946),
        (0.754112, 0.491860),
        (0.797373, 0.579804),
        (0.802356, 0.760130),
        (0.764321, 0.859250),
        (0.764881, 0.859250),
        (0.734650, 0.910755),
        (0.686503, 0.965620),
        (0.605885, 1.023280),
        (0.550461, 1.065830),
        (0.503994, 1.111740),
        (0.464805, 1.162690),
        (0.443530, 1.211950),
        (0.444650, 1.265140),
        (0.458086, 1.320560),
        (0.490557, 1.384940),
        (0.547662, 1.445970),
        (0.591329, 1.482360),
        (0.626040, 1.505310),
        (0.642849, 1.508000),
        (0.642746, 1.518850),
        (0.623204, 1.514370),
        (0.577993, 1.492360),
        (0.539076, 1.458700),
        (0.478071, 1.392430),
        (0.443361, 1.324070),
        (0.430739, 1.269370),
        (0.431791, 1.213630),
        (0.453879, 1.157880),
        (0.489641, 1.106340),
        (0.539076, 1.054800),
        (0.576941, 1.024300),
        (0.0, 1.000000),
    ]

    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Scale(S, S, S)

    ri.Bxdf(
        "PxrSurface",
        "vase_surface",
        {
            "color diffuseColor": [0.05, 0.04, 0.01],
            "float diffuseGain": [0.1],
            "color specularFaceColor": [0.72, 0.58, 0.22],
            "color specularEdgeColor": [0.90, 0.75, 0.35],
            "float specularRoughness": [0.25],
            "color specularIor": [1.80, 1.80, 1.80],
            "int specularFresnelMode": [0],
        },
    )

    for i in range(len(profile) - 1):
        r1, y1 = profile[i]
        r2, y2 = profile[i + 1]
        if abs(r2 - r1) < 0.0001 and abs(y2 - y1) < 0.0001:
            continue  # skip degenerate segments
        ri.TransformBegin()
        ri.Translate(0, y1, 0)
        ri.Rotate(-90, 1, 0, 0)
        ri.Hyperboloid([r1, 0, 0], [r2, 0, y2 - y1], 360)
        ri.TransformEnd()

    # Base disk
    ri.TransformBegin()
    ri.Rotate(90, 1, 0, 0)
    ri.Disk(0, profile[0][1] if profile[0][0] == 0 else profile[1][0], 360)
    ri.TransformEnd()

    ri.AttributeEnd()


# ── Ground plane


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


# ── Showcase placement


def place_showcase(ri):
    random.seed(42)

    def cv():
        return (
            random.uniform(-0.04, 0.04),
            random.uniform(-0.03, 0.03),
            random.uniform(-0.02, 0.02),
        )

    g = GROUND_Y

    make_vase(ri, x=0, y=GROUND_Y, z=0)


# ── Main render

ri = prman.Ri()
ri.Begin("output/main.rib")

ri.Display("output/render.exr", "openexr", "rgba")
ri.Format(1400, 800, 1)

ri.Integrator("PxrPathTracer", "integrator", {"int maxIndirectBounces": [8]})
ri.Option("Ri", {"int Pixelsamples": [32]})

ri.Projection("perspective", {"fov": 45})
ri.Translate(0, 0, 30)
ri.Rotate(-10, 1, 0, 0)
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
