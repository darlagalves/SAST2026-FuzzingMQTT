#!/usr/bin/env python3
import re
import sys
from pathlib import Path

TOTAL = 126

def expand_ranges(text):
    ids = set()

    # aceita IDs separados por vírgula, espaço ou quebra de linha
    text = text.replace(",", " ")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

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

def read_ids(path):
    path = Path(path)
    if not path.exists():
        return set()
    return expand_ranges(path.read_text(errors="ignore"))

def load_diff(diff_dir, mid):
    path = Path(diff_dir) / f"mutant_{mid}.diff"
    if not path.exists():
        return "", path
    return path.read_text(errors="ignore"), path

def classify_sensor(diff):
    low = diff.lower()

    # Excluir mutantes que parecem ser apenas logging, decorator, type hint,
    # metadados ou configuração não observada no fluxo MQTT.
    exclude = [
        "_logger",
        "logger.",
        "logging.getlogger",
        "xxstate recovered",
        "xx expiring",
        "xxclean up",
        "xxinvalid",
        "xxignore",
        "xxignoring",
        "@callback",
        "@staticmethod",
        "@property",
        "default_name",
        "mqtt sensor",
        "suggested_display_precision",
        "translation_key",
        "icon",
        "device_class",
        "unit_of_measurement",
        "native_unit_of_measurement",
        "entity_description",
        "callback_type & none",
        "callable[[receivepayloadtype",
    ]

    if any(x in low for x in exclude):
        return None

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

    if any(x in low for x in [
        "discovery_schema",
        "platform_schema",
        "mqtt_ro_schema",
        "conf_",
        "config",
        "schema",
        "vol.",
    ]):
        return "S5: MQTT schema/configuration"

    return None

def main():
    if len(sys.argv) < 5:
        raise SystemExit(
            "Uso:\n"
            "python build_sensor_mqtt_space_ids.py "
            "<diff_dir> <killed_ids_file> <mutmut_results_1> <mutmut_results_2> <mutmut_results_3>"
        )

    diff_dir = Path(sys.argv[1])
    killed_file = Path(sys.argv[2])
    result_files = [Path(x) for x in sys.argv[3:]]

    all_ids = set(range(1, TOTAL + 1))
    killed_ids = read_ids(killed_file)

    global_survivors = all_ids.copy()
    for rf in result_files:
        survivors = parse_survivors(rf)
        global_survivors &= survivors

    rows = []
    mqtt_survivors = set()

    for mid in sorted(global_survivors):
        diff, diff_path = load_diff(diff_dir, mid)
        cls = classify_sensor(diff)

        if cls is not None:
            mqtt_survivors.add(mid)
            rows.append((mid, cls, diff_path))

    mqtt_space = killed_ids | mqtt_survivors

    outdir = Path("resultados_mutmut/mqtt_observed_space")
    outdir.mkdir(parents=True, exist_ok=True)

    (outdir / "sensor_surviving_mqtt_ids.txt").write_text(
        "\n".join(map(str, sorted(mqtt_survivors))) + "\n"
    )

    (outdir / "sensor_ids.txt").write_text(
        "\n".join(map(str, sorted(mqtt_space))) + "\n"
    )

    with (outdir / "sensor_surviving_mqtt_classification.csv").open("w", encoding="utf-8") as f:
        f.write("mutant_id,class,diff_path\n")
        for mid, cls, path in rows:
            f.write(f"{mid},{cls},{path}\n")

    print("[OK] Resultado sensor.py")
    print(f"Mortos por qualquer fuzzer: {len(killed_ids)}")
    print(f"Sobreviventes globais: {len(global_survivors)}")
    print(f"Sobreviventes classificados como MQTT: {len(mqtt_survivors)}")
    print(f"Total MQTT-related: {len(mqtt_space)}")
    print()
    print("Arquivos gerados:")
    print(outdir / "sensor_killed_ids.txt")
    print(outdir / "sensor_surviving_mqtt_ids.txt")
    print(outdir / "sensor_ids.txt")
    print(outdir / "sensor_surviving_mqtt_classification.csv")

    print()
    print("IDs sobreviventes MQTT:")
    print(" ".join(map(str, sorted(mqtt_survivors))))

if __name__ == "__main__":
    main()
