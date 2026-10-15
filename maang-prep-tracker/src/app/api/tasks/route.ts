import { NextRequest, NextResponse } from 'next/server'
import prisma from '@/lib/prisma'
import initialTasks from '@/data/initial-tasks.json'
import { Prisma } from '@prisma/client'

export async function GET(request: NextRequest) {
  try {
    // Check if database is empty; if so, auto-seed with initial tasks
    const count = await prisma.task.count()
    if (count === 0) {
      console.log('Database empty, performing initial seed...')
      await prisma.task.createMany({
        data: initialTasks,
      })
    }

    const { searchParams } = new URL(request.url)
    const search = searchParams.get('search')?.trim() || ''
    const sprint = searchParams.get('sprint')?.trim() || ''
    const week = searchParams.get('week')?.trim() || ''
    const status = searchParams.get('status')?.trim() || ''
    const priority = searchParams.get('priority')?.trim() || ''

    const where: Prisma.TaskWhereInput = {}

    if (sprint && sprint !== 'all') {
      where.sprint = { contains: sprint, mode: 'insensitive' }
    }

    if (week && week !== 'all') {
      where.week = { contains: week, mode: 'insensitive' }
    }

    if (status && status !== 'all') {
      where.status = status
    }

    if (priority && priority !== 'all') {
      where.priority = priority
    }

    if (search) {
      where.OR = [
        { taskName: { contains: search, mode: 'insensitive' } },
        { phaseRepos: { contains: search, mode: 'insensitive' } },
        { dsaTrack: { contains: search, mode: 'insensitive' } },
        { morningSession: { contains: search, mode: 'insensitive' } },
        { eveningSession: { contains: search, mode: 'insensitive' } },
        { notes: { contains: search, mode: 'insensitive' } },
      ]
    }

    const tasks = await prisma.task.findMany({
      where,
      orderBy: {
        date: 'asc',
      },
    })

    return NextResponse.json({ success: true, count: tasks.length, tasks })
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
    const {
      taskName,
      date,
      sprint,
      week,
      phaseRepos,
      dsaTrack,
      morningSession,
      eveningSession,
      status = 'To Do',
      priority = 'Medium',
      notes = '',
    } = body

    if (!taskName || !date) {
      return NextResponse.json(
        { success: false, error: 'taskName and date are required' },
        { status: 400 }
      )
    }

    const newTask = await prisma.task.create({
      data: {
        taskName,
        date,
        sprint: sprint || 'Custom Sprint',
        week: week || 'Custom Week',
        phaseRepos: phaseRepos || '',
        dsaTrack: dsaTrack || '',
        morningSession: morningSession || '',
        eveningSession: eveningSession || '',
        status,
        priority,
        notes,
      },
    })

    return NextResponse.json({ success: true, task: newTask }, { status: 201 })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error creating task:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to create task' },
      { status: 500 }
    )
  }
}
