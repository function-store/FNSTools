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
  steps: 5,
  reads: 3,
  outputTokens: 1200,
  picks: 8,
  searchHits: 8,
  docChars: 4000,
  timeoutMs: 40000,
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

// What the model is given up front, by context mode (docs/PickerChatbot.md,
// "Search or long context"): 'search' gives the catalog lines and lets it
// search and read docs with tools; 'features' adds every tool's feature
// lines; 'docs' adds every tool's whole doc. The last two answer in one
// request with no searching.
export const CONTEXTS = ['search', 'features', 'docs'];

function featureBlock() {
  return TOOLS.map((t) => [`## ${t.name} (${t.title})`, t.description,
    ...t.features.map((f) => `- ${f}`), ...t.hotkeys.map((h) => `- key ${h}`)]
    .join('\n')).join('\n\n');
}

function docsBlock() {
  return TOOLS.map((t) => [`## ${t.name} (${t.title}) ${t.url}`, t.description,
    ...t.features.map((f) => `- ${f}`),
    ...t.sections.map((s) => `### ${s.heading}\n${s.text}`)].join('\n')).join('\n\n');
}

const CATALOG = catalogLines();
let FEATURES = null;
let DOCS = null;

/**
 * The system instructions. `access` is what this reader can install;
 * `shown` names the tools already offered in this conversation, sent by the
 * page as a list so the history itself stays plain dialogue (picks written
 * into an assistant turn were copied back as a plain-text answer).
 */
export function instructions(access, shown = [], context = 'search') {
  const can = access === 'patreon'
    ? 'This reader is a Patreon supporter and can install Patreon tools.'
    : 'This reader can install free tools. Patreon tools need a Patreon membership.';
  const already = shown.length
    ? `

Already offered in this conversation: ${shown.join(', ')}. When the reader asks for more,
pick other tools that still fit; do not offer these again unless they ask about one.`
    : '';
  const search = context === 'search';
  let reference = '';
  if (context === 'features') {
    FEATURES = FEATURES || featureBlock();
    reference = `\n\nEvery tool's features (the catalog name, then what it does):\n\n${FEATURES}`;
  } else if (context === 'docs') {
    DOCS = DOCS || docsBlock();
    reference = `\n\nEvery tool's documentation (the catalog name, title and docs page, then the doc):\n\n${DOCS}`;
  }
  const lookup = search
    ? `- Before recommending a tool for anything its one-line description does not
  already say, call readDoc on it. Use searchDocs to find candidates.
- You may read at most ${LIMITS.reads} docs; then recommend.
- A how-to question about an FNSTools tool gets a few lines taken from that
  tool's doc (call readDoc) and a link to its docs page. Never answer from memory.`
    : `- Everything you know about the tools is below the catalog. Judge every
  pick against it, and answer straight away with recommend.
- A how-to question about an FNSTools tool gets a few lines taken from that
  tool's ${context === 'docs' ? 'doc below' : 'features below'} and a link to its docs page
  (https://functionstore.tools/docs/<slug>/ as the catalog gives it). Never answer from memory.`;
  return `You are the tool finder on the FNSTools website. FNSTools is a toolkit of
add-on tools for TouchDesigner. A reader tells you what they struggle with or
want to do in TouchDesigner, and you pick the FNSTools tools that help.

First, before anything else, decide whether the reader's latest message
names a concrete problem or task ("my timeline takes too much room", "I want
to map my MIDI controller") or only a broad area of work ("I do live shows",
"I make generative art", "I build installations", "make TouchDesigner
better"). For a broad area, do not ${search ? 'search and do not ' : ''}pick: call recommend
with no picks and a reply that asks which part they mean, offering three or
four concrete parts the catalog covers. For live shows that could be:
controlling parameters from MIDI or OSC, sending output to projectors or
screens, switching scenes or inputs, keeping the show running smoothly. If
your previous turn already asked such a question, pick from their answer.

Rules:
- Only recommend tools from the catalog below, by their exact name. Never invent a tool.
${lookup}
- Every turn ends with exactly one recommend call: picks, a clarifying
  question, a how-to answer and a decline all go through it (with picks
  empty when there are none). Never answer in plain text.
- Each pick's reason is written in the reader's own terms and taken from the
  tool's doc. Keep the reply to two or three sentences; the picks are shown
  under it, so do not list them again in the reply.
- A pick must directly do what the reader asked for. Sharing a word with the
  request (camera, sequence, colour) is not a fit. A tool that only helps
  around the edges is not a pick: leave it out. Fewer, exact picks beat a long list.
- Free and Patreon tools are both fair picks. Say plainly when a pick is a Patreon tool.
  ${can}
- If nothing in the catalog does what they asked, say so plainly, call
  recommend with no picks, and suggest the community page
  https://functionstore.tools/community/ or the Derivative forum.
- Ask at most one clarifying question in a row.
- You do not give general TouchDesigner help. For questions about
  TouchDesigner itself, say briefly that you only know FNSTools and point to
  https://docs.derivative.ca or https://forum.derivative.ca.
- Write in English, in plain sentences: no headings, no markdown, no backticks.
  In the reply, call a tool by its title (BorderlessTD), never its catalog
  name (FNS_BorderlessTD); the catalog name is only for tool calls.

Catalog (name | title | category | access | description | tags):
${CATALOG}${reference}${already}`;
}

/** Strips the markdown a model writes anyway: emphasis, backticks, bullets. */
export function plainReply(text) {
  return String(text || '')
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/`([^`]*)`/g, '$1')
    .replace(/^[ \t]*[*-][ \t]+/gm, '- ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/** Keeps the names of tools already offered that the catalog knows. */
function shownTitles(shown) {
  const out = [];
  for (const n of (Array.isArray(shown) ? shown : []).slice(0, 40)) {
    const t = findTool(n);
    if (t && !out.includes(t.name)) out.push(t.name);
  }
  return out;
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
export async function answer({ messages, access, shown }, { model, abortSignal, context = 'search' } = {}) {
  const msgs = clampMessages(messages);
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user') {
    return { error: 'The conversation must end with a message from you.' };
  }
  const read = [];
  const already = shownTitles(shown);
  let final = null;
  let reads = 0;
  const tools = {
    searchDocs: tool({
      description: 'Keyword search across every FNSTools tool doc. Returns matching tools and sections.',
      inputSchema: z.object({ query: z.string().describe('Words describing the problem or feature') }),
      execute: async ({ query }) => searchDocs(query),
    }),
    readDoc: tool({
      description: 'Read one FNSTools tool\'s documentation by its catalog name.',
      inputSchema: z.object({ name: z.string().describe('Exact catalog name, e.g. FNS_BorderlessTD') }),
      execute: async ({ name }) => {
        reads += 1;
        if (reads > LIMITS.reads) return { error: `Read limit reached (${LIMITS.reads}). Call recommend now.` };
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
        // Never offer again what this conversation already offered: the
        // instructions ask, and the model still repeats (TDXMap twice).
        const v = validatePicks((picks || []).filter((p) => {
          const t = findTool(p && p.name);
          return !(t && already.includes(t.name));
        }));
        final = { reply: String(reply || '').trim(), ...v };
        return { accepted: v.accepted.map((p) => p.name), dropped: v.dropped };
      },
    }),
  };
  const base = {
    model,
    instructions: instructions(access, already, context),
    messages: msgs,
    maxOutputTokens: LIMITS.outputTokens,
    timeout: LIMITS.timeoutMs,
    abortSignal,
    reasoning: 'low',
    tools,
  };
  let result;
  try {
    result = context !== 'search' ? await generateText({
      ...base,
      toolChoice: { type: 'tool', toolName: 'recommend' },
      activeTools: ['recommend'],
      stopWhen: isStepCount(1),
    }) : await generateText({
      ...base,
      // Every step calls a tool, so every turn ends in recommend: a turn
      // answered in plain text draws no rows on the page.
      toolChoice: 'required',
      stopWhen: [hasToolCall('recommend'), isStepCount(LIMITS.steps)],
      // The last step can only answer: a model still searching when the
      // steps run out would otherwise end with no picks and no reply.
      prepareStep: ({ stepNumber }) => (stepNumber >= LIMITS.steps - 1
        ? { toolChoice: { type: 'tool', toolName: 'recommend' }, activeTools: ['recommend'] }
        : undefined),
    });
  } catch (e) {
    // A model that answers in text anyway makes the SDK throw on the
    // required tool choice. Ask once more, with recommend the only option.
    if (final || !/tool choice was required|did not contain a (tool call|call to the required tool)/i.test(String(e && e.message))) throw e;
    result = await generateText({
      ...base,
      toolChoice: { type: 'tool', toolName: 'recommend' },
      activeTools: ['recommend'],
      stopWhen: isStepCount(1),
    });
  }
  if (final) {
    return { reply: plainReply(final.reply || result.text), picks: final.accepted, dropped: final.dropped, read, steps: result.steps.length, usage: result.totalUsage };
  }
  return { reply: plainReply(result.text), picks: [], dropped: [], read, steps: result.steps.length, usage: result.totalUsage };
}
