import { AlertTriangle, CircleHelp, PackageCheck, PackageX, Timer } from "lucide-react";
import type { AvailabilityOverview } from "@/types/dashboard";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ChartPlaceholder } from "@/components/dashboard/chart-placeholder";
import { StatCard } from "@/components/dashboard/stat-card";
import { StatusBadge } from "@/components/dashboard/badge";

export function AvailabilityPanel({ data }: { data: AvailabilityOverview }) {
  return (
    <section id="availability" className="space-y-4">
      <h2 className="text-xl font-bold">Availability</h2>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <StatCard label="In Stock" value={data.in_stock} Icon={PackageCheck} />
        <StatCard label="Out Of Stock" value={data.out_of_stock} Icon={PackageX} />
        <StatCard label="Limited" value={data.limited} Icon={AlertTriangle} />
        <StatCard label="Preorder" value={data.preorder} Icon={Timer} />
        <StatCard label="Unknown" value={data.unknown} Icon={CircleHelp} />
      </div>
      <div className="grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
        <ChartPlaceholder title="Availability Trend" />
        <Card>
          <CardHeader>
            <h3 className="text-sm font-semibold">Current Availability</h3>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-xs uppercase text-muted-foreground">
                  <tr className="border-b">
                    <th className="py-2 pr-4">Provider</th>
                    <th className="py-2 pr-4">Status</th>
                    <th className="py-2 pr-4">Quantity</th>
                    <th className="py-2">Source</th>
                  </tr>
                </thead>
                <tbody>
                  {data.latest.map((row) => (
                    <tr key={row.id} className="border-b last:border-0">
                      <td className="py-3 pr-4 capitalize">{row.provider}</td>
                      <td className="py-3 pr-4"><StatusBadge status={row.status} /></td>
                      <td className="py-3 pr-4">{row.quantity ?? "-"}</td>
                      <td className="py-3">{row.product_source_id}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}

