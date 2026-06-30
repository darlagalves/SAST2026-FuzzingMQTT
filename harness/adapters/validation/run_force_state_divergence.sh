#!/usr/bin/env bash
set -e

echo "[VALIDAÇÃO] run_force_state_divergence.sh EXECUTADO"
echo "[VALIDAÇÃO] MQTT_HOST=$MQTT_HOST"
echo "[VALIDAÇÃO] MQTT_PORT=$MQTT_PORT"
echo "[VALIDAÇÃO] MQTT_TOPIC=$MQTT_TOPIC"

mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
-t "$MQTT_TOPIC" \
-m '{"temperature": 99.9}'

echo "[VALIDAÇÃO] Payload 99.9 publicado"
sleep 3
exit 0
