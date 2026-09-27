# The 10-Step Systematic Troubleshooting Methodology

> When a server misbehaves in production, panic produces catastrophic outages: rebooting destroys volatile evidence, `chmod 777` creates security holes, and restarting services can deadlock databases. Follow this scientific, evidence-based triage workflow.

---

## The 10-Step Triage Tree

```text
       ┌────────────────────────┐
       │ 1. Define the Symptom  │  Objective, reproducible problem statement
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 2. What Changed?       │  Deployments, package upgrades, config edits
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 3. Isolate the Layer   │  HW -> Kernel -> Net -> FS -> Process -> App
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 4. Read-Only Inspect   │  Gather logs, metrics, socket states (/proc)
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 5. Form Hypothesis     │  Falsifiable prediction of root cause
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 6. Test Hypothesis     │  Targeted probe (strace, curl, namei, dig)
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 7. Apply Targeted Fix  │  Minimal required change (no blunt force)
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 8. Verify End-to-End   │  Prove service responds and metrics normalize
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 9. Clean Up Probes     │  Terminate debug daemons, remove test files
       └───────────┬────────────┘
                   ▼
       ┌────────────────────────┐
       │ 10. Automate & Alert   │  Add monitor check so it never happens again
       └────────────────────────┘
```

---

## Diagnostic Checklist by Symptom

### 1. "Website / API is down (Connection Refused)"
1. **Is the machine responding to ICMP?** -> `ping <ip>`
2. **Is the network interface healthy?** -> `ip addr`, `ip route`
3. **Is the web service process alive?** -> `systemctl status nginx`, `ps aux | grep nginx`
4. **Is the service actually listening on the port?** -> `ss -lntp | grep :80`
5. **Is the port listening on `127.0.0.1` instead of `0.0.0.0`?** -> Sockets bound to localhost cannot accept external traffic!
6. **Is local firewall rejecting packets?** -> `sudo iptables -L -n -v` or `sudo nft list ruleset`

### 2. "Disk Full (`No space left on device`)"
1. **Check block allocation**: `df -hT` (Look for 100% usage).
2. **Check inode allocation**: `df -i` (If inodes are 100%, disk blocks can be empty, but file creation fails!).
3. **Find large directories**: `du -ahx / | sort -rh | head -20`
4. **Check for deleted unlinked files held by running processes**:
   ```bash
   lsof +L1
   ```
   *If a process writes to `/var/log/app.log` and you run `rm /var/log/app.log`, the space is NOT freed until the process closes the file descriptor or restarts!*

### 3. "High CPU / System Unresponsive"
1. **Check load averages**: `uptime` (Compare 1, 5, 15 min load to CPU core count).
2. **Break down CPU states**: `top` (Inspect `us`=user, `sy`=kernel syscalls, `wa`=I/O wait, `si`=software interrupts).
3. **Identify rogue processes**: `ps aux --sort=-%cpu | head -10`
4. **Is it high I/O wait?**: `vmstat 1 5` (Check `b` column for processes in uninterruptible disk sleep `D`).
