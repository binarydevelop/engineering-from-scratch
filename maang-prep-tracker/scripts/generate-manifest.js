const fs = require('fs')
const path = require('path')

// Determine parent dir: if run inside maang-prep-tracker, parent is '..'
let rootDir = path.resolve(__dirname, '..', '..')
if (!fs.existsSync(path.join(rootDir, 'operating-systems-from-scratch'))) {
  rootDir = path.resolve(__dirname, '..')
}

const outputPath = path.resolve(__dirname, '..', 'src', 'data', 'repos-manifest.json')

const REPOS = [
  'ai-engineering-from-scratch',
  'ai-systems-from-scratch',
  'aws-from-scratch',
  'backend-engineering-from-scratch',
  'ci-cd-and-software-delivery-from-scratch',
  'computer-networking-from-scratch',
  'data-engineering-from-scratch',
  'data-structures-algorithms-practice',
  'database-and-sql-from-scratch',
  'docker-from-scratch',
  'elasticsearch-from-scratch',
  'java-from-scratch',
  'kafka-from-scratch',
  'kubernetes-from-scratch',
  'linux-from-scratch',
  'low-level-design-from-scratch',
  'nosql-databases-and-query-languages-from-scratch',
  'olap-databases-and-analytical-querying-from-scratch',
  'operating-systems-from-scratch',
  'production-sre-observability-platform-engineering-from-scratch',
  'redis-from-scratch',
  'staff-engineering-and-product-mindset-from-scratch',
  'system-design-from-scratch',
]

function formatTitle(str) {
  return str
    .replace(/\.md$/, '')
    .replace(/^[0-9]+[_\.\-]/, '')
    .replace(/[-_]/g, ' ')
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

const manifest = []

for (const repoId of REPOS) {
  const repoDir = path.join(rootDir, repoId)
  if (!fs.existsSync(repoDir)) continue

  const hasReadme = fs.existsSync(path.join(repoDir, 'README.md'))
  const hasRoadmap = fs.existsSync(path.join(repoDir, 'ROADMAP.md'))

  // Root notes
  const rootNotes = []
  const rootNotesDir = path.join(repoDir, 'notes')
  if (fs.existsSync(rootNotesDir)) {
    const files = fs.readdirSync(rootNotesDir)
    for (const f of files) {
      if (f.endsWith('.md') && !f.startsWith('.')) {
        rootNotes.push({
          filename: f,
          path: `notes/${f}`,
          title: formatTitle(f),
        })
      }
    }
  }

  // Phases
  const phasesDir = path.join(repoDir, 'phases')
  const phases = []

  if (fs.existsSync(phasesDir)) {
    const entries = fs.readdirSync(phasesDir)
    const sortedEntries = entries
      .filter((e) => !e.startsWith('.') && fs.statSync(path.join(phasesDir, e)).isDirectory())
      .sort((a, b) => {
        const numA = parseInt(a.match(/\d+/)?.[0] || '0', 10)
        const numB = parseInt(b.match(/\d+/)?.[0] || '0', 10)
        return numA - numB
      })

    for (const p of sortedEntries) {
      const pDir = path.join(phasesDir, p)
      const hasEnDoc = fs.existsSync(path.join(pDir, 'docs', 'en.md'))
      const hasPhaseReadme = fs.existsSync(path.join(pDir, 'README.md'))
      const hasDoc = hasEnDoc || hasPhaseReadme
      const docPath = hasEnDoc ? `phases/${p}/docs/en.md` : (hasPhaseReadme ? `phases/${p}/README.md` : null)

      // Notes
      const notesDir = path.join(pDir, 'notes')
      const notes = []
      if (fs.existsSync(notesDir)) {
        const nfList = fs.readdirSync(notesDir)
        for (const nf of nfList) {
          if (nf.endsWith('.md') && !nf.startsWith('.')) {
            notes.push({
              filename: nf,
              path: `phases/${p}/notes/${nf}`,
              title: formatTitle(nf),
            })
          }
        }
      }

      // Code
      const codeDir = path.join(pDir, 'code')
      const codeFiles = []
      if (fs.existsSync(codeDir)) {
        const cfList = fs.readdirSync(codeDir)
        for (const cf of cfList) {
          if (!cf.startsWith('.') && fs.statSync(path.join(codeDir, cf)).isFile()) {
            codeFiles.push({
              filename: cf,
              path: `phases/${p}/code/${cf}`,
            })
          }
        }
      }

      phases.push({
        id: p,
        name: formatTitle(p),
        hasDoc,
        docPath,
        notes,
        codeFiles,
      })
    }
  }

  manifest.push({
    id: repoId,
    name: formatTitle(repoId),
    phaseCount: phases.length,
    hasPhases: phases.length > 0,
    hasReadme,
    hasRoadmap,
    rootNotes,
    phases,
  })
}

fs.writeFileSync(outputPath, JSON.stringify(manifest, null, 2))
console.log(`Generated manifest with ${manifest.length} repos at ${outputPath}`)
