import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms and Conditions",
  description: "DealSense terms for affiliate links, pricing accuracy, content usage, and website availability.",
  alternates: { canonical: "/terms" }
};

export default function TermsPage() {
  return (
    <article className="container max-w-3xl py-12">
      <p className="eyebrow">Legal</p>
      <h1 className="mt-3 text-4xl font-bold">Terms and Conditions</h1>
      <p className="mt-3 text-sm text-muted-foreground">Last updated: June 18, 2026</p>
      <div className="mt-8 space-y-6 text-muted-foreground">
        <section>
          <h2 className="text-xl font-semibold text-foreground">Use of DealSense</h2>
          <p className="mt-2">DealSense provides deal discovery, price comparison, and buying-guide content for informational purposes. You are responsible for confirming final pricing, availability, taxes, shipping, and warranty terms with the merchant.</p>
        </section>
        <section>
          <h2 className="text-xl font-semibold text-foreground">Pricing accuracy</h2>
          <p className="mt-2">Prices and discounts can change quickly. DealSense does not guarantee that displayed prices remain available after you leave the website.</p>
        </section>
        <section>
          <h2 className="text-xl font-semibold text-foreground">Affiliate disclosure</h2>
          <p className="mt-2">DealSense may receive compensation from merchants through sponsored or affiliate links. This does not increase your purchase price.</p>
        </section>
        <section>
          <h2 className="text-xl font-semibold text-foreground">No professional advice</h2>
          <p className="mt-2">Content on DealSense is not financial, legal, or professional advice. Product recommendations should be evaluated against your own needs.</p>
        </section>
      </div>
    </article>
  );
}
