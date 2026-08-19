#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path


def expand_ranges(text):
    ids = set()
    text = text.replace("\n", " ").replace("\t", " ")
    for part in text.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            if a.isdigit() and b.isdigit():
                ids.update(range(int(a), int(b) + 1))
        elif part.isdigit():
            ids.add(int(part))
    return ids


def parse_survivors(results_file):
    text = results_file.read_text(errors="ignore")

    survived_count = None
    m = re.search(r"🙁\s*(\d+)", text)
    if m:
        survived_count = int(m.group(1))

    sections = re.findall(
        r"----\s*([^\n-]*?)\s*(?:\((\d+)\))?\s*----\s*\n+(.*?)(?=\n----|\Z)",
        text,
        flags=re.DOTALL,
    )

    candidates = []

    for title, count_text, body in sections:
        ids = expand_ranges(body)
        if not ids:
            continue

        title_low = title.lower()
        count = int(count_text) if count_text and count_text.isdigit() else None

        candidates.append((title_low, count, ids))

        if "surviv" in title_low or "survived" in title_low or "surviving" in title_low:
            return ids

    if survived_count is not None:
        for _title, count, ids in candidates:
            if count == survived_count or len(ids) == survived_count:
                return ids

    if candidates:
        # fallback: normalmente a maior lista é a de sobreviventes
        return max(candidates, key=lambda x: len(x[2]))[2]

    raise RuntimeError(f"Não consegui extrair sobreviventes de {results_file}")


def seed_dir(module_dir, fuzzer, seed):
    candidates = [
        module_dir / fuzzer / f"seed_{seed}",
        module_dir / fuzzer / f"seed{seed}",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


def load_diff(module_dir, fuzzer_dirs, seed, mutant_id):
    candidates = []

    for fuzzer, sdir in fuzzer_dirs.items():
        candidates.append(sdir / "mutant_diffs" / f"mutant_{mutant_id}.diff")

    candidates.extend(module_dir.glob(f"**/mutant_{mutant_id}.diff"))

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


def short_diff(diff, max_lines=12):
    lines = []
    for line in diff.splitlines():
        if line.startswith("@@") or line.startswith("-") or line.startswith("+"):
            lines.append(line)
    return "\\n".join(lines[:max_lines])


def classify_sensor(diff):
    body = diff_body(diff)
    low = body.lower()

    metadata_exclusions = [
        "default_name",
        "mqtt sensor",
        "suggested_display_precision",
        "translation_key",
        "icon",
        "device_class",
        "unit_of_measurement",
        "native_unit_of_measurement",
        "entity_category",
        "entity_description",
    ]

    if any(p in low for p in metadata_exclusions):
        return (
            "não",
            "metadata/configuração de entidade",
            "Altera metadados do sensor, mas não o fluxo MQTT observado de payload, tópico, expiração ou atualização de estado.",
        )

    if any(p in low for p in [
        "payload",
        "message.payload",
        "raw_payload",
        "value_template",
        "last_reset_value_template",
        "conf_value_template",
        "conf_last_reset_value_template",
    ]):
        return (
            "sim",
            "payload/template MQTT",
            "Afeta o processamento do payload MQTT ou o template usado para extrair o valor recebido.",
        )

    if any(p in low for p in [
        "state_topic",
        "availability_topic",
        "json_attributes_topic",
        "async_subscribe",
        "subscription",
        "topic",
        "conf_state_topic",
        "conf_availability_topic",
        "conf_json_attributes_topic",
    ]):
        return (
            "sim",
            "tópico/subscrição MQTT",
            "Afeta tópico, subscrição ou recebimento de mensagens MQTT.",
        )

    if any(p in low for p in [
        "expire_after",
        "expiration",
        "expires",
        "availability",
        "available",
        "async_track_point_in_utc_time",
    ]):
        return (
            "sim",
            "disponibilidade/expiração MQTT",
            "Afeta disponibilidade ou expiração do sensor após mensagens MQTT ou ausência delas.",
        )

    if any(p in low for p in [
        "native_value",
        "_attr_native_value",
        "async_write_ha_state",
        "force_update",
        "state_class",
        "last_reset",
        "state",
    ]):
        return (
            "sim",
            "atualização de estado MQTT",
            "Afeta o estado observável da entidade MQTT após o recebimento de mensagens.",
        )

    if any(p in low for p in [
        "mqtt_ro_schema",
        "platform_schema",
        "config_schema",
        "vol.",
        "config",
        "conf_",
    ]):
        return (
            "talvez",
            "schema/configuração MQTT",
            "Pode afetar a configuração do sensor MQTT, mas precisa de inspeção manual do diff.",
        )

    return (
        "não",
        "fora do fluxo MQTT observado",
        "Não há evidência no diff de relação direta com payload, tópico, subscrição, expiração ou estado MQTT.",
    )


def classify_template(diff):
    body = diff_body(diff)
    low = body.lower()

    # template.py é relacionado ao MQTT apenas de forma indireta,
    # quando o value_template do sensor MQTT passa por esse código.
    if any(p in low for p in [
        "async_render",
        "render(",
        "_render",
        "render_with_possible_json_value",
        "render_complex",
        "compiled.render",
        "template.render",
        "template_vars",
        "variables",
        "value",
        "result",
        "templateerror",
        "template_error",
        "undefinederror",
        "strictundefined",
        "jinja",
        "limited template",
    ]):
        return (
            "sim",
            "renderização/interpretação de template usado pelo MQTT",
            "Afeta a renderização ou interpretação de templates. No experimento, isso é relevante porque o fluxo MQTT usa value_template para transformar payload em estado.",
        )

    if any(p in low for p in [
        "template",
        "renderinfo",
        "tracktemplate",
        "templateenvironment",
        "environment",
        "cache",
        "compiled",
        "all_states",
        "entity_ids",
        "rate_limit",
        "time",
        "now",
        "parse",
        "exception",
    ]):
        return (
            "talvez",
            "infraestrutura de template potencialmente usada pelo MQTT",
            "Está no subsistema de templates e pode ser exercitado pelo value_template, mas precisa de inspeção manual para confirmar relação com o fluxo MQTT.",
        )

    return (
        "não",
        "template genérico não associado ao fluxo MQTT observado",
        "O diff não mostra relação clara com a renderização do value_template exercitado pelo sensor MQTT.",
    )


def analyze_module(module_name, module_dir, total, seed, fuzzers):
    module_dir = Path(module_dir)

    fuzzer_dirs = {}
    survivors_by_fuzzer = {}

    for fuzzer_dir in sorted(module_dir.iterdir()):
        if not fuzzer_dir.is_dir():
            continue

        fuzzer = fuzzer_dir.name

        if fuzzers and fuzzer not in fuzzers:
            continue

        sdir = seed_dir(module_dir, fuzzer, seed)
        results_file = sdir / "mutmut_results.txt"

        if not results_file.exists():
            continue

        survivors = parse_survivors(results_file)

        fuzzer_dirs[fuzzer] = sdir
        survivors_by_fuzzer[fuzzer] = survivors

    if not survivors_by_fuzzer:
        print(f"[AVISO] Nenhum resultado encontrado para {module_name}: {module_dir}")
        return []

    global_survivors = set(range(1, total + 1))
    for survivors in survivors_by_fuzzer.values():
        global_survivors &= survivors

    rows = []

    for mutant_id in sorted(global_survivors):
        diff, diff_path = load_diff(module_dir, fuzzer_dirs, seed, mutant_id)

        if module_name == "sensor.py":
            mqtt_related, category, reason = classify_sensor(diff)
        else:
            mqtt_related, category, reason = classify_template(diff)

        survived_in = ",".join(
            fuzzer for fuzzer, survivors in survivors_by_fuzzer.items()
            if mutant_id in survivors
        )

        rows.append({
            "module": module_name,
            "mutant_id": mutant_id,
            "mqtt_related": mqtt_related,
            "category": category,
            "reason": reason,
            "survived_in": survived_in,
            "diff_path": str(diff_path) if diff_path else "",
            "diff_excerpt": short_diff(diff),
        })

    print(f"[INFO] {module_name}")
    print(f"       Diretório: {module_dir}")
    print(f"       Fuzzers: {', '.join(survivors_by_fuzzer.keys())}")
    print(f"       Sobreviventes globais: {len(global_survivors)}")
    print(f"       MQTT/talvez MQTT: {sum(1 for r in rows if r['mqtt_related'] in {'sim', 'talvez'})}")

    return rows


def write_outputs(rows, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    all_csv = outdir / "sobreviventes_globais_sensor_template.csv"
    mqtt_csv = outdir / "sobreviventes_globais_sensor_template_mqtt_only.csv"
    excluded_csv = outdir / "sobreviventes_globais_sensor_template_excluidos.csv"
    md_file = outdir / "sobreviventes_globais_sensor_template_mqtt_only.md"

    fieldnames = [
        "module",
        "mutant_id",
        "mqtt_related",
        "category",
        "reason",
        "survived_in",
        "diff_path",
        "diff_excerpt",
    ]

    mqtt_rows = [r for r in rows if r["mqtt_related"] in {"sim", "talvez"}]
    excluded_rows = [r for r in rows if r["mqtt_related"] == "não"]

    for path, data in [
        (all_csv, rows),
        (mqtt_csv, mqtt_rows),
        (excluded_csv, excluded_rows),
    ]:
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    with md_file.open("w", encoding="utf-8") as f:
        f.write("# Mutantes sobreviventes relacionados ao fluxo MQTT\n\n")
        f.write("Critério: foram mantidos mutantes classificados como `sim` ou `talvez` em relação ao fluxo MQTT observado.\n\n")
        f.write("Em `sensor.py`, a relação é direta com payload, tópico, subscrição, expiração, disponibilidade ou atualização de estado MQTT.\n\n")
        f.write("Em `template.py`, a relação é indireta: o mutante é relevante quando afeta a renderização/interpretação de templates usados pelo `value_template` do sensor MQTT.\n\n")

        for module in ["sensor.py", "template.py"]:
            module_rows = [r for r in mqtt_rows if r["module"] == module]
            f.write(f"## {module}\n\n")
            f.write(f"Total classificado como MQTT/talvez MQTT: {len(module_rows)}\n\n")

            for r in module_rows:
                f.write(f"### Mutante {r['mutant_id']}\n\n")
                f.write(f"- Relação com MQTT: **{r['mqtt_related']}**\n")
                f.write(f"- Categoria: **{r['category']}**\n")
                f.write(f"- Justificativa: {r['reason']}\n")
                f.write(f"- Sobreviveu em: `{r['survived_in']}`\n")
                f.write(f"- Diff: `{r['diff_path']}`\n\n")
                f.write("```diff\n")
                f.write(r["diff_excerpt"])
                f.write("\n```\n\n")

    print()
    print("[OK] Arquivos gerados:")
    print(all_csv)
    print(mqtt_csv)
    print(excluded_csv)
    print(md_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sensor-dir", required=True)
    parser.add_argument("--template-dir", required=True)
    parser.add_argument("--seed", default="1")
    parser.add_argument("--sensor-total", type=int, default=126)
    parser.add_argument("--template-total", type=int, default=1452)
    parser.add_argument("--outdir", default="resultados_mutmut/analise_sobreviventes_mqtt_sensor_template")
    parser.add_argument("--fuzzers", nargs="*", default=None)
    args = parser.parse_args()

    rows = []

    rows.extend(analyze_module(
        module_name="sensor.py",
        module_dir=args.sensor_dir,
        total=args.sensor_total,
        seed=args.seed,
        fuzzers=args.fuzzers,
    ))

    rows.extend(analyze_module(
        module_name="template.py",
        module_dir=args.template_dir,
        total=args.template_total,
        seed=args.seed,
        fuzzers=args.fuzzers,
    ))

    write_outputs(rows, args.outdir)


if __name__ == "__main__":
    main()
