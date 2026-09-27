#!/usr/bin/env bash
# trace_events.sh
# Streams Docker daemon events to record the exact API sequence of Compose.
set -euo pipefail

docker events --format 'EVENT: type={{.Type}} action={{.Action}} name={{.Actor.Attributes.name}}'
