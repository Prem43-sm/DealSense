export default function ProductLoading() {
  return (
    <main className="container py-8">
      <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_360px]">
        <div className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="aspect-square animate-pulse rounded-lg bg-muted" />
            <div className="space-y-4">
              <div className="h-4 w-32 animate-pulse rounded bg-muted" />
              <div className="h-12 w-4/5 animate-pulse rounded bg-muted" />
              <div className="h-24 animate-pulse rounded bg-muted" />
              <div className="h-28 animate-pulse rounded-lg bg-muted" />
            </div>
          </div>
          <div className="h-64 animate-pulse rounded-lg bg-muted" />
        </div>
        <div className="h-80 animate-pulse rounded-lg bg-muted" />
      </div>
    </main>
  );
}
