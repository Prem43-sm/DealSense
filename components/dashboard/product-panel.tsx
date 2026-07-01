import { CopyCheck, Layers, PackagePlus, ShieldCheck, Sparkles } from "lucide-react";
import type { ProductOverview } from "@/types/dashboard";
import { StatCard } from "@/components/dashboard/stat-card";

export function ProductPanel({ data }: { data: ProductOverview }) {
  return (
    <section id="products" className="space-y-4">
      <h2 className="text-xl font-bold">Products</h2>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <StatCard label="Master Products" value={data.master_products} Icon={Layers} />
        <StatCard label="Marketplace Sources" value={data.marketplace_sources} Icon={CopyCheck} />
        <StatCard label="Products Added Today" value={data.products_added_today} Icon={PackagePlus} />
        <StatCard label="Duplicate Prevented" value={data.duplicate_prevented} Icon={ShieldCheck} />
        <StatCard label="Latest Product" value={data.latest_product ?? "None"} Icon={Sparkles} />
      </div>
    </section>
  );
}

