# Lesson 14.1: Environment Variables and Runtime Configuration

## Motto
"Build the image once; configure it everywhere via environment variables."

## Problem
In naive deployments, developers build three separate container images:
`my-app:dev` (hardcoded to connect to `localhost:5432`),
`my-app:staging` (hardcoded to `staging-db.internal`), and
`my-app:prod` (hardcoded to `prod-db.internal`).
This violates the core principle of container portability:
If you build different images for each environment, what you tested in staging is **not** what you deploy to production!
How can a single immutable image adapt its behavior seamlessly across environments?

## Prediction
1. If an environment variable is defined in both a `.env` file and via `-e KEY=VAL`, which one wins?
2. If an image specifies `ENV PORT=8000`, can you override it at runtime with `docker run -e PORT=9000`?
3. Are environment variables passed to a container encrypted or hidden from host inspection tools?

## Why this matters
The Twelve-Factor App methodology (Factor III: Config) requires strict separation of configuration from code. Passing configuration at runtime allows you to test the exact same cryptographic image digest across development, automated CI pipelines, staging clusters, and production.

## First principles
1. **The Invariant Image Rule**:
   ```text
   Identical Immutable Image Digest
               +
   Environment-Specific Config Injection (-e / --env-file)
               =
   Deterministic Runtime Behavior Across Environments
   ```
2. **Process Environment Injection**:
   In Unix, when `execve()` executes a binary, it passes an array of null-terminated strings (`char *envp[]`). Docker simply populates this array when launching PID 1 inside the container's PID namespace.
3. **Configuration Precedence**:
   - Level 1 (Lowest): Default fallback values hardcoded in application code.
   - Level 2: `ENV` instructions declared in the `Dockerfile`.
   - Level 3: Key-value pairs defined in `--env-file`.
   - Level 4 (Highest): Explicit `-e KEY=VAL` flags passed on the CLI.
4. **The Security Risk**:
   Environment variables are stored in plaintext inside the container's JSON metadata. Anyone with access to the Docker socket or `docker inspect` can view database passwords and API tokens!

## Mental model

```text
               ONE IMMUTABLE IMAGE: my-service:v1.0.0
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
      DEVELOPMENT             STAGING              PRODUCTION
┌─────────────────────┐┌─────────────────────┐┌─────────────────────┐
│ --env-file dev.env  ││ --env-file stage.env││ --env-file prod.env │
│ DB: dev-db:5432     ││ DB: stage-db:5432   ││ DB: prod-cluster    │
│ LOG_LEVEL: DEBUG    ││ LOG_LEVEL: INFO     ││ LOG_LEVEL: WARN     │
│ DEBUG: true         ││ DEBUG: false        ││ DEBUG: false        │
└─────────────────────┘└─────────────────────┘└─────────────────────┘
```

## Build it
Review `configurable_app.py`, `dev.env`, and `prod.env` in `code/`.
The application loads configuration via standard `os.environ.get()` with safe defaults.

## Run it
Execute the experiment runner:

```bash
./phases/14-environment-variables-and-configuration/01-runtime-env-injection/experiments/run_experiment.sh
```

## Inspect it
1. Observe the JSON config dump across Runs 1, 2, and 3.
2. In Run 4, notice that `-e LOG_LEVEL="TRACE"` overrides the `LOG_LEVEL=WARN` defined in `prod.env`.
3. In Run 5, observe how `docker inspect` prints `SECRET_API_KEY=super-secret-12345` in plaintext.

## Break it
Launch a container with an invalid integer configuration that crashes during startup:
```bash
docker run --rm -e MAX_CONNECTIONS="not-a-number" -v $(pwd)/phases/14-environment-variables-and-configuration/01-runtime-env-injection/code/configurable_app.py:/app.py python:3.11-slim python3 /app.py
```
Output:
`ValueError: invalid literal for int() with base 10: 'not-a-number'`
This demonstrates the importance of robust environment variable validation and typed schema parsing (e.g. Pydantic or Zod) during startup.

## Debug it
When a container behaves with incorrect settings:
1. Inspect the container's live environment table:
   ```bash
   docker exec <container> env
   ```
2. Inspect the metadata created by Docker Engine:
   ```bash
   docker inspect <container> --format '{{json .Config.Env}}'
   ```
3. Check for shell quoting errors or unescaped characters in your `.env` file.

## Modify it
Create a `test.env` file with `MAX_CONNECTIONS=50` and `DEBUG=true`. Run the container with this file and verify the configuration output.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Configuration outputs across dev and prod profiles.
- Proof of precedence override with `-e`.
- Security warning observation from `docker inspect`.

## Questions for mastery
1. Why should production databases never use hardcoded credentials in Dockerfiles?
2. If environment variables are visible in `docker inspect`, how should sensitive production secrets (TLS private keys, database credentials) be mounted securely?
3. What is the difference between build-time variables (`ARG`) and runtime variables (`ENV`)?

## What comes next
We have mastered files, networks, and configuration. Now we examine operating system control: **How does Docker prevent a rogue program from consuming 100% of host CPU and crashing your machine?** Proceed to **Phase 15: Resource Limits and cgroups**.
