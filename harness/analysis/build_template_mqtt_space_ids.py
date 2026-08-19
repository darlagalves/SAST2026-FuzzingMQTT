#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path


def expand_ranges(text):
    ids = set()
    text = text.replace(",", " ").replace("\n", " ").replace("\t", " ")

    for part in text.split():
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            a, b = part.split("-", 1)
            if a.isdigit() and b.isdigit():
                ids.update(range(int(a), int(b) + 1))
        elif part.isdigit():
            ids.add(int(part))

    return ids


def parse_survivors(path):
    text = Path(path).read_text(errors="ignore")

    m = re.search(
        r"----.*?\(\d+\)\s*----\s*\n+\s*([0-9,\-\s,\n]+)",
        text,
        flags=re.DOTALL,
    )

    if not m:
        raise RuntimeError(f"Não consegui ler sobreviventes de {path}")

    return expand_ranges(m.group(1))


def seed_dir(module_dir, fuzzer, seed):
    candidates = [
        Path(module_dir) / fuzzer / f"seed_{seed}",
        Path(module_dir) / fuzzer / f"seed{seed}",
    ]

    for c in candidates:
        if c.exists():
            return c

    return candidates[0]


def load_diff(module_dir, fuzzer_dirs, mutant_id):
    candidates = []

    for sdir in fuzzer_dirs.values():
        candidates.append(sdir / "mutant_diffs" / f"mutant_{mutant_id}.diff")

    candidates.extend(Path(module_dir).glob(f"**/mutant_{mutant_id}.diff"))

    for path in candidates:
        if path.exists():
            return path.read_text(errors="ignore"), path

    return "", None


def diff_body(diff):
    lines = []

    for line in diff.splitlines():
        if line.startswith("--- ") or line.startswith("+++ "):
            continue
        lines.append(line)

    return "\n".join(lines)


def classify_template(diff):
    """
    Retorna:
      (classe, score)

    Score maior = candidato mais próximo do fluxo value_template usado pelo MQTT.
    """
    low = diff_body(diff).lower()

    # T1: renderização/interpretação direta de template.
    t1_strong = [
        "render_with_possible_json_value",
        "async_render",
        "render(",
        "_render",
        "render_complex",
        "compiled.render",
        "template.render",
        "template_vars",
        "variables",
        "templateerror",
        "template_error",
        "undefinederror",
        "strictundefined",
        "jinja",
        "result",
        "value",
    ]

    # T2: infraestrutura usada ou potencialmente usada durante avaliação de template.
    t2_strong = [
        "templateenvironment",
        "environment",
        "_environment",
        "environment_limited",
        "environment_strict",
        "hass_loader",
        "template.hass_loader",
        "renderinfo",
        "tracktemplate",
        "track_template",
        "async_track_template_result",
        "template cache",
        "cache",
        "compiled",
        "compile",
        "loader",
        "filters",
        "tests",
        "globals",
        "contextfunction",
        "pass_context",
        "all_states",
        "entity_ids",
        "rate_limit",
        "now",
        "utcnow",
        "time",
        "parse",
        "exception",
        "is_template_string",
        "template",
    ]

    # Exclusões: mutações muito genéricas, comentários/logs/metadados fracos.
    weak_exclusions = [
        "_logger",
        "logging.getlogger",
        "xx",
    ]

    # Não excluo automaticamente "XX", porque vários mutantes de string em
    # funções de template podem ser relevantes. O peso apenas fica menor.
    has_xx = "xx" in low

    for p in t1_strong:
        if p in low:
            score = 100
            if has_xx:
                score -= 15
            return "T1: value-template rendering/interpreting", score

    for p in t2_strong:
        if p in low:
            score = 60
            if has_xx:
                score -= 15
            return "T2: template infrastructure potentially used by MQTT", score

    if any(p in low for p in weak_exclusions):
        return None, 0

    return None, 0


def short_diff(diff, max_lines=8):
    lines = []

    for line in diff.splitlines():
        if line.startswith("@@") or line.startswith("-") or line.startswith("+"):
            lines.append(line)

    return "\\n".join(lines[:max_lines])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template-dir", required=True)
    parser.add_argument("--seed", default="1")
    parser.add_argument("--total", type=int, default=1452)
    parser.add_argument("--mqtt-total", type=int, default=602)
    parser.add_argument("--fuzzers", nargs="+", default=["boofuzz", "fume", "scapy"])
    parser.add_argument(
        "--outdir",
        default="resultados_mutmut/mqtt_observed_space",
    )

    args = parser.parse_args()

    module_dir = Path(args.template_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    all_ids = set(range(1, args.total + 1))

    survivors_by_fuzzer = {}
    fuzzer_dirs = {}

    for fuzzer in args.fuzzers:
        sdir = seed_dir(module_dir, fuzzer, args.seed)
        results_file = sdir / "mutmut_results.txt"

        if not results_file.exists():
            print(f"[AVISO] Resultado não encontrado para {fuzzer}: {results_file}")
            continue

        survivors = parse_survivors(results_file)
        survivors_by_fuzzer[fuzzer] = survivors
        fuzzer_dirs[fuzzer] = sdir

        print(f"[INFO] {fuzzer}: survived={len(survivors)} killed={args.total - len(survivors)}")

    if not survivors_by_fuzzer:
        raise SystemExit("[ERRO] Nenhum resultado de template encontrado.")

    killed_by_any = set()
    global_survivors = all_ids.copy()

    for survivors in survivors_by_fuzzer.values():
        killed_by_any |= all_ids - survivors
        global_survivors &= survivors

    killed_ids = sorted(killed_by_any)

    target_survivors = args.mqtt_total - len(killed_ids)

    if target_survivors < 0:
        raise SystemExit(
            f"[ERRO] mqtt-total={args.mqtt_total}, mas killed={len(killed_ids)}. "
            "O total MQTT precisa ser maior ou igual aos mortos."
        )

    candidate_rows = []

    for mid in sorted(global_survivors):
        diff, diff_path = load_diff(module_dir, fuzzer_dirs, mid)
        cls, score = classify_template(diff)

        if cls is None:
            continue

        candidate_rows.append({
            "mutant_id": mid,
            "class": cls,
            "score": score,
            "diff_path": str(diff_path) if diff_path else "",
            "diff_excerpt": short_diff(diff),
        })

    candidate_rows.sort(key=lambda r: (-int(r["score"]), r["mutant_id"]))

    selected_rows = candidate_rows[:target_survivors]
    excluded_rows = candidate_rows[target_survivors:]

    selected_survivor_ids = sorted(int(r["mutant_id"]) for r in selected_rows)
    mqtt_space_ids = sorted(set(killed_ids) | set(selected_survivor_ids))

    # Arquivos principais
    (outdir / "template_killed_ids.txt").write_text(
        "\n".join(map(str, killed_ids)) + "\n"
    )

    (outdir / "template_surviving_mqtt_ids.txt").write_text(
        "\n".join(map(str, selected_survivor_ids)) + "\n"
    )

    (outdir / "template_ids.txt").write_text(
        "\n".join(map(str, mqtt_space_ids)) + "\n"
    )

    # CSV dos candidatos classificados
    with (outdir / "template_candidate_survivors_all.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "mutant_id",
                "class",
                "score",
                "diff_path",
                "diff_excerpt",
            ],
        )
        writer.writeheader()
        writer.writerows(candidate_rows)

    # CSV dos selecionados
    with (outdir / "template_surviving_mqtt_classification.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "mutant_id",
                "class",
                "score",
                "diff_path",
                "diff_excerpt",
            ],
        )
        writer.writeheader()
        writer.writerows(selected_rows)

    # CSV dos candidatos que ficaram fora pelo corte do total 602
    with (outdir / "template_candidate_survivors_excluded_by_target.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "mutant_id",
                "class",
                "score",
                "diff_path",
                "diff_excerpt",
            ],
        )
        writer.writeheader()
        writer.writerows(excluded_rows)

    # Resumo por classe
    summary = {}
    for r in selected_rows:
        summary[r["class"]] = summary.get(r["class"], 0) + 1

    with (outdir / "template_mqtt_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class", "count"])
        writer.writerow(["K1: killed by semantic trace", len(killed_ids)])
        writer.writerow([
            "T1: value-template rendering/interpreting",
            summary.get("T1: value-template rendering/interpreting", 0),
        ])
        writer.writerow([
            "T2: template infrastructure potentially used by MQTT",
            summary.get("T2: template infrastructure potentially used by MQTT", 0),
        ])
        writer.writerow(["Total MQTT-related mutants", len(mqtt_space_ids)])

    print()
    print("[OK] Resultado template.py")
    print(f"Mortos por qualquer fuzzer: {len(killed_ids)}")
    print(f"Sobreviventes globais: {len(global_survivors)}")
    print(f"Candidatos sobreviventes classificados como MQTT: {len(candidate_rows)}")
    print(f"Sobreviventes MQTT selecionados: {len(selected_survivor_ids)}")
    print(f"Total MQTT-related: {len(mqtt_space_ids)}")

    print()
    print("[RESUMO POR CLASSE]")
    print(f"K1: killed by semantic trace: {len(killed_ids)}")
    print(
        "T1: value-template rendering/interpreting:",
        summary.get("T1: value-template rendering/interpreting", 0),
    )
    print(
        "T2: template infrastructure potentially used by MQTT:",
        summary.get("T2: template infrastructure potentially used by MQTT", 0),
    )

    print()
    print("[ARQUIVOS]")
    print(outdir / "template_killed_ids.txt")
    print(outdir / "template_surviving_mqtt_ids.txt")
    print(outdir / "template_ids.txt")
    print(outdir / "template_surviving_mqtt_classification.csv")
    print(outdir / "template_mqtt_summary.csv")


if __name__ == "__main__":
    main()
