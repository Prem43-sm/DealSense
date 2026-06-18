import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Breadcrumbs } from "@/components/breadcrumbs";
import { Filters } from "@/components/filters";
import { ProductCard } from "@/components/product-card";
import { categories, getCategory, products } from "@/lib/data";

export function generateStaticParams() {
  return categories.map((category) => ({ slug: category.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const category = getCategory(slug);
  if (!category) return {};
  return {
    title: `${category.name} Deals`,
    description: category.description,
    alternates: { canonical: `/categories/${category.slug}` }
  };
}

export default async function CategoryPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const category = getCategory(slug);
  if (!category) notFound();
  const items = products.filter((product) => product.category === category.slug);

  return (
    <>
      <Breadcrumbs items={[{ label: "Categories", href: "/categories" }, { label: category.name }]} />
      <div className="container py-8">
        <div className="mb-8">
          <p className="eyebrow">Category deals</p>
          <h1 className="mt-2 text-3xl font-bold md:text-4xl">{category.name} deals</h1>
          <p className="mt-3 max-w-3xl text-muted-foreground">{category.description}</p>
        </div>
        <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
          <Filters />
          <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
            {items.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
        <section className="mt-12 rounded-lg border bg-card p-6">
          <h2 className="text-xl font-bold">How DealSense ranks {category.name.toLowerCase()} deals</h2>
          <p className="mt-3 text-muted-foreground">
            Category pages are designed for long-form SEO content, internal links, and database-backed filters. Rankings can use merchant price, historical low, availability, user interest, and affiliate conversion rules.
          </p>
        </section>
      </div>
    </>
  );
}
