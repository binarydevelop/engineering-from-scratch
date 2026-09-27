# Lesson 26.1: Image Optimization and the `.dockerignore` Contract

## Motto
"Layers are append-only; deleting a file in a later layer hides it from the container but leaves its bytes permanently embedded in your image."

## Problem
In real-world repositories, developer teams frequently build container images that weigh 2GB or 3GB for simple backend applications.
When pushing to registries or deploying in autoscaling clusters:
- Deployments take 5 to 10 minutes to pull massive image layers.
- Bandwidth bills explode.
- Disks on Kubernetes nodes run out of space.
- A developer attempts to fix it by adding `RUN rm -rf /tmp/build-cache` as the next line, only to discover the image size didn't shrink by a single byte!
Why doesn't `rm` shrink image layers, and how do we build lean images?

## Prediction
1. If layer 3 creates a 100MB file and layer 4 runs `rm` on that file, what is the combined disk size of layers 3 and 4?
2. If your repository contains a `.git` folder with 500MB of history, does `COPY . .` send that history to the Docker daemon?
3. How does `.dockerignore` reduce both build time and image size?

## Why this matters
Image size directly governs cold-start latency, auto-scaling velocity, and attack surface area. An image containing build toolchains (`gcc`, `g++`, `make`), header files, and git history exposes hundreds of additional CVE attack vectors that have no place in a production runtime environment.

## First principles
1. **The Append-Only Layer Invariant**:
   Remember Phase 04: image layers are immutable tar archives.
   - If Layer N adds `/tmp/data.bin` (50MB), that 50MB is written into the layer tarball forever.
   - If Layer N+1 deletes `/tmp/data.bin`, the filesystem union mount merely records a whiteout marker (`.wh.data.bin`) in Layer N+1.
   - The original 50MB tarball remains part of the image manifest and is still downloaded by every server!
   - **Rule**: You must create, use, and delete temporary build files in the **exact same `RUN` command** (e.g. `RUN download && compile && rm -rf`).
2. **The Build Context Contract (`.dockerignore`)**:
   When you run `docker build .`, the CLI archives your current working directory and streams it over the socket to the daemon.
   Without `.dockerignore`, your `.git` folder, test fixtures, `.env` secrets, node_modules, and virtual environments are sent over the wire, bloating build context transfer times.

## Mental model

```text
THE BROKEN RM ILLUSION:
┌────────────────────────────────────────────────────────┐
│ Layer 4: RUN rm -rf /tmp/large.bin                     │
│ └── Whiteout marker: .wh.large.bin (Size: 0 MB)        │
├────────────────────────────────────────────────────────┤
│ Layer 3: RUN dd if=/dev/zero of=/tmp/large.bin (100MB) │
│ └── Tarball contains large.bin (Size: 100 MB!)         │
└────────────────────────────────────────────────────────┘
Total Size Downloaded: 100 MB! The file is STILL THERE.

THE CLEAN RUN PATTERN:
┌────────────────────────────────────────────────────────┐
│ Layer 3: RUN download && compile && clean_temp_files   │
│ └── Resulting Tarball only contains compiled binary!   │
└────────────────────────────────────────────────────────┘
Total Size: 5 MB. Zero debris trapped in history.
```

## Build it
Review `.dockerignore`, `Dockerfile.bloated`, and `Dockerfile.optimized` in `code/`.

## Run it
Execute the experiment runner:

```bash
./phases/26-image-optimization/01-slimming-down-and-dockerignore/experiments/run_experiment.sh
```

## Inspect it
1. Compare sizes: `dfs-opt-bloated` (297MB) vs `dfs-opt-lean` (58MB).
2. Inspect `docker history dfs-opt-bloated:v1`.
   Notice that the `RUN dd ...` step added 15.7MB, and the subsequent `RUN rm ...` step took 12.3kB without reclaiming the 15.7MB!
3. Notice that `large_asset.bin` (20MB) on the host was completely excluded by `.dockerignore`.

## Break it
Temporarily delete `.dockerignore` and run `docker build` on a directory containing a large file.
Watch the build output:
`[internal] load build context` transfers megabytes of useless data across the socket, slowing down the build start.

## Debug it
When analyzing why an image is unexpectedly huge:
1. Inspect layer-by-layer size contribution:
   ```bash
   docker history --human <image-name>
   ```
2. Scan the top layer contributors to find which instruction generated hundreds of megabytes.

## Modify it
Chain package installation and cache cleanup in a single `RUN` command on Alpine:
```dockerfile
RUN apk add --no-cache curl
```
Contrast this with `RUN apk add curl && rm -rf /var/cache/apk/*`. Both produce lean layers because the cleanup happens within the same layer boundary.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Size comparison: Bloated image vs Lean image.
- The `docker history` output showing the trapped layer bytes.
- Explanation of why union filesystems cannot shrink prior layers.

## Questions for mastery
1. Why does chaining commands with `&&` create fewer layers than separate `RUN` commands?
2. What are the compatibility tradeoffs between Alpine Linux (musl libc) and Debian/Ubuntu (glibc)?
3. Why should sensitive files like `.env` always be in `.dockerignore`?

## What comes next
Chaining `RUN` commands helps, but what if you must compile C++, Go, or Rust code using heavy compilers (gcc, cargo) that shouldn't exist in production? Proceed to **Phase 27: Multi-Stage Builds**.
