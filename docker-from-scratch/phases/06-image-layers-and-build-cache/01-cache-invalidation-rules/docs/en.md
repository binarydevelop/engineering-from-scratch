# Lesson 06.1: Image Layers and Build Cache Invalidation Rules

## Motto
"Order instructions from lowest volatility to highest volatility; an invalidation at line N forces every step after N to rebuild."

## Problem
In teams new to Docker, developers frequently complain:
"Every time I change one line of code, `docker build` takes 5 minutes to download packages and recompile everything!"
The root cause is almost always the same: copying the entire project repository (`COPY . .`) *before* running dependency package managers (`npm install`, `pip install`, `cargo build`, `go mod download`).
Understanding how Docker evaluates cache validity transforms 5-minute build cycles into sub-second instantaneous builds.

## Prediction
1. If you change a comment in `app.py`, does Docker re-run `pip install` if `COPY . .` appears before `pip install`?
2. How does Docker determine whether a `COPY` instruction can use cache? (By timestamp, file name, or file content hash?)
3. Can a `RUN apt-get update` instruction use cache even if new security patches were released upstream?

## Why this matters
Build speed directly governs developer feedback loops and CI/CD throughput. An optimized build cache structure can reduce deployment times from 15 minutes to 30 seconds, while saving hundreds of gigabytes of bandwidth across deployment pipelines.

## First principles
1. **The Invalidation Cascade**: Docker evaluates Dockerfile instructions sequentially from top to bottom. As long as the instructions and their inputs match previous builds, Docker reuses the cached layer.
2. **The Cache-Busting Rule**: The moment a single instruction's cache is invalidated, **all subsequent instructions in that stage are automatically invalidated and forced to execute**, regardless of whether their commands changed!
3. **Cache Invalidation Triggers**:
   - For `COPY` / `ADD`: Docker computes a cryptographic checksum of the contents of the files being copied. If any file checksum differs, cache is busted.
   - For `RUN`: Docker compares the literal command string (`RUN apt-get update`). It does **not** query the internet to see if packages changed! If the string matches and previous layers are cached, Docker reuses the cached layer without re-running the command.

## Mental model

```text
THE NAIVE APPROACH (Broken Cache):
┌──────────────────────────────┐
│ 1. FROM python:3.11-slim     │  [CACHED]
├──────────────────────────────┤
│ 2. COPY . .                  │  [INVALIDATED! app.py changed]
├──────────────────────────────┤
│ 3. RUN pip install ...       │  [FORCED TO RE-RUN (300s!)] ◄── PAIN
├──────────────────────────────┤
│ 4. CMD ["python", "app.py"]  │  [RE-BUILT]
└──────────────────────────────┘

THE OPTIMIZED APPROACH (Volatility Ordered):
┌──────────────────────────────┐
│ 1. FROM python:3.11-slim     │  [CACHED]
├──────────────────────────────┤
│ 2. COPY requirements.txt .   │  [CACHED - requirements.txt unchanged]
├──────────────────────────────┤
│ 3. RUN pip install ...       │  [CACHED! Reuses existing layer (0.0s)]
├──────────────────────────────┤
│ 4. COPY app.py .             │  [INVALIDATED! app.py changed]
├──────────────────────────────┤
│ 5. CMD ["python", "app.py"]  │  [RE-BUILT]
└──────────────────────────────┘
```

## Build it
Review the two Dockerfiles in `code/`:
- `Dockerfile.naive`: Copies everything with `COPY . .` before the expensive 3-second build step.
- `Dockerfile.optimized`: Separates low-volatility dependencies (`requirements.txt`) from high-volatility application code (`app.py`).

## Run it
Execute the benchmarking runner:

```bash
./phases/06-image-layers-and-build-cache/01-cache-invalidation-rules/experiments/run_experiment.sh
```

## Inspect it
Observe the build output:
1. In the Naive rebuild, step `[3/3] RUN python3 -c ...` executes every single time.
2. In the Optimized rebuild, step `[2/4] COPY requirements.txt .` and `[3/4] RUN python3 -c ...` display `CACHED`, completing in under 0.2 seconds!

## Break it
Bust the cache of the optimized build intentionally by changing a single byte in `requirements.txt`:
```bash
echo "# bust" >> phases/06-image-layers-and-build-cache/01-cache-invalidation-rules/code/requirements.txt
docker build -f phases/06-image-layers-and-build-cache/01-cache-invalidation-rules/code/Dockerfile.optimized phases/06-image-layers-and-build-cache/01-cache-invalidation-rules/code
```
Notice that BuildKit immediately detects the checksum change on `requirements.txt` and re-runs the expensive installation step.

## Debug it
If a build unexpectedly busts cache at step N:
1. Check if an unintended file changed in the build context (e.g., local `.git` folder, logs, virtual environment `.venv`, or temporary files).
2. Fix this by adding a `.dockerignore` file to exclude volatile host artifacts.

## Modify it
Create a `.dockerignore` file in `code/` containing:
```text
*.log
__pycache__
.git
```
Prove that creating a `debug.log` file on the host does not bust `COPY . .` when `.dockerignore` is present.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Naive rebuild duration vs. Optimized rebuild duration.
- The BuildKit log lines showing `CACHED`.
- The checksum mechanism explanation in your own words.

## Questions for mastery
1. Why does `RUN apt-get update && apt-get install -y curl` combine update and install on a single line, rather than using two separate `RUN` commands?
2. If you pass `--no-cache` to `docker build`, what happens?
3. How does Docker know if a file copied via `COPY` has changed?

## What comes next
We now know how to build and cache images locally. But how are images shared across computers, servers, and clouds? Proceed to **Phase 07: Registries, Tags, Pull and Push**.
