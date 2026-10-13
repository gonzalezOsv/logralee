#!/usr/bin/env python3
"""Pre-deploy checks for logralee.com.

  python3 tools/check.py [http://localhost:8788]

1. No horizontal overflow at 320/360/390/414/600/734/735/768/834/1024/1068/1069/1440.
2. First-view transfer size (HTML + CSS + JS + sprite + hero images) against the 150 KB budget
   (hero images are reported separately, as the brief excludes them).
3. Screenshots at 390 / 768 / 1440 into tools/shots/ for a quick eyeball.

Needs: pip install playwright && python3 -m playwright install chromium
"""
import sys, os, json
from playwright.sync_api import sync_playwright

base = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8788'
widths = [320, 360, 390, 414, 600, 734, 735, 768, 834, 1024, 1068, 1069, 1440]
pages = ['/', '/features/', '/privacy/', '/terms/', '/support/', '/press/', '/joined/']
os.makedirs(os.path.join(os.path.dirname(__file__), 'shots'), exist_ok=True)
fail = False

with sync_playwright() as p:
    b = p.chromium.launch()
    # 1. overflow
    for path in pages:
        for w in widths:
            pg = b.new_page(viewport={'width': w, 'height': 900})
            pg.goto(base + path)
            pg.wait_for_timeout(100)
            r = pg.evaluate("""() => {const d=document.documentElement; return {sw:d.scrollWidth, cw:d.clientWidth}}""")
            if r['sw'] > r['cw']:
                print(f'FAIL overflow {path} @ {w}px: scrollWidth {r["sw"]} > {r["cw"]}')
                fail = True
            pg.close()
    print('overflow check done')

    # 2. weight (first view, phone)
    sizes = {}
    pg = b.new_page(viewport={'width': 390, 'height': 844})
    pg.on('response', lambda res: sizes.__setitem__(res.url, len(res.body()) if res.ok else 0))
    pg.goto(base + '/')
    pg.wait_for_load_state('networkidle')
    core = sum(v for k, v in sizes.items() if not any(x in k for x in ('/assets/img/',)))
    imgs = sum(v for k, v in sizes.items() if '/assets/img/' in k)
    print(f'first view (390px): core {core/1024:.1f} KB (html+css+js+sprite+fonts), images {imgs/1024:.1f} KB, total {(core+imgs)/1024:.1f} KB')
    if core > 150 * 1024:
        print('FAIL budget: core first view over 150 KB'); fail = True
    pg.close()

    # 3. screenshots
    for w in (390, 768, 1440):
        pg = b.new_page(viewport={'width': w, 'height': 900}, device_scale_factor=1)
        pg.goto(base + '/'); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(os.path.dirname(__file__), 'shots', f'home-{w}.png'), full_page=True)
        pg.close()
    b.close()

print('OK' if not fail else 'FAILED')
sys.exit(1 if fail else 0)
