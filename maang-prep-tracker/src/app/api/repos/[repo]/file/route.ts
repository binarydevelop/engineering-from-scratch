import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'
import { exec } from 'child_process'
import { promisify } from 'util'

const execPromise = promisify(exec)

const GITHUB_OWNER = 'binarydevelop'
const GITHUB_REPO = 'engineering-from-scratch'
const GITHUB_BRANCH = 'main'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ repo: string }> }
) {
  try {
    const { repo } = await params
    const { searchParams } = new URL(request.url)
    const filePath = searchParams.get('path')

    if (!filePath) {
      return NextResponse.json(
        { success: false, error: 'Query parameter "path" is required' },
        { status: 400 }
      )
    }

    // 1. Try reading from local filesystem first
    const parentDir = path.resolve(process.cwd(), '..')
    const localFilePath = path.join(parentDir, repo, filePath)

    if (fs.existsSync(localFilePath)) {
      const content = fs.readFileSync(localFilePath, 'utf-8')
      return NextResponse.json({
        success: true,
        source: 'local',
        repo,
        path: filePath,
        content,
      })
    }

    // 2. Fallback to GitHub raw content (for Vercel deployment)
    const githubRawUrl = `https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}/${repo}/${filePath}`
    const headers: Record<string, string> = {}
    const token = process.env.GITHUB_TOKEN || request.headers.get('x-github-token')
    if (token) {
      headers['Authorization'] = `token ${token}`
    }

    const githubRes = await fetch(githubRawUrl, { headers })
    if (githubRes.ok) {
      const content = await githubRes.text()
      return NextResponse.json({
        success: true,
        source: 'github',
        repo,
        path: filePath,
        content,
      })
    }

    return NextResponse.json(
      { success: false, error: `File not found at ${repo}/${filePath}` },
      { status: 404 }
    )
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error reading file:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to read file' },
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
    const { filePath, content, commitMessage, pushToGit = true } = body

    if (!filePath || content === undefined) {
      return NextResponse.json(
        { success: false, error: 'filePath and content are required' },
        { status: 400 }
      )
    }

    const parentDir = path.resolve(process.cwd(), '..')
    const localRepoDir = path.join(parentDir, repo)
    const isLocal = fs.existsSync(localRepoDir)

    // Option A: Running locally on machine
    if (isLocal) {
      const targetFilePath = path.join(localRepoDir, filePath)
      const targetDir = path.dirname(targetFilePath)

      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true })
      }

      fs.writeFileSync(targetFilePath, content, 'utf-8')

      let gitCommitted = false
      if (pushToGit) {
        try {
          const msg = commitMessage || `docs(${repo}): update ${filePath}`
          await execPromise(
            `git -C "${parentDir}" add "${repo}/${filePath}" && git -C "${parentDir}" commit -m "${msg.replace(/"/g, '\\"')}"`
          )
          gitCommitted = true
        } catch (gitErr: unknown) {
          console.warn('Git commit skipped or failed:', gitErr)
        }
      }

      return NextResponse.json({
        success: true,
        savedTo: 'local',
        path: filePath,
        gitCommitted,
        message: gitCommitted
          ? 'File saved and committed to git!'
          : 'File saved to disk successfully!',
      })
    }

    // Option B: Running on Vercel -> Commit via GitHub API
    const token = process.env.GITHUB_TOKEN || request.headers.get('x-github-token')
    if (!token) {
      return NextResponse.json(
        {
          success: false,
          error:
            'GitHub Token required to save when running on Vercel. Set GITHUB_TOKEN in Vercel settings or enter your token in the app settings.',
        },
        { status: 401 }
      )
    }

    const apiUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${repo}/${filePath}`

    // Check if file already exists to get its SHA
    let existingSha: string | undefined
    try {
      const getRes = await fetch(apiUrl, {
        headers: {
          Authorization: `token ${token}`,
          Accept: 'application/vnd.github.v3+json',
        },
      })
      if (getRes.ok) {
        const fileInfo = await getRes.json()
        existingSha = fileInfo.sha
      }
    } catch (e) {
      console.warn('Could not check existing SHA:', e)
    }

    const commitPayload = {
      message: commitMessage || `docs(${repo}): update ${filePath} via web GUI`,
      content: Buffer.from(content).toString('base64'),
      branch: GITHUB_BRANCH,
      ...(existingSha ? { sha: existingSha } : {}),
    }

    const putRes = await fetch(apiUrl, {
      method: 'PUT',
      headers: {
        Authorization: `token ${token}`,
        Accept: 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(commitPayload),
    })

    if (!putRes.ok) {
      const errData = await putRes.json()
      throw new Error(errData.message || 'GitHub API commit failed')
    }

    return NextResponse.json({
      success: true,
      savedTo: 'github',
      path: filePath,
      message: 'Successfully committed and pushed directly to GitHub repository!',
    })
  } catch (error: unknown) {
    const err = error as Error
    console.error('Error saving file:', err)
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to save file' },
      { status: 500 }
    )
  }
}
