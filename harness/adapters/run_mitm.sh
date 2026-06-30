#!/usr/bin/env bash
set -e

cd /home/darla/experimento

exec sudo ./venv_polymorph/bin/python mitm_fuzzer.py
