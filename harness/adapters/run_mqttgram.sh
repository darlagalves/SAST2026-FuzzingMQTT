#!/usr/bin/env bash
set -e

cd /home/darla/experimento/MQTTGRAM

exec sudo ./venv_mqttgram/bin/python fuzz.py
