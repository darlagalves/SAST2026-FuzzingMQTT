#!/usr/bin/env python3
import re
import sys
from pathlib import Path

TOTAL = 126

def expand_ranges(text):
    ids = set()
    text = text.replace("\n", " ").replace("\t", " ")
    for part in text.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            ids.update(range(int(a), int(b) + 1))
        else:
            ids.add(int(part))
    return ids

def parse_survivors(path):
    text = Path(path).read_text(errors="ignore")
    m = re.search(
        r"----.*?\(\d+\)\s*----\s*\n+\s*([0-9,\-\s,\n]+)",
        text,
        flags=re.DOTALL,
    )
    if not m:
        raise RuntimeError(f"Não consegui ler sobreviventes de {path}")
    return expand_ranges(m.group(1))

all_ids = set(range(1, TOTAL + 1))
killed_by_any = set()

for path in sys.argv[1:]:
    survivors = parse_survivors(path)
    killed = all_ids - survivors
    print(f"{path}: survived={len(survivors)} killed={len(killed)}")
    killed_by_any |= killed

out = Path("resultados_mutmut/mqtt_observed_space/sensor_killed_ids.txt")
out.parent.mkdir(parents=True, exist_ok=True)

out.write_text("\n".join(map(str, sorted(killed_by_any))) + "\n")

print()
print("[OK] Mortos por qualquer campanha:")
print(" ".join(map(str, sorted(killed_by_any))))
print(f"[OK] Arquivo salvo em: {out}")
