#!/usr/bin/env python3
import os
import time
import random
import json
import sys

sys.path.append("/home/darla/experimento/harness/fuzzers")
from common_mqtt_publisher import publish_payload


FUZZ_DURATION = int(os.environ.get("FUZZ_DURATION", "60"))
FUZZ_SEED = int(os.environ.get("FUZZ_SEED", "1"))

random.seed(FUZZ_SEED)


GRAMMAR_VALUES = [
    "22.5",
    "0",
    "-5.5",
    "999999999999999999999",
    "-999999999999999999999",
    "null",
    "true",
    "false",
    '"abc"',
    '""',
    "[]",
    "{}",
]


def mqttgram_style_payload():
    choice = random.randint(0, 8)

    if choice == 0:
        return '{"temperature": %s}' % random.choice(GRAMMAR_VALUES)

    if choice == 1:
        return '{"temperature": %s, "last_reset": "invalido"}' % random.choice(GRAMMAR_VALUES)

    if choice == 2:
        return '{"temperature": %s, "unit": "%s"}' % (
            random.choice(GRAMMAR_VALUES),
            random.choice(["C", "F", "", "null", "🔥"]),
        )

    if choice == 3:
        return '{"temperature": '

    if choice == 4:
        return '{"temp": 22.5}'

    if choice == 5:
        return '{}'

    if choice == 6:
        return '[]'

    if choice == 7:
        return '{"temperature": {"nested": [1,2,3]}}'

    return '{"temperature": "\u0000\u0001\u0002"}'


def main():
    start = time.time()
    count = 0

    print(f"[MQTTGRAM-HA] Publicando por {FUZZ_DURATION}s")

    while time.time() - start < FUZZ_DURATION:
        publish_payload(mqttgram_style_payload())
        count += 1
        time.sleep(0.05)

    print(f"[MQTTGRAM-HA] Mensagens publicadas: {count}")


if __name__ == "__main__":
    main()
