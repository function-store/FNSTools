// The Discord side of the tool finder: Discord's interaction signature check,
// and turning a finder answer into a Discord message. HTTP lives in
// api/discord.js; the finder itself in ./finder.js. docs/PickerChatbot.md.
import crypto from 'node:crypto';

export const COMMAND = 'findtool';
export const OPTION = 'problem';
// Discord interaction types and response types we use
export const PING = 1;
export const APPLICATION_COMMAND = 2;
export const PONG = 1;
export const DEFERRED_CHANNEL_MESSAGE = 5;
export const CHANNEL_MESSAGE = 4;
const EPHEMERAL = 64;

// DER prefix that turns a raw 32-byte Ed25519 key into an SPKI public key
const ED25519_SPKI = Buffer.from('302a300506032b6570032100', 'hex');

/**
 * Whether a request really comes from Discord: an Ed25519 signature over
 * the timestamp and the raw body, checked against the app's public key
 * (hex, from the developer portal). Discord refuses an endpoint that
 * accepts a bad signature, and sends one on purpose to test it.
 */
export function isFromDiscord(publicKeyHex, signatureHex, timestamp, rawBody) {
  if (!publicKeyHex || !signatureHex || !timestamp) return false;
  try {
    const key = crypto.createPublicKey({
      key: Buffer.concat([ED25519_SPKI, Buffer.from(publicKeyHex, 'hex')]),
      format: 'der', type: 'spki',
    });
    return crypto.verify(null, Buffer.from(timestamp + rawBody),
      key, Buffer.from(signatureHex, 'hex'));
  } catch {
    return false;
  }
}

/** The text a /findtool call carries, or ''. */
export function problemOf(interaction) {
  const opts = (interaction && interaction.data && interaction.data.options) || [];
  const o = opts.find((x) => x && x.name === OPTION);
  return o && typeof o.value === 'string' ? o.value.trim() : '';
}

/** Whether the caller asked for an answer only they can see. */
export function isPrivate(interaction) {
  const opts = (interaction && interaction.data && interaction.data.options) || [];
  const o = opts.find((x) => x && x.name === 'private');
  return !!(o && o.value === true);
}

export function ephemeralFlags(priv) { return priv ? EPHEMERAL : 0; }

const clip = (s, n) => (String(s || '').length > n ? `${String(s).slice(0, n - 1)}…` : String(s || ''));

/**
 * A finder answer as a Discord message: the reply as text, one embed field
 * per pick (title, Patreon label, reason, docs link), and the way to install.
 * Every length is held under Discord's limits.
 */
export function toMessage(problem, out) {
  const picks = (out && out.picks) || [];
  let content = clip(out && out.reply, 1500);
  if (!picks.length && content.trim().endsWith('?')) {
    content += `\n\nRun /${COMMAND} again with a bit more detail.`;
  }
  const msg = {
    content: `> ${clip(problem.replace(/\n+/g, ' '), 200)}\n${content}`,
    allowed_mentions: { parse: [] },
  };
  if (picks.length) {
    msg.embeds = [{
      color: 0xf5c518,
      fields: picks.slice(0, 8).map((p) => ({
        name: clip(`${p.title}${p.access === 'patreon' ? ' · Patreon' : ''}`, 256),
        value: clip(`${p.why || ''}\n[Docs](${p.url})`, 1024),
      })),
      footer: { text: 'Install from functionstore.tools/get' },
      url: 'https://functionstore.tools/get/',
      title: 'FNSTools tool finder',
    }];
  }
  return msg;
}

/** The PATCH that replaces the deferred "thinking" reply with the answer. */
export function followupUrl(applicationId, token) {
  return `https://discord.com/api/v10/webhooks/${applicationId}/${token}/messages/@original`;
}
