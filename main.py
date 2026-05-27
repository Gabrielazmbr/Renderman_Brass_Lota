import os
import sys

RMANTREE = os.environ.get("RMANTREE", "/Applications/Pixar/RenderManProServer-27.2")
sys.path.insert(0, os.path.join(RMANTREE, "bin"))
import prman

from geometry import make_ground_plane, place_showcase

# ── Main render

ri = prman.Ri()

ri.Begin("output/main.rib")

shader_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shaders")
ri.Option("searchpath", {"string shader": [f"{shader_path}:@"]})


ri.Display("output/render.exr", "openexr", "rgba")
ri.Format(1400, 800, 1)

ri.Integrator("PxrPathTracer", "integrator", {"int maxIndirectBounces": [8]})
ri.Option("Ri", {"int Pixelsamples": [32]})

ri.Projection("perspective", {"fov": 45})
ri.Translate(0, -3, 20)
ri.Rotate(-10, 1, 0, 0)
ri.Rotate(0, 0, 1, 0)

ri.WorldBegin()
ri.AttributeBegin()
ri.Rotate(-90, 1, 0, 0)
ri.Rotate(90, 0, 0, 1)
ri.Light(
    "PxrDomeLight",
    "domeLight",
    {
        "float intensity": [1.0],
        "string lightColorMap": [
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "hdri",
                "INT_AMB_WARM_001.tex",
            )
        ],
    },
)
ri.AttributeEnd()


make_ground_plane(ri)
place_showcase(ri)

ri.WorldEnd()
ri.End()

print("RIB generated successfully!")
