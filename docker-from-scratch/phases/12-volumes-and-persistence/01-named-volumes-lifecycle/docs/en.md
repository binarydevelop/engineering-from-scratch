# Lesson 12.1: Volumes and Persistence

## Motto
"The lifecycle of a container must never be the lifecycle of your data."

## Problem
A junior backend engineer deploys a PostgreSQL container. Over three months, users create accounts, place orders, and store documents.
One night, an automated deployment script runs `docker rm -f postgres-app && docker run -d --name postgres-app postgres:16`.
The application boots up completely empty. All database tables and user data have evaporated.
Why? Because by default, databases write their files to the container's ephemeral writable layer (`upperdir`).
How do we separate the ephemeral lifecycle of processes from the persistent lifecycle of data?

## Prediction
1. If you write a file to `/data` inside a container and run `docker rm`, where does the file go?
2. Does creating a named volume with `docker volume create` allocate disk space immediately?
3. If two containers mount the same named volume at the same time, can they read each other's writes?

## Why this matters
Stateless applications (web servers, workers, proxies) can be destroyed and replaced in milliseconds. But stateful systems (PostgreSQL, MySQL, Redis, Kafka, Elasticsearch) require strict data durability guarantees. Confusing container storage with persistent volumes is the #1 cause of catastrophic data loss in cloud environments.

## First principles
1. **Separation of Lifecycles**:
   ```text
   Container Lifecycle: [Created] ──► [Running] ──► [Exited] ──► [Destroyed (Deleted)]
                                                                         ▲
   Data Lifecycle:      [======== PERSISTENT VOLUME STORAGE ============]│
                        (Survives reboots, upgrades, and container deletion)
   ```
2. **Named Volumes**:
   - Managed directories created by Docker Engine inside `/var/lib/docker/volumes/<name>/_data` on the host/VM filesystem.
   - When a volume is mounted into a container (e.g. `-v my-vol:/data`), Docker bypasses the union filesystem (`overlay2`) and mounts the host directory directly into the container's Mount namespace using a kernel bind mount.
   - Writes to a volume achieve full native filesystem I/O performance with zero Copy-on-Write overhead!

## Mental model

```text
HOST MACHINE / DOCKER ENGINE STORAGE:
┌────────────────────────────────────────────────────────┐
│  /var/lib/docker/volumes/dfs-data-vol/_data            │
│  ├── state.json (PERSISTENT ON DISK)                   │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             │ Mount: -v dfs-data-vol:/data
             ▼                           ▼
┌──────────────────────────┐ ┌──────────────────────────┐
│ Container 1 (dfs-vol-c1) │ │ Container 2 (dfs-vol-c2) │
│ - Writes state.json      │ │ - Reads state.json       │
│ - DESTROYED!             │ │ - (Created 1 hour later) │
└──────────────────────────┘ └──────────────────────────┘
```

## Build it
Review [state_recorder.py](../code/state_recorder.py).
It writes and reads JSON transaction records to `/data/state.json`.

## Run it
Execute the experiment runner:

```bash
./phases/12-volumes-and-persistence/01-named-volumes-lifecycle/experiments/run_experiment.sh
```

## Inspect it
1. Run `docker volume ls`.
2. Inspect the volume details:
   ```bash
   docker volume inspect dfs-data-vol
   ```
   Notice `Mountpoint: /var/lib/docker/volumes/dfs-data-vol/_data`.
3. Verify that `dfs-vol-c2` successfully reads the transactions written by `dfs-vol-c1`.

## Break it
Run `docker volume rm dfs-data-vol` while a container is actively using it:
```bash
docker run -d --name dfs-hold -v dfs-data-vol:/data alpine:latest sleep 60
docker volume rm dfs-data-vol
```
Docker rejects this immediately:
`Error response from daemon: remove dfs-data-vol: volume is in use - [container-id]`
Docker Engine guards active volumes against accidental deletion.
Clean up:
```bash
docker rm -f dfs-hold
docker volume rm dfs-data-vol
```

## Debug it
When persistent data appears to be missing after container restart:
1. Run `docker inspect <container> --format '{{json .Mounts}}'`.
2. Verify:
   - Is `Type` equal to `volume`?
   - Is `Destination` pointing to the exact folder the database writes to (e.g. `/var/lib/postgresql/data` for Postgres)?
   - If `Destination` is misspelled (e.g. `/var/lib/postgres/data`), Postgres will write to the ephemeral layer and data will vanish on `rm`!

## Modify it
Mount the volume as read-only by adding `:ro`:
```bash
docker run --rm -v dfs-data-vol:/data:ro python:3.11-slim python3 /state_recorder.py write "Test"
```
Observe that the write fails with `Read-only file system`!

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Evidence of data loss in Part 1.
- Evidence of data persistence in Part 2.
- The host mountpoint path reported by `docker volume inspect`.

## Questions for mastery
1. Why does writing to a volume have higher I/O performance than writing to the container root filesystem?
2. What happens to orphaned volumes when you remove containers with `docker rm` without the `-v` flag?
3. How do you backup or migrate the data inside a named volume?

## What comes next
Named volumes are isolated inside Docker's internal directories. What if we want to mount our local host code directory into a container for live development? Proceed to **Phase 13: Bind Mounts and Development Workflows**.
