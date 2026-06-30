#!/usr/bin/env bash
set -e

echo "[VALIDAÇÃO] Forçando parada do container $HA_CONTAINER"
docker stop "$HA_CONTAINER"
sleep 2
exit 0
