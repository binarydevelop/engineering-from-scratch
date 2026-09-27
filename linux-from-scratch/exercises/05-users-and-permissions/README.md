# Exercise Set 05: Users, Groups & Permissions

### Ex 5.1: Inspecting User & Group Identity
Inspect your current user's UID, primary GID, and list of all supplementary group memberships using `id`.

### Ex 5.2: The Directory Traversal Trap
Create a directory `/tmp/lfs-lab/private` with mode `0644` (read and write, but NO execute). Try to `cd` into it or read a file inside it. Explain why access is denied despite having read permissions!

### Ex 5.3: Symbolic vs Numeric chmod
Given a file with mode `0600`, grant group read access and other read access using both symbolic syntax (`g+r,o+r`) and numeric octal syntax (`644`).

### Ex 5.4: Umask Calculation
If your current shell umask is `0022`, what will be the exact permission modes of a newly created regular file (`touch`) and a newly created directory (`mkdir`)? Test and verify.

### Ex 5.5: Setting a Restrictive Umask
Change your umask to `0077`. Create a new file and directory. Prove that no other user on the system can read, write, or enter them.

### Ex 5.6: The Setgid Directory for Shared Teams
Create a collaboration directory `/tmp/lfs-lab/team_share`. Configure the directory with the SGID bit (`chmod 2775`). Prove that any file created inside automatically inherits the directory's group owner, regardless of who creates it.

### Ex 5.7: The Sticky Bit on Shared Directories
Inspect `/tmp`. What is its numeric permission mode? Why is the sticky bit (`1777` / `t`) critical on directories where multiple unprivileged users can create files?

### Ex 5.8: SUID Binary Audit
Find all SUID binaries on your system (`chmod 4000`). Explain why `/usr/bin/passwd` must have the SUID bit set to allow non-root users to change their passwords.

### Ex 5.9: Sudo Command Restriction
Inspect your user's sudo privileges using `sudo -l`. Explain how `/etc/sudoers` can allow an operator to run `systemctl restart nginx` without giving them full root shell access.

### Ex 5.10: Diagnosing Multi-Level Access Denials
Given a path `/data/apps/service/config.yaml`, a process running as user `app` gets `Permission denied`. List the exact command to test read/traversal permissions on every directory component in the chain.
