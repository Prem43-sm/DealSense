const ANALYTICS_API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

type AnalyticsPayload = Record<string, string | number>;

export function recordAnalyticsEvent(path: string, payload: AnalyticsPayload) {
  const body = JSON.stringify(payload);
  const url = `${ANALYTICS_API_BASE}${path}`;

  if (typeof navigator !== "undefined" && "sendBeacon" in navigator) {
    const blob = new Blob([body], { type: "application/json" });
    navigator.sendBeacon(url, blob);
    return;
  }

  void fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
    keepalive: true,
  }).catch(() => undefined);
}

export async function recordSearchQuery(query: string) {
  const cleaned = query.trim();
  if (!cleaned) return;

  try {
    await fetch(`${ANALYTICS_API_BASE}/analytics/events/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: cleaned }),
      cache: "no-store",
    });
  } catch {
    return;
  }
}
