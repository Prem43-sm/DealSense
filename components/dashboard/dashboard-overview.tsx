import { Activity, BadgeCheck, Link2, Package, Percent, Server, ShoppingBag } from "lucide-react";
import type { DashboardSummary } from "@/types/dashboard";
import { StatCard } from "@/components/dashboard/stat-card";
import { ChartPlaceholder } from "@/components/dashboard/chart-placeholder";

export function DashboardOverview({ data }: { data: DashboardSummary }) {
  return (
    <section id="dashboard" className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Products" value={data.products} Icon={Package} />
        <StatCard label="Price Records" value={data.price_records} Icon={ShoppingBag} />
        <StatCard label="Affiliate Links" value={data.affiliate_links} Icon={Link2} />
        <StatCard label="Availability Records" value={data.availability_records} Icon={Activity} />
        <StatCard label="Deals" value={data.deals} Icon={Percent} />
        <StatCard label="Connector Health" value={data.connector_health} Icon={Server} />
        <StatCard label="Automation Health" value={data.automation_health} Icon={BadgeCheck} />
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <ChartPlaceholder title="Daily Product Growth" />
        <ChartPlaceholder title="Price Updates" />
      </div>
    </section>
  );
}

