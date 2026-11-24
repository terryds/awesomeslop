// Lantern Cove: a seaside fishing cove at golden hour, as a pop-up paper diorama (papercraft skill, own world).
/* PAPER SPEC
BRIEF    a small fishing cove at golden hour: warm sand, a teal sea, a striped lighthouse on the point, fishing huts on a
         boardwalk, palms, dune grass, boats, crabs and gulls; a kid in a yellow raincoat carrying a lantern
PALETTE  sand #e3cfa2 / #cdb58a ground; lead coral-terracotta #d8643c; teal #2f7f86 accent; cream #f6ead0; ink #2e2218;
         sea #4a95a3 / deep #2f6f80; shadow tint warm umber (golden-hour set)
LIGHT    golden mood (low warm key, cool fill)   LENS harness default (fov 26, pitch 47)
LIFE     gulls crossing, crabs that freeze and watch, gulls that peck and scatter, boats bobbing, chimney smoke, cloud shadows */
import * as P2 from 'papercraft/lib/paperkit-2d.js';
import { makeCard, layeredCard, clusterLayout, platform } from 'papercraft/lib/paperkit-3d.js';
import * as EX from 'papercraft/examples/countryside.js';
import { boxHouse } from 'papercraft/examples/built-ground.js';
import { createLife } from 'papercraft/lib/paper-life.js';
import { createHarness } from './harness.js';

const C = {
  ground: '#dcc89c', sandWet: '#c9b48c', sandLight: '#eadbb4', sea: '#4a95a3', seaDeep: '#2f6f80', foam: '#f5ecd6', board: '#b07a4a',
  coral: '#d8643c', teal: '#2f7f86', cream: '#f6ead0', ink: '#2e2218', grass: '#8f9a55', grassB: '#a8a05a', palm: '#5f8a4a', palmB: '#7a9c4c',
  trunk: '#8a5a34', stone: '#a39a8a', wall: '#efe0c2', wallB: '#b9d3d2', wallC: '#f0c9a6', roofA: '#2f6f86', roofB: '#c8553a', roofC: '#d99a3a',
  window: '#ffc45a', door: '#2f5f6e', dune: '#c9ae7c', pink: '#e58a8a',
};
// leading lines: the shoreline (sea to its left, x < shoreX) and the boardwalk path, both bending through the frame
const shoreX = (z) => -17 - z * 0.3 + Math.sin(z * 0.16) * 3.2 + Math.sin(z * 0.27 + 1.3) * 2.0;
const pathX = (z) => 9 + z * 0.25 + Math.sin(z * 0.14 + 1) * 2.6 + Math.sin(z * 0.22 + 0.4) * 2.4;
const HERO_AT = [pathX(3) + 0.2, 3];
const QS = new URLSearchParams(location.search), PAN = QS.has('pan') || QS.has('panAt');
const FOC = [0, 1.8, -6];   // the lens focus: follows the panning camera
const H = createHarness({ focus: PAN ? FOC : null, ground: C.ground, mood: 'golden', view: { pitch: 47, dist: 66, target: [0, 1.5, -6] }, bounds: { x0: -64, x1: 64, z0: -62, z1: 38 }, play: true,
  walkArea: { x0: -12, x1: 22, z0: -24, z1: 7 }, camBox: PAN ? { x0: -17, x1: 13, z0: -21, z1: 1 } : { x0: -1, x1: 5, z0: -8, z1: -4 }, subject: HERO_AT });
const { walk, flags } = H;
let RES = 1;
const popup = (pts, paint, o = {}) => H.popup(pts, paint, { res: RES, ...o });
const seaDist = (x, z) => x - shoreX(z);   // >0 on land
const JET = { z: -9, len: 9 };              // the jetty runs out into the sea at z = JET.z

H.printGround(({ g, ppu, X, Z, rnd, washes, torn, band, ribbon, drifts }) => {
  washes([C.ground, C.ground, C.sandLight, C.sandWet, C.ground]);
  // the sea: a big torn sheet left of the shore, a wet-sand rim, deeper bands, foam lines along the beach
  const zs = []; for (let z = H.bounds.z0 - 4; z <= H.bounds.z1 + 4; z += 0.8) zs.push(z);
  const region = (off) => [...zs.map((z) => [shoreX(z) + off, z]), [H.bounds.x0 - 10, H.bounds.z1 + 4], [H.bounds.x0 - 10, H.bounds.z0 - 4]];
  torn(region(1.6), C.sandWet);
  torn(region(0), C.sea, 'rgba(250,240,220,0.4)');
  torn(region(-5), P2.rgba(C.seaDeep, 0.45), 'rgba(0,0,0,0)');
  torn(region(-13), P2.rgba(C.seaDeep, 0.6), 'rgba(0,0,0,0)');
  for (const off of [-0.9, -2.2, -3.8]) ribbon((z) => shoreX(z) + off + Math.sin(z * 0.7) * 0.25, 0.22, P2.rgba(C.foam, 0.8 - off * -0.12), undefined, undefined, 0.15);
  for (let k = 0; k < 900; k++) {   // ripples
    const z = H.bounds.z0 + rnd() * (H.bounds.z1 - H.bounds.z0), x = shoreX(z) - 1.5 - rnd() * 40, l = (0.5 + rnd() * 1.2) * ppu, pale = k % 3 !== 0;
    g.strokeStyle = pale ? P2.rgba(C.foam, 0.75) : P2.rgba(C.seaDeep, 0.6); g.lineWidth = 0.1 * ppu;
    g.beginPath(); g.moveTo(X(x) - l / 2, Z(z)); g.quadraticCurveTo(X(x), Z(z) - 0.12 * ppu, X(x) + l / 2, Z(z)); g.stroke();
  }
  // the boardwalk: a torn strip of weathered planks
  torn(band(pathX, (z) => 1.35 + Math.sin(z * 0.5) * 0.1), C.board);
  for (let z = H.bounds.z0; z < H.bounds.z1; z += 0.55) {   // plank seams across the path
    const x = pathX(z), dx = pathX(z + 0.3) - pathX(z - 0.3), a = Math.atan2(0.6, dx);
    g.strokeStyle = P2.rgba('#6e4526', 0.55); g.lineWidth = 0.07 * ppu; g.save(); g.translate(X(x), Z(z)); g.rotate(-a + Math.PI / 2);
    g.beginPath(); g.moveTo(-1.25 * ppu, 0); g.lineTo(1.25 * ppu, 0); g.stroke(); g.restore();
  }
  ribbon(pathX, 0.5, P2.rgba('#e8c79a', 0.35), undefined, undefined, 0.2);
  // sand: shells, pebbles, ripples and grass ticks gathered in drifts
  for (let k = 0; k < 1600; k++) {
    const x = H.bounds.x0 + rnd() * (H.bounds.x1 - H.bounds.x0), z = H.bounds.z0 + rnd() * (H.bounds.z1 - H.bounds.z0);
    if (seaDist(x, z) < 1.8) continue;
    const r = (0.06 + rnd() * 0.08) * ppu; g.fillStyle = rnd() < 0.5 ? P2.rgba('#b89c70', 0.55) : P2.rgba('#fbf1dc', 0.75);
    g.beginPath(); g.ellipse(X(x), Z(z), r * 1.4, r, rnd() * 3, 0, 7); g.fill();
  }
  drifts((x, y) => {
    if (rnd() < 0.8) { g.strokeStyle = P2.rgba(rnd() < 0.5 ? '#8a8a50' : '#a89c5c', 0.7); g.lineWidth = 1.5; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - 0.5) * 3, y - 5 - rnd() * 5); g.stroke(); }
    else { g.fillStyle = rnd() < 0.5 ? '#f6e2d8' : C.pink; for (let q = 0; q < 5; q++) { const t = q / 5 * 6.283; g.beginPath(); g.arc(x + Math.cos(t) * 2, y + Math.sin(t) * 2, 1.5, 0, 7); g.fill(); } }
  });
});

// ---- pieces: this cove's own silhouettes, each a layered drawn print (drawnPiece: every fill its own cut layer) ----
let rnd = P2.rng(101);
const D = P2.draw2, between = (a, b) => a + rnd() * (b - a);
const mound = (w, h, lobes = 7, depth = 0.18) => P2.shape.mound(rnd, { w, h, lobes, depth });
const tuft = (w, h, n) => P2.shape.mound(rnd, { w, h, lobes: n, depth: 0.42 });
const peak = (w, h, lean = 0.15) => { const p = [[w / 2, 0]]; for (let i = 1; i < 28; i++) { const t = i / 28, x = w / 2 - t * w, k = Math.min(1, Math.abs(x / (w / 2) - lean)); p.push([x, h * (1 - Math.pow(k, 1.7)) * (0.95 + 0.05 * Math.sin(t * 11))]); } p.push([-w / 2, 0]); return p; };
// a palm: a leaning ringed trunk and 7 broad fronds, a cluster of coconuts; slotted as a cross
const palm = (h, lean) => P2.drawnPiece((g, ink) => {
  const top = [lean * h * 0.22, h * 0.72];
  g.fillStyle = ink(C.trunk);
  for (let i = 0; i < 9; i++) { const t = i / 8, x = top[0] * t * t, y = t * top[1]; D.ell(g, x, y, h * (0.07 - t * 0.02), h * 0.06); }
  g.fillStyle = ink(P2.shade(C.trunk, -0.25), 'print');
  for (let i = 1; i < 8; i++) { const t = i / 8; D.rect(g, top[0] * t * t - h * 0.05, t * top[1], h * 0.1, h * 0.012); }
  const fr = [[-2.6, C.palm], [-2.0, C.palmB], [-1.2, C.palm], [-0.4, C.palmB], [0.4, C.palm], [1.2, C.palmB], [2.0, C.palm], [2.6, C.palmB]];
  for (const [a, c] of fr) {
    const L = h * 0.34, ang = Math.PI / 2 + a * 0.55, cx = top[0] + Math.cos(ang) * L * 0.5, cy = top[1] + Math.sin(ang) * L * 0.5 - Math.abs(a) * h * 0.03;
    g.fillStyle = ink(c); D.ell(g, cx, cy, L * 0.55, h * 0.065, ang);
    g.fillStyle = ink(P2.shade(c, -0.3), 'print'); D.ell(g, cx, cy, L * 0.5, h * 0.008, ang);
  }
  g.fillStyle = ink('#6a4426'); for (const dx of [-0.06, 0.03, 0.1]) D.ell(g, top[0] + dx * h, top[1] - h * 0.04, h * 0.045, h * 0.045);
}, { w: h * 1.5, h: h * 1.15, name: 'palm' });
const lighthouse = (h) => P2.drawnPiece((g, ink) => {
  const w0 = h * 0.2, w1 = h * 0.13, body = h * 0.74;
  g.fillStyle = ink(C.cream); D.poly(g, [[-w0 / 2, 0], [w0 / 2, 0], [w1 / 2, body], [-w1 / 2, body]]);
  g.fillStyle = ink(C.coral, 'print');
  for (let k = 0; k < 4; k++) { const y0 = body * (0.1 + k * 0.23), y1 = y0 + body * 0.1, a = (y) => (w0 + (w1 - w0) * y / body) / 2; D.poly(g, [[-a(y0), y0], [a(y0), y0], [a(y1), y1], [-a(y1), y1]]); }
  g.fillStyle = ink('#3d4a5c'); D.rect(g, -w1 * 0.75, body, w1 * 1.5, h * 0.03);
  g.fillStyle = ink('#ffd77a'); D.rect(g, -w1 * 0.45, body + h * 0.03, w1 * 0.9, h * 0.09);
  g.fillStyle = ink('#3d4a5c', 'print'); D.rect(g, -w1 * 0.06, body + h * 0.03, w1 * 0.12, h * 0.09);
  g.fillStyle = ink(C.coral); D.poly(g, [[-w1 * 0.6, body + h * 0.12], [w1 * 0.6, body + h * 0.12], [0, body + h * 0.2]]);
  g.fillStyle = ink(C.door, 'print'); D.rect(g, -w0 * 0.12, 0, w0 * 0.24, h * 0.07, w0 * 0.1);
  g.fillStyle = ink(C.door, 'print'); D.ell(g, 0, body * 0.55, w0 * 0.08, w0 * 0.1);
}, { w: h * 0.24, h: h * 1.02, name: 'lighthouse' });
const crab = (s) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink('#9a3a24'); for (const sd of [-1, 1]) for (let i = 0; i < 3; i++) D.rect(g, sd * (0.18 + i * 0.1) * s - 0.03 * s, 0, 0.06 * s, 0.22 * s);
  g.fillStyle = ink('#d8553a'); D.ell(g, 0, 0.26 * s, 0.4 * s, 0.2 * s);
  for (const sd of [-1, 1]) { D.ell(g, sd * 0.52 * s, 0.46 * s, 0.13 * s, 0.1 * s); D.rect(g, sd * 0.38 * s - 0.03 * s, 0.3 * s, 0.06 * s, 0.16 * s); }
  g.fillStyle = ink('#f3c9a0', 'print'); D.ell(g, 0, 0.2 * s, 0.24 * s, 0.07 * s);
  g.fillStyle = ink('#f6ead0'); for (const sd of [-1, 1]) D.ell(g, sd * 0.1 * s, 0.5 * s, 0.06 * s, 0.07 * s);
  g.fillStyle = ink('#2e2218', 'print'); for (const sd of [-1, 1]) D.ell(g, sd * 0.1 * s, 0.5 * s, 0.03 * s, 0.035 * s);
}, { w: 1.4 * s, h: 0.62 * s, name: 'crab' });
const gull = (s) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink('#e3a03a'); D.rect(g, -0.06 * s, 0, 0.04 * s, 0.25 * s); D.rect(g, 0.04 * s, 0, 0.04 * s, 0.25 * s);
  g.fillStyle = ink('#f4f0e6'); D.ell(g, 0, 0.42 * s, 0.32 * s, 0.2 * s); D.ell(g, 0.26 * s, 0.62 * s, 0.13 * s, 0.12 * s);
  g.fillStyle = ink('#8a95a3'); D.ell(g, -0.06 * s, 0.46 * s, 0.24 * s, 0.11 * s, 0.15); D.poly(g, [[-0.25 * s, 0.4 * s], [-0.48 * s, 0.5 * s], [-0.25 * s, 0.5 * s]]);
  g.fillStyle = ink('#e3a03a'); D.poly(g, [[0.36 * s, 0.64 * s], [0.52 * s, 0.6 * s], [0.36 * s, 0.58 * s]]);
  g.fillStyle = ink('#2e2218', 'print'); D.ell(g, 0.29 * s, 0.65 * s, 0.025 * s, 0.03 * s);
}, { w: 1.1 * s, h: 0.8 * s, name: 'gull' });
const buoy = (s) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.cream); D.ell(g, 0, 0.35 * s, 0.26 * s, 0.35 * s);
  g.fillStyle = ink(C.coral); D.rect(g, -0.3 * s, 0.25 * s, 0.6 * s, 0.18 * s);
  g.fillStyle = ink('#3d4a5c'); D.rect(g, -0.03 * s, 0.68 * s, 0.06 * s, 0.22 * s);
}, { w: 0.7 * s, h: 0.95 * s, name: 'buoy' });
const netRack = (s) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink('#7a4e2c'); D.rect(g, -1.1 * s, 0, 0.12 * s, 1.5 * s); D.rect(g, 1.0 * s, 0, 0.12 * s, 1.5 * s); D.rect(g, -1.15 * s, 1.42 * s, 2.3 * s, 0.1 * s);
  g.fillStyle = ink('#8fb3ad'); D.poly(g, [[-1.0 * s, 1.42 * s], [1.0 * s, 1.42 * s], [0.85 * s, 0.35 * s], [0.0, 0.5 * s], [-0.9 * s, 0.3 * s]]);
  g.fillStyle = ink('#5e8580', 'print'); for (let i = -4; i <= 4; i++) D.rect(g, i * 0.21 * s, 0.45 * s, 0.025 * s, 0.95 * s);
  for (let j = 0; j < 4; j++) D.rect(g, -0.9 * s, (0.6 + j * 0.22) * s, 1.8 * s, 0.025 * s);
  g.fillStyle = ink(C.coral); D.ell(g, -0.5 * s, 0.7 * s, 0.09 * s, 0.09 * s); D.ell(g, 0.45 * s, 0.75 * s, 0.09 * s, 0.09 * s);
}, { w: 2.5 * s, h: 1.6 * s, name: 'net rack' });
const crate = (s) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink('#b8844e'); D.rect(g, -0.45 * s, 0, 0.9 * s, 0.7 * s, 0.03 * s);
  g.fillStyle = ink('#8a5a32', 'print'); for (const y of [0.22, 0.46]) D.rect(g, -0.45 * s, y * s, 0.9 * s, 0.04 * s); D.rect(g, -0.45 * s, 0, 0.08 * s, 0.7 * s); D.rect(g, 0.37 * s, 0, 0.08 * s, 0.7 * s);
  g.fillStyle = ink('#9fc3cf'); for (const dx of [-0.2, 0.05, 0.25]) D.ell(g, dx * s, 0.78 * s, 0.17 * s, 0.07 * s, 0.2);
  g.fillStyle = ink('#5d8696', 'print'); for (const dx of [-0.2, 0.05, 0.25]) D.ell(g, dx * s + 0.12 * s, 0.79 * s, 0.03 * s, 0.03 * s);
}, { w: 1.1 * s, h: 0.95 * s, name: 'fish crate' });
const rowboat = (s) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.teal); D.poly(g, [[-1.1 * s, 0.5 * s], [1.15 * s, 0.6 * s], [0.75 * s, 0], [-0.8 * s, 0]]);
  g.fillStyle = ink(C.cream); D.rect(g, -1.05 * s, 0.38 * s, 2.15 * s, 0.1 * s);
  g.fillStyle = ink(C.coral, 'print'); D.rect(g, -0.4 * s, 0.12 * s, 0.6 * s, 0.12 * s);
}, { w: 2.4 * s, h: 0.7 * s, name: 'rowboat' });
const sailboat = (s, sail) => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink(C.cream); D.poly(g, [[0.02 * s, 0.45 * s], [0.02 * s, 1.8 * s], [0.9 * s, 0.5 * s]]); 
  g.fillStyle = ink(sail); D.poly(g, [[-0.06 * s, 0.55 * s], [-0.06 * s, 1.55 * s], [-0.7 * s, 0.55 * s]]);
  g.fillStyle = ink('#5a3a20'); D.rect(g, -0.04 * s, 0.3 * s, 0.07 * s, 1.55 * s);
  g.fillStyle = ink(C.roofA); D.poly(g, [[-1.0 * s, 0.4 * s], [1.0 * s, 0.4 * s], [0.65 * s, 0], [-0.65 * s, 0]]);
  g.fillStyle = ink(C.cream, 'print'); D.rect(g, -0.95 * s, 0.26 * s, 1.9 * s, 0.06 * s);
}, { w: 2.1 * s, h: 1.9 * s, name: 'sailboat' });
const starfish = (s) => P2.drawnPiece((g, ink) => {
  const st = []; for (let i = 0; i < 10; i++) { const a = Math.PI / 2 + i * Math.PI / 5, r = (i % 2 ? 0.16 : 0.4) * s; st.push([Math.cos(a) * r, 0.42 * s + Math.sin(a) * r]); }
  g.fillStyle = ink('#e07a4a'); D.poly(g, st);
  g.fillStyle = ink('#f6d6a8', 'print'); D.ell(g, 0, 0.42 * s, 0.07 * s, 0.07 * s);
}, { w: 0.9 * s, h: 0.85 * s, name: 'starfish' });
const lantern = () => P2.drawnPiece((g, ink) => {
  g.fillStyle = ink('#3d3a3a'); D.rect(g, -0.07, 0, 0.14, 2.3); D.rect(g, -0.25, 0, 0.5, 0.14);
  g.fillStyle = ink('#ffcf6a'); D.rect(g, -0.22, 2.2, 0.44, 0.5, 0.06);
  g.fillStyle = ink(C.teal); D.poly(g, [[-0.32, 2.68], [0, 2.98], [0.32, 2.68]]);
}, { w: 0.7, h: 3.0, name: 'lamp' });
const K = {
  grass: () => [tuft(between(2.6, 3.6), between(2.2, 3.0), 8), EX.paintBush({ leaf: rnd() < 0.5 ? C.grass : C.grassB }, { bands: 2, flowers: false, motifs: false })],
  seapinks: () => [P2.roughen(mound(between(2.6, 3.4), 1.3, 9, 0.25), rnd), EX.paintBush({ leaf: '#7f8f58' }, { bands: 0, flowers: true, motifs: false })],
  shrub: () => { const w = between(3.6, 4.6); return [P2.roughen(mound(w, w * 0.55, 8, 0.14), rnd), EX.paintBush({ leaf: rnd() < 0.5 ? '#6f8a52' : '#9a8a4a' }, { bands: 2 })]; },
  rock: () => { const w = between(2.8, 4.2); return [P2.roughen(mound(w, w * 0.55, 4, 0.1), rnd), EX.paintRock({ stone: P2.shade(C.stone, (rnd() - 0.5) * 0.15), ink: C.ink })]; },
  crab: () => crab(between(1.3, 1.6)), gull: () => gull(between(1.4, 1.7)),
  buoy: () => buoy(between(1.6, 1.9)), net: () => netRack(1.4), crate: () => crate(1.6), starfish: () => starfish(1.1),
  barrel: () => [EX.props.barrel(2.0), EX.paintWood({ wood: '#8a4e2c' }, { planks: 4, vertical: true })],
  rowboat: () => rowboat(1.7), lamp: () => lantern(),
};
const LIFE = { chimneys: [], creatures: [], floaters: [] };
const BEHAVIOUR = { crab: 'shy', gull: 'peck' };
const pathDist = (x, z) => { let d = 1e9; for (let s = -5; s <= 5; s += 0.25) d = Math.min(d, Math.hypot(x - pathX(z + s), s)); return d; };
const keepOut = [], mark = (x, z, r) => keepOut.push([x, z, r]);
const free = (x, z, m = 0) => seaDist(x, z) > 2.2 + m && pathDist(x, z) > 1.8 + m && keepOut.every(([hx, hz, r]) => Math.hypot(x - hx, z - hz) > r + m);
const BACK_TO_FRONT = ['shrub', 'net', 'grass', 'rowboat', 'rock', 'barrel', 'crate', 'buoy', 'seapinks', 'starfish', 'gull', 'crab'];
function group(x, z, kinds, size = 1, ok = free) {
  const rank = (k) => { const i = BACK_TO_FRONT.indexOf(k); return i < 0 ? 99 : i; };
  kinds = kinds.slice().sort((a, b) => rank(a) - rank(b));
  clusterLayout(x, z, { n: kinds.length, size: size * 5.5, seed: Math.round(x * 13 + z * 7) & 1023 }).forEach((c, i) => {
    if (!ok(c.x, c.z, 0.2)) return;
    const [pts, paint] = K[kinds[i]]();
    const h = popup(pts, paint, { x: c.x, z: c.z, yaw: c.yaw, scale: c.scale * size, sway: ['grass', 'shrub', 'seapinks'].includes(kinds[i]) ? 0.6 : 0 });
    if (BEHAVIOUR[kinds[i]]) LIFE.creatures.push([h, BEHAVIOUR[kinds[i]]]);
  });
}
function dune(x, z, { w = 5, h = 3.6, n = 4, yaw = 0 } = {}) {
  const layers = Array.from({ length: n }, (_, k) => ({ pts: P2.roughen(peak(w * (1 - k * 0.1), h * (1 - k * 0.18), 0.25 + (k % 2 ? 0.08 : -0.04)), rnd),
    paint: EX.paintHill({ ground: P2.shade(C.dune, -0.18 + k * 0.1), accent: C.cream, ink: C.ink }), z: k * 0.5 }));
  return popup(null, null, { node: layeredCard(layers.map((L, k) => ({ ...L, pts: L.pts.map(([px, py]) => [px + (k - 1) * w * 0.12, py]) })), H.cardOpts(x, z, 1, null, RES)), height: h, x, z, yaw, solid: w * 0.45 });
}
const houseColors = (wall, roof) => ({ wall, roof, window: C.window, door: C.door, ink: C.ink });

// ---- the hero: a fisher kid in a yellow raincoat and sou'wester, a lantern in one hand, a creel on the back
const heroDoll = () => {
  const g = new H.THREE.Group(), body = new H.THREE.Group(); g.add(body);
  const PROFILE = -Math.PI / 2;                                       // a profile card: its +x points forward (+z)
  const T = 0.05, GAP = 0.03, SIDE = 0.01;                            // card thickness; air between layers; beside each other
  const card = ([pts, paint], seed, { x = 0, y = 0, z = 0, ry = 0, parent = body, back = 'mirror', name = '', cut = null } = {}) => {
    const m = makeCard(pts, { paint, paper: H.paper, thickness: T, edgeWidth: 0.04, pxPerUnit: 64, seed, back, folds: [], geomPts: cut });
    m.position.set(x, y, z); m.rotation.y = ry; m.name = name; parent.add(m); return m;   // named: clips() reports by name
  };
  const ext = ([pts]) => pts.reduce((e, [x, y]) => ({ x0: Math.min(e.x0, x), x1: Math.max(e.x1, x), y0: Math.min(e.y0, y), y1: Math.max(e.y1, y) }), { x0: Infinity, x1: -Infinity, y0: Infinity, y1: -Infinity });
  // a profile card's z so its front edge (its outline's +x, which faces forward) stays a gap behind a front card at z0
  const behind = (piece, z0) => z0 - T / 2 - GAP - ext(piece).x1;
  const band = (pts, lo, hi, k = 1) => [[lo, 1], [hi, -1]].reduce((poly, [v, s]) => {   // keep lo <= y (k 0: x) <= hi
    const out = [], ok = (p) => s * (p[k] - v) >= 0;
    poly.forEach((a, i) => { const b = poly[(i + 1) % poly.length]; if (ok(a)) out.push(a); if (ok(a) !== ok(b)) { const t = (v - a[k]) / (b[k] - a[k]); out.push(k ? [a[0] + (b[0] - a[0]) * t, v] : [v, a[1] + (b[1] - a[1]) * t]); } });
    return out;
  }, pts);
  const plain = (c) => (P) => { P.gradient(P2.shade(c, 0.08), P2.shade(c, -0.1), 0.5); P.felt(); P.innerShade(P2.shade(c, -0.5), { alpha: 0.25, blurPx: 8 }); };
  const jacket = '#f2b632', jacketSide = '#d99a22', collar = '#f6ead0', hat = '#f2b632', trousers = '#34506e', skin = '#e9c49c', hair = '#3a2416';
  // the layers, front to back: hat (z 0.16), face (0.08), jacket and arms (0), legs (-0.16); the profiles behind them
  const Z = { hat: 0.16, face: 0.08, jacket: 0, legs: -0.16 };
  // the torso: the jacket front (collar, buttons, a pocket) with its side (a seam, a side pocket) behind it; a plain back
  const jacketFront = P2.drawnPiece((gg, ink) => {
    gg.fillStyle = ink(jacket); D.rect(gg, -0.38, 0, 0.76, 1.28, 0.22);
    gg.fillStyle = ink(collar); D.poly(gg, [[-0.26, 1.28], [0.26, 1.28], [0.1, 1.08], [-0.1, 1.08]]);
    gg.fillStyle = ink('#c98a1c', 'print'); D.rect(gg, -0.3, 0.18, 0.2, 0.2, 0.04); D.rect(gg, -0.38, 0.62, 0.76, 0.04);
    gg.fillStyle = ink('#2f4a66', 'print'); D.ell(gg, 0.04, 0.95, 0.035, 0.035); D.ell(gg, 0.04, 0.75, 0.035, 0.035); D.ell(gg, 0.04, 0.45, 0.035, 0.035);
  }, { w: 0.85, h: 1.3, name: 'jacket' });
  const jacketY = 0.78, jx = ext(jacketFront), jacketTop = jacketY + jx.y1;
  card(jacketFront, 301, { y: jacketY, z: Z.jacket, back: plain(P2.shade(jacket, -0.06)), name: 'jacket' });
  const jacketSidePiece = P2.drawnPiece((gg, ink) => {
    gg.fillStyle = ink(jacketSide); D.rect(gg, -0.24, 0, 0.48, 1.24, 0.18);
    gg.fillStyle = ink('#b07818', 'print'); D.rect(gg, -0.02, 0.05, 0.04, 1.1); D.rect(gg, 0.06, 0.2, 0.14, 0.16, 0.03);
  }, { w: 0.55, h: 1.3, name: 'jacket side' });
  const TORSO = 0.32;                                                 // the torso's depth: its side card trimmed to it
  const jacketSideZ = behind(jacketSidePiece, Z.jacket), jacketBack = Z.jacket - T / 2 - GAP - TORSO;
  card(jacketSidePiece, 302, { y: 0.8, z: jacketSideZ, ry: PROFILE, name: 'jacket side', cut: band(jacketSidePiece[0], jacketBack - jacketSideZ, 9, 0) });
  // legs: a frontal + a profile card per leg, from hip pivots set apart (the legs never overlap each other, nor the
  // jacket's side card) and a layer behind the jacket, deeper than the jacket's hem moves through when they swing
  const legFront = (i) => P2.drawnPiece((gg, ink) => { gg.fillStyle = ink(trousers); D.rect(gg, -0.1, 0.18, 0.2, 0.8, 0.05); gg.fillStyle = ink('#4a2a18'); D.rect(gg, -0.12, 0, 0.24, 0.22, 0.07); }, { w: 0.3, h: 1.0, name: `leg ${i}` });
  const legSide = (i) => P2.drawnPiece((gg, ink) => { gg.fillStyle = ink(P2.shade(trousers, -0.08)); D.rect(gg, -0.1, 0.18, 0.2, 0.8, 0.05); gg.fillStyle = ink('#4a2a18'); D.rect(gg, -0.1, 0, 0.3, 0.22, 0.08); }, { w: 0.45, h: 1.0, name: `leg ${i} side` });
  const hipX = ext(legFront(0)).x1 + T / 2 + SIDE;                       // the inner edge clears the jacket's side card
  const legs = [-hipX, hipX].map((x, i) => {
    const hip = new H.THREE.Group(); hip.position.set(x, 0.95, Z.legs); body.add(hip);
    const side = legSide(i);
    card(legFront(i), 310 + i, { y: -0.97, parent: hip, name: `leg ${i}` });
    card(side, 320 + i, { y: -0.97, z: behind(side, 0), ry: PROFILE, parent: hip, name: `leg ${i} side` });
    return hip;
  });
  // the head: a face in front of the jacket (hair printed on its back), its profile behind it, trimmed to the band
  // between the collar and the hat's brim so it shares the centre plane with neither the jacket's side nor the hat's
  const face = P2.drawnPiece((gg, ink) => {
    gg.fillStyle = ink(skin); D.ell(gg, 0, 0.38, 0.36, 0.38);
    gg.fillStyle = ink(hair, 'print'); D.rect(gg, -0.3, 0.5, 0.6, 0.12, 0.06);
    gg.fillStyle = ink('#2a1608', 'print'); D.ell(gg, -0.12, 0.35, 0.04, 0.05); D.ell(gg, 0.12, 0.35, 0.04, 0.05);
    gg.fillStyle = ink('#c9845a', 'print'); for (const fx of [-0.2, -0.16, 0.16, 0.2]) D.ell(gg, fx, 0.25, 0.015, 0.015);
    gg.fillStyle = ink('#8a3a22', 'print'); D.rect(gg, -0.07, 0.17, 0.14, 0.03, 0.015);
  }, { w: 0.8, h: 0.8, name: 'face' });
  card(face, 304, { y: 1.88, z: Z.face, back: plain(hair), name: 'face' });
  const hatY = 2.42, headY = 1.86;
  const headSide = P2.drawnPiece((gg, ink) => {
    gg.fillStyle = ink(P2.shade(skin, -0.04)); D.ell(gg, 0, 0.38, 0.34, 0.38);
    gg.fillStyle = ink(hair); D.ell(gg, -0.12, 0.44, 0.24, 0.32);
    gg.fillStyle = ink('#e0b896', 'print'); D.ell(gg, 0.02, 0.36, 0.06, 0.08);
    gg.fillStyle = ink('#2a1608', 'print'); D.ell(gg, 0.22, 0.35, 0.03, 0.045);
  }, { w: 0.75, h: 0.8, name: 'head side' });
  const headSideZ = behind(headSide, Z.face), headBack = headSideZ + ext(headSide).x0;   // the back of the head (hair)
  card(headSide, 305, { y: headY, z: headSideZ, ry: PROFILE, name: 'head side',
    cut: band(headSide[0], jacketTop + GAP - headY, hatY - GAP - headY) });
  // the knitted bobble hat: a frontal crown in front of the face, a profile crown behind it, a pompom on both
  const hatPiece = (c) => P2.drawnPiece((gg, ink) => {
    gg.fillStyle = ink(c); D.rect(gg, -0.34, 0, 0.68, 0.36, 0.16);
    gg.fillStyle = ink(P2.shade(c, -0.22)); D.rect(gg, -0.35, 0, 0.7, 0.1, 0.04);
    gg.fillStyle = ink(P2.shade(c, -0.12)); D.rect(gg, -0.5, 0, 1.0, 0.09, 0.04);
    gg.fillStyle = ink('#2f4a66', 'print'); D.rect(gg, -0.34, 0.16, 0.68, 0.05);
  }, { w: 1.1, h: 0.6, name: 'hat' });
  card(hatPiece(hat), 306, { y: hatY, z: Z.hat, name: 'hat' });
  const hatSide = hatPiece(P2.shade(hat, -0.06));
  card(hatSide, 307, { y: hatY, z: behind(hatSide, Z.face), ry: PROFILE, name: 'hat side' });
  // arms: a frontal + a profile card each, from shoulder pivots just outside the jacket (a swinging arm never sweeps
  // through the body); the right hand carries the watering can, hung just below the hand
  const armArt = (c, name) => P2.drawnPiece((gg, ink) => { gg.fillStyle = ink(c); D.rect(gg, -0.1, 0.14, 0.2, 0.66, 0.09); gg.fillStyle = ink(collar); D.rect(gg, -0.1, 0.12, 0.2, 0.09, 0.04); gg.fillStyle = ink(skin); D.ell(gg, 0, 0.08, 0.09, 0.08); }, { w: 0.3, h: 0.85, name });
  const shoulderX = jx.x1 + ext(armArt(jacket, 'arm')).x1 + SIDE;     // right against the jacket's edge, never over it
  const arms = [-shoulderX, shoulderX].map((x, i) => {
    const sh = new H.THREE.Group(); sh.position.set(x, 1.98, Z.jacket); body.add(sh);
    const side = armArt(jacketSide, `arm ${i} side`);
    card(armArt(jacket, `arm ${i}`), 330 + i, { y: -0.8, parent: sh, name: `arm ${i}` });
    card(side, 340 + i, { y: -0.8, z: behind(side, 0), ry: PROFILE, parent: sh, name: `arm ${i} side` });
    return sh;
  });
  const can = P2.drawnPiece((gg, ink) => {                           // the can, in profile: spout forward, a handle on top
    gg.fillStyle = ink('#3d4a5c'); D.rect(gg, -0.2, 0, 0.4, 0.36, 0.05); D.poly(gg, [[0.16, 0.12], [0.24, 0.16], [0.48, 0.44], [0.44, 0.48]]);
    gg.fillStyle = ink('#ffcf6a'); D.rect(gg, -0.12, 0.34, 0.24, 0.12, 0.04);
    gg.fillStyle = ink('#26303e', 'print'); D.rect(gg, -0.2, 0.1, 0.4, 0.03); D.rect(gg, -0.2, 0.24, 0.4, 0.03);
  }, { w: 1.05, h: 0.55, name: 'lantern' });
  card(can, 350, { y: -0.8 - GAP - ext(can).y1, ry: PROFILE, parent: arms[1], name: 'lantern' });
  // the basket on the back: its side card right behind the torso's (a plane aside where it passes the head's profile),
  // its card behind both (seen from behind: the weave on its back); greens poke up at the shoulders
  const basket = (side) => P2.drawnPiece((gg, ink) => {
    gg.fillStyle = ink('#7fa6b8'); for (const [x, a] of [[-0.18, -0.3], [-0.02, 0.1], [0.14, 0.4]]) D.poly(gg, [[x - 0.05, 0.8], [x + 0.05, 0.8], [x + Math.sin(a) * 0.3 + 0.03, 1.32], [x + Math.sin(a) * 0.3 - 0.03, 1.32]]);
    gg.fillStyle = ink(side ? '#9a6a3a' : '#a8784a'); D.rect(gg, side ? -0.22 : -0.32, 0, side ? 0.44 : 0.64, 0.86, 0.1);
    gg.fillStyle = ink('#7a4e28', 'print'); for (let k = 0; k < 4; k++) D.rect(gg, side ? -0.22 : -0.32, 0.12 + k * 0.18, side ? 0.44 : 0.64, 0.05);
  }, { w: 0.75, h: 1.4, name: 'basket' });
  const basketSide = basket(true), bs = ext(basketSide), basketY = 0.96, DEPTH = 0.25;   // its depth: the side card trimmed
  const basketSideZ = jacketBack - GAP - bs.x1, basketZ = basketSideZ + bs.x1 - DEPTH - GAP - T / 2;
  card(basketSide, 361, { x: T + SIDE, y: basketY, z: basketSideZ, ry: PROFILE, name: 'basket side', cut: band(basketSide[0], bs.x1 - DEPTH, 9, 0) });
  card(basket(false), 360, { y: basketY, z: Math.min(basketZ, headBack - T / 2 - GAP), name: 'basket' });
  // the stride (motion.md section 8): the phase runs with the distance walked; in the stance a leg's angle is LINEAR in
  // distance, so the planted foot stays put; the swing eases forward; arms swing opposite the legs (the loaded arm
  // less); the body bobs twice per stride. Rotation only, never a scale.
  const legLen = 0.97 * 1.25, stepLen = 1.2, R = stepLen / (2 * legLen);
  const leg = (ph, gait) => { const u = (ph / Math.PI) % 2, A = gait * R; if (u >= 1) return A * (3 - 2 * u); const e = u * u * (3 - 2 * u); return A * (2 * e - 1); };
  g.userData.stride = (walked, gait) => {
    const ph = walked / stepLen * Math.PI, l0 = leg(ph, gait), l1 = leg(ph + Math.PI, gait);
    legs[0].rotation.x = -l0; legs[1].rotation.x = -l1;              // + forward = the foot toward +z
    arms[0].rotation.x = l0 * 0.7; arms[1].rotation.x = l1 * 0.7 * 0.3;   // opposite the leg on its side; the can arm swings less
    body.position.y = Math.abs(Math.sin(ph)) * 0.05 * gait;
  };
  return g;
};

if (flags.TEST) {
  { const doll = heroDoll(); H.setHero(popup(null, null, { node: doll, height: 3.1, x: 2, z: -4, sway: 0.2, scale: 1.25 }), { stride: doll.userData.stride }); }
  popup(...palm(9, 0.6), { x: -3, z: -8, cross: true, sway: 0.8 }); popup(...K.crab(), { x: 5, z: -3 }); popup(...K.net(), { x: -1, z: -2.5 });
} else buildWorld();

if (!flags.TEST) {
  const life = createLife({ scene: H.scene, camera: H.camera, heroHeight: H.heroHeight, seed: 41, wind: [0.94, 0.34] });
  life.flock({ size: 6, height: 3.6, colors: ['#f6f1e6', '#e4e2dc'] });
  life.puffs({ at: LIFE.chimneys, perEmitter: 3, life: 4.5, rise: 0.45, size: [0.2, 0.45], colors: ['#f3e8d2', '#ece0c8'] });
  life.cloudShadows({ count: 4 });
  for (const [h, roam] of LIFE.floaters) life.critter(h.group, { behaviour: 'float', roam });
  for (const [h, behaviour] of LIFE.creatures) life.critter(h.group, { behaviour, hero: H.hero.group.position, walk: H.walk, roam: 1.2 });
  life.reset(H.target);
  H.onStep((t, dt) => life.update(dt, H.target));
  H.onRestart(() => life.reset(H.target));
}

function buildWorld() {
  const at = (z, off) => [pathX(z) + off, z];
  // fishing huts along the boardwalk, on the sea side; each with a door scene
  const huts = [[at(-12, -6), { w: 4.6, d: 3.8, wallH: 3.2, roofH: 2.4 }, C.wall, C.roofA, 71, 0.35], [at(-3.5, -6.5), { w: 4.0, d: 3.4, wallH: 2.9, roofH: 2.2, windows: 1 }, C.wallB, C.roofB, 73, 0.15],
    [at(-19, 5.5), { w: 4.4, d: 3.6, wallH: 3.1, roofH: 2.3 }, C.wallC, C.roofC, 79, -0.25], [at(-7, 6.5), { w: 3.8, d: 3.2, wallH: 2.8, roofH: 2.1, windows: 1 }, C.wall, C.roofB, 83, -0.4]];
  for (const [[x, z], dims, wall, roof, seed, yaw] of huts) {
    const node = boxHouse({ ...dims, colors: houseColors(wall, roof), paper: H.paper, seed, print: H.cardOpts(x, z) });
    const h = popup(null, null, { node, height: dims.wallH + dims.roofH, x, z, yaw, solid: 3.2 });
    if (node.userData.chimneyTop) LIFE.chimneys.push(node.userData.chimneyTop);
    H.glowing(h.group); H.lamp(x + Math.sin(yaw) * 2.6, 2.2, z + Math.cos(yaw) * 2.6, 1, 11); mark(x, z, 4.2);
  }
  const DOOR = [['net', 'crate', 'gull'], ['barrel', 'seapinks', 'crab'], ['crate', 'buoy', 'grass'], ['seapinks', 'barrel', 'starfish']];
  huts.forEach(([[x, z], dims, , , , yaw], i) => { const gx = x + Math.cos(yaw) * (dims.w / 2 + 1.6), gz = z + dims.d / 2 + 1.2; group(gx, gz, DOOR[i], 0.6, (px, pz) => pathDist(px, pz) > 1.7 && seaDist(px, pz) > 2); mark(gx, gz, 1.8); });
  // lamps along the boardwalk
  for (const [z, sd] of [[-6, -1], [-15, 1], [1, 1]]) { const x = pathX(z) + sd * 1.9; popup(...K.lamp(), { x, z, scale: 1.25 }); mark(x, z, 1); H.lamp(x, 3.6, z + 0.3, 0.66, 9); }
  // the lighthouse on its rocky point, toy-scale with its lamp in frame
  { const z = -17, x = shoreX(z) + 4.6; popup(...lighthouse(12), { x, z, cross: true }); mark(x, z, 3.5);
    for (const [dx, dz, s] of [[-2.4, 1.2, 1.1], [2.2, 1.5, 0.9], [-0.6, 2.6, 0.8], [3.2, -0.6, 1.0]]) popup(...K.rock(), { x: x + dx, z: z + dz, yaw: (rnd() - 0.5) * 0.6, scale: s }); mark(x, z + 1, 4.5); }
  // the jetty: an OPEN construction from the beach out over the water, a moored sailboat
  {
    const JW = 9, JD = 2, JH = 0.6, jz = -9, jx = shoreX(jz) - JW / 2 + 2.2;
    const posts = (w, h) => P2.fromDrawing((gg) => { D.rect(gg, -w / 2, h - 0.16, w, 0.16); const n = Math.round(w / 0.75); for (let i = 0; i <= n; i++) D.rect(gg, -w / 2 + (n ? i * (w - 0.16) / n : 0), 0, 0.16, h); }, { w: w + 0.1, h: h + 0.05, name: 'posts' });
    const wood = (n, vertical) => EX.paintWood({ wood: C.board }, { planks: n, vertical });
    const jetty = platform({ w: JW, d: JD, h: JH, paper: H.paper, seed: 141, facePts: posts(JW, JH), supportPts: posts(JW * 0.9, JH).map(([px, py]) => [px, py - JH]),
      paints: { face: wood(1, true), deck: wood(Math.round(JW / 0.42), true), support: wood(1, true) }, print: H.cardOpts(jx, jz) });
    jetty.name = 'jetty'; const j = popup(null, null, { node: jetty, height: JH, x: jx, z: jz, level: true }); walk.add(jetty);
    for (const dx of [-JW / 2 + 0.3, -JW / 2 + 2.2]) popup(posts(0.18, 1.1), wood(1, true), { parent: jetty.userData.deck, x: dx, z: 0.05, order: j.order + 0.5 });
    LIFE.floaters.push([popup(...sailboat(2.8, C.coral), { x: jx - 1.5, z: jz + 2.6, yaw: 0.2, sway: 0.35 }), 0.3]);
    mark(shoreX(jz), jz, 3);
  }
  for (const [z, dx, sail, s] of [[-30, -9, C.roofC, 1.8], [-4, -10, C.cream, 1.6], [-18, -14, C.coral, 1.5], [6, -7, C.roofC, 1.4]]) LIFE.floaters.push([popup(...sailboat(s * 1.5, sail), { x: shoreX(z) + dx, z, yaw: (rnd() - 0.5) * 0.6, sway: 0.35 }), 0.5]);
  for (const [z, dx] of [[-13, -4], [-1, -3.5]]) LIFE.floaters.push([popup(...K.buoy(), { x: shoreX(z) + dx, z, sway: 0.3 }), 0.2]);
  walk.block((x, z) => seaDist(x, z) < 0.5);
  // beached rowboats and dunes
  for (const [z, dx, yaw] of [[-14, 3.6, 0.5], [2, 3.4, -0.3]]) { const x = shoreX(z) + dx; popup(...K.rowboat(), { x, z, yaw }); mark(x, z, 2.2); }
  for (const [x, z, o] of [[24, -12, { yaw: -0.2 }], [27, 2, { w: 4.2, h: 3.0, n: 3 }], [18, -26, { w: 5.5, h: 4 }]]) if (free(x, z, 1.5)) { dune(x, z, o); mark(x, z, (o.w || 5) * 0.8); }
  // the hero on the boardwalk
  const doll = heroDoll(), hero = popup(null, null, { node: doll, height: 3.1, x: HERO_AT[0], z: HERO_AT[1], sway: 0.2, scale: 1.25 }); H.setHero(hero, { stride: doll.userData.stride });
  mark(HERO_AT[0], HERO_AT[1], 2.4);

  // the fill: palms (high), groups (middle), clearings (low) from a slow noise, only where the camera sees
  rnd = P2.rng(202);
  const cellSeed = (gx, gz, salt) => (Math.imul(Math.round(gx * 10), 73856093) ^ Math.imul(Math.round(gz * 10), 19349663) ^ Math.imul(salt, 83492791)) >>> 0;
  const ph = [rnd() * 6.28, rnd() * 6.28, rnd() * 6.28, rnd() * 6.28];
  const lush = (x, z) => 0.5 + 0.24 * Math.sin(x * 0.12 + ph[0]) * Math.sin(z * 0.14 + ph[1]) + 0.16 * Math.sin(x * 0.21 + z * 0.15 + ph[2]) + 0.1 * Math.sin(x * 0.05 - z * 0.31 + ph[3]);
  const trees = [], placed = [];
  const DRESS = ['grass', 'grass', 'shrub', 'rock', 'rock', 'seapinks', 'seapinks', 'crate', 'barrel', 'starfish', 'buoy', 'crab', 'gull', 'net'];
  const CAP = { crab: 3, gull: 3, net: 2 }, used = {};
  const kindsFor = (n) => { const out = []; n = Math.min(n, [...new Set(DRESS)].filter((k) => (used[k] || 0) < (CAP[k] ?? Infinity)).length); while (out.length < n) { const k = DRESS[Math.floor(rnd() * DRESS.length)]; if (!out.includes(k) && (used[k] || 0) < (CAP[k] ?? Infinity)) { out.push(k); used[k] = (used[k] || 0) + 1; } } return out; };
  const [hx0, hz0] = HERO_AT;
  const corridor = (x, z) => z > hz0 - 1 && z < hz0 + 16 && Math.abs(x - hx0) < 7 + (z - hz0) * 0.35;
  const fillGroups = (see) => { for (let gz = -46; gz <= 18; gz += 3.1) for (let gx = -46; gx <= 46; gx += 3.1) {
    rnd = P2.rng(cellSeed(gx, gz, 19));
    const x = gx + (rnd() - 0.5) * 2.6, z = gz + (rnd() - 0.5) * 2.6, l = lush(x, z);
    if (!see(x, z, 0.12, 4) || l < 0.3 || placed.some(([px, pz]) => Math.hypot(x - px, z - pz) < 3.0)) continue;
    placed.push([x, z]);
    if (l > 0.56 && free(x, z, 1.6) && !corridor(x, z) && trees.every(([tx, tz]) => Math.hypot(x - tx, z - tz) > 4.8)) {
      trees.push([x, z]); popup(...palm(between(7.5, 10), (rnd() - 0.5) * 1.6), { x, z, cross: true, sway: 0.8 });
    } else if (free(x, z, 1.0)) group(x, z, kindsFor(4 + Math.floor(rnd() * 3)), 1.1);
  } };
  fillGroups(H.inFrame);
  const fillSmall = (see, z0 = -30, x0 = 40) => { for (let gz = z0; gz <= 12; gz += 2.2) for (let gx = -x0; gx <= x0; gx += 2.2) {
    rnd = P2.rng(cellSeed(gx, gz, 69));
    const x = gx + (rnd() - 0.5) * 1.6, z = gz + (rnd() - 0.5) * 1.6, l = lush(x, z);
    if (!see(x, z, 0.05, 1) || l < 0.3 || !free(x, z, 0.4) || placed.some(([px, pz]) => Math.hypot(x - px, z - pz) < 1.9)) continue;
    placed.push([x, z]);
    const k = ['grass', 'seapinks', 'starfish', 'grass', 'rock'][Math.floor(rnd() * 5)];
    popup(...K[k](), { x, z, yaw: (rnd() - 0.5) * 0.7, scale: 0.65 + rnd() * 0.25, sway: k === 'grass' || k === 'seapinks' ? 0.6 : 0 });
  } };
  fillSmall(H.inFrame);
  rnd = P2.rng(303);
  for (const [sx, dz, s, kind] of [[-0.45, 6.7, 1.6, 'grass'], [1.05, 7.2, 1.9, 'palm'], [0.3, 8.2, 1.4, 'shrub']]) {
    const p = H.groundAt(sx, -1); if (!p) continue;
    const x = p.x, z = p.z + dz;
    if (kind === 'palm') popup(...palm(9, -0.5), { x, z, cross: true, scale: s, sway: 0.6 });
    else popup(...K[kind](), { x, z, scale: s, yaw: (rnd() - 0.5) * 0.4, sway: 0.6 });
  }
  const ring = (x, z, m, y) => H.inReach(x, z, 0.02, y) && !H.inFrame(x, z, m, y);
  RES = 0.75; fillGroups(ring); fillSmall(ring, -36, 44); RES = 1;
}

// ---- ?pan: a slow camera pan over the whole cove (the fixed clock drives it: t 3.2 s risen -> +PAN_T s)
if (PAN) {
  const KEYS = [[-16, -1], [-16, -1], [-10, -13], [2, -19], [10, -8], [11, 0], [11, 0]], PAN_T = 12, T0 = QS.has('panT0') ? Number(QS.get('panT0')) : 1.6;
  const cr = (p0, p1, p2, p3, t) => 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t);
  const at = (u) => { const n = KEYS.length - 3, f = Math.min(n - 1e-6, Math.max(0, u * n)), i = Math.floor(f), t = f - i;
    return [0, 1].map((k) => cr(KEYS[i][k], KEYS[i + 1][k], KEYS[i + 2][k], KEYS[i + 3][k], t)); };
  let yaw0 = null;
  // fold-up on camera: every piece lies flat until it comes into the frame, then rises on its hinge (a small
  // per-piece jitter so neighbours stagger); nothing folds back down once it has risen
  const risen = new Set(), _w = new H.THREE.Vector3(), _p = new H.THREE.Vector3();
  H.onRestart(() => risen.clear());
  H.onStep(() => {
    for (const h of H.hinges) {
      if (risen.has(h)) continue;
      h.group.getWorldPosition(_w); _p.set(_w.x, _w.y + 0.5, _w.z).project(H.camera);
      if (Math.abs(_p.x) < 0.98 && _p.y > -1.02 && _p.y < 0.95 && _p.z < 1) { risen.add(h); h.set(1, 0.05 + (h.jit || 0) * 6); }
      else if (h.open !== 0 || h.pending) h.reset(0);
    }
  });
  H.onStep((t) => {
    if (yaw0 === null) yaw0 = H.view.tyaw;
    let u = QS.has('panAt') ? Number(QS.get('panAt')) : (t - T0) / PAN_T; u = Math.min(1, Math.max(0, u)); u = u * u * (3 - 2 * u);
    const [x, z] = at(u);
    H.target.x = x; H.target.z = z; H.view.dist = 50;
    H.view.tyaw = yaw0 - 10 + 20 * u;
    FOC[0] = x - 0.5; FOC[2] = z + 0.5;
  });
}
H.start();
