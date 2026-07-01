import type { DashboardData } from "@/types/dashboard";

export const DASHBOARD_API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${DASHBOARD_API_BASE}${path}`, { cache: "no-store" });
    if (!response.ok) return fallback;
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function getDashboardData(): Promise<DashboardData> {
  const [summary, automation, connectors, products, affiliate, availability] = await Promise.all([
    fetchJson("/dashboard/summary", {
      products: 0,
      price_records: 0,
      affiliate_links: 0,
      availability_records: 0,
      deals: 0,
      connector_health: "0/0",
      automation_health: "offline",
      recent_logs: [],
    }),
    fetchJson("/dashboard/automation", { agents: [] }),
    fetchJson("/dashboard/connectors", { connectors: [] }),
    fetchJson("/dashboard/products", {
      master_products: 0,
      marketplace_sources: 0,
      products_added_today: 0,
      duplicate_prevented: 0,
      latest_product: null,
    }),
    fetchJson("/dashboard/affiliate", {
      generated_links: 0,
      updated_today: 0,
      broken_links: 0,
      providers: 0,
      latest_links: [],
    }),
    fetchJson("/dashboard/availability", {
      in_stock: 0,
      out_of_stock: 0,
      limited: 0,
      preorder: 0,
      unknown: 0,
      latest: [],
    }),
  ]);

  return { summary, automation, connectors, products, affiliate, availability };
}

export async function callDashboardAction(path: string) {
  const response = await fetch(`${DASHBOARD_API_BASE}${path}`, { method: "GET" });
  if (!response.ok) throw new Error(`Request failed with ${response.status}`);
  return response.json();
}

