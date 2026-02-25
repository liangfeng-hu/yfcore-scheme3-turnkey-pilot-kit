#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheme-3 Sidecar Service (Reference / Pilot-Ready)

Endpoints:
  - GET  /health
  - GET  /v1/adjudicate   (header-mode PoC)
  - POST /v1/adjudicate   (json evidence)

Core semantics:
  - GateVectorLen fixed at 91 (Gates 1-89 are SEALED placeholders)
  - Gate90 + Gate91 are implemented here
  - LSE is a meta-gate (not consuming GateVector slot)
  - Fail-Closed: any failure -> WorldWriteback=0, CommitUnique=0
  - Allow world-write only when I_FLOW==0 AND OutLevel=="FOES"
  - Persist replayable AuditCards to data/audit.jsonl

Production requires trusted evidence injection; PoC uses placeholders for speed.
"""

import json
import time
import hashlib
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

GATE_VECTOR_LEN = 91

OUTLEVEL_RANK = {"ShadowOnly": 0, "EvidencePlan": 1, "FOES": 2}

TAU_EX_BY_RISK_CLASS = {
    "CoreSystem": 0.25,
    "HighValue": 0.35,
    "Normal": 0.65,
    "LowValue": 0.80,
}

REQUIRED_RECEIPT_ROOTS = [
    "canon_header",
    "ssot_hash",
    "pending_ledger_root",
    "audit_rec_root",
    "delta_s_log_root",
    "energy_trace_root",
    "zk_proof_root",
    "attestation_root",
    "verifier_refs",
]

AUDIT_VERSION = "AUDITCARD_V1"
LEDGER_VERSION = "LEDGER_V1"
EVIDENCE_VERSION = "EVIDENCE_V1"


def _log(msg: str) -> None:
    sys.stderr.write(msg.rstrip() + "\n")
    sys.stderr.flush()


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _now_ms() -> int:
    return int(time.time() * 1000)


def _canon_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _append_jsonl(path: Path, obj: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(_canon_json(obj) + "\n")


def _rank(out_level: str) -> int:
    return OUTLEVEL_RANK.get(out_level, 0)


def _out_level_leq(a: str, b: str) -> bool:
    return _rank(a) <= _rank(b)


def _first_nonempty(*vals, default=""):
    for v in vals:
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return default


def _bool_from_str(v: str, default: bool = False) -> bool:
    if v is None:
        return default
    x = str(v).strip().lower()
    if x in ("1", "true", "yes", "y", "ok"):
        return True
    if x in ("0", "false", "no", "n"):
        return False
    return default


def _float_from_str(v: str, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


class PersistentLedger:
    """
    Corruption-tolerant rolling ledger root.
    Any corruption => ledger_clean=False => world-write is fail-closed.
    """

    def __init__(self, ledger_path: Path):
        self.ledger_path = ledger_path
        _ensure_dir(self.ledger_path.parent)

        self.events = []
        self.ledger_root = _sha256(f"{LEDGER_VERSION}|INIT")
        self.corrupted = False
        self.corrupt_count = 0
        self._load()

    def _fold_event_hash(self, ev_hash: str) -> None:
        self.ledger_root = _sha256(self.ledger_root + "|" + ev_hash)

    def _load(self) -> None:
        if not self.ledger_path.exists():
            return
        try:
            lines = self.ledger_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception as e:
            self.corrupted = True
            self.corrupt_count += 1
            _log(f"[LEDGER] read failed: {e!r}")
            self._fold_event_hash(_sha256("CORRUPT|READ_FAILED"))
            return

        for idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                e = json.loads(line)
                self._fold_event_hash(_sha256(_canon_json(e)))
                self.events.append(e)
            except Exception:
                self.corrupted = True
                self.corrupt_count += 1
                synthetic = {
                    "ts_ms": 0,
                    "req_id": "CORRUPT",
                    "event": "CORRUPT_LINE",
                    "data": {"line_no": idx, "line_sha": _sha256(line)},
                }
                self._fold_event_hash(_sha256(_canon_json(synthetic)))
                self.events.append(synthetic)

        if self.corrupted:
            _log(f"[LEDGER] corrupted_lines={self.corrupt_count} (world-write disabled)")

    def append(self, req_id: str, event: str, data: dict):
        e = {"ts_ms": _now_ms(), "req_id": req_id, "event": event, "data": data or {}}
        _append_jsonl(self.ledger_path, e)
        self._fold_event_hash(_sha256(_canon_json(e)))
        self.events.append(e)


def _check_receipt_roots(receipt_roots: dict):
    missing = []
    for k in REQUIRED_RECEIPT_ROOTS:
        if not _first_nonempty(receipt_roots.get(k)):
            missing.append(k)
    return missing


def _eval_gate90(intent_group: dict, seed_group: dict):
    iia_ok = bool(intent_group.get("iia_ok", False))
    risk_class = _first_nonempty(intent_group.get("risk_class"), default="Normal")
    s_ex = _float_from_str(intent_group.get("s_ex"), 0.0)
    tau_ex = TAU_EX_BY_RISK_CLASS.get(risk_class, 0.50)
    seed_ok = bool(seed_group.get("seed_continuity_ok", False))

    if not iia_ok:
        return False, "RC_IIA_FAIL", {"risk_class": risk_class, "s_ex": s_ex, "tau_ex": tau_ex, "seed_ok": seed_ok}
    if s_ex > tau_ex:
        return False, "RC_EXTRACT_RISK", {"risk_class": risk_class, "s_ex": s_ex, "tau_ex": tau_ex, "seed_ok": seed_ok}
    if not seed_ok:
        return False, "RC_SEED_BREAK", {"risk_class": risk_class, "s_ex": s_ex, "tau_ex": tau_ex, "seed_ok": seed_ok}
    return True, "", {"risk_class": risk_class, "s_ex": s_ex, "tau_ex": tau_ex, "seed_ok": seed_ok}


def _eval_gate91(out_level: str, physical_group: dict):
    if _out_level_leq(out_level, "EvidencePlan"):
        return True, "", {"bypass": "OutLevel<=EvidencePlan"}

    zk_ok = bool(physical_group.get("zk_ok", False))
    attest_ok = bool(physical_group.get("attestation_ok", False))
    thermo_ok = bool(physical_group.get("thermo_ok", False))
    energy_ok = bool(physical_group.get("energy_ok", False))

    ok = zk_ok and attest_ok and thermo_ok and energy_ok
    if not ok:
        return False, "RC_THERMO_FORGERY", {"zk_ok": zk_ok, "attest_ok": attest_ok, "thermo_ok": thermo_ok, "energy_ok": energy_ok}
    return True, "", {"zk_ok": zk_ok, "attest_ok": attest_ok, "thermo_ok": thermo_ok, "energy_ok": energy_ok}


def _eval_lse(intent_complete: bool, time_complete: bool, phys_complete: bool, seed_ok: bool, out_level: str, gate91_ok: bool, lse_group: dict):
    trust_ok = bool(lse_group.get("trust_ok", True))
    budget_ok = bool(lse_group.get("budget_ok", True))

    complete_all = intent_complete and time_complete and phys_complete
    superpose_ok = seed_ok and (True if _out_level_leq(out_level, "EvidencePlan") else gate91_ok)

    if not trust_ok:
        return False, "RC_LSE_VIOLATION", {"sub_reason": "RC_INFRA_CORRUPTED", "complete_all": complete_all, "superpose_ok": superpose_ok}
    if not budget_ok:
        return False, "RC_LSE_VIOLATION", {"sub_reason": "RC_BUDGET_SELFPROTECT", "complete_all": complete_all, "superpose_ok": superpose_ok}
    if not complete_all:
        return False, "RC_LSE_VIOLATION", {"sub_reason": "RC_LAYER_INCOMPLETE", "complete_all": complete_all, "superpose_ok": superpose_ok}
    if not superpose_ok:
        return False, "RC_LSE_VIOLATION", {"sub_reason": "RC_SUPERPOSE_FAIL", "complete_all": complete_all, "superpose_ok": superpose_ok}
    return True, "", {"complete_all": complete_all, "superpose_ok": superpose_ok, "trust_ok": trust_ok, "budget_ok": budget_ok}


def _build_evidence_from_headers(headers: dict):
    out_level = _first_nonempty(headers.get("X-OutLevel"), default="FOES")

    intent = {
        "risk_class": _first_nonempty(headers.get("X-Risk-Class"), default="Normal"),
        "iia_ok": _bool_from_str(headers.get("X-IIA-OK"), default=True),
        "s_ex": _float_from_str(headers.get("X-S_EX"), default=0.10),
    }
    seed = {"seed_continuity_ok": _bool_from_str(headers.get("X-Seed-OK"), default=True)}
    physical = {
        "zk_ok": _bool_from_str(headers.get("X-ZK-OK"), default=True),
        "attestation_ok": _bool_from_str(headers.get("X-Attest-OK"), default=True),
        "thermo_ok": _bool_from_str(headers.get("X-Thermo-OK"), default=True),
        "energy_ok": _bool_from_str(headers.get("X-Energy-OK"), default=True),
    }
    lse = {
        "trust_ok": _bool_from_str(headers.get("X-Trust-OK"), default=True),
        "budget_ok": _bool_from_str(headers.get("X-Budget-OK"), default=True),
    }

    receipt_roots = {
        "canon_header": _first_nonempty(headers.get("X-Canon-Header"), default="CANONHEADER_POC"),
        "ssot_hash": _first_nonempty(headers.get("X-SSOT-Hash"), default=_sha256("SSOT_POC")),
        "pending_ledger_root": _first_nonempty(headers.get("X-PendingLedgerRoot"), default=_sha256("PEND_POC")),
        "audit_rec_root": _first_nonempty(headers.get("X-AuditRecRoot"), default=_sha256("AUDITREC_POC")),
        "delta_s_log_root": _first_nonempty(headers.get("X-DeltaSLogRoot"), default=_sha256("DELTAS_POC")),
        "energy_trace_root": _first_nonempty(headers.get("X-EnergyTraceRoot"), default=_sha256("ENERGY_POC")),
        "zk_proof_root": _first_nonempty(headers.get("X-ZKProofRoot"), default=_sha256("ZKPROOF_POC")),
        "attestation_root": _first_nonempty(headers.get("X-AttestationRoot"), default=_sha256("ATTEST_POC")),
        "verifier_refs": _first_nonempty(headers.get("X-VerifierRefs"), default="VERIFIERS_POC"),
    }

    return {
        "out_level": out_level,
        "intent_audit_group": intent,
        "seed_continuity": seed,
        "physical_proof": physical,
        "lse_support": lse,
        "receipt_roots": receipt_roots,
    }


class VInfinityHandler(BaseHTTPRequestHandler):
    server_version = "VInfinitySidecar/1.1"

    def _send_json(self, status: int, obj: dict):
        body = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self._send_json(200, {
                "ok": True,
                "service": "Scheme-3 sidecar",
                "ts_ms": _now_ms(),
                "gatevector_len": GATE_VECTOR_LEN,
                "ledger_corrupted": 1 if self.server.ledger.corrupted else 0,
                "ledger_corrupt_count": self.server.ledger.corrupt_count,
            })
        if path == "/v1/adjudicate":
            req_id = _first_nonempty(self.headers.get("X-Req-Id"), default="")[:64] or _sha256("req|" + str(_now_ms()))[:16]
            return self._handle_adjudicate(req_id, _build_evidence_from_headers(self.headers))
        return self._send_json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/v1/adjudicate":
            return self._send_json(404, {"error": "not found"})

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"

        req_id = _first_nonempty(self.headers.get("X-Req-Id"), default="")[:64]
        if not req_id:
            try:
                tmp = json.loads(raw.decode("utf-8"))
                req_id = _first_nonempty(tmp.get("req_id"), default="")[:64]
            except Exception:
                req_id = ""
        if not req_id:
            req_id = _sha256("req|" + str(_now_ms()))[:16]

        try:
            obj = json.loads(raw.decode("utf-8"))
            evidence = obj if isinstance(obj, dict) else _build_evidence_from_headers(self.headers)
        except Exception:
            evidence = _build_evidence_from_headers(self.headers)

        return self._handle_adjudicate(req_id, evidence)

    def _handle_adjudicate(self, req_id: str, evidence: dict):
        out_level = _first_nonempty(evidence.get("out_level"), default="FOES")
        intent_group = evidence.get("intent_audit_group") or {}
        seed_group = evidence.get("seed_continuity") or {}
        physical_group = evidence.get("physical_proof") or {}
        lse_group = evidence.get("lse_support") or {}
        receipt_roots = evidence.get("receipt_roots") or {}

        missing = _check_receipt_roots(receipt_roots)
        ledger_clean = not self.server.ledger.corrupted
        i_ledger_ok = (len(missing) == 0) and ledger_clean

        gate90_ok, gate90_rc, gate90_dbg = _eval_gate90(intent_group, seed_group)
        gate91_ok, gate91_rc, gate91_dbg = _eval_gate91(out_level, physical_group)

        intent_complete = ("iia_ok" in intent_group) and ("s_ex" in intent_group) and ("risk_class" in intent_group)
        time_complete = ("seed_continuity_ok" in seed_group)
        phys_complete = True if _out_level_leq(out_level, "EvidencePlan") else (
            "zk_ok" in physical_group and "attestation_ok" in physical_group and "thermo_ok" in physical_group and "energy_ok" in physical_group
        )

        seed_ok = bool(seed_group.get("seed_continuity_ok", False))
        lse_ok, lse_rc, lse_dbg = _eval_lse(intent_complete, time_complete, phys_complete, seed_ok, out_level, gate91_ok, lse_group)

        i_gatevector_ok = gate90_ok and gate91_ok
        i_flow_ok = i_ledger_ok and i_gatevector_ok and lse_ok

        enforced_out_level = out_level
        pendstop = False

        if (not ledger_clean) or (len(missing) != 0):
            enforced_out_level = "EvidencePlan"
        if not gate90_ok:
            enforced_out_level = "EvidencePlan"
            if gate90_rc == "RC_SEED_BREAK":
                pendstop = True
        if not gate91_ok:
            enforced_out_level = "ShadowOnly"
        if not lse_ok:
            enforced_out_level = "EvidencePlan"
            pendstop = True

        evidence_for_hash = {
            "out_level": out_level,
            "intent_audit_group": intent_group,
            "seed_continuity": seed_group,
            "physical_proof": physical_group,
            "lse_support": lse_group,
            "receipt_roots": receipt_roots,
        }
        evidence_canon = _canon_json(evidence_for_hash)
        evidence_hash = _sha256(f"{EVIDENCE_VERSION}|{evidence_canon}")

        self.server.ledger.append(req_id, "ADJUDICATE", {"evidence_hash": evidence_hash, "out_level": out_level})

        ssot_hash = _first_nonempty(receipt_roots.get("ssot_hash"), default=_sha256("SSOT_POC"))
        ledger_root = self.server.ledger.ledger_root
        seed_t = _sha256(_canon_json({"ssot_hash": ssot_hash, "ledger_root": ledger_root, "evidence_hash": evidence_hash}))

        allow_world = bool(i_flow_ok and (out_level == "FOES"))
        commit_unique = 1 if allow_world else 0
        world_writeback = 1 if allow_world else 0

        if not ledger_clean:
            reason_code = "RC_LEDGER_CORRUPTED"
        elif len(missing) != 0:
            reason_code = "RC_LEDGER_MISSING"
        elif not gate90_ok:
            reason_code = gate90_rc
        elif not gate91_ok:
            reason_code = gate91_rc
        elif not lse_ok:
            reason_code = lse_rc
        elif not allow_world:
            reason_code = "RC_FAIL_CLOSED"
        else:
            reason_code = "RC_SUCCESS"

        audit_receipt_hash = _sha256(
            f"{AUDIT_VERSION}|{ssot_hash}|{ledger_root}|{req_id}|{reason_code}|{enforced_out_level}|{commit_unique}|{world_writeback}|{evidence_hash}"
        )

        audit_card = {
            "version": AUDIT_VERSION,
            "ts_ms": _now_ms(),
            "req_id": req_id,
            "gatevector_len": GATE_VECTOR_LEN,
            "ssot_hash": ssot_hash,
            "canon_header": _first_nonempty(receipt_roots.get("canon_header"), default="CANONHEADER_POC"),
            "ledger_root": ledger_root,
            "seed_t": seed_t,
            "evidence_hash": evidence_hash,
            "evidence_canon": evidence_canon,
            "i_ledger_ok": 1 if i_ledger_ok else 0,
            "ledger_missing": missing,
            "gate90_ok": 1 if gate90_ok else 0,
            "gate91_ok": 1 if gate91_ok else 0,
            "lse_ok": 1 if lse_ok else 0,
            "i_flow": "0" if i_flow_ok else "+∞",
            "commit_unique": commit_unique,
            "world_writeback": world_writeback,
            "out_level": enforced_out_level,
            "reason_code": reason_code,
            "pendstop": 1 if pendstop else 0,
            "debug": {"gate90": gate90_dbg, "gate91": gate91_dbg, "lse": lse_dbg},
            "audit_receipt_hash": audit_receipt_hash,
        }

        _append_jsonl(self.server.audit_path, audit_card)

        payload = {
            "result": "ALLOW" if allow_world else "BLOCK",
            "i_flow": "0" if i_flow_ok else "+∞",
            "commit_unique": commit_unique,
            "world_writeback": world_writeback,
            "out_level": enforced_out_level,
            "reason_code": reason_code,
        }

        return self._send_json(200 if allow_world else 403, {"payload": payload, "audit_card": audit_card})


def main():
    repo = _repo_root()
    data_dir = repo / "data"
    _ensure_dir(data_dir)

    ledger_path = data_dir / "ledger.jsonl"
    audit_path = data_dir / "audit.jsonl"

    httpd = ThreadingHTTPServer(("0.0.0.0", 8787), VInfinityHandler)
    httpd.ledger = PersistentLedger(ledger_path)
    httpd.audit_path = audit_path

    print("Scheme-3 Sidecar Service (Reference)")
    print("Listen : http://127.0.0.1:8787")
    print("Health : http://127.0.0.1:8787/health")
    print("API    : http://127.0.0.1:8787/v1/adjudicate")
    print(f"Ledger : {ledger_path}")
    print(f"Audit  : {audit_path}")
    print("Press Ctrl+C to stop.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
