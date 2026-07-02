"use client";

import Link from "next/link";
import { ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { recordAnalyticsEvent } from "@/lib/analytics";

export function AffiliateButton({
  href,
  productSourceId,
  label = "Buy Now",
  disabled = false,
  variant = "accent",
}: {
  href?: string;
  productSourceId?: number;
  label?: string;
  disabled?: boolean;
  variant?: "default" | "accent" | "outline";
}) {
  if (disabled || !href || href === "#") {
    return (
      <Button disabled variant={variant}>
        Deal unavailable
      </Button>
    );
  }

  function trackClick() {
    if (!productSourceId) return;
    recordAnalyticsEvent("/analytics/events/affiliate-click", { product_source_id: productSourceId });
  }

  return (
    <Button asChild variant={variant}>
      <Link href={href} target="_blank" rel="nofollow sponsored noopener" onClick={trackClick}>
        {label}
        <ExternalLink className="h-4 w-4" />
      </Link>
    </Button>
  );
}
