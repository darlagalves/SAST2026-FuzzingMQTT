#!/usr/bin/env bash
set -e

cd /home/darla/experimento

# 1. Inicia o MitM/Polymorph em background
./venv_polymorph/bin/python mitm_fuzzer.py &
MITM_PID=$!

sleep 3

# 2. Gera tráfego MQTT legítimo para ser mutado
./venv/bin/python harness/fuzzers/mqtt_seed_publisher.py || true

# 3. Encerra o MitM
kill "$MITM_PID" 2>/dev/null || true
wait "$MITM_PID" 2>/dev/null || true
