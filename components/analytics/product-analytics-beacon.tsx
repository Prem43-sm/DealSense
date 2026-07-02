"use client";

import { useEffect } from "react";
import { recordAnalyticsEvent } from "@/lib/analytics";

type ProductAnalyticsBeaconProps =
  | {
      event: "view" | "detail-visit";
      productId: number;
    }
  | {
      event: "detail-visit-by-slug";
      slug: string;
    };

const eventPath = {
  view: "/analytics/events/view",
  "detail-visit": "/analytics/events/detail-visit",
  "detail-visit-by-slug": "/analytics/events/detail-visit-by-slug",
} as const;

export function ProductAnalyticsBeacon(props: ProductAnalyticsBeaconProps) {
  useEffect(() => {
    if (props.event === "detail-visit-by-slug") {
      recordAnalyticsEvent(eventPath[props.event], { slug: props.slug });
      return;
    }

    recordAnalyticsEvent(eventPath[props.event], { product_id: props.productId });
  }, [props]);

  return null;
}
