#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path("/home/darla/experimento")
COV = BASE / "resultados_mutmut" / "coverage_mqtt" / "coverage_mqtt.json"
OUT_DIR = BASE / "resultados_mutmut" / "coverage_mqtt"

TARGETS = {
    "sensor": "components/mqtt/sensor.py",
    "template": "helpers/template.py",
}

if not COV.exists():
    raise SystemExit(f"[ERRO] Coverage não encontrado: {COV}")

data = json.loads(COV.read_text(encoding="utf-8"))

files = data.get("files", {})

for module, suffix in TARGETS.items():
    matched = None

    for path, info in files.items():
        if path.endswith(suffix):
            matched = info
            break

    out = OUT_DIR / f"{module}_covered_lines.txt"

    if not matched:
        out.write_text("", encoding="utf-8")
        print(f"[AVISO] Não encontrei coverage para {module}: {suffix}")
        continue

    lines = sorted(set(matched.get("executed_lines", [])))

    out.write_text("\n".join(map(str, lines)) + "\n", encoding="utf-8")

    print(f"[OK] {module}: {len(lines)} linhas cobertas -> {out}")
