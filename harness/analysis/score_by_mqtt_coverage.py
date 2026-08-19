#!/usr/bin/env python3
import re
import csv
from pathlib import Path

BASE = Path("/home/darla/experimento")
RESULTS = BASE / "resultados_mutmut"

MODULES = ["sensor", "template"]
FUZZERS = ["boofuzz", "fume", "scapy"]
SEED = "1"

OUT = RESULTS / "mqtt_coverage_adjusted_score.csv"


def expand_ranges(text):
    ids = set()

    for part in text.replace(" ", "").split(","):
        if not part:
            continue

        if not re.fullmatch(r"\d+(-\d+)?", part):
            continue

        if "-" in part:
            a, b = part.split("-", 1)
            ids.update(range(int(a), int(b) + 1))
        else:
            ids.add(int(part))

    return ids


def parse_total(run_file):
    if not run_file.exists():
        return None

    text = run_file.read_text(errors="ignore")

    matches = re.findall(
        r"(\d+)/(\d+).*?🎉\s*(\d+).*?🙁\s*(\d+)",
        text,
        flags=re.DOTALL,
    )

    if not matches:
        return None

    return int(matches[-1][1])


def parse_survived(results_file):
    if not results_file.exists():
        return set()

    survived = set()

    for line in results_file.read_text(errors="ignore").splitlines():
        line = line.strip()

        if not re.fullmatch(r"[0-9,\-\s]+", line):
            continue

        if not re.search(r"\d", line):
            continue

        survived.update(expand_ranges(line))

    return survived


def parse_mutant_lines(diff_file):
    if not diff_file.exists():
        return set()

    lines = set()
    old_line = None

    for line in diff_file.read_text(errors="ignore").splitlines():
        h = re.match(r"@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@", line)
        if h:
            old_line = int(h.group(1))
            continue

        if old_line is None:
            continue

        if line.startswith("---") or line.startswith("+++"):
            continue

        if line.startswith("-"):
            lines.add(old_line)
            old_line += 1
        elif line.startswith("+"):
            pass
        else:
            old_line += 1

    return lines


def load_covered_lines(module):
    path = RESULTS / "coverage_mqtt" / f"{module}_covered_lines.txt"

    if not path.exists():
        return set()

    return {
        int(x.strip())
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip().isdigit()
    }


rows = []

for module in MODULES:
    covered_lines = load_covered_lines(module)

    if not covered_lines:
        print(f"[AVISO] Sem linhas cobertas para {module}")
        continue

    # usa o primeiro fuzzer com diffs como referência dos mutantes
    ref_dir = None
    total_ref = None

    for fuzzer in FUZZERS:
        run_dir = RESULTS / module / fuzzer / f"seed_{SEED}"
        total = parse_total(run_dir / "mutmut_run.txt")

        if total:
            ref_dir = run_dir
            total_ref = total
            break

    if ref_dir is None or total_ref is None:
        print(f"[SKIP] Sem campanha para {module}")
        continue

    mutant_lines = {}

    for i in range(1, total_ref + 1):
        diff_file = ref_dir / "mutant_diffs" / f"mutant_{i}.diff"
        mutant_lines[i] = parse_mutant_lines(diff_file)

    reachable_ids = {
        mid
        for mid, lines in mutant_lines.items()
        if lines & covered_lines
    }

    reachable_total = len(reachable_ids)

    for fuzzer in FUZZERS:
        run_dir = RESULTS / module / fuzzer / f"seed_{SEED}"
        run_file = run_dir / "mutmut_run.txt"
        results_file = run_dir / "mutmut_results.txt"

        total = parse_total(run_file)

        if total is None:
            print(f"[SKIP] Sem resultado para {module}/{fuzzer}")
            continue

        all_ids = set(range(1, total + 1))
        survived = parse_survived(results_file) & all_ids
        killed = all_ids - survived

        killed_reachable = killed & reachable_ids

        traditional_score = len(killed) / total if total else 0
        adjusted_score = len(killed_reachable) / reachable_total if reachable_total else 0

        rows.append({
            "module": module,
            "fuzzer": fuzzer,
            "total_mutants": total,
            "covered_lines": len(covered_lines),
            "mqtt_reachable_mutants": reachable_total,
            "traditional_killed": len(killed),
            "traditional_score": round(traditional_score, 4),
            "traditional_score_percent": round(traditional_score * 100, 2),
            "killed_reachable": len(killed_reachable),
            "mqtt_adjusted_score": round(adjusted_score, 4),
            "mqtt_adjusted_score_percent": round(adjusted_score * 100, 2),
            "reachable_ids": " ".join(map(str, sorted(reachable_ids))),
            "killed_reachable_ids": " ".join(map(str, sorted(killed_reachable))),
        })


if not rows:
    raise SystemExit("[ERRO] Nenhum resultado calculado.")

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"[OK] Score salvo em: {OUT}")

for r in rows:
    print(
        f"{r['module']} | {r['fuzzer']} | "
        f"tradicional={r['traditional_score_percent']}% "
        f"({r['traditional_killed']}/{r['total_mutants']}) | "
        f"MQTT-ajustado={r['mqtt_adjusted_score_percent']}% "
        f"({r['killed_reachable']}/{r['mqtt_reachable_mutants']})"
    )
