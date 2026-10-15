'use client'

import React from 'react'
import { Task } from '@/types/task'
import {
  CheckCircle2,
  Circle,
  Code2,
  Edit2,
  Trash2,
  FileText,
} from 'lucide-react'

interface TaskListViewProps {
  tasks: Task[]
  onSelectTask: (task: Task) => void
  onUpdateStatus: (taskId: string, newStatus: string) => void
  onDeleteTask: (task: Task) => void
}

export const TaskListView: React.FC<TaskListViewProps> = ({
  tasks,
  onSelectTask,
  onUpdateStatus,
  onDeleteTask,
}) => {
  if (tasks.length === 0) {
    return (
      <div className="rounded-2xl bg-zinc-900/40 border border-zinc-800 p-12 text-center">
        <p className="text-zinc-400 text-sm">No tasks found matching your filter criteria.</p>
      </div>
    )
  }

  // Group tasks by week
  const groupedWeeks: Record<string, Task[]> = {}
  for (const task of tasks) {
    const weekKey = task.week || 'Other'
    if (!groupedWeeks[weekKey]) {
      groupedWeeks[weekKey] = []
    }
    groupedWeeks[weekKey].push(task)
  }

  return (
    <div className="space-y-6">
      {Object.entries(groupedWeeks).map(([weekTitle, weekTasks]) => {
        const weekDone = weekTasks.filter((t) => t.status === 'Done').length
        const weekTotal = weekTasks.length
        const weekPct = Math.round((weekDone / weekTotal) * 100)

        return (
          <div
            key={weekTitle}
            className="rounded-2xl bg-zinc-900/40 border border-zinc-800/80 overflow-hidden shadow-sm"
          >
            {/* Week Header */}
            <div className="bg-zinc-900/90 border-b border-zinc-800/80 px-4 py-3 flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                <h3 className="text-xs sm:text-sm font-bold text-white tracking-wide">
                  {weekTitle}
                </h3>
              </div>
              <div className="flex items-center gap-3 text-xs">
                <span className="text-zinc-400">
                  {weekDone}/{weekTotal} Completed ({weekPct}%)
                </span>
                <div className="w-20 bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                  <div
                    className="bg-emerald-400 h-full rounded-full transition-all"
                    style={{ width: `${weekPct}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Week Tasks List */}
            <div className="divide-y divide-zinc-800/60">
              {weekTasks.map((task) => {
                const isDone = task.status === 'Done'
                const isInProgress = task.status === 'In Progress'

                return (
                  <div
                    key={task.id}
                    className={`p-4 transition flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-zinc-800/30 ${
                      isDone ? 'opacity-80 bg-zinc-950/20' : ''
                    }`}
                  >
                    {/* Left side: Date, Status toggle, Name & Details */}
                    <div className="flex items-start gap-3.5 flex-1 min-w-0">
                      {/* Status toggle button */}
                      <button
                        onClick={() =>
                          onUpdateStatus(
                            task.id,
                            isDone ? 'To Do' : isInProgress ? 'Done' : 'In Progress'
                          )
                        }
                        className="mt-0.5 flex-shrink-0 transition transform hover:scale-110"
                        title={`Current: ${task.status}. Click to change.`}
                      >
                        {isDone ? (
                          <CheckCircle2 className="w-5 h-5 text-emerald-400 fill-emerald-500/20" />
                        ) : isInProgress ? (
                          <div className="w-5 h-5 rounded-full border-2 border-amber-400 border-t-transparent animate-spin" />
                        ) : (
                          <Circle className="w-5 h-5 text-zinc-600 hover:text-blue-400" />
                        )}
                      </button>

                      {/* Content block */}
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-wrap items-center gap-2 mb-1">
                          <span className="text-xs font-mono font-semibold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                            {task.date}
                          </span>

                          {task.priority === 'Critical' && (
                            <span className="text-[11px] font-semibold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                              Critical
                            </span>
                          )}

                          {task.priority === 'High' && (
                            <span className="text-[11px] font-semibold text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded border border-orange-500/20">
                              High Priority
                            </span>
                          )}

                          <span
                            className={`text-[11px] font-medium px-2 py-0.5 rounded ${
                              isDone
                                ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20'
                                : isInProgress
                                ? 'bg-amber-500/10 text-amber-300 border border-amber-500/20'
                                : 'bg-zinc-800 text-zinc-400'
                            }`}
                          >
                            {task.status}
                          </span>
                        </div>

                        {/* Title */}
                        <h4
                          onClick={() => onSelectTask(task)}
                          className={`text-sm font-semibold cursor-pointer hover:text-blue-400 transition ${
                            isDone ? 'line-through text-zinc-400' : 'text-zinc-100'
                          }`}
                        >
                          {task.taskName}
                        </h4>

                        {/* Sessions Breakdown Preview */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2 text-xs text-zinc-400">
                          {task.morningSession && (
                            <div className="bg-zinc-950/40 p-2 rounded-lg border border-zinc-800/50">
                              <span className="text-blue-400 font-semibold block text-[11px]">
                                🌅 6:00 - 10:00 AM
                              </span>
                              <p className="line-clamp-2 text-zinc-300 text-[11px] mt-0.5">
                                {task.morningSession}
                              </p>
                            </div>
                          )}

                          {task.eveningSession && (
                            <div className="bg-zinc-950/40 p-2 rounded-lg border border-zinc-800/50">
                              <span className="text-indigo-400 font-semibold block text-[11px]">
                                🌙 7:00 - 10:00 PM
                              </span>
                              <p className="line-clamp-2 text-zinc-300 text-[11px] mt-0.5">
                                {task.eveningSession}
                              </p>
                            </div>
                          )}
                        </div>

                        {/* Striver DSA chip */}
                        {task.dsaTrack && (
                          <div className="mt-2 flex items-center gap-1.5 text-xs text-amber-300/90">
                            <Code2 className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
                            <span className="font-mono text-[11px] line-clamp-1">
                              {task.dsaTrack}
                            </span>
                          </div>
                        )}

                        {/* Notes preview if any */}
                        {task.notes && (
                          <div className="mt-2 flex items-center gap-1.5 text-xs text-zinc-400 italic bg-zinc-950/60 px-2 py-1 rounded">
                            <FileText className="w-3.5 h-3.5 text-zinc-400" />
                            <span className="line-clamp-1">{task.notes}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Right side: Action buttons */}
                    <div className="flex md:flex-col items-center justify-end gap-1.5 pt-2 md:pt-0 border-t md:border-t-0 border-zinc-800/40">
                      <button
                        onClick={() => onSelectTask(task)}
                        className="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white bg-zinc-800/70 hover:bg-zinc-700/80 transition flex items-center gap-1.5"
                      >
                        <Edit2 className="w-3 h-3 text-zinc-400" />
                        <span>Edit / Notes</span>
                      </button>

                      <button
                        onClick={() => onDeleteTask(task)}
                        className="px-2 py-1.5 rounded-lg text-xs text-zinc-500 hover:text-rose-400 hover:bg-rose-500/10 transition"
                        title="Delete task"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )
      })}
    </div>
  )
}
