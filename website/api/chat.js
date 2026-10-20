// POST /api/chat -- the /get tool finder's endpoint. The logic lives in
// _lib/finder.js; this file is HTTP only: CORS, body parsing, errors.
// Design: docs/PickerChatbot.md.
//
// The model is a Vercel AI Gateway id in CHAT_MODEL (e.g. "google/<model>").
// On Vercel the Gateway authenticates with the project's OIDC token; locally
// it reads AI_GATEWAY_API_KEY. With no CHAT_MODEL the endpoint answers 503,
// so an unconfigured deploy says so instead of guessing a model.
import { answer } from './_lib/finder.js';

// The site, its Preview deployments, and the installer, which serves the
// same picker from http://127.0.0.1:<port>/ inside TouchDesigner.
const ALLOWED = [
  /^https:\/\/functionstore\.tools$/,
  /^https:\/\/fnstools-[a-z0-9-]+\.vercel\.app$/,
  /^http:\/\/(127\.0\.0\.1|localhost):\d{1,5}$/,
];

function cors(origin) {
  const h = { Vary: 'Origin' };
  if (origin && ALLOWED.some((r) => r.test(origin))) {
    h['Access-Control-Allow-Origin'] = origin;
    h['Access-Control-Allow-Methods'] = 'POST, OPTIONS';
    h['Access-Control-Allow-Headers'] = 'Content-Type';
    h['Access-Control-Max-Age'] = '600';
  }
  return h;
}

function json(status, body, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...cors(origin) },
  });
}

export function OPTIONS(request) {
  return new Response(null, { status: 204, headers: cors(request.headers.get('origin')) });
}

export async function POST(request) {
  const origin = request.headers.get('origin');
  const model = process.env.CHAT_MODEL;
  if (!model) return json(503, { error: 'The tool finder is not configured yet.' }, origin);
  let body;
  try {
    body = await request.json();
  } catch {
    return json(400, { error: 'Send a JSON body: {messages, access}.' }, origin);
  }
  const access = body && body.access === 'patreon' ? 'patreon' : 'free';
  try {
    const out = await answer({ messages: body && body.messages, access },
      { model, abortSignal: request.signal });
    if (out.error) return json(400, out, origin);
    return json(200, out, origin);
  } catch (e) {
    console.error('chat failed:', e && e.name, e && e.message);
    return json(502, { error: 'The tool finder could not answer. Try again, or use the questions instead.' }, origin);
  }
}
