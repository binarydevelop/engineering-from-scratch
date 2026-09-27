# Project 09: Linux Application Host (Capstone)

## Objective
From a clean, pristine Linux installation, assemble a complete, production-grade application hosting platform:
1. **User Management**: Create dedicated system user and runtime directories.
2. **Runtime Setup**: Install and configure application runtime environment.
3. **Application Deployment**: Install code under `/opt/production-app`.
4. **Environment Isolation**: Set up configuration files with permissions `0600`.
5. **Systemd Supervision**: Write and enable custom unit file with sandboxing directives.
6. **Reverse Proxying**: Configure Nginx reverse proxy with SSL termination and custom headers.
7. **Log Management**: Configure logrotate for daily rotation and 14-day retention.
8. **Firewall Defense**: Enforce stateful firewall rules.
9. **Automated Health Probe**: Implement watchdog cron job verifying system reachability.
10. **Automated Verification**: Run end-to-end verification script testing the entire stack.
