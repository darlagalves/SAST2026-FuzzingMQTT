"""
Harness unificado para comparar fuzzers MQTT contra o Home Assistant.

Versão corrigida para evitar que o controle NOOP mate mutantes.

Princípio desta versão:
    - O setUp apenas reinicia o Home Assistant e abre a janela de observação.
    - O setUp NÃO publica payload canário.
    - O setUp NÃO compara estado com baseline.
    - Por padrão, só contam divergências observadas DEPOIS do início do FUZZER_CMD.
    - Assim, se FUZZER_CMD=NOOP, o esperado é 0 mutantes mortos.

Uso:
    source harness/config/experimento.env
    FUZZER_CMD=/home/darla/experimento/harness/adapters/run_boofuzz.sh \
        python -m unittest harness/test_harness_unificado.py
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


def env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "sim", "on"}


# ---------------------------------------------------------------------------
# Configuração geral
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.environ.get("EXP_ROOT", ROOT_DIR.parent)).resolve()

RESULTS_DIR = Path(os.environ.get("RESULTS_DIR", PROJECT_ROOT / "resultados_mutmut" / "harness_runs")).resolve()
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
FUZZ_SEED = os.environ.get("FUZZER_SEED", os.environ.get("FUZZ_SEED", "1"))

STARTUP_SLEEP = int(os.environ.get("STARTUP_SLEEP", "12"))
MONITOR_INTERVAL = float(os.environ.get("MONITOR_INTERVAL", "0.5"))
TERMINATE_GRACE = int(os.environ.get("TERMINATE_GRACE", "5"))

# IMPORTANTÍSSIMO:
# Os oráculos de estado ficam desligados por padrão, porque payload canário
# ou comparação fixa de baseline pode matar mutantes mesmo com FUZZER_CMD=NOOP.
CHECK_STATE_DURING_FUZZ = env_bool("CHECK_STATE_DURING_FUZZ", default=False)
CHECK_STATE_AFTER_FUZZ = env_bool("CHECK_STATE_AFTER_FUZZ", default=False)

# Oráculo por trace: compara a sequência de estados gerada pelo corpus no HA original
# contra a sequência de estados gerada pelo mesmo corpus no mutante.
CHECK_CORPUS_TRACE = env_bool("CHECK_CORPUS_TRACE", default=False)
TRACE_BASELINE_FILE = Path(os.environ.get("TRACE_BASELINE_FILE", "")).resolve() if os.environ.get("TRACE_BASELINE_FILE") else None
TRACE_OUT_FILE = Path(os.environ.get("TRACE_OUT_FILE", PROJECT_ROOT / "resultados_mutmut" / "tmp" / "actual_trace.jsonl")).resolve()

BASELINE_FILE = Path(os.environ.get("BASELINE_FILE", PROJECT_ROOT / "baseline.json")).resolve()
EXPECTED_STATE = os.environ.get("EXPECTED_STATE", "")

# Não use "ERROR" genérico por padrão. Isso pode capturar ruído do HA.
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


def load_baseline_state() -> str | None:
    if EXPECTED_STATE:
        return str(EXPECTED_STATE)

    if not BASELINE_FILE.exists():
        return None

    try:
        with BASELINE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None

    state = data.get("state")
    return None if state is None else str(state)


def default_adapter(tool: str) -> FuzzerAdapter:
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
            command=[
                str(PROJECT_ROOT / "venv_boofuzz" / "bin" / "python"),
                str(ROOT_DIR / "fuzzers" / "boofuzz_mqtt.py"),
            ],
            cwd=PROJECT_ROOT,
        ),
        "fume": FuzzerAdapter(
            name="fume",
            command=[
                str(PROJECT_ROOT / "FUME-Fuzzing-MQTT-Brokers" / "venv_fume" / "bin" / "python"),
                "fuzz.py",
            ],
            cwd=PROJECT_ROOT / "FUME-Fuzzing-MQTT-Brokers",
        ),
        "mqttgram": FuzzerAdapter(
            name="mqttgram",
            command=[
                str(PROJECT_ROOT / "MQTTGRAM" / "venv_mqttgram" / "bin" / "python"),
                "fuzz.py",
            ],
            cwd=PROJECT_ROOT / "MQTTGRAM",
        ),
        "scapy": FuzzerAdapter(
            name="scapy",
            command=[sys.executable, str(ROOT_DIR / "fuzzers" / "scapy_mqtt.py")],
            cwd=PROJECT_ROOT,
        ),
        "mitm": FuzzerAdapter(
            name="mitm",
            command=shlex.split(os.environ.get("MITM_CMD", "python3 mitm_fuzzer.py")),
            cwd=PROJECT_ROOT,
        ),
        "polymorph": FuzzerAdapter(
            name="polymorph",
            command=shlex.split(os.environ.get("POLYMORPH_CMD", "python3 mitm_fuzzer.py")),
            cwd=PROJECT_ROOT,
        ),
    }

    if tool not in adapters:
        raise ValueError(
            f"FUZZER_TOOL={tool!r} desconhecido. Use FUZZER_CMD ou um destes: "
            f"{', '.join(sorted(adapters))}"
        )

    return adapters[tool]


def run_cmd(cmd: list[str], *, timeout: int | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def docker_status() -> str:
    proc = run_cmd(["docker", "inspect", "-f", "{{.State.Status}}", HA_CONTAINER], timeout=10)
    return proc.stdout.strip()


def wait_for_container_running(timeout: int = 60) -> str:
    start = time.time()
    status = "unknown"

    while time.time() - start < timeout:
        status = docker_status()
        if status == "running":
            return status
        time.sleep(1)

    return status


def collect_logs_since(since_epoch: str) -> str:
    proc = run_cmd(["docker", "logs", "--since", since_epoch, HA_CONTAINER], timeout=20)
    return proc.stdout + proc.stderr


def find_log_evidence(logs: str) -> dict[str, bool]:
    evidence: dict[str, bool] = {}

    for pattern in LOG_PATTERNS:
        try:
            evidence[pattern] = re.search(pattern, logs) is not None
        except re.error:
            evidence[pattern] = pattern in logs

    return evidence


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


def load_trace_states(path: Path | str | None) -> list[str]:
    """Lê um trace jsonl e retorna apenas a sequência de estados."""
    if path is None:
        return []

    path = Path(path)

    if not path.exists():
        return []

    states: list[str] = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            states.append(str(item.get("state", "")))

    return states


def compare_corpus_trace(expected_path: Path | str | None, actual_path: Path | str | None) -> tuple[bool, dict[str, Any]]:
    """Compara baseline semântica do corpus contra trace observado no mutante.

    Retorna (divergiu, detalhes). Divergência funcional mata o mutante.
    Falta de baseline/trace é tratada como erro de infraestrutura e não deve matar
    mutantes automaticamente.
    """
    expected = load_trace_states(expected_path)
    actual = load_trace_states(actual_path)

    detail: dict[str, Any] = {
        "expected_path": str(expected_path) if expected_path else None,
        "actual_path": str(actual_path) if actual_path else None,
        "expected_len": len(expected),
        "actual_len": len(actual),
        "first_difference": None,
    }

    if not expected:
        detail["error"] = "baseline_trace_empty_or_missing"
        return False, detail

    if not actual:
        detail["error"] = "actual_trace_empty_or_missing"
        return False, detail

    min_len = min(len(expected), len(actual))

    for i in range(min_len):
        if expected[i] != actual[i]:
            detail["first_difference"] = {
                "index": i + 1,
                "expected": expected[i],
                "actual": actual[i],
            }
            return True, detail

    if len(expected) != len(actual):
        detail["first_difference"] = {
            "index": min_len + 1,
            "expected": expected[min_len] if min_len < len(expected) else "<missing>",
            "actual": actual[min_len] if min_len < len(actual) else "<missing>",
        }
        return True, detail

    return False, detail


class TestMQTTFuzzHarness(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = default_adapter(FUZZER_TOOL)
        self.expected_state = load_baseline_state()
        self.campaign_id = f"{self.adapter.name}_{int(time.time())}_{FUZZ_SEED}"

        self.precondition_error: str | None = None

        # Fase de preparo: NÃO conta como morte do mutante.
        try:
            subprocess.run(
                ["docker", "restart", HA_CONTAINER],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60,
            )

            status = wait_for_container_running(timeout=60)
            if status != "running":
                self.precondition_error = f"container_not_running_after_restart:{status}"

            time.sleep(STARTUP_SLEEP)

        except Exception as exc:
            self.precondition_error = f"restart_failed:{exc!r}"

        # Abre a janela de observação depois do boot.
        # Assim, logs de inicialização e efeitos de setup não entram no oráculo.
        time.sleep(1)
        self.fuzzer_start_epoch = str(int(time.time()))

    def fuzzer_env(self) -> dict[str, str]:
        env = os.environ.copy()
        env.update(
            {
                "MQTT_HOST": MQTT_HOST,
                "MQTT_PORT": str(MQTT_PORT),
                "MQTT_TOPIC": MQTT_TOPIC,
                "MQTT_PAYLOAD": MQTT_PAYLOAD,
                "FUZZ_DURATION": str(FUZZ_DURATION),
                "FUZZ_SEED": str(FUZZ_SEED),
                "FUZZER_SEED": str(FUZZ_SEED),
                "CAMPAIGN_ID": self.campaign_id,
                "BOOFUZZ_DB_PATH": str(RESULTS_DIR / f"boofuzz_{self.campaign_id}.db"),
            }
        )

        if CHECK_CORPUS_TRACE:
            env["TRACE_OUT"] = str(TRACE_OUT_FILE)

        return env

    def check_process(self) -> tuple[bool, str]:
        status = docker_status()
        return status != "running", status

    def check_logs(self) -> tuple[bool, dict[str, bool], str]:
        logs = collect_logs_since(self.fuzzer_start_epoch)
        evidence = find_log_evidence(logs)
        return any(evidence.values()), evidence, logs

    def check_state(self) -> tuple[bool, dict[str, Any]]:
        detail: dict[str, Any] = {
            "enabled": bool(self.expected_state),
            "expected": self.expected_state,
            "actual": None,
            "error": None,
            "raw": None,
        }

        if not self.expected_state:
            detail["error"] = "baseline_ausente"
            return False, detail

        state, payload, err = get_ha_state()
        detail.update({"actual": state, "error": err, "raw": payload})

        if err:
            return True, detail

        return normalize_state(state) != normalize_state(self.expected_state), detail

    def terminate_process(self, proc: subprocess.Popen[str]) -> tuple[str, str]:
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

        return out or "", err or ""

    def run_fuzzer_with_monitoring(self) -> dict[str, Any]:
        if self.precondition_error:
            # Não mate mutantes por problema de preparação/boot.
            return {
                "killed": False,
                "oracle_level": "precondition",
                "detail": self.precondition_error,
                "time_to_kill_sec": None,
                "fuzzer_result": {
                    "command": self.adapter.command,
                    "cwd": str(self.adapter.cwd) if self.adapter.cwd else None,
                    "returncode": None,
                    "duration_sec": 0,
                    "stdout_tail": "",
                    "stderr_tail": "",
                },
            }

        started = time.monotonic()

        if CHECK_CORPUS_TRACE:
            TRACE_OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            TRACE_OUT_FILE.unlink(missing_ok=True)

        proc = subprocess.Popen(
            self.adapter.command,
            cwd=str(self.adapter.cwd) if self.adapter.cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self.fuzzer_env(),
        )

        killed = False
        oracle_level = "none"
        detail: Any = "no_divergence"
        time_to_kill: float | None = None

        while time.monotonic() - started < FUZZ_DURATION:
            crashed, status = self.check_process()
            if crashed:
                killed = True
                oracle_level = "level_1_process"
                detail = status
                time_to_kill = time.monotonic() - started
                break

            log_div, evidence, _logs = self.check_logs()
            if log_div:
                killed = True
                oracle_level = "level_2_logs"
                detail = evidence
                time_to_kill = time.monotonic() - started
                break

            if CHECK_STATE_DURING_FUZZ:
                state_div, state_detail = self.check_state()
                if state_div:
                    killed = True
                    oracle_level = "level_3_4_state_during_fuzz"
                    detail = state_detail
                    time_to_kill = time.monotonic() - started
                    break

            if proc.poll() is not None:
                break

            time.sleep(MONITOR_INTERVAL)

        out, err = self.terminate_process(proc)

        duration = time.monotonic() - started

        # Avaliação final: só processo/log por padrão.
        # Não publica canário e não compara baseline, para evitar NOOP matando mutantes.
        if not killed:
            crashed, status = self.check_process()
            if crashed:
                killed = True
                oracle_level = "level_1_process"
                detail = status
                time_to_kill = duration

        if not killed:
            log_div, evidence, _logs = self.check_logs()
            if log_div:
                killed = True
                oracle_level = "level_2_logs"
                detail = evidence
                time_to_kill = duration

        if not killed and CHECK_STATE_AFTER_FUZZ:
            state_div, state_detail = self.check_state()
            if state_div:
                killed = True
                oracle_level = "level_3_4_state_after_fuzz"
                detail = state_detail
                time_to_kill = duration

        if not killed and CHECK_CORPUS_TRACE:
            trace_div, trace_detail = compare_corpus_trace(
                TRACE_BASELINE_FILE,
                TRACE_OUT_FILE,
            )

            if trace_div:
                killed = True
                oracle_level = "level_3_4_corpus_trace"
                detail = trace_detail
                time_to_kill = duration
            elif trace_detail.get("error"):
                # Erro de infraestrutura: registra, mas não mata o mutante.
                oracle_level = "trace_precondition"
                detail = trace_detail

        return {
            "killed": killed,
            "oracle_level": oracle_level,
            "detail": detail,
            "time_to_kill_sec": round(time_to_kill, 3) if time_to_kill is not None else None,
            "fuzzer_result": {
                "command": self.adapter.command,
                "cwd": str(self.adapter.cwd) if self.adapter.cwd else None,
                "returncode": proc.returncode,
                "duration_sec": round(duration, 3),
                "stdout_tail": out[-4000:],
                "stderr_tail": err[-4000:],
            },
        }

    def write_result(self, result: dict[str, Any]) -> Path:
        out = RESULTS_DIR / f"result_{self.campaign_id}.json"

        payload = {
            "campaign_id": self.campaign_id,
            "fuzzer_tool": self.adapter.name,
            "fuzz_seed": FUZZ_SEED,
            "fuzz_duration": FUZZ_DURATION,
            "ha_container": HA_CONTAINER,
            "ha_entity_id": HA_ENTITY_ID,
            "mqtt_host": MQTT_HOST,
            "mqtt_port": MQTT_PORT,
            "mqtt_topic": MQTT_TOPIC,
            "baseline_file": str(BASELINE_FILE),
            "expected_state": self.expected_state,
            "check_state_during_fuzz": CHECK_STATE_DURING_FUZZ,
            "check_state_after_fuzz": CHECK_STATE_AFTER_FUZZ,
            "check_corpus_trace": CHECK_CORPUS_TRACE,
            "trace_baseline_file": str(TRACE_BASELINE_FILE) if TRACE_BASELINE_FILE else None,
            "trace_out_file": str(TRACE_OUT_FILE),
            "log_patterns": LOG_PATTERNS,
            "result": result,
        }

        with out.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return out

    def test_fuzzer_detecta_mutante(self) -> None:
        result = self.run_fuzzer_with_monitoring()
        result_path = self.write_result(result)

        self.assertFalse(
            result["killed"],
            (
                f"Mutante morto: oracle={result['oracle_level']}, "
                f"detail={result['detail']}, "
                f"time_to_kill={result['time_to_kill_sec']}, "
                f"result={result_path}"
            ),
        )


if __name__ == "__main__":
    unittest.main()
