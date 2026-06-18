import Link from "next/link";
import { ArrowRight, BadgeCheck, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SearchBox } from "@/components/search-box";

export function Hero() {
  return (
    <section className="overflow-hidden border-b">
      <div className="container grid min-h-[620px] items-center gap-10 py-14 lg:grid-cols-[1.05fr_0.95fr]">
        <div className="animate-fade-up">
          <p className="eyebrow">Verified affiliate deals</p>
          <h1 className="mt-4 max-w-4xl text-4xl font-bold leading-tight md:text-6xl">
            Compare prices faster and buy when the deal is real.
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-muted-foreground">
            DealSense tracks products across leading merchants, highlights meaningful price drops, and gives every product a clean comparison page ready for future AI insights.
          </p>
          <div className="mt-8 max-w-2xl">
            <SearchBox />
          </div>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href="/deals">
                Browse deals <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href="/blog">Read buying guides</Link>
            </Button>
          </div>
        </div>
        <div className="relative">
          <div className="absolute inset-0 rounded-full bg-primary/20 blur-3xl" />
          <div className="relative rounded-lg border bg-card/80 p-5 shadow-soft backdrop-blur">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Deal confidence</p>
                <p className="text-3xl font-bold">98.4%</p>
              </div>
              <span className="rounded-md bg-success/15 px-3 py-1 text-sm font-semibold text-success">Live</span>
            </div>
            <div className="space-y-3">
              {[
                ["MacBook Air 13 M3", "$999", "-17%"],
                ["Sony WH-1000XM5", "$298", "-25%"],
                ["Anker Prime Power Bank", "$139", "-22%"]
              ].map(([name, price, drop]) => (
                <div key={name} className="flex items-center justify-between rounded-md border bg-background/70 p-4">
                  <div>
                    <p className="font-medium">{name}</p>
                    <p className="text-sm text-muted-foreground">Best matched merchant</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold">{price}</p>
                    <p className="text-sm font-semibold text-success">{drop}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-5 grid grid-cols-2 gap-3">
              <div className="rounded-md bg-muted p-4">
                <BadgeCheck className="mb-3 h-5 w-5 text-primary" />
                <p className="font-semibold">Merchant verified</p>
              </div>
              <div className="rounded-md bg-muted p-4">
                <Zap className="mb-3 h-5 w-5 text-accent" />
                <p className="font-semibold">Fast SSR pages</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
