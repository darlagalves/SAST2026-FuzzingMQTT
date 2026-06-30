#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

SEED="${1:-1}"

export REPLAY_LIMIT="${REPLAY_LIMIT:-100}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.05}"
export RESET_PAYLOAD='{"temperature": 22.5}'

REPLAYER="/home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py"

FUZZERS=("boofuzz" "fume" "scapy")

for FUZZER in "${FUZZERS[@]}"; do
    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"

    if [ ! -s "$CORPUS" ]; then
        echo "[SKIP] Corpus vazio ou ausente para $FUZZER"
        continue
    fi

    OUT_DIR="resultados_mutmut/baselines_semantic/sensor/${FUZZER}/seed_${SEED}"
    mkdir -p "$OUT_DIR"

    export FUZZER_NAME="$FUZZER"
    export FUZZER_SEED="$SEED"
    export TRACE_OUT="$OUT_DIR/trace.jsonl"

    echo "===================================================="
    echo "[INFO] Gerando baseline semântica para $FUZZER"
    echo "===================================================="

    docker restart "$HA_CONTAINER" >/dev/null
    sleep 25

    "$REPLAYER"

    echo "[OK] Trace salvo em $TRACE_OUT"
    wc -l "$TRACE_OUT"
done