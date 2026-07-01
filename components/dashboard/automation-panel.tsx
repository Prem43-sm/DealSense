"use client";

import { Play, RefreshCw } from "lucide-react";
import type { AutomationAgent } from "@/types/dashboard";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { StatusBadge } from "@/components/dashboard/badge";
import { useDashboardAction } from "@/hooks/use-dashboard-action";

export function AutomationPanel({ agents }: { agents: AutomationAgent[] }) {
  const { loadingKey, notice, run } = useDashboardAction();

  return (
    <section id="automation" className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-xl font-bold">Automation</h2>
        {notice ? (
          <span className={notice.type === "success" ? "text-sm text-success" : "text-sm text-red-500"}>
            {notice.message}
          </span>
        ) : null}
      </div>
      <div className="grid gap-4 xl:grid-cols-4">
        {agents.map((agent) => (
          <Card key={agent.key}>
            <CardHeader className="space-y-3">
              <div className="flex items-center justify-between gap-3">
                <h3 className="text-sm font-semibold">{agent.name}</h3>
                <StatusBadge status={agent.status} />
              </div>
              <p className="text-xs text-muted-foreground">{agent.last_run ?? "No runs recorded"}</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-3 gap-2 text-sm">
                <Metric label="Processed" value={agent.processed} />
                <Metric label="Success" value={agent.success} />
                <Metric label="Failures" value={agent.failures} />
              </div>
              <Button
                className="w-full"
                size="sm"
                variant="outline"
                disabled={loadingKey === agent.key}
                onClick={() => run(agent.key, agent.endpoint)}
              >
                {loadingKey === agent.key ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
                Run
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md bg-muted p-2">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="font-semibold">{value}</p>
    </div>
  );
}

