import type { NextConfig } from "next";

// Auto-detect and bridge Supabase / Vercel Postgres environment variables to DATABASE_URL
const resolvedDbUrl =
  process.env.DATABASE_URL ||
  process.env.POSTGRES_PRISMA_URL ||
  process.env.POSTGRES_URL ||
  process.env.POSTGRES_URL_NON_POOLING ||
  process.env.SUPABASE_DATABASE_URL ||
  process.env.SUPABASE_DB_URL ||
  process.env.SUPABASE_POSTGRES_URL ||
  process.env.SUPABASE_DIRECT_URL ||
  (process.env.POSTGRES_USER && process.env.POSTGRES_PASSWORD && process.env.POSTGRES_HOST && process.env.POSTGRES_DATABASE
    ? `postgresql://${process.env.POSTGRES_USER}:${process.env.POSTGRES_PASSWORD}@${process.env.POSTGRES_HOST}:5432/${process.env.POSTGRES_DATABASE}?sslmode=require`
    : undefined);

if (resolvedDbUrl && !process.env.DATABASE_URL) {
  process.env.DATABASE_URL = resolvedDbUrl;
}

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;

