# Lesson 03.1: Images From First Principles

## Motto
"An image is not a virtual hard drive; it is a stack of immutable tarballs with a JSON execution configuration."

## Problem
Engineers often picture a Docker image as an `.iso` file or a monolithic disk image containing a complete Linux installation.
Under this mistaken model:
- You expect pulling two 500MB images to always consume 1GB of disk space.
- You don't understand why changing one line in a configuration doesn't require redownloading or rebuilding the entire operating system.
- You wonder where your application code sits relative to the Linux root filesystem (`/bin`, `/etc`, `/lib`).

We must decompose an image into its physical files on disk.

## Prediction
Before pulling `alpine`:
1. How large is a minimal Linux root filesystem like Alpine?
2. If two different image tags share the same base layers, does Docker download those layers twice?
3. If you edit a file inside an image, does the image change?

## Why this matters
Misunderstanding images leads to bloated multi-gigabyte deployments, broken production deployments when mutable tags like `:latest` change unexpectedly, and severe registry storage costs. Understanding image immutability and content-addressable storage is the foundation of secure, repeatable deployments.

## First principles
An OCI (Open Container Initiative) image consists of three distinct components:
1. **Manifest**: A JSON document that lists the cryptographic SHA-256 hashes of the configuration object and each filesystem layer.
2. **Layers (Blobs)**: Compressed tar archives (`.tar.gz`). Each layer contains only the filesystem difference (added, changed, or deleted files) relative to the layer below it.
3. **Configuration Object**: A JSON file that stores:
   - Default executable (`Entrypoint`, `Cmd`).
   - Environment variables (`Env`).
   - Working directory (`WorkingDir`).
   - Architecture (`arm64`, `amd64`) and OS (`linux`).
   - Cryptographic DiffIDs of the unpacked layers in order.

**Content-Addressable Storage**: Image IDs and layer IDs are not arbitrary names; they are the exact SHA-256 hashes of their contents. If a single byte changes, the hash changes, producing a new, distinct layer.

## Mental model

```text
IMAGE ANATOMY:
┌────────────────────────────────────────────────────────┐
│  Image Manifest (JSON)                                 │
│  - Config: sha256:abcd1234...                          │
│  - Layer 1: sha256:736e4f3a... (Rootfs tarball)        │
│  - Layer 2: sha256:98fa201b... (Python tarball)        │
└──────────────────────────┬─────────────────────────────┘
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ Config Object (JSON)         │ │ RootFS Layers (Immutable)    │
│ - Architecture: arm64        │ │                              │
│ - Cmd: ["python3", "app.py"] │ │ Layer 2: /app/app.py         │
│ - Env: ["PATH=/usr/bin:..."] │ │ Layer 1: /bin, /lib, /etc    │
└──────────────────────────────┘ └──────────────────────────────┘
```

## Build it
Rather than accepting `docker images` as an opaque table, look at [inspect_image_layers.py](../code/inspect_image_layers.py).
It parses the image JSON from `docker image inspect` and reveals:
- The exact SHA-256 hash of each layer in `RootFS.Layers`.
- The default `Cmd` and `Entrypoint`.
- The architecture and OS target.

## Run it
Execute the experiment runner:

```bash
./phases/03-images-from-first-principles/01-layers-and-metadata/experiments/run_experiment.sh
```

## Inspect it
1. Notice Alpine's size: only ~7.8 MB!
2. Inspect the output of `docker history alpine:latest`. It shows the exact single step that generated the base layer.
3. Run `docker inspect alpine:latest --format '{{json .RootFS.Layers}}'` to see the cryptographic layer hash.

## Break it
Try to mutate an image by editing its tag:

```bash
docker tag alpine:latest my-alpine:v1
```

Now compare the image ID of `alpine:latest` and `my-alpine:v1`:
```bash
docker inspect alpine:latest --format '{{.Id}}'
docker inspect my-alpine:v1 --format '{{.Id}}'
```
Both IDs are 100% identical!
Tags are not distinct images; tags are simply mutable text labels (pointers) pointing to immutable image IDs, exactly like Git branches pointing to commit hashes.

## Debug it
If an image fails to run with `exec format error`:
1. Check the image target architecture:
   ```bash
   docker image inspect <image> --format '{{.Architecture}}'
   ```
2. If your host is `arm64` (e.g. Apple Silicon) and the image is `amd64` (x86_64) without emulation, the host kernel cannot execute the binary syscalls.

## Modify it
Pull `busybox:latest`. Use `inspect_image_layers.py` to compare its layer count and size with `alpine:latest`. Document which has fewer layers.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Alpine's uncompressed layer SHA256 DiffID.
- The size on disk reported by Docker.
- The proof that `docker tag` creates a pointer rather than a data copy.

## Questions for mastery
1. Why are image layers immutable? What would break if a running container could modify an image layer directly?
2. If 10 different containers run simultaneously from `alpine:latest`, how many copies of Alpine's filesystem exist in host memory/disk?
3. What is the difference between an image tag and an image digest?

## What comes next
We now understand that images are read-only stacks of layers. But when we launch a container and create a file, where does that file go? Proceed to **Phase 04: Containers and Filesystems**.
