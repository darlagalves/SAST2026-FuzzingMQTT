#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Uso: $0 <fuzzer_name> <adapter_path> <seed>"
    echo "Exemplo:"
    echo "$0 boofuzz /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py 1"
    exit 1
fi

FUZZER_NAME="$1"
ADAPTER_PATH="$2"
SEED="$3"

cd /home/darla/experimento

source harness/config/experimento.env

export MODULE_UNDER_MUTATION="sensor"
export FUZZER_NAME="$FUZZER_NAME"
export FUZZER_CMD="$ADAPTER_PATH"
export FUZZER_SEED="$SEED"

# Configuração do replay semântico
export REPLAY_LIMIT="${REPLAY_LIMIT:-100}"
export REPLAY_DELAY="${REPLAY_DELAY:-0.05}"
export RESET_PAYLOAD='{"temperature": 22.5}'
export ORACLE_LOG_PATTERNS="${ORACLE_LOG_PATTERNS:-__PADRAO_QUE_NUNCA_APARECE__}"

OUT_DIR="resultados_mutmut/sensor/${FUZZER_NAME}/seed_${SEED}"
mkdir -p "$OUT_DIR"
mkdir -p "$OUT_DIR/mutant_diffs"

export RESULTS_DIR="/home/darla/experimento/${OUT_DIR}/harness_runs"
mkdir -p "$RESULTS_DIR"

# Oráculo por trace semântico
if [ "$FUZZER_NAME" = "noop" ]; then
    export CHECK_CORPUS_TRACE=0
else
    export CHECK_CORPUS_TRACE="${CHECK_CORPUS_TRACE:-1}"
fi

export TRACE_BASELINE_FILE="/home/darla/experimento/resultados_mutmut/baselines_semantic/sensor/${FUZZER_NAME}/seed_${SEED}/trace.jsonl"
export TRACE_OUT_FILE="/home/darla/experimento/${OUT_DIR}/actual_trace.jsonl"

# Garante que existe uma pasta tests/, exigida por esta versão do mutmut
mkdir -p tests
if [ ! -f tests/test_placeholder.py ]; then
    cat > tests/test_placeholder.py <<'PY'
def test_placeholder():
    assert True
PY
fi

# Usa config específica do sensor, se existir
if [ -f configs_mutmut/setup_sensor.cfg ]; then
    cp configs_mutmut/setup_sensor.cfg setup.cfg
fi

echo "[INFO] Módulo: sensor.py"
echo "[INFO] Fuzzer: $FUZZER_NAME"
echo "[INFO] Seed: $SEED"
echo "[INFO] Adapter: $FUZZER_CMD"
echo "[INFO] Saída: $OUT_DIR"
echo "[INFO] CHECK_CORPUS_TRACE=$CHECK_CORPUS_TRACE"
echo "[INFO] TRACE_BASELINE_FILE=$TRACE_BASELINE_FILE"
echo "[INFO] TRACE_OUT_FILE=$TRACE_OUT_FILE"
echo "[INFO] REPLAY_LIMIT=$REPLAY_LIMIT"
echo "[INFO] REPLAY_DELAY=$REPLAY_DELAY"
echo "[INFO] RESULTS_DIR=$RESULTS_DIR"
echo "[INFO] ORACLE_LOG_PATTERNS=${ORACLE_LOG_PATTERNS:-default}"

if [ "$CHECK_CORPUS_TRACE" = "1" ] && [ ! -f "$TRACE_BASELINE_FILE" ]; then
    echo "[ERRO] Baseline semântica não encontrada:"
    echo "$TRACE_BASELINE_FILE"
    echo
    echo "Gere antes com:"
    echo "./harness/corpus/build_sensor_semantic_trace_baselines.sh $SEED"
    exit 1
fi

echo "[INFO] Conferindo se sensor.py do host é o mesmo do container..."

HOST_HASH=$(sha256sum ha_source/homeassistant/components/mqtt/sensor.py | awk '{print $1}')
CONTAINER_HASH=$(docker exec "$HA_CONTAINER" sha256sum /usr/src/homeassistant/homeassistant/components/mqtt/sensor.py | awk '{print $1}')

echo "[INFO] Host hash:      $HOST_HASH"
echo "[INFO] Container hash: $CONTAINER_HASH"

if [ "$HOST_HASH" != "$CONTAINER_HASH" ]; then
    echo "[ERRO] O container não está usando o sensor.py do ha_source."
    exit 1
fi

echo "[INFO] Limpando cache do mutmut..."
rm -rf .mutmut-cache mutants

rm -f "$TRACE_OUT_FILE"

echo "[INFO] Rodando mutmut run com runner explícito..."

set +e
/usr/bin/time -v -o "$OUT_DIR/time.txt" \
mutmut run \
  --paths-to-mutate ha_source/homeassistant/components/mqtt/sensor.py \
  --runner "python -m unittest harness/test_harness_unificado.py" \
  2>&1 | tee "$OUT_DIR/mutmut_run.txt"

MUTMUT_EXIT=${PIPESTATUS[0]}
set -e

echo "[INFO] mutmut terminou com código: $MUTMUT_EXIT"
echo "$MUTMUT_EXIT" > "$OUT_DIR/mutmut_exit_code.txt"

echo "[INFO] Salvando mutmut results..."
mutmut results 2>&1 | tee "$OUT_DIR/mutmut_results.txt" || true

echo "[INFO] Copiando cache da campanha..."
cp -a .mutmut-cache "$OUT_DIR/mutmut-cache" || true

echo "[INFO] Extraindo total de mutantes a partir do mutmut_run.txt..."

TOTAL_MUTANTS=$(python3 - "$OUT_DIR/mutmut_run.txt" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(errors="ignore")
matches = re.findall(r"(\d+)/(\d+)", text)
print(matches[-1][1] if matches else "0")
PY
)

echo "[INFO] Total de mutantes detectado: $TOTAL_MUTANTS"

if [ "$TOTAL_MUTANTS" != "0" ]; then
    echo "[INFO] Gerando diffs e hashes dos mutantes..."

    for i in $(seq 1 "$TOTAL_MUTANTS"); do
        mutmut show "$i" > "$OUT_DIR/mutant_diffs/mutant_${i}.diff" 2>/dev/null || true
    done

    (
        cd "$OUT_DIR/mutant_diffs"
        sha256sum mutant_*.diff 2>/dev/null | sort -V
    ) > "$OUT_DIR/mutant_hashes.tsv" || true
fi

echo "[OK] Campanha finalizada: $OUT_DIR"