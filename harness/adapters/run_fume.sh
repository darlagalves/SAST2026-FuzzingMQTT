#!/usr/bin/env bash
set -e

cd /home/darla/experimento/FUME-Fuzzing-MQTT-Brokers

exec ./venv_fume/bin/python fuzz.py