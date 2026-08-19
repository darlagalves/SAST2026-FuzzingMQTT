#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

SEED="${1:-1}"

export REPLAY_LIMIT="${REPLAY_LIMIT:-100}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.05}"
export RESET_PAYLOAD='{"temperature": 22.5}'

FUZZERS=("boofuzz" "fume" "scapy")

OUT_DIR="resultados_mutmut/coverage_mqtt"
mkdir -p "$OUT_DIR"

echo "[INFO] Habilitando coverage no HA..."
docker exec "$HA_CONTAINER" sh -lc \
"touch /tmp/enable_ha_coverage && rm -f /tmp/.coverage.ha /tmp/coverage_mqtt.json /tmp/coverage_debug.log"

docker restart "$HA_CONTAINER" >/dev/null
sleep 35

echo "[INFO] Debug após boot:"
docker exec "$HA_CONTAINER" sh -lc \
"cat /tmp/coverage_debug.log 2>/dev/null || echo 'sem coverage_debug.log'"

HA_PID=$(docker exec "$HA_CONTAINER" sh -lc \
"pgrep -f 'python3 -m homeassistant' | head -n 1")

if [ -z "$HA_PID" ]; then
    echo "[ERRO] Não encontrei PID do Home Assistant."
    docker exec "$HA_CONTAINER" ps aux
    exit 1
fi

echo "[INFO] HA PID=$HA_PID"

for FUZZER in "${FUZZERS[@]}"; do
    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"

    if [ ! -f "$CORPUS" ]; then
        echo "[SKIP] Sem corpus para $FUZZER"
        continue
    fi

    COUNT=$(wc -l < "$CORPUS" | tr -d ' ')

    if [ "$COUNT" -lt 5 ]; then
        echo "[SKIP] Corpus pequeno demais para $FUZZER: $COUNT"
        continue
    fi

    echo "===================================================="
    echo "[COVERAGE] Replay MQTT com $FUZZER"
    echo "===================================================="

    export FUZZER_NAME="$FUZZER"
    export FUZZER_SEED="$SEED"
    unset TRACE_OUT

    /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py
done

echo "[INFO] Salvando coverage do processo HA..."
docker exec "$HA_CONTAINER" kill -USR1 "$HA_PID" || true
sleep 5

echo "[INFO] Desativando sitecustomize antes de qualquer comando python/coverage..."
docker exec "$HA_CONTAINER" rm -f /tmp/enable_ha_coverage
sleep 1

echo "[INFO] Arquivos gerados:"
docker exec "$HA_CONTAINER" sh -lc \
"ls -lh /tmp/.coverage.ha /tmp/coverage_debug.log 2>/dev/null || true"

echo "[INFO] Debug coverage:"
docker exec "$HA_CONTAINER" sh -lc \
"cat /tmp/coverage_debug.log 2>/dev/null || true"

echo "[INFO] Copiando .coverage.ha bruto para backup..."
docker cp "$HA_CONTAINER:/tmp/.coverage.ha" "$OUT_DIR/.coverage.ha"

echo "[INFO] Coverage debug data:"
docker exec "$HA_CONTAINER" sh -lc \
"COVERAGE_FILE=/tmp/.coverage.ha python3 -m coverage debug data" || true

echo "[INFO] Gerando coverage JSON..."
docker exec "$HA_CONTAINER" sh -lc \
"COVERAGE_FILE=/tmp/.coverage.ha python3 -m coverage json -o /tmp/coverage_mqtt.json --ignore-errors"

docker cp "$HA_CONTAINER:/tmp/coverage_mqtt.json" "$OUT_DIR/coverage_mqtt.json"

echo "[INFO] Reiniciando container normalmente..."
docker restart "$HA_CONTAINER" >/dev/null
sleep 25

echo "[OK] Coverage salvo em: $OUT_DIR/coverage_mqtt.json"
