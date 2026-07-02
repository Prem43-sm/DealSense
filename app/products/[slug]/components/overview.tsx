import type { ProductDetail } from "@/lib/product-detail";

export function Overview({ product }: { product: ProductDetail }) {
  const rows = [
    ["Brand", product.brand ?? "Unknown"],
    ["Category", product.category?.replaceAll("-", " ") ?? "Uncategorized"],
    ["Product ID", String(product.id)],
    ["Created", new Date(product.created_at).toLocaleDateString()],
  ];

  return (
    <section id="overview" className="rounded-lg border bg-card p-6">
      <h2 className="text-xl font-bold">Overview</h2>
      <p className="mt-3 text-muted-foreground">{product.description || "No product description is available yet."}</p>
      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        {rows.map(([label, value]) => (
          <div key={label} className="rounded-md border bg-background p-4">
            <p className="text-xs font-medium uppercase text-muted-foreground">{label}</p>
            <p className="mt-1 font-semibold capitalize">{value}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
