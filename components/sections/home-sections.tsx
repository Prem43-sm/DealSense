import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { FeaturedDealCard } from "@/components/featured-deal-card";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { brands, categories, products, posts } from "@/lib/data";
import type { Product } from "@/lib/types";

export function ProductRail({ title, eyebrow, items = products }: { title: string; eyebrow: string; items?: typeof products }) {
  return (
    <section className="section">
      <div className="container">
        <div className="mb-6 flex items-end justify-between gap-4">
          <div>
            <p className="eyebrow">{eyebrow}</p>
            <h2 className="mt-2 text-2xl font-bold md:text-3xl">{title}</h2>
          </div>
          <Button asChild variant="outline">
            <Link href="/deals">View all</Link>
          </Button>
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {items.slice(0, 4).map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}

type FeaturedDeal = Product & {
  availabilityLabel: string;
  dealUrl?: string;
  dealDisabled?: boolean;
  productSourceId?: number;
};

export function FeaturedDealsRail({ items }: { items: FeaturedDeal[] }) {
  return (
    <section className="section">
      <div className="container">
        <div className="mb-6 flex items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Curated savings</p>
            <h2 className="mt-2 text-2xl font-bold md:text-3xl">Featured deals</h2>
          </div>
          <Button asChild variant="outline">
            <Link href="/deals">View all</Link>
          </Button>
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {items.slice(0, 4).map((product) => (
            <FeaturedDealCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}

export function CategoryGrid() {
  return (
    <section className="section bg-muted/40">
      <div className="container">
        <p className="eyebrow">Explore verticals</p>
        <h2 className="mt-2 text-2xl font-bold md:text-3xl">Top categories</h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((category) => (
            <Link key={category.slug} href={`/categories/${category.slug}`} className="group overflow-hidden rounded-lg border bg-card">
              <div className="relative h-36">
                <Image src={`${category.image}?auto=format&fit=crop&w=700&q=75`} alt="" fill className="object-cover transition group-hover:scale-105" />
              </div>
              <div className="p-5">
                <h3 className="font-semibold">{category.name}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{category.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

export function BrandsAndStats() {
  return (
    <section className="section">
      <div className="container grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
        <div>
          <p className="eyebrow">Trusted coverage</p>
          <h2 className="mt-2 text-2xl font-bold md:text-3xl">Popular brands</h2>
          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            {brands.map((brand) => (
              <Link key={brand.slug} href={`/brands/${brand.slug}`} className="rounded-lg border bg-card p-5 transition hover:border-primary/60">
                <p className="font-semibold">{brand.name}</p>
                <p className="mt-1 text-sm text-muted-foreground">{brand.productCount} tracked products</p>
              </Link>
            ))}
          </div>
        </div>
        <div className="rounded-lg border bg-card p-6">
          <p className="eyebrow">Marketplace signal</p>
          <h2 className="mt-2 text-2xl font-bold md:text-3xl">Built for daily deal decisions</h2>
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            {[
              ["42K+", "daily price checks"],
              ["310+", "merchant feeds ready"],
              ["95+", "target Lighthouse score"]
            ].map(([value, label]) => (
              <div key={label} className="rounded-md bg-muted p-5">
                <p className="text-3xl font-bold">{value}</p>
                <p className="mt-1 text-sm text-muted-foreground">{label}</p>
              </div>
            ))}
          </div>
          <div className="mt-8 grid gap-4">
            {posts.map((post) => (
              <Link key={post.slug} href={`/blog/${post.slug}`} className="flex items-center justify-between rounded-md border p-4 hover:bg-muted">
                <div>
                  <p className="font-medium">{post.title}</p>
                  <p className="text-sm text-muted-foreground">{post.category} • {post.readTime}</p>
                </div>
                <ArrowRight className="h-4 w-4" />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export function Newsletter() {
  return (
    <section className="section bg-muted/40">
      <div className="container">
        <div className="grid gap-6 rounded-lg border bg-card p-6 md:grid-cols-[1fr_auto] md:items-center">
          <div>
            <p className="eyebrow">Deal alerts placeholder</p>
            <h2 className="mt-2 text-2xl font-bold">Get the weekly best-price briefing</h2>
            <p className="mt-2 text-muted-foreground">Newsletter and alert workflows are UI-ready for auth, preferences, and automation.</p>
          </div>
          <form className="flex w-full gap-2 md:w-[420px]">
            <input className="h-11 min-w-0 flex-1 rounded-md border bg-background px-3 text-sm" placeholder="you@example.com" type="email" />
            <Button type="submit">Subscribe</Button>
          </form>
        </div>
      </div>
    </section>
  );
}
