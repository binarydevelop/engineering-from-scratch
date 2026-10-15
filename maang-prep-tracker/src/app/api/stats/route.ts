import { NextResponse } from 'next/server'
import { fetchTaskStats } from '@/lib/db'

export async function GET() {
  try {
    const { stats, hasDb } = await fetchTaskStats()

    return NextResponse.json({
      success: true,
      hasDb,
      stats,
    })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error fetching stats:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to fetch stats' },
      { status: 500 }
    )
  }
}
