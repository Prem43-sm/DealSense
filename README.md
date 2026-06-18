# DealSense

[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=nextdotjs)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-149eca?logo=react&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

DealSense is a production-ready affiliate deal and price comparison website built with Next.js 15, React, TypeScript, Tailwind CSS, shadcn-style UI primitives, and a PostgreSQL-ready schema.

## Features

- Premium responsive affiliate comparison UI
- Dark mode, light mode, and system theme detection
- Product cards, price comparison pages, category pages, brand pages, blog pages, and search
- Affiliate disclosure banner and sponsored outbound merchant links
- Privacy Policy, Terms and Conditions, About, and Contact pages
- Dynamic metadata, Open Graph tags, Twitter cards, canonical URLs, robots, sitemap, and JSON-LD
- Optimized Next/Image usage, static generation where appropriate, and SSR for search
- PostgreSQL schema for products, categories, brands, affiliate links, price history, users, saved products, and blog posts

## Tech Stack

- Next.js App Router
- React 19
- TypeScript strict mode
- Tailwind CSS
- Radix UI primitives
- lucide-react icons
- next-themes
- PostgreSQL via `pg`

## Getting Started

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Production Build

```bash
npm install
npm run build
npm start
```

## Environment Variables

Copy `.env.example` to `.env.local` for local development.

```bash
DATABASE_URL="postgresql://dealsense:dealsense@localhost:5432/dealsense"
NEXT_PUBLIC_SITE_URL="https://dealsense.example.com"
NEXT_PUBLIC_CONTACT_EMAIL="hello@dealsense.example.com"
```

`DATABASE_URL` is only required when replacing seed data with PostgreSQL queries. The current demo builds on Vercel without a database.

## Folder Structure

```text
app/
  about/
  blog/
  brands/
  categories/
  contact/
  deals/
  privacy/
  products/
  search/
  terms/
components/
  layout/
  sections/
  ui/
db/
lib/
public/
```

## SEO

DealSense includes:

- Dynamic route metadata
- Open Graph and Twitter card metadata
- Canonical URLs
- `app/robots.ts`
- `app/sitemap.ts`
- Product JSON-LD
- Website JSON-LD
- Organization JSON-LD
- SEO-friendly route slugs
- Breadcrumb navigation

## Vercel Deployment

1. Push this repository to GitHub.
2. Import the repository in Vercel.
3. Framework preset: Next.js.
4. Build command: `npm run build`.
5. Install command: `npm install`.
6. Add `NEXT_PUBLIC_SITE_URL` with your production domain.
7. Add `NEXT_PUBLIC_CONTACT_EMAIL` if you want a custom contact address.
8. Add `DATABASE_URL` only after wiring the app to a production PostgreSQL database.

GitHub Actions are optional and are not required for Vercel deployment.

## GitHub Publishing

```bash
git init
git remote add origin https://github.com/Prem43-sm/DealSense.git
git add .
git commit -m "Production ready Vercel release"
git branch -M main
git push origin main
```

If the remote already exists locally, skip `git init` and `git remote add origin`.

## Database

The PostgreSQL schema lives in `db/schema.sql` and includes:

- users
- categories
- brands
- products
- affiliate_links
- price_history
- blog_posts
- saved_products

## Affiliate Compliance

DealSense shows a site-wide affiliate disclosure banner and marks outbound merchant buttons with `rel="nofollow sponsored noopener"`.

## License

MIT
