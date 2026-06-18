import type { Metadata } from "next";
import { SlidersHorizontal } from "lucide-react";
import { Filters } from "@/components/filters";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { products } from "@/lib/data";

export const metadata: Metadata = {
  title: "Best Deals",
  description: "Browse verified product deals with filters for category, brand, price, discount, and sorting.",
  alternates: { canonical: "/deals" }
};

export default function DealsPage() {
  return (
    <div className="container py-8">
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="eyebrow">All deals</p>
          <h1 className="mt-2 text-3xl font-bold md:text-4xl">Compare today&apos;s best prices</h1>
          <p className="mt-2 max-w-2xl text-muted-foreground">Filter by brand, category, savings, and product type. Pagination is ready for database-backed result sets.</p>
        </div>
        <Button variant="outline">
          <SlidersHorizontal className="h-4 w-4" />
          Sort: Best discount
        </Button>
      </div>
      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        <Filters />
        <div>
          <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          <div className="mt-8 flex justify-center gap-2">
            <Button variant="outline">Previous</Button>
            <Button>1</Button>
            <Button variant="outline">2</Button>
            <Button variant="outline">Next</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
