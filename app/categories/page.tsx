import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { categories } from "@/lib/data";

export const metadata: Metadata = {
  title: "Deal Categories",
  description: "Browse DealSense categories for laptops, smartphones, audio, gaming, smart home, and wearables.",
  alternates: { canonical: "/categories" }
};

export default function CategoriesPage() {
  return (
    <div className="container py-10">
      <p className="eyebrow">Category directory</p>
      <h1 className="mt-2 text-3xl font-bold md:text-4xl">Shop by product category</h1>
      <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {categories.map((category) => (
          <Link key={category.slug} href={`/categories/${category.slug}`} className="group overflow-hidden rounded-lg border bg-card">
            <div className="relative h-44">
              <Image src={`${category.image}?auto=format&fit=crop&w=800&q=75`} alt={category.name} fill className="object-cover transition group-hover:scale-105" />
            </div>
            <div className="p-5">
              <h2 className="text-lg font-semibold">{category.name}</h2>
              <p className="mt-2 text-sm text-muted-foreground">{category.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
