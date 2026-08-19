#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

SEED="${SEED:-1}"
REPETITIONS="${REPETITIONS:-5}"
REPLAY_LIMIT="${REPLAY_LIMIT:-1000}"
REPLAY_DELAY="${REPLAY_DELAY:-0.02}"
HA_STARTUP_SLEEP="${HA_STARTUP_SLEEP:-35}"

FUZZERS=("boofuzz" "fume" "scapy")

OUT_ROOT="resultados_mutmut/repeated_baseline_replay/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT_ROOT"

echo "[INFO] Saída: $OUT_ROOT"
echo "[INFO] SEED=$SEED"
echo "[INFO] REPETITIONS=$REPETITIONS"
echo "[INFO] REPLAY_LIMIT=$REPLAY_LIMIT"
echo "[INFO] REPLAY_DELAY=$REPLAY_DELAY"
echo "[INFO] HA_CONTAINER=$HA_CONTAINER"
echo "[INFO] HA_BASE_URL=$HA_BASE_URL"
echo "[INFO] MQTT_TOPIC=$MQTT_TOPIC"
echo

for FUZZER in "${FUZZERS[@]}"; do
    CORPUS="resultados_mutmut/corpus/sensor/${FUZZER}/seed_${SEED}/payloads.jsonl"

    if [ ! -f "$CORPUS" ]; then
        echo "[AVISO] Corpus não encontrado para $FUZZER: $CORPUS"
        continue
    fi

    COUNT=$(wc -l < "$CORPUS" | tr -d ' ')

    if [ "$COUNT" -lt 1 ]; then
        echo "[AVISO] Corpus vazio para $FUZZER"
        continue
    fi

    echo "===================================================="
    echo "[FUZZER] $FUZZER | corpus=$COUNT payloads"
    echo "===================================================="

    for RUN in $(seq 1 "$REPETITIONS"); do
        RUN_DIR="$OUT_ROOT/$FUZZER/run_$RUN"
        mkdir -p "$RUN_DIR"

        export FUZZER_NAME="$FUZZER"
        export FUZZER_SEED="$SEED"
        export REPLAY_LIMIT="$REPLAY_LIMIT"
        export REPLAY_DELAY="$REPLAY_DELAY"
        export RESET_PAYLOAD='{"temperature": 22.5}'
        export TRACE_OUT="$RUN_DIR/trace.jsonl"

        echo
        echo "[RUN] $FUZZER repetição $RUN/$REPETITIONS"
        echo "[INFO] TRACE_OUT=$TRACE_OUT"

        docker restart "$HA_CONTAINER" >/dev/null
        sleep "$HA_STARTUP_SLEEP"

        python harness/adapters/run_replay_sensor_corpus_semantic.py \
            > "$RUN_DIR/replay_stdout.log" \
            2> "$RUN_DIR/replay_stderr.log" || true

        if [ -f "$TRACE_OUT" ]; then
            LINES=$(wc -l < "$TRACE_OUT" | tr -d ' ')
            echo "[OK] Trace gerada com $LINES linhas"
        else
            echo "[ERRO] Trace não foi gerada para $FUZZER run $RUN"
        fi
    done

    echo
done

python3 - "$OUT_ROOT" <<'PY'
import csv
import hashlib
import json
import sys
from pathlib import Path

out_root = Path(sys.argv[1])

VOLATILE_KEYS = {
    "timestamp",
    "time",
    "datetime",
    "created_at",
    "updated_at",
    "elapsed",
    "duration",
    "run",
    "pid",
}


def normalize(obj):
    if isinstance(obj, dict):
        clean = {}
        for k, v in obj.items():
            lk = str(k).lower()
            if lk in VOLATILE_KEYS:
                continue
            if "timestamp" in lk or "elapsed" in lk:
                continue
            clean[k] = normalize(v)
        return clean

    if isinstance(obj, list):
        return [normalize(x) for x in obj]

    return obj


def load_trace(path):
    rows = []

    with path.open(errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except Exception:
                obj = {"raw": line}

            rows.append(normalize(obj))

    return rows


def trace_hash(rows):
    data = json.dumps(rows, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


summary_rows = []
details = []

for fuzzer_dir in sorted(p for p in out_root.iterdir() if p.is_dir()):
    traces = sorted(fuzzer_dir.glob("run_*/trace.jsonl"))

    hashes = []
    lengths = []

    for trace in traces:
        rows = load_trace(trace)
        h = trace_hash(rows)
        hashes.append(h)
        lengths.append(len(rows))
        details.append({
            "fuzzer": fuzzer_dir.name,
            "run": trace.parent.name,
            "trace_file": str(trace),
            "lines": len(rows),
            "hash": h,
        })

    unique_hashes = sorted(set(hashes))
    stable = len(unique_hashes) == 1 and len(traces) > 1

    summary_rows.append({
        "fuzzer": fuzzer_dir.name,
        "runs": len(traces),
        "trace_lengths": ";".join(map(str, lengths)),
        "unique_hashes": len(unique_hashes),
        "stable": "yes" if stable else "no",
        "hash": unique_hashes[0] if unique_hashes else "",
    })

    if not stable and len(traces) >= 2:
        # salva uma dica simples do primeiro par divergente
        first = load_trace(traces[0])
        for other_path in traces[1:]:
            other = load_trace(other_path)
            if trace_hash(first) != trace_hash(other):
                diff_path = out_root / f"{fuzzer_dir.name}_first_difference.txt"

                max_len = max(len(first), len(other))
                with diff_path.open("w", encoding="utf-8") as f:
                    f.write(f"Trace A: {traces[0]}\n")
                    f.write(f"Trace B: {other_path}\n\n")

                    for i in range(max_len):
                        a = first[i] if i < len(first) else "<missing>"
                        b = other[i] if i < len(other) else "<missing>"

                        if a != b:
                            f.write(f"First difference at index {i}\n\n")
                            f.write("A:\n")
                            f.write(json.dumps(a, indent=2, ensure_ascii=False))
                            f.write("\n\nB:\n")
                            f.write(json.dumps(b, indent=2, ensure_ascii=False))
                            f.write("\n")
                            break
                break


summary_file = out_root / "summary.csv"
details_file = out_root / "details.csv"

with summary_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["fuzzer", "runs", "trace_lengths", "unique_hashes", "stable", "hash"],
    )
    writer.writeheader()
    writer.writerows(summary_rows)

with details_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["fuzzer", "run", "trace_file", "lines", "hash"],
    )
    writer.writeheader()
    writer.writerows(details)

print()
print("[OK] Resumo salvo em:", summary_file)
print("[OK] Detalhes salvos em:", details_file)
print()
print("=== SUMMARY ===")
for row in summary_rows:
    print(
        f"{row['fuzzer']}: stable={row['stable']} | "
        f"runs={row['runs']} | lengths={row['trace_lengths']} | "
        f"unique_hashes={row['unique_hashes']}"
    )
PY

echo
echo "[OK] Teste concluído."
echo "[INFO] Resultados em: $OUT_ROOT"
