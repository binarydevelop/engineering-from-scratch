import { NextResponse } from 'next/server'
import manifest from '@/data/repos-manifest.json'
import fs from 'fs'
import path from 'path'

interface PhaseManifest {
  notes?: unknown[]
}

interface RepoManifest {
  id: string
  name: string
  phaseCount: number
  hasPhases: boolean
  hasReadme: boolean
  hasRoadmap: boolean
  rootNotes?: unknown[]
  phases?: PhaseManifest[]
}

export async function GET() {
  try {
    const parentDir = path.resolve(process.cwd(), '..')
    const isLocal = fs.existsSync(path.join(parentDir, 'operating-systems-from-scratch'))

    const typedManifest = manifest as RepoManifest[]

    return NextResponse.json({
      success: true,
      isLocal,
      totalRepos: typedManifest.length,
      repos: typedManifest.map((r) => ({
        id: r.id,
        name: r.name,
        phaseCount: r.phaseCount,
        hasPhases: r.hasPhases,
        hasReadme: r.hasReadme,
        hasRoadmap: r.hasRoadmap,
        totalNotes:
          (r.rootNotes?.length || 0) +
          (r.phases?.reduce((acc: number, p) => acc + (p.notes?.length || 0), 0) || 0),
        rootNotes: r.rootNotes || [],
      })),
    })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error fetching repos:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to fetch repos' },
      { status: 500 }
    )
  }
}
