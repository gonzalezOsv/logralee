/**
 * POST /api/waitlist — Cloudflare Pages Function → D1.
 *
 * Accepts application/x-www-form-urlencoded (plain <form> or the site's fetch) or JSON.
 * Fields: email (required), source (optional, "hero" | "footer" | …), website (honeypot, must be empty).
 *
 * Responses
 *   fetch / JSON clients (Accept: application/json):  { ok: true, already?: true } | { ok: false, error }
 *   plain form posts (no JS):                           303 → /joined/   (or back to /#waitlist on error)
 *
 * Protections: strict email check, lower-cased + trimmed, UNIQUE in D1 (duplicates return ok+already),
 * honeypot field, per-IP rate limit (RATE_LIMIT_PER_HOUR, default 5) using a salted hash of the IP that
 * is only kept in the attempts table for the window. No fake counts anywhere.
 *
 * Bindings (wrangler.toml): DB (D1). Vars: RATE_LIMIT_PER_HOUR (optional), IP_SALT (secret, set with
 * `wrangler pages secret put IP_SALT`). See BUILD_NOTES.md.
 */

interface Env {
  DB: D1Database;
  RATE_LIMIT_PER_HOUR?: string;
  IP_SALT?: string;
}

const EMAIL_RE = /^[^\s@]{1,64}@[^\s@]{1,255}\.[a-z]{2,24}$/i;

function wantsJson(req: Request): boolean {
  const accept = req.headers.get('accept') || '';
  const ctype = req.headers.get('content-type') || '';
  return accept.includes('application/json') || ctype.includes('application/json');
}

async function readFields(req: Request): Promise<Record<string, string>> {
  const ctype = req.headers.get('content-type') || '';
  if (ctype.includes('application/json')) {
    const j = (await req.json().catch(() => ({}))) as Record<string, unknown>;
    return Object.fromEntries(Object.entries(j).map(([k, v]) => [k, String(v ?? '')]));
  }
  const form = await req.formData().catch(() => null);
  const out: Record<string, string> = {};
  if (form) for (const [k, v] of form.entries()) out[k] = typeof v === 'string' ? v : '';
  return out;
}

async function sha256Hex(s: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, '0')).join('');
}

function respond(req: Request, status: number, body: Record<string, unknown>, redirectOk = '/joined/', redirectErr = '/#waitlist'): Response {
  if (wantsJson(req)) {
    return new Response(JSON.stringify(body), {
      status,
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
    });
  }
  // No-JS path: a normal form post. Send them to a real page either way.
  const to = body.ok ? redirectOk : redirectErr;
  return new Response(null, { status: 303, headers: { location: to, 'cache-control': 'no-store' } });
}

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const fields = await readFields(request);

  // Honeypot: bots fill every field. Pretend it worked, store nothing.
  if ((fields.website || '').trim() !== '') return respond(request, 200, { ok: true });

  const email = (fields.email || '').trim().toLowerCase();
  if (!email || email.length > 254 || !EMAIL_RE.test(email)) {
    return respond(request, 400, { ok: false, error: 'invalid_email' });
  }
  const source = (fields.source || 'site').slice(0, 32);

  // Rate limit per IP (hashed with a secret salt; the raw IP is never stored).
  const ip = request.headers.get('cf-connecting-ip') || '0.0.0.0';
  const ipHash = (await sha256Hex((env.IP_SALT || 'logralee') + '|' + ip)).slice(0, 32);
  const limit = Math.max(1, parseInt(env.RATE_LIMIT_PER_HOUR || '5', 10) || 5);
  const now = Math.floor(Date.now() / 1000);
  const windowStart = now - 3600;

  try {
    const { results } = await env.DB.prepare('SELECT COUNT(*) AS n FROM waitlist_attempts WHERE ip_hash = ?1 AND at > ?2')
      .bind(ipHash, windowStart)
      .all<{ n: number }>();
    if ((results?.[0]?.n ?? 0) >= limit) return respond(request, 429, { ok: false, error: 'rate_limited' });

    await env.DB.batch([
      env.DB.prepare('INSERT INTO waitlist_attempts (ip_hash, at) VALUES (?1, ?2)').bind(ipHash, now),
      env.DB.prepare('DELETE FROM waitlist_attempts WHERE at < ?1').bind(now - 86400),
    ]);

    const ua = request.headers.get('user-agent') || '';
    const uaHash = (await sha256Hex(ua)).slice(0, 16);
    const res = await env.DB.prepare(
      'INSERT INTO waitlist (email, created_at, source, user_agent_hash) VALUES (?1, ?2, ?3, ?4) ON CONFLICT(email) DO NOTHING'
    )
      .bind(email, now, source, uaHash)
      .run();

    const inserted = (res.meta?.changes ?? 0) > 0;
    return respond(request, 200, inserted ? { ok: true } : { ok: true, already: true });
  } catch (err) {
    console.error('waitlist error', err);
    return respond(request, 500, { ok: false, error: 'server' });
  }
};

// Anything but POST: say so plainly.
export const onRequest: PagesFunction<Env> = async (ctx) => {
  if (ctx.request.method === 'POST') return onRequestPost(ctx);
  return new Response(JSON.stringify({ ok: false, error: 'method' }), {
    status: 405,
    headers: { 'content-type': 'application/json; charset=utf-8', allow: 'POST' },
  });
};
