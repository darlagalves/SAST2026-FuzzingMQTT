import os
import time
import random
import json
import string
import subprocess

MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = os.environ.get("MQTT_PORT", "1883")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "homeassistant/sensor/temp")
FUZZ_DURATION = int(os.environ.get("FUZZ_DURATION", "60"))
FUZZ_SEED = int(os.environ.get("FUZZ_SEED", "1"))

random.seed(FUZZ_SEED)


def random_string(max_len=256):
    size = random.randint(0, max_len)
    alphabet = string.ascii_letters + string.digits + "{}[],:;\"'\\/\x00\n\r\t"
    return "".join(random.choice(alphabet) for _ in range(size))


def generate_payload():
    choices = [
        lambda: json.dumps({"temperature": random.uniform(-1000, 1000)}),
        lambda: json.dumps({"temperature": random.choice([None, True, False, "", [], {}, "abc"])}),
        lambda: json.dumps({"temperature": random_string(64)}),
        lambda: "{}",
        lambda: "[]",
        lambda: "",
        lambda: random_string(512),
        lambda: '{"temperature": ',
        lambda: '{"temperature": null}',
        lambda: '{"temperature": "abc"}',
        lambda: '{"temperature": 999999999999999999999999}',
        lambda: '{"temperature": -999999999999999999999999}',
        lambda: '{"temperature": 22.5, "last_reset": "invalido"}',
    ]

    return random.choice(choices)()


def publish(payload):
    cmd = [
        "mosquitto_pub",
        "-h", MQTT_HOST,
        "-p", MQTT_PORT,
        "-t", MQTT_TOPIC,
        "-s",
    ]

    if isinstance(payload, str):
        payload_bytes = payload.encode("utf-8", errors="surrogateescape")
    else:
        payload_bytes = payload

    subprocess.run(
        cmd,
        input=payload_bytes,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        timeout=2,
    )

def main():
    print(f"[SCAPY-ADAPTER] Iniciando fuzzing por {FUZZ_DURATION}s")
    print(f"[SCAPY-ADAPTER] Broker: {MQTT_HOST}:{MQTT_PORT}")
    print(f"[SCAPY-ADAPTER] Topic: {MQTT_TOPIC}")

    start = time.time()
    count = 0

    while time.time() - start < FUZZ_DURATION:
        payload = generate_payload()
        publish(payload)
        count += 1
        time.sleep(0.05)

    print(f"[SCAPY-ADAPTER] Mensagens enviadas: {count}")


if __name__ == "__main__":
    main()
