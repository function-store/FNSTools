// POST /api/discord/ -- the Discord interactions endpoint for /findtool.
// Discord calls it for every use of the command; there is no bot process.
// Set it in the developer portal WITH the trailing slash (vercel.json's
// trailingSlash would answer the bare path with a redirect Discord does not
// follow). Design: docs/PickerChatbot.md.
//
// Needs DISCORD_PUBLIC_KEY and DISCORD_APPLICATION_ID (both shown in the
// portal, neither secret) and the finder's CHAT_MODEL. No bot token: the
// answer is written through the interaction's own webhook token.
import { waitUntil } from '@vercel/functions';
import { answer } from './_lib/finder.js';
import { take, whenAgain } from './_lib/limit.js';
import {
  isFromDiscord, problemOf, isPrivate, ephemeralFlags, toMessage, followupUrl,
  COMMAND, PING, APPLICATION_COMMAND, PONG, DEFERRED_CHANNEL_MESSAGE, CHANNEL_MESSAGE,
} from './_lib/discord.js';

const reply = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { 'Content-Type': 'application/json' },
});

/** Runs the finder and replaces the deferred reply with the answer. */
export async function finish(interaction, problem, { model, fetchImpl = fetch } = {}) {
  let msg;
  try {
    const out = await answer({ messages: [{ role: 'user', content: problem }], access: 'free' }, { model });
    msg = out.error ? { content: out.error } : toMessage(problem, out);
  } catch (e) {
    console.error('discord findtool failed:', e && e.name, e && e.message);
    msg = { content: /rate ?limit/i.test(String(e && e.message))
      ? 'The tool finder is busy right now. Try again in a minute.'
      : 'The tool finder could not answer this time. Try again, or browse https://functionstore.tools/get/' };
  }
  const r = await fetchImpl(followupUrl(process.env.DISCORD_APPLICATION_ID || interaction.application_id, interaction.token), {
    method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(msg),
  });
  if (!r.ok) console.error('discord followup failed:', r.status);
}

export async function POST(request) {
  const raw = await request.text();
  if (!isFromDiscord(process.env.DISCORD_PUBLIC_KEY, request.headers.get('x-signature-ed25519'),
    request.headers.get('x-signature-timestamp'), raw)) {
    return new Response('invalid request signature', { status: 401 });
  }
  let interaction;
  try { interaction = JSON.parse(raw); } catch { return new Response('bad body', { status: 400 }); }

  if (interaction.type === PING) return reply({ type: PONG });

  if (interaction.type === APPLICATION_COMMAND && interaction.data && interaction.data.name === COMMAND) {
    const flags = ephemeralFlags(isPrivate(interaction));
    const problem = problemOf(interaction);
    const model = process.env.CHAT_MODEL;
    if (!model) return reply({ type: CHANNEL_MESSAGE, data: { content: 'The tool finder is not switched on yet.', flags: 64 } });
    if (!problem) return reply({ type: CHANNEL_MESSAGE, data: { content: `Tell me what gets in your way: /${COMMAND} problem: …`, flags: 64 } });
    // per Discord user, before any model work; the answer to a limited
    // caller is private, so it never lands in the channel
    const who = (interaction.member && interaction.member.user && interaction.member.user.id)
      || (interaction.user && interaction.user.id) || '';
    const lim = await take('discord', who);
    if (!lim.ok) {
      return reply({ type: CHANNEL_MESSAGE, data: { flags: 64,
        content: `You have used /${COMMAND} a lot in a short time. Try again ${whenAgain(lim.retryAfter)}.` } });
    }
    // Discord wants an answer within 3 s; the finder takes longer. Say
    // "thinking" now and edit the reply when the answer is ready.
    waitUntil(finish(interaction, problem, { model }));
    return reply({ type: DEFERRED_CHANNEL_MESSAGE, data: { flags } });
  }
  return reply({ type: CHANNEL_MESSAGE, data: { content: 'Unknown command.', flags: 64 } });
}
