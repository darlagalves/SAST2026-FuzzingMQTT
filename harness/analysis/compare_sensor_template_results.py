#!/usr/bin/env python3
import re
import csv
from pathlib import Path

import matplotlib.pyplot as plt

BASE = Path("/home/darla/experimento")
RESULTS = BASE / "resultados_mutmut"

MODULES = ["sensor", "template"]
FUZZERS = ["boofuzz", "fume", "scapy"]
SEED = "1"

OUT_CSV = RESULTS / "comparacao_sensor_template.csv"
OUT_TEX = RESULTS / "tabela_comparacao_sensor_template.tex"

OUT_GRAPH_SCORE = RESULTS / "grafico_comparacao_score_sensor_template.png"
OUT_GRAPH_KILLED = RESULTS / "grafico_comparacao_mortos_sensor_template.png"
OUT_GRAPH_COMBINED = RESULTS / "grafico_score_combinado_fuzzers.png"


def parse_mutmut_run(path: Path):
    if not path.exists():
        return None

    text = path.read_text(errors="ignore")

    # Exemplo:
    # 1452/1452  🎉 127  ⏰ 0  🤔 0  🙁 1325  🔇 0
    matches = re.findall(
        r"(\d+)/(\d+).*?🎉\s*(\d+).*?⏰\s*(\d+).*?🤔\s*(\d+).*?🙁\s*(\d+).*?🔇\s*(\d+)",
        text,
        flags=re.DOTALL,
    )

    if not matches:
        return None

    current, total, killed, timeout, suspicious, survived, skipped = matches[-1]

    return {
        "total": int(total),
        "killed": int(killed),
        "timeout": int(timeout),
        "suspicious": int(suspicious),
        "survived": int(survived),
        "skipped": int(skipped),
    }


def latex_escape(s):
    return str(s).replace("_", r"\_")


rows = []

for module in MODULES:
    for fuzzer in FUZZERS:
        run_file = RESULTS / module / fuzzer / f"seed_{SEED}" / "mutmut_run.txt"
        parsed = parse_mutmut_run(run_file)

        if parsed is None:
            rows.append({
                "module": module,
                "fuzzer": fuzzer,
                "total": "",
                "killed": "",
                "survived": "",
                "mutation_score": "",
                "mutation_score_percent": "",
                "status": "sem campanha",
            })
            continue

        total = parsed["total"]
        killed = parsed["killed"]
        survived = parsed["survived"]
        score = killed / total if total else 0

        rows.append({
            "module": module,
            "fuzzer": fuzzer,
            "total": total,
            "killed": killed,
            "survived": survived,
            "mutation_score": round(score, 4),
            "mutation_score_percent": round(score * 100, 2),
            "status": "válido",
        })


# CSV principal
with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"[OK] CSV salvo em: {OUT_CSV}")


# Tabela LaTeX
lines = []
lines.append(r"\begin{table}[htbp]")
lines.append(r"\centering")
lines.append(r"\caption{Comparação dos resultados de mutação nos módulos \texttt{sensor.py} e \texttt{template.py}.}")
lines.append(r"\label{tab:comparacao_sensor_template}")
lines.append(r"\begin{tabular}{llrrrrl}")
lines.append(r"\hline")
lines.append(r"\textbf{Módulo} & \textbf{Fuzzer} & \textbf{Total} & \textbf{Mortos} & \textbf{Sobreviventes} & \textbf{Score (\%)} & \textbf{Status} \\")
lines.append(r"\hline")

for r in rows:
    lines.append(
        f"{latex_escape(r['module'])} & "
        f"{latex_escape(r['fuzzer'])} & "
        f"{r['total']} & "
        f"{r['killed']} & "
        f"{r['survived']} & "
        f"{r['mutation_score_percent']} & "
        f"{latex_escape(r['status'])} \\\\"
    )

lines.append(r"\hline")
lines.append(r"\end{tabular}")
lines.append(r"\end{table}")

OUT_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"[OK] Tabela LaTeX salva em: {OUT_TEX}")


# Dados para gráficos
def get_value(module, fuzzer, field):
    for r in rows:
        if r["module"] == module and r["fuzzer"] == fuzzer and r["status"] == "válido":
            return float(r[field])
    return 0.0


# Gráfico 1: mutation score por módulo
x = range(len(FUZZERS))
width = 0.35

sensor_scores = [get_value("sensor", f, "mutation_score_percent") for f in FUZZERS]
template_scores = [get_value("template", f, "mutation_score_percent") for f in FUZZERS]

plt.figure(figsize=(10, 6))
plt.bar([i - width / 2 for i in x], sensor_scores, width, label="sensor.py")
plt.bar([i + width / 2 for i in x], template_scores, width, label="template.py")
plt.xticks(list(x), FUZZERS)
plt.xlabel("Fuzzer")
plt.ylabel("Mutation score (%)")
plt.title("Mutation score por fuzzer e módulo")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_GRAPH_SCORE, dpi=200)
plt.close()

print(f"[OK] Gráfico salvo em: {OUT_GRAPH_SCORE}")


# Gráfico 2: mutantes mortos por módulo
sensor_killed = [get_value("sensor", f, "killed") for f in FUZZERS]
template_killed = [get_value("template", f, "killed") for f in FUZZERS]

plt.figure(figsize=(10, 6))
plt.bar([i - width / 2 for i in x], sensor_killed, width, label="sensor.py")
plt.bar([i + width / 2 for i in x], template_killed, width, label="template.py")
plt.xticks(list(x), FUZZERS)
plt.xlabel("Fuzzer")
plt.ylabel("Mutantes mortos")
plt.title("Mutantes mortos por fuzzer e módulo")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_GRAPH_KILLED, dpi=200)
plt.close()

print(f"[OK] Gráfico salvo em: {OUT_GRAPH_KILLED}")


# Gráfico 3: score combinado ponderado
combined_rows = []

for fuzzer in FUZZERS:
    total_sum = 0
    killed_sum = 0

    for module in MODULES:
        total = get_value(module, fuzzer, "total")
        killed = get_value(module, fuzzer, "killed")
        total_sum += int(total)
        killed_sum += int(killed)

    combined_score = killed_sum / total_sum if total_sum else 0

    combined_rows.append({
        "fuzzer": fuzzer,
        "total": total_sum,
        "killed": killed_sum,
        "score_percent": combined_score * 100,
    })

combined_csv = RESULTS / "comparacao_score_combinado.csv"

with combined_csv.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=combined_rows[0].keys())
    writer.writeheader()
    writer.writerows(combined_rows)

print(f"[OK] CSV combinado salvo em: {combined_csv}")

plt.figure(figsize=(10, 6))
plt.bar([r["fuzzer"] for r in combined_rows], [r["score_percent"] for r in combined_rows])
plt.xlabel("Fuzzer")
plt.ylabel("Mutation score combinado (%)")
plt.title("Mutation score combinado: sensor.py + template.py")
plt.tight_layout()
plt.savefig(OUT_GRAPH_COMBINED, dpi=200)
plt.close()

print(f"[OK] Gráfico salvo em: {OUT_GRAPH_COMBINED}")

print("\nResumo combinado:")
for r in combined_rows:
    print(
        f"{r['fuzzer']}: "
        f"{r['killed']}/{r['total']} mortos "
        f"({r['score_percent']:.2f}%)"
    )
