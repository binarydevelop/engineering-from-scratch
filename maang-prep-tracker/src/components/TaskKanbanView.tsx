'use client'

import React from 'react'
import { Task } from '@/types/task'
import {
  ArrowRight,
  ArrowLeft,
  Code2,
  Calendar,
} from 'lucide-react'

interface TaskKanbanViewProps {
  tasks: Task[]
  onSelectTask: (task: Task) => void
  onUpdateStatus: (taskId: string, newStatus: string) => void
}

export const TaskKanbanView: React.FC<TaskKanbanViewProps> = ({
  tasks,
  onSelectTask,
  onUpdateStatus,
}) => {
  const columns: { id: string; title: string; color: string; dotColor: string }[] = [
    { id: 'To Do', title: 'To Do', color: 'border-blue-500/30', dotColor: 'bg-blue-400' },
    { id: 'In Progress', title: 'In Progress', color: 'border-amber-500/30', dotColor: 'bg-amber-400' },
    { id: 'Done', title: 'Completed', color: 'border-emerald-500/30', dotColor: 'bg-emerald-400' },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {columns.map((col) => {
        const colTasks = tasks.filter((t) => t.status === col.id)

        return (
          <div
            key={col.id}
            className="flex flex-col bg-zinc-900/40 rounded-2xl border border-zinc-800/80 overflow-hidden shadow-sm"
          >
            {/* Column Header */}
            <div className={`p-4 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/70`}>
              <div className="flex items-center gap-2">
                <span className={`w-2.5 h-2.5 rounded-full ${col.dotColor}`} />
                <h3 className="font-bold text-sm text-white">{col.title}</h3>
              </div>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-300">
                {colTasks.length}
              </span>
            </div>

            {/* Task Cards Column */}
            <div className="p-3 space-y-3 flex-1 overflow-y-auto max-h-[calc(100vh-280px)]">
              {colTasks.length === 0 ? (
                <div className="text-center py-12 text-zinc-500 text-xs italic">
                  No tasks in {col.title}
                </div>
              ) : (
                colTasks.map((task) => (
                  <div
                    key={task.id}
                    className="p-3.5 rounded-xl bg-zinc-950/80 border border-zinc-800/90 hover:border-zinc-700 transition shadow-sm group"
                  >
                    {/* Top Row: Date & Priority */}
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[11px] font-mono font-medium text-zinc-400 flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-blue-400" />
                        {task.date}
                      </span>
                      {task.priority === 'Critical' && (
                        <span className="text-[10px] font-bold text-rose-400 bg-rose-500/10 px-1.5 py-0.5 rounded">
                          Critical
                        </span>
                      )}
                      {task.priority === 'High' && (
                        <span className="text-[10px] font-semibold text-orange-400 bg-orange-500/10 px-1.5 py-0.5 rounded">
                          High
                        </span>
                      )}
                    </div>

                    {/* Task Title */}
                    <h4
                      onClick={() => onSelectTask(task)}
                      className="text-xs sm:text-sm font-semibold text-zinc-100 hover:text-blue-400 cursor-pointer transition line-clamp-2 mb-2"
                      title={task.taskName}
                    >
                      {task.taskName}
                    </h4>

                    {/* DSA Chip */}
                    {task.dsaTrack && (
                      <div className="text-[11px] text-amber-300/80 bg-zinc-900/90 px-2 py-1 rounded border border-zinc-800/60 mb-3 flex items-center gap-1 line-clamp-1">
                        <Code2 className="w-3 h-3 text-amber-400 flex-shrink-0" />
                        <span className="truncate">{task.dsaTrack}</span>
                      </div>
                    )}

                    {/* Bottom Action Bar */}
                    <div className="flex items-center justify-between pt-2 border-t border-zinc-800/60 text-xs">
                      {/* Left move button */}
                      {col.id === 'In Progress' && (
                        <button
                          onClick={() => onUpdateStatus(task.id, 'To Do')}
                          className="text-zinc-400 hover:text-white flex items-center gap-1 text-[11px] hover:bg-zinc-800 px-1.5 py-0.5 rounded"
                          title="Move to To Do"
                        >
                          <ArrowLeft className="w-3 h-3" /> To Do
                        </button>
                      )}
                      {col.id === 'Done' && (
                        <button
                          onClick={() => onUpdateStatus(task.id, 'In Progress')}
                          className="text-zinc-400 hover:text-white flex items-center gap-1 text-[11px] hover:bg-zinc-800 px-1.5 py-0.5 rounded"
                          title="Move to In Progress"
                        >
                          <ArrowLeft className="w-3 h-3" /> In Progress
                        </button>
                      )}
                      {col.id === 'To Do' && <div />}

                      {/* Right move button */}
                      {col.id === 'To Do' && (
                        <button
                          onClick={() => onUpdateStatus(task.id, 'In Progress')}
                          className="text-amber-400 hover:text-amber-300 flex items-center gap-1 text-[11px] hover:bg-amber-500/10 px-2 py-0.5 rounded font-medium ml-auto"
                        >
                          Start <ArrowRight className="w-3 h-3" />
                        </button>
                      )}
                      {col.id === 'In Progress' && (
                        <button
                          onClick={() => onUpdateStatus(task.id, 'Done')}
                          className="text-emerald-400 hover:text-emerald-300 flex items-center gap-1 text-[11px] hover:bg-emerald-500/10 px-2 py-0.5 rounded font-medium ml-auto"
                        >
                          Complete <ArrowRight className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
