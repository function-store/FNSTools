// Registers (or updates) the /findtool slash command with Discord. Run it
// once from your own machine; run it again only when the command's options
// change. The bot token is used for this call alone and never goes to Vercel.
//
//   DISCORD_APPLICATION_ID=... DISCORD_BOT_TOKEN=... node tools/register-discord-command.mjs
//   add DISCORD_GUILD_ID=... to register it on one server only (shows up at
//   once; global commands can take a while to appear everywhere)
//
// docs/PickerChatbot.md
import { COMMAND, OPTION } from '../api/_lib/discord.js';

const app = process.env.DISCORD_APPLICATION_ID;
const token = process.env.DISCORD_BOT_TOKEN;
const guild = process.env.DISCORD_GUILD_ID;
if (!app || !token) {
  console.error('Set DISCORD_APPLICATION_ID and DISCORD_BOT_TOKEN (from the Discord developer portal).');
  process.exit(1);
}

const command = {
  name: COMMAND,
  type: 1,
  description: 'Describe what gets in your way in TouchDesigner; get FNSTools that help.',
  // usable in servers that add the app, and by people who add it to their account
  integration_types: [0, 1],
  contexts: [0, 1, 2],
  options: [
    {
      type: 3, name: OPTION, required: true, max_length: 500,
      description: 'What you struggle with or want to do, in your own words',
    },
    {
      type: 5, name: 'private', required: false,
      description: 'Only you see the answer',
    },
  ],
};

const url = guild
  ? `https://discord.com/api/v10/applications/${app}/guilds/${guild}/commands`
  : `https://discord.com/api/v10/applications/${app}/commands`;
// PUT replaces the app's command list with exactly this one
const r = await fetch(url, {
  method: 'PUT',
  headers: { Authorization: `Bot ${token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify([command]),
});
const text = await r.text();
if (!r.ok) {
  console.error(`Discord said ${r.status}: ${text}`);
  process.exit(1);
}
console.log(`Registered /${COMMAND} ${guild ? `on server ${guild}` : 'globally'}.`);
