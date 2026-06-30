"""Gera baseline.json a partir do Home Assistant original, sem mutantes."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

import requests

ROOT_DIR = Path(__file__).resolve().parent
HA_BASE_URL = os.environ.get("HA_BASE_URL", "http://127.0.0.1:8123").rstrip("/")
HA_ENTITY_ID = os.environ.get("HA_ENTITY_ID", "sensor.sensor_fuzzing")
HA_STATE_URL = f"{HA_BASE_URL}/api/states/{HA_ENTITY_ID}"
HA_TOKEN = os.environ.get("HA_TOKEN", "")
MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = os.environ.get("MQTT_PORT", "1883")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "homeassistant/sensor/temp")
MQTT_PAYLOAD = os.environ.get("MQTT_PAYLOAD", '{"temperature": 22.5}')
BASELINE_FILE = Path(os.environ.get("BASELINE_FILE", ROOT_DIR / "baseline.json"))

HEADERS = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}


def publish_canary() -> None:
    subprocess.run(
        [
            "mosquitto_pub",
            "-h",
            MQTT_HOST,
            "-p",
            str(MQTT_PORT),
            "-t",
            MQTT_TOPIC,
            "-m",
            MQTT_PAYLOAD,
        ],
        check=True,
    )


def get_state() -> dict[str, Any]:
    if not HA_TOKEN:
        raise SystemExit("Defina HA_TOKEN antes de coletar baseline.")
    response = requests.get(HA_STATE_URL, headers=HEADERS, timeout=5)
    if response.status_code != 200:
        raise SystemExit(f"Falha ao consultar estado: HTTP {response.status_code} - {response.text[:300]}")
    return response.json()


def main() -> None:
    publish_canary()
    time.sleep(2)
    state_payload = get_state()
    baseline = {
        "entity_id": HA_ENTITY_ID,
        "mqtt_topic": MQTT_TOPIC,
        "mqtt_payload": MQTT_PAYLOAD,
        "state": state_payload.get("state"),
        "attributes": state_payload.get("attributes", {}),
        "collected_at_epoch": int(time.time()),
    }
    BASELINE_FILE.write_text(json.dumps(baseline, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Baseline salvo em {BASELINE_FILE}: state={baseline['state']!r}")


if __name__ == "__main__":
    main()
