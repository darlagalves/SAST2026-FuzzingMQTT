#!/usr/bin/env python3
import os
import time
import random
import sys

sys.path.append("/home/darla/experimento/harness/fuzzers")
from common_mqtt_publisher import publish_payload


FUZZ_DURATION = int(os.environ.get("FUZZ_DURATION", "60"))
FUZZ_SEED = int(os.environ.get("FUZZ_SEED", "1"))

random.seed(FUZZ_SEED)

SEEDS = [
    '{"temperature": 22.5}',
    '{"temperature": 10.0}',
    '{"temperature": 0}',
    '{"temperature": -5.5}',
    '{"temperature": null}',
    '{"temperature": "abc"}',
    '{}',
    '{"temperature": 22.5, "last_reset": "invalido"}',
]


def main():
    start = time.time()
    count = 0

    print(f"[MITM-SEED] Publicando sementes por {FUZZ_DURATION}s")

    while time.time() - start < FUZZ_DURATION:
        publish_payload(random.choice(SEEDS))
        count += 1
        time.sleep(0.1)

    print(f"[MITM-SEED] Mensagens publicadas: {count}")


if __name__ == "__main__":
    main()
