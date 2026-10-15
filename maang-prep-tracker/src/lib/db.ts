import prisma, { getResolvedDatabaseUrl } from './prisma'
import { Prisma } from '@prisma/client'
import initialTasks from '@/data/initial-tasks.json'
import { Task, TaskStats } from '@/types/task'

export function isDbAvailable(): boolean {
  return Boolean(getResolvedDatabaseUrl())
}

let isTableInitialized = false

async function ensureTableExists() {
  if (isTableInitialized) return
  try {
    await prisma.$executeRawUnsafe(`
      CREATE TABLE IF NOT EXISTS "Task" (
        "id" TEXT NOT NULL PRIMARY KEY,
        "taskName" TEXT NOT NULL,
        "date" TEXT NOT NULL,
        "sprint" TEXT NOT NULL,
        "week" TEXT NOT NULL,
        "phaseRepos" TEXT NOT NULL,
        "dsaTrack" TEXT NOT NULL,
        "morningSession" TEXT NOT NULL,
        "eveningSession" TEXT NOT NULL,
        "status" TEXT NOT NULL DEFAULT 'To Do',
        "priority" TEXT NOT NULL DEFAULT 'Medium',
        "notes" TEXT NOT NULL DEFAULT '',
        "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE INDEX IF NOT EXISTS "Task_date_idx" ON "Task"("date");
      CREATE INDEX IF NOT EXISTS "Task_sprint_idx" ON "Task"("sprint");
      CREATE INDEX IF NOT EXISTS "Task_status_idx" ON "Task"("status");
    `)
    isTableInitialized = true
  } catch (err) {
    console.warn('Could not run auto-table create (will attempt query directly):', err)
  }
}

// In-memory store fallback when DATABASE_URL is not set or DB unreachable
interface MemoryTask extends Task {
  id: string
}

let inMemoryTasks: MemoryTask[] = initialTasks.map((t, idx) => ({
  ...t,
  id: `task-${idx + 1}`,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
}))

export async function fetchAllTasks(params?: {
  search?: string
  sprint?: string
  week?: string
  status?: string
  priority?: string
}): Promise<{ tasks: Task[]; hasDb: boolean }> {
  const { search = '', sprint = '', week = '', status = '', priority = '' } = params || {}

  if (isDbAvailable()) {
    try {
      await ensureTableExists()
      // Auto seed if empty
      const count = await prisma.task.count()
      if (count === 0) {
        await prisma.task.createMany({ data: initialTasks })
      }

      const where: Prisma.TaskWhereInput = {}
      if (sprint && sprint !== 'all') where.sprint = { contains: sprint, mode: 'insensitive' }
      if (week && week !== 'all') where.week = { contains: week, mode: 'insensitive' }
      if (status && status !== 'all') where.status = status
      if (priority && priority !== 'all') where.priority = priority
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
        orderBy: { date: 'asc' },
      })

      return { tasks, hasDb: true }
    } catch (e) {
      console.warn('Database query failed, using in-memory fallback:', e)
    }
  }

  // Fallback to in-memory tasks
  let filtered = [...inMemoryTasks]

  if (sprint && sprint !== 'all') {
    filtered = filtered.filter((t) => t.sprint.toLowerCase().includes(sprint.toLowerCase()))
  }
  if (week && week !== 'all') {
    filtered = filtered.filter((t) => t.week.toLowerCase().includes(week.toLowerCase()))
  }
  if (status && status !== 'all') {
    filtered = filtered.filter((t) => t.status === status)
  }
  if (priority && priority !== 'all') {
    filtered = filtered.filter((t) => t.priority === priority)
  }
  if (search) {
    const s = search.toLowerCase()
    filtered = filtered.filter(
      (t) =>
        t.taskName.toLowerCase().includes(s) ||
        t.phaseRepos.toLowerCase().includes(s) ||
        t.dsaTrack.toLowerCase().includes(s) ||
        t.morningSession.toLowerCase().includes(s) ||
        t.eveningSession.toLowerCase().includes(s) ||
        t.notes.toLowerCase().includes(s)
    )
  }

  filtered.sort((a, b) => a.date.localeCompare(b.date))
  return { tasks: filtered, hasDb: false }
}

export async function updateTask(id: string, updates: Partial<Task>): Promise<{ task: Task; hasDb: boolean }> {
  if (isDbAvailable()) {
    try {
      await ensureTableExists()
      const task = await prisma.task.update({
        where: { id },
        data: updates,
      })
      return { task, hasDb: true }
    } catch (e) {
      console.warn('Database update failed, updating in-memory:', e)
    }
  }

  const idx = inMemoryTasks.findIndex((t) => t.id === id)
  if (idx !== -1) {
    inMemoryTasks[idx] = {
      ...inMemoryTasks[idx],
      ...updates,
      updatedAt: new Date().toISOString(),
    }
    return { task: inMemoryTasks[idx], hasDb: false }
  }

  throw new Error(`Task with id ${id} not found`)
}

export async function createTask(data: Omit<Task, 'id'>): Promise<{ task: Task; hasDb: boolean }> {
  if (isDbAvailable()) {
    try {
      await ensureTableExists()
      const task = await prisma.task.create({
        data: {
          taskName: data.taskName,
          date: data.date,
          sprint: data.sprint || 'Custom Sprint',
          week: data.week || 'Custom Week',
          phaseRepos: data.phaseRepos || '',
          dsaTrack: data.dsaTrack || '',
          morningSession: data.morningSession || '',
          eveningSession: data.eveningSession || '',
          status: data.status || 'To Do',
          priority: data.priority || 'High',
          notes: data.notes || '',
        },
      })
      return { task, hasDb: true }
    } catch (e) {
      console.warn('Database create failed, creating in-memory:', e)
    }
  }

  const newTask: MemoryTask = {
    ...data,
    id: `custom-${Date.now()}`,
    status: data.status || 'To Do',
    priority: data.priority || 'High',
    notes: data.notes || '',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  }

  inMemoryTasks.push(newTask)
  return { task: newTask, hasDb: false }
}

export async function deleteTask(id: string): Promise<{ success: boolean; hasDb: boolean }> {
  if (isDbAvailable()) {
    try {
      await ensureTableExists()
      await prisma.task.delete({ where: { id } })
      return { success: true, hasDb: true }
    } catch (e) {
      console.warn('Database delete failed, deleting in-memory:', e)
    }
  }

  inMemoryTasks = inMemoryTasks.filter((t) => t.id !== id)
  return { success: true, hasDb: false }
}

export async function reseedAllTasks(): Promise<{ count: number; hasDb: boolean }> {
  if (isDbAvailable()) {
    try {
      await ensureTableExists()
      await prisma.task.deleteMany({})
      const created = await prisma.task.createMany({ data: initialTasks })
      return { count: created.count, hasDb: true }
    } catch (e) {
      console.warn('Database reseed failed, reseeding in-memory:', e)
    }
  }

  inMemoryTasks = initialTasks.map((t, idx) => ({
    ...t,
    id: `task-${idx + 1}`,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  }))

  return { count: inMemoryTasks.length, hasDb: false }
}

export async function fetchTaskStats(): Promise<{ stats: TaskStats; hasDb: boolean }> {
  const { tasks, hasDb } = await fetchAllTasks()

  const total = tasks.length
  const done = tasks.filter((t) => t.status === 'Done').length
  const inProgress = tasks.filter((t) => t.status === 'In Progress').length
  const todo = tasks.filter((t) => t.status === 'To Do').length
  const completionPercentage = total > 0 ? Math.round((done / total) * 100) : 0

  const priorityCounts = {
    Critical: tasks.filter((t) => t.priority === 'Critical').length,
    High: tasks.filter((t) => t.priority === 'High').length,
    Medium: tasks.filter((t) => t.priority === 'Medium').length,
    Low: tasks.filter((t) => t.priority === 'Low').length,
  }

  const sprintMap: Record<string, { total: number; done: number; inProgress: number; todo: number }> = {}
  for (const t of tasks) {
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

  const nextUpcoming = tasks.find((t) => t.status !== 'Done') || null

  return {
    hasDb,
    stats: {
      total,
      done,
      inProgress,
      todo,
      completionPercentage,
      priorityCounts,
      sprints,
      nextUpcoming,
    },
  }
}
