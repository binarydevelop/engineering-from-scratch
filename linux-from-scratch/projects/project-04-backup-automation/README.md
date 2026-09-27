# Project 04: Production Backup Automation Suite

## Objective
Build a robust, production-ready backup script with strict error handling, checksum validation, and automated restore testing:
- Compresses directories into timestamped tarballs (`.tar.gz`)
- Generates SHA-256 integrity verification files
- Implements retention policy pruning archives older than N days
- Runs an automated restore verification drill into a temporary sandbox
- Alerts via exit code on any failure
