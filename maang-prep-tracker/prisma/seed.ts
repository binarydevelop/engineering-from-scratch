import { PrismaClient } from '@prisma/client'
import fs from 'fs'
import path from 'path'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 Starting seed...')

  const tasksFilePath = path.join(__dirname, '../src/data/initial-tasks.json')
  const rawData = fs.readFileSync(tasksFilePath, 'utf-8')
  const tasks = JSON.parse(rawData)

  console.log(`Found ${tasks.length} tasks to seed.`)

  // Clear existing tasks to ensure clean slate if re-seeding
  const deleted = await prisma.task.deleteMany({})
  console.log(`Cleared ${deleted.count} existing tasks.`)

  // Batch insert all 191 tasks
  const created = await prisma.task.createMany({
    data: tasks,
  })

  console.log(`✅ Successfully seeded ${created.count} tasks!`)
}

main()
  .catch((e) => {
    console.error('❌ Error during seeding:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
