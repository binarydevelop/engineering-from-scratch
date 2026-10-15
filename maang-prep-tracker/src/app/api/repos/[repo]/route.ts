import { NextRequest, NextResponse } from 'next/server'
import manifest from '@/data/repos-manifest.json'
import fs from 'fs'
import path from 'path'

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

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ repo: string }> }
) {
  try {
    const { repo } = await params
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

    let phases: PhaseDetail[] = repoData.phases
    let rootNotes: NoteItem[] = repoData.rootNotes

    if (isLocal) {
      try {
        const phasesDir = path.join(localRepoDir, 'phases')
        if (fs.existsSync(phasesDir)) {
          const scannedPhases: PhaseDetail[] = fs.readdirSync(phasesDir)
            .filter((p) => !p.startsWith('.') && fs.statSync(path.join(phasesDir, p)).isDirectory())
            .sort()
            .map((p) => {
              const pDir = path.join(phasesDir, p)
              const hasDoc = fs.existsSync(path.join(pDir, 'docs/en.md')) || fs.existsSync(path.join(pDir, 'README.md'))
              const docPath = fs.existsSync(path.join(pDir, 'docs/en.md'))
                ? `phases/${p}/docs/en.md`
                : (fs.existsSync(path.join(pDir, 'README.md')) ? `phases/${p}/README.md` : null)

              const notesDir = path.join(pDir, 'notes')
              const notes: NoteItem[] = []
              if (fs.existsSync(notesDir)) {
                for (const nf of fs.readdirSync(notesDir)) {
                  if (nf.endsWith('.md') && !nf.startsWith('.')) {
                    notes.push({
                      filename: nf,
                      path: `phases/${p}/notes/${nf}`,
                      title: nf.replace('.md', '').replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
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
                name: p.replace(/^phase-/, '').replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
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
          rootNotes = fs.readdirSync(rootNotesDir)
            .filter((nf) => nf.endsWith('.md') && !nf.startsWith('.'))
            .map((nf) => ({
              filename: nf,
              path: `notes/${nf}`,
              title: nf.replace('.md', '').replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
            }))
        }
      } catch (e) {
        console.warn('Could not read local filesystem, using manifest:', e)
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
