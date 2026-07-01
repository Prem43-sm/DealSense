export type DashboardSummary = {
  products: number;
  price_records: number;
  affiliate_links: number;
  availability_records: number;
  deals: number;
  connector_health: string;
  automation_health: string;
  recent_logs: { source: string; line: string }[];
};

export type AutomationAgent = {
  name: string;
  key: string;
  status: string;
  last_run: string | null;
  processed: number;
  success: number;
  failures: number;
  endpoint: string;
};

export type ConnectorStatus = {
  provider: string;
  status: string;
  message: string | null;
  product_count: number;
};

export type ProductOverview = {
  master_products: number;
  marketplace_sources: number;
  products_added_today: number;
  duplicate_prevented: number;
  latest_product: string | null;
};

export type AffiliateOverview = {
  generated_links: number;
  updated_today: number;
  broken_links: number;
  providers: number;
  latest_links: {
    id: number;
    provider: string;
    status: string;
    affiliate_url: string;
    product_source_id: number;
  }[];
};

export type AvailabilityOverview = {
  in_stock: number;
  out_of_stock: number;
  limited: number;
  preorder: number;
  unknown: number;
  latest: {
    id: number;
    provider: string;
    status: string;
    quantity: number | null;
    product_source_id: number;
  }[];
};

export type DashboardData = {
  summary: DashboardSummary;
  automation: { agents: AutomationAgent[] };
  connectors: { connectors: ConnectorStatus[] };
  products: ProductOverview;
  affiliate: AffiliateOverview;
  availability: AvailabilityOverview;
};

