#!/usr/bin/env bash
set -e

cd /home/darla/experimento

exec ./venv/bin/python harness/fuzzers/fume_ha_publisher.py
