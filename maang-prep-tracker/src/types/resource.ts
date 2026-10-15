export interface Resource {
  id: string
  repoId: string
  phaseId?: string | null
  title: string
  url: string
  type: 'youtube' | 'article' | 'doc' | 'interactive' | 'embed' | string
  embedUrl?: string | null
  description?: string
  tags?: string
  createdAt?: string | Date
  updatedAt?: string | Date
}

export function getYouTubeEmbedUrl(url: string): string | null {
  try {
    const trimmed = url.trim()
    if (!trimmed) return null

    // Check if already an embed URL
    if (trimmed.includes('youtube.com/embed/')) {
      return trimmed
    }

    // Handle youtu.be/<id>
    if (trimmed.includes('youtu.be/')) {
      const match = trimmed.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/)
      if (match && match[1]) {
        return `https://www.youtube-nocookie.com/embed/${match[1]}`
      }
    }

    // Handle youtube.com/watch?v=<id>
    if (trimmed.includes('youtube.com/watch')) {
      const parsed = new URL(trimmed)
      const v = parsed.searchParams.get('v')
      if (v) {
        return `https://www.youtube-nocookie.com/embed/${v}`
      }
    }

    // Handle youtube.com/shorts/<id>
    if (trimmed.includes('youtube.com/shorts/')) {
      const match = trimmed.match(/shorts\/([a-zA-Z0-9_-]{11})/)
      if (match && match[1]) {
        return `https://www.youtube-nocookie.com/embed/${match[1]}`
      }
    }
  } catch {}
  return null
}
