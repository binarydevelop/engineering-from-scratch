'use client'

import React, { useState } from 'react'
import { Task } from '@/types/task'
import { X, Plus } from 'lucide-react'

interface CreateTaskModalProps {
  isOpen: boolean
  onClose: () => void
  onCreate: (task: Omit<Task, 'id'>) => Promise<void>
}

export const CreateTaskModal: React.FC<CreateTaskModalProps> = ({
  isOpen,
  onClose,
  onCreate,
}) => {
  const [taskName, setTaskName] = useState('')
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10))
  const [sprint, setSprint] = useState('🔶 Sprint 1 — Foundations Blitz')
  const [week, setWeek] = useState('Custom Week')
  const [phaseRepos, setPhaseRepos] = useState('')
  const [dsaTrack, setDsaTrack] = useState('')
  const [morningSession, setMorningSession] = useState('')
  const [eveningSession, setEveningSession] = useState('')
  const [priority, setPriority] = useState('High')
  const [status, setStatus] = useState('To Do')
  const [notes, setNotes] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!taskName.trim() || !date.trim()) return

    setIsSubmitting(true)
    try {
      await onCreate({
        taskName,
        date,
        sprint,
        week,
        phaseRepos,
        dsaTrack,
        morningSession,
        eveningSession,
        priority,
        status,
        notes,
      })
      // Reset form
      setTaskName('')
      setPhaseRepos('')
      setDsaTrack('')
      setMorningSession('')
      setEveningSession('')
      setNotes('')
      onClose()
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm overflow-y-auto">
      <div className="bg-[#0f1016] border border-zinc-800 rounded-2xl w-full max-w-xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl animate-in fade-in duration-200">
        <div className="p-4 sm:p-5 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/60">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <h3 className="text-sm font-bold text-white">Create New Prep Task / Session</h3>
          </div>
          <button
            onClick={onClose}
            className="text-zinc-400 hover:text-white p-1 rounded-lg hover:bg-zinc-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 sm:p-6 space-y-4 overflow-y-auto flex-1">
          <div>
            <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
              Task Title *
            </label>
            <input
              type="text"
              required
              value={taskName}
              onChange={(e) => setTaskName(e.target.value)}
              placeholder="e.g. Mock Interview with Senior Staff Mentor / Meta System Design drill"
              className="w-full px-3.5 py-2.5 bg-zinc-950 border border-zinc-800 rounded-xl text-sm font-semibold text-white placeholder-zinc-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
                Date *
              </label>
              <input
                type="date"
                required
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
                Sprint
              </label>
              <select
                value={sprint}
                onChange={(e) => setSprint(e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="🔶 Sprint 1 — Foundations Blitz">Sprint 1 — Foundations Blitz</option>
                <option value="🔶 Sprint 2 — Backend Engineering Core">Sprint 2 — Backend Engineering Core</option>
                <option value="🔶 Sprint 3 — LLD Mastery">Sprint 3 — LLD Mastery</option>
                <option value="🔶 Sprint 4 — System Design: Foundations">Sprint 4 — System Design: Foundations</option>
                <option value="🔶 Sprint 5 — SD Interview Mode + Infrastructure">Sprint 5 — SD Interview Mode</option>
                <option value="🔶 Sprint 6 — Advanced / Differentiation Track">Sprint 6 — Advanced / Differentiation</option>
                <option value="🔶 Sprint 7 — Staff Engineering + Behavioral">Sprint 7 — Staff Engineering + Behavioral</option>
                <option value="Custom Sprint">Custom Sprint</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
              Week Tag
            </label>
            <input
              type="text"
              value={week}
              onChange={(e) => setWeek(e.target.value)}
              placeholder="e.g. Week 1 — Oct 17–23 | OS + Linux + Striver Steps 1–2"
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
                Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
                Initial Status
              </label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="To Do">To Do</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-amber-400 uppercase tracking-wider mb-1.5">
              DSA Topic (Striver A2Z)
            </label>
            <input
              type="text"
              value={dsaTrack}
              onChange={(e) => setDsaTrack(e.target.value)}
              placeholder="e.g. Striver Step 7: Recursion / Backtracking - N-Queens, Word Search"
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1.5">
              Phase / Repos Focus
            </label>
            <input
              type="text"
              value={phaseRepos}
              onChange={(e) => setPhaseRepos(e.target.value)}
              placeholder="e.g. `kafka` 30-45 (consumer groups, rebalance, offsets)"
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-blue-300 uppercase tracking-wider mb-1.5">
                🌅 Morning Session (6-10 AM)
              </label>
              <textarea
                rows={2}
                value={morningSession}
                onChange={(e) => setMorningSession(e.target.value)}
                placeholder="Morning block goals..."
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-300 focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-1.5">
                🌙 Evening Session (7-10 PM)
              </label>
              <textarea
                rows={2}
                value={eveningSession}
                onChange={(e) => setEveningSession(e.target.value)}
                placeholder="Evening block goals..."
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-300 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div className="pt-4 border-t border-zinc-800 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-medium text-zinc-400 hover:text-white bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 transition shadow-md shadow-emerald-500/20 flex items-center gap-1.5 disabled:opacity-50"
            >
              <Plus className="w-4 h-4" />
              <span>{isSubmitting ? 'Creating...' : 'Create Task'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
