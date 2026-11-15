// Takes the still picture a live piece shows on its gallery card (cover.webp), so the gallery does not have to
// run every piece at once. Headless Chrome opens the piece as the gallery would (?thumb=1), lets it run for a
// few seconds, and saves a screenshot next to it. The file is also named in art.json as "cover".
//
//   node scripts/make-cover.mjs                         every live piece that has no cover yet
//   node scripts/make-cover.mjs arts/<slug> [seconds]   one piece (again), captured after [seconds] (default 4)
//
// Needs Google Chrome. Look at the result: if the moment is a dull one, run it again with other seconds.
import { spawn } from 'node:child_process';
import { mkdtemp, readdir, readFile, writeFile, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const W = 960, H = 720, COVER = 'cover.webp', PORT = 9333 + Math.floor(Math.random() * 500);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
if (!existsSync(CHROME)) { console.error('Chrome not found; set CHROME=/path/to/chrome'); process.exit(1); }

const [dirArg, secArg] = process.argv.slice(2);
const seconds = +secArg || 4;
const readMeta = async (dir) => JSON.parse(await readFile(path.join(dir, 'art.json'), 'utf8'));
let dirs;
if (dirArg) dirs = [path.resolve(dirArg)];
else {
  dirs = [];
  for (const e of await readdir(path.join(root, 'arts'), { withFileTypes: true })) {
    const dir = path.join(root, 'arts', e.name);
    if (e.isDirectory() && existsSync(path.join(dir, 'index.html')) && !(await readMeta(dir)).cover) dirs.push(dir);
  }
}
for (const dir of dirs) if (!existsSync(path.join(dir, 'index.html'))) { console.error(`${dir}: no index.html, not a live piece`); process.exit(1); }
if (!dirs.length) { console.log('covers: nothing to do, every live piece has one'); process.exit(0); }

const tmp = await mkdtemp(path.join(tmpdir(), 'cover-'));
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

  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await send('Page.enable');
  for (const dir of dirs) {
    await send('Page.navigate', { url: 'file://' + path.join(dir, 'index.html') + '?thumb=1' });
    await sleep(seconds * 1000);
    const { data } = await send('Page.captureScreenshot', { format: 'webp', quality: 80 });
    await writeFile(path.join(dir, COVER), Buffer.from(data, 'base64'));
    const meta = await readMeta(dir);
    if (meta.cover !== COVER) await writeFile(path.join(dir, 'art.json'), JSON.stringify({ ...meta, cover: COVER }, null, 2) + '\n');
    console.log(`cover: ${path.relative(root, path.join(dir, COVER))} (${Math.round(Buffer.from(data, 'base64').length / 1024)} KB, at ${seconds}s)`);
  }
} finally {
  ws?.close();
  chrome.kill();
  await sleep(300);
  await rm(tmp, { recursive: true, force: true });
}
