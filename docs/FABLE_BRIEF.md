# Brief: logralee.com — fresh-eyes pass, then build

**Owner:** Osvaldo (Bit Ray Technologies). **Goal:** launch-ready marketing site for the Logralee app, live well before the December 2026 app launch. **Repo:** this one (`/Volumes/EXTDRIVE/Dev/logralee`, GitHub `gonzalezosv/logralee`), deployed on **Cloudflare Pages** at **logralee.com** (logralee.app redirects).

## Read first, in this order

1. `docs/APP_FEATURES.md`: everything the app has, with launch status and a **claim checklist**. The site may only claim what this file supports.
2. `docs/SITE_DESIGN.md`: the approved direction (E2), structure, tokens, components, responsive rules, performance budget, launch modes, backend.
3. `docs/mock/index.html`: static render of the approved mock. Open it at 390px and 1440px. Placeholders look like `[this]`.
4. The current `index.html` at the repo root is the **old placeholder site** (pink/purple, fake waitlist that discards emails, a hard-coded "487" counter, placeholder screenshots). It is being replaced, not edited.

## What the owner cares about

- It must feel **premium and thought out** (Apple product-page calibre) and make people **want to use the app**.
- **Mobile and desktop both have to be excellent.** Not "desktop that also works on phones."
- **Performance is a value**, not a nice-to-have (former Game Boy/PSP/DS developer): no framework, no webfonts, tiny JS, transform/opacity-only motion.
- **Green is only for the logo and activity icons.** He rejected green as a page colour.
- The **picker wheel** in the hero (languages → *lograr* + *log* → **Logralee**) is the signature moment. Keep it, perfect it.
- App voice: warm, short, never guilt or hustle (voice gate in SITE_DESIGN §11).
- **Mock first, then build.** He approves UI changes before code.

## Phase 1: fresh-eyes review (stop here for approval)

Review the docs and mock as a first-time visitor on a phone and on a laptop, then as a designer. Deliver a short, prioritized list (most important first) covering:

- **Selling:** does each section make you want the app? What's missing or weak against `APP_FEATURES.md`? Is the order right? Anything that should be cut?
- **Mobile:** nav (currently wraps to two rows at 390px), hero phone trio (outer phones clip at 390px), picker wheel fit at 360px, tile and section rhythm, thumb reach of CTAs.
- **Desktop:** pacing, density, the "Take a closer look" rhythm (white / grey / black alternation).
- **Claims:** anything that contradicts the claim checklist. Note the open questions (account required? 3D How-to in December?).
- **Accessibility:** contrast, focus states, reduced motion, labels, heading order.
- **Performance:** anything that would break the budget.

If a fix is visual, show it (a quick mock or annotated screenshot), not just a description. Keep the write-up lean: findings and proposed fixes, no essay. **Wait for the owner's OK before Phase 2.**

## Phase 2: build

```
/index.html               one page, sections per SITE_DESIGN §3
/privacy/index.html       /terms/  /support/  /press/
/assets/css/site.css      tokens as CSS custom properties
/assets/js/site.js        picker fallback, Try-it tile, coaching switch, waitlist form, launch mode (vanilla, tiny)
/assets/img/              AVIF/WebP + fallbacks, logo mark, OG image, favicons
/assets/icons/            activity icon SVGs (sprite or inline, currentColor)
/functions/api/waitlist.ts   Cloudflare Pages Function → D1
/schema.sql               waitlist table
/wrangler.toml            D1 binding
/_redirects               old GitHub Pages paths, logralee.app → logralee.com handled in Cloudflare
```

- Launch mode switch per SITE_DESIGN §8 (one value flips waitlist ↔ store badges).
- Waitlist: validate, de-dupe (`UNIQUE`), honeypot, IP rate limit, friendly states, no fake counts.
- Privacy / Terms / Support: clear, honest drafts matching how the app actually handles data (on-device storage; confirm accounts with the owner). Mark anything that needs a lawyer's look.
- SEO/sharing per SITE_DESIGN §10.
- Leave clearly labelled slots for the owner's assets (SITE_DESIGN §12); don't invent screenshots or stats.

## Definition of done

- [ ] Phase 1 findings approved by the owner
- [ ] No horizontal scroll at 360 / 390 / 768 / 1024 / 1440; checked in Safari iOS and Chrome Android sizes
- [ ] Lighthouse mobile: Performance ≥ 95, Accessibility 100, Best Practices ≥ 95, SEO 100
- [ ] First view < 150 KB excluding hero images; CLS ≈ 0
- [ ] `prefers-reduced-motion` respected; works with JS off (except form submit and toggles)
- [ ] Waitlist writes to D1 locally (`wrangler pages dev`) and rejects duplicates and bots
- [ ] Every claim traced to `APP_FEATURES.md`; copy passes the voice gate
- [ ] Owner build notes: how to create the D1 database, bind it, deploy, and flip to launch mode

---

## Copy-paste kickoff prompt

```
You're taking over the Logralee marketing website (logralee.com) for a fresh-eyes pass and then the build.
The repo is /Volumes/EXTDRIVE/Dev/logralee. Read docs/FABLE_BRIEF.md first, then docs/APP_FEATURES.md,
docs/SITE_DESIGN.md, and open docs/mock/index.html at 390px and 1440px.

The approved direction is "E2": Apple product-page style, near-black on white with grey/black alternating
sections, green only in the logo and activity icons, Cotton Candy (#BE58E2) only inside UI drawings, a
picker-wheel hero that spins "achieve" in many languages and lands on lograr + log → Logralee.
It must be excellent on both phone and desktop, fast (no framework, no webfonts), and make people want the app.

Do Phase 1 only: give me a short, prioritized list of what you'd change and why (selling, mobile, desktop,
claims, accessibility, performance), with quick mocks for anything visual. Don't write production code
until I approve. Only claim what APP_FEATURES.md supports.
```
