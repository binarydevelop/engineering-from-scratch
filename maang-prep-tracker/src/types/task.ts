export interface Task {
  id: string
  taskName: string
  date: string
  sprint: string
  week: string
  phaseRepos: string
  dsaTrack: string
  morningSession: string
  eveningSession: string
  status: 'To Do' | 'In Progress' | 'Done' | string
  priority: 'Critical' | 'High' | 'Medium' | 'Low' | string
  notes: string
  createdAt?: string
  updatedAt?: string
}

export interface SprintStat {
  name: string
  total: number
  done: number
  inProgress: number
  todo: number
  percentage: number
}

export interface TaskStats {
  total: number
  done: number
  inProgress: number
  todo: number
  completionPercentage: number
  priorityCounts: {
    Critical: number
    High: number
    Medium: number
    Low: number
  }
  sprints: SprintStat[]
  nextUpcoming: Task | null
}
