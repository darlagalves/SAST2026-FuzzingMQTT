#!/usr/bin/env bash
set -e

cd /home/darla/experimento

exec ./venv/bin/python harness/fuzzers/scapy_mqtt.py
