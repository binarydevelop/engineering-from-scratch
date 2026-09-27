# Project 03: Multi-User Collaboration Server

## Objective
Configure a secure multi-tenant Linux server environment for an engineering team:
1. Create dedicated users: `dev1`, `dev2`, `contractor`.
2. Create collaboration groups: `developers`, `contractors`.
3. Set up a shared project directory: `/data/projects/core`.
4. Configure permissions using SGID (`chmod 2770`) so all newly created files automatically belong to group `developers`.
5. Enforce default umask `0002` or POSIX ACLs to ensure shared group write access.
6. Verify that `contractor` cannot enter or read `/data/projects/core`.
