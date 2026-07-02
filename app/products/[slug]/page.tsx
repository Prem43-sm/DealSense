import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { BadgeCheck, Star } from "lucide-react";
import { ProductAnalyticsBeacon } from "@/components/analytics/product-analytics-beacon";
import { Breadcrumbs } from "@/components/breadcrumbs";
import { AnalyticsPanel } from "@/app/products/[slug]/components/analytics-panel";
import { AvailabilityPanel } from "@/app/products/[slug]/components/availability-panel";
import { Overview } from "@/app/products/[slug]/components/overview";
import { PriceTable } from "@/app/products/[slug]/components/price-table";
import { ProductSidebar } from "@/app/products/[slug]/components/sidebar";
import { Specifications } from "@/app/products/[slug]/components/specifications";
import { StatusBadge } from "@/app/products/[slug]/components/status-badge";
import { currency, products, siteConfig } from "@/lib/data";
import {
  allAvailability,
  currentAnalytics,
  getProductDetail,
  productImage,
  sortedPrices,
} from "@/lib/product-detail";

export const dynamicParams = true;

export function generateStaticParams() {
  return products.map((product) => ({ slug: product.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const product = await getProductDetail(slug);
  if (!product) return {};

  const title = `${product.title} Price Comparison`;
  const description = product.description || `Compare live marketplace prices and availability for ${product.title}.`;
  const canonical = `/products/${product.slug}`;
  const image = productImage(product);

  return {
    title,
    description,
    alternates: { canonical },
    openGraph: {
      title,
      description,
      url: `${siteConfig.url}${canonical}`,
      images: [{ url: image }],
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [image],
    },
  };
}

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await getProductDetail(slug);
  if (!product) notFound();

  const image = productImage(product);
  const prices = sortedPrices(product);
  const lowest = prices[0];
  const availability = allAvailability(product);
  const analytics = currentAnalytics(product);
  const category = product.category ?? "uncategorized";

  return (
    <>
      <ProductAnalyticsBeacon event="detail-visit" productId={product.id} />
      <Breadcrumbs
        items={[
          { label: category.replaceAll("-", " "), href: `/categories/${category}` },
          { label: product.title },
        ]}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Product",
            name: product.title,
            image,
            description: product.description,
            brand: product.brand,
            offers: lowest
              ? {
                  "@type": "AggregateOffer",
                  lowPrice: Number(lowest.current_price),
                  priceCurrency: "INR",
                  offerCount: prices.length,
                  availability: lowest.availability ? "https://schema.org/InStock" : "https://schema.org/OutOfStock",
                }
              : undefined,
          }),
        }}
      />
      <main className="container py-8">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_360px]">
          <div className="min-w-0 space-y-8">
            <section className="grid gap-6 lg:grid-cols-[minmax(0,0.95fr)_minmax(320px,1fr)]">
              <div className="grid gap-4 md:grid-cols-[84px_1fr]">
                <div className="order-2 grid grid-cols-4 gap-3 md:order-1 md:grid-cols-1">
                  {[0, 1, 2, 3].map((index) => (
                    <div key={index} className="relative aspect-square overflow-hidden rounded-md border bg-muted">
                      <Image
                        src={`${image}?auto=format&fit=crop&w=240&q=70`}
                        alt=""
                        fill
                        sizes="84px"
                        className="object-cover"
                      />
                    </div>
                  ))}
                </div>
                <div className="relative order-1 aspect-square overflow-hidden rounded-lg border bg-muted md:order-2">
                  <Image
                    src={`${image}?auto=format&fit=crop&w=1100&q=80`}
                    alt={product.title}
                    fill
                    priority
                    sizes="(min-width: 1024px) 45vw, 100vw"
                    className="object-cover"
                  />
                  <span className="absolute left-4 top-4 rounded-md border bg-background/90 px-3 py-1 text-xs font-semibold">
                    Zoom placeholder
                  </span>
                </div>
              </div>
              <div className="flex flex-col justify-center">
                <p className="eyebrow">{product.brand ?? "Unknown brand"}</p>
                <h1 className="mt-2 text-3xl font-bold md:text-5xl">{product.title}</h1>
                <p className="mt-4 text-lg text-muted-foreground">
                  {product.description || "Live marketplace product tracked by DealSense."}
                </p>
                <div className="mt-5 flex flex-wrap items-center gap-3">
                  <span className="inline-flex items-center gap-1 rounded-md border bg-card px-2 py-1 text-sm">
                    <Star className="h-4 w-4 fill-warning text-warning" />
                    4.7 rating placeholder
                  </span>
                  {analytics && analytics.score > 0 ? (
                    <span className="inline-flex items-center gap-1 rounded-md border bg-primary/10 px-2 py-1 text-sm font-semibold text-primary">
                      <BadgeCheck className="h-4 w-4" />
                      Trending
                    </span>
                  ) : null}
                  <StatusBadge status={availability[0]?.status ?? (lowest?.availability ? "IN_STOCK" : "UNKNOWN")} />
                </div>
                <div className="mt-6 rounded-lg border bg-card p-5">
                  <p className="text-sm text-muted-foreground">Lowest price</p>
                  <p className="mt-1 text-3xl font-bold">{lowest ? currency(Number(lowest.current_price)) : "Pending"}</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {lowest ? `${lowest.store.name} / Updated ${new Date(lowest.updated_at).toLocaleString()}` : "No price records yet"}
                  </p>
                </div>
              </div>
            </section>

            <nav className="flex gap-2 overflow-x-auto border-b pb-2 text-sm font-semibold">
              {["Overview", "Specifications", "Prices", "Availability", "Analytics"].map((label) => (
                <a key={label} href={`#${label.toLowerCase()}`} className="rounded-md px-3 py-2 text-muted-foreground hover:bg-muted hover:text-foreground">
                  {label}
                </a>
              ))}
            </nav>

            <Overview product={product} />
            <Specifications product={product} />
            <PriceTable product={product} />
            <AvailabilityPanel product={product} />
            <AnalyticsPanel product={product} />
          </div>
          <ProductSidebar product={product} />
        </div>
      </main>
    </>
  );
}
