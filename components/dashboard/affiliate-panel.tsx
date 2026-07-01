import { ExternalLink, Link2, ShieldAlert, Tags, TimerReset } from "lucide-react";
import type { AffiliateOverview } from "@/types/dashboard";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { StatCard } from "@/components/dashboard/stat-card";
import { StatusBadge } from "@/components/dashboard/badge";

export function AffiliatePanel({ data }: { data: AffiliateOverview }) {
  return (
    <section id="affiliate" className="space-y-4">
      <h2 className="text-xl font-bold">Affiliate</h2>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Generated Links" value={data.generated_links} Icon={Link2} />
        <StatCard label="Updated Today" value={data.updated_today} Icon={TimerReset} />
        <StatCard label="Broken Links" value={data.broken_links} Icon={ShieldAlert} />
        <StatCard label="Providers" value={data.providers} Icon={Tags} />
      </div>
      <Card>
        <CardHeader>
          <h3 className="text-sm font-semibold">Latest Affiliate Links</h3>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-xs uppercase text-muted-foreground">
                <tr className="border-b">
                  <th className="py-2 pr-4">Provider</th>
                  <th className="py-2 pr-4">Status</th>
                  <th className="py-2 pr-4">Source</th>
                  <th className="py-2">URL</th>
                </tr>
              </thead>
              <tbody>
                {data.latest_links.map((link) => (
                  <tr key={link.id} className="border-b last:border-0">
                    <td className="py-3 pr-4 capitalize">{link.provider}</td>
                    <td className="py-3 pr-4"><StatusBadge status={link.status} /></td>
                    <td className="py-3 pr-4">{link.product_source_id}</td>
                    <td className="py-3">
                      <a className="inline-flex items-center gap-1 text-primary" href={link.affiliate_url} target="_blank" rel="noreferrer">
                        Open <ExternalLink className="h-3 w-3" />
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </section>
  );
}

