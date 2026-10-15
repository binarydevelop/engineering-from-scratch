import { NextResponse } from 'next/server'
import prisma from '@/lib/prisma'
import initialTasks from '@/data/initial-tasks.json'

export async function GET() {
  try {
    let totalCount = await prisma.task.count()
    if (totalCount === 0) {
      await prisma.task.createMany({
        data: initialTasks,
      })
      totalCount = await prisma.task.count()
    }

    const [todoCount, inProgressCount, doneCount] = await Promise.all([
      prisma.task.count({ where: { status: 'To Do' } }),
      prisma.task.count({ where: { status: 'In Progress' } }),
      prisma.task.count({ where: { status: 'Done' } }),
    ])

    const allTasks = await prisma.task.findMany({
      select: {
        id: true,
        taskName: true,
        date: true,
        sprint: true,
        week: true,
        phaseRepos: true,
        dsaTrack: true,
        status: true,
        priority: true,
      },
      orderBy: {
        date: 'asc',
      },
    })

    // Sprints breakdown
    const sprintMap: Record<string, { total: number; done: number; inProgress: number; todo: number }> = {}
    for (const t of allTasks) {
      if (!sprintMap[t.sprint]) {
        sprintMap[t.sprint] = { total: 0, done: 0, inProgress: 0, todo: 0 }
      }
      sprintMap[t.sprint].total++
      if (t.status === 'Done') sprintMap[t.sprint].done++
      else if (t.status === 'In Progress') sprintMap[t.sprint].inProgress++
      else sprintMap[t.sprint].todo++
    }

    const sprints = Object.entries(sprintMap).map(([name, counts]) => ({
      name,
      ...counts,
      percentage: counts.total > 0 ? Math.round((counts.done / counts.total) * 100) : 0,
    }))

    // Priority breakdown
    const priorityCounts = {
      Critical: allTasks.filter((t) => t.priority === 'Critical').length,
      High: allTasks.filter((t) => t.priority === 'High').length,
      Medium: allTasks.filter((t) => t.priority === 'Medium').length,
      Low: allTasks.filter((t) => t.priority === 'Low').length,
    }

    // Find next upcoming task (first task that is not Done)
    const nextUpcoming = allTasks.find((t) => t.status !== 'Done') || null

    const completionPercentage = totalCount > 0 ? Math.round((doneCount / totalCount) * 100) : 0

    return NextResponse.json({
      success: true,
      stats: {
        total: totalCount,
        done: doneCount,
        inProgress: inProgressCount,
        todo: todoCount,
        completionPercentage,
        priorityCounts,
        sprints,
        nextUpcoming,
      },
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
