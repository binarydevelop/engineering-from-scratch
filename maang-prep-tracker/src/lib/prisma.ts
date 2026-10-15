import { PrismaClient } from '@prisma/client'

// Auto-detect Supabase & Vercel Postgres environment variables
export function getResolvedDatabaseUrl(): string | undefined {
  const envCandidates = [
    process.env.DATABASE_URL,
    process.env.POSTGRES_PRISMA_URL, // Supabase default in Vercel
    process.env.POSTGRES_URL,        // Supabase / Vercel default
    process.env.POSTGRES_URL_NON_POOLING,
    process.env.SUPABASE_DATABASE_URL,
    process.env.SUPABASE_DB_URL,
    process.env.SUPABASE_POSTGRES_URL,
    process.env.SUPABASE_DIRECT_URL,
    process.env.POSTGRESQL_URL,
  ]

  for (const candidate of envCandidates) {
    if (candidate && candidate.trim().length > 0) {
      return candidate.trim()
    }
  }

  // If Supabase split credentials exist
  if (
    process.env.POSTGRES_USER &&
    process.env.POSTGRES_PASSWORD &&
    process.env.POSTGRES_HOST &&
    process.env.POSTGRES_DATABASE
  ) {
    return `postgresql://${process.env.POSTGRES_USER}:${process.env.POSTGRES_PASSWORD}@${process.env.POSTGRES_HOST}:5432/${process.env.POSTGRES_DATABASE}?sslmode=require`
  }

  return undefined
}

const resolvedUrl = getResolvedDatabaseUrl()

if (resolvedUrl && !process.env.DATABASE_URL) {
  process.env.DATABASE_URL = resolvedUrl
}

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    datasources: resolvedUrl
      ? {
          db: {
            url: resolvedUrl,
          },
        }
      : undefined,
    log: process.env.NODE_ENV === 'development' ? ['warn', 'error'] : ['error'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

export default prisma
