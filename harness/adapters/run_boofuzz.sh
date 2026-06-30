#!/usr/bin/env bash
set -e

echo "[DEBUG_BOOFUZZ] executado em $(date)" >> /home/darla/experimento/resultados_mutmut/debug_fuzzers.log

echo "[DEBUG_BOOFUZZ] run_boofuzz.sh foi executado em $(date)" >> /home/darla/experimento/resultados_mutmut/debug_fuzzer_cmd.log
echo "[DEBUG_BOOFUZZ] MQTT_TOPIC=$MQTT_TOPIC" >> /home/darla/experimento/resultados_mutmut/debug_fuzzer_cmd.log
echo "[DEBUG_BOOFUZZ] FUZZ_DURATION=$FUZZ_DURATION" >> /home/darla/experimento/resultados_mutmut/debug_fuzzer_cmd.log
echo "[DEBUG_BOOFUZZ] FUZZER_SEED=$FUZZER_SEED" >> /home/darla/experimento/resultados_mutmut/debug_fuzzer_cmd.log

cd /home/darla/experimento

exec ./venv_boofuzz/bin/python harness/fuzzers/boofuzz_mqtt.py
