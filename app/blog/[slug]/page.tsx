import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Breadcrumbs } from "@/components/breadcrumbs";
import { posts, siteConfig } from "@/lib/data";

export function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const post = posts.find((item) => item.slug === slug);
  if (!post) return {};
  return {
    title: post.title,
    description: post.excerpt,
    alternates: { canonical: `/blog/${post.slug}` },
    openGraph: {
      type: "article",
      title: post.title,
      description: post.excerpt,
      url: `${siteConfig.url}/blog/${post.slug}`
    }
  };
}

export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = posts.find((item) => item.slug === slug);
  if (!post) notFound();

  return (
    <>
      <Breadcrumbs items={[{ label: "Blog", href: "/blog" }, { label: post.title }]} />
      <article className="container max-w-3xl py-10">
        <p className="eyebrow">{post.category}</p>
        <h1 className="mt-3 text-4xl font-bold leading-tight md:text-5xl">{post.title}</h1>
        <p className="mt-4 text-muted-foreground">{post.author} / {post.publishedAt} / {post.readTime}</p>
        <div className="prose prose-neutral mt-10 max-w-none dark:prose-invert">
          <p>{post.excerpt}</p>
          <h2>What to check first</h2>
          <p>
            Start with the actual current price, then compare it with recent lows, warranty terms, shipping speed, return policy, and product generation. A large discount on an older model can still be a weak buy if newer alternatives are close in price.
          </p>
          <h2>How DealSense supports this article type</h2>
          <p>
            Article templates include canonical metadata, Open Graph data, internal links, structured sections, and room for affiliate comparison blocks.
          </p>
          <p>
            Continue shopping with <Link href="/deals">all current deals</Link> or explore <Link href="/categories">category pages</Link>.
          </p>
        </div>
      </article>
    </>
  );
}
