#!/usr/bin/env python3
"""Rebuilds index.html from index.src.html.

Fills three placeholders so the hand-written source stays readable:
  {{WM}}      the icon sprite + Quicksand wordmark, inlined (from assets/icons/sprite.svg)
  {{WALL}}    the Journal tile's year wall (deterministic pattern, seed 7)
  {{COVERS}}  the routine/plan cover cards listed in COVERS below

  python3 tools/build_index.py
"""
import os, re, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (image basename in assets/img, title, subtitle, activity icon id, chip text)
COVERS = [
    ('routine-morning-flow', 'Morning Flow', 'Ten minutes to start the day.', 'yoga', 'Yoga · 10 min'),
    ('routine-full-body', 'Full Body Foundations', 'Six moves that cover everything.', 'strength', 'Strength · 45 min'),
    ('routine-fran', 'Fran', 'The benchmark most people measure against.', 'crossfit', 'CrossFit · 12 min'),
    ('routine-morning-mobility', 'Morning Mobility', 'Eight minutes on the floor before the day starts.', 'mobility', 'Mobility · 8 min'),
    ('plan-bro-split', 'The Bro Split', 'One muscle a day, five days a week, eight weeks.', 'strength', 'Plan · 8 weeks'),
    ('routine-cindy', 'Cindy', 'Twenty minutes, three movements, no equipment.', 'bodyweight', 'CrossFit · 20 min'),
]

CARD = '''<li class="cover">
<picture><source type="image/avif" srcset="assets/img/{f}-480.avif 480w, assets/img/{f}-960.avif 960w" sizes="(max-width: 734px) 78vw, 320px"><source type="image/webp" srcset="assets/img/{f}-480.webp 480w, assets/img/{f}-960.webp 960w" sizes="(max-width: 734px) 78vw, 320px"><img src="assets/img/{f}-480.jpg" width="480" height="270" alt="" loading="lazy" decoding="async"></picture>
<div class="b"><b>{name}</b><span>{sub}</span><span class="chip"><svg class="ico" aria-hidden="true"><use href="#i-{ico}"/></svg>{chip}</span></div>
</li>'''

# The icon sprite (eight activity icons + wordmark) is inlined so the page works from file:// too
# (browsers treat an external <use href="sprite.svg#id"> as cross-origin there).
sprite = open(os.path.join(ROOT, 'assets', 'icons', 'sprite.svg')).read()
WM = sprite.replace('<svg ', '<svg style="display:none" aria-hidden="true" ', 1)

random.seed(7)
WALL = ''.join(
    '<div class="mo"><small>%s</small>' % m + ''.join('<i class="on"></i>' if (mi < 10 and random.random() < 0.42) else '<i></i>' for _ in range(28)) + '</div>'
    for mi, m in enumerate('JFMAMJJASOND')
)

cards = '\n'.join(CARD.format(f=f, name=name, sub=sub, ico=ico, chip=chip) for f, name, sub, ico, chip in COVERS)
src = open(os.path.join(ROOT, 'index.src.html')).read()
out = src.replace('{{WM}}', WM).replace('{{WALL}}', WALL).replace('{{COVERS}}', cards)
assert '{{' not in out, 'unfilled placeholder'
open(os.path.join(ROOT, 'index.html'), 'w').write(out)
print('index.html', len(out), 'bytes')
