const auditLog = [];
export function appendAudit(entry) { auditLog.push(entry); }
export function findAuditByDecisionId(decisionId) { return auditLog.find((a) => a.decisionId === decisionId); }
export function getAuditLog() { return auditLog; }
