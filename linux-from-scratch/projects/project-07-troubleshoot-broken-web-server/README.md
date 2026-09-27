# Project 07: Troubleshoot a Broken Web Server

## Scenario
A mission-critical internal web server is reported completely down. Customers receive connection timeouts and 502 Bad Gateway errors. You have root access to the host.

## The Injected Failures
1. The backend application service is failing to start due to a permission denial on `/var/run/app.sock`.
2. Port 8080 is blocked by a rogue debugging script left running.
3. The root filesystem is reporting 100% full due to unlinked deleted files held open by a zombie logger.
4. Nginx configuration has an invalid upstream IP address.

## Triage Walkthrough
Follow the 10-step troubleshooting methodology to diagnose each issue from evidence, apply permanent fixes, and restore full service health.
