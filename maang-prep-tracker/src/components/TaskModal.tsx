'use client'

import React, { useState, useEffect } from 'react'
import { Task } from '@/types/task'
import {
  X,
  Code2,
  Clock,
  BookOpen,
  FileText,
  Trash2,
  Save,
} from 'lucide-react'

interface TaskModalProps {
  task: Task | null
  isOpen: boolean
  onClose: () => void
  onSave: (updatedTask: Partial<Task> & { id: string }) => Promise<void>
  onDelete: (task: Task) => void
  onOpenNotes?: (repoId: string) => void
}

export const TaskModal: React.FC<TaskModalProps> = ({
  task,
  isOpen,
  onClose,
  onSave,
  onDelete,
  onOpenNotes,
}) => {
  const [formData, setFormData] = useState<Partial<Task>>({})
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    if (task) {
      setFormData({ ...task })
    }
  }, [task])

  if (!isOpen || !task) return null

  const handleInputChange = (field: keyof Task, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSaving(true)
    try {
      await onSave({
        ...formData,
        id: task.id,
      })
      onClose()
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm overflow-y-auto">
      <div className="bg-[#0f1016] border border-zinc-800 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl animate-in fade-in duration-200">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/60">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
            <span className="text-xs font-mono text-zinc-400">{formData.date}</span>
            <span className="text-zinc-600">·</span>
            <span className="text-xs text-zinc-300 font-medium truncate max-w-[200px]">
              {formData.sprint}
            </span>
          </div>

          <button
            onClick={onClose}
            className="text-zinc-400 hover:text-white p-1 rounded-lg hover:bg-zinc-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <form onSubmit={handleSubmit} className="p-4 sm:p-6 space-y-4 overflow-y-auto flex-1">
          {/* Title */}
          <div>
            <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
              Task Title
            </label>
            <input
              type="text"
              value={formData.taskName || ''}
              onChange={(e) => handleInputChange('taskName', e.target.value)}
              className="w-full px-3.5 py-2.5 bg-zinc-950 border border-zinc-800 rounded-xl text-sm font-semibold text-white focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* Status & Priority Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
                Status
              </label>
              <select
                value={formData.status || 'To Do'}
                onChange={(e) => handleInputChange('status', e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="To Do">To Do</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done (Completed)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5">
                Priority
              </label>
              <select
                value={formData.priority || 'Medium'}
                onChange={(e) => handleInputChange('priority', e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>
          </div>

          {/* DSA Track */}
          <div>
            <label className="block text-xs font-semibold text-amber-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <Code2 className="w-3.5 h-3.5" />
              DSA Track (Striver A2Z Sheet)
            </label>
            <input
              type="text"
              value={formData.dsaTrack || ''}
              onChange={(e) => handleInputChange('dsaTrack', e.target.value)}
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-200 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Phase / Repos */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-semibold text-blue-400 uppercase tracking-wider flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5" />
                Phase / Repos & Topics
              </label>
              {onOpenNotes && formData.phaseRepos && (
                <button
                  type="button"
                  onClick={() => {
                    const text = (formData.phaseRepos || '').toLowerCase()
                    let repo = 'operating-systems-from-scratch'
                    if (text.includes('os') || text.includes('operating')) repo = 'operating-systems-from-scratch'
                    else if (text.includes('linux')) repo = 'linux-from-scratch'
                    else if (text.includes('network')) repo = 'computer-networking-from-scratch'
                    else if (text.includes('sql') || text.includes('database')) repo = 'database-and-sql-from-scratch'
                    else if (text.includes('java')) repo = 'java-from-scratch'
                    else if (text.includes('lld')) repo = 'low-level-design-from-scratch'
                    else if (text.includes('redis')) repo = 'redis-from-scratch'
                    else if (text.includes('kafka')) repo = 'kafka-from-scratch'
                    else if (text.includes('docker')) repo = 'docker-from-scratch'
                    else if (text.includes('k8s') || text.includes('kubernetes')) repo = 'kubernetes-from-scratch'
                    else if (text.includes('elastic')) repo = 'elasticsearch-from-scratch'

                    onOpenNotes(repo)
                    onClose()
                  }}
                  className="text-[11px] text-purple-400 hover:text-purple-300 font-semibold flex items-center gap-1 hover:underline"
                >
                  <BookOpen className="w-3 h-3" />
                  <span>Open Notes in GUI &rarr;</span>
                </button>
              )}
            </div>
            <input
              type="text"
              value={formData.phaseRepos || ''}
              onChange={(e) => handleInputChange('phaseRepos', e.target.value)}
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-200 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Morning & Evening Sessions */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div>
              <label className="block text-xs font-semibold text-blue-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5" />
                🌅 Morning Session (6:00 - 10:00 AM)
              </label>
              <textarea
                rows={3}
                value={formData.morningSession || ''}
                onChange={(e) => handleInputChange('morningSession', e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-300 focus:outline-none focus:border-blue-500 leading-relaxed"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5" />
                🌙 Evening Session (7:00 - 10:00 PM)
              </label>
              <textarea
                rows={3}
                value={formData.eveningSession || ''}
                onChange={(e) => handleInputChange('eveningSession', e.target.value)}
                className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-300 focus:outline-none focus:border-blue-500 leading-relaxed"
              />
            </div>
          </div>

          {/* Notes & Review Textarea */}
          <div>
            <label className="block text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5" />
              Study Notes & Review Insights
            </label>
            <textarea
              rows={4}
              value={formData.notes || ''}
              onChange={(e) => handleInputChange('notes', e.target.value)}
              placeholder="Add key insights, questions you got wrong, LeetCode submission links, system design tradeoffs..."
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-blue-500 leading-relaxed"
            />
          </div>

          {/* Footer Actions */}
          <div className="pt-4 border-t border-zinc-800 flex items-center justify-between">
            <button
              type="button"
              onClick={() => {
                onDelete(task)
                onClose()
              }}
              className="px-3 py-2 rounded-xl text-xs font-semibold text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 border border-rose-500/20 transition flex items-center gap-1.5"
            >
              <Trash2 className="w-4 h-4" />
              <span>Delete Task</span>
            </button>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl text-xs font-medium text-zinc-400 hover:text-white bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 transition"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSaving}
                className="px-5 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 transition shadow-md shadow-blue-500/20 flex items-center gap-1.5 disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                <span>{isSaving ? 'Saving...' : 'Save Changes'}</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}
