#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 5 ]; then
    echo "Uso: $0 <module_name> <target_path> <fuzzer_name> <adapter_path> <seed>"
    echo "Exemplo:"
    echo "$0 template ha_source/homeassistant/helpers/template.py boofuzz /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py 1"
    exit 1
fi

MODULE_NAME="$1"
TARGET_PATH="$2"
FUZZER_NAME="$3"
ADAPTER_PATH="$4"
SEED="$5"

cd /home/darla/experimento
source harness/config/experimento.env

if [ ! -f "$TARGET_PATH" ]; then
    echo "[ERRO] Arquivo alvo não existe: $TARGET_PATH"
    exit 1
fi

export MODULE_UNDER_MUTATION="$MODULE_NAME"
export FUZZER_NAME="$FUZZER_NAME"
export FUZZER_CMD="$ADAPTER_PATH"
export FUZZER_SEED="$SEED"

export REPLAY_LIMIT="${REPLAY_LIMIT:-100}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.05}"
export RESET_PAYLOAD='{"temperature": 22.5}'

export CHECK_CORPUS_TRACE=1
export CHECK_STATE_DURING_FUZZ=0
export CHECK_STATE_AFTER_FUZZ=0
export ORACLE_LOG_PATTERNS="${ORACLE_LOG_PATTERNS:-__PADRAO_QUE_NUNCA_APARECE__}"

OUT_DIR="resultados_mutmut/${MODULE_NAME}/${FUZZER_NAME}/seed_${SEED}"
mkdir -p "$OUT_DIR"
mkdir -p "$OUT_DIR/mutant_diffs"

export RESULTS_DIR="/home/darla/experimento/${OUT_DIR}/harness_runs"
mkdir -p "$RESULTS_DIR"

# A baseline continua sendo a baseline semântica do sensor,
# porque o comportamento observado ainda é o estado do sensor.
export TRACE_BASELINE_FILE="/home/darla/experimento/resultados_mutmut/baselines_semantic/sensor/${FUZZER_NAME}/seed_${SEED}/trace.jsonl"
export TRACE_OUT_FILE="/home/darla/experimento/${OUT_DIR}/actual_trace.jsonl"

if [ ! -f "$TRACE_BASELINE_FILE" ]; then
    echo "[ERRO] Baseline semântica não encontrada:"
    echo "$TRACE_BASELINE_FILE"
    exit 1
fi

mkdir -p tests
if [ ! -f tests/test_placeholder.py ]; then
    cat > tests/test_placeholder.py <<'PY'
def test_placeholder():
    assert True
PY
fi

echo "[INFO] Módulo: $MODULE_NAME"
echo "[INFO] Target: $TARGET_PATH"
echo "[INFO] Fuzzer: $FUZZER_NAME"
echo "[INFO] Seed: $SEED"
echo "[INFO] Adapter: $FUZZER_CMD"
echo "[INFO] Saída: $OUT_DIR"
echo "[INFO] TRACE_BASELINE_FILE=$TRACE_BASELINE_FILE"
echo "[INFO] TRACE_OUT_FILE=$TRACE_OUT_FILE"
echo "[INFO] RESULTS_DIR=$RESULTS_DIR"

echo "[INFO] Conferindo se o arquivo alvo está montado no container..."

REL_PATH="${TARGET_PATH#ha_source/homeassistant/}"
CONTAINER_PATH="/usr/src/homeassistant/homeassistant/${REL_PATH}"

HOST_HASH=$(sha256sum "$TARGET_PATH" | awk '{print $1}')
CONTAINER_HASH=$(docker exec "$HA_CONTAINER" sha256sum "$CONTAINER_PATH" | awk '{print $1}')

echo "[INFO] Host hash:      $HOST_HASH"
echo "[INFO] Container hash: $CONTAINER_HASH"

if [ "$HOST_HASH" != "$CONTAINER_HASH" ]; then
    echo "[ERRO] O container não está usando o arquivo alvo do ha_source."
    echo "[ERRO] Container path: $CONTAINER_PATH"
    exit 1
fi

echo "[INFO] Limpando cache do mutmut..."
rm -rf .mutmut-cache mutants
rm -f "$TRACE_OUT_FILE"

echo "[INFO] Rodando mutmut..."

set +e
/usr/bin/time -v -o "$OUT_DIR/time.txt" \
mutmut run \
  --paths-to-mutate "$TARGET_PATH" \
  --runner "python -m unittest harness/test_harness_unificado.py" \
  2>&1 | tee "$OUT_DIR/mutmut_run.txt"

MUTMUT_EXIT=${PIPESTATUS[0]}
set -e

echo "$MUTMUT_EXIT" > "$OUT_DIR/mutmut_exit_code.txt"

mutmut results 2>&1 | tee "$OUT_DIR/mutmut_results.txt" || true

cp -a .mutmut-cache "$OUT_DIR/mutmut-cache" || true

TOTAL_MUTANTS=$(python3 - "$OUT_DIR/mutmut_run.txt" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(errors="ignore")
matches = re.findall(r"(\d+)/(\d+)", text)
print(matches[-1][1] if matches else "0")
PY
)

echo "[INFO] Total de mutantes: $TOTAL_MUTANTS"

if [ "$TOTAL_MUTANTS" != "0" ]; then
    for i in $(seq 1 "$TOTAL_MUTANTS"); do
        mutmut show "$i" > "$OUT_DIR/mutant_diffs/mutant_${i}.diff" 2>/dev/null || true
    done

    (
        cd "$OUT_DIR/mutant_diffs"
        sha256sum mutant_*.diff 2>/dev/null | sort -V
    ) > "$OUT_DIR/mutant_hashes.tsv" || true
fi

echo "[OK] Campanha finalizada: $OUT_DIR"
