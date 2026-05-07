const memoryStore = new Map();
export function getMemory(employeeId) {
  return memoryStore.get(employeeId) || { employeeId, roleContext: {}, behavioralMemory: { recentDismissedCards: [] } };
}
export function updateMemoryFromEvent(event) {
  const memory = getMemory(event.employeeId);
  if (event.eventType === 'dismiss' && event.candidateId) {
    memory.behavioralMemory.recentDismissedCards.push(event.candidateId);
  }
  memoryStore.set(event.employeeId, memory);
  return memory;
}
export function seedMemory(employeeId, value) { memoryStore.set(employeeId, value); }
