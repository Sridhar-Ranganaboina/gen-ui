import { describe, it, mock } from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { emitEvent, evaluateDecision } from '../../sdks/genui-core/index.js';

describe('genui-core sdk auth headers', () => {
  it('sends bearer token for evaluateDecision requests', async () => {
    const fetchMock = mock.method(globalThis, 'fetch', async () => ({
      ok: true,
      async json() { return { decisionId: 'd-1' }; }
    }));

    await evaluateDecision('http://localhost:8080', { slot: 'dashboard-hero' }, { token: 'abc123' });

    const [, options] = fetchMock.mock.calls[0].arguments;
    assert.equal(options.headers.authorization, 'Bearer abc123');
    assert.equal(options.headers['content-type'], 'application/json');
    fetchMock.mock.restore();
  });

  it('adds request signature when signing key is configured', async () => {
    const fetchMock = mock.method(globalThis, 'fetch', async () => ({
      ok: true,
      async json() { return { status: 'accepted' }; }
    }));

    const event = { eventType: 'dismiss', employeeId: 'E1' };
    await emitEvent('http://localhost:8080', event, { token: 'abc123', signingKey: 'secret-key' });

    const [, options] = fetchMock.mock.calls[0].arguments;
    const body = JSON.stringify(event);
    const expected = createHmac('sha256', 'secret-key').update(body).digest('hex');
    assert.equal(options.headers['x-genui-signature'], expected);
    assert.equal(options.headers.authorization, 'Bearer abc123');
    fetchMock.mock.restore();
  });
});
