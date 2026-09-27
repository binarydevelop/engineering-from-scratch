# Project 01: Build a Linux Service

## Objective
Design, package, and deploy a production-ready background microservice on Linux following Unix daemon best practices:
- Installed under `/opt/lfs-api`
- Runs under a dedicated, unprivileged system account (`lfs-service`) with no interactive login shell (`/usr/sbin/nologin`)
- Supervised by a native systemd unit file (`/etc/systemd/system/lfs-api.service`)
- Environment variables separated into an external configuration file
- Logs directed to `stdout`/`stderr` captured transparently by `journald`
- Automatic restart behavior on failure with backoff rate-limiting

---

## Architecture

```text
       systemd (PID 1)
             │
             │ forks & drops privileges (User=lfs-service)
             ▼
   /usr/bin/python3 /opt/lfs-api/server.py
             │
             ├── Binds to 0.0.0.0:8080 (TCP socket)
             ├── Reads config: /etc/lfs-api/server.env
             └── Writes logs -> stdout -> systemd-journald
```

---

## File Deliverables
1. `server.py`: Minimal Python HTTP application responding with JSON health metrics.
2. `lfs-api.service`: Systemd service unit definition.
3. `server.env`: Configuration file containing port and environment settings.
4. `deploy.sh`: Automated idempotent deployment script.
