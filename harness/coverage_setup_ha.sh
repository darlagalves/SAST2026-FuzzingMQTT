#!/usr/bin/env bash
set -euo pipefail

cd /home/darla/experimento
source harness/config/experimento.env

mkdir -p harness/coverage

cat > harness/coverage/sitecustomize.py <<'PY'
import atexit
import os
import signal
import traceback

LOG = "/tmp/coverage_debug.log"

def log(msg):
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(str(msg) + "\n")
    except Exception:
        pass

log(f"[sitecustomize] imported pid={os.getpid()}")

if os.path.exists("/tmp/enable_ha_coverage"):
    try:
        import coverage

        log("[coverage] enable file found")

        cov = coverage.Coverage(
            data_file="/tmp/.coverage.ha",
            include=[
                "/usr/src/homeassistant/homeassistant/components/mqtt/sensor.py",
                "/usr/src/homeassistant/homeassistant/helpers/template.py",
                "/usr/src/homeassistant/homeassistant/components/mqtt/__init__.py",
            ],
            concurrency=["thread"],
            timid=True,
        )
        cov.start()
        log("[coverage] started")

        def save_coverage(*_args):
            try:
                cov.stop()
                cov.save()
                log("[coverage] saved by SIGUSR1")
            except Exception:
                log("[coverage] save failed")
                log(traceback.format_exc())

        def reset_coverage(*_args):
            try:
                cov.erase()
                log("[coverage] erased by SIGUSR2")
            except Exception:
                log("[coverage] erase failed")
                log(traceback.format_exc())

        def finish():
            try:
                cov.stop()
                cov.save()
                log("[coverage] saved by atexit")
            except Exception:
                log("[coverage] atexit failed")
                log(traceback.format_exc())

        signal.signal(signal.SIGUSR1, save_coverage)
        signal.signal(signal.SIGUSR2, reset_coverage)
        atexit.register(finish)

    except Exception:
        log("[coverage] startup failed")
        log(traceback.format_exc())
PY

echo "[INFO] Instalando coverage no container..."
docker exec "$HA_CONTAINER" python3 -m pip install coverage >/dev/null

SITE_PACKAGES=$(docker exec "$HA_CONTAINER" python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')

echo "[INFO] site-packages: $SITE_PACKAGES"

if [ -z "$SITE_PACKAGES" ]; then
    echo "[ERRO] Não consegui descobrir site-packages."
    exit 1
fi

docker exec "$HA_CONTAINER" rm -f /sitecustomize.py || true
docker cp harness/coverage/sitecustomize.py "$HA_CONTAINER:$SITE_PACKAGES/sitecustomize.py"

echo "[OK] Coverage preparado no container em: $SITE_PACKAGES/sitecustomize.py"
