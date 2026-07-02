import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { Bell, Heart, Star } from "lucide-react";
import { ProductAnalyticsBeacon } from "@/components/analytics/product-analytics-beacon";
import { Breadcrumbs } from "@/components/breadcrumbs";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { bestPrice, currency, getProduct, products, siteConfig } from "@/lib/data";

export function generateStaticParams() {
  return products.map((product) => ({ slug: product.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const product = getProduct(slug);
  if (!product) return {};
  return {
    title: `${product.name} Price Comparison`,
    description: product.description,
    alternates: { canonical: `/products/${product.slug}` },
    openGraph: {
      title: `${product.name} best price`,
      description: product.description,
      url: `${siteConfig.url}/products/${product.slug}`,
      images: [{ url: `${product.image}?auto=format&fit=crop&w=1200&q=80` }]
    }
  };
}

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = getProduct(slug);
  if (!product) notFound();
  const related = products.filter((item) => item.category === product.category && item.id !== product.id).slice(0, 4);

  return (
    <>
      <ProductAnalyticsBeacon event="detail-visit-by-slug" slug={product.slug} />
      <Breadcrumbs items={[{ label: "Deals", href: "/deals" }, { label: product.name }]} />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Product",
            name: product.name,
            image: product.image,
            description: product.description,
            brand: product.brand,
            aggregateRating: {
              "@type": "AggregateRating",
              ratingValue: product.rating,
              reviewCount: product.reviews
            },
            offers: {
              "@type": "AggregateOffer",
              lowPrice: bestPrice(product),
              priceCurrency: "USD",
              offerCount: product.prices.length
            }
          })
        }}
      />
      <div className="container py-8">
        <div className="grid gap-8 lg:grid-cols-[1fr_0.9fr]">
          <div className="grid gap-4 md:grid-cols-[96px_1fr]">
            <div className="order-2 grid grid-cols-4 gap-3 md:order-1 md:grid-cols-1">
              {[0, 1, 2, 3].map((index) => (
                <div key={index} className="relative aspect-square overflow-hidden rounded-md border bg-muted">
                  <Image src={`${product.image}?auto=format&fit=crop&w=300&q=70&sat=${index * 10}`} alt="" fill className="object-cover" />
                </div>
              ))}
            </div>
            <div className="relative order-1 aspect-square overflow-hidden rounded-lg border bg-muted md:order-2">
              <Image src={`${product.image}?auto=format&fit=crop&w=1000&q=80`} alt={product.name} fill priority className="object-cover" />
            </div>
          </div>
          <div>
            <p className="eyebrow">{product.brand}</p>
            <h1 className="mt-2 text-3xl font-bold md:text-5xl">{product.name}</h1>
            <p className="mt-4 text-lg text-muted-foreground">{product.description}</p>
            <div className="mt-5 flex flex-wrap items-center gap-4">
              <span className="flex items-center gap-1">
                <Star className="h-5 w-5 fill-warning text-warning" />
                <strong>{product.rating}</strong>
                <span className="text-muted-foreground">({product.reviews})</span>
              </span>
              <span className="text-muted-foreground">Best price from {currency(bestPrice(product))}</span>
            </div>
            <div className="mt-6 flex flex-wrap gap-3">
              <Button>
                <Heart className="h-4 w-4" />
                Save product
              </Button>
              <Button variant="outline">
                <Bell className="h-4 w-4" />
                Deal alert
              </Button>
            </div>
            <section className="mt-8 rounded-lg border bg-card">
              <div className="border-b p-5">
                <h2 className="font-semibold">Price comparison</h2>
              </div>
              <div className="divide-y">
                {product.prices.map((price) => (
                  <div key={price.merchant} className="grid gap-4 p-5 sm:grid-cols-[1fr_auto_auto] sm:items-center">
                    <div>
                      <p className="font-semibold">{price.merchant}</p>
                      <p className="text-sm text-muted-foreground">{price.shipping} / {price.inStock ? "In stock" : "Limited"}</p>
                    </div>
                    <div className="text-left sm:text-right">
                      <p className="text-xl font-bold">{currency(price.price)}</p>
                      {price.originalPrice ? <p className="text-sm text-muted-foreground line-through">{currency(price.originalPrice)}</p> : null}
                    </div>
                    <Button asChild variant="accent">
                      <a href={price.url} rel="nofollow sponsored noopener" target="_blank">Buy now</a>
                    </Button>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </div>
        <div className="mt-12 grid gap-6 lg:grid-cols-[1fr_1fr]">
          <section className="rounded-lg border bg-card p-6">
            <h2 className="text-xl font-bold">Specifications</h2>
            <div className="mt-4 divide-y">
              {Object.entries(product.specs).map(([key, value]) => (
                <div key={key} className="grid grid-cols-2 gap-4 py-3 text-sm">
                  <span className="text-muted-foreground">{key}</span>
                  <span className="font-medium">{value}</span>
                </div>
              ))}
            </div>
          </section>
          <section className="rounded-lg border bg-card p-6">
            <h2 className="text-xl font-bold">Price history</h2>
            <div className="mt-4 flex h-56 items-end gap-2 rounded-md bg-muted p-4">
              {[42, 62, 48, 70, 58, 50, 44, 39, 36, 41, 35, 32].map((height, index) => (
                <div key={index} className="flex-1 rounded-t bg-primary/80" style={{ height: `${height}%` }} />
              ))}
            </div>
          </section>
        </div>
        <section className="section">
          <h2 className="mb-6 text-2xl font-bold">Similar alternatives</h2>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {(related.length ? related : products.filter((item) => item.id !== product.id).slice(0, 4)).map((item) => (
              <ProductCard key={item.id} product={item} />
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
