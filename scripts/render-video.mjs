// Renders a "video podcast" art (015-the-thousandth-temple) to an mp4, frame by frame, with its sound.
//
//   node scripts/render-video.mjs arts/015-the-thousandth-temple out.mp4 [seconds]
//
// Picture: headless Chrome opens the piece frozen (?hold), and for every frame the script sets the film's clock,
// redraws, and takes a screenshot. Nothing is recorded in real time, so no frame is ever dropped.
// Sound: the music and effects are rendered by the page's own synth into an offline audio context; the voice
// clips (v00.mp3 ...) are laid on the timeline at the line starts the page reports. ffmpeg joins it all.
// Needs Google Chrome and ffmpeg. The piece must expose T, LEN, LINES, CUES, draw() and its synth as globals.
import { spawn, execFileSync } from 'node:child_process';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';

const [dir, outArg, secArg] = process.argv.slice(2);
if (!dir) { console.error('usage: node scripts/render-video.mjs arts/<slug> [out.mp4] [seconds]'); process.exit(1); }
const out = path.resolve(outArg || path.basename(dir).replace(/^\d+-/, '') + '.mp4');
const FPS = 30, W = 1280, H = 720, SCALE = 1.5, PORT = 9333 + Math.floor(Math.random() * 500);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
if (!existsSync(CHROME)) { console.error('Chrome not found; set CHROME=/path/to/chrome'); process.exit(1); }

const tmp = await mkdtemp(path.join(tmpdir(), 'render-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${path.join(tmp, 'profile')}`,
  '--allow-file-access-from-files', '--hide-scrollbars', '--mute-audio', '--no-first-run', `--window-size=${W},${H}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws;
try {
  let target;
  for (let i = 0; i < 50 && !target; i++) { await sleep(200); try { target = (await (await fetch(`http://127.0.0.1:${PORT}/json`)).json()).find((t) => t.type === 'page'); } catch {} }
  if (!target) throw new Error('Chrome did not start');
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  let id = 0; const pending = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { const [res, rej] = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); } };
  const send = (method, params = {}) => new Promise((res, rej) => { pending.set(++id, [res, rej]); ws.send(JSON.stringify({ id, method, params })); });
  const run = async (expression) => { const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };

  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: SCALE, mobile: false });
  await send('Page.enable');
  await send('Page.navigate', { url: 'file://' + path.resolve(dir, 'index.html') + '?hold&thumb=1' });
  await sleep(1500);
  await run(`new Promise(r => { const t = setInterval(() => { if (Object.values(PHOTOS).every(p => p.im.complete)) { clearInterval(t); r(); } }, 100); })`);
  // fill the frame edge to edge
  const info = await run(`(() => { const d = cv.width / ${W}; K = d; OX = 0; OY = 0; return { LEN, END, t0: LINES.map(l => l.t0) }; })()`);
  const seconds = Math.min(+secArg || info.LEN, info.LEN), frames = Math.round(seconds * FPS);

  // ---- sound: the page's synth, offline
  const n = await run(`(async () => {
    const sr = 44100, oc = new OfflineAudioContext(1, Math.ceil(${seconds} * sr), sr);
    AC = oc; master = oc.createGain(); master.gain.value = .9; master.connect(oc.destination);
    musicG = oc.createGain(); musicG.gain.value = .55; musicG.connect(master);
    for (let b = 0, t = .1; t < ${seconds}; b++, t += .8) { const k = b % 32, d = TUNE[k];
      bell(deg(d), t, .09, 1.5); bell(deg(d + 5), t, .03, .7); bell(deg(TUNE[(k + 1) % 32] + 5), t + .4, .022, .6);
      if (k % 4 === 3) bell(deg(d - 5), t, .07, 2.6); if (k === 31) gong(t, .16); }
    CUES.forEach(c => { if (c[0] < ${seconds} - .05) c[1](c[0]); });
    const f = (await oc.startRendering()).getChannelData(0), u = new Uint8Array(f.length * 2), v = new DataView(u.buffer);
    for (let i = 0; i < f.length; i++) v.setInt16(i * 2, Math.max(-1, Math.min(1, f[i])) * 32767, true);
    window.__pcm = u; return u.length;
  })()`);
  const pcm = Buffer.alloc(n);
  for (let o = 0; o < n; o += 3_000_000) {
    const b64 = await run(`(() => { const s = window.__pcm.subarray(${o}, ${Math.min(n, o + 3_000_000)}); let r = ''; for (let i = 0; i < s.length; i += 32768) r += String.fromCharCode.apply(null, s.subarray(i, i + 32768)); return btoa(r); })()`);
    Buffer.from(b64, 'base64').copy(pcm, o);
  }
  const musicPath = path.join(tmp, 'music.pcm'); await writeFile(musicPath, pcm);

  // ---- picture
  const silent = path.join(tmp, 'picture.mp4');
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-vf', 'scale=1920:1080:flags=lanczos', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
  const started = Date.now();
  for (let f = 0; f < frames; f++) {
    await run(`T = ${(f / FPS).toFixed(5)}; draw(); 0`);
    const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 95 });
    if (!ff.stdin.write(Buffer.from(shot.data, 'base64'))) await new Promise((r) => ff.stdin.once('drain', r));
    if (f % 300 === 0) console.log(`frame ${f} / ${frames}  (${((Date.now() - started) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));

  // ---- join: picture + music + every voice clip at its line start
  const args = ['-loglevel', 'error', '-y', '-i', silent, '-f', 's16le', '-ar', '44100', '-ac', '1', '-i', musicPath];
  const voices = info.t0.map((t, i) => ({ t, f: path.join(dir, `v${String(i).padStart(2, '0')}.mp3`) })).filter((v) => existsSync(v.f) && v.t < seconds);
  voices.forEach((v) => args.push('-i', v.f));
  const filt = voices.map((v, i) => `[${i + 2}]adelay=${Math.round(v.t * 1000)}:all=1[v${i}]`).join(';') + (voices.length ? ';' : '')
    + '[1]' + voices.map((_, i) => `[v${i}]`).join('') + `amix=inputs=${voices.length + 1}:normalize=0,alimiter=limit=0.95[a]`;
  args.push('-filter_complex', filt, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', '-t', String(seconds), '-movflags', '+faststart', out);
  execFileSync('ffmpeg', args, { stdio: 'inherit' });
  console.log(`${frames} frames, ${seconds.toFixed(1)} s -> ${out}`);
} finally {
  try { ws?.close(); } catch {}
  chrome.kill();
  await sleep(300); await rm(tmp, { recursive: true, force: true }).catch(() => {});
}
