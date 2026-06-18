import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Breadcrumbs } from "@/components/breadcrumbs";
import { ProductCard } from "@/components/product-card";
import { brands, getBrand, products } from "@/lib/data";

export function generateStaticParams() {
  return brands.map((brand) => ({ slug: brand.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const brand = getBrand(slug);
  if (!brand) return {};
  return {
    title: `${brand.name} Deals`,
    description: brand.description,
    alternates: { canonical: `/brands/${brand.slug}` }
  };
}

export default async function BrandPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const brand = getBrand(slug);
  if (!brand) notFound();
  const items = products.filter((product) => product.brand === brand.slug);

  return (
    <>
      <Breadcrumbs items={[{ label: "Brands", href: "/brands" }, { label: brand.name }]} />
      <div className="container py-8">
        <div className="mb-8 rounded-lg border bg-card p-6">
          <p className="eyebrow">Brand deals</p>
          <h1 className="mt-2 text-3xl font-bold md:text-4xl">{brand.name}</h1>
          <p className="mt-3 max-w-3xl text-muted-foreground">{brand.description}</p>
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {items.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </>
  );
}
