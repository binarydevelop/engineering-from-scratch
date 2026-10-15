'use client'

import React from 'react'
import {
  Search,
  List,
  Kanban,
  Calendar,
  X,
  Layers,
} from 'lucide-react'

interface TaskFilterBarProps {
  searchQuery: string
  onSearchChange: (query: string) => void
  selectedSprint: string
  onSprintChange: (sprint: string) => void
  selectedStatus: string
  onStatusChange: (status: string) => void
  selectedPriority: string
  onPriorityChange: (priority: string) => void
  activeView: 'list' | 'kanban' | 'calendar'
  onViewChange: (view: 'list' | 'kanban' | 'calendar') => void
  sprintsList: string[]
  totalFiltered: number
}

export const TaskFilterBar: React.FC<TaskFilterBarProps> = ({
  searchQuery,
  onSearchChange,
  selectedSprint,
  onSprintChange,
  selectedStatus,
  onStatusChange,
  selectedPriority,
  onPriorityChange,
  activeView,
  onViewChange,
  sprintsList,
  totalFiltered,
}) => {
  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-4 mb-6 shadow-md space-y-3">
      {/* Top row: Search & View Switcher */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        {/* Search */}
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search tasks, DSA topics, repos, notes..."
            className="w-full pl-9 pr-8 py-2 bg-zinc-950/70 border border-zinc-800 rounded-xl text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
          />
          {searchQuery && (
            <button
              onClick={() => onSearchChange('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* View Switcher & Result Count */}
        <div className="flex items-center justify-between sm:justify-end w-full sm:w-auto gap-3">
          <span className="text-xs text-zinc-400 font-medium">
            Showing <strong className="text-zinc-200">{totalFiltered}</strong> tasks
          </span>

          <div className="flex items-center p-1 bg-zinc-950 rounded-xl border border-zinc-800">
            <button
              onClick={() => onViewChange('list')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
                activeView === 'list'
                  ? 'bg-zinc-800 text-white shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <List className="w-3.5 h-3.5" />
              <span>Timeline</span>
            </button>

            <button
              onClick={() => onViewChange('kanban')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
                activeView === 'kanban'
                  ? 'bg-zinc-800 text-white shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <Kanban className="w-3.5 h-3.5" />
              <span>Kanban</span>
            </button>

            <button
              onClick={() => onViewChange('calendar')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
                activeView === 'calendar'
                  ? 'bg-zinc-800 text-white shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <Calendar className="w-3.5 h-3.5" />
              <span>Overview</span>
            </button>
          </div>
        </div>
      </div>

      {/* Bottom row: Filters */}
      <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-zinc-800/60 text-xs">
        {/* Sprint selector */}
        <div className="flex items-center gap-1.5">
          <Layers className="w-3.5 h-3.5 text-zinc-400" />
          <select
            value={selectedSprint}
            onChange={(e) => onSprintChange(e.target.value)}
            className="bg-zinc-950/80 border border-zinc-800 text-zinc-300 py-1.5 px-2.5 rounded-lg text-xs focus:outline-none focus:border-blue-500"
          >
            <option value="all">All Sprints (1 to 7)</option>
            {sprintsList.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>

        {/* Status Pills */}
        <div className="flex items-center gap-1 ml-auto sm:ml-0">
          {(['all', 'To Do', 'In Progress', 'Done'] as const).map((status) => (
            <button
              key={status}
              onClick={() => onStatusChange(status)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition ${
                selectedStatus === status
                  ? status === 'Done'
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : status === 'In Progress'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    : status === 'To Do'
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    : 'bg-zinc-800 text-white border border-zinc-700'
                  : 'text-zinc-400 hover:text-zinc-200 bg-zinc-950/40 border border-transparent'
              }`}
            >
              {status === 'all' ? 'All Statuses' : status}
            </button>
          ))}
        </div>

        {/* Priority Filter */}
        <div className="flex items-center gap-1">
          {(['all', 'Critical', 'High', 'Medium'] as const).map((priority) => (
            <button
              key={priority}
              onClick={() => onPriorityChange(priority)}
              className={`px-2 py-1 rounded-md text-[11px] font-medium transition ${
                selectedPriority === priority
                  ? priority === 'Critical'
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                    : priority === 'High'
                    ? 'bg-orange-500/20 text-orange-300 border border-orange-500/30'
                    : 'bg-zinc-800 text-white border border-zinc-700'
                  : 'text-zinc-500 hover:text-zinc-300 bg-zinc-950/40 border border-transparent'
              }`}
            >
              {priority === 'all' ? 'All Priority' : priority}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
