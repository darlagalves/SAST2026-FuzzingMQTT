#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

export FUZZ_DURATION="${FUZZ_DURATION:-60}"

SEEDS=("$@")

if [ "$#" -eq 0 ]; then
    SEEDS=("1")
fi

echo "[INFO] FUZZ_DURATION=$FUZZ_DURATION"
echo "[INFO] Seeds: ${SEEDS[*]}"

echo "[INFO] Conferindo se o sensor.py do host é o mesmo do container..."

HOST_HASH=$(sha256sum ha_source/homeassistant/components/mqtt/sensor.py | awk '{print $1}')
CONTAINER_HASH=$(docker exec "$HA_CONTAINER" sha256sum /usr/src/homeassistant/homeassistant/components/mqtt/sensor.py | awk '{print $1}')

echo "[INFO] Host hash:      $HOST_HASH"
echo "[INFO] Container hash: $CONTAINER_HASH"

if [ "$HOST_HASH" != "$CONTAINER_HASH" ]; then
    echo "[ERRO] O container não está usando o sensor.py do ha_source."
    exit 1
fi

declare -A FUZZERS

FUZZERS["boofuzz"]="/home/darla/experimento/harness/adapters/run_boofuzz.sh"
FUZZERS["fume"]="/home/darla/experimento/harness/adapters/run_fume_sensor.sh"
FUZZERS["mqttgram"]="/home/darla/experimento/harness/adapters/run_mqttgram.sh"
FUZZERS["mitm"]="/home/darla/experimento/harness/adapters/run_mitm.sh"
FUZZERS["scapy"]="/home/darla/experimento/harness/adapters/run_scapy.sh"

ORDER=("boofuzz" "fume" "mqttgram" "mitm" "scapy")

BATCH_LOG_DIR="resultados_mutmut/sensor/_batch_logs"
mkdir -p "$BATCH_LOG_DIR"

for SEED in "${SEEDS[@]}"; do
    echo "===================================================="
    echo "[INFO] Iniciando campanhas da seed $SEED"
    echo "===================================================="

    for FUZZER in "${ORDER[@]}"; do
        ADAPTER="${FUZZERS[$FUZZER]}"
        OUT_DIR="resultados_mutmut/sensor/${FUZZER}/seed_${SEED}"

        if [ -f "$OUT_DIR/mutmut_run.txt" ] && [ "${FORCE:-0}" != "1" ]; then
            echo "[SKIP] Resultado já existe para $FUZZER seed $SEED"
            echo "[SKIP] Para sobrescrever, rode com FORCE=1"
            continue
        fi

        echo "----------------------------------------------------"
        echo "[INFO] Rodando $FUZZER | seed $SEED"
        echo "[INFO] Adapter: $ADAPTER"
        echo "----------------------------------------------------"

        ./harness/run_sensor_campaign.sh \
            "$FUZZER" \
            "$ADAPTER" \
            "$SEED" \
            2>&1 | tee "$BATCH_LOG_DIR/${FUZZER}_seed_${SEED}.log"

        echo "[OK] Finalizado: $FUZZER seed $SEED"
    done
done

echo "[INFO] Gerando resumo sensor × fuzzer × seed..."

if [ -f harness/analysis/build_sensor_summary.py ]; then
    python harness/analysis/build_sensor_summary.py || true
fi

if [ -f harness/analysis/check_sensor_mutant_id_stability.py ]; then
    python harness/analysis/check_sensor_mutant_id_stability.py || true
fi

echo "[OK] Todas as campanhas solicitadas foram finalizadas."
