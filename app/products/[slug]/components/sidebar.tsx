import { Bell, Heart, Scale } from "lucide-react";
import { AffiliateButton } from "@/app/products/[slug]/components/affiliate-button";
import { StatusBadge } from "@/app/products/[slug]/components/status-badge";
import { Button } from "@/components/ui/button";
import { currency } from "@/lib/data";
import { allAvailability, bestAffiliate, sortedPrices, type ProductDetail } from "@/lib/product-detail";

export function ProductSidebar({ product }: { product: ProductDetail }) {
  const lowest = sortedPrices(product)[0];
  const affiliate = bestAffiliate(product);
  const availability = allAvailability(product)[0];
  const href = affiliate?.affiliate_url || lowest?.affiliate_url;
  const updatedAt = lowest?.updated_at ? new Date(lowest.updated_at).toLocaleString() : "Not available";

  return (
    <aside className="space-y-4 lg:sticky lg:top-24">
      <section className="rounded-lg border bg-card p-5 shadow-soft">
        <p className="text-sm font-medium text-muted-foreground">Current lowest price</p>
        <p className="mt-2 text-3xl font-bold">{lowest ? currency(Number(lowest.current_price)) : "Pending"}</p>
        <p className="mt-1 text-sm text-muted-foreground">{lowest?.store.name ?? "No marketplace price yet"}</p>
        <div className="mt-4 flex items-center justify-between gap-3 rounded-md border bg-background p-3">
          <span className="text-sm text-muted-foreground">Availability</span>
          <StatusBadge status={availability?.status ?? (lowest?.availability ? "IN_STOCK" : "UNKNOWN")} />
        </div>
        <p className="mt-3 text-xs text-muted-foreground">Last updated: {updatedAt}</p>
        <div className="mt-5 grid gap-2">
          <AffiliateButton href={href} productSourceId={affiliate?.product_source_id} />
          <Button variant="outline" disabled>
            <Scale className="h-4 w-4" />
            Compare
          </Button>
          <Button variant="outline" disabled>
            <Heart className="h-4 w-4" />
            Wishlist
          </Button>
          <Button variant="ghost" disabled>
            <Bell className="h-4 w-4" />
            Price alert
          </Button>
        </div>
      </section>
    </aside>
  );
}
