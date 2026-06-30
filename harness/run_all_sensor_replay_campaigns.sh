#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

export REPLAY_LIMIT="${REPLAY_LIMIT:-200}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.03}"

SEED="${1:-1}"

REPLAYER="/home/darla/experimento/harness/adapters/run_replay_sensor_corpus.py"

FUZZERS=("boofuzz" "fume" "mqttgram" "mitm" "scapy")

echo "[INFO] Rodando campanhas por replay"
echo "[INFO] Seed: $SEED"
echo "[INFO] REPLAY_LIMIT=$REPLAY_LIMIT"
echo "[INFO] REPLAY_DELAY=$REPLAY_DELAY"

HOST_HASH=$(sha256sum ha_source/homeassistant/components/mqtt/sensor.py | awk '{print $1}')
CONTAINER_HASH=$(docker exec "$HA_CONTAINER" sha256sum /usr/src/homeassistant/homeassistant/components/mqtt/sensor.py | awk '{print $1}')

if [ "$HOST_HASH" != "$CONTAINER_HASH" ]; then
    echo "[ERRO] sensor.py do host e do container estão diferentes."
    exit 1
fi

for f in "${FUZZERS[@]}"; do
    CORPUS="resultados_mutmut/corpus/sensor/$f/seed_$SEED/payloads.jsonl"

    if [ ! -f "$CORPUS" ]; then
        echo "[SKIP] Corpus não existe para $f: $CORPUS"
        continue
    fi

    COUNT=$(wc -l < "$CORPUS" | tr -d ' ')

    if [ "$COUNT" -lt 5 ]; then
        echo "[SKIP] Corpus muito pequeno para $f: $COUNT payloads"
        continue
    fi

    echo "===================================================="
    echo "[INFO] Rodando $f com corpus de $COUNT payloads"
    echo "===================================================="

    ./harness/run_sensor_campaign.sh "$f" "$REPLAYER" "$SEED"
done

if [ -f harness/analysis/build_sensor_summary.py ]; then
    python harness/analysis/build_sensor_summary.py || true
fi

if [ -f harness/analysis/check_sensor_mutant_id_stability.py ]; then
    python harness/analysis/check_sensor_mutant_id_stability.py || true
fi

echo "[OK] Campanhas por replay finalizadas."
