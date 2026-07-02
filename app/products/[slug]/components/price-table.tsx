import { AffiliateButton } from "@/app/products/[slug]/components/affiliate-button";
import { StatusBadge } from "@/app/products/[slug]/components/status-badge";
import { currency } from "@/lib/data";
import { affiliateForProvider, sortedPrices, type ProductDetail } from "@/lib/product-detail";

export function PriceTable({ product }: { product: ProductDetail }) {
  const prices = sortedPrices(product);
  const lowest = prices[0];

  return (
    <section id="prices" className="rounded-lg border bg-card p-6">
      <h2 className="text-xl font-bold">Prices</h2>
      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-left text-muted-foreground">
            <tr>
              <th className="pb-3 pr-4 font-medium">Store</th>
              <th className="pb-3 pr-4 font-medium">Price</th>
              <th className="pb-3 pr-4 font-medium">Availability</th>
              <th className="pb-3 font-medium">Affiliate</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {prices.map((price) => {
              const affiliate = affiliateForProvider(product, price.store.name);
              const isLowest = lowest?.id === price.id;
              return (
                <tr key={price.id} className={isLowest ? "bg-success/5" : undefined}>
                  <td className="py-4 pr-4">
                    <p className="font-semibold">{price.store.name}</p>
                    {isLowest ? <p className="mt-1 text-xs font-semibold text-success">Lowest price</p> : null}
                  </td>
                  <td className="py-4 pr-4 text-lg font-bold">{currency(Number(price.current_price))}</td>
                  <td className="py-4 pr-4">
                    <StatusBadge status={price.availability ? "IN_STOCK" : "OUT_OF_STOCK"} />
                  </td>
                  <td className="py-4">
                    <AffiliateButton
                      href={affiliate?.affiliate_url || price.affiliate_url}
                      productSourceId={affiliate?.product_source_id}
                      label="View Deal"
                      variant={isLowest ? "accent" : "outline"}
                    />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {prices.length === 0 ? (
          <p className="rounded-md border bg-background p-4 text-sm text-muted-foreground">No prices available yet.</p>
        ) : null}
      </div>
    </section>
  );
}
