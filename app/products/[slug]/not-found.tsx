import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function ProductNotFound() {
  return (
    <main className="container py-16">
      <div className="max-w-xl">
        <p className="eyebrow">Product unavailable</p>
        <h1 className="mt-2 text-3xl font-bold">Product not found</h1>
        <p className="mt-3 text-muted-foreground">
          This product is not available in the catalog yet, or the backend could not return a matching slug.
        </p>
        <Button asChild className="mt-6">
          <Link href="/deals">Browse deals</Link>
        </Button>
      </div>
    </main>
  );
}
