# Part VIII: Containers in CI/CD (Phases 55–62)

## Motto
> "A container image is an immutable root filesystem archive. Never deploy mutable tags like 'latest' to production — pin exact immutable SHA-256 digests."

---

## Delivery Problem
A company deploys their application to Kubernetes using `image: mycompany/api:latest`. 
During an incident, the cluster auto-scales from 5 replicas to 15 replicas. 
The 5 existing replicas are running code built three days ago, while the 10 newly launched replicas pull a newly pushed `:latest` image from the registry containing unverified code! 

Half the incoming customer traffic succeeds; the other half fails. The on-call team spends two hours debugging "intermittent network issues" because nobody realizes the cluster is split across two completely different code versions running under the exact same tag name.

---

## Prediction
1. Deploying `:latest` creates non-deterministic cluster state where identical pods run different code versions.
2. Building containers without layer caching results in redundant downloads and multi-minute pipeline delays.
3. Running containers as the root user allows a compromised application to modify system files and escape the container sandbox.

---

## First Principles
1. **The Anatomy of an OCI Image**:
   An OCI (Open Container Initiative) container image is a set of tarball layers (representing filesystem diffs) stacked on top of each other, plus a JSON manifest recording layer hashes and configuration.
2. **Tags vs. Digests**:
   - **Image Tag** (`myapp:1.0.0`, `myapp:latest`): A mutable human-readable pointer in the registry. It can be overwritten at any time.
   - **Image Digest** (`myapp@sha256:7f9b8c31...`): The immutable cryptographic hash of the image manifest. It cannot be altered without changing the hash.
3. **Multi-Stage Builds (Least Privilege File Packaging)**:
   Stage 1 contains compilers, build headers, and package manager caches. Stage 2 copies only the compiled runtime artifact into a minimal base image, reducing image size by 80%+ and eliminating attack surface.

---

## Manual Process (Phases 55, 56, 57)
Inspect and build the container manually:

```bash
# 1. Inspect the multi-stage Dockerfile
cat sample-apps/delivery-service/Dockerfile

# 2. Build image with explicit semantic tag
docker build -t delivery-service:1.0.0 sample-apps/delivery-service/

# 3. Inspect image digest
docker inspect --format='{{index .RepoDigests 0}}' delivery-service:1.0.0 2>/dev/null || docker images delivery-service:1.0.0
```

---

## Mental Model

```text
[ Dockerfile: Stage 1 (Builder) ]
- Debian/Python base with gcc, make, dev headers
- Compiles source and installs dependencies
- Size: 950 MB
               │
               ▼ COPY --from=builder (Artifacts only)
[ Dockerfile: Stage 2 (Runtime) ]
- Minimal python:3.12-slim or distroless
- Zero compilers, non-root user 'appuser'
- Size: 120 MB (-87% attack surface reduction)
               │
               ▼
[ Pinned Digest: ghcr.io/org/app@sha256:7f9b... ]
```

---

## Automate It (Phase 58, 60: Docker Build in CI with Layer Caching)

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3.4.0

- name: Build and Push OCI Image
  uses: docker/build-push-action@v6.3.0
  with:
    context: sample-apps/delivery-service
    push: false
    tags: ghcr.io/binarydevelop/delivery-service:1.0.0
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

---

## Run It
Inspect the Dockerfile created in `sample-apps/delivery-service/Dockerfile`:
```bash
grep -E "USER|FROM|HEALTHCHECK" sample-apps/delivery-service/Dockerfile
```

---

## Break It (Phase 56: Mutable Tag Overwrite)
1. Run broken lab `10-mutable-latest-image-tag-overwrite`:
   ```bash
   python3 broken-pipelines/10-mutable-latest-image-tag-overwrite/reproduce_failure.py
   ```
2. Run broken lab `32-multi-stage-docker-copies-from-wrong-stage`:
   ```bash
   python3 broken-pipelines/32-multi-stage-docker-copies-from-wrong-stage/reproduce_failure.py
   ```
3. Run broken lab `33-root-container-fails-in-read-only-filesystem`:
   ```bash
   python3 broken-pipelines/33-root-container-fails-in-read-only-filesystem/reproduce_failure.py
   ```

---

## Debug It
When a container build or deployment fails:
- Check `docker history <image>` to see layer sizes and identify which step blew up the image size.
- Run container locally with `--read-only` to ensure the application does not assume root write access to arbitrary system folders.

---

## Security (Phase 62: Container Hardening)
- **Non-Root User**: Never run as `root` (UID 0). Always create an unprivileged user (`appuser`, UID 10001).
- **No Embedded Secrets**: Never pass build secrets via `ARG` or `ENV` in Dockerfiles; use BuildKit secret mounts (`RUN --mount=type=secret`).
- **Read-Only Root Filesystem**: Configure Kubernetes pods with `readOnlyRootFilesystem: true`.

---

## Optimize It (Phase 60: Layer Caching)
Order Dockerfile commands from least frequently changed to most frequently changed:
1. `FROM base` (Rarely changes)
2. `COPY requirements.txt .` and `RUN pip install` (Changes on dependency bump)
3. `COPY app.py .` (Changes on every commit)
Placing `COPY . .` before `pip install` invalidates layer caching on every code edit, adding minutes to every build!

---

## Deployment Implication
Deploying by content digest (`image@sha256:...`) guarantees that every node in the cluster runs identical code regardless of when pods are scheduled.

---

## Recovery
If a bad container image is pushed to the registry:
- Do NOT delete the tag or image (breaks existing manifests).
- Update the deployment manifest to reference the prior immutable digest and commit to Git.

---

## Practical Exercises (Part VIII)
1. **Exercise 8.1**: Build `sample-apps/delivery-service/Dockerfile` and measure the image size difference between a single-stage build and the multi-stage build.
2. **Exercise 8.2**: Inspect the layer history of an image using `docker history --no-trunc` and identify which layer contributes the most bytes.
3. **Exercise 8.3**: Run `sample-apps/delivery-service` with `docker run --user 10001 --read-only` and verify that health checks pass.
4. **Exercise 8.4**: Write a script that parses `docker inspect` output to extract the canonical repository digest (`RepoDigests`).
5. **Exercise 8.5**: Demonstrate layer cache invalidation by swapping the order of `COPY requirements.txt` and `COPY app.py` and timing the rebuild.
6. **Exercise 8.6**: Test the `HEALTHCHECK` directive in the Dockerfile by simulating a process crash and checking `docker ps` status.
7. **Exercise 8.7**: Scan a local container image for vulnerabilities using Trivy or an equivalent scanner.
8. **Exercise 8.8**: Configure a registry policy that rejects image pushes targeting the tag `:latest`.

---

## Questions for Mastery
1. *Why is deploying an image by immutable SHA-256 digest safer than deploying by release version tag like `:v1.2.0`?*
2. *Why should build toolchains (gcc, make) never be present in production container images?*
3. *What happens to Docker layer caching when a command like `apt-get update` is placed on its own line without `apt-get install`?*

---

## What Comes Next
In **Part IX (Phases 63–69)**, we study Versioning and Releases: semantic versioning, Git tags, automated changelog generation, release notes, and release immutability.
