import { BarChart3, Eye, MousePointerClick, Search, Star, Target } from "lucide-react";
import type { AnalyticsOverview } from "@/types/dashboard";
import { ChartPlaceholder } from "@/components/dashboard/chart-placeholder";
import { StatCard } from "@/components/dashboard/stat-card";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function AnalyticsPanel({ data }: { data: AnalyticsOverview }) {
  return (
    <section id="analytics" className="space-y-4">
      <h2 className="text-xl font-bold">Analytics</h2>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <StatCard label="Views Today" value={data.views_today} Icon={Eye} />
        <StatCard label="Searches Today" value={data.searches_today} Icon={Search} />
        <StatCard label="Affiliate Clicks" value={data.affiliate_clicks} Icon={MousePointerClick} />
        <StatCard label="CTR" value={`${data.ctr}%`} Icon={Target} />
        <StatCard label="Trending Product" value={data.top_product ?? "None"} Icon={Star} />
      </div>
      <div className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <CardHeader>
            <h3 className="text-sm font-semibold">Score Leaderboard</h3>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="text-left text-muted-foreground">
                  <tr>
                    <th className="pb-2 font-medium">Product</th>
                    <th className="pb-2 font-medium">Views</th>
                    <th className="pb-2 font-medium">Clicks</th>
                    <th className="pb-2 font-medium">Score</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {data.top_products.slice(0, 10).map((product) => (
                    <tr key={product.product_id}>
                      <td className="max-w-[280px] truncate py-3 font-medium">{product.title}</td>
                      <td className="py-3">{product.views}</td>
                      <td className="py-3">{product.affiliate_clicks}</td>
                      <td className="py-3 font-semibold">{product.score}</td>
                    </tr>
                  ))}
                  {data.top_products.length === 0 ? (
                    <tr>
                      <td className="py-6 text-muted-foreground" colSpan={4}>No analytics events yet.</td>
                    </tr>
                  ) : null}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
        <div className="grid gap-4">
          <MiniList title="Most Viewed" items={data.most_viewed} metric="views" />
          <MiniList title="Top Searches" items={data.top_searches} metric="searches" />
          <MiniList title="Top Affiliate Clicks" items={data.top_affiliate_clicks} metric="affiliate_clicks" />
        </div>
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <ChartPlaceholder title="Analytics Trend" />
        <ChartPlaceholder title="Click Intent" />
      </div>
    </section>
  );
}

function MiniList({
  title,
  items,
  metric,
}: {
  title: string;
  items: AnalyticsOverview["top_products"];
  metric: "views" | "searches" | "affiliate_clicks";
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-3">
        <h3 className="text-sm font-semibold">{title}</h3>
        <BarChart3 className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent className="space-y-3">
        {items.slice(0, 5).map((item) => (
          <div key={item.product_id} className="flex items-center justify-between gap-3 text-sm">
            <span className="truncate text-muted-foreground">{item.title}</span>
            <span className="font-semibold">{item[metric]}</span>
          </div>
        ))}
        {items.length === 0 ? <p className="text-sm text-muted-foreground">No data yet.</p> : null}
      </CardContent>
    </Card>
  );
}
