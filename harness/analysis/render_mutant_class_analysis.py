#!/usr/bin/env python3
import csv
from pathlib import Path
from collections import defaultdict, OrderedDict

import matplotlib.pyplot as plt


BASE = Path("/home/darla/experimento")
RESULTS = BASE / "resultados_mutmut"

INPUT_FILES = {
    "sensor": RESULTS / "resumo_classes_mutantes_sensor.csv",
    "template": RESULTS / "resumo_classes_mutantes_template.csv",
}

OUT_DIR = RESULTS / "artigo_mutantes"
OUT_DIR.mkdir(parents=True, exist_ok=True)


CLASS_LABELS = OrderedDict([
    ("K1_morto_por_trace", "K1: morto por trace"),
    ("S1_baixa_atingibilidade", "S1: baixa atingibilidade"),
    ("S2_limitacao_oraculo", "S2: limitação do oráculo"),
    ("S3_equivalente_ou_neutro", "S3: equivalente/neutro"),
    ("S4_configuracao_nao_exercitada", "S4: config. não exercitada"),
    ("S5_tratamento_silencioso", "S5: tratamento silencioso"),
    ("S6_fluxo_generico_template", "S6: fluxo genérico template"),
    ("sem_diff", "Sem diff"),
    ("indefinido", "Indefinido"),
])


def latex_escape(text: str) -> str:
    text = str(text)
    repl = {
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
    for a, b in repl.items():
        text = text.replace(a, b)
    return text


def read_summary_csv(path: Path):
    rows = []
    if not path.exists():
        return rows

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "module": row["module"],
                "classification": row["classification"],
                "count": int(float(row["count"])),
                "percent": float(row["percent"]),
            })
    return rows


# ----------------------------
# Carrega dados
# ----------------------------
data = {}
all_classes_present = set()

for module, path in INPUT_FILES.items():
    rows = read_summary_csv(path)
    data[module] = rows
    for r in rows:
        all_classes_present.add(r["classification"])

# mantém ordem fixa e adiciona classes extras no fim
ordered_classes = []
for c in CLASS_LABELS.keys():
    if c in all_classes_present:
        ordered_classes.append(c)
for c in sorted(all_classes_present):
    if c not in ordered_classes:
        ordered_classes.append(c)

# matriz por módulo
counts = defaultdict(dict)
percents = defaultdict(dict)

for module, rows in data.items():
    for cls in ordered_classes:
        counts[module][cls] = 0
        percents[module][cls] = 0.0

    for r in rows:
        cls = r["classification"]
        counts[module][cls] = r["count"]
        percents[module][cls] = r["percent"]


# ----------------------------
# 1) Gráfico empilhado por módulo (contagem)
# ----------------------------
modules = list(INPUT_FILES.keys())

plt.figure(figsize=(11, 7))
bottom = [0] * len(modules)

for cls in ordered_classes:
    values = [counts[m].get(cls, 0) for m in modules]
    label = CLASS_LABELS.get(cls, cls)
    plt.bar(modules, values, bottom=bottom, label=label)
    bottom = [b + v for b, v in zip(bottom, values)]

plt.title("Distribuição das classes de mutantes por módulo")
plt.xlabel("Módulo")
plt.ylabel("Quantidade de mutantes")
plt.legend(loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig(OUT_DIR / "grafico_classes_empilhado_contagem.png", dpi=300)
plt.close()


# ----------------------------
# 2) Gráfico empilhado por módulo (percentual)
# ----------------------------
plt.figure(figsize=(11, 7))
bottom = [0.0] * len(modules)

for cls in ordered_classes:
    values = [percents[m].get(cls, 0.0) for m in modules]
    label = CLASS_LABELS.get(cls, cls)
    plt.bar(modules, values, bottom=bottom, label=label)
    bottom = [b + v for b, v in zip(bottom, values)]

plt.title("Distribuição percentual das classes de mutantes por módulo")
plt.xlabel("Módulo")
plt.ylabel("Percentual (%)")
plt.legend(loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig(OUT_DIR / "grafico_classes_empilhado_percentual.png", dpi=300)
plt.close()


# ----------------------------
# 3) Gráfico comparativo por classe (sensor vs template)
# ----------------------------
x = list(range(len(ordered_classes)))
width = 0.35

sensor_vals = [percents["sensor"].get(cls, 0.0) for cls in ordered_classes]
template_vals = [percents["template"].get(cls, 0.0) for cls in ordered_classes]
labels = [CLASS_LABELS.get(cls, cls) for cls in ordered_classes]

plt.figure(figsize=(14, 7))
plt.bar([i - width / 2 for i in x], sensor_vals, width, label="sensor.py")
plt.bar([i + width / 2 for i in x], template_vals, width, label="template.py")
plt.xticks(x, labels, rotation=25, ha="right")
plt.title("Comparação percentual das classes de mutantes")
plt.xlabel("Classe")
plt.ylabel("Percentual (%)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_DIR / "grafico_classes_comparativo.png", dpi=300)
plt.close()


# ----------------------------
# 4) Tabela LaTeX resumida
# ----------------------------
summary_tex = []
summary_tex.append(r"\begin{table*}[htbp]")
summary_tex.append(r"\centering")
summary_tex.append(r"\caption{Distribuição das classes de mutantes nos módulos \texttt{sensor.py} e \texttt{template.py}.}")
summary_tex.append(r"\label{tab:classes_mutantes_resumo}")
summary_tex.append(r"\begin{tabular}{lrrrr}")
summary_tex.append(r"\hline")
summary_tex.append(r"\textbf{Classe} & \textbf{Sensor (n)} & \textbf{Sensor (\%)} & \textbf{Template (n)} & \textbf{Template (\%)} \\")
summary_tex.append(r"\hline")

for cls in ordered_classes:
    label = CLASS_LABELS.get(cls, cls)
    summary_tex.append(
        f"{latex_escape(label)} & "
        f"{counts['sensor'].get(cls, 0)} & "
        f"{percents['sensor'].get(cls, 0.0):.2f} & "
        f"{counts['template'].get(cls, 0)} & "
        f"{percents['template'].get(cls, 0.0):.2f} \\\\"
    )

summary_tex.append(r"\hline")
summary_tex.append(r"\end{tabular}")
summary_tex.append(r"\end{table*}")

(OUT_DIR / "tabela_classes_mutantes_resumo.tex").write_text(
    "\n".join(summary_tex) + "\n",
    encoding="utf-8"
)


# ----------------------------
# 5) Tabela LaTeX individual por módulo
# ----------------------------
for module in modules:
    tex = []
    tex.append(r"\begin{table}[htbp]")
    tex.append(r"\centering")
    tex.append(
        rf"\caption{{Distribuição das classes de mutantes no módulo \texttt{{{module}.py}}.}}"
    )
    tex.append(
        rf"\label{{tab:classes_mutantes_{module}}}"
    )
    tex.append(r"\begin{tabular}{lrr}")
    tex.append(r"\hline")
    tex.append(r"\textbf{Classe} & \textbf{Quantidade} & \textbf{Percentual (\%)} \\")
    tex.append(r"\hline")

    for cls in ordered_classes:
        n = counts[module].get(cls, 0)
        p = percents[module].get(cls, 0.0)
        if n == 0:
            continue
        label = CLASS_LABELS.get(cls, cls)
        tex.append(
            f"{latex_escape(label)} & {n} & {p:.2f} \\\\"
        )

    tex.append(r"\hline")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table}")

    (OUT_DIR / f"tabela_classes_mutantes_{module}.tex").write_text(
        "\n".join(tex) + "\n",
        encoding="utf-8"
    )


# ----------------------------
# 6) Tabela CSV bonita consolidada
# ----------------------------
with (OUT_DIR / "classes_mutantes_consolidado.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "classe",
        "rotulo",
        "sensor_count",
        "sensor_percent",
        "template_count",
        "template_percent",
    ])
    for cls in ordered_classes:
        writer.writerow([
            cls,
            CLASS_LABELS.get(cls, cls),
            counts["sensor"].get(cls, 0),
            f"{percents['sensor'].get(cls, 0.0):.2f}",
            counts["template"].get(cls, 0),
            f"{percents['template'].get(cls, 0.0):.2f}",
        ])


print("[OK] Arquivos gerados em:", OUT_DIR)
print("[OK] Gráficos:")
print(" - grafico_classes_empilhado_contagem.png")
print(" - grafico_classes_empilhado_percentual.png")
print(" - grafico_classes_comparativo.png")
print("[OK] Tabelas LaTeX:")
print(" - tabela_classes_mutantes_resumo.tex")
print(" - tabela_classes_mutantes_sensor.tex")
print(" - tabela_classes_mutantes_template.tex")
print("[OK] CSV consolidado:")
print(" - classes_mutantes_consolidado.csv")
