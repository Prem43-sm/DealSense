"use client";

import { Button } from "@/components/ui/button";

export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <div className="container flex min-h-[60vh] flex-col items-center justify-center py-16 text-center">
      <p className="eyebrow">Error</p>
      <h1 className="mt-3 text-4xl font-bold">Something interrupted this comparison</h1>
      <p className="mt-3 max-w-lg text-muted-foreground">Try again and DealSense will reload the current route.</p>
      <Button className="mt-6" onClick={reset}>Retry</Button>
    </div>
  );
}
