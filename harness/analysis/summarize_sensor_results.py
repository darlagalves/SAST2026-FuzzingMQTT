#!/usr/bin/env python3
import re
import json
import csv
from pathlib import Path
from collections import Counter

BASE = Path("/home/darla/experimento")
FUZZERS = ["boofuzz", "fume", "mqttgram", "mitm", "scapy"]
SEED = "1"
TOTAL_MUTANTS = 126

def expand_ranges(text):
    ids = set()
    for part in text.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            ids.update(range(int(a), int(b) + 1))
        else:
            ids.add(int(part))
    return ids

rows = []

for fuzzer in FUZZERS:
    run_dir = BASE / "resultados_mutmut" / "sensor" / fuzzer / f"seed_{SEED}"
    run_file = run_dir / "mutmut_run.txt"
    results_file = run_dir / "mutmut_results.txt"
    corpus_file = BASE / "resultados_mutmut" / "corpus" / "sensor" / fuzzer / f"seed_{SEED}" / "payloads.jsonl"
    baseline_file = BASE / "resultados_mutmut" / "baselines_semantic" / "sensor" / fuzzer / f"seed_{SEED}" / "trace.jsonl"
    harness_dir = run_dir / "harness_runs"

    corpus_count = sum(1 for _ in corpus_file.open(encoding="utf-8")) if corpus_file.exists() else 0
    baseline_count = sum(1 for _ in baseline_file.open(encoding="utf-8")) if baseline_file.exists() else 0

    killed = survived = None

    if run_file.exists():
        text = run_file.read_text(errors="ignore")
        m = re.findall(r"🎉\s*(\d+).*?🙁\s*(\d+)", text)
        if m:
            killed, survived = map(int, m[-1])

    survived_ids = set()

    if results_file.exists():
        text = results_file.read_text(errors="ignore")
        m = re.search(r"\n\n([0-9,\-\s]+)\s*$", text)
        if m:
            survived_ids = expand_ranges(m.group(1))

    killed_ids = sorted(set(range(1, TOTAL_MUTANTS + 1)) - survived_ids) if survived_ids else []

    oracle_counter = Counter()
    if harness_dir.exists():
        for p in harness_dir.glob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                oracle_counter[data["result"]["oracle_level"]] += 1
            except Exception:
                pass

    rows.append({
        "fuzzer": fuzzer,
        "seed": SEED,
        "corpus_payloads": corpus_count,
        "baseline_trace_lines": baseline_count,
        "killed": killed if killed is not None else "",
        "survived": survived if survived is not None else "",
        "mutation_score": round(killed / TOTAL_MUTANTS, 4) if killed is not None else "",
        "killed_ids": " ".join(map(str, killed_ids)),
        "oracle_counts": dict(oracle_counter),
    })

out = BASE / "resultados_mutmut" / "sensor_summary_final.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(out)
for r in rows:
    print(r)
