import { NextResponse } from 'next/server'
import prisma from '@/lib/prisma'
import initialTasks from '@/data/initial-tasks.json'

export async function POST() {
  try {
    // Delete all existing tasks
    const deleted = await prisma.task.deleteMany({})

    // Re-seed all 191 tasks
    const created = await prisma.task.createMany({
      data: initialTasks,
    })

    return NextResponse.json({
      success: true,
      message: `Database successfully re-seeded with ${created.count} tasks (cleared ${deleted.count})`,
      count: created.count,
    })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error during re-seed:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to re-seed database' },
      { status: 500 }
    )
  }
}
