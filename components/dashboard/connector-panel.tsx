"use client";

import { HeartPulse, RefreshCw } from "lucide-react";
import type { ConnectorStatus } from "@/types/dashboard";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { StatusBadge } from "@/components/dashboard/badge";
import { useDashboardAction } from "@/hooks/use-dashboard-action";

export function ConnectorPanel({ connectors }: { connectors: ConnectorStatus[] }) {
  const { loadingKey, notice, run } = useDashboardAction();

  return (
    <section id="connectors" className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-xl font-bold">Connectors</h2>
        {notice ? <span className="text-sm text-muted-foreground">{notice.message}</span> : null}
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {connectors.map((connector) => (
          <Card key={connector.provider}>
            <CardHeader>
              <div className="flex items-center justify-between gap-3">
                <h3 className="font-semibold capitalize">{connector.provider}</h3>
                <StatusBadge status={connector.status} />
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Products</span>
                <span className="font-semibold">{connector.product_count}</span>
              </div>
              <p className="min-h-5 text-xs text-muted-foreground">{connector.message ?? "Unknown"}</p>
              <Button
                className="w-full"
                size="sm"
                variant="outline"
                disabled={loadingKey === connector.provider}
                onClick={() => run(connector.provider, `/connectors/${connector.provider}/health`)}
              >
                {loadingKey === connector.provider ? <RefreshCw className="h-4 w-4 animate-spin" /> : <HeartPulse className="h-4 w-4" />}
                Health
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

