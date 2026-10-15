'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { Task, TaskStats } from '@/types/task'
import { Navbar } from '@/components/Navbar'
import { StatsOverview } from '@/components/StatsOverview'
import { TaskFilterBar } from '@/components/TaskFilterBar'
import { TaskListView } from '@/components/TaskListView'
import { TaskKanbanView } from '@/components/TaskKanbanView'
import { TaskGridView } from '@/components/TaskGridView'
import { TaskModal } from '@/components/TaskModal'
import { CreateTaskModal } from '@/components/CreateTaskModal'
import { DeleteConfirmModal } from '@/components/DeleteConfirmModal'
import { RepoNotesBrowser } from '@/components/RepoNotesBrowser'
import { Loader2, CheckCircle2 } from 'lucide-react'

export default function TrackerDashboard() {
  const [appTab, setAppTab] = useState<'tracker' | 'notes'>('tracker')
  const [selectedRepoForNotes, setSelectedRepoForNotes] = useState('operating-systems-from-scratch')

  const [tasks, setTasks] = useState<Task[]>([])
  const [stats, setStats] = useState<TaskStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Filters & Views
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedSprint, setSelectedSprint] = useState('all')
  const [selectedStatus, setSelectedStatus] = useState('all')
  const [selectedPriority, setSelectedPriority] = useState('all')
  const [activeView, setActiveView] = useState<'list' | 'kanban' | 'calendar'>('list')

  // Modals & Actions
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [isReseeding, setIsReseeding] = useState(false)

  // Toast feedback
  const [toastMessage, setToastMessage] = useState<string | null>(null)

  const showToast = (msg: string) => {
    setToastMessage(msg)
    setTimeout(() => {
      setToastMessage(null)
    }, 3500)
  }

  // Fetch Stats
  const loadStats = useCallback(async () => {
    try {
      const res = await fetch('/api/stats')
      const data = await res.json()
      if (data.success) {
        setStats(data.stats)
      }
    } catch (err) {
      console.error('Failed to load stats:', err)
    }
  }, [])

  // Fetch Tasks with filters
  const loadTasks = useCallback(async () => {
    try {
      const params = new URLSearchParams()
      if (searchQuery) params.set('search', searchQuery)
      if (selectedSprint !== 'all') params.set('sprint', selectedSprint)
      if (selectedStatus !== 'all') params.set('status', selectedStatus)
      if (selectedPriority !== 'all') params.set('priority', selectedPriority)

      const res = await fetch(`/api/tasks?${params.toString()}`)
      const data = await res.json()
      if (data.success) {
        setTasks(data.tasks)
      }
    } catch (err) {
      console.error('Failed to load tasks:', err)
    } finally {
      setIsLoading(false)
    }
  }, [searchQuery, selectedSprint, selectedStatus, selectedPriority])

  useEffect(() => {
    loadStats()
  }, [loadStats])

  useEffect(() => {
    loadTasks()
  }, [loadTasks])

  // Extract distinct sprint list for dropdown
  const sprintsList = [
    '🔶 Sprint 1 — Foundations Blitz',
    '🔶 Sprint 2 — Backend Engineering Core',
    '🔶 Sprint 3 — LLD Mastery',
    '🔶 Sprint 4 — System Design: Foundations',
    '🔶 Sprint 5 — SD Interview Mode + Infrastructure',
    '🔶 Sprint 6 — Advanced / Differentiation Track',
    '🔶 Sprint 7 — Staff Engineering + Behavioral',
  ]

  // Handlers
  const handleQuickUpdateStatus = async (taskId: string, newStatus: string) => {
    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t))
    )

    try {
      const res = await fetch(`/api/tasks/${taskId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      })
      const data = await res.json()
      if (data.success) {
        showToast(`Task status updated to ${newStatus}`)
        loadStats()
      } else {
        showToast(`Error: ${data.error}`)
        loadTasks()
      }
    } catch (err) {
      console.error('Failed to update task:', err)
      loadTasks()
    }
  }

  const handleSaveTask = async (updatedFields: Partial<Task> & { id: string }) => {
    try {
      const res = await fetch(`/api/tasks/${updatedFields.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedFields),
      })
      const data = await res.json()
      if (data.success) {
        showToast('Task details saved successfully!')
        loadTasks()
        loadStats()
      } else {
        showToast(`Error: ${data.error}`)
      }
    } catch (err) {
      console.error('Failed to save task:', err)
      showToast('Failed to save task')
    }
  }

  const handleDeleteTask = async (taskId: string) => {
    setIsDeleting(true)
    try {
      const res = await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
      })
      const data = await res.json()
      if (data.success) {
        showToast('Task permanently deleted')
        setTaskToDelete(null)
        loadTasks()
        loadStats()
      } else {
        showToast(`Error: ${data.error}`)
      }
    } catch (err) {
      console.error('Failed to delete task:', err)
      showToast('Failed to delete task')
    } finally {
      setIsDeleting(false)
    }
  }

  const handleCreateTask = async (newTaskData: Omit<Task, 'id'>) => {
    try {
      const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTaskData),
      })
      const data = await res.json()
      if (data.success) {
        showToast('New task created successfully!')
        loadTasks()
        loadStats()
      } else {
        showToast(`Error: ${data.error}`)
      }
    } catch (err) {
      console.error('Failed to create task:', err)
      showToast('Failed to create task')
    }
  }

  const handleReseed = async () => {
    const confirmReset = window.confirm(
      'Are you sure you want to re-seed the database? This will reset all 191 tasks back to their original schedule starting October 17, 2026.'
    )
    if (!confirmReset) return

    setIsReseeding(true)
    try {
      const res = await fetch('/api/seed', { method: 'POST' })
      const data = await res.json()
      if (data.success) {
        showToast('Database successfully re-seeded with 191 tasks!')
        loadTasks()
        loadStats()
      } else {
        showToast(`Error: ${data.error}`)
      }
    } catch (err) {
      console.error('Failed to reseed:', err)
      showToast('Failed to reseed database')
    } finally {
      setIsReseeding(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#090a0f] text-zinc-100 flex flex-col font-sans">
      {/* Navbar */}
      <Navbar
        activeTab={appTab}
        onTabChange={setAppTab}
        onOpenCreateModal={() => setIsCreateModalOpen(true)}
        onReseed={handleReseed}
        isReseeding={isReseeding}
        totalDone={stats?.done || 0}
        totalTasks={stats?.total || 191}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {appTab === 'notes' ? (
          /* Tab 2: Repo Notes & Docs Browser GUI */
          <RepoNotesBrowser initialRepo={selectedRepoForNotes} />
        ) : (
          /* Tab 1: Daily Schedule Tracker */
          <>
            {/* High-level stats cards */}
            <StatsOverview
              stats={stats}
              onQuickUpdateStatus={handleQuickUpdateStatus}
              onSelectTask={(task) => {
                setSelectedTask(task)
                setIsTaskModalOpen(true)
              }}
            />

            {/* Filter & View Switcher */}
            <TaskFilterBar
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
              selectedSprint={selectedSprint}
              onSprintChange={setSelectedSprint}
              selectedStatus={selectedStatus}
              onStatusChange={setSelectedStatus}
              selectedPriority={selectedPriority}
              onPriorityChange={setSelectedPriority}
              activeView={activeView}
              onViewChange={setActiveView}
              sprintsList={sprintsList}
              totalFiltered={tasks.length}
            />

            {/* Dynamic Views */}
            {isLoading ? (
              <div className="py-24 flex flex-col items-center justify-center gap-3">
                <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
                <p className="text-xs text-zinc-400">Loading your schedule from database...</p>
              </div>
            ) : (
              <>
                {activeView === 'list' && (
                  <TaskListView
                    tasks={tasks}
                    onSelectTask={(task) => {
                      setSelectedTask(task)
                      setIsTaskModalOpen(true)
                    }}
                    onUpdateStatus={handleQuickUpdateStatus}
                    onDeleteTask={(task) => setTaskToDelete(task)}
                  />
                )}

                {activeView === 'kanban' && (
                  <TaskKanbanView
                    tasks={tasks}
                    onSelectTask={(task) => {
                      setSelectedTask(task)
                      setIsTaskModalOpen(true)
                    }}
                    onUpdateStatus={handleQuickUpdateStatus}
                  />
                )}

                {activeView === 'calendar' && (
                  <TaskGridView
                    tasks={tasks}
                    onSelectTask={(task) => {
                      setSelectedTask(task)
                      setIsTaskModalOpen(true)
                    }}
                  />
                )}
              </>
            )}
          </>
        )}
      </main>

      {/* Edit / Detail Modal */}
      <TaskModal
        task={selectedTask}
        isOpen={isTaskModalOpen}
        onClose={() => setIsTaskModalOpen(false)}
        onSave={handleSaveTask}
        onDelete={(task) => setTaskToDelete(task)}
        onOpenNotes={(repoId) => {
          setSelectedRepoForNotes(repoId)
          setAppTab('notes')
        }}
      />

      {/* Create Modal */}
      <CreateTaskModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onCreate={handleCreateTask}
      />

      {/* Delete Confirmation Modal */}
      <DeleteConfirmModal
        task={taskToDelete}
        isOpen={!!taskToDelete}
        onClose={() => setTaskToDelete(null)}
        onConfirm={handleDeleteTask}
        isDeleting={isDeleting}
      />

      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-zinc-900 border border-zinc-700 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-2.5 text-xs font-semibold animate-in slide-in-from-bottom-5">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage}</span>
        </div>
      )}
    </div>
  )
}
