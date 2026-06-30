#!/usr/bin/env bash
set -euo pipefail

FUZZER_NAME="$1"
FUZZER_CMD_PATH="$2"

cd /home/darla/experimento
source harness/config/experimento.env

export FUZZER_NAME="$FUZZER_NAME"
export FUZZER_CMD="$FUZZER_CMD_PATH"

OUT_DIR="resultados/${FUZZER_NAME}/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT_DIR"

echo "[INFO] Fuzzer: $FUZZER_NAME"
echo "[INFO] FUZZER_CMD: $FUZZER_CMD"
echo "[INFO] Limpando cache do mutmut..."

rm -rf .mutmut-cache

echo "[INFO] Iniciando mutmut run limpo..."

/usr/bin/time -v -o "$OUT_DIR/time.txt" \
mutmut run 2>&1 | tee "$OUT_DIR/mutmut_run.txt"

echo "[INFO] Salvando mutmut results..."

mutmut results 2>&1 | tee "$OUT_DIR/mutmut_results.txt"

echo "[INFO] Salvando cache da campanha..."

cp -a .mutmut-cache "$OUT_DIR/mutmut-cache"

echo "[OK] Resultado salvo em: $OUT_DIR"
