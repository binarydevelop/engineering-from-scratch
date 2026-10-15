'use client'

import React, { useState } from 'react'
import { MarkdownViewer } from './MarkdownViewer'
import { Save, Eye, Edit3, Columns, GitCommit } from 'lucide-react'

interface NotesEditorProps {
  initialContent: string
  filePath: string
  repo: string
  isCreatingNew?: boolean
  onSave: (filePath: string, content: string, commitMessage: string, pushToGit: boolean) => Promise<void>
  onCancel: () => void
  isSaving: boolean
}

export const NotesEditor: React.FC<NotesEditorProps> = ({
  initialContent,
  filePath,
  repo,
  isCreatingNew = false,
  onSave,
  onCancel,
  isSaving,
}) => {
  const [content, setContent] = useState(initialContent)
  const [customPath, setCustomPath] = useState(filePath)
  const [commitMessage, setCommitMessage] = useState(
    isCreatingNew ? `docs(${repo}): create ${filePath}` : `docs(${repo}): update ${filePath}`
  )
  const [pushToGit, setPushToGit] = useState(true)
  const [editorMode, setEditorMode] = useState<'edit' | 'preview' | 'split'>('split')

  const wordCount = content.trim() ? content.trim().split(/\s+/).length : 0

  const handleSave = async () => {
    const finalPath = isCreatingNew ? customPath.trim() : filePath
    if (!finalPath) return
    await onSave(finalPath, content, commitMessage, pushToGit)
  }

  return (
    <div className="flex flex-col h-full bg-[#0d0e15] rounded-2xl border border-zinc-800 overflow-hidden shadow-xl">
      {/* Top Toolbar */}
      <div className="p-3 bg-zinc-900/90 border-b border-zinc-800 flex flex-wrap items-center justify-between gap-2 text-xs">
        {/* Left: File Path / Title */}
        <div className="flex items-center gap-2 flex-1 min-w-[200px]">
          <span className="text-zinc-500 font-mono">File:</span>
          {isCreatingNew ? (
            <input
              type="text"
              value={customPath}
              onChange={(e) => setCustomPath(e.target.value)}
              placeholder="phases/01-.../notes/my-note.md"
              className="px-2.5 py-1 bg-zinc-950 border border-zinc-700 rounded text-xs font-mono text-white flex-1 focus:outline-none focus:border-blue-500"
            />
          ) : (
            <span className="font-mono text-zinc-300 font-medium truncate">{filePath}</span>
          )}
        </div>

        {/* Center: Mode switcher */}
        <div className="flex items-center p-0.5 bg-zinc-950 rounded-lg border border-zinc-800">
          <button
            onClick={() => setEditorMode('edit')}
            className={`px-2.5 py-1 rounded text-[11px] font-medium transition flex items-center gap-1 ${
              editorMode === 'edit' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
            }`}
          >
            <Edit3 className="w-3 h-3" /> Edit
          </button>
          <button
            onClick={() => setEditorMode('split')}
            className={`px-2.5 py-1 rounded text-[11px] font-medium transition flex items-center gap-1 ${
              editorMode === 'split' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
            }`}
          >
            <Columns className="w-3 h-3" /> Split
          </button>
          <button
            onClick={() => setEditorMode('preview')}
            className={`px-2.5 py-1 rounded text-[11px] font-medium transition flex items-center gap-1 ${
              editorMode === 'preview' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
            }`}
          >
            <Eye className="w-3 h-3" /> Preview
          </button>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={onCancel}
            disabled={isSaving}
            className="px-3 py-1 rounded-lg text-xs text-zinc-400 hover:text-white bg-zinc-800/80 hover:bg-zinc-800 transition"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="px-3.5 py-1 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 transition shadow-sm flex items-center gap-1.5 disabled:opacity-50"
          >
            <Save className="w-3.5 h-3.5" />
            <span>{isSaving ? 'Saving...' : 'Save to Repo'}</span>
          </button>
        </div>
      </div>

      {/* Editor & Preview Workspace */}
      <div className="flex-1 flex overflow-hidden min-h-[500px]">
        {/* Editor Pane */}
        {(editorMode === 'edit' || editorMode === 'split') && (
          <div
            className={`flex flex-col ${
              editorMode === 'split' ? 'w-1/2 border-r border-zinc-800' : 'w-full'
            }`}
          >
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write your markdown notes here... Use # headings, - lists, `code`, and > [!NOTE] callouts..."
              className="w-full h-full p-4 bg-[#0a0b10] text-zinc-200 font-mono text-xs leading-relaxed resize-none focus:outline-none"
            />
          </div>
        )}

        {/* Preview Pane */}
        {(editorMode === 'preview' || editorMode === 'split') && (
          <div
            className={`p-6 overflow-y-auto bg-[#0d0e15] ${
              editorMode === 'split' ? 'w-1/2' : 'w-full'
            }`}
          >
            <MarkdownViewer content={content} />
          </div>
        )}
      </div>

      {/* Bottom Commit & Status Bar */}
      <div className="p-2.5 bg-zinc-900/90 border-t border-zinc-800 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-3 flex-1 min-w-[280px]">
          <GitCommit className="w-3.5 h-3.5 text-zinc-400" />
          <input
            type="text"
            value={commitMessage}
            onChange={(e) => setCommitMessage(e.target.value)}
            placeholder="Git commit message..."
            className="px-2 py-1 bg-zinc-950 border border-zinc-800 rounded text-xs text-zinc-200 flex-1 focus:outline-none focus:border-blue-500"
          />
          <label className="flex items-center gap-1 text-[11px] text-zinc-400 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={pushToGit}
              onChange={(e) => setPushToGit(e.target.checked)}
              className="rounded bg-zinc-950 border-zinc-800 text-blue-500"
            />
            <span>Commit to Git</span>
          </label>
        </div>

        <div className="text-[11px] text-zinc-500 flex items-center gap-3">
          <span>{wordCount} words</span>
          <span>{content.length} characters</span>
        </div>
      </div>
    </div>
  )
}
