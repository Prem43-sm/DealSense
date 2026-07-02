const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export type BackendProductPrice = {
  id: number;
  product_id: number;
  store_id: number;
  current_price: string | number;
  availability: boolean;
  affiliate_url: string;
  updated_at: string;
  store: {
    id: number;
    name: string;
    logo_url?: string | null;
  };
};

export type BackendProduct = {
  id: number;
  title: string;
  slug: string;
  brand?: string | null;
  category?: string | null;
  image_url?: string | null;
  description?: string | null;
  created_at: string;
  prices?: BackendProductPrice[];
};

export async function getProducts(): Promise<BackendProduct[]> {
  const response = await fetch(`${API_BASE}/products`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json();
}

export async function getFeaturedProducts(limit = 4): Promise<BackendProduct[]> {
  const response = await fetch(`${API_BASE}/products?limit=${limit}&with_prices=true`, {
    next: { revalidate: 60 },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch featured products");
  }

  return response.json();
}
