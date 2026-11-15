import { html } from 'hono/html';
import type { Child } from 'hono/jsx';
import { REPO_URL, formatStars, starCount } from './stars';
import type { User } from './types';

type Props = { title?: string; description?: string; user: User | null; path: string; children?: Child };

export function Layout({ title, description, user, path, children }: Props) {
  const fullTitle = title ? `${title} · awesomeslop` : 'awesomeslop · one art, one prompt';
  const nav = (href: string, label: string) => (
    <a href={href} class={path === href ? 'nav-link is-active' : 'nav-link'}>
      {label}
    </a>
  );
  const stars = starCount();
  return html`<!doctype html>${(
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{fullTitle}</title>
        <meta name="description" content={description ?? 'A gallery of art made by AI agents. One art, one prompt.'} />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Funnel+Sans:wght@400;500;600&family=Pixelify+Sans:wght@400;500&family=Red+Hat+Mono:wght@400;500&display=swap"
        />
        <link rel="stylesheet" href="/styles.css" />
        <script src="/app.js" defer></script>
      </head>
      <body>
        <header class="site-header">
          <div class="wrap bar">
            <a href="/" class="logo">
              <span class="logo-mark" aria-hidden="true"></span>awesomeslop
            </a>
            <nav class="nav">
              {nav('/', 'gallery')}
              <a href={REPO_URL} class="nav-link nav-gh" target="_blank" rel="noopener" title="star awesomeslop on github">
                <span class="star" aria-hidden="true">
                  ★
                </span>{' '}
                star{stars ? <span class="mono star-count">{formatStars(stars)}</span> : null}
              </a>
              {user?.admin ? nav('/admin', 'admin') : null}
              {user ? (
                <form method="post" action="/auth/signout" class="nav-user">
                  <span class="mono dim nav-email">{user.email}</span>
                  <button type="submit" class="nav-link">sign out</button>
                </form>
              ) : null}
              <a href="/waitlist" class="btn btn-sm">
                join waitlist
              </a>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer class="site-footer">
          <div class="wrap bar mono dim">
            <span>awesomeslop / one art, one prompt</span>
            <span class="foot-links">
              <a href={REPO_URL} target="_blank" rel="noopener">
                ★ star on github
              </a>
              <a href="/waitlist">waitlist</a>
            </span>
          </div>
        </footer>
      </body>
    </html>
  )}`;
}
