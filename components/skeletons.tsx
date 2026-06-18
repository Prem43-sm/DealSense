export function ProductSkeletonGrid() {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {Array.from({ length: 8 }).map((_, index) => (
        <div key={index} className="overflow-hidden rounded-lg border bg-card">
          <div className="aspect-[4/3] animate-pulse bg-muted" />
          <div className="space-y-3 p-4">
            <div className="h-4 w-1/2 animate-pulse rounded bg-muted" />
            <div className="h-5 animate-pulse rounded bg-muted" />
            <div className="h-8 w-1/3 animate-pulse rounded bg-muted" />
          </div>
        </div>
      ))}
    </div>
  );
}
