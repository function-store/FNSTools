// Offline checks for the tool finder's per-person limit (api/_lib/limit.js)
// against an in-memory stand-in for Redis. node tools/test-limit.mjs
import assert from 'node:assert/strict';
import { take, keyOf, limits, whenAgain, ipOf } from '../api/_lib/limit.js';

let failed = 0;
async function check(name, fn) {
  try { await fn(); console.log(`ok   ${name}`); } catch (e) { failed += 1; console.log(`FAIL ${name}\n     ${e.message}`); }
}

/** Just enough of node-redis: multi() with set NX EX, incr, ttl. */
function fakeRedis(now = () => Date.now()) {
  const store = new Map();
  const live = (k) => {
    const v = store.get(k);
    if (v && v.until <= now()) { store.delete(k); return null; }
    return v || null;
  };
  return {
    store,
    multi() {
      const ops = [];
      const m = {
        set(k, val, o) { ops.push(() => {
          if (o.condition === 'NX' && live(k)) return null;
          store.set(k, { n: Number(val), until: now() + o.expiration.value * 1000 });
          return 'OK';
        }); return m; },
        incr(k) { ops.push(() => { const v = live(k); v.n += 1; return v.n; }); return m; },
        ttl(k) { ops.push(() => { const v = live(k); return v ? Math.ceil((v.until - now()) / 1000) : -2; }); return m; },
        async exec() { return ops.map((f) => f()); },
      };
      return m;
    },
  };
}
const env = { REDIS_URL: 'redis://secret@host:1', CHAT_LIMIT_HOUR: '3', CHAT_LIMIT_DAY: '5' };

await check('limits: defaults, and env overrides', () => {
  assert.deepEqual(limits({}).map((w) => w.max), [10, 30]);
  assert.deepEqual(limits(env).map((w) => w.max), [3, 5]);
  assert.deepEqual(limits({ CHAT_LIMIT_HOUR: 'x', CHAT_LIMIT_DAY: '-1' }).map((w) => w.max), [10, 30]);
});

await check('the hour limit lets max through, then refuses with a wait', async () => {
  const redis = fakeRedis();
  for (let i = 0; i < 3; i += 1) assert.equal((await take('ip', '1.2.3.4', { redis, env })).ok, true);
  const r = await take('ip', '1.2.3.4', { redis, env });
  assert.equal(r.ok, false);
  assert.equal(r.window, 'hour');
  assert.ok(r.retryAfter > 3500 && r.retryAfter <= 3600, String(r.retryAfter));
});

await check('people are counted apart, and website and Discord apart', async () => {
  const redis = fakeRedis();
  for (let i = 0; i < 3; i += 1) await take('ip', 'a', { redis, env });
  assert.equal((await take('ip', 'b', { redis, env })).ok, true);
  assert.equal((await take('discord', 'a', { redis, env })).ok, true);
});

await check('the day limit holds after the hour window passes', async () => {
  let t = 0;
  const redis = fakeRedis(() => t);
  for (let i = 0; i < 3; i += 1) await take('ip', 'a', { redis, env });
  t += 3601 * 1000;
  assert.equal((await take('ip', 'a', { redis, env })).ok, true);
  assert.equal((await take('ip', 'a', { redis, env })).ok, true);
  const r = await take('ip', 'a', { redis, env });
  assert.equal(r.ok, false);
  assert.equal(r.window, 'day');
});

await check('counters carry their expiry from the first question', async () => {
  const redis = fakeRedis();
  await take('ip', 'a', { redis, env });
  assert.equal(redis.store.size, 2);
  for (const v of redis.store.values()) assert.ok(v.until > Date.now());
});

await check('stored keys hold no raw IP or user id', async () => {
  const redis = fakeRedis();
  await take('ip', '203.0.113.9', { redis, env });
  await take('discord', '80351110224678912', { redis, env });
  for (const k of redis.store.keys()) {
    assert.ok(!k.includes('203.0.113.9') && !k.includes('80351110224678912'), k);
    assert.match(k, /^finder:(ip|discord):[0-9a-f]{32}:(hour|day)$/);
  }
  assert.notEqual(keyOf('ip', 'a', 'hour', 's1'), keyOf('ip', 'a', 'hour', 's2'));
});

await check('fails open: no store, no id, or a store error lets the question through', async () => {
  assert.equal((await take('ip', 'a', { env: {} })).ok, true);
  assert.equal((await take('ip', '', { redis: fakeRedis(), env })).ok, true);
  const broken = { multi() { return { set() { return this; }, incr() { return this; }, ttl() { return this; }, async exec() { throw new Error('down'); } }; } };
  const r = await take('ip', 'a', { redis: broken, env });
  assert.equal(r.ok, true);
  assert.equal(r.skipped, 'error');
});

await check('whenAgain and ipOf', () => {
  assert.equal(whenAgain(30), 'in 1 minute');
  assert.equal(whenAgain(600), 'in 10 minutes');
  assert.equal(whenAgain(7200), 'in 2 hours');
  const req = new Request('https://x/', { headers: { 'x-forwarded-for': '198.51.100.7, 10.0.0.1' } });
  assert.equal(ipOf(req), '198.51.100.7');
  assert.equal(ipOf(new Request('https://x/', { headers: { 'x-real-ip': '198.51.100.8' } })), '198.51.100.8');
});

console.log(failed ? `\n${failed} failed` : '\nall passed');
process.exit(failed ? 1 : 0);
