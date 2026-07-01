import { BarChart3 } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function ChartPlaceholder({ title }: { title: string }) {
  return (
    <Card>
      <CardHeader>
        <h3 className="text-sm font-semibold">{title}</h3>
      </CardHeader>
      <CardContent>
        <div className="flex h-44 items-end gap-2 rounded-md border bg-muted/30 p-4">
          {[36, 64, 48, 78, 52, 88, 70].map((height, index) => (
            <div key={index} className="flex flex-1 items-end">
              <div className="w-full rounded-sm bg-primary/70" style={{ height: `${height}%` }} />
            </div>
          ))}
          <BarChart3 className="absolute h-0 w-0" />
        </div>
      </CardContent>
    </Card>
  );
}

