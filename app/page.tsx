import type { Metadata } from "next";
import { Hero } from "@/components/sections/hero";
import { BrandsAndStats, CategoryGrid, Newsletter, ProductRail } from "@/components/sections/home-sections";
import { getProducts } from "@/lib/api";
import { products, siteConfig } from "@/lib/data";

type BackendProductDebug = {
  title?: string;
  brand?: string;
  category?: string;
};

export const metadata: Metadata = {
  alternates: { canonical: "/" }
};

export default async function HomePage() {
  let backendProducts: BackendProductDebug[] = [];

  try {
    backendProducts = await getProducts();
  } catch {
    backendProducts = [];
  }

  const firstBackendProduct = backendProducts[0];
  const newest = [...products].sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  const biggestDrops = [...products].sort((a, b) => b.prices[0].originalPrice! - b.prices[0].price - (a.prices[0].originalPrice! - a.prices[0].price));

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebSite",
            name: "DealSense",
            url: siteConfig.url,
            potentialAction: {
              "@type": "SearchAction",
              target: `${siteConfig.url}/search?q={search_term_string}`,
              "query-input": "required name=search_term_string"
            }
          })
        }}
      />
      <section className="mx-auto mt-6 max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="rounded-lg border border-border bg-card p-4 text-card-foreground shadow-sm">
          <h2 className="text-sm font-semibold">Backend Connection Test</h2>
          {firstBackendProduct ? (
            <div className="mt-3 grid gap-2 text-sm text-muted-foreground sm:grid-cols-3">
              <p>
                <span className="block font-medium text-card-foreground">First Product:</span>
                {firstBackendProduct.title}
              </p>
              <p>
                <span className="block font-medium text-card-foreground">Brand:</span>
                {firstBackendProduct.brand}
              </p>
              <p>
                <span className="block font-medium text-card-foreground">Category:</span>
                {firstBackendProduct.category}
              </p>
            </div>
          ) : (
            <p className="mt-3 text-sm text-muted-foreground">No products found</p>
          )}
        </div>
      </section>
      <Hero />
      <ProductRail title="Featured deals" eyebrow="Curated savings" />
      <ProductRail title="Trending products" eyebrow="High-intent searches" items={newest} />
      <ProductRail title="Biggest price drops" eyebrow="Meaningful movement" items={biggestDrops} />
      <CategoryGrid />
      <BrandsAndStats />
      <Newsletter />
    </>
  );
}
