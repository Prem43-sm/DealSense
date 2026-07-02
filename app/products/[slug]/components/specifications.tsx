import type { ProductDetail } from "@/lib/product-detail";

export function Specifications({ product }: { product: ProductDetail }) {
  const specs = product.specifications ?? {};
  const rows = Object.entries(specs);

  return (
    <section id="specifications" className="rounded-lg border bg-card p-6">
      <h2 className="text-xl font-bold">Specifications</h2>
      {rows.length > 0 ? (
        <div className="mt-4 divide-y">
          {rows.map(([key, value]) => (
            <div key={key} className="grid gap-3 py-3 text-sm sm:grid-cols-[180px_1fr]">
              <span className="text-muted-foreground">{key}</span>
              <span className="font-medium">{value}</span>
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-4 rounded-md border bg-background p-4 text-sm text-muted-foreground">
          No specifications available.
        </p>
      )}
    </section>
  );
}
