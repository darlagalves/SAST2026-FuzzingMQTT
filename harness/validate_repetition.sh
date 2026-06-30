#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

OUT="resultados/validacao_harness/repeticao_noop"
mkdir -p "$OUT"

for i in 1 2 3 4 5; do
    echo "[RUN $i] Controle negativo NOOP"

    FUZZER_CMD=/home/darla/experimento/harness/adapters/validation/run_noop.sh \
    python3 -m unittest harness/test_harness_unificado.py \
    > "$OUT/run_${i}.txt" 2>&1 || true

    tail -n 5 "$OUT/run_${i}.txt"
done
