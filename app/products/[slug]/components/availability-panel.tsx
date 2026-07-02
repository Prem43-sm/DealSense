import { StatusBadge } from "@/app/products/[slug]/components/status-badge";
import { allAvailability, type ProductDetail } from "@/lib/product-detail";

const marketplaceOrder = ["amazon", "flipkart", "croma", "reliance", "ajio", "cuelinks"];

export function AvailabilityPanel({ product }: { product: ProductDetail }) {
  const records = allAvailability(product);
  const byProvider = new Map(records.map((record) => [record.provider.toLowerCase(), record]));
  const marketplaces = marketplaceOrder.map((provider) => byProvider.get(provider) ?? {
    provider,
    marketplace: provider,
    status: "UNKNOWN",
    quantity: null,
    last_checked: "",
    last_changed: "",
    product_source_id: 0,
    id: provider,
  });

  return (
    <section id="availability" className="rounded-lg border bg-card p-6">
      <h2 className="text-xl font-bold">Availability</h2>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {marketplaces.map((record) => (
          <div key={`${record.provider}-${record.id}`} className="flex items-center justify-between gap-4 rounded-md border bg-background p-4">
            <div>
              <p className="font-semibold capitalize">{record.marketplace}</p>
              <p className="mt-1 text-xs text-muted-foreground">
                {record.last_checked ? `Checked ${new Date(record.last_checked).toLocaleString()}` : "Awaiting connector check"}
              </p>
            </div>
            <StatusBadge status={record.status} />
          </div>
        ))}
      </div>
    </section>
  );
}
