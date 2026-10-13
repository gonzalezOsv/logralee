#!/usr/bin/env python3
"""Generates the secondary pages (/features, /privacy, /terms, /support, /press, /joined, 404)
from tools/pages/*.html bodies plus the shared head, nav and footer below.

  python3 tools/pages.py        # writes <slug>/index.html and 404.html at the repo root

The home page (index.html) is hand-written and not touched. Edit nav/footer here, re-run, commit."""
import os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'pages')
WORDMARK = open(os.path.join(ROOT, 'assets', 'icons', 'wordmark.svg')).read()
WM_SYMBOL = re.sub(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', r'<symbol id="wordmark" viewBox="\1">\2</symbol>', WORDMARK, flags=re.S)
WM_INLINE = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">' + WM_SYMBOL + '</svg>'

HEAD = '''<!doctype html>
<html lang="en" data-mode="prelaunch">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://logralee.com{path}">
{robots}<meta property="og:type" content="website">
<meta property="og:site_name" content="Logralee">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://logralee.com{path}">
<meta property="og:image" content="https://logralee.com/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{p}favicon.ico" sizes="32x32">
<link rel="icon" href="{p}assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{p}assets/img/icon-180.png">
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
{wm}
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
<div class="wrap">
<a class="logo" href="{p}" aria-label="Logralee home"><img src="{p}assets/img/icon-64.png" width="24" height="24" alt=""><svg class="wm" aria-hidden="true"><use href="#wordmark"/></svg></a>
<nav class="links" aria-label="Main">
<a href="{p}#highlights">Highlights</a><a href="{p}#routines">Routines</a><a href="{p}#coaching">Coaching</a><a href="{p}#moments">Moments</a><a href="{p}features/"{cur_features}>Features</a><a href="{p}support/"{cur_support}>Support</a>
</nav>
<div class="right">
<a class="pill cta prelaunch" href="{p}#waitlist">Join waitlist</a>
<a class="pill cta launched" href="{p}#get">Get the app</a>
<details class="menu" id="menu">
<summary aria-label="Menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></summary>
<nav class="sheet" aria-label="Sections"><a href="{p}#highlights">Highlights</a><a href="{p}#routines">Routines</a><a href="{p}#coaching">Coaching</a><a href="{p}#moments">Moments</a><a href="{p}features/">Features</a><a href="{p}support/">Support</a><a href="{p}privacy/">Privacy</a></nav>
</details>
</div>
</div>
</header>
<main id="main">
'''

FOOT = '''
</main>
<footer class="footer">
<div class="wrap">
<span>© {year} Bit Ray Technologies</span>
<nav aria-label="Footer"><a href="{p}features/">Features</a><a href="{p}privacy/">Privacy</a><a href="{p}terms/">Terms</a><a href="{p}support/">Support</a><a href="{p}press/">Press kit</a></nav>
</div>
</footer>
<script src="{p}assets/js/site.js" defer></script>
</body>
</html>
'''

PAGES = {
    'features': ('Logralee features: everything the app does', 'Logging, routines and plans, the coaching engine, 3D guided sessions, Journal, Moments, My Progress, weight, Live Activity, themes and privacy.', '/features/'),
    'privacy': ('Privacy · Logralee', 'How Logralee handles your data: your training journal stays on your phone. No account, no tracking.', '/privacy/'),
    'terms': ('Terms of use · Logralee', 'The terms for using the Logralee app and logralee.com.', '/terms/'),
    'support': ('Support · Logralee', 'Answers to common questions about Logralee, and how to reach us.', '/support/'),
    'press': ('Press kit · Logralee', 'Logralee in one paragraph, the facts, and brand assets.', '/press/'),
    'joined': ("You're on the list · Logralee", 'Thanks for joining the Logralee waitlist.', '/joined/'),
    '404': ('Page not found · Logralee', 'That page isn’t here.', '/404.html'),
}

for slug, (title, desc, path) in PAGES.items():
    body = open(os.path.join(SRC, slug + '.html')).read()
    robots = '<meta name="robots" content="noindex">\n' if slug in ('joined', '404') else ''
    prefix = '' if slug == '404' else '../'
    html = HEAD.format(p=prefix, title=title, desc=desc, path=path, robots=robots, wm=WM_INLINE,
                       cur_features=' aria-current="page"' if slug == 'features' else '',
                       cur_support=' aria-current="page"' if slug == 'support' else '') + body.replace('{p}', prefix) + FOOT.format(p=prefix, year=datetime.date.today().year)
    if slug == '404':
        out = os.path.join(ROOT, '404.html')
    else:
        os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
        out = os.path.join(ROOT, slug, 'index.html')
    open(out, 'w').write(html)
    print('wrote', os.path.relpath(out, ROOT), len(html))
