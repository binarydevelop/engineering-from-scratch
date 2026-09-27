# Exercise Set 09: Services, systemd & Logging

### Ex 9.1: Systemd Service States
Explain the difference between `loaded`, `active (running)`, `active (exited)`, and `failed` in `systemctl status`.

### Ex 9.2: Starting, Stopping, and Reloading
Demonstrate the operational difference between `systemctl restart nginx` and `systemctl reload nginx`. Why is `reload` preferred in production?

### Ex 9.3: Enabling Services at Boot
What physical filesystem operation does `systemctl enable <service>` perform? Inspect `/etc/systemd/system/multi-user.target.wants/` to verify.

### Ex 9.4: Writing a Minimal Service Unit
Create a custom systemd service unit `/etc/systemd/system/lfs-demo.service` that runs a Python script as an unprivileged user, automatically restarting on failure (`Restart=on-failure`).

### Ex 9.5: Systemd Unit Reload Mechanics
Why must you execute `systemctl daemon-reload` after editing a unit file on disk before restarting the service?

### Ex 9.6: Journalctl Service Filtering
Use `journalctl` to view logs for a specific service from the current boot, following new log entries in real-time (`-f`).

### Ex 9.7: Journalctl Time Windows and Priority
Use `journalctl` to extract all error-level (`-p err`) messages across the entire operating system that occurred between 1 hour ago and now.

### Ex 9.8: Systemd Timers vs Cron
Create a systemd timer unit `lfs-backup.timer` configured to trigger a backup service every night at 02:00 UTC. Verify active timers with `systemctl list-timers`.

### Ex 9.9: Debugging a Service with Exit Code 203/EXEC
Create a service whose `ExecStart` points to a non-existent binary or a script without executable permissions. Start the service. Use `systemctl status` and `journalctl` to diagnose exit status 203.

### Ex 9.10: Inspecting Service Cgroups and Resource Limits
Use `systemd-cgls` and `systemctl show <service> -p MemoryCurrent` to inspect the live CPU and memory resources allocated to an active service unit.
