"use client";

import {
  Activity,
  Bot,
  Boxes,
  BrainCircuit,
  Cable,
  Gauge,
  Link2,
  Package,
  ScrollText,
  Settings,
} from "lucide-react";
import type { DashboardData } from "@/types/dashboard";
import { DashboardOverview } from "@/components/dashboard/dashboard-overview";
import { AutomationPanel } from "@/components/dashboard/automation-panel";
import { ConnectorPanel } from "@/components/dashboard/connector-panel";
import { ProductPanel } from "@/components/dashboard/product-panel";
import { AffiliatePanel } from "@/components/dashboard/affiliate-panel";
import { AvailabilityPanel } from "@/components/dashboard/availability-panel";
import { LogsPanel } from "@/components/dashboard/logs-panel";

const nav = [
  ["Dashboard", Gauge],
  ["Products", Package],
  ["Automation", Bot],
  ["Connectors", Cable],
  ["Affiliate", Link2],
  ["Availability", Activity],
  ["Logs", ScrollText],
  ["Settings", Settings],
  ["Future AI", BrainCircuit],
] as const;

export function AdminShell({ data }: { data: DashboardData }) {
  return (
    <div className="min-h-screen bg-muted/30">
      <div className="grid lg:grid-cols-[240px_1fr]">
        <aside className="border-b bg-card lg:min-h-screen lg:border-b-0 lg:border-r">
          <div className="flex h-16 items-center gap-2 border-b px-5">
            <Boxes className="h-5 w-5 text-primary" />
            <div>
              <p className="text-sm font-bold">DealSense Ops</p>
              <p className="text-xs text-muted-foreground">Internal</p>
            </div>
          </div>
          <nav className="flex gap-1 overflow-x-auto p-3 lg:block lg:space-y-1">
            {nav.map(([label, Icon]) => (
              <a
                key={label}
                href={`#${label.toLowerCase().replaceAll(" ", "-")}`}
                className="flex min-w-max items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                <Icon className="h-4 w-4" />
                {label}
              </a>
            ))}
          </nav>
        </aside>
        <section className="min-w-0 p-4 md:p-6 xl:p-8">
          <div className="mx-auto max-w-7xl space-y-6">
            <header className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
              <div>
                <p className="text-sm font-semibold text-primary">Operations</p>
                <h1 className="text-2xl font-bold md:text-3xl">Admin Dashboard</h1>
              </div>
              <div className="rounded-md border bg-card px-3 py-2 text-xs text-muted-foreground">
                Auth placeholder: middleware ready
              </div>
            </header>
            <DashboardOverview data={data.summary} />
            <ProductPanel data={data.products} />
            <AutomationPanel agents={data.automation.agents} />
            <ConnectorPanel connectors={data.connectors.connectors} />
            <AffiliatePanel data={data.affiliate} />
            <AvailabilityPanel data={data.availability} />
            <LogsPanel logs={data.summary.recent_logs} />
          </div>
        </section>
      </div>
    </div>
  );
}

