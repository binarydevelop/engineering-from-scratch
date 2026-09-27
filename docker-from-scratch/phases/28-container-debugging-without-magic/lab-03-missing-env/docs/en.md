# Lesson 28.3: Debugging Lab 03 — Missing Environment Variable

## Motto
"Inspect standard error logs first; unhandled configuration keys reveal themselves immediately in the stack trace."

## Problem
**Symptom:**
An API service was deployed using `docker compose up -d`.
The command returned code 0.
However, two seconds later, `docker compose ps` reports the service in state `Exited (1)`.
The developer wonders if there is a port issue or network bug.
What caused the container to exit with code 1?

## Prediction
1. What does exit code 1 generally signify in a Python container?
2. Where does Python print uncaught exceptions?
3. How can you inspect environment variables passed to the container?

## Why this matters
Modern 12-factor microservices read database credentials, third-party API keys, and feature flags from environment variables. Failing to provide a mandatory environment variable causes immediate startup crashes that are easily misdiagnosed as networking failures.

## First principles
When a Python process looks up `os.environ["KEY"]` and the key is not defined, Python raises `KeyError`. Because the exception is uncaught at the module level, Python prints a traceback to `stderr` and terminates PID 1 with exit code `1`.

## Mental model
```
Host Environment / Compose Env Block
                  │
                  ▼
Docker Engine passes envp array to execve()
                  │
                  ▼
Python process reads os.environ["API_SECRET_KEY"]
                  │
         ├── Found? ──► Continues booting (ExitCode 0 / Running)
         └── Missing? ─► KeyError -> stderr -> Process Death (ExitCode 1)
```

## Build it
Review `code/app.py` and `code/docker-compose.yml`.
Notice `os.environ["API_SECRET_KEY"]` without a default value, and the absence of the key in `docker-compose.yml`.

## Run it
Execute the lab runner:

```bash
./phases/28-container-debugging-without-magic/lab-03-missing-env/experiments/run_experiment.sh
```

## Inspect it
1. Observe that `docker compose ps -a` shows `Exited (1)`.
2. Inspect `docker compose logs api`.
   Notice the line: `KeyError: 'API_SECRET_KEY'`.
3. Inspect `docker inspect <container> --format '{{json .Config.Env}}'`.
   Notice `API_SECRET_KEY` is completely missing.

## Break it
Inject an empty string `-e API_SECRET_KEY=""` and see if the app crashes or succeeds.

## Debug it
1. Formulate Hypothesis: *The container exited with code 1 due to an application crash or missing configuration.*
2. Check logs: `docker compose logs <service>`.
3. Add the missing variable to `environment:` in `compose.yaml`.

## Modify it
Update `app.py` to provide a sensible fallback: `os.environ.get("API_SECRET_KEY", "dev-default")` so the app boots in local development without crashing.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The `KeyError` traceback from `docker compose logs`.
- Verification of successful boot after injecting the variable.

## Questions for mastery
1. Why is `os.environ.get("KEY", default)` safer than `os.environ["KEY"]` during development?
2. In production, should a service crash early if a critical secret is missing? Why?

## What comes next
In the next lab, a service is running and listening, but external requests are rejected because of host interface binding. Proceed to **Lab 04: The Localhost Trap**.
