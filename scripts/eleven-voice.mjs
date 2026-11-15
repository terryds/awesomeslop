// Records the voices for a "video podcast" art with ElevenLabs.
//
//   ELEVENLABS_API_KEY=... node scripts/eleven-voice.mjs arts/015-the-thousandth-temple
//
// Reads the script lines out of the art's index.html ({ w: 'L' | 'D', t: "..." }), asks ElevenLabs for each line with
// word timings, gives each line its place on one timeline, and writes:
//   <art>/v00.mp3, v01.mp3 ...  one clip per line
//   <art>/index.html         the `const VOICE = ...;` line, filled with line starts, lengths and per-word timings
// Each line's result is kept in node_modules/.cache/eleven, so a re-run only pays for lines whose text or voice changed.
// Voices: ELEVEN_VOICE_L and ELEVEN_VOICE_D (voice ids). Needs ffmpeg.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import path from 'node:path';

const dir = process.argv[2];
const key = process.env.ELEVENLABS_API_KEY;
if (!dir) { console.error('usage: ELEVENLABS_API_KEY=... node scripts/eleven-voice.mjs arts/<slug>'); process.exit(1); }
const VOICES = { L: process.env.ELEVEN_VOICE_L || '6qpxBH5KUSDb40bij36w', D: process.env.ELEVEN_VOICE_D || 'aSXZu6bgEOS8MXVRzjPi' };
const MODEL = process.env.ELEVEN_MODEL || 'eleven_multilingual_v2';
const LEAD = 0.7, GAP_SAME = 0.26, GAP_TURN = 0.34, TAIL = 0.12;

const htmlPath = path.join(dir, 'index.html');
let html = await readFile(htmlPath, 'utf8');
const lines = [...html.matchAll(/\{ w: '([LD])', t: "((?:[^"\\]|\\.)*)"/g)].map((m) => ({ w: m[1], t: JSON.parse(`"${m[2]}"`) }));
if (!lines.length) { console.error('no script lines found in ' + htmlPath); process.exit(1); }

const cache = path.resolve('node_modules/.cache/eleven');
await mkdir(cache, { recursive: true });
const r3 = (x) => Math.round(x * 1000) / 1000;
const out = { t0: [], dur: [], w: [] };
const clips = [];
let t = LEAD, spent = 0;

for (const [i, l] of lines.entries()) {
  const id = createHash('sha1').update([MODEL, VOICES[l.w], l.t].join('|')).digest('hex').slice(0, 16);
  const mp3 = path.join(cache, id + '.mp3'), json = path.join(cache, id + '.json');
  if (!existsSync(mp3) || !existsSync(json)) {
    if (!key) { console.error(`line ${i} is not recorded yet: set ELEVENLABS_API_KEY`); process.exit(1); }
    const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICES[l.w]}/with-timestamps?output_format=mp3_44100_128`, {
      method: 'POST',
      headers: { 'xi-api-key': key, 'content-type': 'application/json' },
      body: JSON.stringify({ text: l.t, model_id: MODEL, voice_settings: { stability: 0.42, similarity_boost: 0.8, style: 0.35, use_speaker_boost: true } }),
    });
    if (!res.ok) { console.error(`line ${i}: ${res.status} ${(await res.text()).slice(0, 300)}`); process.exit(1); }
    const d = await res.json();
    await writeFile(mp3, Buffer.from(d.audio_base64, 'base64'));
    await writeFile(json, JSON.stringify(d.alignment));
    spent += l.t.length;
  }
  const a = JSON.parse(await readFile(json, 'utf8'));
  // words = runs of characters between spaces, same split as the page uses for its captions
  const words = []; let cur = null;
  a.characters.forEach((ch, k) => {
    if (ch === ' ') { cur = null; return; }
    if (!cur) { cur = [a.character_start_times_seconds[k], 0]; words.push(cur); }
    cur[1] = a.character_end_times_seconds[k];
  });
  const want = l.t.split(' ').length;
  if (words.length !== want) { console.error(`line ${i}: got ${words.length} words, the page splits it into ${want}`); process.exit(1); }
  const dur = words[words.length - 1][1] + TAIL;
  t += i === 0 ? 0 : lines[i - 1].w === l.w ? GAP_SAME : GAP_TURN;
  out.t0.push(r3(t)); out.dur.push(r3(dur)); out.w.push(words.map((w) => [r3(w[0]), r3(w[1])]));
  clips.push({ mp3, at: t, dur, w: l.w });
  t += dur;
}

// one small file per line (v00.mp3, v01.mp3, ...), trimmed to its speech. Separate files need no seeking to play,
// so they work on servers that ignore byte ranges.
// Level the two voices: measure how loud each clip is, take each host's typical loudness, and give every clip of
// that host the same gain so both sit at TARGET. One gain per host keeps a shout louder than a murmur.
const TARGET = -17; // LUFS
const loud = (f, dur) => {
  const r = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', f, '-af', `atrim=0:${dur.toFixed(3)},ebur128`, '-f', 'null', '-'], { encoding: 'utf8' });
  const m = [...r.stderr.matchAll(/I:\s+(-?[\d.]+) LUFS/g)].pop();
  return m ? +m[1] : NaN;
};
const gain = {};
for (const who of ['L', 'D']) {
  const ls = clips.filter((c) => c.w === who && c.dur > 1).map((c) => loud(c.mp3, c.dur)).filter((x) => x > -60).sort((a, b) => a - b);
  const med = ls.length ? ls[ls.length >> 1] : TARGET;
  gain[who] = TARGET - med;
  console.log(`${who}: typical ${med.toFixed(1)} LUFS, gain ${gain[who].toFixed(1)} dB`);
}
for (const [i, c] of clips.entries()) {
  execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-i', c.mp3, '-af',
    `atrim=0:${c.dur.toFixed(3)},volume=${gain[c.w].toFixed(2)}dB,alimiter=limit=0.89:level=false,afade=t=out:st=${(c.dur - 0.06).toFixed(3)}:d=0.06`,
    '-ac', '1', '-ar', '44100', '-b:a', '72k', path.join(dir, `v${String(i).padStart(2, '0')}.mp3`)], { stdio: 'inherit' });
}

if (!/const VOICE = .*;/.test(html)) { console.error('index.html has no `const VOICE = ...;` line'); process.exit(1); }
html = html.replace(/const VOICE = .*;/, () => `const VOICE = ${JSON.stringify(out)};`);
await writeFile(htmlPath, html);
console.log(`${lines.length} lines, ${t.toFixed(1)} s, ${spent} characters newly recorded -> ${dir}/v00.mp3 ... v${String(lines.length - 1).padStart(2, '0')}.mp3`);
