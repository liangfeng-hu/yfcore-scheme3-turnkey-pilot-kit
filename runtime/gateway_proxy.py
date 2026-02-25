import json
import os
import time
import hashlib
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

VBUS_URL = os.environ.get("VBUS_URL", "http://127.0.0.1:8787/v1/adjudicate")
UPSTREAM_URL = os.environ.get("UPSTREAM_URL", "http://127.0.0.1:9001/v1/chat/completions")


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _bool(v: str, default: bool) -> bool:
    if v is None:
        return default
    x = v.strip().lower()
    if x in ("1", "true", "yes", "y", "ok"):
        return True
    if x in ("0", "false", "no", "n"):
        return False
    return default


def _float(v: str, default: float) -> float:
    try:
        return float(v)
    except Exception:
        return default


def _post_json(url: str, obj: dict, timeout_s: int = 5):
    data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return e.code, body
    except Exception as e:
        return 502, json.dumps({"error": "sidecar_unreachable", "detail": str(e)}, ensure_ascii=False)


def _proxy_to_upstream(raw_body: bytes, content_type: str):
    req = urllib.request.Request(
        UPSTREAM_URL,
        data=raw_body,
        headers={"Content-Type": content_type or "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        out_body = resp.read()
        out_type = resp.headers.get("Content-Type", "application/json")
        return resp.status, out_type, out_body


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "VInfinityGatewayProxy/1.0"

    def _send(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path == "/health":
            body = (json.dumps({"ok": True, "service": "gateway_proxy", "vbus": VBUS_URL, "upstream": UPSTREAM_URL},
                               ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            return self._send(200, body)
        return self._send(404, b'{"error":"not found"}\n')

    def do_POST(self):
        path = urlparse(self.path).path
        if path not in ("/v1/chat/completions", "/completion", "/"):
            return self._send(404, b'{"error":"not found"}\n')

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length) if length > 0 else b"{}"
        content_type = self.headers.get("Content-Type", "application/json")

        risk_class = (self.headers.get("X-Risk-Class") or "Normal").strip()
        s_ex = _float(self.headers.get("X-Distill-Risk"), 0.10)
        iia_ok = _bool(self.headers.get("X-IIA-OK"), True)
        seed_ok = _bool(self.headers.get("X-Seed-OK"), True)
        thermo_ok = _bool(self.headers.get("X-Thermo-OK"), True)
        attest_ok = _bool(self.headers.get("X-Attest-OK"), True)
        zk_ok = _bool(self.headers.get("X-ZK-OK"), True)
        energy_ok = _bool(self.headers.get("X-Energy-OK"), True)
        trust_ok = _bool(self.headers.get("X-Trust-OK"), True)
        budget_ok = _bool(self.headers.get("X-Budget-OK"), True)
        out_level = (self.headers.get("X-OutLevel") or "FOES").strip()

        canon_header = "CANONHEADER_POC"
        ssot_hash = _sha256("SSOT_POC")
        req_fingerprint = _sha256(raw_body.decode("utf-8", errors="ignore") + "|" + path + "|" + str(int(time.time())))

        receipt_roots = {
            "canon_header": canon_header,
            "ssot_hash": ssot_hash,
            "pending_ledger_root": _sha256("PEND|" + req_fingerprint),
            "audit_rec_root": _sha256("AUDITREC|" + req_fingerprint),
            "delta_s_log_root": _sha256("DELTAS|" + req_fingerprint),
            "energy_trace_root": _sha256("ENERGY|" + req_fingerprint),
            "zk_proof_root": _sha256("ZKPROOF|" + req_fingerprint),
            "attestation_root": _sha256("ATTEST|" + req_fingerprint),
            "verifier_refs": "VERIFIERS_POC",
        }

        evidence = {
            "out_level": out_level,
            "intent_audit_group": {"risk_class": risk_class, "iia_ok": iia_ok, "s_ex": s_ex},
            "seed_continuity": {"seed_continuity_ok": seed_ok},
            "physical_proof": {"zk_ok": zk_ok, "attestation_ok": attest_ok, "thermo_ok": thermo_ok, "energy_ok": energy_ok},
            "lse_support": {"trust_ok": trust_ok, "budget_ok": budget_ok},
            "receipt_roots": receipt_roots,
        }

        vbus_status, vbus_body = _post_json(VBUS_URL, evidence, timeout_s=5)
        if vbus_status != 200:
            return self._send(403, (vbus_body + "\n").encode("utf-8", errors="ignore"))

        try:
            up_status, up_type, up_body = _proxy_to_upstream(raw_body, content_type)
            return self._send(up_status, up_body, content_type=up_type)
        except Exception as e:
            body = (json.dumps({"error": "upstream_failed", "detail": str(e)}, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            return self._send(502, body)


def main():
    httpd = ThreadingHTTPServer(("0.0.0.0", 8080), GatewayHandler)
    print("Gateway Proxy listening on http://127.0.0.1:8080")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
