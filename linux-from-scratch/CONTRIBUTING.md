# Contributing to linux-from-scratch

Thank you for helping make `linux-from-scratch` the highest-quality, first-principles Linux curriculum available.

---

## Guiding Principles

1. **First Principles Over Memorization**: Never introduce a command as "run this to do that." Always explain what question we are asking, what Linux object holds the answer, and which tool inspects it.
2. **Safety First**: Every failure injection experiment must be completely isolated (namespaces, loop devices, `/tmp/` sandboxes, or VMs).
3. **Strict Lesson Structure**: All lessons must follow [LESSON_TEMPLATE.md](file:///Users/tushar/Desktop/private/repos/linux-from-scratch/LESSON_TEMPLATE.md).
4. **Defensive Scripting**: All Bash scripts must include `set -euo pipefail`, proper quoting, and cleanup traps.
5. **No Cargo Culting**: Never recommend `chmod 777`, blind `sudo`, or unexamined service restarts.

---

## Submitting New Content or Fixes

1. Verify that scripts run cleanly on Ubuntu 24.04 LTS / Debian 12.
2. Run shellcheck on all scripts:
   ```bash
   shellcheck scripts/*.sh exercises/*/*.sh
   ```
3. Test that broken system scenarios can be reproduced and verified cleanly:
   ```bash
   bash broken-systems/scenario-01-web-server-port-conflict/setup.sh
   bash broken-systems/scenario-01-web-server-port-conflict/verify.sh
   ```
