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

    # tenta pegar a quantidade de sobreviventes indicada pelo emoji do mutmut
    survived_count = None
    m = re.search(r"🙁\s*(\d+)", text)
    if m:
        survived_count = int(m.group(1))

    # blocos do tipo:
    # ---- survived mutants (106) ----
    # 1-8, 10...
    blocks = re.findall(
        r"----.*?\((\d+)\)\s*----\s*\n+\s*([0-9,\-\s,\n]+)",
        text,
        flags=re.DOTALL,
    )

    candidates = []
    for count_text, ids_text in blocks:
        ids = expand_ranges(ids_text)
        if ids:
            candidates.append((int(count_text), ids))

    if survived_count is not None:
        for count_text, ids in candidates:
            if len(ids) == survived_count or count_text == survived_count:
                return ids

    # fallback: mantém compatibilidade com o script antigo
    if candidates:
        return candidates[0][1]

    raise RuntimeError(f"Não consegui extrair sobreviventes de {results_file}")

def load_diff(backup_dir, fuzzers, seed, mutant_id):
    candidates = []

    for fuzzer in fuzzers:
        candidates.append(
            backup_dir / fuzzer / f"seed_{seed}" / "mutant_diffs" / f"mutant_{mutant_id}.diff"
        )

    # fallback: tenta achar em qualquer lugar dentro do backup
    candidates.extend(backup_dir.glob(f"**/mutant_{mutant_id}.diff"))

    for path in candidates:
        if path.exists():
            return path.read_text(errors="ignore"), path

    return "", None

def classify(diff):
    body_lines = []
    for line in diff.splitlines():
        if line.startswith("--- ") or line.startswith("+++ "):
            continue
        body_lines.append(line)

    body = "\n".join(body_lines)
    low = body.lower()

    # Exclusões: estão em sensor.py, mas são metadados/configuração genérica,
    # não comportamento MQTT observável do payload/tópico.
    exclude_patterns = [
        "default_name",
        "mqtt sensor",
        "suggested_display_precision",
        "default_entity_id",
        "translation_key",
        "icon",
        "device_class",
        "unit_of_measurement",
        "native_unit_of_measurement",
        "entity_category",
    ]

    if any(p in low for p in exclude_patterns):
        return (
            "não",
            "metadata/configuração de sensor",
            "Baixa relação com MQTT: altera metadados ou configuração geral da entidade, não o processamento de mensagens MQTT.",
        )

    if any(p in low for p in [
        "message.payload",
        "payload",
        "raw_payload",
        "value_template",
        "last_reset_value_template",
        "template",
    ]):
        return (
            "sim",
            "processamento de payload/template MQTT",
            "Relacionado ao caminho principal MQTT, pois afeta payload, template ou extração/conversão de valor recebido via mensagem.",
        )

    if any(p in low for p in [
        "state_topic",
        "availability_topic",
        "json_attributes_topic",
        "async_subscribe",
        "subscription",
        "topic",
        "mqtt_subscribe",
    ]):
        return (
            "sim",
            "subscrição/tópico MQTT",
            "Relacionado ao MQTT porque afeta tópico, subscrição ou recebimento de mensagens.",
        )

    if any(p in low for p in [
        "expire_after",
        "expiration",
        "async_track_point_in_utc_time",
        "expires",
        "availability",
        "available",
    ]):
        return (
            "sim",
            "disponibilidade/expiração MQTT",
            "Relacionado ao comportamento observável do sensor MQTT após mensagens ou ausência de mensagens.",
        )

    if any(p in low for p in [
        "native_value",
        "_attr_native_value",
        "state",
        "force_update",
        "state_class",
        "last_reset",
    ]):
        return (
            "sim",
            "atualização de estado do sensor MQTT",
            "Relacionado ao efeito observado das mensagens MQTT no estado da entidade.",
        )

    if any(p in low for p in [
        "mqtt_ro_schema",
        "platform_schema",
        "config_schema",
        "config_entry",
        "conf_state_topic",
        "conf_value_template",
        "conf_json_attributes",
        "conf_last_reset_value_template",
        "vol.",
    ]):
        return (
            "talvez",
            "schema/configuração MQTT",
            "Relaciona-se à configuração do sensor MQTT, mas precisa de inspeção manual para confirmar se afeta o fluxo de mensagens.",
        )

    return (
        "não",
        "fora do fluxo MQTT observado",
        "Não há evidência no diff de relação direta com payload, tópico, subscrição, expiração ou atualização de estado MQTT.",
    )

def short_diff(diff, max_lines=10):
    lines = []
    for line in diff.splitlines():
        if line.startswith("@@") or line.startswith("-") or line.startswith("+"):
            lines.append(line)
    return "\\n".join(lines[:max_lines])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", required=True)
    parser.add_argument("--seed", default="1")
    parser.add_argument("--total", type=int, default=126)
    parser.add_argument("--outdir", default="resultados_mutmut/analise_sobreviventes_mqtt")
    args = parser.parse_args()

    backup_dir = Path(args.backup)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    fuzzers = []
    survivors_by_fuzzer = {}

    for child in sorted(backup_dir.iterdir()):
        if not child.is_dir():
            continue

        results_file = child / f"seed_{args.seed}" / "mutmut_results.txt"
        if not results_file.exists():
            continue

        fuzzer = child.name
        survivors = parse_survivors(results_file)

        fuzzers.append(fuzzer)
        survivors_by_fuzzer[fuzzer] = survivors

    if not fuzzers:
        raise SystemExit(f"[ERRO] Não encontrei mutmut_results.txt em {backup_dir}")

    global_survivors = set(range(1, args.total + 1))
    for survivors in survivors_by_fuzzer.values():
        global_survivors &= survivors

    rows = []

    for mutant_id in sorted(global_survivors):
        diff, diff_path = load_diff(backup_dir, fuzzers, args.seed, mutant_id)
        mqtt_related, category, reason = classify(diff)

        survived_in = ",".join(
            fuzzer for fuzzer in fuzzers if mutant_id in survivors_by_fuzzer[fuzzer]
        )

        rows.append({
            "mutant_id": mutant_id,
            "mqtt_related": mqtt_related,
            "category": category,
            "reason": reason,
            "survived_in": survived_in,
            "diff_path": str(diff_path) if diff_path else "",
            "diff_excerpt": short_diff(diff),
        })

    all_csv = outdir / "sobreviventes_globais_sensor.csv"
    mqtt_csv = outdir / "sobreviventes_globais_sensor_mqtt_only.csv"
    excluded_csv = outdir / "sobreviventes_globais_sensor_excluidos.csv"
    md_file = outdir / "sobreviventes_globais_sensor_mqtt_only.md"

    fieldnames = [
        "mutant_id",
        "mqtt_related",
        "category",
        "reason",
        "survived_in",
        "diff_path",
        "diff_excerpt",
    ]

    with all_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    mqtt_rows = [r for r in rows if r["mqtt_related"] in {"sim", "talvez"}]
    excluded_rows = [r for r in rows if r["mqtt_related"] == "não"]

    with mqtt_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mqtt_rows)

    with excluded_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(excluded_rows)

    with md_file.open("w", encoding="utf-8") as f:
        f.write("# Mutantes sobreviventes relacionados ao MQTT — sensor.py\n\n")
        f.write(f"Backup analisado: `{backup_dir}`\n\n")
        f.write(f"Fuzzers encontrados: `{', '.join(fuzzers)}`\n\n")
        f.write(f"Total de mutantes: {args.total}\n\n")
        f.write(f"Sobreviventes globais: {len(global_survivors)}\n\n")
        f.write(f"Sobreviventes classificados como MQTT/talvez MQTT: {len(mqtt_rows)}\n\n")

        for r in mqtt_rows:
            f.write(f"## Mutante {r['mutant_id']}\n\n")
            f.write(f"- Relação com MQTT: **{r['mqtt_related']}**\n")
            f.write(f"- Categoria: **{r['category']}**\n")
            f.write(f"- Justificativa: {r['reason']}\n")
            f.write(f"- Sobreviveu em: `{r['survived_in']}`\n")
            f.write(f"- Diff: `{r['diff_path']}`\n\n")
            f.write("```diff\n")
            f.write(r["diff_excerpt"])
            f.write("\n```\n\n")

    print("[OK] Análise concluída")
    print(f"[INFO] Backup: {backup_dir}")
    print(f"[INFO] Fuzzers encontrados: {', '.join(fuzzers)}")
    print(f"[INFO] Sobreviventes globais: {len(global_survivors)}")
    print(f"[INFO] MQTT/talvez MQTT: {len(mqtt_rows)}")
    print()
    print(f"[CSV completo] {all_csv}")
    print(f"[CSV MQTT] {mqtt_csv}")
    print(f"[CSV excluídos] {excluded_csv}")
    print(f"[Markdown MQTT] {md_file}")

if __name__ == "__main__":
    main()
