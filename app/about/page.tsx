import type { Metadata } from "next";
import Link from "next/link";
import { BadgeCheck, BarChart3, SearchCheck } from "lucide-react";
import { Button } from "@/components/ui/button";

export const metadata: Metadata = {
  title: "About",
  description: "Learn how DealSense helps shoppers compare prices, understand discounts, and buy with confidence.",
  alternates: { canonical: "/about" }
};

export default function AboutPage() {
  return (
    <div className="container py-12">
      <div className="max-w-3xl">
        <p className="eyebrow">About DealSense</p>
        <h1 className="mt-3 text-4xl font-bold leading-tight md:text-5xl">A faster, cleaner way to compare deals.</h1>
        <p className="mt-5 text-lg text-muted-foreground">
          DealSense is built for shoppers who want clear product comparisons, transparent affiliate disclosures, and reliable deal pages without noisy clutter.
        </p>
      </div>
      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {[
          { title: "Verified comparison", copy: "Product pages organize prices, availability, shipping notes, and merchant links.", Icon: SearchCheck },
          { title: "Price context", copy: "Deal modules are structured for price history, drops, and future feed-backed rankings.", Icon: BarChart3 },
          { title: "Trust first", copy: "Affiliate relationships are disclosed clearly and outbound links are marked sponsored.", Icon: BadgeCheck }
        ].map(({ title, copy, Icon }) => (
          <section key={title} className="rounded-lg border bg-card p-6">
            <Icon className="h-6 w-6 text-primary" aria-hidden="true" />
            <h2 className="mt-4 font-semibold">{title}</h2>
            <p className="mt-2 text-sm text-muted-foreground">{copy}</p>
          </section>
        ))}
      </div>
      <Button asChild className="mt-10">
        <Link href="/deals">Browse current deals</Link>
      </Button>
    </div>
  );
}
