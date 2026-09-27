# Lesson: Debugging Container DNS Resolution Failure

## Motto
"Containers do not resolve each other by magic; they require Docker's embedded DNS server (127.0.0.11), which only exists on user-defined networks."

## Problem
An engineer deploys two containers that need to communicate: an application and a cache service. When the application attempts to connect to `http://cache:6379` or resolve `cache`, the call immediately fails with:
```
socket.gaierror: [Errno -2] Name or service not known
```
The developer verifies that both containers are running via `docker ps` and that both have IP addresses assigned. Why does hostname resolution completely fail even though the containers are running on the same machine?

## Prediction
If containers are attached to the default Docker bridge network (`bridge` / `docker0`), DNS resolution using container names will fail. When attached to a user-defined bridge network, Docker will configure `/etc/resolv.conf` to use `127.0.0.11`, enabling container name resolution.

## Why this matters
In production microservices and local Compose environments, services must discover one another dynamically without hardcoding volatile container IP addresses. Understanding why DNS resolution succeeds in Compose by default but fails when using default Docker CLI flags (`docker run`) prevents elusive networking bugs and flawed network configurations.

## First principles
1. **The Default Bridge (`docker0`):** Historically, Docker's default bridge network did not support automatic service discovery via DNS. It only supported static `/etc/hosts` injection via the deprecated `--link` flag.
2. **User-Defined Bridge Networks:** When you create a custom bridge network (`docker network create` or via Docker Compose), Docker starts an embedded DNS server inside the daemon listening on loopback IP `127.0.0.11` within the container's network namespace.
3. **`/etc/resolv.conf` Configuration:**
   - On the default bridge, `/etc/resolv.conf` mirrors the host's DNS settings (e.g. `192.168.65.7` or upstream DNS). Host DNS servers have no knowledge of local container names.
   - On custom networks, `/etc/resolv.conf` has `nameserver 127.0.0.11`. Any request for a container name or service alias is intercepted and resolved by Docker daemon's internal DNS table.

## Mental model
```
Default Bridge (No 127.0.0.11):
Container A ---> /etc/resolv.conf (Upstream DNS: 1.1.1.1) ---> "cache?" ---> NXDOMAIN!

User-Defined Bridge:
Container A ---> /etc/resolv.conf (127.0.0.11) ---> Docker Daemon DNS Table ---> 172.18.0.2!
```

## Build it
1. `code/app.py`: A diagnostic client that attempts to resolve a target hostname using `socket.gethostbyname()`.
2. `code/docker-compose.yml`: A broken compose file specifying `network_mode: "bridge"`, reproducing the legacy behavior.
3. `code/docker-compose.fixed.yml`: A fixed compose file creating and attaching to a custom bridge network `lab06-net`.

## Run it
Run the experiment script:
```bash
./phases/28-container-debugging-without-magic/lab-06-dns-resolution/experiments/run_experiment.sh
```

## Inspect it
Compare `/etc/resolv.conf` across both network modes:
```bash
# In default bridge:
docker exec <container> cat /etc/resolv.conf
# Output: nameserver 192.168.65.7 (Host DNS)

# In user-defined bridge:
docker exec <container> cat /etc/resolv.conf
# Output: nameserver 127.0.0.11 (Embedded DNS)
```

## Break it
Force a container in Compose to use `network_mode: bridge` or run standalone containers with `docker run -d --name cache alpine sleep 3600` without specifying `--network`. Try resolving `cache` from another standalone container.

## Debug it
1. Run `docker exec -it <app> cat /etc/resolv.conf`. Does it contain `nameserver 127.0.0.11`? If not, the container is on the default bridge.
2. Run `docker network ls` and `docker inspect <container>` to verify the network attachments under `.NetworkSettings.Networks`.
3. Test DNS resolution manually using `nslookup`, `dig`, or `getent hosts <target>`.

## Modify it
Add multiple aliases to a service in `docker-compose.fixed.yml` using `networks.lab06-net.aliases: [my-cache, redis-primary]`. Verify that `python /app.py my-cache` resolves to the same IP.

## Evidence
Running `run_experiment.sh` produces:
```
[*] Attempting to resolve hostname: lab06-broken-cache...
[-] ERROR: Failed to resolve 'lab06-broken-cache': [Errno -2] Name or service not known
[-] First Principles Diagnostic: Embedded DNS (127.0.0.11) is inactive on the default bridge.
[+] CONFIRMED: Embedded DNS 127.0.0.11 is ABSENT on default bridge.
[+] CONFIRMED: Embedded DNS 127.0.0.11 is ACTIVE on user-defined bridge.
[*] Attempting to resolve hostname: cache...
[+] SUCCESS: Resolved 'cache' to IP 172.18.0.2
```

## Questions for mastery
1. Why didn't the Docker team simply add 127.0.0.11 to the default bridge network?
2. What happens to requests for external hostnames like `google.com` when sent to `127.0.0.11`?
3. How does Docker handle round-robin DNS when multiple containers share the same network alias?

## What comes next
In Lab 07, we explore the startup dependency race condition: why `depends_on` alone does not prevent application crashes during database initialization.
