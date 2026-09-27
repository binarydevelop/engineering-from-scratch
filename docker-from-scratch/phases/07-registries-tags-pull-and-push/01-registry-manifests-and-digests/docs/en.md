# Lesson 07.1: Registries, Tags, Pull and Push

## Motto
"Tags are mutable human pointers; digests are immutable cryptographic truths; registries are content-addressable blob stores."

## Problem
A frequent incident in production environments:
A service configured with `image: python:3.11` runs flawlessly for six months. One morning, the container crashes on restart because the upstream image maintainer pushed new security patches or a breaking dependency update under the same mutable `python:3.11` tag!
If you do not understand where images come from, how tags point to manifests, and why immutable digests exist, you will suffer unexplainable drift across development, staging, and production environments.

## Prediction
1. When you run `docker pull redis:7`, what machine on the internet is contacted?
2. If two different machines pull `redis:7` on different days, are they guaranteed to get the exact same bytes?
3. What is the difference between pulling by tag (`redis:7`) versus pulling by digest (`redis@sha256:...`)?

## Why this matters
Using mutable tags like `:latest` or `:v1` in production is an anti-pattern. An attacker can overwrite a mutable tag in a compromised registry to inject malicious code. Pinning containers to cryptographic digests (`@sha256:...`) guarantees byte-for-byte reproducibility and cryptographic supply-chain integrity.

## First principles
1. **The Full Anatomy of an Image Name**:
   ```text
   [REGISTRY_HOST[:PORT]/][NAMESPACE/]REPOSITORY[:TAG|@DIGEST]
   ```
   - When no host is specified, Docker defaults to `docker.io` (Docker Hub).
   - When no namespace is specified for Docker Hub, Docker defaults to `library/` (official images like `library/redis` or `library/python`).
   - When no tag or digest is specified, Docker defaults to `:latest`.
2. **The Registry Transfer Flow**:
   A registry (OCI Distribution API) does not store monolithic container files. It stores:
   - **Manifests**: JSON documents specifying layer hashes and architecture.
   - **Blobs**: Gzipped layer tarballs (`/v2/<name>/blobs/sha256:<hash>`).
3. **The Pull Sequence**:
   ```text
   docker CLI
      ↓ GET /v2/library/redis/manifests/7
   Registry returns JSON Manifest with layer SHA256 hashes
      ↓ Check local cache
   Docker Daemon checks /var/lib/docker/image/
   Only downloads missing layer blobs!
      ↓
   Assembles layers into local image store
   ```

## Mental model

```text
OCI REGISTRY (HTTP REST API: registry.docker.io / ghcr.io)
┌────────────────────────────────────────────────────────┐
│  Tag "7-alpine" ──► Pointer to Manifest SHA256:abc123  │
├────────────────────────────────────────────────────────┤
│  Manifest (JSON)                                       │
│  - Config: sha256:520775...                            │
│  - Layers: [sha256:545d2c..., sha256:e1acae...]        │
├────────────────────────────────────────────────────────┤
│  Blob Store (Content-Addressable)                      │
│  - /blobs/sha256:545d2c... (Tarball Layer 1)           │
│  - /blobs/sha256:e1acae... (Tarball Layer 2)           │
└──────────────────────────┬─────────────────────────────┘
                           │ docker pull (Downloads only missing blobs)
                           ▼
LOCAL DOCKER ENGINE STORE (/var/lib/docker)
┌────────────────────────────────────────────────────────┐
│  Reconstructs image, unpacks snapshotter, links tag    │
└────────────────────────────────────────────────────────┘
```

## Build it
Review [inspect_registry_manifest.py](../code/inspect_registry_manifest.py).
It parses image reference strings to uncover the implicit registry host and namespace, and queries the local Docker daemon for `RepoDigests`.

## Run it
Execute the experiment runner:

```bash
./phases/07-registries-tags-pull-and-push/01-registry-manifests-and-digests/experiments/run_experiment.sh
```

## Inspect it
1. Run `docker image inspect redis:7-alpine --format '{{json .RepoDigests}}'`.
2. Notice the format: `redis@sha256:520775...`
3. Notice that you can run a container specifying the exact digest:
   ```bash
   docker run --rm redis@sha256:520775a41a63e77e06c73e35d2fd9cc15921a609516818796b4ecbb813078bc7 echo "Pinned by digest!"
   ```

## Break it
Try to tag an image with an invalid registry name containing uppercase letters or illegal characters:

```bash
docker tag redis:7-alpine Invalid_Host:5000/MyRepo:v1
```
Docker rejects this immediately:
`Error parsing reference: "Invalid_Host:5000/MyRepo:v1" is not a valid repository/tag: invalid reference format`
The OCI specification strictly requires lowercase repository names.

## Debug it
When encountering `manifest for <image> not found`:
1. Check the tag spelling (`alpine:3.20` vs `alpine:3.20.0`).
2. Verify architecture compatibility. If you are on an `arm64` machine and request an image with only `amd64` manifest, Docker will report:
   `no matching manifest for linux/arm64/v8 in the manifest list entries`.

## Modify it
Tag `alpine:latest` as `my-registry.local:5000/core/alpine:stable`. Run `docker images` and verify that the virtual size and image ID match `alpine:latest` exactly.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The parsed registry, namespace, and tag components.
- The `RepoDigests` string for your local image.
- Explanation of why digests cannot be overwritten.

## Questions for mastery
1. What prevents someone from replacing the contents of an image pinned by `image@sha256:...`?
2. If your registry loses network connectivity, can you still run images you already pulled? Why?
3. What is the difference between `docker tag` and `docker push`?

## What comes next
We now understand images, layers, Dockerfiles, and registries. Now we enter the core mechanism where most engineers get stuck: **Networking**. Proceed to **Phase 08: Container Networking: Start With localhost**.
