import { NextRequest, NextResponse } from 'next/server'
import { updateTask, deleteTask } from '@/lib/db'

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const body = await request.json()

    const { task, hasDb } = await updateTask(id, body)
    return NextResponse.json({ success: true, hasDb, task })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error updating task:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to update task' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params

    const { success, hasDb } = await deleteTask(id)
    return NextResponse.json({ success, hasDb, message: 'Task deleted successfully' })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error deleting task:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to delete task' },
      { status: 500 }
    )
  }
}
