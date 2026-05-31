import os
import sys

RMANTREE = os.environ.get("RMANTREE", "/Applications/Pixar/RenderManProServer-27.2")
sys.path.insert(0, os.path.join(RMANTREE, "bin"))
import prman

from geometry import AimZ, make_back_wall, make_ground_plane, place_showcase

# ── Main render

ri = prman.Ri()

ri.Begin("output/main.rib")

shader_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shaders")
ri.Option("searchpath", {"string shader": [f"{shader_path}:@"]})


ri.Display("output/render.exr", "openexr", "rgba")
ri.Format(1512, 2016, 1)  # 1512 × 2016 - 1008 x 1344

ri.Integrator(
    "PxrPathTracer",
    "integrator",
    {
        "int maxIndirectBounces": [16],  # 16 -4
        "int numLightSamples": [4],  # 4 -2
        "int numBxdfSamples": [4],  # 4-2
    },
)
ri.Option("Ri", {"int Pixelsamples": [256]})  # 25 - 256


# ── Camera

# ri.Projection("perspective", {"fov": 45})

# Cam 01
"""
ri.Projection(
    "perspective",
    {
        "fov": 45,
        "float fStop": [8.0],
        "float focalLength": [1.0],
        "float focalDistance": [15.0],
    },
)

ri.Translate(0, -2.5, 15)
ri.Rotate(-15, 1, 0, 0)
ri.Rotate(0, 0, 1, 0)
"""

# Cam 02
ri.Projection(
    "perspective",
    {
        "fov": 45,
        "float fStop": [8.0],
        "float focalLength": [1.0],
        "float focalDistance": [15.0],
    },
)

ri.Translate(0, -2.5, 15)
ri.Rotate(-15, 1, 0, 0)
ri.Rotate(0, 0, 1, 0)


# ── Lights


ri.WorldBegin()
make_back_wall(ri)
ri.AttributeBegin()
ri.Rotate(-90, 1, 0, 0)
ri.Rotate(90, 0, 0, 1)

ri.Light(
    "PxrDomeLight",
    "domeLight",
    {
        "float intensity": [0.5],
        "string lightColorMap": [
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "hdri",
                "INT_AMB_WARM_002.tex",
            )
        ],
    },
)
ri.AttributeEnd()


ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(-20, 25, 15)
To = [3, -2.5, -2]
From = [-20, 25, 15]
direction = list(map(lambda x, y: x - y, To, From))
AimZ(ri, direction)
ri.Light(
    "PxrRectLight",
    "keyLight",
    {
        "float intensity": [10000],
        "float exposure": [1.0],
        "color lightColor": [1.0, 0.90, 0.70],
        "int enableShadows": [1],
        "color shadowColor": [0, 0, 0],
        "float coneAngle": [12.0],
        "float coneSoftness": [0.2],
        "float specular": [0.5],
        "float diffuse": [1.5],
        "float intensityNearDist": [50.0],
        "float specularNearDist": [50.0],
    },
)
ri.AttributeEnd()
ri.TransformEnd()


ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(-40, 100, 30)
To = [-15, -2.5, 15]
From = [-40, 100, 30]
direction = list(map(lambda x, y: x - y, To, From))
AimZ(ri, direction)
ri.Light(
    "PxrRectLight",
    "keyLight",
    {
        "float intensity": [20000],
        "float exposure": [2.0],
        "color lightColor": [1.0, 0.90, 0.70],
        "int enableShadows": [1],
        "color shadowColor": [0, 0, 0],
        "float coneAngle": [5.0],
        "float specular": [0.5],
        "float diffuse": [1.5],
        "float coneSoftness": [0.2],
        "float intensityNearDist": [5.0],
    },
)
ri.AttributeEnd()
ri.TransformEnd()


# ── Geometry

make_ground_plane(ri)
place_showcase(ri)

ri.WorldEnd()
ri.End()

print("RIB generated successfully!")
