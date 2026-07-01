import { cn } from "@/lib/utils";

export function StatusBadge({ status }: { status: string }) {
  const normalized = status.toLowerCase();
  return (
    <span
      className={cn(
        "inline-flex h-6 items-center rounded-full border px-2 text-xs font-semibold",
        normalized.includes("ready") || normalized.includes("valid") || normalized.includes("stock")
          ? "border-success/30 bg-success/10 text-success"
          : normalized.includes("offline") || normalized.includes("invalid") || normalized.includes("out")
            ? "border-red-500/30 bg-red-500/10 text-red-600 dark:text-red-300"
            : "border-warning/30 bg-warning/10 text-warning"
      )}
    >
      {status}
    </span>
  );
}

