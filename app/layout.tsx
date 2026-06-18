import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import type { ReactNode } from "react";
import "./globals.css";
import { Providers } from "@/app/providers";
import { AffiliateDisclosure } from "@/components/affiliate-disclosure";
import { Footer } from "@/components/layout/footer";
import { Navbar } from "@/components/layout/navbar";
import { siteConfig } from "@/lib/data";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: {
    default: "DealSense - Compare Prices and Discover Verified Deals",
    template: "%s | DealSense"
  },
  description: siteConfig.description,
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url: siteConfig.url,
    title: "DealSense",
    description: siteConfig.description,
    siteName: "DealSense"
  },
  twitter: {
    card: "summary_large_image",
    title: "DealSense",
    description: siteConfig.description
  }
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  colorScheme: "dark light",
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#0c111d" },
    { media: "(prefers-color-scheme: light)", color: "#f8fafc" }
  ]
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <Navbar />
          <AffiliateDisclosure />
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify({
                "@context": "https://schema.org",
                "@type": "Organization",
                name: siteConfig.name,
                url: siteConfig.url,
                contactPoint: {
                  "@type": "ContactPoint",
                  email: process.env.NEXT_PUBLIC_CONTACT_EMAIL ?? "hello@dealsense.example.com",
                  contactType: "customer support"
                }
              })
            }}
          />
          <main>{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
