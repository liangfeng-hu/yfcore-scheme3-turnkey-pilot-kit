#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheme-3 Turnkey Pilot Kit — Enhanced Self-Check (Cross-platform)

What it does:
1) Checks required files exist
2) Starts docker compose stack (root docker-compose.yml)
3) Runs 3 blackbox cases via HTTP (no bash/curl dependency)
4) Runs audit replay check
5) Tears down stack

Usage:
  python check_pilot_kit_enhanced.py
"""

import json
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def cprint(text: str, color: str | None = None, bold: bool = False) -> None:
    prefix = Color.BOLD if bold else ""
    if color == "green":
        prefix += Color.GREEN
    elif color == "red":
        prefix += Color.RED
    elif color == "yellow":
        prefix += Color.YELLOW
    elif color == "cyan":
        prefix += Color.CYAN
    print(f"{prefix}{text}{Color.RESET}")


EXPECTED_FILES = [
    "README.md",
    "docker-compose.yml",
    "reference-impl/python/sidecar_service.py",
    "runtime/Dockerfile",
    "runtime/gateway_proxy.py",
    "runtime/upstream_stub.py",
    "examples/curl_test.sh",
    "audit/replay.py",
    "audit/schema_v1.json",
    "adapters/envoy-ext-authz.md",
    "adapters/nginx.md",
]


def run_cmd(cmd: str, cwd: Path, timeout: int = 300) -> bool:
    try:
        r = subprocess.run(
            cmd,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if r.returncode == 0:
            cprint(f"✅ {cmd}", "green")
            return True
        cprint(f"❌ {cmd}", "red", bold=True)
        if r.stderr.strip():
            print("   " + r.stderr.strip())
        if r.stdout.strip():
            print("   " + r.stdout.strip())
        return False
    except Exception as e:
        cprint(f"❌ {cmd} failed: {e}", "red", bold=True)
        return False


def http_post(url: str, body: dict, headers: dict | None = None) -> int:
    data = (json.dumps(body) + "\n").encode("utf-8")
    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urlopen(req, timeout=10) as resp:
            return int(resp.status)
    except HTTPError as e:
        return int(e.code)
    except URLError:
        return 0


def main() -> int:
    root = Path(__file__).resolve().parent
    cprint("🚀 Scheme-3 Enhanced Self-Check starting...\n", "cyan", bold=True)

    missing = [f for f in EXPECTED_FILES if not (root / f).exists()]
    if missing:
        cprint("❌ Missing required files:", "red", bold=True)
        for m in missing:
            print("   - " + m)
        return 1
    cprint("✅ Required files present", "green")

    # Clear data/
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    for p in data_dir.glob("*.jsonl"):
        try:
            p.unlink()
        except Exception:
            pass
    cprint("✅ data/ cleared", "green")

    # Compose up
    cprint("\nStarting docker compose stack...", "cyan", bold=True)
    if not run_cmd("docker compose up -d --build", root, timeout=900):
        cprint("Docker compose failed. Ensure Docker Desktop is running.", "red", bold=True)
        return 1
    time.sleep(6)

    # Blackbox cases (HTTP)
    base = "http://127.0.0.1:8080/v1/chat/completions"
    cprint("\nRunning blackbox cases...", "cyan", bold=True)

    s1 = http_post(base, {"hint": "hello"})
    if s1 != 200:
        cprint(f"❌ Case 1 expected 200, got {s1}", "red", bold=True)
        run_cmd("docker compose logs --tail=200", root, timeout=60)
        run_cmd("docker compose down -v", root, timeout=120)
        return 1
    cprint("✅ Case 1 PASS (ALLOW 200)", "green")

    s2 = http_post(base, {"hint": "try extract"}, headers={"X-Distill-Risk": "0.92"})
    if s2 != 403:
        cprint(f"❌ Case 2 expected 403, got {s2}", "red", bold=True)
        run_cmd("docker compose logs --tail=200", root, timeout=60)
        run_cmd("docker compose down -v", root, timeout=120)
        return 1
    cprint("✅ Case 2 PASS (FAIL-CLOSED 403)", "green")

    s3 = http_post(base, {"hint": "force physical fail"}, headers={"X-Thermo-OK": "false"})
    if s3 != 403:
        cprint(f"❌ Case 3 expected 403, got {s3}", "red", bold=True)
        run_cmd("docker compose logs --tail=200", root, timeout=60)
        run_cmd("docker compose down -v", root, timeout=120)
        return 1
    cprint("✅ Case 3 PASS (FAIL-CLOSED 403)", "green")

    # Replay
    cprint("\nRunning audit replay...", "cyan", bold=True)
    if not run_cmd("python audit/replay.py data/audit.jsonl", root, timeout=120):
        run_cmd("docker compose down -v", root, timeout=120)
        return 1

    # Tear down
    run_cmd("docker compose down -v", root, timeout=120)

    cprint("\n🎉 ALL PASS — Scheme-3 is ready to ship.", "green", bold=True)
    cprint("Production requires vendor SEALED GateKernel + trusted evidence injection + SLA.", "cyan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
