"use client";

import Link from "next/link";
import type { Route } from "next";
import * as Dialog from "@radix-ui/react-dialog";
import { Menu, ShoppingBag, X } from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { SearchBox } from "@/components/search-box";
import { categories } from "@/lib/data";

const links = [
  { href: "/deals", label: "Deals" },
  { href: "/categories", label: "Categories" },
  { href: "/brands", label: "Brands" },
  { href: "/blog", label: "Guides" }
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b bg-background/86 backdrop-blur">
      <div className="container flex h-16 items-center gap-4">
        <Link href="/" className="flex items-center gap-2 font-bold">
          <span className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <ShoppingBag className="h-5 w-5" />
          </span>
          <span>DealSense</span>
        </Link>
        <nav className="hidden items-center gap-1 md:flex">
          <div className="group relative">
            <Link href="/deals" className="rounded-md px-3 py-2 text-sm font-medium hover:bg-muted">
              Deals
            </Link>
            <div className="invisible absolute left-0 top-9 w-[560px] rounded-lg border bg-card p-5 opacity-0 shadow-soft transition group-hover:visible group-hover:opacity-100">
              <p className="mb-4 text-sm font-semibold">Shop by category</p>
              <div className="grid grid-cols-2 gap-3">
                {categories.map((category) => (
                  <Link key={category.slug} href={`/categories/${category.slug}` as Route} className="rounded-md p-3 hover:bg-muted">
                    <span className="font-medium">{category.name}</span>
                    <span className="mt-1 block text-sm text-muted-foreground">{category.description}</span>
                  </Link>
                ))}
              </div>
            </div>
          </div>
          {links.slice(1).map((link) => (
            <Link key={link.href} href={link.href} className="rounded-md px-3 py-2 text-sm font-medium hover:bg-muted">
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="ml-auto hidden w-full max-w-sm lg:block">
          <SearchBox compact />
        </div>
        <div className="ml-auto flex items-center gap-1 lg:ml-0">
          <ThemeToggle />
          <Button asChild className="hidden md:inline-flex" variant="accent">
            <Link href="/deals">Track deals</Link>
          </Button>
          <MobileMenu />
        </div>
      </div>
    </header>
  );
}

function MobileMenu() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <Button aria-label="Open menu" className="md:hidden" variant="ghost" size="icon">
          <Menu className="h-5 w-5" />
        </Button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm" />
        <Dialog.Content className="fixed right-0 top-0 z-50 h-full w-[86vw] max-w-sm border-l bg-background p-5 shadow-soft">
          <div className="mb-6 flex items-center justify-between">
            <Dialog.Title className="font-bold">DealSense</Dialog.Title>
            <Dialog.Close asChild>
              <Button aria-label="Close menu" variant="ghost" size="icon">
                <X className="h-5 w-5" />
              </Button>
            </Dialog.Close>
          </div>
          <SearchBox compact />
          <nav className="mt-6 grid gap-2">
            {links.map((link) => (
              <Dialog.Close asChild key={link.href}>
                <Link href={link.href as Route} className="rounded-md px-3 py-3 font-medium hover:bg-muted">
                  {link.label}
                </Link>
              </Dialog.Close>
            ))}
          </nav>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
