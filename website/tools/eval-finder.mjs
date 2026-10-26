// Scores the /get tool finder against tools/finder-eval.json with a real
// model, once per context mode, and prints a table. Needs Gateway auth in
// the environment (VERCEL_OIDC_TOKEN from `vercel env pull`, or
// AI_GATEWAY_API_KEY) and api/_data/chat.json (`npm run pages`).
//
//   node tools/eval-finder.mjs [--model google/gemini-2.5-flash]
//        [--modes search,features,docs] [--set basic|hard] [--only id,id] [--rpm 5] [--out file.json]
//
// --rpm paces the model requests: the free Gateway tier allows 5 a minute.
import { readFileSync, writeFileSync } from 'node:fs';
import { answer, CONTEXTS } from '../api/_lib/finder.js';

const arg = (k, d) => {
  const i = process.argv.indexOf(`--${k}`);
  return i === -1 ? d : process.argv[i + 1];
};
const model = arg('model', process.env.CHAT_MODEL || 'google/gemini-2.5-flash');
const modes = arg('modes', CONTEXTS.join(',')).split(',');
const only = arg('only', '') ? arg('only', '').split(',') : null;
const rpm = Number(arg('rpm', '5'));
const out = arg('out', '');
const suite = JSON.parse(readFileSync(new URL('./finder-eval.json', import.meta.url), 'utf8'));
const set = arg('set', '');
const cases = suite.cases.filter((c) => (!only || only.includes(c.id)) && (!set || c.set === set));

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const stamps = [];
async function pace(requests) {
  // keep at most `rpm` requests in any 60 s window
  for (let i = 0; i < requests; i += 1) {
    while (stamps.length >= rpm && Date.now() - stamps[stamps.length - rpm] < 61000) {
      await sleep(61000 - (Date.now() - stamps[stamps.length - rpm]));
    }
    stamps.push(Date.now());
  }
}

function judge(c, r) {
  if (r.error) return { pass: false, note: `error: ${r.error}` };
  const names = r.picks.map((p) => p.name);
  const bad = names.filter((n) => (c.bad || []).includes(n));
  const known = new Set([...(c.must || []), ...(c.good || [])]);
  const other = names.filter((n) => !known.has(n) && !bad.includes(n));
  let pass;
  if (c.kind === 'pick') pass = names.some((n) => c.must.includes(n));
  else if (c.kind === 'ask') pass = !names.length && r.reply.includes('?');
  else if (c.kind === 'decline') pass = !names.length;
  // the docs link may be in the reply or on the pick's row (both pages and
  // Discord show every pick with its docs link)
  else if (c.kind === 'howto') pass = r.reply.includes(`/docs/${c.slug}/`)
    || r.picks.some((p) => String(p.url || '').includes(`/docs/${c.slug}/`));
  if (bad.length) pass = false;
  const starts = r.picks.filter((p) => p.start).length;
  const note = [names.length ? `picks ${names.join(', ')}` : 'no picks',
    names.length ? `try-it ${starts}/${names.length}` : '',
    r.startsDropped ? `DROPPED-START ${r.startsDropped}` : '',
    bad.length ? `BAD ${bad.join(', ')}` : '', other.length ? `unlisted ${other.join(', ')}` : '']
    .filter(Boolean).join('; ');
  return { pass, note };
}

const rows = [];
for (const mode of modes) {
  for (const c of cases) {
    const messages = c.turns || [{ role: 'user', content: c.say }];
    // search mode spends up to 5 requests, the others 1 (2 on a retry)
    await pace(mode === 'search' ? 4 : 1);
    const t0 = Date.now();
    let r;
    for (let attempt = 0; attempt < 2; attempt += 1) {
      try {
        r = await answer({ messages, access: c.access || 'free', shown: [] }, { model, context: mode });
        break;
      } catch (e) {
        r = { error: String(e && e.message).split('\n')[0].slice(0, 160) };
        if (!/rate ?limit/i.test(r.error)) break;
        await sleep(62000);
      }
    }
    const secs = (Date.now() - t0) / 1000;
    const j = judge(c, r);
    const inTok = r.usage && (r.usage.inputTokens && (r.usage.inputTokens.total ?? r.usage.inputTokens));
    rows.push({ mode, id: c.id, kind: c.kind, pass: j.pass, secs, steps: r.steps, inTok, note: j.note, reply: r.reply, picks: r.picks, startsDropped: r.startsDropped || 0 });
    console.log(`${j.pass ? 'PASS' : 'FAIL'}  ${mode.padEnd(8)} ${c.id.padEnd(17)} ${secs.toFixed(1).padStart(5)}s `
      + `${String(r.steps ?? '-').padStart(2)} steps ${String(inTok ?? '-').padStart(7)} in  ${j.note}`);
  }
}

console.log('\nmode      passed   avg s   avg steps   avg input tokens');
for (const mode of modes) {
  const m = rows.filter((x) => x.mode === mode);
  const avg = (f) => m.reduce((a, x) => a + (Number(f(x)) || 0), 0) / m.length;
  console.log(`${mode.padEnd(9)} ${String(m.filter((x) => x.pass).length).padStart(2)}/${m.length}`
    + `   ${avg((x) => x.secs).toFixed(1).padStart(5)}   ${avg((x) => x.steps).toFixed(1).padStart(9)}`
    + `   ${Math.round(avg((x) => x.inTok)).toString().padStart(16)}`);
}
if (out) writeFileSync(out, JSON.stringify({ model, rows }, null, 1));
