'use client'

import React, { useState } from 'react'
import { Resource } from '@/types/resource'
import { YouTubeIcon } from './YouTubeIcon'
import {
  BookOpen,
  Globe,
  Code2,
  ExternalLink,
  Trash2,
  Plus,
  Search,
  Sparkles,
  Maximize2,
  Minimize2,
} from 'lucide-react'

interface ResourcesViewerProps {
  resources: Resource[]
  repoId?: string
  selectedPhaseId?: string | null
  phases: { id: string; name: string }[]
  onOpenAddModal: () => void
  onDeleteResource: (id: string) => void
  onSelectPhaseFilter?: (phaseId: string | null) => void
}

export const ResourcesViewer: React.FC<ResourcesViewerProps> = ({
  resources,
  selectedPhaseId,
  phases,
  onOpenAddModal,
  onDeleteResource,
  onSelectPhaseFilter,
}) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedType, setSelectedType] = useState<string>('all')
  const [expandedIframeId, setExpandedIframeId] = useState<string | null>(null)

  // Filter resources
  const filtered = resources.filter((r) => {
    // Type filter
    if (selectedType !== 'all' && r.type !== selectedType) {
      return false
    }

    // Phase filter
    if (selectedPhaseId && r.phaseId && r.phaseId !== selectedPhaseId) {
      return false
    }

    // Search query
    if (searchQuery) {
      const q = searchQuery.toLowerCase()
      const titleMatch = r.title.toLowerCase().includes(q)
      const descMatch = (r.description || '').toLowerCase().includes(q)
      const tagsMatch = (r.tags || '').toLowerCase().includes(q)
      return titleMatch || descMatch || tagsMatch
    }

    return true
  })

  const getDomain = (url: string) => {
    try {
      const u = new URL(url)
      return u.hostname.replace('www.', '')
    } catch {
      return 'link'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'youtube':
        return <YouTubeIcon className="w-4 h-4 text-rose-400" />
      case 'doc':
        return <BookOpen className="w-4 h-4 text-purple-400" />
      case 'interactive':
        return <Code2 className="w-4 h-4 text-emerald-400" />
      default:
        return <Globe className="w-4 h-4 text-blue-400" />
    }
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-[#0b0c14] overflow-hidden">
      {/* Top Filter & Action Bar */}
      <div className="p-4 bg-zinc-900/60 border-b border-zinc-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
        {/* Search & Type filter */}
        <div className="flex items-center gap-2 flex-1 min-w-[260px]">
          <div className="relative flex-1 max-w-xs">
            <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search resources, tags, notes..."
              className="w-full pl-8 pr-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Type Filter Buttons */}
          <div className="hidden sm:flex items-center gap-1 p-0.5 bg-zinc-950 rounded-lg border border-zinc-800">
            {['all', 'youtube', 'article', 'doc', 'interactive'].map((t) => (
              <button
                key={t}
                onClick={() => setSelectedType(t)}
                className={`px-2.5 py-1 rounded text-[11px] font-medium capitalize transition ${
                  selectedType === t
                    ? 'bg-zinc-800 text-white shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                {t === 'all' ? 'All Types' : t}
              </button>
            ))}
          </div>
        </div>

        {/* Phase Filter dropdown & Add Resource Button */}
        <div className="flex items-center gap-2">
          {onSelectPhaseFilter && (
            <select
              value={selectedPhaseId || ''}
              onChange={(e) => onSelectPhaseFilter(e.target.value || null)}
              className="bg-zinc-950 border border-zinc-800 rounded-lg py-1.5 px-2.5 text-zinc-300 text-xs focus:outline-none focus:border-blue-500 max-w-[200px] truncate"
            >
              <option value="">All Phases & General</option>
              {phases.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          )}

          <button
            onClick={onOpenAddModal}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 transition flex items-center gap-1.5 shadow-lg shadow-blue-600/20"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Embed Resource</span>
          </button>
        </div>
      </div>

      {/* Resources Content Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {filtered.length === 0 ? (
          <div className="py-16 text-center max-w-md mx-auto">
            <div className="w-12 h-12 rounded-2xl bg-zinc-900 border border-zinc-800 flex items-center justify-center mx-auto mb-3 text-zinc-500">
              <Sparkles className="w-6 h-6 text-zinc-400" />
            </div>
            <h3 className="text-sm font-bold text-white mb-1">No embedded resources found</h3>
            <p className="text-xs text-zinc-400 mb-4">
              Found a great YouTube lecture, technical blog post, or textbook chapter? Embed it here so it stays attached to this topic.
            </p>
            <button
              onClick={onOpenAddModal}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 transition inline-flex items-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Embed Your First Resource</span>
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            {filtered.map((resource) => {
              const phaseName = phases.find((p) => p.id === resource.phaseId)?.name
              const isYouTube = resource.type === 'youtube' && resource.embedUrl
              const isIframeOpen = expandedIframeId === resource.id

              return (
                <div
                  key={resource.id}
                  className="bg-[#0f111a] rounded-2xl border border-zinc-800/90 hover:border-zinc-700/80 transition flex flex-col overflow-hidden shadow-xl"
                >
                  {/* YouTube Embed Player */}
                  {isYouTube ? (
                    <div className="relative aspect-video w-full bg-black">
                      <iframe
                        src={resource.embedUrl!}
                        title={resource.title}
                        className="w-full h-full border-0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                      />
                    </div>
                  ) : isIframeOpen ? (
                    /* Web page Iframe embed */
                    <div className="relative aspect-video w-full bg-zinc-950 border-b border-zinc-800">
                      <iframe
                        src={resource.url}
                        title={resource.title}
                        className="w-full h-full border-0"
                        sandbox="allow-same-origin allow-scripts allow-popups"
                      />
                    </div>
                  ) : null}

                  {/* Card Details */}
                  <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between">
                    <div>
                      {/* Top Meta: Type icon & Badges */}
                      <div className="flex items-center justify-between gap-2 mb-2.5">
                        <div className="flex items-center gap-1.5">
                          <div className="p-1.5 rounded-lg bg-zinc-900 border border-zinc-800">
                            {getTypeIcon(resource.type)}
                          </div>
                          <span className="text-[11px] font-semibold text-zinc-400 capitalize">
                            {resource.type}
                          </span>
                          <span className="text-zinc-600">·</span>
                          <span className="text-[11px] text-zinc-500 font-mono">
                            {getDomain(resource.url)}
                          </span>
                        </div>

                        {phaseName ? (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-500/10 text-blue-300 border border-blue-500/20 truncate max-w-[180px]">
                            {phaseName}
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-zinc-800 text-zinc-400 border border-zinc-700">
                            Repo General
                          </span>
                        )}
                      </div>

                      {/* Title */}
                      <h4 className="text-sm font-bold text-white mb-2 leading-snug">
                        {resource.title}
                      </h4>

                      {/* Description */}
                      {resource.description && (
                        <p className="text-xs text-zinc-400 mb-3 line-clamp-3 leading-relaxed">
                          {resource.description}
                        </p>
                      )}

                      {/* Tags */}
                      {resource.tags && (
                        <div className="flex flex-wrap gap-1.5 mb-4">
                          {resource.tags.split(',').map((tag) => (
                            <span
                              key={tag.trim()}
                              className="px-2 py-0.5 rounded-md text-[10px] bg-zinc-900 border border-zinc-800 text-zinc-400"
                            >
                              #{tag.trim()}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Bottom Action Footer */}
                    <div className="pt-3 border-t border-zinc-800/80 flex items-center justify-between gap-2 text-xs">
                      <div className="flex items-center gap-2">
                        <a
                          href={resource.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-zinc-800 hover:bg-zinc-750 border border-zinc-700 transition inline-flex items-center gap-1.5"
                        >
                          <ExternalLink className="w-3.5 h-3.5 text-zinc-400" />
                          <span>Open Link</span>
                        </a>

                        {!isYouTube && (
                          <button
                            onClick={() =>
                              setExpandedIframeId(isIframeOpen ? null : resource.id)
                            }
                            className="px-2.5 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 transition inline-flex items-center gap-1"
                          >
                            {isIframeOpen ? (
                              <>
                                <Minimize2 className="w-3 h-3" />
                                <span>Collapse</span>
                              </>
                            ) : (
                              <>
                                <Maximize2 className="w-3 h-3" />
                                <span>Preview</span>
                              </>
                            )}
                          </button>
                        )}
                      </div>

                      <button
                        onClick={() => {
                          if (confirm(`Remove "${resource.title}"?`)) {
                            onDeleteResource(resource.id)
                          }
                        }}
                        className="p-1.5 rounded-lg text-zinc-500 hover:text-rose-400 hover:bg-rose-500/10 transition"
                        title="Delete resource"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
