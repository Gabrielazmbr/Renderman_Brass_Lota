import math
import os
import random

import prman

# ── Scene constants
GROUND_Y = -2.5


# ── Geometry


def make_vase(ri, x, y, z, scale=1.0):
    S = 5.305 * scale  # scale factor

    # Profile points (radius, height)
    profile = [
        (0.0, 0.0),
        (0.399754, 0.0),
        (0.40236, 0.128591),
        (0.410758, 0.134008),
        (0.419154, 0.139429),
        (0.427546, 0.144855),
        (0.435933, 0.150286),
        (0.444318, 0.155722),
        (0.452702, 0.161158),
        (0.461092, 0.166587),
        (0.469496, 0.172),
        (0.477918, 0.177389),
        (0.486362, 0.18275),
        (0.494819, 0.188093),
        (0.503269, 0.193444),
        (0.511675, 0.19885),
        (0.519987, 0.204377),
        (0.528148, 0.210097),
        (0.536111, 0.216072),
        (0.543857, 0.222327),
        (0.551404, 0.228837),
        (0.558801, 0.23554),
        (0.566108, 0.242361),
        (0.573382, 0.249229),
        (0.580665, 0.25609),
        (0.587985, 0.262912),
        (0.595348, 0.269686),
        (0.602741, 0.276425),
        (0.61013, 0.28316),
        (0.617462, 0.289944),
        (0.624668, 0.29684),
        (0.63168, 0.303913),
        (0.638444, 0.311212),
        (0.644947, 0.31875),
        (0.651223, 0.326497),
        (0.65734, 0.334393),
        (0.663373, 0.342372),
        (0.669384, 0.350376),
        (0.675408, 0.358372),
        (0.681443, 0.366353),
        (0.687453, 0.374341),
        (0.693374, 0.382379),
        (0.699126, 0.39052),
        (0.704638, 0.398812),
        (0.709872, 0.407281),
        (0.714841, 0.415919),
        (0.719599, 0.424694),
        (0.724217, 0.433557),
        (0.728763, 0.442465),
        (0.733289, 0.451386),
        (0.737822, 0.460301),
        (0.742368, 0.469205),
        (0.746919, 0.478102),
        (0.751461, 0.487003),
        (0.755978, 0.495915),
        (0.760463, 0.504844),
        (0.764916, 0.513789),
        (0.769345, 0.522748),
        (0.773757, 0.531715),
        (0.778161, 0.540686),
        (0.782563, 0.549658),
        (0.786967, 0.55863),
        (0.791373, 0.5676),
        (0.795782, 0.576569),
        (0.79755, 0.58619),
        (0.79893, 0.636141),
        (0.800034, 0.676101),
        (0.801139, 0.716061),
        (0.802243, 0.756021),
        (0.799224, 0.765439),
        (0.796123, 0.774847),
        (0.792894, 0.784243),
        (0.789537, 0.793629),
        (0.78608, 0.803006),
        (0.782562, 0.812374),
        (0.779009, 0.821722),
        (0.775421, 0.83103),
        (0.771769, 0.840267),
        (0.767997, 0.849399),
        (0.764034, 0.8584),
        (0.759818, 0.867261),
        (0.755311, 0.87599),
        (0.750503, 0.884598),
        (0.745397, 0.89308),
        (0.739994, 0.901421),
        (0.734298, 0.909598),
        (0.728322, 0.917603),
        (0.722107, 0.925447),
        (0.715701, 0.933146),
        (0.709134, 0.940704),
        (0.702408, 0.948098),
        (0.69549, 0.955277),
        (0.688333, 0.962183),
        (0.680903, 0.968775),
        (0.673205, 0.975062),
        (0.665281, 0.981093),
        (0.6572, 0.986948),
        (0.649029, 0.992705),
        (0.640826, 0.998431),
        (0.632632, 1.00417),
        (0.62447, 1.00995),
        (0.61635, 1.01579),
        (0.608274, 1.02168),
        (0.600237, 1.02762),
        (0.592234, 1.03361),
        (0.584264, 1.03964),
        (0.576333, 1.04571),
        (0.568463, 1.05187),
        (0.560684, 1.05813),
        (0.553026, 1.06453),
        (0.545509, 1.0711),
        (0.538139, 1.07783),
        (0.530906, 1.08472),
        (0.523802, 1.09174),
        (0.516828, 1.09888),
        (0.509997, 1.10616),
        (0.503321, 1.11358),
        (0.496808, 1.12114),
        (0.490453, 1.12885),
        (0.484257, 1.13669),
        (0.478244, 1.14468),
        (0.472464, 1.15284),
        (0.466992, 1.1612),
        (0.461906, 1.16979),
        (0.457275, 1.17863),
        (0.453171, 1.18769),
        (0.449684, 1.19695),
        (0.446918, 1.20641),
        (0.44495, 1.21605),
        (0.443788, 1.22583),
        (0.44336, 1.23572),
        (0.443561, 1.24568),
        (0.444296, 1.25565),
        (0.445498, 1.26558),
        (0.447118, 1.27546),
        (0.449109, 1.28527),
        (0.451441, 1.29498),
        (0.454106, 1.30458),
        (0.45712, 1.31407),
        (0.460497, 1.32343),
        (0.464225, 1.33267),
        (0.468263, 1.3418),
        (0.472567, 1.35082),
        (0.477119, 1.35972),
        (0.481949, 1.36844),
        (0.487114, 1.37694),
        (0.492677, 1.38515),
        (0.498654, 1.39306),
        (0.504998, 1.40071),
        (0.511621, 1.40815),
        (0.518427, 1.41546),
        (0.525342, 1.42267),
        (0.532329, 1.42981),
        (0.53939, 1.43687),
        (0.546547, 1.44383),
        (0.553824, 1.45067),
        (0.561238, 1.45739),
        (0.568789, 1.464),
        (0.576479, 1.4705),
        (0.584312, 1.47683),
        (0.592295, 1.48293),
        (0.600434, 1.48869),
        (0.60872, 1.494),
        (0.617134, 1.49877),
        (0.625647, 1.50299),
        (0.634224, 1.50673),
        (0.642828, 1.51021),
        (0.641428, 1.51855),
        (0.631856, 1.51572),
        (0.622358, 1.5127),
        (0.612998, 1.50931),
        (0.603824, 1.50547),
        (0.594877, 1.50114),
        (0.586193, 1.49631),
        (0.577804, 1.49097),
        (0.569717, 1.48517),
        (0.561914, 1.47896),
        (0.554357, 1.47243),
        (0.547009, 1.46565),
        (0.539833, 1.45869),
        (0.532791, 1.45158),
        (0.52584, 1.44438),
        (0.51894, 1.43713),
        (0.512067, 1.42986),
        (0.505235, 1.42255),
        (0.498493, 1.41519),
        (0.491928, 1.4077),
        (0.485642, 1.40002),
        (0.479724, 1.39207),
        (0.474212, 1.38382),
        (0.469077, 1.37531),
        (0.464247, 1.36658),
        (0.459652, 1.35769),
        (0.455261, 1.3487),
        (0.451095, 1.33962),
        (0.447214, 1.33043),
        (0.443689, 1.32112),
        (0.440567, 1.31168),
        (0.437857, 1.30211),
        (0.435552, 1.29241),
        (0.433654, 1.28262),
        (0.432181, 1.27274),
        (0.431159, 1.2628),
        (0.430602, 1.25283),
        (0.430523, 1.24286),
        (0.43096, 1.23292),
        (0.431976, 1.22306),
        (0.433634, 1.21331),
        (0.435956, 1.20369),
        (0.43889, 1.19421),
        (0.442348, 1.18487),
        (0.446249, 1.17567),
        (0.450539, 1.16664),
        (0.455196, 1.15779),
        (0.460193, 1.14915),
        (0.465484, 1.14069),
        (0.471015, 1.1324),
        (0.476746, 1.12428),
        (0.482662, 1.11633),
        (0.488779, 1.10854),
        (0.495122, 1.10092),
        (0.501714, 1.09343),
        (0.508571, 1.08604),
        (0.5157, 1.07871),
        (0.523085, 1.07145),
        (0.53066, 1.06427),
        (0.538271, 1.05728),
        (0.545657, 1.05058),
        (0.552462, 1.04428),
        (0.558311, 1.03848),
        (0.562953, 1.03323),
        (0.566423, 1.02845),
        (0.569146, 1.02397),
        (0.0, 1.0),
    ]

    ri.AttributeBegin()
    ri.Translate(x, y, z)
    ri.Scale(S, S, S)

    ri.ShadingRate(0.2)  # 2.0 - 0.2

    for i in range(len(profile) - 1):
        r1, y1 = profile[i]
        r2, y2 = profile[i + 1]
        if abs(r2 - r1) < 0.0001 and abs(y2 - y1) < 0.0001:
            continue

        ri.AttributeBegin()

        if i < 2:
            ri.Pattern("zone1_skin", "z1_out", {})
            # Zone 1 — base
            ri.Bxdf(
                "PxrSurface",
                "zone1",
                {
                    "color diffuseColor": [0.02, 0.015, 0.005],
                    "float diffuseGain": [0.05],
                    "reference color specularFaceColor": ["z1_out:resultSpecular"],
                    "color specularEdgeColor": [0.55, 0.45, 0.22],
                    "float specularRoughness": [0.30],
                    "color specularIor": [1.80, 1.80, 1.80],
                    "int specularFresnelMode": [0],
                },
            )

        elif i < 64:
            # Zone 2 - lower belly
            ri.Attribute(
                "displacementbound",
                {"float sphere": [0.002], "string coordinatesystem": ["object"]},
            )
            ri.Pattern("zone2_skin", "z2_out", {"float grooveAmp": [0.0025]})

            ri.Displace(
                "PxrDisplace",
                "z2_disp",
                {
                    "float dispAmount": [1.0],
                    "reference vector dispVector": ["z2_out:dPdisp"],
                },
            )

            ri.Bxdf(
                "PxrSurface",
                "zone2",
                {
                    "color diffuseColor": [0.03, 0.02, 0.005],
                    "float diffuseGain": [0.08],
                    "reference color specularFaceColor": ["z2_out:resultSpecular"],
                    "color specularEdgeColor": [0.55, 0.45, 0.22],
                    "float specularRoughness": [0.45],
                    "color specularIor": [1.80, 1.80, 1.80],
                    "int specularFresnelMode": [0],
                },
            )

        elif i < 68:
            # Zone 3 — horizontal lathe grooves
            ri.Attribute(
                "displacementbound",
                {"float sphere": [0.015], "string coordinatesystem": ["object"]},
            )
            ri.Pattern("zone3_skin", "z3_out", {"float grooveAmp": [0.0005]})

            ri.Displace(
                "PxrDisplace",
                "z3_disp",
                {
                    "float dispAmount": [1.0],
                    "reference vector dispVector": ["z3_out:dPdisp"],
                },
            )

            ri.Bxdf(
                "PxrSurface",
                "zone3",
                {
                    "color diffuseColor": [0.02, 0.015, 0.005],
                    "float diffuseGain": [0.04],
                    "reference color specularFaceColor": ["z3_out:resultSpecular"],
                    "color specularEdgeColor": [0.55, 0.45, 0.22],
                    "float specularRoughness": [0.40],
                    "color specularIor": [1.80, 1.80, 1.80],
                    "int specularFresnelMode": [0],
                },
            )

        elif i < 103:
            # Zone 4 — art pattern band
            tex_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "textures",
                "TEXTURE_SYMBOLS_ALBEDO_2.tex",
            )
            disp_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "textures",
                "TEXTURE_SYMBOLS_DISP.tex",
            )
            ri.Attribute(
                "displacementbound",
                {"float sphere": [0.015], "string coordinatesystem": ["object"]},
            )
            ri.Pattern(
                "zone4_skin",
                "z4_out",
                {
                    "string texturefile": [tex_path],
                    "string dispfile": [disp_path],
                },
            )

            ri.Displace(
                "PxrDisplace",
                "z4_disp",
                {
                    "float dispAmount": [1.0],
                    "reference vector dispVector": ["z4_out:dPdisp"],
                },
            )

            ri.Bxdf(
                "PxrSurface",
                "zone4",
                {
                    "reference color diffuseColor": ["z4_out:resultRGB"],
                    "float diffuseGain": [0.15],
                    "reference color specularFaceColor": ["z4_out:resultSpecular"],
                    "color specularEdgeColor": [0.80, 0.65, 0.28],
                    "reference float specularRoughness": ["z4_out:resultRough"],
                    "color specularIor": [1.80, 1.80, 1.80],
                    "int specularFresnelMode": [0],
                },
            )

        elif i < 167:
            # Zone 5 — neck
            ri.Attribute(
                "displacementbound",
                {"float sphere": [0.002], "string coordinatesystem": ["object"]},
            )
            ri.Pattern("zone5_skin", "z5_out", {"float grooveAmp": [0.003]})

            ri.Displace(
                "PxrDisplace",
                "z5_disp",
                {
                    "float dispAmount": [1.0],
                    "reference vector dispVector": ["z5_out:dPdisp"],
                },
            )

            ri.ShadingRate(0.2)  # 2.0 - 0.2
            ri.Bxdf(
                "PxrSurface",
                "zone5",
                {
                    "color diffuseColor": [0.02, 0.015, 0.005],
                    "float diffuseGain": [0.05],
                    "reference color specularFaceColor": ["z5_out:resultSpecular"],
                    "color specularEdgeColor": [0.55, 0.45, 0.22],
                    "float specularRoughness": [0.60],
                    "color specularIor": [1.80, 1.80, 1.80],
                    "int specularFresnelMode": [0],
                },
            )

        else:
            # Zone 6 — inner rim
            ri.Pattern("zone6_skin", "z6_out", {})
            ri.Bxdf(
                "PxrSurface",
                "zone6",
                {
                    "color diffuseColor": [0.04, 0.03, 0.008],
                    "float diffuseGain": [0.10],
                    "reference color specularFaceColor": ["z6_out:resultSpecular"],
                    "color specularEdgeColor": [0.82, 0.68, 0.30],
                    "float specularRoughness": [0.40],
                    "color specularIor": [1.80, 1.80, 1.80],
                    "int specularFresnelMode": [0],
                },
            )

        ri.TransformBegin()
        ri.Translate(0, y1, 0)
        ri.Rotate(-90, 1, 0, 0)
        ri.Hyperboloid([r1, 0, 0], [r2, 0, y2 - y1], 360)
        ri.TransformEnd()

        ri.AttributeEnd()

    ri.TransformBegin()
    ri.Rotate(90, 1, 0, 0)
    ri.Disk(0, profile[1][0], 360)
    ri.TransformEnd()

    ri.AttributeEnd()


# ── Surrondings


def make_ground_plane(ri):
    albedo_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "textures",
        "TEXTURE_FLOOR_WOOD_ALBEDO.tex",
    )
    rough_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "textures",
        "TEXTURE_FLOOR_WOOD_ROUG.tex",
    )

    ri.AttributeBegin()
    ri.Pattern(
        "ground_wood",
        "gw_out",
        {
            "string albedofile": [albedo_path],
            "string roughfile": [rough_path],
            "float tileScale": [1.0],
        },
    )
    ri.Bxdf(
        "PxrSurface",
        "ground_material",
        {
            "reference color diffuseColor": ["gw_out:resultRGB"],
            "float diffuseGain": [0.6],
            "color specularFaceColor": [0.20, 0.14, 0.08],
            "color specularEdgeColor": [0.18, 0.15, 0.12],
            "reference float specularRoughness": ["gw_out:resultRough"],
            "color specularIor": [1.50, 1.50, 1.50],
            "int specularFresnelMode": [0],
        },
    )
    ri.Rotate(-25, 0, 1, 0)
    ri.Patch(
        "bilinear",
        {
            "P": [
                -30,
                GROUND_Y,
                30,
                30,
                GROUND_Y,
                30,
                -30,
                GROUND_Y,
                -30,
                30,
                GROUND_Y,
                -30,
            ]
        },
    )
    ri.AttributeEnd()


def make_back_wall(ri):
    ri.AttributeBegin()
    ri.Bxdf("PxrDiffuse", "wall_mat", {"color diffuseColor": [0.85, 0.82, 0.78]})
    ri.Patch(
        "bilinear",
        {
            "P": [
                -30,
                GROUND_Y,
                20,
                30,
                GROUND_Y,
                20,
                -30,
                20,
                20,
                30,
                20,
                20,
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


# ── Helpers


def AimZ(ri, direction):
    dx, dy, dz = direction
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / length, dy / length, dz / length
    yaw = math.degrees(math.atan2(dx, dz))
    pitch = math.degrees(math.asin(-dy))
    ri.Rotate(yaw, 0, 1, 0)
    ri.Rotate(pitch, 1, 0, 0)
