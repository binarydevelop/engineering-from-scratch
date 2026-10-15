# ⚡ MAANG 2027 Staff Tracker Web App

A high-performance, full-stack Next.js web application designed to track, update, and manage your 27-week MAANG Senior & Staff interview preparation schedule. Pre-seeded with all **191 structured daily sessions** starting **Saturday, October 17, 2026**.

![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)
![Prisma](https://img.shields.io/badge/Prisma-6-darkblue?style=flat-square&logo=prisma)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-cyan?style=flat-square&logo=tailwind-css)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?style=flat-square&logo=postgresql)

---

## ✨ Features

- **Full Database CRUD**:
  - **Create**: Add custom study sessions, mock interviews, or extra revision days.
  - **Read**: Live search across topics, filters by Sprint (1 to 7), Week, Status (`To Do`, `In Progress`, `Done`), and Priority (`Critical`, `High`, `Medium`).
  - **Update**: One-click status toggling (`To Do` → `In Progress` → `Done`), priority editing, and rich personal review notes.
  - **Delete**: Safe deletion of any task with confirmation modal.
  - **Self-Seeding & Reset**: Auto-populates all 191 schedule items on a fresh database; one-click "Reset / Re-seed" button anytime.
- **3 Interactive Views**:
  - 📋 **Timeline View**: Grouped by week with expandable session breakdowns (Morning 6–10 AM, Evening 7–10 PM, Striver DSA chip, priority badge).
  - 📌 **Kanban Board**: 3-column workflow (`To Do`, `In Progress`, `Completed`) with rapid advance buttons.
  - 🗓️ **191-Day Matrix**: Bird's-eye overview of the entire 27-week journey with color-coded status cells.
- **Study Rhythm Architecture**:
  - **Weekdays**: 6:00–10:00 AM (DSA + Domain A) + 7:00–10:00 PM (Domain B + Practice) = **7 hrs/day**
  - **Weekends**: 6:00 AM–4:00 PM + 7:00–10:00 PM = **~10 hrs/day** (Revision blocks, LLD/SD Mocks, STAR behavioral stories)
- **Zero-Friction Vercel Deployment**: Serverless PostgreSQL compatibility (Neon, Supabase, Vercel Postgres, Railway) with automated Prisma client generation.

---

## 🚀 One-Click Deployment to Vercel

### Step 1: Push to GitHub
If you haven't already initialized git:
```bash
git init
git add .
git commit -m "Initial commit of MAANG Prep Tracker"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

### Step 2: Deploy on Vercel
1. Go to [vercel.com](https://vercel.com) and click **"Add New Project"** → Import your GitHub repository.
2. In Project Settings, add a **PostgreSQL Database**:
   - You can use **Vercel Postgres**, **Neon** (free tier at [neon.tech](https://neon.tech)), or **Supabase** (free tier at [supabase.com](https://supabase.com)).
3. Add the environment variable:
   - Key: `DATABASE_URL`
   - Value: `postgresql://user:password@host/dbname?sslmode=require`
4. Click **Deploy**!

### Step 3: Initialize Database Schema
Run this once from your terminal to sync the schema to your remote database:
```bash
DATABASE_URL="your-remote-postgres-connection-string" npx prisma db push
```
*(Note: If the database is empty when the deployed app first opens, the API will automatically seed all 191 tasks on initial load!)*

---

## 💻 Local Development Setup

### 1. Prerequisites
- Node.js 18+ (tested on Node 20 / 22 / 24 / 26)
- Local PostgreSQL instance (or free remote DB)

### 2. Install Dependencies
```bash
npm install
```

### 3. Setup Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Ensure your `DATABASE_URL` is set:
```env
DATABASE_URL="postgresql://user@localhost:5432/maang_tracker"
```

### 4. Push Schema & Seed
```bash
# Push Prisma schema to create the Task table
npx prisma db push

# Seed the 191 schedule items
npm run seed
```

### 5. Start Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📊 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/tasks` | `GET` | List all tasks with optional search, sprint, week, status, and priority query filters (auto-seeds if empty) |
| `/api/tasks` | `POST` | Create a new task |
| `/api/tasks/[id]` | `PATCH` | Update task fields (status, priority, notes, sessions, etc.) |
| `/api/tasks/[id]` | `DELETE` | Permanently delete a task |
| `/api/stats` | `GET` | Aggregated statistics, sprint completion percentages, next upcoming task |
| `/api/seed` | `POST` | Re-seed/reset database with all 191 original tasks |

---

## 🗺️ Roadmap Architecture (Oct 17, 2026 – May 2027)

- **Sprint 1 (Weeks 1–4)**: Foundations Blitz — OS, Linux, Networking, SQL, Java Core, Striver Steps 1–5
- **Sprint 2 (Weeks 5–8)**: Backend Engineering Core — Java Concurrency, Redis, Kafka, Docker, Striver Steps 6–8
- **Sprint 3 (Weeks 9–13)**: Low-Level Design (LLD) Mastery — 20+ Real-world design patterns, Capstones, Striver Steps 9–12
- **Sprint 4 (Weeks 14–17)**: System Design Foundations — Distributed Systems, Storage, K8s, Elasticsearch, Striver Steps 13–14
- **Sprint 5 (Weeks 18–20)**: SD Interview Mode + Infrastructure — Observability, Cloud, Security, Mocks, Striver Steps 15–16
- **Sprint 6 (Weeks 21–24)**: Advanced Differentiation Track — High Throughput, io_uring, eBPF, NewSQL, Striver Step 17–18
- **Sprint 7 (Weeks 25–28)**: Staff Engineering & Behavioral Polish — System Design Speedrun, STAR Stories, Offer Strategy
