#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
import urllib.request
import hashlib
from pathlib import Path

BASE = Path("/home/darla/experimento")

FUZZER_NAME = os.environ["FUZZER_NAME"]
FUZZER_SEED = os.environ.get("FUZZER_SEED", "1")

MQTT_HOST = os.environ["MQTT_HOST"]
MQTT_PORT = os.environ.get("MQTT_PORT", "1883")
MQTT_TOPIC = os.environ["MQTT_TOPIC"]

HA_BASE_URL = os.environ["HA_BASE_URL"]
HA_TOKEN = os.environ["HA_TOKEN"]
HA_ENTITY_ID = os.environ["HA_ENTITY_ID"]

REPLAY_LIMIT = int(os.environ.get("REPLAY_LIMIT", "100"))
REPLAY_DELAY = float(os.environ.get("REPLAY_DELAY", "0.05"))
TRACE_OUT = os.environ.get("TRACE_OUT")

RESET_PAYLOAD = os.environ.get("RESET_PAYLOAD", '{"temperature": 22.5}')

corpus_file = (
    BASE
    / "resultados_mutmut"
    / "corpus"
    / "sensor"
    / FUZZER_NAME
    / f"seed_{FUZZER_SEED}"
    / "payloads.jsonl"
)

if not corpus_file.exists():
    print(f"[ERRO] Corpus não encontrado: {corpus_file}", file=sys.stderr)
    sys.exit(2)


def normalize_payload(raw: str) -> str:
    digest = hashlib.sha256(raw.encode("utf-8", errors="surrogatepass")).hexdigest()
    n = int(digest[:12], 16)
    value = (n % 2000000) / 1000.0 - 1000.0
    return json.dumps({"temperature": value}, ensure_ascii=False)


def publish(payload: str) -> None:
    subprocess.run(
        [
            "mosquitto_pub",
            "-h", MQTT_HOST,
            "-p", str(MQTT_PORT),
            "-t", MQTT_TOPIC,
            "-s",
        ],
        input=payload.encode("utf-8", errors="surrogatepass"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def get_state() -> str:
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
            return str(data.get("state", ""))
    except Exception as exc:
        return f"API_ERROR:{type(exc).__name__}"


payloads = []

with corpus_file.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            payloads.append(json.loads(line)["payload"])

payloads = payloads[:REPLAY_LIMIT]

print(
    f"[SEMANTIC_REPLAY] fuzzer={FUZZER_NAME} seed={FUZZER_SEED} "
    f"payloads={len(payloads)} topic={MQTT_TOPIC}"
)

publish(RESET_PAYLOAD)
time.sleep(1)

trace_fp = None

if TRACE_OUT:
    trace_path = Path(TRACE_OUT)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace_fp = trace_path.open("w", encoding="utf-8")

for i, raw_payload in enumerate(payloads, start=1):
    normalized = normalize_payload(raw_payload)

    publish(normalized)
    time.sleep(REPLAY_DELAY)

    if trace_fp:
        state = get_state()
        trace_fp.write(
            json.dumps(
                {
                    "index": i,
                    "state": state,
                    "normalized_payload": normalized,
                },
                ensure_ascii=False,
            )
            + "\n"
        )
        trace_fp.flush()

if trace_fp:
    trace_fp.close()

time.sleep(1)
print("[SEMANTIC_REPLAY] finalizado")
