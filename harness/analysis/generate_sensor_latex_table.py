#!/usr/bin/env python3
import csv
from pathlib import Path

BASE = Path("/home/darla/experimento")
CSV_PATH = BASE / "resultados_mutmut" / "sensor_summary_final.csv"

OUT_SUMMARY = BASE / "resultados_mutmut" / "tabela_sensor_resultados.tex"
OUT_DETAILED = BASE / "resultados_mutmut" / "tabela_sensor_resultados_detalhada.tex"

TOTAL_MUTANTS = 126


def latex_escape(text):
    text = str(text)
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def as_int(value, default=0):
    try:
        return int(float(value))
    except Exception:
        return default


def as_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


if not CSV_PATH.exists():
    raise SystemExit(
        f"[ERRO] CSV não encontrado: {CSV_PATH}\n"
        "Rode antes: python harness/analysis/plot_sensor_results.py"
    )

rows = []

with CSV_PATH.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        fuzzer = row.get("fuzzer", "")
        corpus = as_int(row.get("corpus_payloads", 0))
        baseline = as_int(row.get("baseline_trace_lines", 0))
        killed = as_int(row.get("killed", 0))
        survived = as_int(row.get("survived", 0))
        score = as_float(row.get("mutation_score", 0.0))

        if corpus < 5 or baseline == 0:
            status = "Limitado"
        elif killed == 0 and survived == 0:
            status = "Não executado"
        else:
            status = "Válido"

        rows.append({
            "fuzzer": fuzzer,
            "corpus": corpus,
            "baseline": baseline,
            "killed": killed,
            "survived": survived,
            "score": score,
            "score_percent": score * 100,
            "status": status,
        })


# -------------------------
# Tabela principal
# -------------------------
summary_lines = []
summary_lines.append(r"\begin{table}[htbp]")
summary_lines.append(r"\centering")
summary_lines.append(r"\caption{Resultado da campanha de mutação no módulo \texttt{sensor.py}.}")
summary_lines.append(r"\label{tab:resultados_sensor}")
summary_lines.append(r"\begin{tabular}{lrrrrl}")
summary_lines.append(r"\hline")
summary_lines.append(r"\textbf{Fuzzer} & \textbf{Corpus} & \textbf{Mortos} & \textbf{Sobreviventes} & \textbf{Score (\%)} & \textbf{Status} \\")
summary_lines.append(r"\hline")

for r in rows:
    summary_lines.append(
        f"{latex_escape(r['fuzzer'])} & "
        f"{r['corpus']} & "
        f"{r['killed']} & "
        f"{r['survived']} & "
        f"{r['score_percent']:.2f} & "
        f"{latex_escape(r['status'])} \\\\"
    )

summary_lines.append(r"\hline")
summary_lines.append(r"\end{tabular}")
summary_lines.append(r"\end{table}")

OUT_SUMMARY.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


# -------------------------
# Tabela detalhada
# -------------------------
detailed_lines = []
detailed_lines.append(r"\begin{table}[htbp]")
detailed_lines.append(r"\centering")
detailed_lines.append(r"\caption{Resumo detalhado da campanha semântica no módulo \texttt{sensor.py}.}")
detailed_lines.append(r"\label{tab:resultados_sensor_detalhado}")
detailed_lines.append(r"\begin{tabular}{lrrrrrrl}")
detailed_lines.append(r"\hline")
detailed_lines.append(
    r"\textbf{Fuzzer} & "
    r"\textbf{Corpus} & "
    r"\textbf{Trace} & "
    r"\textbf{Total} & "
    r"\textbf{Mortos} & "
    r"\textbf{Sobrev.} & "
    r"\textbf{Score} & "
    r"\textbf{Status} \\"
)
detailed_lines.append(r"\hline")

for r in rows:
    detailed_lines.append(
        f"{latex_escape(r['fuzzer'])} & "
        f"{r['corpus']} & "
        f"{r['baseline']} & "
        f"{TOTAL_MUTANTS} & "
        f"{r['killed']} & "
        f"{r['survived']} & "
        f"{r['score']:.4f} & "
        f"{latex_escape(r['status'])} \\\\"
    )

detailed_lines.append(r"\hline")
detailed_lines.append(r"\end{tabular}")
detailed_lines.append(r"\end{table}")

OUT_DETAILED.write_text("\n".join(detailed_lines) + "\n", encoding="utf-8")


print(f"[OK] Tabela principal salva em: {OUT_SUMMARY}")
print(f"[OK] Tabela detalhada salva em: {OUT_DETAILED}")

print("\nUse no LaTeX com:")
print(r"\input{resultados_mutmut/tabela_sensor_resultados.tex}")
print(r"\input{resultados_mutmut/tabela_sensor_resultados_detalhada.tex}")
