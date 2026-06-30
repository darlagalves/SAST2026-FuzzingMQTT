import os
import subprocess


MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = os.environ.get("MQTT_PORT", "1883")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "homeassistant/sensor/temp")


def publish_payload(payload) -> None:
    if isinstance(payload, str):
        payload_bytes = payload.encode("utf-8", errors="replace")
    else:
        payload_bytes = bytes(payload)

    subprocess.run(
        [
            "mosquitto_pub",
            "-h", MQTT_HOST,
            "-p", MQTT_PORT,
            "-t", MQTT_TOPIC,
            "-s",
        ],
        input=payload_bytes,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        timeout=3,
    )