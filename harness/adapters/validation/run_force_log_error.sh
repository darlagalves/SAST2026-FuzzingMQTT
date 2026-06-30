#!/usr/bin/env bash
set -e

echo "[VALIDAÇÃO] Injetando erro artificial no stderr do processo principal"

docker exec "$HA_CONTAINER" sh -c \
'echo "ERROR [homeassistant.components.mqtt] VALIDATION_EXCEPTION Traceback Exception" > /proc/1/fd/2'

sleep 2
exit 0
