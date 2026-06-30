#!/usr/bin/env python3
import re
import json
import csv
from pathlib import Path

import matplotlib.pyplot as plt

BASE = Path("/home/darla/experimento")
RESULTS_BASE = BASE / "resultados_mutmut"
FUZZERS = ["boofuzz", "fume", "mqttgram", "mitm", "scapy"]
SEED = "1"
TOTAL_MUTANTS = 126


def parse_run_counts(run_file: Path):
    if not run_file.exists():
        return None, None
    text = run_file.read_text(errors="ignore")
    m = re.findall(r"🎉\s*(\d+).*?🙁\s*(\d+)", text)
    if not m:
        return None, None
    killed, survived = map(int, m[-1])
    return killed, survived


def count_lines(path: Path):
    if not path.exists():
        return 0
    with path.open(encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)


def oracle_counter(harness_dir: Path):
    counts = {}
    if not harness_dir.exists():
        return counts
    for p in harness_dir.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            oracle = data["result"]["oracle_level"]
            counts[oracle] = counts.get(oracle, 0) + 1
        except Exception:
            pass
    return counts


rows = []

for fuzzer in FUZZERS:
    run_dir = RESULTS_BASE / "sensor" / fuzzer / f"seed_{SEED}"
    corpus_file = RESULTS_BASE / "corpus" / "sensor" / fuzzer / f"seed_{SEED}" / "payloads.jsonl"
    baseline_file = RESULTS_BASE / "baselines_semantic" / "sensor" / fuzzer / f"seed_{SEED}" / "trace.jsonl"
    run_file = run_dir / "mutmut_run.txt"
    harness_dir = run_dir / "harness_runs"

    corpus_count = count_lines(corpus_file)
    baseline_count = count_lines(baseline_file)
    killed, survived = parse_run_counts(run_file)
    oracles = oracle_counter(harness_dir)

    if killed is None:
        killed = 0
    if survived is None:
        survived = 0

    score = killed / TOTAL_MUTANTS if TOTAL_MUTANTS else 0.0

    rows.append({
        "fuzzer": fuzzer,
        "corpus_payloads": corpus_count,
        "baseline_trace_lines": baseline_count,
        "killed": killed,
        "survived": survived,
        "mutation_score": score,
        "oracle_level_3_4_corpus_trace": oracles.get("level_3_4_corpus_trace", 0),
        "oracle_none": oracles.get("none", 0),
    })

# salva CSV
out_csv = RESULTS_BASE / "sensor_summary_final.csv"
with out_csv.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"[OK] CSV salvo em: {out_csv}")

# imprime tabela no terminal
print("\nResumo:")
for r in rows:
    print(r)

# gráfico 1: mutantes mortos
labels = [r["fuzzer"] for r in rows]
killed_vals = [r["killed"] for r in rows]

plt.figure(figsize=(10, 6))
plt.bar(labels, killed_vals)
plt.title("Mutantes mortos por fuzzer - sensor.py")
plt.xlabel("Fuzzer")
plt.ylabel("Mutantes mortos")
plt.tight_layout()
out1 = RESULTS_BASE / "grafico_sensor_mutantes_mortos.png"
plt.savefig(out1, dpi=200)
plt.close()
print(f"[OK] Gráfico salvo em: {out1}")

# gráfico 2: mutation score
scores = [r["mutation_score"] for r in rows]

plt.figure(figsize=(10, 6))
plt.bar(labels, scores)
plt.title("Mutation score por fuzzer - sensor.py")
plt.xlabel("Fuzzer")
plt.ylabel("Mutation score")
plt.tight_layout()
out2 = RESULTS_BASE / "grafico_sensor_mutation_score.png"
plt.savefig(out2, dpi=200)
plt.close()
print(f"[OK] Gráfico salvo em: {out2}")

# gráfico 3: tamanho do corpus
corpus_vals = [r["corpus_payloads"] for r in rows]

plt.figure(figsize=(10, 6))
plt.bar(labels, corpus_vals)
plt.title("Tamanho do corpus por fuzzer - sensor.py")
plt.xlabel("Fuzzer")
plt.ylabel("Payloads no corpus")
plt.tight_layout()
out3 = RESULTS_BASE / "grafico_sensor_corpus.png"
plt.savefig(out3, dpi=200)
plt.close()
print(f"[OK] Gráfico salvo em: {out3}")

# gráfico 4: mortos vs sobreviventes
survived_vals = [r["survived"] for r in rows]

x = range(len(labels))
plt.figure(figsize=(10, 6))
plt.bar(x, killed_vals, label="Mortos")
plt.bar(x, survived_vals, bottom=killed_vals, label="Sobreviventes")
plt.xticks(list(x), labels)
plt.title("Mortos vs Sobreviventes por fuzzer - sensor.py")
plt.xlabel("Fuzzer")
plt.ylabel("Quantidade de mutantes")
plt.legend()
plt.tight_layout()
out4 = RESULTS_BASE / "grafico_sensor_empilhado.png"
plt.savefig(out4, dpi=200)
plt.close()
print(f"[OK] Gráfico salvo em: {out4}")
