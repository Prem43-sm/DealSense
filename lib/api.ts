const API_BASE = "http://localhost:8000";

export async function getProducts() {
  const response = await fetch(`${API_BASE}/products`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json();
}