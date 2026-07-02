import { cache } from "react";
import { getProduct, products } from "@/lib/data";

const PRODUCT_API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";
const fallbackImage = "https://images.unsplash.com/photo-1496181133206-80ce9b88a853";

export type ProductPriceDetail = {
  id: number;
  product_id: number;
  store_id: number;
  current_price: string | number;
  availability: boolean;
  affiliate_url: string;
  updated_at: string;
  store: {
    id: number;
    name: string;
    logo_url?: string | null;
  };
};

export type ProductAffiliateLink = {
  id: number;
  provider: string;
  affiliate_url: string;
  short_url?: string | null;
  tracking_id?: string | null;
  status: string;
  click_count: number;
  last_generated: string;
};

export type ProductAvailability = {
  id: number;
  provider: string;
  status: string;
  quantity?: number | null;
  last_checked: string;
  last_changed: string;
};

export type ProductSourceDetail = {
  id: number;
  source_name: string;
  external_product_id: string;
  product_url?: string | null;
  affiliate_links?: ProductAffiliateLink[];
  availability_statuses?: ProductAvailability[];
};

export type ProductAnalyticsSummary = {
  id: number;
  date: string;
  views: number;
  searches: number;
  affiliate_clicks: number;
  wishlist_adds: number;
  compare_adds: number;
  detail_page_visits: number;
  score: number;
};

export type ProductDetail = {
  id: number;
  title: string;
  slug: string;
  brand?: string | null;
  category?: string | null;
  image_url?: string | null;
  description?: string | null;
  created_at: string;
  specifications?: Record<string, string>;
  prices: ProductPriceDetail[];
  sources: ProductSourceDetail[];
  analytics: ProductAnalyticsSummary[];
};

export const getProductDetail = cache(async (slug: string): Promise<ProductDetail | null> => {
  try {
    const response = await fetch(`${PRODUCT_API_BASE}/products/${encodeURIComponent(slug)}`, {
      next: { revalidate: 60 },
    });
    if (response.status === 404 || response.status === 422) return getFallbackProductDetail(slug);
    if (!response.ok) return getFallbackProductDetail(slug);
    return (await response.json()) as ProductDetail;
  } catch {
    return getFallbackProductDetail(slug);
  }
});

export function getFallbackProductDetail(slug: string): ProductDetail | null {
  const product = getProduct(slug);
  if (!product) return null;

  return {
    id: Number(product.id),
    title: product.name,
    slug: product.slug,
    brand: product.brand,
    category: product.category,
    image_url: product.image,
    description: product.description,
    created_at: product.createdAt,
    specifications: product.specs,
    prices: product.prices.map((price, index) => ({
      id: index + 1,
      product_id: Number(product.id),
      store_id: index + 1,
      current_price: price.price,
      availability: price.inStock,
      affiliate_url: price.url,
      updated_at: product.createdAt,
      store: {
        id: index + 1,
        name: price.merchant,
      },
    })),
    sources: [],
    analytics: [],
  };
}

export function productImage(product: ProductDetail) {
  return product.image_url || fallbackImage;
}

export function sortedPrices(product: ProductDetail) {
  return [...product.prices].sort((a, b) => Number(a.current_price) - Number(b.current_price));
}

export function currentAnalytics(product: ProductDetail) {
  return [...(product.analytics ?? [])].sort((a, b) => b.date.localeCompare(a.date))[0] ?? null;
}

export function allAvailability(product: ProductDetail) {
  return product.sources.flatMap((source) =>
    (source.availability_statuses ?? []).map((availability) => ({
      ...availability,
      product_source_id: source.id,
      marketplace: source.source_name,
    }))
  );
}

export function affiliateForProvider(product: ProductDetail, provider: string) {
  const normalized = provider.toLowerCase();
  const source = product.sources.find((item) => item.source_name.toLowerCase() === normalized);
  const link = source?.affiliate_links?.find((item) => item.status === "VALID") ?? source?.affiliate_links?.[0];
  return link && source ? { ...link, product_source_id: source.id } : null;
}

export function bestAffiliate(product: ProductDetail) {
  for (const source of product.sources) {
    const link = source.affiliate_links?.find((item) => item.status === "VALID") ?? source.affiliate_links?.[0];
    if (link) return { ...link, product_source_id: source.id };
  }
  return null;
}

export function relatedFallbackProducts(product: ProductDetail) {
  return products.filter((item) => item.category === product.category && item.slug !== product.slug).slice(0, 4);
}
