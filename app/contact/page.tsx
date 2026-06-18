import type { Metadata } from "next";
import { Mail } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const contactEmail = process.env.NEXT_PUBLIC_CONTACT_EMAIL ?? "hello@dealsense.example.com";

export const metadata: Metadata = {
  title: "Contact",
  description: "Contact DealSense for corrections, partnerships, affiliate questions, or product listing updates.",
  alternates: { canonical: "/contact" }
};

export default function ContactPage() {
  return (
    <div className="container grid gap-10 py-12 lg:grid-cols-[0.8fr_1.2fr]">
      <section>
        <p className="eyebrow">Contact</p>
        <h1 className="mt-3 text-4xl font-bold md:text-5xl">Send DealSense a note.</h1>
        <p className="mt-4 text-muted-foreground">
          Use this page for product corrections, merchant partnership requests, affiliate disclosure questions, or editorial feedback.
        </p>
        <a href={`mailto:${contactEmail}`} className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-primary">
          <Mail className="h-4 w-4" aria-hidden="true" />
          {contactEmail}
        </a>
      </section>
      <form className="rounded-lg border bg-card p-6" aria-label="Contact form">
        <div className="grid gap-4">
          <label className="grid gap-2 text-sm font-medium">
            Name
            <Input name="name" autoComplete="name" placeholder="Your name" />
          </label>
          <label className="grid gap-2 text-sm font-medium">
            Email
            <Input name="email" type="email" autoComplete="email" placeholder="you@example.com" />
          </label>
          <label className="grid gap-2 text-sm font-medium">
            Message
            <textarea
              name="message"
              rows={6}
              className="min-h-36 rounded-md border border-input bg-background px-3 py-2 text-sm outline-none focus-visible:ring-2 focus-visible:ring-ring"
              placeholder="How can we help?"
            />
          </label>
          <Button type="submit">Send message</Button>
          <p className="text-xs text-muted-foreground">Static demo form. Connect to a server action or form provider before production intake.</p>
        </div>
      </form>
    </div>
  );
}
