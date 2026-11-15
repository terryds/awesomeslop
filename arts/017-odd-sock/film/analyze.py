# Measures the song so the film can follow it: writes film/data.json.
#   python3 analyze.py <dir with vocals/bass/drums/guitar/piano/other .mp3> <align.json> <out.json>
# Per film frame (24 a second): the loudness of each stem (0..1) and the mouth shape from the aligned lyrics.
# Also the beat grid (period and first beat) and the kick drum hits, measured from the drum stem.
import sys, json, subprocess, numpy as np

stems, align, out = sys.argv[1:4]
FPS, SR = 24, 22050


def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{stems}/{name}.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def env(x, win=0.05, hop=1 / FPS):
    """RMS in a short window centred on each film frame, scaled so the 98th percentile is 1."""
    n = int(len(x) / SR * FPS) + 1
    w = int(win * SR)
    e = np.array([np.sqrt(np.mean(x[max(0, int(i * hop * SR) - w // 2): int(i * hop * SR) + w // 2 + 1] ** 2) + 1e-12) for i in range(n)])
    return np.clip(e / np.percentile(e, 98), 0, 1.3)


data = {"fps": FPS}
X = {k: load(k) for k in ("vocals", "bass", "drums", "guitar", "piano", "other")}
data["frames"] = int(len(X["drums"]) / SR * FPS)
for k, x in X.items():
    data[k] = [round(float(v), 3) for v in env(x)]

# ---- kick: the drum stem below ~120 Hz
d = X["drums"]
F = np.fft.rfft(d)
F[int(120 * len(d) / SR):] = 0
low = np.fft.irfft(F, len(d))
h = 64
e = np.sqrt((low[: len(low) // h * h].reshape(-1, h) ** 2).mean(1))
fr = SR / h
on = np.maximum(0, np.diff(e, prepend=0))
# ---- beat grid: the period and phase whose comb collects the most onset energy
best = (0, 0, 0)
t = np.arange(len(on)) / fr
for per in np.arange(0.490, 0.510, 0.0002):
    for ph in np.arange(0, per, 0.004):
        idx = np.round((np.arange(ph, t[-1], per)) * fr).astype(int)
        s = on[idx[idx < len(on)]].sum()
        if s > best[0]:
            best = (s, per, ph)
_, per, ph = best
data["beat"], data["beat0"] = round(float(per), 5), round(float(ph), 4)
thr = np.percentile(on, 99) * 0.5
kicks, last = [], -1
for i in range(1, len(on) - 1):
    if on[i] > thr and on[i] >= on[i - 1] and on[i] >= on[i + 1] and i / fr - last > 0.2:
        last = i / fr
        kicks.append(round(last, 3))
data["kicks"] = kicks

# ---- mouth: open and wide per frame, from the letters being sung
al = json.load(open(align))
SHAPE = {"a": (1.0, 1.0), "e": (0.6, 1.2), "i": (0.45, 1.25), "o": (0.9, 0.62), "u": (0.55, 0.5), "y": (0.45, 1.2),
         "m": (0.03, 0.9), "b": (0.03, 0.9), "p": (0.03, 0.9), "w": (0.3, 0.45), "f": (0.12, 1.0), "v": (0.12, 1.0)}
chars = [(c["start"], c["end"], c["text"].lower()) for c in al["characters"]]
words = [(w["start"], w["end"], w["text"]) for w in al["words"] if w["text"].strip()]
N = len(data["vocals"])
op, wd = np.zeros(N), np.ones(N)
for i in range(N):
    tt = i / FPS
    inword = any(a - 0.03 <= tt <= b + 0.04 for a, b, _ in words)
    if not inword:
        continue
    for a, b, c in chars:
        if a <= tt < b:
            o, w = SHAPE.get(c, (0.28, 1.0)) if c.strip() else (0.1, 1.0)
            op[i], wd[i] = o, w
            break
k = np.array([0.25, 0.5, 0.25])
op, wd = np.convolve(op, k, "same"), np.convolve(wd, k, "same")
v = np.array(data["vocals"])
op = op * np.clip(0.45 + 0.75 * v, 0, 1.15)
data["mouth"] = [round(float(x), 3) for x in op]
data["wide"] = [round(float(x), 3) for x in wd]
data["words"] = [[round(a, 2), round(b, 2), w] for a, b, w in words]
json.dump(data, open(out, "w"), separators=(",", ":"))
print("frames", data["frames"], "beat", data["beat"], "first", data["beat0"], "bpm", 60 / per, "kicks", len(kicks), kicks[:12])
