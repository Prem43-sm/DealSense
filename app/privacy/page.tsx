import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "DealSense privacy policy covering analytics, affiliate links, cookies, and user contact information.",
  alternates: { canonical: "/privacy" }
};

export default function PrivacyPage() {
  return (
    <article className="container max-w-3xl py-12">
      <p className="eyebrow">Legal</p>
      <h1 className="mt-3 text-4xl font-bold">Privacy Policy</h1>
      <p className="mt-3 text-sm text-muted-foreground">Last updated: June 18, 2026</p>
      <div className="mt-8 space-y-6 text-muted-foreground">
        <section>
          <h2 className="text-xl font-semibold text-foreground">Information we collect</h2>
          <p className="mt-2">DealSense may collect basic analytics, search queries, contact form submissions, saved-product preferences, and technical logs needed to operate the website.</p>
        </section>
        <section>
          <h2 className="text-xl font-semibold text-foreground">Affiliate links</h2>
          <p className="mt-2">Some outbound merchant links are affiliate links. We may earn a commission if you purchase through those links, and merchants may use cookies or tracking parameters to attribute referrals.</p>
        </section>
        <section>
          <h2 className="text-xl font-semibold text-foreground">Cookies and analytics</h2>
          <p className="mt-2">Production deployments may use privacy-conscious analytics, performance monitoring, and cookies for preferences such as theme selection.</p>
        </section>
        <section>
          <h2 className="text-xl font-semibold text-foreground">Contact</h2>
          <p className="mt-2">For privacy questions, contact the address listed on the Contact page.</p>
        </section>
      </div>
    </article>
  );
}
