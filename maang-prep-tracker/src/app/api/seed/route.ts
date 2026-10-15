import { NextResponse } from 'next/server'
import { reseedAllTasks } from '@/lib/db'

export async function POST() {
  try {
    const { count, hasDb } = await reseedAllTasks()

    return NextResponse.json({
      success: true,
      hasDb,
      message: `Database successfully re-seeded with ${count} tasks`,
      count,
    })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error during re-seed:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to re-seed tasks' },
      { status: 500 }
    )
  }
}
