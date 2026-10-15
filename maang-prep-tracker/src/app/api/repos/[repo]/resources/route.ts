import { NextRequest, NextResponse } from 'next/server'
import { fetchResources, createResource, deleteResource } from '@/lib/db'
import { getYouTubeEmbedUrl } from '@/types/resource'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ repo: string }> }
) {
  try {
    const { repo } = await params
    const searchParams = request.nextUrl.searchParams
    const phaseId = searchParams.get('phaseId')

    const { resources, hasDb } = await fetchResources(repo, phaseId)
    return NextResponse.json({ success: true, hasDb, resources })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error fetching resources:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to fetch resources' },
      { status: 500 }
    )
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ repo: string }> }
) {
  try {
    const { repo } = await params
    const body = await request.json()
    const { title, url, type = 'article', phaseId = null, description = '', tags = '' } = body

    if (!title || !url) {
      return NextResponse.json(
        { success: false, error: 'Title and URL are required' },
        { status: 400 }
      )
    }

    let embedUrl = body.embedUrl || null
    if (type === 'youtube' || url.includes('youtube.com') || url.includes('youtu.be')) {
      embedUrl = getYouTubeEmbedUrl(url) || embedUrl
    }

    const { resource, hasDb } = await createResource({
      repoId: repo,
      phaseId: phaseId || null,
      title,
      url,
      type: type || (embedUrl ? 'youtube' : 'article'),
      embedUrl,
      description,
      tags,
    })

    return NextResponse.json({ success: true, hasDb, resource }, { status: 201 })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error creating resource:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to create resource' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ repo: string }> }
) {
  try {
    await params
    const searchParams = request.nextUrl.searchParams
    const id = searchParams.get('id')

    if (!id) {
      return NextResponse.json({ success: false, error: 'Resource id is required' }, { status: 400 })
    }

    const { success, hasDb } = await deleteResource(id)
    return NextResponse.json({ success, hasDb, message: 'Resource deleted successfully' })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error deleting resource:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to delete resource' },
      { status: 500 }
    )
  }
}
