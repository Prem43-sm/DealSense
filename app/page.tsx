import type { Metadata } from "next";
import { Hero } from "@/components/sections/hero";
import { BrandsAndStats, CategoryGrid, Newsletter, ProductRail } from "@/components/sections/home-sections";
import { products, siteConfig } from "@/lib/data";

export const metadata: Metadata = {
  alternates: { canonical: "/" }
};

export default function HomePage() {
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
