'use client'

import React from 'react'
import { TaskStats, Task } from '@/types/task'
import {
  Trophy,
  Flame,
  Clock,
  ArrowRight,
  CheckCircle,
  PlayCircle,
} from 'lucide-react'

interface StatsOverviewProps {
  stats: TaskStats | null
  onQuickUpdateStatus: (taskId: string, newStatus: string) => void
  onSelectTask: (task: Task) => void
}

export const StatsOverview: React.FC<StatsOverviewProps> = ({
  stats,
  onQuickUpdateStatus,
  onSelectTask,
}) => {
  if (!stats) return null

  const {
    done,
    inProgress,
    todo,
    completionPercentage,
    nextUpcoming,
  } = stats

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Card 1: Overall Progress */}
      <div className="rounded-2xl bg-zinc-900/60 border border-zinc-800 p-5 shadow-lg relative overflow-hidden flex flex-col justify-between">
        <div className="absolute -top-12 -right-12 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl pointer-events-none" />
        <div>
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400 flex items-center gap-1.5">
              <Trophy className="w-4 h-4 text-amber-400" />
              Overall Completion
            </span>
            <span className="text-2xl font-black text-white">{completionPercentage}%</span>
          </div>

          <div className="w-full bg-zinc-800 h-2.5 rounded-full overflow-hidden mb-4">
            <div
              className="bg-gradient-to-r from-blue-500 via-indigo-500 to-emerald-400 h-full rounded-full transition-all duration-700 ease-out"
              style={{ width: `${completionPercentage}%` }}
            />
          </div>

          <div className="grid grid-cols-3 gap-2 text-center pt-2 border-t border-zinc-800/60">
            <div className="p-2 rounded-lg bg-zinc-950/40">
              <span className="text-xs text-emerald-400 font-semibold block">{done}</span>
              <span className="text-[11px] text-zinc-500">Done</span>
            </div>
            <div className="p-2 rounded-lg bg-zinc-950/40">
              <span className="text-xs text-amber-400 font-semibold block">{inProgress}</span>
              <span className="text-[11px] text-zinc-500">In Progress</span>
            </div>
            <div className="p-2 rounded-lg bg-zinc-950/40">
              <span className="text-xs text-zinc-400 font-semibold block">{todo}</span>
              <span className="text-[11px] text-zinc-500">To Do</span>
            </div>
          </div>
        </div>
      </div>

      {/* Card 2: Next Focus / Up Next */}
      <div className="rounded-2xl bg-zinc-900/60 border border-zinc-800 p-5 shadow-lg relative overflow-hidden flex flex-col justify-between">
        <div className="absolute -top-12 -right-12 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl pointer-events-none" />
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
              <Flame className="w-4 h-4 text-emerald-400" />
              Next Scheduled Session
            </span>
            {nextUpcoming && (
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-300">
                {nextUpcoming.date}
              </span>
            )}
          </div>

          {nextUpcoming ? (
            <div className="mt-1">
              <h4
                onClick={() => onSelectTask(nextUpcoming)}
                className="text-sm font-semibold text-white hover:text-blue-400 cursor-pointer line-clamp-1 transition"
                title={nextUpcoming.taskName}
              >
                {nextUpcoming.taskName}
              </h4>
              <p className="text-xs text-zinc-400 mt-1 line-clamp-2">
                {nextUpcoming.phaseRepos || nextUpcoming.dsaTrack}
              </p>
              <div className="mt-3 flex items-center gap-2">
                {nextUpcoming.status !== 'In Progress' ? (
                  <button
                    onClick={() => onQuickUpdateStatus(nextUpcoming.id, 'In Progress')}
                    className="px-3 py-1 rounded-md text-xs font-medium text-amber-300 bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 transition flex items-center gap-1"
                  >
                    <PlayCircle className="w-3.5 h-3.5" />
                    Start Session
                  </button>
                ) : (
                  <button
                    onClick={() => onQuickUpdateStatus(nextUpcoming.id, 'Done')}
                    className="px-3 py-1 rounded-md text-xs font-medium text-emerald-300 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 transition flex items-center gap-1"
                  >
                    <CheckCircle className="w-3.5 h-3.5" />
                    Mark Completed
                  </button>
                )}
                <button
                  onClick={() => onSelectTask(nextUpcoming)}
                  className="px-2.5 py-1 rounded-md text-xs text-zinc-400 hover:text-white bg-zinc-800/80 hover:bg-zinc-800 transition flex items-center gap-1"
                >
                  View Plan <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          ) : (
            <div className="py-4 text-center text-xs text-zinc-500">
              🎉 All scheduled sessions completed!
            </div>
          )}
        </div>
      </div>

      {/* Card 3: Study Architecture & Hours */}
      <div className="rounded-2xl bg-zinc-900/60 border border-zinc-800 p-5 shadow-lg relative overflow-hidden flex flex-col justify-between">
        <div className="absolute -top-12 -right-12 w-32 h-32 bg-purple-500/10 rounded-full blur-2xl pointer-events-none" />
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-purple-400 flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-purple-400" />
              Daily Study Architecture
            </span>
            <span className="text-xs text-zinc-400">Total: 191 Days</span>
          </div>

          <div className="space-y-2 mt-2">
            <div className="flex items-center justify-between p-2 rounded-lg bg-zinc-950/40 text-xs">
              <span className="text-zinc-300 font-medium flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span> Weekdays (Mon-Fri)
              </span>
              <span className="font-mono font-semibold text-white">7 hrs / day</span>
            </div>
            <div className="flex items-center justify-between p-2 rounded-lg bg-zinc-950/40 text-xs">
              <span className="text-zinc-300 font-medium flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-amber-400"></span> Weekends (Sat-Sun)
              </span>
              <span className="font-mono font-semibold text-white">~10 hrs / day</span>
            </div>
          </div>

          <div className="mt-3 pt-2 border-t border-zinc-800/60 flex items-center justify-between text-[11px] text-zinc-400">
            <span>Striver A2Z DSA: 455+ Problems</span>
            <span>SystemOverflow SD</span>
          </div>
        </div>
      </div>
    </div>
  )
}
