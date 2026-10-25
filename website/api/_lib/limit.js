// Per-person limit for the tool finder, shared by the website (per IP) and
// Discord (per Discord user). Counters live in Redis (REDIS_URL, connected
// from the Vercel Marketplace): one per hour and one per day, each created
// with its expiry, so the store only ever holds the last day's askers.
// docs/PickerChatbot.md, "Per-person limit".
//
// Who asked is never stored as is: the key is an HMAC of the IP or user id,
// keyed by the Redis URL (a secret only this project holds), so the store
// cannot be read back into addresses.
//
// Fails OPEN: with Redis unreachable or unconfigured the question goes
// through and the failure is logged. A finder that stops answering because
// a counter store hiccuped is worse than a few unmetered questions, and the
// Gateway budget caps the spend either way.
import crypto from 'node:crypto';
import { createClient } from 'redis';

export const WINDOWS = [
  { name: 'hour', seconds: 3600, env: 'CHAT_LIMIT_HOUR', fallback: 10 },
  { name: 'day', seconds: 86400, env: 'CHAT_LIMIT_DAY', fallback: 30 },
];

export function limits(env = process.env) {
  return WINDOWS.map((w) => {
    const n = Number(env[w.env]);
    return { ...w, max: Number.isFinite(n) && n > 0 ? Math.floor(n) : w.fallback };
  });
}

/** The stored key for one person and one window: no raw IP or user id. */
export function keyOf(kind, id, window, secret = process.env.REDIS_URL || '') {
  const h = crypto.createHmac('sha256', secret).update(`${kind}:${id}`).digest('hex').slice(0, 32);
  return `finder:${kind}:${h}:${window}`;
}

let clientPromise = null;
/** One connection per function instance, reused across requests. */
function client() {
  if (!process.env.REDIS_URL) return null;
  if (!clientPromise) {
    const c = createClient({
      url: process.env.REDIS_URL,
      socket: { connectTimeout: 1500, reconnectStrategy: (n) => (n > 3 ? false : 200 * n) },
    });
    c.on('error', (e) => console.error('limit redis error:', e && e.message));
    clientPromise = c.connect().then(() => c).catch((e) => {
      clientPromise = null;
      throw e;
    });
  }
  return clientPromise;
}

/**
 * Counts one question for `id` and says whether it is allowed:
 * {ok: true} or {ok: false, window, max, retryAfter (seconds)}.
 * `redis` replaces the real client (tests).
 */
export async function take(kind, id, { redis, env = process.env } = {}) {
  if (!id) return { ok: true, skipped: 'no id' };
  let r;
  try {
    r = redis || (await client());
  } catch (e) {
    console.error('limit: redis unreachable, allowing:', e && e.message);
    return { ok: true, skipped: 'unreachable' };
  }
  if (!r) return { ok: true, skipped: 'not configured' };
  const ws = limits(env);
  try {
    const m = r.multi();
    for (const w of ws) {
      const k = keyOf(kind, id, w.name, env.REDIS_URL || '');
      // created with its expiry the first time, then only counted up
      m.set(k, '0', { expiration: { type: 'EX', value: w.seconds }, condition: 'NX' });
      m.incr(k);
      m.ttl(k);
    }
    const out = await m.exec();
    for (let i = 0; i < ws.length; i += 1) {
      const count = Number(out[i * 3 + 1]);
      const ttl = Number(out[i * 3 + 2]);
      if (count > ws[i].max) {
        return { ok: false, window: ws[i].name, max: ws[i].max, retryAfter: ttl > 0 ? ttl : ws[i].seconds };
      }
    }
    return { ok: true };
  } catch (e) {
    console.error('limit: count failed, allowing:', e && e.message);
    return { ok: true, skipped: 'error' };
  }
}

/** "in 12 minutes", "in 3 hours": when the limit lifts. */
export function whenAgain(seconds) {
  const m = Math.ceil(seconds / 60);
  if (m < 60) return `in ${m} minute${m === 1 ? '' : 's'}`;
  const h = Math.ceil(m / 60);
  return `in ${h} hour${h === 1 ? '' : 's'}`;
}

/** The website caller's IP, as Vercel reports it. */
export function ipOf(request) {
  const xff = request.headers.get('x-forwarded-for') || '';
  return xff.split(',')[0].trim() || request.headers.get('x-real-ip') || '';
}
