"use client";

import { Download, Search } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export function LogsPanel({ logs }: { logs: { source: string; line: string }[] }) {
  const [query, setQuery] = useState("");
  const filtered = useMemo(
    () => logs.filter((log) => `${log.source} ${log.line}`.toLowerCase().includes(query.toLowerCase())),
    [logs, query]
  );

  function download() {
    const blob = new Blob([filtered.map((log) => `[${log.source}] ${log.line}`).join("\n")], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "dealsense-logs.txt";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section id="logs" className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-xl font-bold">Logs</h2>
        <Button size="sm" variant="outline" onClick={download}>
          <Download className="h-4 w-4" />
          Download
        </Button>
      </div>
      <Card>
        <CardHeader>
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input className="pl-9" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search logs" />
          </div>
        </CardHeader>
        <CardContent>
          <div className="max-h-80 overflow-auto rounded-md border bg-background">
            {filtered.map((log, index) => (
              <div key={`${log.source}-${index}`} className="grid gap-2 border-b px-3 py-2 text-xs last:border-0 md:grid-cols-[160px_1fr]">
                <span className="font-semibold text-muted-foreground">{log.source}</span>
                <code className="whitespace-pre-wrap break-words">{log.line}</code>
              </div>
            ))}
            {filtered.length === 0 ? <p className="p-4 text-sm text-muted-foreground">No logs found.</p> : null}
          </div>
        </CardContent>
      </Card>
    </section>
  );
}

