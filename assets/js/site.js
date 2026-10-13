/* logralee.com — site.js (vanilla, no dependencies)
   Everything on the page works without this file; it only adds:
   1. Try-it tile (log a set / undo)
   2. Coaching level switch
   3. Waitlist form via fetch (falls back to a normal POST → /joined/)
   4. Phone menu closes after choosing a link
   5. Picker wheel replay on tap (respects reduced motion) */
(function () {
  'use strict';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Try it */
  $$('[data-tryit]').forEach(function (tile) {
    var btn = $('.circle', tile);
    if (!btn) return;
    btn.addEventListener('click', function () {
      var on = btn.getAttribute('aria-pressed') !== 'true';
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.setAttribute('aria-label', on ? 'Set logged. Tap to undo' : 'Log set');
      tile.classList.toggle('is-logged', on);
    });
  });

  /* 2. Coaching level */
  $$('[data-levels]').forEach(function (box) {
    var buttons = $$('.seg button', box);
    var lines = $$('.line p', box);
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var level = b.getAttribute('data-level');
        buttons.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        lines.forEach(function (p) {
          if (p.getAttribute('data-level') === level) p.setAttribute('data-on', ''); else p.removeAttribute('data-on');
        });
      });
    });
  });

  /* 3. Waitlist */
  $$('form[data-waitlist]').forEach(function (form) {
    var msg = $('.msg', form);
    var input = $('input[type="email"]', form);
    function say(state, text) {
      if (!msg) return;
      msg.setAttribute('data-state', state);
      msg.textContent = text;
    }
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return; // plain POST → /joined/
      e.preventDefault();
      var email = (input.value || '').trim();
      if (!email || email.indexOf('@') < 1) { say('error', 'That doesn’t look like an email address.'); input.focus(); return; }
      form.classList.add('is-sending');
      say('', 'One moment…');
      var body = new URLSearchParams(new FormData(form));
      fetch(form.action, { method: 'POST', body: body, headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          form.classList.remove('is-sending');
          if (res.ok && res.j && res.j.ok) {
            say('ok', res.j.already ? 'You’re already on the list.' : 'You’re on the list.');
            input.value = '';
          } else if (res.j && res.j.error === 'invalid_email') {
            say('error', 'That doesn’t look like an email address.');
          } else if (res.j && res.j.error === 'rate_limited') {
            say('error', 'Too many tries from here. Give it a little while.');
          } else {
            say('error', 'That didn’t go through. Try again?');
          }
        })
        .catch(function () {
          form.classList.remove('is-sending');
          say('error', 'That didn’t go through. Try again?');
        });
    });
  });

  /* 4. Phone menu */
  var menu = $('#menu');
  if (menu) {
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { menu.removeAttribute('open'); }); });
    document.addEventListener('click', function (e) { if (menu.hasAttribute('open') && !menu.contains(e.target)) menu.removeAttribute('open'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') menu.removeAttribute('open'); });
  }

  /* 5. Picker replay: restart the CSS animation once on tap/click */
  var picker = $('#picker');
  if (picker && !reduced) {
    var parts = $$('.wl, .wr, .cols, .merged', picker);
    var busy = false;
    picker.addEventListener('click', function () {
      if (busy) return;
      busy = true;
      picker.classList.add('replay');
      parts.forEach(function (el) { el.style.animation = 'none'; });
      void picker.offsetWidth; // reflow so the animation restarts
      parts.forEach(function (el) { el.style.animation = ''; });
      setTimeout(function () { busy = false; }, 9200);
    });
  }
})();
