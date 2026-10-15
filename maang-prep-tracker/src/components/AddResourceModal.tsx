'use client'

import React, { useState, useEffect } from 'react'
import { X, BookOpen, Globe, Code2, Link as LinkIcon, Sparkles } from 'lucide-react'
import { getYouTubeEmbedUrl } from '@/types/resource'
import { YouTubeIcon } from './YouTubeIcon'

interface AddResourceModalProps {
  isOpen: boolean
  onClose: () => void
  repoId: string
  phases: { id: string; name: string }[]
  initialPhaseId?: string | null
  onSuccess: (msg: string) => void
}

export const AddResourceModal: React.FC<AddResourceModalProps> = ({
  isOpen,
  onClose,
  repoId,
  phases,
  initialPhaseId,
  onSuccess,
}) => {
  const [title, setTitle] = useState('')
  const [url, setUrl] = useState('')
  const [type, setType] = useState<'youtube' | 'article' | 'doc' | 'interactive'>('youtube')
  const [phaseId, setPhaseId] = useState<string>(initialPhaseId || '')
  const [description, setDescription] = useState('')
  const [tags, setTags] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [previewEmbedUrl, setPreviewEmbedUrl] = useState<string | null>(null)

  useEffect(() => {
    if (initialPhaseId) {
      setPhaseId(initialPhaseId)
    }
  }, [initialPhaseId])

  // Auto-detect YouTube URL
  useEffect(() => {
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
      setType('youtube')
      const embed = getYouTubeEmbedUrl(url)
      setPreviewEmbedUrl(embed)
    } else {
      setPreviewEmbedUrl(null)
    }
  }, [url])

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim() || !url.trim()) return

    setIsSubmitting(true)
    try {
      const res = await fetch(`/api/repos/${repoId}/resources`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: title.trim(),
          url: url.trim(),
          type,
          phaseId: phaseId ? phaseId : null,
          description: description.trim(),
          tags: tags.trim(),
        }),
      })

      const data = await res.json()
      if (data.success) {
        onSuccess('Resource added successfully!')
        setTitle('')
        setUrl('')
        setDescription('')
        setTags('')
        onClose()
      } else {
        alert(data.error || 'Failed to add resource')
      }
    } catch (err: unknown) {
      const error = err as Error
      alert(`Error: ${error.message}`)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-[#0f111a] border border-zinc-800 rounded-2xl w-full max-w-xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="p-4 sm:p-5 border-b border-zinc-800/80 flex items-center justify-between bg-zinc-900/50">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white">Add Additional Resource / Embed</h2>
              <p className="text-xs text-zinc-400">Embed helpful videos, articles, docs, or interactive tools</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="p-4 sm:p-6 overflow-y-auto space-y-4 text-xs">
          {/* Resource Type Buttons */}
          <div>
            <label className="block text-zinc-400 font-semibold mb-1.5">Resource Type</label>
            <div className="grid grid-cols-4 gap-2">
              <button
                type="button"
                onClick={() => setType('youtube')}
                className={`py-2 px-2.5 rounded-xl border flex flex-col items-center gap-1 transition ${
                  type === 'youtube'
                    ? 'bg-rose-500/20 border-rose-500/50 text-rose-300 font-bold'
                    : 'bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <YouTubeIcon className="w-4 h-4 text-rose-400" />
                <span className="text-[11px]">YouTube</span>
              </button>

              <button
                type="button"
                onClick={() => setType('article')}
                className={`py-2 px-2.5 rounded-xl border flex flex-col items-center gap-1 transition ${
                  type === 'article'
                    ? 'bg-blue-500/20 border-blue-500/50 text-blue-300 font-bold'
                    : 'bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <BookOpen className="w-4 h-4 text-blue-400" />
                <span className="text-[11px]">Article / Post</span>
              </button>

              <button
                type="button"
                onClick={() => setType('doc')}
                className={`py-2 px-2.5 rounded-xl border flex flex-col items-center gap-1 transition ${
                  type === 'doc'
                    ? 'bg-purple-500/20 border-purple-500/50 text-purple-300 font-bold'
                    : 'bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <Globe className="w-4 h-4 text-purple-400" />
                <span className="text-[11px]">Docs / Book</span>
              </button>

              <button
                type="button"
                onClick={() => setType('interactive')}
                className={`py-2 px-2.5 rounded-xl border flex flex-col items-center gap-1 transition ${
                  type === 'interactive'
                    ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300 font-bold'
                    : 'bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <Code2 className="w-4 h-4 text-emerald-400" />
                <span className="text-[11px]">Tool / Site</span>
              </button>
            </div>
          </div>

          {/* Title */}
          <div>
            <label className="block text-zinc-300 font-semibold mb-1">
              Title <span className="text-rose-400">*</span>
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. MIT 6.S081: OS Isolation & System Calls"
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* URL */}
          <div>
            <label className="block text-zinc-300 font-semibold mb-1">
              URL / Link <span className="text-rose-400">*</span>
            </label>
            <div className="relative">
              <LinkIcon className="w-4 h-4 text-zinc-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="url"
                required
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://www.youtube.com/watch?v=... or https://..."
                className="w-full pl-9 pr-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500 font-mono text-[11px]"
              />
            </div>
          </div>

          {/* YouTube Embed Preview */}
          {previewEmbedUrl && (
            <div className="p-3 bg-zinc-950 rounded-xl border border-zinc-800/80">
              <span className="text-[11px] font-semibold text-rose-400 block mb-2">
                Embedded Video Preview:
              </span>
              <div className="relative aspect-video rounded-lg overflow-hidden bg-black">
                <iframe
                  src={previewEmbedUrl}
                  title="YouTube Preview"
                  className="w-full h-full border-0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>
            </div>
          )}

          {/* Tag to Phase */}
          <div>
            <label className="block text-zinc-300 font-semibold mb-1">
              Tag to Phase (Optional)
            </label>
            <select
              value={phaseId}
              onChange={(e) => setPhaseId(e.target.value)}
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-zinc-200 focus:outline-none focus:border-blue-500 text-xs"
            >
              <option value="">General (Repo-Wide Resource)</option>
              {phases.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </div>

          {/* Description / Key takeaways */}
          <div>
            <label className="block text-zinc-300 font-semibold mb-1">
              Key Takeaway / Notes
            </label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Why this resource is valuable, key points to remember, timestamps..."
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500 text-xs"
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-zinc-300 font-semibold mb-1">
              Tags (comma separated)
            </label>
            <input
              type="text"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="e.g. xv6, syscalls, kernel, video"
              className="w-full px-3 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500 text-xs"
            />
          </div>

          {/* Submit Buttons */}
          <div className="pt-3 border-t border-zinc-800/80 flex items-center justify-end gap-2.5">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-medium text-zinc-400 hover:text-white bg-zinc-900 hover:bg-zinc-800 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 transition shadow-lg shadow-blue-600/20 disabled:opacity-50"
            >
              {isSubmitting ? 'Saving...' : 'Embed Resource'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
