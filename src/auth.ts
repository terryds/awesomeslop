import { Hono, type Context } from 'hono';
import { deleteCookie, getCookie, getSignedCookie, setCookie, setSignedCookie } from 'hono/cookie';
import type { AppEnv, User } from './types';

const SESSION = 'ah_session';
const OAUTH = 'ah_oauth';
const THIRTY_DAYS = 60 * 60 * 24 * 30;

type Ctx = Context<AppEnv>;

const isHttps = (c: Ctx) => new URL(c.req.url).protocol === 'https:';
const isLocalhost = (c: Ctx) => ['localhost', '127.0.0.1', '[::1]'].includes(new URL(c.req.url).hostname);
const devLoginAllowed = (c: Ctx) => c.env.DEV_LOGIN === '1' && isLocalhost(c);

// Only ever redirect back to a path on this site.
const safeNext = (next?: string) => (next && next.startsWith('/') && !next.startsWith('//') ? next : '/');

function secret(c: Ctx) {
  if (!c.env.SESSION_SECRET) throw new Error('SESSION_SECRET is not set');
  return c.env.SESSION_SECRET;
}

export async function currentUser(c: Ctx): Promise<User | null> {
  if (!getCookie(c, SESSION)) return null;
  const raw = await getSignedCookie(c, secret(c), SESSION);
  if (!raw) return null;
  try {
    const { id, email, name, picture } = JSON.parse(raw) as User;
    return { id, email, name, picture };
  } catch {
    return null;
  }
}

export function isAdmin(c: Ctx, user: User | null) {
  if (!user) return false;
  const admins = (c.env.ADMIN_EMAILS ?? '').split(',').map((e) => e.trim().toLowerCase()).filter(Boolean);
  return admins.includes(user.email.toLowerCase());
}

async function signIn(c: Ctx, user: User) {
  await c.env.DB.prepare(
    `INSERT INTO users (id, email, name, picture) VALUES (?1, ?2, ?3, ?4)
     ON CONFLICT(id) DO UPDATE SET email = ?2, name = ?3, picture = ?4`,
  )
    .bind(user.id, user.email, user.name, user.picture)
    .run();
  await setSignedCookie(c, SESSION, JSON.stringify(user), secret(c), {
    path: '/',
    httpOnly: true,
    secure: isHttps(c),
    sameSite: 'Lax',
    maxAge: THIRTY_DAYS,
  });
}

export const auth = new Hono<AppEnv>();

auth.get('/google', (c) => {
  const next = safeNext(c.req.query('next'));
  if (!c.env.GOOGLE_CLIENT_ID || !c.env.GOOGLE_CLIENT_SECRET) {
    if (devLoginAllowed(c)) return c.redirect(`/auth/dev?next=${encodeURIComponent(next)}`);
    return c.text('Google sign-in is not configured yet: set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.', 503);
  }
  const state = crypto.randomUUID();
  setCookie(c, OAUTH, JSON.stringify({ state, next }), {
    path: '/auth',
    httpOnly: true,
    secure: isHttps(c),
    sameSite: 'Lax',
    maxAge: 600,
  });
  const url = new URL('https://accounts.google.com/o/oauth2/v2/auth');
  url.search = new URLSearchParams({
    client_id: c.env.GOOGLE_CLIENT_ID,
    redirect_uri: new URL('/auth/google/callback', c.req.url).toString(),
    response_type: 'code',
    scope: 'openid email profile',
    state,
    prompt: 'select_account',
  }).toString();
  return c.redirect(url.toString());
});

auth.get('/google/callback', async (c) => {
  let saved: { state?: string; next?: string } = {};
  try {
    saved = JSON.parse(getCookie(c, OAUTH) ?? '{}');
  } catch {}
  deleteCookie(c, OAUTH, { path: '/auth' });

  const code = c.req.query('code');
  if (!code || !saved.state || saved.state !== c.req.query('state')) {
    return c.text('Sign-in failed or was cancelled. Go back and try again.', 400);
  }

  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code,
      client_id: c.env.GOOGLE_CLIENT_ID!,
      client_secret: c.env.GOOGLE_CLIENT_SECRET!,
      redirect_uri: new URL('/auth/google/callback', c.req.url).toString(),
      grant_type: 'authorization_code',
    }),
  });
  if (!tokenRes.ok) {
    console.error('google token exchange failed', tokenRes.status, await tokenRes.text());
    return c.text('Google rejected the sign-in. Try again.', 502);
  }
  const { access_token } = (await tokenRes.json()) as { access_token: string };

  const infoRes = await fetch('https://openidconnect.googleapis.com/v1/userinfo', {
    headers: { authorization: `Bearer ${access_token}` },
  });
  if (!infoRes.ok) return c.text('Could not read your Google profile. Try again.', 502);
  const info = (await infoRes.json()) as {
    sub: string;
    email?: string;
    email_verified?: boolean;
    name?: string;
    picture?: string;
  };
  if (!info.email || !info.email_verified) return c.text('Your Google account needs a verified email.', 403);

  await signIn(c, { id: info.sub, email: info.email, name: info.name ?? null, picture: info.picture ?? null });
  return c.redirect(safeNext(saved.next));
});

// Local development only: sign in without Google. Needs DEV_LOGIN=1 and a localhost URL.
auth.get('/dev', async (c) => {
  if (!devLoginAllowed(c)) return c.notFound();
  await signIn(c, { id: 'dev-user', email: 'dev@localhost', name: 'Dev User', picture: null });
  return c.redirect(safeNext(c.req.query('next')));
});

auth.post('/signout', (c) => {
  deleteCookie(c, SESSION, { path: '/' });
  return c.redirect('/');
});
