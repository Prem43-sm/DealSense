import type { Metadata } from "next";
import { AdminShell } from "@/components/dashboard/admin-shell";
import { getDashboardData } from "@/lib/dashboard/api";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Operations Dashboard",
};

export default async function AdminPage() {
  const data = await getDashboardData();
  return <AdminShell data={data} />;
}

