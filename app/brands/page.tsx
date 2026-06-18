import type { Metadata } from "next";
import Link from "next/link";
import { brands } from "@/lib/data";

export const metadata: Metadata = {
  title: "Brand Directory",
  description: "Browse popular technology brands tracked by DealSense.",
  alternates: { canonical: "/brands" }
};

export default function BrandsPage() {
  return (
    <div className="container py-10">
      <p className="eyebrow">Brand directory</p>
      <h1 className="mt-2 text-3xl font-bold md:text-4xl">Popular brands tracked by DealSense</h1>
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {brands.map((brand) => (
          <Link key={brand.slug} href={`/brands/${brand.slug}`} className="rounded-lg border bg-card p-6 transition hover:border-primary/60">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-md bg-primary/12 text-lg font-bold text-primary">
              {brand.name.slice(0, 1)}
            </div>
            <h2 className="text-lg font-semibold">{brand.name}</h2>
            <p className="mt-2 text-sm text-muted-foreground">{brand.description}</p>
            <p className="mt-4 text-sm font-medium">{brand.productCount} products tracked</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
