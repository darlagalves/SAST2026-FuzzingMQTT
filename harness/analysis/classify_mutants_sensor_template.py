#!/usr/bin/env python3
import re
import csv
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path("/home/darla/experimento")
RESULTS = BASE / "resultados_mutmut"

MODULES = {
    "sensor": {
        "total": 126,
        "fuzzers": ["boofuzz", "fume", "scapy"],
    },
    "template": {
        "total": 1452,
        "fuzzers": ["boofuzz", "fume", "scapy"],
    },
}

SEED = "1"


def expand_ranges(text):
    ids = set()
    text = text.replace(" ", "").replace("\n", "")
    if not text:
        return ids

    for part in text.split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            ids.update(range(int(a), int(b) + 1))
        else:
            ids.add(int(part))
    return ids


def survived_ids_from_results(path):
    if not path.exists():
        return set()

    text = path.read_text(errors="ignore")

    # Pega a última linha/bloco de IDs sobreviventes depois do caminho do arquivo
    matches = re.findall(r"\n\n([0-9,\-\s]+)\s*$", text)
    if not matches:
        return set()

    return expand_ranges(matches[-1])


def classify_diff(diff_text, module):
    lower = diff_text.lower()

    if not diff_text.strip():
        return "sem_diff", "Diff não disponível para inspeção."

    if module == "sensor":
        if "expire_after" in lower or "_expired" in lower:
            return "S4_configuracao_nao_exercitada", "Mutação relacionada a expire_after/expiração do sensor, dependente de configuração específica."

        if "device_class" in lower or "state_class" in lower or "unit" in lower:
            return "S4_configuracao_nao_exercitada", "Mutação relacionada a atributos/configuração do sensor não necessariamente exercitados pelo cenário."

        if "value_template" in lower or "template" in lower:
            return "S2_limitacao_oraculo", "Mutação relacionada à transformação de valor; pode não gerar diferença observável no estado final."

        if "if " in lower or " and " in lower or " or " in lower:
            return "S1_baixa_atingibilidade", "Mutação condicional; pode depender de branch não alcançado pelos payloads da campanha."

        if "return" in lower:
            return "S2_limitacao_oraculo", "Mutação em retorno interno; pode não alterar o estado observado pelo oráculo."

        return "S5_tratamento_silencioso", "Mutação possivelmente mascarada pelo tratamento silencioso ou fallback do Home Assistant."

    if module == "template":
        if "exception" in lower or "error" in lower or "undefined" in lower:
            return "S5_tratamento_silencioso", "Mutação relacionada a erros/exceções de template que podem ser tratados internamente."

        if "render" in lower or "async_render" in lower:
            return "S2_limitacao_oraculo", "Mutação em renderização de template; pode não alterar o estado final observado."

        if "jinja" in lower or "template" in lower:
            return "S6_fluxo_generico_template", "Mutação em parte genérica do mecanismo de template, enquanto o experimento usa um template simples."

        if "if " in lower or " and " in lower or " or " in lower:
            return "S1_baixa_atingibilidade", "Mutação condicional em branch possivelmente não alcançado pelo value_template usado."

        if "return" in lower:
            return "S3_equivalente_ou_neutro", "Mutação em retorno que pode ser equivalente para o cenário observado."

        return "S6_fluxo_generico_template", "Mutação em região ampla do template.py, possivelmente fora do caminho MQTT exercitado."

    return "indefinido", "Módulo não reconhecido."


def main():
    all_rows = []

    for module, cfg in MODULES.items():
        total = cfg["total"]
        fuzzers = cfg["fuzzers"]

        killed_by_mutant = defaultdict(list)
        survived_by_fuzzer = {}

        for fuzzer in fuzzers:
            result_file = RESULTS / module / fuzzer / f"seed_{SEED}" / "mutmut_results.txt"
            survived = survived_ids_from_results(result_file)
            survived_by_fuzzer[fuzzer] = survived

            all_ids = set(range(1, total + 1))
            killed = sorted(all_ids - survived)

            for mid in killed:
                killed_by_mutant[mid].append(fuzzer)

        rows = []

        for mid in range(1, total + 1):
            killed_by = killed_by_mutant.get(mid, [])
            killed_count = len(killed_by)

            diff_file = None

            # Usa diff do primeiro fuzzer que tiver o arquivo
            for fuzzer in fuzzers:
                candidate = RESULTS / module / fuzzer / f"seed_{SEED}" / "mutant_diffs" / f"mutant_{mid}.diff"
                if candidate.exists():
                    diff_file = candidate
                    break

            diff_text = diff_file.read_text(errors="ignore") if diff_file else ""
            category, explanation = classify_diff(diff_text, module)

            if killed_count > 0:
                final_class = "K1_morto_por_trace"
                final_explanation = f"Mutante morto por: {', '.join(killed_by)}."
            else:
                final_class = category
                final_explanation = explanation

            row = {
                "module": module,
                "mutant_id": mid,
                "killed_count": killed_count,
                "killed_by": " ".join(killed_by),
                "classification": final_class,
                "explanation": final_explanation,
            }

            rows.append(row)
            all_rows.append(row)

        out_csv = RESULTS / f"analise_mutantes_{module}.csv"
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "module",
                    "mutant_id",
                    "killed_count",
                    "killed_by",
                    "classification",
                    "explanation",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)

        summary = Counter(r["classification"] for r in rows)
        out_summary = RESULTS / f"resumo_classes_mutantes_{module}.csv"

        with out_summary.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["module", "classification", "count", "percent"])
            for cls, count in summary.most_common():
                writer.writerow([module, cls, count, round(count / total * 100, 2)])

        print(f"[OK] {out_csv}")
        print(f"[OK] {out_summary}")

    out_all = RESULTS / "analise_mutantes_sensor_template.csv"
    with out_all.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "module",
                "mutant_id",
                "killed_count",
                "killed_by",
                "classification",
                "explanation",
            ],
        )
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"[OK] {out_all}")


if __name__ == "__main__":
    main()
