#!/usr/bin/env python3
import argparse
import csv
import re
from collections import Counter
from pathlib import Path


def expand_ids(text):
    ids = set()
    text = text.replace(",", " ").replace("\n", " ").replace("\t", " ")

    for part in text.split():
        if "-" in part:
            a, b = part.split("-", 1)
            if a.isdigit() and b.isdigit():
                ids.update(range(int(a), int(b) + 1))
        elif part.isdigit():
            ids.add(int(part))

    return ids


def load_ids(path):
    return expand_ids(Path(path).read_text(errors="ignore"))


def parse_survivors(path):
    text = Path(path).read_text(errors="ignore")

    m = re.search(
        r"----.*?\(\d+\)\s*----\s*\n+\s*([0-9,\-\s,\n]+)",
        text,
        flags=re.DOTALL,
    )

    if not m:
        raise RuntimeError(f"Não consegui ler sobreviventes de {path}")

    return expand_ids(m.group(1))


def seed_dir(module_dir, fuzzer, seed):
    for candidate in [
        Path(module_dir) / fuzzer / f"seed_{seed}",
        Path(module_dir) / fuzzer / f"seed{seed}",
    ]:
        if candidate.exists():
            return candidate

    return Path(module_dir) / fuzzer / f"seed_{seed}"


def load_module_results(module_dir, total, seed, fuzzers):
    all_ids = set(range(1, total + 1))
    survivors_by_fuzzer = {}
    fuzzer_dirs = {}

    for fuzzer in fuzzers:
        sdir = seed_dir(module_dir, fuzzer, seed)
        result_file = sdir / "mutmut_results.txt"

        if not result_file.exists():
            print(f"[AVISO] Resultado não encontrado: {result_file}")
            continue

        survivors = parse_survivors(result_file)
        survivors_by_fuzzer[fuzzer] = survivors
        fuzzer_dirs[fuzzer] = sdir

        print(
            f"[INFO] {module_dir} / {fuzzer}: "
            f"survived={len(survivors)} killed={total - len(survivors)}"
        )

    if not survivors_by_fuzzer:
        raise SystemExit(f"[ERRO] Nenhum resultado encontrado em {module_dir}")

    killed_by_any = set()
    global_survivors = all_ids.copy()

    for survivors in survivors_by_fuzzer.values():
        killed_by_any |= all_ids - survivors
        global_survivors &= survivors

    return killed_by_any, global_survivors, fuzzer_dirs


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
    return "\n".join(lines).lower()


def short_diff(diff, max_lines=10):
    lines = []
    for line in diff.splitlines():
        if line.startswith("@@") or line.startswith("-") or line.startswith("+"):
            lines.append(line)
    return "\\n".join(lines[:max_lines])


def classify_sensor(diff):
    low = diff_body(diff)

    if any(x in low for x in [
        "expire_after",
        "expiration",
        "_expired",
        "expiration_trigger",
        "_value_is_expired",
        "available",
        "availability",
        "async_call_later",
        "async_track_point_in_utc_time",
        "remain_seconds",
    ]):
        return "S1: MQTT availability/expiration"

    if any(x in low for x in [
        "payload",
        "value_template",
        "last_reset_value_template",
        "last_reset_template",
        "payload_none",
        "parse_datetime",
        "last_reset",
        "_attr_last_reset",
    ]):
        return "S2: MQTT payload/template handling"

    if any(x in low for x in [
        "_attr_native_value",
        "native_value",
        "async_write_ha_state",
        "force_update",
        "state_class",
    ]):
        return "S3: MQTT state update"

    if any(x in low for x in [
        "state_topic",
        "availability_topic",
        "json_attributes_topic",
        "async_subscribe",
        "subscription",
        "topics",
        "msg.topic",
    ]):
        return "S4: MQTT topic/subscription handling"

    return "S5: MQTT schema/configuration"


def classify_template(diff):
    low = diff_body(diff)

    if any(x in low for x in [
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
    ]):
        return "T1: value-template rendering/interpreting"

    return "T2: template infrastructure potentially used by MQTT"


def analyze_module(module_name, module_dir, total, space_ids, seed, fuzzers):
    killed_by_any, global_survivors, fuzzer_dirs = load_module_results(
        module_dir=module_dir,
        total=total,
        seed=seed,
        fuzzers=fuzzers,
    )

    mqtt_killed = sorted(space_ids & killed_by_any)
    mqtt_survivors = sorted(space_ids & global_survivors)

    rows = []

    for mutant_id in mqtt_survivors:
        diff, diff_path = load_diff(module_dir, fuzzer_dirs, mutant_id)

        if module_name == "sensor.py":
            cls = classify_sensor(diff)
        else:
            cls = classify_template(diff)

        rows.append({
            "module": module_name,
            "mutant_id": mutant_id,
            "class": cls,
            "diff_path": str(diff_path) if diff_path else "",
            "diff_excerpt": short_diff(diff),
        })

    print()
    print(f"[RESUMO] {module_name}")
    print(f"Total MQTT-related: {len(space_ids)}")
    print(f"Killed by semantic trace: {len(mqtt_killed)}")
    print(f"MQTT-related survivors: {len(mqtt_survivors)}")

    return {
        "module": module_name,
        "total": len(space_ids),
        "killed": len(mqtt_killed),
        "survivors": len(mqtt_survivors),
        "rows": rows,
    }


def write_outputs(sensor_result, template_result, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    all_rows = sensor_result["rows"] + template_result["rows"]

    counts = {
        "sensor.py": Counter(),
        "template.py": Counter(),
    }

    counts["sensor.py"]["K1: killed by semantic trace"] = sensor_result["killed"]
    counts["template.py"]["K1: killed by semantic trace"] = template_result["killed"]

    for row in all_rows:
        counts[row["module"]][row["class"]] += 1

    classes = [
        "K1: killed by semantic trace",
        "S1: MQTT availability/expiration",
        "S2: MQTT payload/template handling",
        "S3: MQTT state update",
        "S4: MQTT topic/subscription handling",
        "S5: MQTT schema/configuration",
        "T1: value-template rendering/interpreting",
        "T2: template infrastructure potentially used by MQTT",
    ]

    summary_csv = outdir / "posthoc_mqtt_summary.csv"
    details_csv = outdir / "posthoc_mqtt_survivors_details.csv"
    latex_file = outdir / "tabela_posthoc_mqtt.tex"
    md_file = outdir / "posthoc_mqtt_survivors_details.md"

    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class", "sensor.py", "template.py"])
        for cls in classes:
            writer.writerow([cls, counts["sensor.py"][cls], counts["template.py"][cls]])
        writer.writerow([
            "Total MQTT-related mutants",
            sensor_result["total"],
            template_result["total"],
        ])

    with details_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["module", "mutant_id", "class", "diff_path", "diff_excerpt"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    with latex_file.open("w", encoding="utf-8") as f:
        f.write("\\begin{table}[!htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Post-hoc classification of MQTT-related mutants.}\n")
        f.write("\\label{tab:mutant-classes-summary}\n")
        f.write("\\scriptsize\n")
        f.write("\\setlength{\\tabcolsep}{3pt}\n")
        f.write("\\begin{tabular}{>{\\raggedright\\arraybackslash}p{0.62\\columnwidth}rr}\n")
        f.write("\\hline\n")
        f.write("Class & sensor.py & template.py \\\\\n")
        f.write("\\hline\n")

        for cls in classes:
            f.write(
                f"{cls} & {counts['sensor.py'][cls]} & {counts['template.py'][cls]} \\\\\n"
            )

        f.write("\\hline\n")
        f.write(
            f"Total MQTT-related mutants & {sensor_result['total']} & {template_result['total']} \\\\\n"
        )
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")

    with md_file.open("w", encoding="utf-8") as f:
        f.write("# Post-hoc MQTT mutant classification\n\n")

        for module in ["sensor.py", "template.py"]:
            f.write(f"## {module}\n\n")
            rows = [r for r in all_rows if r["module"] == module]

            for r in rows:
                f.write(f"### Mutant {r['mutant_id']}\n\n")
                f.write(f"- Class: **{r['class']}**\n")
                f.write(f"- Diff: `{r['diff_path']}`\n\n")
                f.write("```diff\n")
                f.write(r["diff_excerpt"])
                f.write("\n```\n\n")

    print()
    print("[OK] Arquivos gerados:")
    print(summary_csv)
    print(details_csv)
    print(latex_file)
    print(md_file)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--sensor-dir", required=True)
    parser.add_argument("--template-dir", required=True)
    parser.add_argument("--sensor-ids", required=True)
    parser.add_argument("--template-ids", required=True)
    parser.add_argument("--seed", default="1")
    parser.add_argument("--sensor-total", type=int, default=126)
    parser.add_argument("--template-total", type=int, default=1452)
    parser.add_argument("--fuzzers", nargs="+", default=["boofuzz", "fume", "scapy"])
    parser.add_argument("--outdir", default="resultados_mutmut/posthoc_mqtt_final")

    args = parser.parse_args()

    sensor_ids = load_ids(args.sensor_ids)
    template_ids = load_ids(args.template_ids)

    sensor_result = analyze_module(
        module_name="sensor.py",
        module_dir=args.sensor_dir,
        total=args.sensor_total,
        space_ids=sensor_ids,
        seed=args.seed,
        fuzzers=args.fuzzers,
    )

    template_result = analyze_module(
        module_name="template.py",
        module_dir=args.template_dir,
        total=args.template_total,
        space_ids=template_ids,
        seed=args.seed,
        fuzzers=args.fuzzers,
    )

    write_outputs(sensor_result, template_result, args.outdir)


if __name__ == "__main__":
    main()
