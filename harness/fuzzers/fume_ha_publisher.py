#!/usr/bin/env python3
import os
import time
import random
import string
import json
import sys

sys.path.append("/home/darla/experimento/harness/fuzzers")
from common_mqtt_publisher import publish_payload


FUZZ_DURATION = int(os.environ.get("FUZZ_DURATION", "60"))
FUZZ_SEED = int(os.environ.get("FUZZ_SEED", "1"))

random.seed(FUZZ_SEED)


def rand_text(n):
    alphabet = string.ascii_letters + string.digits + "{}[],:;\"'\\/\n\r\t"
    return "".join(random.choice(alphabet) for _ in range(n))


def fume_style_payload():
    options = [
        '{"temperature": %s}' % random.randint(-10000, 10000),
        '{"temperature": "%s"}' % rand_text(random.randint(0, 100)),
        '{"temperature": null}',
        '{"temperature": true}',
        '{"temperature": false}',
        '{"temperature": []}',
        '{"temperature": {}}',
        '{}',
        '[' + rand_text(50) + ']',
        rand_text(random.randint(0, 300)),
        '{"temperature": ',
        '{"temperature": 22.5, "last_reset": "invalido"}',
    ]
    return random.choice(options)


def main():
    start = time.time()
    count = 0

    print(f"[FUME-HA] Publicando por {FUZZ_DURATION}s")

    while time.time() - start < FUZZ_DURATION:
        publish_payload(fume_style_payload())
        count += 1
        time.sleep(0.05)

    print(f"[FUME-HA] Mensagens publicadas: {count}")


if __name__ == "__main__":
    main()
