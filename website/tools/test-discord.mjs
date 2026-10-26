// Offline checks for the Discord /findtool endpoint (api/discord.js,
// api/_lib/discord.js): requests signed with a throwaway Ed25519 key, a mock
// model, and global fetch replaced so nothing reaches Discord or the
// Gateway. Needs api/_data/chat.json (npm run pages). node tools/test-discord.mjs
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { MockLanguageModelV4 } from 'ai/test';
import { isFromDiscord, toMessage, problemOf, isPrivate, followupUrl } from '../api/_lib/discord.js';
import { POST, finish } from '../api/discord.js';

let failed = 0;
async function check(name, fn) {
  try { await fn(); console.log(`ok   ${name}`); } catch (e) { failed += 1; console.log(`FAIL ${name}\n     ${e.message}`); }
}

const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
const pubHex = publicKey.export({ format: 'der', type: 'spki' }).subarray(12).toString('hex');
const sign = (ts, body) => crypto.sign(null, Buffer.from(ts + body), privateKey).toString('hex');
process.env.DISCORD_PUBLIC_KEY = pubHex;
process.env.DISCORD_APPLICATION_ID = '1234';

function req(obj, { badSig = false } = {}) {
  const body = JSON.stringify(obj);
  const ts = String(Math.floor(Date.now() / 1000));
  const sig = badSig ? sign(ts, body + 'x') : sign(ts, body);
  return new Request('https://functionstore.tools/api/discord/', {
    method: 'POST', body,
    headers: { 'content-type': 'application/json', 'x-signature-ed25519': sig, 'x-signature-timestamp': ts },
  });
}
const command = (value, extra = []) => ({
  type: 2, token: 'tok', application_id: '1234',
  data: { name: 'findtool', options: [{ name: 'problem', type: 3, value }, ...extra] },
});

const usage = {
  inputTokens: { total: 1, noCache: 1, cacheRead: undefined, cacheWrite: undefined },
  outputTokens: { total: 1, text: 1, reasoning: undefined },
};
const recommendModel = (reply, picks) => new MockLanguageModelV4({
  doGenerate: async () => ({
    content: [{ type: 'tool-call', toolCallId: 'r', toolName: 'recommend', input: JSON.stringify({ reply, picks }) }],
    finishReason: { unified: 'tool-calls', raw: undefined }, usage, warnings: [],
  }),
});

await check('signature: a real one passes, a tampered one fails', () => {
  const ts = '1700000000';
  assert.ok(isFromDiscord(pubHex, sign(ts, '{"a":1}'), ts, '{"a":1}'));
  assert.ok(!isFromDiscord(pubHex, sign(ts, '{"a":1}'), ts, '{"a":2}'));
  assert.ok(!isFromDiscord(pubHex, 'zz', ts, '{}'));
  assert.ok(!isFromDiscord('', sign(ts, '{}'), ts, '{}'));
});

await check('POST: a bad signature is refused with 401', async () => {
  assert.equal((await POST(req({ type: 1 }, { badSig: true }))).status, 401);
});

await check('POST: PING answers PONG', async () => {
  assert.deepEqual(await (await POST(req({ type: 1 }))).json(), { type: 1 });
});

await check('POST: no model configured answers privately, without deferring', async () => {
  delete process.env.CHAT_MODEL;
  const d = await (await POST(req(command('my timeline is in the way')))).json();
  assert.equal(d.type, 4);
  assert.equal(d.data.flags, 64);
});

await check('POST: /findtool defers at once and then PATCHes the answer', async () => {
  process.env.CHAT_MODEL = 'test/none';
  const calls = [];
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (url, init) => {
    calls.push({ url: String(url), init });
    // the Gateway call fails (no model here), Discord's PATCH succeeds
    return String(url).includes('discord.com') ? new Response('{}', { status: 200 }) : new Response('nope', { status: 500 });
  };
  try {
    const d = await (await POST(req(command('my timeline is in the way', [{ name: 'private', type: 5, value: true }])))).json();
    assert.equal(d.type, 5);
    assert.equal(d.data.flags, 64);
    for (let i = 0; i < 50 && !calls.some((c) => c.url.includes('discord.com')); i += 1) await new Promise((r) => setTimeout(r, 100));
    const patch = calls.find((c) => c.url.includes('discord.com'));
    assert.ok(patch, 'no PATCH to Discord');
    assert.equal(patch.url, followupUrl('1234', 'tok'));
    assert.equal(patch.init.method, 'PATCH');
    assert.ok(JSON.parse(patch.init.body).content.length > 0);
  } finally {
    globalThis.fetch = realFetch;
    delete process.env.CHAT_MODEL;
  }
});

await check('finish: picks become an embed with titles, Patreon labels and docs links', async () => {
  let sent;
  const fetchImpl = async (url, init) => { sent = { url, body: JSON.parse(init.body) }; return new Response('{}'); };
  await finish(command('palettes'), 'I want nicer colour palettes', {
    model: recommendModel('These make palettes.', [{ name: 'ColorGen', why: 'Builds palettes.' }, { name: 'FNS_Nope', why: 'x' }]),
    fetchImpl,
  });
  const f = sent.body.embeds[0].fields;
  assert.equal(f.length, 1);
  assert.equal(f[0].name, 'ColorGen · Patreon');
  assert.ok(f[0].value.includes('[Docs](https://functionstore.tools/docs/colorgen/)'));
  assert.ok(sent.body.content.startsWith('> I want nicer colour palettes'));
  assert.deepEqual(sent.body.allowed_mentions, { parse: [] });
  assert.equal(sent.body.embeds[0].url, 'https://functionstore.tools/get/#add=ColorGen');
  assert.ok(sent.body.embeds[0].description.includes('(https://functionstore.tools/get/#add=ColorGen)'));
});

await check('toMessage: a clarifying question gets a re-run hint, no embed', () => {
  const m = toMessage('live shows', { reply: 'Which part of your show?', picks: [] });
  assert.ok(!m.embeds);
  assert.ok(m.content.includes('/findtool again'));
});

await check('toMessage: lengths stay under Discord limits', () => {
  const long = 'x'.repeat(5000);
  const picks = Array.from({ length: 12 }, () => ({ title: long, access: 'free', why: long, url: 'https://functionstore.tools/docs/x/' }));
  const m = toMessage(long, { reply: long, picks });
  assert.ok(m.content.length <= 2000);
  assert.ok(m.embeds[0].fields.length <= 8);
  assert.ok(m.embeds[0].fields.every((x) => x.name.length <= 256 && x.value.length <= 1024));
});

await check('option readers', () => {
  assert.equal(problemOf(command('  hi  ')), 'hi');
  assert.equal(problemOf({ data: {} }), '');
  assert.equal(isPrivate(command('a', [{ name: 'private', value: true }])), true);
  assert.equal(isPrivate(command('a')), false);
});

console.log(failed ? `\n${failed} failed` : '\nall passed');
process.exit(failed ? 1 : 0);
