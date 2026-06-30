#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

SEED="${1:-1}"

export FUZZ_DURATION="${FUZZ_DURATION:-60}"
export REPLAY_LIMIT="${REPLAY_LIMIT:-100}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.05}"

export CHECK_CORPUS_TRACE=1
export CHECK_STATE_DURING_FUZZ=0
export CHECK_STATE_AFTER_FUZZ=0
export ORACLE_LOG_PATTERNS="__PADRAO_QUE_NUNCA_APARECE__"

declare -A ADAPTERS
ADAPTERS[boofuzz]="/home/darla/experimento/harness/adapters/run_boofuzz_sensor.sh"
ADAPTERS[fume]="/home/darla/experimento/harness/adapters/run_fume_sensor.sh"
ADAPTERS[mqttgram]="/home/darla/experimento/harness/adapters/run_mqttgram_sensor.sh"
ADAPTERS[mitm]="/home/darla/experimento/harness/adapters/run_mitm_sensor.sh"
ADAPTERS[scapy]="/home/darla/experimento/harness/adapters/run_scapy_sensor.sh"

FUZZERS=("boofuzz" "fume" "mqttgram" "mitm" "scapy")

echo "===================================================="
echo "[FASE 1] Coletando corpora"
echo "===================================================="

for FUZZER in "${FUZZERS[@]}"; do
    echo
    echo "===================================================="
    echo "[COLETA] $FUZZER"
    echo "===================================================="

    pkill -f mosquitto_sub || true
    pkill -f run_with_sensor_bridge || true
    sleep 2

    rm -rf "resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}"

    ./harness/corpus/collect_sensor_corpus.sh \
        "$FUZZER" \
        "${ADAPTERS[$FUZZER]}" \
        "$SEED" || true

    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"

    if [ -f "$CORPUS" ]; then
        COUNT=$(wc -l < "$CORPUS" | tr -d ' ')
    else
        COUNT=0
    fi

    echo "[INFO] Corpus $FUZZER: $COUNT payloads"
done

echo
echo "===================================================="
echo "[FASE 2] Gerando baselines semânticas"
echo "===================================================="

for FUZZER in "${FUZZERS[@]}"; do
    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"

    if [ ! -f "$CORPUS" ]; then
        echo "[SKIP] $FUZZER sem corpus"
        continue
    fi

    COUNT=$(wc -l < "$CORPUS" | tr -d ' ')

    if [ "$COUNT" -lt 5 ]; then
        echo "[SKIP] $FUZZER corpus pequeno demais: $COUNT payloads"
        continue
    fi

    echo
    echo "===================================================="
    echo "[BASELINE] $FUZZER"
    echo "===================================================="

    OUT_DIR="resultados_mutmut/baselines_semantic/sensor/${FUZZER}/seed_${SEED}"
    mkdir -p "$OUT_DIR"

    export FUZZER_NAME="$FUZZER"
    export FUZZER_SEED="$SEED"
    export TRACE_OUT="/home/darla/experimento/${OUT_DIR}/trace.jsonl"
    export RESET_PAYLOAD='{"temperature": 22.5}'

    rm -f "$TRACE_OUT"

    docker restart "$HA_CONTAINER" >/dev/null
    sleep 25

    /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py

    if [ -f "$TRACE_OUT" ]; then
        wc -l "$TRACE_OUT"
    else
        echo "[ERRO] Baseline não gerada para $FUZZER"
    fi
done

echo
echo "===================================================="
echo "[FASE 3] Rodando campanhas mutmut"
echo "===================================================="

for FUZZER in "${FUZZERS[@]}"; do
    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"
    BASELINE="resultados_mutmut/baselines_semantic/sensor/${FUZZER}/seed_${SEED}/trace.jsonl"

    if [ ! -f "$CORPUS" ]; then
        echo "[SKIP] $FUZZER sem corpus"
        continue
    fi

    COUNT=$(wc -l < "$CORPUS" | tr -d ' ')

    if [ "$COUNT" -lt 5 ]; then
        echo "[SKIP] $FUZZER corpus pequeno demais: $COUNT payloads"
        continue
    fi

    if [ ! -f "$BASELINE" ]; then
        echo "[SKIP] $FUZZER sem baseline semântica"
        continue
    fi

    echo
    echo "===================================================="
    echo "[CAMPANHA] $FUZZER"
    echo "===================================================="

    ./harness/run_sensor_campaign.sh \
        "$FUZZER" \
        /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py \
        "$SEED"
done

echo
echo "===================================================="
echo "[RESUMO]"
echo "===================================================="

for FUZZER in "${FUZZERS[@]}"; do
    RUN_FILE="resultados_mutmut/sensor/${FUZZER}/seed_${SEED}/mutmut_run.txt"

    echo "===== $FUZZER ====="

    if [ -f "$RUN_FILE" ]; then
        grep "🎉" "$RUN_FILE" | tail -n 1 || true
    else
        echo "sem campanha"
    fi
done

echo
echo "[OK] Pipeline finalizado."
