# Project 05: Server Health Monitor CLI

## Objective
Create a standalone Linux diagnostic utility in Bash/Python that collects metrics from kernel virtual filesystems (`/proc`) without relying on brittle screen-scraping of `top`.
- CPU utilization & core counts (`/proc/stat`, `/proc/cpuinfo`)
- Memory metrics: Total, Free, Available, Buffers/Cache (`/proc/meminfo`)
- Load averages & runnable tasks (`/proc/loadavg`)
- Storage capacity & inode pressure (`statvfs`)
- Network socket statistics (`/proc/net/tcp` or `ss`)
- Systemd failed unit detection
