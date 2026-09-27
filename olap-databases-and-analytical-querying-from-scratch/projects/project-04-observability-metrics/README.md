# Project: Observability Analytics Platform

## Overview
Analyze service telemetry, compute p95 and p99 request latencies, and detect failing endpoints.

## Architecture & Mechanics
- **Engine**: DuckDB / ClickHouse / Parquet
- **Core Primitives**: Columnar projection, vectorization, partitioning, aggregations.

## Quickstart
Run the project script:
```bash
.venv/bin/python main.py
```
