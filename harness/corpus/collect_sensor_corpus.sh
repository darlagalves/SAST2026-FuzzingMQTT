#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Uso: $0 <fuzzer_name> <adapter_sensor_path> <seed>"
    exit 1
fi

FUZZER_NAME="$1"
ADAPTER_PATH="$2"
SEED="$3"

cd /home/darla/experimento
source harness/config/experimento.env

export FUZZER_NAME="$FUZZER_NAME"
export FUZZER_CMD="$ADAPTER_PATH"
export FUZZER_SEED="$SEED"
export FUZZ_DURATION="${FUZZ_DURATION:-60}"

OUT_DIR="resultados_mutmut/corpus/sensor/${FUZZER_NAME}/seed_${SEED}"
mkdir -p "$OUT_DIR"

RAW_TOPIC="$OUT_DIR/raw_topic_payloads.txt"
RAW_BRIDGE="$OUT_DIR/raw_bridge_payloads.txt"
JSONL="$OUT_DIR/payloads.jsonl"
META="$OUT_DIR/metadata.txt"

rm -f "$RAW_TOPIC" "$RAW_BRIDGE" "$JSONL" "$META"
: > "$RAW_TOPIC"
: > "$RAW_BRIDGE"

export BRIDGE_CAPTURE_FILE="/home/darla/experimento/$RAW_BRIDGE"

echo "[INFO] Coletando corpus híbrido"
echo "[INFO] Fuzzer: $FUZZER_NAME"
echo "[INFO] Adapter: $ADAPTER_PATH"
echo "[INFO] Seed: $SEED"
echo "[INFO] Duração: $FUZZ_DURATION"
echo "[INFO] MQTT_TOPIC: $MQTT_TOPIC"
echo "[INFO] Bridge capture: $BRIDGE_CAPTURE_FILE"

pkill -f mosquitto_sub || true
sleep 1

timeout "$((FUZZ_DURATION + 10))s" \
mosquitto_sub -R -h "$MQTT_HOST" -p "$MQTT_PORT" -t "$MQTT_TOPIC" \
> "$RAW_TOPIC" &

SUB_PID=$!

sleep 1

timeout "$((FUZZ_DURATION + 15))s" "$ADAPTER_PATH" || true

sleep 2
kill "$SUB_PID" 2>/dev/null || true

python3 - "$RAW_TOPIC" "$RAW_BRIDGE" "$JSONL" <<'PY'
import json
import hashlib
import sys
from pathlib import Path

raw_topic = Path(sys.argv[1])
raw_bridge = Path(sys.argv[2])
out_path = Path(sys.argv[3])

payloads = []

for path in [raw_topic, raw_bridge]:
    if path.exists():
        payloads.extend(path.read_text(errors="ignore").splitlines())

seen = set()
kept = []

for p in payloads:
    h = hashlib.sha256(p.encode(errors="ignore")).hexdigest()
    if h in seen:
        continue
    seen.add(h)
    kept.append(p)

MAX_PAYLOADS = 200
kept = kept[:MAX_PAYLOADS]

with out_path.open("w", encoding="utf-8") as f:
    for p in kept:
        f.write(json.dumps({"payload": p}, ensure_ascii=False) + "\n")

print(len(kept))
PY

COUNT=$(wc -l < "$JSONL" | tr -d ' ')
RAW_TOPIC_LINES=$(wc -l < "$RAW_TOPIC" | tr -d ' ')
RAW_BRIDGE_LINES=$(wc -l < "$RAW_BRIDGE" | tr -d ' ')

{
    echo "fuzzer=$FUZZER_NAME"
    echo "seed=$SEED"
    echo "adapter=$ADAPTER_PATH"
    echo "duration=$FUZZ_DURATION"
    echo "mqtt_topic=$MQTT_TOPIC"
    echo "raw_topic_lines=$RAW_TOPIC_LINES"
    echo "raw_bridge_lines=$RAW_BRIDGE_LINES"
    echo "unique_payloads=$COUNT"
    echo "corpus_file=$JSONL"
} > "$META"

echo "[OK] Corpus salvo em: $JSONL"
echo "[OK] Payloads únicos: $COUNT"

if [ "$COUNT" -lt 5 ]; then
    echo "[AVISO] Corpus muito pequeno. Esse fuzzer/adaptador pode não estar atingindo bem sensor.py."
fi