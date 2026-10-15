'use client'

import React from 'react'
import { Task } from '@/types/task'

interface TaskGridViewProps {
  tasks: Task[]
  onSelectTask: (task: Task) => void
}

export const TaskGridView: React.FC<TaskGridViewProps> = ({ tasks, onSelectTask }) => {
  return (
    <div className="bg-zinc-900/40 rounded-2xl border border-zinc-800/80 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-bold text-white text-base">Full Roadmap Matrix (191 Days)</h3>
          <p className="text-xs text-zinc-400">Click any block to view or edit the day&apos;s study plan</p>
        </div>
        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-emerald-500"></span>
            <span className="text-zinc-300">Done</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-amber-500"></span>
            <span className="text-zinc-300">In Progress</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-zinc-800 border border-zinc-700"></span>
            <span className="text-zinc-400">To Do</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2.5">
        {tasks.map((task, idx) => {
          const isDone = task.status === 'Done'
          const isInProgress = task.status === 'In Progress'

          return (
            <div
              key={task.id}
              onClick={() => onSelectTask(task)}
              className={`p-2.5 rounded-xl border text-xs cursor-pointer transition flex flex-col justify-between h-24 hover:scale-[1.02] ${
                isDone
                  ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-200'
                  : isInProgress
                  ? 'bg-amber-950/30 border-amber-500/40 text-amber-200'
                  : 'bg-zinc-950/60 border-zinc-800 text-zinc-300 hover:border-zinc-700'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono text-zinc-400">D{idx + 1}</span>
                <span className="text-[10px] font-mono font-semibold">{task.date.slice(5)}</span>
              </div>

              <p className="line-clamp-2 text-[11px] font-medium leading-tight my-1">
                {task.taskName}
              </p>

              <div className="flex items-center justify-between text-[10px]">
                <span className="text-zinc-500 truncate max-w-[80px]">
                  {task.priority === 'Critical' ? '🔴 Critical' : task.priority}
                </span>
                <span
                  className={`px-1.5 py-0.2 rounded ${
                    isDone
                      ? 'bg-emerald-500/20 text-emerald-300'
                      : isInProgress
                      ? 'bg-amber-500/20 text-amber-300'
                      : 'bg-zinc-800 text-zinc-400'
                  }`}
                >
                  {task.status}
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
