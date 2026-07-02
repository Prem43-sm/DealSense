import type { Metadata } from "next";
import { Hero } from "@/components/sections/hero";
import { BrandsAndStats, CategoryGrid, FeaturedDealsRail, Newsletter, ProductRail } from "@/components/sections/home-sections";
import { getFeaturedProducts } from "@/lib/api";
import { products, siteConfig } from "@/lib/data";
import type { BackendProduct } from "@/lib/api";
import type { Product } from "@/lib/types";

const fallbackImage = "https://images.unsplash.com/photo-1496181133206-80ce9b88a853";

export const metadata: Metadata = {
  alternates: { canonical: "/" }
};

export default async function HomePage() {
  const featuredDeals = await getFeaturedDeals();
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
      <FeaturedDealsRail items={featuredDeals} />
      <ProductRail title="Trending products" eyebrow="High-intent searches" items={newest} />
      <ProductRail title="Biggest price drops" eyebrow="Meaningful movement" items={biggestDrops} />
      <CategoryGrid />
      <BrandsAndStats />
      <Newsletter />
    </>
  );
}

type FeaturedDeal = Product & {
  availabilityLabel: string;
  dealUrl?: string;
  dealDisabled?: boolean;
};

async function getFeaturedDeals(): Promise<FeaturedDeal[]> {
  try {
    const liveProducts = await getFeaturedProducts(4);
    const mapped = liveProducts.map(mapBackendProduct).filter((product): product is FeaturedDeal => Boolean(product));
    return mapped.length > 0 ? mapped : mockFeaturedDeals();
  } catch {
    return mockFeaturedDeals();
  }
}

function mapBackendProduct(product: BackendProduct): FeaturedDeal | null {
  const prices = product.prices ?? [];
  if (prices.length === 0) return null;

  const sortedPrices = [...prices].sort((a, b) => Number(a.current_price) - Number(b.current_price));
  const best = sortedPrices[0];
  const inStock = sortedPrices.some((price) => price.availability);

  return {
    id: String(product.id),
    name: product.title,
    slug: product.slug,
    description: product.description ?? "Live marketplace product tracked by DealSense.",
    category: product.category ?? "uncategorized",
    brand: product.brand ?? "Unknown",
    image: product.image_url || fallbackImage,
    rating: 4.7,
    reviews: 0,
    specs: {},
    tags: ["Live deal"],
    createdAt: product.created_at,
    availabilityLabel: inStock ? "In stock" : "Unavailable",
    dealUrl: best.affiliate_url && best.affiliate_url !== "#" ? best.affiliate_url : undefined,
    dealDisabled: !best.affiliate_url || best.affiliate_url === "#",
    prices: sortedPrices.map((price) => ({
      merchant: price.store?.name ?? "Marketplace",
      price: Number(price.current_price),
      shipping: "See merchant",
      url: price.affiliate_url || "#",
      inStock: price.availability,
    })),
  };
}

function mockFeaturedDeals(): FeaturedDeal[] {
  return products.slice(0, 4).map((product) => {
    const best = [...product.prices].sort((a, b) => a.price - b.price)[0];
    return {
      ...product,
      availabilityLabel: best.inStock ? "In stock" : "Unavailable",
      dealUrl: best.url && best.url !== "#" ? best.url : undefined,
      dealDisabled: !best.url || best.url === "#",
    };
  });
}
