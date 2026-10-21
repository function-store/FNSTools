// Offline checks for the /get tool finder (api/chat.js, api/_lib/finder.js)
// with a mock model: no Gateway key, no network. Needs api/_data/chat.json,
// so run `npm run pages` first. Usage: node tools/test-chat.mjs
import assert from 'node:assert/strict';
import { MockLanguageModelV4, mockValues } from 'ai/test';
import {
  answer, searchDocs, readDoc, validatePicks, clampMessages, instructions, plainReply, LIMITS,
} from '../api/_lib/finder.js';
import { GET, POST, OPTIONS } from '../api/chat.js';
import { readFileSync } from 'node:fs';

const data = JSON.parse(readFileSync(new URL('../api/_data/chat.json', import.meta.url), 'utf8'));

let failed = 0;
async function check(name, fn) {
  try {
    await fn();
    console.log(`ok   ${name}`);
  } catch (e) {
    failed += 1;
    console.log(`FAIL ${name}\n     ${e.message}`);
  }
}

const usage = {
  inputTokens: { total: 1, noCache: 1, cacheRead: undefined, cacheWrite: undefined },
  outputTokens: { total: 1, text: 1, reasoning: undefined },
};
const call = (toolName, input, id) => ({
  content: [{ type: 'tool-call', toolCallId: id, toolName, input: JSON.stringify(input) }],
  finishReason: { unified: 'tool-calls', raw: undefined }, usage, warnings: [],
});
const text = (t) => ({
  content: [{ type: 'text', text: t }],
  finishReason: { unified: 'stop', raw: undefined }, usage, warnings: [],
});
const scripted = (...steps) => {
  const next = mockValues(...steps);
  const prompts = [];
  const model = new MockLanguageModelV4({
    doGenerate: async (opts) => { prompts.push(opts.prompt); return next(); },
  });
  return { model, prompts };
};

const real = data.tools[0].name;

await check('chat data has no previews and every tool has a doc', () => {
  assert.ok(data.tools.length > 50);
  assert.ok(data.tools.every((t) => t.access === 'free' || t.access === 'patreon'));
  assert.ok(data.tools.every((t) => t.sections.length > 0));
});

await check('searchDocs finds the timeline tool for a timeline problem', () => {
  const r = searchDocs('hide the timeline for more screen space');
  assert.ok(r.results.length > 0);
  assert.ok(r.results.some((x) => x.name === 'FNS_BorderlessTD'), JSON.stringify(r.results.map((x) => x.name)));
});

await check('searchDocs with only stop words returns nothing', () => {
  assert.equal(searchDocs('the and how').results.length, 0);
});

await check('readDoc by name and by title, unknown is an error', () => {
  assert.equal(readDoc('FNS_BorderlessTD').title, 'BorderlessTD');
  assert.equal(readDoc('borderlesstd').name, 'FNS_BorderlessTD');
  assert.ok(readDoc('FNS_DoesNotExist').error);
  assert.ok(readDoc('FNS_BorderlessTD').doc.length <= LIMITS.docChars + 200);
});

await check('validatePicks drops invented names, dedupes, caps', () => {
  const many = data.tools.slice(0, 12).map((t) => ({ name: t.name, why: 'x' }));
  const v = validatePicks([{ name: 'FNS_Invented', why: 'x' }, { name: real, why: 'a' }, { name: real, why: 'b' }, ...many]);
  assert.deepEqual(v.dropped, ['FNS_Invented']);
  assert.equal(v.accepted[0].name, real);
  assert.equal(v.accepted.length, LIMITS.picks);
});

await check('validatePicks refuses every preview package', () => {
  const v = validatePicks(['FNS_RadialMenu', 'FNS_POPOverlay', 'PandorasTox', 'FNS_OpSequencer']
    .map((name) => ({ name, why: 'x' })));
  assert.equal(v.accepted.length, 0);
});

await check('clampMessages keeps the newest turns and starts on a user turn', () => {
  const long = Array.from({ length: 30 }, (_, i) => ({ role: i % 2 ? 'assistant' : 'user', content: 'x'.repeat(2000) }));
  const k = clampMessages(long);
  assert.ok(k.length <= LIMITS.messages);
  assert.equal(k[0].role, 'user');
  assert.ok(k.reduce((n, m) => n + m.content.length, 0) <= LIMITS.totalChars);
  assert.equal(clampMessages([{ role: 'system', content: 'x' }]).length, 0);
});

await check('instructions carry the catalog and the reader\'s access', () => {
  assert.ok(instructions('free').includes('FNS_BorderlessTD | BorderlessTD'));
  assert.ok(instructions('patreon').includes('Patreon supporter'));
  assert.ok(!instructions('free').includes('FNS_RadialMenu'));
});

await check('instructions list the tools already offered, and only then', () => {
  assert.ok(!instructions('free').includes('Already offered'));
  assert.ok(instructions('free', ['FNS_BorderlessTD']).includes('Already offered in this conversation: FNS_BorderlessTD.'));
});

await check('plainReply strips markdown a model writes anyway', () => {
  assert.equal(plainReply('*   **midiMapper**: maps `MIDI`.\n\n\n- ok'), '- midiMapper: maps MIDI.\n\n- ok');
});

await check('answer: every step must call a tool; shown reaches the instructions', async () => {
  const seen = [];
  const model = new MockLanguageModelV4({
    doGenerate: async (opts) => {
      seen.push({ choice: opts.toolChoice, sys: JSON.stringify(opts.prompt[0]) });
      return call('recommend', { reply: 'More: **Output**.', picks: [{ name: 'FNS_Output', why: 'x' }] }, 'r1');
    },
  });
  const out = await answer({ messages: [{ role: 'user', content: 'more' }], shown: ['FNS_BorderlessTD', 'FNS_Nope'] }, { model });
  assert.equal(seen[0].choice.type, 'required');
  assert.ok(seen[0].sys.includes('Already offered in this conversation: FNS_BorderlessTD.'));
  assert.ok(!seen[0].sys.includes('FNS_Nope.'));
  assert.equal(out.reply, 'More: Output.');
});

await check('answer: a tool already offered is never offered again', async () => {
  const { model } = scripted(call('recommend', { reply: 'More.',
    picks: [{ name: 'TDXMap', why: 'x' }, { name: 'midiMapper', why: 'y' }] }, 'r1'));
  const out = await answer({ messages: [{ role: 'user', content: 'more' }], shown: ['TDXMap'] }, { model });
  assert.deepEqual(out.picks.map((p) => p.name), ['midiMapper']);
});

await check('answer: search, read, recommend; invented pick dropped', async () => {
  const { model, prompts } = scripted(
    call('searchDocs', { query: 'hide timeline' }, 'c1'),
    call('readDoc', { name: 'FNS_BorderlessTD' }, 'c2'),
    call('recommend', {
      reply: 'BorderlessTD hides the timeline.',
      picks: [{ name: 'FNS_BorderlessTD', why: 'Hides the timeline on a key.' }, { name: 'FNS_MadeUp', why: 'x' }],
    }, 'c3'),
    text('should never be reached'),
  );
  const out = await answer({ messages: [{ role: 'user', content: 'my timeline takes too much room' }], access: 'free' }, { model });
  assert.equal(prompts.length, 3, 'stops on recommend');
  assert.equal(out.reply, 'BorderlessTD hides the timeline.');
  assert.deepEqual(out.picks.map((p) => p.name), ['FNS_BorderlessTD']);
  assert.equal(out.picks[0].url, 'https://functionstore.tools/docs/fns-borderlesstd/');
  assert.deepEqual(out.dropped, ['FNS_MadeUp']);
  assert.deepEqual(out.read, ['FNS_BorderlessTD']);
});

await check('answer: a plain-text answer is retried once through recommend', async () => {
  const choices = [];
  const model = new MockLanguageModelV4({
    doGenerate: async (opts) => {
      const forced = opts.toolChoice && opts.toolChoice.type === 'tool';
      choices.push(forced ? 'recommend' : opts.toolChoice && opts.toolChoice.type);
      return forced
        ? call('recommend', { reply: 'I only know FNSTools; see https://docs.derivative.ca.', picks: [] }, 'r1')
        : text('*   **Noise TOP**: lower the speed.');
    },
  });
  const out = await answer({ messages: [{ role: 'user', content: 'how do I use a noise TOP' }] }, { model });
  assert.deepEqual(choices, ['required', 'recommend']);
  assert.equal(out.picks.length, 0);
  assert.ok(out.reply.includes('FNSTools'));
});

await check('answer: the last step is forced to recommend', async () => {
  const choices = [];
  let n = 0;
  const model = new MockLanguageModelV4({
    doGenerate: async (opts) => {
      choices.push(opts.toolChoice && opts.toolChoice.type === 'tool' ? opts.toolChoice.toolName : 'auto');
      n += 1;
      return opts.toolChoice && opts.toolChoice.type === 'tool'
        ? call('recommend', { reply: 'Nothing fits.', picks: [] }, 'r' + n)
        : call('searchDocs', { query: 'x' + n }, 's' + n);
    },
  });
  const out = await answer({ messages: [{ role: 'user', content: 'anything' }] }, { model });
  assert.equal(choices.length, LIMITS.steps);
  assert.equal(choices[choices.length - 1], 'recommend');
  assert.ok(choices.slice(0, -1).every((c) => c === 'auto'));
  assert.equal(out.reply, 'Nothing fits.');
});

await check('answer: reads past the cap are refused', async () => {
  const names = data.tools.slice(0, LIMITS.reads + 1).map((t) => t.name);
  const { model } = scripted(...names.map((nm, i) => call('readDoc', { name: nm }, 'd' + i)),
    call('recommend', { reply: 'ok', picks: [] }, 'r'));
  const out = await answer({ messages: [{ role: 'user', content: 'anything' }] }, { model });
  assert.equal(out.read.length, LIMITS.reads);
});

await check('answer: a conversation ending on the assistant is refused', async () => {
  const { model } = scripted(text('x'));
  const out = await answer({ messages: [{ role: 'user', content: 'a' }, { role: 'assistant', content: 'b' }] }, { model });
  assert.ok(out.error);
});

const req = (origin, body, method = 'POST') => new Request('https://functionstore.tools/api/chat', {
  method, headers: { 'Content-Type': 'application/json', ...(origin ? { Origin: origin } : {}) },
  body: method === 'POST' ? body : undefined,
});

await check('CORS: site, previews and the installer allowed; others not', () => {
  for (const o of ['https://functionstore.tools', 'https://fnstools-git-dev25-abc.vercel.app', 'http://127.0.0.1:9981', 'http://localhost:3000']) {
    assert.equal(OPTIONS(req(o, null, 'OPTIONS')).headers.get('access-control-allow-origin'), o, o);
  }
  for (const o of ['https://evil.example', 'http://127.0.0.1.evil.example:80', 'https://functionstore.tools.evil.example']) {
    assert.equal(OPTIONS(req(o, null, 'OPTIONS')).headers.get('access-control-allow-origin'), null, o);
  }
});

await check('GET says whether a model is configured', async () => {
  const saved = process.env.CHAT_MODEL;
  delete process.env.CHAT_MODEL;
  assert.deepEqual(await GET(req('https://functionstore.tools', null, 'GET')).json(), { ready: false });
  process.env.CHAT_MODEL = 'test/none';
  assert.deepEqual(await GET(req('https://functionstore.tools', null, 'GET')).json(), { ready: true });
  if (saved === undefined) delete process.env.CHAT_MODEL; else process.env.CHAT_MODEL = saved;
});

await check('POST without CHAT_MODEL answers 503', async () => {
  const saved = process.env.CHAT_MODEL;
  delete process.env.CHAT_MODEL;
  const r = await POST(req('https://functionstore.tools', JSON.stringify({ messages: [] })));
  assert.equal(r.status, 503);
  if (saved !== undefined) process.env.CHAT_MODEL = saved;
});

await check('POST with a bad body answers 400', async () => {
  process.env.CHAT_MODEL = 'test/none';
  const r = await POST(req('https://functionstore.tools', '{not json'));
  assert.equal(r.status, 400);
  delete process.env.CHAT_MODEL;
});

console.log(failed ? `\n${failed} failed` : '\nall passed');
process.exit(failed ? 1 : 0);
