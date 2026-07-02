import { cn } from "@/lib/utils";

export function StatusBadge({ status }: { status: string }) {
  const normalized = status.toUpperCase();
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-1 text-xs font-semibold",
        normalized === "IN_STOCK" && "border-success/30 bg-success/10 text-success",
        normalized === "LIMITED_STOCK" && "border-warning/30 bg-warning/10 text-warning",
        normalized === "PREORDER" && "border-primary/30 bg-primary/10 text-primary",
        normalized === "OUT_OF_STOCK" && "border-border bg-muted text-muted-foreground",
        normalized === "DISCONTINUED" && "border-border bg-muted text-muted-foreground",
        normalized === "UNKNOWN" && "border-border bg-background text-muted-foreground"
      )}
    >
      {status.replaceAll("_", " ")}
    </span>
  );
}
