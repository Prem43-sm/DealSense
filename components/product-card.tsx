import Image from "next/image";
import Link from "next/link";
import { Heart, Scale, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { bestPrice, currency, discountPercent } from "@/lib/data";
import type { Product } from "@/lib/types";

export function ProductCard({ product }: { product: Product }) {
  const discount = discountPercent(product);

  return (
    <Card className="group overflow-hidden">
      <Link href={`/products/${product.slug}`} className="block">
        <div className="relative aspect-[4/3] overflow-hidden bg-muted">
          <Image
            src={`${product.image}?auto=format&fit=crop&w=800&q=75`}
            alt={product.name}
            fill
            sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"
            className="object-cover transition duration-300 group-hover:scale-105"
          />
          {discount > 0 ? (
            <span className="absolute left-3 top-3 rounded-md bg-accent px-2 py-1 text-xs font-bold text-accent-foreground">
              {discount}% off
            </span>
          ) : null}
        </div>
      </Link>
      <div className="space-y-4 p-4">
        <div>
          <div className="mb-2 flex items-center gap-2 text-xs text-muted-foreground">
            <span className="capitalize">{product.brand}</span>
            <span>•</span>
            <span className="capitalize">{product.category.replace("-", " ")}</span>
          </div>
          <Link href={`/products/${product.slug}`} className="line-clamp-2 font-semibold leading-snug hover:text-primary">
            {product.name}
          </Link>
        </div>
        <div className="flex items-end justify-between">
          <div>
            <p className="text-xs text-muted-foreground">Best price</p>
            <p className="text-2xl font-bold">{currency(bestPrice(product))}</p>
          </div>
          <div className="flex items-center gap-1 text-sm text-muted-foreground">
            <Star className="h-4 w-4 fill-warning text-warning" />
            {product.rating}
          </div>
        </div>
        <div className="grid grid-cols-[1fr_auto_auto] gap-2">
          <Button asChild size="sm">
            <Link href={`/products/${product.slug}`}>Compare</Link>
          </Button>
          <Button aria-label="Save product" variant="outline" size="icon">
            <Heart className="h-4 w-4" />
          </Button>
          <Button aria-label="Add to compare" variant="outline" size="icon">
            <Scale className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </Card>
  );
}
