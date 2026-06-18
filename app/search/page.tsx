import type { Metadata } from "next";
import { ProductCard } from "@/components/product-card";
import { SearchBox } from "@/components/search-box";
import { products } from "@/lib/data";

export const metadata: Metadata = {
  title: "Search Deals",
  description: "Search DealSense for products, categories, brands, and live deal pages.",
  alternates: { canonical: "/search" }
};

export default async function SearchPage({ searchParams }: { searchParams: Promise<{ q?: string }> }) {
  const { q } = await searchParams;
  const query = q?.toLowerCase() ?? "";
  const results = query
    ? products.filter((product) =>
        [product.name, product.description, product.brand, product.category, ...product.tags].join(" ").toLowerCase().includes(query)
      )
    : products;

  return (
    <div className="container py-10">
      <p className="eyebrow">Search</p>
      <h1 className="mt-2 text-3xl font-bold md:text-4xl">Find deals fast</h1>
      <div className="mt-6 max-w-2xl">
        <SearchBox />
      </div>
      <p className="mt-6 text-sm text-muted-foreground">{results.length} result{results.length === 1 ? "" : "s"} found</p>
      <div className="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {results.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
