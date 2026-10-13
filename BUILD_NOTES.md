# logralee.com — build notes for the owner

Static site + one Cloudflare Pages Function. No framework, no webfonts. Every page opens straight from Finder
(`file://`) as well as from a server: all paths are relative, and the icon sprite is inlined.

```
index.html               the page (generated from index.src.html — edit the .src, run tools/build_index.py)
index.src.html           hand-written source with three placeholders ({{WM}} {{WALL}} {{COVERS}})
features/ privacy/ terms/ support/ press/ joined/   secondary pages (generated from tools/pages/*.html)
404.html
assets/css/site.css      tokens as CSS custom properties, all layout and motion
assets/js/site.js        4.5 KB vanilla: try-it tile, coaching switch, waitlist fetch, menu, picker replay
assets/img/              AVIF + WebP (+ JPEG for cover cards), two sizes each; icons; og.jpg
assets/icons/sprite.svg  the eight activity icons + wordmark (C2PA metadata stripped: 90 KB → 31 KB); inlined into index.html by the build script
assets/icons/wordmark.svg  "Logralee" in Quicksand Bold as outlines (3.9 KB) — no font file shipped
functions/api/waitlist.ts  POST /api/waitlist → D1
schema.sql  wrangler.toml  _redirects  _headers  robots.txt  sitemap.xml  favicon.ico
tools/build_index.py     rebuild index.html
tools/pages.py           rebuild the secondary pages (shared nav/footer live here)
tools/check.py           overflow at 13 widths, weight budget, screenshots (needs playwright)
```

## 1. First deploy (Cloudflare Pages)

1. Push this repo to GitHub (`gonzalezosv/logralee`).
2. Cloudflare dashboard → Workers & Pages → Create → Pages → connect the repo.
   Framework preset: **None**. Build command: *(empty)*. Build output directory: **/** (repo root).
3. Custom domains: add **logralee.com** (and `www.logralee.com` → redirect to apex).
   For **logralee.app** add a Redirect Rule (or Bulk Redirect) on that zone: `https://logralee.app/*` → `https://logralee.com/$1`, 301.
4. Retire GitHub Pages for this repo (Settings → Pages → None) once DNS is live. `_redirects` already maps `/logralee/*` paths.

## 2. Waitlist database (D1)

```bash
npm i -g wrangler && wrangler login
wrangler d1 create logralee-waitlist          # copy the database_id it prints
# paste it into wrangler.toml → [[d1_databases]] database_id
wrangler d1 execute logralee-waitlist --remote --file=./schema.sql
wrangler pages secret put IP_SALT             # any long random string; used only to hash IPs for rate limiting
```

In the Pages project settings → Functions → D1 database bindings: confirm **DB → logralee-waitlist** is bound
(Pages reads `wrangler.toml` on deploy; if the binding doesn't appear, add it in the dashboard).

Local preview without the waitlist: just open `index.html`. With the waitlist:

```bash
wrangler d1 execute logralee-waitlist --local --file=./schema.sql
wrangler pages dev . --port 8788
curl -H 'Accept: application/json' -d 'email=you@example.com' http://localhost:8788/api/waitlist
# {"ok":true}   second time → {"ok":true,"already":true}
```

Export for the launch email:

```bash
wrangler d1 execute logralee-waitlist --remote --json \
  --command "SELECT email, datetime(created_at,'unixepoch') AS joined, source FROM waitlist ORDER BY id" > waitlist.json
```

Behaviour: validates and lower-cases, `UNIQUE(email)` de-dupes, honeypot field `website` (bots get a fake 200),
**5 sign-ups per IP per hour** (`RATE_LIMIT_PER_HOUR` in `wrangler.toml`), IPs stored only as a salted hash for 24 h.
With JavaScript off the form posts normally and lands on `/joined/`.
If spam shows up anyway: add Cloudflare Turnstile (a widget in the form + a server-side verify in the function).

## 3. Launch day: flip to store badges

One attribute on `<html>` in `index.html` **and** `index.src.html`, and in `tools/pages.py` (HEAD template):

```html
<html lang="en" data-mode="prelaunch">   →   <html lang="en" data-mode="launched">
```

Then, in `index.html` / `index.src.html`:
- replace `APP_STORE_ID` and `PLAY_PACKAGE_ID` in the two badge links,
- un-comment the Apple Smart App Banner meta tag and fill the id,
- drop the **official** badges into `assets/img/badge-appstore.svg` and `assets/img/badge-play.svg`
  (Apple: developer.apple.com/app-store/marketing/guidelines — Google: play.google.com/intl/en_us/badges).
  The placeholder pills in there now are plain text, on purpose.
- `tools/build_index.py && python3 tools/pages.py`, commit, push. Pages deploys in about a minute.

The waitlist forms, "Coming this December" line and "Join waitlist" nav pill hide themselves; badges and
"Get the app" appear. The `/api/waitlist` function keeps working if anyone has an old tab open.

## 4. Asset slots to fill before launch

| Slot | File(s) | Now |
|---|---|---|
| Hero phones (3) | `assets/img/hero-home-*`, `hero-routines-*`, `hero-yoga-*` | Real captures from Oct 13, Cotton Candy; Home shows the demo name "Maya", the routines capture shows a body-weight card. Replace with demo-account captures (1125×2436, status bar cropped: top 5.5 %). |
| Hero note / launch date | `index.src.html` | "Coming this December to iPhone and Android. Free." |
| Store ids | `index.src.html` | `APP_STORE_ID`, `PLAY_PACKAGE_ID` |
| Contact emails | `tools/pages/*.html` | `support@logralee.com`, `press@logralee.com` — confirm or change |
| Press screenshots | `tools/pages/press.html` | "coming with the launch build" |
| Legal review | `/privacy/`, `/terms/` | Drafts match the app (on-device, no account, no analytics). Yellow callouts mark what a lawyer should read. |

To regenerate the images from new captures, the sizes used are: hero centre 560/1120 w, sides 460/920 w, covers 480/960 w,
plan thumbs 160 w, pose/how-to 560/1120 w. AVIF quality ~50, WebP ~72. Keep `width`/`height` attributes in sync.

## 5. Checks before each deploy

```bash
pip install playwright && python3 -m playwright install chromium   # once
wrangler pages dev . --port 8788 &
python3 tools/check.py http://localhost:8788
```

Fails loudly on any horizontal overflow at 320–1440 px on every page, or if the first view (excluding images) passes 150 KB.
Current: ~100 KB uncompressed before images (Cloudflare serves it brotli-compressed, roughly a third of that); hero images ~85 KB.
Lighthouse (mobile) is the final gate: aim Performance ≥ 95, Accessibility 100, Best Practices ≥ 95, SEO 100.

## 6. Editing content

- Home page copy: `index.src.html` → `python3 tools/build_index.py`.
- Routine cards: the `COVERS` list in `tools/build_index.py` (drop a new cover into `assets/img/` at 480 and 960 wide as AVIF/WebP/JPEG).
- Any secondary page: `tools/pages/<slug>.html` → `python3 tools/pages.py`. Nav and footer for those pages are in `pages.py`.
- Every number on the site (110 / 26 / 251 / 45) traces to `docs/APP_FEATURES.md`. Re-verify against the catalog before launch.
- Voice gate: short sentences, present tense, no guilt, no streak pressure, no "crush"/"beast mode".

## 7. Known decisions

- Picker wheel plays twice on load then rests on the wordmark; tap it to replay once. Reduced-motion users see the wordmark only.
- Phone nav collapses behind a menu below 900 px (so the link row never crowds the CTA on tablets).
- The hero trio scales with the viewport between 735 and 1068 px so it never clips.
- `html { overflow-x: clip }` is a guard, not a fix; `tools/check.py` is what proves there's nothing to clip.
- CSP in `_headers` allows inline styles/scripts (the page has a few inline `style=` attributes and the JSON-LD block). Tighten if you remove them.
