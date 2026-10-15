'use client'

import React from 'react'
import { Plus, RotateCcw, CheckCircle2, Calendar, BookOpen } from 'lucide-react'

interface NavbarProps {
  activeTab: 'tracker' | 'notes'
  onTabChange: (tab: 'tracker' | 'notes') => void
  onOpenCreateModal: () => void
  onReseed: () => void
  isReseeding: boolean
  totalDone: number
  totalTasks: number
  hasDb?: boolean
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  onTabChange,
  onOpenCreateModal,
  onReseed,
  isReseeding,
  totalDone,
  totalTasks,
  hasDb = false,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-zinc-800/80 bg-[#0a0b12]/85 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand & Tabs */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 via-orange-500 to-rose-500 flex items-center justify-center font-bold text-white shadow-lg shadow-orange-500/20">
                ⚡
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-base sm:text-lg font-bold text-white tracking-tight">MAANG Staff Tracker</h1>
                  {hasDb ? (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                      PostgreSQL
                    </span>
                  ) : (
                    <span
                      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20"
                      title="Add DATABASE_URL in Vercel to enable cloud database"
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                      In-Memory Mode
                    </span>
                  )}
                </div>
                <p className="text-[11px] text-zinc-400 hidden sm:block">
                  Target: May 2027 · SDE-2 → Staff Target
                </p>
              </div>
            </div>

            {/* Navigation Tabs */}
            <div className="hidden md:flex items-center p-1 bg-zinc-950 rounded-xl border border-zinc-800">
              <button
                onClick={() => onTabChange('tracker')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                  activeTab === 'tracker'
                    ? 'bg-zinc-800 text-white shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <Calendar className="w-3.5 h-3.5 text-blue-400" />
                <span>Schedule Tracker</span>
              </button>

              <button
                onClick={() => onTabChange('notes')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                  activeTab === 'notes'
                    ? 'bg-zinc-800 text-white shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <BookOpen className="w-3.5 h-3.5 text-purple-400" />
                <span>Repo Notes & Docs GUI</span>
              </button>
            </div>
          </div>

          {/* Quick Stats & Actions */}
          <div className="flex items-center gap-2 sm:gap-3">
            {activeTab === 'tracker' && (
              <>
                <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>
                    <strong className="text-white">{totalDone}</strong> / {totalTasks} Completed
                  </span>
                </div>

                <button
                  onClick={onReseed}
                  disabled={isReseeding}
                  title="Reset database to original 191 schedule tasks"
                  className="px-2.5 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white bg-zinc-900/80 hover:bg-zinc-800 border border-zinc-800 transition flex items-center gap-1.5 disabled:opacity-50"
                >
                  <RotateCcw className={`w-3.5 h-3.5 ${isReseeding ? 'animate-spin' : ''}`} />
                  <span className="hidden sm:inline">Reset</span>
                </button>

                <button
                  onClick={onOpenCreateModal}
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-md shadow-blue-500/20 border border-blue-500/30 transition flex items-center gap-1.5"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Task</span>
                </button>
              </>
            )}

            {/* Mobile Tab Toggle */}
            <div className="flex md:hidden items-center p-0.5 bg-zinc-950 rounded-lg border border-zinc-800 text-xs">
              <button
                onClick={() => onTabChange('tracker')}
                className={`p-1.5 rounded ${activeTab === 'tracker' ? 'bg-zinc-800 text-white' : 'text-zinc-400'}`}
                title="Schedule Tracker"
              >
                <Calendar className="w-4 h-4" />
              </button>
              <button
                onClick={() => onTabChange('notes')}
                className={`p-1.5 rounded ${activeTab === 'notes' ? 'bg-zinc-800 text-white' : 'text-zinc-400'}`}
                title="Repo Notes & Docs"
              >
                <BookOpen className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
