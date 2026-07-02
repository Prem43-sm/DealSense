"use client";

import Image from "next/image";
import Link from "next/link";
import { BadgeCheck, ExternalLink } from "lucide-react";
import { ProductAnalyticsBeacon } from "@/components/analytics/product-analytics-beacon";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { recordAnalyticsEvent } from "@/lib/analytics";
import { currency } from "@/lib/data";
import type { Product } from "@/lib/types";

type FeaturedDeal = Product & {
  availabilityLabel: string;
  dealUrl?: string;
  dealDisabled?: boolean;
  productSourceId?: number;
};

export function FeaturedDealCard({ product }: { product: FeaturedDeal }) {
  const best = Math.min(...product.prices.map((price) => price.price));
  const href = product.dealUrl || `/products/${product.slug}`;
  const productId = Number(product.id);

  function trackAffiliateClick() {
    if (!product.productSourceId) return;
    recordAnalyticsEvent("/analytics/events/affiliate-click", { product_source_id: product.productSourceId });
  }

  return (
    <Card className="group overflow-hidden">
      {Number.isFinite(productId) ? <ProductAnalyticsBeacon event="view" productId={productId} /> : null}
      <Link href={`/products/${product.slug}`} className="block">
        <div className="relative aspect-[4/3] overflow-hidden bg-muted">
          <Image
            src={`${product.image}?auto=format&fit=crop&w=800&q=75`}
            alt={product.name}
            fill
            sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"
            className="object-cover transition duration-300 group-hover:scale-105"
          />
          <span className="absolute left-3 top-3 rounded-md bg-accent px-2 py-1 text-xs font-bold text-accent-foreground">
            Live deal
          </span>
        </div>
      </Link>
      <div className="space-y-4 p-4">
        <div>
          <div className="mb-2 flex items-center gap-2 text-xs text-muted-foreground">
            <span className="capitalize">{product.brand || "Unknown brand"}</span>
            <span>|</span>
            <span className="capitalize">{(product.category || "uncategorized").replace("-", " ")}</span>
          </div>
          <Link href={`/products/${product.slug}`} className="line-clamp-2 font-semibold leading-snug hover:text-primary">
            {product.name}
          </Link>
        </div>
        <div className="flex items-end justify-between gap-3">
          <div>
            <p className="text-xs text-muted-foreground">Lowest price</p>
            <p className="text-2xl font-bold">{currency(best)}</p>
          </div>
          <span className="inline-flex items-center gap-1 rounded-md border bg-muted px-2 py-1 text-xs font-semibold">
            <BadgeCheck className="h-3 w-3 text-success" />
            {product.availabilityLabel}
          </span>
        </div>
        <Button asChild={!product.dealDisabled} className="w-full" size="sm" disabled={product.dealDisabled}>
          {product.dealDisabled ? (
            <span>Deal unavailable</span>
          ) : (
            <Link
              href={href}
              target={href.startsWith("http") ? "_blank" : undefined}
              rel={href.startsWith("http") ? "nofollow sponsored noopener" : undefined}
              onClick={trackAffiliateClick}
            >
              View Deal <ExternalLink className="h-4 w-4" />
            </Link>
          )}
        </Button>
      </div>
    </Card>
  );
}
