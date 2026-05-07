export function evaluateRules({ context = {}, memory = {} }) {
  const isManager = Boolean(context?.roleContext?.isManager || memory?.roleContext?.isManager);
  if (isManager) return { candidateId: 'manager-pending-approvals-card', reasonCodes: ['RULE_MANAGER'] };
  return { candidateId: 'default-dashboard-card', reasonCodes: ['FALLBACK_DEFAULT'] };
}
