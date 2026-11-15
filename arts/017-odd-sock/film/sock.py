# odd sock: a disco-pop music video in a laundromat at night.
# 76 seconds, posed entirely from the time and from measurements of the song (data.json); rendered with Blender (EEVEE).
#   blender -b --factory-startup -P sock.py -- <first> <last> <size> <outdir> [samples]
import bpy, bmesh, math, sys, os, random, json
from mathutils import Vector, Matrix

PI = math.pi
FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "data.json")))
BEAT, B0 = D["beat"], D["beat0"]           # 0.5 s, first beat at 0.104 s
NF = len(D["vocals"])
LEN = 76.07
# sections of the song (each starts on a bar line)
S_V, S_P, S_CA, S_CB, S_BR, S_RA, S_RB, S_OUT = (B0 + x for x in (8, 24, 32, 40, 48, 56, 64, 72))

a = sys.argv[sys.argv.index("--") + 1:]
FRAMES = [int(x) for x in a[0].split(",") if x] if "," in a[0] else list(range(int(a[0]), int(a[1]) + 1))   # "12,40,90 -" renders just those
SIZE, OUT = int(a[2]), a[3]
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
    S.eevee.shadow_ray_count = 1
    S.eevee.shadow_step_count = 6
    S.eevee.volumetric_tile_size = "4"
    S.eevee.volumetric_samples = 48
    S.eevee.volumetric_end = 120
except Exception as e:
    print("OPT", e)
S.view_settings.view_transform = "AgX"
try:
    S.view_settings.look = "AgX - Punchy"
except Exception as e:
    print("LOOK", e)
rng = random.Random(11)


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


def vlerp(p, q, t):
    return tuple(lerp(x, y, t) for x, y in zip(p, q))


def mixc(c1, c2, t):
    return tuple(lerp(x, y, t) for x, y in zip(lin(c1), lin(c2)))


MATS = {}


def mat(color, rough=0.6, metal=0.0, sheen=0.0, coat=0.0, emit=None, estr=1.0, alpha=1.0, uniq=None):
    key = (color, rough, metal, sheen, coat, emit, estr, alpha, uniq)
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
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    MATS[key] = m
    return m


def glow(m, strength, color=None):
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Strength"].default_value = strength
    if color is not None:
        b.inputs["Emission Color"].default_value = (*color, 1)


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


def cyl(r, h, m, loc=(0, 0, 0), r2=None, seg=48, bevel=0.02, caps=True, **kw):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=caps, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    return add(mesh(bm), m, loc, bevel=bevel, **kw)


def ball(r, m, loc=(0, 0, 0), scale=(1, 1, 1), seg=32, **kw):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(8, seg // 2), radius=r, matrix=Matrix.Diagonal((*scale, 1)))
    return add(mesh(bm), m, loc, **kw)


def tube(pts, r, m, parent=None, nurbs=True, res=5, cyclic=False):
    cu = bpy.data.curves.new("t", "CURVE")
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = "3D", r, res, True
    sp = cu.splines.new("NURBS" if nurbs else "POLY")
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1)
    if cyclic:
        sp.use_cyclic_u = True
    elif nurbs:
        sp.use_endpoint_u = True
        sp.order_u = min(4, len(pts))
    o = bpy.data.objects.new("t", cu)
    COL.objects.link(o)
    cu.materials.append(m)
    if parent:
        o.parent = parent
    return o


def ring(r, thick, m, loc=(0, 0, 0), parent=None, n=48):
    """A torus standing in the xz plane (facing the camera)."""
    o = tube([(r * math.cos(2 * PI * k / n), 0, r * math.sin(2 * PI * k / n)) for k in range(n)], thick, m, parent=parent, nurbs=False, cyclic=True)
    o.location = loc
    return o


def empty(loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    o = bpy.data.objects.new("e", None)
    COL.objects.link(o)
    o.location, o.rotation_euler = loc, rot
    if parent:
        o.parent = parent
    return o


def text(body, size, m, loc, depth=0.0, outline=0.0, parent=None, align="CENTER"):
    cu = bpy.data.curves.new("txt", "FONT")
    cu.body, cu.size, cu.align_x, cu.align_y = body, size, align, "CENTER"
    cu.extrude = depth
    if outline:
        cu.fill_mode, cu.bevel_depth, cu.bevel_resolution = "NONE", outline, 3
    o = bpy.data.objects.new("txt", cu)
    COL.objects.link(o)
    cu.materials.append(m)
    o.location, o.rotation_euler = loc, (PI / 2, 0, 0)
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


def point_at(o, target):
    o.rotation_euler = (Vector(target) - o.location).to_track_quat("-Z", "Y").to_euler()


# ---------------------------------------------------------------- the song, as numbers
def smoothed(xs, n):
    out = []
    for i in range(len(xs)):
        w = xs[max(0, i - n): i + n + 1]
        out.append(sum(w) / len(w))
    return out


ENV = {k: D[k] for k in ("vocals", "bass", "drums", "guitar", "other", "mouth", "wide")}
ENV["bass_s"], ENV["vocals_s"], ENV["drums_s"], ENV["other_s"] = (smoothed(D[k], 2) for k in ("bass", "vocals", "drums", "other"))
KICKS = D["kicks"]


def E(name, T):
    x = clamp(T * FPS, 0, NF - 1.001)
    i = int(x)
    xs = ENV[name]
    return lerp(xs[i], xs[i + 1], x - i)


def kick(T, rate=8.0):
    """1 at a kick drum hit, decaying."""
    best = 9.0
    for k in KICKS:
        if k > T + 0.001:
            break
        best = T - k
    return math.exp(-best * rate) if best < 2 else 0.0


def since(T, t0, period):
    k = math.floor((T - t0) / period)
    return (T - t0) - k * period, k


def flick(T, seed=0):
    """A fluorescent tube that cannot make up its mind: 0 or 1."""
    k = int(T * 24) * 7919 + seed * 104729
    return 1.0 if ((k * 2654435761) >> 7) % 5 < 2 else 0.06


# ================================================================ the laundromat
FY, PZ, MH = 5.8, 3.3, 8.6            # machine fronts, porthole height, machine height
TOPZ = MH + 0.3                       # the folding counter on top of the machines: the stage
MXS = (-13.0, -6.5, 0.0, 6.5, 13.0)
WALLX, WALLY, CEIL = 22.0, 12.5, 24.0

# floor: checker tiles, a little wet
fm = bpy.data.materials.new("floor")
fm.use_nodes = True
nt = fm.node_tree
bs = nt.nodes["Principled BSDF"]
bs.inputs["Roughness"].default_value = 0.16
tc = nt.nodes.new("ShaderNodeTexCoord")
ck = nt.nodes.new("ShaderNodeTexChecker")
ck.inputs["Color1"].default_value = (*lin("#e9e2d2"), 1)
ck.inputs["Color2"].default_value = (*lin("#4d7f86"), 1)
ck.inputs["Scale"].default_value = 0.36
nt.links.new(tc.outputs["Object"], ck.inputs["Vector"])
nt.links.new(ck.outputs["Color"], bs.inputs["Base Color"])
box((90, 90, 1), fm, (0.01, -20.01, -0.5), bevel=0)
wallm = mat("#c9ddd2", 0.85)
box((90, 1, 40), wallm, (0, WALLY + 0.5, 12), bevel=0)
for sx in (-1, 1):
    box((1, 90, 40), wallm, (sx * (WALLX + 0.5), -20, 12), bevel=0)
box((90, 90, 1), mat("#aebfb8", 0.9), (0, -20, CEIL + 0.5), bevel=0)
box((44, 0.2, 0.5), mat("#e76f51", 0.6), (0, WALLY - 0.1, 11.6), bevel=0)        # a painted stripe round the room
box((44, 0.2, 0.2), mat("#f2b83a", 0.6), (0, WALLY - 0.1, 12.1), bevel=0)
for sx in (-1, 1):
    box((0.2, 60, 0.5), mat("#e76f51", 0.6), (sx * (WALLX - 0.1), -17, 11.6), bevel=0)
    box((0.2, 60, 0.2), mat("#f2b83a", 0.6), (sx * (WALLX - 0.1), -17, 12.1), bevel=0)

enamel = mat("#f1f0ea", 0.28, coat=0.6)
chrome = mat("#cfd3d8", 0.18, metal=1.0)
steel = mat("#8d949c", 0.35, metal=1.0)
darkm = mat("#14161a", 0.5)
panelm = mat("#22313c", 0.4, coat=0.4)
cream = mat("#f4ecd8", 0.5)
redm = mat("#e2412f", 0.4)
brass = mat("#c9a45a", 0.3, metal=1.0)
copper = mat("#b9683f", 0.3, metal=1.0)


DIALFACE = mat("#f4ecd8", 0.5, emit="#ffe9c0", estr=0.5, uniq="dial")


def plate(mx):
    """The machine's front: a sheet with a round hole for the porthole."""
    R, n = 2.05, 72
    L, Rr, Bt, Tp = -3.15, 3.15, -PZ, 6.0 - PZ
    vs, fs = [], []

    def outer(an):
        c, s = math.cos(an), math.sin(an)
        k = min((Rr if c > 0 else -L) / max(abs(c), 1e-9), (Tp if s > 0 else -Bt) / max(abs(s), 1e-9))
        return (mx + k * c, FY, PZ + k * s)
    corners = [(math.atan2(z, x) % (2 * PI), (mx + x, FY, PZ + z)) for x, z in ((Rr, Tp), (L, Tp), (L, Bt), (Rr, Bt))]
    for k in range(n):
        a0, a1 = 2 * PI * k / n, 2 * PI * (k + 1) / n
        i = len(vs)
        vs += [(mx + R * math.cos(a0), FY, PZ + R * math.sin(a0)), (mx + R * math.cos(a1), FY, PZ + R * math.sin(a1)), outer(a1), outer(a0)]
        fs.append((i, i + 1, i + 2, i + 3))
        for ca, cp in corners:
            if a0 < ca <= a1:
                vs.append(cp)
                fs.append((i + 3, i + 2, len(vs) - 1))
    me = bpy.data.meshes.new("plate")
    me.from_pydata(vs, [], fs)
    me.update()
    return add(me, enamel, smooth_=False)


def make_dial(cx, cy, cz, r, rim, big=False, labels=None):
    """A round gauge facing the camera. Returns the needle (rotate it about y)."""
    cyl(r * 1.12, 0.22, rim, (cx, cy + 0.02, cz), rot=(PI / 2, 0, 0), bevel=0.04)
    cyl(r, 0.24, DIALFACE, (cx, cy, cz), rot=(PI / 2, 0, 0), bevel=0)
    for k in range(13):
        an = lerp(-2.1, 2.1, k / 12)
        hot = k >= 10
        ln = (0.2 if k % 3 == 0 else 0.12) * r
        box((0.045 * r * (1.8 if hot else 1), 0.03, ln), redm if hot else darkm,
            (cx + (0.86 * r - ln / 2) * math.sin(an), cy - 0.125, cz + (0.86 * r - ln / 2) * math.cos(an)), rot=(0, an, 0), bevel=0)
    if labels:
        for txt, an in labels:
            text(txt, 0.2 * r, darkm, (cx + 0.56 * r * math.sin(an), cy - 0.13, cz + 0.56 * r * math.cos(an)))
    nd = empty((cx, cy - 0.16, cz))
    box((0.07 * r, 0.03, 0.95 * r), redm, (0, 0, 0.3 * r), bevel=0, parent=nd)
    cyl(0.12 * r, 0.1, darkm, rot=(PI / 2, 0, 0), bevel=0.01, parent=nd)
    return nd


DRUMS, DOORS, DIALS, LEDS, DLIGHTS, DISPLAYS = [], [], [], [], [], []
LEDCOL = ["#3dff7a"] * 5 + ["#ffc233"] * 2 + ["#ff3b30"]
LED_ON = [mat(c, 0.4, emit=c, estr=7.0) for c in LEDCOL]
LED_OFF = [mat("#20262b", 0.4, emit=c, estr=0.03, uniq="off") for c in LEDCOL]
laundry_cols = ("#e76f51", "#f2b83a", "#3fb8af", "#7c6cf2", "#f29aa8", "#f4f1de", "#4d8fd9")
drum_cols = ("#ff7a3a", "#3fd0ff", "#ffd9a0", "#ff5fa8", "#8a7cff")
for mi, mx in enumerate(MXS):
    plate(mx)
    box((6.3, 6.6, MH - 5.9), enamel, (mx, FY + 3.3, 5.9 + (MH - 5.9) / 2), bevel=0.1)       # the top block, behind the panel
    for sx in (-1, 1):
        box((0.12, 6.6, 6.0), enamel, (mx + sx * 3.09, FY + 3.3, 3.0), bevel=0)
    box((6.3, 6.5, 0.3), darkm, (mx, FY + 3.35, 0.15), bevel=0)
    cyl(2.08, 4.2, mat("#2a2d33", 0.5, metal=0.6), (mx, FY + 2.12, PZ), rot=(PI / 2, 0, 0), bevel=0, caps=False)
    # the drum: turns about y
    dr = empty((mx, FY + 2.0, PZ))
    drm = mat("#aab1b9", 0.32, metal=1.0)
    cyl(1.98, 3.6, drm, rot=(PI / 2, 0, 0), bevel=0, caps=False, parent=dr)
    cyl(1.98, 0.1, drm, (0, 1.8, 0), rot=(PI / 2, 0, 0), bevel=0, parent=dr)
    for k in range(3):
        an = k * 2 * PI / 3
        box((0.5, 3.3, 0.34), mat("#d5dae0", 0.3, metal=1.0), (1.8 * math.cos(an), 0, 1.8 * math.sin(an)), rot=(0, -an + PI / 2, 0), bevel=0.06, parent=dr)
        box((0.16, 0.05, 1.3), darkm, (0.95 * math.cos(an), 1.72, 0.95 * math.sin(an)), rot=(0, -an + PI / 2, 0), bevel=0, parent=dr)
    cyl(0.4, 0.2, chrome, (0, 1.7, 0), rot=(PI / 2, 0, 0), parent=dr)
    blobs = []
    for k in range(7):
        an, rr = rng.uniform(0, 2 * PI), rng.uniform(0.75, 1.3)
        c = laundry_cols[(k + mi * 2) % len(laundry_cols)]
        b = ball(0.62, mat(c, 0.9, sheen=0.7), (rr * math.cos(an), rng.uniform(0.4, 1.2) if mi == 2 else rng.uniform(-0.9, 1.1), rr * math.sin(an)),
                 (rng.uniform(0.7, 1.2), rng.uniform(0.6, 1.0), rng.uniform(0.5, 0.9)), seg=20, parent=dr)
        b.rotation_euler = (rng.uniform(0, 3), rng.uniform(0, 3), rng.uniform(0, 3))
        blobs.append(b)
    DRUMS.append((dr, blobs))
    DLIGHTS.append(light("POINT", (mx, FY + 0.9, PZ + 0.6), 300, drum_cols[mi], 0.5))
    # the door: hinged on its left edge
    hinge = empty((mx - 2.5, FY - 0.12, PZ))
    ring(2.25, 0.3, chrome, (2.5, 0, 0), parent=hinge)
    ring(1.92, 0.1, darkm, (2.5, -0.05, 0), parent=hinge)
    ball(1.95, mat("#cfe9ff", 0.03, coat=1.0, alpha=0.16), (2.5, 0.05, 0), (1, 0.22, 1), parent=hinge, shadow=False)
    box((0.3, 0.34, 1.1), chrome, (4.82, -0.1, 0), bevel=0.08, parent=hinge)
    cyl(0.16, 1.2, chrome, (0, 0.05, 0), bevel=0.03, parent=hinge)
    DOORS.append(hinge)
    # control panel
    box((6.0, 0.3, 2.3), panelm, (mx, FY - 0.1, 7.2), bevel=0.08)
    labels = [("30", -2.1), ("40", -0.7), ("60", 0.7), ("90", 2.1)] if mi == 2 else None
    DIALS.append(make_dial(mx - 1.7, FY - 0.3, 7.2, 0.86, chrome, labels=labels))
    segs = []
    for k in range(8):
        segs.append(box((0.3, 0.08, 0.62), LED_OFF[k], (mx - 0.15 + k * 0.4, FY - 0.27, 7.62), bevel=0.02))
    LEDS.append(segs)
    dm = mat("#ffb347", 0.4, emit="#ffb347", estr=2.0, uniq=mi)
    box((1.9, 0.08, 0.5), dm, (mx + 0.7, FY - 0.27, 6.72), bevel=0.03)
    DISPLAYS.append(dm)
    if mi == 2:
        text("40°", 0.42, darkm, (mx + 0.7, FY - 0.32, 6.72))
    kn = cyl(0.36, 0.3, chrome, (mx + 2.45, FY - 0.35, 6.75), rot=(PI / 2, 0, 0), bevel=0.05)
    for fx in (-2.6, 2.6):
        cyl(0.3, 0.3, darkm, (mx + fx, FY + 0.6, 0.0), bevel=0)
# the folding counter on top
box((33.6, 7.4, 0.3), mat("#e6c79a", 0.35, coat=0.5), (0, FY + 3.3, MH + 0.15), bevel=0.08)
for sx in (-1, 1):
    box((0.4, 6.6, MH), enamel, (sx * 16.45, FY + 3.3, MH / 2), bevel=0.05)

# ---------------------------------------------------------------- the wall: neon, pipes with big gauges, a clothes line
NEON1 = mat("#ff4f9a", 0.4, emit="#ff3d8b", estr=9.0, uniq="n1")
NEON2 = mat("#52e0ff", 0.4, emit="#33d1ff", estr=9.0, uniq="n2")
text("SPIN CYCLE", 3.5, NEON1, (0, WALLY - 0.35, 19.2), outline=0.09)
text("open all night", 1.35, NEON2, (0, WALLY - 0.35, 16.4), outline=0.05)
box((27, 0.15, 6.6), mat("#1c2530", 0.7), (0, WALLY - 0.08, 18.2), bevel=0.05)
NL1 = light("AREA", (0, WALLY - 2.2, 19.2), 3000, "#ff3d8b", 10.0, target=(0, WALLY - 2.2, 0))
NL2 = light("AREA", (0, WALLY - 2.0, 16.2), 1200, "#33d1ff", 8.0, target=(0, WALLY - 2.0, 0))
PIPEZ = 13.6
tube([(15.2, WALLY - 0.6, PIPEZ), (WALLX, WALLY - 0.6, PIPEZ)], 0.28, copper, nurbs=False)
tube([(15.2, WALLY - 0.6, PIPEZ), (15.2, WALLY - 0.6, CEIL)], 0.28, copper, nurbs=False)
BIG = []
BIGX = (-19.0, -15.2, 15.6, 19.4)
for k, gx in enumerate(BIGX):
    gz = 15.6
    BIG.append(make_dial(gx, WALLY - 0.75, gz, 1.55, brass, big=True))
    tube([(gx, WALLY - 0.6, gz - 1.6), (gx, WALLY - 0.6, PIPEZ)], 0.16, copper, nurbs=False)
tube([(-WALLX, WALLY - 0.6, PIPEZ), (-12.8, WALLY - 0.6, PIPEZ)], 0.28, copper, nurbs=False)
tube([(-12.8, WALLY - 0.6, PIPEZ), (-12.8, WALLY - 0.6, CEIL)], 0.28, copper, nurbs=False)
for vx in (-17.1, 17.5):
    cyl(0.5, 0.16, redm, (vx, WALLY - 1.0, PIPEZ), rot=(PI / 2, 0, 0), bevel=0.03)

# clothes line with three pegs: the backing singers
LINEY, LINEZ = 10.2, 13.1
ropem = mat("#efe6d2", 0.8)
tube([(-WALLX, LINEY, LINEZ + 0.5), (-10, LINEY, LINEZ - 0.12), (0, LINEY, LINEZ + 0.3), (10, LINEY, LINEZ - 0.12), (WALLX, LINEY, LINEZ + 0.5)], 0.05, ropem)
woodm = mat("#e0b877", 0.55)


def make_peg(x, tipc):
    root = empty((x, LINEY, LINEZ - 0.05))
    prongs = []
    eyem = mat("#0b0b10", 0.08, coat=1.0)
    for sx in (-1, 1):
        p = empty((sx * 0.02, 0, -0.55), root)                       # pivots at the spring
        box((0.36, 0.5, 2.7), woodm, (sx * 0.2, 0, -0.75), bevel=0.06, parent=p)
        box((0.37, 0.51, 0.55), mat(tipc, 0.5), (sx * 0.2, 0, -1.84), bevel=0.06, parent=p)
        e = empty((sx * 0.2, -0.27, -0.45), p)
        ball(0.12, eyem, parent=e, seg=16)
        ball(0.035, mat("#ffffff", 0.3, emit="#ffffff", estr=2), (0.03, -0.09, 0.05), parent=e, seg=8, shadow=False)
        ball(0.09, mat("#ff9b8a", 0.8), (sx * 0.2, -0.26, -0.8), (1, 0.3, 0.7), parent=p, seg=12)
        prongs.append((p, e))
    ring(0.2, 0.045, steel, (0, 0, -0.55), parent=root, n=16).rotation_euler = (0, 0, PI / 2)
    return {"root": root, "prongs": prongs}


PEGS = [make_peg(x, c) for x, c in ((-11.6, "#ff5fa8"), (-9.4, "#3fd0ff"), (-7.2, "#ffc233"))]

# ---------------------------------------------------------------- ceiling: tubes, spots, the mirror ball
TUBEM = mat("#f4fff6", 0.5, emit="#eafff0", estr=12.0, uniq="tube")
TUBES = []
for tx in (-9.5, 9.5):
    box((11, 1.5, 0.3), mat("#dfe5e2", 0.6), (tx, -1.0, CEIL - 0.15), bevel=0.05)
    box((10.4, 0.5, 0.22), TUBEM, (tx, -1.0, CEIL - 0.36), bevel=0.1, shadow=False)
    TUBES.append(light("AREA", (tx, -1.0, CEIL - 0.7), 0, "#e6fff0", 9.0, target=(tx, -1.0, 0)))
truss = mat("#23272d", 0.5, metal=0.8)
box((40, 0.5, 0.5), truss, (0, -3.0, CEIL - 1.6), bevel=0.05)
SPOTS = []
SPOTX = (-15, -9, -3, 3, 9, 15)
for sx_ in SPOTX:
    h = empty((sx_, -3.0, CEIL - 2.2))
    cyl(0.55, 1.2, truss, (sx_, -3.0, CEIL - 2.3), r2=0.75, bevel=0.03)
    SPOTS.append(light("SPOT", (sx_, -3.0, CEIL - 2.9), 0, "#ffffff", 0.25, target=(sx_ * 0.6, 8, 9), spot_size=0.55, spot_blend=0.5))
FOLLOW = light("SPOT", (2.0, -16.0, CEIL - 2.5), 0, "#fff2e0", 0.4, target=(0, 7.5, 11), spot_size=0.34, spot_blend=0.6)
FILL = light("AREA", (0, -30, 16), 6000, "#9fb4ff", 30.0, target=(0, 6, 8))
BALLP = Vector((0.0, 1.0, 20.6))
BALL = empty((BALLP.x, BALLP.y, 40))
ballm = mat("#dfe6ee", 0.06, metal=1.0, emit="#b9c8ff", estr=0.25)
mb = ball(1.7, ballm, parent=BALL, seg=26, smooth_=False)
BALLT = [mat("#ffffff", 0.1, metal=1.0, emit=c, estr=3.0, uniq="tile") for c in ("#ffffff", "#ffd0e6", "#c8f2ff")]
for m_ in BALLT + [mat("#5a6472", 0.1, metal=1.0)]:
    mb.data.materials.append(m_)
for pl_ in mb.data.polygons:
    q = rng.random()
    pl_.material_index = 0 if q < 0.45 else (4 if q < 0.6 else rng.randint(1, 3))
cyl(0.25, 0.4, truss, (0, 0, 1.8), parent=BALL)
tube([(0, 0, 1.9), (0, 0, 9)], 0.04, truss, parent=BALL, nurbs=False)
# the dots it throws: flat discs laid on whatever surface the ray meets
NDOT = 170
DOTM = [mat(c, 0.5, emit=c, estr=6.0, uniq="dot") for c in ("#ffffff", "#ffd0e6", "#c8f2ff", "#fff0c0")]
DOTS = []
for k in range(NDOT):
    z = rng.uniform(-0.95, 0.35)
    an = rng.uniform(0, 2 * PI)
    r = math.sqrt(1 - z * z)
    o = cyl(0.3, 0.012, DOTM[k % 4], seg=10, bevel=0, shadow=False)
    DOTS.append((o, an, r, z))


def dot_hit(d):
    """Where a ray from the ball lands: (point, surface) for the nearest of the room's planes."""
    best = None
    def tryp(t, kind):
        nonlocal best
        if t > 0.5 and (best is None or t < best[0]):
            p = BALLP + d * t
            ok = True
            if kind == "floor":
                ok = p.y < FY and abs(p.x) < WALLX
            elif kind == "top":
                ok = FY - 0.4 <= p.y <= WALLY and abs(p.x) < 16.8
            elif kind == "front":
                ok = p.z < TOPZ and abs(p.x) < 16.8
            elif kind == "back":
                ok = p.z > 0 and abs(p.x) < WALLX and p.z < CEIL
            elif kind == "side":
                ok = 0 < p.z < CEIL and p.y < WALLY
            if ok:
                best = (t, p, kind)
    if d.z < 0:
        tryp(-BALLP.z / d.z, "floor")
        tryp((TOPZ - BALLP.z) / d.z, "top")
    if d.y > 0:
        tryp((FY - 0.42 - BALLP.y) / d.y, "front")
        tryp((WALLY - 0.2 - BALLP.y) / d.y, "back")
    if abs(d.x) > 1e-6:
        tryp(((WALLX - 0.05) * (1 if d.x > 0 else -1) - BALLP.x) / d.x, "side")
    return best


# ---------------------------------------------------------------- props: a basket, a bench, a mic
bk = mat("#f29aa8", 0.5)
cyl(2.3, 3.2, bk, (-17.5, -1.5, 1.6), r2=2.9, seg=40, bevel=0.08)
for k in range(9):
    an, rr = k * 2.4, 0.4 + 0.2 * (k % 4)
    ball(1.1, mat(laundry_cols[k % 7], 0.9, sheen=0.7), (-17.5 + rr * 2 * math.cos(an), -1.5 + rr * 2 * math.sin(an), 3.3 + 0.12 * k), (1.1, 0.9, 0.55), seg=20)
box((8, 2.4, 0.4), mat("#e6c79a", 0.4, coat=0.4), (16.5, -3.0, 2.6), bevel=0.12)
for fx in (-3.3, 3.3):
    box((0.4, 2.0, 2.4), truss, (16.5 + fx, -3.0, 1.2), bevel=0.06)
MICP = Vector((-0.35, 6.6, TOPZ))
cyl(0.55, 0.1, truss, (MICP.x, MICP.y, TOPZ + 0.05), bevel=0.03)
tube([(MICP.x, MICP.y, TOPZ), (MICP.x, MICP.y, TOPZ + 1.5)], 0.05, chrome, nurbs=False)
MICZ = TOPZ + 1.7
ball(0.24, mat("#3a3d44", 0.35, metal=1.0), (MICP.x, MICP.y, MICZ), seg=20)
cyl(0.13, 0.4, darkm, (MICP.x, MICP.y, MICZ - 0.3), bevel=0.02)


# ================================================================ the cast
SOCKS = 1.2


def make_sock(main, accent, stripe):
    root = empty()
    sq = empty(parent=root)                         # squashes and hops
    knit, acc, st = mat(main, 0.8, sheen=0.25), mat(accent, 0.8, sheen=0.25), mat(stripe, 0.8, sheen=0.25)
    ball(0.95, knit, (0.95, 0, 0.64), (1.62, 0.92, 0.67), parent=sq, seg=40)
    ball(0.95, acc, (2.12, 0, 0.6), (0.42, 0.84, 0.62), parent=sq, seg=32)
    ball(0.8, acc, (-0.36, 0, 0.62), (0.8, 1.0, 0.8), parent=sq, seg=32)
    leg = empty((0, 0, 0.85), sq)
    cyl(0.84, 3.0, knit, (0, 0, 1.5), r2=0.9, parent=leg, bevel=0, seg=40)
    ball(0.86, knit, (0, 0, 0.05), parent=leg, seg=32)
    cyl(0.93, 0.75, acc, (0, 0, 3.1), parent=leg, bevel=0.1, seg=40)
    for k in range(26):
        an = 2 * PI * k / 26
        box((0.06, 0.1, 0.6), acc, (0.925 * math.cos(an), 0.925 * math.sin(an), 3.1), rot=(0, 0, an), bevel=0.02, parent=leg)
    cyl(0.6, 0.06, mat("#2a1a1a", 0.9), (0, 0, 3.47), parent=leg, bevel=0)
    for z_ in (0.42, 0.78):
        cyl(0.87, 0.2, st, (0, 0, z_), parent=leg, bevel=0, seg=40)
    cyl(0.91, 0.14, st, (0, 0, 2.52), parent=leg, bevel=0, seg=40)
    white, black = mat("#ffffff", 0.25, coat=0.6), mat("#0b0b10", 0.08, coat=1.0)
    eyes = []
    for sgn in (1, -1):
        e = empty((0.74, 0.36 * sgn, 1.98), leg)
        ball(0.3, white, parent=e, seg=24)
        pu = ball(0.17, black, (0.24, 0, 0), (0.6, 1, 1), parent=e, seg=20)
        ball(0.045, mat("#ffffff", 0.3, emit="#ffffff", estr=2), (0.1, -0.05, 0.07), parent=pu, seg=10, shadow=False)
        lid = ball(0.315, knit, (0, 0, 0), parent=e, seg=24)
        eyes.append((e, pu, lid))
        ball(0.17, mat("#ff8f7f", 0.85), (0.82, 0.56 * sgn, 1.5), (0.35, 1, 0.65), parent=leg, seg=14)
    mouth = empty((0.9, 0, 1.3), leg)
    ball(0.4, mat("#4a0f1a", 0.6), parent=mouth, seg=24)
    ball(0.23, mat("#f0707a", 0.6), (0.05, 0, -0.2), (1, 1.1, 0.6), parent=mouth, seg=16)
    return {"root": root, "sq": sq, "leg": leg, "eyes": eyes, "mouth": mouth}


def pose_sock(s, loc, yaw, hop=0.0, squash=1.0, lean=0.0, sway=0.0, twist=0.0, shut=0.0, mouth=0.0, wide=1.0, scale=1.0, tumble=0.0, look=(0.0, 0.0), roll=0.0):
    s["root"].location = loc
    s["root"].rotation_euler = (roll, tumble, yaw)
    s["root"].scale = (scale * SOCKS,) * 3
    s["sq"].location = (0, 0, hop)
    k = 1 / math.sqrt(squash)
    s["sq"].scale = (k, k, squash)
    s["leg"].rotation_euler = (sway, lean, twist)
    for e, pu, lid in s["eyes"]:
        lid.scale = (1.0, 1.0, 1.0)
        lid.rotation_euler = (0, lerp(-2.5, -0.2, shut), 0)       # the lid is a cap that rolls down over the eye
        lid.scale = (1.12, 1.12, 1.12)
        pu.location = (0.24 - 0.03 * (abs(look[0]) + abs(look[1])), 0.11 * look[0], 0.11 * look[1])
    s["mouth"].scale = (0.5, 0.75 * lerp(0.85, wide, clamp(mouth * 3)), 0.07 + 0.95 * mouth)


def lid_fix(s):
    """Turn each eyelid from a full ball into a half shell (done once)."""
    for e, pu, lid in s["eyes"]:
        me = lid.data
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x < -0.02], context="VERTS")
        bm.to_mesh(me)
        bm.free()


SOCK = make_sock("#f2b83a", "#e2553f", "#2f9c95")      # the singer
PAIR = make_sock("#f2b83a", "#e2553f", "#2f9c95")      # the one that went missing
lid_fix(SOCK)
lid_fix(PAIR)

# the bass player: a detergent bottle with a rubber-band bass
BOT = empty((9.6, 8.6, TOPZ))
BOTB = empty(parent=BOT)
botm = mat("#3f7fd9", 0.25, coat=0.7)
box((2.7, 1.7, 3.3), botm, (0, 0, 1.65), bevel=0.55, seg=6, parent=BOTB)
cyl(0.5, 0.6, botm, (-0.45, 0, 3.5), parent=BOTB, bevel=0.05)
cyl(0.6, 0.55, redm, (-0.45, 0, 3.95), parent=BOTB, bevel=0.08)
tube([(0.5, 0, 3.2), (1.5, 0, 3.3), (1.75, 0, 2.3), (1.3, 0, 1.6)], 0.2, botm, parent=BOTB)
box((1.9, 0.06, 1.5), cream, (-0.1, -0.86, 2.2), bevel=0.2, parent=BOTB)
for sgn in (-1, 1):
    ball(0.17, mat("#0b0b10", 0.08, coat=1.0), (-0.1 + 0.4 * sgn, -0.92, 2.5), parent=BOTB, seg=16)
    ball(0.05, mat("#ffffff", 0.3, emit="#ffffff", estr=2), (-0.06 + 0.4 * sgn, -1.06, 2.57), parent=BOTB, seg=8, shadow=False)
    ball(0.14, mat("#ff9b8a", 0.8), (-0.1 + 0.72 * sgn, -0.9, 2.15), (1, 0.3, 0.7), parent=BOTB, seg=12)
BMOUTH = ball(0.2, mat("#5a1420", 0.6), (-0.1, -0.9, 2.0), (1, 0.3, 0.5), parent=BOTB, seg=16)
BASS = empty((-0.55, -1.5, 0.75), BOTB, rot=(0, 1.0, 0))
BASS.scale = (0.72,) * 3
bassm = mat("#ff8a3d", 0.3, coat=0.6)
cyl(0.95, 0.3, bassm, rot=(PI / 2, 0, 0), parent=BASS, bevel=0.08)
cyl(0.7, 0.3, bassm, (0, 0, 0.8), rot=(PI / 2, 0, 0), parent=BASS, bevel=0.08)
box((0.3, 0.2, 3.4), mat("#5a3320", 0.4, coat=0.4), (0, -0.05, 2.5), bevel=0.05, parent=BASS)
box((0.46, 0.22, 0.7), bassm, (0, -0.05, 4.4), bevel=0.08, parent=BASS)
box((0.6, 0.1, 0.16), chrome, (0, -0.2, -0.2), bevel=0.02, parent=BASS)
BSTR = []
for k in range(4):
    x = -0.12 + 0.08 * k
    BSTR.append((tube([(x, -0.22, -0.2), (x, -0.2, 1.9), (x, -0.18, 4.1)], 0.014, mat("#e9e2d0", 0.3, metal=1), parent=BASS, res=2), x))
glove = mat("#ffffff", 0.5, sheen=0.5)
HAND1 = ball(0.3, glove, parent=BOTB, seg=20)
HAND2 = ball(0.3, glove, parent=BOTB, seg=20)

# soap bubbles
BUBM = mat("#e8f6ff", 0.02, coat=1.0, alpha=0.2, emit="#bfe4ff", estr=0.35)
BUBS = []
for k in range(70):
    t0 = rng.uniform(S_CB - 0.5, S_BR - 2.0) if k % 2 else rng.uniform(S_RB - 0.5, S_OUT + 0.5)
    BUBS.append((ball(1.0, BUBM, seg=20, shadow=False), t0, Vector((rng.uniform(-16, 16), rng.uniform(-3, 7), rng.uniform(1, 9))), rng.uniform(0.25, 0.7), rng.uniform(0, 6)))

# ---------------------------------------------------------------- air, world, camera
w = bpy.data.worlds.new("w")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*lin("#0c1024"), 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.3
S.world = w
HAZE = None
if os.environ.get("HAZE", "1") == "1":
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1, matrix=Matrix.Diagonal((2 * WALLX - 0.4, 64, CEIL - 0.4, 1)))
    hm = bpy.data.materials.new("haze")
    hm.use_nodes = True
    nt = hm.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    vs_ = nt.nodes.new("ShaderNodeVolumeScatter")
    vs_.inputs["Density"].default_value = 0.009
    vs_.inputs["Anisotropy"].default_value = 0.35
    nt.links.new(vs_.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
    HAZE = add(mesh(bm), hm, (0, -19.5, CEIL / 2), smooth_=False, shadow=False)
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


def move(T, t0, t1, p0, p1, g0, g1, lens, focus=None, fstop=1.2, ease=False):
    u = clamp((T - t0) / (t1 - t0))
    if ease:
        u = u * u * (3 - 2 * u)
    shot(vlerp(p0, p1, u), vlerp(g0, g1, u), lens, focus=focus, fstop=fstop)


# ---------------------------------------------------------------- how fast each drum turns, summed into an angle
def drum_speed(i, t):
    if t < S_V:
        base = 3.0 * smooth(1.0 + 0.9 * abs(i - 2), 6.5, t)
    elif t < S_CA:
        base = 3.2
    elif t < S_CB:
        base = 1.3
    elif t < S_BR:
        base = 8.5
    elif t < S_RA:
        base = 2.6 if i != 2 else lerp(2.6, 0.75, smooth(S_BR, S_BR + 1.5, t)) * (1 - smooth(S_RA - 1.0, S_RA - 0.1, t))
    elif t < S_RB:
        base = 1.3 if i != 2 else 0.0
    elif t < S_OUT:
        base = 8.5 if i != 2 else 0.0
    else:
        base = (8.5 if i != 2 else 0.0) * (1 - smooth(S_OUT, S_OUT + 2.6, t)) ** 2
    return base * (1 if i % 2 == 0 else -1)


ANG = [[0.0] for _ in MXS]
for i in range(len(MXS)):
    acc = rng.uniform(0, 6)
    ANG[i][0] = acc
    for f in range(1, NF * 4 + 8):
        acc += drum_speed(i, f / (FPS * 4)) / (FPS * 4)
        ANG[i].append(acc)


def drum_angle(i, T):
    return ANG[i][int(clamp(T * FPS * 4, 0, len(ANG[i]) - 1))]


PARTY = ("#ff3d8b", "#33d1ff", "#ffc233", "#8a5cff", "#3dff9e")
SING = [(w0, w1) for w0, w1, _ in D["words"]]
YAW0 = -PI / 2 + 0.5                               # the singer faces the camera, toe turned a little to the right
HOME = Vector((0.15, 8.2, TOPZ))                   # where the singer stands, behind the mic
EDGE = Vector((1.7, 6.55, TOPZ))                  # the edge of the counter, over the middle porthole
DUO_A, DUO_B = Vector((1.4, 7.9, TOPZ)), Vector((-2.1, 7.9, TOPZ))
YAW_A, YAW_B = -PI / 2 - 0.1, -PI / 2 + 0.1        # side by side, toes to the camera


def blink(t, period, ph):
    return 1.0 if ((t + ph) % period) < 0.11 else 0.0


def bez(p0, p1, p2, u):
    return (1 - u) ** 2 * Vector(p0) + 2 * u * (1 - u) * Vector(p1) + u * u * Vector(p2)


# ================================================================ pose everything for time T
def update(T):
    bt, bk_ = since(T, B0, BEAT)                    # seconds since the last beat, and which beat
    bar_t, bar_k = since(T, B0, 4 * BEAT)
    kp = kick(T)
    running = smooth(1.5, 6.0, T) * (1 - smooth(S_OUT + 0.3, S_OUT + 3.0, T))
    full = (S_CB <= T < S_BR) or (S_RB <= T < S_OUT)
    soft = (S_CA <= T < S_CB) or (S_RA <= T < S_RB)
    bridge = S_BR <= T < S_RA
    out = T >= S_OUT
    out_k = math.exp(-(T - S_OUT) * 1.3) if out else 1.0

    # ---- room light
    if T < 6.4:
        tubes = 1.0
    elif T < S_V:
        tubes = flick(T)
    elif T < 74.2:
        tubes = 0.0
    elif T < 75.0:
        tubes = flick(T, 3)
    else:
        tubes = 1.0
    glow(TUBEM, 0.15 + 12 * tubes)
    for i, t_ in enumerate(TUBES):
        t_.data.energy = 20000 * tubes
    FILL.data.energy = 3000 + 3000 * tubes + (3000 if full else 0)
    neon = 0.0 if T < 7.0 else (flick(T, 5) if T < S_V else 1.0)
    neon *= (0.55 if bridge else 1.0) * (0.8 + 0.2 * kp)
    glow(NEON1, 0.15 + 10 * neon)
    glow(NEON2, 0.15 + 9 * neon * (1.0 if (bk_ % 2 == 0 or not full) else 0.35))
    NL1.data.energy = 3500 * neon
    NL2.data.energy = 1300 * neon

    # ---- coloured spots
    blue = smooth(27.0, 27.5, T) * (1 - smooth(S_CA - 0.05, S_CA + 0.05, T))
    for i, sp in enumerate(SPOTS):
        if T < S_V:
            lv, col = 0.0, lin("#ffffff")
        elif T < S_CA:
            lv = 0.75 * smooth(S_V, S_V + 0.3, T) * (0.75 + 0.25 * math.exp(-bt * 5))
            col = mixc(("#ff3d8b", "#ffc233", "#33d1ff")[(i + bar_k // 2) % 3], "#2a5cff" if i % 2 else "#3fb4ff", blue)
            lv *= 1 + 0.5 * blue
            tgt = (SPOTX[i] * 0.75 + 2.0 * math.sin(0.6 * T + i), 8.0, 9.5)
        elif soft:
            lv, col = 0.16, lin("#8a5cff" if T < S_CB else "#ffb866")
            tgt = (SPOTX[i] * 0.8, 8.0, 9.5)
        elif full or out:
            lv = (0.75 + 0.6 * kp) * out_k
            col = lin(PARTY[(i + bk_) % 5]) if not out else lin(PARTY[i % 5])
            sw = T * 1.9 + i * 1.1
            tgt = (SPOTX[i] * 0.5 + 9 * math.sin(sw), 5.0 + 5 * math.cos(sw * 0.7), 6.5 + 3 * math.sin(sw * 1.3))
        else:                                       # bridge
            lv, col = 0.3, lin("#6a4cff" if i % 2 else "#2f6bff")
            tgt = (SPOTX[i] * 0.3, 5.5, 4.0)
        if T < S_V:
            tgt = (SPOTX[i] * 0.6, 8, 9)
        sp.data.energy = 130000 * lv
        sp.data.color = col
        point_at(sp, tgt)
    # the follow spot stays on the singer
    if T < S_V:
        fl = 0.0
    elif soft:
        fl = 1.25
    elif full:
        fl = 1.05
    elif bridge:
        fl = 0.55
    else:
        fl = 0.8
    FOLLOW.data.energy = 60000 * fl * smooth(S_V - 0.05, S_V + 0.25, T) * (out_k if out else 1)
    FOLLOW.data.color = lin("#ffd9a8" if T >= S_RA and T < S_RB else "#fff2e0")

    # ---- machines: drums, dials, level lights
    feeds = ("other_s", "bass_s", "vocals_s", "drums_s", "bass_s")
    shake = smooth(24.3, 24.8, T) * (1 - smooth(27.6, 28.2, T))
    for i, (dr, blobs) in enumerate(DRUMS):
        dr.rotation_euler = (0, drum_angle(i, T), 0)
        v = E(feeds[i], T) * running
        if i == 3:
            v = max(v, 0.9 * kp * running)
        if i in (0, 4):
            v = clamp(v * 1.6 + 0.25 * kp * running, 0, 1.2)
        ang = lerp(-2.1, 2.1, clamp(v / 1.15)) + 0.04 * math.sin(T * 31 + i) * running + shake * 0.3 * math.sin(T * 47 + 2 * i)
        if i == 2:
            forty = smooth(28.3, 28.9, T) * (1 - smooth(31.0, 32.0, T))
            ang = lerp(ang, -0.7 + 0.05 * math.sin(T * 38), forty)
        DIALS[i].rotation_euler = (0, ang, 0)
        lit = v * 8.4
        for k, seg in enumerate(LEDS[i]):
            seg.data.materials[0] = LED_ON[k] if lit > k + 0.5 else LED_OFF[k]
        glow(DISPLAYS[i], (0.3 + 2.5 * running) * (0.7 + 0.5 * kp))
        e_ = (250 + 900 * kp + 500 * v) * running
        if bridge and i == 2:
            e_ = 1500
        if T >= S_RA and i == 2:
            e_ = 1400 * (out_k if out else 1)
        DLIGHTS[i].data.energy = e_
    big_feed = ("bass_s", "drums_s", "vocals_s", "other_s")
    for i, nd in enumerate(BIG):
        v = E(big_feed[i], T) * running
        if i == 1:
            v = max(v * 0.6, kp * running)
        nd.rotation_euler = (0, lerp(-2.1, 2.1, clamp(v / 1.1)) + 0.03 * math.sin(T * 29 + i * 2) * running + shake * 0.25 * math.sin(T * 43 + i), 0)

    # ---- the door of the middle machine springs open for the reunion
    od = T - S_RA
    opening = 0.0 if od < 0 else (1 - math.exp(-od * 5) * math.cos(od * 9))
    DOORS[2].rotation_euler = (0, 0, -1.9 * opening)

    # ---- mirror ball and its dots
    drop = smooth(S_CA - 2.2, S_CA + 0.4, T)
    BALL.location = (BALLP.x, BALLP.y, lerp(CEIL + 6, BALLP.z, drop))
    spin = 0.35 * T if not full else 0.35 * T + 0.5 * (T - (S_CB if T < S_BR else S_RB))
    BALL.rotation_euler = (0, 0, spin)
    dots_on = smooth(S_CA - 0.3, S_CA + 0.8, T) * (0.45 if bridge else 1.0) * (out_k if out else 1)
    glow(ballm, 0.3 + 0.6 * dots_on)
    for m_ in BALLT:
        glow(m_, 0.3 + 5.0 * dots_on)
    for m_ in DOTM:
        glow(m_, 7.0 * dots_on * (0.8 + 0.4 * kp))
    for o, an, r, z in DOTS:
        if dots_on < 0.01:
            o.scale = (0, 0, 0)
            continue
        d = Vector((r * math.cos(an + spin), r * math.sin(an + spin), z))
        h = dot_hit(d)
        if not h:
            o.scale = (0, 0, 0)
            continue
        t, p, kind = h
        sc = 0.5 + t * 0.035
        o.scale = (sc, sc, 1)
        if kind in ("floor", "top"):
            o.location, o.rotation_euler = (p.x, p.y, p.z + 0.03), (0, 0, 0)
        elif kind in ("front", "back"):
            o.location, o.rotation_euler = (p.x, p.y - 0.03, p.z), (PI / 2, 0, 0)
        else:
            o.location, o.rotation_euler = (p.x - 0.03 * (1 if d.x > 0 else -1), p.y, p.z), (0, PI / 2, 0)

    # ---- the singer
    mo, wi = E("mouth", T), E("wide", T)
    beat_bob = math.exp(-bt * 6)
    swing = math.sin(PI * (T - B0) / (2 * BEAT))          # side to side, one way per beat pair
    loc, yaw = HOME.copy(), YAW0
    hop, sq, lean, sway, twist, shut, look = 0.0, 1.0, 0.0, 0.0, 0.0, blink(T, 3.3, 0.7), (0.0, 0.0)
    if T < S_V:                                           # lying on the counter, just a sock
        up = smooth(S_V - 0.25, S_V + 0.2, T)
        over = math.exp(-(T - S_V) * 6) * math.sin((T - S_V) * 14) if T > S_V else 0
        lean = lerp(-1.5, 0.0, up)
        shut = 1.0 if T < S_V - 0.12 else 0.0
        if 4.0 < T < S_V - 0.3:                           # the beat makes it twitch
            lean += 0.05 * kp
        mo = 0
    elif T < S_CA:
        hop = 0.1 * beat_bob
        sq = 1 - 0.05 * beat_bob
        lean = 0.1 + 0.12 * E("vocals_s", T)
        sway = 0.13 * swing
        twist = 0.1 * math.sin(PI * (T - B0) / (4 * BEAT))
        over = math.exp(-(T - S_V) * 6) * math.sin((T - S_V) * 14)
        lean += 0.35 * over
        if T > 30.4:                                      # "still missing you"
            lean = lerp(lean, -0.12, smooth(30.4, 31.2, T))
            look = (0, 0.7 * smooth(30.4, 31.2, T))
    elif T < S_CB:                                        # the soft half of the chorus: slow sway, one slow turn
        sway = 0.22 * math.sin(PI * (T - B0) / (4 * BEAT))
        lean = 0.1 + 0.1 * E("vocals_s", T)
        yaw += 2 * PI * smooth(36.5, 38.5, T)             # "round and round"
        shut = max(shut, smooth(36.4, 36.7, T) * (1 - smooth(38.3, 38.6, T)) * 0.8)
        crouch = smooth(39.4, S_CB - 0.05, T)             # winds up for the drop
        sq = 1 - 0.22 * crouch
    elif T < S_BR:                                        # the full chorus: jump on every beat
        u = clamp(bt / (BEAT * 0.72))
        hop = 0.75 * 4 * u * (1 - u) if u < 1 else 0
        sq = 1 - 0.16 * math.exp(-max(0, bt - BEAT * 0.72) * 14) if bt > BEAT * 0.72 else 1 + 0.1 * math.sin(PI * u)
        sway = 0.26 * swing
        twist = 0.35 * swing
        lean = 0.12
    elif T < S_RA:                                        # the bridge: goes to the edge and looks down at the glass
        go = smooth(S_BR, S_BR + 0.9, T)
        loc = HOME.lerp(EDGE, go)
        hop = 0.9 * math.sin(PI * go) if go < 1 else 0.04 * beat_bob
        yaw = lerp(YAW0, -PI / 2 - 0.1, go)
        peer = smooth(S_BR + 0.8, S_BR + 1.7, T)
        lean = 0.1 + 0.85 * peer + 0.06 * math.sin(T * 2.2)
        look = (0, -0.9 * peer)
        back = smooth(S_RA - 0.5, S_RA - 0.05, T)         # startled upright as the door goes
        lean = lerp(lean, -0.25, back)
    else:                                                 # together again
        back_u = smooth(S_RA + 0.15, S_RA + 0.95, T)      # hops back from the edge to make room
        loc = EDGE.lerp(DUO_A, back_u)
        yaw = lerp(-PI / 2 - 0.1, YAW_A, back_u)
        hop = 1.3 * math.sin(PI * back_u) if back_u < 1 else 0.0
        land = T - (S_RA + 1.45)                          # when the other one lands beside it
        if T < S_RB:
            back = 1 - smooth(S_RA + 0.2, S_RA + 1.0, T)
            lean = -0.25 * back + 0.1
            look = (-0.9 * smooth(S_RA + 0.3, S_RA + 1.2, T), 0.5 * (1 - smooth(S_RA + 0.8, S_RA + 1.5, T)))
            sway = 0.2 * math.sin(PI * (T - B0) / (4 * BEAT)) + 0.14 * smooth(0, 0.6, land)
            if land > 0:
                hop += 0.5 * math.exp(-land * 5) * abs(math.sin(land * 9))
            yaw += 2 * PI * smooth(60.5, 62.5, T)
        elif not out:
            u = clamp(bt / (BEAT * 0.72))
            hop = 0.75 * 4 * u * (1 - u) if u < 1 else 0
            sq = 1 - 0.16 * math.exp(-max(0, bt - BEAT * 0.72) * 14) if bt > BEAT * 0.72 else 1 + 0.1 * math.sin(PI * u)
            sway = 0.24 * swing + 0.08
            twist = 0.3 * swing
            lean = 0.12
            look = (-0.5, 0)
        else:
            ot = T - S_OUT
            sq = 1 - 0.2 * math.exp(-ot * 5) * math.cos(ot * 16)
            sway = 0.2 * smooth(0, 0.5, ot)               # leans on the other one
            look = (-0.8, 0)
            flop = smooth(74.3, 75.1, T)
            lean = lerp(0.05, -1.5, flop)
            sway *= 1 - flop
            shut = max(shut, smooth(73.9, 74.3, T))
            mo = 0
    pose_sock(SOCK, loc, yaw, hop, sq, lean, sway, twist, shut, mo, wi, look=look)

    # ---- the missing one: in the middle drum until the door opens
    DC = Vector((0, FY + 1.2, PZ))
    if T < S_BR - 0.4:
        pose_sock(PAIR, DC, 0, scale=0.0)
    elif T < S_RA + 0.12:
        an = drum_angle(2, T) * 0.6
        p = DC + Vector((0.45 * math.cos(an), -0.75, 0.45 * math.sin(an) - 0.5))
        wake = smooth(S_BR + 3.2, S_BR + 4.4, T)
        pose_sock(PAIR, p, -PI / 2, scale=0.52, roll=an, shut=1 - wake, lean=0.15, look=(0, 0.6 * wake),
                  mouth=0.35 * smooth(S_RA - 1.2, S_RA - 0.6, T))
    else:
        j = clamp((T - (S_RA + 0.12)) / 1.33)             # the leap out of the drum and up onto the counter
        dest = DUO_B
        PY_ = YAW_B
        if j < 1:
            p = bez(DC + Vector((0, -1.2, 0)), (-1.2, -1.5, 15.0), dest, j)
            pose_sock(PAIR, p, lerp(-PI / 2, PY_, j), scale=lerp(0.52, 1.0, smooth(0, 0.6, j)), tumble=-2 * PI * (1 - j) * 1.0,
                      lean=0.3 * math.sin(PI * j), mouth=0.6 * math.sin(PI * j), wide=1.1)
        else:
            lt = T - (S_RA + 1.45)
            hop2, sq2, sway2, twist2, lean2, look2, shut2, mo2 = 0.0, 1 - 0.3 * math.exp(-lt * 6) * math.cos(lt * 15), 0.0, 0.0, 0.1, (0.8, 0), blink(T, 2.9, 1.3), 0.0
            yaw2 = PY_
            if T < S_RB:
                sway2 = 0.2 * math.sin(PI * (T - B0) / (4 * BEAT)) - 0.14 * smooth(0, 0.6, lt)
                yaw2 -= 2 * PI * smooth(60.5, 62.5, T)
                mo2 = mo * smooth(58.2, 58.6, T)
            elif not out:
                u = clamp(bt / (BEAT * 0.72))
                hop2 = 0.75 * 4 * u * (1 - u) if u < 1 else 0
                sq2 = 1 - 0.16 * math.exp(-max(0, bt - BEAT * 0.72) * 14) if bt > BEAT * 0.72 else 1 + 0.1 * math.sin(PI * u)
                sway2 = 0.24 * swing - 0.08
                twist2 = 0.3 * swing
                mo2 = mo
                look2 = (0.5, 0)
            else:
                ot = T - S_OUT
                sq2 = 1 - 0.2 * math.exp(-ot * 5) * math.cos(ot * 16)
                sway2 = -0.2 * smooth(0, 0.5, ot)
                flop = smooth(74.3, 75.1, T)
                lean2 = lerp(0.05, -1.5, flop)
                sway2 *= 1 - flop
                shut2 = max(shut2, smooth(73.9, 74.3, T))
            pose_sock(PAIR, dest, yaw2, hop2, sq2, lean2, sway2, twist2, shut2, mo2, wi, look=look2)

    # ---- pegs: they sing the chorus by opening their legs
    in_ch = (S_CA <= T < S_BR) or (S_RA + 0.2 <= T < S_OUT)
    for i, pg in enumerate(PEGS):
        op = (mo if in_ch else 0.0) * (1.0 if full else 0.6)
        swy = (0.22 if full else 0.1) * math.sin(PI * (T - B0) / (2 * BEAT) + i * 0.5) * (running if T > S_V else 0.3 * running)
        pg["root"].rotation_euler = (0.1 * kp if full else 0, swy, 0)
        pg["root"].location.z = LINEZ - 0.05 + (0.18 * math.exp(-bt * 7) if (T > S_V and not out) else 0)
        for sx, (p, e) in zip((-1, 1), pg["prongs"]):
            p.rotation_euler = (0, sx * (0.03 + 0.3 * op), 0)
            e.scale = (1, 1, 0.15 if blink(T, 2.6 + 0.4 * i, i) else 1)

    # ---- the bottle on bass
    bv = E("bass_s", T) * running
    BOTB.location = (0, 0, 0.14 * beat_bob * running + 0.25 * kp * (1 if full else 0.4))
    BOTB.rotation_euler = (0.06 * math.sin(PI * (T - B0) / BEAT) * running, 0.12 * swing * running, 0.1 * math.sin(PI * (T - B0) / (4 * BEAT)) * running)
    k_ = 1 - 0.07 * kp * running
    BOTB.scale = (1 / math.sqrt(k_), 1 / math.sqrt(k_), k_)
    BMOUTH.scale = (1 + 0.6 * bv, 0.3, 0.5 + 0.9 * bv)
    BASS.rotation_euler = (0, 1.0 + 0.08 * swing * running, 0)
    pl = math.exp(-since(T, B0, BEAT / 2)[0] * 9) * clamp(bv * 2)
    HAND1.location = (-0.75 + 0.2 * pl, -1.95, 0.8 - 0.25 * pl)
    HAND2.location = (1.25 + 0.3 * math.sin(T * 1.7) * running, -1.8, 1.75 + 0.2 * math.sin(T * 1.7) * running)
    for i, (st, x) in enumerate(BSTR):
        st.data.splines[0].points[1].co = (x + 0.05 * bv * math.sin(T * 140 + i * 2), -0.2, 1.9, 1)

    # ---- bubbles
    for o, t0, p0, r, ph in BUBS:
        age = T - t0
        if 0 < age < 7 and T < 75.2:
            o.location = (p0.x + 0.8 * math.sin(age * 1.3 + ph), p0.y + 0.5 * math.cos(age * 0.9 + ph), p0.z + 2.1 * age)
            sc = r * smooth(0, 0.5, age) * (1 - smooth(6.3, 7, age)) * (1 + 0.06 * math.sin(age * 9 + ph))
            o.scale = (sc, sc, sc)
        else:
            o.scale = (0, 0, 0)

    # ---- camera
    head = Vector((HOME.x + 0.4, HOME.y - 0.8, TOPZ + 3.05))
    duo = (-0.35, 7.4, TOPZ + 2.9)
    wide_p, wide_g = (0, -40, 9.5), (0, 8, 10.3)
    if T < B0 + 4:                                        # the room, strip lights on
        move(T, 0, B0 + 4, (0, -43, 9.0), (0, -39, 9.3), wide_g, wide_g, 36, focus=(0, 7, 9), fstop=4.0)
    elif T < S_V:                                         # the middle machine wakes up
        move(T, B0 + 4, S_V, (-2.6, -6.5, 6.2), (-1.2, -5.2, 6.6), (-0.6, FY, 6.0), (-0.3, FY, 6.4), 40, focus=(-1.7, FY, 7.2), fstop=1.4)
    elif T < B0 + 16:                                     # the singer
        move(T, S_V, B0 + 16, (3.2, -7.5, 11.2), (2.2, -5.0, 11.5), head, head, 50, focus=head, fstop=1.0)
    elif T < B0 + 20:                                     # along the row of drums
        move(T, B0 + 16, B0 + 20, (-21, -9.0, 5.2), (-19, -7.0, 6.0), (-2, 6, 6.2), (0, 6, 6.6), 30, focus=(-9, FY, 5), fstop=2.2)
    elif T < S_P:                                         # singer with the bass player behind
        move(T, B0 + 20, S_P, (-6.5, -5.5, 10.6), (-5.6, -4.6, 10.9), (3.4, 8, 11.2), (3.4, 8, 11.2), 50, focus=head, fstop=1.4)
    elif T < B0 + 28:                                     # "every dial is shaking": along the dials
        move(T, S_P, B0 + 28, (-13.5, -1.2, 7.0), (7.5, -1.2, 7.0), (-11.5, FY, 7.2), (9.5, FY, 7.2), 40, focus=None, fstop=1.6)
    elif T < B0 + 30.5:                                       # "forty degrees"
        move(T, B0 + 28, B0 + 30.5, (-0.3, -0.6, 7.0), (-0.6, 0.6, 7.0), (-0.55, FY, 7.05), (-0.6, FY, 7.05), 60, fstop=1.6)
    elif T < S_CA:                                        # "still missing you"
        move(T, B0 + 30.5, S_CA, (1.4, -3.6, 11.6), (1.3, -3.2, 11.6), head, head, 70, focus=head, fstop=1.0)
    elif T < B0 + 36:                                     # the ball comes down
        move(T, S_CA, B0 + 36, (0, -34, 7.0), (0, -30, 8.0), (0, 8, 12.5), (0, 8, 12.0), 32, focus=(0, 7, 10), fstop=3.0)
    elif T < S_CB:                                        # "round and round"
        move(T, B0 + 36, S_CB, (5.0, -7.5, 11.4), (-1.5, -8.5, 11.0), head, head, 45, focus=head, fstop=1.2)
    elif T < B0 + 44:                                     # everything at once
        move(T, S_CB, B0 + 44, (-9, -30, 4.5), (7, -27, 5.5), (0, 8, 10.5), (0, 8, 10.5), 30, focus=(0, 7, 10), fstop=3.0)
    elif T < B0 + 46:                                     # the pegs
        move(T, B0 + 44, B0 + 46, (-11.5, -1.5, 11.0), (-10.5, -1.0, 11.2), (-9.4, LINEY, 12.0), (-9.4, LINEY, 12.0), 50, fstop=1.4)
    elif T < S_BR:                                        # the bottle and the big gauges
        move(T, B0 + 46, S_BR, (6.5, -4.5, 10.5), (7.5, -3.5, 10.8), (12.5, 9, 12.6), (12.5, 9, 12.6), 40, focus=(9.6, 8.0, 11), fstop=1.6)
    elif T < B0 + 52.5:                                       # at the edge, looking down
        move(T, S_BR, B0 + 52.5, (-7.0, -12.5, 3.4), (-5.5, -11.0, 3.2), (0.8, FY, 7.8), (0.8, FY, 7.6), 40, focus=(1, FY, 8), fstop=2.0, ease=True)
    elif T < S_RA:                                        # behind the glass
        move(T, B0 + 52.5, S_RA, (0.6, -2.6, 3.5), (0.3, -1.6, 3.4), (0, FY, PZ), (0, FY, PZ), 50, focus=(0, FY + 0.6, PZ), fstop=1.4)
    elif T < B0 + 60:                                     # out it comes
        move(T, S_RA, B0 + 60, (4.5, -17, 6.0), (3.5, -14, 8.8), (0, FY, 7.2), (-0.3, 7.5, 11.0), 36, focus=(0, 7, 9), fstop=2.2, ease=True)
    elif T < S_RB:                                        # the two of them
        move(T, B0 + 60, S_RB, (-2.8, -8.5, 11.6), (1.6, -8.0, 11.6), duo, duo, 45, focus=duo, fstop=1.4)
    elif T < B0 + 68:                                     # everything at once, again
        move(T, S_RB, B0 + 68, (8, -29, 4.5), (-8, -26, 6.0), (0, 8, 10.5), (0, 8, 10.5), 30, focus=(0, 7, 10), fstop=3.0)
    elif T < B0 + 70:                                     # gauges and pegs
        move(T, B0 + 68, B0 + 70, (-8.0, -1.5, 12.4), (-9.0, -1.0, 12.6), (-12.0, WALLY, 13.4), (-12.0, WALLY, 13.4), 36, focus=(-9.4, LINEY, 12), fstop=2.0)
    elif T < S_OUT:                                       # "play it once again"
        move(T, B0 + 70, S_OUT, (0.6, -7.5, 10.2), (-0.1, -8.5, 10.4), duo, duo, 42, focus=duo, fstop=1.4)
    else:                                                 # the room again
        move(T, S_OUT, LEN, (0, -37, 9.2), (0, -43, 9.0), wide_g, wide_g, 36, focus=(0, 7, 9), fstop=4.0)


os.makedirs(OUT, exist_ok=True)
for f in FRAMES:
    path = os.path.join(OUT, f"f_{f:04d}.png")
    if os.path.exists(path):
        continue
    S.frame_set(f)
    update(f / FPS)
    S.render.filepath = path
    bpy.ops.render.render(write_still=True)
