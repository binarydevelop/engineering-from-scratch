# Lesson 04.1: Containers and Filesystems (The Copy-on-Write Layer)

## Motto
"Images are immutable roots; containers are disposable lenses that record mutations in a temporary upper layer."

## Problem
A common developer pitfall:
1. You run a database or application container.
2. You insert records or write local state into `/data/app.db`.
3. The container stops or you run `docker rm my-app`.
4. You run `docker run my-app` again.
5. All your data has vanished!

Why did the data disappear? Where did it go? And if 5 containers run from `alpine`, why doesn't one container's file appear in another container?

## Prediction
1. If container A creates `/tmp/secret.txt`, will container B started from the same image see `/tmp/secret.txt`?
2. If container A modifies an existing file from the image (e.g., `/etc/hosts`), does the underlying image file change?
3. What happens to files created inside a container when the container is deleted?

## Why this matters
Failing to understand the container's ephemeral writable layer leads to catastrophic data loss in production, bloated containers with massive disk usage, and confusion over why containers cannot share state simply by writing to disk.

## First principles
Docker uses a **Union Filesystem** (most commonly `overlay2` or `overlayfs`).
A union mount merges multiple directories from disk and presents them to the container process as a single coherent filesystem tree:
1. **Lowerdir (Read-Only)**: The immutable image layers stacked in order.
2. **Upperdir (Read-Write)**: A thin, private writable directory created on the host specifically for this container instance.
3. **Mergeddir**: The unified mount view mounted into the container's Mount namespace (`/`).
4. **Copy-on-Write (CoW)**:
   - When a process **reads** a file, the kernel checks `upperdir`. If not found, it falls through to `lowerdir`.
   - When a process **modifies** a file from `lowerdir`, the kernel copies the entire file up to `upperdir` first, then applies the edit. The underlying image layer remains pristine.
   - When a process **deletes** a file from `lowerdir`, the kernel creates a special "whiteout device marker" in `upperdir` that masks the file from view.

When `docker rm` is executed, the daemon simply deletes the container's `upperdir`. All mutations are gone forever.

## Mental model

```text
TWO CONTAINERS FROM THE SAME IMAGE:

  CONTAINER 1 (dfs-cow-1)                   CONTAINER 2 (dfs-cow-2)
┌──────────────────────────────┐          ┌──────────────────────────────┐
│ UpperDir (Private R/W Layer) │          │ UpperDir (Private R/W Layer) │
│  + /tmp/unique_to_c1.txt     │          │  (Clean - no mutations)     │
└──────────────┬───────────────┘          └──────────────┬───────────────┘
               │                                         │
               │ Union Mount                             │ Union Mount
               ▼                                         ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LowerDir: Immutable Base Image Layers (Shared / Read-Only)             │
│ - Layer 2: /data                                                       │
│ - Layer 1: /bin, /etc, /lib, /usr                                      │
└────────────────────────────────────────────────────────────────────────┘
```

## Build it
Look at [test_cow_isolation.py](../code/test_cow_isolation.py).
It automates the proof of CoW isolation:
1. Launches `dfs-cow-1` and creates `/tmp/unique_to_c1.txt`.
2. Launches `dfs-cow-2` and verifies `cat /tmp/unique_to_c1.txt` returns `No such file or directory`.
3. Runs `docker diff` to inspect the mutation log of each container.
4. Removes `dfs-cow-1`, launches `dfs-cow-3`, and verifies the file is gone.

## Run it
Execute the experiment runner:

```bash
./phases/04-containers-and-filesystems/01-copy-on-write-layer/experiments/run_experiment.sh
```

## Inspect it
1. Run `docker diff dfs-cow-1`.
   Notice the symbols:
   - `A`: File Added (`/tmp/unique_to_c1.txt`)
   - `C`: Directory Changed (`/tmp`)
   - `D`: File Deleted
2. Inspect the container's storage driver:
   ```bash
   docker inspect <container> --format '{{.Driver}}'
   ```
   Modern engines use `overlayfs` via containerd snapshotters.

## Break it
Launch a container and delete a system file provided by the base image:

```bash
docker run --name dfs-break -d alpine:latest sleep 30
docker exec dfs-break rm -f /bin/ls
# Inside the container, ls is gone:
docker exec dfs-break ls
# (Returns: exec: "ls": executable file not found)
```
Now check `docker diff dfs-break`:
You will see `D /bin/ls` (a whiteout marker in `upperdir`).
Now launch a second container:
```bash
docker run --rm alpine:latest ls /bin
```
Notice `/bin/ls` is still completely intact in the image! The destruction was strictly confined to `dfs-break`'s private upperdir.
Clean up:
```bash
docker rm -f dfs-break
```

## Debug it
If a container's disk usage is ballooning uncontrollably:
1. Run `docker ps -s` to inspect the `SIZE` column:
   - `virtual size`: Base image size + writable layer size.
   - `writable layer size`: Exact number of bytes written to the container's `upperdir`.
2. If `writable layer size` is gigabytes, the application is writing temporary files, caches, or logs directly to the root filesystem instead of a mounted volume!

## Modify it
Start an Alpine container, install `curl` using `apk add curl`, and run `docker diff` on the container. Document how many directories and files were modified in `upperdir`.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Output from `test_cow_isolation.py`.
- The `docker diff` output showing `C` and `A` entries.
- Explanation of why `dfs-cow-3` could not see the file from `dfs-cow-1`.

## Questions for mastery
1. Why does copying a 1GB file inside an image layer to another directory double the image size, even if you delete the original file in a subsequent build step?
2. What is the difference between an immutable image layer and a container's writable layer?
3. If container filesystems are ephemeral, how do databases store persistent state?

## What comes next
We have manually inspected containers, images, and layers. Now we are ready to build custom images declaratively. Proceed to **Phase 05: Building Images with Dockerfiles**.
