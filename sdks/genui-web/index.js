import { evaluateDecision } from '../genui-core/index.js';

export async function renderSlot({ baseUrl, appId, employeeId, slot, el }) {
  const decision = await evaluateDecision(baseUrl, { appId, employeeId, channel: 'web', slot });
  el.textContent = decision.manifest.components?.[0]?.props?.title || 'Fallback';
  return decision;
}
