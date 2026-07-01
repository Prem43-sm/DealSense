"use client";

import { useState } from "react";
import { callDashboardAction } from "@/lib/dashboard/api";

export function useDashboardAction() {
  const [loadingKey, setLoadingKey] = useState<string | null>(null);
  const [notice, setNotice] = useState<{ type: "success" | "error"; message: string } | null>(null);

  async function run(key: string, path: string) {
    setLoadingKey(key);
    setNotice(null);
    try {
      await callDashboardAction(path);
      setNotice({ type: "success", message: "Action completed successfully." });
    } catch {
      setNotice({ type: "error", message: "Action failed. Check backend status and logs." });
    } finally {
      setLoadingKey(null);
    }
  }

  return { loadingKey, notice, run };
}

