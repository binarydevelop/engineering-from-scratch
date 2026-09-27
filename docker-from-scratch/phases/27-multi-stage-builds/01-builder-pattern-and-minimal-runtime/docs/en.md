# Lesson 27.1: Multi-Stage Builds and Minimal Runtimes

## Motto
"Build in a rich factory stage; ship only the compiled artifact in an empty runtime stage."

## Problem
When deploying compiled languages (Go, Rust, C++, Java) or frontend builds (React, Vue, Next.js), the build process requires heavy tooling:
Compilers (`gcc`, `cargo`), package managers (`npm`, `pip`, `maven`), source code, header files (`linux-headers`), and intermediate object files (`.o`, `.class`).
In a naive single-stage Dockerfile, all of these build tools remain permanently baked into the production image.
The resulting image weighs 1GB to 2GB, takes forever to download, and contains compilers that attackers can exploit for living-off-the-land attacks.
How can we compile code inside Docker without shipping compilers to production?

## Prediction
1. Can a Dockerfile have more than one `FROM` instruction?
2. What happens to the layers of the first stage when the second stage begins?
3. How do you copy a file from stage 1 into stage 2?

## Why this matters
Multi-stage builds are the gold standard of cloud-native engineering. A Go microservice image can be shrunk from 800MB (with Go toolchain) down to 10MB (or even a zero-dependency `scratch` image), eliminating 99% of CVE vulnerabilities and enabling instantaneous pod launches.

## First principles
1. **Multiple `FROM` Stages**:
   Each `FROM` instruction starts a fresh build stage with a completely independent base image and clean filesystem.
2. **Naming Stages (`AS <name>`)**:
   `FROM golang:1.22-alpine AS builder` names the stage `builder`.
3. **Artifact Extraction (`COPY --from=<stage>`)**:
   ```dockerfile
   COPY --from=builder /build/app /app/app
   ```
   Docker extracts *only* that specific file across the stage boundary.
4. **Discarding Build-Time Layers**:
   When the build finishes, Docker only exports the final stage to the image store! All intermediate layers from earlier stages are completely discarded and never pushed to registries.

## Mental model

```text
STAGE 1: "builder" (Heavyweight Factory)
┌────────────────────────────────────────────────────────┐
│ FROM python:3.11-slim AS builder                       │
│ - Installs compilers, build dependencies (500MB)       │
│ - Compiles application source code                     │
│ - Produces binary: /build/app_binary (5MB)             │
└──────────────────────────┬─────────────────────────────┘
                           │
                           │ COPY --from=builder /build/app_binary
                           ▼
STAGE 2: "runtime" (Lean Shipping Container)
┌────────────────────────────────────────────────────────┐
│ FROM alpine:latest                                     │
│ - Clean rootfs (Zero compilers, zero build tools)      │
│ - /app/app_binary (Copied from builder)                │
│                                                        │
│ RESULT: 10MB Total Size! 100% Secure & Minimal         │
└────────────────────────────────────────────────────────┘
```

## Build it
Review `Dockerfile.single` and `Dockerfile.multistage` in `code/`.
Notice:
- `Dockerfile.single` leaves `/build/tools/compiler_suite.bin` (50MB) trapped in the image.
- `Dockerfile.multistage` uses `FROM ... AS builder` and extracts only the binary via `COPY --from=builder`.

## Run it
Execute the experiment runner:

```bash
./phases/27-multi-stage-builds/01-builder-pattern-and-minimal-runtime/experiments/run_experiment.sh
```

## Inspect it
1. Observe Step 3: `dfs-single` (313MB) vs `dfs-multi` (58MB).
2. Observe Step 4: The single-stage image contains `/build/tools/compiler_suite.bin`.
3. Observe Step 5: The multi-stage image has no `/build` directory at all!
4. Both run and execute the exact same production logic.

## Break it
Misspell the source stage name in `COPY --from`:
```dockerfile
COPY --from=builderrr /build/app_binary /app/app_binary
```
Run `docker build`:
BuildKit fails immediately during graph compilation:
`error: invalid from flag value builderrr: stage not found`.

## Debug it
When a binary copied from a builder stage fails to execute in the runtime stage with `exec format error` or `file not found`:
1. Check standard C library compatibility:
   If the builder used Ubuntu/Debian (`glibc`) and the runtime is Alpine (`musl`), the dynamic linker will fail to find `/lib/ld-linux-x86-64.so.2`!
   Fix by compiling statically (`CGO_ENABLED=0` in Go, or `-static` in GCC), or matching the base OS across stages.

## Modify it
Create a 3-stage Dockerfile:
- Stage 1 (`test`): Runs unit tests and linter.
- Stage 2 (`builder`): Compiles the artifact.
- Stage 3 (`runtime`): Copies the binary for production.
If Stage 1 fails, BuildKit aborts and never builds Stage 2 or 3!

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Image size comparison: Single-stage vs Multi-stage.
- Verification that build debris was excluded from the runtime container.
- Execution confirmation of the binary in both environments.

## Questions for mastery
1. Why is building inside a Docker `builder` stage better than compiling on your host laptop and copying the binary into Docker? (Hint: toolchain consistency and OS ABI compatibility).
2. What is `FROM scratch`, and when can it be used?
3. How does BuildKit parallelize independent stages in multi-stage Dockerfiles?

## What comes next
We have mastered container infrastructure from kernel processes to production hardening.
Now comes the ultimate test of your understanding:
In **Phase 28**, you will enter **8 real-world broken labs** where you will receive symptoms, not solutions, and must diagnose and fix each container failure. Proceed to **Phase 28: Container Debugging Without Magic**.
