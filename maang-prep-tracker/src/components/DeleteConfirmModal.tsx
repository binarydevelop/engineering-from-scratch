'use client'

import React from 'react'
import { Task } from '@/types/task'
import { AlertTriangle, Trash2 } from 'lucide-react'

interface DeleteConfirmModalProps {
  task: Task | null
  isOpen: boolean
  onClose: () => void
  onConfirm: (taskId: string) => Promise<void>
  isDeleting: boolean
}

export const DeleteConfirmModal: React.FC<DeleteConfirmModalProps> = ({
  task,
  isOpen,
  onClose,
  onConfirm,
  isDeleting,
}) => {
  if (!isOpen || !task) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
      <div className="bg-[#0f1016] border border-rose-500/20 rounded-2xl w-full max-w-md p-6 shadow-2xl animate-in fade-in duration-200">
        <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 mb-4">
          <AlertTriangle className="w-6 h-6" />
        </div>

        <h3 className="text-base font-bold text-white mb-2">Delete Scheduled Task?</h3>
        <p className="text-xs text-zinc-400 leading-relaxed mb-4">
          Are you sure you want to delete{' '}
          <strong className="text-zinc-200">{task.taskName}</strong> scheduled for{' '}
          <strong className="text-blue-400">{task.date}</strong>? This action will permanently remove it from the database.
        </p>

        <div className="flex items-center justify-end gap-2 pt-2">
          <button
            onClick={onClose}
            disabled={isDeleting}
            className="px-4 py-2 rounded-xl text-xs font-medium text-zinc-400 hover:text-white bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 transition"
          >
            Cancel
          </button>
          <button
            onClick={() => onConfirm(task.id)}
            disabled={isDeleting}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-rose-600 hover:bg-rose-500 transition shadow-md shadow-rose-500/20 flex items-center gap-1.5 disabled:opacity-50"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>{isDeleting ? 'Deleting...' : 'Delete Permanently'}</span>
          </button>
        </div>
      </div>
    </div>
  )
}
