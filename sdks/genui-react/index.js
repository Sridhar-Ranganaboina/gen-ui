// Minimal placeholder API surface for React SDK MVP.
export function GenUIProvider({ children }) { return children; }
export async function useGenUI({ client, request, fallback }) {
  try { return await client(request); } catch { return fallback; }
}
