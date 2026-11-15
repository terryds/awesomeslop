# A small band: three birds, a record player, a guitar, a drum and a piano, in one room.
# 30 seconds, posed entirely from the time; rendered with Blender (EEVEE).
#   blender -b --factory-startup -P band.py -- <first> <last> <size> <outdir> [samples]
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Matrix, Euler

PI = math.pi
FPS = 24
OFF = 1.56          # where the music starts in the track, just after the needle drops
BEAT = 0.75         # 80 bpm
C1, C2, C3, C4 = OFF + 6, OFF + 12, OFF + 18, OFF + 24
CUTS = [0.0, C1, C2, C3, C4, 30.0]

a = sys.argv[sys.argv.index("--") + 1:]
FIRST, LAST, SIZE, OUT = int(a[0]), int(a[1]), int(a[2]), a[3]
SAMPLES = int(a[4]) if len(a) > 4 else 32

bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
COL = S.collection
S.render.engine = "BLENDER_EEVEE"
S.render.resolution_x = S.render.resolution_y = SIZE
S.render.fps = FPS
S.render.image_settings.file_format = "PNG"
S.render.image_settings.color_mode = "RGB"
S.eevee.taa_render_samples = SAMPLES
S.eevee.use_raytracing = True
S.eevee.use_shadows = True
try:
    S.eevee.ray_tracing_options.resolution_scale = "2"
    S.eevee.use_fast_gi = True
    S.eevee.shadow_ray_count = 2
    S.eevee.shadow_step_count = 6
except Exception as e:
    print("OPT", e)
S.view_settings.view_transform = "AgX"
try:
    S.view_settings.look = "AgX - Punchy"
except Exception as e:
    print("LOOK", e)
rng = random.Random(5)


# ---------------------------------------------------------------- helpers
def lin(c):
    c = c.lstrip("#")
    v = [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in v)


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def smooth(e0, e1, x):
    t = clamp((x - e0) / (e1 - e0))
    return t * t * (3 - 2 * t)


def lerp(p, q, t):
    return p + (q - p) * t


MATS = {}


def mat(color, rough=0.6, metal=0.0, sheen=0.0, coat=0.0, emit=None, estr=1.0):
    key = (color, rough, metal, sheen, coat, emit, estr)
    if key in MATS:
        return MATS[key]
    m = bpy.data.materials.new("m")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(color), 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    for k, v in (("Sheen Weight", sheen), ("Coat Weight", coat)):
        if k in b.inputs:
            b.inputs[k].default_value = v
    if emit:
        b.inputs["Emission Color"].default_value = (*lin(emit), 1)
        b.inputs["Emission Strength"].default_value = estr
    MATS[key] = m
    return m


def add(me, m, loc=(0, 0, 0), rot=(0, 0, 0), smooth_=True, bevel=0.0, seg=3, parent=None, shadow=True):
    if smooth_:
        me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    o = bpy.data.objects.new("o", me)
    COL.objects.link(o)
    o.location, o.rotation_euler = loc, rot
    me.materials.append(m)
    if bevel:
        md = o.modifiers.new("b", "BEVEL")
        md.width, md.segments, md.limit_method, md.angle_limit = bevel, seg, "ANGLE", 0.6
    if parent:
        o.parent = parent
    o.visible_shadow = shadow
    return o


def mesh(bm):
    me = bpy.data.meshes.new("m")
    bm.to_mesh(me)
    bm.free()
    return me


def box(size, m, loc=(0, 0, 0), bevel=0.04, **kw):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1, matrix=Matrix.Diagonal((*size, 1)))
    return add(mesh(bm), m, loc, bevel=bevel, **kw)


def cyl(r, h, m, loc=(0, 0, 0), r2=None, seg=48, bevel=0.02, **kw):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    return add(mesh(bm), m, loc, bevel=bevel, **kw)


def ball(r, m, loc=(0, 0, 0), scale=(1, 1, 1), seg=32, **kw):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(8, seg // 2), radius=r, matrix=Matrix.Diagonal((*scale, 1)))
    return add(mesh(bm), m, loc, **kw)


def tube(pts, r, m, parent=None, nurbs=True, res=5):
    cu = bpy.data.curves.new("t", "CURVE")
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = "3D", r, res, True
    sp = cu.splines.new("NURBS" if nurbs else "POLY")
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1)
    if nurbs:
        sp.use_endpoint_u = True
        sp.order_u = min(4, len(pts))
    o = bpy.data.objects.new("t", cu)
    COL.objects.link(o)
    cu.materials.append(m)
    if parent:
        o.parent = parent
    return o


def empty(loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    o = bpy.data.objects.new("e", None)
    COL.objects.link(o)
    o.location, o.rotation_euler = loc, rot
    if parent:
        o.parent = parent
    return o


def light(kind, loc, energy, color, size=1.0, target=None, parent=None, **kw):
    l = bpy.data.lights.new("l", kind)
    l.energy, l.color = energy, lin(color)
    if kind == "AREA":
        l.size = size
    elif kind == "SUN":
        l.angle = size
    else:
        l.shadow_soft_size = size
    for k, v in kw.items():
        setattr(l, k, v)
    o = bpy.data.objects.new("l", l)
    COL.objects.link(o)
    o.location = loc
    if target:
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    if parent:
        o.parent = parent
    return o


def aim(o, p, q):
    """Put o at p with its +Z axis pointing at q."""
    o.location = p
    o.rotation_euler = (Vector(q) - Vector(p)).to_track_quat("Z", "Y").to_euler()


# ================================================================ the room
wall_c, floor_c = "#3d5f66", "#a8734a"
fm = bpy.data.materials.new("floor")
fm.use_nodes = True
nt = fm.node_tree
bs = nt.nodes["Principled BSDF"]
bs.inputs["Roughness"].default_value = 0.42
tc = nt.nodes.new("ShaderNodeTexCoord")
mp = nt.nodes.new("ShaderNodeMapping")
mp.inputs["Rotation"].default_value = (0, 0, PI / 2)
nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
br = nt.nodes.new("ShaderNodeTexBrick")
br.inputs["Color1"].default_value = (*lin("#b07a4e"), 1)
br.inputs["Color2"].default_value = (*lin("#96653f"), 1)
br.inputs["Mortar"].default_value = (*lin("#5f3d27"), 1)
br.inputs["Scale"].default_value = 1.0
br.inputs["Mortar Size"].default_value = 0.012
br.inputs["Brick Width"].default_value = 9.0
br.inputs["Row Height"].default_value = 1.3
nt.links.new(mp.outputs[0], br.inputs["Vector"])
nt.links.new(br.outputs["Color"], bs.inputs["Base Color"])
box((70, 60, 1), fm, (0, -8, -0.5), bevel=0)
wm = mat(wall_c, 0.9)
box((70, 1, 34), wm, (0, 12.5, 16), bevel=0)
box((70, 0.3, 1.2), mat("#e6dccb", 0.6), (0, 11.9, 0.6))
# left wall with a window in it
WX = -26
for size, loc in (((1, 60, 6), (WX - 0.5, -8, 3)), ((1, 60, 16), (WX - 0.5, -8, 25)),
                  ((1, 2.5, 11), (WX - 0.5, 10.75, 11.5)), ((1, 37, 11), (WX - 0.5, -17.5, 11.5))):
    box(size, wm, loc, bevel=0)
frame = mat("#efe5d2", 0.5)
for size, loc in (((0.5, 9, 0.4), (WX, 5.25, 6.1)), ((0.5, 9, 0.4), (WX, 5.25, 16.9)), ((0.5, 0.4, 11), (WX, 1.1, 11.5)),
                  ((0.5, 0.4, 11), (WX, 9.4, 11.5)), ((0.4, 0.25, 11), (WX, 5.25, 11.5)), ((0.4, 8.5, 0.25), (WX, 5.25, 11.5))):
    box(size, frame, loc)
box((1.6, 9.6, 0.3), frame, (WX + 0.6, 5.25, 5.85))
box((0.1, 40, 40), mat("#ffc98a", 0.9, emit="#ffb46a", estr=2.2), (WX - 6, 5, 12), bevel=0, shadow=False)
# rug
cyl(11.5, 0.12, mat("#c9654b", 0.95, sheen=0.6), (0.5, 2.6, 0.06), seg=72, bevel=0.03).scale = (1, 0.62, 1)
cyl(9.6, 0.13, mat("#ecd9b8", 0.95, sheen=0.6), (0.5, 2.6, 0.07), seg=72, bevel=0.0).scale = (1, 0.62, 1)
cyl(8.6, 0.14, mat("#d9805f", 0.95, sheen=0.6), (0.5, 2.6, 0.08), seg=72, bevel=0.0).scale = (1, 0.62, 1)

# ---------------------------------------------------------------- sideboard, record player, speaker, lamp
walnut = mat("#7a4c32", 0.42, coat=0.3)
box((16, 4.6, 5.4), walnut, (-14.5, 9.6, 4.3), bevel=0.12)
for k in range(3):
    box((4.9, 0.1, 4.6), mat("#8a5a3c", 0.42, coat=0.3), (-19.7 + k * 5.2, 7.28, 4.3), bevel=0.05)
    cyl(0.14, 0.2, mat("#d9b36a", 0.3, metal=1), (-17.6 + k * 5.2, 7.2, 4.6), rot=(PI / 2, 0, 0))
for fx in (-21.6, -7.4):
    for fy in (8.0, 11.2):
        cyl(0.22, 1.6, mat("#3a2a22", 0.5), (fx, fy, 0.8), r2=0.14)
TOP = 7.0
PX, PY = -13.4, 9.5                                # the player
plinth = mat("#2f7377", 0.33, coat=0.6)
chrome = mat("#c9ccd2", 0.22, metal=1.0)
dark = mat("#1b1c20", 0.5)
box((4.6, 3.5, 0.55), plinth, (PX + 0.6, PY, TOP + 0.4), bevel=0.12, seg=5)
for fx in (-1.4, 2.6):
    for fy in (-1.4, 1.4):
        cyl(0.22, 0.14, dark, (PX + fx, PY + fy, TOP + 0.07))
cyl(1.62, 0.12, chrome, (PX, PY, TOP + 0.735), seg=72, bevel=0.03)
rec = bpy.data.materials.new("vinyl")
rec.use_nodes = True
nt = rec.node_tree
bs = nt.nodes["Principled BSDF"]
bs.inputs["Base Color"].default_value = (0.012, 0.012, 0.014, 1)
bs.inputs["Roughness"].default_value = 0.26
tc = nt.nodes.new("ShaderNodeTexCoord")
wv = nt.nodes.new("ShaderNodeTexWave")
wv.wave_type, wv.rings_direction = "RINGS", "Z"
wv.inputs["Scale"].default_value = 24
wv.inputs["Distortion"].default_value = 0.0
nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
bp = nt.nodes.new("ShaderNodeBump")
bp.inputs["Strength"].default_value = 0.4
nt.links.new(wv.outputs[1], bp.inputs["Height"])
nt.links.new(bp.outputs[0], bs.inputs["Normal"])
SPIN = empty((PX, PY, TOP + 0.83))
cyl(1.5, 0.03, rec, seg=96, bevel=0.008, parent=SPIN)
cyl(0.52, 0.012, mat("#f08a5d", 0.6), (0, 0, 0.018), bevel=0, parent=SPIN)
cyl(0.30, 0.012, mat("#fff1d6", 0.6), (0, 0, 0.022), bevel=0, parent=SPIN)
box((0.34, 0.08, 0.01), mat("#3a2a3a", 0.6), (0.0, 0.40, 0.026), bevel=0, parent=SPIN)
box((0.2, 0.05, 0.01), mat("#3a2a3a", 0.6), (0.1, -0.41, 0.026), bevel=0, parent=SPIN)
cyl(0.045, 0.16, chrome, (0, 0, 0.07), parent=SPIN, bevel=0.01)
# tone arm, hinged at the pivot
PIV = Vector((PX + 2.15, PY + 1.05, TOP + 1.12))
cyl(0.2, 0.34, chrome, (PIV.x, PIV.y, TOP + 0.84), bevel=0.03)
ARM = empty(PIV)
cyl(0.11, 0.2, dark, (0, 0, -0.04), bevel=0.02, parent=ARM)
AL = 2.05
tube([(0.75, 0, 0), (0, 0, 0), (-AL * 0.6, 0, 0.03), (-AL, 0, -0.03)], 0.035, chrome, parent=ARM)
cyl(0.15, 0.36, dark, (0.72, 0, 0), rot=(0, PI / 2, 0), bevel=0.03, parent=ARM)
box((0.34, 0.2, 0.09), dark, (-AL, 0, -0.05), bevel=0.02, parent=ARM)
cyl(0.16, 0.12, chrome, (PX + 2.45, PY - 1.25, TOP + 0.72), bevel=0.03)
cyl(0.11, 0.1, chrome, (PX + 1.95, PY - 1.25, TOP + 0.71), bevel=0.03)
ball(0.05, mat("#ff7a3a", 0.3, emit="#ff7a3a", estr=6), (PX + 1.5, PY - 1.3, TOP + 0.69), seg=12)
# speaker
spk = mat("#4a3327", 0.5, coat=0.2)
box((2.6, 2.4, 4.0), spk, (-20.3, 10.0, TOP + 2.0), bevel=0.1)
CONES = []
for cz_, r in ((TOP + 1.35, 0.85), (TOP + 3.05, 0.42)):
    cyl(r + 0.12, 0.1, mat("#c9ccd2", 0.3, metal=1), (-20.3, 8.78, cz_), rot=(PI / 2, 0, 0), bevel=0.02)
    CONES.append(cyl(r, 0.14, mat("#15161a", 0.7), (-20.3, 8.72, cz_), r2=r * 0.3, rot=(-PI / 2, 0, 0), bevel=0.0))
# lamp and sleeves
brass = mat("#c9a45a", 0.3, metal=1.0)
LX, LY = -8.3, 10.3
cyl(0.5, 0.12, brass, (LX, LY, TOP + 0.06), bevel=0.04)
tube([(LX, LY, TOP + 0.1), (LX, LY, TOP + 2.3)], 0.05, brass)
cyl(0.95, 1.05, mat("#ffd9a0", 0.8, emit="#ffb866", estr=3.0), (LX, LY, TOP + 2.75), r2=0.55, bevel=0)
light("POINT", (LX, LY, TOP + 2.2), 1500, "#ffc27a", 0.4)
for i, c in enumerate(("#e76f51", "#f4d58d", "#84a98c")):
    s_ = box((2.6, 0.07, 2.6), mat(c, 0.7), (-10.6 + i * 0.22, 11.45 - i * 0.14, TOP + 1.32), bevel=0.012)
    s_.rotation_euler = (-0.16, 0, 0.04 * i)

# ---------------------------------------------------------------- piano
ivory, pdark = mat("#ece2cf", 0.35, coat=0.5), mat("#2b2623", 0.3, coat=0.6)
QX = 12.0
box((16.2, 3.2, 12.4), ivory, (QX, 10.3, 6.2), bevel=0.14)
box((16.8, 3.6, 0.4), ivory, (QX, 10.2, 12.6), bevel=0.1)
box((16.2, 2.9, 1.1), ivory, (QX, 7.3, 6.85), bevel=0.1)
for sx in (-1, 1):
    box((0.75, 3.1, 2.0), ivory, (QX + sx * 7.75, 7.4, 7.9), bevel=0.14)
    box((0.9, 0.9, 6.4), ivory, (QX + sx * 7.5, 6.3, 3.2), bevel=0.14)
box((14.75, 0.5, 1.5), ivory, (QX, 8.55, 8.25), bevel=0.1).rotation_euler = (0.12, 0, 0)
box((7.5, 0.16, 2.3), ivory, (QX, 8.45, 10.3), bevel=0.05).rotation_euler = (-0.22, 0, 0)
box((7.9, 0.5, 0.2), ivory, (QX, 8.42, 9.2), bevel=0.05)
for dx in (-1.3, 1.3):
    sh = box((2.3, 0.04, 2.0), mat("#fbf7ec", 0.8), (QX + dx, 8.2, 10.32), bevel=0)
    sh.rotation_euler = (-0.22, 0, 0)
    for k in range(5):
        l_ = box((1.9, 0.02, 0.035), mat("#55504a", 0.8), (QX + dx, 8.2 - 0.03 + 0.07 * k, 9.75 + 0.3 * k), bevel=0)
        l_.rotation_euler = (-0.22, 0, 0)
for dx in (-0.7, 0, 0.7):
    box((0.3, 1.1, 0.12), brass, (QX + dx, 8.3, 0.5), bevel=0.04)
NW = 49
KW = 0.29
KX0 = QX - NW * KW / 2 + KW / 2
KEYS, BLACK = [], []
wkey, bkey = mat("#fbf8f0", 0.25, coat=0.4), mat("#1c1a1a", 0.3, coat=0.5)
for i in range(NW):
    e = empty((KX0 + i * KW, 8.25, 7.5))
    box((KW - 0.03, 1.9, 0.26), wkey, (0, -0.95, 0), bevel=0.025, parent=e)
    KEYS.append(e)
    if i % 7 in (0, 1, 3, 4, 5) and i < NW - 1:
        e2 = empty((KX0 + (i + 0.5) * KW, 8.25, 7.68))
        box((0.16, 1.15, 0.26), bkey, (0, -0.6, 0), bevel=0.03, parent=e2)
        BLACK.append(e2)
# on top: a metronome and a plant
cone_ = cyl(0.55, 1.5, mat("#8a5a3c", 0.4, coat=0.4), (QX + 5.2, 10.1, 13.55), r2=0.2, seg=4, bevel=0.03, smooth_=False)
cone_.rotation_euler = (0, 0, PI / 4)
TICK = empty((QX + 5.2, 9.66, 13.05))
box((0.06, 0.03, 1.3), brass, (0, 0, 0.65), bevel=0, parent=TICK)
box((0.2, 0.06, 0.2), brass, (0, 0, 0.95), bevel=0.02, parent=TICK)
cyl(0.5, 0.8, mat("#e8e1d5", 0.5), (QX - 5.6, 10.2, 13.2), r2=0.62, bevel=0.03)
leafm = mat("#4f8f5f", 0.5)
for i in range(9):
    an = i * 2.4
    r = 0.25 + 0.06 * i
    lf = ball(0.55, leafm, (QX - 5.6 + math.cos(an) * r, 10.2 + math.sin(an) * r, 14.0 + 0.17 * i), (0.5, 0.2, 1.0), seg=16)
    lf.rotation_euler = (0.55 * math.sin(an), 0.55 * math.cos(an), an)

# ---------------------------------------------------------------- guitar
GS = 0.8
GROOT = empty((-3.2, 5.2, 0.55), rot=(PI / 2 - 0.2, 0, 0.12))
GROOT.scale = (GS,) * 3
spruce, maho, ebony = mat("#e3b072", 0.38, coat=0.5), mat("#7b3f25", 0.35, coat=0.5), mat("#241a16", 0.4)


def gw(y):
    wl = 1.9 * math.sqrt(max(0.0, 1 - ((y - 1.75) / 1.76) ** 2))
    wu = 1.45 * math.sqrt(max(0.0, 1 - ((y - 4.15) / 1.16) ** 2))
    return (wl ** 5 + wu ** 5) ** 0.2


ys = [5.3 * (0.5 - 0.5 * math.cos(PI * k / 44)) for k in range(45)]
ring = [(gw(y), y) for y in ys] + [(-gw(y), y) for y in reversed(ys[1:-1])]
n = len(ring)
V = [(x, y, 0.0) for x, y in ring] + [(x, y, -1.0) for x, y in ring]
F = [tuple(range(n)), tuple(reversed(range(n, 2 * n)))] + [(i, n + i, n + (i + 1) % n, (i + 1) % n) for i in range(n)]
me = bpy.data.meshes.new("g")
me.from_pydata(V, [], F)
me.update()
gb = add(me, maho, bevel=0.09, seg=4, parent=GROOT)
me.materials.append(spruce)
me.polygons[0].material_index = 1
cyl(0.62, 0.02, mat("#5a3320", 0.5), (0, 3.3, 0.012), bevel=0, parent=GROOT)
cyl(0.5, 0.03, mat("#120c0a", 0.9), (0, 3.3, 0.016), bevel=0, parent=GROOT)
box((1.7, 0.36, 0.12), ebony, (0, 1.3, 0.06), bevel=0.03, parent=GROOT)
box((0.62, 6.6, 0.42), maho, (0, 8.1, -0.2), bevel=0.1, parent=GROOT)
box((0.66, 7.4, 0.08), ebony, (0, 7.7, 0.045), bevel=0.02, parent=GROOT)
for k in range(1, 15):
    fy = 11.4 - (11.4 - 1.3) * (1 - 2 ** (-k / 12))
    box((0.66, 0.035, 0.03), chrome, (0, fy, 0.095), bevel=0, parent=GROOT)
hd = box((0.95, 1.9, 0.26), maho, (0, 12.3, -0.22), bevel=0.08, parent=GROOT)
hd.rotation_euler = (-0.18, 0, 0)
for k in range(3):
    for sx in (-1, 1):
        cyl(0.11, 0.2, chrome, (sx * 0.62, 11.75 + k * 0.5, -0.2 - 0.09 * k), rot=(0, PI / 2, 0), parent=GROOT)
STRINGS = []
for k in range(6):
    x = -0.24 + k * 0.096
    st = tube([(x, 1.3, 0.16), (x, 6.35, 0.15), (x, 11.4, 0.14)], 0.012 + 0.003 * (5 - k), mat("#e9e2d0", 0.3, metal=1), parent=GROOT, res=2)
    STRINGS.append((st, x))
steel = mat("#2a2c31", 0.4, metal=1)
tube([(-3.2, 5.9, 0.1), (-3.2, 6.4, 4.2), (-3.15, 6.9, 7.6)], 0.09, steel)
for sx in (-1, 1):
    tube([(-3.2, 6.1, 1.4), (-3.2 + sx * 1.2, 5.4, 0.9), (-3.2 + sx * 1.5, 4.5, 0.75)], 0.07, steel)
    tube([(-3.2, 6.2, 2.4), (-3.2 + sx * 1.9, 6.6, 0.05)], 0.07, steel)
tube([(-3.2, 6.2, 2.4), (-3.2, 8.0, 0.05)], 0.07, steel)
# a stool for the guitarist
cyl(1.25, 0.3, mat("#d9805f", 0.8, sheen=0.5), (-0.55, 4.3, 2.35), bevel=0.1, seg=5)
for k in range(3):
    an = k * 2.094 + 0.5
    tube([(-0.55 + 0.6 * math.cos(an), 4.3 + 0.6 * math.sin(an), 2.2), (-0.55 + 1.1 * math.cos(an), 4.3 + 1.1 * math.sin(an), 0.0)], 0.09, walnut, nurbs=False)

# ---------------------------------------------------------------- drum and hi-hat
DX, DY, DZ = 6.6, 1.2, 3.5
cyl(1.7, 1.25, mat("#d94f4f", 0.25, coat=0.8), (DX, DY, DZ - 0.66), seg=64, bevel=0.0)
for dz in (-1.3, -0.02):
    cyl(1.78, 0.14, chrome, (DX, DY, DZ + dz), seg=64, bevel=0.04)
HEAD = cyl(1.66, 0.04, mat("#f4efe2", 0.6), (DX, DY, DZ + 0.06), seg=64, bevel=0.0)
for k in range(8):
    an = k * PI / 4
    box((0.14, 0.14, 0.7), chrome, (DX + 1.74 * math.cos(an), DY + 1.74 * math.sin(an), DZ - 0.66), rot=(0, 0, an), bevel=0.03)
tube([(DX, DY, DZ - 1.3), (DX, DY, 0.9)], 0.11, steel, nurbs=False)
for k in range(3):
    an = k * 2.094 + 0.3
    tube([(DX, DY, 1.5), (DX + 1.6 * math.cos(an), DY + 1.6 * math.sin(an), 0.05)], 0.08, steel, nurbs=False)
HX, HY, HZ = 3.75, 1.9, 4.75
tube([(HX, HY, 0.05), (HX, HY, HZ + 0.7)], 0.06, steel, nurbs=False)
for k in range(3):
    an = k * 2.094 + 1.2
    tube([(HX, HY, 1.3), (HX + 1.3 * math.cos(an), HY + 1.3 * math.sin(an), 0.05)], 0.07, steel, nurbs=False)
HAT = empty((HX, HY, HZ))
cymb = mat("#d9b05a", 0.28, metal=1.0)
cyl(1.25, 0.14, cymb, (0, 0, 0.09), r2=0.12, seg=64, bevel=0, parent=HAT)
cyl(1.25, 0.14, cymb, (0, 0, -0.07), r2=0.12, seg=64, bevel=0, parent=HAT, rot=(PI, 0, 0))

# ---------------------------------------------------------------- walls: posters, lights, a big plant
for (px, pz, w, h, bg, fg, shape) in ((-17.3, 14.4, 4.6, 5.8, "#f2e3c6", "#e76f51", "disc"), (-11.6, 13.6, 3.6, 3.6, "#22333b", "#f4d58d", "ring"),
                                      (12.6, 18.2, 6.4, 4.4, "#f4d58d", "#3d5a80", "wave")):
    box((w + 0.5, 0.25, h + 0.5), mat("#2b211c", 0.5), (px, 11.85, pz), bevel=0.05)
    box((w, 0.1, h), mat(bg, 0.8), (px, 11.72, pz), bevel=0)
    if shape == "disc":
        cyl(1.5, 0.05, mat(fg, 0.7), (px, 11.66, pz + 0.5), rot=(PI / 2, 0, 0), bevel=0)
        cyl(0.35, 0.06, mat(bg, 0.7), (px, 11.64, pz + 0.5), rot=(PI / 2, 0, 0), bevel=0)
        box((3.2, 0.05, 0.25), mat("#22333b", 0.7), (px, 11.66, pz - 2.0), bevel=0)
    elif shape == "ring":
        for r_, c_ in ((1.3, fg), (0.95, bg), (0.6, "#e76f51"), (0.25, bg)):
            cyl(r_, 0.04 + 0.01 * (1.4 - r_), mat(c_, 0.7), (px, 11.66 - 0.01 * (1.4 - r_), pz), rot=(PI / 2, 0, 0), bevel=0)
    else:
        for k in range(9):
            hh = 0.6 + 1.3 * abs(math.sin(k * 0.9 + 0.4))
            box((0.34, 0.06, hh), mat(fg if k % 3 else "#e76f51", 0.7), (px - 2.3 + k * 0.58, 11.66, pz), bevel=0)
BULBS = []
bulbc = ("#ffd27a", "#ff9b8a", "#9fe0d0", "#ffe9b0")
pts = []
for k in range(41):
    u = k / 40
    x = -25 + 50 * u
    z = 21.0 - 1.5 * math.sin(PI * ((u * 4) % 1)) ** 0.8
    pts.append((x, 11.75, z))
    if k % 2 == 1:
        c_ = bulbc[(k // 2) % 4]
        BULBS.append(ball(0.2, mat(c_, 0.4, emit=c_, estr=5), (x, 11.6, z - 0.22), seg=12, shadow=False))
tube(pts, 0.035, mat("#1d2326", 0.6), nurbs=False, res=2)
cyl(1.3, 2.4, mat("#e8e1d5", 0.55), (-23.2, 9.6, 1.2), r2=1.7, bevel=0.06)
stemm = mat("#3f7a52", 0.5)
for i in range(8):
    an = i * 0.85 + 0.3
    ln, hh = 2.0 + 0.5 * (i % 3), 5.0 + 1.0 * i
    tip = Vector((-23.2 + math.cos(an) * ln, 9.6 + math.sin(an) * ln * 0.6 - 0.6, hh))
    tube([(-23.2, 9.6, 2.2), (-23.2 + math.cos(an) * ln * 0.3, 9.6, hh * 0.6), tuple(tip)], 0.09, stemm)
    lf = ball(1.5, leafm, tip + Vector((math.cos(an) * 0.9, -0.2, 0.2)), (1.0, 0.75, 0.12), seg=20)
    lf.rotation_euler = (0.5, -0.5 * math.cos(an), an)


# ================================================================ birds
def make_bird(color, belly, scale):
    root = empty()
    root.scale = (scale,) * 3
    body = empty(parent=root)
    fe, be = mat(color, 0.75, sheen=0.35), mat(belly, 0.8, sheen=0.35)
    bk, ey = mat("#f0803c", 0.4), mat("#0b0b10", 0.08, coat=1.0)
    ball(1.0, fe, (0, 0, 1.02), (0.95, 0.9, 1.0), parent=body, seg=48)
    ball(0.78, be, (0.26, 0, 0.82), (0.8, 0.86, 0.9), parent=body, seg=40)
    eyes, wings = [], []
    for sgn in (1, -1):
        e = empty((0.72, 0.36 * sgn, 1.42), body)
        ball(0.115, ey, parent=e, seg=24)
        ball(0.035, mat("#ffffff", 0.3, emit="#ffffff", estr=2), (0.08, -0.03 * sgn, 0.06), parent=e, seg=12, shadow=False)
        eyes.append(e)
        ball(0.13, mat("#ff9b8a", 0.8), (0.80, 0.50 * sgn, 1.18), (0.4, 1, 0.7), parent=body, seg=16)
        w = empty((-0.05, 0.80 * sgn, 1.35), body)
        ball(0.55, fe, (-0.07, 0.04 * sgn, -0.42), (0.75, 0.24, 1.0), parent=w)
        wings.append(w)
        ball(0.2, bk, (0.28, 0.3 * sgn, 0.06), (1.5, 0.9, 0.35), parent=body, seg=16)
    bkc = cyl(0.17, 0.34, bk, (1.0, 0, 1.30), r2=0.01, seg=24, bevel=0, parent=body)
    bkc.rotation_euler = (0, PI / 2 + 0.1, 0)
    for dx, tl in ((-0.12, -0.35), (0.0, 0.0), (0.12, 0.35)):
        t_ = ball(0.12, fe, (dx - 0.05, 0, 2.08), (0.6, 0.6, 1.6), parent=body, seg=16)
        t_.rotation_euler = (0, tl, 0)
    tl_ = ball(0.4, fe, (-0.95, 0, 0.75), (1.2, 0.5, 0.35), parent=body)
    tl_.rotation_euler = (0, -0.6, 0)
    return {"root": root, "body": body, "eyes": eyes, "wings": wings, "s": scale}


def pose(b, loc, yaw, hop=0.0, squash=1.0, pitch=0.0, roll=0.0, shut=False, flap=0.0, flap2=None):
    b["root"].location = loc
    b["root"].rotation_euler = (0, 0, yaw)
    b["body"].location = (0, 0, hop / b["s"])
    b["body"].rotation_euler = (roll, pitch, 0)
    k = 1 / math.sqrt(squash)
    b["body"].scale = (k, k, squash)
    for e in b["eyes"]:
        e.scale = (1, 1, 0.12 if shut else 1)
    b["wings"][0].rotation_euler = (-flap, 0, 0)
    b["wings"][1].rotation_euler = (flap if flap2 is None else flap2, 0, 0)


def blink(t, period, ph):
    return ((t + ph) % period) < 0.1


A = make_bird("#f2b02e", "#fff0c4", 0.86)      # listens, then plays the piano
B = make_bird("#5fb7c4", "#eef7f2", 0.84)      # guitar
C = make_bird("#f29aa8", "#fff0ee", 0.80)      # drum
stickm = mat("#e3c08a", 0.5)
STICKS = [cyl(0.045, 1.9, stickm, r2=0.03, seg=12, bevel=0) for _ in range(2)]
for s_ in STICKS:
    s_.data.transform(Matrix.Translation((0, 0, 0.95)))

# ---------------------------------------------------------------- notes that float up
NOTE_COLS = ("#ffb84a", "#ff7a6a", "#5fd0c0", "#ffd98a")


def make_note(ci, double):
    c = NOTE_COLS[ci]
    m = mat(c, 0.4, emit=c, estr=1.6)
    e = empty()
    for k in range(2 if double else 1):
        ball(0.17, m, (k * 0.5, 0, 0), (1.25, 0.6, 0.9), parent=e, seg=16, shadow=False).rotation_euler = (0, -0.4, 0)
        box((0.045, 0.045, 0.72), m, (k * 0.5 + 0.17, 0, 0.36), bevel=0, parent=e, shadow=False)
    if double:
        box((0.55, 0.05, 0.12), m, (0.42, 0, 0.68), bevel=0, parent=e, shadow=False)
    else:
        box((0.3, 0.05, 0.1), m, (0.3, 0, 0.62), bevel=0, parent=e, shadow=False).rotation_euler = (0, 0.5, 0)
    e.scale = (0, 0, 0)
    return e


SOUNDHOLE = Vector((-3.1, 4.55, 3.3))
EVENTS = []                                          # (time, where, sideways drift)
for k in range(18):
    EVENTS.append((OFF + k * 1.5 + 0.2, Vector((PX + rng.uniform(-0.8, 0.8), PY - 0.4, TOP + 1.2)), rng.uniform(-1, 1)))
for k in range(8, 32):
    EVENTS.append((OFF + k * BEAT, SOUNDHOLE + Vector((rng.uniform(-0.4, 0.4), -0.3, 0)), rng.uniform(-1, 1)))
for k in range(48, 64):
    EVENTS.append((OFF + k * 0.375, Vector((KX0 + (12 + (k - 48) * 1.5) * KW, 7.0, 8.3)), rng.uniform(-1, 1)))
for k in range(10):
    EVENTS.append((C4 + 0.05 * k, Vector((rng.uniform(-14, 16), rng.uniform(3, 8), rng.uniform(5, 9))), rng.uniform(-1, 1)))
NOTES = [(make_note(i % 4, i % 3 == 0), ev) for i, ev in enumerate(EVENTS)]

# ---------------------------------------------------------------- light
w = bpy.data.worlds.new("w")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*lin("#33456e"), 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.55
S.world = w
SUN = light("SUN", (0, 0, 0), 5.5, "#ffb070", 0.05)
SUN.rotation_euler = Vector((1, 0.22, -0.42)).to_track_quat("-Z", "Y").to_euler()
light("AREA", (4, -26, 24), 40000, "#b8ccff", 26.0, target=(0, 6, 4))
light("AREA", (-22, 5, 12), 9000, "#ffc890", 8.0, target=(0, 5, 3))
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
COL.objects.link(cam)
S.camera = cam
cam.data.clip_start, cam.data.clip_end = 0.5, 400
cam.data.dof.use_dof = True


def shot(pos, target, lens, focus=None, fstop=1.2):
    cam.location = pos
    cam.rotation_euler = (Vector(target) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.dof.focus_distance = (Vector(focus if focus else target) - Vector(pos)).length
    cam.data.dof.aperture_fstop = fstop


def since(T, t0, period):
    """Seconds since the last event of a train starting at t0; and that event's index."""
    k = math.floor((T - t0) / period)
    return (T - t0) - k * period, k


def hop_arc(tau, period, air, height):
    """A hop that lands exactly on each event: up during the last `air` seconds before it."""
    u = clamp((tau - (period - air)) / air)
    return height * 4 * u * (1 - u)


def land_squash(tau, amt=0.2, rate=9.0):
    return 1 - amt * math.exp(-tau * rate) * math.cos(tau * 22)


# ================================================================ pose everything for time T
def update(T):
    mt = T - OFF                                    # music time
    on = mt >= 0 and T < 28.6                       # is the needle down
    beat_tau, beat_k = since(T, OFF, BEAT) if mt >= 0 else (9, -1)
    pulse = math.exp(-beat_tau * 7) if on else 0.0
    # record player
    SPIN.rotation_euler = (0, 0, -3.46 * T)
    swing = smooth(0.5, 1.1, T) * (1 - smooth(28.9, 29.7, T))
    down = smooth(1.1, 1.36, T) * (1 - smooth(28.6, 28.9, T))
    ARM.rotation_euler = (0, -0.11 + 0.105 * down, lerp(-1.02, -0.50 - 0.004 * T, swing))
    for i, c in enumerate(CONES):
        c.scale = (1, 1 + (1.6 if i == 0 else 0.8) * pulse, 1)
    TICK.rotation_euler = (0, 0.5 * math.sin(PI * mt / BEAT) if on else 0, 0)
    for i, b in enumerate(BULBS):
        b.scale = (0.9 + 0.2 * math.sin(1.7 * T + i * 1.3),) * 3

    # ---- bird A: listens by the record, later walks the keys
    final = T >= C4
    if T < C1:
        wake = smooth(OFF - 0.06, OFF + 0.25, T)
        j = clamp((T - OFF - 0.03) / 0.42)
        jump = 0.9 * math.sin(PI * j) if 0 < j < 1 else 0
        tau = beat_tau if on else 9
        leave = smooth(C1 - 1.2, C1 - 0.3, T)
        pose(A, (PX - 3.45 + 9 * leave, PY - 0.75, TOP + 0.02), 0.32, hop=jump + 0.16 * math.exp(-tau * 6) * wake + 2.2 * math.sin(PI * leave),
             squash=1 - 0.08 * math.exp(-tau * 8) * wake, pitch=0.16 * math.exp(-tau * 5) * wake, roll=0.1 * math.sin(PI * mt / BEAT / 2) * wake,
             shut=T < OFF - 0.04 or blink(T, 3.1, 0.4), flap=0.9 * (math.sin(PI * j) if 0 < j < 1 else 0) + 0.8 * math.sin(PI * leave))
    elif T < C3:
        tau = beat_tau
        pose(A, (KX0 + 12 * KW, 7.25, 7.62), -0.55, hop=0.12 * math.exp(-tau * 6), squash=1 - 0.06 * math.exp(-tau * 8),
             roll=0.1 * math.sin(PI * mt / BEAT / 2), shut=blink(T, 2.3, 1.1))
    elif not final:
        tau, k = since(T, OFF, 0.375)
        k -= 48
        key = 12 + clamp(k, 0, 15) * 1.5
        nxt = 12 + clamp(k + 1, 0, 15) * 1.5
        u = clamp((tau - 0.1) / 0.275)
        x = KX0 + lerp(key, nxt, u * u * (3 - 2 * u)) * KW
        pose(A, (x, 7.25, 7.64 - 0.05 * math.exp(-tau * 14)), -0.55, hop=0.5 * 4 * u * (1 - u), squash=land_squash(tau, 0.16, 12),
             pitch=0.12, shut=blink(T, 2.3, 1.1), flap=0.55 * math.sin(PI * u))
    else:
        tau = T - C4
        pose(A, (KX0 + 24 * KW, 7.25, 7.6), -0.9 - 0.5 * smooth(0.6, 1.6, tau), hop=0, squash=land_squash(tau, 0.28, 5),
             roll=0.09 * math.sin(1.6 * tau), shut=tau > 1.2 and (blink(T, 2.2, 0.3) or tau > 4.6), flap=0.5 * math.exp(-tau * 3))
    # piano keys
    press = {}
    if C3 <= T < C4:
        tau, k = since(T, OFF, 0.375)
        kc = 12 + clamp(k - 48, 0, 15) * 1.5
        for kk in (int(math.floor(kc)), int(math.floor(kc)) + 1):
            press[kk] = math.exp(-tau * 5)
        bt, bk_ = since(T, OFF, 1.5)
        for kk in ((3, 7, 10), (5, 8, 12))[bk_ % 2]:
            press[kk] = max(press.get(kk, 0), math.exp(-bt * 2.2))
    if final:
        for kk in (3, 7, 10, 22, 24, 26, 29):
            press[kk] = math.exp(-(T - C4) * 0.5) * (1 - smooth(28.4, 29.0, T))
    for i, e in enumerate(KEYS):
        e.rotation_euler = (0.075 * press.get(i, 0), 0, 0)

    # ---- bird B: plucks the guitar on every beat
    g_on = T >= C1 - 0.3
    tau, k = since(T, OFF, BEAT) if mt >= 0 else (9, 0)
    reach = clamp((tau - (BEAT - 0.2)) / 0.2) if (g_on and not final) else 0
    peck = max(reach ** 2, math.exp(-tau * 9) if (T >= C1 and not final) else 0)
    if final:
        ft = T - C4
        peck = math.exp(-ft * 2.5)
    pose(B, (-1.0, 4.35, 2.52), PI + 0.42, pitch=0.5 * peck, squash=1 - 0.05 * peck, roll=0.07 * math.sin(PI * mt / BEAT / 2),
         shut=blink(T, 2.7, 0.9) or (final and T > 29.3), flap=0.25 * peck)
    for i, (st, x) in enumerate(STRINGS):
        amp = 0.0
        if C1 <= T < C4 and (k * 5 + 2) % 6 == i:
            amp = 0.055 * math.exp(-tau * 4.5)
        if final:
            amp = 0.075 * math.exp(-(T - C4 - 0.03 * i) * 1.6) if T - C4 > 0.03 * i else 0
        st.data.splines[0].points[1].co = (x + amp * math.sin(T * 150 + i), 6.35, 0.15, 1)

    # ---- bird C: hops on the drum on 2 and 4, taps the hi-hat on every eighth
    d_on = T >= C2
    tau2, k2 = since(T, OFF + BEAT, 2 * BEAT)
    hop = hop_arc(tau2, 2 * BEAT, 0.34, 0.6) if (d_on and not final) else 0
    sq = land_squash(tau2, 0.2, 10) if (d_on and not final) else 1
    if final:
        ft = T - C4
        sq = land_squash(ft, 0.3, 5)
    te, ke = since(T, OFF, 0.375)
    tap = math.exp(-te * 16) if (d_on and not final) else (math.exp(-(T - C4) * 6) if final else 0)
    lift = clamp((te - 0.19) / 0.185) if (d_on and not final) else 0
    croot = Vector((DX + 0.25, DY + 0.1, DZ + 0.08))
    pose(C, croot, -PI / 2 - 0.35, hop=hop, squash=sq, roll=0.08 * math.sin(PI * mt / BEAT), shut=blink(T, 2.9, 1.7) or (final and T > 29.3),
         flap=0.5 + 0.3 * lift, flap2=0.7 + 0.4 * math.sin(PI * mt / BEAT))
    HEAD.location.z = DZ + 0.06 - 0.03 * (math.exp(-tau2 * 12) if (d_on and not final) else 0)
    HAT.rotation_euler = (0.07 * tap * math.sin(T * 60), 0.05 * tap * math.cos(T * 47), 0)
    hand = croot + Vector((-0.75, -0.25, 1.05 + hop))
    tipz = HZ + 0.2 + 0.75 * math.sin(PI * lift) * (1 if d_on else 0)
    aim(STICKS[0], hand, (HX + 0.85, HY - 0.35, tipz))
    hand2 = croot + Vector((0.72, -0.35, 1.0 + hop))
    aim(STICKS[1], hand2, hand2 + Vector((0.5, -0.9, 0.9 + 0.5 * math.sin(PI * mt / BEAT))))

    # ---- notes
    for e, (t0, p0, dr) in NOTES:
        age = (T - t0) / 2.6
        if 0 <= age < 1 and T < 29.6:
            e.location = p0 + Vector((0.5 * dr * age + 0.25 * math.sin(4 * age + dr * 3), -0.3 * age, 3.4 * age ** 0.8))
            e.rotation_euler = (0, 0.3 * math.sin(5 * age + dr), 0.25 * dr)
            sc = 1.25 * smooth(0, 0.15, age) * (1 - smooth(0.7, 1.0, age))
            e.scale = (sc, sc, sc)
        else:
            e.scale = (0, 0, 0)

    # ---- camera
    if T < C1:
        u = T / C1
        shot((PX + 3.6 - 1.4 * u, PY - 11.5 + 1.2 * u, TOP + 4.4 - 0.4 * u), (PX - 0.9, PY - 0.2, TOP + 1.0), 50, focus=(PX, PY, TOP + 0.9), fstop=0.6)
    elif T < C2:
        u = (T - C1) / 6
        shot((1.6 - 0.9 * u, -5.6 + 0.9 * u, 4.3), (-2.3, 4.6, 3.35), 52, focus=(-2.2, 4.4, 3.3), fstop=0.6)
    elif T < C3:
        u = (T - C2) / 6
        shot((3.4 + 1.2 * u, -8.6 + 0.8 * u, 6.2 - 0.3 * u), (5.5, 1.6, 4.3), 50, focus=(DX, DY, DZ + 0.8), fstop=0.6)
    elif T < C4:
        u = (T - C3) / 6
        bx_ = KX0 + (12 + 22.5 * u) * KW
        shot((bx_ - 4.6, -0.6, 10.2), (bx_ + 0.5, 7.4, 8.45), 48, focus=(bx_, 7.25, 8.2), fstop=0.6)
    else:
        u = smooth(0, 30 - C4, T - C4)
        shot((0.5, -29 - 4 * u, 8.2 + 1.0 * u), (0.5, 7, 8.6), 32, focus=(0, 5, 5), fstop=2.0)

os.makedirs(OUT, exist_ok=True)
for f in range(FIRST, LAST + 1):
    path = os.path.join(OUT, f"f_{f:04d}.png")
    if os.path.exists(path):
        continue
    S.frame_set(f)
    update(f / FPS)
    S.render.filepath = path
    bpy.ops.render.render(write_still=True)
