# SAFETY & RISK PROTOCOL

Operating systems give privileged users the power to alter disk partitions, drop active network connections, and unrecoverably delete filesystems. This curriculum teaches advanced system administration, failure injection, and debugging, which inherently involves operating near system limits.

---

## Core Safety Invariants

1. **NEVER practice destructive commands on personal host machines.**
   Always practice in an isolated virtual machine (e.g. Multipass, UTM, VirtualBox) or a disposable cloud instance.
2. **NEVER run commands with `sudo` unless the specific lesson explicitly requires root privileges.**
   If an exercise fails with `Permission denied`, diagnosing *why* permissions are denied is the pedagogical goal. Blindly running `sudo` destroys the learning opportunity.
3. **NEVER use `chmod 777` as a quick fix.**
   `chmod 777` disables Linux Discretionary Access Control. It teaches dangerous habits and violates the principle of least privilege.
4. **Use loop devices and disposable images for storage labs.**
   Do not format, resize, or fill real disk partitions. All storage labs in this curriculum use loopback files mounted via `losetup`.
5. **Use network namespaces for network breakage.**
   Do not flush your host firewall rules (`iptables -F` / `nft flush ruleset`) or change your default gateway on a remote SSH session.

---

## Dangerous Commands & Safe Alternatives

| Dangerous Command | Real Risk | Safe Sandbox Pattern Used Here |
| :--- | :--- | :--- |
| `rm -rf /` or `rm -rf $VAR/*` (if unset) | Destroys the host filesystem | Strict Bash quoting, safe sandbox directories under `/tmp/lfs-lab/`, `set -u` |
| `mkfs.ext4 /dev/sda1` | Overwrites disk partitions and data | Create a sparse image file (`dd` or `truncate`) and mount via loopback |
| `iptables -P INPUT DROP` | Instantly locks you out of remote SSH | Test firewall rules inside isolated network namespaces (`ip netns`) |
| `chmod -R 777 /` or `chown -R` | Destroys system security and SUID bits | Confine ownership changes strictly to lab workspaces |
| `:(){ :|:& };:` (Fork bomb) | Exhausts process table, hangs host | Run inside user cgroups with strict `pids.max` limits or disposable VM |
| `dd if=/dev/zero of=/dev/sda` | Wipes storage drives | Write only to allocated loop files (`/tmp/lfs-storage.img`) |

---

## The 5-Step Failure Injection Rule

Whenever an exercise asks you to break something, follow this mandatory structure:

```text
1. RISK:            Identify precisely what resource or state is being altered.
2. EXPECTED IMPACT: Predict what error message or symptom will manifest.
3. SAFE SANDBOX:    Confirm the blast radius is confined to the lab directory or namespace.
4. RECOVERY:        Identify the exact reverse command BEFORE breaking the system.
5. CLEANUP:         Restore the environment to pristine baseline state.
```

---

## Recovery and Lab Reset

If an experiment enters an unrecoverable state:
1. Run the lab cleanup script:
   ```bash
   bash scripts/cleanup.sh
   ```
2. If working inside a virtual machine, revert to your initial snapshot:
   ```bash
   # In Multipass
   multipass delete --purge lfs-lab && multipass launch --name lfs-lab 24.04
   ```
