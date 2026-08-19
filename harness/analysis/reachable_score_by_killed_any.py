#!/usr/bin/env python3
import re
import csv
from pathlib import Path

BASE = Path("/home/darla/experimento")
RESULTS = BASE / "resultados_mutmut"

MODULES = ["sensor", "template"]
FUZZERS = ["boofuzz", "fume", "scapy"]
SEED = "1"

OUT = RESULTS / "reachable_score_killed_any.csv"


def expand_ranges(text):
    ids = set()

    text = text.strip()
    if not text:
        return ids

    for part in text.replace(" ", "").split(","):
        if not part:
            continue

        # Aceita apenas "12" ou "12-30"
        if not re.fullmatch(r"\d+(-\d+)?", part):
            continue

        if "-" in part:
            a, b = part.split("-", 1)
            ids.update(range(int(a), int(b) + 1))
        else:
            ids.add(int(part))

    return ids


def parse_total_from_run(run_file):
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

    _current, total, _killed, _survived = matches[-1]
    return int(total)


def parse_survived_ids(results_file):
    if not results_file.exists():
        return set()

    text = results_file.read_text(errors="ignore")
    survived_ids = set()

    for line in text.splitlines():
        line = line.strip()

        # Só aceita linha composta por números, vírgulas, espaços e intervalos.
        # Ignora linhas tipo "---- ha_source/... ----"
        if not line:
            continue

        if not re.fullmatch(r"[0-9,\-\s]+", line):
            continue

        # Precisa conter pelo menos um número
        if not re.search(r"\d", line):
            continue

        ids = expand_ranges(line)
        if ids:
            survived_ids.update(ids)

    return survived_ids


def parse_module_fuzzer(module, fuzzer):
    run_file = RESULTS / module / fuzzer / f"seed_{SEED}" / "mutmut_run.txt"
    results_file = RESULTS / module / fuzzer / f"seed_{SEED}" / "mutmut_results.txt"

    total = parse_total_from_run(run_file)

    if total is None:
        return None, set(), set()

    survived_ids = parse_survived_ids(results_file)
    all_ids = set(range(1, total + 1))

    # Garante que não entra ID fora do total
    survived_ids = survived_ids & all_ids
    killed_ids = all_ids - survived_ids

    return total, killed_ids, survived_ids


rows = []

for module in MODULES:
    killed_by_fuzzer = {}
    total_ref = None

    for fuzzer in FUZZERS:
        total, killed_ids, survived_ids = parse_module_fuzzer(module, fuzzer)

        if total is None:
            print(f"[SKIP] Sem resultado para {module}/{fuzzer}")
            continue

        total_ref = total
        killed_by_fuzzer[fuzzer] = killed_ids

    if not killed_by_fuzzer:
        continue

    # Classificação conservadora:
    # mutante alcançável = morto por pelo menos um fuzzer
    reachable_ids = set()
    for killed_ids in killed_by_fuzzer.values():
        reachable_ids.update(killed_ids)

    reachable_total = len(reachable_ids)

    for fuzzer, killed_ids in killed_by_fuzzer.items():
        killed_reachable = len(killed_ids & reachable_ids)
        adjusted_score = killed_reachable / reachable_total if reachable_total else 0

        traditional_score = len(killed_ids) / total_ref if total_ref else 0

        rows.append({
            "module": module,
            "fuzzer": fuzzer,
            "total_mutants": total_ref,
            "traditional_killed": len(killed_ids),
            "traditional_score": round(traditional_score, 4),
            "traditional_score_percent": round(traditional_score * 100, 2),
            "reachable_by_killed_any": reachable_total,
            "killed_reachable": killed_reachable,
            "reachable_adjusted_score": round(adjusted_score, 4),
            "reachable_adjusted_score_percent": round(adjusted_score * 100, 2),
            "reachable_ids": " ".join(map(str, sorted(reachable_ids))),
            "killed_ids": " ".join(map(str, sorted(killed_ids))),
        })


if not rows:
    raise SystemExit("[ERRO] Nenhum resultado encontrado.")

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"[OK] Resultado salvo em: {OUT}")

for r in rows:
    print(
        f"{r['module']} | {r['fuzzer']} | "
        f"tradicional={r['traditional_score_percent']}% "
        f"({r['traditional_killed']}/{r['total_mutants']}) | "
        f"ajustado={r['reachable_adjusted_score_percent']}% "
        f"({r['killed_reachable']}/{r['reachable_by_killed_any']})"
    )
