import type { Metadata } from "next";
import Link from "next/link";
import { posts } from "@/lib/data";

export const metadata: Metadata = {
  title: "Buying Guides and Comparisons",
  description: "SEO-optimized buying guides, product comparisons, and technology news from DealSense.",
  alternates: { canonical: "/blog" }
};

export default function BlogPage() {
  return (
    <div className="container py-10">
      <p className="eyebrow">DealSense editorial</p>
      <h1 className="mt-2 text-3xl font-bold md:text-4xl">Buying guides, comparisons, and tech news</h1>
      <div className="mt-8 grid gap-5 lg:grid-cols-3">
        {posts.map((post) => (
          <Link key={post.slug} href={`/blog/${post.slug}`} className="rounded-lg border bg-card p-6 transition hover:border-primary/60">
            <p className="text-sm font-semibold text-primary">{post.category}</p>
            <h2 className="mt-3 text-xl font-bold">{post.title}</h2>
            <p className="mt-3 text-sm text-muted-foreground">{post.excerpt}</p>
            <p className="mt-5 text-sm text-muted-foreground">{post.author} / {post.readTime}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
