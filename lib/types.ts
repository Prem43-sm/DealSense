export type MerchantPrice = {
  merchant: string;
  price: number;
  originalPrice?: number;
  shipping: string;
  url: string;
  inStock: boolean;
};

export type Category = {
  name: string;
  slug: string;
  description: string;
  image: string;
};

export type Brand = {
  name: string;
  slug: string;
  description: string;
  productCount: number;
};

export type Product = {
  id: string;
  name: string;
  slug: string;
  description: string;
  category: string;
  brand: string;
  image: string;
  rating: number;
  reviews: number;
  specs: Record<string, string>;
  prices: MerchantPrice[];
  tags: string[];
  createdAt: string;
};

export type BlogPost = {
  title: string;
  slug: string;
  excerpt: string;
  category: string;
  author: string;
  publishedAt: string;
  readTime: string;
};
