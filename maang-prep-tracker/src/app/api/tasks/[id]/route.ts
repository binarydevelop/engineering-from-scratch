import { NextRequest, NextResponse } from 'next/server'
import prisma from '@/lib/prisma'

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const body = await request.json()

    const updatedTask = await prisma.task.update({
      where: { id },
      data: body,
    })

    return NextResponse.json({ success: true, task: updatedTask })
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

    await prisma.task.delete({
      where: { id },
    })

    return NextResponse.json({ success: true, message: 'Task deleted successfully' })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error deleting task:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to delete task' },
      { status: 500 }
    )
  }
}
