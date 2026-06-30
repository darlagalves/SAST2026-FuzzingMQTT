#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <adapter_original>"
    exit 1
fi

ORIGINAL_ADAPTER="$1"

cd /home/darla/experimento
source harness/config/experimento.env

LOG_DIR="/home/darla/experimento/resultados_mutmut/bridge_logs"
mkdir -p "$LOG_DIR"

CAPTURE_FILE="${BRIDGE_CAPTURE_FILE:-}"

echo "[BRIDGE] start $(date) adapter=$ORIGINAL_ADAPTER topic=$MQTT_TOPIC" >> "$LOG_DIR/bridge.log"

mosquitto_sub -R -h "$MQTT_HOST" -p "$MQTT_PORT" -t "#" -v | \
while IFS= read -r line; do
    topic="${line%% *}"
    payload="${line#* }"

    [ "$topic" = "$line" ] && continue
    [ "$topic" = "$MQTT_TOPIC" ] && continue

    if [ -n "$CAPTURE_FILE" ]; then
        printf '%s\n' "$payload" >> "$CAPTURE_FILE"
    fi

    printf '%s\n' "$payload" | mosquitto_pub \
        -h "$MQTT_HOST" \
        -p "$MQTT_PORT" \
        -t "$MQTT_TOPIC" \
        -l || true

    echo "[REPUBLISH] from=$topic to=$MQTT_TOPIC payload=$payload" >> "$LOG_DIR/bridge_republish.log"
done &

BRIDGE_PID=$!

cleanup() {
    kill "$BRIDGE_PID" 2>/dev/null || true
}
trap cleanup EXIT

timeout "${FUZZ_DURATION:-60}s" "$ORIGINAL_ADAPTER" || true
sleep 2
