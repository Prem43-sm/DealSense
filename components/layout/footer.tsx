import Link from "next/link";
import type { Route } from "next";
import { brands, categories } from "@/lib/data";

export function Footer() {
  return (
    <footer className="border-t bg-card/40">
      <div className="container grid gap-8 py-12 md:grid-cols-[1.3fr_1fr_1fr_1fr]">
        <div>
          <p className="text-lg font-bold">DealSense</p>
          <p className="mt-3 max-w-sm text-sm text-muted-foreground">
            A fast affiliate comparison platform for verified prices, useful buying guides, and better shopping decisions.
          </p>
        </div>
        <FooterGroup
          title="Top categories"
          links={categories.slice(0, 5).map((item) => ({ href: `/categories/${item.slug}`, label: item.name }))}
        />
        <FooterGroup
          title="Popular brands"
          links={brands.slice(0, 5).map((item) => ({ href: `/brands/${item.slug}`, label: item.name }))}
        />
        <FooterGroup
          title="Company"
          links={[
            { href: "/deals", label: "All deals" },
            { href: "/blog", label: "Buying guides" },
            { href: "/search", label: "Search" },
            { href: "/about", label: "About" },
            { href: "/contact", label: "Contact" },
            { href: "/privacy", label: "Privacy policy" },
            { href: "/terms", label: "Terms" },
            { href: "/sitemap.xml", label: "Sitemap" }
          ]}
        />
      </div>
      <div className="border-t py-5">
        <div className="container flex flex-col gap-2 text-sm text-muted-foreground md:flex-row md:items-center md:justify-between">
          <p>Copyright 2026 DealSense. Affiliate disclosure: we may earn from qualifying purchases.</p>
          <p>Built for performance, SEO, and scalable PostgreSQL data.</p>
        </div>
      </div>
    </footer>
  );
}

function FooterGroup({ title, links }: { title: string; links: { href: string; label: string }[] }) {
  return (
    <div>
      <p className="mb-3 font-semibold">{title}</p>
      <div className="grid gap-2 text-sm text-muted-foreground">
        {links.map((link) => (
          <Link key={link.href} href={link.href as Route} className="hover:text-foreground">
            {link.label}
          </Link>
        ))}
      </div>
    </div>
  );
}
