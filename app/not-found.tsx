import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="container flex min-h-[60vh] flex-col items-center justify-center py-16 text-center">
      <p className="eyebrow">404</p>
      <h1 className="mt-3 text-4xl font-bold">This deal page moved or expired</h1>
      <p className="mt-3 max-w-lg text-muted-foreground">Browse current deals or search for the product again.</p>
      <Button asChild className="mt-6">
        <Link href="/deals">Browse deals</Link>
      </Button>
    </div>
  );
}
