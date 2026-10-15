import { NextRequest, NextResponse } from 'next/server'
import { fetchAllTasks, createTask } from '@/lib/db'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const search = searchParams.get('search')?.trim() || ''
    const sprint = searchParams.get('sprint')?.trim() || ''
    const week = searchParams.get('week')?.trim() || ''
    const status = searchParams.get('status')?.trim() || ''
    const priority = searchParams.get('priority')?.trim() || ''

    const { tasks, hasDb } = await fetchAllTasks({
      search,
      sprint,
      week,
      status,
      priority,
    })

    return NextResponse.json({
      success: true,
      hasDb,
      count: tasks.length,
      tasks,
    })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error fetching tasks:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to fetch tasks' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { taskName, date } = body

    if (!taskName || !date) {
      return NextResponse.json(
        { success: false, error: 'taskName and date are required' },
        { status: 400 }
      )
    }

    const { task, hasDb } = await createTask(body)
    return NextResponse.json({ success: true, hasDb, task }, { status: 201 })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error creating task:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to create task' },
      { status: 500 }
    )
  }
}
