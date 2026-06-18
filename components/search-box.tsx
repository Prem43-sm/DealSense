"use client";

import { Search } from "lucide-react";
import { useMemo, useState } from "react";
import Link from "next/link";
import { products } from "@/lib/data";
import { Input } from "@/components/ui/input";

export function SearchBox({ compact = false }: { compact?: boolean }) {
  const [query, setQuery] = useState("");
  const suggestions = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (q.length < 2) return [];
    return products
      .filter((product) => product.name.toLowerCase().includes(q) || product.brand.includes(q))
      .slice(0, 5);
  }, [query]);

  return (
    <div className="relative w-full">
      <form action="/search" className="relative">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          name="q"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={compact ? "Search deals" : "Search laptops, phones, headphones..."}
          className="h-12 rounded-lg pl-10 pr-4"
        />
      </form>
      {suggestions.length > 0 ? (
        <div className="absolute z-30 mt-2 w-full overflow-hidden rounded-lg border bg-card shadow-soft">
          {suggestions.map((product) => (
            <Link
              key={product.id}
              href={`/products/${product.slug}`}
              className="block px-4 py-3 text-sm transition hover:bg-muted"
            >
              <span className="font-medium">{product.name}</span>
              <span className="ml-2 text-muted-foreground">{product.category}</span>
            </Link>
          ))}
        </div>
      ) : null}
    </div>
  );
}
