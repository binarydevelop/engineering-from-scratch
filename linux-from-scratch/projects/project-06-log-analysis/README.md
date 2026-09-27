# Project 06: High-Performance Log Analysis Pipeline

## Objective
Analyze real-world Nginx/Apache web server access logs using standard Linux text stream processing utilities (`awk`, `sed`, `sort`, `uniq`, `cut`):
1. Top 10 client IP addresses with highest request volumes.
2. HTTP response code distribution (Percentage of 200, 301, 404, 500 responses).
3. Top 10 most requested URL endpoints.
4. Hourly traffic distribution across 24 hours.
5. Identify potential brute-force or DDoS attacks (IPs generating >100 requests per minute).
