# logralee.com — design spec

> The direction the owner approved on 2026-10-13 after five mock rounds: **E2 · Apple-style, picker wheel**.
> Reference mock: `docs/mock/index.html` (a static render of the approved artboard; placeholders are marked `[like this]`).
> Feature facts come from `docs/APP_FEATURES.md`. Never claim anything that file doesn't support.

---

## 1. What this site must do

1. Make people **want to use the app**: show the app working, not just describe it.
2. Collect **real** waitlist sign-ups now, and switch to App Store / Play links on launch day with a one-line change.
3. Host the **Privacy, Terms and Support** pages App Store Connect and Play Console need.
4. Load fast on a phone. The owner comes from Game Boy/PSP/DS development: no bloat, no slowdowns.

## 2. Direction: what was decided and why

- **Apple product-page style.** Big confident type, generous space, alternating white / light-grey / black sections, a "Get the highlights" tile grid, then "Take a closer look" feature sections. It reads as premium and well thought out.
- **Green is the logo's colour, not the page's.** Round 1 used forest green as the page background and the owner rejected it as overbearing. Green appears only in the logo mark and the activity icons.
- **The app brings the colour.** UI drawings and phone screens use the app's default theme, Cotton Candy (`#BE58E2` on `#F7EFFB`). Buttons and text are near-black.
- **App design principles on the web.** Interactive moments borrowed from the app (tap a circle to log a set, a segmented coaching switch, notification-style cards with the app's voice, a Lock Screen Live Activity) so visitors get a feel for using it.
- **No "lograr · to achieve" label.** The meaning is told by the picker wheel (§5.2).

## 3. Page structure (single page, top to bottom)

| # | Section | Background | Content |
|---|---|---|---|
| 0 | Sticky nav | frosted white | Logo mark + "Logralee" · Highlights · Coaching · Guided · Moments · Privacy · **Join waitlist** pill |
| 1 | Hero | white | Picker wheel → H1 "A journal for every way you move." → sub → email form → "Coming this December to iPhone and Android." → three phones rising from the bottom edge (Lavender, Cotton Candy centre, Terracotta) |
| 2 | Get the highlights | `#F5F5F7` | 6 tiles: **Try it** (tap to log a set, interactive) · Eight activities (icons) · Routines and plans (110 / 26) · Journal *(replaces the Moments tile, which duplicated §7)* · Privacy (lock) · Themes (7 swatches) |
| 3 | "Take a closer look." | white | Section heading |
| 4 | Coaching engine | white | "A coach that pays attention." + three coach cards (warm-up, beat last time, longer rest with mini ring) + Off / Minimal / Full segmented switch whose line changes (interactive) |
| 5 | Guided sessions | `#F5F5F7` | "See the move before you make it." Yoga player card with **3D figure render**, pose, muscles, timer, Hide guide. Stats: 251 exercises · 45 muscles mapped |
| 6 | Live Activity | black | "Your workout, right on your Lock Screen." iPhone Lock Screen with the Live Activity card |
| 7 | My Progress | `#F5F5F7` | "See how far you've come." Card: "+N lb added since …" headline and start → now bars |
| 8 | Moments | black | "Your lift. Your photo. Your numbers." Phone with photo + glass stat card (date, lift, weight, PR chip, second activity, logo). Four cards: Save it · Share to Stories · Save the overlay (checkerboard thumbnail) · Filters and layouts |
| 9 | Weight | white | "The trend, not the daily noise." Card: today's weight, monthly change, trend line over daily dots, Week avg / Goal / To go |
| 10 | Up next | `#F5F5F7` | "Lift, then stretch." Chest Day (done) → Hip Mobility (Up next, Start) |
| 11 | Voice | white | "A training partner, not a drill sergeant." + three notification-style cards in the app's voice |
| 12 | Closing CTA | black | Logo mark (cream) · "Achieve it. Starting with the first log." · email form · "iPhone and Android · Free to download" |
| 13 | Footer | `#F5F5F7` | © 2026 Bit Ray Technologies · Privacy · Terms · Support · Press kit |

Other pages: `/privacy`, `/terms`, `/support`, `/press` (same nav/footer, simple text layout, max-width ~720px).

## 4. Tokens

**Colour**

| Token | Value | Use |
|---|---|---|
| `--bg` | `#FFFFFF` | Page |
| `--bg-alt` | `#F5F5F7` | Alternating sections, tiles |
| `--bg-dark` | `#000000` | Live Activity, Moments, closing CTA |
| `--surface-dark` | `#1D1D1F` | Cards on black |
| `--text` | `#1D1D1F` | Body and headings |
| `--text-2` | `#6E6E73` | Secondary (passes 4.5:1 on white and `#F5F5F7`) |
| `--text-3` | `#86868B` | Captions ≥14px only |
| `--text-on-dark-2` | `#A1A1A6` | Secondary on black |
| `--line` | `#D2D2D7` | Inputs, dividers |
| `--app` | `#BE58E2` | Cotton Candy primary: UI drawings only (bars, rings, "UP NEXT") |
| `--app-tint` | `#F7EFFB` | Cotton Candy canvas: phone screens, icon wells |
| `--brand` | `#2F462C` | Logo mark on light |
| `--brand-icon` | `#4F6E4A` | Activity icons |
| `--brand-cream` | `#F3EFE4` | Logo mark on dark |
| `--pr` | `#F5C542` on `#3A2A00` text | PR chip |

**Type**: system stack, no webfont download (SF Pro on Apple devices, Roboto/Segoe elsewhere):
`-apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", system-ui, sans-serif`

| Role | Size | Weight | Tracking |
|---|---|---|---|
| H1 | `clamp(44px, 6.6vw, 86px)` / 1.04 | 700 | −0.035em |
| Section H2 | `clamp(36px, 4.6vw, 56px)` / 1.05 | 700 | −0.035em |
| Feature H2 (Coaching, Moments) | `clamp(40px, 5.6vw, 72px)` / 1.02 | 700 | −0.04em |
| Tile H3 | 28px / 1.1 | 700 | −0.025em |
| Lead paragraph | 21px / 1.38 | 400 | |
| Body | 17px / 1.47 | 400 | −0.01em |
| Eyebrow | 17px (sections) / 14px (tiles) | 600 | |

**Shape**: tiles and cards 28px radius; small cards 22px; pills 999px; inputs 12px. Shadows soft and rare (`0 16–20px 40–50px rgba(0,0,0,.06–.08)`).

**Space**: sections 112–120px vertical on desktop, 72–80px on phone; content max-width 1024px; side gutter 22px (16px minimum at phone width).

## 5. Components

### 5.1 Nav
Sticky, 44–52px tall, `rgba(255,255,255,.8)` + `backdrop-filter: saturate(180%) blur(20px)`, 1px bottom border. On phone: logo + "Join waitlist" pill visible; section links collapse behind a menu button (Apple-style full-width dropdown) or a horizontally scrollable row. Decide in the build; no layout shift.

### 5.2 Picker wheel (hero signature)
An iOS time-picker look: one rounded selection band (`#F2F2F5`) spanning two columns, edges faded with a vertical mask gradient.

- **Left column** (right-aligned) spins through "achieve" in many languages and lands on **lograr**:
  achieve · réussir · erreichen · 達成 · raggiungere · 성취 · conquistar · başarmak · 实现 · osiągnąć · accomplish · **lograr**
  (Swedish "lyckas" was removed: the owner found it odd.)
- **Right column** (left-aligned, grey) spins write · track · record · keep · note · save · journal · **log**, starting a beat later.
- After both land, they hold, then shrink and fade while **Logralee** settles into the band. Hold, fade, loop.
- Timing (9s loop): left lands at ~38%, right at ~42%, columns fade 54–62%, name in 57–66%, holds to 94%. Easing `cubic-bezier(.1,.55,.15,1)` for the spin.
- Pure CSS keyframes, transforms and opacity only (GPU-composited, no layout). Row height in `em` so it scales with `clamp(30px, 4.6vw, 54px)`.
- `prefers-reduced-motion: reduce` → no animation, show "Logralee" in the band.
- Accessibility: wrapper `role="img"` with an `aria-label` describing it; the H1 carries the real message.
- Open: merged name in near-black (current) or the logo green. Owner to decide.

### 5.3 Tiles
White on `#F5F5F7`, radius 28, padding 32, min-height ~360 desktop. Eyebrow → H3 → visual anchored to the bottom (`margin-top: auto`). Grid `repeat(auto-fit, minmax(300px, 1fr))`, gap 20.

### 5.4 Feature section
Two-column flex (text `flex: 999 1 400px`, visual `flex: 1 1 340px`), alternating sides with `wrap-reverse` so text always comes first on phone. Eyebrow, H2, 21px lead, optional stat pair.

### 5.5 UI drawings
Drawn in HTML/CSS/SVG, not screenshots, wherever possible: crisp at any size, tiny, and can animate. Cotton Candy accents. Example numbers stay realistic and are not presented as user data. Real screenshots go in phone frames (hero, Moments) once the owner supplies captures.

### 5.6 Interactive bits (must work without a framework)
- **Try it tile**: an empty circle button (`aria-label="Log set"`); tap → filled black check + "**Set logged.** You showed up. That's the whole thing." Tap again to undo.
- **Coaching switch**: three `aria-pressed` buttons. Lines: Off "Just you and your log. No tips, no prompts." · Minimal "A quiet nudge when something changes, like more reps than last time." · Full "Cues for every exercise and your rest, in plain words."
- Vanilla JS, a few hundred bytes. Everything readable with JS off.

### 5.7 Waitlist form
Visually-hidden `<label>`, email input (48px), black pill button. States: idle → sending → "You're on the list." → error ("That didn't go through. Try again?"). No fake counts. Honeypot field + server-side rate limit. Optional Cloudflare Turnstile if spam shows up.

## 6. Responsive rules (mobile and desktop are equal citizens)

Breakpoints (Apple's): **phone ≤ 734px**, tablet 735–1068px, desktop ≥ 1069px. Check at 360, 390, 768, 1024, 1440.

- No horizontal scroll at any width; 16px minimum gutter.
- Feature sections stack text-first on phone.
- Hero phones: three at desktop; on phone show the centre phone only (or scale the trio to fit). Never overflow.
- Picker wheel fits at 360px: the longest words ("raggiungere", "accomplish") must not clip. Shrink the font or column widths at the phone breakpoint.
- Tiles one per row on phone; min-height relaxes.
- Touch targets ≥ 44px. Forms full-width on phone.
- Type uses `clamp()`. Test Dynamic Type-like zoom (200%) without breakage.

## 7. Performance budget

- Static HTML + one CSS file + a tiny JS file. No framework, no webfonts, no tracking scripts by default.
- Target: **< 150 KB** over the wire for first view, excluding the hero phone image(s). LCP < 2.0s on 4G, CLS ≈ 0.
- Images: AVIF/WebP with `srcset`, explicit `width`/`height`, `loading="lazy"` below the fold. Logo mark as a small PNG/WebP or SVG.
- Activity icons: SVG (from `logralee-icons`), inlined or as a sprite, coloured with `currentColor`.
- Animations: transform/opacity only.

## 8. Launch modes

A single config value (e.g. `data-mode="prelaunch" | "launched"` on `<html>`, or a build constant) switches:

| | Pre-launch | Launched |
|---|---|---|
| Primary CTA | Email form "Join the waitlist" | App Store + Google Play badges |
| Hero note | "Coming this December…" | "Free on iPhone and Android." |
| Extras | — | Apple Smart App Banner meta tag, Play link |

## 9. Hosting and backend

- **Cloudflare Pages** (owner already uses it). Domains: **logralee.com** canonical, **logralee.app** 301 → .com.
- Waitlist: **Pages Function** `POST /api/waitlist` → **D1** table `waitlist(email UNIQUE, created_at, source, user_agent_hash)`. Validate, de-dupe, rate-limit by IP. Export to CSV for the launch email.
- Retire the old GitHub Pages site (redirect `gonzalezosv.github.io/logralee` → logralee.com).

## 10. SEO and sharing

`<title>Logralee: a journal for every way you move</title>`, meta description, Open Graph + Twitter card image (1200×630, logo + headline), favicon set from the logo mark, `apple-touch-icon`, canonical URL, `sitemap.xml`, `robots.txt`.

## 11. Voice gate (all copy)

From the app's soul doc: short sentences, present tense, direct address. Banned: "crush", "beast mode", "no excuses", "no pain no gain", guilt framing, streak pressure. Rest days are part of the plan; showing up is the win. Effort copy is descriptive, never moral.

## 12. Assets needed from the owner

- [ ] Real iOS captures (Cotton Candy, light): Home, Journal, Routine/plan page, plus Lavender and Terracotta variants for the hero trio
- [ ] A real Moment (photo + card) the owner is happy to publish
- [ ] **3D figure render** in a yoga pose (transparent PNG, ~1200px tall), ideally with muscle highlights
- [ ] Coaching engine's real cue lines (3) and the app's real voice lines (3)
- [ ] Live Activity: confirm the three controls
- [ ] Logo mark as SVG (or high-res transparent PNG) in green and cream
- [ ] Activity icons from `~/Dev/logralee-icons` (SVG masters)

## 13. Open questions

1. Is an account required at launch? (Decides "No account needed to start.")
2. Is the 3D How-to in the December release?
3. Merged "Logralee" in the picker: near-black or logo green?
4. Exact launch wording/date for the hero note.
