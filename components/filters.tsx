import { brands, categories } from "@/lib/data";
import { Button } from "@/components/ui/button";

export function Filters() {
  return (
    <aside className="space-y-6 rounded-lg border bg-card p-5 lg:sticky lg:top-24 lg:h-fit">
      <div>
        <h2 className="font-semibold">Filters</h2>
        <p className="text-sm text-muted-foreground">Refine by category, brand, price, and savings.</p>
      </div>
      <FilterGroup title="Category" items={categories.map((item) => item.name)} />
      <FilterGroup title="Brand" items={brands.map((item) => item.name)} />
      <FilterGroup title="Discount" items={["10% or more", "20% or more", "30% or more", "Clearance"]} />
      <div>
        <p className="mb-3 text-sm font-medium">Price range</p>
        <div className="grid grid-cols-2 gap-2">
          <input className="h-10 rounded-md border bg-background px-3 text-sm" placeholder="$ Min" />
          <input className="h-10 rounded-md border bg-background px-3 text-sm" placeholder="$ Max" />
        </div>
      </div>
      <Button className="w-full" variant="secondary">
        Apply filters
      </Button>
    </aside>
  );
}

function FilterGroup({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <p className="mb-3 text-sm font-medium">{title}</p>
      <div className="space-y-2">
        {items.map((item) => (
          <label key={item} className="flex items-center gap-2 text-sm text-muted-foreground">
            <input type="checkbox" className="h-4 w-4 accent-primary" />
            {item}
          </label>
        ))}
      </div>
    </div>
  );
}
