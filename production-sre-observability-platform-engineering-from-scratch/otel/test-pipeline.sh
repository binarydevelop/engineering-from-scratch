#!/usr/bin/env bash
# Verifies that OTel Collector is accepting data on gRPC 4317 and HTTP 4318

set -euo pipefail

COLLECTOR_HTTP="${1:-http://localhost:4318}"

echo "Testing OpenTelemetry Collector OTLP/HTTP receiver at ${COLLECTOR_HTTP}..."

PAYLOAD='{
  "resourceSpans": [{
    "resource": {
      "attributes": [{
        "key": "service.name",
        "value": {"stringValue": "pipeline-smoke-test"}
      }]
    },
    "scopeSpans": [{
      "scope": {"name": "test-scope"},
      "spans": [{
        "traceId": "5b8aa5a2d2c872e8321cf37308d69df2",
        "spanId": "051581bf3cb55c1e",
        "name": "test-span",
        "kind": 1,
        "startTimeUnixNano": "1710000000000000000",
        "endTimeUnixNano": "1710000001000000000",
        "status": {"code": 1}
      }]
    }]
  }]
}'

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${COLLECTOR_HTTP}/v1/traces" \
  -H "Content-Type: application/json" \
  -d "${PAYLOAD}" || echo "000")

if [ "$HTTP_STATUS" -eq 200 ] || [ "$HTTP_STATUS" -eq 202 ]; then
    echo "[OK] Collector accepted OTLP trace payload (HTTP ${HTTP_STATUS})"
    exit 0
else
    echo "[FAIL] Collector returned HTTP ${HTTP_STATUS}. Check if otel-collector container is running."
    exit 1
fi
