import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from '../../services/api/server.js';

async function withServer(fn) {
  const server = createServer();
  await new Promise((resolve) => server.listen(0, resolve));
  const { port } = server.address();
  const baseUrl = `http://127.0.0.1:${port}`;
  try { await fn(baseUrl); } finally { await new Promise((resolve) => server.close(resolve)); }
}

test('decision + event + audit flow works end-to-end', async () => {
  await withServer(async (baseUrl) => {
    const decisionRes = await fetch(`${baseUrl}/v1/decisions/evaluate`, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ appId: 'employee-portal', channel: 'web', slot: 'dashboard-hero', employeeId: 'E999', context: { roleContext: { isManager: false } } })
    });
    assert.equal(decisionRes.status, 200);
    const decision = await decisionRes.json();
    assert.ok(decision.decisionId);

    const eventRes = await fetch(`${baseUrl}/v1/events/interactions`, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ eventType: 'impression', employeeId: 'E999', slot: 'dashboard-hero', timestamp: new Date().toISOString(), candidateId: decision.candidateId })
    });
    assert.equal(eventRes.status, 202);

    const auditRes = await fetch(`${baseUrl}/v1/audit`);
    assert.equal(auditRes.status, 200);
    const audits = await auditRes.json();
    assert.ok(audits.find((a) => a.decisionId === decision.decisionId));
  });
});
