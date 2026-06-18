import Link from "next/link";
import type { Route } from "next";

export function Breadcrumbs({ items }: { items: { label: string; href?: string }[] }) {
  return (
    <nav aria-label="Breadcrumb" className="container pt-6 text-sm text-muted-foreground">
      <ol className="flex flex-wrap items-center gap-2">
        <li>
          <Link href="/" className="hover:text-foreground">
            Home
          </Link>
        </li>
        {items.map((item) => (
          <li key={item.label} className="flex items-center gap-2">
            <span>/</span>
            {item.href ? (
              <Link href={item.href as Route} className="hover:text-foreground">
                {item.label}
              </Link>
            ) : (
              <span className="text-foreground">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
