import { createHmac } from 'node:crypto';

function getAuthHeaders(body, auth = {}) {
  const token = auth.token ?? process.env.GENUI_API_TOKEN ?? 'dev-token';
  const signingKey = auth.signingKey ?? process.env.GENUI_SIGNING_KEY;
  const headers = {
    authorization: `Bearer ${token}`
  };

  if (signingKey) {
    headers['x-genui-signature'] = createHmac('sha256', signingKey).update(body).digest('hex');
  }

  return headers;
}

export async function evaluateDecision(baseUrl, request, auth) {
  const body = JSON.stringify(request);
  const headers = { 'content-type': 'application/json', ...getAuthHeaders(body, auth) };
  const res = await fetch(`${baseUrl}/v1/decisions/evaluate`, { method: 'POST', headers, body });
  if (!res.ok) throw new Error('decision failed');
  return res.json();
}
export async function emitEvent(baseUrl, event, auth) {
  const body = JSON.stringify(event);
  const headers = { 'content-type': 'application/json', ...getAuthHeaders(body, auth) };
  const res = await fetch(`${baseUrl}/v1/events/interactions`, { method: 'POST', headers, body });
  if (!res.ok) throw new Error('event failed');
  return res.json();
}
