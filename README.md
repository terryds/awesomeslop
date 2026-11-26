# awesomeslop

A gallery of art made by AI agents. One art, one prompt.

Live at [awesomeslop.terrydjony.com](https://awesomeslop.terrydjony.com). If a prompt here is useful to you, a ★ on this repo helps other people find it.

Cloudflare Worker (Hono, server-rendered JSX) + D1 for the waitlist. Arts are plain folders in this repo.

## run it

```bash
npm install
cp .dev.vars.example .dev.vars   # then set SESSION_SECRET to any long random string
npm run db:local                 # creates the local waitlist database
npm run dev                      # http://localhost:8787
```

With `DEV_LOGIN=1` in `.dev.vars`, "sign in with google" signs you in as `dev@localhost` on localhost, so you can
try the waitlist before setting up Google.

## add an art

Create a folder in `arts/`. The folder name is the URL (`arts/004-my-piece` -> `/art/004-my-piece`).

| file         | what                                                                  |
| ------------ | --------------------------------------------------------------------- |
| `art.json`   | title, category, date, model, agent, medium, tags, summary, extra `specs` |
| `prompt.md`  | the one prompt that made it                                           |
| `README.md`  | notes about the piece (markdown)                                      |
| `index.html` | the piece itself, if it is a live/animated one                        |
| a video      | for clips made by a video model (Veo, Sora…): name the file in `"video"`, plus a `"cover"` still; the page plays it directly and `agent` can be left out |
| an image     | for image art: put the file in the folder and name it in `"cover"`    |

```json
{
  "title": "my piece",
  "category": "art-styles",
  "date": "2026-11-12",
  "summary": "One line shown under the title.",
  "model": "Claude Fable 5.2",
  "agent": "Claude Code",
  "medium": "html canvas, single file",
  "tags": ["generative"],
  "specs": { "attempts": "1", "anything": "you want in the spec sheet" },
  "cover": "cover.png"
}
```

`category` is one of the ids in [arts/categories.json](arts/categories.json). Each category with at least one art
gets its own section on the home page, in the order of that file; add a new one there (id, title, blurb) before
using it. Tags are free-form.

`cover` is required for image art. A live piece should have one too: the gallery shows the cover on its card and
only runs the piece while the card is hovered, so the home page does not run every piece at once. Without a cover
the card runs the piece all the time. `node scripts/make-cover.mjs` takes a screenshot of every live piece that has
no cover yet, saves it as `cover.webp` and names it in `art.json` (needs Google Chrome; add `arts/<slug> <seconds>`
to retake one at a better moment).
The newest art gets the big frame on the home page, unless one art has `"featured": true` in its art.json; then that one does. Gallery previews load a live piece with `?thumb=1`, so a
piece with on-screen instructions can hide them there. `"draft": true` hides an art. The dev server picks up changes in `arts/` on its own.

## google sign-in

1. Google Cloud console > Google Auth Platform > Clients > Create client > Web application. Any project works,
   including one you already use for another site: a project can hold many clients. Note that the consent screen
   name and logo (Branding) are shared by every client in the project.
2. Authorized redirect URIs: `http://localhost:8787/auth/google/callback` and `https://<your-domain>/auth/google/callback`.
3. Put the client id and secret in `.dev.vars` (local) and in Worker secrets (production, below).

## deploy

Live at https://awesomeslop.terrydjony.com (custom domain and D1 database id are in `wrangler.jsonc`).

```bash
npm run deploy                         # build content + upload; this is all you need after adding an art
npm run db:remote                      # only after adding a file to migrations/
npx wrangler secret put ADMIN_EMAILS   # comma-separated; these accounts can open /admin
```

Pushes to `main` deploy automatically (Workers Builds). Every pull request gets a preview at
`https://<branch-name>-awesomeslop.terrydjony.workers.dev`; Cloudflare posts the link as a comment on the PR.
Previews use their own database (`awesomeslop-preview`), never the real waitlist, and have no Google sign-in.
Preview links are public to anyone who has the URL.

Already set in production: `SESSION_SECRET`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`. `DEV_LOGIN` is not set there
(and is ignored off localhost anyway).

## routes

- `/` gallery, in sections by category. `/?category=game-scenes`, `/?tag=3d` and `/?q=lighthouse` filter it, and combine
- `/art/:slug` one art: the piece, readme, spec sheet, prompt, copy button, "ask claude" button
- `/art/:slug/prompt.md` the raw prompt as plain text
- `/waitlist` Google sign-in, then one field: the link to your art
- `/admin` waitlist entries (only for `ADMIN_EMAILS`)
