'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { MarkdownViewer } from './MarkdownViewer'
import { NotesEditor } from './NotesEditor'
import {
  FolderGit2,
  BookOpen,
  FileText,
  Code2,
  Plus,
  ExternalLink,
  Search,
  ChevronRight,
  ChevronDown,
  Edit2,
  CheckCircle2,
  Sparkles,
} from 'lucide-react'

interface RepoMeta {
  id: string
  name: string
  phaseCount: number
  totalNotes: number
}

interface PhaseDetail {
  id: string
  name: string
  hasDoc: boolean
  docPath: string | null
  notes: { filename: string; path: string; title: string }[]
  codeFiles: { filename: string; path: string }[]
}

interface RepoDetail {
  id: string
  name: string
  phaseCount: number
  hasPhases: boolean
  hasReadme: boolean
  hasRoadmap: boolean
  rootNotes: { filename: string; path: string; title: string }[]
  phases: PhaseDetail[]
  isLocal: boolean
}

interface RepoNotesBrowserProps {
  initialRepo?: string
  initialPhaseId?: string
}

export const RepoNotesBrowser: React.FC<RepoNotesBrowserProps> = ({
  initialRepo = 'operating-systems-from-scratch',
  initialPhaseId,
}) => {
  const [reposList, setReposList] = useState<RepoMeta[]>([])
  const [selectedRepoId, setSelectedRepoId] = useState<string>(initialRepo)
  const [repoDetail, setRepoDetail] = useState<RepoDetail | null>(null)
  const [selectedPhase, setSelectedPhase] = useState<PhaseDetail | null>(null)
  const [activeFilePath, setActiveFilePath] = useState<string | null>(null)
  const [fileContent, setFileContent] = useState<string>('')
  const [fileSource, setFileSource] = useState<'local' | 'github'>('local')
  const [isLoading, setIsLoading] = useState(false)
  const [isFileLoading, setIsFileLoading] = useState(false)
  const [phaseSearch, setPhaseSearch] = useState('')

  // Editor states
  const [isEditing, setIsEditing] = useState(false)
  const [isCreatingNew, setIsCreatingNew] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [statusMessage, setStatusMessage] = useState<string | null>(null)

  const showStatus = (msg: string) => {
    setStatusMessage(msg)
    setTimeout(() => setStatusMessage(null), 3500)
  }

  // 1. Fetch Repos List
  useEffect(() => {
    async function loadRepos() {
      try {
        const res = await fetch('/api/repos')
        const data = await res.json()
        if (data.success) {
          setReposList(data.repos)
        }
      } catch (e) {
        console.error('Failed to load repos:', e)
      }
    }
    loadRepos()
  }, [])

  // 2. Fetch Selected Repo Detail
  const loadRepoDetail = useCallback(async (repoId: string, targetPhaseId?: string) => {
    setIsLoading(true)
    try {
      const res = await fetch(`/api/repos/${repoId}`)
      const data = await res.json()
      if (data.success) {
        setRepoDetail(data.repo)

        // Select phase
        const initialP = targetPhaseId
          ? data.repo.phases.find((p: PhaseDetail) => p.id === targetPhaseId || p.id.includes(targetPhaseId))
          : data.repo.phases[0]

        if (initialP) {
          setSelectedPhase(initialP)
          // Default to notes file if present, or docPath
          if (initialP.notes && initialP.notes.length > 0) {
            loadFileContent(repoId, initialP.notes[0].path)
          } else if (initialP.docPath) {
            loadFileContent(repoId, initialP.docPath)
          }
        } else if (data.repo.hasRoadmap) {
          loadFileContent(repoId, 'ROADMAP.md')
        }
      }
    } catch (e) {
      console.error('Failed to load repo detail:', e)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    if (selectedRepoId) {
      loadRepoDetail(selectedRepoId, initialPhaseId)
    }
  }, [selectedRepoId, loadRepoDetail, initialPhaseId])

  // 3. Load File Content
  const loadFileContent = async (repoId: string, path: string) => {
    setIsFileLoading(true)
    setActiveFilePath(path)
    setIsEditing(false)
    setIsCreatingNew(false)
    try {
      const res = await fetch(`/api/repos/${repoId}/file?path=${encodeURIComponent(path)}`)
      const data = await res.json()
      if (data.success) {
        setFileContent(data.content)
        setFileSource(data.source)
      } else {
        setFileContent(`*Error loading file: ${data.error}*`)
      }
    } catch (e: unknown) {
      const err = e as Error
      setFileContent(`*Failed to load content: ${err.message}*`)
    } finally {
      setIsFileLoading(false)
    }
  }

  // 4. Save / Create File
  const handleSaveFile = async (
    targetPath: string,
    content: string,
    commitMessage: string,
    pushToGit: boolean
  ) => {
    setIsSaving(true)
    try {
      const res = await fetch(`/api/repos/${selectedRepoId}/file`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filePath: targetPath,
          content,
          commitMessage,
          pushToGit,
        }),
      })
      const data = await res.json()
      if (data.success) {
        showStatus(data.message || 'File saved successfully!')
        setFileContent(content)
        setActiveFilePath(targetPath)
        setIsEditing(false)
        setIsCreatingNew(false)
        // Refresh repo detail to reflect newly added note in tree
        loadRepoDetail(selectedRepoId, selectedPhase?.id)
      } else {
        showStatus(`Error: ${data.error}`)
      }
    } catch (e: unknown) {
      const err = e as Error
      showStatus(`Save failed: ${err.message}`)
    } finally {
      setIsSaving(false)
    }
  }

  // Filter phases by search
  const filteredPhases = repoDetail?.phases.filter(
    (p) =>
      p.name.toLowerCase().includes(phaseSearch.toLowerCase()) ||
      p.id.toLowerCase().includes(phaseSearch.toLowerCase()) ||
      p.notes.some((n) => n.title.toLowerCase().includes(phaseSearch.toLowerCase()))
  ) || []

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] bg-[#090a0f] text-zinc-100 rounded-2xl border border-zinc-800 overflow-hidden shadow-2xl">
      {/* Top Header Bar */}
      <div className="p-3 sm:p-4 bg-zinc-900/90 border-b border-zinc-800 flex flex-wrap items-center justify-between gap-3">
        {/* Repo selector dropdown */}
        <div className="flex items-center gap-2.5 flex-1 min-w-[280px]">
          <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <FolderGit2 className="w-4 h-4" />
          </div>
          <select
            value={selectedRepoId}
            onChange={(e) => setSelectedRepoId(e.target.value)}
            className="bg-zinc-950 border border-zinc-700 text-white font-semibold text-xs sm:text-sm py-2 px-3 rounded-xl focus:outline-none focus:border-blue-500 max-w-sm truncate"
          >
            {reposList.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} ({r.phaseCount} phases{r.totalNotes > 0 ? ` · ${r.totalNotes} notes` : ''})
              </option>
            ))}
          </select>

          <span className="hidden md:inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-zinc-800 text-zinc-300">
            binarydevelop/engineering-from-scratch
          </span>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          {selectedPhase && !isEditing && (
            <button
              onClick={() => {
                const defaultNewNoteName = `phases/${selectedPhase.id}/notes/0${selectedPhase.notes.length + 1}-interview-notes.md`
                setActiveFilePath(defaultNewNoteName)
                setFileContent(`# Notes on ${selectedPhase.name}\n\n## Key Concepts\n- \n\n## Interview Questions\n- \n\n## Trade-offs & Production Gotchas\n- \n`)
                setIsCreatingNew(true)
                setIsEditing(true)
              }}
              className="px-3 py-1.5 rounded-lg text-xs font-semibold text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 transition flex items-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Note</span>
            </button>
          )}

          {activeFilePath && !isEditing && (
            <button
              onClick={() => setIsEditing(true)}
              className="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-750 border border-zinc-700 transition flex items-center gap-1.5"
            >
              <Edit2 className="w-3.5 h-3.5" />
              <span>Edit Note</span>
            </button>
          )}

          {activeFilePath && (
            <a
              href={`https://github.com/binarydevelop/engineering-from-scratch/blob/main/${selectedRepoId}/${activeFilePath}`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-2.5 py-1.5 rounded-lg text-xs text-zinc-400 hover:text-zinc-200 bg-zinc-950 border border-zinc-800 transition flex items-center gap-1"
              title="View on GitHub"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">GitHub</span>
            </a>
          )}
        </div>
      </div>

      {/* Main Split Layout: Sidebar & Content Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar: Phases & Files Tree */}
        <div className="w-80 md:w-96 border-r border-zinc-800/80 bg-[#0a0b10] flex flex-col">
          {/* Phase search bar */}
          <div className="p-3 border-b border-zinc-800">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={phaseSearch}
                onChange={(e) => setPhaseSearch(e.target.value)}
                placeholder="Search phases or notes..."
                className="w-full pl-8 pr-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          {/* Quick Repo Root Links */}
          {repoDetail && (repoDetail.hasRoadmap || repoDetail.hasReadme || repoDetail.rootNotes.length > 0) && (
            <div className="p-2 border-b border-zinc-800/60 bg-zinc-950/40 text-xs space-y-1">
              <span className="px-2 text-[10px] font-semibold uppercase tracking-wider text-zinc-500">
                Repo Root
              </span>
              {repoDetail.hasRoadmap && (
                <button
                  onClick={() => loadFileContent(selectedRepoId, 'ROADMAP.md')}
                  className={`w-full text-left px-2 py-1 rounded text-xs transition flex items-center gap-1.5 ${
                    activeFilePath === 'ROADMAP.md'
                      ? 'bg-blue-600/20 text-blue-300 font-semibold'
                      : 'text-zinc-400 hover:text-white'
                  }`}
                >
                  <BookOpen className="w-3 h-3 text-blue-400" />
                  <span>ROADMAP.md</span>
                </button>
              )}
              {repoDetail.hasReadme && (
                <button
                  onClick={() => loadFileContent(selectedRepoId, 'README.md')}
                  className={`w-full text-left px-2 py-1 rounded text-xs transition flex items-center gap-1.5 ${
                    activeFilePath === 'README.md'
                      ? 'bg-blue-600/20 text-blue-300 font-semibold'
                      : 'text-zinc-400 hover:text-white'
                  }`}
                >
                  <FileText className="w-3 h-3 text-zinc-400" />
                  <span>README.md</span>
                </button>
              )}
              {repoDetail.rootNotes.map((rn) => (
                <button
                  key={rn.path}
                  onClick={() => loadFileContent(selectedRepoId, rn.path)}
                  className={`w-full text-left px-2 py-1 rounded text-xs transition flex items-center gap-1.5 ${
                    activeFilePath === rn.path
                      ? 'bg-blue-600/20 text-blue-300 font-semibold'
                      : 'text-zinc-400 hover:text-white'
                  }`}
                >
                  <Sparkles className="w-3 h-3 text-purple-400" />
                  <span className="truncate">{rn.title}</span>
                </button>
              ))}
            </div>
          )}

          {/* Phases List */}
          <div className="flex-1 overflow-y-auto divide-y divide-zinc-900">
            {isLoading ? (
              <div className="p-8 text-center text-xs text-zinc-500">Loading phases...</div>
            ) : filteredPhases.length === 0 ? (
              <div className="p-8 text-center text-xs text-zinc-500">No matching phases found</div>
            ) : (
              filteredPhases.map((phase) => {
                const isSelected = selectedPhase?.id === phase.id

                return (
                  <div key={phase.id} className="p-2">
                    {/* Phase Header */}
                    <button
                      onClick={() => {
                        setSelectedPhase(phase)
                        if (phase.notes.length > 0) {
                          loadFileContent(selectedRepoId, phase.notes[0].path)
                        } else if (phase.docPath) {
                          loadFileContent(selectedRepoId, phase.docPath)
                        }
                      }}
                      className={`w-full text-left px-2 py-1.5 rounded-lg text-xs font-semibold transition flex items-center justify-between ${
                        isSelected
                          ? 'bg-zinc-800 text-white'
                          : 'text-zinc-300 hover:bg-zinc-900 hover:text-white'
                      }`}
                    >
                      <span className="truncate flex-1">{phase.name}</span>
                      <div className="flex items-center gap-1.5 ml-2">
                        {phase.notes.length > 0 && (
                          <span className="px-1.5 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300 font-bold">
                            {phase.notes.length} notes
                          </span>
                        )}
                        {isSelected ? (
                          <ChevronDown className="w-3.5 h-3.5 text-zinc-400" />
                        ) : (
                          <ChevronRight className="w-3.5 h-3.5 text-zinc-500" />
                        )}
                      </div>
                    </button>

                    {/* Files inside this phase */}
                    {isSelected && (
                      <div className="mt-1 pl-3 space-y-0.5 border-l border-zinc-800/80 ml-2">
                        {/* Doc file */}
                        {phase.docPath && (
                          <button
                            onClick={() => loadFileContent(selectedRepoId, phase.docPath!)}
                            className={`w-full text-left px-2 py-1 rounded text-xs transition flex items-center gap-1.5 ${
                              activeFilePath === phase.docPath
                                ? 'bg-blue-600/20 text-blue-300 font-semibold'
                                : 'text-zinc-400 hover:text-white'
                            }`}
                          >
                            <BookOpen className="w-3 h-3 text-blue-400 flex-shrink-0" />
                            <span className="truncate">Phase Guide</span>
                          </button>
                        )}

                        {/* Notes files */}
                        {phase.notes.map((note) => (
                          <button
                            key={note.path}
                            onClick={() => loadFileContent(selectedRepoId, note.path)}
                            className={`w-full text-left px-2 py-1 rounded text-xs transition flex items-center gap-1.5 ${
                              activeFilePath === note.path
                                ? 'bg-purple-600/20 text-purple-300 font-semibold'
                                : 'text-zinc-400 hover:text-white'
                            }`}
                          >
                            <FileText className="w-3 h-3 text-purple-400 flex-shrink-0" />
                            <span className="truncate" title={note.title}>
                              {note.title}
                            </span>
                          </button>
                        ))}

                        {/* Code files */}
                        {phase.codeFiles.map((code) => (
                          <button
                            key={code.path}
                            onClick={() => loadFileContent(selectedRepoId, code.path)}
                            className={`w-full text-left px-2 py-1 rounded text-xs transition flex items-center gap-1.5 ${
                              activeFilePath === code.path
                                ? 'bg-emerald-600/20 text-emerald-300 font-semibold'
                                : 'text-zinc-500 hover:text-zinc-300'
                            }`}
                          >
                            <Code2 className="w-3 h-3 text-emerald-400 flex-shrink-0" />
                            <span className="truncate font-mono text-[11px]">{code.filename}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )
              })
            )}
          </div>
        </div>

        {/* Right Main Content Pane */}
        <div className="flex-1 flex flex-col bg-[#0b0c12] overflow-hidden">
          {/* Breadcrumb / File Header */}
          <div className="px-4 py-2.5 bg-zinc-900/40 border-b border-zinc-800/80 flex items-center justify-between text-xs">
            <div className="flex items-center gap-1.5 text-zinc-400 font-mono truncate">
              <span className="text-zinc-300">{selectedRepoId}</span>
              <span>/</span>
              <span className="text-blue-400 truncate">{activeFilePath || 'Select a document'}</span>
            </div>

            <div className="flex items-center gap-2">
              <span
                className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                  fileSource === 'local'
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                }`}
              >
                {fileSource === 'local' ? 'Local Disk' : 'GitHub Live'}
              </span>
            </div>
          </div>

          {/* Body: Either Editor or Viewer */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-8">
            {isFileLoading ? (
              <div className="py-24 text-center text-xs text-zinc-500">Loading document...</div>
            ) : isEditing ? (
              <NotesEditor
                initialContent={fileContent}
                filePath={activeFilePath || ''}
                repo={selectedRepoId}
                isCreatingNew={isCreatingNew}
                onSave={handleSaveFile}
                onCancel={() => {
                  setIsEditing(false)
                  setIsCreatingNew(false)
                }}
                isSaving={isSaving}
              />
            ) : (
              <MarkdownViewer content={fileContent} />
            )}
          </div>
        </div>
      </div>

      {/* Toast Notification */}
      {statusMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-zinc-900 border border-zinc-700 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-2.5 text-xs font-semibold animate-in slide-in-from-bottom-5">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{statusMessage}</span>
        </div>
      )}
    </div>
  )
}
