# Lesson 28.5: Debugging Lab 05 — Permission Denied on Mount

## Motto
"Linux permissions evaluate numeric UIDs across mount boundaries; align host and container UIDs to eliminate `EACCES`."

## Problem
**Symptom:**
Following best practices from Phase 25, a backend team configures their container image to run as unprivileged `USER 10001:10001`.
They deploy the container with a host bind mount: `-v /var/data/logs:/data`.
On boot, the application crashes with:
`PermissionError: [Errno 13] Permission denied: '/data/audit.log'`
The developer checks their terminal on the host machine, and they can write to `/var/data/logs` without issue!
Why does the host user have write access while the container user is blocked?

## Prediction
1. Does the Linux kernel check username strings (like "appuser" vs "tushar") or raw integer UIDs (like 10001 vs 501)?
2. If host directory permissions are `rwxr-xr-x` (755), can an arbitrary non-owner UID write to it?
3. How can you inspect the current UID of a container process?

## Why this matters
UID/GID mismatch on mounted volumes is the single most common cause of storage failures when transitioning from root development images to hardened production containers.

## First principles
1. **Numeric UID Evaluation**:
   The Linux filesystem layer does not care what username string exists in `/etc/passwd`. It compares the **effective UID (eUID)** of the calling process against the numeric owner UID and POSIX mode bits of the target file/directory.
2. **The 755 Trap**:
   Mode `755` means:
   - Owner (UID X): `rwx` (read, write, execute)
   - Group (GID Y): `r-x` (read, execute)
   - Other: `r-x` (read, execute - **NO WRITE**)
   If the container process runs as UID `10001` and is neither the owner nor in the group, the kernel returns `EACCES` (Permission denied).

## Mental model
```
Host Directory (/data on host):
Owner UID = 501 (host user) | Mode = 755 (rwxr-xr-x)
                 ▲
                 │ (Bind Mount into Container)
                 ▼
Container Process:
Effective UID = 10001 (appuser)
Kernel check: Is 10001 == 501? NO.
              Is 10001 in group? NO.
              Does 'Other' have write permission (w)? NO.
              Result: open("/data/audit.log", O_WRONLY) -> EACCES (Permission Denied)
```

## Build it
Review `writer.py` in `code/`.
It attempts to append a timestamped log to `/data/audit.log`.

## Run it
Execute the lab runner:

```bash
./phases/28-container-debugging-without-magic/lab-05-permissions-mount/experiments/run_experiment.sh
```

## Inspect it
1. Observe Step 1: The container exits with exit code 13 (`Permission denied`).
2. Run `ls -ld /tmp/dfs_lab05_restricted_dir`. Notice that only the host owner has write permissions.
3. In Step 4: After granting write access, the container writes successfully.

## Break it
Mount a directory with read-only flag `:ro` and attempt to create a file inside it:
Notice that even `root` (UID 0) receives `Read-only file system`.

## Debug it
1. Hypothesis: The process running in the container has an eUID that lacks write permissions on the mounted directory.
2. Check container UID: `docker run --rm <image> id -u`.
3. Check host directory owner and mode: `ls -ld <path-on-host>`.
4. Fix options:
   - Run container matching host user: `--user $(id -u):$(id -g)`.
   - Update host folder ownership: `chown -R 10001:10001 <path>`.

## Modify it
Run the container passing `--user $(id -u):$(id -g)` without changing the folder permissions. Verify it writes cleanly.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The `PermissionError` message.
- Explanation of numeric UID evaluation.
- Verification of the fixed permissions.

## Questions for mastery
1. Why does running as `root` (UID 0) in development mask permissions bugs that explode in production?
2. How do User Namespaces (`userns-remap`) change UID evaluation?

## What comes next
In the next lab, a service cannot communicate with its database because of a DNS resolution failure. Proceed to **Lab 06: DNS Resolution Failure**.
