#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

SEED="${1:-1}"

export REPLAY_LIMIT="${REPLAY_LIMIT:-100}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.05}"
export RESET_BEFORE_REPLAY=1
export RESET_PAYLOAD='{"temperature": 22.5}'

REPLAYER="/home/darla/experimento/harness/adapters/run_replay_sensor_corpus.py"

FUZZERS=("boofuzz" "fume" "mqttgram" "mitm" "scapy")

for FUZZER in "${FUZZERS[@]}"; do
    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"

    if [ ! -f "$CORPUS" ]; then
        echo "[SKIP] Corpus não encontrado para $FUZZER"
        continue
    fi

    OUT_DIR="resultados_mutmut/baselines/sensor/${FUZZER}/seed_${SEED}"
    mkdir -p "$OUT_DIR"

    export FUZZER_NAME="$FUZZER"
    export FUZZER_SEED="$SEED"
    export TRACE_OUT="$OUT_DIR/trace.jsonl"

    echo "===================================================="
    echo "[INFO] Gerando baseline trace para $FUZZER seed $SEED"
    echo "[INFO] Saída: $TRACE_OUT"
    echo "===================================================="

    docker restart "$HA_CONTAINER" >/dev/null
    sleep 25

    "$REPLAYER"

    echo "[OK] Baseline salvo: $TRACE_OUT"
    echo "[INFO] Linhas:"
    wc -l "$TRACE_OUT"
done
