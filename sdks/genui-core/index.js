export async function evaluateDecision(baseUrl, request) {
  const res = await fetch(`${baseUrl}/v1/decisions/evaluate`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(request) });
  if (!res.ok) throw new Error('decision failed');
  return res.json();
}
export async function emitEvent(baseUrl, event) {
  const res = await fetch(`${baseUrl}/v1/events/interactions`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(event) });
  if (!res.ok) throw new Error('event failed');
  return res.json();
}
