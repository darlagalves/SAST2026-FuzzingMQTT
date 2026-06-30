#!/usr/bin/env python3
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

BASE = Path("/home/darla/experimento")

MQTT_HOST = os.environ["MQTT_HOST"]
MQTT_PORT = os.environ.get("MQTT_PORT", "1883")
MQTT_TOPIC = os.environ["MQTT_TOPIC"]
HA_BASE_URL = os.environ["HA_BASE_URL"]
HA_TOKEN = os.environ["HA_TOKEN"]
HA_ENTITY_ID = os.environ["HA_ENTITY_ID"]

FUZZERS = ["boofuzz", "fume", "mqttgram", "mitm", "scapy"]

def get_state():
    req = urllib.request.Request(
        f"{HA_BASE_URL}/api/states/{HA_ENTITY_ID}",
        headers={
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            return data.get("state"), data.get("attributes", {})
    except Exception as e:
        return f"API_ERROR:{e}", {}

def publish(payload):
    subprocess.run(
        [
            "mosquitto_pub",
            "-h", MQTT_HOST,
            "-p", MQTT_PORT,
            "-t", MQTT_TOPIC,
            "-s",
        ],
        input=payload.encode("utf-8", errors="surrogatepass"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

out_dir = BASE / "resultados_mutmut" / "diagnostico_sensor"
out_dir.mkdir(parents=True, exist_ok=True)

summary = []

for fuzzer in FUZZERS:
    corpus = BASE / "resultados_mutmut" / "corpus" / "sensor" / fuzzer / "seed_1" / "payloads.jsonl"

    if not corpus.exists():
        summary.append((fuzzer, 0, 0, "sem corpus"))
        continue

    payloads = []
    with corpus.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                payloads.append(json.loads(line)["payload"])

    states = []
    details_file = out_dir / f"effects_{fuzzer}.tsv"

    with details_file.open("w", encoding="utf-8") as out:
        out.write("index\tpayload\tstate\n")

        for i, payload in enumerate(payloads[:100], start=1):
            publish(payload)
            time.sleep(0.1)
            state, attrs = get_state()
            states.append(str(state))
            out.write(f"{i}\t{payload!r}\t{state!r}\n")

    unique_states = sorted(set(states))
    summary.append((fuzzer, len(payloads), len(unique_states), ",".join(unique_states[:10])))

summary_file = out_dir / "corpus_effects_summary.tsv"

with summary_file.open("w", encoding="utf-8") as out:
    out.write("fuzzer\tpayloads\tunique_states\tfirst_states\n")
    for row in summary:
        out.write("\t".join(map(str, row)) + "\n")

print(summary_file)
