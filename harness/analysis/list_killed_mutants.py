#!/usr/bin/env python3
import re
import sys
from pathlib import Path

TOTAL = int(sys.argv[1])
RESULTS_FILE = Path(sys.argv[2])

def expand_ranges(text):
    ids = set()
    for part in text.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            ids.update(range(int(a), int(b) + 1))
        else:
            ids.add(int(part))
    return ids

text = RESULTS_FILE.read_text(errors="ignore")

m = re.search(r"----.*?\(\d+\)\s*----\s*\n\n([0-9,\-\s]+)", text, re.DOTALL)

if not m:
    print("[ERRO] Não consegui encontrar lista de sobreviventes.")
    sys.exit(1)

survived = expand_ranges(m.group(1))
all_ids = set(range(1, TOTAL + 1))
killed = sorted(all_ids - survived)

print(" ".join(map(str, killed)))
