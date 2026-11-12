// Turns ./arts/<slug>/ folders into:
//   src/generated/arts.json         metadata + prompt + rendered README for every art
//   src/generated/categories.json   the home page sections, from arts/categories.json (order = display order)
//   public/a/<slug>/          the art's own files (index.html, images, ...)
//
// One art = one folder:
//   art.json    { title, category, date, model, agent, medium, tags, summary, specs, cover }
//   prompt.md   the one prompt that made it
//   README.md   notes about the piece
//   index.html  a live piece (optional)   -or-   an image named in art.json "cover"
import { readdir, readFile, mkdir, rm, cp, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';

const root = path.resolve(import.meta.dirname, '..');
const artsDir = path.join(root, 'arts');
const outJson = path.join(root, 'src/generated/arts.json');
const outAssets = path.join(root, 'public/a');
const RESERVED = new Set(['art.json', 'prompt.md', 'README.md']);

const read = (p) => readFile(p, 'utf8');
const fail = (slug, msg) => {
  console.error(`arts/${slug}: ${msg}`);
  process.exit(1);
};

await rm(outAssets, { recursive: true, force: true });
await mkdir(outAssets, { recursive: true });
await mkdir(path.dirname(outJson), { recursive: true });

// Categories are the sections of the home page. Add one to arts/categories.json before using it in an art.
const categoriesPath = path.join(artsDir, 'categories.json');
const categories = existsSync(categoriesPath) ? JSON.parse(await read(categoriesPath)) : [];
const categoryIds = new Set(categories.map((c) => c.id));

const arts = [];
const entries = existsSync(artsDir) ? await readdir(artsDir, { withFileTypes: true }) : [];
for (const entry of entries) {
  if (!entry.isDirectory() || entry.name.startsWith('.') || entry.name.startsWith('_')) continue;
  const slug = entry.name;
  const dir = path.join(artsDir, slug);
  if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) fail(slug, 'folder name must be lowercase letters, digits and dashes');
  for (const f of ['art.json', 'prompt.md']) if (!existsSync(path.join(dir, f))) fail(slug, `missing ${f}`);

  let meta;
  try {
    meta = JSON.parse(await read(path.join(dir, 'art.json')));
  } catch (e) {
    fail(slug, `art.json is not valid JSON (${e.message})`);
  }
  if (!meta.title) fail(slug, 'art.json needs a "title"');
  if (meta.draft) continue;
  if (meta.category && !categoryIds.has(meta.category)) fail(slug, `unknown category "${meta.category}" (known: ${[...categoryIds].join(', ')})`);

  const hasLive = existsSync(path.join(dir, 'index.html'));
  if (meta.cover && !existsSync(path.join(dir, meta.cover))) fail(slug, `cover "${meta.cover}" not found`);
  if (!hasLive && !meta.cover) fail(slug, 'needs an index.html (live piece) or a "cover" image in art.json');

  const prompt = (await read(path.join(dir, 'prompt.md'))).trim();
  const readmePath = path.join(dir, 'README.md');
  const readme = existsSync(readmePath) ? await read(readmePath) : '';

  await cp(dir, path.join(outAssets, slug), {
    recursive: true,
    filter: (src) => !RESERVED.has(path.basename(src)),
  });

  arts.push({
    slug,
    title: meta.title,
    category: meta.category ?? null,
    date: meta.date ?? null,
    summary: meta.summary ?? '',
    model: meta.model ?? null,
    agent: meta.agent ?? null,
    medium: meta.medium ?? (hasLive ? 'html' : 'image'),
    tags: meta.tags ?? [],
    specs: meta.specs ?? {},
    kind: hasLive ? 'live' : 'image',
    src: hasLive ? `/a/${slug}/` : `/a/${slug}/${meta.cover}`,
    cover: meta.cover ? `/a/${slug}/${meta.cover}` : null,
    prompt,
    readmeHtml: readme ? await marked.parse(readme) : '',
  });
}

// Oldest first gets no. 1; the gallery shows newest first.
arts.sort((a, b) => (a.date ?? '').localeCompare(b.date ?? '') || a.slug.localeCompare(b.slug));
arts.forEach((a, i) => (a.no = i + 1));
arts.reverse();

for (const [file, value] of [[outJson, arts], [path.join(path.dirname(outJson), 'categories.json'), categories]]) {
  const json = JSON.stringify(value, null, 2) + '\n';
  if (!existsSync(file) || (await read(file)) !== json) await writeFile(file, json); // only touch files that changed
}
console.log(`content: ${arts.length} art${arts.length === 1 ? '' : 's'}`);
