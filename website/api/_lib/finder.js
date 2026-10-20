// The /get tool finder: a reader describes what gets in their way in
// TouchDesigner, a model grounded in the catalog and the tool docs answers
// with picks. Design and the owner's decisions: docs/PickerChatbot.md.
//
// Kept apart from api/chat.js (the HTTP wrapper) so tools/test-chat.mjs can
// drive it with a mock model. The underscore folder is not a route.
import { generateText, tool, isStepCount, hasToolCall } from 'ai';
import { z } from 'zod';
import { readFileSync } from 'node:fs';

// Read through import.meta.url so Vercel's file tracer bundles it with the
// function. Written by tools/build-site.mjs.
const data = JSON.parse(readFileSync(new URL('../_data/chat.json', import.meta.url), 'utf8'));

// Caps on what one request may cost. A conversation past these is cut from
// the front, never refused: the newest turns are the ones that matter.
export const LIMITS = {
  messages: 12,
  messageChars: 1500,
  totalChars: 8000,
  steps: 6,
  outputTokens: 1200,
  picks: 8,
  searchHits: 8,
  docChars: 6000,
  timeoutMs: 25000,
};

const TOOLS = data.tools;
const byName = new Map(TOOLS.map((t) => [t.name.toLowerCase(), t]));
const byTitle = new Map(TOOLS.map((t) => [t.title.toLowerCase(), t]));

/** Finds a catalog tool by package name or public title, or null. */
export function findTool(name) {
  const k = String(name || '').trim().toLowerCase();
  return byName.get(k) || byTitle.get(k) || null;
}

const STOP = new Set(('the and for with that this from into what when where which how '
  + 'can you your are was its have has not but all any out get use using want need '
  + 'make lot lots like just some more then than them they there their touchdesigner td')
  .split(' '));

function terms(query) {
  return [...new Set(String(query || '').toLowerCase()
    .split(/[^a-z0-9+]+/)
    .filter((w) => w.length >= 3 && !STOP.has(w)))];
}

function hits(text, ts) {
  const s = String(text || '').toLowerCase();
  let n = 0;
  for (const t of ts) if (s.includes(t)) n += 1;
  return n;
}

function excerpt(text, ts, size = 240) {
  const s = String(text || '').replace(/\s+/g, ' ');
  const low = s.toLowerCase();
  let at = -1;
  for (const t of ts) {
    const i = low.indexOf(t);
    if (i !== -1 && (at === -1 || i < at)) at = i;
  }
  const start = Math.max(0, at - 60);
  return (start ? '...' : '') + s.slice(start, start + size) + (start + size < s.length ? '...' : '');
}

/** Keyword search over every public tool's doc sections. */
export function searchDocs(query) {
  const ts = terms(query);
  if (!ts.length) return { results: [], note: 'No searchable words in the query.' };
  const scored = [];
  for (const t of TOOLS) {
    const head = hits(`${t.title} ${t.name} ${t.description} ${t.fits.join(' ')}`, ts) * 2
      + hits(t.features.join(' '), ts) * 2;
    for (const s of t.sections) {
      const score = head + hits(s.heading, ts) * 3 + hits(s.text, ts);
      if (score > 0) scored.push({ score, t, s });
    }
    if (!t.sections.length && head > 0) scored.push({ score: head, t, s: { heading: '', text: t.description } });
  }
  scored.sort((a, b) => b.score - a.score);
  const seen = new Set();
  const results = [];
  for (const { t, s } of scored) {
    const key = `${t.name}#${s.heading}`;
    if (seen.has(key)) continue;
    seen.add(key);
    results.push({ name: t.name, title: t.title, section: s.heading, excerpt: excerpt(s.text, ts) });
    if (results.length >= LIMITS.searchHits) break;
  }
  return { results };
}

/** One tool's doc, trimmed to fit a model's context. */
export function readDoc(name) {
  const t = findTool(name);
  if (!t) return { error: `No tool called "${name}" in the catalog.` };
  let body = '';
  for (const s of t.sections) {
    const add = `## ${s.heading}\n${s.text}\n\n`;
    if (body.length + add.length > LIMITS.docChars) {
      body += `## ${s.heading}\n(cut for length; the docs page has the rest)\n`;
      break;
    }
    body += add;
  }
  return {
    name: t.name, title: t.title, access: t.access, tier: t.tier, url: t.url,
    description: t.description, features: t.features, hotkeys: t.hotkeys, doc: body.trim(),
  };
}

/** Keeps only catalog tools, once each, at most LIMITS.picks. */
export function validatePicks(picks) {
  const accepted = [];
  const dropped = [];
  const seen = new Set();
  for (const p of picks || []) {
    const t = findTool(p && p.name);
    if (!t) { dropped.push(String((p && p.name) || '')); continue; }
    if (seen.has(t.name) || accepted.length >= LIMITS.picks) continue;
    seen.add(t.name);
    accepted.push({
      name: t.name, title: t.title, url: t.url, access: t.access, tier: t.tier,
      why: String((p && p.why) || '').trim().slice(0, 300),
    });
  }
  return { accepted, dropped };
}

function catalogLines() {
  return TOOLS.map((t) => [
    t.name, t.title, t.category,
    t.access === 'patreon' ? `Patreon${t.tier ? ` ${t.tier}` : ''}` : 'free',
    t.description, t.fits.join(','),
  ].join(' | ')).join('\n');
}

const CATALOG = catalogLines();

/** The system instructions; `access` is what this reader can install. */
export function instructions(access) {
  const can = access === 'patreon'
    ? 'This reader is a Patreon supporter and can install Patreon tools.'
    : 'This reader can install free tools. Patreon tools need a Patreon membership.';
  return `You are the tool finder on the FNSTools website. FNSTools is a toolkit of
add-on tools for TouchDesigner. A reader tells you what they struggle with or
want to do in TouchDesigner, and you pick the FNSTools tools that help.

Rules:
- Only recommend tools from the catalog below, by their exact name. Never invent a tool.
- Before recommending a tool for anything its one-line description does not
  already say, call readDoc on it. Use searchDocs to find candidates.
- Give your answer by calling recommend once, with each pick's reason written
  in the reader's own terms and taken from the tool's doc. Keep the reply short.
- Free and Patreon tools are both fair picks. Say plainly when a pick is a Patreon tool.
  ${can}
- If nothing in the catalog fits, say so and call recommend with no picks.
  Do not stretch a tool to fit.
- Ask at most one clarifying question, and only when the request is too vague to pick anything.
- A how-to question about an FNSTools tool gets a few lines taken from that
  tool's doc (call readDoc) and a link to its docs page. Never answer from memory.
- You do not give general TouchDesigner help. For questions about
  TouchDesigner itself, say briefly that you only know FNSTools and point to
  https://docs.derivative.ca or https://forum.derivative.ca.
- Write in English, in plain sentences, no headings.

Catalog (name | title | category | access | description | tags):
${CATALOG}`;
}

/** Trims a conversation to the caps, newest turns kept. */
export function clampMessages(messages) {
  const clean = (Array.isArray(messages) ? messages : [])
    .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
    .map((m) => ({ role: m.role, content: m.content.slice(0, LIMITS.messageChars) }))
    .slice(-LIMITS.messages);
  let total = 0;
  const kept = [];
  for (let i = clean.length - 1; i >= 0; i -= 1) {
    total += clean[i].content.length;
    if (total > LIMITS.totalChars) break;
    kept.unshift(clean[i]);
  }
  while (kept.length && kept[0].role !== 'user') kept.shift();
  return kept;
}

/**
 * Answers one turn. Returns {reply, picks, dropped, read}: picks are
 * catalog-validated, read names the docs the model opened.
 */
export async function answer({ messages, access }, { model, abortSignal } = {}) {
  const msgs = clampMessages(messages);
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user') {
    return { error: 'The conversation must end with a message from you.' };
  }
  const read = [];
  let final = null;
  const result = await generateText({
    model,
    instructions: instructions(access),
    messages: msgs,
    maxOutputTokens: LIMITS.outputTokens,
    timeout: LIMITS.timeoutMs,
    abortSignal,
    stopWhen: [hasToolCall('recommend'), isStepCount(LIMITS.steps)],
    tools: {
      searchDocs: tool({
        description: 'Keyword search across every FNSTools tool doc. Returns matching tools and sections.',
        inputSchema: z.object({ query: z.string().describe('Words describing the problem or feature') }),
        execute: async ({ query }) => searchDocs(query),
      }),
      readDoc: tool({
        description: 'Read one FNSTools tool\'s documentation by its catalog name.',
        inputSchema: z.object({ name: z.string().describe('Exact catalog name, e.g. FNS_BorderlessTD') }),
        execute: async ({ name }) => {
          const d = readDoc(name);
          if (!d.error) read.push(d.name);
          return d;
        },
      }),
      recommend: tool({
        description: 'Give the final answer: a short reply and the picked tools. Call once, last.',
        inputSchema: z.object({
          reply: z.string().describe('A short answer to the reader, plain sentences'),
          picks: z.array(z.object({
            name: z.string().describe('Exact catalog name'),
            why: z.string().describe('One sentence in the reader\'s terms'),
          })).describe('Best first; empty when nothing fits or when only answering a question'),
        }),
        execute: async ({ reply, picks }) => {
          const v = validatePicks(picks);
          final = { reply: String(reply || '').trim(), ...v };
          return { accepted: v.accepted.map((p) => p.name), dropped: v.dropped };
        },
      }),
    },
  });
  if (final) {
    return { reply: final.reply || result.text.trim(), picks: final.accepted, dropped: final.dropped, read };
  }
  return { reply: result.text.trim(), picks: [], dropped: [], read };
}
