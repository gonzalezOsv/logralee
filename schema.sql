-- logralee.com waitlist (Cloudflare D1)
-- Apply:  wrangler d1 execute logralee-waitlist --remote --file=./schema.sql   (and --local for dev)

CREATE TABLE IF NOT EXISTS waitlist (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  email           TEXT    NOT NULL UNIQUE,          -- lower-cased, trimmed
  created_at      INTEGER NOT NULL,                 -- unix seconds
  source          TEXT    NOT NULL DEFAULT 'site',  -- hero | footer | …
  user_agent_hash TEXT                              -- first 16 hex of sha256(UA); no raw UA stored
);

-- short-lived, hashed IP attempts for the per-IP rate limit; rows older than a day are pruned on write
CREATE TABLE IF NOT EXISTS waitlist_attempts (
  ip_hash TEXT    NOT NULL,                         -- sha256(IP_SALT | ip), first 32 hex
  at      INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_attempts_ip_at ON waitlist_attempts (ip_hash, at);

-- Export for the launch email:
--   wrangler d1 execute logralee-waitlist --remote --command "SELECT email, datetime(created_at,'unixepoch') AS joined, source FROM waitlist ORDER BY id" --json > waitlist.json
