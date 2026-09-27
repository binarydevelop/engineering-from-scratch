# Lesson 05.1: Building Images with Dockerfiles

## Motto
"A Dockerfile is an executable recipe that translates human intent into a stack of immutable, content-addressed image layers."

## Problem
In previous lessons, we used pre-built images (`alpine`, `hello-world`). But in real software engineering, you write code and must package your own runtime environment.
Without Dockerfiles, developers manually started a container, ran `apt-get`, copied files in via `docker cp`, and committed the running container using `docker commit`.
This manual process was catastrophic:
- Builds were non-reproducible and unversioned.
- Nobody knew what packages were installed or why.
- Layers were bloated with intermediate build debris and cache files.

We need a declarative, deterministic format to build images.

## Prediction
1. Does every instruction in a Dockerfile create a new filesystem layer?
2. If you change a variable in `ENV`, does the image require re-downloading the base operating system?
3. What is the difference between `CMD` and `ENTRYPOINT`?

## Why this matters
The Dockerfile is the standard contract between developers and production operations. Writing bad Dockerfiles leads to slow builds, bloated images, non-reproducible artifacts, and security vulnerabilities. Understanding the core instructions (`FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `CMD`) is mandatory for every backend and infrastructure engineer.

## First principles
Each line in a Dockerfile informs Docker's builder (BuildKit) to perform a state transition:
1. `FROM`: Defines the initial immutable base image layers.
2. `WORKDIR`: Sets the current working directory for subsequent instructions and sets default runtime `WorkingDir` in metadata. Creates the directory if it does not exist.
3. `COPY <src> <dest>`: Copies files from the **build context** (host directory sent to the daemon) into the container layer.
4. `RUN <command>`: Executes a command inside an intermediate container, records all filesystem changes, and freezes them into a new layer.
5. `ENV <key>=<val>`: Sets persistent environment variables recorded into the image JSON configuration.
6. `EXPOSE <port>`: Documents which port the container application listens on. **Does not publish the port to the host!**
7. `CMD ["exec", "param"]`: Specifies the default executable and parameters if none are provided to `docker run`.

**The Exec Form vs. Shell Form**:
- `CMD python3 app.py` (Shell form): Runs `/bin/sh -c "python3 app.py"`. Spawns a shell as PID 1; prevents signals from reaching Python!
- `CMD ["python3", "app.py"]` (Exec form): Executes `python3` directly as PID 1. Always prefer exec form for backend services!

## Mental model

```text
DOCKERFILE INSTRUCTIONS:                RESULTING ARTIFACT:
┌─────────────────────────────┐        ┌─────────────────────────────┐
│ FROM python:3.11-slim       │  ───►  │ Base Layers (Python runtime)│
├─────────────────────────────┤        ├─────────────────────────────┤
│ WORKDIR /app                │  ───►  │ Metadata: WorkingDir = /app │
├─────────────────────────────┤        ├─────────────────────────────┤
│ COPY app.py .               │  ───►  │ New Layer: /app/app.py       │
├─────────────────────────────┤        ├─────────────────────────────┤
│ ENV SERVICE_NAME=microsvc   │  ───►  │ Metadata: Env = [SERVICE..] │
├─────────────────────────────┤        ├─────────────────────────────┤
│ CMD ["python3", "app.py"]   │  ───►  │ Metadata: Cmd = [python3..] │
└─────────────────────────────┘        └─────────────────────────────┘
```

## Build it
Review [Dockerfile](../code/Dockerfile) and [app.py](../code/app.py).
We build the image with:
```bash
docker build -t dfs-custom-app:v1 phases/05-building-images-with-dockerfiles/01-dockerfile-primitives/code
```

## Run it
Execute the experiment runner:

```bash
./phases/05-building-images-with-dockerfiles/01-dockerfile-primitives/experiments/run_experiment.sh
```

## Inspect it
1. Run `docker history dfs-custom-app:v1`. Trace each line of your Dockerfile to the exact layer ID and size it produced.
2. Run `docker image inspect dfs-custom-app:v1 --format '{{json .Config.Cmd}}'`. Verify that the exec form array is preserved.
3. Query the running container: `curl http://localhost:8000`.

## Break it
Edit `Dockerfile` and misspell the script name: `COPY app_typo.py .`
Run `docker build .` and observe the failure:
`failed to calculate checksum of ref ... "/app_typo.py": not found`
Notice that Docker validates the build context during execution and stops immediately on failure.

## Debug it
When a Dockerfile build fails:
1. Check the failing step in the build logs.
2. Note that BuildKit caches previous successful steps up to the point of failure.
3. If a `RUN` instruction fails (e.g. `pip install`), run an interactive container from the prior step's image to investigate interactively:
   ```bash
   docker run --rm -it <previous-layer-id> /bin/sh
   ```

## Modify it
Add an instruction `ENV PORT=9000` to the Dockerfile. Update `app.py` to read `PORT = int(os.environ.get("PORT", 8000))`. Rebuild the image with tag `v2`, run it with `-p 9000:9000`, and verify with `curl http://localhost:9000`.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The output of `docker history dfs-custom-app:v1`.
- The JSON response from `curl http://localhost:8000`.
- Stored metadata for `Cmd` and `WorkingDir`.

## Questions for mastery
1. Why does `EXPOSE 8000` not make port 8000 accessible from your host machine?
2. What is the build context, and why can sending a large directory slow down `docker build`?
3. Why should you avoid using shell form (`CMD python app.py`) in production images?

## What comes next
You noticed how fast the second build was. Why? How does Docker know which layers can be reused? Proceed to **Phase 06: Image Layers and Build Cache**.
