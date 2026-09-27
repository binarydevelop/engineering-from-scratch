# Lesson 23.1: Compose Volumes and Persistent State

## Motto
"`docker compose down` removes containers and networks; adding `-v` destroys all your persistent volumes and database disks."

## Problem
A developer is testing database migrations on their machine.
They want to restart the project fresh, so they search online and find the command:
`docker compose down -v && docker compose up`
They run it on a staging or test server, and suddenly all uploaded user avatars, PostgreSQL database tables, and Redis cache keys are completely erased.
Why did `-v` delete everything? What is the difference between `docker compose down` and `docker compose down -v`?

## Prediction
1. If you run `docker compose down`, does Compose delete your named volumes by default?
2. How does Compose name named volumes on disk? (Does it prefix them with the project name?)
3. What exact flag must you add to `docker compose down` to intentionally delete all persistent volumes?

## Why this matters
The `-v` (or `--volumes`) flag is an irreversible destructive command. Many CI scripts, documentation guides, and junior engineers blindly add `-v` to clean up without realizing that `-v` means "delete all attached stateful disks". Knowing the boundary between container cleanup and storage destruction prevents catastrophic data loss incidents.

## First principles
1. **The Safe Shutdown (`docker compose down`)**:
   - Stops all running service containers gracefully (sending `SIGTERM`).
   - Removes stopped service containers (`docker rm`).
   - Removes user-defined networks created for this project (`docker network rm`).
   - **PRESERVES ALL VOLUMES INTACT ON DISK!**
2. **The Destructive Wipe (`docker compose down -v`)**:
   - Executes everything in `down`.
   - **ALSO** calls `docker volume rm` on every named volume declared in the `volumes:` section of the compose file!
3. **Project Namespace Scoping**:
   Compose scopes volumes by project name:
   `volumes: { db-data: }` in project `my-app` becomes `my-app_db-data` in `/var/lib/docker/volumes/`.

## Mental model

```text
COMPOSE PROJECT STATE:
┌────────────────────────────────────────────────────────────────────────┐
│  Containers:  my-app-database-1, my-app-api-1                          │
│  Networks:    my-app_default                                           │
│  Volumes:     my-app_db-data (Stores PostgreSQL database files)        │
└────────────────────────────────────────────────────────────────────────┘

COMMAND EXECUTION CONSEQUENCES:

$ docker compose down
┌───────────────────────────────────────┐
│ Containers: REMOVED                   │
│ Networks:   REMOVED                   │
│ Volumes:    PRESERVED! (Data intact)  │ ◄── Safe routine shutdown
└───────────────────────────────────────┘

$ docker compose down -v
┌───────────────────────────────────────┐
│ Containers: REMOVED                   │
│ Networks:   REMOVED                   │
│ Volumes:    PERMANENTLY DESTROYED!    │ ◄── DESTRUCTIVE WIPE!
└───────────────────────────────────────┘
```

## Build it
Review `compose.yaml` in `code/`.
It configures PostgreSQL with named volume `db-data`.

## Run it
Execute the experiment runner:

```bash
./phases/23-compose-volumes-and-persistent-state/01-compose-state-lifecycle/experiments/run_experiment.sh
```

## Inspect it
1. Observe Step 2: The `users` table is created and populated with Alice and Bob.
2. In Step 3: `docker compose down` removes the container and network, but `docker volume ls` confirms `dfs-volume-lifecycle_db-data` still exists.
3. In Step 4: Relaunching with `docker compose up -d` queries the database and verifies that Alice and Bob are still there.
4. In Step 5: `docker compose down -v` explicitly removes the volume.
5. In Step 6: Relaunching results in `ERROR: relation "users" does not exist`, proving that the state was completely wiped.

## Break it
Simulate an accidental volume wipe:
Run `docker compose down -v` on a project where you intended to keep database state.
Notice that Docker prompts for no confirmation; the data is deleted immediately from disk.

## Debug it
When you want to inspect what is stored inside a named volume without starting your entire Compose stack:
```bash
docker run --rm -v dfs-volume-lifecycle_db-data:/data alpine:latest ls -la /data
```
This mounts the volume into a temporary Alpine container and lets you inspect raw files.

## Modify it
Mark a volume as `external: true` in `compose.yaml`:
```yaml
volumes:
  db-data:
    external: true
```
Notice that when a volume is marked `external: true`, `docker compose down -v` will **refuse to delete it**, protecting critical databases against accidental deletion!

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Verification that data survived `docker compose down`.
- Output showing volume deletion after `docker compose down -v`.
- The PostgreSQL error confirming database state was wiped.

## Questions for mastery
1. Why is `external: true` recommended for production database volumes in Compose?
2. If you change a volume name in `compose.yaml`, what happens to the data in the previous volume?
3. How can you migrate data from an old Compose volume to a new one?

## What comes next
We now understand both single-container primitives and multi-container Compose orchestration.
Now: When things break in production, how do you debug them systematically?
Proceed to **Phase 24: Debugging Containers**.
