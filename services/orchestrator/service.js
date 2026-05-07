import { evaluateRules } from '../rules/engine.js';
import { getMemory } from '../memory/service.js';

export function evaluateDecision(request) {
  const memory = getMemory(request.employeeId);
  const dismissed = new Set(memory?.behavioralMemory?.recentDismissedCards || []);
  const choice = evaluateRules({ context: request.context, memory });
  const fallback = choice.candidateId === 'manager-pending-approvals-card' && dismissed.has(choice.candidateId);
  const candidateId = fallback ? 'default-dashboard-card' : choice.candidateId;
  const reasonCodes = fallback ? ['SUPPRESSED_DISMISSED', 'FALLBACK_DEFAULT'] : choice.reasonCodes;

  return {
    decisionId: `dec_${Date.now()}`,
    candidateId,
    reasonCodes,
    manifest: {
      schemaVersion: '1.0.0',
      surface: 'employee-dashboard',
      slot: request.slot,
      components: [{
        type: 'summary_card',
        id: candidateId,
        props: {
          title: candidateId === 'manager-pending-approvals-card' ? 'You have pending approvals' : 'Welcome back',
          body: candidateId === 'manager-pending-approvals-card' ? '3 approvals are waiting for your review.' : 'No personalized content right now.',
          cta: { label: 'Open', action: 'open_link', target: '/approvals' }
        }
      }]
    },
    audit: { ruleHits: reasonCodes, modelVersion: 'mock-llm-disabled' }
  };
}
