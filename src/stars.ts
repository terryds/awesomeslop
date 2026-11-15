// GitHub star count for the "star" links. Looked up at most once an hour: the answer is kept in this isolate's
// memory and in the edge cache, so page views never wait on GitHub. If GitHub is slow, rate-limited or down,
// the links simply show no number.

export const REPO = 'terryds/awesomeslop';
export const REPO_URL = `https://github.com/${REPO}`;

const TTL = 3600; // seconds a good answer is kept
const RETRY = 300; // seconds before asking again after a failure
const CACHE_KEY = `https://stars.internal/${REPO}`;

let memo: { count: number | null; until: number } | null = null;

/** The last known star count, or null when it is unknown. Never waits. */
export const starCount = () => memo?.count ?? null;

/** 1234 -> "1.2k" */
export const formatStars = (n: number) => (n < 1000 ? String(n) : `${(n / 1000).toFixed(1).replace(/\.0$/, '')}k`);

/** Makes sure starCount() is fresh. Cheap to call on every request. */
export async function refreshStars(): Promise<void> {
  if (memo && memo.until > Date.now()) return;
  const remember = (count: number | null, seconds: number) => {
    memo = { count, until: Date.now() + seconds * 1000 };
  };
  try {
    const cache = caches.default;
    const hit = await cache.match(CACHE_KEY);
    if (hit) return remember(Number(await hit.text()), TTL);

    const res = await fetch(`https://api.github.com/repos/${REPO}`, {
      headers: { accept: 'application/vnd.github+json', 'user-agent': 'awesomeslop-site' },
      signal: AbortSignal.timeout(1500),
    });
    if (!res.ok) throw new Error(`github ${res.status}`);
    const { stargazers_count: count } = await res.json<{ stargazers_count: number }>();
    if (typeof count !== 'number') throw new Error('no star count in reply');
    remember(count, TTL);
    await cache.put(CACHE_KEY, new Response(String(count), { headers: { 'cache-control': `max-age=${TTL}` } }));
  } catch {
    remember(memo?.count ?? null, RETRY); // keep the old number if there is one
  }
}
