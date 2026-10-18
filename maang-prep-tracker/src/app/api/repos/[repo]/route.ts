import { NextRequest, NextResponse } from 'next/server'
import manifest from '@/data/repos-manifest.json'
import fs from 'fs'
import path from 'path'

const GITHUB_OWNER = 'binarydevelop'
const GITHUB_REPO = 'engineering-from-scratch'
const GITHUB_BRANCH = 'main'

interface NoteItem {
  filename: string
  path: string
  title: string
}

interface CodeItem {
  filename: string
  path: string
}

interface PhaseDetail {
  id: string
  name: string
  hasDoc: boolean
  docPath: string | null
  notes: NoteItem[]
  codeFiles: CodeItem[]
}

interface RepoData {
  id: string
  name: string
  phaseCount: number
  hasPhases: boolean
  hasReadme: boolean
  hasRoadmap: boolean
  rootNotes: NoteItem[]
  phases: PhaseDetail[]
}

function formatTitle(str: string): string {
  return str
    .replace(/\.md$/, '')
    .replace(/^[0-9]+[_\.\-]/, '')
    .replace(/[-_]/g, ' ')
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ repo: string }> }
) {
  try {
    const { repo } = await params
    const searchParams = request.nextUrl.searchParams
    const targetPhaseId = searchParams.get('phaseId')
    const shouldSync = searchParams.get('sync') === 'true'

    const typedManifest = manifest as unknown as RepoData[]
    const repoData = typedManifest.find((r) => r.id === repo)

    if (!repoData) {
      return NextResponse.json(
        { success: false, error: `Repository ${repo} not found` },
        { status: 404 }
      )
    }

    const parentDir = path.resolve(process.cwd(), '..')
    const localRepoDir = path.join(parentDir, repo)
    const isLocal = fs.existsSync(localRepoDir)

    // Deep clone phases so runtime modifications do not mutate cached modules
    let phases: PhaseDetail[] = JSON.parse(JSON.stringify(repoData.phases))
    let rootNotes: NoteItem[] = JSON.parse(JSON.stringify(repoData.rootNotes || []))

    // 1. If running locally on user's machine, scan filesystem directly
    if (isLocal) {
      try {
        const phasesDir = path.join(localRepoDir, 'phases')
        if (fs.existsSync(phasesDir)) {
          const scannedPhases: PhaseDetail[] = fs
            .readdirSync(phasesDir)
            .filter((p) => !p.startsWith('.') && fs.statSync(path.join(phasesDir, p)).isDirectory())
            .sort((a, b) => {
              const numA = parseInt(a.match(/\d+/)?.[0] || '0', 10)
              const numB = parseInt(b.match(/\d+/)?.[0] || '0', 10)
              return numA - numB
            })
            .map((p) => {
              const pDir = path.join(phasesDir, p)
              const hasEnDoc = fs.existsSync(path.join(pDir, 'docs/en.md'))
              const hasPhaseReadme = fs.existsSync(path.join(pDir, 'README.md'))
              const hasDoc = hasEnDoc || hasPhaseReadme
              const docPath = hasEnDoc
                ? `phases/${p}/docs/en.md`
                : hasPhaseReadme
                ? `phases/${p}/README.md`
                : null

              const notesDir = path.join(pDir, 'notes')
              const notes: NoteItem[] = []
              if (fs.existsSync(notesDir)) {
                for (const nf of fs.readdirSync(notesDir)) {
                  if (nf.endsWith('.md') && !nf.startsWith('.')) {
                    notes.push({
                      filename: nf,
                      path: `phases/${p}/notes/${nf}`,
                      title: formatTitle(nf),
                    })
                  }
                }
              }

              const codeDir = path.join(pDir, 'code')
              const codeFiles: CodeItem[] = []
              if (fs.existsSync(codeDir)) {
                for (const cf of fs.readdirSync(codeDir)) {
                  if (!cf.startsWith('.') && fs.statSync(path.join(codeDir, cf)).isFile()) {
                    codeFiles.push({
                      filename: cf,
                      path: `phases/${p}/code/${cf}`,
                    })
                  }
                }
              }

              return {
                id: p,
                name: formatTitle(p),
                hasDoc,
                docPath,
                notes,
                codeFiles,
              }
            })

          if (scannedPhases.length > 0) {
            phases = scannedPhases
          }
        }

        const rootNotesDir = path.join(localRepoDir, 'notes')
        if (fs.existsSync(rootNotesDir)) {
          rootNotes = fs
            .readdirSync(rootNotesDir)
            .filter((nf) => nf.endsWith('.md') && !nf.startsWith('.'))
            .map((nf) => ({
              filename: nf,
              path: `notes/${nf}`,
              title: formatTitle(nf),
            }))
        }
      } catch (e) {
        console.warn('Could not read local filesystem, using manifest:', e)
      }
    }

    // 2. On Vercel / Cloud: Live GitHub API sync when a phase is viewed or sync requested
    if (!isLocal && (targetPhaseId || shouldSync)) {
      try {
        const targetPhasesToSync = targetPhaseId
          ? [targetPhaseId]
          : phases.slice(0, 5).map((p) => p.id)

        const apiHeaders: Record<string, string> = {
          Accept: 'application/vnd.github.v3+json',
          'User-Agent': 'MAANG-Prep-Tracker',
        }
        const token = process.env.GITHUB_TOKEN || request.headers.get('x-github-token')
        if (token) apiHeaders['Authorization'] = `token ${token}`

        await Promise.all(
          targetPhasesToSync.map(async (pId) => {
            const notesUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${repo}/phases/${pId}/notes?ref=${GITHUB_BRANCH}`
            const res = await fetch(notesUrl, {
              headers: apiHeaders,
              cache: 'no-store',
            })

            if (res.ok) {
              const items = await res.json()
              if (Array.isArray(items)) {
                const liveNotes: NoteItem[] = items
                  .filter((f) => f.name.endsWith('.md') && !f.name.startsWith('.'))
                  .map((f) => ({
                    filename: f.name,
                    path: `phases/${pId}/notes/${f.name}`,
                    title: formatTitle(f.name),
                  }))

                const targetPhaseObj = phases.find((p) => p.id === pId)
                if (targetPhaseObj) {
                  targetPhaseObj.notes = liveNotes
                }
              }
            }
          })
        )
      } catch (err) {
        console.warn('Failed to fetch live notes from GitHub API:', err)
      }
    }

    return NextResponse.json({
      success: true,
      repo: {
        id: repoData.id,
        name: repoData.name,
        phaseCount: phases.length,
        hasPhases: phases.length > 0,
        hasReadme: repoData.hasReadme,
        hasRoadmap: repoData.hasRoadmap,
        rootNotes,
        phases,
        isLocal,
      },
    })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error fetching repo detail:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to fetch repo' },
      { status: 500 }
    )
  }
}
