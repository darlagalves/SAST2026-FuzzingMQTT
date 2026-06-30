#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

SEED="${1:-1}"

# Ajuste se o caminho do template.py for outro
TEMPLATE_TARGET="${TEMPLATE_TARGET:-ha_source/homeassistant/helpers/template.py}"

if [ ! -f "$TEMPLATE_TARGET" ]; then
    echo "[ERRO] Arquivo não encontrado: $TEMPLATE_TARGET"
    echo "Descubra o caminho com:"
    echo "find ha_source/homeassistant -type f | grep -E 'template.py$'"
    exit 1
fi

export CHECK_CORPUS_TRACE=1
export CHECK_STATE_DURING_FUZZ=0
export CHECK_STATE_AFTER_FUZZ=0
export ORACLE_LOG_PATTERNS="__PADRAO_QUE_NUNCA_APARECE__"

export REPLAY_LIMIT="${REPLAY_LIMIT:-100}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.05}"

FUZZERS=("boofuzz" "fume" "scapy")

for FUZZER in "${FUZZERS[@]}"; do
    echo
    echo "===================================================="
    echo "[CAMPANHA TEMPLATE] $FUZZER seed=$SEED"
    echo "===================================================="

    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"
    BASELINE="resultados_mutmut/baselines_semantic/sensor/${FUZZER}/seed_${SEED}/trace.jsonl"

    if [ ! -f "$CORPUS" ]; then
        echo "[SKIP] Sem corpus para $FUZZER: $CORPUS"
        continue
    fi

    COUNT=$(wc -l < "$CORPUS" | tr -d ' ')

    if [ "$COUNT" -lt 5 ]; then
        echo "[SKIP] Corpus pequeno demais para $FUZZER: $COUNT payloads"
        continue
    fi

    if [ ! -f "$BASELINE" ]; then
        echo "[SKIP] Sem baseline semântica para $FUZZER: $BASELINE"
        continue
    fi

    pkill -f mosquitto_sub || true
    pkill -f run_with_sensor_bridge || true
    sleep 2

    ./harness/run_module_campaign.sh \
        template \
        "$TEMPLATE_TARGET" \
        "$FUZZER" \
        /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py \
        "$SEED"
done

echo
echo "===================================================="
echo "[RESUMO TEMPLATE]"
echo "===================================================="

for FUZZER in "${FUZZERS[@]}"; do
    RUN_FILE="resultados_mutmut/template/${FUZZER}/seed_${SEED}/mutmut_run.txt"

    echo "===== $FUZZER ====="

    if [ -f "$RUN_FILE" ]; then
        grep "🎉" "$RUN_FILE" | tail -n 1 || true
    else
        echo "sem campanha"
    fi
done

echo
echo "[OK] Campanhas do template finalizadas."
