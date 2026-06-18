import type { MetadataRoute } from "next";
import { brands, categories, posts, products, siteConfig } from "@/lib/data";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes = ["", "/deals", "/categories", "/brands", "/blog", "/search", "/about", "/contact", "/privacy", "/terms"];
  return [
    ...staticRoutes.map((route) => ({ url: `${siteConfig.url}${route}`, lastModified: new Date() })),
    ...products.map((product) => ({ url: `${siteConfig.url}/products/${product.slug}`, lastModified: new Date(product.createdAt) })),
    ...categories.map((category) => ({ url: `${siteConfig.url}/categories/${category.slug}`, lastModified: new Date() })),
    ...brands.map((brand) => ({ url: `${siteConfig.url}/brands/${brand.slug}`, lastModified: new Date() })),
    ...posts.map((post) => ({ url: `${siteConfig.url}/blog/${post.slug}`, lastModified: new Date(post.publishedAt) }))
  ];
}
