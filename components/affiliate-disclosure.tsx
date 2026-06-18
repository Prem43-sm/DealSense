import Link from "next/link";
import { ShieldCheck } from "lucide-react";

export function AffiliateDisclosure() {
  return (
    <div className="border-b bg-accent/12 text-sm">
      <div className="container flex flex-col gap-2 py-3 text-muted-foreground sm:flex-row sm:items-center sm:justify-between">
        <p className="flex items-start gap-2">
          <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
          <span>
            Affiliate disclosure: DealSense may earn a commission when you buy through merchant links, at no extra cost to you.
          </span>
        </p>
        <Link href="/privacy" className="font-medium text-foreground hover:text-primary">
          Learn more
        </Link>
      </div>
    </div>
  );
}
