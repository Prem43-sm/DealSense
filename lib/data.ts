import type { BlogPost, Brand, Category, Product } from "@/lib/types";

export const siteConfig = {
  name: "DealSense",
  url: process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealsense.example.com",
  description:
    "Compare live prices, discover verified deals, and find smarter buying guides across top shopping platforms."
};

export const categories: Category[] = [
  {
    name: "Laptops",
    slug: "laptops",
    description: "Creator, gaming, business, and student laptops ranked by real price movement.",
    image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
  },
  {
    name: "Smartphones",
    slug: "smartphones",
    description: "Flagship, foldable, and budget phones with carrier and unlocked offers.",
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"
  },
  {
    name: "Audio",
    slug: "audio",
    description: "Headphones, speakers, earbuds, and studio gear with daily drops.",
    image: "https://images.unsplash.com/photo-1546435770-a3e426bf472b"
  },
  {
    name: "Smart Home",
    slug: "smart-home",
    description: "Security, lighting, thermostats, and connected home bundles.",
    image: "https://images.unsplash.com/photo-1558002038-1055907df827"
  },
  {
    name: "Gaming",
    slug: "gaming",
    description: "Consoles, accessories, monitors, components, and limited time bundles.",
    image: "https://images.unsplash.com/photo-1542751371-adc38448a05e"
  },
  {
    name: "Wearables",
    slug: "wearables",
    description: "Smartwatches, trackers, rings, and fitness tech offers.",
    image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30"
  }
];

export const brands: Brand[] = [
  { name: "Apple", slug: "apple", description: "Premium phones, tablets, laptops, and accessories.", productCount: 18 },
  { name: "Samsung", slug: "samsung", description: "Phones, displays, storage, appliances, and wearables.", productCount: 24 },
  { name: "Sony", slug: "sony", description: "Audio, cameras, gaming, and entertainment hardware.", productCount: 14 },
  { name: "Dell", slug: "dell", description: "Business laptops, gaming PCs, monitors, and docks.", productCount: 16 },
  { name: "Anker", slug: "anker", description: "Chargers, smart home devices, speakers, and power banks.", productCount: 21 },
  { name: "Logitech", slug: "logitech", description: "Peripherals, webcams, gaming gear, and productivity tools.", productCount: 12 }
];

export const products: Product[] = [
  {
    id: "p1",
    name: "MacBook Air 13 M3",
    slug: "macbook-air-13-m3",
    description: "A quiet, efficient ultraportable for students, founders, and frequent travelers.",
    category: "laptops",
    brand: "apple",
    image: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8",
    rating: 4.8,
    reviews: 1824,
    tags: ["Editors pick", "Lowest this month"],
    createdAt: "2026-06-11",
    specs: { Chip: "Apple M3", Memory: "16GB", Storage: "512GB SSD", Display: "13.6-inch Liquid Retina" },
    prices: [
      { merchant: "Amazon", price: 999, originalPrice: 1199, shipping: "Free 2-day", url: "#", inStock: true },
      { merchant: "Best Buy", price: 1049, originalPrice: 1199, shipping: "Store pickup", url: "#", inStock: true },
      { merchant: "Apple", price: 1199, shipping: "Free delivery", url: "#", inStock: true }
    ]
  },
  {
    id: "p2",
    name: "Samsung Galaxy S25 Ultra",
    slug: "samsung-galaxy-s25-ultra",
    description: "A flagship Android phone for photography, productivity, and high-end gaming.",
    category: "smartphones",
    brand: "samsung",
    image: "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf",
    rating: 4.7,
    reviews: 958,
    tags: ["Carrier deal", "Hot"],
    createdAt: "2026-06-14",
    specs: { Display: "6.8-inch AMOLED", Storage: "256GB", Camera: "200MP main", Battery: "5000mAh" },
    prices: [
      { merchant: "Samsung", price: 1099, originalPrice: 1299, shipping: "Free delivery", url: "#", inStock: true },
      { merchant: "Amazon", price: 1149, originalPrice: 1299, shipping: "Free 2-day", url: "#", inStock: true },
      { merchant: "Walmart", price: 1199, shipping: "Free delivery", url: "#", inStock: true }
    ]
  },
  {
    id: "p3",
    name: "Sony WH-1000XM5",
    slug: "sony-wh-1000xm5",
    description: "Noise-canceling headphones with excellent comfort and travel-ready battery life.",
    category: "audio",
    brand: "sony",
    image: "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb",
    rating: 4.9,
    reviews: 4211,
    tags: ["Big drop", "Travel"],
    createdAt: "2026-06-16",
    specs: { Type: "Over-ear", Battery: "30 hours", ANC: "Adaptive", Weight: "250g" },
    prices: [
      { merchant: "Amazon", price: 298, originalPrice: 399, shipping: "Free 2-day", url: "#", inStock: true },
      { merchant: "Target", price: 329, originalPrice: 399, shipping: "Free delivery", url: "#", inStock: true },
      { merchant: "Sony", price: 399, shipping: "Free delivery", url: "#", inStock: true }
    ]
  },
  {
    id: "p4",
    name: "Dell XPS 14 OLED",
    slug: "dell-xps-14-oled",
    description: "A premium Windows laptop with a vivid OLED display and workstation-class polish.",
    category: "laptops",
    brand: "dell",
    image: "https://images.unsplash.com/photo-1541807084-5c52b6b3adef",
    rating: 4.6,
    reviews: 612,
    tags: ["Creator deal"],
    createdAt: "2026-06-10",
    specs: { Processor: "Intel Core Ultra 7", Memory: "32GB", Storage: "1TB SSD", Display: "14.5-inch OLED" },
    prices: [
      { merchant: "Dell", price: 1699, originalPrice: 2099, shipping: "Free delivery", url: "#", inStock: true },
      { merchant: "Best Buy", price: 1799, originalPrice: 2099, shipping: "Store pickup", url: "#", inStock: true }
    ]
  },
  {
    id: "p5",
    name: "Anker Prime 27650 Power Bank",
    slug: "anker-prime-27650-power-bank",
    description: "High-capacity travel charging with fast USB-C output for laptops and phones.",
    category: "smart-home",
    brand: "anker",
    image: "https://images.unsplash.com/photo-1603539444875-76e7684265f6",
    rating: 4.5,
    reviews: 774,
    tags: ["Under $150"],
    createdAt: "2026-06-15",
    specs: { Capacity: "27650mAh", Output: "250W max", Ports: "2 USB-C, 1 USB-A", Display: "Smart status screen" },
    prices: [
      { merchant: "Amazon", price: 139, originalPrice: 179, shipping: "Free 2-day", url: "#", inStock: true },
      { merchant: "Anker", price: 159, originalPrice: 179, shipping: "Free delivery", url: "#", inStock: true }
    ]
  },
  {
    id: "p6",
    name: "Logitech MX Master 4",
    slug: "logitech-mx-master-4",
    description: "A precision productivity mouse for multi-device workflows and long desk sessions.",
    category: "gaming",
    brand: "logitech",
    image: "https://images.unsplash.com/photo-1527814050087-3793815479db",
    rating: 4.7,
    reviews: 1340,
    tags: ["Work setup"],
    createdAt: "2026-06-13",
    specs: { Sensor: "8K DPI", Connectivity: "Bluetooth, USB-C receiver", Battery: "70 days", Buttons: "8 programmable" },
    prices: [
      { merchant: "Logitech", price: 89, originalPrice: 119, shipping: "Free delivery", url: "#", inStock: true },
      { merchant: "Amazon", price: 94, originalPrice: 119, shipping: "Free 2-day", url: "#", inStock: true }
    ]
  }
];

export const posts: BlogPost[] = [
  {
    title: "How to Know Whether a Laptop Deal Is Actually Good",
    slug: "how-to-know-laptop-deal-is-good",
    excerpt: "A practical checklist for specs, historical pricing, warranty terms, and timing your purchase.",
    category: "Buying Guides",
    author: "DealSense Research",
    publishedAt: "2026-06-12",
    readTime: "6 min"
  },
  {
    title: "OLED vs Mini LED Monitors: Which Discount Matters More?",
    slug: "oled-vs-mini-led-monitors",
    excerpt: "Compare panel strengths and learn which price drops are worth acting on.",
    category: "Product Comparisons",
    author: "Mira Chen",
    publishedAt: "2026-06-08",
    readTime: "8 min"
  },
  {
    title: "The Smarter Way to Track Phone Launch Offers",
    slug: "track-phone-launch-offers",
    excerpt: "Trade-in credits, carrier locks, and unlocked discounts explained in plain terms.",
    category: "Technology News",
    author: "Noah Patel",
    publishedAt: "2026-06-03",
    readTime: "5 min"
  }
];

export function bestPrice(product: Product) {
  return Math.min(...product.prices.map((price) => price.price));
}

export function discountPercent(product: Product) {
  const best = product.prices.reduce((lowest, current) => (current.price < lowest.price ? current : lowest), product.prices[0]);
  if (!best.originalPrice) return 0;
  return Math.round(((best.originalPrice - best.price) / best.originalPrice) * 100);
}

export function getProduct(slug: string) {
  return products.find((product) => product.slug === slug);
}

export function getCategory(slug: string) {
  return categories.find((category) => category.slug === slug);
}

export function getBrand(slug: string) {
  return brands.find((brand) => brand.slug === slug);
}

export function currency(value: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}
