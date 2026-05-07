import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateDecision } from '../../services/orchestrator/service.js';
import { seedMemory } from '../../services/memory/service.js';

test('manager gets manager card', () => {
  seedMemory('E1', { employeeId: 'E1', roleContext: { isManager: true }, behavioralMemory: { recentDismissedCards: [] } });
  const decision = evaluateDecision({ appId: 'employee-portal', channel: 'web', slot: 'dashboard-hero', employeeId: 'E1' });
  assert.equal(decision.candidateId, 'manager-pending-approvals-card');
});

test('dismissed card is suppressed', () => {
  seedMemory('E2', { employeeId: 'E2', roleContext: { isManager: true }, behavioralMemory: { recentDismissedCards: ['manager-pending-approvals-card'] } });
  const decision = evaluateDecision({ appId: 'employee-portal', channel: 'web', slot: 'dashboard-hero', employeeId: 'E2' });
  assert.equal(decision.candidateId, 'default-dashboard-card');
  assert.deepEqual(decision.reasonCodes, ['SUPPRESSED_DISMISSED', 'FALLBACK_DEFAULT']);
});
