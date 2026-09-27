# Container Troubleshooting & Diagnostic Guide

When a container fails, **do not guess**. Follow this diagnostic protocol to systematically isolate the faulty layer.

---

## 1. The 10-Step Diagnostic Protocol

```text
What was supposed to happen?
  ↓
1. Is the container running?
   $ docker ps -a --filter "name=<target>"
  ↓
2. Why did it exit? (Inspect exit code & status)
   $ docker inspect <target> --format '{{.State.Status}} (ExitCode: {{.State.ExitCode}}, OOMKilled: {{.State.OOMKilled}})'
  ↓
3. What do the process streams say?
   $ docker logs --tail 50 <target>
  ↓
4. What process was executed?
   $ docker inspect <target> --format 'Entrypoint: {{.Path}}, Args: {{json .Args}}'
  ↓
5. Is the process actually listening on the expected port?
   $ docker exec <target> netstat -tuln  (or ss -tuln)
  ↓
6. Is the port bound to 127.0.0.1 (local only) or 0.0.0.0 (all interfaces)?
   (Binding to 127.0.0.1 inside container blocks host/bridge access!)
  ↓
7. Which network is the container attached to?
   $ docker inspect <target> --format '{{json .NetworkSettings.Networks}}'
  ↓
8. Can DNS resolve the peer container?
   $ docker exec <target> nslookup <peer-name>
  ↓
9. Are volume / bind mount permissions aligned?
   $ docker exec <target> ls -la <mount-path>
  ↓
10. Did resource limits starve the process?
   $ docker stats --no-stream
```

---

## 2. Common Exit Codes Decoded

| Exit Code | Meaning | Immediate Diagnostic Action |
| :--- | :--- | :--- |
| **0** | Clean termination. The main process finished its work and exited. | Check if you ran a batch script or server in background. Containers only stay alive as long as PID 1 is running. |
| **1** | Application error / exception. | Check `docker logs <container>`. Look for uncaught exceptions, missing files, or bad config. |
| **127** | Command not found. | The executable in `ENTRYPOINT` or `CMD` does not exist in `$PATH` inside the image, or a binary was compiled for the wrong OS/architecture. |
| **137** | Process terminated by `SIGKILL` (`128 + 9`). | Run `docker inspect <container> --format '{{.State.OOMKilled}}'`. If `true`, the process exceeded its cgroup memory limit and the kernel OOM-killer killed it. Alternatively, `docker stop` timed out after 10s. |
| **139** | Segmentation fault (`SIGSEGV`: `128 + 11`). | Memory corruption in C/C++ libraries or native dependencies (e.g., PyTorch, NumPy binary mismatch). |
| **143** | Clean termination via `SIGTERM` (`128 + 15`). | Normal shutdown when stopped cleanly. |

---

## 3. High-Frequency Failure Modes

### Failure A: "I can ping localhost:8000 on my laptop, but curl gives Connection Refused"
- **Cause 1**: The port was not published with `-p 8000:8000`. Exposing in Dockerfile is not publishing!
- **Cause 2**: Inside the container, the application bound to `127.0.0.1:8000` instead of `0.0.0.0:8000`. Remember: `127.0.0.1` inside a container is only reachable from *within that same container*.
- **Fix**: Reconfigure your server to bind to `0.0.0.0` (all interfaces) and run with `-p 8000:8000`.

### Failure B: "Service A cannot find Service B by name"
- **Cause 1**: Both containers are running on the default `bridge` network. Docker's embedded DNS server is **only enabled on user-defined networks**!
- **Cause 2**: Typo in container name or service name.
- **Fix**: Create a custom bridge network (`docker network create my-net`), and attach both containers with `--network my-net`.

### Failure C: "Database files disappear when I restart or rebuild"
- **Cause**: The database writes data to the ephemeral container writable layer, not a named volume or host bind mount.
- **Fix**: Declare a named volume with `-v my_db_data:/var/lib/postgresql/data`.

### Failure D: "Permission Denied writing to mounted directory"
- **Cause**: The container process runs as non-root user (e.g. `UID 1000`), but the host folder on disk is owned by `root` (or a different host UID).
- **Fix**: Check `id -u` inside the container and ensure the host directory has corresponding ownership or write permissions.
