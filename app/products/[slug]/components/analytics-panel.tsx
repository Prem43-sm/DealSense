import { BarChart3, Eye, Heart, MousePointerClick, Search, SlidersHorizontal, Star } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { currentAnalytics, type ProductDetail } from "@/lib/product-detail";

export function AnalyticsPanel({ product }: { product: ProductDetail }) {
  const analytics = currentAnalytics(product);

  const rows: [string, number, LucideIcon][] = analytics
    ? [
        ["Trending Score", analytics.score, Star],
        ["Views", analytics.views, Eye],
        ["Detail Visits", analytics.detail_page_visits, BarChart3],
        ["Affiliate Clicks", analytics.affiliate_clicks, MousePointerClick],
        ["Searches", analytics.searches, Search],
        ["Wishlist Adds", analytics.wishlist_adds, Heart],
        ["Compare Adds", analytics.compare_adds, SlidersHorizontal],
      ]
    : [];

  return (
    <section id="analytics" className="rounded-lg border bg-card p-6">
      <h2 className="text-xl font-bold">Analytics</h2>
      {analytics ? (
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {rows.map(([label, value, Icon]) => (
            <div key={String(label)} className="rounded-md border bg-background p-4">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm text-muted-foreground">{label}</p>
                <Icon className="h-4 w-4 text-muted-foreground" />
              </div>
              <p className="mt-2 text-2xl font-bold">{value}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-4 rounded-md border bg-background p-4 text-sm text-muted-foreground">
          Analytics will appear after this product receives traffic.
        </p>
      )}
    </section>
  );
}
