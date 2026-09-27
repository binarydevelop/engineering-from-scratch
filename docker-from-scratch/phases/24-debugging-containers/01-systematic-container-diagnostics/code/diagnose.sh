#!/usr/bin/env bash
# diagnose.sh
# Automated implementation of the 10-Step Container Diagnostic Protocol.

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: ./diagnose.sh <CONTAINER_NAME_OR_ID>"
    exit 1
fi

TARGET="$1"

echo "============================================================"
echo "    SYSTEMATIC CONTAINER DIAGNOSTIC REPORT: $TARGET"
echo "============================================================"

# 1. Existence & Status
if ! docker inspect "$TARGET" >/dev/null 2>&1; then
    echo "[CRITICAL] Container '$TARGET' does not exist in Docker engine!"
    exit 1
fi

STATUS=$(docker inspect "$TARGET" --format '{{.State.Status}}')
RUNNING=$(docker inspect "$TARGET" --format '{{.State.Running}}')
EXIT_CODE=$(docker inspect "$TARGET" --format '{{.State.ExitCode}}')
OOM_KILLED=$(docker inspect "$TARGET" --format '{{.State.OOMKilled}}')

echo "1. Container Lifecycle State:"
echo "   Status:     $STATUS"
echo "   Running:    $RUNNING"
echo "   ExitCode:   $EXIT_CODE"
echo "   OOMKilled:  $OOM_KILLED"

if [ "$OOM_KILLED" = "true" ]; then
    echo "   [ROOT CAUSE DETECTED] Process exceeded memory limit and was killed by OOM killer!"
elif [ "$STATUS" = "exited" ] && [ "$EXIT_CODE" -ne 0 ]; then
    echo "   [ROOT CAUSE DETECTED] Process exited with error code $EXIT_CODE!"
fi

# 2. Executed Entrypoint & Command
echo ""
echo "2. Executable & Arguments:"
ENTRYPOINT=$(docker inspect "$TARGET" --format '{{json .Config.Entrypoint}}')
CMD=$(docker inspect "$TARGET" --format '{{json .Config.Cmd}}')
PATH_VAL=$(docker inspect "$TARGET" --format '{{.Path}}')
ARGS_VAL=$(docker inspect "$TARGET" --format '{{json .Args}}')
echo "   Config.Entrypoint: $ENTRYPOINT"
echo "   Config.Cmd:        $CMD"
echo "   Executed:          $PATH_VAL $ARGS_VAL"

# 3. Environment Summary
echo ""
echo "3. Environment Variables (Count: $(docker inspect "$TARGET" --format '{{len .Config.Env}}')):"
docker inspect "$TARGET" --format '{{range .Config.Env}}     - {{println .}}{{end}}' | head -n 8

# 4. Networking & Published Ports
echo ""
echo "4. Network Configuration:"
docker inspect "$TARGET" --format '{{range $net, $val := .NetworkSettings.Networks}}   Network: {{$net}} | IP: {{$val.IPAddress}} | Gateway: {{$val.Gateway}}{{println}}{{end}}'
echo "   Port Bindings:"
docker inspect "$TARGET" --format '{{range $port, $bind := .NetworkSettings.Ports}}     - Container {{$port}} -> Host {{json $bind}}{{println}}{{end}}'

# 5. Mounts & Storage
echo ""
echo "5. Mounts & Filesystem:"
docker inspect "$TARGET" --format '{{range .Mounts}}   Type: {{.Type}} | Source: {{.Source}} -> Target: {{.Destination}} (RW: {{.RW}}){{println}}{{end}}'

# 6. Tail Logs
echo ""
echo "6. Recent Process Output (stdout & stderr):"
echo "------------------------------------------------------------"
docker logs --tail 10 "$TARGET" 2>&1 || echo "   (No logs available)"
echo "------------------------------------------------------------"

echo ""
echo "Diagnostic analysis complete."
