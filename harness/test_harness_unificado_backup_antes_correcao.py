"""
Harness unificado para comparar fuzzers MQTT contra o Home Assistant.

Uso básico:
    source harness/config/experimento.env
    FUZZER_CMD=/home/darla/experimento/harness/adapters/run_boofuzz.sh \
        python3 -m unittest harness/test_harness_unificado.py

Ideia central:
    - O setUp reinicia o Home Assistant e estabiliza o estado baseline.
    - O fuzzer/adaptador roda uma única vez.
    - Enquanto o fuzzer roda, o harness monitora processo, logs e estado.
    - Se houver divergência observável, o teste falha de propósito.
      Para o mutmut, essa falha significa: mutante morto.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
import time
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


# ---------------------------------------------------------------------------
# Configuração geral do ambiente
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.environ.get("EXP_ROOT", ROOT_DIR.parent)).resolve()
RESULTS_DIR = Path(os.environ.get("RESULTS_DIR", ROOT_DIR / "results")).resolve()
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

HA_CONTAINER = os.environ.get("HA_CONTAINER", "ha-test")
HA_BASE_URL = os.environ.get("HA_BASE_URL", "http://127.0.0.1:8123").rstrip("/")
HA_ENTITY_ID = os.environ.get("HA_ENTITY_ID", "sensor.sensor_fuzzing")
HA_STATE_URL = f"{HA_BASE_URL}/api/states/{HA_ENTITY_ID}"
HA_TOKEN = os.environ.get("HA_TOKEN", "")

MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "homeassistant/sensor/temp")
MQTT_PAYLOAD = os.environ.get("MQTT_PAYLOAD", '{"temperature": 22.5}')

FUZZER_TOOL = os.environ.get("FUZZER_TOOL", "scapy").lower()
FUZZ_DURATION = int(os.environ.get("FUZZ_DURATION", "60"))
FUZZ_TIMEOUT = int(os.environ.get("FUZZ_TIMEOUT", str(FUZZ_DURATION + 10)))
FUZZ_SEED = os.environ.get("FUZZ_SEED", "1")

STARTUP_SLEEP = int(os.environ.get("STARTUP_SLEEP", "12"))
CANARY_WAIT = int(os.environ.get("CANARY_WAIT", "10"))
MONITOR_INTERVAL = float(os.environ.get("MONITOR_INTERVAL", "0.5"))
TERMINATE_GRACE = int(os.environ.get("TERMINATE_GRACE", "5"))

# Seu experimento usa baseline.json na raiz. Se BASELINE_FILE estiver no .env,
# ele terá prioridade.
BASELINE_FILE = Path(os.environ.get("BASELINE_FILE", PROJECT_ROOT / "baseline.json")).resolve()
EXPECTED_STATE = os.environ.get("EXPECTED_STATE", "")

# Evite usar a palavra genérica "ERROR" sozinha, pois o Home Assistant pode gerar
# erros não relacionados durante inicialização. Inclua padrões mais específicos se necessário.
LOG_PATTERNS = [
    p.strip()
    for p in os.environ.get(
        "ORACLE_LOG_PATTERNS",
        "Traceback,Exception,ERROR (MainThread) [homeassistant.components.mqtt]",
    ).split(",")
    if p.strip()
]

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}


@dataclass
class FuzzerAdapter:
    name: str
    command: list[str]
    cwd: Path | None = None
    uses_timeout_as_success: bool = True


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "sim", "on"}


def _load_baseline_state() -> str | None:
    if EXPECTED_STATE:
        return EXPECTED_STATE

    if not BASELINE_FILE.exists():
        return None

    with BASELINE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    state = data.get("state")
    return None if state is None else str(state)


def _default_adapter(tool: str) -> FuzzerAdapter:
    """Mapeia cada ferramenta para um comando padrão, sobrescrevível por env."""
    custom_cmd = os.environ.get("FUZZER_CMD")
    custom_cwd = os.environ.get("FUZZER_CWD")
    if custom_cmd:
        return FuzzerAdapter(
            name=os.environ.get("FUZZER_NAME", tool),
            command=shlex.split(custom_cmd),
            cwd=Path(custom_cwd).resolve() if custom_cwd else None,
        )

    adapters: dict[str, FuzzerAdapter] = {
        "boofuzz": FuzzerAdapter(
            name="boofuzz",
            command=[str(PROJECT_ROOT / "venv_boofuzz" / "bin" / "python"), str(ROOT_DIR / "fuzzers" / "boofuzz_mqtt.py")],
            cwd=PROJECT_ROOT,
        ),
        "fume": FuzzerAdapter(
            name="fume",
            command=[str(PROJECT_ROOT / "FUME-Fuzzing-MQTT-Brokers" / "venv_fume" / "bin" / "python"), "fuzz.py"],
            cwd=PROJECT_ROOT / "FUME-Fuzzing-MQTT-Brokers",
        ),
        "mqttgram": FuzzerAdapter(
            name="mqttgram",
            command=[str(PROJECT_ROOT / "MQTTGRAM" / "venv_mqttgram" / "bin" / "python"), "fuzz.py"],
            cwd=PROJECT_ROOT / "MQTTGRAM",
        ),
        "scapy": FuzzerAdapter(
            name="scapy",
            command=[sys.executable, str(ROOT_DIR / "fuzzers" / "scapy_mqtt.py")],
            cwd=PROJECT_ROOT,
        ),
        "mitm": FuzzerAdapter(
            name="mitm",
            command=shlex.split(os.environ.get("MITM_CMD", "python3 mitm_wrapper.py")),
            cwd=PROJECT_ROOT,
        ),
        "polymorph": FuzzerAdapter(
            name="polymorph",
            command=shlex.split(os.environ.get("POLYMORPH_CMD", "python3 mitm_wrapper.py")),
            cwd=PROJECT_ROOT,
        ),
    }

    if tool not in adapters:
        raise ValueError(
            f"FUZZER_TOOL={tool!r} desconhecido. Use um destes: "
            f"{', '.join(sorted(adapters))}; ou informe FUZZER_CMD."
        )
    return adapters[tool]


def run_cmd(
    cmd: list[str],
    *,
    timeout: int | None = None,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=check,
    )


def docker_status() -> str:
    proc = run_cmd(
        ["docker", "inspect", "-f", "{{.State.Status}}", HA_CONTAINER],
        timeout=10,
    )
    return proc.stdout.strip()


def wait_for_container_running(timeout: int = 60) -> str:
    start = time.time()
    last_status = "unknown"
    while time.time() - start < timeout:
        last_status = docker_status()
        if last_status == "running":
            return last_status
        time.sleep(1)
    return last_status


def normalize_state(state: Any) -> str | None:
    if state in (None, "", "None"):
        return None
    return str(state)


def get_ha_state() -> tuple[str | None, dict[str, Any] | None, str | None]:
    if not HA_TOKEN:
        return None, None, "HA_TOKEN_AUSENTE"

    try:
        response = requests.get(HA_STATE_URL, headers=HEADERS, timeout=5)
    except requests.RequestException as exc:
        return None, None, f"EXCECAO_HTTP: {exc}"

    if response.status_code == 401:
        return None, None, "HTTP_401_TOKEN_INVALIDO"
    if response.status_code != 200:
        return None, None, f"HTTP_{response.status_code}"

    try:
        payload = response.json()
    except ValueError:
        return None, None, "RESPOSTA_NAO_JSON"

    return normalize_state(payload.get("state")), payload, None


def wait_for_state(timeout: int = CANARY_WAIT) -> tuple[str | None, dict[str, Any] | None, str | None]:
    start = time.time()
    last: tuple[str | None, dict[str, Any] | None, str | None] = (None, None, None)
    while time.time() - start < timeout:
        last = get_ha_state()
        state, _payload, err = last
        if err:
            return last
        if state not in (None, "unknown", "unavailable"):
            return last
        time.sleep(0.5)
    return last


def publish_canary(self):
    subprocess.run(
        [
            "mosquitto_pub",
            "-h", MQTT_HOST,
            "-p", str(MQTT_PORT),
            "-t", MQTT_TOPIC,
            "-m", MQTT_PAYLOAD,
        ],
        check=True,
    )


def collect_logs_since(since_epoch: str) -> str:
    proc = run_cmd(
        ["docker", "logs", "--since", since_epoch, HA_CONTAINER],
        timeout=20,
    )
    return proc.stdout + proc.stderr


def find_log_evidence(logs: str) -> dict[str, bool]:
    evidence: dict[str, bool] = {}
    for pattern in LOG_PATTERNS:
        try:
            evidence[pattern] = re.search(pattern, logs) is not None
        except re.error:
            evidence[pattern] = pattern in logs
    return evidence


class TestMQTTFuzzHarness(unittest.TestCase):
    """Teste único e parametrizável: muda-se só FUZZER_TOOL/FUZZER_CMD."""

    def setUp(self) -> None:
        self.adapter = _default_adapter(FUZZER_TOOL)
        self.expected_state = _load_baseline_state()
        self.setup_started_epoch = str(int(time.time()))
        self.campaign_id = f"{self.adapter.name}_{self.setup_started_epoch}_{FUZZ_SEED}"

        self.restart_ha()

        if _as_bool(os.environ.get("PUBLISH_INITIAL_CANARY"), default=True):
            publish_canary()
            time.sleep(1)

        # O baseline precisa estar estável antes do fuzzer começar. Isso evita falso
        # positivo no controle negativo e evita contaminar time_to_kill com inicialização.
        self.wait_for_baseline_state()

        # A partir daqui começa a janela do oráculo da campanha/fuzzer.
        # Isso evita que erros antigos ou de boot contaminem o controle negativo NOOP.
        self.start_time = str(int(time.time()))

    # ------------------------------------------------------------------
    # Compatibilidade com a versão anterior sugerida no chat
    # ------------------------------------------------------------------
    def restart_ha(self) -> None:
        subprocess.run(
            ["docker", "restart", HA_CONTAINER],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        status = wait_for_container_running(timeout=60)
        if status != "running":
            self.fail(f"Home Assistant não ficou running após restart: status={status}")
        time.sleep(STARTUP_SLEEP)

    def publish_canary(self) -> subprocess.CompletedProcess[str]:
        return publish_canary()

    def wait_for_baseline_state(self, timeout: int = CANARY_WAIT) -> None:
        if not self.expected_state:
            # Mantém a possibilidade de rodar só com oráculo de processo/log.
            return

        start = time.time()
        last_state: str | None = None
        last_err: str | None = None

        while time.time() - start < timeout:
            state, _payload, err = get_ha_state()
            last_state, last_err = state, err
            if err:
                self.fail(f"Erro consultando estado do HA antes do fuzzing: {err}")
            if normalize_state(state) == normalize_state(self.expected_state):
                return
            time.sleep(0.5)

        self.fail(
            "Baseline não estabilizou antes do fuzzing: "
            f"esperado={self.expected_state!r}, atual={last_state!r}, erro={last_err!r}"
        )

    def check_nivel1(self) -> tuple[bool, str]:
        status = docker_status()
        return status != "running", status

    def check_nivel2(self) -> tuple[bool, str]:
        logs = collect_logs_since(self.start_time)
        evidence = find_log_evidence(logs)
        return any(evidence.values()), logs

    def check_nivel3_4(self) -> tuple[bool, dict[str, Any]]:
        detail: dict[str, Any] = {
            "enabled": bool(self.expected_state),
            "expected": self.expected_state,
            "actual": None,
            "error": None,
            "raw": None,
        }

        if not self.expected_state:
            detail["error"] = f"baseline ausente ({BASELINE_FILE}) e EXPECTED_STATE não definido"
            return False, detail

        state, payload, err = get_ha_state()
        detail.update({"actual": state, "error": err, "raw": payload})

        if err:
            return True, detail

        return normalize_state(state) != normalize_state(self.expected_state), detail

    def _fuzzer_env(self) -> dict[str, str]:
        env = os.environ.copy()
        env.update(
            {
                "MQTT_HOST": MQTT_HOST,
                "MQTT_PORT": str(MQTT_PORT),
                "MQTT_TOPIC": MQTT_TOPIC,
                "MQTT_PAYLOAD": MQTT_PAYLOAD,
                "FUZZ_DURATION": str(FUZZ_DURATION),
                "FUZZ_SEED": str(FUZZ_SEED),
                "CAMPAIGN_ID": self.campaign_id,
                "BOOFUZZ_DB_PATH": str(RESULTS_DIR / f"boofuzz_{self.campaign_id}.db"),
            }
        )
        return env

    def run_fuzzer(self) -> dict[str, Any]:
        """Execução simples, mantida para compatibilidade; o teste usa monitoring."""
        started = time.time()
        try:
            proc = run_cmd(
                self.adapter.command,
                cwd=self.adapter.cwd,
                env=self._fuzzer_env(),
                timeout=FUZZ_TIMEOUT,
                check=False,
            )
            return {
                "command": self.adapter.command,
                "cwd": str(self.adapter.cwd) if self.adapter.cwd else None,
                "returncode": proc.returncode,
                "timeout": False,
                "duration_sec": round(time.time() - started, 3),
                "stdout_tail": proc.stdout[-4000:],
                "stderr_tail": proc.stderr[-4000:],
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "command": self.adapter.command,
                "cwd": str(self.adapter.cwd) if self.adapter.cwd else None,
                "returncode": None,
                "timeout": True,
                "duration_sec": round(time.time() - started, 3),
                "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                "stderr_tail": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
            }

    def evaluate_oracle(self) -> dict[str, Any]:
        """
        Avalia o oráculo no estado atual, sem publicar canário final.
        Publicar canário aqui apagaria divergências de estado causadas pelo fuzzer.
        """
        crashed, status = self.check_nivel1()
        log_divergence, logs = self.check_nivel2()
        log_evidence = find_log_evidence(logs)

        if crashed:
            state_divergence = False
            state_detail = {
                "enabled": False,
                "expected": self.expected_state,
                "actual": None,
                "error": "skip_l3_4_container_down",
                "raw": None,
            }
        else:
            state_divergence, state_detail = self.check_nivel3_4()

        return {
            "level1_process": {"divergence": crashed, "status": status},
            "level2_logs": {
                "divergence": log_divergence,
                "patterns": log_evidence,
                "log_tail": logs[-4000:],
            },
            "level3_4_state": {"divergence": state_divergence, **state_detail},
            "divergence": crashed or log_divergence or state_divergence,
        }

    def write_result(self, fuzzer_result: dict[str, Any], oracle: dict[str, Any]) -> Path:
        result = {
            "campaign_id": self.campaign_id,
            "fuzzer_tool": self.adapter.name,
            "fuzz_seed": FUZZ_SEED,
            "fuzz_duration": FUZZ_DURATION,
            "ha_container": HA_CONTAINER,
            "ha_entity_id": HA_ENTITY_ID,
            "mqtt_host": MQTT_HOST,
            "mqtt_port": MQTT_PORT,
            "mqtt_topic": MQTT_TOPIC,
            "mqtt_payload": MQTT_PAYLOAD,
            "baseline_file": str(BASELINE_FILE),
            "expected_state": self.expected_state,
            "oracle": oracle,
            "fuzzer_result": fuzzer_result,
        }
        out = RESULTS_DIR / f"result_{self.campaign_id}.json"
        with out.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return out

    def run_fuzzer_with_monitoring(self) -> tuple[bool, str, Any, float, dict[str, Any]]:
        """Executa o adaptador e monitora os níveis do oráculo durante a execução."""
        started = time.monotonic()
        stdout_chunks: list[str] = []
        stderr_chunks: list[str] = []

        proc = subprocess.Popen(
            self.adapter.command,
            cwd=str(self.adapter.cwd) if self.adapter.cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self._fuzzer_env(),
        )

        killed = False
        oracle_level = "none"
        detail: Any = "no_divergence"

        try:
            while time.monotonic() - started < FUZZ_DURATION:
                crashed, status = self.check_nivel1()
                if crashed:
                    killed = True
                    oracle_level = "level_1_process"
                    detail = status
                    break

                log_div, logs = self.check_nivel2()
                if log_div:
                    killed = True
                    oracle_level = "level_2_logs"
                    detail = find_log_evidence(logs)
                    break

                estado_anomalo, estado_detail = self.check_nivel3_4()
                if estado_anomalo:
                    killed = True
                    oracle_level = "level_3_4_state"
                    detail = estado_detail
                    break

                if proc.poll() is not None:
                    break

                time.sleep(MONITOR_INTERVAL)

            elapsed = time.monotonic() - started

        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=TERMINATE_GRACE)
                except subprocess.TimeoutExpired:
                    proc.kill()

            try:
                out, err = proc.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
                out, err = proc.communicate()

            stdout_chunks.append(out or "")
            stderr_chunks.append(err or "")

        fuzzer_result = {
            "command": self.adapter.command,
            "cwd": str(self.adapter.cwd) if self.adapter.cwd else None,
            "returncode": proc.returncode,
            "timeout": proc.returncode is None,
            "duration_sec": round(time.monotonic() - started, 3),
            "time_to_kill_sec": round(elapsed, 3) if killed else None,
            "stdout_tail": "".join(stdout_chunks)[-4000:],
            "stderr_tail": "".join(stderr_chunks)[-4000:],
        }

        return killed, oracle_level, detail, elapsed, fuzzer_result

    def test_fuzzer_detecta_mutante(self) -> None:
        killed, oracle_level, detail, elapsed, fuzzer_result = self.run_fuzzer_with_monitoring()

        # Avaliação final, sem publicar canário, para registrar o estado/log final.
        oracle = self.evaluate_oracle()
        oracle["first_detection"] = {
            "killed": killed,
            "oracle_level": oracle_level,
            "detail": detail,
            "time_to_kill_sec": round(elapsed, 3) if killed else None,
        }
        result_path = self.write_result(fuzzer_result, oracle)

        self.assertFalse(
            killed,
            (
                f"Mutante morto: oracle={oracle_level}, "
                f"detail={detail}, time_to_kill={elapsed:.2f}s, "
                f"result={result_path}"
            ),
        )


if __name__ == "__main__":
    unittest.main()
