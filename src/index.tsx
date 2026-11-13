import { Hono } from 'hono';
import { csrf } from 'hono/csrf';
import { auth, currentUser, isAdmin } from './auth';
import { artNo, arts, categories, claudeBreakdownUrl, getArt, getCategory } from './content';
import { Layout } from './layout';
import type { AppEnv, Art } from './types';

const app = new Hono<AppEnv>();

app.use(csrf());
app.use(async (c, next) => {
  const user = await currentUser(c);
  c.set('user', user && { ...user, admin: isAdmin(c, user) });
  await next();
});
app.route('/auth', auth);

// ---------- gallery ----------

function Preview({ art, thumb }: { art: Art; thumb?: boolean }) {
  if (art.kind === 'image' || (thumb && art.cover)) {
    return <img src={art.cover ?? art.src} alt={art.title} loading={thumb ? 'lazy' : undefined} />;
  }
  // Art runs sandboxed: scripts allowed, but no access to this site's cookies or DOM.
  return (
    <iframe
      src={thumb ? `${art.src}?thumb=1` : art.src /* a piece can read ?thumb=1 to hide its own controls */}
      title={art.title}
      sandbox={thumb ? 'allow-scripts' : 'allow-scripts allow-pointer-lock'}
      loading={thumb ? 'lazy' : undefined}
      tabindex={thumb ? -1 : undefined}
    ></iframe>
  );
}

function Card({ art }: { art: Art }) {
  return (
    <a href={`/art/${art.slug}`} class="card">
      <div class="frame thumb">
        <Preview art={art} thumb />
      </div>
      <div class="card-label">
        <span class="tag">
          {artNo(art.no)} · {art.title}
        </span>
      </div>
      <p class="mono dim card-meta">{[art.model, art.date].filter(Boolean).join(' · ')}</p>
    </a>
  );
}

const norm = (s: string) => s.toLowerCase().trim();

// Every tag with how many arts carry it, most used first.
const tagCounts = [...arts.flatMap((a) => a.tags.map(norm)).reduce((m, t) => m.set(t, (m.get(t) ?? 0) + 1), new Map<string, number>())].sort(
  (a, b) => b[1] - a[1] || a[0].localeCompare(b[0]),
);

// Search looks at everything a visitor might type: title, summary, tags, model, agent, medium and the prompt itself.
function matchesSearch(art: Art, q: string) {
  const hay = norm([art.title, art.summary, art.model, art.agent, art.medium, art.tags.join(' '), art.prompt].join(' '));
  return q.split(/\s+/).every((word) => hay.includes(word));
}

const SECTION_SIZE = 6; // arts shown per category on the home page before "see all"

app.get('/', (c) => {
  const tag = norm(c.req.query('tag') ?? '');
  const q = norm(c.req.query('q') ?? '').slice(0, 100);
  const category = getCategory(c.req.query('category') ?? null);
  const filtering = Boolean(tag || q || category);
  const found = arts.filter(
    (a) => (!category || a.category === category.id) && (!tag || a.tags.some((t) => norm(t) === tag)) && (!q || matchesSearch(a, q)),
  );
  // The big frame: the art marked "featured": true in its art.json, else the newest piece.
  const featured = filtering ? undefined : (arts.find((a) => a.featured) ?? arts[0]);
  // Home page sections: one per category that has something in it, plus a catch-all for uncategorised arts.
  const sections = [...categories, { id: '', title: 'everything else', blurb: '' }]
    .map((cat) => ({ cat, items: arts.filter((a) => (a.category ?? '') === cat.id) }))
    .filter((s) => s.items.length > 0);
  // Links keep the other active filters, so tag + category + search combine.
  const link = (change: { tag?: string; category?: string }) => {
    const params = new URLSearchParams();
    const next = { category: category?.id ?? '', tag, ...change };
    if (next.category) params.set('category', next.category);
    if (next.tag) params.set('tag', next.tag);
    if (q) params.set('q', q);
    return (params.size ? `/?${params}` : '/') + '#browse';
  };
  return c.html(
    <Layout user={c.get('user')} path="/">
      <section class="wrap hero">
        <h1 class="pixel">one art. one prompt.</h1>
        <p class="lede">
          awesomeslop is a gallery of art made by AI agents. Every piece comes from a single prompt: read it, copy it,
          hand it to your own agent.
        </p>
        <p class="mono dim counter">
          <b>{String(arts.length).padStart(4, '0')}</b> / pieces on the wall
        </p>
      </section>

      <section class="wrap">
        {featured ? (
          <a href={`/art/${featured.slug}`} class="card featured">
            <div class="frame">
              <Preview art={featured} thumb />
            </div>
            <div class="card-label">
              <span class="tag">
                {artNo(featured.no)} · {featured.title}
              </span>
            </div>
            <p class="mono dim card-meta">
              {[featured.summary, featured.model, featured.date].filter(Boolean).join(' · ')}
            </p>
          </a>
        ) : null}

        <div class="browse" id="browse">
          <form method="get" action="/#browse" class="search" role="search">
            <span class="mono search-key" aria-hidden="true">
              /
            </span>
            <input type="search" name="q" value={q} placeholder="search titles, tags, models, prompts" aria-label="search the gallery" maxlength={100} />
            {category ? <input type="hidden" name="category" value={category.id} /> : null}
            {tag ? <input type="hidden" name="tag" value={tag} /> : null}
            <button type="submit" class="btn btn-sm">
              search
            </button>
          </form>
          <div class="chips mono">
            <span class="chips-label">category</span>
            <a href={link({ category: '' })} class={category ? 'chip' : 'chip is-on'}>
              all <span>{arts.length}</span>
            </a>
            {sections
              .filter((s) => s.cat.id)
              .map(({ cat, items }) => (
                <a href={link({ category: cat.id === category?.id ? '' : cat.id })} class={cat.id === category?.id ? 'chip is-on' : 'chip'}>
                  {cat.title} <span>{items.length}</span>
                </a>
              ))}
          </div>
          <div class="chips mono">
            <span class="chips-label">tag</span>
            {tagCounts.map(([t, n]) => (
              <a href={link({ tag: t === tag ? '' : t })} class={t === tag ? 'chip is-on' : 'chip'}>
                {t} <span>{n}</span>
              </a>
            ))}
          </div>
          {filtering ? (
            <p class="mono dim results">
              <b>{String(found.length).padStart(4, '0')}</b> / {found.length === 1 ? 'piece' : 'pieces'}
              {category ? ` in ${category.title}` : ''}
              {tag ? ` tagged "${tag}"` : ''}
              {q ? ` matching "${q}"` : ''} · <a href="/#browse">clear</a>
            </p>
          ) : null}
        </div>

        {arts.length === 0 ? <p class="mono dim empty">nothing on the wall yet. add a folder to ./arts</p> : null}
        {filtering ? (
          found.length === 0 ? (
            <p class="mono dim empty">nothing matches. try another word, tag or category.</p>
          ) : (
            <ul class="grid">
              {found.map((art) => (
                <li>
                  <Card art={art} />
                </li>
              ))}
            </ul>
          )
        ) : (
          sections.map(({ cat, items }) => (
            <section class="shelf">
              <div class="shelf-head">
                <div>
                  <h2 class="pixel">{cat.title}</h2>
                  {cat.blurb ? <p class="dim shelf-blurb">{cat.blurb}</p> : null}
                </div>
                <p class="mono dim">
                  <b>{String(items.length).padStart(4, '0')}</b>
                  {cat.id ? (
                    <>
                      {' '}
                      · <a href={link({ category: cat.id })}>see all</a>
                    </>
                  ) : null}
                </p>
              </div>
              <ul class="grid">
                {items.slice(0, SECTION_SIZE).map((art) => (
                  <li>
                    <Card art={art} />
                  </li>
                ))}
              </ul>
            </section>
          ))
        )}
      </section>

      <section class="wrap cta">
        <h2 class="pixel">show your art here.</h2>
        <p class="lede">
          Right now this is a one-person gallery. If you make art with prompts and want a wall of your own, leave a
          link to your work.
        </p>
        <a href="/waitlist" class="btn btn-lg btn-accent">
          join the waitlist
        </a>
      </section>
    </Layout>,
  );
});

// ---------- one art ----------

// Arts that were renamed: old links keep working.
const MOVED: Record<string, string> = { '007-washing-day': '007-pencil-town' };
app.get('/art/:slug{.*}', async (c, next) => {
  const [slug, ...rest] = c.req.param('slug').split('/');
  const to = MOVED[slug];
  return to ? c.redirect(['/art', to, ...rest].join('/'), 301) : next();
});

app.get('/art/:slug/prompt.md', (c) => {
  const art = getArt(c.req.param('slug'));
  if (!art) return c.notFound();
  return c.body(art.prompt + '\n', 200, { 'content-type': 'text/markdown; charset=utf-8' });
});

app.get('/art/:slug', (c) => {
  const art = getArt(c.req.param('slug'));
  if (!art) return c.notFound();
  const category = getCategory(art.category);
  const specs: [string, string | null][] = [
    ['model', art.model],
    ['agent', art.agent],
    ['medium', art.medium],
    ['made', art.date],
    ...Object.entries(art.specs),
  ];
  return c.html(
    <Layout user={c.get('user')} path="/art" title={art.title} description={art.summary}>
      <article class="wrap art">
        <p class="mono dim crumbs">
          <a href="/">awesomeslop</a> /{' '}
          {category ? (
            <>
              <a href={`/?category=${category.id}#browse`}>{category.title}</a> /{' '}
            </>
          ) : null}
          {artNo(art.no)}
        </p>

        <div class="frame stage" id="stage">
          <Preview art={art} />
        </div>

        <div class="art-head">
          <div>
            <h1 class="pixel">{art.title}</h1>
            {art.summary ? <p class="lede">{art.summary}</p> : null}
          </div>
          <div class="actions">
            {/* Fullscreens the stage in place (the running iframe keeps its state); falls back to opening the piece itself. */}
            <a href={art.src} target="_blank" rel="noopener" class="btn btn-lg btn-accent" data-play="#stage">
              ▶ {art.category === 'game-scenes' ? 'play the game' : art.kind === 'image' ? 'view fullscreen' : 'play fullscreen'}
            </a>
            <button type="button" class="btn btn-lg" data-copy="#prompt-text" data-copied="copied. paste it to your agent">
              copy prompt for your agent
            </button>
            <a href={claudeBreakdownUrl(art)} target="_blank" rel="noopener" class="btn btn-lg">
              ask claude to break it down ↗
            </a>
            <p class="mono dim hint">
              the second button opens claude.ai with the prompt and a "break this down" question prefilled.
            </p>
          </div>
        </div>

        <div class="cols">
          <section class="readme">
            <h2 class="mono label">readme.md</h2>
            {art.readmeHtml ? (
              <div class="prose" dangerouslySetInnerHTML={{ __html: art.readmeHtml }} />
            ) : (
              <p class="mono dim">no readme for this one.</p>
            )}
          </section>

          <aside class="side">
            <section>
              <h2 class="mono label">specs</h2>
              <dl class="specs mono">
                {specs
                  .filter(([, v]) => v)
                  .map(([k, v]) => (
                    <div>
                      <dt>{k}</dt>
                      <dd>{v}</dd>
                    </div>
                  ))}
                {category ? (
                  <div>
                    <dt>category</dt>
                    <dd class="tag-links">
                      <a href={`/?category=${category.id}#browse`} class="chip">
                        {category.title}
                      </a>
                    </dd>
                  </div>
                ) : null}
                {art.tags.length ? (
                  <div>
                    <dt>tags</dt>
                    <dd class="tag-links">
                      {art.tags.map((t) => (
                        <a href={`/?tag=${encodeURIComponent(norm(t))}#browse`} class="chip">
                          {t}
                        </a>
                      ))}
                    </dd>
                  </div>
                ) : null}
              </dl>
            </section>

            <section>
              <div class="prompt-bar">
                <h2 class="mono label">prompt.md</h2>
                <span class="mono dim">
                  {art.prompt.length.toLocaleString('en-US')} chars ·{' '}
                  <a href={`/art/${art.slug}/prompt.md`}>raw</a> ·{' '}
                  <button type="button" class="link" data-copy="#prompt-text" data-copied="copied">
                    copy
                  </button>
                </span>
              </div>
              <pre class="prompt mono" id="prompt-text">
                {art.prompt}
              </pre>
            </section>

            {art.kind === 'live' ? (
              <a href={art.src} target="_blank" rel="noopener" class="btn btn-ghost">
                open the piece in a new tab ↗
              </a>
            ) : null}
          </aside>
        </div>
      </article>
    </Layout>,
  );
});

// ---------- waitlist ----------

function parseArtUrl(input: string): string | null {
  let value = input.trim();
  if (!value || value.length > 500) return null;
  if (!/^https?:\/\//i.test(value)) value = `https://${value}`;
  try {
    const url = new URL(value);
    if (!['http:', 'https:'].includes(url.protocol) || !url.hostname.includes('.')) return null;
    return url.toString();
  } catch {
    return null;
  }
}

app.get('/waitlist', async (c) => {
  const user = c.get('user');
  const entry = user
    ? await c.env.DB.prepare('SELECT art_url FROM waitlist WHERE user_id = ?').bind(user.id).first<{ art_url: string }>()
    : null;
  const saved = c.req.query('saved') === '1';
  const error = c.req.query('error') === '1';
  return c.html(
    <Layout user={user} path="/waitlist" title="waitlist">
      <section class="wrap narrow waitlist">
        <p class="mono dim crumbs">
          <a href="/">awesomeslop</a> / waitlist
        </p>
        <h1 class="pixel">show your art here.</h1>
        <p class="lede">
          awesomeslop will open up to other artists. One question to get on the list: where can I see your art?
        </p>

        {!user ? (
          <div class="panel">
            <p class="mono dim step">step 1 / 2 · who are you</p>
            <a href="/auth/google?next=/waitlist" class="btn btn-lg">
              <span class="g" aria-hidden="true">
                G
              </span>
              sign in with google
            </a>
            <p class="mono dim hint">only your name and email are read. nothing is posted anywhere.</p>
          </div>
        ) : (
          <form method="post" action="/waitlist" class="panel">
            <p class="mono dim step">
              step 2 / 2 · signed in as {user.email}
            </p>
            {saved ? <p class="note ok mono">you're on the list. you can update the link any time.</p> : null}
            {error ? <p class="note err mono">that doesn't look like a link. try something like https://your.site</p> : null}
            <label for="art_url">link where I can see your art</label>
            <input
              id="art_url"
              name="art_url"
              type="text"
              inputmode="url"
              required
              maxlength={500}
              placeholder="https://"
              value={entry?.art_url ?? ''}
              autocomplete="url"
            />
            <button type="submit" class="btn btn-lg btn-accent">
              {entry ? 'update my link' : 'join the waitlist'}
            </button>
          </form>
        )}
      </section>
    </Layout>,
  );
});

app.post('/waitlist', async (c) => {
  const user = c.get('user');
  if (!user) return c.redirect('/waitlist');
  const body = await c.req.parseBody();
  const artUrl = parseArtUrl(typeof body.art_url === 'string' ? body.art_url : '');
  if (!artUrl) return c.redirect('/waitlist?error=1');
  await c.env.DB.prepare(
    `INSERT INTO waitlist (user_id, art_url) VALUES (?1, ?2)
     ON CONFLICT(user_id) DO UPDATE SET art_url = ?2, updated_at = datetime('now')`,
  )
    .bind(user.id, artUrl)
    .run();
  return c.redirect('/waitlist?saved=1');
});

// ---------- admin: who is on the waitlist ----------

app.get('/admin', async (c) => {
  const user = c.get('user');
  if (!isAdmin(c, user)) return c.notFound();
  const { results } = await c.env.DB.prepare(
    `SELECT u.name, u.email, w.art_url, w.created_at
     FROM waitlist w JOIN users u ON u.id = w.user_id
     ORDER BY w.created_at DESC`,
  ).all<{ name: string | null; email: string; art_url: string; created_at: string }>();
  return c.html(
    <Layout user={user} path="/admin" title="admin">
      <section class="wrap">
        <p class="mono dim crumbs">
          <a href="/">awesomeslop</a> / admin
        </p>
        <h1 class="pixel">waitlist.</h1>
        <p class="mono dim counter">
          <b>{String(results.length).padStart(4, '0')}</b> / people waiting
        </p>
        {results.length === 0 ? (
          <p class="mono dim empty">nobody yet.</p>
        ) : (
          <div class="table-scroll">
            <table class="table mono">
              <thead>
                <tr>
                  <th>joined</th>
                  <th>name</th>
                  <th>email</th>
                  <th>art link</th>
                </tr>
              </thead>
              <tbody>
                {results.map((r) => (
                  <tr>
                    <td class="dim">{r.created_at.slice(0, 10)}</td>
                    <td>{r.name ?? '-'}</td>
                    <td>{r.email}</td>
                    <td>
                      <a href={r.art_url} target="_blank" rel="noopener noreferrer nofollow">
                        {r.art_url}
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </Layout>,
  );
});

// ---------- fallbacks ----------

app.notFound((c) =>
  c.html(
    <Layout user={c.get('user') ?? null} path="" title="404">
      <section class="wrap narrow waitlist">
        <p class="mono dim crumbs">error / 404</p>
        <h1 class="pixel">nothing hangs here.</h1>
        <a href="/" class="btn btn-lg">
          back to the gallery
        </a>
      </section>
    </Layout>,
    404,
  ),
);

app.onError((err, c) => {
  // Deliberate HTTP errors (e.g. the 403 from the cross-site form check) keep their own status.
  if ('getResponse' in err) return err.getResponse();
  console.error(err);
  return c.text('Something broke on our side. Try again in a moment.', 500);
});

export default app;
